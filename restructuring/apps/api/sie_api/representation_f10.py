"""Deterministic, revision-bound electrical drawing and report artifacts (F10).

This module renders only data supplied by the caller. It does not calculate
electrical compliance, infer geometry, or certify a design.
"""
from __future__ import annotations

from dataclasses import dataclass
from html import escape
from typing import Any


class ArtifactError(ValueError):
    """Raised when artifact inputs are incomplete or internally inconsistent."""


@dataclass(frozen=True)
class ArtifactContract:
    project_id: str
    revision_id: str
    calculation_run_id: str
    rule_version: str
    template_version: str

    def __post_init__(self) -> None:
        for name, value in self.__dict__.items():
            if not isinstance(value, str) or not value.strip():
                raise ArtifactError(f"{name} is required")


def _finite_number(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ArtifactError(f"{label} must be numeric")
    number = float(value)
    if number != number or number in (float("inf"), float("-inf")):
        raise ArtifactError(f"{label} must be finite")
    return number


def validate_snapshot(snapshot: dict[str, Any]) -> None:
    """Validate the minimal versioned graph contract used by F10 renderers."""
    if not isinstance(snapshot, dict):
        raise ArtifactError("snapshot must be an object")
    for key in ("project_id", "revision_id", "calculation_run_id", "rule_version"):
        if not isinstance(snapshot.get(key), str) or not snapshot[key].strip():
            raise ArtifactError(f"snapshot.{key} is required")
    elements = snapshot.get("elements")
    circuits = snapshot.get("circuits")
    if not isinstance(elements, list) or not isinstance(circuits, list):
        raise ArtifactError("elements and circuits must be lists")
    ids: set[str] = set()
    for element in elements:
        if not isinstance(element, dict) or not isinstance(element.get("id"), str) or not element["id"].strip():
            raise ArtifactError("each element requires an id")
        if element["id"] in ids:
            raise ArtifactError(f"duplicate element id: {element['id']}")
        ids.add(element["id"])
    for circuit in circuits:
        if not isinstance(circuit, dict) or not isinstance(circuit.get("id"), str):
            raise ArtifactError("each circuit requires an id")
        if circuit.get("panel_id") not in ids:
            raise ArtifactError(f"circuit {circuit['id']} references an unknown panel")
        load = _finite_number(circuit.get("load_va"), f"circuit {circuit['id']} load_va")
        if load < 0:
            raise ArtifactError(f"circuit {circuit['id']} load_va cannot be negative")
        if not isinstance(circuit.get("phase"), str) or not circuit["phase"].strip():
            raise ArtifactError(f"circuit {circuit['id']} phase is required")
        if not isinstance(circuit.get("breaker_id"), str) or not circuit["breaker_id"].strip():
            raise ArtifactError(f"circuit {circuit['id']} breaker_id is required")
        if not isinstance(circuit.get("conductor_id"), str) or not circuit["conductor_id"].strip():
            raise ArtifactError(f"circuit {circuit['id']} conductor_id is required")


def _check_contract(snapshot: dict[str, Any], contract: ArtifactContract) -> None:
    validate_snapshot(snapshot)
    for key in ("project_id", "revision_id", "calculation_run_id", "rule_version"):
        if snapshot[key] != getattr(contract, key):
            raise ArtifactError(f"artifact contract mismatch: {key}")


def render_single_line_svg(snapshot: dict[str, Any], contract: ArtifactContract) -> str:
    """Render a simple accessible SVG single-line view from panel/circuit graph."""
    _check_contract(snapshot, contract)
    panels = [e for e in snapshot["elements"] if e.get("kind") == "panel"]
    if not panels:
        raise ArtifactError("snapshot has no panel")
    width = 760
    row_h = 76
    height = 100 + max(1, len(snapshot["circuits"])) * row_h
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="title desc" viewBox="0 0 {width} {height}">',
        f'<title id="title">Diagrama unifilar — {escape(snapshot["project_id"])}</title>',
        '<desc id="desc">Representação dos circuitos cadastrados no snapshot informado; não é aprovação normativa.</desc>',
        '<style>text{font:14px sans-serif;fill:#172033}.wire{stroke:#26364a;stroke-width:2}.box{fill:#f3f6fa;stroke:#52657a}</style>',
    ]
    panel_x, panel_y = 30, 30
    parts += [
        f'<rect class="box" x="{panel_x}" y="{panel_y}" width="150" height="42" rx="4"/>',
        f'<text x="{panel_x + 12}" y="{panel_y + 26}">{escape(str(panels[0]["id"]))}</text>',
    ]
    for index, circuit in enumerate(snapshot["circuits"]):
        y = 112 + index * row_h
        parts += [
            f'<path class="wire" d="M 105 72 V {y} H 220"/>',
            f'<rect class="box" x="220" y="{y - 22}" width="500" height="46" rx="4"/>',
            f'<text x="232" y="{y - 2}">{escape(str(circuit["id"]))} · {escape(str(circuit["breaker_id"]))} · {escape(str(circuit["conductor_id"]))}</text>',
            f'<text x="232" y="{y + 16}">{_finite_number(circuit["load_va"], "load_va"):g} VA · fase {escape(circuit["phase"])}</text>',
        ]
    return "".join(parts + ["</svg>"])


