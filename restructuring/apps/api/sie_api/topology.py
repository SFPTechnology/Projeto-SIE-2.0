"""F05: declared physical metadata over the authoritative F02 graph.

No normative factors or electrical parameters are synthesized. F02 snapshot
serialization stays unchanged, preserving historical snapshot verification.
"""
from decimal import Decimal, localcontext
import json
from typing import Literal
from uuid import UUID
from pydantic import Field, ValidationError, field_validator, model_validator
from .domain.installation import (DomainModel, Installation, Magnitude, NonNegative,
                                  Positive, NamedIdentity)
from .installation_service import create_snapshot, InstallationSnapshot, digest


class Origin(DomainModel):
    reference: str = Field(min_length=1, max_length=500)
    method: Literal['DECLARED', 'MEASURED', 'DOCUMENTED']
    @field_validator('reference')
    @classmethod
    def nonblank(cls, value):
        if not value.strip():
            raise ValueError('Referência de origem não pode estar vazia')
        return value.strip()


class SourceImpedance(DomainModel):
    resistance: NonNegative
    reactance: Magnitude
    unit: Literal['ohm']
    frequency_hz: Positive
    origin: Origin
    confirmed: bool = Field(strict=True)


class SourceDetails(DomainModel):
    utility: str | None = Field(default=None, min_length=1, max_length=200)
    transformer: str | None = Field(default=None, min_length=1, max_length=200)
    status: Literal['DECLARED', 'CONFIRMED', 'PENDING']
    origin: Origin
    impedance: SourceImpedance | None = None

    @field_validator('utility', 'transformer')
    @classmethod
    def optional_nonblank(cls, value):
        if value is not None and not value.strip():
            raise ValueError('Dado desconhecido deve ser null, não texto vazio')
        return value.strip() if value is not None else None


class Bus(NamedIdentity):
    role: Literal['PHASE', 'NEUTRAL', 'PE', 'PEN', 'DECLARED']
    circuit_ids: list[UUID] = Field(default_factory=list)


class BoardDetails(DomainModel):
    origin: Origin
    buses: list[Bus] = Field(default_factory=list)


class SegmentDetails(DomainModel):
    origin: Origin
    route_from: str = Field(min_length=1, max_length=200)
    route_to: str = Field(min_length=1, max_length=200)
    route_status: Literal['DECLARED', 'MEASURED', 'DOCUMENTED']
    conductor_count: int = Field(gt=0, strict=True)
    containment_material: str = Field(min_length=1, max_length=200)
    environment: str = Field(min_length=1, max_length=500)
    soil: str | None = Field(default=None, min_length=1, max_length=500)
    external_influences: dict[str, str] = Field(default_factory=dict, max_length=100)

    @field_validator('route_from', 'route_to', 'containment_material', 'environment', 'soil')
    @classmethod
    def nonblank(cls, value):
        if value is not None and not value.strip():
            raise ValueError('Condição física não pode estar vazia')
        return value.strip() if value is not None else None

    @field_validator('external_influences')
    @classmethod
    def declared_influences(cls, value):
        if any(not k.strip() or not v.strip() or len(k) > 100 or len(v) > 500 for k, v in value.items()):
            raise ValueError('Influências exigem chave/valor declarados e limitados')
        return value


