#!/usr/bin/env python3
"""aggregate-scores.py — Aggregate AIOX task-runs into final score-report.json.

Origin: STORY-153.7 (EPIC-153 DEEP-RESEARCH-GOLDIFY).

Reads:
    docs/bench/aiox-deep-research-bench-submission/task-runs/*.jsonl

Writes:
    docs/bench/aiox-deep-research-bench-submission/score-report.json

Usage:
    python3 aggregate-scores.py            # full report
    python3 aggregate-scores.py --pilot    # pilot-only (first 5 tasks)
    python3 aggregate-scores.py --halt-below 0.40   # exit 2 if score < threshold
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from datetime import datetime, timezone


SCRIPT_DIR = Path(__file__).resolve().parent
SUBMISSION_DIR = SCRIPT_DIR.parent
TASK_RUNS_DIR = SUBMISSION_DIR / "task-runs"
TEMPLATE_PATH = SUBMISSION_DIR / "score-report.template.json"
OUTPUT_PATH = SUBMISSION_DIR / "score-report.json"


def load_task_runs(pilot: bool = False) -> list[dict]:
    """Load all task-run jsonl files. If pilot=True, only first 5."""
    runs = []
    if not TASK_RUNS_DIR.exists():
        return runs
    files = sorted(TASK_RUNS_DIR.glob("*.jsonl"))
    if pilot:
        files = files[:5]
    for f in files:
        try:
            with f.open("r", encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if line:
                        runs.append(json.loads(line))
        except (json.JSONDecodeError, OSError) as e:
            sys.stderr.write(f"WARNING: failed to parse {f}: {e}\n")
    return runs


def aggregate(runs: list[dict]) -> dict:
    """Compute overall_score, race_score, fact_score, costs, stats from task runs."""
    if not runs:
        return {
            "tasks_total": 0,
            "tasks_with_score": 0,
            "overall_score": 0.0,
            "race_score": 0.0,
            "fact_score": 0.0,
            "total_cost_usd": 0.0,
            "wall_time_minutes": 0,
        }

    scored = [r for r in runs if isinstance(r.get("score"), (int, float))]
    n_scored = len(scored)

    overall = sum(r["score"] for r in scored) / n_scored if n_scored else 0.0
    race = sum(r.get("race_score", r.get("score", 0)) for r in scored) / n_scored if n_scored else 0.0
    fact = sum(r.get("fact_score", r.get("score", 0)) for r in scored) / n_scored if n_scored else 0.0
    total_cost = sum(r.get("cost_usd", 0) for r in runs)
    total_seconds = sum(r.get("wall_time_sec", 0) for r in runs)

    return {
        "tasks_total": len(runs),
        "tasks_with_score": n_scored,
        "overall_score": round(overall, 4),
        "race_score": round(race, 4),
        "fact_score": round(fact, 4),
        "total_cost_usd": round(total_cost, 2),
        "wall_time_minutes": round(total_seconds / 60, 1),
    }


def build_report(agg: dict, pilot: bool, runs: list[dict]) -> dict:
    """Build the final score-report.json structure."""
    if TEMPLATE_PATH.exists():
        with TEMPLATE_PATH.open("r", encoding="utf-8") as f:
            report = json.load(f)
    else:
        report = {}

    report["_status"] = "pilot" if pilot else "full"
    report["_generated_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    report.setdefault("submission", {})
    report["submission"]["date"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    report.setdefault("scores", {})
    report["scores"]["overall_score"] = agg["overall_score"]
    report["scores"]["race_score"] = agg["race_score"]
    report["scores"]["fact_score"] = agg["fact_score"]

    report.setdefault("stats", {})
    report["stats"]["tasks_total"] = agg["tasks_total"]
    report["stats"]["tasks_executed"] = agg["tasks_with_score"]
    report["stats"]["tasks_skipped"] = agg["tasks_total"] - agg["tasks_with_score"]

    report.setdefault("costs", {})
    report["costs"]["total_usd"] = agg["total_cost_usd"]
    report["costs"]["avg_per_task_usd"] = round(agg["total_cost_usd"] / max(agg["tasks_total"], 1), 4)
    report["costs"]["wall_time_minutes"] = agg["wall_time_minutes"]

    report["per_task_breakdown"] = [
        {
            "task_id": r.get("task_id", "?"),
            "score": r.get("score"),
            "cost_usd": r.get("cost_usd", 0),
            "wall_time_sec": r.get("wall_time_sec", 0),
        }
        for r in runs
    ]

    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Aggregate AIOX bench task runs into score-report.json")
    parser.add_argument("--pilot", action="store_true", help="Pilot mode (first 5 tasks only)")
    parser.add_argument("--halt-below", type=float, default=None, help="Exit 2 if overall_score below threshold")
    parser.add_argument("--quiet", action="store_true", help="Suppress stdout summary")
    args = parser.parse_args()

    runs = load_task_runs(pilot=args.pilot)
    agg = aggregate(runs)
    report = build_report(agg, args.pilot, runs)

    out_path = SUBMISSION_DIR / ("score-report.pilot.json" if args.pilot else "score-report.json")
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)

    if not args.quiet:
        print(f"📊 Mode: {'pilot' if args.pilot else 'full'}")
        print(f"   Tasks: {agg['tasks_total']} total, {agg['tasks_with_score']} scored")
        print(f"   Overall score: {agg['overall_score']:.4f}")
        print(f"   RACE: {agg['race_score']:.4f}")
        print(f"   FACT: {agg['fact_score']:.4f}")
        print(f"   Cost: ${agg['total_cost_usd']:.2f}")
        print(f"   Wall time: {agg['wall_time_minutes']:.1f} min")
        print(f"   Report: {out_path}")

    if args.halt_below is not None and agg["overall_score"] < args.halt_below:
        sys.stderr.write(f"❌ HALT: overall_score {agg['overall_score']} < threshold {args.halt_below}\n")
        return 2

    return 0


if __name__ == "__main__":
    sys.exit(main())
