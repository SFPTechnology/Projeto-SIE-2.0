"""F07 segmented AC study. Server-owned limited F01 cells; no normative release.

Longitudinal steady-state approximation, identical outgoing/return conductors,
lagging sinusoidal load, balanced three-phase. No implicit Rdc-to-Rac conversion.
"""
from decimal import Decimal, localcontext, ROUND_HALF_UP
from typing import Literal
from uuid import UUID
from pydantic import Field, model_validator
from pydantic import BaseModel
from .domain.installation import DomainModel, Positive, NonNegative, Magnitude
from .topology import Topology, topology_hash, load_document, report as topology_report
from .installation_service import digest
from . import cell_bindings

VERSION = 'SIE-F07-1.0'
MODEL = 'Longitudinal AC: k L I (Rca cosφ + X sinφ); k=2 mono, sqrt(3) tri equilibrado'

class Evidence(DomainModel):
    document: str = Field(min_length=1, max_length=500, pattern=r'.*\S.*')
    edition: str = Field(min_length=1, max_length=100, pattern=r'.*\S.*')
    reference: str = Field(min_length=1, max_length=500, pattern=r'.*\S.*')
    sha256: str = Field(pattern=r'^[0-9a-f]{64}$')

class DeclaredMinimum(DomainModel):
    section_mm2: Positive
    evidence: Evidence

class CircuitInput(DomainModel):
    power_factor: Positive = Field(le=1)
    phase_set: Literal['L1_N','L2_N','L3_N','L1_L2','L2_L3','L3_L1','L1_L2_L3'] | None = None
    regime: Literal['SINUSOIDAL_STEADY_BALANCED_EQUAL_RETURN']
    loaded_conductors: int = Field(ge=2, le=3, strict=True)
    neutral_required: bool = Field(strict=True)
    neutral_section_mm2: Positive | None = None
    pe_section_mm2: Positive | None = None
    phase_minimum: DeclaredMinimum | None = None
    neutral_minimum: DeclaredMinimum | None = None
    pe_minimum: DeclaredMinimum | None = None
    total_drop_limit_percent: Positive | None = Field(default=None, le=100)
    limit_evidence: Evidence | None = None

    @model_validator(mode='after')
    def paired_limit(self):
        if (self.total_drop_limit_percent is None) != (self.limit_evidence is None):
            raise ValueError('Limite exige fonte; fonte exige limite')
        if not self.neutral_required and (self.neutral_section_mm2 is not None or self.neutral_minimum is not None):
            raise ValueError('Neutro não aplicável não aceita seção/regra de neutro')
        return self

class SegmentInput(DomainModel):
    installation_number: int = Field(strict=True)
    infrared: bool = Field(strict=True)
    grouping: Literal['ISOLADO', 'FEIXE']
    homogeneous: bool = Field(strict=True)
    uniformly_loaded: bool = Field(strict=True)
    arrangement: str = Field(min_length=1, max_length=500, pattern=r'.*\S.*')
    impedance_evidence: Evidence | None = None
    impedance_section_mm2: Positive | None = None
    impedance_material: Literal['Cu','Al','OTHER_DECLARED'] | None = None
    impedance_insulation: str | None = Field(default=None,min_length=1,max_length=100)
    impedance_kind: Literal['RAC_XL_AT_DECLARED_CONDITIONS'] | None = None

