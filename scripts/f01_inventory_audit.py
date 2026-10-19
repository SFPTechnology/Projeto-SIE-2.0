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
