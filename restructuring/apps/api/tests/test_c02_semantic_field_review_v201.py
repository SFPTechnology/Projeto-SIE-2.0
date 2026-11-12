"""C02: verify exactly all 45 fields; no normative promotion by JSON/CSV."""
import csv
from io import StringIO
from pathlib import Path
import pytest
from sie_api.v201_c_field_review import verify_field_review

BASE=Path(__file__).resolve().parents[4]/"docs/implantacao-sie-2-0/GREENFIELD"
def source():
    return (BASE/"C02_MATRIZ_COMPLETA_OPERACIONAL_V201.csv").read_text(encoding="utf-8")
def review():
    return (BASE/"C02_REVISAO_SEMANTICA_45_CAMPOS_V201.csv").read_text(encoding="utf-8")
def encode(rows):
    sink=StringIO()
    writer=csv.DictWriter(sink,fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
    return sink.getvalue()

def test_exhaustive_mapping_with_pending_engineering():
    result=verify_field_review(source(),review())
    assert result["scope"]=="45_OF_45_FIELDS_CLASSIFIED"
    assert result["source_inventory"]=="99_OF_99_COLUMNS_TRACKED"
    assert result["distribution"]=={
       "SOURCE_ONLY_NO_INFER":15,"PROFESSIONAL_REVIEW_REQUIRED":7,
       "ZERO_ROWS_ARCHIVE_CONTRACT":22,"SCHEMA_AND_USER_REVIEW_REQUIRED":1}
    assert result["professional_signoff_approved"] is False
    assert result["live_import_authorized"] is False
    assert result["gate_gc"]=="BLOCKED"

def test_invented_or_duplicate_field_rejected():
    rows=list(csv.DictReader(StringIO(review())))
    rows[0]["legacy_column"]="no_such_column"
    with pytest.raises(ValueError):
        verify_field_review(source(),encode(rows))
    rows=list(csv.DictReader(StringIO(review())))
    rows[1]["legacy_table"]=rows[0]["legacy_table"]
    rows[1]["legacy_column"]=rows[0]["legacy_column"]
    with pytest.raises(ValueError):
        verify_field_review(source(),encode(rows))

def test_no_fake_signoff_or_invalid_zero_row_claim():
    rows=list(csv.DictReader(StringIO(review())))
    n=next(x for x in rows if x["decision"]=="PROFESSIONAL_REVIEW_REQUIRED")
    n["status"]="APPROVED"
    with pytest.raises(ValueError):
        verify_field_review(source(),encode(rows))
    rows=list(csv.DictReader(StringIO(review())))
    n=next(x for x in rows if x["decision"]=="ZERO_ROWS_ARCHIVE_CONTRACT")
    n["rows_at_readback"]="3"
    with pytest.raises(ValueError):
        verify_field_review(source(),encode(rows))

def test_source_schema_drift_rejected():
    src=source().replace('"QUARANTINE_UNMAPPED"','"DIRECT"')
    with pytest.raises(ValueError):
        verify_field_review(src,review())
