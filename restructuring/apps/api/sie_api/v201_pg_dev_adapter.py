"""B04/B05 greenfield PostgreSQL 17 writer, INJECTED disposable CI connection only.

This component intentionally CANNOT be used on the existing Supabase project.
No DSN/secret is loaded from environment. A caller MUST supply a local
connection to one of the disposable CI databases and pass preflight. Privileged
queries require a trusted server identity, not user_metadata or a browser field.

Remote deployment requires a separate, reviewed adapter, A03/A04 applied
and read back, verified Auth sessions, DB backup, and DDL authorization.
"""
from __future__ import annotations

from decimal import Decimal, InvalidOperation
from hashlib import sha256
import os
from ipaddress import ip_address
from uuid import UUID

from .v201_postgres_contract import (
    IntegrationNotReady, PROJECT_REF, read_only_preflight,
)


class PgConflict(ValueError):
    pass


class PgMissing(LookupError):
    pass


def _uuid(value) -> UUID:
    return UUID(str(value))


def _text(value,limit=160) -> str:
    if not isinstance(value,str) or not 1<=len(value.strip())<=limit:
        raise ValueError("invalid text field")
    return value.strip()


def _number(value, scale, upper, positive=True) -> Decimal:
    try:
        n=Decimal(str(value))
        q=Decimal(1).scaleb(-scale)
        if (not n.is_finite() or n>=Decimal(upper) or
            (positive and n<=0) or (not positive and n<0) or n!=n.quantize(q)):
            raise ValueError("invalid finite decimal or precision")
        return n
    except (ValueError, InvalidOperation):
        raise ValueError("invalid numeric field") from None