class Topology(DomainModel):
    schema_version: Literal['SIE_TOPOLOGY_V1'] = 'SIE_TOPOLOGY_V1'
    installation: Installation
    source_details: dict[UUID, SourceDetails] = Field(default_factory=dict)
    board_details: dict[UUID, BoardDetails] = Field(default_factory=dict)
    segment_details: dict[UUID, SegmentDetails] = Field(default_factory=dict)

    @model_validator(mode='before')
    @classmethod
    def explicit_phases(cls, value):
        # F02 historical default remains readable there; F05 never infers phases.
        if isinstance(value, dict):
            raw = value.get('installation')
            if isinstance(raw, dict) and isinstance(raw.get('circuits'), list) and any(isinstance(c, dict) and 'phases' not in c for c in raw['circuits']):
                raise ValueError('F05 exige fases explícitas em todos os circuitos')
        return value

    @model_validator(mode='after')
    def metadata_integrity(self):
        inst = self.installation
        for entries, entities in [(self.source_details, inst.supplies),
                                  (self.board_details, inst.boards),
                                  (self.segment_details, inst.segments)]:
            if not set(entries).issubset({x.id for x in entities}):
                raise ValueError('Metadado órfão: UUID não pertence à coleção canônica')
        supplies = {x.id: x for x in inst.supplies}
        for key, detail in self.source_details.items():
            if detail.impedance and detail.impedance.frequency_hz != supplies[key].frequency_hz:
                raise ValueError('Frequência da impedância diverge da fonte')
        ids = {inst.project.id}
        for name in type(inst).model_fields:
            values = getattr(inst, name)
            if isinstance(values, list):
                ids.update(x.id for x in values)
        circuits = {x.id: x for x in inst.circuits}
        for board_id, detail in self.board_details.items():
            for bus in detail.buses:
                if bus.id in ids:
                    raise ValueError('ID de barra duplicado')
                ids.add(bus.id)
                if len(bus.circuit_ids) != len(set(bus.circuit_ids)):
                    raise ValueError('Vínculo duplicado na barra')
                if any(key not in circuits or circuits[key].board_id != board_id for key in bus.circuit_ids):
                    raise ValueError('Barra referencia circuito de outro quadro ou inexistente')
        # A run is one ordered physical path; distinct runs remain alternatives,
        # never added as though they were successive lengths.
        for run in inst.cable_runs:
            details = [self.segment_details.get(key) for key in run.segment_ids]
            for left, right in zip(details, details[1:]):
                if left and right and left.route_to != right.route_from:
                    raise ValueError('Passagem física descontínua no percurso ' + str(run.id))
        return self


def exact_sum(values):
    values = list(values)
    if not values:
        return '0'
    with localcontext() as ctx:
        ctx.prec = max(v.adjusted() for v in values) - min(v.as_tuple().exponent for v in values) + len(str(len(values))) + 3
        return str(sum(values, Decimal(0)))


def topology_hash(document):
    raw = document.model_dump(mode='json')
    # Results and revision counters are not physical inputs.
    raw['installation'].pop('calculation_runs')
    raw['installation'].pop('revisions')
    raw['installation']['project'].pop('revision')
    return digest(raw)


def inspect_topology(raw):
    try:
        document = Topology.model_validate(raw)
    except ValidationError as exc:
        return {'valid': False, 'errors': [{'location': list(e['loc']), 'message': e['msg']} for e in exc.errors()],
                'normative_conformity_verified': False}
    return report(document)


