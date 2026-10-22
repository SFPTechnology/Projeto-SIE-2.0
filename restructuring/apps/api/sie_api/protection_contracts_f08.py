"""F08 typed study contracts. Decimal text; declarations never authenticate sources."""
from decimal import Decimal
from typing import Literal
from uuid import UUID
from pydantic import Field, model_validator, BaseModel
from .domain.installation import DomainModel, Positive, NonNegative, Magnitude
from .conductor_f07 import Study as ConductorStudy, Evidence

class Device(DomainModel):
    id: UUID
    family: Literal['MCB','FUSE','RCD','SPD']
    board_id: UUID | None = None
    manufacturer: str | None = Field(default=None,min_length=1,max_length=200)
    model: str | None = Field(default=None,min_length=1,max_length=200)
    edition: str | None = Field(default=None,min_length=1,max_length=100)
    evidence: Evidence | None = None
    catalog_key: str | None = Field(default=None,min_length=1,max_length=200)
    nominal_current_a: Positive | None = None
    i2_a: Positive | None = None
    rated_voltage_v: Positive | None = None
    breaking_capacity_a: Positive | None = None
    breaking_standard: str | None = Field(default=None,min_length=1,max_length=100)
    curve: str | None = Field(default=None,min_length=1,max_length=100)
    poles: int | None = Field(default=None,ge=1,le=4,strict=True)

class FaultScenario(DomainModel):
    id: str = Field(min_length=1,max_length=100)
    circuit_id: UUID
    segment_id: UUID | None = None
    kind: Literal['MAX','MIN']
    fault_type: Literal['THREE_PHASE','PHASE_NEUTRAL','PHASE_PE','PHASE_PHASE']
    voltage_v: Positive
    voltage_factor: Positive = Field(le=2)
    source_r_ohm: NonNegative
    source_x_ohm: NonNegative
    path_r_ohm: NonNegative
    path_x_ohm: NonNegative
    source_evidence: Evidence
    path_evidence: Evidence
    model: Literal['SINGLE_RADIAL_THEVENIN_NO_OTHER_CONTRIBUTIONS']
    additional_contributions: bool = Field(strict=True)
    source_voltage_basis: Literal['FN','FF']
    location: Literal['DEVICE','SEGMENT_END']
    @model_validator(mode='after')
    def nonzero(self):
        if self.location=='SEGMENT_END' and self.segment_id is None:
            raise ValueError('Falta no fim de trecho exige segment_id real')
        if self.location=='DEVICE' and self.segment_id is not None:
            raise ValueError('Falta no dispositivo não recebe trecho final')
        if self.source_r_ohm+self.source_x_ohm+self.path_r_ohm+self.path_x_ohm == 0:
            raise ValueError('Impedância nula não define curto finito')
        if self.fault_type=='THREE_PHASE' and self.source_voltage_basis!='FF':
            raise ValueError('Curto trifásico exige tensão FF')
        if self.fault_type in ('PHASE_NEUTRAL','PHASE_PE') and self.source_voltage_basis!='FN':
            raise ValueError('Falta fase-neutro/PE exige tensão FN')
        if self.fault_type=='PHASE_PHASE' and self.source_voltage_basis!='FF':
            raise ValueError('Falta fase-fase exige tensão FF e impedância de laço completo')
        return self

class Thermal(DomainModel):
    device_id: UUID | None = None
    fault_scenario_id: str | None = None
    maximum_current_a: Positive | None = None
    k_a_sqrt_s_mm2: Positive
    duration_s: Positive
    energy_a2s: Positive | None = None
    effective_current_a: Positive | None = None
    asymmetry_negligible: bool | None = Field(default=None,strict=True)
    evidence: Evidence
    material: Literal['Cu','Al','OTHER_DECLARED']
    insulation: str = Field(min_length=1,max_length=100)
    initial_temperature_c: Magnitude
    final_temperature_c: Magnitude
    @model_validator(mode='after')
    def coherent(self):
        if (self.energy_a2s is None)==(self.effective_current_a is None):
            raise ValueError('Informe integral passante OU corrente eficaz, exclusivamente')
        if self.final_temperature_c<=self.initial_temperature_c:
            raise ValueError('Temperatura final deve exceder inicial')
        return self

class Trip(DomainModel):
    maximum_current_a: Positive | None = None
    at_current_a: Positive
    max_time_s: Positive
    evidence: Evidence
    # A bound from a curve is not extrapolated below its stated current.
    voltage_v: Positive