class Study(DomainModel):
    id: UUID
    topology: Topology
    circuits: dict[UUID, CircuitInput] = Field(default_factory=dict)
    segments: dict[UUID, SegmentInput] = Field(default_factory=dict)
    cell_revision: str = cell_bindings.REVISION
    origin_drop_percent: NonNegative | None = None
    origin_evidence: Evidence | None = None

    @model_validator(mode='after')
    def references(self):
        def bounded(value):
            if isinstance(value, Decimal) and (len(value.as_tuple().digits)>30 or abs(value.as_tuple().exponent)>30):
                raise ValueError('F07 suporta até 30 dígitos e expoente absoluto 30 por grandeza')
            if isinstance(value, BaseModel):
                for key in type(value).model_fields: bounded(getattr(value,key))
            elif isinstance(value, dict):
                for v in value.values(): bounded(v)
            elif isinstance(value, list):
                for v in value: bounded(v)
        bounded(self)
        if not set(self.circuits).issubset({c.id for c in self.topology.installation.circuits}):
            raise ValueError('Parâmetro de circuito órfão')
        if not set(self.segments).issubset({s.id for s in self.topology.installation.segments}):
            raise ValueError('Parâmetro de trecho órfão')
        for c in self.topology.installation.circuits:
            ci = self.circuits.get(c.id)
            if ci:
                if c.voltage.basis == 'FN' and not ci.neutral_required:
                    raise ValueError('Circuito FN exige neutro')
                expected = {'L1_L2_L3'} if c.phases == 3 else ({'L1_N','L2_N','L3_N'} if c.voltage.basis == 'FN' else {'L1_L2','L2_L3','L3_L1'})
                if ci.phase_set is not None and ci.phase_set not in expected:
                    raise ValueError('Fases declaradas incompatíveis com conexão')
        if (self.origin_drop_percent is None) != (self.origin_evidence is None):
            raise ValueError('Queda anterior à origem exige valor e fonte explícitos, inclusive zero')
        return self


def criterion(status, reason, **values):
    return {'status': status, 'reason': reason, **values}


def minimum(section, rule):
    if section is None or rule is None:
        return criterion('PENDENTE', 'Seção ou mínimo e fonte não informados')
    return criterion('ATENDE_ESTUDO' if section >= rule.section_mm2 else 'REPROVADO',
                     'Comparação com mínimo declarado; aplicabilidade não homologada',
                     section_mm2=str(section), minimum_mm2=str(rule.section_mm2),
                     evidence=rule.evidence.model_dump(mode='json'))


def neutral(section, rule, required):
    return minimum(section, rule) if required else criterion('NAO_APLICAVEL', 'Ausência de neutro declarada; conferir conexão')


def protective_earth(section, rule):
    # No inference from phase section; short-circuit/adiabatic check belongs to F08.
    return minimum(section, rule)


def temperature_factor(temperature):
    if temperature == 30: return Decimal(1)
    if temperature == 40:
        return Decimal(next(c[3] for c in cell_bindings.CELLS if c[0] == 'CEL-05'))
    raise ValueError('Temperatura sem célula vinculada no lote 01')


def grouping_factor(count):
    if count == 1: return Decimal(1)
    key = {2:'CEL-07', 3:'CEL-08'}.get(count)
    if key is None: raise ValueError('Agrupamento sem célula vinculada no lote 01')
    return Decimal(next(c[3] for c in cell_bindings.CELLS if c[0] == key))


