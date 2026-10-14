"""Deterministic electrical calculation primitives.

These formulas are engineering calculations, not a substitute for a normative
design review.  Each result carries its assumptions and is released only when
the normative evidence gate is explicitly approved by the caller.
"""
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP

Q = Decimal("0.01")


def _positive(value: Decimal, name: str) -> None:
    if not value.is_finite() or value <= 0:
        raise ValueError(f"{name} deve ser positivo e finito")


def _round(value: Decimal) -> Decimal:
    return value.quantize(Q, rounding=ROUND_HALF_UP)


@dataclass(frozen=True)
class QuedaTensaoResultado:
    queda_v: Decimal
    queda_percentual: Decimal
    formula: str


def calcular_queda_tensao_monofasica(
    corrente_a: Decimal, comprimento_m: Decimal, resistencia_ohm_km: Decimal, tensao_v: Decimal
) -> QuedaTensaoResultado:
    """ΔV = 2 · L(km) · I · R, for a purely resistive single-phase model."""
    _positive(corrente_a, "corrente")
    _positive(comprimento_m, "comprimento")
    _positive(resistencia_ohm_km, "resistencia")
    _positive(tensao_v, "tensao")
    queda = Decimal("2") * (comprimento_m / Decimal("1000")) * corrente_a * resistencia_ohm_km
    return QuedaTensaoResultado(_round(queda), _round(queda * Decimal("100") / tensao_v), "2 × L(km) × I × R")


@dataclass(frozen=True)
class DisjuntorResultado:
    corrente_projeto_a: Decimal
    corrente_disjuntor_minima_a: Decimal
    corrente_disjuntor_comercial_a: Decimal
    criterio: str


def selecionar_disjuntor(
    corrente_projeto_a: Decimal, corrente_condutor_corrigida_a: Decimal, catalogo_a: tuple[Decimal, ...]
) -> DisjuntorResultado:
    """Selects the smallest catalog value satisfying Ib ≤ In ≤ Iz."""
    _positive(corrente_projeto_a, "corrente de projeto")
    _positive(corrente_condutor_corrigida_a, "corrente do condutor")
    if corrente_projeto_a > corrente_condutor_corrigida_a:
        raise ValueError("Ib excede Iz; aumente o condutor ou reduza a carga")
    validos = sorted({x for x in catalogo_a if x >= corrente_projeto_a and x <= corrente_condutor_corrigida_a})
    if not validos:
        raise ValueError("Nenhum disjuntor comercial atende Ib ≤ In ≤ Iz")
    return DisjuntorResultado(_round(corrente_projeto_a), _round(corrente_projeto_a), _round(validos[0]), "Ib ≤ In ≤ Iz")


@dataclass(frozen=True)
class CondutorResultado:
    secao_mm2: Decimal
    capacidade_corrigida_a: Decimal
    fator_correcao: Decimal
    criterio: str


def selecionar_condutor(
    corrente_projeto_a: Decimal, fator_correcao: Decimal, tabela: tuple[tuple[Decimal, Decimal], ...]
) -> CondutorResultado:
    """Selects the smallest section where Iz_base × factor ≥ Ib."""
    _positive(corrente_projeto_a, "corrente de projeto")
    _positive(fator_correcao, "fator de correcao")
    if fator_correcao > Decimal("1"):
        raise ValueError("Fator de correcao não pode exceder 1 neste motor")
    candidatos = []
    for secao, capacidade in tabela:
        _positive(secao, "secao")
        _positive(capacidade, "capacidade")
        corrigida = capacidade * fator_correcao
        if corrigida >= corrente_projeto_a:
            candidatos.append((secao, corrigida))
    if not candidatos:
        raise ValueError("Tabela informada não possui seção suficiente")
    secao, capacidade = min(candidatos, key=lambda item: item[0])
    return CondutorResultado(_round(secao), _round(capacidade), _round(fator_correcao), "Iz_base × fatores ≥ Ib")
