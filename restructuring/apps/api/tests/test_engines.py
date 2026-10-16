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


@pytest.mark.parametrize("invalid", ["NaN", "Infinity", "-Infinity", "0", "-1"])
def test_breaker_catalog_rejects_invalid_items(invalid):
    with pytest.raises(ValueError):
        selecionar_disjuntor(Decimal("10"), Decimal("25"), (Decimal("16"), Decimal(invalid)))


def test_breaker_catalog_rejects_empty():
    with pytest.raises(ValueError):
        selecionar_disjuntor(Decimal("10"), Decimal("25"), ())


@pytest.mark.parametrize("invalid", ["NaN", "Infinity", "-Infinity", "0", "-1"])
def test_conductor_table_rejects_invalid_items_even_after_valid_candidate(invalid):
    with pytest.raises(ValueError):
        selecionar_condutor(
            Decimal("10"), Decimal("0.8"),
            ((Decimal("4"), Decimal("32")), (Decimal("6"), Decimal(invalid))),
        )


def test_conductor_table_rejects_duplicate_section():
    with pytest.raises(ValueError, match="duplicada"):
        selecionar_condutor(
            Decimal("10"), Decimal("0.8"),
            ((Decimal("4"), Decimal("32")), (Decimal("4"), Decimal("40"))),
        )


def test_conductor_table_rejects_empty():
    with pytest.raises(ValueError):
        selecionar_condutor(Decimal("10"), Decimal("0.8"), ())


def test_zero_length_single_phase_has_zero_drop():
    result = calcular_queda_tensao_monofasica(
        Decimal("20"), Decimal("0"), Decimal("7.41"), Decimal("220")
    )
    assert result.queda_v == Decimal("0.00")
    assert result.queda_percentual == Decimal("0.00")


def test_zero_length_three_phase_has_zero_drop():
    from sie_api.domain.engines import calcular_queda_tensao_trifasica_resistiva
    result = calcular_queda_tensao_trifasica_resistiva(
        Decimal("20"), Decimal("0"), Decimal("7.41"), Decimal("380")
    )
    assert result.queda_v == Decimal("0.00")
    assert result.queda_percentual == Decimal("0.00")


@pytest.mark.parametrize("invalid", ["NaN", "Infinity", "-Infinity", "-1"])
def test_voltage_drop_rejects_invalid_length(invalid):
    with pytest.raises(ValueError):
        calcular_queda_tensao_monofasica(
            Decimal("20"), Decimal(invalid), Decimal("7.41"), Decimal("220")
        )

@pytest.mark.parametrize("invalid", [None, "20", 20])
def test_non_decimal_input_fails_safely(invalid):
    with pytest.raises(ValueError):
        calcular_queda_tensao_monofasica(
            invalid, Decimal("30"), Decimal("7.41"), Decimal("220")
        )


def test_never_round_up_iz_before_breaker_decision():
    # Iz = 20 A * 0.9998 = 19.996 A; apparent 20.00 A is NOT available.
    corrente_projeto = Decimal("19.99")
    condutor = selecionar_condutor(
        corrente_projeto, Decimal("0.9998"),
        ((Decimal("4"), Decimal("20")),),
    )
    assert condutor.capacidade_corrigida_a == Decimal("19.9960")
    with pytest.raises(ValueError, match="Nenhum disjuntor"):
        selecionar_disjuntor(
            corrente_projeto, condutor.capacidade_corrigida_a,
            (Decimal("16"), Decimal("20")),
        )


def test_do_not_round_up_iz_even_when_decision_is_far_from_threshold():
    condutor = selecionar_condutor(
        Decimal("15"), Decimal("0.9998"),
        ((Decimal("4"), Decimal("20")),),
    )
    disjuntor = selecionar_disjuntor(
        Decimal("15"), condutor.capacidade_corrigida_a,
        (Decimal("16"), Decimal("20")),
    )
    assert disjuntor.corrente_disjuntor_comercial_a == Decimal("16.00")
