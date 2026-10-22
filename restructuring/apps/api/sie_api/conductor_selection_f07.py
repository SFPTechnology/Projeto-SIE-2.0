"""Source-linked finite F07 selection over the complete topology.

Policy: first satisfy ampacity/minima, then conservatively grow every available
conductor on a failed voltage path (including homogeneous group companions).
This terminates at the finite catalog maximum and does not claim economic optimum.
The selected sizes are proposals; canonical topology is never silently overwritten.
"""
from copy import deepcopy
from datetime import date
from decimal import Decimal, localcontext
from typing import Literal
from uuid import UUID
from pydantic import Field, model_validator
from .domain.installation import DomainModel, Positive, NonNegative, Installation
from .topology import Topology, topology_hash, load_document
from .installation_service import digest,create_snapshot
from .conductor_f07 import Study, Evidence, analyze, capacity, criterion
from . import conductor_registry_f07 as registry
from . import cell_bindings

VERSION='SIE-F07-SELECTION-1.0'
POLICY='MIN_LOCAL_THEN_GROW_FAILED_PATHS_AND_HOMOGENEOUS_GROUPS_V1'

class CircuitSelection(DomainModel):
    use: Literal['LIGHTING','POWER']
    power_factor: Positive=Field(le=1)
    phase_set: Literal['L1_N','L2_N','L3_N','L1_L2','L2_L3','L3_L1']
    neutral_required: bool=Field(strict=True)
    pe_layout: Literal['SAME_CLOSED_CONDUIT','SEPARATE_MECHANICALLY_PROTECTED','SEPARATE_UNPROTECTED']
    regime: Literal['SINUSOIDAL_STEADY_NO_RELEVANT_HARMONICS']

class SegmentSelection(DomainModel):
    product: Literal['PRYSMIAN_SUPERASTIC']
    arrangement: Literal['TWO_LOADED_TOUCHING']
    installation_number: int=Field(strict=True)
    infrared: bool=Field(strict=True)

class HomogeneousGroup(DomainModel):
    segment_ids: list[UUID]=Field(min_length=2,max_length=3)
    @model_validator(mode='after')
    def unique(self):
        if len(set(self.segment_ids))!=len(self.segment_ids): raise ValueError('Trecho duplicado no grupo')
        return self

class Selection(DomainModel):
    schema_version: Literal['SIE_F07_SELECTION_V1']='SIE_F07_SELECTION_V1'
    id: UUID
    topology: Topology
    circuits: dict[UUID,CircuitSelection]=Field(default_factory=dict)
    segments: dict[UUID,SegmentSelection]=Field(default_factory=dict)
    groups: dict[str,HomogeneousGroup]=Field(default_factory=dict,max_length=256)
    catalog_version: str=Field(min_length=1,max_length=100)
    application: Literal['ORDINARY_FIXED_INSTALLATION_NO_SPECIAL_REQUIREMENTS']
    normative_basis: Literal['ABNT_NBR_5410_2004_CORRIGIDA_2008']
    reference_date: date
    origin: Literal['LV_UTILITY_POINT_OF_DELIVERY']
    origin_drop_percent: NonNegative
    origin_evidence: Evidence

    @model_validator(mode='after')
    def integrity(self):
        inst=self.topology.installation
        if len(inst.circuits)>64 or len(inst.segments)>256:
            raise ValueError('Seleção F07 limitada a64circuitos e256trechos por análise')
        if not set(self.circuits).issubset({c.id for c in inst.circuits}): raise ValueError('Circuito de seleção órfão')
        if not set(self.segments).issubset({s.id for s in inst.segments}): raise ValueError('Trecho de seleção órfão')
        # Reuse the exact numeric bounds of Study without changing historical F02.
        probe={'id':self.id,'topology':self.topology,'origin_drop_percent':self.origin_drop_percent,
               'origin_evidence':self.origin_evidence}
        Study.model_validate(probe)
        for ci in self.circuits.values():
            v=ci.power_factor
            if len(v.as_tuple().digits)>30 or abs(v.as_tuple().exponent)>30:
                raise ValueError('Fator de potência fora da precisão suportada')
        used=set();segments={s.id:s for s in inst.segments};runs={r.id:r for r in inst.cable_runs}
        for key,group in self.groups.items():
            if not key.strip() or len(key)>100: raise ValueError('Identificação de grupo inválida')
            if any(sid not in segments for sid in group.segment_ids): raise ValueError('Trecho de grupo órfão')
            if used.intersection(group.segment_ids): raise ValueError('Trecho pertence a mais de um grupo')
            used.update(group.segment_ids)
            cids=[runs[segments[sid].cable_run_id].circuit_id for sid in group.segment_ids]
            if len(set(cids))!=len(cids): raise ValueError('Grupo deve conter circuitos distintos, sem paralelo implícito')
        return self


