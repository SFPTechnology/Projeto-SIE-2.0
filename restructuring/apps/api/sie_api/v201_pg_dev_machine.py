"""B06: server-origin machine records in disposable PostgreSQL 17 only.

Uses an already-guarded Pg17DisposableAdapter with no connection credentials.
No client HTTP endpoint, no user supplied actor, and no normative approval.
Deterministic identifiers provide idempotent replay without changing GF02 tables.
"""
from __future__ import annotations

import hashlib
import json
from uuid import UUID, NAMESPACE_URL, uuid5

from .v201_pg_dev_adapter import Pg17DisposableAdapter, PgMissing, PgConflict, _uuid, _text


class PgDevMachineWriter:
    def __init__(self,adapter: Pg17DisposableAdapter):
        if type(adapter) is not Pg17DisposableAdapter:
            raise TypeError("disposable PG17 adapter required")
        self.adapter=adapter

    @staticmethod
    def _json(value) -> tuple[str,str]:
        try:
            blob=json.dumps(value,sort_keys=True,separators=(",",":"),
                            ensure_ascii=False,allow_nan=False)
        except (ValueError,TypeError):
            raise ValueError("output must be finite JSON") from None
        return blob,hashlib.sha256(blob.encode("utf-8")).hexdigest()

    @staticmethod
    def _uuid(*segments) -> UUID:
        return uuid5(NAMESPACE_URL,"sie2-dev-v201:"+":".join(map(str,segments)))

    @classmethod
    def _audit(cls,cur,actor,project,revision,event_type,resource_id):
        aid=cls._uuid("audit",project,revision,event_type,resource_id)
        cur.execute("""INSERT INTO public.sie_audit_events(
                   id,project_id,revision_id,actor_id,event_type,payload)
                   VALUES(%s,%s,%s,%s,%s,%s::jsonb)
                   ON CONFLICT (id) DO NOTHING""",
                   (aid,project,revision,actor,event_type,
                    json.dumps({"resource_id":str(resource_id),
                                "origin":"trusted-backend","normative_status":"NOT_EVALUATED"})))

    def record_run(self,owner,project,revision,input_sha256,engine_version,output,key):
        owner,project,revision=_uuid(owner),_uuid(project),_uuid(revision)
        engine_version=_text(engine_version,100)
        key=_text(key,128)
        if len(key)<8 or not isinstance(input_sha256,str) or len(input_sha256)!=64:
            raise ValueError("bad idempotency key or input hash")
        payload,digest=self._json(output)
        run_id=self._uuid("run",project,revision,key)
        with self.adapter.conn.transaction():
            with self.adapter.conn.cursor() as cur:
                self.adapter._owner(cur,owner,project)
                cur.execute("""SELECT lifecycle_state,sealed_snapshot_sha256
                             FROM public.sie_project_revisions WHERE id=%s
                             AND project_id=%s FOR UPDATE""",(revision,project))
                r=cur.fetchone()
                if not r or r[0]!="SEALED" or r[1]!=input_sha256:
                    raise PgConflict("only sealed matching inputs can be calculated")
                cur.execute("""INSERT INTO public.sie_calculation_runs(
                       id,project_id,revision_id,input_sha256,engine_version,
                       normative_status,output_snapshot)
                       VALUES(%s,%s,%s,%s,%s,'NOT_EVALUATED',%s::jsonb)
                       ON CONFLICT (id) DO NOTHING""",
                       (run_id,project,revision,input_sha256,engine_version,payload))
                cur.execute("""SELECT input_sha256,engine_version,
                       normative_status,output_snapshot
                       FROM public.sie_calculation_runs
                       WHERE id=%s AND project_id=%s AND revision_id=%s""",
                       (run_id,project,revision))
                existing=cur.fetchone()
                if (not existing or existing[0]!=input_sha256 or
                    existing[1]!=engine_version or existing[2]!="NOT_EVALUATED" or
                    self._json(existing[3])[1]!=digest):
                    raise PgConflict("calculation retry changed original payload")
                self._audit(cur,owner,project,revision,"calculation.created",run_id)
                return {"id":str(run_id),"input_sha256":input_sha256,
                        "output_sha256":digest,"normative_status":"NOT_EVALUATED"}

    def record_artifact(self,owner,project,revision,run,artifact_type,content):
        owner,project,revision,run=map(_uuid,(owner,project,revision,run))
        if artifact_type not in {"LOAD_SCHEDULE","SINGLE_LINE","MEMORIAL","DRAWING","OTHER"}:
            raise ValueError("unknown artifact type")
        if not isinstance(content,(bytes,bytearray)) or len(content)>2097152:
            raise ValueError("invalid artifact size")
        digest=hashlib.sha256(content).hexdigest()
        artifact_id=self._uuid("artifact",project,revision,run,artifact_type,digest)
        with self.adapter.conn.transaction():
            with self.adapter.conn.cursor() as cur:
                self.adapter._owner(cur,owner,project)
                cur.execute("""SELECT lifecycle_state FROM public.sie_project_revisions
                            WHERE id=%s AND project_id=%s FOR UPDATE""",
                            (revision,project))
                rev=cur.fetchone()
                if not rev or rev[0] not in ("SEALED","SUPERSEDED"):
                    raise PgConflict("artifact requires sealed revision")
                cur.execute("""SELECT 1 FROM public.sie_calculation_runs
                             WHERE id=%s AND project_id=%s AND revision_id=%s""",
                            (run,project,revision))
                if cur.fetchone() is None:
                    raise PgMissing("calculation not found in owner scope")
                cur.execute("""INSERT INTO public.sie_artifacts(
                           id,project_id,revision_id,calculation_run_id,
                           artifact_type,content_sha256,artifact_status)
                           VALUES(%s,%s,%s,%s,%s,%s,'DRAFT')
                           ON CONFLICT (id) DO NOTHING""",
                           (artifact_id,project,revision,run,artifact_type,digest))
                self._audit(cur,owner,project,revision,"artifact.created",artifact_id)
                return {"id":str(artifact_id),"content_sha256":digest,
                        "artifact_status":"DRAFT","normative_status":"NOT_EVALUATED"}
