"""Endpoints consultivos fail-closed para governança de fontes normativas."""
from datetime import date
from typing import Literal
from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field
from .domain.normative import RECORDS, Context, inspect_record

router = APIRouter(prefix="/api/v1/normas", tags=["governanca-normativa"])

class ApplicabilityRequest(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    typology: Literal["residencial", "comercial", "predial"]
    uf: str = Field(pattern=r"^[A-Z]{2}$")
    voltage_v: float = Field(gt=0, le=100000)
    reference_date: date
    distributor: str | None = Field(default=None, max_length=40)
    material: str | None = Field(default=None, max_length=40)
    installation_method: str | None = Field(default=None, max_length=40)
    use: str | None = Field(default=None, max_length=80)

@router.get("/catalogo")
def get_normative_catalog():
    return {"normative_conformity_verified": False, "release_allowed": False,
            "sources": [{"id": r.id, "document": r.document, "edition": r.edition,
                         "data_status": "NAO_VERIFICADA"} for r in RECORDS]}

@router.post("/aplicabilidade")
def assess_normative_applicability(payload: ApplicabilityRequest):
    ctx = Context(**payload.model_dump())
    return {"normative_conformity_verified": False, "release_allowed": False,
            "evaluation": "TRIAGEM_DE_METADADOS_SEM_HOMOLOGACAO",
            "rules": [inspect_record(r, ctx) for r in RECORDS]}
