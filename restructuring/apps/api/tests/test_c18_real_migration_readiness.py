"""C18: readiness for real migration remains evidence-gated, even under a new directive."""
import importlib.util
import json
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[4]
SPEC=importlib.util.spec_from_file_location("c18_readiness",ROOT/"scripts/c18_real_migration_readiness.py")
assert SPEC and SPEC.loader
mod=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod)
CONTRACT=ROOT/"docs/implantacao-sie-2-0/GREENFIELD/C08_CONTRATO_ENTREGA_C_V201.json"
MIGRATIONS=ROOT/"restructuring/supabase/migrations"


def baseline():
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def check(data=None, **changed):
    kwargs={
        "actual_applied":("20261027195557",),
        "auth_users":1,"auth_sessions":0,
        "dest_projects":0,"source_projects":5,
        "legacy_real_etl_enabled":False,
    }
    kwargs.update(changed)
    return mod.assess(data or baseline(),MIGRATIONS,**kwargs)


def test_real_migration_files_are_ordered_and_authenticated_by_sha():
    result=check()
    assert len(result["migration_files"])==4
    assert result["migration_order"]==[
        "20261028102000","20261028102100","20261028153000","20261028203000"
    ]
    for entry in result["migration_files"]:
        assert len(entry["sha256"])==64 and entry["bytes"]>0
    assert result["gate_gc"]=="BLOCKED"
    assert not result["migrations_remote_go"]
    assert not result["real_import_go"]


def test_no_real_auth_session_or_recovery_is_not_hidden_by_approval():
    result=check()
    assert "NO_VERIFIED_REAL_AUTH_SESSION" in result["blockers"]
    assert "DESTINATION_RECOVERY_ALTERNATIVE_PENDING" in result["blockers"]
    assert "REAL_ETL_IMPLEMENTATION_DISABLED" not in result["blockers"]
    assert "SOURCE_FIVE_PROJECT_INVENTORY_DRIFT" not in result["blockers"]
    assert result["delivery_strategy"]=="GREENFIELD_NO_LEGACY_IMPORT"
    assert result["legacy_import_requirement"]=="DEFERRED_OPTIONAL"
    assert result["honors_user_no_remote_backup_decision"]


def test_unauthenticated_or_migrated_target_is_detected():
    result=check(auth_users=1,auth_sessions=1,dest_projects=8)
    assert "DESTINATION_NOT_EMPTY_REVIEW_DRIFT" in result["blockers"]
    assert not result["migrations_remote_go"]


def test_unexpected_remote_applied_migration_blocks_readiness():
    with pytest.raises(ValueError,match="drift"):
        check(actual_applied=("20261027195557","20261028102000"))


def test_wrong_destination_and_unapproved_scoped_authorization_rejected():
    doc=baseline()
    doc["supabase_project_ref"]="hlbksclcandbsyqrsbmx"
    with pytest.raises(ValueError,match="destination"):
        check(data=doc)
    doc=baseline()
    doc["preproduction_authorization"]["migration_application_approved_conditionally"]=False
    with pytest.raises(ValueError,match="consent"):
        check(data=doc)


def test_even_falsified_entire_manifest_cannot_go_without_external_proof():
    doc=baseline()
    doc["preproduction_authorization"]["backup_real_state"]="VERIFIED"
    doc["preproduction_authorization"]["restore_real_state"]="VERIFIED"
    result=check(data=doc,auth_sessions=1,legacy_real_etl_enabled=True)
    assert result["migrations_remote_go"] is False
    assert result["real_import_go"] is False
    assert result["gate_gc"]=="BLOCKED"


def test_does_not_connect_or_execute_any_remote_sql():
    source=(ROOT/"scripts/c18_real_migration_readiness.py").read_text(encoding="utf-8")
    for item in ("psycopg", "execute_sql(", "apply_migration(", "create_engine(", "requests."):
        assert item not in source


def test_greenfield_ignores_missing_legacy_projects_without_silencing_auth_safety():
    result=check(source_projects=0,legacy_real_etl_enabled=False)
    assert "SOURCE_FIVE_PROJECT_INVENTORY_DRIFT" not in result["blockers"]
    assert "REAL_ETL_IMPLEMENTATION_DISABLED" not in result["blockers"]
    assert "DESTINATION_RECOVERY_ALTERNATIVE_PENDING" in result["blockers"]
    assert "NO_VERIFIED_REAL_AUTH_SESSION" in result["blockers"]
    assert result["gate_gc"]=="BLOCKED"


def test_historical_legacy_scoped_contract_remains_strict_if_selected():
    doc=baseline()
    doc["current_delivery_scope"]["strategy"]="LEGACY_IMPORT_SCOPED"
    result=check(data=doc,source_projects=0)
    assert "SOURCE_FIVE_PROJECT_INVENTORY_DRIFT" in result["blockers"]
    assert "REAL_ETL_IMPLEMENTATION_DISABLED" in result["blockers"]
    assert result["legacy_import_requirement"]=="REQUIRED"


def test_greenfield_requires_no_access_to_legacy_database():
    result=check(source_projects=None)
    assert result["legacy_import_requirement"]=="DEFERRED_OPTIONAL"
    assert result["read_only_observations"]["source_projects"] is None
    assert "SOURCE_FIVE_PROJECT_INVENTORY_DRIFT" not in result["blockers"]
    assert "DESTINATION_RECOVERY_ALTERNATIVE_PENDING" in result["blockers"]


def test_c17_refusal_is_constraint_not_a_failed_recovery_proof():
    result=check()
    assert "USER_DECLINED_REMOTE_BACKUP" not in result["blockers"]
    assert result["recovery_requirement"] == "INDEPENDENTLY_PROVEN_DESTINATION_RECOVERY"
    assert not result["recovery_alternative_verified_by_this_check"]


def test_fabricated_alternative_or_backup_flags_cannot_satisfy_recovery():
    doc=baseline()
    doc["preproduction_authorization"].update(
        backup_real_state="VERIFIED", restore_real_state="VERIFIED",
        alternative_recovery_verified=True)
    result=check(data=doc, auth_sessions=1)
    assert "DESTINATION_RECOVERY_ALTERNATIVE_PENDING" in result["blockers"]
    assert not result["migrations_remote_go"]
    assert not result["recovery_alternative_verified_by_this_check"]


def test_historical_backup_path_is_preserved_when_c17_not_declined():
    doc=baseline()
    doc["effective_user_decision_20261104"]["c17_execution_permitted"]=True
    result=check(data=doc)
    assert "NO_VERIFIED_RECOVERABLE_DESTINATION_BACKUP_AND_RESTORE" in result["blockers"]
    assert "DESTINATION_RECOVERY_ALTERNATIVE_PENDING" not in result["blockers"]
    assert not result["migrations_remote_go"]
