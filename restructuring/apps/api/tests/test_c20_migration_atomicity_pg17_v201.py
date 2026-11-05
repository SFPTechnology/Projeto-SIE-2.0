"""Synthetic PG17 rollback evidence; never a remote recovery certificate.

Uses a separate fixed-name CI database, retaining GF02 rows, grants, policies
and definitions across an injected failure after each pending migration.
"""
from __future__ import annotations

import os
from pathlib import Path

import pytest

pytestmark = pytest.mark.skipif(
    os.environ.get("SIE_PG17_DISPOSABLE_TEST") != "1",
    reason="requires isolated PostgreSQL 17 GitHub Actions service",
)
ROOT = Path(__file__).resolve().parents[4]
MIGRATIONS = ROOT / "restructuring/supabase/migrations"
VERSIONS = ("20261028102000", "20261028102100", "20261028153000", "20261028203000")
DATABASE = "sie2_c20_atomicity_ci"
DSN = "host=localhost port=5432 user=postgres password=postgres_ci_only connect_timeout=5"


def migration(version):
    files = list(MIGRATIONS.glob(f"{version}_*.sql"))
    assert len(files) == 1
    return files[0].read_text()


@pytest.fixture
def baseline():
    import psycopg
    from psycopg import sql

    # No URI/env connection string is accepted; no remote address is usable.
    assert os.environ.get("PGHOST") in (None, "localhost", "127.0.0.1")
    assert not any(os.environ.get(key) for key in (
        "DATABASE_URL", "SUPABASE_DB_URL", "SUPABASE_ACCESS_TOKEN", "SUPABASE_SERVICE_ROLE_KEY",
    ))
    with psycopg.connect(DSN + " dbname=postgres", autocommit=True) as admin:
        assert 170000 <= int(admin.info.server_version) < 180000
        # Refuse to reuse or delete a preexisting DB. Cleanup belongs only to
        # the successful CREATE below, so another process cannot lose its DB.
        admin.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(DATABASE)))
        try:
            with psycopg.connect(DSN + f" dbname={DATABASE}", autocommit=True) as conn:
                conn.execute("""
                    CREATE SCHEMA auth;
                    CREATE TABLE auth.users(id uuid PRIMARY KEY);
                    CREATE FUNCTION auth.uid() RETURNS uuid LANGUAGE sql STABLE
                    AS $$ SELECT nullif(current_setting('request.jwt.claim.sub', true), '')::uuid $$;
                    GRANT USAGE ON SCHEMA auth, public TO authenticated, service_role;
                    GRANT EXECUTE ON FUNCTION auth.uid() TO authenticated, service_role;
                """)
                conn.execute(migration("20261027195557"))
                conn.execute("""
                    INSERT INTO auth.users VALUES ('11111111-1111-4111-8111-111111111111');
                    INSERT INTO public.sie_projects(id,owner_id,name) VALUES
                    ('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
                     '11111111-1111-4111-8111-111111111111','GF02 preserved');
                    INSERT INTO public.sie_project_revisions(id,project_id,version,created_by) VALUES
                    ('cccccccc-cccc-4ccc-8ccc-cccccccccccc',
                     'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',1,
                     '11111111-1111-4111-8111-111111111111');
                """)
                yield conn
        finally:
            admin.execute(sql.SQL("DROP DATABASE {}").format(sql.Identifier(DATABASE)))


def snapshot(conn):
    """Definitions and privileges as well as retained data, not just counts."""
    queries = {
        "columns": "SELECT table_name,column_name,ordinal_position,data_type,is_nullable,column_default FROM information_schema.columns WHERE table_schema='public' ORDER BY 1,3",
        "constraints": "SELECT c.relname,x.conname,pg_get_constraintdef(x.oid) FROM pg_constraint x JOIN pg_class c ON c.oid=x.conrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='public' ORDER BY 1,2",
        "indexes": "SELECT tablename,indexname,indexdef FROM pg_indexes WHERE schemaname='public' ORDER BY 1,2",
        "policies": "SELECT * FROM pg_policies WHERE schemaname='public' ORDER BY tablename,policyname",
        "table_security": "SELECT c.relname,c.relrowsecurity,c.relforcerowsecurity,c.relacl::text FROM pg_class c JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='public' ORDER BY 1",
        "column_grants": "SELECT table_name,column_name,grantee,privilege_type,is_grantable FROM information_schema.column_privileges WHERE table_schema='public' ORDER BY 1,2,3,4",
        "functions": "SELECT p.proname,pg_get_functiondef(p.oid),p.proacl::text FROM pg_proc p JOIN pg_namespace n ON n.oid=p.pronamespace WHERE n.nspname='public' ORDER BY 1,2",
        "triggers": "SELECT c.relname,t.tgname,pg_get_triggerdef(t.oid) FROM pg_trigger t JOIN pg_class c ON c.oid=t.tgrelid JOIN pg_namespace n ON n.oid=c.relnamespace WHERE n.nspname='public' AND NOT t.tgisinternal ORDER BY 1,2",
        "users": "SELECT * FROM auth.users ORDER BY id",
        "projects": "SELECT * FROM public.sie_projects ORDER BY id",
        "revisions": "SELECT * FROM public.sie_project_revisions ORDER BY id",
    }
    return {name: conn.execute(query).fetchall() for name, query in queries.items()}


@pytest.mark.parametrize("failure_after", range(1, 5), ids=("A03", "A04", "B04", "C03"))
def test_failure_rolls_back_entire_bundle_and_allows_clean_retry(baseline, failure_after):
    import psycopg

    before = snapshot(baseline)
    with pytest.raises(psycopg.errors.DivisionByZero):
        with baseline.transaction():
            for version in VERSIONS[:failure_after]:
                baseline.execute(migration(version))
            baseline.execute("SELECT 1/0")
    assert snapshot(baseline) == before

    # Failed attempt must leave no partial columns/indexes/grants that prevent
    # a complete retry; existing GF02 data survives the successful upgrade.
    with baseline.transaction():
        for version in VERSIONS:
            baseline.execute(migration(version))
    assert baseline.execute("SELECT name,idempotency_key FROM public.sie_projects").fetchall() == [("GF02 preserved", None)]
    assert baseline.execute("SELECT lifecycle_state,lock_version FROM public.sie_project_revisions").fetchall() == [("DRAFT", 0)]
    assert baseline.execute("SELECT count(*) FROM pg_tables WHERE schemaname='public'").fetchone()[0] == 19
