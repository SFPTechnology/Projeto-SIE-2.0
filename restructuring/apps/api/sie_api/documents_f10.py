"""Engineering documents derived exclusively from the verified F10 snapshot."""
from __future__ import annotations

import csv
import io
import json
from hashlib import sha256
from html import escape
from typing import Any

from .representation_f10 import ArtifactContract, ArtifactError, _check_contract, load_schedule, quantity_ledger


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(",", ":"))


def _hash(value: Any) -> str:
    return sha256(canonical(value).encode("utf-8")).hexdigest()


def _facts(value: Any, path: str = "") -> list[dict[str, Any]]:
    """Retain JSON paths for every input/intermediate/formula actually returned."""
    if isinstance(value, dict):
        return [row for key, item in value.items() for row in _facts(item, f"{path}.{key}" if path else key)]
    if isinstance(value, list):
        return [row for key, item in enumerate(value) for row in _facts(item, f"{path}[{key}]")]
    return [{"source_path": path, "value": value}]


def technical_memorial(snapshot: dict[str, Any], contract: ArtifactContract) -> dict[str, Any]:
    _check_contract(snapshot, contract)
    if "verified_calculations_f10" in snapshot:
        verified_list = snapshot["verified_calculations_f10"]
        dependencies = snapshot.get("calculation_dependencies_f10")
        if (snapshot.get("calculation_scope_f10") != "PER_CIRCUIT_RUN_MAP_V1"
                or not isinstance(verified_list, list) or not verified_list or not isinstance(dependencies, list)):
            raise ArtifactError("per-circuit calculation dependency contract required")
        circuits = {row["id"]: row for row in snapshot["circuits"]}
        try:
            by_circuit = {row["circuit_id"]: row for row in verified_list}
            dep_by_circuit = {row["circuit_id"]: row for row in dependencies}
            if (len(by_circuit) != len(verified_list) or len(dep_by_circuit) != len(dependencies)
                    or set(by_circuit) != set(circuits) or set(dep_by_circuit) != set(circuits)):
                raise ValueError("exact circuit coverage required")
            calculations = []
            for cid in sorted(circuits):
                item, dep = by_circuit[cid], dep_by_circuit[cid]
                record = item["record"]
                if (item["run_id"] != dep["run_id"] or record["circuit_id"] != cid
                        or record["input_sha256"] != dep["input_sha256"]
                        or record["result_sha256"] != dep["output_sha256"]
                        or record["algorithm_version"] != dep["algorithm_version"]
                        or record["rule_version"] != dep["rule_version"]
                        or record["snapshot_sha256"] != dep["snapshot_sha256"]
                        or dep["snapshot_sha256"] != snapshot["source_evidence_f10"]["installation_snapshot_sha256"]
                        or item["execution_sha256"] != dep["execution_sha256"]):
                    raise ValueError("per-circuit dependency mismatch")
                per_contract = ArtifactContract(contract.project_id, contract.revision_id,
                    item["run_id"], dep["rule_version"], contract.template_version)
                per_source = {**snapshot, "calculation_run_id": item["run_id"],
                    "rule_version": dep["rule_version"], "circuits": [circuits[cid]],
                    "verified_calculation_f10": item,
                    "source_evidence_f10": {**snapshot["source_evidence_f10"],
                        "calculation_output_sha256": dep["output_sha256"],
                        "algorithm_version": dep["algorithm_version"],
                        "installation_snapshot_sha256": dep["snapshot_sha256"],
                        "motor_execution_sha256": dep["execution_sha256"]}}
                per_source.pop("verified_calculations_f10", None)
                calculation = technical_memorial(per_source, per_contract)
                calculation["calculation_run_id"] = item["run_id"]
                calculations.append(calculation)
        except (KeyError, TypeError, ValueError) as exc:
            raise ArtifactError("per-circuit verified calculations incomplete or inconsistent") from exc
        return {"schema_version": "SIE_F10_MEMORIAL_MULTI_V1", "contract": contract.__dict__.copy(),
            "calculation_scope_f10": "PER_CIRCUIT_RUN_MAP_V1", "calculations": calculations,
            "calculation_dependencies_f10": dependencies,
            "input_facts": [dict(fact, source_path=f"circuits[{calc['calculation_circuit_id']}]." + fact["source_path"]) for calc in calculations for fact in calc["input_facts"]],
            "result_facts": [dict(fact, source_path=f"circuits[{calc['calculation_circuit_id']}]." + fact["source_path"]) for calc in calculations for fact in calc["result_facts"]],
            "formulas": [dict(fact, circuit_id=calc["calculation_circuit_id"]) for calc in calculations for fact in calc["formulas"]],
            "limitations": calculations[0]["limitations"] if calculations else [],
            "normative_conformity_verified": False}
    verified = snapshot.get("verified_calculation_f10")
    if not isinstance(verified, dict):
        raise ArtifactError("verified calculation is required for engineering memorial")
    try:
        from .installation_service import CalculationRecord
        record = CalculationRecord.model_validate(verified["record"]).model_dump(mode="json")
        parameters = verified["parameters"]
        evidence = snapshot["source_evidence_f10"]
        result = json.loads(record["result_json"])
        circuit_ids = {row["id"] for row in snapshot["circuits"]}
        if (record["project_id"] != contract.project_id or record["circuit_id"] not in circuit_ids
                or record["rule_version"] != contract.rule_version
                or record["result_sha256"] != evidence["calculation_output_sha256"]
                or record["input_sha256"] != _hash(parameters)
                or record["algorithm_version"] != evidence["algorithm_version"]
                or record["snapshot_sha256"] != evidence["installation_snapshot_sha256"]
                or record["revision"] != evidence["installation_revision"]
                or verified["execution_sha256"] != evidence["motor_execution_sha256"]):
            raise ValueError("calculation lineage mismatch")
        if not isinstance(parameters, dict) or not isinstance(result, dict):
            raise ValueError("calculation objects required")
        if result.get("liberado_para_uso_normativo") is not False:
            raise ValueError("unverified normative release")
    except (KeyError, TypeError, ValueError) as exc:
        raise ArtifactError("verified calculation is incomplete or inconsistent") from exc
    # Values, intermediate results and formulas are copied from the executed
    # engine record; the document layer never recomputes electrical quantities.
    return {
        "schema_version": "SIE_F10_MEMORIAL_V1",
        "contract": contract.__dict__.copy(),
        "calculation_circuit_id": record["circuit_id"],
        "execution_sha256": verified["execution_sha256"],
        "input_sha256": record["input_sha256"], "result_sha256": record["result_sha256"],
        "algorithm_version": record["algorithm_version"],
        "input_facts": _facts(parameters, "parameters"),
        "result_facts": _facts(result, "record.result_json"),
        "formulas": [fact for fact in _facts(result, "record.result_json") if fact["source_path"].endswith(".formula")],
        "result": result,
        "limitations": ["Somente fórmulas e intermediários presentes no retorno do motor são transcritos.",
                         "Ausência de valor não é preenchida por estimativa.",
                         "Estudo computacional; não constitui homologação normativa ou profissional."],
        "normative_conformity_verified": False,
    }


