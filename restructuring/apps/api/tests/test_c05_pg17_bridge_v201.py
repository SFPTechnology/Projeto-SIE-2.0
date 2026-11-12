"""C05 persisted PostgreSQL 17 bridge, ephemeral CI service only (no Supabase)."""
from __future__ import annotations
import os
from uuid import UUID
import pytest
from sie_api.v201_pg_dev_adapter import Pg17DisposableAdapter, PgMissing
from sie_api.v201_pg_dev_machine import PgDevMachineWriter
from sie_api.v201_c_calculation import calculate

pytestmark=pytest.mark.skipif(
    os.environ.get("SIE_PG17_DISPOSABLE_TEST")!="1",
    reason="disposable PostgreSQL 17 only")
A=UUID("11111111-1111-4111-8111-111111111111")
B=UUID("22222222-2222-4222-8222-222222222222")

def test_c05_sealed_pg17_snapshot_and_server_run():
    import psycopg
    db=psycopg.connect("host=localhost port=5432 dbname=sie2_gf02_ci "
        "user=postgres password=postgres_ci_only connect_timeout=5",autocommit=True)
    try:
        adapter=Pg17DisposableAdapter(db)
        p=adapter.create_project(A,"C05 PG17 fixture","c05-pg-project-001")["id"]
        rev=adapter.create_revision(A,p,"c05-pg-revision-001")["id"]
        bundle={
          "rooms":[{"ref":"r","name":"Sala","width_m":"4.0000","length_m":"5.0000"}],
          "loads":[{"ref":"l","room_ref":"r","label":"TUE","kind":"TUE",
                    "apparent_power_va":"1270.000"}],
          "circuits":[{"ref":"c","code":"C1","nominal_voltage_v":"127.000"}],
          "links":[{"load_ref":"l","circuit_ref":"c"}]}
        assert adapter.add_bundle(A,p,rev,bundle)["loads"]==1
        sealed=adapter.seal(A,p,rev,0)
        with db.cursor() as cur:
            cur.execute("""SELECT sealed_snapshot,sealed_snapshot_sha256
                           FROM public.sie_project_revisions
                           WHERE id=%s AND project_id=%s""",(rev,p))
            snapshot,hash_value=cur.fetchone()
        assert hash_value==sealed["snapshot_sha256"]
        assert len(hash_value)==64
        snapshot["links"]=snapshot.pop("circuit_loads")
        output=calculate(snapshot)
        assert output["installed_apparent_power_va"]=="1270.000"
        assert output["normative_status"]=="EVIDENCE_PENDING"
        assert output["liberado_para_uso_normativo"] is False
        writer=PgDevMachineWriter(adapter)
        result=writer.record_run(A,p,rev,hash_value,"c05-pg17-dev-v1",
                                 output,"c05-pg-run-001")
        assert result["normative_status"]=="NOT_EVALUATED"
        assert writer.record_run(A,p,rev,hash_value,"c05-pg17-dev-v1",
                                 output,"c05-pg-run-001")["id"]==result["id"]
        with pytest.raises(PgMissing):
            writer.record_run(B,p,rev,hash_value,"c05-pg17-dev-v1",
                              output,"c05-pg-denied")
    finally:
        db.close()
