"""C15: offline integrity and gate verifier, stdlib only, no DB or secrets.

Commands only read local files. A synthetic record never authorizes remote DDL.
The real backup manifest documents pg_dump completeness and a restore report
documents the separately executed native PostgreSQL recovery.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

DEST = "fozrymsidnaxmuvxxfhh"
REQUIRED_CHECKS = (
    "dump_exit_zero", "restore_exit_zero", "schema_equivalent",
    "row_counts_equivalent", "rls_policies_equivalent",
    "auth_data_equivalent", "roles_acl_equivalent",
    "extensions_equivalent", "external_services_recovery_reviewed",
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def verify_manifest(manifest: dict, backup: Path, expected_ref: str = DEST) -> dict:
    if type(manifest) is not dict:
        raise ValueError("manifest must be an object")
    if manifest.get("schema_version") != "C15-1" or manifest.get("project_ref") != expected_ref:
        raise ValueError("unrecognized project or C15 manifest")
    if manifest.get("mode") not in ("REAL_REMOTE_READ_ONLY", "SYNTHETIC_OFFLINE"):
        raise ValueError("unsupported mode")
    if manifest.get("dump_format") != "custom" or manifest.get("remote_write_performed") is not False:
        raise ValueError("unsafe or unsupported dump manifest")
    if manifest.get("migration_go") is not False or manifest.get("restore_state") != "NOT_VERIFIED":
        raise ValueError("backup manifest cannot grant restore or migration")
    info = manifest.get("backup", {})
    if not isinstance(info, dict) or info.get("name") != backup.name:
        raise ValueError("backup identity mismatch")
    if not backup.is_file() or backup.stat().st_size <= 0:
        raise ValueError("backup missing or empty")
    actual_hash = sha256(backup)
    if actual_hash != info.get("sha256") or backup.stat().st_size != info.get("bytes"):
        raise ValueError("backup size or SHA256 mismatch")
    if manifest["mode"] == "SYNTHETIC_OFFLINE" and manifest.get("source_kind") != "SYNTHETIC_FIXTURE":
        raise ValueError("synthetic fixture provenance missing")
    return {
        "backup_integrity": "PASS",
        "project_ref": expected_ref,
        "mode": manifest["mode"],
        "sha256": actual_hash,
        "restore_state": "NOT_VERIFIED",
        "migration_go": False,
    }


def verify_restore(manifest: dict, backup: Path, proof: dict) -> dict:
    base = verify_manifest(manifest, backup)
    if not isinstance(proof, dict) or proof.get("schema_version") != "C15-RESTORE-1":
        raise ValueError("invalid restore evidence format")
    if proof.get("project_ref") != base["project_ref"]:
        raise ValueError("restore project identity mismatch")
    if proof.get("backup_sha256") != base["sha256"]:
        raise ValueError("restore proof does not match exact backup")
    if proof.get("restore_target") != "LOCAL_POSTGRESQL_17_DISPOSABLE":
        raise ValueError("restore must be local and disposable")
    checks = proof.get("checks")
    if type(checks) is not dict or set(checks) != set(REQUIRED_CHECKS):
        raise ValueError("required restore checks incomplete")
    failures = sorted(key for key, value in checks.items() if value is not True)
    # A synthetic fixture is never a valid real pre-migration restore, even if
    # its locally generated example satisfies all the booleans.
    if base["mode"] == "SYNTHETIC_OFFLINE":
        failures.append("REAL_BACKUP_REQUIRED")
    state = "VERIFICATION_REQUIRED" if failures else "PASS_DOCUMENTARY_CHECKS"
    return {
        "gate": "NO_GO" if failures else "REVIEW_REQUIRED",
        "verification_state": state,
        "remaining": failures,
        "automated_remote_ddl_authorized": False,
        "professional_acceptance": False,
        "sha256": base["sha256"],
    }


def synthetic_fixture(outdir: Path) -> dict:
    outdir.mkdir(parents=True, exist_ok=False)
    dump = outdir / "synthetic.dump"
    dump.write_bytes(b"PGDMP" + b"C15-synthetic-only-" * 16)
    m = {
        "schema_version": "C15-1",
        "project_ref": DEST,
        "mode": "SYNTHETIC_OFFLINE",
        "source_kind": "SYNTHETIC_FIXTURE",
        "dump_format": "custom",
        "remote_write_performed": False,
        "migration_go": False,
        "restore_state": "NOT_VERIFIED",
        "utc_created_at": datetime.now(timezone.utc).isoformat(),
        "backup": {"name": dump.name, "bytes": dump.stat().st_size, "sha256": sha256(dump)},
    }
    (outdir / "manifest.json").write_text(json.dumps(m, indent=2) + "\n", encoding="utf-8")
    proof = {
        "schema_version": "C15-RESTORE-1",
        "project_ref": DEST,
        "backup_sha256": m["backup"]["sha256"],
        "restore_target": "LOCAL_POSTGRESQL_17_DISPOSABLE",
        "checks": {item: True for item in REQUIRED_CHECKS},
    }
    (outdir / "synthetic-restore-proof.json").write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
    return verify_restore(m, dump, proof)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="mode", required=True)
    for name in ("verify-backup", "verify-restore"):
        cmd = sub.add_parser(name)
        cmd.add_argument("--manifest", type=Path, required=True)
        cmd.add_argument("--backup", type=Path, required=True)
        if name == "verify-restore":
            cmd.add_argument("--proof", type=Path, required=True)
    s = sub.add_parser("synthetic-test")
    s.add_argument("--output", type=Path, required=True)
    args = p.parse_args()
    if args.mode == "synthetic-test":
        output = synthetic_fixture(args.output)
    else:
        m = json.loads(args.manifest.read_text(encoding="utf-8-sig"))
        if args.mode == "verify-backup":
            output = verify_manifest(m, args.backup)
        else:
            proof = json.loads(args.proof.read_text(encoding="utf-8-sig"))
            output = verify_restore(m, args.backup, proof)
    print(json.dumps(output, sort_keys=True))
    if output.get("backup_integrity") == "PASS":
        return
    if output.get("gate") == "NO_GO":
        # Deliberate exit code 0 for a safe, correctly denied synthetic trial.
        return


if __name__ == "__main__":
    main()
