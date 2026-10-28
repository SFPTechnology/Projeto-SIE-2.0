"""C05 owner-scoped DEV-only API. No remote Supabase writes or client-run imports."""
from __future__ import annotations
from uuid import UUID
from fastapi import APIRouter, Depends, Header
from .auth_boundary_v201 import AuthIdentity, current_identity
from .v201_dev_api import dev_gate, _store, _run
from .v201_c_calculation import run_sealed_dev, read_run_dev

router = APIRouter(prefix="/api/v2/sie/dev", tags=["SIE2 DEV C05"],
                   dependencies=[Depends(dev_gate)])

@router.post("/projects/{project_id}/revisions/{revision_id}/calculate",status_code=201)
def calculate_revision(project_id: UUID, revision_id: UUID,
                       idempotency_key: str = Header(...,alias="Idempotency-Key"),
                       identity: AuthIdentity = Depends(current_identity)):
    row=_run(run_sealed_dev,_store(),identity.user_id,project_id,revision_id,idempotency_key)
    return {"id":row["id"],"input_sha256":row["input_sha256"],
            "output_sha256":row["output_sha256"],"normative_status":"EVIDENCE_PENDING",
            "dev_only":True}

@router.get("/projects/{project_id}/revisions/{revision_id}/calculations/{run_id}")
def read_calculation(project_id: UUID, revision_id: UUID, run_id: UUID,
                     identity: AuthIdentity = Depends(current_identity)):
    return _run(read_run_dev,_store(),identity.user_id,project_id,revision_id,run_id)
