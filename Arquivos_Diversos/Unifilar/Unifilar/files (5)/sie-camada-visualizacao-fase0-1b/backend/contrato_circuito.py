"""
SIE — Contrato de Circuito Canônico (PRD Camada de Visualização v1.0, Seção 5).

Abstração consumida pelas Camadas A (Fable 5) e B (SVG próprio).
Desacopla a Divisão de Circuitos (produtora futura) dos consumidores.

Disciplinas normativas embutidas:
- INC-01: va_total é VA direto — NUNCA dividido por FP neste contrato.
- INC-04: tensao_v ausente => None (nunca fallback silencioso para 127V).
- INC-07: secao_mm2, quando preenchida, DEVE pertencer à série IEC 60228.
- Rastreabilidade: fonte_linha / status_linha obrigatórios (evolução do C3).

Nenhum valor é recalculado aqui: a camada de visualização é projeção,
não recálculo (Seção 1.2 do PRD).
"""

from __future__ import annotations

from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------


class TipoCircuito(str, Enum):
    ILUMINACAO = "iluminacao"
    TUG = "tug"
    TUE = "tue"
    OUTRA = "outra"


class Fase(str, Enum):
    R = "R"
    S = "S"
    T = "T"


class GrupoEDP(str, Enum):
    """Grupos A–I da PT.DT.PDN.00068 v09. Forno elétrico => D, não E (INC-02)."""

    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"
    G = "G"
    H = "H"
    I = "I"


class StatusLinha(str, Enum):
    INFO = "INFO"
    ATENCAO = "ATENÇÃO"
    ERRO = "ERRO"


class EsquemaCC(str, Enum):
    """Ponto de extensão — revisão NBR 5410 (~fim 2026)."""

    SOLAR_FV = "solar_fv"
    BATERIA = "bateria"
    OUTRO = "outro"


# ---------------------------------------------------------------------------
# Série normalizada IEC 60228 (mm²) — validação INC-07
# ---------------------------------------------------------------------------

SERIE_IEC_60228_MM2: tuple[float, ...] = (
    0.5, 0.75, 1.0, 1.5, 2.5, 4.0, 6.0, 10.0, 16.0, 25.0, 35.0, 50.0,
    70.0, 95.0, 120.0, 150.0, 185.0, 240.0, 300.0, 400.0, 500.0, 630.0,
    800.0, 1000.0,
)

VERIFICAR = "[VERIFICAR]"


# ---------------------------------------------------------------------------
# Registro de derivação — Click-to-Trace (PRD 4.1)
# ---------------------------------------------------------------------------


class DerivacaoRegistro(BaseModel):
    """Registro que liga um elemento visual à regra e ao cálculo que o gerou."""

    model_config = ConfigDict(frozen=True)

    regra_id: str = Field(description="Id interno da regra, ex.: NBR5410-9.5.3.2")
    referencia_normativa: str = Field(description="Cláusula legível, ex.: 'NBR 5410:2004 §9.5.3.2'")
    formula: str = Field(description="Fórmula aplicada, ex.: 'IB = S / V'")
    entradas: dict[str, str | int | float | None] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Ponto de carga (entrada do adaptador; produzido pelo módulo IB hoje)
# ---------------------------------------------------------------------------


