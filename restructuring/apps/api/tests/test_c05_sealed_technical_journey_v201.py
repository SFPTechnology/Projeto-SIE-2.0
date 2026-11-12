"""C05 integrated persisted technical inputs and owner A/B isolation in DEV."""
from uuid import UUID
import time
import pytest
from fastapi.testclient import TestClient
from sie_api.v201_dev_store import DevStore,Conflict,Missing
from sie_api.v201_c_calculation import run_sealed_dev,read_run_dev
from sie_api.v201_c_technical import put_technical
from sie_api.auth_boundary_v201 import AuthIdentity,current_identity
from sie_api.main import app

A=UUID("11111111-1111-4111-8111-111111111111")
B=UUID("22222222-2222-4222-8222-222222222222")
SPEC={"phase_mode":"SINGLE","phase_label":"A","demand_factor":"0.8",
  "correction_factor":"0.8","cable_catalog":[["2.5","25"],["4","32"]],
  "selected_mm2":"2.5","breaker_a":"16","length_m":"30",
  "resistance_ohm_km":"4","reactance_ohm_km":"0.1","power_factor":"0.8"}

def seed(tmp_path):
    store=DevStore(str((tmp_path/"c05-integrated.sqlite3").resolve()))
    p=store.create_project(A,"C05 Integrated","c05-integrated-project-01")["id"]
    rev=store.create_revision(A,p,"c05-integrated-rev-01")["id"]
    ids=store.add_bundle(A,p,rev,{
     "rooms":[{"ref":"r","name":"Sala","width_m":"4.0000","length_m":"5.0000"}],
     "loads":[{"ref":"l","room_ref":"r","label":"L","kind":"TUE",
               "apparent_power_va":"1270.000","quantity":1}],
     "circuits":[{"ref":"c","code":"C1","nominal_voltage_v":"127.000"}],
     "links":[{"load_ref":"l","circuit_ref":"c"}]})["ids"]
    return store,p,rev,ids["circuits"]["c"]

def test_engine_reads_hash_bound_technical_and_clone(tmp_path):
    store,p,rev,cid=seed(tmp_path)
    s=put_technical(store,A,p,rev,cid,SPEC,0)
    assert s["revision_lock_version"]==1
    snapshot=store.snapshot(A,p,rev)
    assert snapshot["circuit_technical"][0]["circuit_id"]==cid
    assert snapshot["circuit_technical"][0]["spec"]==SPEC
    with pytest.raises(Conflict):
        put_technical(store,A,p,rev,cid,SPEC,0)
    with pytest.raises(Missing):
        put_technical(store,B,p,rev,cid,SPEC,1)
    sealed=store.seal_revision(A,p,rev,1)
    run=run_sealed_dev(store,A,p,rev,"c05-integrated-run-key")
    output=read_run_dev(store,A,p,rev,run["id"])["output_snapshot"]
    result=output["explicit_technical_checks"][cid]
    assert result["design_current_a"]=="10"
    assert result["overcurrent"]["ib_le_in_le_iz"] is True
    assert result["liberado_para_uso_normativo"] is False
    assert "APPLICATION_CONDITIONS_UNVERIFIED" in result["pending"]
    assert run["id"]==run_sealed_dev(store,A,p,rev,"c05-integrated-run-key")["id"]
    assert store.snapshot(A,p,rev)==snapshot
    with pytest.raises(Conflict):
        put_technical(store,A,p,rev,cid,SPEC,1)
    with pytest.raises(Missing):
        read_run_dev(store,B,p,rev,run["id"])
    next_rev=store.create_revision(A,p,"c05-integrated-rev-02",rev)["id"]
    cloned=store.snapshot(A,p,next_rev)
    new_cid=cloned["circuits"][0]["id"]
    assert new_cid != cid
    assert cloned["circuit_technical"][0]["circuit_id"]==new_cid
    assert cloned["circuit_technical"][0]["spec"]==SPEC

def test_http_put_owner_and_cas(tmp_path,monkeypatch):
    store,p,rev,cid=seed(tmp_path)
    monkeypatch.setenv("SIE_ENV","test")
    monkeypatch.setenv("SIE_V201_DEV_WRITES","1")
    monkeypatch.setenv("SIE_V201_DEV_DB_PATH",str(store.path))
    url=f"/api/v2/sie/dev/projects/{p}/revisions/{rev}/circuits/{cid}/technical"
    old=dict(app.dependency_overrides)
    try:
        app.dependency_overrides[current_identity]=lambda:AuthIdentity(A,int(time.time())+3600)
        c=TestClient(app)
        resp=c.put(url,json={"expected_lock_version":0,"technical":SPEC})
        assert resp.status_code==200,resp.text
        assert c.put(url,json={"expected_lock_version":0,"technical":SPEC}).status_code==409
        app.dependency_overrides[current_identity]=lambda:AuthIdentity(B,int(time.time())+3600)
        assert c.put(url,json={"expected_lock_version":1,"technical":SPEC}).status_code==404
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(old)
