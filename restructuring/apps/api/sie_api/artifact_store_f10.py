"""F10 local immutable-export boundary: manifest, snapshot and fail-closed verification.

This is local study-document persistence, not a production database or an
attestation that the underlying electrical installation is compliant.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import tempfile
from typing import Any
from uuid import uuid4

from .representation_f10 import ArtifactContract, ArtifactError, artifact_bundle

_ALLOWED_NAME = re.compile(r"^[a-z][a-z0-9_]*\.(?:json|csv|svg|html)$")
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
) -> tuple[dict[str, bytes], dict[str, Any]]:
    """Generate all payloads before touching the destination directory."""
    rendered = artifact_bundle(snapshot, contract)
    files = {name: content.encode("utf-8") for name, content in rendered.items()}
    files["snapshot.json"] = _canonical_json(snapshot) + b"\n"
    if not all(_ALLOWED_NAME.fullmatch(name) for name in files):
        raise ArtifactError("unsafe artifact filename")
    snapshot_sha = _digest(files["snapshot.json"])
    manifest = {
        "schema_version": "F10-MANIFEST-1",
        "artifact_id": str(uuid4()),
        "artifact_type": "electrical_study_bundle",
        "artifact_status": "STUDY",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "snapshot_id": snapshot_sha,
        "snapshot_sha256": snapshot_sha,
        "dependencies": {
            **{key: getattr(contract, key) for key in _CONTRACT_FIELDS},
            "floor_plan_id": snapshot.get("floor_plan", {}).get("id")
                if isinstance(snapshot.get("floor_plan"), dict) else None,
        },
        "files_sha256": {name: _digest(data) for name, data in sorted(files.items())},
        "normative_conformity_verified": False,
    }
    files["manifest.json"] = _canonical_json(manifest) + b"\n"
    return files, manifest


def publish_verified_bundle(
    snapshot: dict[str, Any], contract: ArtifactContract, destination: str | Path,
) -> dict[str, Any]:
    """Stage complete output and atomically expose its directory, never overwrite.

    Exclusive sibling lock coordinates writers using this function. No promise
    is made against actors modifying files outside this API.
    """
    files, manifest = build_verified_bundle(snapshot, contract)
    target = Path(destination)
    target.parent.mkdir(parents=True, exist_ok=True)
    lock_path = target.parent / ("." + target.name + ".f10.lock")
    lock_fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    stage: Path | None = None
    try:
        if target.exists() or target.is_symlink():
            raise FileExistsError(f"artifact destination already exists: {target}")
        stage = Path(tempfile.mkdtemp(prefix=".f10-stage-", dir=target.parent))
        os.chmod(stage, 0o700)
        for name, data in files.items():
            with (stage / name).open("xb") as output:
                output.write(data)
                output.flush()
                os.fsync(output.fileno())
        if target.exists() or target.is_symlink():
            raise FileExistsError(f"artifact destination already exists: {target}")
        os.rename(stage, target)
        stage = None
        return manifest
    finally:
        if stage is not None:
            shutil.rmtree(stage)
        os.close(lock_fd)
        lock_path.unlink(missing_ok=True)


def verify_verified_bundle(
    directory: str | Path,
    current_snapshot: dict[str, Any] | None = None,
    current_contract: ArtifactContract | None = None,
) -> dict[str, Any]:
    """Integrity is checked against stored bytes; currentness needs live input.

    Without an independently supplied current source, CURRENT is never returned.
    This function does not verify signatures or authorize source revisions.
    """
    root = Path(directory)
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
        regenerated = artifact_bundle(stored_snapshot, stored_contract)
        if set(regenerated) | {"snapshot.json"} != set(payloads):
            raise ArtifactError("generated artifact inventory diverges from snapshot")
        for name, content in regenerated.items():
            if content.encode("utf-8") != payloads[name]:
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
