"""Opt-in local persistence using the existing immutable project revision store."""
from uuid import UUID
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from .installation_service import InstallationSnapshot
from .storage_api import _storage
from .storage import ConflitoRevisao

router = APIRouter(prefix='/api/v1/local/projetos', tags=['Canonical local snapshots'])


class SaveInstallation(BaseModel):
    model_config = ConfigDict(extra='forbid')
    nome: str = Field(min_length=1, max_length=160)
    snapshot: InstallationSnapshot
    revisao_esperada: int = Field(ge=0, strict=True)


def persist_snapshot(repo, project_id, request):
    if (request.snapshot.project_id != project_id or
            request.snapshot.revision != request.revisao_esperada + 1):
        raise ValueError('Modelo deve pertencer ao projeto e à próxima revisão esperada')
    previous = repo.carregar(str(project_id))
    data = {} if previous is None else dict(previous['dados'])
    data['installation_snapshot'] = request.snapshot.model_dump(mode='json')
    revision = repo.salvar(str(project_id), request.nome, data, request.revisao_esperada)
    return {'id': str(project_id), 'revisao': revision, 'snapshot_sha256': request.snapshot.snapshot_sha256}


@router.put('/{project_id}/modelo')
def save_installation(project_id: UUID, request: SaveInstallation,
                      authorization: str | None = Header(default=None)):
    repo = _storage(authorization)
    try:
        return persist_snapshot(repo, project_id, request)
    except ConflitoRevisao as exc:
        raise HTTPException(status_code=409, detail={'code': 'REVISION_CONFLICT', 'message': str(exc)}) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail={'code': 'SNAPSHOT_REFERENCE_INVALID', 'message': str(exc)}) from exc
