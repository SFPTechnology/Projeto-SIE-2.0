"""B04/B05 transaction-safe SQLite DEV adapter; never a remote Supabase migration.

This adapter is intentionally local, only used by explicitly enabled /api/v2/sie/dev
routes. Identical domain invariants must be tested in PostgreSQL before integration.
"""
from __future__ import annotations

from contextlib import contextmanager, closing
from decimal import Decimal, InvalidOperation
from hashlib import sha256
import json
import sqlite3
from pathlib import Path
from uuid import UUID, uuid4


class Missing(LookupError):
    pass


class Conflict(ValueError):
    pass


class Invalid(ValueError):
    pass


SCHEMA = """
PRAGMA foreign_keys=ON;
CREATE TABLE IF NOT EXISTS v201_projects(
 id TEXT PRIMARY KEY, owner TEXT NOT NULL, name TEXT NOT NULL,
 lock_version INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
CREATE TABLE IF NOT EXISTS v201_project_keys(
 owner TEXT NOT NULL, key TEXT NOT NULL, project_id TEXT NOT NULL,
 payload_sha TEXT NOT NULL, PRIMARY KEY(owner,key),
 FOREIGN KEY(project_id) REFERENCES v201_projects(id));
CREATE TABLE IF NOT EXISTS v201_revisions(
 id TEXT PRIMARY KEY, project_id TEXT NOT NULL, version INTEGER NOT NULL CHECK(version>0),
 created_by TEXT NOT NULL, base_id TEXT, state TEXT NOT NULL DEFAULT 'DRAFT'
 CHECK(state IN ('DRAFT','SEALED','SUPERSEDED')),
 lock_version INTEGER NOT NULL DEFAULT 0, idem_key TEXT NOT NULL,
 snapshot TEXT, snapshot_sha TEXT, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 UNIQUE(project_id,version), UNIQUE(project_id,idem_key), UNIQUE(id,project_id),
 FOREIGN KEY(project_id) REFERENCES v201_projects(id),
 FOREIGN KEY(base_id,project_id) REFERENCES v201_revisions(id,project_id));
CREATE TABLE IF NOT EXISTS v201_rooms(
 id TEXT PRIMARY KEY, project_id TEXT NOT NULL, revision_id TEXT NOT NULL,
 name TEXT NOT NULL, width_m TEXT NOT NULL, length_m TEXT NOT NULL,
 excluded_perimeter_m TEXT NOT NULL,
 UNIQUE(id,project_id,revision_id),
 FOREIGN KEY(revision_id,project_id) REFERENCES v201_revisions(id,project_id));
CREATE TABLE IF NOT EXISTS v201_loads(
 id TEXT PRIMARY KEY, project_id TEXT NOT NULL, revision_id TEXT NOT NULL,
 room_id TEXT NOT NULL, label TEXT NOT NULL, kind TEXT NOT NULL
 CHECK(kind IN ('LIGHTING','TUG','TUE','OTHER')),
 apparent_power_va TEXT NOT NULL, quantity INTEGER NOT NULL CHECK(quantity BETWEEN 1 AND 100000),
 UNIQUE(id,project_id,revision_id),
 FOREIGN KEY(room_id,project_id,revision_id)
 REFERENCES v201_rooms(id,project_id,revision_id));
CREATE TABLE IF NOT EXISTS v201_circuits(
 id TEXT PRIMARY KEY, project_id TEXT NOT NULL, revision_id TEXT NOT NULL,
 code TEXT NOT NULL, nominal_voltage_v TEXT NOT NULL,
 UNIQUE(id,project_id,revision_id), UNIQUE(project_id,revision_id,code),
 FOREIGN KEY(revision_id,project_id) REFERENCES v201_revisions(id,project_id));
CREATE TABLE IF NOT EXISTS v201_links(
 id TEXT PRIMARY KEY, project_id TEXT NOT NULL, revision_id TEXT NOT NULL,
 circuit_id TEXT NOT NULL, load_id TEXT NOT NULL,
 UNIQUE(project_id,revision_id,load_id),
 UNIQUE(project_id,revision_id,circuit_id,load_id),
 FOREIGN KEY(circuit_id,project_id,revision_id)
 REFERENCES v201_circuits(id,project_id,revision_id),
 FOREIGN KEY(load_id,project_id,revision_id)
 REFERENCES v201_loads(id,project_id,revision_id));
"""


