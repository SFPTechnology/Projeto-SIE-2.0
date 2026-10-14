from decimal import Decimal
from sie_api.domain.edp import enquadrar_edp


def test_verified_edp_catalog_selects_t2_for_583_a():
    result = enquadrar_edp("T", Decimal("58.3"), Decimal("22.215"), True)
    assert result["catalogo"]["status"] == "VERIFICADO"
    assert result["categoria"]["codigo"] == "T2"
    assert result["categoria"]["disjuntor_entrada_a"] == 63
    assert result["candidato_para_estudo"] is True
    assert result["status_engenharia"] == "PENDENTE"
    assert result["liberado_para_padrao_entrada"] is False


def test_edp_blocks_t_without_declared_three_phase_load():
    result = enquadrar_edp("T", Decimal("58.3"), Decimal("22.215"), False)
    assert result["liberado_para_padrao_entrada"] is False
    assert result["alertas"][0]["codigo"] == "EDP-002"


def test_edp_blocks_secondary_supply_above_75_kw():
    result = enquadrar_edp("D", Decimal("80"), Decimal("75.01"), False)
    assert result["liberado_para_padrao_entrada"] is False
    assert result["alertas"][0]["codigo"] == "EDP-001"


def test_edp_rejects_non_finite_values():
    import pytest
    for invalid in ("NaN", "Infinity", "-Infinity"):
        with pytest.raises(ValueError):
            enquadrar_edp("U", Decimal(invalid), Decimal("12"), False)
