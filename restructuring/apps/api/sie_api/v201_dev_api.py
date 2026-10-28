"""B04/B05 local-only development API, opt-in, never writes to Supabase.

JWT authentication is still delegated to the verified B02 Supabase Auth boundary.
The local DB is a *development simulator* and is NOT the PostgreSQL remote adapter.
"""
from __future__ import annotations

from decimal import Decimal
import ipaddress
import os
import sqlite3
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field

from .auth_boundary_v201 import AuthIdentity, current_identity
from .v201_dev_store import Conflict, DevStore, Invalid, Missing


def dev_gate(request: Request):
    if os.environ.get("SIE_ENV", "dev") not in {"dev", "test"}:
        raise HTTPException(status_code=503, detail="Modo DEV indisponivel")
    if os.environ.get("SIE_V201_DEV_WRITES") != "1":
        raise HTTPException(status_code=503, detail="CRUD DEV desativado")
    addr = request.client.host if request.client else ""
    try:
        loopback = ipaddress.ip_address(addr).is_loopback
    except ValueError:
        loopback = addr == "testclient"
    if not loopback:
        raise HTTPException(status_code=403, detail="CRUD DEV somente loopback")
    if not os.environ.get("SIE_V201_DEV_DB_PATH"):
        raise HTTPException(status_code=503, detail="Banco DEV nao configurado")


def _store():
    try:
        return DevStore(os.environ["SIE_V201_DEV_DB_PATH"])
    except (KeyError, Invalid, OSError, sqlite3.Error):
        raise HTTPException(status_code=503, detail="Banco DEV indisponivel") from None


def _run(func, *args):
    try:
        return func(*args)
    except Missing:
        raise HTTPException(status_code=404, detail="Recurso nao encontrado") from None
    except Conflict as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from None
    except Invalid as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from None
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=409, detail="Relacionamento ou chave duplicada") from None
    except (sqlite3.DatabaseError, OSError):
        raise HTTPException(status_code=503, detail="Persistencia DEV indisponivel") from None


router = APIRouter(prefix="/api/v2/sie/dev", tags=["SIE2 DEV B04/B05"],
                   dependencies=[Depends(dev_gate)])


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)


class ProjectIn(Strict):
    name: str = Field(min_length=1, max_length=160)


class ProjectRename(ProjectIn):
    expected_lock_version: int = Field(ge=0)


class RevisionIn(Strict):
    base_revision_id: UUID | None = None


class TransitionIn(Strict):
    expected_lock_version: int = Field(ge=0)


class RoomIn(Strict):
    name: str = Field(min_length=1, max_length=160)
    width_m: Decimal = Field(gt=0, lt=100000)
    length_m: Decimal = Field(gt=0, lt=100000)
    excluded_perimeter_m: Decimal = Field(ge=0, lt=200000, default=Decimal("0"))


class LoadIn(Strict):
    room_id: UUID
    label: str = Field(min_length=1, max_length=160)
    kind: str = Field(pattern="^(LIGHTING|TUG|TUE|OTHER)$")
    apparent_power_va: Decimal = Field(gt=0, lt=1000000000)
    quantity: int = Field(ge=1, le=100000, default=1)


class CircuitIn(Strict):
    code: str = Field(min_length=1, max_length=64)
    nominal_voltage_v: Decimal = Field(gt=0, lt=100000)


class LinkIn(Strict):
    circuit_id: UUID
    load_id: UUID


@router.post("/projects", status_code=201)
def create_project(body: ProjectIn, identity: AuthIdentity = Depends(current_identity),
                   idempotency_key: str = Header(..., alias="Idempotency-Key")):
    result = _run(_store().create_project, identity.user_id, body.name, idempotency_key)
    return {"id": result["id"], "name": result["name"],
            "lock_version": result["lock_version"], "dev_only": True}


@router.get("/projects")
def projects(identity: AuthIdentity = Depends(current_identity)):
    return {"projects": _run(_store().list_projects, identity.user_id), "dev_only": True}


@router.patch("/projects/{project_id}")
def rename(project_id: UUID, body: ProjectRename,
           identity: AuthIdentity = Depends(current_identity)):
    r = _run(_store().rename_project, identity.user_id, project_id, body.name,
             body.expected_lock_version)
    return {"id": r["id"], "name": r["name"], "lock_version": r["lock_version"]}


@router.post("/projects/{project_id}/revisions", status_code=201)
def create_revision(project_id: UUID, body: RevisionIn,
                    identity: AuthIdentity = Depends(current_identity),
                    idempotency_key: str = Header(..., alias="Idempotency-Key")):
    r = _run(_store().create_revision, identity.user_id, project_id, idempotency_key,
             body.base_revision_id)
    return {"id": r["id"], "version": r["version"], "state": r["state"],
            "base_revision_id": r["base_id"], "lock_version": r["lock_version"]}