def load_schedule(snapshot: dict[str, Any], contract: ArtifactContract) -> dict[str, Any]:
    """Return a load schedule preserving the exact snapshot/run identity."""
    _check_contract(snapshot, contract)
    rows = []
    for circuit in snapshot["circuits"]:
        rows.append({
            "circuit_id": circuit["id"],
            "panel_id": circuit["panel_id"],
            "load_va": _finite_number(circuit["load_va"], "load_va"),
            "phase": circuit["phase"],
            "breaker_id": circuit["breaker_id"],
            "conductor_id": circuit["conductor_id"],
        })
    return {
        "project_id": contract.project_id,
        "revision_id": contract.revision_id,
        "calculation_run_id": contract.calculation_run_id,
        "rule_version": contract.rule_version,
        "template_version": contract.template_version,
        "rows": rows,
        "status": "study",
        "normative_conformity_verified": False,
    }


def cross_validate_documents(schedule: dict[str, Any], diagram_snapshot: dict[str, Any],
                             contract: ArtifactContract) -> list[str]:
    """Return blocking discrepancies across revision, topology and scheduled facts."""
    _check_contract(diagram_snapshot, contract)
    errors: list[str] = []
    for key in ("project_id", "revision_id", "calculation_run_id", "rule_version", "template_version"):
        if schedule.get(key) != getattr(contract, key):
            errors.append(f"schedule contract mismatch: {key}")
    expected = {c["id"]: c for c in diagram_snapshot["circuits"]}
    rows = schedule.get("rows")
    if not isinstance(rows, list):
        return errors + ["schedule rows must be a list"]
    seen: set[str] = set()
    for row in rows:
        cid = row.get("circuit_id") if isinstance(row, dict) else None
        if cid not in expected:
            errors.append(f"unknown scheduled circuit: {cid}")
            continue
        if cid in seen:
            errors.append(f"duplicate scheduled circuit: {cid}")
            continue
        seen.add(cid)
        source = expected[cid]
        for field in ("panel_id", "phase", "breaker_id", "conductor_id"):
            if row.get(field) != source.get(field):
                errors.append(f"circuit {cid} mismatch: {field}")
        try:
            if _finite_number(row.get("load_va"), f"circuit {cid} load_va") != _finite_number(source.get("load_va"), f"circuit {cid} load_va"):
                errors.append(f"circuit {cid} mismatch: load_va")
        except ArtifactError as exc:
            errors.append(str(exc))
    errors.extend(f"missing scheduled circuit: {cid}" for cid in sorted(set(expected) - seen))
    return errors
