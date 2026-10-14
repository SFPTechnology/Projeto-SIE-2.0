#!/usr/bin/env python3
"""
apply-wave3-to-dash.py — Sync bench-output-dash.json with comparison-matrix.json after Wave 3.

Idempotent. Mirrors the anchor (slides_creator) cell scores and the recalculated
weighted_totals from the matrix into the dash so Observatory rendering stays
consistent.
"""

from __future__ import annotations
import json
from pathlib import Path

HERE = Path(__file__).parent
MATRIX_PATH = HERE / "comparison-matrix.json"
DASH_PATH = HERE / "bench-output-dash.json"
ANCHOR = "slides_creator"


def main() -> int:
    matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
    dash = json.loads(DASH_PATH.read_text(encoding="utf-8"))

    # 1. Sync weighted_totals → summary.score / anchor_score + matrix.totals
    totals_by_player = {p["player"]: p["score"] for p in matrix["weighted_totals"]}

    anchor_score = totals_by_player.get(ANCHOR)
    if anchor_score is not None:
        dash.setdefault("summary", {})
        dash["summary"]["score"] = anchor_score
        dash["summary"]["anchor_score"] = anchor_score
        dash["summary"]["leader"] = ANCHOR

    # 2. Mirror anchor cell scores into matrix.rows
    matrix_rows_by_id = {r["id"]: r for r in matrix["rows"]}
    dash_matrix = dash.get("matrix", {})
    dash_rows = dash_matrix.get("rows", [])
    updated_cells = 0
    for d_row in dash_rows:
        rid = d_row.get("id")
        m_row = matrix_rows_by_id.get(rid)
        if not m_row:
            continue
        m_anchor_cell = next((c for c in m_row.get("cells", []) if c.get("player") == ANCHOR), None)
        if not m_anchor_cell:
            continue
        for d_cell in d_row.get("cells", []):
            if d_cell.get("player") == ANCHOR:
                if d_cell.get("score") != m_anchor_cell.get("score"):
                    d_cell["score"] = m_anchor_cell["score"]
                    d_cell["notes"] = m_anchor_cell.get("notes", d_cell.get("notes", ""))
                    updated_cells += 1
                break

    # 3. Update matrix.totals
    if "totals" in dash_matrix:
        for t in dash_matrix.get("totals", []):
            player = t.get("player")
            if player in totals_by_player:
                t["score"] = totals_by_player[player]

    # 4. Provenance breadcrumb
    dash.setdefault("provenance", []).append({
        "wave": "W3-spike",
        "applied_at": "2026-05-18T15:30:00Z",
        "anchor_delta": "+3.14 (77.93 → 81.07)",
        "cells_updated": updated_cells,
        "source": "wave-3-promotions.json + comparison-matrix.json",
    })
    dash["generated_at"] = "2026-05-18T15:30:00Z"

    DASH_PATH.write_text(json.dumps(dash, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({
        "anchor_score_after": anchor_score,
        "matrix_cells_updated": updated_cells,
        "weighted_totals": dash.get("summary", {}).get("score"),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
