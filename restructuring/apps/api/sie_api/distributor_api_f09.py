"""F09 consultative distributor and optional extension API."""
from uuid import UUID
from fastapi import APIRouter, Header, HTTPException
from pydantic import Field, ValidationError
from .domain.installation import DomainModel
from .distributor_persistence_f09 import F09EvidencePending, enquadrar_persistido, history_f09
from .storage import ConflitoRevisao
from .storage_api import _storage
from .edp_context import ContextoEDP

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


class PersistedAssessment(DomainModel):
    distributor_id: str = Field(min_length=2, max_length=80)
    supply_id: UUID
    modality: str = Field(pattern=r'^[UDT]$')
    context: ContextoEDP
    expected_revision: int = Field(ge=1, strict=True)


@router.get("/distribuidoras")
def listar_distribuidoras():
    return {"items": catalogo_distribuidoras(), "selection_requires_context": True}


@router.post("/distribuidoras/enquadrar")
def enquadrar_distribuidora(payload: DistributorAssessment):
    try:
        return diagnosticar_distribuidora(payload)
    except (ValueError, ValidationError) as exc:
        raise HTTPException(status_code=422, detail="Dados de enquadramento inválidos") from exc


@router.put("/local/projetos/{project_id}/distribuidoras/enquadrar")
def enquadrar_distribuidora_persistida(
    project_id: UUID, payload: PersistedAssessment,
    authorization: str | None = Header(default=None),
):
    try:
        return enquadrar_persistido(_storage(authorization), project_id, payload, payload.expected_revision)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ConflitoRevisao as exc:
        raise HTTPException(status_code=409, detail="Revisão concorrente; reabra o projeto") from exc
    except F09EvidencePending as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except (ValueError, ValidationError) as exc:
        raise HTTPException(status_code=422, detail="Evidências/contexto incompatíveis para F09") from exc


@router.get("/local/projetos/{project_id}/distribuidoras/enquadramentos")
def historico_enquadramentos_f09(project_id: UUID, authorization: str | None = Header(default=None)):
    project = _storage(authorization).carregar(str(project_id))
    if project is None:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    return {"project_revision": project["revisao"], "items": history_f09(project["dados"])}


@router.get("/extensoes-especializadas")
def listar_extensoes_especializadas():
    return {"items": catalogo_extensoes(), "all_optional": True}


@router.post("/extensoes-especializadas/avaliar")
def avaliar_extensao_especializada(payload: ExtensionRequest):
    try:
        return avaliar_extensao(payload)
    except (ValueError, ValidationError) as exc:
        raise HTTPException(status_code=422, detail="Dados da extensão inválidos") from exc
