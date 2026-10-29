"""C11/C12 automated E01..E11 *development* verification with actual C05 engines.

Uses synthetic arithmetic fixtures only. The evaluator is independently
reproducible, refuses to infer regulatory limits and cannot issue any professional
approval, normative release, merge or remote migration authorization.

python -m sie_api.v201_c_e01_e11_evidence --output <file.json>
"""
from __future__ import annotations

from decimal import Decimal
from hashlib import sha256
from pathlib import Path
import argparse
import csv
import json
import os
from io import StringIO

from .v201_c_calculation import calculate
from .v201_c_explicit_checks import analyze_explicit
from .v201_c_normative import catalog_snapshot, resolve_rule
from .v201_c_field_review import verify_field_review


BASE = Path(__file__).resolve().parents[4]
SOURCE = BASE / "docs/implantacao-sie-2-0/GREENFIELD/C02_MATRIZ_COMPLETA_OPERACIONAL_V201.csv"
REVIEW = BASE / "docs/implantacao-sie-2-0/GREENFIELD/C02_REVISAO_SEMANTICA_45_CAMPOS_V201.csv"
PID = "11111111-1111-4111-8111-111111111111"
RID = "22222222-2222-4222-8222-222222222222"
ROOM = "33333333-3333-4333-8333-333333333333"

SYNTHETIC = {
    "correction_factor": "0.8",
    "cable_catalog": [["2.5", "24"], ["4", "32"]],
    "selected_mm2": "4",
    "breaker_a": "20",
    "length_m": "30",
    "resistance_ohm_km": "7.41",
    "reactance_ohm_km": "0",
    "power_factor": "1",
    "phase_label": "A",
    "demand_factor": "0.75",
}
REQUIRED = frozenset(f"E{i:02d}" for i in range(1, 12))

def _require(condition, message):
    if not condition:
        raise ValueError("E01-E11 evidence assertion failed: " + message)

def _canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False,
                      separators=(",", ":"), allow_nan=False)

def _record(group, case, expected, observed, blockers, *, detail):
    _require(expected == observed, f"{group}/{case}: expected {expected!r}, observed {observed!r}")
    return {
        "group": group, "case_id": case,
        "observed": observed, "expected": expected, "assertion": "PASS",
        "input_class": "SYNTHETIC_UNLICENSED",
        "independent_reference": detail,
        "development_status": "PASS_GUARD_OR_ARITHMETIC",
        "normative_status": "NOT_EVALUATED",
        "professional_signature": None,
        "pending_independent_evidence": blockers,
    }

def _single(**override):
    return analyze_explicit("4400", "220", "SINGLE", {**SYNTHETIC, **override})

def evaluate_e01():
    snap = {
        "schema_version": 1, "project_id": PID, "revision_id": RID,
        "rooms": [{
            "id": ROOM, "project_id": PID, "revision_id": RID,
            "width_m": "4", "length_m": "5", "excluded_perimeter_m": "0",
        }],
        "loads": [], "circuits": [], "links": [],
    }
    output = calculate(snap)
    _require(not output["liberado_para_uso_normativo"], "E01 cannot release lighting/TUG")
    return _record(
        "E01", "E01-GUARD-NO-INFERRED-LIGHTING-AND-TUG",
        {"va": "0.000", "pending": True},
        {"va": output["installed_apparent_power_va"],
         "pending": "illumination_and_tug_normative" in output["pending_checks"]},
        ["Independent NBR 5410 lighting/TUG minimum and space-type golden cases",
         "C05 does not compute lighting/TUG minima"], detail="No source load => VA=0; no guessed minimum")

def evaluate_e02():
    result = _single()
    tri = analyze_explicit("6600", "220", "THREE",
                           {k: v for k, v in SYNTHETIC.items() if k != "phase_label"})
    _require(abs(Decimal(tri["design_current_a"]) -
                 Decimal("6600") / (Decimal("3").sqrt() * Decimal("220"))) <
             Decimal("0.00000000001"), "E02 independent three-phase current")
    invalid = False
    try:
        analyze_explicit("4400", "0", "SINGLE", SYNTHETIC)
    except ValueError:
        invalid = True
    return _record(
        "E02", "E02-CURRENTS-AND-MISSING-VOLTAGE",
        {"single_a": "20", "three_phase_formula_ok": True, "no_zero_voltage": True,
         "normative_release": False},
        {"single_a": str(Decimal(result["design_current_a"])),
         "three_phase_formula_ok": True, "no_zero_voltage": invalid,
         "normative_release": result["liberado_para_uso_normativo"]},
        ["Real phase/neutral/line-line topology", "W and BTU/h conversion rules require evidence",
         "four missing voltages and two three-phase legacy loads"],
        detail="Single: 4400/220=20 A; three-phase: 6600/(sqrt(3)*220) A")

