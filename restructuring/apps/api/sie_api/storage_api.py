"""Local-only project persistence API, disabled until configured explicitly."""
import os
import secrets
from uuid import UUID
from typing import Any

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, ConfigDict, Field

from .storage import ConflitoRevisao, RepositorioProjetos
from .analysis_contracts import AnaliseCircuito

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


@router.get("/{projeto_id}/revisoes")
def consultar_revisoes(projeto_id: UUID, authorization: str | None = Header(default=None)):
    repo = _storage(authorization)
    if repo.carregar(str(projeto_id)) is None:
        raise HTTPException(status_code=404, detail="Projeto nao encontrado")
    return {"id": str(projeto_id), "revisoes": repo.listar_revisoes(str(projeto_id)),
            "versoes_legadas_sem_backfill": True,
            "normative_conformity_verified": False}


@router.get("/{projeto_id}/revisoes/{revisao}")
def consultar_revisao_historica(
    projeto_id: UUID, revisao: int, authorization: str | None = Header(default=None)
):
    repo = _storage(authorization)
    try:
        item = repo.carregar_revisao(str(projeto_id), revisao)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    if item is None:
        raise HTTPException(status_code=404,
                            detail="Revisao anterior nao armazenada; sem reconstrução artificial")
    return item


@router.post("/{projeto_id}/revisoes/{revisao}/circuitos/{circuito_nome}/ensaios")
def executar_ensaio_circuito(
    projeto_id: UUID, revisao: int, circuito_nome: str, payload: AnaliseCircuito,
    authorization: str | None = Header(default=None),
):
    """Motor executado no servidor; formula rastreavel, SEM homologacao normativa."""
    repo = _storage(authorization)
    try:
        return repo.registrar_ensaio(str(projeto_id), revisao,
                                     circuito_nome, payload.model_dump(mode="json"))
    except ConflitoRevisao as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except (ValueError, TypeError, KeyError, ArithmeticError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@router.get("/{projeto_id}/revisoes/{revisao}/ensaios")
def listar_ensaios_circuitos(
    projeto_id: UUID, revisao: int, authorization: str | None = Header(default=None),
):
    repo = _storage(authorization)
    try:
        return {"id": str(projeto_id), "revisao": revisao,
                "ensaios": repo.listar_ensaios(str(projeto_id), revisao),
                "normative_conformity_verified": False}
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@router.get("/{projeto_id}/ensaios/{ensaio_id}")
def consultar_ensaio_circuito(
    projeto_id: UUID, ensaio_id: UUID, authorization: str | None = Header(default=None),
):
    repo = _storage(authorization)
    try:
        ensaio = repo.consultar_ensaio(str(projeto_id), str(ensaio_id))
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    if ensaio is None:
        raise HTTPException(status_code=404, detail="Ensaio inexistente")
    return ensaio
