"""Static A03 candidate and pure A04 lifecycle regression (no remote mutations)."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import re

import pytest

ROOT = Path(__file__).resolve().parents[4]
MODULE = ROOT / "restructuring" / "supabase" / "greenfield" / "lifecycle_contract.py"
spec = importlib.util.spec_from_file_location("sie2_v201_lifecycle_contract", MODULE)
assert spec is not None and spec.loader is not None
lifecycle = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = lifecycle
spec.loader.exec_module(lifecycle)


def draft():
    return lifecycle.RevisionContract(id="rev1", project_id="project1", version=1)


def sealed():
    return lifecycle.transition(draft(), "SEALED", 0, {"rooms": [], "version": 1})


def test_sealed_snapshot_is_deterministic():
    assert lifecycle.canonical_sha256({"x": 1, "z": [2, 3]}) == lifecycle.canonical_sha256(
        {"z": [2, 3], "x": 1})


def test_nonfinite_snapshot_rejected():
    with pytest.raises(lifecycle.LifecycleViolation):
        lifecycle.canonical_sha256({"invalid": float("nan")})


def test_seal_moves_lock_and_stores_sha():
    target = sealed()
    assert target.state == "SEALED"
    assert target.lock_version == 1
    assert len(target.snapshot_sha256) == 64


def test_sealing_without_snapshot_rejected():
    with pytest.raises(lifecycle.LifecycleViolation):
        lifecycle.transition(draft(), "SEALED", 0)


def test_optimistic_conflict_is_fail_closed():
    with pytest.raises(lifecycle.RevisionConflict):
        lifecycle.transition(draft(), "SEALED", 3, {"a": 1})


def test_sealed_cannot_reopen_or_reseal():
    for state in ("DRAFT", "SEALED"):
        with pytest.raises(lifecycle.LifecycleViolation):
            lifecycle.transition(sealed(), state, 1, {"a": 1})


def test_supersede_preserves_snapshot():
    base = sealed()
    target = lifecycle.transition(base, "SUPERSEDED", 1)
    assert target.state == "SUPERSEDED"
    assert target.snapshot_sha256 == base.snapshot_sha256
    with pytest.raises(lifecycle.LifecycleViolation):
        lifecycle.transition(target, "DRAFT", 2)


def test_clone_requires_sealed_origin():
    with pytest.raises(lifecycle.LifecycleViolation):
        lifecycle.clone_draft(draft(), "rev2", 2)


def test_clone_from_sealed_creates_new_draft():
    derived = lifecycle.clone_draft(sealed(), "rev2", 2)
    assert derived.state == "DRAFT"
    assert derived.base_revision_id == "rev1"
    assert derived.snapshot_sha256 is None
    assert derived.lock_version == 0


def test_idempotency_keys_are_scoped_to_owner_and_project():
    assert lifecycle.idempotency_scope("ownerA", "project1", "k1") != (
        lifecycle.idempotency_scope("ownerB", "project1", "k1"))
    with pytest.raises(lifecycle.LifecycleViolation):
        lifecycle.idempotency_scope("ownerA", "project1", "")


def test_a03_candidate_contains_only_four_missing_fk_indexes():
    path = ROOT / "docs" / "implantacao-sie-2-0" / "GREENFIELD" / "A03_INDICES_CANDIDATO.sql"
    sql = path.read_text()
    uncommented = "\n".join(line for line in sql.splitlines() if not line.lstrip().startswith("--"))
    assert re.findall(r"CREATE INDEX ([a-z_]+)", uncommented) == [
        "sie_projects_owner_idx", "sie_revisions_created_by_idx",
        "sie_audit_actor_idx", "sie_audit_revision_fk_idx",
    ]
    assert not re.search(r"\b(DROP|TRUNCATE|DELETE|REVOKE|GRANT|ALTER TABLE|CREATE TABLE)\b", uncommented)
