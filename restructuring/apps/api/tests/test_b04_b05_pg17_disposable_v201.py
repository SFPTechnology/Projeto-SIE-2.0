"""Integration suite. Run ONLY in .github/workflows/sie-b04-b05-pg17.yml.

Disposable database: postgres 17 GF02+A03+A04, synthetic auth.users, NO remote
Supabase, credentials from CI service. This module is skipped by regular pytest.
"""
from __future__ import annotations
import os
import uuid

import pytest
from sie_api.v201_pg_dev_adapter import Pg17DisposableAdapter, PgConflict, PgMissing
from sie_api.v201_postgres_contract import IntegrationNotReady

pytestmark=pytest.mark.skipif(
    os.environ.get("SIE_PG17_DISPOSABLE_TEST")!="1",
    reason="only disposable PostgreSQL 17 GitHub Actions test service"
)

A=uuid.UUID("11111111-1111-4111-8111-111111111111")
B=uuid.UUID("22222222-2222-4222-8222-222222222222")

@pytest.fixture
def conn():
    import psycopg
    db=psycopg.connect(
        "host=localhost port=5432 dbname=sie2_gf02_ci "
        "user=postgres password=postgres_ci_only connect_timeout=5",
        autocommit=True
    )
    try:
        yield db
    finally:
        db.close()


def test_disposable_pg17_clone_and_bundle_atomically(conn):
    adapter=Pg17DisposableAdapter(conn)
    project=adapter.create_project(A,"B05 PostgreSQL 17 fixture","create-b05-fixture-01")["id"]
    rev=adapter.create_revision(A,project,"idempotency-rev1")
    assert rev["replayed"] is False
    assert adapter.create_revision(A,project,"idempotency-rev1")["id"]==rev["id"]
    with pytest.raises(PgConflict):
        adapter.create_revision(A,project,"idempotency-rev2")
    bundle={
        "rooms":[
            {"ref":"sala","name":"Sala","width_m":"4.0000","length_m":"5.0000"},
            {"ref":"cozinha","name":"Cozinha","width_m":"3.0000","length_m":"3.0000"}],
        "circuits":[
            {"ref":"c1","code":"C1","nominal_voltage_v":"127.000"},
            {"ref":"c2","code":"C2","nominal_voltage_v":"220.000"}],
        "loads":[
            {"ref":"l1","room_ref":"sala","label":"Lampada","kind":"LIGHTING",
             "apparent_power_va":"120.000"},
            {"ref":"l2","room_ref":"sala","label":"Tomada sala","kind":"TUG",
             "apparent_power_va":"250.000"},
            {"ref":"l3","room_ref":"cozinha","label":"Tomada cozinha","kind":"TUG",
             "apparent_power_va":"650.000"}],
        "links":[
            {"circuit_ref":"c1","load_ref":"l1"},
            {"circuit_ref":"c1","load_ref":"l2"},
            {"circuit_ref":"c2","load_ref":"l3"}],
    }
    assert adapter.add_bundle(A,project,rev["id"],bundle)=={
        "rooms":2,"loads":3,"circuits":2,"links":3}
    with conn.cursor() as cur:
        cur.execute("""SELECT COUNT(*) FROM public.sie_circuit_loads
            WHERE project_id=%s AND revision_id=%s""",(project,rev["id"]))
        assert cur.fetchone()[0]==3
    with pytest.raises(PgMissing):
        adapter.add_bundle(B,project,rev["id"],bundle)
    with pytest.raises(PgMissing):
        adapter.seal(B,project,rev["id"],0)
    sealed=adapter.seal(A,project,rev["id"],0)
    assert sealed["state"]=="SEALED" and sealed["lock_version"]==1
    assert len(sealed["snapshot_sha256"])==64
    with pytest.raises(PgConflict):
        adapter.create_revision(A,project,"idempotency-rev1",uuid.uuid4())
    with pytest.raises(Exception):
        adapter.seal(A,project,rev["id"],0)
    clone=adapter.create_revision(A,project,"idempotency-rev2",rev["id"])
    assert clone["version"]==2
    assert clone["replayed"] is False
    assert adapter.create_revision(A,project,"idempotency-rev2",rev["id"])["replayed"] is True
    with conn.cursor() as cur:
        for table,count in (("sie_rooms",2),("sie_loads",3),
                            ("sie_circuits",2),("sie_circuit_loads",3)):
            cur.execute(f"""SELECT COUNT(*) FROM public.{table}
                        WHERE project_id=%s AND revision_id=%s""",
                        (project,clone["id"]))
            assert cur.fetchone()[0]==count
        cur.execute("""SELECT COUNT(*) FROM public.sie_loads l
            JOIN public.sie_rooms r
            ON r.id=l.room_id AND r.revision_id=l.revision_id
            WHERE l.project_id=%s AND l.revision_id=%s""",(project,clone["id"]))
        assert cur.fetchone()[0]==3


