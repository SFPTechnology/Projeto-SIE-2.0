"""API foundation. Engineering design decisions require validated reference data."""
from .demand_api import router as demand_router
import sqlite3
from decimal import Decimal
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, ConfigDict
from .application import analisar_circuito
from .analysis_contracts import AnaliseCircuito, Evidencia, LinhaCondutor
from .domain.edp import enquadrar_edp
from .edp_context import ContextoEDP, enquadrar_com_contexto
from .storage_api import router as storage_router
from .normative_api import router as normative_router
from .installation_api import router as installation_router
from .installation_storage_api import router as installation_storage_router
from .distributor_api_f09 import router as distributor_router_f09

app = FastAPI(title="SIE 2.0 - API modular", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_methods=["GET", "POST", "PUT"],
    allow_headers=["Content-Type", "Authorization"],
)
@app.middleware("http")
async def local_storage_boundary(request, call_next):
    if request.url.path.startswith("/api/v1/local/"):
        import os
        import ipaddress
        if os.environ.get("SIE_ENV", "dev") not in {"dev", "test"}:
            return JSONResponse(status_code=503, content={"detail": "Persistencia local desabilitada neste ambiente"})
        peer = request.client.host if request.client else ""
        try:
            local = ipaddress.ip_address(peer).is_loopback
        except ValueError:
            local = peer == "testclient"
        if not local:
            return JSONResponse(status_code=403, content={"detail": "Acesso somente local"})
    return await call_next(request)


@app.exception_handler(sqlite3.DatabaseError)
async def erro_armazenamento_seguro(request, exc):
    return JSONResponse(status_code=503, content={
        "detail": "Armazenamento indisponivel; nenhuma operacao confirmada"})


@app.exception_handler(RequestValidationError)
async def erro_validacao_seguro(request, exc):
    # Do not echo raw input/context: nonfinite floats cannot be serialized as JSON.
    return JSONResponse(status_code=422, content={"detail": [
        {"loc": error["loc"], "msg": error["msg"], "type": error["type"]}
        for error in exc.errors()
    ]})


from .load_survey_api import router as load_survey_router
from .topology_api import router as topology_router
from .conductor_api import router as conductor_router
from .protection_api import router as protection_router
app.include_router(protection_router)
app.include_router(conductor_router)
app.include_router(demand_router)
app.include_router(topology_router)
app.include_router(load_survey_router)
app.include_router(storage_router)
app.include_router(normative_router)
app.include_router(installation_router)
app.include_router(installation_storage_router)
app.include_router(distributor_router_f09)


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



class EnquadramentoEDP(BaseModel):
    model_config = ConfigDict(extra="forbid", allow_inf_nan=False)
    modalidade: str = Field(pattern="^[UDT]$")
    corrente_demanda_a: float = Field(gt=0)
    carga_instalada_kw: float = Field(gt=0)
    tem_carga_trifasica: bool = False
    contexto: ContextoEDP | None = None


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
        if payload.contexto is not None:
            return enquadrar_com_contexto(
                payload.modalidade, Decimal(str(payload.corrente_demanda_a)),
                Decimal(str(payload.carga_instalada_kw)), payload.tem_carga_trifasica,
                payload.contexto.model_dump(mode="json"))
        return enquadrar_edp(
            payload.modalidade,
            Decimal(str(payload.corrente_demanda_a)),
            Decimal(str(payload.carga_instalada_kw)),
            payload.tem_carga_trifasica,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

from .artifacts_api_f10 import router as artifacts_router_f10
app.include_router(artifacts_router_f10)
