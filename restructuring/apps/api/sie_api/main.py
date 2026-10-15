"""API foundation. Engineering design decisions require validated reference data."""
from decimal import Decimal
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, ConfigDict
from .application import analisar_circuito
from .domain.edp import enquadrar_edp
from .storage_api import router as storage_router
from .normative_api import router as normative_router

app = FastAPI(title="SIE 2.0 - API modular", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_methods=["GET", "POST", "PUT"],
    allow_headers=["Content-Type", "Authorization"],
)
app.include_router(storage_router)
app.include_router(normative_router)


class Circuito(BaseModel):
    model_config = ConfigDict(extra="forbid")
    nome: str = Field(min_length=1, max_length=120)
    corrente_a: float = Field(gt=0, le=10000)
    comprimento_m: float = Field(ge=0, le=100000)
    tensao_v: float = Field(gt=0, le=100000)


class Projeto(BaseModel):
    model_config = ConfigDict(extra="forbid")
    nome: str = Field(min_length=1, max_length=160)
    circuitos: list[Circuito] = Field(default_factory=list)


class Evidencia(BaseModel):
    model_config = ConfigDict(extra="forbid")
    documento: str = Field(min_length=1)
    edicao: str = Field(min_length=1)
    referencia: str = Field(min_length=1)
    dados_validados: bool = False
    testes_independentes: bool = False


class LinhaCondutor(BaseModel):
    secao_mm2: float = Field(gt=0)
    capacidade_a: float = Field(gt=0)


class AnaliseCircuito(BaseModel):
    model_config = ConfigDict(extra="forbid")
    corrente_a: float = Field(gt=0)
    comprimento_m: float = Field(ge=0)
    tensao_v: float = Field(gt=0)
    resistencia_ohm_km: float = Field(gt=0)
    fator_correcao: float = Field(gt=0, le=1)
    tabela_condutores: list[LinhaCondutor] = Field(min_length=1)
    evidencia: Evidencia


class EnquadramentoEDP(BaseModel):
    model_config = ConfigDict(extra="forbid")
    modalidade: str = Field(pattern="^[UDT]$")
    corrente_demanda_a: float = Field(gt=0)
    carga_instalada_kw: float = Field(gt=0)
    tem_carga_trifasica: bool = False


@app.get("/api/v1/health")
def health():
    return {"status": "ok", "component": "api", "engineering_engine": "calculation_available_normative_release_disabled", "version": app.version}


@app.post("/api/v1/projetos/validar")
def validar_projeto(projeto: Projeto):
    """Only validate project shape; does NOT assert ABNT compliance."""
    nomes = [c.nome.strip().casefold() for c in projeto.circuitos]
    if len(nomes) != len(set(nomes)):
        raise HTTPException(status_code=422, detail="Nomes de circuitos duplicados")
    return {"validacao_estrutural": "aprovada", "validacao_normativa": "nao_realizada", "circuitos": len(nomes)}


@app.post("/api/v1/circuitos/analisar")
def analisar(payload: AnaliseCircuito):
    try:
        return analisar_circuito(payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc


@app.post("/api/v1/edp/enquadrar")
def enquadrar_edp_endpoint(payload: EnquadramentoEDP):
    try:
        return enquadrar_edp(
            payload.modalidade,
            Decimal(str(payload.corrente_demanda_a)),
            Decimal(str(payload.carga_instalada_kw)),
            payload.tem_carga_trifasica,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
