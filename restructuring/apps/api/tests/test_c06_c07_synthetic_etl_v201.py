"""C06-C07 synthetic staging: idempotence, rollback, ownership, sealed boundaries."""
from __future__ import annotations
from copy import deepcopy
from uuid import UUID
import pytest
from sie_api.v201_c_etl import stage_synthetic,reconcile_synthetic
from sie_api.v201_dev_store import DevStore,Invalid,Conflict,Missing

A=UUID("11111111-1111-4111-8111-111111111111")
B=UUID("22222222-2222-4222-8222-222222222222")

def fixture():
    return {"source_kind":"SYNTHETIC_TEST",
     "rooms":[{"source_id":"r-1","name":"Sala","width_m":"3.0000","length_m":"4.0000"}],
     "circuits":[{"source_id":"c-1","code":"C1","nominal_voltage_v":"127.000"}],
     "loads":[{"source_id":"l-1","room_source_id":"r-1","label":"Ponto 1",
              "kind":"TUG","apparent_power_va":"100.000","quantity":2}],
     "links":[{"circuit_source_id":"c-1","load_source_id":"l-1"}]}

def test_import_idempotent_and_reconciled(tmp_path):
    store=DevStore(str((tmp_path/"etl.sqlite3").resolve()))
    p=store.create_project(A,"ETL Synthetic","etl-project-01")["id"]
    r=store.create_revision(A,p,"etl-revision-01")["id"]
    payload=fixture()
    result=stage_synthetic(store,A,p,r,"etl-batch-01",payload)
    assert result==stage_synthetic(store,A,p,r,"etl-batch-01",payload)
    assert reconcile_synthetic(store,A,p,r,result)["state"]=="PASS_DEV_SYNTHETIC"
    assert result["counts"]=={"rooms":1,"loads":1,"circuits":1,"links":1}
    assert len(store.snapshot(A,p,r)["loads"])==1
    with pytest.raises(Conflict):
        mutated=deepcopy(payload)
        mutated["loads"][0]["quantity"]=999
        stage_synthetic(store,A,p,r,"etl-batch-01",mutated)
    with pytest.raises(Missing):
        stage_synthetic(store,B,p,r,"etl-batch-02",payload)
    assert len(store.snapshot(A,p,r)["loads"])==1
    bad=deepcopy(payload)
    bad["links"][0]["load_source_id"]="missing"
    with pytest.raises(Invalid):
        stage_synthetic(store,A,p,r,"etl-bad-batch",bad)
    assert len(store.snapshot(A,p,r)["loads"])==1
    with pytest.raises(Invalid):
        stage_synthetic(store,A,p,r,"etl-real-denied",{**payload,"source_kind":"REAL_LEGACY"})
    store.seal_revision(A,p,r,0)
    with pytest.raises(Conflict):
        stage_synthetic(store,A,p,r,"etl-after-seal",payload)
