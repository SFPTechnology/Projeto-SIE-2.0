"""F07 study API; persistent routes inherit local authorization boundary."""
from uuid import UUID
from fastapi import APIRouter, Header, HTTPException
from pydantic import Field
from .domain.installation import DomainModel
from .conductor_f07 import Study, analyze, save, history
from .storage_api import _storage
from .storage import ConflitoRevisao
from .conductor_selection_f07 import Selection,select,save_selection,selection_history
from . import conductor_registry_f07 as selection_registry
router=APIRouter(tags=['Condutores F07'])

@router.post('/api/v1/condutores/analisar')
def analysis(study:Study):
    return analyze(study)

class SaveStudy(DomainModel):
    study:Study
    expected_revision:int=Field(ge=0,strict=True)

@router.put('/api/v1/local/projetos/{project_id}/condutores')
def persist(project_id:UUID,payload:SaveStudy,authorization:str|None=Header(default=None)):
    try:
        return save(_storage(authorization),project_id,payload.study,payload.expected_revision)
    except ConflitoRevisao as exc:
        raise HTTPException(409,'Revisão concorrente; reabra o projeto') from exc
    except ValueError as exc:
        raise HTTPException(422,str(exc)) from exc

@router.get('/api/v1/local/projetos/{project_id}/condutores')
def studies(project_id:UUID,authorization:str|None=Header(default=None)):
    item=_storage(authorization).carregar(str(project_id))
    if item is None: raise HTTPException(404,'Projeto não encontrado')
    try:
        return {'revision':item['revisao'],'studies':history(item['dados']),'selections':selection_history(item['dados'])}
    except (ValueError,KeyError) as exc:
        raise HTTPException(422,'Histórico/topologia incompatível') from exc


@router.get('/api/v1/condutores/catalogo')
def source_catalog():
    try:
        return {**selection_registry.catalog(),'catalog_sha256':selection_registry.catalog_hash()}
    except ValueError as exc:
        raise HTTPException(422,str(exc)) from exc

@router.post('/api/v1/condutores/selecionar')
def selection(request:Selection):
    return select(request)

class SaveSelection(DomainModel):
    request:Selection
    expected_revision:int=Field(ge=0,strict=True)

@router.put('/api/v1/local/projetos/{project_id}/condutores/selecao')
def persist_selection(project_id:UUID,payload:SaveSelection,authorization:str|None=Header(default=None)):
    try:
        return save_selection(_storage(authorization),project_id,payload.request,payload.expected_revision)
    except ConflitoRevisao as exc:
        raise HTTPException(409,'Revisão concorrente; reabra o projeto') from exc
    except ValueError as exc:
        raise HTTPException(422,str(exc)) from exc
