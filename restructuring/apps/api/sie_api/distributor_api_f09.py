"""F09 consultative distributor and optional extension API."""
from fastapi import APIRouter, HTTPException
from pydantic import ValidationError

from .distributor_engine_f09 import (
    DistributorAssessment,
    catalogo_distribuidoras,
    diagnosticar_distribuidora,
)
from .specialized_extensions_f09 import (
    ExtensionRequest,
    avaliar_extensao,
    catalogo_extensoes,
)

router = APIRouter(prefix="/api/v1", tags=["distributor-screening"])


@router.get("/distribuidoras")
def listar_distribuidoras():
    return {"items": catalogo_distribuidoras(), "selection_requires_context": True}


@router.post("/distribuidoras/enquadrar")
def enquadrar_distribuidora(payload: DistributorAssessment):
    try:
        return diagnosticar_distribuidora(payload)
    except (ValueError, ValidationError) as exc:
        raise HTTPException(status_code=422, detail="Dados de enquadramento inválidos") from exc


@router.get("/extensoes-especializadas")
def listar_extensoes_especializadas():
    return {"items": catalogo_extensoes(), "all_optional": True}


@router.post("/extensoes-especializadas/avaliar")
def avaliar_extensao_especializada(payload: ExtensionRequest):
    try:
        return avaliar_extensao(payload)
    except (ValueError, ValidationError) as exc:
        raise HTTPException(status_code=422, detail="Dados da extensão inválidos") from exc
