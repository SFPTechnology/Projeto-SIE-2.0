"""C05 API DEV: owner isolation, sealed revision, idempotent replay; synthetic Auth."""
from __future__ import annotations
import time
from uuid import UUID
from fastapi.testclient import TestClient
from sie_api.auth_boundary_v201 import AuthIdentity,current_identity
from sie_api.main import app
from sie_api.v201_dev_store import DevStore

A=UUID("11111111-1111-4111-8111-111111111111")
B=UUID("22222222-2222-4222-8222-222222222222")

def test_c05_api_owner_and_replay(tmp_path,monkeypatch):
    path=(tmp_path/"c05-api.sqlite3").resolve()
    monkeypatch.setenv("SIE_ENV","test")
    monkeypatch.setenv("SIE_V201_DEV_WRITES","1")
    monkeypatch.setenv("SIE_V201_DEV_DB_PATH",str(path))
    store=DevStore(str(path))
    project=store.create_project(A,"C05 API security","api-c05-project-01")["id"]
    revision=store.create_revision(A,project,"api-c05-revision-01")["id"]
    store.seal_revision(A,project,revision,0)
    prefix=f"/api/v2/sie/dev/projects/{project}/revisions/{revision}"
    old=dict(app.dependency_overrides)
    try:
        app.dependency_overrides[current_identity]=lambda: AuthIdentity(A,int(time.time())+3600)
        c=TestClient(app)
        a=c.post(prefix+"/calculate",content=b"{}",headers={"Idempotency-Key":"api-c05-run-001"})
        assert a.status_code==201,a.text
        assert a.json()["normative_status"]=="EVIDENCE_PENDING"
        second=c.post(prefix+"/calculate",content=b"{}",headers={"Idempotency-Key":"api-c05-run-001"})
        assert second.status_code==201,second.text
        assert a.json()["id"]==second.json()["id"]
        value=c.get(prefix+"/calculations/"+a.json()["id"])
        assert value.status_code==200,value.text
        assert value.json()["freshness"]=="CURRENT"
        app.dependency_overrides[current_identity]=lambda: AuthIdentity(B,int(time.time())+3600)
        assert c.get(prefix+"/calculations/"+a.json()["id"]).status_code==404
        assert c.post(prefix+"/calculate",content=b"{}",headers={"Idempotency-Key":"api-c05-run-002"}).status_code==404
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(old)