def test_disposable_pg17_batch_rollback(conn):
    adapter=Pg17DisposableAdapter(conn)
    pid=adapter.create_project(A,"B05 rollback","create-b05-rollback")["id"]
    rid=adapter.create_revision(A,pid,"rollback-key-1")["id"]
    invalid={
        "rooms":[{"ref":"s1","name":"Sala","width_m":"4.0000","length_m":"5.0000"}],
        "circuits":[{"ref":"c1","code":"C1","nominal_voltage_v":"127.000"}],
        "loads":[{"ref":"l1","room_ref":"s1","label":"TUG","kind":"TUG",
                  "apparent_power_va":"200.000"}],
        "links":[{"circuit_ref":"c1","load_ref":"wrong"}],
    }
    with pytest.raises(PgConflict):
        adapter.add_bundle(A,pid,rid,invalid)
    with conn.cursor() as cur:
        cur.execute("SELECT count(*) FROM public.sie_rooms WHERE project_id=%s",(pid,))
        assert cur.fetchone()[0]==0
    assert adapter.add_bundle(A,pid,rid,{
        "rooms":[],"loads":[],"circuits":[],"links":[]
    })=={"rooms":0,"loads":0,"circuits":0,"links":0}


def test_disposable_pg17_rejects_non_disposable_targets(conn):
    from unittest.mock import Mock
    for host in ("fozrymsidnaxmuvxxfhh.supabase.co","10.0.0.1"):
        fake=Mock()
        fake.info.host=host
        fake.info.dbname="sie2_gf02_ci"
        fake.autocommit=True
        with pytest.raises(IntegrationNotReady):
            Pg17DisposableAdapter(fake)
    fake=Mock()
    fake.info.host="localhost"
    fake.info.dbname="production"
    fake.autocommit=True
    with pytest.raises(IntegrationNotReady):
        Pg17DisposableAdapter(fake)



def test_disposable_pg17_draft_edits_and_fk_protected_deletions(conn):
    import psycopg
    adapter=Pg17DisposableAdapter(conn)
    project=adapter.create_project(A,"B05 edit-delete PG","create-b05-edit-01")["id"]
    revision=adapter.create_revision(A,project,"revision-edit-01")["id"]
    adapter.add_bundle(A,project,revision,{
        "rooms":[{"ref":"r","name":"Sala","width_m":"4.0000","length_m":"5.0000"}],
        "circuits":[{"ref":"c","code":"C1","nominal_voltage_v":"127.000"}],
        "loads":[{"ref":"l","room_ref":"r","label":"TUG","kind":"TUG",
                  "apparent_power_va":"100.000"}],
        "links":[{"load_ref":"l","circuit_ref":"c"}],
    })
    ids={}
    with conn.cursor() as cur:
        for table in ("sie_rooms","sie_loads","sie_circuits","sie_circuit_loads"):
            cur.execute(f"""SELECT id FROM public.{table}
                           WHERE project_id=%s AND revision_id=%s""",
                        (project,revision))
            ids[table]=cur.fetchone()[0]
    updated=adapter.edit_entity(A,project,revision,"rooms",ids["sie_rooms"],
                                {"name":"Sala alterada"},0)
    assert updated["revision_lock_version"]==1
    with pytest.raises(PgConflict):
        adapter.edit_entity(A,project,revision,"rooms",ids["sie_rooms"],
                            {"name":"Replay obsoleto"},0)
    with pytest.raises(ValueError):
        adapter.edit_entity(A,project,revision,"rooms",ids["sie_rooms"],
                            {"owner_id":str(B)},1)
    with pytest.raises(PgMissing):
        adapter.edit_entity(B,project,revision,"rooms",ids["sie_rooms"],
                            {"name":"Cross-owner"},1)
    with pytest.raises(psycopg.errors.ForeignKeyViolation):
        adapter.delete_entity(A,project,revision,"rooms",ids["sie_rooms"],1)
    # A failed deletion rolls back and preserves the lock.
    assert adapter.delete_entity(A,project,revision,"links",ids["sie_circuit_loads"],1)[
        "revision_lock_version"]==2
    assert adapter.delete_entity(A,project,revision,"loads",ids["sie_loads"],2)[
        "revision_lock_version"]==3
    assert adapter.delete_entity(A,project,revision,"rooms",ids["sie_rooms"],3)[
        "revision_lock_version"]==4
    assert adapter.delete_entity(A,project,revision,"circuits",ids["sie_circuits"],4)[
        "revision_lock_version"]==5
    assert adapter.seal(A,project,revision,5)["state"]=="SEALED"
    with pytest.raises(PgConflict):
        adapter.edit_entity(A,project,revision,"circuits",ids["sie_circuits"],
                            {"code":"TAMPER"},6)

