"""C07: enforce real-source selection as a no-write, no-approval plan."""
from pathlib import Path
from copy import deepcopy
import json
import pytest
from sie_api.v201_c_migration_preflight import verify_selection

BASE=Path(__file__).resolve().parents[4]/"docs/implantacao-sie-2-0/GREENFIELD"

def selection():
    return json.loads((BASE/"C01_C07_SELECTION_ALL_FIVE_V201.json").read_text(encoding="utf-8"))

def matrix():
    return (BASE/"C02_MATRIZ_COMPLETA_OPERACIONAL_V201.csv").read_text(encoding="utf-8")

def test_all_five_projects_and_all_columns_are_explicitly_covered():
    report=verify_selection(selection(),matrix())
    assert report["scope"]=="ALL_FIVE_LEGACY_PROJECTS"
    assert report["user_intent"]=="CONFIRMED"
    assert report["selection_integrity"]=="PASS"
    assert report["source_project_count"]==5
    assert report["source_room_count"]==41
    assert report["source_additional_load_count"]==52
    assert report["mapped_column_count"]==99
    assert report["source_table_count"]==15
    assert report["review_or_quarantine_column_count"]>=45
    assert report["target_auth_verified"] is False
    assert report["real_import_authorized"] is False
    assert report["gate_gc"]=="BLOCKED"
    assert len(report["matrix_sha256"])==64

def test_remote_or_production_go_cannot_be_conferred_by_manifest():
    for key in ("real_import_authorized","remote_ddl_authorized",
                "production_deploy_authorized","main_or_f12_write_authorized"):
        altered=selection()
        altered["release"][key]=True
        with pytest.raises(ValueError):
            verify_selection(altered,matrix())

def test_partial_selection_and_duplicate_sources_are_rejected():
    altered=selection()
    altered["projects"].pop()
    with pytest.raises(ValueError):
        verify_selection(altered,matrix())
    altered=selection()
    altered["projects"][1]["legacy_id"]=altered["projects"][0]["legacy_id"]
    with pytest.raises(ValueError):
        verify_selection(altered,matrix())
    altered=selection()
    altered["projects"][1]["selection"]="SKIP"
    with pytest.raises(ValueError):
        verify_selection(altered,matrix())

def test_wrong_source_and_inconsistent_totals_are_rejected():
    altered=selection()
    altered["source"]["project_ref"]="unknown"
    with pytest.raises(ValueError):
        verify_selection(altered,matrix())
    altered=selection()
    altered["projects"][0]["rooms"]+=1
    with pytest.raises(ValueError):
        verify_selection(altered,matrix())

def test_malformed_matrix_and_duplicates_rejected():
    with pytest.raises(ValueError):
        verify_selection(selection(),matrix()+"\n"+"x,y,z,w,q,t\n")
    with pytest.raises(ValueError):
        verify_selection(selection(),matrix().replace('"QUARANTINE_UNMAPPED"','"MIGRATE_NOW"'))
    with pytest.raises(ValueError):
        verify_selection(selection(),"legacy_table,legacy_column\na,b\n")

def test_target_uuid_not_authorization_even_if_syntactically_valid():
    altered=selection()
    altered["destination"]["target_auth_user_id"]="11111111-1111-4111-8111-111111111111"
    report=verify_selection(altered,matrix())
    assert report["target_auth_verified"] is False
    assert report["real_import_authorized"] is False
    altered["destination"]["target_auth_user_id"]="not-a-uuid"
    with pytest.raises(ValueError):
        verify_selection(altered,matrix())
