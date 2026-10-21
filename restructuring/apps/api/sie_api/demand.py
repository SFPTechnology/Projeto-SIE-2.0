"""F06 deterministic demand study; explicit rules, never normative approval.

The authoritative connectivity and load powers are F05/F02. Classification and
rule selection are independent, explicit inputs. Synthetic rules remain studies.
"""
from decimal import Decimal, localcontext
from typing import Literal
from uuid import UUID
from pydantic import Field, model_validator, field_validator
from .domain.installation import DomainModel, Magnitude
from .topology import Topology, topology_hash, load_document
from .installation_service import digest

VERSION = 'SIE_DEMAND_V1'
Purpose = Literal['ENTRANCE', 'FEEDER', 'FINAL_CIRCUIT', 'STUDY']
Number = Magnitude

class Bounded(DomainModel):
    @field_validator('*')
    @classmethod
    def numeric_bounds(cls, value):
        if isinstance(value, Decimal) and (abs(value) > Decimal('1e15') or value.as_tuple().exponent < -24):
            raise ValueError('Magnitude excede limites F06 (1e15; 24 casas)')
        return value

class Band(Bounded):
    lower_va: Number = Field(ge=0)
    upper_va: Number | None = Field(default=None, gt=0)
    factor: Number = Field(ge=0, le=1)

class Rule(Bounded):
    id: str = Field(min_length=1, max_length=120)
    version: str = Field(min_length=1, max_length=120)
    category: str = Field(min_length=1, max_length=120)
    purpose: Purpose
    scope: Literal['TERMINAL_CIRCUIT', 'BOARD', 'SUPPLY'] = 'TERMINAL_CIRCUIT'
    mode: Literal['WHOLE_GROUP', 'PROGRESSIVE'] = 'WHOLE_GROUP'
    source: str = Field(min_length=1, max_length=500)
    edition: str = Field(min_length=1, max_length=120)
    condition: str = Field(min_length=1, max_length=500)
    status: Literal['PENDING', 'SYNTHETIC_STUDY', 'VERIFIED']
    # VERIFIED is not accepted from arbitrary HTTP/CLI input as a normative registry.
    bands: list[Band] = Field(min_length=1, max_length=100)
    utility: str | None = Field(default=None, min_length=1)
    locality: str | None = Field(default=None, min_length=1)
    typology: str | None = Field(default=None, min_length=1)

    @field_validator('id', 'version', 'category', 'source', 'edition', 'condition', 'utility', 'locality', 'typology')
    @classmethod
    def nonblank(cls, value):
        if value is not None and not value.strip():
            raise ValueError('Texto obrigatório não pode ser vazio')
        return value.strip() if value is not None else None

    @model_validator(mode='after')
    def ordered_bands(self):
        for idx, band in enumerate(self.bands):
            if band.upper_va is not None and band.upper_va <= band.lower_va:
                raise ValueError('Faixa vazia/invertida')
            if idx and (self.bands[idx-1].upper_va is None or band.lower_va < self.bands[idx-1].upper_va):
                raise ValueError('Faixas sobrepostas ou fora de ordem')
        if self.mode == 'PROGRESSIVE' and (self.bands[0].lower_va != 0 or any(self.bands[i-1].upper_va != self.bands[i].lower_va for i in range(1,len(self.bands)))):
            raise ValueError('Modelo progressivo exige faixas contíguas desde zero')
        return self

class Assignment(Bounded):
    category: str = Field(min_length=1, max_length=120)
    criterion: str = Field(min_length=1, max_length=500)
    group: str = Field(min_length=1, max_length=120)
    rule_id: str | None = None
    target_id: UUID | None = None
    condition_evidence: str | None = Field(default=None, min_length=1, max_length=500)
    power_factor: Number | None = Field(default=None, gt=0, le=1)

    @field_validator('category', 'criterion', 'group', 'rule_id', 'condition_evidence')
    @classmethod
    def nonblank(cls, value):
        if value is not None and not value.strip():
            raise ValueError('Classificação/evidência não pode ser vazia')
        return value.strip() if value is not None else None

class SupplyContext(DomainModel):
    utility: str = Field(min_length=1)
    locality: str = Field(min_length=1)
    typology: str = Field(min_length=1)
    edition: str = Field(min_length=1)
    concession_confirmed: bool = Field(strict=True)

