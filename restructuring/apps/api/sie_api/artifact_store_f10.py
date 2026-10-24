"""F10 local immutable-export boundary: manifest, snapshot and fail-closed verification.

This is local study-document persistence, not a production database or an
attestation that the underlying electrical installation is compliant.
"""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
from typing import Any
from uuid import UUID, uuid4

try:
    import fcntl
except ImportError:  # pragma: no cover - exercised on Windows
    fcntl = None
    import msvcrt

from .representation_f10 import ArtifactContract, ArtifactError, artifact_bundle

_ALLOWED_NAME = re.compile(r"^[a-z][a-z0-9_]*\.(?:json|csv|svg|html|pdf)$")
_CONTRACT_FIELDS = (
    "project_id", "revision_id", "calculation_run_id", "rule_version", "template_version"
)


def _digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _canonical_json(data: Any) -> bytes:
    try:
        return json.dumps(
            data, sort_keys=True, ensure_ascii=False, allow_nan=False,
            separators=(",", ":")
        ).encode("utf-8")
    except (TypeError, ValueError, OverflowError) as exc:
        raise ArtifactError("snapshot is not canonically serializable") from exc


def build_verified_bundle(
    snapshot: dict[str, Any], contract: ArtifactContract,
    artifact_id: str | None = None,
) -> tuple[dict[str, bytes], dict[str, Any]]:
    """Render from one detached snapshot/contract captured before generation."""
    # Serialize first, then render and persist from the same detached value. This
    # prevents a caller mutating a shared snapshot between rendering and hashing
    # it, which could otherwise produce a hybrid package.
    snapshot_bytes = _canonical_json(snapshot)
    frozen_snapshot = json.loads(snapshot_bytes)
    frozen_contract = ArtifactContract(
        **{key: getattr(contract, key) for key in _CONTRACT_FIELDS}
    )
    if artifact_id is None:
        artifact_id = str(uuid4())
    try:
        artifact_id = str(UUID(str(artifact_id)))
    except (ValueError, TypeError, AttributeError) as exc:
        raise ArtifactError("artifact_id must be a UUID") from exc
    rendered = artifact_bundle(frozen_snapshot, frozen_contract)
    files = {name: (content if isinstance(content, bytes) else content.encode("utf-8")) for name, content in rendered.items()}
    files["snapshot.json"] = snapshot_bytes + b"\n"
    if not all(_ALLOWED_NAME.fullmatch(name) for name in files):
        raise ArtifactError("unsafe artifact filename")
    snapshot_sha = _digest(files["snapshot.json"])
    manifest = {
        "schema_version": "F10-MANIFEST-1",
        "artifact_id": artifact_id,
        "artifact_type": "electrical_study_bundle",
        "artifact_status": "STUDY",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "snapshot_id": snapshot_sha,
        "snapshot_sha256": snapshot_sha,
        "dependencies": {
            **{key: getattr(frozen_contract, key) for key in _CONTRACT_FIELDS},
            "floor_plan_id": frozen_snapshot.get("floor_plan", {}).get("id")
                if isinstance(frozen_snapshot.get("floor_plan"), dict) else None,
        },
        "files_sha256": {name: _digest(data) for name, data in sorted(files.items())},
        "normative_conformity_verified": False,
    }
    if frozen_snapshot.get("full_f10") is True:
        manifest["dependencies"]["calculation_scope_f10"] = frozen_snapshot["calculation_scope_f10"]
        manifest["dependencies"]["calculation_dependencies_f10"] = frozen_snapshot["calculation_dependencies_f10"]
    files["manifest.json"] = _canonical_json(manifest) + b"\n"
    return files, manifest


def publish_verified_bundle(
    snapshot: dict[str, Any], contract: ArtifactContract, destination: str | Path,
    artifact_id: str | None = None,
) -> dict[str, Any]:
    files, manifest = build_verified_bundle(snapshot, contract, artifact_id)
    return publish_prebuilt_bundle(files, manifest, destination)


@contextmanager
def artifact_parent_lock(destination: str | Path, *, shared: bool = False,
                         create_parent: bool = True):
    """Coordinate registry+filesystem operations sharing a destination parent."""
    target = Path(destination).expanduser().absolute()
    if create_parent:
        target.parent.mkdir(parents=True, exist_ok=True)
    for ancestor in (target.parent, *target.parent.parents):
        if ancestor.is_symlink():
            raise ArtifactError("artifact destination path cannot contain symlinks")
    if fcntl is not None:
        lock_fd = os.open(target.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    else:  # Windows byte-range lock; the OS releases it when the process exits.
        lock_path = target.parent / ".sie-f10-publisher.lock"
        lock_fd = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o600)
        if os.fstat(lock_fd).st_size == 0:
            os.write(lock_fd, b"\0")
            os.fsync(lock_fd)
    try:
        if fcntl is not None:
            fcntl.flock(lock_fd, fcntl.LOCK_SH if shared else fcntl.LOCK_EX)
        else:
            os.lseek(lock_fd, 0, os.SEEK_SET)
            msvcrt.locking(lock_fd, msvcrt.LK_LOCK, 1)
        yield lock_fd
    finally:
        if fcntl is not None:
            fcntl.flock(lock_fd, fcntl.LOCK_UN)
        else:
            os.lseek(lock_fd, 0, os.SEEK_SET)
            msvcrt.locking(lock_fd, msvcrt.LK_UNLCK, 1)
        os.close(lock_fd)