class Pg17DisposableAdapter:
    """A proof of implementation, not an authorization to write remotely.

    Does not own the connection. psycopg 3 connection must be local to a
    throwaway CI PG17 instance and autocommit=True. The guards are enforced
    BEFORE ANY SQL write (including project creation and clone).
    """
    ALLOWED_DB=frozenset({"sie2_gf02_ci","sie2_gf02_second"})

    def __init__(self,conn,project_ref=PROJECT_REF):
        self.conn=conn
        self.project_ref=project_ref
        if os.environ.get("GITHUB_ACTIONS")!="true" or os.environ.get("SIE_PG17_DISPOSABLE_TEST")!="1":
            raise IntegrationNotReady("PostgreSQL writer is CI-only; no remote adapter")
        info=getattr(conn,"info",None)
        host=getattr(info,"host",None)
        dbname=getattr(info,"dbname",None)
        if host not in ("localhost","127.0.0.1","::1","/var/run/postgresql"):
            raise IntegrationNotReady("not a local disposable connection")
        if dbname not in self.ALLOWED_DB:
            raise IntegrationNotReady("database not designated disposable CI")
        if not getattr(conn,"autocommit",False):
            raise IntegrationNotReady("injected connection must use autocommit")
        with conn.cursor() as cur:
            cur.execute("SELECT current_database(),inet_server_addr()")
            database,address=cur.fetchone()
            if database != dbname:
                raise IntegrationNotReady("database mismatch")
            # Docker port publishing returns a private container interface
            # (often 172.18.x.x), not a loopback source; combined with
            # CI-only gate, localhost DSN and disposable DB name only.
            if address is not None:
                server=ip_address(str(address))
                if not (server.is_loopback or server.is_private):
                    raise IntegrationNotReady("not a disposable private PostgreSQL service")
        ready=read_only_preflight(conn,project_ref)
        if not ready.ready:
            raise IntegrationNotReady("GF02+A03+A04 migration preflight failed")

    @staticmethod
    def _owner(cur,owner,project):
        cur.execute("""SELECT id FROM public.sie_projects
                       WHERE id=%s AND owner_id=%s FOR UPDATE""",
                    (_uuid(project),_uuid(owner)))
        if cur.fetchone() is None:
            raise PgMissing("project not owned by authenticated actor")

    @staticmethod
    def _revision(cur,project,revision,require_draft=True):
        cur.execute("""SELECT lifecycle_state,lock_version
                       FROM public.sie_project_revisions
                       WHERE id=%s AND project_id=%s FOR UPDATE""",
                    (_uuid(revision),_uuid(project)))
        row=cur.fetchone()
        if not row: raise PgMissing("revision missing")
        if require_draft and row[0]!="DRAFT":
            raise PgConflict("sealed revision cannot be changed")
        return row

    def create_project(self,owner,name,key):
        """B04 exactly-once project creation: owner+key, persisted original payload."""
        owner=_uuid(owner);name=_text(name);key=_text(key,128)
        if len(key)<8: raise ValueError("short project idempotency key")
        fingerprint=sha256(name.encode("utf-8")).hexdigest()
        with self.conn.transaction():
            with self.conn.cursor() as cur:
                cur.execute("""INSERT INTO public.sie_projects(
                        owner_id,name,idempotency_key,request_fingerprint_sha256)
                        VALUES (%s,%s,%s,%s)
                        ON CONFLICT (owner_id,idempotency_key)
                        WHERE idempotency_key IS NOT NULL DO NOTHING
                        RETURNING id,name""",(owner,name,key,fingerprint))
                row=cur.fetchone()
                if row:
                    return {"id":str(row[0]),"name":row[1],"replayed":False}
                cur.execute("""SELECT id,name,request_fingerprint_sha256
                         FROM public.sie_projects
                         WHERE owner_id=%s AND idempotency_key=%s
                         FOR UPDATE""",(owner,key))
                previous=cur.fetchone()
                if previous is None: raise PgConflict("missing idempotent project")
                if previous[2]!=fingerprint:
                    raise PgConflict("project key reused with different original payload")
                return {"id":str(previous[0]),"name":previous[1],"replayed":True}

    def create_revision(self,owner,project,key,base=None):
        owner,project=_uuid(owner),_uuid(project)
        key=_text(key,128)
        if len(key)<8: raise ValueError("short idempotency key")
        base=_uuid(base) if base is not None else None
        with self.conn.transaction():
            with self.conn.cursor() as cur:
                self._owner(cur,owner,project)
                # Serialise version allocation, same project only.
                cur.execute("SELECT pg_advisory_xact_lock(hashtextextended(%s,20261029))",
                            (str(project),))
                cur.execute("""SELECT id,version,base_revision_id FROM public.sie_project_revisions
                    WHERE project_id=%s AND idempotency_key=%s""",(project,key))
                prior=cur.fetchone()
                if prior:
                    if prior[2]!=base: raise PgConflict("idempotency key replay changed base")
                    return {"id":str(prior[0]),"version":prior[1],"replayed":True}
                cur.execute("""SELECT 1 FROM public.sie_project_revisions
                               WHERE project_id=%s AND lifecycle_state='DRAFT' LIMIT 1""",
                            (project,))
                if cur.fetchone(): raise PgConflict("draft already exists")
                if base is not None:
                    cur.execute("""SELECT version,lifecycle_state
                                   FROM public.sie_project_revisions
                                   WHERE id=%s AND project_id=%s""",(base,project))
                    source=cur.fetchone()
                    if source is None or source[1] not in ("SEALED","SUPERSEDED"):
                        raise PgConflict("base must be sealed and same project")
                cur.execute("""SELECT COALESCE(MAX(version),0)+1
                               FROM public.sie_project_revisions
                               WHERE project_id=%s""",(project,))
                version=cur.fetchone()[0]
                cur.execute("""INSERT INTO public.sie_project_revisions(
                        project_id,version,created_by,idempotency_key,base_revision_id)
                        VALUES (%s,%s,%s,%s,%s) RETURNING id""",
                        (project,version,owner,key,base))
                rid=cur.fetchone()[0]
                if base is not None:
                    self._clone(cur,project,base,rid)
                return {"id":str(rid),"version":version,"replayed":False}

    @staticmethod
    def _clone(cur,project,base,new):
        """Four-table copy, all UUID and FK remaps, one outer SQL transaction."""
        remap={}
        # Room UUIDs are remapped before loads, circuits before links.
        for table,fk in (
            ("sie_rooms",None),
            ("sie_loads","room_id"),
            ("sie_circuits",None),
            ("sie_circuit_loads","link"),
        ):
            cur.execute(f"""SELECT * FROM public.{table}
                         WHERE project_id=%s AND revision_id=%s ORDER BY id""",
                        (project,base))
            columns=[d.name for d in cur.description]
            rows=[dict(zip(columns,row)) for row in cur.fetchall()]
            for row in rows:
                cur.execute("SELECT gen_random_uuid()")
                new_id=cur.fetchone()[0]
                remap[row["id"]]=new_id
                row["id"]=new_id
                row["revision_id"]=new
                if fk=="room_id":
                    row["room_id"]=remap[row["room_id"]]
                elif fk=="link":
                    row["load_id"]=remap[row["load_id"]]
                    row["circuit_id"]=remap[row["circuit_id"]]
                # Created_at must reflect new revision creation.
                row.pop("created_at",None)
                cols=list(row)
                cur.execute(f"""INSERT INTO public.{table}
                    ({','.join(cols)}) VALUES ({','.join(['%s']*len(cols))})""",
                    tuple(row[c] for c in cols))

    def add_bundle(self,owner,project,revision,bundle):
        """Insert validated B05 entities atomically, no partial commits."""
        owner,project,revision=_uuid(owner),_uuid(project),_uuid(revision)
        if set(bundle)!={"rooms","loads","circuits","links"}:
            raise ValueError("bundle schema keys mismatch")
        if any(type(bundle[t]) is not list or len(bundle[t])>100
               for t in ("rooms","loads","circuits","links")):
            raise ValueError("invalid batch size")
        refs={name:{} for name in ("rooms","loads","circuits")}
        with self.conn.transaction():
            with self.conn.cursor() as cur:
                self._owner(cur,owner,project)
                self._revision(cur,project,revision)
                for room in bundle["rooms"]:
                    ref=_text(room["ref"],64)
                    if ref in refs["rooms"]: raise PgConflict("duplicate room alias")
                    width=_number(room["width_m"],4,"100000")
                    length=_number(room["length_m"],4,"100000")
                    excluded=_number(room.get("excluded_perimeter_m",0),4,"200000",False)
                    if excluded>=2*(width+length): raise ValueError("invalid room perimeter")
                    cur.execute("""INSERT INTO public.sie_rooms
                        (project_id,revision_id,name,width_m,length_m,excluded_perimeter_m)
                        VALUES (%s,%s,%s,%s,%s,%s) RETURNING id""",
                        (project,revision,_text(room["name"]),width,length,excluded))
                    refs["rooms"][ref]=cur.fetchone()[0]
                for circuit in bundle["circuits"]:
                    ref=_text(circuit["ref"],64)
                    if ref in refs["circuits"]: raise PgConflict("duplicate circuit alias")
                    cur.execute("""INSERT INTO public.sie_circuits
                        (project_id,revision_id,code,nominal_voltage_v)
                        VALUES(%s,%s,%s,%s) RETURNING id""",
                        (project,revision,_text(circuit["code"],64),
                         _number(circuit["nominal_voltage_v"],3,"100000")))
                    refs["circuits"][ref]=cur.fetchone()[0]
                for load in bundle["loads"]:
                    ref=_text(load["ref"],64)
                    if ref in refs["loads"]: raise PgConflict("duplicate load alias")
                    kind=load["kind"]
                    if kind not in {"LIGHTING","TUG","TUE","OTHER"}:
                        raise ValueError("invalid load kind")
                    quantity=load.get("quantity",1)
                    if type(quantity) is not int or not 1<=quantity<=100000:
                        raise ValueError("invalid load quantity")
                    room=refs["rooms"].get(load["room_ref"])
                    if room is None: raise PgConflict("load room alias missing")
                    cur.execute("""INSERT INTO public.sie_loads
                        (project_id,revision_id,room_id,label,kind,apparent_power_va,quantity)
                        VALUES (%s,%s,%s,%s,%s,%s,%s) RETURNING id""",
                        (project,revision,room,_text(load["label"]),kind,
                         _number(load["apparent_power_va"],3,"1000000000"),quantity))
                    refs["loads"][ref]=cur.fetchone()[0]
                for link in bundle["links"]:
                    circuit=refs["circuits"].get(link["circuit_ref"])
                    load=refs["loads"].get(link["load_ref"])
                    if circuit is None or load is None:
                        raise PgConflict("invalid circuit/load alias")
                    cur.execute("""INSERT INTO public.sie_circuit_loads
                        (project_id,revision_id,circuit_id,load_id)
                        VALUES (%s,%s,%s,%s)""",(project,revision,circuit,load))
        return {name:len(bundle[name]) for name in ("rooms","loads","circuits","links")}

    def seal(self,owner,project,revision,expected_version):
        owner,project,revision=_uuid(owner),_uuid(project),_uuid(revision)
        if type(expected_version) is not int or expected_version<0:
            raise ValueError("invalid version")
        with self.conn.transaction():
            with self.conn.cursor() as cur:
                self._owner(cur,owner,project)
                self._revision(cur,project,revision,False)
                cur.execute("""SELECT lifecycle_state,lock_version,sealed_snapshot_sha256
                        FROM public.sie_a04_transition_revision(%s,%s,%s,'SEALED')""",
                        (project,revision,expected_version))
                state,version,digest=cur.fetchone()
                return {"state":state,"lock_version":version,
                        "snapshot_sha256":digest}


    # B05 entity writes in the disposable PG17 transaction.
    # Never use client-supplied column/table identifiers in SQL.
    _TABLES={
        "rooms":("sie_rooms",frozenset({
            "name","width_m","length_m","excluded_perimeter_m"})),
        "loads":("sie_loads",frozenset({
            "room_id","label","kind","apparent_power_va","quantity"})),
        "circuits":("sie_circuits",frozenset({
            "code","nominal_voltage_v"})),
        "links":("sie_circuit_loads",frozenset({
            "circuit_id","load_id"})),
    }

    def _fields(self,kind,fields):
        if kind not in self._TABLES or not fields or not set(fields)<=self._TABLES[kind][1]:
            raise ValueError("invalid or immutable B05 fields")
        allowed={}
        for k,v in fields.items():
            if k in ("name","label","code"):
                allowed[k]=_text(v,64 if k=="code" else 160)
            elif k in ("width_m","length_m","excluded_perimeter_m"):
                allowed[k]=_number(v,4,"200000" if k=="excluded_perimeter_m" else "100000",
                                    k!="excluded_perimeter_m")
            elif k in ("apparent_power_va","nominal_voltage_v"):
                allowed[k]=_number(v,3,"1000000000" if k=="apparent_power_va" else "100000")
            elif k in ("room_id","circuit_id","load_id"):
                allowed[k]=_uuid(v)
            elif k=="quantity":
                if type(v) is not int or not 1<=v<=100000: raise ValueError("invalid quantity")
                allowed[k]=v
            elif k=="kind":
                if v not in ("LIGHTING","TUG","TUE","OTHER"): raise ValueError("invalid kind")
                allowed[k]=v
        return allowed

    def edit_entity(self,owner,project,revision,kind,entity,fields,expected_lock):
        if type(expected_lock) is not int or expected_lock<0:
            raise ValueError("invalid optimistic lock")
        project,revision,entity=_uuid(project),_uuid(revision),_uuid(entity)
        allowed=self._fields(kind,fields)
        table=self._TABLES[kind][0]
        with self.conn.transaction():
            with self.conn.cursor() as cur:
                self._owner(cur,owner,project)
                state,lock=self._revision(cur,project,revision)
                if lock!=expected_lock:
                    raise PgConflict("stale revision lock")
                cur.execute(f"""SELECT id FROM public.{table}
                    WHERE id=%s AND project_id=%s AND revision_id=%s""",
                    (entity,project,revision))
                if cur.fetchone() is None: raise PgMissing("entity not found in scope")
                cols=sorted(allowed)
                assignment=",".join(f"{col}=%s" for col in cols)
                cur.execute(f"""UPDATE public.{table} SET {assignment}
                    WHERE id=%s AND project_id=%s AND revision_id=%s""",
                    tuple(allowed[col] for col in cols)+(entity,project,revision))
                cur.execute("""UPDATE public.sie_project_revisions
                    SET lock_version=lock_version+1 WHERE id=%s AND project_id=%s
                    AND lock_version=%s AND lifecycle_state='DRAFT'""",
                    (revision,project,expected_lock))
                if cur.rowcount!=1: raise PgConflict("stale revision lock")
                return {"id":str(entity),"revision_lock_version":expected_lock+1}

    def delete_entity(self,owner,project,revision,kind,entity,expected_lock):
        if kind not in self._TABLES: raise ValueError("invalid entity kind")
        if type(expected_lock) is not int or expected_lock<0:
            raise ValueError("invalid optimistic lock")
        project,revision,entity=_uuid(project),_uuid(revision),_uuid(entity)
        table=self._TABLES[kind][0]
        with self.conn.transaction():
            with self.conn.cursor() as cur:
                self._owner(cur,owner,project)
                state,lock=self._revision(cur,project,revision)
                if lock!=expected_lock: raise PgConflict("stale revision lock")
                cur.execute(f"""DELETE FROM public.{table}
                    WHERE id=%s AND project_id=%s AND revision_id=%s
                    RETURNING id""",(entity,project,revision))
                if cur.fetchone() is None: raise PgMissing("entity not found")
                cur.execute("""UPDATE public.sie_project_revisions
                    SET lock_version=lock_version+1 WHERE id=%s AND project_id=%s
                    AND lifecycle_state='DRAFT' AND lock_version=%s""",
                    (revision,project,expected_lock))
                if cur.rowcount!=1: raise PgConflict("stale revision lock")
                return {"deleted_id":str(entity),"revision_lock_version":expected_lock+1}
