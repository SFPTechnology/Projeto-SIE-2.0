"""F01: triagem normativa, fronteira HTTP e prevenção de aprovação falsa."""
from datetime import date
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sie_api.domain.normative import RECORDS, Context, inspect_record
from sie_api.normative_api import router

app = FastAPI()
app.include_router(router)
client = TestClient(app)
BASE = {"typology": "residencial", "uf": "SP", "voltage_v": 220,
        "reference_date": "2026-10-15", "distributor": "EDP_SP"}

def _rules(payload=BASE):
    response = client.post("/api/v1/normas/aplicabilidade", json=payload)
    assert response.status_code == 200, response.text
    return {r["rule_id"]: r for r in response.json()["rules"]}

def test_catalog_remains_unverified():
    data = client.get("/api/v1/normas/catalogo").json()
    assert data["release_allowed"] is False
    assert data["normative_conformity_verified"] is False
    assert len(data["sources"]) == 8
    assert {x["data_status"] for x in data["sources"]} == {"NAO_VERIFICADA"}

def test_all_matched_sources_are_blocked():
    assert all(r["status"] == "BLOQUEADO" for r in _rules().values() if r["status"] != "NAO_APLICAVEL")
    assert all(not r["normative_approved"] for r in _rules().values())

def test_unknown_evidence_flags_are_rejected():
    for name in ("approved", "verified", "source_verified", "approver", "normative_approved", "release_allowed"):
        r = client.post("/api/v1/normas/aplicabilidade", json={**BASE, name: True})
        assert r.status_code == 422, name

def test_wrong_typology_rejected_at_api_boundary():
    r = client.post("/api/v1/normas/aplicabilidade", json={**BASE, "typology": "industrial"})
    assert r.status_code == 422

def test_invalid_voltage_rejected():
    for voltage in (0, -1, 100001):
        assert client.post("/api/v1/normas/aplicabilidade", json={**BASE, "voltage_v": voltage}).status_code == 422

def test_date_is_required():
    payload = dict(BASE)
    payload.pop("reference_date")
    assert client.post("/api/v1/normas/aplicabilidade", json=payload).status_code == 422

def test_wrong_uf_excludes_edp():
    results = _rules({**BASE, "uf": "RJ"})
    assert results["EDP-SP-PTDT00068-V09"]["status"] == "NAO_APLICAVEL"

def test_wrong_distributor_excludes_edp():
    assert _rules({**BASE, "distributor": "OUTRA"})["EDP-SP-PTDT00068-V09"]["status"] == "NAO_APLICAVEL"

def test_missing_distributor_is_pending():
    assert _rules({**BASE, "distributor": None})["EDP-SP-PTDT00068-V09"]["status"] == "PENDENTE"

def test_nr10_future_is_excluded_in_2026():
    assert _rules()["NR-10-A-PARTIR-2027"]["status"] == "NAO_APLICAVEL"

def test_nr10_old_is_excluded_after_transition():
    results = _rules({**BASE, "reference_date": "2027-06-02"})
    assert results["NR-10-ATE-2027"]["status"] == "PENDENTE"
    assert results["NR-10-A-PARTIR-2027"]["status"] == "BLOQUEADO"

def test_stateless_immutable_registry():
    original = RECORDS[0]
    _rules({**BASE, "use": "spda", "material": "aluminio", "installation_method": "B1"})
    assert RECORDS[0] == original
    assert inspect_record(original, Context("residencial", "SP", 220.0, date(2026,10,15)))["normative_approved"] is False

def test_main_application_mounts_routes():
    # Isolar inspeção porque outros testes podem manipular módulos FastAPI em sys.modules.
    import importlib
    import sie_api.main as main_module
    integrated_app = importlib.reload(main_module).app
    routes = {getattr(route, "path", "") for route in integrated_app.routes}
    assert "/api/v1/normas/aplicabilidade" in routes, sorted(routes)
    assert "/api/v1/circuitos/analisar" in routes