def test_project_idempotency_persists_across_retries_and_is_owner_scoped(conn):
    adapter=Pg17DisposableAdapter(conn)
    key="project-same-key-2026"
    a=adapter.create_project(A,"Projeto idempotente",key)
    retry=adapter.create_project(A,"Projeto idempotente",key)
    assert a["id"]==retry["id"]
    assert a["replayed"] is False and retry["replayed"] is True
    with pytest.raises(PgConflict):
        adapter.create_project(A,"Payload diferente",key)
    owner_b=adapter.create_project(B,"Projeto idempotente",key)
    assert owner_b["id"]!=a["id"] and not owner_b["replayed"]
    # Identity and retry fingerprint remain immutable despite project renaming.
    with conn.cursor() as cur:
        cur.execute("UPDATE public.sie_projects SET name=%s WHERE id=%s",
                    ("Projeto renomeado",a["id"]))
        cur.execute("SELECT request_fingerprint_sha256 FROM public.sie_projects WHERE id=%s",
                    (a["id"],))
        assert len(cur.fetchone()[0])==64
    again=adapter.create_project(A,"Projeto idempotente",key)
    assert again["id"]==a["id"] and again["replayed"] is True
    with pytest.raises(PgConflict):
        adapter.create_project(A,"Projeto renomeado",key)


def test_b04_project_immutable_owner_and_request_identity(conn):
    import psycopg
    adapter=Pg17DisposableAdapter(conn)
    p=adapter.create_project(A,"Projeto protegido","project-guard-key-1")["id"]
    with conn.cursor() as cur:
        with pytest.raises(psycopg.errors.CheckViolation):
            cur.execute("UPDATE public.sie_projects SET owner_id=%s WHERE id=%s",
                        (B,p))
        with pytest.raises(psycopg.errors.CheckViolation):
            cur.execute("UPDATE public.sie_projects SET idempotency_key=%s WHERE id=%s",
                        ("changed-key",p))
        cur.execute("SELECT owner_id FROM public.sie_projects WHERE id=%s",(p,))
        assert cur.fetchone()[0]==A


def test_b04_b05_role_permissions_minimum(conn):
    with conn.cursor() as cur:
        for table in ("sie_rooms","sie_loads","sie_circuits","sie_circuit_loads"):
            cur.execute("SELECT has_table_privilege('authenticated',%s,'DELETE')",
                        ("public."+table,))
            assert cur.fetchone()[0] is False
            cur.execute("SELECT has_table_privilege('service_role',%s,'DELETE')",
                        ("public."+table,))
            assert cur.fetchone()[0] is True
        cur.execute("SELECT has_column_privilege('service_role','public.sie_projects','owner_id','UPDATE')")
        assert cur.fetchone()[0] is False
        cur.execute("SELECT has_column_privilege('service_role','public.sie_projects','name','UPDATE')")
        assert cur.fetchone()[0] is True
        cur.execute("SELECT has_column_privilege('authenticated','public.sie_rooms','name','UPDATE')")
        assert cur.fetchone()[0] is False


def test_b04_b05_actual_pg_role_a_b_and_backend_dml(conn):
    import psycopg
    adapter=Pg17DisposableAdapter(conn)
    pid=adapter.create_project(A,"A/B protected PG17","owner-a-fixture-key")["id"]
    rid=adapter.create_revision(A,pid,"a-b-revision-key")["id"]
    adapter.add_bundle(A,pid,rid,{
        "rooms":[{"ref":"room","name":"Comodo A","width_m":"2.0000","length_m":"3.0000"}],
        "loads":[],"circuits":[],"links":[]
    })
    with conn.cursor() as cur:
        cur.execute("SELECT id FROM public.sie_rooms WHERE project_id=%s",(pid,))
        room_id=cur.fetchone()[0]
    with conn.cursor() as cur:
        try:
            cur.execute("SET ROLE authenticated")
            cur.execute("SET request.jwt.claim.sub = %s",(str(A),))
            cur.execute("SELECT COUNT(*) FROM public.sie_projects WHERE id=%s",(pid,))
            assert cur.fetchone()[0]==1
            cur.execute("SET request.jwt.claim.sub = %s",(str(B),))
            cur.execute("SELECT COUNT(*) FROM public.sie_projects WHERE id=%s",(pid,))
            assert cur.fetchone()[0]==0
            with pytest.raises(psycopg.errors.InsufficientPrivilege):
                cur.execute("DELETE FROM public.sie_rooms WHERE id=%s",(room_id,))
            cur.execute("RESET ROLE")
            cur.execute("RESET request.jwt.claim.sub")
            cur.execute("SET ROLE service_role")
            # No user-supplied owner_id or JWT role enters this privileged write.
            cur.execute("UPDATE public.sie_rooms SET name=%s WHERE id=%s",
                        ("Editado pelo backend",room_id))
            assert cur.rowcount==1
            with pytest.raises(psycopg.errors.InsufficientPrivilege):
                cur.execute("UPDATE public.sie_projects SET owner_id=%s WHERE id=%s",
                            (B,pid))
        finally:
            cur.execute("RESET ROLE")
            cur.execute("RESET request.jwt.claim.sub")
    with conn.cursor() as cur:
        cur.execute("SELECT name FROM public.sie_rooms WHERE id=%s",(room_id,))
        assert cur.fetchone()[0]=="Editado pelo backend"
