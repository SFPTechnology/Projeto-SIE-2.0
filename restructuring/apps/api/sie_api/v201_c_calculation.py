"""C05 development calculations: only sealed B04 snapshots; no normative release.

The original SIE models do not provide phase, method or conductor evidence for
every B05 circuit. For those checks, return an explicit pending state instead
of guessing a conductor, breaker, demand or approval.
"""
from __future__ import annotations
from contextlib import closing
from decimal import Decimal, InvalidOperation
from hashlib import sha256
from uuid import UUID
from .v201_dev_store import DevStore, Conflict, Invalid, _uuid
from .v201_dev_server_writer import ServerWriter, hash_snapshot
from .v201_c_normative import catalog_snapshot
from .v201_c_explicit_checks import analyze_explicit

ENGINE_VERSION = "sie2-c05-v201-dev-1"
PENDING_CHECKS = ("illumination_and_tug_normative", "demand_and_balance",
                  "phase_topology", "conductor_and_voltage_drop",
                  "overcurrent_dr_dps_earthing", "distributor_category")

def dec(value, positive=False):
    try:
        d = Decimal(str(value))
        if not d.is_finite() or (positive and d <= 0) or (not positive and d < 0):
            raise ValueError()
        return d
    except (InvalidOperation, ValueError, TypeError):
        raise Invalid("nonfinite/negative electrical quantity") from None

def amount(value, digits=3):
    return format(value.quantize(Decimal(1).scaleb(-digits)), f".{digits}f")

def calculate(snapshot, *, catalog_path=None):
    if not isinstance(snapshot, dict) or snapshot.get("schema_version") != 1:
        raise Invalid("unsupported snapshot")
    if not all(snapshot.get(k) is not None and isinstance(snapshot[k], list)
               for k in ("rooms", "loads", "circuits", "links")):
        raise Invalid("snapshot entities missing")
    project, revision = _uuid(snapshot["project_id"]), _uuid(snapshot["revision_id"])
    def index(kind):
        result = {}
        for row in snapshot[kind]:
            if not isinstance(row, dict) or row.get("id") in result:
                raise Invalid("duplicate/invalid entity")
            if row.get("project_id") != project or row.get("revision_id") != revision:
                raise Invalid("cross-revision entity")
            _uuid(row["id"])
            result[row["id"]] = row
        return result
    rooms, loads, circuits, links = (index(k) for k in ("rooms","loads","circuits","links"))
    room_totals = {k: Decimal(0) for k in rooms}
    circuit_totals = {k: Decimal(0) for k in circuits}
    load_powers = {}
    for rid, row in rooms.items():
        width, length = dec(row["width_m"], True), dec(row["length_m"], True)
        excluded = dec(row["excluded_perimeter_m"])
        if excluded >= 2 * (width+length):
            raise Invalid("invalid excluded perimeter")
    for lid, row in loads.items():
        if row["room_id"] not in rooms or row["kind"] not in {"LIGHTING","TUG","TUE","OTHER"}:
            raise Invalid("invalid load room or category")
        qty = row["quantity"]
        if type(qty) is not int or not 1 <= qty <= 100000:
            raise Invalid("invalid quantity")
        power = dec(row["apparent_power_va"], True) * qty
        load_powers[lid] = power
        room_totals[row["room_id"]] += power
    linked = set()
    for link in links.values():
        lid,cid=link["load_id"],link["circuit_id"]
        if lid not in loads or cid not in circuits or lid in linked:
            raise Invalid("invalid or duplicate circuit link")
        linked.add(lid)
        circuit_totals[cid] += load_powers[lid]
    for circuit in circuits.values():
        dec(circuit["nominal_voltage_v"], True)
    catalog, cdigest = catalog_snapshot(catalog_path)
    total = sum(load_powers.values(),Decimal(0))
    technical_checks={}
    records=snapshot.get("circuit_technical",[])
    if not isinstance(records,list):
        raise Invalid("circuit technical snapshot invalid")
    seen=set()
    for entry in records:
        if not isinstance(entry,dict) or set(entry)!={"circuit_id","spec"}:
            raise Invalid("invalid technical record")
        cid=entry["circuit_id"]
        if cid in seen or cid not in circuits:
            raise Invalid("cross-revision or duplicate technical circuit")
        seen.add(cid)
        spec=entry["spec"]
        if not isinstance(spec,dict) or spec.get("phase_mode") not in ("SINGLE","THREE"):
            raise Invalid("unknown technical phase mode")
        try:
            technical_checks[cid]=analyze_explicit(
                circuit_totals[cid],circuits[cid]["nominal_voltage_v"],
                spec["phase_mode"],{k:v for k,v in spec.items() if k!="phase_mode"})
        except (TypeError,ValueError) as exc:
            raise Invalid("calculation technical inputs invalid: "+str(exc)) from None
    return {
        "schema_version": 1, "engine_version": ENGINE_VERSION,
        "project_id": project, "revision_id": revision,
        "catalog_sha256": cdigest, "normative_status": "EVIDENCE_PENDING",
        "liberado_para_uso_normativo": False,
        "assumptions": ["Only explicitly entered loads; lighting/TUG minima not inferred",
                        "VA sums exclude demand factors and current phase inference"],
        "counts": {k: len(snapshot[k]) for k in ("rooms","loads","circuits","links")},
        "installed_apparent_power_va": amount(total),
        "room_load_va": {k: amount(v) for k,v in sorted(room_totals.items())},
        "circuit_load_va": {k: amount(v) for k,v in sorted(circuit_totals.items())},
        "explicit_technical_checks": {k: technical_checks[k] for k in sorted(technical_checks)},
        "unassigned_load_ids": sorted(set(loads)-linked),
        "pending_checks": list(PENDING_CHECKS),
        "catalog_records": len(catalog["records"])
    }

