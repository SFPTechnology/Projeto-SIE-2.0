"""C04: deterministic, fail-closed catalog gateway; no normative approval by config."""
from __future__ import annotations
from hashlib import sha256
from pathlib import Path
import json

REGISTRY = Path(__file__).parent / "data" / "normative_registry.json"
STATES = {"CANDIDATE", "EVIDENCE_PENDING", "REVIEW_REQUIRED", "APPROVED", "REVOKED"}

def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)

def catalog_snapshot(path=None):
    raw = json.loads(Path(path or REGISTRY).read_text(encoding="utf-8"))
    if raw.get("schema_version") != 1 or not isinstance(raw.get("records"), list):
        raise ValueError("catalog schema not recognized")
    records = raw["records"]
    if any(not isinstance(r, dict) or not r.get("id") or not isinstance(r.get("revision"), int)
           for r in records):
        raise ValueError("invalid catalog record")
    ids = [(r["id"], r["revision"]) for r in records]
    if len(ids) != len(set(ids)):
        raise ValueError("ambiguous catalog rule version")
    return raw, sha256(canonical(raw).encode("utf-8")).hexdigest()

def resolve_rule(rule_id, *, revision=None, uf=None, distributor=None, path=None):
    """Exact rule and version required. Do not infer locality or conditions."""
    catalog, digest = catalog_snapshot(path)
    candidates = [r for r in catalog["records"] if r["id"] == rule_id
                  and (revision is None or r["revision"] == revision)]
    if revision is None and len(candidates) > 1:
        return {"rule_id": rule_id, "status": "REVIEW_REQUIRED",
                "reason": "RULE_VERSION_REQUIRED", "catalog_sha256": digest}
    if len(candidates) != 1:
        return {"rule_id": rule_id, "status": "REVIEW_REQUIRED",
                "reason": "RULE_NOT_FOUND", "catalog_sha256": digest}
    r = candidates[0]
    if (r.get("uf") and r["uf"] != uf) or (r.get("distributor") and r["distributor"] != distributor):
        return {"rule_id": rule_id, "status": "REVIEW_REQUIRED",
                "reason": "LOCALITY_UNVERIFIED", "catalog_sha256": digest}
    if r.get("status") == "REVOKED":
        status, reason = "REVOKED", "RULE_REVOKED"
    elif r.get("status") == "APPROVED":
        # A mutable JSON record does not authenticate a licensed normative
        # source or a professional sign-off. Trusted attestation belongs to E03.
        status, reason = "REVIEW_REQUIRED", "TRUSTED_APPROVAL_ATTESTATION_REQUIRED"
    else:
        status, reason = "EVIDENCE_PENDING", "NO_VERIFIED_RULE_EVIDENCE"
    return {"rule_id": r["id"], "revision": r["revision"], "status": status,
            "reason": reason, "catalog_sha256": digest, "edition": r.get("edition"),
            "license_status": r.get("license_status", "UNVERIFIED")}
