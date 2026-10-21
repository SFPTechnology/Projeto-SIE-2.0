#!/usr/bin/env python3
"""Collect immutable Copilot QA3 runner artifacts into an auditable bundle.

All 3 first-pass and 3 cross-review jobs must have succeeded and submitted
report files. A machine-readable record with the SHA-256 of each report is
produced. These are AUTOMATION ARTIFACTS, not external source signoff.
"""
from __future__ import annotations
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import sys

import f01_copilot_reports_gate as qa

ROLES = ("QA-01", "QA-02", "QA-03")
PEERS = {"QA-01": "QA-03", "QA-02": "QA-01", "QA-03": "QA-02"}


def inspect(first_root: Path, cross_root: Path, baseline: str, run_id: str) -> dict:
    if not qa.SHA_RE.fullmatch(baseline):
        raise ValueError("Baseline does not identify a full immutable Git SHA")
    if not re.fullmatch(r"[0-9]{1,20}", run_id):
        raise ValueError("GitHub Actions run ID missing or invalid")
    artifacts, agents, cross_reviews = {}, [], []
    for role in ROLES:
        qa.first_pass(first_root, role, baseline)
        folder = first_root / role
        for name in ("PARECER_QA.md", "MATRIZ_6_GATES.json"):
            path = folder / name
            qa._read_text(path)  # Reject likely leaked tokens before including files.
            artifacts[f"firstpass/{role}/{name}"] = sha256(path.read_bytes()).hexdigest()
        agents.append({"id": role, "artifact_integrity_checked": True,
                       "independent_runner_claim": "github_actions_matrix_job",
                       "first_pass_frozen": True})
    for reviewer in ROLES:
        qa.cross_review(cross_root, reviewer, baseline)
        author = PEERS[reviewer]
        path = cross_root / reviewer / f"CROSS_REVIEW_{author}.md"
        qa._read_text(path)
        artifacts[f"crossreview/{reviewer}/{path.name}"] = sha256(path.read_bytes()).hexdigest()
        cross_reviews.append({"reviewer": reviewer, "author": author,
                              "artifact_integrity_checked": True,
                              "independent_runner_claim": "github_actions_matrix_job"})
    if len(artifacts) != 9:
        raise ValueError("Expected six first-pass files plus three cross-reviews")
    return {"schema_version": 1, "phase": "F01",
            "kind": "COPILOT_QA3_EXECUTION_ARTIFACT_CHECK_NOT_PROFESSIONAL_ATTESTATION",
            "source_sha": baseline, "github_actions_run_id": run_id,
            "first_passes_found": len(agents), "cross_reviews_found": len(cross_reviews),
            "agents": agents, "cross_reviews": cross_reviews,
            "files_sha256": artifacts,
            "independence_level": "SEPARATE_GITHUB_ACTIONS_JOBS_NOT_INDEPENDENT_PROFESSIONALS",
            "independent_professional_signoff": False,
            "normative_cells_verified_by_bundle": 0,
            "accepted_normative_gates": 0, "f01_released": False,
            "f02_release_allowed": False}


def main(argv=None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--first-root", required=True, type=Path)
    p.add_argument("--cross-root", required=True, type=Path)
    p.add_argument("--baseline", required=True)
    p.add_argument("--run-id", required=True)
    p.add_argument("--output", required=True, type=Path)
    args = p.parse_args(argv)
    try:
        report = inspect(args.first_root, args.cross_root, args.baseline, args.run_id)
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f"BLOCKED_QA3_BUNDLE: {exc}", file=sys.stderr)
        return 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                           encoding="utf-8")
    print(json.dumps({"status": "QA3_ARTIFACTS_VERIFIED_NOT_NORMATIVELY_APPROVED",
                      "first_passes": 3, "cross_reviews": 3, "sha": args.baseline,
                      "actions_run_id": args.run_id, "normative_gates_accepted": 0}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