class Scenario(DomainModel):
    schema_version: Literal['SIE_DEMAND_V1'] = VERSION
    id: UUID
    name: str = Field(min_length=1, max_length=160)
    purpose: Purpose
    topology: Topology
    assignments: dict[UUID, Assignment] = Field(default_factory=dict, max_length=20000)
    rules: list[Rule] = Field(default_factory=list, max_length=1000)
    contexts: dict[UUID, SupplyContext] = Field(default_factory=dict)
    source_connections: dict[UUID, Literal['SINGLE_PHASE_FN', 'SINGLE_PHASE_FF', 'THREE_PHASE']] = Field(default_factory=dict)
    balanced_three_phase: bool = Field(default=False, strict=True)

    @model_validator(mode='after')
    def integrity(self):
        inst = self.topology.installation
        for load in inst.loads:
            for power in (load.active_power, load.reactive_power, load.apparent_power):
                if power and (abs(power.value) > Decimal('1e15') or power.value.as_tuple().exponent < -24):
                    raise ValueError('Potência fora dos limites numéricos F06')
        if not set(self.assignments).issubset({x.id for x in inst.loads}):
            raise ValueError('Classificação de carga inexistente')
        if not set(self.source_connections).issubset({x.id for x in inst.supplies}):
            raise ValueError('Conexão de fonte inexistente')
        if not set(self.contexts).issubset({x.id for x in inst.supplies}):
            raise ValueError('Contexto de fonte inexistente')
        if len({x.id for x in self.rules}) != len(self.rules):
            raise ValueError('Regra duplicada')
        return self


def fingerprint(scenario):
    raw = scenario.model_dump(mode='json')
    raw['topology'] = topology_hash(scenario.topology)
    raw.pop('id'); raw.pop('name')
    return digest(raw)


def _powers(load, assignment):
    p = load.active_power.value if load.active_power else None
    q = load.reactive_power.value if load.reactive_power else None
    s = load.apparent_power.value if load.apparent_power else None
    fp = assignment.power_factor if assignment else None
    if s is not None and p is not None and p > s:
        raise ValueError('P excede S')
    if p is not None and q is not None:
        resultant = (p*p+q*q).sqrt()
        if s is not None and abs(s-resultant) > max(Decimal('0.01'), s*Decimal('0.001')):
            raise ValueError('P/Q/S inconsistentes')
        s = resultant if s is None else s
    if fp is not None:
        if p is not None and s is not None and s and abs(p/s-fp) > Decimal('0.001'):
            raise ValueError('Fator de potência contradiz P/S')
        if p is not None and s is None: s = p/fp
        if s is not None and p is None: p = s*fp
    if s is not None and q is not None and abs(q) > s:
        raise ValueError('|Q| excede S')
    # Reactive sign is never inferred from power factor.
    return {'p_w': p, 'q_var': q, 's_va': s}


def _sum(rows):
    result = {}
    for field in ('p_w', 'q_var', 's_va'):
        values = [r[field] for r in rows]
        result[field] = {'value': str(sum((x for x in values if x is not None), Decimal(0))),
                         'missing': sum(x is None for x in values)}
    # S is sum of individual VA (conservative scalar aggregation), not |sum(P+jQ)|.
    result['s_method'] = 'SUM_INDIVIDUAL_VA'
    return result


def calculate(scenario: Scenario):
    with localcontext() as ctx:
        ctx.prec = 80
        return _calculate(scenario)


