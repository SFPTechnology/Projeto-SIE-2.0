"""C05 exact arithmetic golden and fail-closed checks, synthetic inputs only."""
from decimal import Decimal
import pytest
from sie_api.v201_c_explicit_checks import analyze_explicit

BASE={"correction_factor":"0.8",
      "cable_catalog":[["2.5","25"],["4","32"]],
      "selected_mm2":"2.5","breaker_a":"16",
      "length_m":"30","resistance_ohm_km":"4",
      "reactance_ohm_km":"0.1","power_factor":"0.8",
      "phase_label":"A","demand_factor":"0.8"}

def test_single_phase_known_values():
    r=analyze_explicit("1270","127","SINGLE",BASE)
    assert Decimal(r["design_current_a"])==Decimal("10")
    assert Decimal(r["demand_va"])==Decimal("1016")
    assert r["overcurrent"]["ib_le_in_le_iz"] is True
    assert Decimal(r["voltage_drop"]["drop_v"])==Decimal("1.956")
    assert r==analyze_explicit("1270","127","SINGLE",BASE)
    assert r["normative_status"]=="EVIDENCE_PENDING"
    assert r["liberado_para_uso_normativo"] is False
    assert "DR_DPS_EARTHING_UNVERIFIED" in r["pending"]

def test_three_phase_balanced_declared_only():
    opts={**BASE,"breaker_a":"20"}
    opts.pop("phase_label")
    r=analyze_explicit("6600","220","THREE",opts)
    assert abs(Decimal(r["design_current_a"])-Decimal("17.320508"))<Decimal("0.000001")
    assert r["overcurrent"]["ib_le_in_le_iz"] is True
    assert r["liberado_para_uso_normativo"] is False

def test_missing_fields_remain_pending():
    r=analyze_explicit("1270","127","SINGLE",{})
    assert "CABLE_AMPACITY_BREAKER_INPUTS_MISSING" in r["pending"]
    assert "RX_LENGTH_PF_UNVERIFIED" in r["pending"]
    assert "PHASE_ASSIGNMENT_REQUIRED" in r["pending"]
    assert "voltage_drop" not in r

def test_overcurrent_failure_fails_closed():
    r=analyze_explicit("1270","127","SINGLE",{**BASE,"breaker_a":"25"})
    assert r["mathematical_status"]=="REVIEW_REQUIRED"
    assert r["overcurrent"]["ib_le_in_le_iz"] is False

@pytest.mark.parametrize("field,value",[
("power_factor","1.1"),("demand_factor","1.2"),
("length_m","NaN"),("resistance_ohm_km","Infinity"),
("selected_mm2","3"),("correction_factor","1.1"),
("breaker_a",True)])
def test_invalid_parameters_rejected(field,value):
    with pytest.raises(ValueError):
        analyze_explicit("1270","127","SINGLE",{**BASE,field:value})

def test_invalid_phase_and_unknown_field_rejected():
    with pytest.raises(ValueError):
        analyze_explicit("1270","127","TWO",BASE)
    with pytest.raises(ValueError):
        analyze_explicit("1270","127","SINGLE",{**BASE,"approve":True})
    with pytest.raises(ValueError):
        analyze_explicit("1270","127","THREE",BASE)
