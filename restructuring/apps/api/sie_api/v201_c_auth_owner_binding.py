"""C01 owner identity evidence: read-only, injected connection, NO user creation.

Credential proof and session subject MUST originate in the trusted Supabase
auth boundary. A record in auth.users alone does not grant project ownership.
No DSN, secrets, privileged write, synthetic UUID or user_metadata accepted.
"""
from __future__ import annotations
from uuid import UUID

SOURCE="hlbksclcandbsyqrsbmx"
DEST="fozrymsidnaxmuvxxfhh"
EXPECTED_IDS={
 "proj-1","proj-1bd66860-4044-416a-845d-f1ceb1a41a87",
 "proj-2","proj-54a80990-0c54-433e-991e-b89dd48e5c91",
 "proj-774c6110-b6bd-460d-b435-8149fe03d059"}

def _uuid(v):
    try:
        u=UUID(str(v))
    except (ValueError,TypeError,AttributeError):
        raise ValueError("valid Auth UUID required") from None
    if u.int==0:raise ValueError("zero UUID cannot identify owner")
    return u

def check_real_auth_user(conn, *, project_ref, verified_jwt_subject):
    """Readback against an INJECTED read-only destination DB connection.

    verified_jwt_subject must be the backend verified JWT subject, not a
    caller's JSON, metadata, or email. Read Supabase PK/confirmation only.
    """
    if project_ref!=DEST:raise ValueError("different Supabase destination")
    uid=_uuid(verified_jwt_subject)
    with conn.cursor() as cursor:
        cursor.execute("""SELECT id, (email_confirmed_at IS NOT NULL) AS confirmed
           FROM auth.users WHERE id=%s""",(uid,))
        row=cursor.fetchone()
    if row is None:
        return {"identity_status":"NOT_FOUND","auth_user_verified":False,
                "owner_binding_accepted":False,"real_migration_authorized":False}
    db_id,confirmed=row
    valid=bool(confirmed and _uuid(db_id)==uid)
    return {"identity_status":"AUTH_CONFIRMED" if valid else "AUTH_EMAIL_UNCONFIRMED",
            "auth_user_verified":valid,
            "owner_binding_accepted":False,
            "real_migration_authorized":False}

def check_owner_selection(selection, binding, auth_proof):
    """No self-attestation, manifest value, or synthetic Auth fixture = approval."""
    if (selection.get("source",{}).get("project_ref")!=SOURCE or
        selection.get("destination",{}).get("project_ref")!=DEST):
        raise ValueError("source or destination mismatch")
    project_ids={p["legacy_id"] for p in selection.get("projects",[])}
    if project_ids!=EXPECTED_IDS or len(selection["projects"])!=5 or (
        any(p.get("selection")!="MIGRATE" for p in selection["projects"])
    ):
        raise ValueError("all five source IDs must be explicitly selected")
    if not isinstance(binding,dict) or set(binding)!=EXPECTED_IDS:
        raise ValueError("missing/mismatched binding to one of five projects")
    owners={str(_uuid(v)) for v in binding.values()}
    if len(owners)!=1:
        raise ValueError("the five projects must bind to one verified owner account")
    target=next(iter(owners))
    if selection.get("destination",{}).get("target_auth_user_id") not in (None,target):
        raise ValueError("manifest target identity mismatch")
    return {"project_scope_status":"FIVE_OF_FIVE_SELECTED",
            "target_owner_uid":target,"binds_to_one_account":True,
            "auth_status":auth_proof.get("identity_status","NOT_EVALUATED"),
            "auth_readback_required":auth_proof.get("auth_user_verified") is not True,
            "independent_owner_attestation_required":True,
            "binding_applied":False,"migration_authorized":False,"gc":"BLOCKED"}
