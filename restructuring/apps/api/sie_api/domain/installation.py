"""Canonical installation aggregate, independent of HTTP, persistence and normative engines.

Magnitude input is deliberately decimal text/Decimal, never a binary float. Units
are explicit and conversions must be performed before constructing the aggregate.
This module checks identities/topology; it does not size or approve installations.
"""
from decimal import Decimal
from typing import Annotated, Literal
from uuid import UUID

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, WithJsonSchema, field_validator, model_validator


def _decimal(value):
    if not isinstance(value, (str, Decimal)):
        raise ValueError('Magnitude requires decimal text or Decimal; convert units explicitly')
    if isinstance(value, str) and len(value) > 1100:
        raise ValueError('Decimal magnitude exceeds supported text length')
    try:
        number = Decimal(value)
    except Exception as exc:
        raise ValueError('Invalid decimal magnitude') from exc
    if not number.is_finite():
        raise ValueError('Magnitude must be finite')
    parts = number.as_tuple()
    if len(parts.digits) > 1000 or abs(parts.exponent) > 1000:
        raise ValueError('Decimal magnitude exceeds 1000 digits or absolute exponent 1000')
    return number


Magnitude = Annotated[Decimal, BeforeValidator(_decimal),
                      WithJsonSchema({'type': 'string'}, mode='validation')]
Positive = Annotated[Magnitude, Field(gt=0)]
NonNegative = Annotated[Magnitude, Field(ge=0)]


class DomainModel(BaseModel):
    model_config = ConfigDict(extra='forbid', validate_assignment=True, allow_inf_nan=False)


class Voltage(DomainModel):
    value: Positive
    unit: Literal['V']
    basis: Literal['FN', 'FF']


class Current(DomainModel):
    value: Positive
    unit: Literal['A']


class ActivePower(DomainModel):
    value: NonNegative
    unit: Literal['W']


class ReactivePower(DomainModel):
    value: Magnitude
    unit: Literal['var']


class ApparentPower(DomainModel):
    value: NonNegative
    unit: Literal['VA']


class Length(DomainModel):
    value: Positive
    unit: Literal['m']


class CrossSection(DomainModel):
    value: Positive
    unit: Literal['mm2']


class Temperature(DomainModel):
    value: Annotated[Magnitude, Field(gt=Decimal('-273.15'))]
    unit: Literal['degC']


class ImpedancePerLength(DomainModel):
    resistance: NonNegative
    reactance: Magnitude
    unit: Literal['ohm/km']
    frequency_hz: Positive
    conductor_temperature: Temperature
    source_reference: str = Field(min_length=1, max_length=500)

    @field_validator('source_reference')
    @classmethod
    def source_not_blank(cls, value):
        if not value.strip():
            raise ValueError('Source reference cannot be blank')
        return value.strip()


class NamedIdentity(DomainModel):
    id: UUID
    name: str = Field(min_length=1, max_length=200)

    @field_validator('name')
    @classmethod
    def name_not_blank(cls, value):
        if not value.strip():
            raise ValueError('Name cannot be blank')
        return value.strip()


class Project(NamedIdentity):
    revision: int = Field(ge=1, strict=True)


class Entity(NamedIdentity):
    project_id: UUID


class Building(Entity):
    pass


class Floor(Entity):
    building_id: UUID
    level: int = Field(strict=True)


class Room(Entity):
    floor_id: UUID


def _strict_phases(value):
    if type(value) is not int:
        raise ValueError('Phases requires integer 1 or 3, without coercion')
    return value


class Supply(Entity):
    phases: Annotated[Literal[1, 3], BeforeValidator(_strict_phases)]
    voltage_fn: Voltage | None = None
    voltage_ff: Voltage | None = None
    frequency_hz: Positive
    earthing_system: str = Field(min_length=1, max_length=100)

    @model_validator(mode='after')
    def explicit_voltage_basis(self):
        if self.voltage_fn is None and self.voltage_ff is None:
            raise ValueError('Supply requires at least one explicit nominal voltage')
        if self.voltage_fn is not None and self.voltage_fn.basis != 'FN':
            raise ValueError('voltage_fn requires FN basis')
        if self.voltage_ff is not None and self.voltage_ff.basis != 'FF':
            raise ValueError('voltage_ff requires FF basis')
        if not self.earthing_system.strip():
            raise ValueError('Earthing system cannot be blank or inferred')
        return self


