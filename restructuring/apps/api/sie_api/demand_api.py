"""F06 stateless study and optimistic authenticated local history."""
from uuid import UUID
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from .demand import Scenario, calculate, save_scenario, scenario_history, compare
from .storage_api import _storage
from .storage import ConflitoRevisao
router = APIRouter(tags=['Demanda F06'])

class SaveScenario(BaseModel):
    model_config = ConfigDict(extra='forbid')
    scenario: Scenario
    expected_revision: int = Field(ge=0, strict=True)

@router.post('/api/v1/demanda/calcular')
def study(scenario: Scenario):
    return calculate(scenario)

@router.put('/api/v1/local/projetos/{project_id}/demanda')
def save(project_id: UUID, payload: SaveScenario, authorization: str | None = Header(default=None)):
    repo = _storage(authorization)
    try:
        return save_scenario(repo, project_id, payload.scenario, payload.expected_revision)
    except ConflitoRevisao as exc:
        raise HTTPException(409, 'Revisão concorrente; reabra o projeto') from exc
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc

@router.get('/api/v1/local/projetos/{project_id}/demanda')
def history(project_id: UUID, authorization: str | None = Header(default=None)):
    item = _storage(authorization).carregar(str(project_id))
    if item is None: raise HTTPException(404, 'Projeto não encontrado')
    try:
        return {'revision': item['revisao'], 'scenarios': scenario_history(item['dados'])}
    except (ValueError, KeyError) as exc:
        raise HTTPException(422, 'Cadastre uma topologia válida') from exc

class Comparison(BaseModel):
    model_config = ConfigDict(extra='forbid')
    before: Scenario
    after: Scenario

@router.post('/api/v1/demanda/comparar')
def comparison(payload: Comparison):
    try:
        return compare(payload.before, payload.after)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc

from .load_survey import Survey
from .topology import Topology
from .demand import project_survey

class SurveyProjection(BaseModel):
    model_config = ConfigDict(extra='forbid')
    survey: Survey
    topology: Topology
    links: dict[UUID, UUID]

@router.post('/api/v1/demanda/projetar-levantamento')
def projection(payload: SurveyProjection):
    try:
        return project_survey(payload.survey, payload.topology, payload.links)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc


@router.get('/api/v1/demanda/catalogo')
def demand_catalog():
    from .demand_registry import catalog, CATALOG_HASH
    return {**catalog(), 'catalog_sha256':CATALOG_HASH}