class Residual(DomainModel):
    device_id: UUID
    sensitivity_a: Positive
    required_max_sensitivity_a: Positive | None = None
    nominal_current_a: Positive
    required_type: Literal['AC','A','F','B'] | None = None
    actual_type: Literal['AC','A','F','B']
    all_live_conductors: bool | None = Field(default=None,strict=True)
    pe_separated_upstream: bool | None = Field(default=None,strict=True)
    max_time_s: Positive | None = None
    conditional_short_circuit_a: Positive | None = None
    backup_device_id: UUID | None = None
    backup_voltage_v: Positive | None = None
    backup_protection_verified: bool | None = Field(default=None,strict=True)
    evidence: Evidence

class Surge(DomainModel):
    device_id: UUID
    uc_v: Positive
    minimum_uc_v: Positive
    up_v: Positive
    equipment_withstand_v: Positive
    spd_type: Literal['T1','T2','T3','T1_T2']
    required_type: Literal['T1','T2','T3','T1_T2']
    backup_coordinated: bool | None = Field(default=None,strict=True)
    bonding_verified: bool | None = Field(default=None,strict=True)
    connection_length_verified: bool | None = Field(default=None,strict=True)
    nominal_discharge_a: Positive | None = None
    required_nominal_discharge_a: Positive | None = None
    impulse_current_a: Positive | None = None
    required_impulse_current_a: Positive | None = None
    max_discharge_a: Positive | None = None
    required_max_discharge_a: Positive | None = None
    earthing: Literal['TN_S','TN_C','TN_C_S','TT','IT'] | None = None
    required_connection_scheme: str | None = Field(default=None,min_length=1,max_length=200)
    connection_scheme_declared: str | None = Field(default=None,min_length=1,max_length=200)
    evidence: Evidence

class CircuitProtection(DomainModel):
    device_id: UUID
    fault_max_id: str | None = None
    fault_min_id: str | None = None
    overload_hours_year: NonNegative | None = None
    overload_hours_life: NonNegative | None = None
    thermal: Thermal | None = None
    pe_thermal: Thermal | None = None
    neutral_thermal: Thermal | None = None
    trip: Trip | None = None
    earthing: Literal['TN_S','TN_C','TN_C_S','TT','IT']
    disconnection_limit_s: Positive | None = None
    disconnection_evidence: Evidence | None = None
    touch_limit_v: Positive | None = None
    earth_resistance_ohm: Positive | None = None
    bonding_verified: bool | None = Field(default=None,strict=True)
    rcd_required: bool | None = Field(default=None,strict=True)
    rcd: Residual | None = None
    spd_required: bool | None = Field(default=None,strict=True)
    spd: Surge | None = None

class Coordination(DomainModel):
    catalog_key: str | None = Field(default=None,min_length=1,max_length=200)
    upstream_circuit_id: UUID
    downstream_circuit_id: UUID
    upstream_device_id: UUID
    downstream_device_id: UUID
    voltage_v: Positive
    selectivity_limit_a: Positive | None = None
    total_selectivity: bool = Field(default=False,strict=True)
    evidence: Evidence | None = None