class PontoCarga(BaseModel):
    """Ponto de carga tal como o módulo IB o expõe. O adaptador 1:1 consome isto."""

    model_config = ConfigDict(frozen=True)

    id: str
    descricao: str
    tipo: TipoCircuito
    dependencia_id: str
    va: int = Field(gt=0, description="Potência aparente em VA — VA direto (INC-01)")
    tensao_v: Optional[int] = Field(
        default=None,
        description="Tensão declarada. None = pendente [VERIFICAR] (INC-04), nunca 127V implícito.",
    )
    corrente_ib_a: Optional[float] = Field(
        default=None,
        description="IB calculado pelo módulo IB (VA direto / V). None se tensão pendente.",
    )
    fases: tuple[Fase, ...] = Field(default=())
    grupo_edp: GrupoEDP
    zona_molhada: Optional[bool] = Field(
        default=None, description="None = classificação pendente (INC-03)"
    )
    tensao_resolvida_por_contrato: bool = Field(
        default=False,
        description=(
            "CONF-03: True quando a tensão veio do contrato de integração "
            "(Saída A, default ILU/TUG 127 V) e não de declaração explícita. "
            "Permitido só para ILU/TUG — o adaptador rejeita em TUE/outra (INC-04)."
        ),
    )

    @field_validator("tensao_v")
    @classmethod
    def _tensao_valida(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v not in (127, 220, 380):
            raise ValueError(f"Tensão {v}V fora do conjunto suportado (127/220/380).")
        return v


# ---------------------------------------------------------------------------
# Contrato de Circuito Canônico (Seção 5)
# ---------------------------------------------------------------------------


class CircuitoCanonico(BaseModel):
    """Schema canônico de circuito — consumido pelas Camadas A e B."""

    model_config = ConfigDict(frozen=True)

    id: str = Field(description="Ex.: ILUM-Dormitorio-1")
    tipo: TipoCircuito
    pontos: tuple[str, ...] = Field(min_length=1, description="Ids dos pontos servidos")
    dependencias: tuple[str, ...] = Field(min_length=1)
    va_total: int = Field(gt=0, description="Soma de VA dos pontos — VA direto, sem FP (INC-01)")
    tensao_v: Optional[int] = Field(
        default=None, description="None => [VERIFICAR], jamais 127V por fallback (INC-04)"
    )
    corrente_projeto_a: Optional[float] = Field(
        default=None, description="IB do módulo de cálculo; nunca recalculado pela visualização"
    )
    fases: tuple[Fase, ...] = Field(default=(), description="R|S|T; bifásico = 2 fases")
    requisito_dr: Optional[bool] = Field(
        default=None, description="None = pendente de classificação de zona molhada (INC-03)"
    )
    grupo_edp: GrupoEDP
    disjuntor_a: Optional[int] = Field(default=None, description="Aguarda módulo P1/proteção")
    secao_mm2: Optional[float] = Field(
        default=None, description="Aguarda P1/condutor; validada contra IEC 60228 (INC-07)"
    )
    fonte_linha: str = Field(description="Rastreabilidade normativa da linha de origem")
    status_linha: StatusLinha = Field(default=StatusLinha.INFO)
    provisorio: bool = Field(
        default=False,
        description="True quando produzido pelo adaptador 1:1 (árvore provisória — risco R-04)",
    )
    derivacao: Optional[DerivacaoRegistro] = Field(
        default=None, description="Registro click-to-trace do elemento (PRD 4.1)"
    )
    pendencias: tuple[str, ...] = Field(
        default=(), description="Mensagens [VERIFICAR] associadas ao circuito"
    )

    # --- Pontos de extensão: revisão NBR 5410 (~fim 2026) -----------------
    afdd: Optional[bool] = Field(default=None, description="Proteção contra falha de arco")
    esquema_cc: Optional[EsquemaCC] = Field(default=None, description="Circuito CC / solar")
    ponto_recarga_ve: Optional[bool] = Field(default=None, description="Recarga de veículo elétrico")
    ampacidade_revisada: Optional[float] = Field(
        default=None, description="Nova tabela de capacidade de corrente (rev. 2026)"
    )

    # --- Validações ---------------------------------------------------------

    @field_validator("secao_mm2")
    @classmethod
    def _secao_iec_60228(cls, v: Optional[float]) -> Optional[float]:
        """INC-07: rejeita seção fora da série normalizada IEC 60228."""
        if v is not None and v not in SERIE_IEC_60228_MM2:
            raise ValueError(
                f"Seção {v} mm² não pertence à série normalizada IEC 60228. "
                f"Valores válidos: {SERIE_IEC_60228_MM2}"
            )
        return v

    @field_validator("tensao_v")
    @classmethod
    def _tensao_valida(cls, v: Optional[int]) -> Optional[int]:
        if v is not None and v not in (127, 220, 380):
            raise ValueError(f"Tensão {v}V fora do conjunto suportado (127/220/380).")
        return v
