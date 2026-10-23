from copy import deepcopy
import json
from pathlib import Path

import pytest

from sie_api.representation_f10 import (
    ArtifactContract, ArtifactError, artifact_bundle, cross_validate_documents, main as representation_main,
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
    assert bundle["quantities.csv"].startswith("row_type,project_id,revision_id,calculation_run_id,rule_version,template_version")
    assert "P-1" in bundle["quantities.csv"] and "CALC-3" in bundle["quantities.csv"]
    assert "CALC-3" in bundle["diagram.svg"]
    assert "CALC-3" in bundle["report.html"]


def test_plant_overlay_requires_declared_revision_scale_and_element_ids(snapshot, contract):
    snapshot["floor_plan"] = {
        "id": "FP-1", "revision_id": "R-2", "source_ref": "authorized:plant-01",
        "units": "m", "width": 10, "height": 8, "model_units_per_canvas_unit": 1,
        "placements": [{"element_id": "QD1", "x": 2, "y": 3, "label": "QD1"}],
    }
    bundle = artifact_bundle(snapshot, contract)
    plant = bundle["floor_plan.svg"]
    assert "authorized:plant-01" in plant
    assert 'cx="2" cy="3"' in plant
    assert "floor_plan.svg" in bundle


def test_plant_overlay_blocks_scale_or_revision_mismatch(snapshot, contract):
    snapshot["floor_plan"] = {
        "id": "FP-1", "revision_id": "OLD", "source_ref": "authorized:plant-01",
        "units": "m", "width": 10, "height": 8, "model_units_per_canvas_unit": 0,
        "placements": [],
    }
    with pytest.raises(ArtifactError, match="revision mismatch"):
        artifact_bundle(snapshot, contract)
    snapshot["floor_plan"]["revision_id"] = "R-2"
    with pytest.raises(ArtifactError, match="positive"):
        artifact_bundle(snapshot, contract)


def test_plant_overlay_blocks_placement_outside_canvas(snapshot, contract):
    snapshot["floor_plan"] = {
        "id": "FP-1", "revision_id": "R-2", "source_ref": "authorized:plant-01",
        "units": "m", "width": 10, "height": 8, "model_units_per_canvas_unit": 1,
        "placements": [{"element_id": "QD1", "x": 11, "y": 3}],
    }
    with pytest.raises(ArtifactError, match="outside plan bounds"):
        artifact_bundle(snapshot, contract)


def test_plant_overlay_blocks_unmapped_element(snapshot, contract):
    snapshot["floor_plan"] = {
        "id": "FP-1", "revision_id": "R-2", "source_ref": "authorized:plant-01",
        "units": "m", "width": 10, "height": 8, "model_units_per_canvas_unit": 1,
        "placements": [{"element_id": "UNKNOWN", "x": 2, "y": 3}],
    }
    with pytest.raises(ArtifactError, match="unknown element"):
        artifact_bundle(snapshot, contract)


def test_snapshot_rejects_duplicate_circuit_ids(snapshot, contract):
    snapshot["circuits"].append(dict(snapshot["circuits"][0]))
    with pytest.raises(ArtifactError, match="duplicate circuit id"):
        artifact_bundle(snapshot, contract)


def test_plant_svg_contains_complete_artifact_contract(snapshot, contract):
    snapshot["floor_plan"] = {
        "id": "FP-1", "revision_id": "R-2", "source_ref": "authorized:plant-01",
        "units": "m", "width": 10, "height": 8, "model_units_per_canvas_unit": 1,
        "placements": [],
    }
    svg = artifact_bundle(snapshot, contract)["floor_plan.svg"]
    assert "CALC-3" in svg and "template-1" in svg


def test_cli_creates_revision_bound_artifacts_without_overwrite(snapshot, contract, tmp_path):
    source = tmp_path / "input.json"
    source.write_text(json.dumps({
        "snapshot": snapshot,
        "artifact_contract": contract.__dict__,
    }), encoding="utf-8")
    destination = tmp_path / "result"
    assert representation_main(["--input", str(source), "--output-dir", str(destination)]) == 0
    assert {p.name for p in destination.iterdir()} == {
        "schedule.json", "diagram.svg", "quantities.csv", "report.html"
    }
    with pytest.raises(FileExistsError):
        representation_main(["--input", str(source), "--output-dir", str(destination)])
    assert len(list(destination.iterdir())) == 4
