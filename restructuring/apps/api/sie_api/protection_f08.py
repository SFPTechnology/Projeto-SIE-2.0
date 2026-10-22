"""F08 radial protection studies. Explicit hypotheses; never normative release.

Fault inputs are complete equivalent impedances in ohm at the declared maximum
or minimum condition. No hidden factor 2, temperature correction or source
contribution. Curves, energy, RCD/SPD and coordination remain declared unless a
server registry explicitly verifies the exact characteristic and its domain.
"""
from decimal import Decimal, localcontext
from .protection_contracts_f08 import Study
from .conductor_f07 import analyze as conductor_analyze, fingerprint as conductor_fingerprint
from .topology import topology_hash
from .installation_service import digest

VERSION='SIE-F08-1.0'

def registry_hash():
    try:
        from . import protection_registry_f08 as registry
        return registry.catalog_hash()
    except ImportError:
        return 'NO_VERIFIED_CATALOG'

def fingerprint(study):
    study=Study.model_validate(study)
    return digest({'study':study.model_dump(mode='json'),'algorithm':VERSION,'catalog':registry_hash()})

def check(status,reason,**values):
    return {'status':status,'reason':reason,**values}

def decision(value,reason,**values):
    return check('ATENDE_ESTUDO' if value else 'REPROVADO',reason,**values)

def fault(scenario):
    with localcontext() as ctx:
        ctx.prec=200
        r=scenario.source_r_ohm+scenario.path_r_ohm
        x=scenario.source_x_ohm+scenario.path_x_ohm
        z=(r*r+x*x).sqrt()
        divisor=Decimal(3).sqrt() if scenario.fault_type=='THREE_PHASE' else Decimal(1)
        current=scenario.voltage_factor*scenario.voltage_v/(divisor*z)
    base={'id':scenario.id,'circuit_id':str(scenario.circuit_id),'segment_id':str(scenario.segment_id) if scenario.segment_id else None,
          'kind':scenario.kind,'location':scenario.location,'fault_type':scenario.fault_type,'z_ohm':str(z),'r_ohm':str(r),'x_ohm':str(x),
          'formula':'c Uff / (sqrt(3) |Z1|)' if scenario.fault_type=='THREE_PHASE' else 'c U / |Z_loop|',
          'input':scenario.model_dump(mode='json'),'sources_verified':False}
    if scenario.additional_contributions:
        return {**base,'status':'BLOQUEADO','current_a':None,'reason':'Contribuições adicionais exigem outro modelo; não ignoradas'}
    return {**base,'status':'CALCULADO_ESTUDO','current_a':str(current),'reason':'Equivalente radial declarado; hipóteses max/min não autenticadas'}

def _device(device):
    data=device.model_dump(mode='json'); data['source_status']='DECLARADA_NAO_VERIFICADA'
    if device.catalog_key:
        try:
            from . import protection_registry_f08 as registry
            product=registry.resolve(device.catalog_key)
        except (ImportError,ValueError,KeyError):
            data['registry_error']='Produto não disponível no catálogo verificado';return data
        data['catalog_product']=product
        for key in ('family','manufacturer','model','edition'):
            val=product.get(key)
            if val is not None:
                if data.get(key) is not None and data[key]!=val:
                    data['registry_error']='Identidade declarada contradiz catálogo: '+key
                data[key]=val
        # Never use a registry merely as a seal for contradictory client values.
        for key in ('nominal_current_a','i2_a','rated_voltage_v','breaking_capacity_a','breaking_standard','curve','poles'):
            val=product.get(key)
            if val is not None:
                if data.get(key) is not None and str(data[key])!=str(val):
                    data['registry_error']='Característica declarada contradiz catálogo: '+key
                data[key]=val
        data['source_status']='CATALOGO_SERVIDOR_RECORTE_LIMITADO'
    return data

def _number(device,key):
    v=device.get(key)
    return Decimal(str(v)) if v is not None else None

