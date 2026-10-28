"""Pure lifecycle contract for SIE 2.0 V2.0.1.

Development-only reference implementation; does not mutate PostgreSQL.
Persisted revisions/locking/immutability require an authorized migration and API.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
import hashlib
import json
import re
from typing import Any, Mapping

STATES = frozenset({"DRAFT", "SEALED", "SUPERSEDED"})
SHA256_PATTERN = re.compile(r"^[a-f0-9]{64}$")


class LifecycleViolation(ValueError):
    """Invalid state transition or attempt to change sealed content."""


class RevisionConflict(LifecycleViolation):
    """Optimistic lock conflict. A persistence adapter should return HTTP 409."""


@dataclass(frozen=True)
class RevisionContract:
    id: str
    project_id: str
    version: int
    state: str = "DRAFT"
    lock_version: int = 0
    base_revision_id: str | None = None
    snapshot_sha256: str | None = None

    def __post_init__(self):
        if not self.id or not self.project_id or self.version < 1:
            raise LifecycleViolation("revision id, project and positive version required")
        if self.state not in STATES or self.lock_version < 0:
            raise LifecycleViolation("invalid lifecycle state or lock_version")
        if self.state != "DRAFT" and (
            self.snapshot_sha256 is None
            or SHA256_PATTERN.fullmatch(self.snapshot_sha256) is None
        ):
            raise LifecycleViolation("sealed and superseded revisions require snapshot hash")
        if self.state == "DRAFT" and self.snapshot_sha256 is not None:
            raise LifecycleViolation("a draft must not claim a sealed snapshot hash")


def canonical_sha256(document: Mapping[str, Any]) -> str:
    """Stable hash of JSON objects, excluding external metadata by caller contract."""
    try:
        payload = json.dumps(document, sort_keys=True, separators=(",", ":"),
                             ensure_ascii=False, allow_nan=False).encode("utf-8")
    except (TypeError, ValueError) as exc:
        raise LifecycleViolation("snapshot must be serializable finite JSON") from exc
    return hashlib.sha256(payload).hexdigest()


def transition(
    revision: RevisionContract,
    target: str,
    expected_lock_version: int,
    snapshot: Mapping[str, Any] | None = None,
) -> RevisionContract:
    if expected_lock_version != revision.lock_version:
        raise RevisionConflict("stale revision lock_version")
    if (revision.state, target) not in {
        ("DRAFT", "SEALED"), ("SEALED", "SUPERSEDED")
    }:
        raise LifecycleViolation("forbidden revision transition")
    if target == "SEALED":
        if snapshot is None:
            raise LifecycleViolation("sealing requires canonical snapshot")
        return replace(revision, state="SEALED",
                       snapshot_sha256=canonical_sha256(snapshot),
                       lock_version=revision.lock_version + 1)
    if snapshot is not None:
        raise LifecycleViolation("superseding cannot rewrite sealed snapshot")
    return replace(revision, state="SUPERSEDED",
                   lock_version=revision.lock_version + 1)


def clone_draft(
    baseline: RevisionContract,
    new_revision_id: str,
    new_version: int,
) -> RevisionContract:
    if baseline.state not in {"SEALED", "SUPERSEDED"}:
        raise LifecycleViolation("clone must originate from sealed revision")
    if not new_revision_id or new_revision_id == baseline.id:
        raise LifecycleViolation("clone needs distinct ID")
    if new_version <= baseline.version:
        raise LifecycleViolation("new revision must increase logical version")
    return RevisionContract(id=new_revision_id, project_id=baseline.project_id,
                            version=new_version, state="DRAFT", lock_version=0,
                            base_revision_id=baseline.id, snapshot_sha256=None)


def idempotency_scope(owner_id: str, project_id: str, key: str) -> tuple[str, str, str]:
    if not all(isinstance(value, str) and value.strip() for value in (owner_id, project_id, key)):
        raise LifecycleViolation("owner, project and idempotency key are required")
    if len(key) > 128:
        raise LifecycleViolation("idempotency key too long")
    return owner_id, project_id, key
