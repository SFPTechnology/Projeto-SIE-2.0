"""V2.0.1 / A02: tests the canonical catalog without connecting to Supabase."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil

import pytest

ROOT = Path(__file__).resolve().parents[4]
MODULE = ROOT / "restructuring" / "supabase" / "greenfield" / "check_catalog.py"
spec = importlib.util.spec_from_file_location("sie2_greenfield_check_catalog", MODULE)
assert spec is not None and spec.loader is not None
catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalog)


def copy_workspace(tmp_path: Path) -> Path:
    workspace = tmp_path / "restructuring" / "supabase"
    (workspace / "migrations").mkdir(parents=True)
    (workspace / "greenfield").mkdir(parents=True)
    src = ROOT / "restructuring" / "supabase"
    for file in (src / "migrations").glob("*.sql"):
        shutil.copy2(file, workspace / "migrations" / file.name)
    shutil.copy2(src / "greenfield" / "manifest.json",
                 workspace / "greenfield" / "manifest.json")
    return workspace


def test_real_repo_catalog_is_canonical():
    result = catalog.verify(ROOT)
    assert result["ok"], result["errors"]
    assert result["legacy_root_excluded"] is True
    assert len(result["migrations"]) == 1
    assert len(result["migrations"][0]["sha256"]) == 64


def test_legacy_root_migrations_are_not_part_of_catalog(tmp_path):
    copy_workspace(tmp_path)
    old = tmp_path / "supabase" / "migrations"
    old.mkdir(parents=True)
    (old / "20260701000000_legacy.sql").write_text("CREATE TABLE public.legacy(x int);")
    assert catalog.verify(tmp_path)["ok"]


def test_detects_baseline_tampering(tmp_path):
    workspace = copy_workspace(tmp_path)
    sql = next((workspace / "migrations").glob("*.sql"))
    sql.write_bytes(sql.read_bytes() + b"\n-- unauthorized byte\n")
    result = catalog.verify(tmp_path)
    assert not result["ok"]
    assert any("incorrect source blob" in error for error in result["errors"])


def test_rejects_unlisted_migration(tmp_path):
    workspace = copy_workspace(tmp_path)
    (workspace / "migrations" / "20261028000000_extra.sql").write_text("SELECT 1;")
    result = catalog.verify(tmp_path)
    assert not result["ok"]
    assert any("manifest drift" in error for error in result["errors"])


def test_rejects_project_ref_change(tmp_path):
    workspace = copy_workspace(tmp_path)
    manifest_path = workspace / "greenfield" / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["project_ref"] = "not-the-authorized-project"
    manifest_path.write_text(json.dumps(manifest))
    result = catalog.verify(tmp_path)
    assert not result["ok"]
    assert "unexpected project_ref" in result["errors"]


def test_refuses_static_authorization_to_write_production(tmp_path):
    workspace = copy_workspace(tmp_path)
    manifest_path = workspace / "greenfield" / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["remote_ddl_authorized"] = True
    manifest_path.write_text(json.dumps(manifest))
    result = catalog.verify(tmp_path)
    assert not result["ok"]
    assert any("DDL authorization" in error for error in result["errors"])


def test_a03_a04_pending_migrations_match_manifest_and_are_not_applied():
    result = catalog.verify(ROOT)
    assert result["ok"], result["errors"]
    assert len(result["migrations"]) == 1  # GF02 remains the only installed migration
    pending = result["pending_migrations"]
    assert [item["version"] for item in pending] == [
        "20261028102000", "20261028102100", "20261028153000",
        "20261028203000"]
    assert all(item["state"] == "PENDING" for item in pending)
    manifest = json.loads((ROOT / "restructuring" / "supabase" / "greenfield"
                           / "manifest.json").read_text())
    assert manifest["remote_ddl_authorized"] is False
    assert all(item["applied_remote"] is False for item in manifest["pending_migrations"])


def test_pending_migration_cannot_falsely_claim_remote_application(tmp_path):
    workspace = copy_workspace(tmp_path)
    manifest_path = workspace / "greenfield" / "manifest.json"
    manifest = json.loads(manifest_path.read_text())
    manifest["pending_migrations"][0]["applied_remote"] = True
    manifest_path.write_text(json.dumps(manifest))
    result = catalog.verify(tmp_path)
    assert not result["ok"]
    assert any("falsely claims remote application" in e for e in result["errors"])


def test_a03_a04_are_additive_without_legacy_table_creation():
    root = ROOT / "restructuring" / "supabase" / "migrations"
    for version in ("20261028102000", "20261028102100", "20261028153000"):
        sql = next(root.glob(version + "_*.sql")).read_text()
        executable = "\n".join(
            line for line in sql.splitlines() if not line.strip().startswith("--")
        )
        assert "DROP TABLE" not in executable.upper()
        assert "CREATE TABLE" not in executable.upper()
        assert "public.projetos" not in executable.lower()
    lifecycle = next(root.glob("20261028102100_*.sql")).read_text()
    for table in ("sie_rooms", "sie_loads", "sie_circuits", "sie_circuit_loads"):
        assert "BEFORE INSERT OR UPDATE OR DELETE ON public." + table in lifecycle
    assert "SEALED" in lifecycle and "SUPERSEDED" in lifecycle
