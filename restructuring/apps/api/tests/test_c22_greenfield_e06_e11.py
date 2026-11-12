from __future__ import annotations

from hashlib import sha256
import json
import pytest

from sie_api.v201_c_greenfield_e06_e11 import (
    evaluate_e06_protection, evaluate_e07_dr_dps, evaluate_e08_grounding,
    evaluate_e09_utility_catalog, evaluate_e11_integrity,
)


def test_e06_synthetic_golden_contract_stays_pending():
    result = evaluate_e06_protection({
        "ib_a": 10, "in_a": 16, "iz_a": 20, "i2_a": 20, "icc_a": 1000,
        "interrupting_a": 3000, "curve_ref": "SYNTHETIC-CURVE", "selectivity_ref": "SYNTHETIC-SELECTIVITY", "source_ref": "SYNTHETIC-CONTRACT",
    })
    assert result["status"] == "PENDING_EVIDENCE"
    assert result["ib_le_in_le_iz"] is True
    assert result["normative_approval"] is False


@pytest.mark.parametrize("field,value", [("in_a", 8), ("interrupting_a", 500)])
def test_e06_rejects_internal_inconsistency(field, value):
    fixture = {"ib_a": 10, "in_a": 16, "iz_a": 20, "i2_a": 20, "icc_a": 1000,
               "interrupting_a": 3000, "curve_ref": "c", "selectivity_ref": "s", "source_ref": "x"}
    fixture[field] = value
    assert evaluate_e06_protection(fixture)["status"] == "FAIL"


def test_e07_e08_positive_contracts_never_approve_normative_use():
    e07 = evaluate_e07_dr_dps({"dr_present": True, "dr_current_a": 25, "dps_present": True,
                                "dps_uc_v": 275, "system_voltage_v": 230,
                                "application_ref": "synthetic", "source_ref": "synthetic"})
    e08 = evaluate_e08_grounding({"earthing_system": "TN", "pe_present": True, "neutral_present": True,
                                  "equipotential_bonding": True, "shock_protection_ref": "synthetic", "source_ref": "synthetic"})
    assert e07["status"] == e08["status"] == "PENDING_EVIDENCE"
    assert not e07["normative_approval"] and not e08["normative_approval"]


@pytest.mark.parametrize("fn,row", [
    (evaluate_e07_dr_dps, {"dr_present": False, "dr_current_a": 25, "dps_present": True, "dps_uc_v": 275, "system_voltage_v": 230, "application_ref": "a", "source_ref": "b"}),
    (evaluate_e08_grounding, {"earthing_system": "TT", "pe_present": False, "neutral_present": True, "equipotential_bonding": True, "shock_protection_ref": "a", "source_ref": "b"}),
])
def test_e07_e08_fail_closed_for_missing_safety_condition(fn, row):
    assert fn(row)["status"] == "FAIL"


def test_e09_provenance_is_hashed_and_e11_detects_tamper():
    catalog = {"utility": "TEST-UTILITY", "category": "X", "version": "fixture-v1", "effective_date": "2026-01-01", "source_ref": "fixture", "cell_ref": "A1"}
    assert evaluate_e09_utility_catalog(catalog)["status"] == "PENDING_EVIDENCE"
    payload = {"catalog": catalog, "result": "synthetic"}
    digest = sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    assert evaluate_e11_integrity(payload, digest, "fixture-v1")["status"] == "PENDING_EVIDENCE"
    assert evaluate_e11_integrity(payload, "0" * 64, "fixture-v1")["status"] == "FAIL"


def test_contracts_reject_unknown_or_missing_fields():
    with pytest.raises(ValueError):
        evaluate_e09_utility_catalog({"utility": "x"})
    with pytest.raises(ValueError):
        evaluate_e11_integrity([], "0" * 64, "v1")
