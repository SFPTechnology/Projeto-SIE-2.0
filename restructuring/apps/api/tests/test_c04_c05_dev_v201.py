"""C04/C05: deterministic snapshots and negative security, synthetic DEV only."""
from __future__ import annotations
from uuid import UUID
import pytest
from sie_api.v201_c_normative import resolve_rule,catalog_snapshot
from sie_api.v201_c_calculation import calculate,run_sealed_dev,read_run_dev
from sie_api.v201_dev_store import DevStore,Conflict,Missing
A=UUID("11111111-1111-4111-8111-111111111111")
B=UUID("22222222-2222-4222-8222-222222222222")

def setup(tmp_path):
    store=DevStore(str((tmp_path/"c05.sqlite3").resolve()))
    p=store.create_project(A,"C05 Casa","c05-project-01")["id"]
    r=store.create_revision(A,p,"c05-revision-01")["id"]
    s=store.add_bundle(A,p,r,{
      "rooms":[{"ref":"sala","name":"Sala","width_m":"4.0000","length_m":"5.0000"}],
      "circuits":[{"ref":"c1","code":"C1","nominal_voltage_v":"127.000"}],
      "loads":[{"ref":"l1","room_ref":"sala","label":"Teste","kind":"LIGHTING",
                 "apparent_power_va":"120.000","quantity":2}],
      "links":[{"load_ref":"l1","circuit_ref":"c1"}]})
    return store,p,r,s

def test_catalog_rejects_unverified_rules_and_bad_locality():
    catalog,digest=catalog_snapshot()
    assert len(digest)==64
    r=resolve_rule("ABNT-NBR-5410",revision=1)
    assert r["status"]=="EVIDENCE_PENDING"
    assert r["catalog_sha256"]==digest
    assert resolve_rule("EDP-SP-PTDT00068-V09",revision=2)["status"]=="REVIEW_REQUIRED"
    assert resolve_rule("does-not-exist")["status"]=="REVIEW_REQUIRED"

def test_c05_hash_idempotency_pendings_and_cross_owner(tmp_path):
    store,p,r,ids=setup(tmp_path)
    snap=store.snapshot(A,p,r)
    first=calculate(snap)
    assert first==calculate(snap)
    assert first["installed_apparent_power_va"]=="240.000"
    assert first["normative_status"]=="EVIDENCE_PENDING"
    assert first["liberado_para_uso_normativo"] is False
    with pytest.raises(Conflict):
        run_sealed_dev(store,A,p,r,"c05-run-retry-01")
    seal=store.seal_revision(A,p,r,0)
    run=run_sealed_dev(store,A,p,r,"c05-run-retry-01")
    assert run["input_sha256"]==seal["snapshot_sha"]
    assert run["id"]==run_sealed_dev(store,A,p,r,"c05-run-retry-01")["id"]
    value=read_run_dev(store,A,p,r,run["id"])
    assert value["output_snapshot"]["installed_apparent_power_va"]=="240.000"
    with pytest.raises(Missing):
        read_run_dev(store,B,p,r,run["id"])
    assert store.snapshot(A,p,r)==snap
    with pytest.raises(Conflict):
        store.add_bundle(A,p,r,{"rooms":[],"loads":[],"circuits":[],"links":[]})

def test_c05_rejects_cross_revision_snapshot(tmp_path):
    store,p,r,ids=setup(tmp_path)
    snap=store.snapshot(A,p,r)
    snap["loads"][0]["revision_id"]=str(B)
    with pytest.raises(Exception):
        calculate(snap)