def _uuid(value) -> str:
    return str(UUID(str(value)))


def _decimal(value, places: int, maximum: str, *, positive: bool = True) -> str:
    try:
        v = Decimal(str(value))
        if not v.is_finite() or (positive and v <= 0) or (not positive and v < 0) or v >= Decimal(maximum):
            raise Invalid()
        q = Decimal(1).scaleb(-places)
        if v != v.quantize(q):
            raise Invalid()
        return format(v.quantize(q), f".{places}f")
    except (ValueError, InvalidOperation):
        raise Invalid(f"valor decimal deve ser finito e ter no maximo {places} casas") from None


def _name(value: str, max_len: int = 160) -> str:
    if not isinstance(value, str) or not 1 <= len(value.strip()) <= max_len:
        raise Invalid("nome ou codigo invalido")
    return value.strip()


def _key(value: str) -> str:
    if not isinstance(value, str) or not 8 <= len(value) <= 128 or value != value.strip():
        raise Invalid("Idempotency-Key obrigatoria (8..128 caracteres)")
    return value


def _sha(payload) -> str:
    return sha256(json.dumps(payload, sort_keys=True, separators=(",", ":"),
                             ensure_ascii=False, allow_nan=False).encode("utf-8")).hexdigest()


class DevStore:
    def __init__(self, path: str):
        self.path = Path(path)
        if not self.path.is_absolute() or self.path.suffix != ".sqlite3":
            raise Invalid("database DEV must be absolute .sqlite3 path")
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with closing(self._connect()) as db:
            db.executescript(SCHEMA)

    def _connect(self):
        db = sqlite3.connect(str(self.path), timeout=8, isolation_level=None)
        db.row_factory = sqlite3.Row
        db.execute("PRAGMA foreign_keys=ON")
        db.execute("PRAGMA busy_timeout=8000")
        return db

    @contextmanager
    def _txn(self):
        db = self._connect()
        try:
            db.execute("BEGIN IMMEDIATE")
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    def _project(self, db, owner, project):
        row = db.execute("SELECT * FROM v201_projects WHERE id=? AND owner=?",
                         (_uuid(project), _uuid(owner))).fetchone()
        if row is None:
            raise Missing("projeto nao encontrado")
        return row

    def _revision(self, db, owner, project, revision, *, draft=False):
        self._project(db, owner, project)
        row = db.execute("SELECT * FROM v201_revisions WHERE id=? AND project_id=?",
                         (_uuid(revision), _uuid(project))).fetchone()
        if row is None:
            raise Missing("revisao nao encontrada")
        if draft and row["state"] != "DRAFT":
            raise Conflict("revisao selada nao pode ser alterada")
        return row

    def create_project(self, owner, name: str, key: str):
        owner, name, key = _uuid(owner), _name(name), _key(key)
        digest = _sha({"name": name})
        with self._txn() as db:
            prior = db.execute("SELECT * FROM v201_project_keys WHERE owner=? AND key=?",
                               (owner, key)).fetchone()
            if prior:
                if prior["payload_sha"] != digest:
                    raise Conflict("chave repetida com corpo diferente")
                return dict(self._project(db, owner, prior["project_id"]))
            pid = str(uuid4())
            db.execute("INSERT INTO v201_projects(id,owner,name) VALUES(?,?,?)",
                       (pid,owner,name))
            db.execute("INSERT INTO v201_project_keys(owner,key,project_id,payload_sha) VALUES(?,?,?,?)",
                       (owner,key,pid,digest))
            return dict(self._project(db,owner,pid))

    def list_projects(self,owner):
        with self._connect() as db:
            rows=db.execute("SELECT id,name,lock_version,created_at FROM v201_projects WHERE owner=? ORDER BY created_at,id",
                            (_uuid(owner),)).fetchall()
            return [dict(r) for r in rows]

    def list_revisions(self,owner,project):
        with closing(self._connect()) as db:
            self._project(db,owner,project)
            rows=db.execute("""SELECT id,version,base_id,state,lock_version,snapshot_sha,created_at
                               FROM v201_revisions WHERE project_id=? ORDER BY version""",
                            (_uuid(project),)).fetchall()
            return [dict(r) for r in rows]

    def rename_project(self, owner, project, name, expected_lock):
        name = _name(name)
        with self._txn() as db:
            self._project(db,owner,project)
            cur=db.execute("UPDATE v201_projects SET name=?,lock_version=lock_version+1 WHERE id=? AND owner=? AND lock_version=?",
                           (name,_uuid(project),_uuid(owner),expected_lock))
            if cur.rowcount != 1: raise Conflict("versao desatualizada")
            return dict(self._project(db,owner,project))

    def create_revision(self, owner, project, key, base=None):
        owner, project, key = _uuid(owner), _uuid(project), _key(key)
        base = _uuid(base) if base is not None else None
        with self._txn() as db:
            self._project(db,owner,project)
            prior = db.execute("SELECT * FROM v201_revisions WHERE project_id=? AND idem_key=?",
                               (project,key)).fetchone()
            if prior:
                if prior["base_id"] != base: raise Conflict("replay com base diferente")
                return dict(prior)
            draft = db.execute("SELECT 1 FROM v201_revisions WHERE project_id=? AND state='DRAFT'",
                               (project,)).fetchone()
            if draft: raise Conflict("ja existe revisao DRAFT no projeto")
            if base:
                source = self._revision(db,owner,project,base)
                if source["state"] not in ("SEALED","SUPERSEDED"):
                    raise Conflict("base deve estar selada")
            version = db.execute("SELECT COALESCE(MAX(version),0)+1 FROM v201_revisions WHERE project_id=?",
                                 (project,)).fetchone()[0]
            rid = str(uuid4())
            db.execute("""INSERT INTO v201_revisions(id,project_id,version,created_by,base_id,idem_key)
                       VALUES(?,?,?,?,?,?)""",(rid,project,version,owner,base,key))
            if base:
                self._clone_entities(db,project,base,rid)
            return dict(db.execute("SELECT * FROM v201_revisions WHERE id=?",(rid,)).fetchone())

    def _clone_entities(self,db,pid,base,rid):
        """Clone four types atomically with NEW UUIDs and remapped FK references."""
        maps = {}
        for table in ("rooms","loads","circuits","links"):
            rows=db.execute(f"SELECT * FROM v201_{table} WHERE project_id=? AND revision_id=? ORDER BY id",
                            (pid,base)).fetchall()
            maps[table]={r["id"]: str(uuid4()) for r in rows}
            for r in rows:
                item=dict(r)
                item["id"]=maps[table][r["id"]]
                item["revision_id"]=rid
                if table=="loads": item["room_id"]=maps["rooms"][r["room_id"]]
                if table=="links":
                    item["circuit_id"]=maps["circuits"][r["circuit_id"]]
                    item["load_id"]=maps["loads"][r["load_id"]]
                cols=list(item)
                db.execute(f"INSERT INTO v201_{table} ({','.join(cols)}) VALUES ({','.join('?' for _ in cols)})",
                           tuple(item[k] for k in cols))

    def _add(self,owner,project,revision,table,item):
        with self._txn() as db:
            self._revision(db,owner,project,revision,draft=True)
            item=dict(item,id=str(uuid4()),project_id=_uuid(project),revision_id=_uuid(revision))
            cols=list(item)
            try:
                db.execute(f"INSERT INTO v201_{table} ({','.join(cols)}) VALUES ({','.join('?' for _ in cols)})",
                           tuple(item[k] for k in cols))
            except sqlite3.IntegrityError as exc:
                raise Conflict("relacao inconsistente ou duplicada") from exc
            return item

    def add_room(self,owner,project,revision,name,width,length,excluded="0"):
        w=_decimal(width,4,"100000"); h=_decimal(length,4,"100000")
        e=_decimal(excluded,4,"200000",positive=False)
        if Decimal(e) >= 2*(Decimal(w)+Decimal(h)):
            raise Invalid("perimetro excluido invalido")
        return self._add(owner,project,revision,"rooms",{
            "name":_name(name),"width_m":w,"length_m":h,"excluded_perimeter_m":e})

    def add_load(self,owner,project,revision,room,label,kind,power,quantity):
        if kind not in ("LIGHTING","TUG","TUE","OTHER"): raise Invalid("tipo de carga invalido")
        if not isinstance(quantity,int) or not 1<=quantity<=100000: raise Invalid("quantidade invalida")
        return self._add(owner,project,revision,"loads",{
            "room_id":_uuid(room),"label":_name(label),"kind":kind,
            "apparent_power_va":_decimal(power,3,"1000000000"),"quantity":quantity})

    def add_circuit(self,owner,project,revision,code,voltage):
        return self._add(owner,project,revision,"circuits",{
            "code":_name(code,64),"nominal_voltage_v":_decimal(voltage,3,"100000")})

    def link_load(self,owner,project,revision,circuit,load):
        return self._add(owner,project,revision,"links",{
            "circuit_id":_uuid(circuit),"load_id":_uuid(load)})

    def snapshot(self,owner,project,revision):
        with self._connect() as db:
            row=self._revision(db,owner,project,revision)
            return self._snapshot_db(db,project,revision) if row["state"]=="DRAFT" else json.loads(row["snapshot"])

    @staticmethod
    def _snapshot_db(db,project,revision):
        data={"schema_version":1,"project_id":_uuid(project),"revision_id":_uuid(revision)}
        for name in ("rooms","loads","circuits","links"):
            data[name]=[dict(r) for r in db.execute(
                f"SELECT * FROM v201_{name} WHERE project_id=? AND revision_id=? ORDER BY id",
                (_uuid(project),_uuid(revision))).fetchall()]
        return data

    def seal_revision(self,owner,project,revision,expected_lock):
        with self._txn() as db:
            row=self._revision(db,owner,project,revision,draft=True)
            if row["lock_version"]!=expected_lock: raise Conflict("versao desatualizada")
            snapshot=self._snapshot_db(db,project,revision)
            serialized=json.dumps(snapshot,sort_keys=True,separators=(",",":"),ensure_ascii=False)
            digest=sha256(serialized.encode("utf-8")).hexdigest()
            db.execute("""UPDATE v201_revisions SET state='SEALED',
                          lock_version=lock_version+1,snapshot=?,snapshot_sha=?
                          WHERE id=? AND state='DRAFT' AND lock_version=?""",
                       (serialized,digest,_uuid(revision),expected_lock))
            return dict(db.execute("SELECT * FROM v201_revisions WHERE id=?",
                                   (_uuid(revision),)).fetchone())

    def supersede_revision(self,owner,project,revision,expected_lock):
        with self._txn() as db:
            row=self._revision(db,owner,project,revision)
            if row["state"]!="SEALED" or row["lock_version"]!=expected_lock:
                raise Conflict("revisao nao selada ou versao desatualizada")
            successor=db.execute("""SELECT 1 FROM v201_revisions WHERE project_id=?
                                 AND base_id=? AND state='SEALED'""",
                                 (_uuid(project),_uuid(revision))).fetchone()
            if not successor: raise Conflict("sucessor selado obrigatorio")
            db.execute("""UPDATE v201_revisions SET state='SUPERSEDED',lock_version=lock_version+1
                       WHERE id=?""",(_uuid(revision),))
            return dict(db.execute("SELECT * FROM v201_revisions WHERE id=?",
                                   (_uuid(revision),)).fetchone())


    def add_bundle(self,owner,project,revision,bundle):
        """B05 atomic 4-entity import with client aliases, no external FK injection."""
        with self._txn() as db:
            self._revision(db,owner,project,revision,draft=True)
            pid,rid=_uuid(project),_uuid(revision)
            maps={kind:{} for kind in ("rooms","loads","circuits","links")}
            def new_id(kind,ref):
                ref=_name(ref,64)
                if ref in maps[kind]: raise Conflict("referencia duplicada no lote")
                uid=str(uuid4())
                maps[kind][ref]=uid
                return uid
            def known(kind,ref):
                if ref not in maps[kind]:
                    raise Conflict("referencia ausente no lote")
                return maps[kind][ref]

            for room in bundle["rooms"]:
                rid_local=new_id("rooms",room["ref"])
                width=_decimal(room["width_m"],4,"100000")
                length=_decimal(room["length_m"],4,"100000")
                excluded=_decimal(room.get("excluded_perimeter_m","0"),4,"200000",positive=False)
                if Decimal(excluded)>=2*(Decimal(width)+Decimal(length)):
                    raise Invalid("perimetro excluido invalido")
                db.execute("""INSERT INTO v201_rooms(id,project_id,revision_id,name,width_m,length_m,excluded_perimeter_m)
                              VALUES(?,?,?,?,?,?,?)""",
                           (rid_local,pid,rid,_name(room["name"]),width,length,excluded))
            for circuit in bundle["circuits"]:
                cid=new_id("circuits",circuit["ref"])
                db.execute("""INSERT INTO v201_circuits(id,project_id,revision_id,code,nominal_voltage_v)
                              VALUES(?,?,?,?,?)""",
                           (cid,pid,rid,_name(circuit["code"],64),
                            _decimal(circuit["nominal_voltage_v"],3,"100000")))
            for load in bundle["loads"]:
                lid=new_id("loads",load["ref"])
                kind=load["kind"]
                if kind not in ("LIGHTING","TUG","TUE","OTHER"): raise Invalid("tipo de carga invalido")
                qty=load.get("quantity",1)
                if not isinstance(qty,int) or not 1<=qty<=100000: raise Invalid("quantidade invalida")
                db.execute("""INSERT INTO v201_loads(id,project_id,revision_id,room_id,label,kind,apparent_power_va,quantity)
                              VALUES(?,?,?,?,?,?,?,?)""",
                           (lid,pid,rid,known("rooms",load["room_ref"]),
                            _name(load["label"]),kind,_decimal(load["apparent_power_va"],3,"1000000000"),qty))
            for i,link in enumerate(bundle["links"]):
                new_id("links",str(i))
                db.execute("""INSERT INTO v201_links(id,project_id,revision_id,circuit_id,load_id)
                              VALUES(?,?,?,?,?)""",
                           (maps["links"][str(i)],pid,rid,
                            known("circuits",link["circuit_ref"]),
                            known("loads",link["load_ref"])))
            return {"ids":maps,"counts":{kind:len(ids) for kind,ids in maps.items()},
                    "transaction":"COMMITTED_DEV_ONLY"}


    # B05: field-level editing, subject to the draft's optimistic lock.
    # IDs, owner and scope are NEVER caller-mutable. Deleting referenced entities
    # fails atomically with FK RESTRICT; detach links first.
    _ENTITY_FIELDS = {
        "rooms": frozenset({"name","width_m","length_m","excluded_perimeter_m"}),
        "loads": frozenset({"room_id","label","kind","apparent_power_va","quantity"}),
        "circuits": frozenset({"code","nominal_voltage_v"}),
        "links": frozenset({"circuit_id","load_id"}),
    }

    def _validated_patch(self, table, source):
        if table not in self._ENTITY_FIELDS or not source or not set(source) <= self._ENTITY_FIELDS[table]:
            raise Invalid("campos invalidos ou imutaveis")
        fields=dict(source)
        if "name" in fields: fields["name"]=_name(fields["name"])
        if "label" in fields: fields["label"]=_name(fields["label"])
        if "code" in fields: fields["code"]=_name(fields["code"],64)
        for name,scale,limit,positive in (
            ("width_m",4,"100000",True),("length_m",4,"100000",True),
            ("excluded_perimeter_m",4,"200000",False),
            ("apparent_power_va",3,"1000000000",True),
            ("nominal_voltage_v",3,"100000",True),
        ):
            if name in fields:
                fields[name]=_decimal(fields[name],scale,limit,positive=positive)
        for name in ("room_id","circuit_id","load_id"):
            if name in fields: fields[name]=_uuid(fields[name])
        if "kind" in fields and fields["kind"] not in ("LIGHTING","TUG","TUE","OTHER"):
            raise Invalid("tipo de carga invalido")
        if "quantity" in fields and (
            type(fields["quantity"]) is not int or not 1<=fields["quantity"]<=100000
        ):
            raise Invalid("quantidade invalida")
        return fields

    def _entity_row(self, db,table,project,revision,entity_id):
        row=db.execute(f"SELECT * FROM v201_{table} WHERE id=? AND project_id=? AND revision_id=?",
                       (_uuid(entity_id),_uuid(project),_uuid(revision))).fetchone()
        if row is None: raise Missing("entidade nao encontrada")
        return row

    def _check_revision_lock(self, db, owner,project,revision, expected_lock):
        row=self._revision(db,owner,project,revision,draft=True)
        if type(expected_lock) is not int or expected_lock < 0 or row["lock_version"] != expected_lock:
            raise Conflict("versao de revisao desatualizada")

    def update_entity(self,owner,project,revision,table,entity_id,fields,expected_lock):
        normalized=self._validated_patch(table,fields)
        with self._txn() as db:
            self._check_revision_lock(db,owner,project,revision,expected_lock)
            row=dict(self._entity_row(db,table,project,revision,entity_id))
            row.update(normalized)
            if table=="rooms":
                if Decimal(row["excluded_perimeter_m"])>=2*(Decimal(row["width_m"])+Decimal(row["length_m"])):
                    raise Invalid("perimetro excluido invalido")
            keys=sorted(normalized)
            try:
                db.execute(f"UPDATE v201_{table} SET "+",".join(f"{key}=?" for key in keys)+
                           " WHERE id=? AND project_id=? AND revision_id=?",
                           tuple(normalized[k] for k in keys)+
                           (_uuid(entity_id),_uuid(project),_uuid(revision)))
            except sqlite3.IntegrityError as exc:
                raise Conflict("integridade ou exclusividade violada") from exc
            cur=db.execute("""UPDATE v201_revisions SET lock_version=lock_version+1
                         WHERE id=? AND project_id=? AND state='DRAFT' AND lock_version=?""",
                         (_uuid(revision),_uuid(project),expected_lock))
            if cur.rowcount!=1: raise Conflict("versao de revisao desatualizada")
            return {"item":dict(self._entity_row(db,table,project,revision,entity_id)),
                    "revision_lock_version":expected_lock+1}

    def delete_entity(self,owner,project,revision,table,entity_id,expected_lock):
        if table not in self._ENTITY_FIELDS: raise Invalid("tipo de entidade invalido")
        with self._txn() as db:
            self._check_revision_lock(db,owner,project,revision,expected_lock)
            self._entity_row(db,table,project,revision,entity_id)
            try:
                db.execute(f"DELETE FROM v201_{table} WHERE id=? AND project_id=? AND revision_id=?",
                           (_uuid(entity_id),_uuid(project),_uuid(revision)))
            except sqlite3.IntegrityError as exc:
                raise Conflict("entidade possui dependencias; remova os vinculos primeiro") from exc
            cur=db.execute("""UPDATE v201_revisions SET lock_version=lock_version+1
                         WHERE id=? AND project_id=? AND state='DRAFT' AND lock_version=?""",
                         (_uuid(revision),_uuid(project),expected_lock))
            if cur.rowcount!=1: raise Conflict("versao de revisao desatualizada")
            return {"deleted_id":_uuid(entity_id),"revision_lock_version":expected_lock+1}
