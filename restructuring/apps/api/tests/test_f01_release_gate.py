"""Regression: no F01/F02 approval via artificial QA manifests or missing evidence."""
from copy import deepcopy
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SCRIPT = ROOT / "scripts" / "f01_release_gate.py"
spec = importlib.util.spec_from_file_location("f01_release_gate", SCRIPT)
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


def _docs():
    m = json.loads((ROOT / "docs/implantacao-sie-2-0/F01/QA3_MANIFEST.json").read_text(encoding="utf-8"))
    state = json.loads((ROOT / "docs/sie-orchestrator/ORCHESTRATOR_STATE.json").read_text(encoding="utf-8"))
    return m, state


def test_github_agent_skills_declared_and_independent_paths_exist():
    assert guard.verify_profiles(ROOT) == []


def test_f01_current_project_closed_without_fake_normative_100_percent():
    m, state = _docs()
    out = guard.inspect(ROOT, m, state)
    assert out["integrity_errors"] == []
    assert out["f01_state"] == "DONE"
    assert out["project_f01_closed"] is True
    assert out["f02_development_allowed"] is True
    assert out["passed_gates"] == []
    assert out["evidence_ready_for_external_decision"] is False
    assert out["f02_release_allowed"] is False


def test_manual_checkboxes_without_evidence_are_rejected():
    m, state = _docs()
    m = deepcopy(m)
    for gate in m["gates"]:
        gate.update(status="PASS", accepted=True, independent_external_verification=True)
    result = guard.inspect(ROOT, m, state)
    assert len(result["integrity_errors"]) >= 6
    assert result["evidence_ready_for_external_decision"] is False


def test_release_flag_cannot_be_turned_on_from_blocked():
    m, state = _docs()
    m["f02_release_allowed"] = True
    errors = guard.inspect(ROOT, m, state)["integrity_errors"]
    assert any("F02" in error for error in errors)


def test_agent_sessions_must_not_share_same_first_pass_commit():
    m, state = _docs()
    for agent in m["agents"]:
        agent["status"] = "REVIEWED"
        agent["independent_first_pass_commit"] = "a" * 40
        agent["review_package"] = "different-path.md"
    err = guard.inspect(ROOT, m, state)["integrity_errors"]
    assert any("mesmo commit" in error for error in err)


def test_f01_done_without_external_evidence_or_owner_decision_is_rejected():
    m, state = _docs()
    m.pop("project_acceptance", None)
    next(t for t in state["tasks"] if t["id"] == "F01").pop("project_acceptance", None)
    m["state"] = "DONE"
    for task in state["tasks"]:
        if task["id"] == "F01":
            task["state"] = "DONE"
    errors = guard.inspect(ROOT, m, state)["integrity_errors"]
    assert any("F01 DONE" in e for e in errors)


def test_evidence_sha256_and_path_traversal_guard(tmp_path):
    file = tmp_path / "fixture.txt"
    file.write_text("evidencia de ensaio somente", encoding="utf-8")
    proof = {"path": "fixture.txt", "sha256": sha256(file.read_bytes()).hexdigest()}
    assert guard.evidence_ok(tmp_path, proof)
    assert not guard.evidence_ok(tmp_path, {**proof, "sha256": "0" * 64})
    assert not guard.evidence_ok(tmp_path, {**proof, "path": "../fixture.txt"})


def test_f01_gate_main_verifies_without_changing_source(tmp_path):
    # Verify stdout/exit semantics against committed source; no edits or side effects.
    assert guard.main(["--root", str(ROOT), "--verify-invariants"]) == 0
    assert guard.main(["--root", str(ROOT), "--check-release"]) == 1
    assert guard.main(["--root", str(ROOT), "--check-development"]) == 0
