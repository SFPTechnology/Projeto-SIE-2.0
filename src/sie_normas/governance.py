"""Governança normativa conservadora: não inclui valores de tabelas técnicas."""
from dataclasses import dataclass
from datetime import date
from typing import Optional

@dataclass(frozen=True)
class Context:
    typology: str
    voltage_v: int
    state: str
    distributor: str
    on_date: date
    material: Optional[str] = None
    method: Optional[str] = None
    use: Optional[str] = None

@dataclass(frozen=True)
class Rule:
    rule_id: str
    revision: int
    source_id: str
    edition: str
    scope: str
    verified: bool = False
    approved: bool = False
    approver: Optional[str] = None
    effective_from: Optional[date] = None
    effective_until: Optional[date] = None
    typologies: tuple[str, ...] = ()
    states: tuple[str, ...] = ()
    distributors: tuple[str, ...] = ()
    min_voltage: Optional[int] = None
    max_voltage: Optional[int] = None
    material: Optional[str] = None
    method: Optional[str] = None
    use: Optional[str] = None
    superseded: bool = False

@dataclass(frozen=True)
class Decision:
    status: str
    reasons: tuple[str, ...]
    rule_id: str
    revision: int

def evaluate(rule: Rule, ctx: Context, *, source_verified: bool = False, conflict: bool = False) -> Decision:
    reasons = []
    if rule.typologies and ctx.typology not in rule.typologies: reasons.append("TIPOLOGIA_INCOMPATIVEL")
    if rule.states and ctx.state not in rule.states: reasons.append("UF_INCOMPATIVEL")
    if rule.distributors and ctx.distributor not in rule.distributors: reasons.append("DISTRIBUIDORA_INCOMPATIVEL")
    if rule.min_voltage is not None and ctx.voltage_v < rule.min_voltage: reasons.append("TENSAO_INFERIOR")
    if rule.max_voltage is not None and ctx.voltage_v > rule.max_voltage: reasons.append("TENSAO_SUPERIOR")
    for field in ("material", "method", "use"):
        expected = getattr(rule, field)
        if expected is not None and getattr(ctx, field) != expected: reasons.append(field.upper() + "_INCOMPATIVEL")
    if rule.effective_from is None or ctx.on_date < rule.effective_from: reasons.append("VIGENCIA_NAO_COMPROVADA")
    if rule.effective_until is not None and ctx.on_date > rule.effective_until: reasons.append("EDICAO_EXPIRADA")
    if rule.superseded: reasons.append("REGRA_SUPERADA")
    if reasons: return Decision("NAO_APLICAVEL", tuple(reasons), rule.rule_id, rule.revision)
    if conflict: return Decision("BLOQUEADO", ("CONFLITO_NORMATIVO",), rule.rule_id, rule.revision)
    if not source_verified or not rule.verified or not rule.approved or not rule.approver or not rule.edition:
        return Decision("BLOQUEADO", ("FONTE_OU_APROVACAO_PENDENTE",), rule.rule_id, rule.revision)
    return Decision("ELEGIVEL_PARA_CALCULO", (), rule.rule_id, rule.revision)

def snapshot(rule: Rule, source_sha256: str) -> dict:
    if len(source_sha256) != 64 or any(c not in "0123456789abcdef" for c in source_sha256):
        raise ValueError("SHA-256 inválido")
    return dict(rule_id=rule.rule_id, revision=rule.revision, source_id=rule.source_id,
                edition=rule.edition, source_sha256=source_sha256)
