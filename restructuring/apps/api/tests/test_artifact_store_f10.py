"""Adversarial regression for F10 artifact persistence and traceability."""
from copy import deepcopy
import hashlib
import json

import pytest

import sie_api.artifact_store_f10 as artifact_store
from sie_api.artifact_store_f10 import (
    build_verified_bundle, publish_verified_bundle, verify_verified_bundle,
    main as artifact_store_main,
)
from sie_api.representation_f10 import ArtifactContract, ArtifactError


@pytest.fixture
def source():
    contract = ArtifactContract("P-1", "R-2", "CALC-3", "rules-1", "template-1")
    snapshot = {
        "project_id": "P-1", "revision_id": "R-2",
        "calculation_run_id": "CALC-3", "rule_version": "rules-1",
        "elements": [{"id": "QD1", "kind": "panel"}],
        "circuits": [
            {"id": "C1", "panel_id": "QD1", "load_va": 1200, "phase": "L1",
             "breaker_id": "DJ1", "conductor_id": "COND1"}
        ],
        "segments": [{"id": "S1", "circuit_id": "C1", "conductor_id": "COND1",
                      "length_m": 7.25, "status": "MEASURED", "origin": "levantamento:01"}],
    }
    return snapshot, contract


def test_manifest_contains_real_hashes_and_dependencies(source):
    snapshot, contract = source
    files, manifest = build_verified_bundle(snapshot, contract)
    assert manifest["artifact_type"] == "electrical_study_bundle"
    assert manifest["dependencies"]["revision_id"] == "R-2"
    assert manifest["dependencies"]["calculation_run_id"] == "CALC-3"
    assert manifest["normative_conformity_verified"] is False
    assert manifest["snapshot_id"] == hashlib.sha256(files["snapshot.json"]).hexdigest()
    assert manifest["files_sha256"]["diagram.svg"] == hashlib.sha256(files["diagram.svg"]).hexdigest()
    assert json.loads(files["snapshot.json"]) == snapshot
    assert "manifest.json" in files


def test_reserved_artifact_id_is_preserved_and_validated(source):
    snapshot, contract = source
    artifact_id = "7b03aee2-ecae-4a2a-bcba-0d5e23fe3cb5"
    _, manifest = build_verified_bundle(snapshot, contract, artifact_id)
    assert manifest["artifact_id"] == artifact_id
    with pytest.raises(ArtifactError, match="artifact_id"):
        build_verified_bundle(snapshot, contract, "not-a-uuid")


def test_same_snapshot_fingerprint_is_independent_of_object_key_order(source):
    snapshot, contract = source
    reordered = dict(reversed(list(snapshot.items())))
    _, m1 = build_verified_bundle(snapshot, contract)
    _, m2 = build_verified_bundle(reordered, contract)
    assert m1["snapshot_sha256"] == m2["snapshot_sha256"]
    assert m1["artifact_id"] != m2["artifact_id"]


def test_bundle_renders_and_hashes_one_detached_snapshot(source, monkeypatch):
    snapshot, contract = source
    expected_snapshot = deepcopy(snapshot)
    original_renderer = artifact_store.artifact_bundle

    def mutate_caller_then_render(frozen_snapshot, frozen_contract):
        # Simulate a concurrent caller changing the shared object as generation
        # starts. Rendering and snapshot persistence must still use the capture.
        snapshot["circuits"][0]["load_va"] = 9999
        snapshot["segments"][0]["origin"] = "mutated-after-capture"
        return original_renderer(frozen_snapshot, frozen_contract)

    monkeypatch.setattr(artifact_store, "artifact_bundle", mutate_caller_then_render)
    files, _ = build_verified_bundle(snapshot, contract)
    expected_files, _ = build_verified_bundle(expected_snapshot, contract)

    assert files["snapshot.json"] == expected_files["snapshot.json"]
    for name in expected_files:
        if name != "manifest.json":
            assert files[name] == expected_files[name]


def test_package_does_not_claim_current_without_live_source(tmp_path, source):
    snapshot, contract = source
    dest = tmp_path / "out"
    publish_verified_bundle(snapshot, contract, dest)
    result = verify_verified_bundle(dest)
    assert result["integrity"] == "VERIFIED"
    assert result["currentness"] == "CURRENTNESS_UNVERIFIED"
    assert result["normative_conformity_verified"] is False
    assert verify_verified_bundle(dest, snapshot, contract)["currentness"] == "CURRENT"


@pytest.mark.parametrize("field,value", [
    ("calculation_run_id", "CALC-4"),
    ("revision_id", "R-3"),
])
def test_changed_revision_or_calculation_is_stale(tmp_path, source, field, value):
    snapshot, contract = source
    dest = tmp_path / "out"
    publish_verified_bundle(snapshot, contract, dest)
    modified = deepcopy(snapshot)
    modified[field] = value
    data = {k: getattr(contract, k) for k in contract.__dict__}
    data[field] = value
    newer = ArtifactContract(**data)
    assert verify_verified_bundle(dest, modified, newer)["currentness"] == "STALE"


