"""Contratos comuns para analise de circuito, usados pela API e auditoria local."""
from .protection_extended import ProtecaoCurtoCircuito, EstudoCoordenacao
from .voltage_checks import QuedaImpedancia

from pydantic import BaseModel, ConfigDict, Field, field_validator


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


class CondicoesCelulas(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, allow_inf_nan=False)
    material: str
    isolacao: str
    temperatura_condutor_c: int
    metodo_referencia: str
    metodo_instalacao: int
    descricao_instalacao: str = Field(min_length=1, max_length=1000)
    condutores_carregados: int
    meio: str
    temperatura_ambiente_c: int
    radiacao_solar: bool
    radiacao_infravermelha: bool
    circuitos_agrupados: int = Field(ge=1)
    agrupamento: str
    grupo_homogeneo: bool
    carga_uniforme: bool


class VinculoCelulas(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, allow_inf_nan=False)
    registro_revisao: str
    celulas_ids: list[str] = Field(min_length=1, max_length=8)
    condicoes: CondicoesCelulas


class FonteDispositivo(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, allow_inf_nan=False)
    documento: str = Field(min_length=1, max_length=500)
    revisao: str = Field(min_length=1, max_length=100)
    referencia: str = Field(min_length=1, max_length=500)
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    dispositivo_id: str = Field(min_length=1, max_length=200)


    @field_validator('documento', 'revisao', 'referencia', 'dispositivo_id')
    @classmethod
    def fonte_nao_vazia(cls, value):
        if not value.strip():
            raise ValueError('Identificação da fonte não pode ser vazia')
        return value.strip()


class ProtecaoSobrecarga(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, allow_inf_nan=False)
    corrente_nominal_a: float = Field(gt=0)
    corrente_atuacao_i2_a: float = Field(gt=0)
    fonte: FonteDispositivo
    duracao_sobrecarga_h_12_meses: float | None = Field(default=None, ge=0)
    duracao_sobrecarga_h_vida: float | None = Field(default=None, ge=0)


class AnaliseCircuito(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, allow_inf_nan=False)
    corrente_a: float = Field(gt=0)
    comprimento_m: float = Field(ge=0)
    tensao_v: float = Field(gt=0)
    resistencia_ohm_km: float = Field(gt=0)
    fator_correcao: float = Field(gt=0, le=1)
    tabela_condutores: list[LinhaCondutor] = Field(min_length=1)
    evidencia: Evidencia

    vinculo_celulas: VinculoCelulas | None = None
    protecao_sobrecarga: ProtecaoSobrecarga | None = None
    protecao_curto_circuito: ProtecaoCurtoCircuito | None = None
    estudo_coordenacao: EstudoCoordenacao | None = None
    queda_impedancia: QuedaImpedancia | None = None