def _calculate(sc):
    inst = sc.topology.installation
    boards = {x.id: x for x in inst.boards}
    incoming = {c.downstream_board_id: c for c in inst.circuits if c.kind == 'FEEDER'}
    paths = {}
    load_points = {p.id: p for p in inst.load_points}
    circuits = {c.id: c for c in inst.circuits}
    for c in inst.circuits:
        if c.kind != 'TERMINAL': continue
        chain = [c]; board = boards[c.board_id]
        while board.supply_id is None:
            feeder = incoming[board.id]; chain.append(feeder); board = boards[feeder.board_id]
        for key in c.load_ids:
            paths[key] = (chain, board.supply_id)
    rules = {r.id: r for r in sc.rules}
    powers = {}; problems = []; parcels = []; groups = {}
    for load in inst.loads:
        a = sc.assignments.get(load.id)
        try: powers[load.id] = _powers(load, a)
        except ValueError as exc:
            powers[load.id] = dict(p_w=None, q_var=None, s_va=None)
            problems.append({'load_id': str(load.id), 'code': 'POWER_CONFLICT', 'message': str(exc)})
        if a is None:
            problems.append({'load_id': str(load.id), 'code': 'CLASSIFICATION_PENDING'})
        # Groups are scoped to terminal circuit: upstream totals sum the same parcels.
        terminal = paths[load.id][0][0]
        selected_rule = rules.get(a.rule_id) if a else None
        scope = selected_rule.scope if selected_rule else 'TERMINAL_CIRCUIT'
        target = a.target_id if a and a.target_id else terminal.id
        valid_target = ((scope == 'TERMINAL_CIRCUIT' and target == terminal.id) or
                        (scope == 'BOARD' and a and a.target_id in {c.board_id for c in paths[load.id][0]}) or
                        (scope == 'SUPPLY' and a and a.target_id == paths[load.id][1]))
        key = (scope, target, a.group if a else str(load.id), valid_target)
        groups.setdefault(key, []).append(load.id)
    demand = {key: dict(p_w=None, q_var=None, s_va=None) for key in powers}
    applied_targets = {}
    for (scope, target_id, group, valid_target), ids in groups.items():
        assignments = [sc.assignments.get(key) for key in ids]
        selected = {a.rule_id for a in assignments if a}
        rule = rules.get(next(iter(selected))) if len(selected) == 1 else None
        reason = None
        if not valid_target: reason = 'INVALID_AGGREGATION_TARGET'
        elif sc.purpose == 'FINAL_CIRCUIT' and scope != 'TERMINAL_CIRCUIT': reason = 'SCOPE_NOT_ALLOWED_FOR_FINAL_CIRCUIT'
        elif any(a is None for a in assignments): reason = 'CLASSIFICATION_PENDING'
        elif rule is None: reason = 'RULE_PENDING_OR_CONFLICT'
        elif any(a.category != rule.category for a in assignments): reason = 'CATEGORY_MISMATCH'
        elif rule.purpose != sc.purpose: reason = 'PURPOSE_MISMATCH'
        elif any(not a.condition_evidence for a in assignments): reason = 'CONDITION_EVIDENCE_PENDING'
        elif rule.status != 'SYNTHETIC_STUDY': reason = 'TRUSTED_NORMATIVE_REGISTRY_PENDING'
        source = paths[ids[0]][1]
        if reason is None and sc.purpose == 'ENTRANCE':
            context = sc.contexts.get(source)
            if (context is None or not context.concession_confirmed or
                not all(getattr(rule, k) == getattr(context, k) for k in ('utility','locality','typology','edition'))):
                reason = 'UTILITY_SCOPE_MISMATCH'
        total = _sum([powers[key] for key in ids])
        factor = None
        if reason is None:
            if total['s_va']['missing']: reason = 'APPARENT_POWER_PENDING'
            else:
                s = Decimal(total['s_va']['value'])
                band = next((b for b in rule.bands if b.lower_va <= s and (b.upper_va is None or s < b.upper_va)), None)
                if band is None: reason = 'OUTSIDE_RULE_BANDS'
                elif rule.mode == 'WHOLE_GROUP' or s == 0: factor = band.factor
                else:
                    demanded = sum((max(Decimal(0),min(s,b.upper_va if b.upper_va is not None else s)-b.lower_va)*b.factor for b in rule.bands),Decimal(0))
                    factor = demanded/s
        if factor is not None:
            for key in ids:
                demand[key] = {k: v*factor if v is not None else None for k,v in powers[key].items()}
                applied_targets[key] = (scope, target_id)
        else:
            problems.append({'circuit_id': str(target_id), 'group': group, 'code': reason})
        parcels.append({'scope': scope, 'target_id': str(target_id), 'circuit_id': str(target_id), 'group': group, 'load_ids': list(map(str,ids)),
                        'installed': total, 'factor': str(factor) if factor is not None else None,
                        'rule': rule.model_dump(mode='json') if rule else None,
                        'assignments': [a.model_dump(mode='json') if a else None for a in assignments],
                        'status': reason or 'CALCULATED_STUDY'})
    def aggregate(ids):
        return {'installed': _sum([powers[key] for key in ids]), 'demand': _sum([demand[key] for key in ids])}
    by_circuit = {}
    for circuit in inst.circuits:
        ids = [key for key,(chain,source) in paths.items() if circuit.id in {c.id for c in chain}]
        row = aggregate(ids)
        applicable = ((circuit.kind == 'TERMINAL' and sc.purpose in ('FINAL_CIRCUIT','STUDY')) or
                      (circuit.kind == 'FEEDER' and sc.purpose in ('FEEDER','STUDY')))
        s = row['demand']['s_va']
        # An upstream diversity rule never sizes a branch below its target.
        branch_scope_ok = all(
            applied_targets.get(key, ('PENDING', None))[0] == 'TERMINAL_CIRCUIT' or
            (applied_targets.get(key, ('PENDING', None))[0] == 'BOARD' and
             next((idx for idx,c in enumerate(paths[key][0]) if c.id == circuit.id), -1) >=
             next((idx for idx,c in enumerate(paths[key][0]) if c.downstream_board_id == applied_targets[key][1]), len(paths[key][0])))
            for key in ids)
        eligible = applicable and branch_scope_ok and not s['missing'] and (circuit.phases == 1 or sc.balanced_three_phase)
        divisor = circuit.voltage.value*(Decimal(3).sqrt() if circuit.phases == 3 else Decimal(1))
        row['design_current'] = {'value_a': str(Decimal(s['value'])/divisor) if eligible else None,
            'status': 'CALCULATED_STUDY' if eligible else 'PENDING_OR_PURPOSE_MISMATCH',
            'formula': 'Ib=S/(sqrt(3)*U_FF)' if circuit.phases == 3 else 'Ib=S/U',
            'voltage': circuit.voltage.model_dump(mode='json'),
            'assumptions': ['SUM_INDIVIDUAL_VA', 'BALANCED_THREE_PHASE' if circuit.phases == 3 else 'SINGLE_PHASE'],
            'precision_digits': 80, 'authoritative_for_sizing': False}
        by_circuit[str(circuit.id)] = row
    rooms = {key: load_points[load.load_point_id].room_id for key,load in ((x.id,x) for x in inst.loads)}
    by_supply = {}
    for source in inst.supplies:
        row = aggregate([key for key,(_,sid) in paths.items() if sid == source.id])
        connection = sc.source_connections.get(source.id)
        three = connection == 'THREE_PHASE'
        voltage = source.voltage_ff if connection in ('THREE_PHASE', 'SINGLE_PHASE_FF') else source.voltage_fn
        eligible = (connection is not None and voltage is not None and
                    sc.purpose in ('ENTRANCE','STUDY') and not row['demand']['s_va']['missing'] and
                    (not three or (source.phases == 3 and sc.balanced_three_phase)))
        divisor = voltage.value*(Decimal(3).sqrt() if three else Decimal(1)) if voltage else None
        row['design_current'] = {'value_a':str(Decimal(row['demand']['s_va']['value'])/divisor) if eligible else None,
                                'formula':'Ib=S/(sqrt(3)*U_FF)' if three else 'Ib=S/U',
                                'connection':connection, 'precision_digits':80,
                                'status':'CALCULATED_STUDY' if eligible else 'PENDING',
                                'authoritative_for_sizing':False}
        by_supply[str(source.id)] = row
    return {'algorithm_version': VERSION, 'scenario_id': str(sc.id), 'input_sha256': fingerprint(sc),
        'purpose': sc.purpose, 'total': aggregate(list(powers)),
        'by_room': {str(r.id): aggregate([k for k in powers if rooms[k] == r.id]) for r in inst.rooms},
        'by_circuit': by_circuit,
        'by_board': {str(b.id): aggregate([k for k,(chain,_) in paths.items() if b.id in {c.board_id for c in chain}]) for b in inst.boards},
        'by_supply': by_supply,
        'parcels': parcels, 'problems': problems,
        'status': 'PENDING' if problems else 'CALCULATED_STUDY',
        'normative_conformity_verified': False, 'utility_approval': False,
        'rule_aggregation_scope': 'EXPLICIT_TARGET_GROUP',
        'limitations': ['Fatores limitados ao alvo explícito; correntes abaixo do alvo não usam diversidade a montante.',
                        'Resultados de estudo não substituem corrente canônica nem homologação.']}