class Board(Entity):
    room_id: UUID
    supply_id: UUID | None = None


class LoadPoint(Entity):
    room_id: UUID


class Load(Entity):
    load_point_id: UUID
    connection: Literal['SINGLE_PHASE_FN', 'SINGLE_PHASE_FF', 'THREE_PHASE']
    active_power: ActivePower | None = None
    reactive_power: ReactivePower | None = None
    apparent_power: ApparentPower | None = None
    design_current: Current | None = None

    @model_validator(mode='after')
    def declared_power_or_current(self):
        if all(getattr(self, field) is None for field in (
                'active_power', 'reactive_power', 'apparent_power', 'design_current')):
            raise ValueError('Load requires explicitly declared power or design current')
        return self


class Device(Entity):
    board_id: UUID
    kind: Literal['PROTECTION', 'SWITCHING', 'PROTECTION_AND_SWITCHING']
    nominal_current: Current | None = None
    source_reference: str | None = Field(default=None, min_length=1, max_length=500)


class Circuit(Entity):
    design_current: Current
    voltage: Voltage
    phases: Annotated[Literal[1, 3], BeforeValidator(_strict_phases)] = 1
    board_id: UUID
    device_id: UUID
    kind: Literal['TERMINAL', 'FEEDER']
    load_ids: list[UUID] = Field(default_factory=list)
    downstream_board_id: UUID | None = None

    @model_validator(mode='after')
    def terminal_or_feeder(self):
        if self.phases == 3 and self.voltage.basis != 'FF':
            raise ValueError('Three-phase circuit requires line-line voltage basis FF')
        if self.kind == 'TERMINAL':
            if not self.load_ids or self.downstream_board_id is not None:
                raise ValueError('Terminal circuit requires loads and no downstream board')
        elif self.load_ids or self.downstream_board_id is None:
            raise ValueError('Feeder circuit requires downstream board and no terminal loads')
        if len(self.load_ids) != len(set(self.load_ids)):
            raise ValueError('Circuit contains duplicate load references')
        return self


class InstallationConditions(DomainModel):
    installation_method: str = Field(min_length=1, max_length=200)
    medium: Literal['AIR', 'GROUND', 'OTHER_DECLARED']
    ambient_temperature: Temperature
    conductor_temperature: Temperature | None = None
    grouped_circuits: int = Field(gt=0, strict=True)
    solar_exposure: bool = Field(strict=True)
    additional_conditions: str | None = Field(default=None, min_length=1, max_length=1000)

    @field_validator('installation_method')
    @classmethod
    def method_not_blank(cls, value):
        if not value.strip():
            raise ValueError('Installation method cannot be inferred from blank text')
        return value.strip()


class CableRun(Entity):
    circuit_id: UUID
    segment_ids: list[UUID] = Field(min_length=1)
    section: CrossSection
    material: Literal['Cu', 'Al', 'OTHER_DECLARED']
    insulation: str = Field(min_length=1, max_length=100)

    @field_validator('insulation')
    @classmethod
    def insulation_not_blank(cls, value):
        if not value.strip():
            raise ValueError('Insulation cannot be blank')
        return value.strip()

    @field_validator('segment_ids')
    @classmethod
    def unique_segments(cls, value):
        if len(value) != len(set(value)):
            raise ValueError('Cable run contains duplicate segment references')
        return value


class Segment(Entity):
    cable_run_id: UUID
    length: Length
    conditions: InstallationConditions
    impedance: ImpedancePerLength | None = None


class Revision(Entity):
    sequence: int = Field(gt=0, strict=True)
    parent_revision_id: UUID | None = None
    input_sha256: str = Field(pattern=r'^[0-9a-f]{64}$')