def publish_prebuilt_bundle(
    files: dict[str, bytes], manifest: dict[str, Any], destination: str | Path,
    *, lock_held: bool = False,
) -> dict[str, Any]:
    """Stage complete output and atomically expose its directory, never overwrite.

    An advisory lock on the parent directory coordinates writers across
    processes and is released by the OS after a crash; it cannot become a stale
    lock file. No promise is made against actors modifying files outside this API.
    """
    if not isinstance(manifest, dict) or not isinstance(files, dict):
        raise ArtifactError("prebuilt artifact package is invalid")
    manifest_bytes = _canonical_json(manifest) + b"\n"
    if files.get("manifest.json") != manifest_bytes or "snapshot.json" not in files:
        raise ArtifactError("prebuilt manifest and files diverge")
    if any(not isinstance(name, str) or not _ALLOWED_NAME.fullmatch(name)
           or not isinstance(data, bytes) for name, data in files.items()):
        raise ArtifactError("prebuilt artifact contains unsafe files")
    expected_files = manifest.get("files_sha256")
    if (not isinstance(expected_files, dict)
            or set(expected_files) != set(files) - {"manifest.json"}
            or any(_digest(files[name]) != expected_files.get(name) for name in expected_files)
            or _digest(files["snapshot.json"]) != manifest.get("snapshot_sha256")):
        raise ArtifactError("prebuilt artifact hashes do not match manifest")
    try:
        artifact_id = str(UUID(str(manifest["artifact_id"])))
    except (KeyError, ValueError, TypeError, AttributeError) as exc:
        raise ArtifactError("prebuilt artifact_id must be a UUID") from exc
    target = Path(destination)
    target.parent.mkdir(parents=True, exist_ok=True)
    if lock_held:
        if fcntl is not None:
            lock_fd = os.open(target.parent, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
            try:
                return _publish_prebuilt_bundle_locked(files, manifest, target, lock_fd)
            finally:
                os.close(lock_fd)
        return _publish_prebuilt_bundle_locked(files, manifest, target, None)
    with artifact_parent_lock(target) as lock_fd:
        return _publish_prebuilt_bundle_locked(files, manifest, target, lock_fd)


def _publish_prebuilt_bundle_locked(
    files: dict[str, bytes], manifest: dict[str, Any], target: Path, lock_fd: int | None,
) -> dict[str, Any]:
    artifact_id = str(UUID(str(manifest["artifact_id"])))
    stage: Path | None = None
    try:
        if target.exists() or target.is_symlink():
            raise FileExistsError(f"artifact destination already exists: {target}")
        stage = target.parent / (".f10-stage-" + artifact_id)
        if stage.is_symlink():
            raise ArtifactError("staging path is a symlink")
        if stage.exists():
            if not stage.is_dir():
                raise ArtifactError("staging path is not a directory")
            shutil.rmtree(stage)
        stage.mkdir(mode=0o700)
        os.chmod(stage, 0o700)
        for name, data in files.items():
            with (stage / name).open("xb") as output:
                output.write(data)
                output.flush()
                os.fsync(output.fileno())
        if os.name != "nt":
            stage_fd = os.open(stage, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
            try:
                os.fsync(stage_fd)
            finally:
                os.close(stage_fd)
        if target.exists() or target.is_symlink():
            raise FileExistsError(f"artifact destination already exists: {target}")
        os.rename(stage, target)
        stage = None
        if fcntl is not None and lock_fd is not None:
            os.fsync(lock_fd)
        elif lock_fd is not None:
            os.fsync(lock_fd)
        return manifest
    finally:
        if stage is not None:
            shutil.rmtree(stage)


def verify_verified_bundle(
    directory: str | Path,
    current_snapshot: dict[str, Any] | None = None,
    current_contract: ArtifactContract | None = None,
    *, lock_held: bool = False,
) -> dict[str, Any]:
    """Verify under a shared publisher lock unless the caller already holds it."""
    if lock_held:
        return _verify_verified_bundle_locked(directory, current_snapshot, current_contract)
    with artifact_parent_lock(directory, shared=True, create_parent=False):
        return _verify_verified_bundle_locked(directory, current_snapshot, current_contract)


def _verify_verified_bundle_locked(
    directory: str | Path,
    current_snapshot: dict[str, Any] | None = None,
    current_contract: ArtifactContract | None = None,
) -> dict[str, Any]:
    """Integrity is checked against stored bytes; currentness needs live input.

    Without an independently supplied current source, CURRENT is never returned.
    This function does not verify signatures or authorize source revisions.
    """
    root = Path(directory)
    if root.is_symlink() or not root.is_dir():
        raise ArtifactError("artifact directory missing or not a regular directory")
    manifest_path = root / "manifest.json"
    if not manifest_path.is_file() or manifest_path.is_symlink():
        raise ArtifactError("manifest missing or not a regular file")
    try:
        manifest = json.loads(manifest_path.read_bytes())
        if manifest.get("schema_version") != "F10-MANIFEST-1":
            raise ArtifactError("unknown manifest schema")
        expected_hashes = manifest["files_sha256"]
        if not isinstance(expected_hashes, dict) or "snapshot.json" not in expected_hashes:
            raise ArtifactError("manifest has no snapshot")
        expected_names = set(expected_hashes) | {"manifest.json"}
        if (any(not isinstance(name, str) or not _ALLOWED_NAME.fullmatch(name) for name in expected_names)
                or {p.name for p in root.iterdir()} != expected_names):
            raise ArtifactError("artifact file inventory mismatch")
        payloads = {}
        for name, expected_hash in expected_hashes.items():
            path = root / name
            if path.is_symlink() or not path.is_file():
                raise ArtifactError(f"not a regular artifact file: {name}")
            payload = path.read_bytes()
            if not isinstance(expected_hash, str) or _digest(payload) != expected_hash:
                raise ArtifactError(f"artifact hash mismatch: {name}")
            payloads[name] = payload
        if _digest(payloads["snapshot.json"]) != manifest.get("snapshot_sha256"):
            raise ArtifactError("snapshot hash mismatch")
        if manifest.get("snapshot_id") != manifest["snapshot_sha256"]:
            raise ArtifactError("snapshot id mismatch")
        stored_snapshot = json.loads(payloads["snapshot.json"])
        if _canonical_json(stored_snapshot) + b"\n" != payloads["snapshot.json"]:
            raise ArtifactError("noncanonical snapshot")
        dependencies = manifest.get("dependencies")
        if not isinstance(dependencies, dict):
            raise ArtifactError("missing dependency contract")
        stored_contract = ArtifactContract(
            **{key: dependencies[key] for key in _CONTRACT_FIELDS}
        )
        if stored_snapshot.get("full_f10") is True:
            for name in ("calculation_scope_f10", "calculation_dependencies_f10"):
                if dependencies.get(name) != stored_snapshot.get(name):
                    raise ArtifactError("manifest per-circuit dependencies differ from snapshot")
        regenerated = artifact_bundle(stored_snapshot, stored_contract)
        if set(regenerated) | {"snapshot.json"} != set(payloads):
            raise ArtifactError("generated artifact inventory diverges from snapshot")
        for name, content in regenerated.items():
            if (content if isinstance(content, bytes) else content.encode("utf-8")) != payloads[name]:
                raise ArtifactError(f"artifact diverges from snapshot: {name}")
        if manifest.get("normative_conformity_verified") is not False:
            raise ArtifactError("manifest cannot claim normative conformity")
    except (OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError) as exc:
        raise ArtifactError("invalid artifact package or manifest") from exc

    status = "CURRENTNESS_UNVERIFIED"
    if current_snapshot is not None or current_contract is not None:
        if current_snapshot is None or current_contract is None:
            raise ArtifactError("both current_snapshot and current_contract are required")
        try:
            artifact_bundle(current_snapshot, current_contract)
            current_bytes = _canonical_json(current_snapshot) + b"\n"
            same_identity = all(
                dependencies[key] == getattr(current_contract, key) for key in _CONTRACT_FIELDS
            )
            status = "CURRENT" if same_identity and _digest(current_bytes) == manifest["snapshot_sha256"] else "STALE"
        except ArtifactError:
            status = "SOURCE_INVALID"
    return {
        "artifact_id": manifest["artifact_id"],
        "snapshot_sha256": manifest["snapshot_sha256"],
        "integrity": "VERIFIED",
        "currentness": status,
        "normative_conformity_verified": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="F10 local export and integrity verification.")
    commands = parser.add_subparsers(dest="command", required=True)
    generate = commands.add_parser("generate")
    generate.add_argument("--input", required=True)
    generate.add_argument("--output-dir", required=True)
    verify = commands.add_parser("verify")
    verify.add_argument("--directory", required=True)
    verify.add_argument("--current-input", help="Trusted current snapshot/contract JSON")
    args = parser.parse_args(argv)
    if args.command == "generate":
        payload = json.loads(Path(args.input).read_text(encoding="utf-8-sig"))
        contract = ArtifactContract(**payload["artifact_contract"])
        result = publish_verified_bundle(payload["snapshot"], contract, args.output_dir)
        print(json.dumps({"artifact_id": result["artifact_id"],
                          "snapshot_sha256": result["snapshot_sha256"],
                          "files": sorted(result["files_sha256"]), "status": "STUDY"},
                         ensure_ascii=False))
        return 0
    live = None
    contract = None
    if args.current_input:
        source = json.loads(Path(args.current_input).read_text(encoding="utf-8-sig"))
        live = source["snapshot"]
        contract = ArtifactContract(**source["artifact_contract"])
    result = verify_verified_bundle(args.directory, live, contract)
    print(json.dumps(result, ensure_ascii=False))
    return 0 if result["currentness"] not in {"STALE", "SOURCE_INVALID"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