def save_scenario(repo, project_id, scenario, expected):
    if scenario.topology.installation.project.id != project_id:
        raise ValueError('Cenário pertence a outro projeto')
    previous = repo.carregar(str(project_id))
    if previous is None: raise ValueError('Cadastre a topologia canônica antes do cenário')
    data = dict(previous['dados'])
    if topology_hash(load_document(data)) != topology_hash(scenario.topology):
        raise ValueError('Cenário diverge da topologia atual; reabra antes de calcular')
    result = calculate(scenario)
    history = list(data.get('demand_scenarios', []))
    if any(x['scenario']['id'] == str(scenario.id) for x in history):
        raise ValueError('ID histórico imutável; crie novo cenário')
    history.append({'scenario': scenario.model_dump(mode='json'), 'result': result,
                    'topology_sha256': topology_hash(scenario.topology),
                    'survey_sha256': digest(data.get('levantamento'))})
    data['demand_scenarios'] = history
    revision = repo.salvar(str(project_id), previous['nome'], data, expected)
    return {'revision': revision, 'result': result}


def scenario_history(data):
    topology = topology_hash(load_document(data))
    survey = digest(data.get('levantamento'))
    return [{**item, 'stale': item['topology_sha256'] != topology or item['survey_sha256'] != survey}
            for item in data.get('demand_scenarios', [])]


