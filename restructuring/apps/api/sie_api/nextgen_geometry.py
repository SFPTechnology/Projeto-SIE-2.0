"""SIE 2.0 greenfield: deterministic geometric inventory (not electrical approval)."""
from __future__ import annotations
import hashlib
import json
from decimal import Decimal, InvalidOperation
from uuid import UUID

class GeometryError(ValueError):
    """Invalid input geometry."""

def _object(value: object, label: str, allowed: set[str], required: set[str]) -> dict:
    if not isinstance(value, dict):
        raise GeometryError(f"{label}: objeto JSON esperado")
    missing = required - value.keys()
    extra = value.keys() - allowed
    if missing or extra:
        raise GeometryError(f"{label}: campos ausentes={sorted(missing)} desconhecidos={sorted(extra)}")
    return value

def _uuid(value: object, label: str) -> str:
    if not isinstance(value, str):
        raise GeometryError(f"{label}: UUID esperado")
    try:
        return str(UUID(value))
    except (ValueError, AttributeError) as exc:
        raise GeometryError(f"{label}: UUID invalido") from exc

def _decimal(value: object, label: str, *, positive: bool) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (str, int, float, Decimal)):
        raise GeometryError(f"{label}: numero decimal esperado")
    try:
        number = Decimal(str(value))
    except InvalidOperation as exc:
        raise GeometryError(f"{label}: numero decimal invalido") from exc
    if not number.is_finite() or number < 0 or (positive and number == 0):
        raise GeometryError(f"{label}: valor finito {'positivo' if positive else 'nao negativo'} exigido")
    return number

def _fmt(value: Decimal) -> str:
    return format(value.normalize(), "f")

def analyze_project(payload: object) -> dict:
    """Validate rectangular-room data and calculate geometric values via Decimal.

    No lighting, sockets, demand, protections or normative approval is inferred.
    """
    project = _object(payload, "projeto", {"project_id", "revision_id", "rooms"},
                      {"project_id", "revision_id", "rooms"})
    project_id = _uuid(project["project_id"], "project_id")
    revision_id = _uuid(project["revision_id"], "revision_id")
    rooms = project["rooms"]
    if not isinstance(rooms, list) or not 1 <= len(rooms) <= 500:
        raise GeometryError("rooms: lista de 1 a 500 ambientes exigida")
    seen: set[str] = set()
    normalized: list[dict] = []
    results: list[dict] = []
    for index, item in enumerate(rooms):
        label = f"rooms[{index}]"
        room = _object(item, label,
                       {"room_id", "name", "width_m", "length_m", "excluded_perimeter_m"},
                       {"room_id", "name", "width_m", "length_m"})
        room_id = _uuid(room["room_id"], f"{label}.room_id")
        if room_id in seen:
            raise GeometryError(f"{label}: room_id duplicado")
        seen.add(room_id)
        name = room["name"]
        if not isinstance(name, str) or not 1 <= len(name.strip()) <= 120:
            raise GeometryError(f"{label}.name: nome obrigatorio (1-120 caracteres)")
        name = name.strip()
        width = _decimal(room["width_m"], f"{label}.width_m", positive=True)
        length = _decimal(room["length_m"], f"{label}.length_m", positive=True)
        excluded = _decimal(room.get("excluded_perimeter_m", 0),
                            f"{label}.excluded_perimeter_m", positive=False)
        gross = 2 * (width + length)
        if excluded >= gross:
            raise GeometryError(f"{label}: perimetro excluido deve ser menor que o bruto")
        normalized.append({"room_id": room_id, "name": name, "width_m": _fmt(width),
                           "length_m": _fmt(length), "excluded_perimeter_m": _fmt(excluded)})
        results.append({"room_id": room_id, "name": name,
                        "area_m2": _fmt(width * length),
                        "gross_perimeter_m": _fmt(gross),
                        "useful_perimeter_m": _fmt(gross - excluded)})
    canonical = {"project_id": project_id, "revision_id": revision_id, "rooms": normalized}
    content = json.dumps(canonical, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
    return {"schema_version": 1, "project_id": project_id, "revision_id": revision_id,
            "geometry_assumption": "rectangular_only", "normative_status": "NOT_EVALUATED",
            "source_sha256": digest, "rooms": results}