def overload(ib,iz,device,cp):
    nominal=_number(device,'nominal_current_a');i2=_number(device,'i2_a')
    if nominal is None or iz is None: return check('PENDENTE','In ou Iz aplicável ausente')
    basic=ib<=nominal<=iz
    if i2 is None:return check('PENDENTE' if basic else 'REPROVADO','I2 ausente; Ib≤In≤Iz não basta',ib_in_iz=basic)
    if i2<nominal:return check('BLOQUEADO','I2 menor que In é incoerente')
    restricted=(cp.overload_hours_year is not None and cp.overload_hours_year>100) or (cp.overload_hours_life is not None and cp.overload_hours_life>500)
    known=restricted or (cp.overload_hours_year is not None and cp.overload_hours_life is not None)
    limit=iz*(Decimal(1) if restricted else Decimal('1.45'))
    matches=basic and i2<=limit
    return check('REPROVADO' if not matches else ('ATENDE_ESTUDO' if known else 'PENDENTE'),
                 'Ib≤In≤Iz e I2≤Iz para duração restrita; demais I2≤1,45Iz',ib_a=str(ib),in_a=str(nominal),iz_a=str(iz),i2_a=str(i2),i2_limit_a=str(limit),duration_known=known)

def thermal(section,row,cp,current):
    t=cp.thermal
    if t is None:return check('PENDENTE','k, energia/tempo e condições térmicas não informados')
    if current is None or current.get('current_a') is None or t.device_id!=cp.device_id or t.fault_scenario_id!=current.get('id') or t.maximum_current_a is None or t.maximum_current_a<Decimal(current['current_a']):
        return check('PENDENTE','Energia/tempo exige vínculo ao dispositivo e cenário/faixa de falta avaliada')
    if t.material!=row['material'] or t.insulation!=row['insulation']:
        return check('BLOQUEADO','k declarado não corresponde ao material/isolação')
    if t.duration_s>5:return check('BLOQUEADO','Modelo adiabático limitado a5s')
    if t.duration_s<Decimal('.1') and t.energy_a2s is None and t.asymmetry_negligible is not True:
        return check('PENDENTE','Abaixo0,1s exige integral passante ou assimetria explicitamente desprezível')
    energy=t.energy_a2s if t.energy_a2s is not None else t.effective_current_a*t.effective_current_a*t.duration_s
    limit=t.k_a_sqrt_s_mm2*t.k_a_sqrt_s_mm2*section*section
    # An effective current/energy is a curve declaration, not Ikmax squared by default.
    return decision(energy<=limit,'Integral passante≤k²S², k e aplicabilidade declarados',energy_a2s=str(energy),limit_a2s=str(limit),duration_s=str(t.duration_s),evidence=t.evidence.model_dump(mode='json'),sources_verified=False)

def residual(cp,device,ib,maximum):
    r=cp.rcd
    if cp.rcd_required is False and r is None:return check('NAO_APLICAVEL','Dispensa DR declarada; aplicabilidade não homologada')
    if r is None:return check('PENDENTE','DR/requisito não informado')
    if cp.earthing=='TN_C':return check('REPROVADO','DR incompatível com trecho TN-C')
    flags=[r.all_live_conductors,r.pe_separated_upstream,cp.bonding_verified]
    upstream_in=_number(device,'nominal_current_a')
    if False in flags or r.nominal_current_a<ib or (upstream_in is not None and r.nominal_current_a<upstream_in):return check('REPROVADO','Ligação/equipotencialização ou corrente nominal DR inadequadas')
    if r.required_max_sensitivity_a is not None and r.sensitivity_a>r.required_max_sensitivity_a:
        return check('REPROVADO','Sensibilidade DR acima do limite declarado')
    if r.required_type is not None and r.required_type!=r.actual_type:
        return check('REPROVADO','Tipo DR difere da aplicação declarada; não presumir equivalência')
    if None in flags or r.required_type is None or r.required_max_sensitivity_a is None:
        return check('PENDENTE','Condições completas de seleção DR não demonstradas')
    if r.backup_device_id!=cp.device_id or r.backup_voltage_v!=_number(device,'rated_voltage_v'):
        return check('PENDENTE','DR exige associação de retaguarda identificada e tensão compatível')
    if maximum is None or maximum.get('current_a') is None or r.conditional_short_circuit_a is None or r.backup_protection_verified is None:
        return check('PENDENTE','DR exige corrente condicional de curto e retaguarda para falta máxima')
    if not r.backup_protection_verified or r.conditional_short_circuit_a<Decimal(maximum['current_a']):
        return check('REPROVADO','Suportabilidade condicional/retaguarda DR insuficiente')
    return check('ATENDE_ESTUDO','Comparações DR declaradas; coordenação/suportabilidade não homologadas',evidence=r.evidence.model_dump(mode='json'),sources_verified=False)