def fingerprint(request):
    raw=request.model_dump(mode='json');raw.pop('id');raw['topology']=topology_hash(request.topology)
    return digest({'request':raw,'catalog_sha256':registry.catalog_hash(),'algorithm':VERSION,'policy':POLICY})


def _problem(code,message,entity=None):
    return {'code':code,'message':message,'entity_id':str(entity) if entity else None}


def inspect_scope(request,catalog):
    """Only explicit supported physical and electrical conditions can enter selection."""
    problems=[];inst=request.topology.installation
    if request.catalog_version!=catalog['catalog_version']:
        problems.append(_problem('CATALOG_VERSION','Versão de catálogo desconhecida'))
    if not date(2020,9,23)<=request.reference_date<=date.fromisoformat(catalog['source']['verified_on']):
        problems.append(_problem('REFERENCE_DATE','Data fora do recorte documental conferido (2020-09-23 a2026-10-22)'))
    if not inst.circuits: problems.append(_problem('EMPTY_INSTALLATION','Não há circuitos para selecionar'))
    circuits={c.id:c for c in inst.circuits};runs={r.id:r for r in inst.cable_runs}
    segments={s.id:s for s in inst.segments};group_for={sid:key for key,g in request.groups.items() for sid in g.segment_ids}
    for source in inst.supplies:
        if source.frequency_hz!=Decimal(catalog['scope']['frequency_hz']):
            problems.append(_problem('FREQUENCY','Catálogo Rca/XL cobre somente60Hz',source.id))
        if source.voltage_fn is not None and source.voltage_fn.value>450:
            problems.append(_problem('INSULATION_UO','Tensão FN excede Uo450V do Superastic450/750V',source.id))
        if source.voltage_ff is not None and (source.voltage_ff.value>750 or (source.voltage_ff.value>450 and source.voltage_fn is None)):
            problems.append(_problem('INSULATION_U','Tensão FF excede750V ou tensão para terra não foi comprovada para FF>450V',source.id))
        if source.earthing_system not in ('TT','TN-S'):
            problems.append(_problem('EARTHING','Seleção N/PE separados cobre TT ou TN-S; PEN/outros fora do recorte',source.id))
    for cid,circuit in circuits.items():
        ci=request.circuits.get(cid)
        if ci is None:
            problems.append(_problem('CIRCUIT_DATA','Uso/fases/cosφ/N/PE/regime não declarados',cid));continue
        if circuit.phases!=1:
            problems.append(_problem('PHASES','Catálogo de seleção cobre dois condutores carregados; fórmula tri permanece disponível no estudo',cid))
        allowed={'L1_N','L2_N','L3_N'} if circuit.voltage.basis=='FN' else {'L1_L2','L2_L3','L3_L1'}
        if ci.phase_set not in allowed or ci.neutral_required!=(circuit.voltage.basis=='FN'):
            problems.append(_problem('CONNECTION','Fases/neutro divergem da conexão explícita FN/FF',cid))
        rating=Decimal('450') if circuit.voltage.basis=='FN' else Decimal('750')
        if not Decimal(catalog['scope']['min_voltage_v'])<=circuit.voltage.value<=rating:
            problems.append(_problem('VOLTAGE_RANGE','Tensão fora do recorte: mínimo50V, máximoFN450V/FF750V do produto',cid))
        rs=[r for r in inst.cable_runs if r.circuit_id==cid]
        if len(rs)!=1: problems.append(_problem('ALTERNATIVE_RUNS','Seleção exige percurso único por circuito; paralelos/alternativas não inferidos',cid))
    for run in inst.cable_runs:
        if run.material!='Cu' or run.insulation!='PVC':
            problems.append(_problem('MATERIAL_INSULATION','Recorte cobre Cu/PVC/Superastic',run.id))
    for sid,seg in segments.items():
        si=request.segments.get(sid);cond=seg.conditions;physical=request.topology.segment_details.get(sid)
        if si is None:
            problems.append(_problem('SEGMENT_DATA','Produto/arranjo/método/infra-vermelho não declarados',sid));continue
        if si.installation_number not in catalog['scope']['installation_numbers'] or cond.installation_method!='B1':
            problems.append(_problem('METHOD','Recorte B1 métodos3/5/7',sid))
        if cond.medium!='AIR' or cond.additional_conditions or cond.solar_exposure or si.infrared:
            problems.append(_problem('ENVIRONMENT','Meio/influências adicionais sem regra do recorte',sid))
        if cond.ambient_temperature.value not in [Decimal(x) for x in catalog['corrections']['temperature']]:
            problems.append(_problem('TEMPERATURE','Temperatura ambiente sem célula vinculada30/40°C',sid))
        if cond.conductor_temperature is None or cond.conductor_temperature.value!=70:
            problems.append(_problem('CONDUCTOR_TEMPERATURE','Rca de catálogo é para70°C; sem conversão térmica implícita',sid))
        if physical is None or physical.containment_material!='PVC' or physical.soil or physical.external_influences or physical.conductor_count!=(3 if request.circuits.get(runs[seg.cable_run_id].circuit_id) is None or request.circuits[runs[seg.cable_run_id].circuit_id].pe_layout=='SAME_CLOSED_CONDUIT' else 2):
            problems.append(_problem('PHYSICAL_SCOPE','Recorte exige condutores físicos compatíveis com PE no mesmo conduto(3) ou separado(2), condutoPVC e ausência de influências adicionais',sid))
        if cond.grouped_circuits not in (1,2,3):
            problems.append(_problem('GROUP_RANGE','Agrupamento sem célula vinculada1–3',sid))
        if cond.grouped_circuits==1 and sid in group_for:
            problems.append(_problem('GROUP_CONFLICT','Trecho isolado foi incluído em grupo',sid))
        if cond.grouped_circuits>1:
            key=group_for.get(sid)
            if key is None:
                problems.append(_problem('GROUP_MEMBERS','Seleção agrupada exige todos os trechos/circuitos do feixe explicitamente identificados',sid))
            elif len(request.groups[key].segment_ids)!=cond.grouped_circuits:
                problems.append(_problem('GROUP_COUNT','Número de circuitos diverge dos membros identificados',sid))
    for key,group in request.groups.items():
        members=[segments[sid] for sid in group.segment_ids]
        cids=[runs[s.cable_run_id].circuit_id for s in members]
        if len({circuits[cid].design_current.value for cid in cids})!=1:
            problems.append(_problem('GROUP_CURRENT','Fator do feixe exige mesma corrente declarada em todos os membros: '+key))
        if any(s.conditions.grouped_circuits!=len(members) for s in members):
            problems.append(_problem('GROUP_COUNT','Cada trecho do grupo deve declarar o número completo de circuitos: '+key))
    # Same nominal basis, phase identity and cosφ are required along every path.
    boards={b.id:b for b in inst.boards};incoming={c.downstream_board_id:c for c in inst.circuits if c.kind=='FEEDER'}
    for leaf in inst.circuits:
        chain=[leaf];board=boards[leaf.board_id]
        while board.supply_id is None:
            feeder=incoming[board.id];chain.append(feeder);board=boards[feeder.board_id]
        if all(c.id in request.circuits for c in chain):
            ci=request.circuits[leaf.id]
            if any(c.voltage!=leaf.voltage or request.circuits[c.id].phase_set!=ci.phase_set or request.circuits[c.id].power_factor!=ci.power_factor for c in chain):
                problems.append(_problem('ACCUMULATION_MODEL','Caminho misto exige modelo fasorial além do recorte; não somar bases/fases/cosφ diferentes',leaf.id))
    return problems


