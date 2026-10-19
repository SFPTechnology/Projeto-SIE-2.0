"""Fail-closed F01 checks for isolated QA, normative inventory, and acceptance gates."""
import csv
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[4]

def load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

qa = load("f01_qa_workflow_audit")
inventory = load("f01_inventory_audit")
dashboard = load("f01_gate_dashboard")


def test_copilot_safe_workflow_static_checks_pass_without_credentials():
    workflow = (ROOT / qa.WORKFLOW).read_text(encoding="utf-8")
    result = qa.check(workflow)
    assert result["safe_static_configuration"], result["errors"]
    assert result["actual_copilot_sessions_executed"] == 0
    assert not result["f02_release_allowed"]


@pytest.mark.parametrize("unsafe_change", [
    lambda s: s.replace("contents: read", "contents: write", 1),
    lambda s: s.replace("create,apply_patch,skill", "apply_patch,skill"),
    lambda s: s.replace("ref: $" + "{{ github.sha }}", "ref: main"),
    lambda s: s.replace("--deny-tool=shell", "--allow-all", 1),
    lambda s: s.replace("sha256sum --check", "true"),
    lambda s: s.replace("chmod a-w {} +", "true", 1),
])
def test_copilot_rejects_security_regressions_without_spending_tokens(unsafe_change):
    original = (ROOT / qa.WORKFLOW).read_text(encoding="utf-8")
    mutated = unsafe_change(original)
    assert mutated != original
    result = qa.check(mutated)
    assert not result["safe_static_configuration"]
    assert result["errors"]


def read_inventory():
    with (ROOT / inventory.TABLE).open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    engine = (ROOT / inventory.EDP_ENGINE).read_text(encoding="utf-8")
    return rows, engine


def test_inventory_matches_all_edp_candidates_without_homologation():
    rows, engine = read_inventory()
    result = inventory.inspect(rows, engine)
    assert not result["errors"], result["errors"]
    assert result["records"] >= 24
    assert result["edp_category_candidates"] == 13
    assert result["primary_source_cells_independently_verified"] == 0
    assert not result["eligible_for_release"]


def test_inventory_cannot_omit_edp_category():
    rows, engine = read_inventory()
    rows = [r for r in rows if r["id"] != "EDP-CAT-T2"]
    assert inventory.inspect(rows, engine)["errors"]


def test_inventory_cannot_invent_normative_approval():
    rows, engine = read_inventory()
    rows[0]["estado_de_conferencia"] = "HOMOLOGADO"
    assert any("cannot auto-claim" in e for e in inventory.inspect(rows, engine)["errors"])


def read_release():
    manifest = json.loads((ROOT / dashboard.MANIFEST).read_text(encoding="utf-8"))
    state = json.loads((ROOT / dashboard.STATE).read_text(encoding="utf-8"))
    return manifest, state


def test_six_gates_and_ten_criteria_report_only_actual_accepted():
    manifest, state = read_release()
    result = dashboard.inspect(manifest, state)
    assert not result["integrity_errors"], result["integrity_errors"]
    assert result["accepted_gates"] == 0
    assert result["total_gates"] == 6
    assert result["passed_acceptance_criteria"] == 1
    assert result["total_acceptance_criteria"] == 10
    assert result["verified_qa_first_passes"] == 0
    assert result["verified_cross_reviews"] == 0
    assert not result["eligible_for_external_release_review"]
    assert result["f00_state"] == "DONE"
    assert result["f01_state"] == "BLOCKED"


def test_gates_reject_premature_approval_and_f02_release():
    manifest, state = read_release()
    forged = deepcopy(manifest)
    forged["gates"][0]["accepted"] = True
    assert any("cannot accept" in e for e in dashboard.inspect(forged, state)["integrity_errors"])
    forged = deepcopy(manifest)
    forged["f02_release_allowed"] = True
    assert dashboard.inspect(forged, state)["integrity_errors"]


def test_gates_reject_missing_ac_or_false_phase_done():
    manifest, state = read_release()
    tampered = deepcopy(state)
    next(t for t in tampered["tasks"] if t["id"] == "F01")["criteria"].pop()
    assert dashboard.inspect(manifest, tampered)["integrity_errors"]
    tampered = deepcopy(state)
    next(t for t in tampered["tasks"] if t["id"] == "F01")["state"] = "DONE"
    result = dashboard.inspect(manifest, tampered)
    assert any("falsely claimed" in s for s in result["integrity_errors"])