def run_sealed_dev(store: DevStore, owner, project, revision, key: str):
    """Internal only: owner-scoped B store and B06 immutable writer; not remote."""
    if not isinstance(store, DevStore):
        raise Invalid("development-only store required")
    owner, project, revision = _uuid(owner), _uuid(project), _uuid(revision)
    with closing(store._connect()) as db:
        row = store._revision(db, owner, project, revision)
        if row["state"] != "SEALED":
            raise Conflict("calculation requires SEALED revision")
        expected = row["snapshot_sha"]
    snap = store.snapshot(owner, project, revision)
    blob, actual = hash_snapshot(snap)
    if actual != expected:
        raise Conflict("snapshot hash mismatch")
    result = calculate(snap)
    result["input_sha256"] = actual
    return ServerWriter(store).record_run(owner, project, revision, expected,
                                          ENGINE_VERSION, result, key)

def read_run_dev(store: DevStore, owner, project, revision, run_id):
    owner,project,revision,run_id=map(_uuid,(owner,project,revision,run_id))
    ServerWriter(store)
    with closing(store._connect()) as db:
        store._revision(db,owner,project,revision)
        row=db.execute("""SELECT * FROM v201_runs WHERE id=? AND project_id=?
                          AND revision_id=?""",(run_id,project,revision)).fetchone()
        if row is None:
            from .v201_dev_store import Missing
            raise Missing("run not found")
        result=dict(row)
        result["output_snapshot"]=__import__("json").loads(result["output_snapshot"])
        # Historical output remains immutable. Freshness is a derived read-time
        # view, not a rewrite of a published calculation or normative release.
        saved_catalog=result["output_snapshot"].get("catalog_sha256")
        current_catalog=catalog_snapshot()[1]
        result["freshness"] = ("STALE_CATALOG" if saved_catalog != current_catalog
                               else "HISTORICAL_REVISION" if
                               store._revision(db,owner,project,revision)["state"] != "SEALED"
                               else "CURRENT")
        return result
