#!/usr/bin/env python3
"""Deterministic F01 6-gate / 10-acceptance evidence dashboard (no approval grant).

Two modes: default prints open blockers with exit 0 if consistent;
--strict exits 1 if any requirement incomplete. Never modifies project state.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path("docs/implantacao-sie-2-0/F01/QA3_MANIFEST.json")
STATE = Path("docs/sie-orchestrator/ORCHESTRATOR_STATE.json")
REQUIRED_G = {f"G{i:02d}" for i in range(1, 7)}
REQUIRED_AC = {f"AC-01.{i:02d}" for i in range(1, 11)}
REQUIRED_QA = {"QA-01", "QA-02", "QA-03"}

def inspect(manifest: dict, state: dict) -> dict:
    errors, blockers = [], []
    tasks = {t.get("id"): t for t in state.get("tasks", []) if isinstance(t, dict)}
    f00, f01 = tasks.get("F00", {}), tasks.get("F01", {})
    if f00.get("state") != "DONE":
        errors.append("F00 baseline must remain DONE")
    if not f01 or f01.get("state") not in {"BLOCKED", "PENDING_REVIEW", "DONE"}:
        errors.append("F01 state missing/invalid")
    if manifest.get("phase") != "F01" or manifest.get("schema_version") != 1:
        errors.append("QA3 manifest schema invalid")
    gates = manifest.get("gates", [])
    ac = f01.get("criteria", [])
    agents = manifest.get("agents", [])
    cross = manifest.get("cross_reviews", [])
    if not isinstance(gates, list) or len(gates) != 6 or {g.get("id") for g in gates if isinstance(g, dict)} != REQUIRED_G:
        errors.append("G01–G06 exactly once required")
        gates = []
    if not isinstance(ac, list) or len(ac) != 10 or {a.get("id") for a in ac if isinstance(a, dict)} != REQUIRED_AC:
        errors.append("AC-01.01 through AC-01.10 exactly once required")
        ac = []
    if not isinstance(agents, list) or len(agents) != 3 or {a.get("id") for a in agents if isinstance(a, dict)} != REQUIRED_QA:
        errors.append("Three distinct QA agent identities required")
        agents = []
    if not isinstance(cross, list) or len(cross) != 3:
        errors.append("Three cross-review positions required")
        cross = []
    for gate in gates:
        if type(gate.get("accepted")) is not bool:
            errors.append(f"{gate.get('id')}: boolean acceptance required")
        if gate.get("accepted") is True and not gate.get("independent_external_verification"):
            errors.append(f"{gate['id']}: cannot accept without external verification")
        if gate.get("accepted") is not True:
            blockers.append(f"{gate['id']}: {gate.get('status', 'BLOCKED')}")
    for item in ac:
        if type(item.get("passed")) is not bool:
            errors.append(f"{item.get('id')}: acceptance flag invalid")
        if not item.get("passed"):
            blockers.append(f"{item.get('id')}: no formal acceptance")
    for agent in agents:
        if (agent.get("status") != "EXECUTED" or
                not agent.get("independent_first_pass_commit") or
                not agent.get("review_package")):
            blockers.append(f"{agent.get('id', '?')}: independent QA not proven")
    for review in cross:
        if review.get("status") != "EXECUTED":
            blockers.append(f"Cross-review {review.get('author','?')} -> {review.get('reviewer','?')}: missing")
    signoff = manifest.get("external_normative_signoff", {})
    if not isinstance(signoff, dict) or signoff.get("status") != "SIGNED":
        blockers.append("Independent professional source/cell signoff not proven")
    if manifest.get("f02_release_allowed") is not False:
        errors.append("F02 must remain locked in this diagnostic phase")
    if f01.get("state") == "DONE" and (errors or blockers):
        errors.append("F01 DONE falsely claimed while proof is missing")
    return {"phase": "F01", "f00_state": f00.get("state"),
            "f01_state": f01.get("state"), "f02_release_allowed": False,
            "accepted_gates": sum(x.get("accepted") is True for x in gates),
            "total_gates": len(REQUIRED_G),
            "passed_acceptance_criteria": sum(x.get("passed") is True for x in ac),
            "total_acceptance_criteria": len(REQUIRED_AC),
            "verified_qa_first_passes": sum(x.get("status") == "EXECUTED" and bool(x.get("independent_first_pass_commit")) for x in agents),
            "verified_cross_reviews": sum(x.get("status") == "EXECUTED" for x in cross),
            "blockers": blockers, "integrity_errors": errors,
            "eligible_for_external_release_review": not errors and not blockers,
            "tool_grants_normative_approval": False}

def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--root", type=Path, default=ROOT)
    p.add_argument("--strict", action="store_true")
    args = p.parse_args(argv)
    try:
        state = json.loads((args.root / STATE).read_text(encoding="utf-8"))
        manifest = json.loads((args.root / MANIFEST).read_text(encoding="utf-8"))
        result = inspect(manifest, state)
    except (OSError, ValueError, TypeError) as exc:
        result = {"integrity_errors": [str(exc)], "eligible_for_external_release_review": False}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["integrity_errors"]:
        return 2
    if args.strict and not result["eligible_for_external_release_review"]:
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
