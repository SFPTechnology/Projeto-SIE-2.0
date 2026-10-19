#!/usr/bin/env python3
"""Preflight that catches unsafe Copilot QA3 workflow before any paid invocation.

This is a static structural check, NOT a Copilot run or normative signoff.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = Path(".github/workflows/f01-copilot-qa-isolated.yml")
AGENTS = ("f01-qa-arquiteto", "f01-qa-engenheiro-eletrico", "f01-qa-dados-ux-llm")

def check(source: str) -> dict:
    errors = []
    if not re.search(r"(?m)^permissions:\s*\n\s+contents:\s*read\s*$", source):
        errors.append("Workflow must use contents: read only")
    if "refs/heads/feat/f01-governanca-normativa" not in source:
        errors.append("Protected F01 ref missing")
    if source.count("persist-credentials: false") < 3:
        errors.append("All agent checkouts must omit persisted credentials")
    if source.count("ref: " + chr(36) + "{{ github.sha }}") < 3:
        errors.append("Every job must check out the same SHA")
    if source.count("copilot --agent=") != 2:
        errors.append("Exactly two matrix-driven Copilot commands required")
    for agent in AGENTS:
        if source.count(f"agent: {agent}") != 2:
            errors.append(f"Missing matrix entry in QA or cross-review: {agent}")
    for flag in ("--no-ask-user", "--autopilot", "--max-autopilot-continues=5",
                 "--disable-builtin-mcps", "--deny-tool=shell",
                 "--available-tools='view,grep,glob,edit,create,apply_patch,skill'"):
        if source.count(flag) < 2:
            errors.append(f"Missing CLI safeguard in both stages: {flag}")
    if source.count("chmod a-w {} +") != 4:
        errors.append("Read-only source-tree barriers missing")
    if "  cli-smoke:" not in source or "needs: [preflight, cli-smoke]" not in source:
        errors.append("Copilot CLI must be tested in no-token runner before model execution")
    if "copilot --help" not in source or "npm install -g @github/copilot" not in source:
        errors.append("Copilot CLI must install and validate its real command surface")
    if "F01_COPILOT_PAT" not in source or "secrets.F01_COPILOT_PAT" not in source:
        errors.append("Protected personal token secret missing")
    if "needs: [preflight, first-pass]" not in source:
        errors.append("Cross reviews cannot proceed before all first passes")
    if "sha256sum --check" not in source:
        errors.append("Frozen peer artifacts must remain unchanged")
    if "needs: [preflight, first-pass, cross-review]" not in source or "  evidence-bundle:" not in source:
        errors.append("QA3 evidence consolidation must require all six jobs")
    if "scripts/f01_qa3_evidence_bundle.py" not in source:
        errors.append("Nine source reports must be bundled and hashed")
    if source.count("actions/download-artifact@v4") < 7:
        errors.append("All 3 original and 3 cross-review reports must be downloaded")
    if "f01-qa3-evidence-" not in source:
        errors.append("No immutable QA3 execution bundle archived")

    if source.count("scripts/f01_copilot_reports_gate.py") < 2:
        errors.append("Both stages must validate report schemas")
    if "actions/upload-artifact@" not in source or "actions/download-artifact@" not in source:
        errors.append("Frozen artifact hand-off missing")
    active_source = "\n".join(line for line in source.splitlines()
                              if not line.lstrip().startswith("#"))
    for dangerous in ("--allow-all", "--yolo", "--allow-tool='shell",
                      "force: true", "contents: write", "pull-requests: write"):
        if dangerous in active_source:
            errors.append(f"Unsafe workflow option detected: {dangerous}")
    return {"phase": "F01", "safe_static_configuration": not errors,
            "errors": errors, "actual_copilot_sessions_executed": 0,
            "normative_gates_approved_by_preflight": 0,
            "f02_release_allowed": False}

def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=ROOT)
    opts = p.parse_args(argv)
    try:
        result = check((opts.root / WORKFLOW).read_text(encoding="utf-8"))
    except OSError as exc:
        result = {"safe_static_configuration": False, "errors": [str(exc)]}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["safe_static_configuration"] else 2

if __name__ == "__main__":
    sys.exit(main())
