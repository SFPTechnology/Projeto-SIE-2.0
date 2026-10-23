"""F09 tests assert consultative behavior, isolation, and fail-closed defaults."""
from decimal import Decimal
from fastapi.testclient import TestClient
import pytest

from sie_api.main import app
from sie_api.distributor_engine_f09 import diagnosticar_distribuidora
from sie_api.specialized_extensions_f09 import avaliar_extensao, catalogo_extensoes


def payload(distributor="EDP_SP", **context_changes):
    context = {
        "uf": "SP", "distribuidora": "EDP_SP", "area_concessao_confirmada": True,
        "rede": "AEREA_SECUNDARIA", "sistema": "ESTRELA",
        "tensao_fase_neutro_v": 127, "tensao_linha_v": 220, "frequencia_hz": 60,
        "data_referencia": "2026-10-20", "isolacao_entrada": "PVC",
        "possui_mmgd": False, "maior_motor_fn_cv": 0, "maior_motor_ff_cv": 0,
        "maior_motor_fff_cv": 0, "possui_cargas_especiais": False,
        **context_changes,
    }
    return {
        "distributor_id": distributor, "modality": "T", "demand_current_a": Decimal('50'),
        "installed_load_kw": Decimal('30'), "has_three_phase_load": False, "context": context,
    }


def test_known_edp_candidate_keeps_all_external_eligibility_gates_pending():
    result = diagnosticar_distribuidora(payload())
    assert result["status"] == "CANDIDATE_FOR_REVIEW"
    assert result["candidate"]["codigo"] == "T2"
    assert result["connection_release"] is False
    assert result["distributor_standard"]["edition"] == "09"
    assert result["distributor_standard"]["territory"] == {
        "uf": "SP", "network": "AEREA_SECUNDARIA"
    }
    assert {gate["id"] for gate in result["pending_gates"]} == {
        "territory_confirmed", "standard_current", "supply_conditions",
        "demand_and_metering", "entry_design", "protection_coordination",
        "distributor_process",
    }


def test_unsupported_distributor_never_inherits_edp_data():
    result = diagnosticar_distribuidora(payload("OTHER_DSO"))
    assert result["status"] == "PADRAO_NAO_CADASTRADO"
    assert result["candidate"] is None
    assert result["connection_release"] is False
    assert "nenhum dado EDP foi reutilizado" in result["alerts"][0]["message"]


def test_out_of_territory_and_special_loads_block_category_candidate():
    result = diagnosticar_distribuidora(payload("EDP_SP", uf="RJ", possui_cargas_especiais=True))
    assert result["status"] == "BLOCKED"
    assert result["candidate"] is None
    assert result["connection_release"] is False


def test_future_project_date_requires_catalog_refresh_before_category_suggestion():
    result = diagnosticar_distribuidora(payload("EDP_SP", data_referencia="2026-10-23"))
    assert result["candidate"] is None
    assert result["status"] == "BLOCKED"
    assert any(alert["codigo"] == "DISTRIBUTOR_SOURCE_REFRESH_REQUIRED" for alert in result["alertas"])


def test_http_routes_expose_source_scope_and_consultative_diagnostic():
    client = TestClient(app)
    registry = client.get("/api/v1/distribuidoras").json()
    assert registry["selection_requires_context"] is True
    assert len(registry["items"]) == 1
    api_payload = payload()
    api_payload['demand_current_a'] = 50
    api_payload['installed_load_kw'] = 30
    response = client.post("/api/v1/distribuidoras/enquadrar", json=api_payload)
    assert response.status_code == 200
    assert response.json()["connection_release"] is False
    api_payload['distributor_id'] = 'OTHER_DSO'
    assert client.post("/api/v1/distribuidoras/enquadrar", json=api_payload).json()["candidate"] is None


def test_specialized_extensions_are_optional_and_never_release_calculations():
    registry = catalogo_extensoes()
    assert len(registry) == 4
    assert all(item["optional"] and not item["release"] for item in registry)
    spda = avaliar_extensao({"extension_id": "SPDA", "applicable": True, "context": {}})
    assert spda["standard"].startswith("ABNT NBR 5419")
    assert spda["engine_status"] == "NOT_CONFIGURED"
    assert spda["release"] is False
    not_applicable = avaliar_extensao({"extension_id": "EV_CHARGING", "applicable": False})
    assert not_applicable["status"] == "NOT_APPLICABLE_BY_DECLARATION"
    assert not_applicable["release"] is False


def test_extension_contract_rejects_unknown_domain_instead_of_fallback():
    with pytest.raises(Exception):
        avaliar_extensao({"extension_id": "GENERIC", "applicable": True})
