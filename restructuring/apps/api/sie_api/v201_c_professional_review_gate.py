"""C04/C05 offline professional-review packet integrity.

This tool performs structural checks only. It cannot authenticate a reviewer,
certify electrical conformity, verify licensed norms or approve production.
"""
from __future__ import annotations

REQUIRED_CODES=frozenset("E%02d" % i for i in range(1,12))
REQUIRED_REFS=frozenset({"ABNT-NBR-5410","EDP-SP-PTDT00068-V09","NR-10-ATE-2027"})
UNVERIFIED={"EVIDENCE_PENDING","REVIEW_REQUIRED","NOT_EVALUATED"}

def verify_review_packet(packet,catalog):
    if not isinstance(packet,dict) or packet.get("contract_version")!="SIE-C04-C05-PROFESSIONAL-REVIEW-1":
        raise ValueError("unknown professional review contract")
    if not isinstance(catalog,dict) or catalog.get("schema_version")!=1:
        raise ValueError("invalid normative registry")
    case_ids=[r.get("code") for r in packet.get("requirements",[])]
    if len(case_ids)!=11 or set(case_ids)!=REQUIRED_CODES:
        raise ValueError("required engineering cases missing or duplicated")
    if any(c.get("state") not in UNVERIFIED or not c.get("needed")
           for c in packet["requirements"]):
        raise ValueError("review pack cannot confer engineering approval")
    cited=packet.get("references",[])
    ids=[v.get("id") for v in cited]
    registry_ids={x["id"] for x in catalog.get("records",[])}
    if len(ids)!=len(set(ids)) or not REQUIRED_REFS<=set(ids) or not set(ids)<=registry_ids:
        raise ValueError("normative citations missing/ambiguous/unrecognized")
    if any(v.get("status")!="PENDING" for v in cited):
        raise ValueError("normative references need independently verified approval")
    reviewer=packet.get("professional_review")
    if (not isinstance(reviewer,dict) or
        reviewer.get("state")!="NOT_SUBMITTED" or
        any(reviewer.get(k) is not None for k in (
          "external_signature_or_process_ref","signed_evidence_sha256","signed_at"))
    ):
        raise ValueError("fabricated approval/signature cannot pass dossier gate")
    if packet.get("normative_approved") is not False or (
        packet.get("production_or_remote_approval") is not False
    ):
        raise ValueError("mutable review packet cannot authorize conformity or deployment")
    return {"review_packet":"STRUCTURAL_PASS",
            "required_cases":len(case_ids),"references":len(ids),
            "normative_catalog_verified":False,
            "external_professional_attestation":"MISSING",
            "electrical_acceptance":"NOT_APPROVED",
            "remote_migration_authorized":False,"gate_gc":"BLOCKED"}
