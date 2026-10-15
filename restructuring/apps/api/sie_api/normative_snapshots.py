"""F01: snapshot confiável do CATÁLOGO, não de regra aplicada nem cálculo homologado.

Isola as fontes versionadas do payload do cliente; nenhuma aprovação sai daqui.
A associação ao projeto é efetuada na mesma transação SQLite do salvamento.
"""
from dataclasses import asdict
from datetime import date
from hashlib import sha256
import json
from .domain.normative import load_registry


class SnapshotCorrompido(ValueError):
    pass


def serializar_catalogo() -> tuple[str, str]:
    """Captura metadados atuais do servidor, sem bytes licenciados de normas."""
    records = []
    for record in load_registry():
        if record.verified_data is not False:
            raise ValueError("Registro técnico não homologado não pode receber status aprovado")
        meta = asdict(record)
        for key in ("effective_from", "effective_until", "official_publication_date"):
            if isinstance(meta.get(key), date):
                meta[key] = meta[key].isoformat()
        meta["typologies"] = list(meta["typologies"])
        records.append(meta)
    content = {
        "schema_version": 1,
        "snapshot_kind": "CATALOG_METADATA_ONLY_NOT_RULES_USED",
        "normative_conformity_verified": False,
        "release_allowed": False,
        "rules": sorted(records, key=lambda r: r["id"]),
    }
    serialized = json.dumps(content, ensure_ascii=False, sort_keys=True,
                            separators=(",", ":"), allow_nan=False)
    return serialized, sha256(serialized.encode("utf-8")).hexdigest()


def validar_snapshot(serialized: str, digest: str) -> dict:
    actual = sha256(serialized.encode("utf-8")).hexdigest()
    if actual != digest:
        raise SnapshotCorrompido("Hash do snapshot normativo não confere")
    result = json.loads(serialized)
    if (result.get("schema_version") != 1 or
        result.get("snapshot_kind") != "CATALOG_METADATA_ONLY_NOT_RULES_USED" or
        result.get("normative_conformity_verified") is not False or
        result.get("release_allowed") is not False):
        raise SnapshotCorrompido("Formato ou estado do snapshot normativo inválido")
    return result


def diferenca_snapshot(antes: dict, depois: dict) -> dict:
    """Diferença de metadados, nunca nova certificação ou recálculo automático."""
    old = {r["id"]: r for r in antes["rules"]}
    new = {r["id"]: r for r in depois["rules"]}
    changes = []
    for key in sorted(set(old) | set(new)):
        if old.get(key) != new.get(key):
            changes.append({"id": key, "type": (
                "ADICIONADA" if key not in old else
                "REMOVIDA" if key not in new else "ALTERADA"),
                "old_revision": old[key].get("revision") if key in old else None,
                "new_revision": new[key].get("revision") if key in new else None})
    return {"changed": bool(changes), "changes": changes,
            "requires_technical_revalidation": bool(changes),
            "release_allowed": False, "recalculated_automatically": False}
