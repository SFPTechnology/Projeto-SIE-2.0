"""Source aggregate C15: offline, read-only, fail-closed tests."""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[4]
SPEC=importlib.util.spec_from_file_location(
    "c15_source_reconciliation",ROOT/"scripts/c15_source_reconciliation.py"
)
assert SPEC and SPEC.loader
guard=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(guard)


def inventory():
    return {
        "source_project_ref":guard.SOURCE,
        "destination_project_ref":guard.DEST,
        "capture_method":"READ_ONLY_AGGREGATE_SQL",
        "table_counts":dict(guard.BASELINE),
        "operational_columns":99,
        "selected_projects":5,
        "contains_personal_data":False,
        "real_backup_verified":False,
        "real_restore_verified":False,
        "source_cutoff_approved":False,
        "remote_migration_go":False,
        "real_import_go":False,
    }


def test_stable_source_still_blocks_all_real_operations():
    result=guard.assess_source_inventory(inventory())
    assert result["status"]=="STABLE_AGGREGATE_READBACK"
    assert result["source_total_rows"]==1934
    assert result["operational_tables"]==15
    assert result["source_drift"]=={}
    assert result["real_migration_go"] is False
    assert result["remote_ddl_go"] is False
    assert result["gate_gc"]=="BLOCKED"


def test_increased_counts_identify_exact_table_without_approving():
    data=inventory()
    data["table_counts"]["dependencias"]+=1
    result=guard.assess_source_inventory(data)
    assert result["status"]=="DRIFT_REQUIRES_REVIEW"
    assert result["source_total_rows"]==1935
    assert result["source_drift"]["dependencias"]=={"baseline":41,"observed":42}
    assert not result["real_migration_go"]


@pytest.mark.parametrize("field,bad_value",[
    ("source_project_ref","fozrymsidnaxmuvxxfhh"),
    ("destination_project_ref","hlbksclcandbsyqrsbmx"),
    ("capture_method","IMPORTED_UNVERIFIED"),
    ("contains_personal_data",True),
    ("real_backup_verified",True),
    ("remote_migration_go",True),
    ("real_import_go",True),
    ("source_cutoff_approved",True),
    ("real_restore_verified",True),
])
def test_wrong_provenance_or_claimed_go_rejected(field,bad_value):
    data=inventory()
    data[field]=bad_value
    with pytest.raises(ValueError):
        guard.assess_source_inventory(data)


def test_missing_invalid_or_extra_tables_rejected():
    data=inventory()
    data["table_counts"].pop("projetos")
    with pytest.raises(ValueError):
        guard.assess_source_inventory(data)
    data=inventory()
    data["table_counts"]["sie_schema_migrations"]=3
    with pytest.raises(ValueError):
        guard.assess_source_inventory(data)
    data=inventory()
    data["table_counts"]["projetos"]=-1
    with pytest.raises(ValueError):
        guard.assess_source_inventory(data)


def test_columns_and_project_selection_drift_detected():
    data=inventory()
    data["operational_columns"]=100
    data["selected_projects"]=4
    report=guard.assess_source_inventory(data)
    assert set(report["source_drift"])=={"operational_columns","selected_projects"}
    assert report["gate_gc"]=="BLOCKED"


def test_schema_migration_bookkeeping_excluded_from_operational_counts():
    assert "sie_schema_migrations" not in guard.BASELINE
    assert sum(guard.BASELINE.values())==1934
