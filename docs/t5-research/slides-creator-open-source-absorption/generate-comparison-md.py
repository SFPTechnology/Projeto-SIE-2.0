#!/usr/bin/env python3
"""
generate-comparison-md.py — Regenerate comparison-matrix.md from comparison-matrix.json.

Idempotent. Writes the .md alongside the .json so the dashboard markdown reflects
the latest wave's promotions without manual editing.
"""

from __future__ import annotations
import json
from pathlib import Path

HERE = Path(__file__).parent
JSON_PATH = HERE / "comparison-matrix.json"
MD_PATH = HERE / "comparison-matrix.md"


def main() -> int:
    matrix = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    players = matrix["weighted_totals"]
    rows = matrix["rows"]

    md = []
    md.append("# Micro Capability Matrix — slides creator open-source absorption\n")
    md.append("Esta matriz quebra 36 dimensões macro em 108 microdimensões. Cada célula usa escala 0-100 por cinco lentes: cobertura, profundidade, fidelidade, evidência e absorvibilidade.\n")
    md.append("Última atualização: 2026-05-18 (após Wave 3 spike).\n")
    md.append("## Ranking consolidado\n")
    md.append("| Rank | Player | Score |")
    md.append("|---:|---|---:|")
    for i, p in enumerate(players, 1):
        md.append(f"| {i} | {p['label']} | {p['score']} |")
    md.append("")
    md.append("## Matriz\n")

    header_cols = ["Dimensão micro", "Grupo", "Peso"]
    for p in players:
        header_cols.append(p["label"])
    header_cols.append("Líder")
    md.append("| " + " | ".join(header_cols) + " |")
    md.append("|" + "|".join(["---"] * len(header_cols)) + "|")

    player_order = [p["player"] for p in players]
    player_label_by_key = {p["player"]: p["label"] for p in players}

    for row in rows:
        cells_by_player = {c.get("player"): c for c in row.get("cells", [])}
        line = [row["label"], row["group"], f"{row['weight']}"]
        for player_key in player_order:
            cell = cells_by_player.get(player_key)
            line.append(str(cell.get("score", "-") if cell else "-"))
        best_player = row.get("best_player")
        best_label = player_label_by_key.get(best_player, best_player or "-")
        line.append(best_label)
        md.append("| " + " | ".join(line) + " |")

    md.append("")
    MD_PATH.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"regenerated {MD_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