def capacity(study, run, segment, ci, si):
    """Exact lookup only, reusing all applicability checks of F01 resolver."""
    if ci is None or si is None:
        return criterion('BLOQUEADO', 'Condições/carregamento do trecho não cadastrados')
    cond = segment.conditions
    if study.cell_revision != cell_bindings.REVISION:
        return criterion('BLOQUEADO', 'Versão de células desconhecida')
    if cond.additional_conditions or cond.medium != 'AIR':
        return criterion('BLOQUEADO', 'Meio/condições adicionais fora do escopo das células')
    physical = study.topology.segment_details.get(segment.id)
    if physical is None or physical.external_influences or physical.soil:
        return criterion('BLOQUEADO', 'Dados físicos ausentes ou influências sem regra vinculada')
    if physical.conductor_count < ci.loaded_conductors:
        return criterion('BLOQUEADO', 'Condutores carregados excedem total físico declarado')
    try:
        ft = temperature_factor(cond.ambient_temperature.value)
        fg = grouping_factor(cond.grouped_circuits)
        ctx = {'material':run.material, 'isolacao':run.insulation,
               'temperatura_condutor_c':int(cond.conductor_temperature.value) if cond.conductor_temperature and cond.conductor_temperature.value == 70 else -1,
               'metodo_referencia':cond.installation_method, 'metodo_instalacao':si.installation_number,
               'descricao_instalacao':si.arrangement, 'condutores_carregados':ci.loaded_conductors,
               'meio':'AR', 'temperatura_ambiente_c':int(cond.ambient_temperature.value),
               'radiacao_solar':cond.solar_exposure, 'radiacao_infravermelha':si.infrared,
               'circuitos_agrupados':cond.grouped_circuits, 'agrupamento':si.grouping,
               'grupo_homogeneo':si.homogeneous, 'carga_uniforme':si.uniformly_loaded}
        ids = ['CEL-01','CEL-02','CEL-03','CEL-04']
        if ft != 1: ids.append('CEL-05')
        if fg != 1: ids.append('CEL-07' if cond.grouped_circuits == 2 else 'CEL-08')
        table = [{'secao_mm2':float(c[2]), 'capacidade_a':float(c[3])} for c in cell_bindings.CELLS if c[1] == '36']
        _, provenance = cell_bindings.resolver_vinculo({'vinculo_celulas':{'registro_revisao':study.cell_revision,'celulas_ids':ids,'condicoes':ctx}, 'tabela_condutores':table, 'fator_correcao':float(ft*fg)})
        base = next((Decimal(c[3]) for c in cell_bindings.CELLS if c[1] == '36' and Decimal(c[2]) == run.section.value), None)
        if base is None: return criterion('BLOQUEADO', 'Seção sem célula vinculada; sem extrapolação')
        circuit = next(c for c in study.topology.installation.circuits if c.id == run.circuit_id)
        iz = base*ft*fg
        return criterion('ATENDE_LOTE_LIMITADO' if iz >= circuit.design_current.value else 'REPROVADO',
                         'Iz_base × ft × fg ≥ Ib; não conclui proteção', iz_base_a=str(base),
                         temperature_factor=str(ft), grouping_factor=str(fg), iz_a=str(iz),
                         ib_a=str(circuit.design_current.value), provenance=provenance)
    except ValueError as exc:
        return criterion('BLOQUEADO', str(exc))


def voltage_drop(current, length, resistance, reactance, power_factor, phases):
    """Pure formula with Decimal values; 100 significant digits in orchestrator."""
    if phases not in (1,3) or type(phases) is not int: raise ValueError('Fases inválidas')
    for v in (current,length,resistance,reactance,power_factor):
        if not isinstance(v,Decimal) or not v.is_finite(): raise ValueError('Grandeza Decimal finita exigida')
    if current <= 0 or length < 0 or resistance < 0 or reactance < 0 or not 0 < power_factor <= 1:
        raise ValueError('Grandeza fora da faixa do modelo')
    k = Decimal(2) if phases == 1 else Decimal(3).sqrt()
    sin = (1-power_factor*power_factor).sqrt()
    return k*length/1000*current*(resistance*power_factor+reactance*sin)


def fingerprint(study):
    raw = study.model_dump(mode='json'); raw.pop('id')
    raw['topology'] = topology_hash(study.topology)
    raw['server_cells'] = digest({'cells':cell_bindings.CELLS,'revision':cell_bindings.REVISION,'source':cell_bindings.SOURCE,'acceptance':cell_bindings.ACCEPTANCE})
    raw['algorithm_version'] = VERSION
    return digest(raw)


def analyze(study):
    with localcontext() as ctx:
        ctx.prec = 200
        return _analyze(study)


