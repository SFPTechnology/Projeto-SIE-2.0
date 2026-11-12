"""C22 static guardrails for disposable PG17 migration evidence.

This prevents the C20 test from silently gaining a remote connection input.
It is a source-level contract; C20 remains the transactional execution test.
"""
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SOURCE = ROOT / "restructuring/apps/api/tests/test_c20_migration_atomicity_pg17_v201.py"


def test_c20_pg17_evidence_is_explicitly_disposable_and_local_only():
    text = SOURCE.read_text(encoding="utf-8")
    assert 'SIE_PG17_DISPOSABLE_TEST") != "1"' in text
    assert 'host=localhost port=5432' in text
    assert 'DATABASE_URL", "SUPABASE_DB_URL", "SUPABASE_ACCESS_TOKEN", "SUPABASE_SERVICE_ROLE_KEY"' in text
    assert "assert 170000 <= int(admin.info.server_version) < 180000" in text
    assert 'CREATE DATABASE {}' in text
    assert 'DROP DATABASE {}' in text


def test_c20_covers_each_pending_migration_and_failed_transaction():
    text = SOURCE.read_text(encoding="utf-8")
    for version in ("20261028102000", "20261028102100", "20261028153000", "20261028203000"):
        assert version in text
    assert "pytest.mark.parametrize" in text
    assert "DivisionByZero" in text
    assert "snapshot(baseline) == before" in text
    assert "for version in VERSIONS:" in text
