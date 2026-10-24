import hashlib
import json
from uuid import uuid4

import pytest

from sie_api.artifact_registry_f10 import ArtifactRegistryError, ArtifactRegistryF10
from sie_api.storage import RepositorioProjetos


@pytest.fixture
def registry(tmp_path):
    repo = RepositorioProjetos(tmp_path / "sie.sqlite3")
    project_id, run_id = str(uuid4()), str(uuid4())
    repo.salvar(project_id, "Projeto", {"x": 1}, 0)
    return ArtifactRegistryF10(repo), repo, project_id, run_id, tmp_path / "exports"


def reserve(registry, *, destination="bundle"):
    store, _repo, project_id, run_id, root = registry
    return store.reserve(
        project_id=project_id, revision_id=1, calculation_run_id=run_id,
        template_version="v1", snapshot_sha256="a" * 64,
        artifact_root=root, destination=destination,
    )


def test_reservation_persists_preparing_before_publication(registry):
    store, _repo, _pid, _run_id, root = registry
    row = reserve(registry)
    assert row["state"] == "PREPARING"
    assert row["artifact_root"] == str(root.resolve())
    assert row["destination_relative"] == "bundle"
    assert store.events(row["artifact_id"])[0]["new_state"] == "PREPARING"
    assert store.recoverable()[0]["artifact_id"] == row["artifact_id"]


def test_same_logical_reservation_is_idempotent(registry):
    first = reserve(registry)
    second = reserve(registry, destination="another-name")
    assert second["artifact_id"] == first["artifact_id"]
    assert second["destination_relative"] == "bundle"
    assert len(registry[0].events(first["artifact_id"])) == 1


def test_state_transition_is_compare_and_set_and_event_append_only(registry):
    store = registry[0]
    row = reserve(registry)
    store.transition(row["artifact_id"], "PREPARING", "STAGED")
    manifest_hash = hashlib.sha256(b"manifest").hexdigest()
    final = store.transition(row["artifact_id"], "STAGED", "PUBLISHED",
                             manifest_sha256=manifest_hash)
    assert final["state"] == "PUBLISHED"
    assert [event["new_state"] for event in store.events(row["artifact_id"])] == [
        "PREPARING", "STAGED", "PUBLISHED"]
    with pytest.raises(ArtifactRegistryError, match="changed concurrently"):
        store.transition(row["artifact_id"], "STAGED", "FAILED")
    with store.repository._conectar() as db:
        with pytest.raises(Exception, match="imutavel"):
            db.execute("UPDATE eventos_artefato_f10 SET detail_json='{}' WHERE artifact_id=?",
                       (row["artifact_id"],))


def test_published_requires_authoritative_manifest_hash(registry):
    store = registry[0]
    row = reserve(registry)
    with pytest.raises(ArtifactRegistryError, match="requires"):
        store.transition(row["artifact_id"], "PREPARING", "PUBLISHED")


@pytest.mark.parametrize("destination", ["../outside", "/tmp/outside"])
def test_rejects_destination_outside_root(registry, destination):
    with pytest.raises(ArtifactRegistryError, match="outside|escapes|invalid"):
        reserve(registry, destination=destination)


def test_reconcile_adopts_verified_rename_after_crash(registry):
    store, _repo, _pid, _run_id, root = registry
    row = reserve(registry)
    target = root / "bundle"
    target.mkdir(parents=True)
    manifest = {
        "artifact_id": row["artifact_id"], "snapshot_sha256": "a" * 64,
        "dependencies": {
            "project_id": row["project_id"], "revision_id": "1",
            "calculation_run_id": row["calculation_run_id"],
            "template_version": row["template_version"],
        },
    }
    encoded = json.dumps(manifest, sort_keys=True).encode()
    (target / "manifest.json").write_bytes(encoded)
    digest = hashlib.sha256(encoded).hexdigest()
    result = store.reconcile_published(
        row["artifact_id"], lambda _path: {"integrity": "VERIFIED"})
    assert result["state"] == "PUBLISHED"
    assert result["manifest_sha256"] == digest
    assert store.events(row["artifact_id"])[-1]["detail_json"]


def test_reconcile_never_marks_missing_or_mismatched_target_published(registry):
    store = registry[0]
    row = reserve(registry)
    result = store.reconcile_published(
        row["artifact_id"], lambda _path: {"integrity": "VERIFIED"})
    assert result["state"] == "RECOVERY_REQUIRED"
    assert store.recoverable()[0]["artifact_id"] == row["artifact_id"]


def test_reconcile_rejects_manifest_dependency_drift(registry):
    store, _repo, _pid, _run_id, root = registry
    row = reserve(registry)
    target = root / "bundle"
    target.mkdir(parents=True)
    manifest = {
        "artifact_id": row["artifact_id"], "snapshot_sha256": "a" * 64,
        "dependencies": {
            "project_id": row["project_id"], "revision_id": "99",
            "calculation_run_id": row["calculation_run_id"],
            "template_version": row["template_version"],
        },
    }
    (target / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    result = store.reconcile_published(
        row["artifact_id"], lambda _path: {"integrity": "VERIFIED"})
    assert result["state"] == "RECOVERY_REQUIRED"


def test_retry_requires_absent_destination_and_appends_transition(registry):
    store = registry[0]
    row = reserve(registry)
    store.transition(row["artifact_id"], "PREPARING", "RECOVERY_REQUIRED",
                     detail={"reason": "interrupted"})
    retried = store.start_retry(row["artifact_id"])
    assert retried["state"] == "PREPARING"
    assert [event["new_state"] for event in store.events(row["artifact_id"])] == [
        "PREPARING", "RECOVERY_REQUIRED", "PREPARING"]
    assert json.loads(store.events(row["artifact_id"])[-1]["detail_json"])["retry"] is True


def test_retry_refuses_existing_destination(registry):
    store, _repo, _pid, _run_id, root = registry
    row = reserve(registry)
    store.transition(row["artifact_id"], "PREPARING", "RECOVERY_REQUIRED")
    (root / "bundle").mkdir(parents=True)
    with pytest.raises(ArtifactRegistryError, match="destination exists"):
        store.start_retry(row["artifact_id"])
    assert store.get(row["artifact_id"])["state"] == "RECOVERY_REQUIRED"


def test_retry_refuses_existing_destination(registry):
    store, _repo, _pid, _run_id, root = registry
    row = reserve(registry)
    store.transition(row["artifact_id"], "PREPARING", "RECOVERY_REQUIRED")
    root.mkdir(parents=True, exist_ok=True)
    (root / "bundle").mkdir()
    with pytest.raises(ArtifactRegistryError, match="destination exists"):
        store.start_retry(row["artifact_id"])
    assert store.get(row["artifact_id"])["state"] == "RECOVERY_REQUIRED"


def test_registry_survives_repository_reopen_and_keeps_history(registry):
    store, repo, project_id, _run_id, _root = registry
    first = reserve(registry)
    reopened = ArtifactRegistryF10(RepositorioProjetos(repo.caminho))
    assert reopened.get(first["artifact_id"])["state"] == "PREPARING"
    assert [row["artifact_id"] for row in reopened.history(project_id)] == [first["artifact_id"]]