def _pe_minimum(section,layout,catalog):
    floor={'SAME_CLOSED_CONDUIT':Decimal(0),
           'SEPARATE_MECHANICALLY_PROTECTED':Decimal(catalog['minimums']['pe_separate_protected_floor_mm2']),
           'SEPARATE_UNPROTECTED':Decimal(catalog['minimums']['pe_separate_unprotected_floor_mm2'])}[layout]
    return max(section,floor)


def resolve(request,indices,catalog):
    """Explicit source resolution, recorded alongside original inputs in the result."""
    raw=request.topology.model_dump(mode='json');inst=raw['installation'];rows=catalog['sections']
    data={'id':str(request.id),'topology':raw,'circuits':{},'segments':{},'cell_revision':cell_bindings.REVISION,
          'origin_drop_percent':str(request.origin_drop_percent),'origin_evidence':request.origin_evidence.model_dump(mode='json')}
    segment_map={s['id']:s for s in inst['segments']};circuit_map={c['id']:c for c in inst['circuits']}
    group_ids={sid:key for key,g in request.groups.items() for sid in g.segment_ids}
    selected={}
    for cid,ci in request.circuits.items():
        row=rows[indices[cid]];section=Decimal(row['section_mm2']);pe=_pe_minimum(section,ci.pe_layout,catalog)
        # Every PE candidate belongs to this finite commercial catalog.
        pe_section=next(Decimal(r['section_mm2']) for r in rows if Decimal(r['section_mm2'])>=pe)
        selected[str(cid)]={'phase_mm2':str(section),'neutral_mm2':str(section) if ci.neutral_required else None,'pe_mm2':str(pe_section)}
        def minimum(value,ref): return {'section_mm2':str(value),'evidence':registry.evidence(ref)}
        data['circuits'][str(cid)]={'power_factor':str(ci.power_factor),'phase_set':ci.phase_set,
            'regime':'SINUSOIDAL_STEADY_BALANCED_EQUAL_RETURN','loaded_conductors':2,'neutral_required':ci.neutral_required,
            'neutral_section_mm2':str(section) if ci.neutral_required else None,'pe_section_mm2':str(pe_section),
            'phase_minimum':minimum(catalog['minimums']['phase'][ci.use],catalog['minimums']['phase_reference']),
            'neutral_minimum':minimum(section,catalog['minimums']['neutral_reference']) if ci.neutral_required else None,
            'pe_minimum':minimum(pe,catalog['minimums']['pe_reference']),
            'total_drop_limit_percent':catalog['voltage']['total_origin_limit_percent'],
            'limit_evidence':registry.evidence(catalog['voltage']['reference'])}
        for run in inst['cable_runs']:
            if run['circuit_id']!=str(cid):continue
            run['section']['value']=str(section)
            for sid_text in run['segment_ids']:
                sid=UUID(sid_text);si=request.segments[sid];seg=segment_map[sid_text]
                seg['impedance']={'resistance':row['rca_ohm_km'],'reactance':row['xl_ohm_km'],'unit':'ohm/km','frequency_hz':'60',
                    'conductor_temperature':{'value':'70','unit':'degC'},'source_reference':catalog['source']['url']+'#page=33; '+row['impedance_reference']+'; seção='+str(section)}
                data['segments'][sid_text]={'installation_number':si.installation_number,'infrared':si.infrared,
                    'grouping':'FEIXE' if sid in group_ids else 'ISOLADO','homogeneous':True,'uniformly_loaded':True,
                    'arrangement':'PRYSMIAN_SUPERASTIC_TWO_LOADED_TOUCHING_60HZ_70C_NONFERROMAGNETIC',
                    'impedance_evidence':registry.evidence(row['impedance_reference']+'; seção='+str(section)),
                    'impedance_section_mm2':str(section),'impedance_material':'Cu','impedance_insulation':'PVC','impedance_kind':'RAC_XL_AT_DECLARED_CONDITIONS'}
    return Study.model_validate(data),selected


