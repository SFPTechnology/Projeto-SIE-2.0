"""B05 editing/deletion, B06 append-only audit, B07 hardening; DEV only.

All identity substitutions are fixtures and DO NOT prove remote Supabase RLS.
"""
from __future__ import annotations

import sqlite3
import time
from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from sie_api.main import app
from sie_api.auth_boundary_v201 import AuthIdentity, current_identity
from sie_api.v201_dev_store import DevStore

A=UUID("11111111-1111-4111-8111-111111111111")
B=UUID("22222222-2222-4222-8222-222222222222")


@pytest.fixture
def env(tmp_path,monkeypatch):
    monkeypatch.setenv("SIE_ENV","test")
    monkeypatch.setenv("SIE_V201_DEV_WRITES","1")
    monkeypatch.setenv("SIE_V201_DEV_DB_PATH",str(tmp_path/"dev.sqlite3"))
    previous=dict(app.dependency_overrides)
    app.dependency_overrides[current_identity]=lambda: AuthIdentity(A,int(time.time())+600)
    try:
        yield TestClient(app),tmp_path/"dev.sqlite3"
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(previous)


def base(c):
    p=c.post("/api/v2/sie/dev/projects",json={"name":"Casa"},
             headers={"Idempotency-Key":"project-b05-key"}).json()["id"]
    r=c.post(f"/api/v2/sie/dev/projects/{p}/revisions",json={},
             headers={"Idempotency-Key":"revision-b05-key"}).json()["id"]
    prefix=f"/api/v2/sie/dev/projects/{p}/revisions/{r}"
    room=c.post(prefix+"/rooms",json={"name":"Sala","width_m":"4","length_m":"5"}).json()
    load=c.post(prefix+"/loads",json={"room_id":room["id"],"label":"TUG",
        "kind":"TUG","apparent_power_va":"125.000"}).json()
    circ=c.post(prefix+"/circuits",json={"code":"C1","nominal_voltage_v":"127"}).json()
    link=c.post(prefix+"/links",json={"circuit_id":circ["id"],"load_id":load["id"]}).json()
    return p,r,prefix,room,load,circ,link


def edit(c,prefix,kind,entity,lock,**fields):
    return c.patch(f"{prefix}/{kind}/{entity}?expected_revision_lock_version={lock}",
                   json=fields)


def delete(c,prefix,kind,entity,lock):
    return c.delete(f"{prefix}/{kind}/{entity}?expected_revision_lock_version={lock}")


def test_b05_edit_and_restrict_dependencies_and_delete_in_order(env):
    c,path=env
    p,r,prefix,room,load,circuit,link=base(c)
    result=edit(c,prefix,"rooms",room["id"],0,width_m="6.2500")
    assert result.status_code==200,result.text
    assert result.json()["revision_lock_version"]==1
    assert result.json()["item"]["width_m"]=="6.2500"
    assert delete(c,prefix,"rooms",room["id"],1).status_code==409
    assert delete(c,prefix,"links",link["id"],1).status_code==200
    assert delete(c,prefix,"loads",load["id"],2).status_code==200
    assert delete(c,prefix,"rooms",room["id"],3).status_code==200
    assert delete(c,prefix,"circuits",circuit["id"],4).status_code==200
    assert all(not DevStore(str(path)).snapshot(A,p,r)[k]
               for k in ("rooms","loads","links","circuits"))


def test_b05_rejects_stale_scope_identity_and_immutable_fields(env):
    c,path=env
    p,r,prefix,room,load,circ,link=base(c)
    assert edit(c,prefix,"rooms",room["id"],1,name="stale").status_code==409
    assert edit(c,prefix,"rooms",room["id"],0,owner_id=str(B)).status_code==422
    assert edit(c,prefix,"rooms",room["id"],0,project_id=str(B)).status_code==422
    assert edit(c,prefix,"rooms",room["id"],0,width_m="1.00001").status_code==422
    assert edit(c,prefix,"loads",load["id"],0,room_id=str(B)).status_code==409
    assert edit(c,prefix,"rooms",room["id"],0,name="Alterada").status_code==200
    assert edit(c,prefix,"rooms",room["id"],0,name="Perdida").status_code==409
    app.dependency_overrides[current_identity]=lambda: AuthIdentity(B,int(time.time())+600)
    assert edit(c,prefix,"rooms",room["id"],1,name="B").status_code==404
    assert delete(c,prefix,"links",link["id"],1).status_code==404
    assert DevStore(str(path)).snapshot(A,p,r)["rooms"][0]["name"]=="Alterada"