def surge(cp):
    s=cp.spd
    if cp.spd_required is False and s is None:return check('NAO_APLICAVEL','Dispensa DPS declarada; aplicabilidade não homologada')
    if s is None:return check('PENDENTE','DPS/requisito não informado')
    flags=[s.backup_coordinated,s.bonding_verified,s.connection_length_verified]
    ok=s.uc_v>=s.minimum_uc_v and s.up_v<=s.equipment_withstand_v and s.spd_type==s.required_type
    if not ok or False in flags:return check('REPROVADO','Uc/Up/tipo ou retaguarda/equipotencialização/conexões não atendem')
    if None in flags:return check('PENDENTE','Retaguarda/equipotencialização/conexões não demonstradas')
    if s.earthing is None or s.connection_scheme_declared is None or s.required_connection_scheme is None:
        return check('PENDENTE','Esquema aterramento/ligação DPS não definido')
    if s.connection_scheme_declared!=s.required_connection_scheme:return check('REPROVADO','Ligação DPS difere da requerida para aplicação')
    if s.earthing!=cp.earthing:return check('REPROVADO','DPS selecionado para outro esquema de aterramento')
    required=[]
    if s.spd_type in ('T1','T1_T2'):required.append((s.impulse_current_a,s.required_impulse_current_a,'Iimp'))
    if s.spd_type in ('T2','T1_T2'):required.extend([(s.nominal_discharge_a,s.required_nominal_discharge_a,'In'),(s.max_discharge_a,s.required_max_discharge_a,'Imax')])
    if s.spd_type=='T3':return check('PENDENTE','T3 requer ensaio de onda combinada e coordenação não modelados')
    if any(a is None or b is None for a,b,_ in required):return check('PENDENTE','Correntes de descarga/impulso e requisitos não informados')
    if s.spd_type in ('T2','T1_T2') and s.max_discharge_a < s.nominal_discharge_a:
        return check('BLOQUEADO','Imax do DPS inferior a In; características incoerentes')
    if any(a<b for a,b,_ in required):return check('REPROVADO','Correntes de descarga/impulso insuficientes')
    return check('ATENDE_ESTUDO','Uc/Up/tipo/correntes/esquema e coordenação declarados; fontes não homologadas',evidence=s.evidence.model_dump(mode='json'),complete_selection=False)

def shock(cp,minimum,circuit):
    if cp.earthing=='IT':return check('PENDENTE','IT exige primeira/segunda falta, DSI e topologia próprios; sem aprovação genérica')
    if cp.bonding_verified is False:return check('REPROVADO','Equipotencialização declarada não atendida')
    if cp.earthing=='TT':
        if cp.rcd is None:return check('PENDENTE','TT exige DR; sobrecorrente não substitui seccionamento contra choque')
        if cp.earth_resistance_ohm is None or cp.touch_limit_v is None:
            return check('PENDENTE','TT exige RA e UL aplicável')
        touch=cp.earth_resistance_ohm*cp.rcd.sensitivity_a
        if touch>cp.touch_limit_v:return check('REPROVADO','RA×IΔn>UL',touch_v=str(touch))
        if cp.rcd.max_time_s is None or cp.disconnection_limit_s is None or cp.disconnection_evidence is None or cp.bonding_verified is None:
            return check('PENDENTE','RA×IΔn≤UL não demonstra sozinho tempo/condições',touch_v=str(touch))
        return decision(cp.rcd.max_time_s<=cp.disconnection_limit_s,'TT: RA×IΔn≤UL e tempo declarado; DR deve passar seleção',touch_v=str(touch))
    if minimum is None or minimum.get('current_a') is None or cp.trip is None or cp.disconnection_limit_s is None or cp.disconnection_evidence is None:
        return check('PENDENTE','TN exige falta mínima fase-PE, curva e limite de tempo aplicável')
    if minimum['fault_type']!='PHASE_PE':return check('BLOQUEADO','Choque TN exige corrente de laço fase-PE')
    if cp.trip.voltage_v!=circuit.voltage.value:return check('BLOQUEADO','Curva declarada para outra tensão')
    if cp.bonding_verified is None:return check('PENDENTE','Equipotencialização não demonstrada')
    if cp.trip.maximum_current_a is None:return check('PENDENTE','Curva exige limite superior da faixa de corrente aplicável')
    if Decimal(minimum['current_a'])>cp.trip.maximum_current_a:return check('BLOQUEADO','Ikmin fora da faixa superior da curva; sem extrapolação')
    return decision(Decimal(minimum['current_a'])>=cp.trip.at_current_a and cp.trip.max_time_s<=cp.disconnection_limit_s,
                    'Ikmin≥Ia e tempo de curva≤limite declarado; condições de curva não autenticadas',minimum_a=minimum['current_a'],ia_a=str(cp.trip.at_current_a),time_s=str(cp.trip.max_time_s))