def report(document):
    inst = document.installation
    boards = {x.id: x for x in inst.boards}
    circuits = {x.id: x for x in inst.circuits}
    incoming = {c.downstream_board_id: c for c in inst.circuits if c.kind == 'FEEDER'}
    segments = {x.id: x for x in inst.segments}
    by_circuit = {c.id: [r for r in inst.cable_runs if r.circuit_id == c.id] for c in inst.circuits}
    warnings, paths = [], []
    for supply in inst.supplies:
        details = document.source_details.get(supply.id)
        if not details or details.status != 'CONFIRMED' or not details.impedance or not details.impedance.confirmed:
            warnings.append({'id': str(supply.id), 'code': 'SOURCE_UNCONFIRMED',
                             'message': 'Curto-circuito definitivo bloqueado: fonte/impedância sem confirmação'})
    for board in inst.boards:
        if board.id not in document.board_details or not document.board_details[board.id].buses:
            warnings.append({'id': str(board.id), 'code': 'BUSES_UNDECLARED', 'message': 'Barras não cadastradas'})
    for segment in inst.segments:
        if segment.id not in document.segment_details:
            warnings.append({'id': str(segment.id), 'code': 'PHYSICAL_DATA_PENDING', 'message': 'Origem e passagem física não cadastradas'})
        elif document.segment_details[segment.id].route_status == 'DECLARED':
            warnings.append({'id': str(segment.id), 'code': 'DECLARED_ROUTE', 'message': 'Percurso declarado; sem distância geométrica calculada'})
    for load in inst.loads:
        terminal = next(c for c in inst.circuits if load.id in c.load_ids)
        chain, board = [terminal], boards[terminal.board_id]
        while board.supply_id is None:
            feeder = incoming[board.id]
            chain.append(feeder)
            board = boards[feeder.board_id]
        chain.reverse()
        legs = []
        for circuit in chain:
            runs = []
            for run in by_circuit[circuit.id]:
                items = []
                for key in run.segment_ids:
                    segment = segments[key]
                    items.append({'id': str(key), 'name': segment.name,
                                  'length': segment.length.model_dump(mode='json'),
                                  'conditions': segment.conditions.model_dump(mode='json'),
                                  'impedance': segment.impedance.model_dump(mode='json') if segment.impedance else None,
                                  'physical': document.segment_details[key].model_dump(mode='json') if key in document.segment_details else None})
                runs.append({'id': str(run.id), 'segments': items,
                             'length_m': exact_sum(segments[k].length.value for k in run.segment_ids)})
            legs.append({'circuit_id': str(circuit.id), 'name': circuit.name, 'kind': circuit.kind,
                         'board_id': str(circuit.board_id), 'runs': runs})
        unambiguous = all(len(leg['runs']) == 1 for leg in legs)
        paths.append({'load_id': str(load.id), 'source_id': str(board.supply_id),
                      'board_ids': [str(c.board_id) for c in chain], 'legs': legs,
                      'length_m': exact_sum(Decimal(leg['runs'][0]['length_m']) for leg in legs) if unambiguous else None,
                      'length_status': 'DECLARED_SEGMENTS' if unambiguous else 'AMBIGUOUS_RUNS'})
    return {'valid': True, 'errors': [], 'warnings': warnings, 'paths': paths,
            'topology_sha256': topology_hash(document),
            'normative_conformity_verified': False,
            'definitive_short_circuit_allowed': False}


def load_document(data):
    snapshot = InstallationSnapshot.model_validate(data['installation_snapshot'])
    metadata = data.get('topology_metadata', {})
    if not isinstance(metadata, dict) or 'installation' in metadata:
        raise ValueError('Metadados não podem substituir a conectividade canônica')
    return Topology.model_validate({**metadata, 'installation': json.loads(snapshot.canonical_json)})


def persist(repo, project_id, document, expected):
    inst = document.installation
    if inst.project.id != project_id or inst.project.revision != expected + 1:
        raise ValueError('Topologia deve pertencer ao projeto e à próxima revisão esperada')
    previous = repo.carregar(str(project_id))
    data = dict(previous['dados']) if previous else {}
    changed = data.get('topology_sha256') != topology_hash(document)
    # Never retain a VALID result after a changed physical input.
    raw = inst.model_dump(mode='json')
    if changed:
        for run in raw['calculation_runs']:
            if run['state'] in ('VALID', 'PENDING'):
                run['state'] = 'STALE'
    inst = Installation.model_validate(raw)
    data['installation_snapshot'] = create_snapshot(inst).model_dump(mode='json')
    metadata = document.model_dump(mode='json')
    metadata.pop('installation')
    data['topology_metadata'] = metadata
    data['topology_sha256'] = topology_hash(document)
    data['topology_results_stale'] = changed or data.get('topology_results_stale', False)
    revision = repo.salvar(str(project_id), inst.project.name, data, expected)
    return {'id': str(project_id), 'revision': revision, 'results_stale': data['topology_results_stale'],
            'topology_sha256': data['topology_sha256']}
