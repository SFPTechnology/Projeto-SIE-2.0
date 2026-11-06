"""B06 server-origin calculations/artifacts (DEV simulator only).

There are NO FastAPI routes to invoke these write operations. Only trusted
internal application code should construct a ServerWriter after ownership has
been verified. Remote Supabase integration is intentionally not implemented.
"""
from __future__ import annotations
from contextlib import closing
import hashlib
import json
import sqlite3
from uuid import uuid4

from .v201_dev_store import DevStore, Conflict, Invalid, Missing, _uuid, _key, _name
from .v201_dev_audit import digest

MACHINE_SCHEMA = """
CREATE TABLE IF NOT EXISTS v201_runs(
 id TEXT PRIMARY KEY,
 project_id TEXT NOT NULL, revision_id TEXT NOT NULL,
 idempotency_key TEXT NOT NULL,
 input_sha256 TEXT NOT NULL, output_sha256 TEXT NOT NULL,
 engine_version TEXT NOT NULL,
 output_snapshot TEXT NOT NULL,
 normative_status TEXT NOT NULL DEFAULT 'NOT_EVALUATED',
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 UNIQUE(project_id,revision_id,idempotency_key),
 UNIQUE(id,project_id,revision_id),
 FOREIGN KEY(revision_id,project_id) REFERENCES v201_revisions(id,project_id));
CREATE TABLE IF NOT EXISTS v201_artifacts(
 id TEXT PRIMARY KEY,
 project_id TEXT NOT NULL, revision_id TEXT NOT NULL, run_id TEXT NOT NULL,
 artifact_type TEXT NOT NULL, content_sha256 TEXT NOT NULL,
 status TEXT NOT NULL DEFAULT 'DRAFT',
 created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY(run_id,project_id,revision_id)
  REFERENCES v201_runs(id,project_id,revision_id));
CREATE TRIGGER IF NOT EXISTS sie_dev_runs_no_update BEFORE UPDATE ON v201_runs
 BEGIN SELECT RAISE(ABORT,'run immutable'); END;
CREATE TRIGGER IF NOT EXISTS sie_dev_runs_no_delete BEFORE DELETE ON v201_runs
 BEGIN SELECT RAISE(ABORT,'run immutable'); END;
CREATE TRIGGER IF NOT EXISTS sie_dev_artifacts_no_update BEFORE UPDATE ON v201_artifacts
 BEGIN SELECT RAISE(ABORT,'artifact immutable'); END;
CREATE TRIGGER IF NOT EXISTS sie_dev_artifacts_no_delete BEFORE DELETE ON v201_artifacts
 BEGIN SELECT RAISE(ABORT,'artifact immutable'); END;
"""


def hash_snapshot(value) -> tuple[str,str]:
    try:
        data=json.dumps(value,sort_keys=True,separators=(",",":"),
                        ensure_ascii=False,allow_nan=False)
    except (TypeError,ValueError):
        raise Invalid("snapshot deve ser JSON finito") from None
    return data,hashlib.sha256(data.encode("utf-8")).hexdigest()


class ServerWriter:
    def __init__(self,store: DevStore):
        if not isinstance(store,DevStore):
            raise Invalid("DEV store required")
        self.store=store
        with closing(store._connect()) as db:
            db.executescript(MACHINE_SCHEMA)

    @staticmethod
    def _audit(db,owner,pid,rid,event_type,entity_id):
        # Same transaction as the business record. No input, PII or tokens in logs.
        occurred=db.execute("SELECT strftime('%Y-%m-%dT%H:%M:%fZ','now')").fetchone()[0]
        digest_value=digest(event_type,str(owner),str(pid),str(rid),entity_id,occurred)
        db.execute("""INSERT INTO v201_audit_events(
                   project_id,revision_id,actor_id,event_type,entity_id,occurred_at,event_sha256)
                   VALUES (?,?,?,?,?,?,?)""",
                   (pid,rid,str(owner),event_type,entity_id,occurred,digest_value))

    def record_run(self,owner,project,revision,expected_input_hash,engine_version,output,key):
        owner,project,revision=_uuid(owner),_uuid(project),_uuid(revision)
        key=_key(key)
        engine_version=_name(engine_version,100)
        encoded,digest_out=hash_snapshot(output)
        normative_status=output.get("normative_status","NOT_EVALUATED") if isinstance(output,dict) else "NOT_EVALUATED"
        if normative_status not in ("NOT_EVALUATED","EVIDENCE_PENDING","REVIEW_REQUIRED"):
            raise Invalid("normative status cannot be approved by a machine")
        if not isinstance(expected_input_hash,str) or len(expected_input_hash)!=64:
            raise Invalid("hash de entrada invalido")
        with self.store._txn() as db:
            rev=self.store._revision(db,owner,project,revision)
            if rev["state"]!="SEALED" or rev["snapshot_sha"]!=expected_input_hash:
                raise Conflict("calculo requer snapshot selado e hash de entrada correspondente")
            prior=db.execute("""SELECT * FROM v201_runs WHERE project_id=? AND revision_id=?
                                AND idempotency_key=?""",(project,revision,key)).fetchone()
            if prior:
                if (prior["output_sha256"],prior["engine_version"],prior["input_sha256"],
                    prior["normative_status"]) != (
                    digest_out,engine_version,expected_input_hash,normative_status):
                    raise Conflict("retry calculo com corpo distinto")
                return dict(prior)
            rid=str(uuid4())
            db.execute("""INSERT INTO v201_runs(id,project_id,revision_id,idempotency_key,
               input_sha256,output_sha256,engine_version,output_snapshot,normative_status)
               VALUES(?,?,?,?,?,?,?,?,?)""",
               (rid,project,revision,key,expected_input_hash,digest_out,engine_version,encoded,
                normative_status))
            self._audit(db,owner,project,revision,"calculation.created",rid)
            return dict(db.execute("SELECT * FROM v201_runs WHERE id=?",(rid,)).fetchone())

    def record_artifact(self,owner,project,revision,run_id,artifact_type,content):
        owner,project,revision=_uuid(owner),_uuid(project),_uuid(revision)
        run_id=_uuid(run_id)
        if artifact_type not in ("LOAD_SCHEDULE","SINGLE_LINE","MEMORIAL","DRAWING","OTHER"):
            raise Invalid("tipo de artefato invalido")
        if not isinstance(content,(bytes,bytearray)) or len(content)>2097152:
            raise Invalid("conteudo invalido ou excessivo")
        checksum=hashlib.sha256(content).hexdigest()
        with self.store._txn() as db:
            rev=self.store._revision(db,owner,project,revision)
            if rev["state"]!="SEALED":
                raise Conflict("artefato requer revisao selada")
            run=db.execute("""SELECT id FROM v201_runs WHERE id=? AND project_id=?
                              AND revision_id=?""",(run_id,project,revision)).fetchone()
            if run is None: raise Missing("execucao nao encontrada no escopo")
            aid=str(uuid4())
            db.execute("""INSERT INTO v201_artifacts(id,project_id,revision_id,
                        run_id,artifact_type,content_sha256) VALUES(?,?,?,?,?,?)""",
                       (aid,project,revision,run_id,artifact_type,checksum))
            self._audit(db,owner,project,revision,"artifact.created",aid)
            return dict(db.execute("SELECT * FROM v201_artifacts WHERE id=?",(aid,)).fetchone())
