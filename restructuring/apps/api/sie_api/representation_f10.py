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


def quantity_ledger(snapshot: dict[str, Any], contract: ArtifactContract) -> list[dict[str, Any]]:
    """Summarize only explicit segment lengths, retaining measurement provenance."""
    _check_contract(snapshot, contract)
    circuits = {c["id"]: c for c in snapshot["circuits"]}
    segments = snapshot.get("segments", [])
    if not isinstance(segments, list):
        raise ArtifactError("segments must be a list")
    seen: set[str] = set()
    ledger = []
    for segment in segments:
        if not isinstance(segment, dict):
            raise ArtifactError("each segment must be an object")
        sid = segment.get("id")
        if not isinstance(sid, str) or not sid.strip() or sid in seen:
            raise ArtifactError(f"segment id missing or duplicated: {sid}")
        seen.add(sid)
        circuit_id = segment.get("circuit_id")
        if circuit_id not in circuits:
            raise ArtifactError(f"segment {sid} references unknown circuit")
        length = _finite_number(segment.get("length_m"), f"segment {sid} length_m")
        if length < 0:
            raise ArtifactError(f"segment {sid} length_m cannot be negative")
        status = segment.get("status")
        if status not in {"MEASURED", "DOCUMENTED", "ESTIMATED"}:
            raise ArtifactError(f"segment {sid} requires a measurement status")
        origin = segment.get("origin")
        if not isinstance(origin, str) or not origin.strip():
            raise ArtifactError(f"segment {sid} requires origin evidence")
        conductor_id = segment.get("conductor_id", circuits[circuit_id]["conductor_id"])
        if conductor_id != circuits[circuit_id]["conductor_id"]:
            raise ArtifactError(f"segment {sid} conductor differs from its circuit")
        ledger.append({
            "segment_id": sid,
            "circuit_id": circuit_id,
            "conductor_id": conductor_id,
            "length_m": length,
            "status": status,
            "origin": origin.strip(),
        })
    return ledger


def render_report_html(schedule: dict[str, Any], diagram_svg: str,
                       quantities: list[dict[str, Any]]) -> str:
    """Build a printable study report; all caller-controlled text is escaped."""
    headers = ("Circuito", "Quadro", "Carga (VA)", "Fase", "Disjuntor", "Condutor")
    head = "".join(f"<th scope='col'>{escape(h)}</th>" for h in headers)
    rows = []
    for row in schedule["rows"]:
        cells = (row["circuit_id"], row["panel_id"], str(row["load_va"]),
                 row["phase"], row["breaker_id"], row["conductor_id"])
        rows.append("<tr>" + "".join(f"<td>{escape(str(v))}</td>" for v in cells) + "</tr>")
    quantity_rows = "".join(
        "<tr>" + "".join(f"<td>{escape(str(row[k]))}</td>" for k in
                         ("segment_id", "circuit_id", "conductor_id", "length_m", "status", "origin")) + "</tr>"
        for row in quantities
    )
    contract = "".join(
        f"<dt>{escape(key)}</dt><dd>{escape(str(schedule[key]))}</dd>"
        for key in ("project_id", "revision_id", "calculation_run_id", "rule_version", "template_version")
    )
    return (
        "<!doctype html><html lang='pt-BR'><meta charset='utf-8'>"
        "<meta name='viewport' content='width=device-width, initial-scale=1'>"
        "<title>Relatório técnico do estudo elétrico</title>"
        "<style>body{font:16px system-ui;max-width:1100px;margin:2rem auto;padding:0 1rem;color:#172033}"
        "table{border-collapse:collapse;width:100%;margin:1rem 0}th,td{border:1px solid #94a3b8;padding:.45rem;text-align:left}"
        "svg{width:100%;height:auto}.notice{padding:1rem;background:#fff4cc}</style>"
        "<main><h1>Relatório técnico — estudo</h1>"
        "<p class='notice'>Estudo computacional. Não constitui aprovação normativa, profissional ou de concessionária.</p>"
        f"<h2>Identificação e rastreabilidade</h2><dl>{contract}</dl>"
        f"<h2>Diagrama unifilar</h2>{diagram_svg}"
        f"<h2>Quadro de cargas</h2><table><thead><tr>{head}</tr></thead><tbody>{''.join(rows)}</tbody></table>"
        "<h2>Trechos e quantitativos rastreáveis</h2>"
        "<p>Somente trechos explicitamente informados são listados; ausência não é estimada.</p>"
        "<table><thead><tr><th>Trecho</th><th>Circuito</th><th>Condutor</th><th>Comprimento (m)</th><th>Estado</th><th>Origem</th></tr></thead>"
        f"<tbody>{quantity_rows}</tbody></table></main></html>"
    )