def evaluate_e03():
    result = _single()
    nofactor = _single(demand_factor=None)
    return _record(
        "E03", "E03-DECLARED-DEMAND-AND-NO-INFER",
        {"demand_va": "3300.00", "factor_absent_pending": True},
        {"demand_va": str(Decimal(result["demand_va"]).quantize(Decimal("0.01"))),
         "factor_absent_pending": "DEMAND_FACTOR_UNVERIFIED" in nofactor["pending"]},
        ["Demand factors official per intended classification",
         "Phase assignment, distribution of circuits and balance remain untested"],
        detail="4400 VA x 0.75 explicit hypothetical factor = 3300 VA")

def evaluate_e04():
    result = _single()
    return _record(
        "E04", "E04-AMPACITY-CORRECTION-SYNTHETIC",
        {"min_mm2": "4", "chosen_mm2": "4", "iz_a": "25.6"},
        {"min_mm2": str(Decimal(result["conductor"]["minimum_mm2"]).normalize()),
         "chosen_mm2": str(Decimal(result["conductor"]["selected_mm2"]).normalize()),
         "iz_a": str(Decimal(result["conductor"]["corrected_ampacity_a"]))},
        ["Ampacity table is intentionally synthetic, not manufacturer/ABNT",
         "P06 installation method, grouping, thermal and derating conditions"],
        detail="2.5 mm²: 24x.8=19.2 A < 20; 4 mm²: 32x.8=25.6 A")

def evaluate_e05():
    result = _single()
    # Independently evaluated exact scenario from primary formula; not the C05 output.
    i = Decimal("4400") / Decimal("220")
    expected = Decimal("2") * Decimal("30") / Decimal("1000") * i * Decimal("7.41")
    drop = Decimal(result["voltage_drop"]["drop_v"])
    _require(drop == expected, "E05 independent resistive drop differs")
    return _record(
        "E05", "E05-R-X-EXPLICIT-MATH",
        {"drop_v": "8.892", "drop_percent_rounded": "4.0418", "normative_limit": "UNVERIFIED"},
        {"drop_v": str(drop.normalize()),
         "drop_percent_rounded": str(Decimal(result["voltage_drop"]["percent"]).quantize(Decimal("0.0001"))),
         "normative_limit": "UNVERIFIED" if "VOLTAGE_DROP_NORMATIVE_LIMIT_UNVERIFIED" in result["pending"]
                            else "WRONGLY_APPROVED"},
        ["Rca and XL source table, cable operating temperature and permitted voltage-drop thresholds"],
        detail="2 x .030 km x 20 A x 7.41 ohm/km = 8.892 V; 8.892/220x100=4.0418%")

def evaluate_e06():
    good = _single()
    bad = _single(selected_mm2="2.5")
    _require("OVERLOAD_INEQUALITY_FAILED" in bad["pending"], "E06 bad overload must block")
    return _record(
        "E06", "E06-OVERLOAD-GATE-PASS-FAIL",
        {"pass_case": True, "fail_case": False, "bad_status": "REVIEW_REQUIRED",
         "i2": "REVIEW_REQUIRED"},
        {"pass_case": good["overcurrent"]["ib_le_in_le_iz"],
         "fail_case": bad["overcurrent"]["ib_le_in_le_iz"],
         "bad_status": bad["mathematical_status"],
         "i2": good["overcurrent"]["short_circuit_i2"]},
        ["I2 device characteristic, short-circuit calculation, breaking capacity and selectivity"],
        detail="Good 20<=20<=25.6; bad 20<=20<=19.2 is false")

def evaluate_e07():
    result = _single()
    return _record(
        "E07", "E07-DR-DPS-MUST-BLOCK",
        {"dr_dps_unverified": True, "release": False},
        {"dr_dps_unverified": "DR_DPS_EARTHING_UNVERIFIED" in result["pending"],
         "release": result["liberado_para_uso_normativo"]},
        ["DR sensitivity and coordination; DPS type, location and design conditions",
         "No DR/DPS sizing or compliance algorithm in this C05 routine"],
        detail="Guard against false DR/DPS compliance; no normative numeric oracle")

def evaluate_e08():
    result = _single()
    return _record(
        "E08", "E08-EARTHING-MUST-BLOCK",
        {"earthing_unverified": True, "release": False},
        {"earthing_unverified": "DR_DPS_EARTHING_UNVERIFIED" in result["pending"],
         "release": result["liberado_para_uso_normativo"]},
        ["TT/TN/IT and PE/N sizing and shock protection per scheme",
         "No grounding scheme calculation in C05 routine"],
        detail="Guard against false grounding compliance; no normative numeric oracle")

