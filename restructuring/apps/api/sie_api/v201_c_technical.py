"""C05 DEV technical inputs: owner-bound, DRAFT-only, optimistic-lock writer."""
from __future__ import annotations
import json
from .v201_dev_store import DevStore, Invalid, Conflict, Missing, _uuid
from .v201_dev_server_writer import ServerWriter
from .v201_c_explicit_checks import analyze_explicit

FIELDS={"phase_mode","correction_factor","cable_catalog","selected_mm2",
        "breaker_a","length_m","resistance_ohm_km","reactance_ohm_km",
        "power_factor","phase_label","demand_factor"}

def put_technical(store:DevStore,owner,project,revision,circuit,technical,expected_lock):
    if not isinstance(store,DevStore) or not isinstance(technical,dict):
        raise Invalid("technical record must be structured")
    if type(expected_lock) is not int or expected_lock<0:
        raise Invalid("revision lock required")
    if not set(technical)<=FIELDS or technical.get("phase_mode") not in ("SINGLE","THREE"):
        raise Invalid("phase or field unsupported")
    # Validate all supplied mathematical inputs without approval or guessed data.
    try:
        analyze_explicit("1270","127",technical["phase_mode"],
                         {k:v for k,v in technical.items() if k!="phase_mode"})
        blob=json.dumps(technical,sort_keys=True,separators=(",",":"),
                        ensure_ascii=False,allow_nan=False)
    except (TypeError,ValueError) as exc:
        raise Invalid("technical data invalid: "+str(exc)) from None
    if len(blob.encode("utf-8"))>16384:
        raise Invalid("technical record too large")
    owner,project,revision,circuit=map(_uuid,(owner,project,revision,circuit))
    with store._txn() as db:
        rev=store._revision(db,owner,project,revision,draft=True)
        if rev["lock_version"]!=expected_lock:
            raise Conflict("revision version mismatch")
        exists=db.execute("""SELECT 1 FROM v201_circuits WHERE id=?
                          AND project_id=? AND revision_id=?""",
                          (circuit,project,revision)).fetchone()
        if not exists:raise Missing("circuit not found")
        db.execute("""INSERT INTO v201_c_technical
            (circuit_id,project_id,revision_id,spec_json)
            VALUES(?,?,?,?)
            ON CONFLICT(circuit_id) DO UPDATE SET spec_json=excluded.spec_json""",
            (circuit,project,revision,blob))
        updated=db.execute("""UPDATE v201_revisions SET lock_version=lock_version+1
            WHERE id=? AND project_id=? AND state='DRAFT' AND lock_version=?""",
            (revision,project,expected_lock))
        if updated.rowcount!=1:
            raise Conflict("stale revision lock")
        ServerWriter._audit(db,owner,project,revision,"circuit.technical_updated",circuit)
        return {"circuit_id":circuit,"revision_id":revision,
                "revision_lock_version":expected_lock+1,
                "normative_status":"EVIDENCE_PENDING","dev_only":True}
