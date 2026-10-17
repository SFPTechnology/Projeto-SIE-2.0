#!/usr/bin/env python3
"""Validate real F01 Copilot QA artifacts without granting normative approval.

No approved G01..G06 can be derived from model-produced text or fields.
This tool checks shape, independence metadata, and unsafe leaked credentials;
professional signoffs and ABNT/EDP cell verification are separate gates.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROLES = {"QA-01", "QA-02", "QA-03"}
GATES = {f"G{i:02d}" for i in range(1, 7)}
SECRET_RE = re.compile(
    r"(?:github_pat_[A-Za-z0-9_]{20,}|gh[pousr]_[A-Za-z0-9]{20,}|"
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----)"
)
SHA_RE = re.compile(r"^[0-9a-f]{40}$")
CROSS_REVIEWER = {"QA-01": "QA-02", "QA-02": "QA-03", "QA-03": "QA-01"}


def _read_text(path: Path) -> str:
    data = path.read_text(encoding="utf-8")
    if SECRET_RE.search(data):
        raise ValueError(f"Potential credential/private-key leak in {path.name}")
    if len(data.encode("utf-8")) > 220_000:
        raise ValueError(f"Oversized report: {path.name}")
    return data


def first_pass(root: Path, role: str, baseline: str) -> dict:
    if role not in ROLES or not SHA_RE.fullmatch(baseline):
        raise ValueError("Invalid role or baseline SHA")
    folder = root / role
    report = _read_text(folder / "PARECER_QA.md")
    raw = _read_text(folder / "MATRIZ_6_GATES.json")
    if len(report.strip()) < 300 or role not in report:
        raise ValueError("Missing substantive first-pass technical report")
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("QA matrix must be an object")
    expected = {
        "schema_version": 1, "phase": "F01", "agent": role,
        "baseline_sha": baseline, "independent_first_pass": True,
        "source_values_approved": False, "f02_release_allowed": False,
    }
    for k, v in expected.items():
        if data.get(k) != v or type(data.get(k)) is not type(v):
            raise ValueError(f"Invalid/unsafe QA attribute: {k}")
    gates = data.get("gates")
    if not isinstance(gates, list) or len(gates) != 6:
        raise ValueError("Exactly six gates required")
    if {g.get("id") for g in gates if isinstance(g, dict)} != GATES:
        raise ValueError("G01–G06 each required once")
    for gate in gates:
        if gate.get("accepted") is not False or gate.get("status") not in {"PARTIAL", "BLOCKED"}:
            raise ValueError(f"Agent cannot normatively approve gate {gate.get('id')}")
        if not isinstance(gate.get("finding"), str) or len(gate["finding"].strip()) < 15:
            raise ValueError("A concrete finding is required for each gate")
    blockers = data.get("blockers")
    if not isinstance(blockers, list) or not blockers or not all(
        isinstance(s, str) and s.strip() for s in blockers
    ):
        raise ValueError("Explicit blocking evidence required")
    return {"role": role, "baseline_sha": baseline, "gates": len(gates),
            "professional_signoff": False, "normative_cells_approved": 0}


def cross_review(root: Path, reviewer: str, baseline: str) -> dict:
    if reviewer not in ROLES or not SHA_RE.fullmatch(baseline):
        raise ValueError("Invalid reviewer/baseline")
    author = next(a for a, r in CROSS_REVIEWER.items() if r == reviewer)
    text = _read_text(root / reviewer / f"CROSS_REVIEW_{author}.md")
    if len(text.strip()) < 300 or reviewer not in text or author not in text or baseline not in text:
        raise ValueError("Incomplete cross-review artifact or missing SHA")
    return {"reviewer": reviewer, "author": author, "baseline_sha": baseline,
            "professional_signoff": False}


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, required=True)
    p.add_argument("--baseline", required=True)
    p.add_argument("--role", choices=sorted(ROLES), required=True)
    p.add_argument("--stage", choices=["first-pass", "cross-review"], required=True)
    args = p.parse_args(argv)
    try:
        result = (first_pass(args.root, args.role, args.baseline)
                  if args.stage == "first-pass"
                  else cross_review(args.root, args.role, args.baseline))
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f"BLOCKED_QA_ARTIFACT: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({"status": "QA_ARTIFACT_STRUCTURALLY_VALID_NOT_SIGNED", **result},
                     ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
