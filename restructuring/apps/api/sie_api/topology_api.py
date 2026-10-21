"""F05 stateless inspection and authenticated optimistic local revision writes."""
from uuid import UUID
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from .topology import Topology, inspect_topology, report, persist, load_document
from .storage_api import _storage
from .storage import ConflitoRevisao

router = APIRouter(tags=['Topologia F05'])
class SaveTopology(BaseModel):
    model_config = ConfigDict(extra='forbid')
    document: Topology
    expected_revision: int = Field(ge=0, strict=True)

@router.post('/api/v1/topologia/validar')
def validate_topology(raw: dict):
    return inspect_topology(raw)

@router.post('/api/v1/topologia/percursos')
def paths(document: Topology):
    return report(document)

@router.get('/api/v1/local/projetos/{project_id}/topologia')
def get_topology(project_id: UUID, authorization: str | None = Header(default=None)):
    repo = _storage(authorization)
    item = repo.carregar(str(project_id))
    if not item or 'installation_snapshot' not in item['dados']:
        raise HTTPException(404, 'Topologia não cadastrada')
    try:
        document = load_document(item['dados'])
    except (ValueError, KeyError) as exc:
        raise HTTPException(422, 'Metadados incompatíveis; revise o modelo canônico') from exc
    return {'document': document.model_dump(mode='json'), 'revision': item['revisao'],
            'results_stale': item['dados'].get('topology_results_stale', True)}

@router.put('/api/v1/local/projetos/{project_id}/topologia')
def save_topology(project_id: UUID, payload: SaveTopology, authorization: str | None = Header(default=None)):
    repo = _storage(authorization)
    try:
        return persist(repo, project_id, payload.document, payload.expected_revision)
    except ConflitoRevisao as exc:
        raise HTTPException(409, 'Revisão concorrente; reabra antes de salvar') from exc
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