def test_changed_topology_or_load_becomes_stale(tmp_path, source):
    snapshot, contract = source
    dest = tmp_path / "out"
    publish_verified_bundle(snapshot, contract, dest)
    modified = deepcopy(snapshot)
    modified["circuits"][0]["load_va"] = 1201
    assert verify_verified_bundle(dest, modified, contract)["currentness"] == "STALE"


@pytest.mark.parametrize("filename", ["schedule.json", "diagram.svg", "quantities.csv", "snapshot.json"])
def test_tampered_artifact_is_rejected(tmp_path, source, filename):
    snapshot, contract = source
    dest = tmp_path / "out"
    publish_verified_bundle(snapshot, contract, dest)
    with (dest / filename).open("ab") as output:
        output.write(b"INJECTED")
    with pytest.raises(ArtifactError, match="hash mismatch"):
        verify_verified_bundle(dest)


def test_missing_or_extra_file_is_rejected(tmp_path, source):
    snapshot, contract = source
    dest = tmp_path / "out"
    publish_verified_bundle(snapshot, contract, dest)
    (dest / "unexpected.txt").write_text("x")
    with pytest.raises(ArtifactError, match="inventory mismatch"):
        verify_verified_bundle(dest)


def test_republication_cannot_overwrite_existing_data(tmp_path, source):
    snapshot, contract = source
    dest = tmp_path / "out"
    publish_verified_bundle(snapshot, contract, dest)
    original = (dest / "snapshot.json").read_bytes()
    with pytest.raises(FileExistsError):
        publish_verified_bundle(snapshot, contract, dest)
    assert (dest / "snapshot.json").read_bytes() == original
    assert not list(tmp_path.glob(".f10-stage-*"))
    assert not list(tmp_path.glob("*.f10.lock"))


def test_retry_removes_only_deterministic_orphan_stage(tmp_path, source):
    snapshot, contract = source
    artifact_id = "7b03aee2-ecae-4a2a-bcba-0d5e23fe3cb5"
    stage = tmp_path / (".f10-stage-" + artifact_id)
    stage.mkdir(mode=0o700)
    (stage / "partial.tmp").write_bytes(b"interrupted")
    destination = tmp_path / "out"
    manifest = publish_verified_bundle(snapshot, contract, destination, artifact_id)
    assert manifest["artifact_id"] == artifact_id
    assert not stage.exists()
    assert verify_verified_bundle(destination)["integrity"] == "VERIFIED"


def test_concurrent_publication_to_same_destination_never_overwrites(tmp_path, source):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier

    snapshot, contract = source
    barrier = Barrier(2)

    def publish():
        barrier.wait()
        try:
            publish_verified_bundle(snapshot, contract, tmp_path / "same-target")
            return "published"
        except FileExistsError:
            return "conflict"

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: publish(), range(2)))
    assert sorted(results) == ["conflict", "published"]
    assert verify_verified_bundle(tmp_path / "same-target")["integrity"] == "VERIFIED"


def test_rejects_nonfinite_input_without_creating_destination(tmp_path, source):
    snapshot, contract = source
    broken = deepcopy(snapshot)
    broken["annotations"] = {"bad_value": float("nan")}
    dest = tmp_path / "bad"
    with pytest.raises(ArtifactError, match="canonically serializable"):
        publish_verified_bundle(broken, contract, dest)
    assert not dest.exists()


def test_source_invalid_is_not_mislabeled_current(tmp_path, source):
    snapshot, contract = source
    dest = tmp_path / "out"
    publish_verified_bundle(snapshot, contract, dest)
    invalid = deepcopy(snapshot)
    invalid["circuits"][0]["panel_id"] = "MISSING"
    assert verify_verified_bundle(dest, invalid, contract)["currentness"] == "SOURCE_INVALID"


def test_cli_generate_and_verify_real_package(tmp_path, source, capsys):
    snapshot, contract = source
    source_file = tmp_path / "source.json"
    source_file.write_text(json.dumps({"snapshot": snapshot, "artifact_contract": contract.__dict__}))
    target = tmp_path / "export"
    assert artifact_store_main(["generate", "--input", str(source_file), "--output-dir", str(target)]) == 0
    assert (target / "manifest.json").exists()
    assert artifact_store_main(["verify", "--directory", str(target)]) == 0
    assert artifact_store_main(["verify", "--directory", str(target), "--current-input", str(source_file)]) == 0
    assert "CURRENT" in capsys.readouterr().out


def test_cli_reports_stale_with_nonzero_exit(tmp_path, source):
    snapshot, contract = source
    target = tmp_path / "export"
    publish_verified_bundle(snapshot, contract, target)
    newer = deepcopy(snapshot)
    newer["circuits"][0]["load_va"] += 10
    path = tmp_path / "new.json"
    path.write_text(json.dumps({"snapshot": newer, "artifact_contract": contract.__dict__}))
    assert artifact_store_main(["verify", "--directory", str(target), "--current-input", str(path)]) == 2
