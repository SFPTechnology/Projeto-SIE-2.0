"""C01-C07 real-source owner preflight: no migration and no self-attestation.

Legitimate owner assignments require independent human verification, valid
Supabase destination Auth identities and authorized cutover in E02-E06.
This function validates structure only and NEVER authorizes real import.
"""
from uuid import UUID
from hashlib import sha256
import json

def _uuid(value):
    try:
        parsed=UUID(str(value))
        if parsed.int==0:
            raise ValueError()
        return str(parsed)
    except (ValueError,TypeError,AttributeError):
        raise ValueError("valid Auth UUID required") from None

def preflight_owners(source_project_ids, claims, orphan_audit_count=0):
    if not isinstance(source_project_ids,list) or not isinstance(claims,dict):
        raise ValueError("project IDs and claim mapping required")
    if type(orphan_audit_count) is not int or orphan_audit_count<0:
        raise ValueError("orphan count invalid")
    ids=[str(i) for i in source_project_ids]
    if not ids or len(ids)!=len(set(ids)) or any(not i.strip() for i in ids):
        raise ValueError("source project inventory missing or duplicated")
    if set(claims)!=set(ids):
        raise ValueError("unmapped or foreign source projects; refuse partial import")
    sanitized=[]
    for source_id in sorted(ids):
        item=claims[source_id]
        if type(item) is not dict or set(item)!={"target_owner_auth_uuid","approval_reference"}:
            raise ValueError("claim structure invalid")
        owner=_uuid(item["target_owner_auth_uuid"])
        reference=item["approval_reference"]
        if type(reference) is not str or len(reference.strip())<8 or len(reference)>200:
            raise ValueError("external approval reference required")
        sanitized.append((source_id,owner,reference.strip()))
    digest=sha256(json.dumps(sanitized,sort_keys=True,ensure_ascii=False,
                    separators=(",",":")).encode("utf-8")).hexdigest()
    return {"structural_mapping":"PASS","mapping_sha256":digest,
            "projects_mapped":len(ids),"quarantined_audit_orphans":orphan_audit_count,
            "migration_authorized":False,
            "authority_status":"HUMAN_ATTESTATION_AND_DESTINATION_AUTH_CHECK_REQUIRED",
            "state":"HUMAN_REQUIRED"}