def _analyze(study):
    inst = study.topology.installation
    circuits = {c.id:c for c in inst.circuits}
    segments = {s.id:s for s in inst.segments}
    rows, circuit_rows = [], {}
    for cid,circuit in circuits.items():
        ci = study.circuits.get(cid)
        runs = [r for r in inst.cable_runs if r.circuit_id == cid]
        cr = {'circuit_id':str(cid), 'runs':[], 'drop_percent':None}
        for run in runs:
            drops = []
            for sid in run.segment_ids:
                seg = segments[sid]; si = study.segments.get(sid)
                checks = {'capacity':capacity(study,run,seg,ci,si),
                          'minimum_phase':minimum(run.section.value,ci.phase_minimum if ci else None),
                          'neutral':neutral(ci.neutral_section_mm2,ci.neutral_minimum,ci.neutral_required) if ci else criterion('PENDENTE','Neutro não declarado'),
                          'pe':protective_earth(ci.pe_section_mm2,ci.pe_minimum) if ci else criterion('PENDENTE','PE não declarado')}
                imp = seg.impedance
                compatible = (ci and si and imp and si.impedance_evidence and si.impedance_kind and
                              seg.conditions.conductor_temperature and imp.conductor_temperature.value == seg.conditions.conductor_temperature.value and
                              imp.reactance >= 0 and (circuit.phases != 3 or ci.loaded_conductors == 3) and
                              si.impedance_section_mm2 == run.section.value and si.impedance_material == run.material and si.impedance_insulation == run.insulation and
                              (circuit.phases != 1 or circuit.voltage.basis != 'FN' or ci.neutral_section_mm2 == run.section.value))
                if compatible:
                    drop = voltage_drop(circuit.design_current.value,seg.length.value,imp.resistance,imp.reactance,ci.power_factor,circuit.phases)
                    drops.append(drop*100/circuit.voltage.value)
                    checks['voltage'] = criterion('CALCULADO_ESTUDO','Rca/XL declarados para seção/arranjo/temperatura; sem autenticação da fonte',
                        drop_v=str(drop),drop_percent=str(drops[-1]),formula=MODEL,
                        rca_ohm_km=str(imp.resistance),xl_ohm_km=str(imp.reactance),
                        length_m=str(seg.length.value),ib_a=str(circuit.design_current.value),
                        power_factor=str(ci.power_factor),frequency_hz=str(imp.frequency_hz),
                        temperature_c=str(imp.conductor_temperature.value),
                        evidence=si.impedance_evidence.model_dump(mode='json'), arrangement=si.arrangement)
                else:
                    checks['voltage'] = criterion('BLOQUEADO','Rca/XL, fonte, condição térmica, carregamento ou modelo ausente/incompatível')
                row = {'circuit_id':str(cid),'run_id':str(run.id),'segment_id':str(sid),
                       'section_mm2':str(run.section.value),'material':run.material,'insulation':run.insulation,'criteria':checks}
                rows.append(row)
            drop_percent = sum(drops,Decimal(0)) if len(drops)==len(run.segment_ids) else None
            cr['runs'].append({'run_id':str(run.id),'drop_percent':str(drop_percent) if drop_percent is not None else None})
        if len(runs)==1: cr['drop_percent']=cr['runs'][0]['drop_percent']
        else: cr['reason']='Percursos alternativos/paralelos sem definição de distribuição; não somados'
        circuit_rows[str(cid)]=cr
    boards={b.id:b for b in inst.boards}
    incoming={c.downstream_board_id:c for c in inst.circuits if c.kind=='FEEDER'}
    for cid,leaf in circuits.items():
        chain=[leaf]; board=boards[leaf.board_id]
        while board.supply_id is None:
            feeder=incoming[board.id];chain.append(feeder);board=boards[feeder.board_id]
        chain.reverse()
        ci=study.circuits.get(cid)
        vals=[circuit_rows[str(c.id)]['drop_percent'] for c in chain]
        same_model=ci and ci.phase_set is not None and all(c.phases==leaf.phases and c.voltage==leaf.voltage and study.circuits.get(c.id) and study.circuits[c.id].power_factor==ci.power_factor and study.circuits[c.id].phase_set==ci.phase_set for c in chain)
        check=criterion('PENDENTE','Acumulação exige base/fases/cosφ compatíveis, percurso único e queda anterior explícita')
        if same_model and all(v is not None for v in vals) and study.origin_drop_percent is not None:
            total=study.origin_drop_percent+sum((Decimal(v) for v in vals),Decimal(0))
            check=criterion('PENDENTE','Limite total e fonte ausentes',total_percent=str(total))
            if ci.total_drop_limit_percent is not None:
                delta=total-ci.total_drop_limit_percent
                status='PENDENTE' if abs(delta)<Decimal('1e-100') else ('ATENDE_ESTUDO' if delta<0 else 'REPROVADO')
                check=criterion(status,'Soma longitudinal; faixa de incerteza absoluta 1e-100 ponto percentual na fronteira',
                    total_percent=str(total),limit_percent=str(ci.total_drop_limit_percent),evidence=ci.limit_evidence.model_dump(mode='json'))
        circuit_rows[str(cid)]['voltage_total']=check
        circuit_rows[str(cid)]['upstream_circuit_ids']=[str(c.id) for c in chain]
    paths = [{'load_id':path['load_id'],'circuit_ids':[l['circuit_id'] for l in path['legs']],
              'voltage_total':circuit_rows[path['legs'][-1]['circuit_id']]['voltage_total']}
             for path in topology_report(study.topology)['paths']]
    # Even a numerically complete study cannot confer normative status to client evidence.
    failed=any(v['status']=='REPROVADO' for r in rows for v in r['criteria'].values()) or any(p['voltage_total']['status']=='REPROVADO' for p in circuit_rows.values())
    return {'algorithm_version':VERSION,'input_sha256':fingerprint(study),'status':'REPROVADO' if failed else 'PENDENTE',
            'input_snapshot':study.model_dump(mode='json'),'project_revision':inst.project.revision,'topology_sha256':topology_hash(study.topology),
            'segments':rows,'circuits':circuit_rows,'paths':paths,'selected_commercial_section_mm2':None,
            'normative_conformity_verified':False,'authoritative_for_sizing':False,
            'mandatory_pending':['Aplicabilidade e fonte de mínimos fase/neutro/PE e Rca/XL não homologadas',
                                 'Proteção integral/adiabático não concluídos por Ib ≤ Iz',
                                 'Seleção comercial multicritério depende de catálogo verificado completo'],
            'precision':{'significant_digits':200,'input_max_digits':30,'input_max_absolute_exponent':30,'voltage_boundary_guard_percent':'1e-100','decision_rounding':'NONE','units':['A','V','m','mm2','ohm/km','%']}}