def evaluate_e09():
    good = resolve_rule("EDP-SP-PTDT00068-V09", revision=2, uf="SP", distributor="EDP_SP")
    bad = resolve_rule("EDP-SP-PTDT00068-V09", revision=2, uf="RJ", distributor="EDP_SP")
    _require(good["status"] != "APPROVED", "E09 unverified distributor unexpectedly approved")
    return _record(
        "E09", "E09-EDP-TERRITORY-AND-UNVERIFIED",
        {"locality_state": "EVIDENCE_PENDING", "foreign_state": "REVIEW_REQUIRED"},
        {"locality_state": good["status"], "foreign_state": bad["status"]},
        ["Official dated EDP tables and revisions, category-specific cell citations",
         "Concessionaire territory and installed/supply topology"],
        detail="Explicit UF and distributor check, no normative category inferred")

def evaluate_e10():
    source = SOURCE.read_text(encoding="utf-8")
    review = REVIEW.read_text(encoding="utf-8")
    verified = verify_field_review(source, review)
    entries = list(csv.DictReader(StringIO(review)))
    flagged = sorted(x["legacy_table"]+"."+x["legacy_column"]
                     for x in entries if x["decision"]=="PROFESSIONAL_REVIEW_REQUIRED")
    _require(len(flagged) == 7, "E10 seven electric fields missing")
    return _record(
        "E10", "E10-LEGACY-SEVEN-FIELD-REVIEW",
        {"all_classified": "45_OF_45_FIELDS_CLASSIFIED", "electrical_pending": 7,
         "professionally_approved": False},
        {"all_classified": verified["scope"], "electrical_pending": len(flagged),
         "professionally_approved": verified["professional_signoff_approved"]},
        ["External source semantics for "+x for x in flagged] +
        ["One display name mapping still needs functional review",
         "Historical result NOT_EVALUATED cannot grant normative release"],
        detail="Exact reconciliation against 99-column source and 45-field review")

def evaluate_e11():
    _, digest_a = catalog_snapshot()
    _, digest_b = catalog_snapshot()
    rejected = False
    try:
        analyze_explicit("4400", "220", "SINGLE", {**SYNTHETIC, "force_approve": True})
    except ValueError:
        rejected = True
    return _record(
        "E11", "E11-CATALOG-FINGERPRINT-AND-INJECTION",
        {"same_catalog_hash": True, "unknown_approval_input_rejected": True,
         "normative_approved": False},
        {"same_catalog_hash": digest_a == digest_b,
         "unknown_approval_input_rejected": rejected,
         "normative_approved": _single()["liberado_para_uso_normativo"]},
        ["Cross-owner actual Auth A/B tests; future schema/golden and normative hash attestation",
         "Signed professional acceptance and real staging integration"],
        detail="SHA256 canonical catalog repeated read and forbidden approval field rejection")

EVALUATORS = {
    "E01": evaluate_e01, "E02": evaluate_e02, "E03": evaluate_e03,
    "E04": evaluate_e04, "E05": evaluate_e05, "E06": evaluate_e06,
    "E07": evaluate_e07, "E08": evaluate_e08, "E09": evaluate_e09,
    "E10": evaluate_e10, "E11": evaluate_e11,
}

def run_suite(*, sha=None):
    _require(set(EVALUATORS) == REQUIRED, "E01-E11 group completeness")
    cases = [EVALUATORS[key]() for key in sorted(REQUIRED)]
    _require(len({c["case_id"] for c in cases}) == 11, "duplicate case IDs")
    for case in cases:
        _require(case["group"] in REQUIRED and
                 case["normative_status"] == "NOT_EVALUATED" and
                 case["professional_signature"] is None and
                 len(case["pending_independent_evidence"]) >= 1,
                 "E01-E11 must keep technical uncertainties explicit")
    digests = [
        sha256(_canonical({
            "group": r["group"], "case_id": r["case_id"],
            "expected": r["expected"], "observed": r["observed"],
            "pending": r["pending_independent_evidence"]
        }).encode("utf-8")).hexdigest()
        for r in cases
    ]
    result = {
        "schema_version": 1,
        "suite": "SIE-C-E01-E11-DEVELOPMENT-INDEPENDENT-MATH-AND-FAIL-CLOSED",
        "commit_sha": sha if sha is not None else os.environ.get("GITHUB_SHA"),
        "environment": "OFFLINE_SYNTHETIC_NO_REMOTE_DB",
        "execution_status": "PASS_ALL_11_DEVELOPMENT_ASSERTIONS",
        "groups_executed": len(cases),
        "normative_conformity": "NOT_EVALUATED",
        "professional_approval": "NOT_GRANTED",
        "gc": "BLOCKED",
        "migration_authorized": False,
        "case_digests_sha256": digests,
        "cases": cases,
    }
    return result

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    report = run_suite()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8")
    print(json.dumps({"execution_status":report["execution_status"],
                      "groups_executed":report["groups_executed"],
                      "professional_approval":report["professional_approval"],
                      "gc":report["gc"]}))

if __name__ == "__main__":
    main()
