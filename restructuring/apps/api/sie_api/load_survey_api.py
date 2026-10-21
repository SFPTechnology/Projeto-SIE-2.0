from uuid import UUID
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from .load_survey import Survey, summarize, persist
from .storage_api import _storage
from .storage import ConflitoRevisao

router = APIRouter(tags=['Levantamento preliminar F04'])
class SaveSurvey(BaseModel):
    model_config = ConfigDict(extra='forbid')
    levantamento: Survey
    revisao_esperada: int = Field(ge=0, strict=True)

@router.post('/api/v1/levantamentos/validar')
def validate_survey(survey: Survey):
    return summarize(survey)

@router.put('/api/v1/local/projetos/{project_id}/levantamento')
def save_survey(project_id: UUID, payload: SaveSurvey, authorization: str | None = Header(default=None)):
    repo = _storage(authorization)
    try:
        return persist(repo, project_id, payload.levantamento, payload.revisao_esperada)
    except ConflitoRevisao as exc:
        raise HTTPException(409, 'Revisão alterada; reabra antes de salvar') from exc
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc
