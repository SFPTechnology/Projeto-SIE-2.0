"""Static, read-only guard for SIE 2.0 greenfield migrations.

Usage: python restructuring/supabase/greenfield/check_catalog.py [--root REPO] [--json]
Does NOT invoke Supabase, connect to a DB, or execute migrations.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

TABLES = (
    "sie_projects", "sie_project_revisions", "sie_rooms", "sie_loads",
    "sie_circuits", "sie_circuit_loads", "sie_calculation_runs",
    "sie_artifacts", "sie_audit_events",
)
MIGRATION_NAME = re.compile(r"^(\d{14})_([a-z][a-z0-9_]*)\.sql$")
GIT_BLOB = re.compile(r"^[0-9a-f]{40}$")


def git_blob_sha1(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode("ascii") + b"\x00"
    return hashlib.sha1(header + data).hexdigest()


def verify(root: Path) -> dict:
    root = Path(root).resolve()
    workspace = root / "restructuring" / "supabase"
    errors: list[str] = []
    details: list[dict] = []
    manifest_path = workspace / "greenfield" / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return {"ok": False, "errors": [f"manifest unreadable: {exc}"], "files": []}

    if manifest.get("project_ref") != "fozrymsidnaxmuvxxfhh":
        errors.append("unexpected project_ref")
    if manifest.get("migration_directory") != "restructuring/supabase/migrations":
        errors.append("migration workspace may not be repository legacy root")
    if manifest.get("forbidden_legacy_directory") != "supabase/migrations":
        errors.append("legacy migration exclusion missing")
    if manifest.get("remote_ddl_authorized") is not False:
        errors.append("remote DDL authorization cannot be declared by static manifest")
    entries = manifest.get("applied_migrations")
    if not isinstance(entries, list) or not entries:
        errors.append("no declared baseline migrations")
        entries = []
    pending = manifest.get("pending_migrations", [])
    if not isinstance(pending, list):
        errors.append("pending_migrations must be an array")
        pending = []
    if any(item.get("applied_remote") is not False for item in pending):
        errors.append("pending migration falsely claims remote application")
    applied_names = {item.get("file") for item in entries}
    declared: set[str] = set()
    versions: set[str] = set()
    for item in entries + pending:
        name = item.get("file", "")
        match = MIGRATION_NAME.fullmatch(name)
        if not match or "/" in name or ".." in name:
            errors.append(f"invalid migration file {name!r}")
            continue
        if match.group(1) != item.get("version") or match.group(2) != item.get("name"):
            errors.append(f"filename/version mismatch for {name}")
        if match.group(1) in versions or name in declared:
            errors.append(f"duplicated migration {name}")
        declared.add(name)
        versions.add(match.group(1))
        expected_sha1 = item.get("git_blob_sha1", "")
        if not GIT_BLOB.fullmatch(expected_sha1):
            errors.append(f"invalid source blob SHA for {name}")
        path = workspace / "migrations" / name
        try:
            raw = path.read_bytes()
        except OSError:
            errors.append(f"migration missing: {name}")
            continue
        digest = git_blob_sha1(raw)
        if digest != expected_sha1:
            errors.append(f"migration modified or incorrect source blob: {name}")
        sql = raw.decode("utf-8")
        details.append({"file": name, "version": match.group(1),
                        "state": "APPLIED" if name in applied_names else "PENDING",
                        "git_blob_sha1": digest, "sha256": hashlib.sha256(raw).hexdigest()})
        if match.group(1) == "20261027195557":
            if "DROP TABLE" in sql.upper() or "TRUNCATE " in sql.upper():
                errors.append("GF02 baseline unexpectedly includes destructive statements")
            tables = re.findall(r"(?im)^CREATE TABLE public\.(sie_[a-z_]+)\s*\(", sql)
            if set(tables) != set(TABLES):
                errors.append(f"GF02 table set differs: {sorted(tables)}")
            if len(re.findall(r"(?im)^ALTER TABLE public\.sie_[a-z_]+ ENABLE ROW LEVEL SECURITY;", sql)) != 9:
                errors.append("GF02 requires 9 RLS-enabling statements")
            if len(re.findall(r"(?im)^CREATE POLICY sie_[a-z_]+", sql)) != 16:
                errors.append("GF02 requires 16 policy definitions")
            if "raw_user_meta_data" in sql.lower():
                errors.append("untrusted user_metadata authorization detected")
            if re.search(r"(?i)\bGRANT\s+.+\bTO\s+anon\s*;", sql):
                errors.append("anonymous table grant detected")

    directory = workspace / "migrations"
    actual = {p.name for p in directory.glob("*.sql")} if directory.is_dir() else set()
    if actual != declared:
        errors.append(f"canonical manifest drift: unlisted={sorted(actual - declared)}, absent={sorted(declared - actual)}")
    if len(versions) != len(declared):
        errors.append("migration version collision")
    return {
        "ok": not errors, "project_ref": manifest.get("project_ref"),
        "scope": "static-catalog-only; not remote schema equivalence",
        "migrations": [x for x in details if x["state"] == "APPLIED"],
        "pending_migrations": [x for x in details if x["state"] == "PENDING"],
        "errors": errors,
        "legacy_root_excluded": True,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path,
                        default=Path(__file__).resolve().parents[3],
                        help="Repository root")
    parser.add_argument("--json", action="store_true", help="JSON report")
    args = parser.parse_args(argv)
    result = verify(args.root)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print("PASS" if result["ok"] else "FAIL", json.dumps(result, ensure_ascii=False))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