def evaluate(request,indices,catalog):
    study,selected=resolve(request,indices,catalog);memory=analyze(study)
    failures=[];pending=[];failed_paths=[]
    for row in memory['segments']:
        for key,check in row['criteria'].items():
            if check['status']=='REPROVADO':failures.append({'circuit_id':row['circuit_id'],'segment_id':row['segment_id'],'criterion':key})
            elif check['status'] not in ('ATENDE_STUDY','ATENDE_ESTUDO','ATENDE_LOTE_LIMITADO','CALCULADO_ESTUDO','NAO_APLICAVEL'):
                pending.append({'circuit_id':row['circuit_id'],'segment_id':row['segment_id'],'criterion':key,'reason':check['reason']})
            if check['status'] in ('ATENDE_ESTUDO','ATENDE_LOTE_LIMITADO','CALCULADO_ESTUDO'):
                check['status']='ATENDE_FONTE_VINCULADA'
                check['binding']='F01_ACCEPTED_CELLS' if key=='capacity' else catalog['catalog_version']
                check['reason']='Critério F07 calculado com parâmetro resolvido no servidor; não homologa instalação'
    for cid,cr in memory['circuits'].items():
        total=cr['voltage_total']
        if total['status']=='REPROVADO':
            failures.append({'circuit_id':cid,'criterion':'voltage_total'});failed_paths.append(cr['upstream_circuit_ids'])
        elif total['status']!='ATENDE_ESTUDO':pending.append({'circuit_id':cid,'criterion':'voltage_total','reason':total['reason']})
        else:total['status']='ATENDE_FONTE_VINCULADA'
        circuit=next(c for c in request.topology.installation.circuits if str(c.id)==cid)
        local=criterion('NAO_APLICAVEL','Limite local terminal não se aplica a alimentador')
        if circuit.kind=='TERMINAL':
            value=cr['drop_percent'];limit=Decimal(catalog['voltage']['terminal_local_limit_percent'])
            if value is None:
                local=criterion('BLOQUEADO','Queda local incompleta');pending.append({'circuit_id':cid,'criterion':'voltage_terminal'})
            else:
                delta=Decimal(value)-limit
                status='PENDENTE' if abs(delta)<Decimal('1e-100') else ('ATENDE_FONTE_VINCULADA' if delta<0 else 'REPROVADO')
                local=criterion(status,'Limite local4% independente do total5% desde ponto de entrega',drop_percent=value,
                    limit_percent=str(limit),evidence=registry.evidence(catalog['voltage']['reference']))
                if status=='REPROVADO':failures.append({'circuit_id':cid,'criterion':'voltage_terminal'});failed_paths.append([cid])
                elif status=='PENDENTE':pending.append({'circuit_id':cid,'criterion':'voltage_terminal','reason':'Fronteira numérica exige conferência'})
        cr['voltage_terminal']=local
    memory.pop('selected_commercial_section_mm2',None)
    memory['mandatory_pending']=[]
    memory['status']='REPROVADO' if failures else ('PENDENTE' if pending else 'CALCULATED_SOURCE_LINKED')
    memory['selected_sections_by_circuit']=selected if not failures and not pending else None
    return memory,selected,failures,pending,failed_paths


