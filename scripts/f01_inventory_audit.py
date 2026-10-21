#!/usr/bin/env python3
"""Audit F01 engineering dependency inventory against code.

Counts LEGACY CANDIDATES and missing cell references, not source-approved cells.
Never fills ABNT tables from secondary copies nor grants normative release.
"""
from __future__ import annotations
import argparse
import csv
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
TABLE = Path("docs/implantacao-sie-2-0/F01/INVENTARIO_CELULAS_E_REGRAS_USADAS.csv")
EDP_ENGINE = Path("restructuring/apps/api/sie_api/domain/edp.py")
FIELDS = {"id", "motor", "dado_necessario", "evidencia_existente",
          "localizacao_candidata_na_copia_derivada", "estado_de_conferencia",
          "risco", "proxima_comprovacao"}
# Explicit known active candidate families. These are NOT ampacity/EDP homologations.
FAMILIES = ("RCA", "XL", "IZ", "FATORES_CORRECAO",
            "EDP_DEMANDA", "EDP_MODALIDADE")

def limited_lot_metrics(root: Path) -> dict:
    """Report the received limited acceptance separately from candidate inventory.

    These counts do not establish the unknown complete F01 denominator and do
    not claim independent verification of a professional credential or source.
    """
    receipt_path = Path("docs/implantacao-sie-2-0/F01/ACEITE_PROFISSIONAL_LOTE01_RECEBIDO_2026-10-20.json")
    registry_path = Path("restructuring/apps/api/sie_api/data/f01_lote01_cells_v1.json")
    lot_cells = {f"CEL-{n:02d}" for n in range(1, 9)}
    lot_cases = {f"C{n:02d}" for n in range(1, 7)}
    result = {"scope": "LOTE01_ONLY_NOT_COMPLETE_F01", "accepted_cells": 0,
              "lot_cells_total": 8, "accepted_cases": 0, "lot_cases_total": 6,
              "complete_f01_cells_total": None, "complete_f01_cases_total": None,
              "complete_f01_denominator_known": False,
              "acceptance_kind": "NOT_AVAILABLE", "errors": []}
    if not (root / receipt_path).exists() and not (root / registry_path).exists():
        return result
    try:
        receipt = json.loads((root / receipt_path).read_text(encoding="utf-8"))
        registry = json.loads((root / registry_path).read_text(encoding="utf-8"))
        cells = registry["celulas"]
        ids = [cell["id"] for cell in cells]
        accepted = receipt["accepted_in_limited_scope"]
        flags = receipt["release_flags_declared_in_submission"]
        if (len(ids) != len(set(ids)) or set(ids) != lot_cells or
                len(accepted) != len(set(accepted)) or
                receipt.get("confirmation_flag_in_submission") is not True or
                receipt.get("verdict_declared_in_submission") != "ACEITO_NO_ESCOPO_DO_LOTE" or
                registry["aceite_sha256"] != receipt["private_submission_sha256"] or
                registry["fonte_sha256_declarada_rt"] != receipt["source_sha256_declared_by_reviewer"] or
                any(flags.get(key) is not False for key in
                    ("normative_release", "f01_release_allowed", "f02_release_allowed")) or
                not set(ids).issubset(accepted)):
            raise ValueError("Limited lot receipt/registry mismatch or unauthorized release")
        case_ids = [item for item in accepted if re.fullmatch(r"C\d{2}", item)]
        if not set(case_ids).issubset(lot_cases):
            raise ValueError("Unexpected case outside the limited lot")
        result.update(accepted_cells=len(set(ids).intersection(accepted)),
                      accepted_cases=len(case_ids),
                      acceptance_kind="RECEIVED_PROFESSIONAL_LIMITED_SCOPE_DECLARATION",
                      receipt_path=str(receipt_path), registry_path=str(registry_path),
                      pending_items=receipt["pending_items"])
    except (OSError, KeyError, TypeError, ValueError) as exc:
        result["errors"].append(str(exc))
    return result

def inspect(rows: list[dict], edp_code: str) -> dict:
    errors = []
    candidates = set(re.findall(r'CategoriaEDP\("([UDT]\d+)"', edp_code))
    if not candidates:
        errors.append("Unable to inspect EDP categories from active engine")
    seen = set()
    actual_edp = set()
    for n, row in enumerate(rows, 1):
        if set(row) != FIELDS:
            errors.append(f"Inventory row {n}: header/schema changed")
            continue
        key = row["id"]
        if not key or key in seen:
            errors.append(f"Inventory row {n}: missing/duplicated id")
        seen.add(key)
        if any(not isinstance(v, str) or not v.strip() for v in row.values()):
            errors.append(f"{key}: required description/evidence missing")
        if row["estado_de_conferencia"] != "NAO_HOMOLOGADO":
            errors.append(f"{key}: cannot auto-claim normative review")
        if key.startswith("EDP-CAT-"):
            actual_edp.add(key.removeprefix("EDP-CAT-"))
    if candidates != actual_edp:
        errors.append(f"Missing/extra EDP categories: {sorted(candidates - actual_edp)} / {sorted(actual_edp - candidates)}")
    if len(rows) < len(candidates):
        errors.append("Cannot omit legacy EDP input candidates")
    return {"phase": "F01", "records": len(rows), "edp_category_candidates": len(candidates),
            "other_dependency_groups": len(rows) - len(actual_edp),
            "active_code_candidate_categories": sorted(candidates),
            "inventory_categories": sorted(actual_edp),
            "primary_source_cells_independently_verified": 0,
            "all_active_normative_cells_enumerated": False,
            "eligible_for_release": False, "errors": errors}

def build_pending_cell_work_items(rows: list[dict]) -> dict:
    """Ready-to-review work items, no numerical cells invented from Markdown."""
    return {
        "phase": "F01", "schema_version": 1,
        "kind": "CANDIDATE_GROUPS_NOT_CERTIFIED_ABNT_EDP_TABLE_CELLS",
        "enumeration_complete": False, "independent_source_reviews_complete": False,
        "normative_conformity_verified": False, "f02_release_allowed": False,
        "items": [
            {"candidate_id": row["id"], "engine": row["motor"],
             "source_candidate": row["localizacao_candidata_na_copia_derivada"],
             "source_verified": False, "required_cells_enumerated": False,
             "cell_instances": [], "second_independent_reader_confirmed": False,
             "state": "BLOCKED_SOURCE"}
            for row in rows
        ],
    }


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument("--write-pending", type=Path,
                   help="Optional JSON candidate work-items output, never certified cells")
    args = p.parse_args(argv)
    try:
        with (args.root / TABLE).open(encoding="utf-8", newline="") as stream:
            data = list(csv.DictReader(stream))
        engine = (args.root / EDP_ENGINE).read_text(encoding="utf-8")
        result = inspect(data, engine)
        result["primary_source_cells_independently_verified_scope"] = "CANDIDATE_INVENTORY_ONLY_EXCLUDES_LIMITED_LOT"
        result["limited_lot_progress"] = limited_lot_metrics(args.root)
        result["errors"].extend(result["limited_lot_progress"]["errors"])
        if args.write_pending is not None and not result["errors"]:
            output = args.write_pending.resolve()
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(json.dumps(build_pending_cell_work_items(data),
                                         ensure_ascii=False, indent=2) + "\n",
                              encoding="utf-8")
    except OSError as exc:
        result = {"errors": [str(exc)], "eligible_for_release": False}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if result["errors"] else 0

if __name__ == "__main__":
    sys.exit(main())
