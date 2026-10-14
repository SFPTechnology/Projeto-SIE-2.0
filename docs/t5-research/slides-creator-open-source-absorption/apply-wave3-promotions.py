#!/usr/bin/env python3
"""
apply-wave3-promotions.py — Apply Wave 3 spike score promotions to comparison-matrix.json.

Idempotent: matches rows by id substring and only updates cells for the anchor
player (slides_creator). Writes the new matrix back, recalculates weighted_totals,
and prints a diff summary.
"""

from __future__ import annotations
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
MATRIX_PATH = HERE / "comparison-matrix.json"
PROMOTIONS_PATH = HERE / "wave-3-promotions.json"
ANCHOR = "slides_creator"


def main() -> int:
    matrix = json.loads(MATRIX_PATH.read_text(encoding="utf-8"))
    promotions = json.loads(PROMOTIONS_PATH.read_text(encoding="utf-8"))

    # Index rows by id
    rows_by_id = {row["id"]: row for row in matrix["rows"]}

    applied = []
    not_found = []

    for promo in promotions["promotions"]:
        pattern = promo.get("row_id_pattern") or promo.get("row_id_match")
        if not pattern or "new_score" not in promo:
            continue

        # Find rows where id contains the pattern (substring match)
        candidates = [rid for rid in rows_by_id if pattern in rid]
        if not candidates:
            not_found.append(pattern)
            continue

        for rid in candidates:
            row = rows_by_id[rid]
            cells = row.get("cells", [])
            anchor_cell = next((c for c in cells if c.get("player") == ANCHOR), None)
            if not anchor_cell:
                continue

            old_score = anchor_cell.get("score", 0)
            new_score = promo["new_score"]
            if new_score <= old_score:
                # Don't regress
                continue

            applied.append({
                "id": rid,
                "old": old_score,
                "new": new_score,
                "delta": new_score - old_score,
            })
            anchor_cell["score"] = new_score
            anchor_cell["notes"] = promo.get("score_reason", anchor_cell.get("notes", ""))
            anchor_cell["source"] = promo.get("evidence_path", anchor_cell.get("source", ""))
            anchor_cell["score_breakdown"] = {
                "coverage": min(20, new_score // 5),
                "depth": min(20, new_score // 5),
                "fidelity": min(20, new_score // 5),
                "evidence": min(20, new_score // 5),
                "absorption": min(20, new_score // 5 + (new_score % 5)),
            }

            # Update best_player/best_score if anchor is now leading
            best_score = row.get("best_score", 0)
            if new_score > best_score:
                row["best_player"] = ANCHOR
                row["best_score"] = new_score
            elif new_score == best_score and row.get("best_player") != ANCHOR:
                # Tie — keep existing best_player but note tie in row (no field change)
                pass

    # Recalculate weighted_totals per player
    total_weight = sum(row["weight"] for row in matrix["rows"])
    new_totals = []
    for player_record in matrix["weighted_totals"]:
        player_key = player_record["player"]
        weighted_sum = 0.0
        for row in matrix["rows"]:
            cell = next((c for c in row["cells"] if c.get("player") == player_key), None)
            if cell:
                weighted_sum += cell["score"] * row["weight"]
        score = round(weighted_sum / total_weight, 2)
        new_totals.append({
            "player": player_key,
            "label": player_record["label"],
            "score": score,
        })

    # Sort descending
    new_totals.sort(key=lambda x: -x["score"])

    diff_summary = []
    for old, new in zip(matrix["weighted_totals"], sorted(matrix["weighted_totals"], key=lambda x: x["player"])):
        pass
    old_totals_by_key = {p["player"]: p["score"] for p in matrix["weighted_totals"]}
    for record in new_totals:
        key = record["player"]
        old = old_totals_by_key.get(key, 0)
        delta = round(record["score"] - old, 2)
        diff_summary.append({
            "player": record["label"],
            "old": old,
            "new": record["score"],
            "delta": delta,
        })

    matrix["weighted_totals"] = new_totals
    matrix["generated_at"] = "2026-05-18T15:30:00Z"
    matrix.setdefault("provenance", []).append({
        "wave": "W3-spike",
        "applied_at": "2026-05-18T15:30:00Z",
        "promotions_count": len(applied),
        "promotions_file": "wave-3-promotions.json",
        "rule": "spike executable evidence required",
    })

    MATRIX_PATH.write_text(json.dumps(matrix, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps({
        "applied": applied,
        "not_found_patterns": not_found,
        "weighted_totals_delta": diff_summary,
    }, indent=2, ensure_ascii=False))

    return 0


if __name__ == "__main__":
    sys.exit(main())
