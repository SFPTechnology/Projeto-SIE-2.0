"""F08 study API. Persistent operations retain the local token boundary."""
from uuid import UUID
from fastapi import APIRouter, Header, HTTPException
from pydantic import Field
from .domain.installation import DomainModel
from .protection_contracts_f08 import Study
from .protection_f08 import analyze
from .protection_storage_f08 import save, history
from .storage_api import _storage
from .storage import ConflitoRevisao

router = APIRouter(tags=['Proteções F08'])


class SaveStudy(DomainModel):
    study: Study
    expected_revision: int = Field(ge=0, strict=True)


@router.post('/api/v1/protecoes/analisar')
def analysis(study: Study):
    try:
        return analyze(study)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc


@router.put('/api/v1/local/projetos/{project_id}/protecoes')
def persist(project_id: UUID, payload: SaveStudy, authorization: str | None = Header(default=None)):
    try:
        return save(_storage(authorization), project_id, payload.study, payload.expected_revision)
    except ConflitoRevisao as exc:
        raise HTTPException(409, 'Revisão concorrente; reabra o projeto') from exc
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc


@router.get('/api/v1/local/projetos/{project_id}/protecoes')
def studies(project_id: UUID, authorization: str | None = Header(default=None)):
    item = _storage(authorization).carregar(str(project_id))
    if item is None:
        raise HTTPException(404, 'Projeto não encontrado')
    try:
        return {'revision': item['revisao'], 'studies': history(item['dados'])}
    except (ValueError, KeyError) as exc:
        raise HTTPException(422, 'Histórico/topologia incompatível') from exc


@router.get('/api/v1/protecoes/catalogo')
def source_catalog():
    from . import protection_registry_f08 as registry
    try:
        return {**registry.catalog(), 'catalog_sha256': registry.catalog_hash()}
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
