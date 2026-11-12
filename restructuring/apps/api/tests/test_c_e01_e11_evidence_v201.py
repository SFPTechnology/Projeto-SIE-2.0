"""Eleven engineering groups actually execute C04/C05 code against synthetic oracles.

Green means *arithmetical invariant or fail-closed safety*, NEVER ABNT/EDP
validation, professional signoff, authorization to merge, or live ETL.
"""
from pathlib import Path
import json
import pytest
from sie_api import v201_c_e01_e11_evidence as evidence

@pytest.mark.parametrize("code", sorted(evidence.REQUIRED))
def test_each_e01_e11_actual_engine_or_guard(code):
    result = evidence.EVALUATORS[code]()
    assert result["group"] == code
    assert result["assertion"] == "PASS"
    assert result["normative_status"] == "NOT_EVALUATED"
    assert result["professional_signature"] is None
    assert result["pending_independent_evidence"]

def test_suite_is_exhaustive_and_does_not_promote_gc():
    report = evidence.run_suite(sha="a"*40)
    assert report["execution_status"] == "PASS_ALL_11_DEVELOPMENT_ASSERTIONS"
    assert report["groups_executed"] == 11
    assert report["commit_sha"] == "a"*40
    assert report["professional_approval"] == "NOT_GRANTED"
    assert report["normative_conformity"] == "NOT_EVALUATED"
    assert report["migration_authorized"] is False
    assert report["gc"] == "BLOCKED"
    assert len(set(report["case_digests_sha256"])) == 11

def test_export_machine_readable_real_results(tmp_path):
    target = tmp_path/"e01-e11-evidence.json"
    evidence.main(["--output", str(target)])
    packet = json.loads(target.read_text(encoding="utf-8"))
    assert packet["groups_executed"] == 11
    assert len(packet["cases"]) == 11
    assert packet["environment"] == "OFFLINE_SYNTHETIC_NO_REMOTE_DB"
    assert all(x["input_class"]=="SYNTHETIC_UNLICENSED" for x in packet["cases"])

def test_caught_engine_arithmetic_regression_cannot_fake_pass(monkeypatch):
    original=evidence.analyze_explicit
    def bad_analyze(va, voltage, phase, technical):
        result=original(va,voltage,phase,technical)
        result["design_current_a"] = "999999"
        return result
    monkeypatch.setattr(evidence,"analyze_explicit",bad_analyze)
    with pytest.raises(ValueError, match="E01-E11 evidence assertion failed"):
        evidence.evaluate_e02()

def test_e07_false_compliance_or_e09_fake_catalog_state_fails(monkeypatch):
    original=evidence.analyze_explicit
    def fake_release(*args,**kwargs):
        result=original(*args,**kwargs)
        result["liberado_para_uso_normativo"]=True
        return result
    monkeypatch.setattr(evidence,"analyze_explicit",fake_release)
    with pytest.raises(ValueError,match="E01-E11 evidence assertion failed"):
        evidence.evaluate_e07()
    with pytest.raises(ValueError,match="E01-E11 evidence assertion failed"):
        evidence.evaluate_e08()
    with pytest.raises(ValueError,match="E01-E11 evidence assertion failed"):
        evidence.evaluate_e11()

def test_result_hashes_are_deterministic_without_git_sha():
    first=evidence.run_suite(sha="A")
    second=evidence.run_suite(sha="B")
    assert first["case_digests_sha256"]==second["case_digests_sha256"]