def _analyze(study):
    inst=study.conductor_study.topology.installation
    f07=conductor_analyze(study.conductor_study)
    faults=[fault(x) for x in study.fault_scenarios]; by_fault={x['id']:x for x in faults}
    boards_by_id={b.id:b for b in inst.boards}; incoming={c.downstream_board_id:c for c in inst.circuits if c.kind=='FEEDER'}; supplies={s.id:s for s in inst.supplies}
    for scenario,result in zip(study.fault_scenarios,faults):
        circuit=next(c for c in inst.circuits if c.id==scenario.circuit_id); board=boards_by_id[circuit.board_id]
        while board.supply_id is None: board=boards_by_id[incoming[board.id].board_id]
        supply=supplies[board.supply_id]; voltage=supply.voltage_fn if scenario.source_voltage_basis=='FN' else supply.voltage_ff
        if voltage is None:result.update(status='BLOQUEADO',current_a=None,reason='Tensão nominal da base FN/FF não cadastrada na fonte; sem inferência')
    devices={d.id:_device(d) for d in study.devices}
    circuits={c.id:c for c in inst.circuits}; output={}
    for cid,c in circuits.items():
        cp=study.circuits.get(cid); rows=[r for r in f07['segments'] if r['circuit_id']==str(cid)]
        out={'circuit_id':str(cid),'device_id':str(c.device_id),'board_id':str(c.board_id),'segments':[],'checks':{}}
        output[str(cid)]=out
        if cp is None:
            out['checks']['protection']=check('PENDENTE','Proteção do circuito não parametrizada');out['criteria']=out['checks'];continue
        dev=devices[cp.device_id];out['device']=dev
        maximum=by_fault.get(cp.fault_max_id);minimum=by_fault.get(cp.fault_min_id)
        if dev.get('catalog_product'):
            product=dev['catalog_product']; temperatures={seg.conditions.ambient_temperature.value for seg in inst.segments if any(str(seg.id)==r['segment_id'] for r in rows)}
            temp=product.get('reference_temperature_c')
            freqs={seg.impedance.frequency_hz for seg in inst.segments if seg.impedance and any(str(seg.id)==r['segment_id'] for r in rows)}
            if (voltage_catalog:=_number(dev,'rated_voltage_v')) is not None and voltage_catalog!=c.voltage.value:
                dev['registry_error']='Produto fora da tensão vinculada no catálogo'
            if temp is not None and (not temperatures or temperatures!={Decimal(str(temp))}):
                dev['registry_error']='Produto fora da temperatura de referência; falta derating'
            allowed_freqs={Decimal(str(x)) for x in product.get('frequency_hz',[])}
            if allowed_freqs and (not freqs or not freqs.issubset(allowed_freqs)):
                dev['registry_error']='Frequência fora do catálogo ou não declarada'
            required_poles=3 if c.phases==3 else (2 if c.voltage.basis=='FF' else 1)
            if dev.get('poles') is not None and int(dev['poles'])!=required_poles:
                dev['registry_error']='Número de pólos incompatível com conexão'
        if dev.get('registry_error'):out['checks']['catalog']=check('BLOQUEADO',dev['registry_error'])
        else:out['checks']['catalog']=check('ATENDE_ESTUDO' if cp.device_id in devices else 'PENDENTE','Origem das características registrada',source_status=dev['source_status'])
        nominal=_number(dev,'nominal_current_a')
        topo_dev=next(d for d in inst.devices if d.id==cp.device_id)
        if nominal is not None and topo_dev.nominal_current is not None and nominal!=topo_dev.nominal_current.value:
            out['checks']['device_identity']=check('BLOQUEADO','In F08 contradiz In cadastrado na topologia')
        for row in rows:
            cap=row['criteria']['capacity']; iz=Decimal(cap['iz_a']) if 'iz_a' in cap and cap['status']!='BLOQUEADO' else None
            checks={'overload':overload(c.design_current.value,iz,dev,cp),'thermal':thermal(Decimal(row['section_mm2']),row,cp,maximum)}
            # k must also cover actual initial conductor temperature, not only insulation label.
            seg=next(s for s in inst.segments if str(s.id)==row['segment_id'])
            if cp.thermal and seg.conditions.conductor_temperature and cp.thermal.initial_temperature_c<seg.conditions.conductor_temperature.value:
                checks['thermal']=check('BLOQUEADO','Temperatura inicial usada para k inferior à do condutor')
            ci=study.conductor_study.circuits.get(cid)
            for kind,section,td,fault_type in [('pe',ci.pe_section_mm2 if ci else None,cp.pe_thermal,'PHASE_PE'),('neutral',ci.neutral_section_mm2 if ci else None,cp.neutral_thermal,'PHASE_NEUTRAL')]:
                if kind=='neutral' and ci is not None and not ci.neutral_required:
                    checks['thermal_'+kind]=check('NAO_APLICAVEL','Circuito não contém neutro')
                elif td is None or section is None:
                    checks['thermal_'+kind]=check('PENDENTE','Seção e curva térmica próprias do condutor retorno não informadas')
                else:
                    mf=next((f for f in faults if f['circuit_id']==str(cid) and f['kind']=='MAX' and f['fault_type']==fault_type and f['id']==td.fault_scenario_id),None)
                    checks['thermal_'+kind]=thermal(section,row,cp.model_copy(update={'thermal':td}),mf)
                    if seg.conditions.conductor_temperature and td.initial_temperature_c<seg.conditions.conductor_temperature.value:
                        checks['thermal_'+kind]=check('BLOQUEADO','k retorno usa temperatura inicial inferior à do recorte de condutor')
            out['segments'].append({'segment_id':row['segment_id'],'run_id':row['run_id'],'section_mm2':row['section_mm2'],'checks':checks})
        f07_statuses=[v['status'] for r in rows for v in r['criteria'].values()]+[f07['circuits'][str(cid)]['voltage_total']['status']]
        conductor_status='REPROVADO' if 'REPROVADO' in f07_statuses else ('BLOQUEADO' if 'BLOQUEADO' in f07_statuses else ('ATENDE_ESTUDO' if rows and all(v in ('ATENDE_ESTUDO','ATENDE_LOTE_LIMITADO','NAO_APLICAVEL','CALCULADO_ESTUDO') for v in f07_statuses) else 'PENDENTE'))
        out['checks']['conductor_state']=check(conductor_status,'Estado dos critérios F07 herdado; proteção não supera condutor inválido')
        if not rows:out['checks']['conductors']=check('PENDENTE','Circuito sem trecho de condutor avaliado')
        breaking=_number(dev,'breaking_capacity_a');voltage=_number(dev,'rated_voltage_v')
        if maximum is None or maximum['current_a'] is None or breaking is None or voltage is None or dev.get('breaking_standard') is None:
            out['checks']['interruption']=check('PENDENTE','Falta máxima, capacidade/tensão/norma de interrupção ausentes')
        elif maximum['location']!='DEVICE':
            out['checks']['interruption']=check('PENDENTE','Falta máxima no fim do trecho não demonstra interrupção no dispositivo')
        elif voltage!=c.voltage.value:
            out['checks']['interruption']=check('BLOQUEADO','Capacidade não extrapolada a outra tensão')
        else:out['checks']['interruption']=decision(breaking>=Decimal(maximum['current_a']),'Capacidade direta≥Ikmax; retaguarda não presumida',breaking_capacity_a=str(breaking),fault_a=maximum['current_a'],standard=dev['breaking_standard'])
        if maximum and minimum and maximum['current_a'] and minimum['current_a'] and Decimal(maximum['current_a'])<Decimal(minimum['current_a']):
            out['checks']['fault_order']=check('BLOQUEADO','Icc máxima menor que mínima; cenários incoerentes')
        out['checks']['shock']=shock(cp,minimum,c)
        out['checks']['rcd']=residual(cp,dev,c.design_current.value,maximum)
        out['checks']['spd']=surge(cp)
        out['criteria']=out['checks']
        out['checks']['source_authentication']=check('PENDENTE','Curvas, energia, condições de fonte e estudos declarados exigem revisão técnica; não homologados')
    coordination=[]
    for pair in study.coordination:
        down=output[str(pair.downstream_circuit_id)];up=circuits[pair.upstream_circuit_id]; dc=circuits[pair.downstream_circuit_id]
        # Prove upstream/downstream against F07 graph, not labels/client order.
        chain=f07['circuits'][str(dc.id)]['upstream_circuit_ids']
        if str(up.id) not in chain[:-1]: result=check('BLOQUEADO','Circuitos não formam par montante/jusante no grafo')
        elif pair.voltage_v!=dc.voltage.value: result=check('BLOQUEADO','Estudo de seletividade para outra tensão')
        else:
            cp=study.circuits.get(dc.id);mx=by_fault.get(cp.fault_max_id) if cp else None
            if pair.evidence is None or (pair.selectivity_limit_a is None and not pair.total_selectivity) or mx is None or mx['current_a'] is None:
                result=check('PENDENTE','Dados específicos do par e falta máxima ausentes; In não prova seletividade')
            elif pair.selectivity_limit_a is not None and Decimal(mx['current_a'])>pair.selectivity_limit_a:
                result=check('REPROVADO','Falta excede limite parcial declarado',classification='PARCIAL',limit_a=str(pair.selectivity_limit_a))
            else:result=check('PENDENTE','Tabela/estudo declarado deve ser autenticado para estes produtos, tensão e edição',classification='TOTAL_DECLARADA' if pair.total_selectivity else 'PARCIAL_DECLARADA',evidence=pair.evidence.model_dump(mode='json'))
        if pair.catalog_key:
            try:
                from . import protection_registry_f08 as registry
                verified=registry.resolve_pair(pair.catalog_key)
                updev=devices.get(pair.upstream_device_id,{});downdev=devices.get(pair.downstream_device_id,{})
                match=True
                for actual,expected in ((updev,verified['upstream']),(downdev,verified['downstream'])):
                    for key in ('family','manufacturer','curve','poles','nominal_current_a'):
                        if str(actual.get(key))!=str(expected.get(key)):match=False
                    if actual.get('model')!='iC60N' and not (actual.get('model')=='A9F74116' and expected.get('nominal_current_a')=='16' and expected.get('poles')==1):match=False
                cp=study.circuits.get(dc.id);mx=by_fault.get(cp.fault_max_id) if cp else None
                identity_errors = (updev.get('registry_error') or downdev.get('registry_error') or
                    any(output[str(c.id)]['checks'].get('device_identity', {}).get('status') == 'BLOQUEADO'
                        for c in (up, dc)))
                connection_matches = all(c.phases == 1 and c.voltage.basis == 'FN' for c in (up, dc))
                if str(up.id) not in chain[:-1] or not match or identity_errors or not connection_matches or pair.voltage_v!=Decimal(verified['voltage_v']) or dc.voltage.value!=pair.voltage_v or up.voltage.value!=pair.voltage_v:
                    result=check('BLOQUEADO','Par de catálogo diverge identidade/tensão/caminho real')
                elif mx is None or mx['current_a'] is None or mx['location'] != 'DEVICE':result=check('PENDENTE','Falta máxima no dispositivo jusante necessária para limite do par')
                else:result=decision(Decimal(mx['current_a'])<=Decimal(verified['selectivity_limit_a']),'Seletividade parcial do par oficial até limite; não prova retaguarda/energia',classification='PARTIAL_BELOW_LIMIT',limit_a=verified['selectivity_limit_a'],source_verified=True,evidence=verified['evidence'])
            except (ImportError,ValueError,KeyError):result=check('BLOQUEADO','Par não disponível no catálogo verificado')
        coordination.append({'upstream_circuit_id':str(pair.upstream_circuit_id),'downstream_circuit_id':str(pair.downstream_circuit_id),**result})
    # Every actual feeder/terminal pair needs a result even if user omitted studies.
    present={(p['upstream_circuit_id'],p['downstream_circuit_id']) for p in coordination}
    for cid,row in f07['circuits'].items():
        chain=row['upstream_circuit_ids']
        if len(chain)>1 and (chain[-2],cid) not in present:
            coordination.append({'upstream_circuit_id':chain[-2],'downstream_circuit_id':cid,**check('PENDENTE','Par adjacente sem estudo de fabricante')})
    boards=[]
    for b in inst.boards:
        currents={p:Decimal(0) for p in ('L1','L2','L3')};pending=[]
        for c in inst.circuits:
            if c.board_id!=b.id:continue
            ci=study.conductor_study.circuits.get(c.id)
            if ci is None or ci.phase_set is None:pending.append(str(c.id));continue
            for phase in ci.phase_set.split('_'):
                if phase in currents:currents[phase]+=c.design_current.value
        fixed={p:Decimal(0) for p in ('L1','L2','L3')};movable=[]
        board=boards_by_id[b.id];allowed={'L1','L2','L3'}
        while board.supply_id is None:
            feeder=incoming[board.id];fi=study.conductor_study.circuits.get(feeder.id)
            allowed.intersection_update(set(fi.phase_set.split('_')) if fi and fi.phase_set else set())
            board=boards_by_id[feeder.board_id]
        supply=supplies[board.supply_id]
        if supply.phases==1:allowed.intersection_update({'L1'})
        for c in inst.circuits:
            if c.board_id!=b.id:continue
            ci=study.conductor_study.circuits.get(c.id)
            if ci is None or ci.phase_set is None:continue
            if c.phases==1 and c.voltage.basis=='FN':movable.append(c)
            else:
                for phase in ci.phase_set.split('_'):
                    if phase in fixed:fixed[phase]+=c.design_current.value
        proposed=dict(fixed);assignments=[]
        for c in sorted(movable,key=lambda x:(-x.design_current.value,str(x.id))):
            if not allowed:break
            phase=min(allowed,key=lambda p:(proposed[p],p));proposed[phase]+=c.design_current.value
            assignments.append({'circuit_id':str(c.id),'proposed_phase_set':phase+'_N','current_phase_set':study.conductor_study.circuits[c.id].phase_set})
        previous_spread=max(currents.values())-min(currents.values());new_spread=max(proposed.values())-min(proposed.values())
        acceptable=not pending and len(assignments)==len(movable) and new_spread<=previous_spread
        proposal={'status':'PROPOSTA_ESTUDO' if acceptable else 'PENDENTE_OU_SEM_MELHORIA','assignments':assignments if acceptable else [],'phase_currents_a':{k:str(v) for k,v in proposed.items()} if acceptable else None,'spread_a':str(new_spread) if acceptable else None,'applied':False,'requires_full_recalculation':True,'available_phases':sorted(allowed)}
        boards.append({'board_id':str(b.id),'circuit_ids':[str(c.id) for c in inst.circuits if c.board_id==b.id],
                       'phase_current_magnitudes_a':{k:str(v) for k,v in currents.items()},
                       'balance_status':'PENDENTE' if pending else 'CALCULADO_ESTUDO',
                       'pending_circuit_ids':pending,'spread_a':str(max(currents.values())-min(currents.values())),
                       'method':'Soma conservadora de módulos por fase; não fasorial, sem diversidade ou realocação automática',
                       'designer_decision_preserved':True,'proposal':proposal})
    selection={}
    for cid,candidates in study.candidate_device_ids.items():
        c=circuits[cid];steps=[]; chosen=None; terminated='NO_SOLUTION'
        iz_values=[Decimal(r['criteria']['capacity']['iz_a']) for r in f07['segments'] if r['circuit_id']==str(cid) and 'iz_a' in r['criteria']['capacity']]
        iz=min(iz_values) if iz_values else None
        for index,did in enumerate(candidates):
            if index>=study.max_iterations:terminated='ITERATION_LIMIT';break
            d=devices[did];n=_number(d,'nominal_current_a');i2=_number(d,'i2_a')
            cp=study.circuits.get(cid)
            overload_result=overload(c.design_current.value,iz,d,cp) if cp else check('PENDENTE','Dados sobrecarga ausentes')
            ok=overload_result['status']=='ATENDE_ESTUDO' and not d.get('registry_error') and d['family'] in ('MCB','FUSE')
            steps.append({'device_id':str(did),'basic_overload_candidate':ok})
            if ok:chosen=str(did);terminated='CANDIDATE_REQUIRES_FULL_RECALCULATION';break
        selection[str(cid)]={'status':terminated,'candidate_device_id':chosen,'iterations':len(steps),'steps':steps,
                              'applied':False,'converged':False,'reason':'Busca finita consultiva; trocar dispositivo/seção exige novo estudo completo, sem modificar topologia'}
    variants=[]
    def physical_conductor(cs):
        ins=cs.topology.installation
        return digest({'runs':[r.model_dump(mode='json') for r in ins.cable_runs],'segments':[r.model_dump(mode='json') for r in ins.segments],'supplies':[r.model_dump(mode='json') for r in ins.supplies]})
    def fault_physical(fs):
        return sorted([(str(f.circuit_id),f.kind,f.fault_type,str(f.segment_id),f.location,str(f.voltage_v),str(f.voltage_factor),str(f.source_r_ohm),str(f.source_x_ohm),str(f.path_r_ohm),str(f.path_x_ohm)) for f in fs])
    converged_variant=None
    for index,variant in enumerate(study.selection_variants):
        if index>=study.max_iterations:
            variants.append({'status':'ITERATION_LIMIT','iterations':index});break
        if physical_conductor(variant.conductor_study)!=physical_conductor(study.conductor_study) and fault_physical(variant.fault_scenarios)==fault_physical(study.fault_scenarios):
            variants.append({'id':str(variant.id),'status':'BLOQUEADO','reason':'Condutor alterado exige novos cenários/impedâncias; entradas de falta antigas não reutilizadas'});continue
        result=_analyze(variant)
        if result['computational_state']=='ATENDE_ESTUDO':converged_variant=str(variant.id)
        variants.append({'id':str(variant.id),'status':result['status'],'input_sha256':result['input_sha256'],'conductor_input_sha256':result['conductor_input_sha256'],'circuits':result['circuits'],'fault_scenarios':result['fault_scenarios']})
        if converged_variant is not None:break
    selection['variants']={'status':'CONVERGED_STUDY' if converged_variant is not None else ('ITERATION_LIMIT' if len(study.selection_variants)>study.max_iterations else ('EVALUATED_FINITE_SET' if variants else 'NOT_REQUESTED')),'iterations':min(len(variants),study.max_iterations),'evaluations':variants,'applied':False,'converged':converged_variant is not None,'converged_variant_id':converged_variant,'reason':'Cada variante reexecuta F07 e todas proteções; pendência documental não convertida em solução'}
    statuses=[v['status'] for row in output.values() for v in row['checks'].values()]+[v['status'] for row in output.values() for seg in row['segments'] for v in seg['checks'].values()]+[v['status'] for v in coordination]
    computational_statuses=[v['status'] for row in output.values() for key,v in row['checks'].items() if key!='source_authentication']+[v['status'] for row in output.values() for seg in row['segments'] for v in seg['checks'].values()]+[v['status'] for v in coordination]
    computational_ok=bool(computational_statuses) and all(s in ('ATENDE_ESTUDO','NAO_APLICAVEL') for s in computational_statuses) and all(f['status']=='CALCULADO_ESTUDO' for f in faults)
    failed='REPROVADO' in statuses; blocked='BLOQUEADO' in statuses or any(f['status']=='BLOQUEADO' for f in faults)
    return {'algorithm_version':VERSION,'input_sha256':fingerprint(study),'input_snapshot':study.model_dump(mode='json'),
            'project_revision':inst.project.revision,'topology_sha256':topology_hash(study.conductor_study.topology),
            'conductor_input_sha256':conductor_fingerprint(study.conductor_study),'registry_sha256':registry_hash(),
            'computational_state':'ATENDE_ESTUDO' if computational_ok else 'PENDENTE_OU_FALHO','status':'BLOQUEADO' if blocked else ('REPROVADO' if failed else 'PENDENTE'),
            'circuits':output,'fault_scenarios':faults,'coordination':coordination,'boards':boards,'selection':selection,
            'normative_conformity_verified':False,'authoritative_for_sizing':False,'professional_approval':False,
            'mandatory_pending':['Aplicabilidade das fontes, fabricante e ensaios não homologados','Coordenação não aprovada por In ou declarações','Seleção consultiva requer recálculo completo e decisão do projetista'],
            'precision':{'significant_digits':200,'rounding_for_decisions':'NONE','units':['V','A','ohm','mm2','s','A2s']}}

def analyze(study):
    study=Study.model_validate(study)
    with localcontext() as ctx:
        ctx.prec=200
        return _analyze(study)
