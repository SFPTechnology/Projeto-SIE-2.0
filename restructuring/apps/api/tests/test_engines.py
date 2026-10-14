from decimal import Decimal
import pytest
from sie_api.domain.engines import calcular_queda_tensao_monofasica, selecionar_condutor, selecionar_disjuntor


def test_voltage_drop_single_phase_is_traceable():
    result = calcular_queda_tensao_monofasica(Decimal("20"), Decimal("30"), Decimal("7.41"), Decimal("220"))
    assert result.queda_v == Decimal("8.89")
    assert result.queda_percentual == Decimal("4.04")


def test_selects_smallest_sufficient_conductor():
    result = selecionar_condutor(Decimal("20"), Decimal("0.8"), ((Decimal("2.5"), Decimal("24")), (Decimal("4"), Decimal("32"))))
    assert result.secao_mm2 == Decimal("4.00")


def test_breaker_must_stay_below_corrected_conductor_capacity():
    result = selecionar_disjuntor(Decimal("20"), Decimal("25"), (Decimal("16"), Decimal("20"), Decimal("25"), Decimal("32")))
    assert result.corrente_disjuntor_comercial_a == Decimal("20.00")


def test_breaker_rejects_unsafe_relation():
    with pytest.raises(ValueError):
        selecionar_disjuntor(Decimal("32"), Decimal("25"), (Decimal("32"),))


def test_three_phase_resistive_drop_has_explicit_assumptions():
    from sie_api.domain.engines import calcular_queda_tensao_trifasica_resistiva
    resultado = calcular_queda_tensao_trifasica_resistiva(
        Decimal("20"), Decimal("30"), Decimal("7.41"), Decimal("380")
    )
    assert resultado.queda_v == Decimal("7.70")
    assert resultado.queda_percentual == Decimal("2.03")
    assert "cos(phi)=1" in resultado.formula


def test_three_phase_drop_increases_with_length():
    from sie_api.domain.engines import calcular_queda_tensao_trifasica_resistiva
    curto = calcular_queda_tensao_trifasica_resistiva(
        Decimal("20"), Decimal("30"), Decimal("7.41"), Decimal("380")
    )
    longo = calcular_queda_tensao_trifasica_resistiva(
        Decimal("20"), Decimal("60"), Decimal("7.41"), Decimal("380")
    )
    assert longo.queda_v == curto.queda_v * 2


def test_three_phase_drop_rejects_non_finite_input():
    from sie_api.domain.engines import calcular_queda_tensao_trifasica_resistiva
    with pytest.raises(ValueError):
        calcular_queda_tensao_trifasica_resistiva(
            Decimal("NaN"), Decimal("30"), Decimal("7.41"), Decimal("380")
        )
