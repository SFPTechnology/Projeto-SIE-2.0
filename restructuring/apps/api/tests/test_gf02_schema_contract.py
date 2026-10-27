"""Contract/static review for the GF02 SQL migration candidate (no external DB needed)."""
from pathlib import Path
import re
import pytest

ROOT = Path(__file__).resolve().parents[4]
SOURCE = ROOT / "docs/implantacao-sie-2-0/GREENFIELD/GF02_SCHEMA_CANDIDATE.sql"
SQL = SOURCE.read_text(encoding="utf-8")
TABLES = (
    "sie_projects", "sie_project_revisions", "sie_rooms", "sie_loads",
    "sie_circuits", "sie_circuit_loads", "sie_calculation_runs",
    "sie_artifacts", "sie_audit_events",
)
CLIENT_INSERT = (
    "sie_projects", "sie_project_revisions", "sie_rooms",
    "sie_loads", "sie_circuits", "sie_circuit_loads",
)
SERVER_ONLY = ("sie_calculation_runs", "sie_artifacts", "sie_audit_events")


@pytest.mark.parametrize("table", TABLES)
def test_rls_and_select_owner_policy(table):
    assert f"CREATE TABLE public.{table} (" in SQL
    assert f"ALTER TABLE public.{table} ENABLE ROW LEVEL SECURITY;" in SQL
    assert f"REVOKE ALL ON TABLE public.{table} FROM PUBLIC, anon, authenticated;" in SQL
    assert f"GRANT SELECT ON TABLE public.{table} TO authenticated;" in SQL
    assert f"CREATE POLICY {table}_owner_select ON public.{table}" in SQL


@pytest.mark.parametrize("table", CLIENT_INSERT)
def test_client_insert_requires_owner_policy(table):
    assert f"GRANT INSERT (" in SQL
    assert f" ON TABLE public.{table} TO authenticated;" in SQL
    assert f"CREATE POLICY {table}_owner_insert ON public.{table}" in SQL


@pytest.mark.parametrize("table", SERVER_ONLY)
def test_machine_outputs_not_writable_by_client(table):
    assert f"CREATE POLICY {table}_owner_insert" not in SQL
    assert not re.search(rf"GRANT\s+INSERT\b[^;]*\bpublic\.{table}\b", SQL)


def test_not_authored_as_a_legacy_schema():
    assert "CREATE TABLE public.projetos " not in SQL
    assert "DROP TABLE" not in SQL.upper()
    assert "TRUNCATE " not in SQL.upper()
    assert "ON DELETE CASCADE" not in SQL.upper()


def test_owner_id_never_derived_from_user_metadata():
    assert "raw_user_meta_data" not in SQL
    assert "auth.uid()" in SQL
    assert "owner_id uuid NOT NULL DEFAULT auth.uid()" in SQL


def test_relationships_keep_project_and_revision_in_same_scope():
    for item in (
        "FOREIGN KEY (revision_id, project_id)",
        "FOREIGN KEY (room_id, project_id, revision_id)",
        "FOREIGN KEY (circuit_id, project_id, revision_id)",
        "FOREIGN KEY (load_id, project_id, revision_id)",
        "FOREIGN KEY (calculation_run_id, project_id, revision_id)",
    ):
        assert item in SQL


def test_no_anonymous_grants_or_unrestricted_policies():
    assert not re.search(r"GRANT\s+.+\s+TO\s+anon\s*;", SQL, re.IGNORECASE)
    assert not re.search(r"CREATE POLICY[\s\S]*?TO anon", SQL, re.IGNORECASE)
    assert "USING (true)" not in SQL.lower()
    assert "WITH CHECK (true)" not in SQL.lower()


def test_no_client_update_except_project_name():
    updates = re.findall(r"GRANT UPDATE\s*\(([^)]+)\)\s*ON TABLE\s+public\.(\w+)\s+TO authenticated;", SQL)
    assert updates == [("name", "sie_projects")]
    assert "GRANT DELETE" not in SQL.upper()


def test_normative_run_status_does_not_pretend_approval():
    assert "NOT_EVALUATED" in SQL
    assert "'PUBLISHED'" not in SQL
    assert "APPROVED" not in SQL
