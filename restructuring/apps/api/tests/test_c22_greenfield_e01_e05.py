from decimal import Decimal

import pytest

from sie_api.v201_c_greenfield_e01_e05 import GreenfieldInputError, evaluate_e01_e05


def complete_inputs():
    return {
        "room": {"area_m2": "12", "perimeter_m": "14", "type": "OFFICE"},
        "loads": [
            {"kind": "LIGHTING", "value": "100", "unit": "W", "power_factor": "1"},
            {"kind": "TUG", "value": "0.6", "unit": "KVA", "power_factor": None},
        ],
        "voltage_v": "220", "phase_mode": "SINGLE",
        "demand_factor": "0.7", "demand_source_ref": "SYNTHETIC-DEMAND-1",
        "cable_catalog": [{"mm2": "2.5", "ampacity_a": "21"}],
        "cable_source_ref": "SYNTHETIC-CABLE-1", "correction_factor": "0.8", "selected_mm2": "2.5",
        "length_m": "20", "resistance_ohm_km": "7", "reactance_ohm_km": "0.08",
        "rx_source_ref": "SYNTHETIC-RX-1", "power_factor": "0.9",
    }


def test_golden_explicit_inputs_are_deterministic_and_never_normatively_released():
    first = evaluate_e01_e05(complete_inputs())
    second = evaluate_e01_e05(complete_inputs())
    assert first == second
    assert first["status"] == "PENDING_EVIDENCE"
    assert first["liberado_para_uso_normativo"] is False
    assert Decimal(first["installed_apparent_power_va"]) == Decimal("700")
    assert Decimal(first["demand_va"]) == Decimal("490.0")
    assert Decimal(first["corrected_ampacity_a"]) == Decimal("16.8")
    assert "E01_NORMATIVE_MINIMA_SOURCE_MISSING" in first["pending"]


@pytest.mark.parametrize("field,value", [("voltage_v", "0"), ("phase_mode", "TWO")])
def test_invalid_topology_or_voltage_is_rejected(field, value):
    data = complete_inputs()
    data[field] = value
    with pytest.raises(GreenfieldInputError):
        evaluate_e01_e05(data)


def test_active_power_without_pf_is_rejected_instead_of_guessed():
    data = complete_inputs()
    data["loads"][0]["power_factor"] = None
    with pytest.raises(GreenfieldInputError, match="power_factor_required"):
        evaluate_e01_e05(data)


def test_zero_is_not_treated_as_missing_rx_data():
    data = complete_inputs()
    data["resistance_ohm_km"] = "0"
    data["reactance_ohm_km"] = "0"
    output = evaluate_e01_e05(data)
    assert Decimal(output["voltage_drop_v"]) == 0


def test_missing_catalogue_produces_pending_evidence_not_approval():
    data = complete_inputs()
    data["cable_catalog"] = None
    output = evaluate_e01_e05(data)
    assert output["status"] == "PENDING_EVIDENCE"
    assert "E04_AMPACITY_SOURCE_MISSING" in output["pending"]
