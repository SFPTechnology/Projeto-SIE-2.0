from copy import deepcopy

import pytest

from sie_api.representation_f10 import (
    ArtifactContract, ArtifactError, artifact_bundle, cross_validate_documents,
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
    snapshot["circuits"][0]["id"] = "<script>"
    svg = render_single_line_svg(snapshot, contract)
    assert "<script>" not in svg
    assert "&lt;script&gt;" in svg


def test_missing_circuit_in_schedule_is_a_blocker(snapshot, contract):
    schedule = load_schedule(snapshot, contract)
    schedule["rows"].pop()
    assert cross_validate_documents(schedule, snapshot, contract) == [
        "missing scheduled circuit: C2"
    ]


def test_quantity_ledger_preserves_origin_and_status(snapshot, contract):
    snapshot["segments"] = [
        {"id": "S1", "circuit_id": "C1", "length_m": 12.5, "status": "MEASURED",
         "origin": "levantamento local"}
    ]
    bundle = artifact_bundle(snapshot, contract)
    assert "S1" in bundle["quantities.csv"]
    assert "levantamento local" in bundle["quantities.csv"]
    assert "MEASURED" in bundle["report.html"]
    assert "normative conformity" not in bundle["report.html"].lower()


def test_quantity_ledger_rejects_unproven_length(snapshot, contract):
    snapshot["segments"] = [
        {"id": "S1", "circuit_id": "C1", "length_m": 12.5, "status": "ESTIMATED",
         "origin": "orçamento preliminar"}
    ]
    ledger = artifact_bundle(snapshot, contract)["quantities.csv"]
    assert "ESTIMATED" in ledger
    assert "orçamento preliminar" in ledger


def test_quantity_ledger_rejects_unknown_circuit(snapshot, contract):
    snapshot["segments"] = [
        {"id": "S1", "circuit_id": "UNKNOWN", "length_m": 1, "status": "MEASURED",
         "origin": "ensaio"}
    ]
    with pytest.raises(ArtifactError, match="unknown circuit"):
        artifact_bundle(snapshot, contract)


def test_html_report_escapes_untrusted_origin(snapshot, contract):
    snapshot["segments"] = [
        {"id": "S1", "circuit_id": "C1", "length_m": 2, "status": "DOCUMENTED",
         "origin": "<script>alert(1)</script>"}
    ]
    html = artifact_bundle(snapshot, contract)["report.html"]
    assert "<script>" not in html
    assert "&lt;script&gt;" in html


def test_artifact_bundle_outputs_all_supported_formats(snapshot, contract):
    bundle = artifact_bundle(snapshot, contract)
    assert set(bundle) == {"schedule.json", "diagram.svg", "quantities.csv", "report.html"}
    assert '"revision_id": "R-2"' in bundle["schedule.json"]
    assert 'viewBox=' in bundle["diagram.svg"]
    assert bundle["quantities.csv"].startswith("segment_id,circuit_id")
    assert "CALC-3" in bundle["report.html"]