def select(request):
    with localcontext() as ctx:
        ctx.prec=200
        return _select(request)


def _select(request):
    try:catalog=registry.catalog();catalog_sha=registry.catalog_hash()
    except ValueError as exc:
        return {'algorithm_version':VERSION,'status':'BLOQUEADO','problems':[_problem('CATALOG_INVALID',str(exc))],
                'selected_sections_by_circuit':None,'normative_conformity_verified':False,'authoritative_for_sizing':False}
    problems=inspect_scope(request,catalog)
    base={'algorithm_version':VERSION,'policy':POLICY,'catalog_version':catalog['catalog_version'],'catalog_sha256':catalog_sha,
          'source':catalog['source'],'input_sha256':fingerprint(request),'input_snapshot':request.model_dump(mode='json'),
          'topology_sha256':topology_hash(request.topology),'normative_conformity_verified':False,'authoritative_for_sizing':False,
          'professional_approval':False,'f08_protection_checks_pending':True,
          'scope_criteria':['capacity_corrected_all_segments','phase_minimum','neutral_same_section','pe_geometry_minimum','voltage_total_each_circuit','voltage_terminal_local'],
          'scope_limits':catalog['boundaries']}
    if problems:return {**base,'status':'BLOQUEADO','problems':problems,'selected_sections_by_circuit':None,'iterations':[]}
    inst=request.topology.installation;rows=catalog['sections'];circuits={c.id:c for c in inst.circuits}
    indices={cid:0 for cid in circuits}
    # Capacity and mechanical minima are local, exact and independent of upstream drop.
    for cid,circuit in circuits.items():
        found=False
        for k,row in enumerate(rows):
            indices[cid]=k
            candidate,_,_,_,_=evaluate(request,indices,catalog)
            checks=[check for r in candidate['segments'] if r['circuit_id']==str(cid) for key,check in r['criteria'].items() if key!='voltage']
            if all(check['status'] in ('ATENDE_FONTE_VINCULADA','NAO_APLICAVEL') for check in checks):found=True;break
        if not found:
            return {**base,'status':'NO_SOLUTION_IN_CATALOG','problems':[_problem('LOCAL_CRITERIA_EXHAUSTED','Nenhuma seção do catálogo atende capacidade/mínimos deste circuito',cid)],
                    'selected_sections_by_circuit':None,'iterations':[],'memory':candidate}
    runs={r.id:r for r in inst.cable_runs};segments={s.id:s for s in inst.segments}
    groups=[[runs[segments[sid].cable_run_id].circuit_id for sid in g.segment_ids] for g in request.groups.values()]
    def normalize():
        changed=True
        while changed:
            changed=False
            for group in groups:
                maximum=max(indices[cid] for cid in group)
                for cid in group:
                    if indices[cid]!=maximum:indices[cid]=maximum;changed=True
    normalize();iterations=[]
    bound=1+len(circuits)*(len(rows)-1)
    for number in range(bound):
        memory,selected,failures,pending,paths=evaluate(request,indices,catalog)
        iterations.append({'iteration':number+1,'sections':selected,'status':memory['status'],'failures':failures,'pending':pending})
        if pending:
            return {**base,'status':'PENDENTE','problems':pending,'iterations':iterations,'selected_sections_by_circuit':None,'memory':memory}
        if not failures:
            return {**base,'status':'SELECTED_SOURCE_LINKED','problems':[],'iterations':iterations,'selected_sections_by_circuit':selected,
                    'memory':memory,'resolved_topology':memory['input_snapshot']['topology'],
                    'selection_note':'Solução conservadora do catálogo finito, sem promessa de ótimo econômico; requer verificações F08 antes de dimensionamento definitivo'}
        grow={UUID(cid) for path in paths for cid in path}
        # Any unexpected non-voltage failure remains explicit, never hidden by upsizing.
        for fail in failures:
            if not fail['criterion'].startswith('voltage'):grow.add(UUID(fail['circuit_id']))
        can_grow=[cid for cid in grow if indices[cid]<len(rows)-1]
        if not can_grow:
            return {**base,'status':'NO_SOLUTION_IN_CATALOG','problems':failures,'iterations':iterations,'selected_sections_by_circuit':None,'memory':memory}
        for cid in can_grow:indices[cid]+=1
        normalize()
    # Monotonic finite policy makes this unreachable for a validated catalog.
    return {**base,'status':'PENDENTE','problems':[_problem('SEARCH_BUDGET','Busca não concluída; não equivale a ausência de solução')],
            'iterations':iterations,'selected_sections_by_circuit':None}


