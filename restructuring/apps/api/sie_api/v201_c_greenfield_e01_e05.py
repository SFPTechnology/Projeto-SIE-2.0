"""GREENFIELD E01--E05 input contracts.

This module deliberately performs no normative lookup.  It accepts only
explicit, traceable engineering inputs and reports ``PENDING_EVIDENCE`` when
an otherwise mathematical result would depend on a missing catalogue cell or
professional source.  It is therefore safe to use in synthetic development
and cannot turn absent normative data into an approval.
"""
from __future__ import annotations

from decimal import Decimal, InvalidOperation, localcontext


class GreenfieldInputError(ValueError):
    """Raised for malformed or physically impossible explicit input."""


def _decimal(value: object, field: str, *, positive: bool = True) -> Decimal:
    if isinstance(value, bool):
        raise GreenfieldInputError(field)
    try:
        parsed = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise GreenfieldInputError(field) from exc
    if not parsed.is_finite() or (parsed <= 0 if positive else parsed < 0):
        raise GreenfieldInputError(field)
    return parsed


def _reference(value: object, field: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str) or not value.strip():
        raise GreenfieldInputError(field)
    return value.strip()


def apparent_power_va(value: object, unit: object, power_factor: object | None = None) -> Decimal:
    """Normalise an explicit power quantity without guessing a power factor."""
    amount = _decimal(value, "power")
    if unit == "VA":
        return amount
    if unit == "KVA":
        return amount * Decimal("1000")
    if unit in ("W", "KW"):
        if power_factor is None:
            raise GreenfieldInputError("power_factor_required_for_active_power")
        pf = _decimal(power_factor, "power_factor")
        if pf > 1:
            raise GreenfieldInputError("power_factor")
        watts = amount * (Decimal("1000") if unit == "KW" else 1)
        return watts / pf
    raise GreenfieldInputError("power_unit")


def evaluate_e01_e05(inputs: dict) -> dict:
    """Evaluate only explicitly supported E01--E05 development assertions.

    The return shape is deterministic and every non-proven dimension is kept
    in ``pending``.  ``status`` is never ``PASS`` because the module neither
    owns nor imports normative sources.
    """
    if not isinstance(inputs, dict):
        raise GreenfieldInputError("inputs")
    allowed = {
        "room", "loads", "voltage_v", "phase_mode", "demand_factor",
        "demand_source_ref", "cable_catalog", "cable_source_ref",
        "correction_factor", "selected_mm2", "length_m",
        "resistance_ohm_km", "reactance_ohm_km", "rx_source_ref",
        "power_factor",
    }
    unknown = set(inputs) - allowed
    if unknown:
        raise GreenfieldInputError("unknown_input:" + ",".join(sorted(unknown)))
    room = inputs.get("room")
    if not isinstance(room, dict) or set(room) != {"area_m2", "perimeter_m", "type"}:
        raise GreenfieldInputError("room")
    _decimal(room["area_m2"], "area_m2")
    _decimal(room["perimeter_m"], "perimeter_m")
    if not isinstance(room["type"], str) or not room["type"].strip():
        raise GreenfieldInputError("room_type")
    loads = inputs.get("loads")
    if not isinstance(loads, list) or not loads:
        raise GreenfieldInputError("loads")
    total = Decimal(0)
    for load in loads:
        if not isinstance(load, dict) or set(load) != {"kind", "value", "unit", "power_factor"}:
            raise GreenfieldInputError("load")
        if load["kind"] not in {"LIGHTING", "TUG", "TUE", "OTHER"}:
            raise GreenfieldInputError("load_kind")
        total += apparent_power_va(load["value"], load["unit"], load["power_factor"])
    voltage = _decimal(inputs.get("voltage_v"), "voltage_v")
    phase = inputs.get("phase_mode")
    if phase not in {"SINGLE", "THREE"}:
        raise GreenfieldInputError("phase_mode")
    with localcontext() as ctx:
        ctx.prec = 48
        current = total / (voltage if phase == "SINGLE" else Decimal(3).sqrt() * voltage)
    pending = [
        "E01_NORMATIVE_MINIMA_SOURCE_MISSING",
        "E04_APPLICATION_CONDITIONS_SOURCE_MISSING",
        "E05_NORMATIVE_LIMIT_SOURCE_MISSING",
    ]
    result = {
        "status": "PENDING_EVIDENCE",
        "liberado_para_uso_normativo": False,
        "installed_apparent_power_va": str(total),
        "design_current_a": str(current),
        "phase_mode": phase,
        "pending": pending,
    }
    factor = inputs.get("demand_factor")
    demand_ref = _reference(inputs.get("demand_source_ref"), "demand_source_ref")
    if factor is None or demand_ref is None:
        pending.append("E03_DEMAND_FACTOR_SOURCE_MISSING")
    else:
        demand = _decimal(factor, "demand_factor")
        if demand > 1:
            raise GreenfieldInputError("demand_factor")
        result["demand_va"] = str(total * demand)
        result["demand_source_ref"] = demand_ref
    catalog = inputs.get("cable_catalog")
    cable_ref = _reference(inputs.get("cable_source_ref"), "cable_source_ref")
    correction = inputs.get("correction_factor")
    selected = inputs.get("selected_mm2")
    if None in (catalog, cable_ref, correction, selected):
        pending.append("E04_AMPACITY_SOURCE_MISSING")
    else:
        if not isinstance(catalog, list) or not catalog:
            raise GreenfieldInputError("cable_catalog")
        entries = { _decimal(row["mm2"], "cable_mm2"): _decimal(row["ampacity_a"], "ampacity_a")
                    for row in catalog
                    if isinstance(row, dict) and set(row) == {"mm2", "ampacity_a"} }
        if len(entries) != len(catalog):
            raise GreenfieldInputError("cable_catalog")
        selected_value = _decimal(selected, "selected_mm2")
        if selected_value not in entries:
            raise GreenfieldInputError("selected_mm2")
        factor_value = _decimal(correction, "correction_factor")
        if factor_value > 1:
            raise GreenfieldInputError("correction_factor")
        result["corrected_ampacity_a"] = str(entries[selected_value] * factor_value)
        result["cable_source_ref"] = cable_ref
    rx_ref = _reference(inputs.get("rx_source_ref"), "rx_source_ref")
    rx_keys = ("length_m", "resistance_ohm_km", "reactance_ohm_km", "power_factor")
    if rx_ref is None or any(inputs.get(key) is None for key in rx_keys):
        pending.append("E05_RX_SOURCE_MISSING")
    else:
        length, resistance, reactance = (_decimal(inputs[key], key, positive=False)
                                        for key in rx_keys[:3])
        pf = _decimal(inputs["power_factor"], "power_factor")
        if pf > 1:
            raise GreenfieldInputError("power_factor")
        scalar = Decimal(2) if phase == "SINGLE" else Decimal(3).sqrt()
        drop = scalar * (length / Decimal(1000)) * current * (resistance * pf + reactance * (1 - pf * pf).sqrt())
        result["voltage_drop_v"] = str(drop)
        result["rx_source_ref"] = rx_ref
    result["pending"] = sorted(set(pending))
    return result