def equipment_ledger(snapshot: dict[str, Any], contract: ArtifactContract) -> list[dict[str, Any]]:
    _check_contract(snapshot, contract)
    items: dict[str, dict[str, Any]] = {}
    # A unique physical ID is counted once, even when shared by several rows.
    for element in snapshot["elements"]:
        items[element["id"]] = {"item_id": element["id"], "kind": element.get("kind", "element"),
                                "quantity": 1, "unit": "un", "source_path": f"elements[{element['id']}]"}
    for circuit in snapshot["circuits"]:
        for field, kind in (("breaker_id", "device"), ("conductor_id", "cable_run")):
            key = circuit[field]
            if key in items and items[key]["kind"] not in {kind, "breaker", "conductor"}:
                raise ArtifactError(f"equipment identity has incompatible kinds: {key}")
            items.setdefault(key, {"item_id": key, "kind": kind, "quantity": 1, "unit": "un",
                                   "source_path": f"circuits[{circuit['id']}].{field}"})
    return [items[key] for key in sorted(items)]


def render_memorial_html(memorial: dict[str, Any], schedule: dict[str, Any], quantities: list[dict[str, Any]], equipment: list[dict[str, Any]]) -> str:
    def table(rows):
        return "<table><thead><tr><th scope='col'>Origem</th><th scope='col'>Valor</th></tr></thead><tbody>" + "".join(
            f"<tr><td>{escape(str(row['source_path']))}</td><td>{escape(canonical(row['value']))}</td></tr>" for row in rows) + "</tbody></table>"
    return ("<!doctype html><html lang='pt-BR'><meta charset='utf-8'><meta name='viewport' content='width=device-width, initial-scale=1'>"
            "<title>Memorial técnico rastreável</title><style>body{font:16px sans-serif;max-width:1100px;margin:auto;padding:1rem;color:#172033}table{width:100%;border-collapse:collapse}td,th{border:1px solid #aaa;padding:.4rem;overflow-wrap:anywhere}pre{white-space:pre-wrap;overflow-wrap:anywhere}@media print{h2{break-after:avoid}tr{break-inside:avoid}}</style><main>"
            "<h1>Memorial técnico rastreável</h1><p>Estudo computacional. Uso normativo não homologado.</p>"
            f"<h2>Identificação e proveniência</h2><pre>{escape(canonical({key: memorial[key] for key in ('contract','algorithm_version','execution_sha256','input_sha256','result_sha256','calculation_dependencies_f10') if key in memorial}))}</pre>"
            "<h2>Entradas persistidas</h2>" + table(memorial["input_facts"]) + "<h2>Resultados, intermediários e fórmulas executadas</h2>" + table(memorial["result_facts"]) +
            f"<h2>Quadro de cargas</h2><pre>{escape(json.dumps(schedule, ensure_ascii=False, indent=2))}</pre>"
            f"<h2>Quantitativos por trecho e origem</h2><pre>{escape(json.dumps(quantities, ensure_ascii=False, indent=2))}</pre>"
            f"<h2>Equipamentos cadastrados</h2><pre>{escape(json.dumps(equipment, ensure_ascii=False, indent=2))}</pre>"
            "<h2>Limitações e pendências</h2><ul>" + "".join(f"<li>{escape(item)}</li>" for item in memorial["limitations"]) + "</ul></main></html>")


