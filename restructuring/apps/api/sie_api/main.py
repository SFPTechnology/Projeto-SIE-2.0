"""API foundation. Engineering design decisions require validated reference data."""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, ConfigDict

app = FastAPI(title="SIE 2.0 - API modular", version="0.1.0")


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


@app.get("/api/v1/health")
def health():
    return {"status": "ok", "component": "api", "engineering_engine": "blocked_pending_validation"}


@app.post("/api/v1/projetos/validar")
def validar_projeto(projeto: Projeto):
    """Only validate project shape; does NOT assert ABNT compliance."""
    nomes = [c.nome.strip().casefold() for c in projeto.circuitos]
    if len(nomes) != len(set(nomes)):
        raise HTTPException(status_code=422, detail="Nomes de circuitos duplicados")
    return {"validacao_estrutural": "aprovada", "validacao_normativa": "nao_realizada", "circuitos": len(nomes)}
