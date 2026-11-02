"""Onda 1 C15: real code paths, synthetic SHA-256 and fail-closed gate tests.

No Docker/Desktop, no Supabase connection, no real DB and no fake GO.
"""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[4]
MODULE=ROOT / "scripts/c15_integrity.py"
SPEC=importlib.util.spec_from_file_location("c15_integrity",MODULE)
assert SPEC and SPEC.loader
module=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)
DEST="fozrymsidnaxmuvxxfhh"
CONTRACT=ROOT/"docs/implantacao-sie-2-0/GREENFIELD/C08_CONTRATO_ENTREGA_C_V201.json"


def fixture(tmp_path):
    directory=tmp_path/"offline-test"
    report=module.synthetic_fixture(directory)
    return (directory, json.loads((directory/"manifest.json").read_text()),
            json.loads((directory/"synthetic-restore-proof.json").read_text()), report)


def test_generated_synthetic_sha256_succeeds_and_never_unlocks(tmp_path):
    directory,manifest,proof,result=fixture(tmp_path)
    assert result["gate"]=="NO_GO"
    assert result["automated_remote_ddl_authorized"] is False
    assert "REAL_BACKUP_REQUIRED" in result["remaining"]
    valid=module.verify_manifest(manifest,directory/"synthetic.dump")
    assert valid["backup_integrity"]=="PASS"
    assert valid["migration_go"] is False
    assert len(manifest["backup"]["sha256"])==64


def test_tampered_dump_fails(tmp_path):
    directory,manifest,_,_=fixture(tmp_path)
    with (directory/"synthetic.dump").open("ab") as output:
        output.write(b"CORRUPT")
    with pytest.raises(ValueError,match="size or SHA256"):
        module.verify_manifest(manifest,directory/"synthetic.dump")


def test_bad_project_file_or_mode_fails(tmp_path):
    directory,manifest,_,_=fixture(tmp_path)
    bad={**manifest,"project_ref":"hlbksclcandbsyqrsbmx"}
    with pytest.raises(ValueError,match="project"):
        module.verify_manifest(bad,directory/"synthetic.dump")
    bad={**manifest,"migration_go":True}
    with pytest.raises(ValueError,match="cannot grant"):
        module.verify_manifest(bad,directory/"synthetic.dump")
    bad={**manifest,"mode":"REAL_REMOTE_READ_ONLY"}
    assert module.verify_manifest(bad,directory/"synthetic.dump")["migration_go"] is False


def test_restore_wrong_hash_target_and_missing_checks_fails(tmp_path):
    directory,manifest,proof,_=fixture(tmp_path)
    source=directory/"synthetic.dump"
    bad={**proof,"backup_sha256":"0"*64}
    with pytest.raises(ValueError,match="exact backup"):
        module.verify_restore(manifest,source,bad)
    bad={**proof,"restore_target":"db.fozrymsidnaxmuvxxfhh.supabase.co"}
    with pytest.raises(ValueError,match="local"):
        module.verify_restore(manifest,source,bad)
    bad={**proof,"checks":{**proof["checks"]}}
    del bad["checks"]["roles_acl_equivalent"]
    with pytest.raises(ValueError,match="incomplete"):
        module.verify_restore(manifest,source,bad)


def test_restore_evidence_incomplete_blocks(tmp_path):
    directory,manifest,proof,_=fixture(tmp_path)
    proof["checks"]["roles_acl_equivalent"]=False
    result=module.verify_restore(manifest,directory/"synthetic.dump",proof)
    assert result["gate"]=="NO_GO"
    assert "roles_acl_equivalent" in result["remaining"]
    assert result["professional_acceptance"] is False


def test_no_docker_in_selected_windows_scripts_and_no_remote_write(tmp_path):
    scripts=("c15_native_common.ps1","c15_preflight_windows.ps1","c15_backup_native.ps1","c15_restore_native.ps1")
    content="\n".join((ROOT/"scripts"/p).read_text(encoding="utf-8") for p in scripts)
    assert "pg_dump" in content and "pg_restore" in content
    assert "PGSSLMODE" in content and "verify-full" in content
    assert "PGPASSFILE" in content
    assert "Assert-C15Local" in content
    assert "127.0.0.1" in content
    for token in ("& docker ", "docker info", "supabase db push", "supabase db reset",
                  "apply_migration(", "DROP DATABASE", "supabase db dump"):
        assert token not in content
    assert "remote_write_performed=$false" in content


def test_dockerless_c15_plan_and_conditional_go_not_rewritten():
    plan=ROOT/"docs/implantacao-sie-2-0/GREENFIELD/C15_PLANO_IMPLEMENTACAO_SEM_DOCKER_DESKTOP_V201.md"
    assert plan.is_file()
    contract=json.loads(CONTRACT.read_text(encoding="utf-8"))
    grant=contract["preproduction_authorization"]
    assert contract["state"]=="BLOCKED"
    assert grant["migration_application_permitted_now"] is False
    assert grant["legacy_import_permitted_now"] is False
    assert grant["backup_real_state"]=="MISSING"
    assert grant["restore_real_state"]=="MISSING"
    assert grant["selected_windows_backup_strategy"]=="POSTGRESQL_17_NATIVE_PG_DUMP_AND_PG_RESTORE_NOT_EXECUTED"
