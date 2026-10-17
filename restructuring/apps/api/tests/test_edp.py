from decimal import Decimal
from sie_api.domain.edp import enquadrar_edp


def test_unverified_edp_catalog_selects_only_candidate_t2_for_583_a():
    result = enquadrar_edp("T", Decimal("58.3"), Decimal("22.215"), True)
    assert result["catalogo"]["status"] == "DOCUMENTADO_SEM_FONTE_PRIMARIA"
    assert result["catalogo"]["normative_conformity_verified"] is False
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


def test_edp_conservatively_blocks_ud_with_three_phase_load():
    for modalidade in ("U", "D"):
        result = enquadrar_edp(
            modalidade, Decimal("42"), Decimal("17"), True)
        assert "EDP-003" in {x["codigo"] for x in result["alertas"]}
        assert result["status_engenharia"] == "BLOQUEADO"
        assert result["liberado_para_padrao_entrada"] is False
        assert result["candidato_para_estudo"] is False


def test_edp_non_homologated_values_can_never_be_released():
    result = enquadrar_edp("U", Decimal("20"), Decimal("5"), False)
    assert result["catalogo"]["release_allowed"] is False
    assert result["catalogo"]["normative_conformity_verified"] is False
    assert result["regra_selecao"]["status"] == "DOCUMENTADO_SEM_FONTE_PRIMARIA"
    assert result["status_engenharia"] == "PENDENTE"
    assert result["liberado_para_padrao_entrada"] is False


def test_official_edp_document_location_is_not_cell_homologation():
    result = enquadrar_edp("T", Decimal("58.3"), Decimal("22.215"), True)
    record = result["catalogo"]
    assert record["url_fonte_edp"] == "https://www.edp.com.br/Ginp/Download/PT.DT.PDN.00068_V9.pdf"
    assert record["publicacao_portal"] == "2026-04-15"
    assert record["confirmacao_binaria_pdf"] is False
    assert record["normative_conformity_verified"] is False
    assert record["status"] == "DOCUMENTADO_SEM_FONTE_PRIMARIA"
    assert result["liberado_para_padrao_entrada"] is False
