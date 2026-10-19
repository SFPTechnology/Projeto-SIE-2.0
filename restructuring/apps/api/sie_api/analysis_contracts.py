"""Contratos comuns para analise de circuito, usados pela API e auditoria local."""
from pydantic import BaseModel, ConfigDict, Field


class Evidencia(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, allow_inf_nan=False)
    documento: str = Field(min_length=1)
    edicao: str = Field(min_length=1)
    referencia: str = Field(min_length=1)
    dados_validados: bool = False
    testes_independentes: bool = False


class LinhaCondutor(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, allow_inf_nan=False)
    secao_mm2: float = Field(gt=0)
    capacidade_a: float = Field(gt=0)


class AnaliseCircuito(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, allow_inf_nan=False)
    corrente_a: float = Field(gt=0)
    comprimento_m: float = Field(ge=0)
    tensao_v: float = Field(gt=0)
    resistencia_ohm_km: float = Field(gt=0)
    fator_correcao: float = Field(gt=0, le=1)
    tabela_condutores: list[LinhaCondutor] = Field(min_length=1)
    evidencia: Evidencia
