"""Governança normativa consultiva: metadados versionados, liberação sempre bloqueada."""
from dataclasses import dataclass
from datetime import date
from importlib.resources import files
import json
from typing import Optional

@dataclass(frozen=True)
class NormativeRecord:
    id: str
    document: str
    edition: str
    subject: str
    revision: int = 1
    official_url: Optional[str] = None
    official_publication_date: Optional[date] = None
    license_status: str = "NAO_CONFERIDA"
    typologies: tuple[str, ...] = ("residencial", "comercial", "predial")
    uf: Optional[str] = None
    distributor: Optional[str] = None
    effective_from: Optional[date] = None
    effective_until: Optional[date] = None
    verified_data: bool = False

def load_registry() -> tuple[NormativeRecord, ...]:
    """Importar metadados revisados no Git; nenhum campo confere homologação."""
    path = files("sie_api").joinpath("data", "normative_registry.json")
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or data.get("registry_state") != "NAO_HOMOLOGADO":
        raise ValueError("Registro normativo incompatível ou estado inválido")
    items = data.get("records")
    if not isinstance(items, list) or not items:
        raise ValueError("Registro normativo vazio")
    ids = set()
    records = []
    for raw in items:
        if raw["id"] in ids:
            raise ValueError("ID normativo duplicado")
        ids.add(raw["id"])
        if raw.get("verified_data") is not False or raw.get("revision", 0) < 1:
            raise ValueError("Fonte não homologada não pode ser importada como verificada")
        item = dict(raw)
        item["typologies"] = tuple(item["typologies"])
        for key in ("effective_from", "effective_until", "official_publication_date"):
            if item.get(key):
                item[key] = date.fromisoformat(item[key])
        records.append(NormativeRecord(**item))
    return tuple(records)

RECORDS = load_registry()

@dataclass(frozen=True)
class Context:
    typology: str
    uf: str
    voltage_v: float
    reference_date: date
    distributor: Optional[str] = None
    material: Optional[str] = None
    installation_method: Optional[str] = None
    use: Optional[str] = None

def inspect_record(record: NormativeRecord, ctx: Context) -> dict:
    """Somente metadados confiáveis do servidor; nunca flags de aprovação do cliente."""
    reasons = []
    if ctx.typology not in record.typologies:
        return _decision(record, "NAO_APLICAVEL", ["TIPOLOGIA_FORA_DO_RECORTE"])
    if record.uf is not None and ctx.uf != record.uf:
        return _decision(record, "NAO_APLICAVEL", ["UF_FORA_DO_RECORTE"])
    if record.effective_from and ctx.reference_date < record.effective_from:
        return _decision(record, "NAO_APLICAVEL", ["ANTES_DA_VIGENCIA"])
    if record.effective_until and ctx.reference_date > record.effective_until:
        # NR-10 2026 prevê regra transitória para instalações existentes.
        # Não presumir que o regime anterior deixou de importar para todos os casos.
        if record.id == "NR-10-ATE-2027":
            return _decision(record, "PENDENTE", ["TRANSICAO_INSTALACOES_EXISTENTES_A_CONFERIR"])
        return _decision(record, "NAO_APLICAVEL", ["APOS_A_VIGENCIA"])
    if record.distributor is not None and ctx.distributor is None:
        return _decision(record, "PENDENTE", ["DISTRIBUIDORA_NAO_INFORMADA"])
    if record.distributor is not None and ctx.distributor != record.distributor:
        return _decision(record, "NAO_APLICAVEL", ["DISTRIBUIDORA_DIFERENTE"])
    if not record.verified_data:
        reasons.append("FONTE_E_REGRAS_NAO_HOMOLOGADAS")
    if record.distributor:
        reasons.append("AREA_CONCESSAO_NAO_VERIFICADA")
    if record.document.startswith("ABNT NBR 5419"):
        reasons.append("AVALIACAO_SPDA_PENDENTE")
    if record.document == "NR-10":
        reasons.append("TRANSICAO_E_EXCECOES_A_VERIFICAR")
    return _decision(record, "BLOQUEADO", reasons)

def _decision(record: NormativeRecord, status: str, reasons: list[str]) -> dict:
    return {"rule_id": record.id, "revision": record.revision, "document": record.document, "edition": record.edition,
            "status": status, "reasons": reasons,
            "normative_approved": False, "verified_data": False}