@router.get("/projects/{project_id}/revisions/{revision_id}/snapshot")
def snapshot(project_id: UUID, revision_id: UUID,
             identity: AuthIdentity = Depends(current_identity)):
    return _run(_store().snapshot, identity.user_id, project_id, revision_id)


@router.post("/projects/{project_id}/revisions/{revision_id}/seal")
def seal(project_id: UUID, revision_id: UUID, body: TransitionIn,
         identity: AuthIdentity = Depends(current_identity)):
    r = _run(_store().seal_revision, identity.user_id, project_id,
             revision_id, body.expected_lock_version)
    return {"id": r["id"], "state": r["state"], "lock_version": r["lock_version"],
            "snapshot_sha256": r["snapshot_sha"]}


@router.post("/projects/{project_id}/revisions/{revision_id}/supersede")
def supersede(project_id: UUID, revision_id: UUID, body: TransitionIn,
              identity: AuthIdentity = Depends(current_identity)):
    r = _run(_store().supersede_revision, identity.user_id, project_id,
             revision_id, body.expected_lock_version)
    return {"id": r["id"], "state": r["state"], "lock_version": r["lock_version"]}


@router.post("/projects/{project_id}/revisions/{revision_id}/rooms", status_code=201)
def room(project_id: UUID, revision_id: UUID, body: RoomIn,
         identity: AuthIdentity = Depends(current_identity)):
    return _run(_store().add_room, identity.user_id, project_id, revision_id,
                body.name, body.width_m, body.length_m, body.excluded_perimeter_m)


@router.post("/projects/{project_id}/revisions/{revision_id}/loads", status_code=201)
def load(project_id: UUID, revision_id: UUID, body: LoadIn,
         identity: AuthIdentity = Depends(current_identity)):
    return _run(_store().add_load, identity.user_id, project_id, revision_id,
                body.room_id, body.label, body.kind, body.apparent_power_va, body.quantity)


@router.post("/projects/{project_id}/revisions/{revision_id}/circuits", status_code=201)
def circuit(project_id: UUID, revision_id: UUID, body: CircuitIn,
            identity: AuthIdentity = Depends(current_identity)):
    return _run(_store().add_circuit, identity.user_id, project_id, revision_id,
                body.code, body.nominal_voltage_v)


@router.post("/projects/{project_id}/revisions/{revision_id}/links", status_code=201)
def link(project_id: UUID, revision_id: UUID, body: LinkIn,
         identity: AuthIdentity = Depends(current_identity)):
    return _run(_store().link_load, identity.user_id, project_id,
                revision_id, body.circuit_id, body.load_id)


class BundleRoom(Strict):
    ref: str = Field(min_length=1,max_length=64)
    name: str = Field(min_length=1,max_length=160)
    width_m: Decimal = Field(gt=0,lt=100000)
    length_m: Decimal = Field(gt=0,lt=100000)
    excluded_perimeter_m: Decimal = Field(ge=0,lt=200000,default=Decimal("0"))


class BundleLoad(Strict):
    ref: str = Field(min_length=1,max_length=64)
    room_ref: str = Field(min_length=1,max_length=64)
    label: str = Field(min_length=1,max_length=160)
    kind: str = Field(pattern="^(LIGHTING|TUG|TUE|OTHER)$")
    apparent_power_va: Decimal = Field(gt=0,lt=1000000000)
    quantity: int = Field(ge=1,le=100000,default=1)


class BundleCircuit(Strict):
    ref: str = Field(min_length=1,max_length=64)
    code: str = Field(min_length=1,max_length=64)
    nominal_voltage_v: Decimal = Field(gt=0,lt=100000)


class BundleLink(Strict):
    circuit_ref: str = Field(min_length=1,max_length=64)
    load_ref: str = Field(min_length=1,max_length=64)


class BundleIn(Strict):
    rooms: list[BundleRoom] = Field(default_factory=list,max_length=100)
    loads: list[BundleLoad] = Field(default_factory=list,max_length=100)
    circuits: list[BundleCircuit] = Field(default_factory=list,max_length=100)
    links: list[BundleLink] = Field(default_factory=list,max_length=100)


@router.post("/projects/{project_id}/revisions/{revision_id}/bundle",status_code=201)
def insert_bundle(project_id: UUID,revision_id: UUID,body: BundleIn,
                  identity: AuthIdentity = Depends(current_identity)):
    return _run(_store().add_bundle,identity.user_id,project_id,revision_id,
                body.model_dump(mode="json"))