def save_selection(repo,project_id,request,expected):
    if request.topology.installation.project.id!=project_id:raise ValueError('Seleção pertence a outro projeto')
    previous=repo.carregar(str(project_id))
    if previous is None:raise ValueError('Cadastre topologia antes da seleção')
    data=dict(previous['dados'])
    if topology_hash(load_document(data))!=topology_hash(request.topology):raise ValueError('Topologia divergente; reabra antes de selecionar')
    items=list(data.get('conductor_selections',[]))
    if any(x['request']['id']==str(request.id) for x in items):raise ValueError('Histórico imutável; novo UUID obrigatório')
    result=select(request)
    items.append({'request':request.model_dump(mode='json'),'result':result,'survey_sha256':digest(data.get('levantamento'))})
    data['conductor_selections']=items;data['documents_stale']=True;data['protection_results_stale']=True
    raw=load_document(data).installation.model_dump(mode='json')
    for run in raw['calculation_runs']:
        if run['state'] in ('VALID','PENDING'):run['state']='STALE'
    data['installation_snapshot']=create_snapshot(Installation.model_validate(raw)).model_dump(mode='json')
    revision=repo.salvar(str(project_id),previous['nome'],data,expected)
    return {'revision':revision,'result':result}


def selection_history(data):
    current=topology_hash(load_document(data));items=data.get('conductor_selections',[])
    latest=items[-1]['result'].get('input_sha256') if items else None
    result=[]
    for item in items:
        request=Selection.model_validate(item['request'])
        try:changed=item['result'].get('input_sha256')!=fingerprint(request)
        except ValueError:changed=True
        stale=changed or item['result'].get('topology_sha256')!=current or item['survey_sha256']!=digest(data.get('levantamento')) or item['result'].get('input_sha256')!=latest
        result.append({**item,'stale':stale,'dependent_documents_stale':stale or data.get('documents_stale',True),
                       'dependent_protection_stale':stale or data.get('protection_results_stale',True)})
    return result
