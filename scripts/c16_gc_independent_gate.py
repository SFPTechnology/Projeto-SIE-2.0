"""C16 SIE2 GC — independent reviewer evidence validator (offline, fail-closed).

Reviews are AI role protocols and immutable evidence requirements, NOT
professionally signed approvals. This utility does not execute SQL, publish
projects, access secrets or grant migration authority.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

REVIEWERS = ("ARQ","DBA","SEC","ETL","ELE","QA","SRE","AUD")
REAL = (
    "destination_real_backup_verified", "destination_real_restore_verified",
    "legacy_source_backup_verified", "legacy_consistent_cutoff_verified",
    "trusted_jwt_subject_verified", "five_owner_bindings_verified",
    "real_etl_pass", "remote_migrations_4_of_4_applied",
    "independent_normative_e01_e11_verified",
    "professional_c13_signed_and_verified",
    "real_auth_a_b_isolation_verified", "final_sha_ci_5_of_5_verified",
    "independent_auditor_go",
)
STATES = {"BLOCKED", "PASS_DEV_ONLY", "NOT_TESTED", "PASS_REAL_VERIFIED"}
LEGACY_ONLY_EVIDENCE = frozenset(("legacy_source_backup_verified", "legacy_consistent_cutoff_verified", "five_owner_bindings_verified", "real_etl_pass"))
LEGACY_ONLY_REVIEWERS = frozenset(("ETL",))
EXPECTED = "fozrymsidnaxmuvxxfhh"


def assess(contract: dict, report: dict) -> dict:
    if type(contract) is not dict or type(report) is not dict:
        raise ValueError("invalid evidence structure")
    if (report.get("schema_version") != "C16-GC-INDEPENDENT-REVIEWS-1" or
        report.get("gate") != "GC" or contract.get("gate") != "GC" or
        contract.get("supabase_project_ref") != EXPECTED or
        report.get("destination_reference") != EXPECTED):
        raise ValueError("gate, schema or Supabase destination mismatch")
    if report.get("source_reference") != "hlbksclcandbsyqrsbmx":
        raise ValueError("source identity mismatch")
    if report.get("remote_operations_performed") is not False:
        raise ValueError("unverified remote operations asserted by role review")
    reviewers = report.get("reviewers")
    if (not isinstance(reviewers,list) or
        len(reviewers)!=len(REVIEWERS) or
        {x.get("id") for x in reviewers if isinstance(x,dict)}!=set(REVIEWERS)):
        raise ValueError("missing or duplicated independent reviewer role")
    for reviewer in reviewers:
        if (reviewer.get("status") not in STATES or
            not reviewer.get("evidence") or not reviewer.get("finding") or
            not reviewer.get("next") or not reviewer.get("agent")):
            raise ValueError("reviewer has no checkable findings and scope")
    evidence = report.get("mandatory_real_evidence")
    if type(evidence) is not dict or set(evidence)!=set(REAL):
        raise ValueError("required real-evidence fields missing or unexpected")
    if any(type(value) is not bool for value in evidence.values()):
        raise ValueError("invalid real-evidence state")
    pre = contract.get("preproduction_authorization")
    if (not isinstance(pre,dict) or
        pre.get("project_ref") != EXPECTED or
        pre.get("migration_application_approved_conditionally") is not True):
        raise ValueError("missing conditional authorization evidence")

    delivery=contract.get("current_delivery_scope",{}).get("strategy")
    greenfield=delivery=="GREENFIELD_NO_LEGACY_IMPORT"
    required=set(REAL)-LEGACY_ONLY_EVIDENCE if greenfield else set(REAL)
    deferred=sorted(LEGACY_ONLY_EVIDENCE) if greenfield else []
    required_reviewers=set(REVIEWERS)-LEGACY_ONLY_REVIEWERS if greenfield else set(REVIEWERS)
    missing = sorted(key for key in required if not evidence[key])
    reviews_pending = sorted(r["id"] for r in reviewers if r["id"] in required_reviewers and r["status"]!="PASS_REAL_VERIFIED")
    qualified = not missing and not reviews_pending
    # Reviewer notes/booleans alone are not proof of a backup/restore, Auth,
    # production-safe DDL or human C13 signature. An independent trusted
    # verifier and external professional acceptance are always required.
    alleged_pass = (
        contract.get("state")=="PASS" or
        report.get("overall_verdict") in ("PASS","GC_PASS") or
        report.get("automatic_go") is True or
        pre.get("migration_application_permitted_now") is True or
        pre.get("legacy_import_permitted_now") is True
    )
    if alleged_pass and (not qualified or not report.get("professional_signature_present")):
        raise ValueError("premature GC=PASS or remote GO without full evidence")
    if not qualified:
        return {
            "gate":"GC",
            "verdict":"BLOCKED",
            "evidence_pending":missing,
            "review_roles_pending":reviews_pending,
            "independent_reviewers":len(reviewers),
            "active_reviewers":len(required_reviewers),
            "legacy_evidence_deferred":deferred,
            "legacy_import_release_requirement":"DEFERRED_OPTIONAL" if greenfield else "REQUIRED",
            "remote_ddl_permitted_by_this_check":False,
            "legacy_import_permitted_by_this_check":False,
            "automatic_release":False,
        }
    return {
        "gate":"GC",
        "verdict":"ELIGIBLE_FOR_EXTERNAL_HUMAN_AND_OPERATIONAL_VERIFICATION",
        "evidence_pending":[],
        "review_roles_pending":[],
        "independent_reviewers":len(reviewers),
        "active_reviewers":len(required_reviewers),
        "legacy_evidence_deferred":deferred,
        "legacy_import_release_requirement":"DEFERRED_OPTIONAL" if greenfield else "REQUIRED",
        "remote_ddl_permitted_by_this_check":False,
        "legacy_import_permitted_by_this_check":False,
        "automatic_release":False,
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--contract",required=True,type=Path)
    parser.add_argument("--reviews",required=True,type=Path)
    parser.add_argument("--expect-blocked",action="store_true")
    args=parser.parse_args()
    contract=json.loads(args.contract.read_text(encoding="utf-8-sig"))
    reviews=json.loads(args.reviews.read_text(encoding="utf-8-sig"))
    result=assess(contract,reviews)
    print(json.dumps(result,indent=2,sort_keys=True))
    if args.expect_blocked and result["verdict"]!="BLOCKED":
        raise SystemExit("UNSAFE: GC unblocked without independent external proof")


if __name__=="__main__":
    main()
