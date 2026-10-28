"""C06-C07: DEV-only synthetic ETL. Real legacy imports are deliberately disabled.

Imports to an existing owner-verified DRAFT revision, atomically. Deterministic
UUIDs and a batch ledger make repeated identical imports idempotent. A real
source requires separately governed provenance, owner mapping, and staging GO.
"""
from __future__ import annotations
from contextlib import closing
from hashlib import sha256
from uuid import uuid5, NAMESPACE_URL
import json
import sqlite3
from .v201_dev_store import DevStore, Invalid, Conflict, _uuid, _key, _name, _decimal, _sha

LEDGER = """CREATE TABLE IF NOT EXISTS v201_c_etl_batches(
  idempotency_key TEXT NOT NULL, project_id TEXT NOT NULL,
  revision_id TEXT NOT NULL, owner TEXT NOT NULL, payload_sha256 TEXT NOT NULL,
  result_json TEXT NOT NULL,
  PRIMARY KEY(owner,project_id,revision_id,idempotency_key),
  FOREIGN KEY(revision_id,project_id) REFERENCES v201_revisions(id,project_id));"""
KINDS = ("rooms","loads","circuits","links")

def _payload(value):
    if not isinstance(value, dict) or set(value) != {"source_kind","rooms","loads","circuits","links"}:
        raise Invalid("unrecognized ETL manifest")
    if value["source_kind"] != "SYNTHETIC_TEST":
        raise Invalid("REAL_LEGACY_SOURCE_DISABLED_UNTIL_PROVENANCE_AND_GO")
    for kind in KINDS:
        if not isinstance(value[kind],list) or len(value[kind]) > 2000:
            raise Invalid("invalid batch rows")
    if sum(len(value[k]) for k in KINDS)>4000:
        raise Invalid("batch too large")
    return _sha(value)

def stage_synthetic(store: DevStore, owner, project, revision, key, payload):
    if not isinstance(store,DevStore):
        raise Invalid("local DEV store required")
    owner,project,revision = _uuid(owner),_uuid(project),_uuid(revision)
    key=_key(key)
    digest=_payload(payload)
    with closing(store._connect()) as db:
        db.execute(LEDGER)
    with store._txn() as db:
        store._revision(db,owner,project,revision,draft=True)
        prior=db.execute("""SELECT payload_sha256,result_json FROM v201_c_etl_batches
                WHERE owner=? AND project_id=? AND revision_id=? AND idempotency_key=?""",
                (owner,project,revision,key)).fetchone()
        if prior:
            if prior["payload_sha256"]!=digest:
                raise Conflict("same ETL idempotency key with different manifest")
            return json.loads(prior["result_json"])
        maps={k:{} for k in KINDS}
        def assign(kind, ref):
            ref=_name(ref,128)
            if ref in maps[kind]:
                raise Invalid("duplicate source identifier")
            out=str(uuid5(NAMESPACE_URL,"sie2-etl:"+":".join(
                (owner,project,revision,key,kind,ref))))
            maps[kind][ref]=out
            return out
        def known(kind,ref):
            try:
                return maps[kind][ref]
            except (KeyError,TypeError):
                raise Invalid("dangling source reference") from None
        for room in payload["rooms"]:
            if set(room)-{"source_id","name","width_m","length_m","excluded_perimeter_m"}:
                raise Invalid("unmapped room column")
            uid=assign("rooms",room["source_id"])
            w=_decimal(room["width_m"],4,"100000")
            l=_decimal(room["length_m"],4,"100000")
            ex=_decimal(room.get("excluded_perimeter_m","0"),4,"200000",positive=False)
            if __import__("decimal").Decimal(ex) >= 2*(
                __import__("decimal").Decimal(w)+__import__("decimal").Decimal(l)):
                raise Invalid("invalid perimeter")
            db.execute("""INSERT INTO v201_rooms
                      (id,project_id,revision_id,name,width_m,length_m,excluded_perimeter_m)
                      VALUES (?,?,?,?,?,?,?)""",
                      (uid,project,revision,_name(room["name"]),w,l,ex))
        for circuit in payload["circuits"]:
            if set(circuit)-{"source_id","code","nominal_voltage_v"}:
                raise Invalid("unmapped circuit column")
            uid=assign("circuits",circuit["source_id"])
            db.execute("""INSERT INTO v201_circuits
                         (id,project_id,revision_id,code,nominal_voltage_v)
                         VALUES (?,?,?,?,?)""",
                       (uid,project,revision,_name(circuit["code"],64),
                        _decimal(circuit["nominal_voltage_v"],3,"100000")))
        for load in payload["loads"]:
            if set(load)-{"source_id","room_source_id","label","kind","apparent_power_va","quantity"}:
                raise Invalid("unmapped load column")
            uid=assign("loads",load["source_id"])
            if load["kind"] not in {"LIGHTING","TUG","TUE","OTHER"}:
                raise Invalid("unrecognized load kind")
            quantity=load.get("quantity",1)
            if type(quantity) is not int or not 1<=quantity<=100000:
                raise Invalid("invalid load quantity")
            db.execute("""INSERT INTO v201_loads
                        (id,project_id,revision_id,room_id,label,kind,apparent_power_va,quantity)
                        VALUES (?,?,?,?,?,?,?,?)""",
                       (uid,project,revision,known("rooms",load["room_source_id"]),
                        _name(load["label"]),load["kind"],
                        _decimal(load["apparent_power_va"],3,"1000000000"),quantity))
        for i,link in enumerate(payload["links"]):
            if set(link)!={"circuit_source_id","load_source_id"}:
                raise Invalid("unmapped link column")
            uid=assign("links",f"link-{i}")
            db.execute("""INSERT INTO v201_links
                          (id,project_id,revision_id,circuit_id,load_id)
                          VALUES (?,?,?,?,?)""",
                       (uid,project,revision,known("circuits",link["circuit_source_id"]),
                        known("loads",link["load_source_id"])))
        result={"source_kind":"SYNTHETIC_TEST","idempotency_key":key,
                "payload_sha256":digest,
                "counts":{k:len(maps[k]) for k in KINDS},
                "source_id_map":maps,
                "migration_state":"STAGED_DEV_ONLY"}
        db.execute("""INSERT INTO v201_c_etl_batches
            (owner,project_id,revision_id,idempotency_key,payload_sha256,result_json)
            VALUES (?,?,?,?,?,?)""",
            (owner,project,revision,key,digest,
             json.dumps(result,sort_keys=True,separators=(",",":"))))
        return result

def reconcile_synthetic(store:DevStore,owner,project,revision,result):
    """Compare every imported ID against the owner-scoped destination snapshot."""
    snap=store.snapshot(owner,project,revision)
    if result.get("source_kind")!="SYNTHETIC_TEST":
        raise Invalid("invalid reconciliation manifest")
    mismatches={}
    for kind in KINDS:
        actual={row["id"] for row in snap[kind]}
        mapped=set(result["source_id_map"][kind].values())
        missing=sorted(mapped-actual)
        if missing: mismatches[kind]=missing
        if len(mapped)!=result["counts"][kind]:
            mismatches[kind+".count"]="count mismatch"
    return {"state":"PASS_DEV_SYNTHETIC" if not mismatches else "BLOCKED",
            "mismatches":mismatches,"counts":result["counts"],
            "real_legacy_data_migrated":False}
