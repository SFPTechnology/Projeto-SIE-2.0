"""B06 server-only DEV writer; no browser endpoints or remote Supabase writes."""
from __future__ import annotations
import hashlib
import sqlite3
from uuid import UUID

import pytest
from sie_api.v201_dev_store import DevStore, Conflict, Missing
from sie_api.v201_dev_server_writer import ServerWriter, Invalid

A=UUID("11111111-1111-4111-8111-111111111111")
B=UUID("22222222-2222-4222-8222-222222222222")


def prepared(tmp_path):
    store=DevStore(str(tmp_path/"server.sqlite3"))
    pid=store.create_project(A,"Usina fixture","project-server-key")["id"]
    rev=store.create_revision(A,pid,"revision-server-key")["id"]
    store.add_room(A,pid,rev,"Sala",4,5)
    sealed=store.seal_revision(A,pid,rev,0)
    return store,pid,rev,sealed


def test_server_run_and_artifact_are_immutable_and_audited(tmp_path):
    store,pid,rev,sealed=prepared(tmp_path)
    writer=ServerWriter(store)
    data={"total_va":250,"status":"NOT_EVALUATED"}
    run=writer.record_run(A,pid,rev,sealed["snapshot_sha"],
                          "dev-engine-0.1",data,"run-server-key")
    assert run["normative_status"]=="NOT_EVALUATED"
    assert run["output_sha256"]
    same=writer.record_run(A,pid,rev,sealed["snapshot_sha"],
                           "dev-engine-0.1",data,"run-server-key")
    assert same["id"]==run["id"]
    with pytest.raises(Conflict):
        writer.record_run(A,pid,rev,sealed["snapshot_sha"],
                          "dev-engine-0.1",{"total_va":999},"run-server-key")
    artifact=writer.record_artifact(A,pid,rev,run["id"],"MEMORIAL",b"synthetic")
    assert artifact["status"]=="DRAFT"
    assert artifact["content_sha256"]==hashlib.sha256(b"synthetic").hexdigest()
    events=store.audit_events(A,pid)
    assert any(x["event_type"]=="calculation.created" for x in events)
    assert any(x["event_type"]=="artifact.created" for x in events)
    assert len([x for x in events if x["event_type"]=="calculation.created"])==1
    with store._connect() as db:
        with pytest.raises(sqlite3.DatabaseError):
            db.execute("DELETE FROM v201_runs")
        with pytest.raises(sqlite3.DatabaseError):
            db.execute("UPDATE v201_artifacts SET status='PUBLISHED'")


def test_server_write_rejects_foreign_owner_and_unsealed_revision(tmp_path):
    store,pid,rev,sealed=prepared(tmp_path)
    writer=ServerWriter(store)
    with pytest.raises(Missing):
        writer.record_run(B,pid,rev,sealed["snapshot_sha"],
                          "v1",{"value":1},"run-key-111")
    bad=store.create_revision(A,pid,"revision-second-key",rev)
    with pytest.raises(Conflict):
        writer.record_run(A,pid,bad["id"],sealed["snapshot_sha"],
                          "v1",{"value":1},"run-key-111")
    assert not any(x["event_type"]=="calculation.created" for x in store.audit_events(A,pid))


def test_server_write_rejects_foreign_run_and_invalid_artifact(tmp_path):
    store,pid,rev,sealed=prepared(tmp_path)
    writer=ServerWriter(store)
    run=writer.record_run(A,pid,rev,sealed["snapshot_sha"],"v1",
                          {"status":"NOT_EVALUATED"},"run-key-111")
    baseline=len(store.audit_events(A,pid))
    with pytest.raises(Missing):
        writer.record_artifact(A,pid,rev,UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"),
                               "MEMORIAL",b"x")
    with pytest.raises(Invalid):
        writer.record_artifact(A,pid,rev,run["id"],"WRONG",b"x")
    assert len(store.audit_events(A,pid))==baseline
