"""Fail-closed GREENFIELD validation contracts for E06--E09 and E11.

The module intentionally validates evidence completeness and internal
consistency only.  It contains no normative coefficients or approval path.
Every successful synthetic contract stays ``PENDING_EVIDENCE``.
"""
from __future__ import annotations

from decimal import Decimal, InvalidOperation
from hashlib import sha256
import json


def _decimal(value: object, name: str) -> Decimal:
    if isinstance(value, bool):
        raise ValueError(name)
    try:
        result = Decimal(str(value))
    except (InvalidOperation, TypeError, ValueError) as exc:
        raise ValueError(name) from exc
    if not result.is_finite() or result <= 0:
        raise ValueError(name)
    return result


def _mapping(value: object, keys: set[str], label: str) -> dict:
    if not isinstance(value, dict) or set(value) != keys:
        raise ValueError(label)
    return value


def _pending(check: str, *, consistent: bool, missing: list[str] | None = None) -> dict:
    return {
        "check": check,
        "status": "PENDING_EVIDENCE" if consistent else "FAIL",
        "synthetic_only": True,
        "normative_approval": False,
        "consistent": consistent,
        "missing_evidence": sorted(missing or []),
    }


def evaluate_e06_protection(data: object) -> dict:
    """Check explicit protection values without inferring a breaker curve."""
    row = _mapping(data, {
        "ib_a", "in_a", "iz_a", "i2_a", "icc_a", "interrupting_a",
        "curve_ref", "selectivity_ref", "source_ref",
    }, "E06 contract")
    ib, inn, iz = (_decimal(row[key], key) for key in ("ib_a", "in_a", "iz_a"))
    i2, icc, interrupting = (_decimal(row[key], key) for key in ("i2_a", "icc_a", "interrupting_a"))
    for name in ("curve_ref", "selectivity_ref", "source_ref"):
        if not isinstance(row[name], str) or not row[name].strip():
            raise ValueError(name)
    consistent = ib <= inn <= iz and interrupting >= icc and i2 >= inn
    missing = [] if consistent else ["OVERLOAD_OR_INTERRUPTING_CAPACITY_INCONSISTENT"]
    return _pending("E06", consistent=consistent, missing=missing) | {
        "ib_le_in_le_iz": ib <= inn <= iz,
        "interrupting_capacity_ok": interrupting >= icc,
        "i2_not_below_in": i2 >= inn,
    }


def evaluate_e07_dr_dps(data: object) -> dict:
    row = _mapping(data, {
        "dr_present", "dr_current_a", "dps_present", "dps_uc_v",
        "system_voltage_v", "application_ref", "source_ref",
    }, "E07 contract")
    if not isinstance(row["dr_present"], bool) or not isinstance(row["dps_present"], bool):
        raise ValueError("E07 presence")
    voltage = _decimal(row["system_voltage_v"], "system_voltage_v")
    dr = _decimal(row["dr_current_a"], "dr_current_a")
    uc = _decimal(row["dps_uc_v"], "dps_uc_v")
    for name in ("application_ref", "source_ref"):
        if not isinstance(row[name], str) or not row[name].strip():
            raise ValueError(name)
    consistent = row["dr_present"] and row["dps_present"] and dr > 0 and uc >= voltage
    missing = [] if consistent else ["DR_DPS_REQUIRED_OR_INCOMPATIBLE"]
    return _pending("E07", consistent=consistent, missing=missing) | {"dps_uc_not_below_voltage": uc >= voltage}


def evaluate_e08_grounding(data: object) -> dict:
    row = _mapping(data, {
        "earthing_system", "pe_present", "neutral_present", "equipotential_bonding",
        "shock_protection_ref", "source_ref",
    }, "E08 contract")
    if row["earthing_system"] not in {"TT", "TN", "IT"}:
        raise ValueError("earthing_system")
    for name in ("pe_present", "neutral_present", "equipotential_bonding"):
        if not isinstance(row[name], bool):
            raise ValueError(name)
    for name in ("shock_protection_ref", "source_ref"):
        if not isinstance(row[name], str) or not row[name].strip():
            raise ValueError(name)
    consistent = row["pe_present"] and row["equipotential_bonding"]
    return _pending("E08", consistent=consistent,
                    missing=[] if consistent else ["PE_OR_EQUIPOTENTIAL_BONDING_MISSING"]) | {
                        "earthing_system": row["earthing_system"]}


def evaluate_e09_utility_catalog(data: object) -> dict:
    row = _mapping(data, {"utility", "category", "version", "effective_date", "source_ref", "cell_ref"}, "E09 contract")
    for name in row:
        if not isinstance(row[name], str) or not row[name].strip():
            raise ValueError(name)
    digest = sha256(json.dumps(row, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return _pending("E09", consistent=True) | {"catalog_sha256": digest, "catalog_identity": f"{row['utility']}:{row['version']}:{row['cell_ref']}"}


def evaluate_e11_integrity(payload: object, expected_sha256: object, catalog_version: object) -> dict:
    if not isinstance(payload, dict) or not isinstance(expected_sha256, str) or len(expected_sha256) != 64:
        raise ValueError("E11 payload/hash")
    if not isinstance(catalog_version, str) or not catalog_version.strip():
        raise ValueError("catalog_version")
    actual = sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    consistent = actual == expected_sha256
    return _pending("E11", consistent=consistent,
                    missing=[] if consistent else ["EVIDENCE_HASH_MISMATCH"]) | {
                        "actual_sha256": actual,
                        "catalog_version": catalog_version,
                        "force_approve_allowed": False,
                    }
