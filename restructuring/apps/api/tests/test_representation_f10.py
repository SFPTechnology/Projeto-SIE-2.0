from copy import deepcopy

import pytest

from sie_api.representation_f10 import (
    ArtifactContract, ArtifactError, cross_validate_documents,
    load_schedule, render_single_line_svg,
)


@pytest.fixture
def snapshot():
    return {
        "project_id": "P-1",
        "revision_id": "R-2",
        "calculation_run_id": "CALC-3",
        "rule_version": "rules-1",
        "elements": [{"id": "QD1", "kind": "panel"}],
        "circuits": [
            {"id": "C1", "panel_id": "QD1", "load_va": 1200, "phase": "L1",
             "breaker_id": "DJ1", "conductor_id": "COND1"},
            {"id": "C2", "panel_id": "QD1", "load_va": 800, "phase": "L2",
             "breaker_id": "DJ2", "conductor_id": "COND2"},
        ],
    }


@pytest.fixture
def contract():
    return ArtifactContract("P-1", "R-2", "CALC-3", "rules-1", "template-1")


def test_schedule_and_diagram_share_exact_snapshot(snapshot, contract):
    schedule = load_schedule(snapshot, contract)
    svg = render_single_line_svg(snapshot, contract)
    assert schedule["revision_id"] == "R-2"
    assert schedule["calculation_run_id"] == "CALC-3"
    assert [r["circuit_id"] for r in schedule["rows"]] == ["C1", "C2"]
    assert "C1" in svg and "DJ1" in svg and "COND1" in svg
    assert schedule["status"] == "study"
    assert schedule["normative_conformity_verified"] is False
    assert cross_validate_documents(schedule, snapshot, contract) == []


def test_contract_rejects_mixed_revision(snapshot):
    contract = ArtifactContract("P-1", "R-OTHER", "CALC-3", "rules-1", "template-1")
    with pytest.raises(ArtifactError, match="revision_id"):
        load_schedule(snapshot, contract)


def test_cross_validation_blocks_different_breaker(snapshot, contract):
    schedule = load_schedule(snapshot, contract)
    schedule["rows"][0]["breaker_id"] = "DJ-WRONG"
    assert "circuit C1 mismatch: breaker_id" in cross_validate_documents(schedule, snapshot, contract)


def test_snapshot_rejects_unknown_panel(snapshot, contract):
    broken = deepcopy(snapshot)
    broken["circuits"][0]["panel_id"] = "QD-UNKNOWN"
    with pytest.raises(ArtifactError, match="unknown panel"):
        load_schedule(broken, contract)


def test_snapshot_rejects_nonfinite_or_negative_load(snapshot, contract):
    broken = deepcopy(snapshot)
    broken["circuits"][0]["load_va"] = float("nan")
    with pytest.raises(ArtifactError, match="finite"):
        load_schedule(broken, contract)
    broken["circuits"][0]["load_va"] = -1
    with pytest.raises(ArtifactError, match="negative"):
        load_schedule(broken, contract)


def test_svg_escapes_untrusted_labels(snapshot, contract):
    snapshot["elements"][0]["id"] = "<script>"
    svg = render_single_line_svg(snapshot, contract)
    assert "<script>" not in svg
    assert "&lt;script&gt;" in svg


def test_missing_circuit_in_schedule_is_a_blocker(snapshot, contract):
    schedule = load_schedule(snapshot, contract)
    schedule["rows"].pop()
    assert cross_validate_documents(schedule, snapshot, contract) == [
        "missing scheduled circuit: C2"
    ]