class CalculationRun(Entity):
    revision_id: UUID
    project_revision: int = Field(ge=1, strict=True)
    circuit_id: UUID
    input_sha256: str = Field(pattern=r'^[0-9a-f]{64}$')
    output_sha256: str | None = Field(default=None, pattern=r'^[0-9a-f]{64}$')
    algorithm_version: str = Field(min_length=1, max_length=100)
    rule_version: str = Field(min_length=1, max_length=100)
    state: Literal['VALID', 'PENDING', 'INVALID', 'STALE']
    normative_conformity_verified: Literal[False] = False

    @model_validator(mode='after')
    def valid_result_requires_digest(self):
        if self.state == 'VALID' and self.output_sha256 is None:
            raise ValueError('VALID calculation run requires output digest')
        return self


class Installation(DomainModel):
    schema_version: Literal['SIE_INSTALLATION_V1'] = 'SIE_INSTALLATION_V1'
    project: Project
    buildings: list[Building] = Field(default_factory=list)
    floors: list[Floor] = Field(default_factory=list)
    rooms: list[Room] = Field(default_factory=list)
    supplies: list[Supply] = Field(default_factory=list)
    boards: list[Board] = Field(default_factory=list)
    load_points: list[LoadPoint] = Field(default_factory=list)
    loads: list[Load] = Field(default_factory=list)
    devices: list[Device] = Field(default_factory=list)
    circuits: list[Circuit] = Field(default_factory=list)
    cable_runs: list[CableRun] = Field(default_factory=list)
    segments: list[Segment] = Field(default_factory=list)
    revisions: list[Revision] = Field(default_factory=list)
    calculation_runs: list[CalculationRun] = Field(default_factory=list)

    @model_validator(mode='after')
    def references_and_topology(self):
        names = ('buildings', 'floors', 'rooms', 'supplies', 'boards', 'load_points',
                 'loads', 'devices', 'circuits', 'cable_runs', 'segments', 'revisions',
                 'calculation_runs')
        ids = {self.project.id}
        indexed = {}
        for name in names:
            indexed[name] = {}
            for entity in getattr(self, name):
                if entity.project_id != self.project.id:
                    raise ValueError(f'{name}: entity belongs to another project')
                if entity.id in ids:
                    raise ValueError('Entity UUIDs must be unique across aggregate')
                ids.add(entity.id)
                indexed[name][entity.id] = entity

        def require(collection, reference):
            if reference not in indexed[collection]:
                raise ValueError(f'Orphan reference to {collection}: {reference}')
            return indexed[collection][reference]

        for floor in self.floors:
            require('buildings', floor.building_id)
        for room in self.rooms:
            require('floors', room.floor_id)
        for board in self.boards:
            require('rooms', board.room_id)
            if board.supply_id is not None:
                require('supplies', board.supply_id)
        for point in self.load_points:
            require('rooms', point.room_id)
        for load in self.loads:
            require('load_points', load.load_point_id)
        for device in self.devices:
            require('boards', device.board_id)

        incoming = {board.id: [] for board in self.boards}
        graph = {board.id: [] for board in self.boards}
        used_loads, used_devices = set(), set()
        for circuit in self.circuits:
            require('boards', circuit.board_id)
            device = require('devices', circuit.device_id)
            if device.board_id != circuit.board_id:
                raise ValueError('Circuit device must belong to its origin board')
            if device.id in used_devices:
                raise ValueError('Device cannot originate multiple circuits')
            used_devices.add(device.id)
            for load_id in circuit.load_ids:
                load = require('loads', load_id)
                expected_connection = ('THREE_PHASE' if circuit.phases == 3 else
                                       'SINGLE_PHASE_' + circuit.voltage.basis)
                if load.connection != expected_connection:
                    raise ValueError('Load connection differs from circuit phases/voltage basis')
                if load_id in used_loads:
                    raise ValueError('Load cannot belong to multiple circuits')
                used_loads.add(load_id)
            if circuit.downstream_board_id is not None:
                require('boards', circuit.downstream_board_id)
                incoming[circuit.downstream_board_id].append(circuit.id)
                graph[circuit.board_id].append(circuit.downstream_board_id)
        for board in self.boards:
            upstream = int(board.supply_id is not None) + len(incoming[board.id])
            if upstream != 1:
                raise ValueError('Board requires exactly one supply or incoming feeder')
        if used_loads != set(indexed['loads']):
            raise ValueError('Every load requires a terminal circuit')
        if used_devices != set(indexed['devices']):
            raise ValueError('Every device requires its downstream circuit')
        used_supplies = {board.supply_id for board in self.boards if board.supply_id is not None}
        if used_supplies != set(indexed['supplies']):
            raise ValueError('Every supply requires a root board')

        # Board graph has in-degree exactly one except supply roots. Kahn's
        # algorithm avoids recursion limits for large but valid installations.
        degree = {key: len(incoming[key]) for key in graph}
        queue = [key for key, count in degree.items() if count == 0]
        source_by_board = {board.id: board.supply_id for board in self.boards
                           if board.supply_id is not None}
        phases_by_board = {board.id: indexed['supplies'][board.supply_id].phases
                           for board in self.boards if board.supply_id is not None}
        visited = 0
        while queue:
            key = queue.pop()
            visited += 1
            for child in graph[key]:
                source_by_board[child] = source_by_board[key]
                feeder = indexed['circuits'][incoming[child][0]]
                phases_by_board[child] = min(phases_by_board[key], feeder.phases)
                degree[child] -= 1
                if degree[child] == 0:
                    queue.append(child)
        if visited != len(graph):
            raise ValueError('Electrical topology must be acyclic')
        for circuit in self.circuits:
            supply = indexed['supplies'][source_by_board[circuit.board_id]]
            if circuit.phases > phases_by_board[circuit.board_id]:
                raise ValueError('Circuit phases exceed supply or ancestral feeder phases')
            nominal = supply.voltage_fn if circuit.voltage.basis == 'FN' else supply.voltage_ff
            if nominal is None or nominal.value != circuit.voltage.value:
                raise ValueError('Circuit nominal voltage differs from its declared ancestral supply')

        runs_for_circuits = set()
        used_segments = set()
        for run in self.cable_runs:
            require('circuits', run.circuit_id)
            runs_for_circuits.add(run.circuit_id)
            for segment_id in run.segment_ids:
                segment = require('segments', segment_id)
                if segment.cable_run_id != run.id:
                    raise ValueError('Segment does not belong to the declaring cable run')
                board_id = indexed['circuits'][run.circuit_id].board_id
                supply = indexed['supplies'][source_by_board[board_id]]
                if segment.impedance is not None and segment.impedance.frequency_hz != supply.frequency_hz:
                    raise ValueError('Segment impedance frequency differs from ancestral supply')
                if segment_id in used_segments:
                    raise ValueError('Segment cannot be shared across cable runs')
                used_segments.add(segment_id)
        if runs_for_circuits != set(indexed['circuits']):
            raise ValueError('Every circuit requires an explicitly segmented cable run')
        if used_segments != set(indexed['segments']):
            raise ValueError('Every segment requires a declaring cable run')
        for segment in self.segments:
            require('cable_runs', segment.cable_run_id)
        sequences = set()
        for revision in self.revisions:
            if revision.sequence > self.project.revision:
                raise ValueError('Revision sequence exceeds current project revision')
            if revision.sequence in sequences:
                raise ValueError('Revision sequence must be unique')
            sequences.add(revision.sequence)
            if revision.parent_revision_id is not None:
                parent = require('revisions', revision.parent_revision_id)
                if parent.sequence >= revision.sequence:
                    raise ValueError('Revision parent must precede child')
        for run in self.calculation_runs:
            revision = require('revisions', run.revision_id)
            if revision.sequence != run.project_revision or run.project_revision > self.project.revision:
                raise ValueError('Calculation run revision is inconsistent with project history')
            require('circuits', run.circuit_id)
        return self
