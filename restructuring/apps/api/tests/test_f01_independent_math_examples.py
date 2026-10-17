"""Independent arithmetic reference examples; NEVER ABNT/EDP normative fixtures.

Expectations are explicit mathematical derivations, not replayed engine snapshots.
Synthetic tables are deliberately fabricated and must NEVER populate normative data.
"""
from decimal import Decimal
from math import sqrt

import pytest

from sie_api.domain.engines import (
    calcular_queda_tensao_monofasica, calcular_queda_tensao_trifasica_resistiva,
    selecionar_condutor, selecionar_disjuntor,
)


def test_independent_resistive_single_phase_math_example():
    # Synthetic: ΔV = 2 x 0.030 km x 20 A x 7.41 ohm/km = 8.892 V => 8.89 V
    # Percentage = 8.892 / 220 x 100 = 4.041818... => 4.04 %
    result = calcular_queda_tensao_monofasica(
        Decimal("20"), Decimal("30"), Decimal("7.41"), Decimal("220")
    )
    assert result.queda_v == Decimal("8.89")
    assert result.queda_percentual == Decimal("4.04")


def test_independent_resistive_three_phase_math_example():
    # Synthetic: sqrt(3) x 0.1 km x 15 A x 1.25 ohm/km = 3.247595... V.
    # Rounded by the engine's declared 0.01 resolution.
    expected = round(sqrt(3) * .1 * 15 * 1.25, 2)
    result = calcular_queda_tensao_trifasica_resistiva(
        Decimal("15"), Decimal("100"), Decimal("1.25"), Decimal("400")
    )
    assert result.queda_v == Decimal(str(expected))
    assert result.queda_percentual == Decimal("0.81")


def test_independent_synthetic_capacity_and_breaker_inequality():
    # Base 24 A x .8 = 19.2 A insufficient for Ib=20 A.
    # Base 32 A x .8 = 25.6 A. Hypothetical 20 A nominal satisfies 20<=20<=25.6.
    condutor = selecionar_condutor(
        Decimal("20"), Decimal("0.8"),
        ((Decimal("2.5"), Decimal("24")), (Decimal("4"), Decimal("32"))),
    )
    assert condutor.secao_mm2 == Decimal("4")
    assert condutor.capacidade_corrigida_a == Decimal("25.60")
    disj = selecionar_disjuntor(
        Decimal("20"), condutor.capacidade_corrigida_a,
        (Decimal("16"), Decimal("20"), Decimal("25"), Decimal("32")),
    )
    assert disj.corrente_disjuntor_comercial_a == Decimal("20")


def test_independent_hypothetical_breaker_rejection():
    # Synthetic: 20 A would exceed the corrected 19.2 A capacity.
    with pytest.raises(ValueError, match="Iz"):
        selecionar_disjuntor(
            Decimal("20"), Decimal("19.2"), (Decimal("16"), Decimal("20"))
        )


def test_zero_length_drop_reference_is_exactly_zero():
    result = calcular_queda_tensao_monofasica(
        Decimal("20"), Decimal("0"), Decimal("7.41"), Decimal("220")
    )
    assert result.queda_v == Decimal("0.00")
    assert result.queda_percentual == Decimal("0.00")
