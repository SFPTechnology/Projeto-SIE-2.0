"""B04/B05/B03b — real SQLite transactions, FastAPI routes, negative A/B fixtures.

The DEV adapter is NOT Supabase RLS. It is not authorized for remote deployment.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
import json
import sqlite3
import time
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from sie_api.auth_boundary_v201 import AuthIdentity, current_identity
from sie_api.main import app
from sie_api.v201_dev_store import DevStore, Conflict

A = UUID("11111111-1111-4111-8111-111111111111")
B = UUID("22222222-2222-4222-8222-222222222222")


@pytest.fixture
def env(tmp_path, monkeypatch):
    path = tmp_path / "dev_v201.sqlite3"
    monkeypatch.setenv("SIE_ENV", "test")
    monkeypatch.setenv("SIE_V201_DEV_WRITES", "1")
    monkeypatch.setenv("SIE_V201_DEV_DB_PATH", str(path))
    old = dict(app.dependency_overrides)
    app.dependency_overrides[current_identity] = lambda: AuthIdentity(A, int(time.time())+600)
    try:
        yield TestClient(app), path
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(old)


def post(c, path, data, key=None):
    headers={"Idempotency-Key":key} if key else None
    return c.post("/api/v2/sie/dev"+path, json=data, headers=headers)


def create(c, name="Obra A", key="project-key-001"):
    r=post(c,"/projects",{"name":name},key)
    assert r.status_code==201, r.text
    return r.json()["id"]


def revision(c,p,key="revision-key-001",base=None):
    r=post(c,f"/projects/{p}/revisions",{"base_revision_id":base},key)
    assert r.status_code==201, r.text
    return r.json()["id"]


def test_dev_api_is_disabled_in_production_even_with_flag(env,monkeypatch):
    c,_=env
    monkeypatch.setenv("SIE_ENV","production")
    assert post(c,"/projects",{"name":"x"},"project-key").status_code==503


def test_dev_api_requires_explicit_flag_and_path(env,monkeypatch):
    c,_=env
    monkeypatch.delenv("SIE_V201_DEV_WRITES")
    assert post(c,"/projects",{"name":"x"},"project-key").status_code==503
    monkeypatch.setenv("SIE_V201_DEV_WRITES","1")
    monkeypatch.delenv("SIE_V201_DEV_DB_PATH")
    assert post(c,"/projects",{"name":"x"},"project-key").status_code==503


def test_no_authenticated_session_fails_before_write(env):
    c,path=env
    app.dependency_overrides.pop(current_identity,None)
    assert post(c,"/projects",{"name":"Unauthorized"},"project-key").status_code==401
    assert not path.exists()


def test_project_create_idempotency_and_conflicting_payload(env):
    c,_=env
    p=create(c)
    assert post(c,"/projects",{"name":"Obra A"},"project-key-001").json()["id"]==p
    assert post(c,"/projects",{"name":"Different"},"project-key-001").status_code==409
    assert len(c.get("/api/v2/sie/dev/projects").json()["projects"])==1


def test_project_rename_lock_and_foreign_owner_denied(env):
    c,_=env
    p=create(c)
    u=c.patch(f"/api/v2/sie/dev/projects/{p}",json={"name":"Renamed","expected_lock_version":0})
    assert u.status_code==200 and u.json()["lock_version"]==1
    assert c.patch(f"/api/v2/sie/dev/projects/{p}",
       json={"name":"Overwritten","expected_lock_version":0}).status_code==409
    app.dependency_overrides[current_identity]=lambda: AuthIdentity(B,int(time.time())+600)
    assert c.patch(f"/api/v2/sie/dev/projects/{p}",
       json={"name":"Attack","expected_lock_version":1}).status_code==404
    assert c.get("/api/v2/sie/dev/projects").json()["projects"]==[]


def test_project_create_race_uses_single_id(env):
    _,path=env
    repo=DevStore(str(path))
    def run(_):
        return repo.create_project(A,"Race","same-key-race")["id"]
    with ThreadPoolExecutor(max_workers=2) as pool:
        ids=list(pool.map(run,[1,2]))
    assert ids[0]==ids[1]
    assert len(repo.list_projects(A))==1


def test_revision_numbering_idempotency_lock_clone_and_restart(env):
    c,path=env
    p=create(c)
    r=revision(c,p)
    assert revision(c,p)==r
    assert post(c,f"/projects/{p}/revisions",{"base_revision_id":str(A)},
                "revision-key-001").status_code==409
    room=post(c,f"/projects/{p}/revisions/{r}/rooms",
              {"name":"Sala","width_m":"3.0000","length_m":"4.25"}).json()
    assert room["width_m"]=="3.0000"
    assert post(c,f"/projects/{p}/revisions/{r}/loads",{
        "room_id":room["id"],"label":"Iluminacao","kind":"LIGHTING",
        "apparent_power_va":"130.125","quantity":2}).status_code==201
    circuit=post(c,f"/projects/{p}/revisions/{r}/circuits",{
        "code":"C1","nominal_voltage_v":"127.000"}).json()
    old_snapshot=c.get(f"/api/v2/sie/dev/projects/{p}/revisions/{r}/snapshot").json()
    assert len(old_snapshot["loads"])==1
    load=old_snapshot["loads"][0]
    assert post(c,f"/projects/{p}/revisions/{r}/links",
                {"load_id":load["id"],"circuit_id":circuit["id"]}).status_code==201
    sealed=post(c,f"/projects/{p}/revisions/{r}/seal",
                {"expected_lock_version":0})
    assert sealed.status_code==200, sealed.text
    digest=sealed.json()["snapshot_sha256"]
    assert len(digest)==64
    assert post(c,f"/projects/{p}/revisions/{r}/rooms",
                {"name":"tampered","width_m":2,"length_m":2}).status_code==409
    assert post(c,f"/projects/{p}/revisions/{r}/seal",
                {"expected_lock_version":0}).status_code==409
    cloned=post(c,f"/projects/{p}/revisions",
                {"base_revision_id":r},"clone-key-001")
    assert cloned.status_code==201,cloned.text
    r2=cloned.json()["id"]
    assert cloned.json()["version"]==2
    assert post(c,f"/projects/{p}/revisions",{"base_revision_id":r},
                "clone-key-001").json()["id"]==r2
    snap2=c.get(f"/api/v2/sie/dev/projects/{p}/revisions/{r2}/snapshot").json()
    snap1=c.get(f"/api/v2/sie/dev/projects/{p}/revisions/{r}/snapshot").json()
    for k in ("rooms","loads","circuits","links"):
        assert len(snap1[k])==len(snap2[k])==1
        assert snap1[k][0]["id"]!=snap2[k][0]["id"]
    assert snap2["loads"][0]["room_id"]==snap2["rooms"][0]["id"]
    assert snap2["links"][0]["circuit_id"]==snap2["circuits"][0]["id"]
    assert snap2["links"][0]["load_id"]==snap2["loads"][0]["id"]
    # Even a fresh repository after restart must reconstruct the same data.
    other=DevStore(str(path))
    assert other.snapshot(A,p,r2)==snap2
    assert other.snapshot(A,p,r)==snap1
    assert sha256(json.dumps(snap1,sort_keys=True,separators=(",",":"),
                             ensure_ascii=False).encode()).hexdigest()==digest
    assert post(c,f"/projects/{p}/revisions/{r}/supersede",
        {"expected_lock_version":1}).status_code==409  # successor must be sealed
    assert post(c,f"/projects/{p}/revisions/{r2}/seal",
        {"expected_lock_version":0}).status_code==200
    assert post(c,f"/projects/{p}/revisions/{r}/supersede",
        {"expected_lock_version":1}).status_code==200


def test_cross_revision_room_and_circuit_fk_rejected_atomically(env):
    c,path=env
    p=create(c)
    r=revision(c,p)
    room=post(c,f"/projects/{p}/revisions/{r}/rooms",
              {"name":"Area","width_m":2,"length_m":3}).json()
    circuit=post(c,f"/projects/{p}/revisions/{r}/circuits",
                 {"code":"C1","nominal_voltage_v":"220"}).json()
    foreign=str(UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"))
    assert post(c,f"/projects/{p}/revisions/{r}/loads",
       {"room_id":foreign,"label":"Orfa","kind":"TUG",
        "apparent_power_va":"120"}).status_code==409
    assert post(c,f"/projects/{p}/revisions/{r}/links",
       {"circuit_id":circuit["id"],"load_id":foreign}).status_code==409
    assert DevStore(str(path)).snapshot(A,p,r)["loads"]==[]
    assert post(c,f"/projects/{p}/revisions/{r}/loads",
       {"room_id":room["id"],"label":"TUE","kind":"TUE",
        "apparent_power_va":"2250.100"}).status_code==201
    load=DevStore(str(path)).snapshot(A,p,r)["loads"][0]
    assert post(c,f"/projects/{p}/revisions/{r}/links",
       {"circuit_id":circuit["id"],"load_id":load["id"]}).status_code==201
    assert post(c,f"/projects/{p}/revisions/{r}/links",
       {"circuit_id":circuit["id"],"load_id":load["id"]}).status_code==409


def test_a_cannot_read_or_modify_project_b(env):
    c,path=env
    p=create(c)
    r=revision(c,p)
    app.dependency_overrides[current_identity]=lambda: AuthIdentity(B,int(time.time())+600)
    assert c.get(f"/api/v2/sie/dev/projects/{p}/revisions/{r}/snapshot").status_code==404
    assert post(c,f"/projects/{p}/revisions/{r}/rooms",
       {"name":"Cross","width_m":2,"length_m":2}).status_code==404
    assert post(c,f"/projects/{p}/revisions",{}, "foreign-revision-key").status_code==404
    assert DevStore(str(path)).snapshot(A,p,r)["rooms"]==[]


@pytest.mark.parametrize("payload", [
 {"name":"a","width_m":"2.00001","length_m":"3"},
 {"name":"a","width_m":"2","length_m":"3","excluded_perimeter_m":"10"},
 {"name":"a","width_m":"NaN","length_m":"2"},
 {"name":"a","width_m":"3","length_m":"4","owner_id":str(B)},
])
def test_b05_rejects_invalid_geometry_and_extra_fields(env,payload):
    c,_=env
    p=create(c);r=revision(c,p)
    assert post(c,f"/projects/{p}/revisions/{r}/rooms",payload).status_code==422


def test_b05_invalid_load_type_denied(env):
    c,_=env
    p=create(c);r=revision(c,p)
    room=post(c,f"/projects/{p}/revisions/{r}/rooms",
       {"name":"Sala","width_m":"3","length_m":"3"}).json()
    assert post(c,f"/projects/{p}/revisions/{r}/loads",
       {"room_id":room["id"],"label":"x","kind":"EVIL",
        "apparent_power_va":"12"}).status_code==422


def test_clone_is_all_or_nothing_on_database_error(env):
    c,path=env
    p=create(c);r=revision(c,p)
    room=post(c,f"/projects/{p}/revisions/{r}/rooms",
       {"name":"Sala","width_m":"4","length_m":"4"}).json()
    post(c,f"/projects/{p}/revisions/{r}/loads",
         {"room_id":room["id"],"label":"FAIL_CLONE","kind":"LIGHTING",
          "apparent_power_va":"100"})
    assert post(c,f"/projects/{p}/revisions/{r}/seal",
       {"expected_lock_version":0}).status_code==200
    with sqlite3.connect(path) as db:
        db.executescript("""CREATE TRIGGER reject_new_clone BEFORE INSERT ON v201_loads
            WHEN NEW.label='FAIL_CLONE' BEGIN SELECT RAISE(ABORT,'fixture'); END;""")
    r1=post(c,f"/projects/{p}/revisions",
            {"base_revision_id":r},"clone-key-rollback")
    assert r1.status_code==503, r1.text
    with sqlite3.connect(path) as db:
        assert db.execute("SELECT COUNT(*) FROM v201_revisions").fetchone()[0]==1
        db.execute("DROP TRIGGER reject_new_clone")
    r2=post(c,f"/projects/{p}/revisions",
            {"base_revision_id":r},"clone-key-rollback")
    assert r2.status_code==201, r2.text