def artifact_bundle(snapshot: dict[str, Any], contract: ArtifactContract) -> dict[str, str]:
    """Generate reproducible CSV/JSON/SVG/HTML artifacts without overwriting files."""
    import csv
    import io
    import json

    schedule = load_schedule(snapshot, contract)
    svg = render_single_line_svg(snapshot, contract)
    quantities = quantity_ledger(snapshot, contract)
    errors = cross_validate_documents(schedule, snapshot, contract)
    if errors:
        raise ArtifactError("cross-validation blocked export: " + "; ".join(errors))
    csv_out = io.StringIO(newline="")
    writer = csv.DictWriter(csv_out, fieldnames=[
        "segment_id", "circuit_id", "conductor_id", "length_m", "status", "origin"
    ])
    writer.writeheader()
    writer.writerows(quantities)
    bundle = {
        "schedule.json": json.dumps(schedule, ensure_ascii=False, allow_nan=False, sort_keys=True, indent=2) + "\n",
        "diagram.svg": svg,
        "quantities.csv": csv_out.getvalue(),
        "report.html": render_report_html(schedule, svg, quantities),
    }
    if "floor_plan" in snapshot:
        bundle["floor_plan.svg"] = render_plant_svg(snapshot, contract)
    return bundle


def main(argv: list[str] | None = None) -> int:
    import argparse
    import json
    from pathlib import Path

    parser = argparse.ArgumentParser(description="Generate revision-bound SIE study artifacts.")
    parser.add_argument("--input", required=True, help="JSON object with snapshot and artifact_contract.")
    parser.add_argument("--output-dir", required=True, help="New directory; existing paths are not overwritten.")
    args = parser.parse_args(argv)
    source = json.loads(Path(args.input).read_text(encoding="utf-8-sig"))
    if not isinstance(source, dict) or not isinstance(source.get("snapshot"), dict):
        parser.error("input must contain an object snapshot")
    raw_contract = source.get("artifact_contract")
    if not isinstance(raw_contract, dict):
        parser.error("input must contain artifact_contract")
    contract = ArtifactContract(**raw_contract)
    bundle = artifact_bundle(source["snapshot"], contract)
    destination = Path(args.output_dir)
    destination.mkdir(parents=True, exist_ok=False)
    try:
        for name, content in bundle.items():
            with (destination / name).open("x", encoding="utf-8", newline="") as output:
                output.write(content)
    except BaseException:
        for item in destination.iterdir():
            item.unlink()
        destination.rmdir()
        raise
    print(json.dumps({"files": sorted(bundle), "status": "study",
                      "normative_conformity_verified": False}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

def render_plant_svg(snapshot: dict[str, Any], contract: ArtifactContract) -> str:
    """Render an explicitly scaled 2D placement map; it does not derive routes."""
    _check_contract(snapshot, contract)
    plan = snapshot.get("floor_plan")
    if not isinstance(plan, dict):
        raise ArtifactError("floor_plan is required")
    for key in ("id", "revision_id", "source_ref", "units"):
        if not isinstance(plan.get(key), str) or not plan[key].strip():
            raise ArtifactError(f"floor_plan.{key} is required")
    if plan["revision_id"] != contract.revision_id:
        raise ArtifactError("floor plan revision mismatch")
    width = _finite_number(plan.get("width"), "floor_plan.width")
    height = _finite_number(plan.get("height"), "floor_plan.height")
    scale = _finite_number(plan.get("model_units_per_canvas_unit"), "floor_plan.scale")
    if width <= 0 or height <= 0 or scale <= 0:
        raise ArtifactError("floor plan dimensions and scale must be positive")
    placements = plan.get("placements")
    if not isinstance(placements, list):
        raise ArtifactError("floor_plan.placements must be a list")
    known = {e["id"] for e in snapshot["elements"]}
    used: set[str] = set()
    output = [
        f'<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="plant-title plant-desc" viewBox="0 0 {width:g} {height:g}">',
        f'<title id="plant-title">Planta {escape(plan["id"])} · revisão {escape(plan["revision_id"])}</title>',
        f'<desc id="plant-desc">Origem {escape(plan["source_ref"])}; unidade {escape(plan["units"])}; escala informada {scale:g} unidades do modelo por unidade gráfica. Rotas não inferidas.</desc>',
        '<rect width="100%" height="100%" fill="#fff"/>',
    ]
    for placement in placements:
        if not isinstance(placement, dict):
            raise ArtifactError("each placement must be an object")
        element_id = placement.get("element_id")
        if element_id not in known:
            raise ArtifactError(f"placement references unknown element: {element_id}")
        if element_id in used:
            raise ArtifactError(f"duplicate placement for element: {element_id}")
        used.add(element_id)
        x = _finite_number(placement.get("x"), f"placement {element_id} x")
        y = _finite_number(placement.get("y"), f"placement {element_id} y")
        if not 0 <= x <= width or not 0 <= y <= height:
            raise ArtifactError(f"placement outside plan bounds: {element_id}")
        label = escape(str(placement.get("label", element_id)))
        output += [
            f'<g aria-label="{label}"><circle cx="{x:g}" cy="{y:g}" r="7" fill="#155eef"/>',
            f'<text x="{x + 10:g}" y="{y - 10:g}" font-family="sans-serif" font-size="12">{label}</text></g>',
        ]
    return "".join(output + ["</svg>"])