def test_b05_sealed_cannot_edit_or_delete(env):
    c,path=env
    p,r,prefix,room,load,circ,link=base(c)
    assert c.post(prefix+"/seal",json={"expected_lock_version":0}).status_code==200
    assert edit(c,prefix,"rooms",room["id"],0,name="tamper").status_code==409
    assert delete(c,prefix,"links",link["id"],0).status_code==409
    assert DevStore(str(path)).snapshot(A,p,r)["rooms"][0]["name"]=="Sala"


def test_b06_audit_records_only_commits_and_is_append_only(env):
    c,path=env
    p,r,prefix,room,load,circ,link=base(c)
    audit=f"/api/v2/sie/dev/projects/{p}/audit"
    before=c.get(audit)
    assert before.status_code==200,before.text
    events=before.json()["events"]
    assert len(events)>=6  # project + revision + room + load + circuit + link
    assert any(e["event_type"]=="projects.created" or e["event_type"]=="project.created"
               for e in events)
    assert all(len(e["event_sha256"])==64 for e in events)
    assert all(e["actor_id"]==str(A) and e["project_id"]==p for e in events)
    assert c.patch(prefix+f"/loads/{load['id']}?expected_revision_lock_version=0",
        json={"room_id":str(B)}).status_code==409
    assert len(c.get(audit).json()["events"])==len(events)
    assert edit(c,prefix,"rooms",room["id"],0,name="Atualizada").status_code==200
    after=c.get(audit).json()["events"]
    assert len(after)>=len(events)+2  # entity updated + revision lock advanced
    with sqlite3.connect(path) as db:
        with pytest.raises(sqlite3.DatabaseError):
            db.execute("DELETE FROM v201_audit_events")
        with pytest.raises(sqlite3.DatabaseError):
            db.execute("UPDATE v201_audit_events SET event_type='fake'")
    assert c.get(audit).status_code==200


def test_b06_owner_cannot_read_other_audit(env):
    c,_=env
    p,r,prefix,*_=base(c)
    app.dependency_overrides[current_identity]=lambda: AuthIdentity(B,int(time.time())+600)
    assert c.get(f"/api/v2/sie/dev/projects/{p}/audit").status_code==404


def test_b07_headers_and_oversized_payload_rejected(env):
    c,path=env
    res=c.post("/api/v2/sie/dev/projects",data="X"*262145,
               headers={"Content-Type":"application/json","Idempotency-Key":"large-key"})
    assert res.status_code==413
    assert not path.exists()
    ok=c.get("/api/v2/sie/dev/projects")
    assert ok.status_code==200
    assert ok.headers["Cache-Control"]=="no-store"
    assert ok.headers["X-Content-Type-Options"]=="nosniff"
    assert UUID(ok.headers["X-Request-ID"])


def test_b07_dev_routes_off_in_prod_even_if_flag_is_set(env,monkeypatch):
    c,_=env
    monkeypatch.setenv("SIE_ENV","prod")
    assert c.get("/api/v2/sie/dev/projects").status_code==503



def test_b07_rate_limiter_blocks_repeated_dev_writes(env,monkeypatch):
    from sie_api.v201_dev_rate import reset_dev_test_only
    c,_=env
    reset_dev_test_only()
    monkeypatch.setenv("SIE_V201_DEV_RATE_LIMIT","1")
    try:
        first=c.post("/api/v2/sie/dev/projects",json={"name":"A"},
                     headers={"Idempotency-Key":"rate-project-key-1"})
        assert first.status_code==201,first.text
        rejected=c.post("/api/v2/sie/dev/projects",json={"name":"B"},
                        headers={"Idempotency-Key":"rate-project-key-2"})
        assert rejected.status_code==429
        assert rejected.headers["Retry-After"]=="60"
    finally:
        reset_dev_test_only()


def test_b07_cors_accepts_local_patch_but_rejects_external_origin():
    c=TestClient(app)
    hdr={"Origin":"http://localhost:5173","Access-Control-Request-Method":"PATCH"}
    good=c.options("/api/v2/sie/dev/projects",headers=hdr)
    assert good.status_code==200
    blocked=c.options("/api/v2/sie/dev/projects",headers={
        "Origin":"https://evil.example","Access-Control-Request-Method":"DELETE"})
    assert blocked.status_code==400
    assert blocked.headers.get("Access-Control-Allow-Origin") is None
