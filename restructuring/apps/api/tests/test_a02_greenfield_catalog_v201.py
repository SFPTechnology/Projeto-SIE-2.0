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
    for name in ("20261027195557_sie2_greenfield_foundation_owner_rls_v1.sql",):
        shutil.copy2(src / "migrations" / name, workspace / "migrations" / name)
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