def engineering_documents(snapshot: dict[str, Any], contract: ArtifactContract) -> dict[str, str | bytes]:
    """Generate full engineering exports only from an explicit verified record."""
    from .pdf_f10 import render_engineering_pdf
    memorial = technical_memorial(snapshot, contract)
    schedule, quantities = load_schedule(snapshot, contract), quantity_ledger(snapshot, contract)
    equipment = equipment_ledger(snapshot, contract)
    csv_out = io.StringIO(newline="")
    writer = csv.DictWriter(csv_out, fieldnames=(*contract.__dict__, "item_id", "kind", "quantity", "unit", "source_path"))
    writer.writeheader()
    for row in equipment:
        values = {**contract.__dict__, **row}
        # Spreadsheet applications must not execute untrusted identifiers.
        writer.writerow({key: ("'" + value if isinstance(value, str) and value.lstrip().startswith(("=", "+", "-", "@", "\t", "\r")) else value) for key, value in values.items()})
    return {"memorial.json": canonical(memorial) + "\n",
            "memorial.html": render_memorial_html(memorial, schedule, quantities, equipment),
            "equipment.json": canonical({"contract": contract.__dict__, "items": equipment}) + "\n",
            "equipment.csv": csv_out.getvalue(),
            "report.pdf": render_engineering_pdf(memorial, schedule, quantities, equipment)}
