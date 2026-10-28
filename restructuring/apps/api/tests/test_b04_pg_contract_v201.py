"""B04 PostgreSQL adapter rejects missing migrations and cross-owner results.

No database or Supabase connection. A PostgreSQL integration test must be
repeated after A03/A04 are authorized and applied.
"""
from __future__ import annotations
from uuid import UUID
import pytest
from sie_api.v201_postgres_contract import (
    IntegrationNotReady, read_only_preflight, list_owned_projects, deny_remote_write,
    PROJECT_REF, REQUIRED_MIGRATIONS,
)


class Cursor:
    def __init__(self,conn): self.conn=conn
    def __enter__(self): return self
    def __exit__(self,*args): return False
    def execute(self,sql,parameters=None):
        self.conn.queries.append((sql,parameters))
        self.sql=sql
    def fetchall(self):
        if "supabase_migrations.schema_migrations" in self.sql:
            return [(v,) for v in sorted(self.conn.versions)]
        if "information_schema.columns" in self.sql:
            return [(v,) for v in sorted(self.conn.columns)]
        return self.conn.rows


class Connection:
    def __init__(self,versions=None,rows=None,columns=None):
        self.queries=[]
        self.versions=versions if versions is not None else set(REQUIRED_MIGRATIONS)
        self.columns=columns if columns is not None else {
            "lifecycle_state","base_revision_id","lock_version",
            "idempotency_key","sealed_snapshot","sealed_snapshot_sha256"}
        self.rows=rows or []
    def cursor(self): return Cursor(self)


A=UUID("11111111-1111-4111-8111-111111111111")
B=UUID("22222222-2222-4222-8222-222222222222")


def test_remote_writes_cannot_be_enabled_via_adapter():
    with pytest.raises(IntegrationNotReady):
        deny_remote_write()


def test_wrong_supabase_project_rejected_without_sql():
    conn=Connection()
    with pytest.raises(IntegrationNotReady):
        read_only_preflight(conn,"wrong-project")
    assert conn.queries==[]


def test_missing_a03_a04_blocks_remote_read():
    conn=Connection(versions={"20261027195557"})
    result=read_only_preflight(conn,PROJECT_REF)
    assert not result.ready
    assert set(result.missing)=={"20261028102000","20261028102100"}
    with pytest.raises(IntegrationNotReady):
        list_owned_projects(conn,PROJECT_REF,A)


def test_missing_revision_columns_blocks_remote_read():
    conn=Connection(columns={"version","id"})
    with pytest.raises(IntegrationNotReady):
        list_owned_projects(conn,PROJECT_REF,A)


def test_owner_filtered_read_is_parameterized():
    conn=Connection(rows=[(str(A),str(A),"Projeto A","2026-10-28")])
    result=list_owned_projects(conn,PROJECT_REF,A)
    assert len(result)==1
    query,parameters=conn.queries[-1]
    assert "WHERE owner_id=%s" in query
    assert parameters==(str(A),100)
    assert str(A) not in query


def test_adapter_detects_cross_owner_even_when_db_returns_wrong_row():
    conn=Connection(rows=[(str(A),str(B),"Projeto B","2026-10-28")])
    with pytest.raises(IntegrationNotReady):
        list_owned_projects(conn,PROJECT_REF,A)
