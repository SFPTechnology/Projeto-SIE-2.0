"""Local-only project persistence API, disabled until configured explicitly."""
import os
import secrets
from uuid import UUID
from typing import Any

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from .storage import ConflitoRevisao, RepositorioProjetos

router = APIRouter(prefix="/api/v1/local/projetos", tags=["Local project store"])


class SalvarProjeto(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: UUID
    nome: str = Field(min_length=1, max_length=160)
    dados: dict[str, Any]
    revisao_esperada: int = Field(ge=0)


def _storage(authorization: str | None) -> RepositorioProjetos:
    token = os.environ.get("SIE_LOCAL_API_TOKEN", "")
    caminho = os.environ.get("SIE_LOCAL_DB_PATH", "")
    if len(token) < 24 or not caminho:
        raise HTTPException(status_code=503, detail="Armazenamento local desabilitado")
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Credencial de acesso local obrigatoria")
    informado = authorization[len("Bearer "):]
    if not secrets.compare_digest(token, informado):
        raise HTTPException(status_code=401, detail="Credencial de acesso local invalida")
    return RepositorioProjetos(caminho)


@router.put("")
def salvar_projeto(payload: SalvarProjeto, authorization: str | None = Header(default=None)):
    repo = _storage(authorization)
    try:
        nova = repo.salvar(str(payload.id), payload.nome, payload.dados, payload.revisao_esperada)
    except ConflitoRevisao as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {"id": str(payload.id), "revisao": nova, "estado": "armazenado_localmente"}


@router.get("/{projeto_id}")
def carregar_projeto(projeto_id: UUID, authorization: str | None = Header(default=None)):
    repo = _storage(authorization)
    projeto = repo.carregar(str(projeto_id))
    if projeto is None:
        raise HTTPException(status_code=404, detail="Projeto nao encontrado")
    return projeto


@router.get("/{projeto_id}/historico")
def historico_projeto(projeto_id: UUID, authorization: str | None = Header(default=None)):
    repo = _storage(authorization)
    return {"id": str(projeto_id), "eventos": repo.historico(str(projeto_id))}


# Consultas locais somente leitura; token da mesma fronteira do armazenamento.
# Não concedem aprovação normativa, nem reconstroem snapshots legados ausentes.
@router.get("/{projeto_id}/snapshots-normativos/{revisao}")
def consultar_snapshot_normativo(
    projeto_id: UUID, revisao: int, authorization: str | None = Header(default=None)
):
    repo = _storage(authorization)
    try:
        snapshot = repo.snapshot_normativo(str(projeto_id), revisao)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    if snapshot is None:
        raise HTTPException(status_code=404, detail="Snapshot inexistente; revisao legada nao reconstruida")
    return snapshot


@router.get("/{projeto_id}/impacto-normativo/{revisao}")
def consultar_impacto_normativo(
    projeto_id: UUID, revisao: int, authorization: str | None = Header(default=None)
):
    repo = _storage(authorization)
    try:
        impacto = repo.impacto_normativo(str(projeto_id), revisao)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    if impacto is None:
        raise HTTPException(status_code=404, detail="Snapshot inexistente; sem comparacao historica segura")
    return impacto


@router.get("/{projeto_id}/historico-normativo")
def consultar_historico_normativo(
    projeto_id: UUID, authorization: str | None = Header(default=None)
):
    repo = _storage(authorization)
    return {"id": str(projeto_id), "eventos": repo.historico_snapshot_normativo(str(projeto_id)),
            "normative_conformity_verified": False}