def compare(before: Scenario, after: Scenario):
    if before.topology.installation.project.id != after.topology.installation.project.id:
        raise ValueError('Comparação exige o mesmo projeto')
    left, right = calculate(before), calculate(after)
    return {'before': left, 'after': right, 'inputs_changed': fingerprint(before) != fingerprint(after),
            'normative_conformity_verified': False}


def project_survey(survey, topology: Topology, links: dict[UUID, UUID]):
    """Explicit one-to-one equipment identity bridge; quantities multiplied once.

    Does not persist or guess electrical connection, room, classification or rule.
    Result is a F05 draft and must pass its normal revision/authenticated save.
    """
    if survey.projeto_id != topology.installation.project.id:
        raise ValueError('Levantamento de outro projeto')
    active = {x.id: x for x in survey.cargas if not x.arquivado}
    canonical = {x.id for x in topology.installation.loads}
    if set(links) != set(active) or set(links.values()) != canonical or len(links) != len(set(links.values())):
        raise ValueError('Ponte exige bijeção explícita entre todas as cargas ativas F04 e F02')
    raw = topology.model_dump(mode='json')
    lookup = {x['id']: x for x in raw['installation']['loads']}
    circuits = {key:c for c in topology.installation.circuits for key in c.load_ids}
    audit = []
    with localcontext() as ctx:
        ctx.prec = 80
        for key, source in active.items():
            target = links[key]; load = lookup[str(target)]; circuit = circuits[target]
            if source.tensao_v is not None and source.tensao_v != circuit.voltage.value:
                raise ValueError('Tensão F04 diverge do circuito F05; revisar conexão')
            if source.fases is not None and ((source.fases == 3) != (load['connection'] == 'THREE_PHASE') or
                                             (source.fases == 2 and load['connection'] != 'SINGLE_PHASE_FF')):
                raise ValueError('Fases F04 divergem da conexão F05')
            p,q,s = source.p_w, source.q_var, source.s_va
            if p is None and s is None:
                raise ValueError('Declare P ou S no levantamento; potência de placa não substitui entrada silenciosamente')
            if p is not None and s is None and source.fator_potencia is not None:
                s = (p/source.fator_potencia).quantize(Decimal('1e-24'))
            for field, value, unit in [('active_power',p,'W'),('reactive_power',q,'var'),('apparent_power',s,'VA')]:
                load[field] = {'value':str(value*source.quantidade), 'unit':unit} if value is not None else None
            load['design_current'] = None
            audit.append({'survey_load_id':str(key), 'canonical_load_id':str(target),
                          'quantity_applied_once':source.quantidade, 'category_not_inferred':True,
                          'derived_s_precision_decimal_places':24 if source.s_va is None and s is not None else None})
    projected = Topology.model_validate(raw)
    source_for = {links[key]:item for key,item in active.items()}
    # Reject a contradictory power triangle before returning the editable draft.
    for load in projected.installation.loads:
        fp = source_for[load.id].fator_potencia
        _powers(load, Assignment(category='BRIDGE',criterion='Explicit survey bridge',group='BRIDGE',power_factor=fp))
    return {'topology': projected.model_dump(mode='json'), 'audit':audit,
            'survey_sha256':digest(survey.model_dump(mode='json')),
            'requires_topology_revision_save':True, 'normative_conformity_verified':False}
