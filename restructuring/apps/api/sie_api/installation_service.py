"""F02 snapshots, calculation references and explicit legacy compatibility boundary.

Pure application operations: no database, HTTP, browser or normative approval.
Snapshots retain canonical serialized bytes, never a mutable object reference.
"""
from decimal import Decimal, localcontext
from hashlib import sha256
from inspect import getsource
import json
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from .domain.installation import Installation
from .analysis_contracts import AnaliseCircuito
from .application import analisar_circuito
from . import application
from .domain import engines
from . import cell_bindings, protection_checks, complementary_checks, protection_extended, voltage_checks

ALGORITHM_VERSION = 'F02_LEGACY_ADAPTER_V1'


def canonical_json(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=False, allow_nan=False)


def digest(value):
    return sha256(canonical_json(value).encode()).hexdigest()


class InstallationSnapshot(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)
    schema_version: Literal['SIE_SNAPSHOT_V1'] = 'SIE_SNAPSHOT_V1'
    project_id: UUID
    revision: int = Field(ge=1, strict=True)
    canonical_json: str
    snapshot_sha256: str = Field(pattern=r'^[0-9a-f]{64}$')

    @model_validator(mode='after')
    def verify(self):
        raw = json.loads(self.canonical_json)
        installation = Installation.model_validate(raw)
        if canonical_json(installation.model_dump(mode='json')) != self.canonical_json:
            raise ValueError('Snapshot não está na representação canônica do modelo')
        if sha256(self.canonical_json.encode()).hexdigest() != self.snapshot_sha256:
            raise ValueError('Hash do snapshot inválido')
        if installation.project.id != self.project_id or installation.project.revision != self.revision:
            raise ValueError('Snapshot diverge da identidade/revisão do projeto')
        return self


def create_snapshot(installation: Installation):
    text = canonical_json(installation.model_dump(mode='json'))
    return InstallationSnapshot(project_id=installation.project.id, revision=installation.project.revision,
                                canonical_json=text, snapshot_sha256=sha256(text.encode()).hexdigest())


class RevisionReference(BaseModel):
    """Documents and calculations must reference the exact same project snapshot."""
    model_config = ConfigDict(extra='forbid', frozen=True)
    project_id: UUID
    revision: int = Field(ge=1, strict=True)
    snapshot_sha256: str = Field(pattern=r'^[0-9a-f]{64}$')


def require_same_revision(snapshot: InstallationSnapshot, reference: RevisionReference):
    if (snapshot.project_id, snapshot.revision, snapshot.snapshot_sha256) != (
            reference.project_id, reference.revision, reference.snapshot_sha256):
        raise ValueError('Documento/cálculo não referencia o mesmo snapshot de projeto')


class CalculationRecord(RevisionReference):
    schema_version: Literal['SIE_CALCULATION_RECORD_V1'] = 'SIE_CALCULATION_RECORD_V1'
    circuit_id: UUID
    algorithm_version: str = Field(min_length=1, max_length=200)
    rule_version: str = Field(min_length=1, max_length=200)
    input_sha256: str = Field(pattern=r'^[0-9a-f]{64}$')
    result_json: str | None = None
    result_sha256: str | None = Field(default=None, pattern=r'^[0-9a-f]{64}$')
    normative_conformity_verified: Literal[False] = False

    @model_validator(mode='after')
    def result_integrity(self):
        if (self.result_json is None) != (self.result_sha256 is None):
            raise ValueError('Resultado e hash devem existir juntos')
        if self.result_json is not None:
            result = json.loads(self.result_json)
            if (canonical_json(result) != self.result_json or
                    sha256(self.result_json.encode()).hexdigest() != self.result_sha256):
                raise ValueError('Integridade do resultado comprometida')
            if not isinstance(result, dict):
                raise ValueError('Resultado de cálculo deve ser objeto JSON')
            required = {'status_engenharia', 'liberado_para_uso_normativo', 'condutor', 'disjuntor', 'queda_tensao'}
            if not required.issubset(result) or any(not isinstance(result[k], dict) for k in ('condutor', 'disjuntor', 'queda_tensao')):
                raise ValueError('Resultado não corresponde ao contrato do motor legado')
            for group, field in [('condutor', 'secao_mm2'), ('disjuntor', 'corrente_a'), ('queda_tensao', 'queda_percentual')]:
                value = result[group].get(field)
                if isinstance(value, bool) or not isinstance(value, (int, float)) or not Decimal(str(value)).is_finite() or (value < 0 if field == 'queda_percentual' else value <= 0):
                    raise ValueError('Resultado contém grandeza inválida')
            if result.get('status_engenharia') not in ('PENDENTE', 'BLOQUEADO'):
                raise ValueError('Estado de engenharia inválido no resultado legado')
            if result.get('liberado_para_uso_normativo') is not False:
                raise ValueError('Adaptador F02 não concede aprovação normativa')
        return self