def presentation(value):
    with localcontext() as ctx:
        ctx.prec=max(110,len(value.as_tuple().digits)+abs(value.adjusted())+10)
        return str(value.quantize(Decimal('.01'),rounding=ROUND_HALF_UP))


def save(repo,project_id,study,expected):
    if study.topology.installation.project.id != project_id: raise ValueError('Estudo de outro projeto')
    previous=repo.carregar(str(project_id))
    if previous is None: raise ValueError('Cadastre topologia antes do estudo')
    data=dict(previous['dados'])
    if topology_hash(load_document(data))!=topology_hash(study.topology): raise ValueError('Topologia divergente; reabra')
    history=list(data.get('conductor_studies',[]))
    if any(x['study']['id']==str(study.id) for x in history): raise ValueError('Histórico imutável; novo UUID obrigatório')
    result=analyze(study)
    history.append({'study':study.model_dump(mode='json'),'result':result,'survey_sha256':digest(data.get('levantamento'))})
    data['conductor_studies']=history
    # A changed sizing input invalidates dependent protection/documents explicitly.
    data['protection_results_stale']=True; data['documents_stale']=True
    from .installation_service import create_snapshot
    inst=load_document(data).installation
    raw=inst.model_dump(mode='json')
    for run in raw['calculation_runs']:
        if run['state'] in ('VALID','PENDING'): run['state']='STALE'
    from .domain.installation import Installation
    data['installation_snapshot']=create_snapshot(Installation.model_validate(raw)).model_dump(mode='json')
    revision=repo.salvar(str(project_id),previous['nome'],data,expected)
    return {'revision':revision,'result':result}


def history(data):
    current=topology_hash(load_document(data)); items=data.get('conductor_studies',[])
    latest=items[-1]['result']['input_sha256'] if items else None
    result=[]
    for item in items:
        study=Study.model_validate(item['study'])
        stale=(item['result']['topology_sha256']!=current or item['survey_sha256']!=digest(data.get('levantamento')) or item['result']['input_sha256']!=fingerprint(study) or item['result']['input_sha256']!=latest)
        result.append({**item,'stale':stale,'dependent_protection_stale':stale or data.get('protection_results_stale',True),
                       'dependent_documents_stale':stale or data.get('documents_stale',True)})
    return result
