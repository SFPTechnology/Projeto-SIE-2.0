"""C01 source cutoff: changed payload with same row count still blocks release."""
from pathlib import Path
import json
from copy import deepcopy
import pytest
from sie_api.v201_c_source_cutoff import TABLES,fingerprint_sql,compare_readbacks

P=Path(__file__).resolve().parents[4]/"docs/implantacao-sie-2-0/GREENFIELD/C01_SOURCE_FULL_PAYLOAD_FINGERPRINT_V201.json"

def baseline():
    return json.loads(P.read_text(encoding="utf-8"))

def test_read_only_pg17_fingerprint_and_reconciliation():
    sql=fingerprint_sql()
    assert sql.count("SELECT '")==len(TABLES)
    assert sql.count("UNION ALL")==len(TABLES)-1
    assert sql.count("public.")==len(TABLES)
    assert all(term not in sql.upper() for term in ("INSERT INTO","UPDATE ","DELETE FROM","DROP TABLE","TRUNCATE "))
    result=compare_readbacks(baseline(),baseline())
    assert result["drift_state"]=="PASS_SAME_OBSERVATION"
    assert result["compared_tables"]==15
    assert result["changed_tables"]==[]
    assert result["real_import_authorized"] is False
    assert result["source_backup_verified"] is False
    assert baseline()["total_rows"]==1934

def test_same_row_count_changed_payload_is_blocked():
    actual=deepcopy(baseline())
    actual["tables"][0]["rows_sha256"]="f"*64
    result=compare_readbacks(baseline(),actual)
    assert result["drift_state"]=="BLOCKED_CHANGED_SOURCE"
    assert result["changed_tables"][0]["table"]=="projetos"
    assert result["changed_tables"][0]["payload_changed"] is True

def test_count_changed_and_mathematically_consistent_still_blocked():
    actual=deepcopy(baseline())
    actual["tables"][0]["count_rows"]+=1
    actual["total_rows"]+=1
    result=compare_readbacks(baseline(),actual)
    assert result["drift_state"]=="BLOCKED_CHANGED_SOURCE"

def test_partial_or_forged_report_rejected():
    changed=baseline()
    changed["tables"].pop()
    with pytest.raises(ValueError):
        compare_readbacks(baseline(),changed)
    changed=baseline()
    changed["source_project_ref"]="wrong"
    with pytest.raises(ValueError):
        compare_readbacks(baseline(),changed)
    changed=baseline()
    changed["tables"][1]["rows_sha256"]="not a hash"
    with pytest.raises(ValueError):
        compare_readbacks(baseline(),changed)