def calculation_status(record: CalculationRecord, snapshot: InstallationSnapshot,
                       algorithm_version: str, rule_version: str, input_sha256: str):
    installation = Installation.model_validate_json(snapshot.canonical_json)
    if record.project_id != snapshot.project_id or record.circuit_id not in {c.id for c in installation.circuits}:
        return {'status': 'INVALID', 'reason': 'Projeto/circuito não pertence à revisão consultada'}
    if (record.snapshot_sha256 != snapshot.snapshot_sha256 or record.revision != snapshot.revision or
            record.algorithm_version != algorithm_version or record.rule_version != rule_version or
            record.input_sha256 != input_sha256):
        return {'status': 'STALE', 'reason': 'Modelo, algoritmo, regra ou entrada mudou; recalcular explicitamente'}
    if record.result_json is None:
        return {'status': 'PENDING', 'reason': 'Cálculo ainda não executado'}
    return {'status': 'VALID', 'reason': 'Integridade e dependências computacionais correspondem; não é homologação'}


def algorithm_identity():
    source = [getsource(analisar_circuito), getsource(analyze_legacy)]
    source.extend(getsource(module) for module in
                  (application, engines, cell_bindings, protection_checks, complementary_checks,
                   protection_extended, voltage_checks))
    source.append(canonical_json([str(value) for value in application.CATALOGO_DISJUNTORES]))
    return ALGORITHM_VERSION + ':' + sha256('\n'.join(source).encode()).hexdigest()


def analyze_legacy(snapshot: InstallationSnapshot, circuit_id: UUID, parameters: AnaliseCircuito,
                   rule_version: str):
    installation = Installation.model_validate_json(snapshot.canonical_json)
    circuits = [c for c in installation.circuits if c.id == circuit_id]
    if not circuits:
        raise ValueError('Circuito não pertence ao snapshot')
    circuit = circuits[0]
    if circuit.design_current is None or circuit.voltage is None:
        raise ValueError('Adaptador exige corrente e tensão explícitas no circuito canônico')
    if getattr(circuit, 'phases', None) == 3:
        raise ValueError('Motor legado monofásico não suporta circuito trifásico')
    runs = [r for r in installation.cable_runs if r.circuit_id == circuit.id]
    if len(runs) != 1:
        raise ValueError('Adaptador legado exige exatamente um percurso sem ramificações')
    by_id = {s.id: s for s in installation.segments}
    segments = [by_id[key] for key in runs[0].segment_ids]
    if any(segment.impedance is not None for segment in segments):
        raise ValueError('Impedância canônica exige motor com mapeamento explícito; adaptador resistivo não pode ignorá-la')
    lengths = [segment.length.value for segment in segments]
    with localcontext() as ctx:
        ctx.prec = max(1, max(value.adjusted() for value in lengths)) - min(value.as_tuple().exponent for value in lengths) + len(str(len(lengths))) + 2
        length = sum(lengths, Decimal('0'))
    expected = (circuit.design_current.value, circuit.voltage.value, length)
    actual = (Decimal(str(parameters.corrente_a)), Decimal(str(parameters.tensao_v)),
              Decimal(str(parameters.comprimento_m)))
    if expected != actual:
        raise ValueError('Grandezas legadas divergem da corrente/tensão/percurso canônicos')
    conditions = [by_id[key].conditions.model_dump(mode='json') for key in runs[0].segment_ids]
    if len({canonical_json(c) for c in conditions}) > 1:
        raise ValueError('Condições distintas por trecho exigem motor segmentado; não usar fator global legado')
    raw = parameters.model_dump(mode='json')
    if any(raw.get(key) is not None for key in ('protecao_sobrecarga', 'protecao_curto_circuito', 'estudo_coordenacao', 'queda_impedancia')):
        raise ValueError('Verificações complementares exigem mapeamento ao modelo; use contrato F01 separado')
    if parameters.vinculo_celulas is not None:
        raise ValueError('Vínculo normativo por trecho exige mapeamento explícito; use contrato F01 separado')
    result = analisar_circuito(raw)
    if Decimal(str(result['condutor']['secao_mm2'])) != runs[0].section.value:
        raise ValueError('Seção selecionada pelo legado difere do cabo canônico; revisar o modelo explicitamente')
    device = next(device for device in installation.devices if device.id == circuit.device_id)
    if device.nominal_current is not None and device.nominal_current.value != Decimal(str(result['disjuntor']['corrente_a'])):
        raise ValueError('Disjuntor selecionado difere da corrente nominal do dispositivo canônico')
    text = canonical_json(result)
    return CalculationRecord(project_id=snapshot.project_id, revision=snapshot.revision,
        snapshot_sha256=snapshot.snapshot_sha256, circuit_id=circuit_id,
        algorithm_version=algorithm_identity(), rule_version=rule_version,
        input_sha256=digest(raw), result_json=text, result_sha256=sha256(text.encode()).hexdigest())
