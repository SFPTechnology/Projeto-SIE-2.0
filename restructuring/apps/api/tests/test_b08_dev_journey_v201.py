"""B08: full synthetic A/B journey in real transactional SQLite DEV.

Two rooms, three loads, two circuits and FKs; immutable snapshot, server-only
calculation and artifact; replay after reopening store; B denied every API read.
NOT a remote Supabase Auth, RLS, Data API, or UI test.
"""
from __future__ import annotations

import time
from uuid import UUID

from fastapi.testclient import TestClient

from sie_api.auth_boundary_v201 import AuthIdentity, current_identity
from sie_api.main import app
from sie_api.v201_dev_store import DevStore
from sie_api.v201_dev_server_writer import ServerWriter

A=UUID("11111111-1111-4111-8111-111111111111")
B=UUID("22222222-2222-4222-8222-222222222222")


def test_b08_full_dev_ab_journey(tmp_path,monkeypatch):
    path=tmp_path/"sie2_b08.sqlite3"
    monkeypatch.setenv("SIE_ENV","test")
    monkeypatch.setenv("SIE_V201_DEV_WRITES","1")
    monkeypatch.setenv("SIE_V201_DEV_DB_PATH",str(path))
    old=dict(app.dependency_overrides)
    app.dependency_overrides[current_identity]=lambda: AuthIdentity(A,int(time.time())+3600)
    c=TestClient(app)
    base="/api/v2/sie/dev/projects"
    try:
        project=c.post(base,json={"name":"Residencia exemplo B08"},
                       headers={"Idempotency-Key":"b08-project-idempotent"}).json()["id"]
        revision=c.post(f"{base}/{project}/revisions",json={},
                        headers={"Idempotency-Key":"b08-first-revision"}).json()["id"]
        prefix=f"{base}/{project}/revisions/{revision}"
        bundle={
          "rooms":[
             {"ref":"living","name":"Sala","width_m":"4.2000","length_m":"5.0000"},
             {"ref":"kitchen","name":"Cozinha","width_m":"3.1000","length_m":"3.4500"}],
          "loads":[
             {"ref":"l1","room_ref":"living","label":"Iluminacao sala","kind":"LIGHTING",
              "apparent_power_va":"120.000","quantity":1},
             {"ref":"l2","room_ref":"living","label":"Tomadas sala","kind":"TUG",
              "apparent_power_va":"300.000","quantity":2},
             {"ref":"l3","room_ref":"kitchen","label":"Tomadas cozinha","kind":"TUG",
              "apparent_power_va":"600.000","quantity":3}],
          "circuits":[
             {"ref":"c1","code":"C1","nominal_voltage_v":"127.000"},
             {"ref":"c2","code":"C2","nominal_voltage_v":"220.000"}],
          "links":[
             {"load_ref":"l1","circuit_ref":"c1"},
             {"load_ref":"l2","circuit_ref":"c1"},
             {"load_ref":"l3","circuit_ref":"c2"}]}
        r=c.post(prefix+"/bundle",json=bundle)
        assert r.status_code==201,r.text
        assert r.json()["counts"]=={"rooms":2,"loads":3,"circuits":2,"links":3}
        snapshot=c.get(prefix+"/snapshot").json()
        assert [len(snapshot[key]) for key in ("rooms","loads","circuits","links")]==[2,3,2,3]
        seal=c.post(prefix+"/seal",json={"expected_lock_version":0})
        assert seal.status_code==200,seal.text
        digest=seal.json()["snapshot_sha256"]
        assert len(digest)==64
        assert c.get(prefix+"/snapshot").json()==snapshot
        assert c.post(prefix+"/bundle",json=bundle).status_code==409
        # Backend-origin output: no browser route exists for machine writes.
        store=DevStore(str(path))
        writer=ServerWriter(store)
        run=writer.record_run(A,project,revision,digest,"b08-engine-dev",
                              {"normative_status":"NOT_EVALUATED",
                               "totals":{"rooms":2,"loads":3,"circuits":2}},
                              "b08-run-key-001")
        assert run["normative_status"]=="NOT_EVALUATED"
        artifact=writer.record_artifact(A,project,revision,run["id"],
                                        "LOAD_SCHEDULE",b"SYNTHETIC B08")
        assert artifact["status"]=="DRAFT"
        assert any(e["event_type"]=="calculation.created" for e in store.audit_events(A,project))
        assert any(e["event_type"]=="artifact.created" for e in store.audit_events(A,project))
        # Reinitialize same database: persistent content must be unchanged.
        reopened=DevStore(str(path))
        assert reopened.snapshot(A,project,revision)==snapshot
        assert len(reopened.audit_events(A,project))>=8
        cloned=c.post(f"{base}/{project}/revisions",
                     json={"base_revision_id":revision},
                     headers={"Idempotency-Key":"b08-clone-key-001"})
        assert cloned.status_code==201,cloned.text
        cloned_id=cloned.json()["id"]
        cloned_snap=c.get(f"{base}/{project}/revisions/{cloned_id}/snapshot").json()
        assert [len(cloned_snap[k]) for k in ("rooms","loads","circuits","links")]==[2,3,2,3]
        assert {r["id"] for r in cloned_snap["rooms"]}.isdisjoint(
               {r["id"] for r in snapshot["rooms"]})
        # Verified identity B cannot read, mutate, link or read audit for A.
        app.dependency_overrides[current_identity]=lambda: AuthIdentity(B,int(time.time())+3600)
        assert c.get(base).json()["projects"]==[]
        assert c.get(f"{base}/{project}/revisions").status_code==404
        assert c.get(prefix+"/snapshot").status_code==404
        assert c.get(f"{base}/{project}/audit").status_code==404
        assert c.post(prefix+"/rooms",json={
                "name":"Attack","width_m":2,"length_m":2}).status_code==404
        assert c.patch(f"{prefix}/rooms/{snapshot['rooms'][0]['id']}"
               "?expected_revision_lock_version=1",json={"name":"Attack"}).status_code==404
        assert c.post(prefix+"/bundle",json=bundle).status_code==404
        assert reopened.snapshot(A,project,revision)==snapshot
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(old)