class Study(DomainModel):
    id: UUID
    conductor_study: ConductorStudy
    circuits: dict[UUID,CircuitProtection] = Field(default_factory=dict)
    fault_scenarios: list[FaultScenario] = Field(default_factory=list,max_length=1000)
    devices: list[Device] = Field(default_factory=list,max_length=1000)
    coordination: list[Coordination] = Field(default_factory=list,max_length=1000)
    max_iterations: int = Field(default=20,ge=1,le=100,strict=True)
    candidate_device_ids: dict[UUID,list[UUID]] = Field(default_factory=dict)
    selection_variants: list['Study'] = Field(default_factory=list,max_length=100)
    @model_validator(mode='after')
    def references(self):
        if any(v.selection_variants for v in self.selection_variants):
            raise ValueError('Variantes aninhadas não permitidas; busca finita de um nível')
        if len({v.id for v in self.selection_variants})!=len(self.selection_variants):
            raise ValueError('Variantes duplicadas')
        inst=self.conductor_study.topology.installation
        if any(v.conductor_study.topology.installation.project.id!=inst.project.id for v in self.selection_variants):
            raise ValueError('Variante de outro projeto')
        circuits={c.id:c for c in inst.circuits}; device_ids={d.id for d in inst.devices}
        devices={d.id:d for d in self.devices}; faults={f.id:f for f in self.fault_scenarios}
        if len(devices)!=len(self.devices) or len(faults)!=len(self.fault_scenarios):
            raise ValueError('Dispositivo/cenário duplicado')
        if not set(self.circuits).issubset(circuits) or not set(self.candidate_device_ids).issubset(circuits):
            raise ValueError('Circuito órfão')
        boards={b.id:b for b in inst.boards}
        incoming={c.downstream_board_id:c for c in inst.circuits if c.kind=='FEEDER'}
        supplies={x.id:x for x in inst.supplies}
        def supply_for(cid):
            board=boards[circuits[cid].board_id]
            while board.supply_id is None: board=boards[incoming[board.id].board_id]
            return supplies[board.supply_id]
        for d in self.devices:
            if d.family in ('MCB','FUSE') and d.id not in device_ids:
                raise ValueError('Proteção de sobrecorrente não cadastrada na topologia')
            if d.family in ('RCD','SPD') and d.board_id not in boards:
                raise ValueError('DR/DPS exige vínculo a quadro real')
        for cid,cp in self.circuits.items():
            if cp.device_id!=circuits[cid].device_id or cp.device_id not in devices:
                raise ValueError('Proteção deve corresponder ao dispositivo do circuito')
            if devices[cp.device_id].family not in ('MCB','FUSE'):
                raise ValueError('Proteção de sobrecorrente exige disjuntor/fusível')
            for fid,kind in ((cp.fault_max_id,'MAX'),(cp.fault_min_id,'MIN')):
                if fid is not None and (fid not in faults or faults[fid].circuit_id!=cid or faults[fid].kind!=kind):
                    raise ValueError('Cenário de falta não corresponde ao circuito/tipo')
            for obj,family in ((cp.rcd,'RCD'),(cp.spd,'SPD')):
                if obj and (obj.device_id not in devices or devices[obj.device_id].family!=family or devices[obj.device_id].board_id!=circuits[cid].board_id):
                    raise ValueError('DR/DPS exige dispositivo compatível cadastrado')
        for f in self.fault_scenarios:
            if f.circuit_id not in circuits: raise ValueError('Falta em circuito inexistente')
            supply=supply_for(f.circuit_id)
            voltage=supply.voltage_fn if f.source_voltage_basis=='FN' else supply.voltage_ff
            if voltage is not None and voltage.value!=f.voltage_v:
                raise ValueError('Tensão de falta diverge da fonte cadastrada')
            if f.fault_type=='THREE_PHASE' and circuits[f.circuit_id].phases!=3:
                raise ValueError('Falta trifásica em circuito não trifásico')
            runs=[r for r in inst.cable_runs if r.circuit_id==f.circuit_id]
            if f.kind=='MIN' and f.location!='SEGMENT_END':
                raise ValueError('Falta mínima exige fim de trecho explicitamente identificado')
            if f.kind=='MIN' and (len(runs)!=1 or f.segment_id!=runs[0].segment_ids[-1]):
                raise ValueError('Mínima deve cobrir fim do percurso único; paralelos/alternativos fora do domínio')
            if f.segment_id is not None and f.segment_id not in {s for r in runs for s in r.segment_ids}:
                raise ValueError('Trecho de falta não pertence ao circuito')
        for pair in self.coordination:
            if pair.upstream_circuit_id not in circuits or pair.downstream_circuit_id not in circuits:
                raise ValueError('Par de coordenação órfão')
            if pair.upstream_circuit_id==pair.downstream_circuit_id:
                raise ValueError('Coordenação exige circuitos distintos')
            if pair.upstream_device_id!=circuits[pair.upstream_circuit_id].device_id or pair.downstream_device_id!=circuits[pair.downstream_circuit_id].device_id:
                raise ValueError('Par de dispositivos não corresponde aos circuitos')
        for ids in self.candidate_device_ids.values():
            if len(ids)>100 or len(ids)!=len(set(ids)) or not set(ids).issubset(devices):
                raise ValueError('Candidatos devem ser únicos, conhecidos e no máximo 100')
        def bounds(v):
            if isinstance(v,Decimal) and (len(v.as_tuple().digits)>30 or abs(v.as_tuple().exponent)>30):
                raise ValueError('F08 suporta até30 dígitos/expoente30')
            if isinstance(v,BaseModel):
                for key in type(v).model_fields: bounds(getattr(v,key))
            elif isinstance(v,dict):
                for x in v.values(): bounds(x)
            elif isinstance(v,list):
                for x in v: bounds(x)
        bounds(self)
        return self
