"""F01: triagem normativa, fronteira HTTP e prevenção de aprovação falsa."""
from datetime import date
from fastapi.testclient import TestClient
from sie_api.domain.normative import RECORDS, Context, inspect_record
from sie_api.main import app

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
    # Testar por HTTP evita assumir detalhes internos de _IncludedRouter (FastAPI 0.143+).
    assert client.get("/api/v1/normas/catalogo").status_code == 200
    assert client.get("/api/v1/health").status_code == 200
    assert client.post("/api/v1/normas/aplicabilidade", json=BASE).status_code == 200


def test_versioned_registry_is_independent_from_code_and_unapproved():
    from importlib.resources import files
    import json
    from sie_api.domain.normative import load_registry
    source = files("sie_api").joinpath("data", "normative_registry.json")
    manifest = json.loads(source.read_text(encoding="utf-8"))
    records = load_registry()
    assert manifest["schema_version"] == 1
    assert manifest["registry_state"] == "NAO_HOMOLOGADO"
    assert len(records) == len(manifest["records"]) == 8
    assert len(set(r.id for r in records)) == len(records)
    assert all(r.revision >= 1 and r.verified_data is False for r in records)
    assert all("revision" in r for r in _rules().values())

def test_edp_edition_published_after_reference_date_requires_review():
    earlier = _rules({**BASE, "reference_date": "2026-03-01"})
    item = earlier["EDP-SP-PTDT00068-V09"]
    assert item["status"] == "PENDENTE"
    assert "EDICAO_PUBLICADA_APOS_DATA_REFERENCIA" in item["reasons"]
    assert item["normative_approved"] is False

def test_edp_official_publication_metadata_not_equivalent_to_approval():
    registry = {r.id: r for r in RECORDS}
    edp = registry["EDP-SP-PTDT00068-V09"]
    assert edp.revision == 2
    assert edp.official_publication_date == date(2026, 4, 15)
    assert edp.official_url == "https://www.edp.com.br/normas-e-padroes-tecnicos/"
    assert edp.verified_data is False


def test_nr10_portaria_737_2026_only_has_narrow_10_6_4_e_transition():
    # Fonte: Portaria MTE 737/2026, arts. 3 e 5 (publicacao 01/06/2026).
    # A nova redacao geral entra em vigor em 01/06/2027; instalacoes
    # existentes nessa data recebem 1 ano a mais somente para 10.6.4(e).
    base = {**BASE, "reference_date": "2027-06-02"}
    existing = _rules({**base, "existing_installation_on_2027_06_01": True})
    assert existing["NR-10-ATE-2027"]["status"] == "PENDENTE"
    new_rule = existing["NR-10-A-PARTIR-2027"]
    assert new_rule["status"] == "BLOQUEADO"
    assert "10_6_4_E_PRAZO_ESPECIFICO_INSTALACAO_EXISTENTE_ATE_2028_05_31" in new_rule["reasons"]
    assert new_rule["normative_approved"] is False

    new_install = _rules({**base, "existing_installation_on_2027_06_01": False})
    assert new_install["NR-10-ATE-2027"]["status"] == "NAO_APLICAVEL"
    assert "10_6_4_E_PRAZO_ESPECIFICO_INSTALACAO_EXISTENTE_ATE_2028_05_31" not in new_install["NR-10-A-PARTIR-2027"]["reasons"]

    unknown = _rules(base)
    assert "10_6_4_E_EXISTENCIA_EM_2027_A_CONFERIR" in unknown["NR-10-A-PARTIR-2027"]["reasons"]


def test_nr10_transition_specific_deadline_expired_after_2028_06_01():
    for reference in ("2028-06-01", "2029-01-01"):
        x = _rules({**BASE, "reference_date": reference,
                    "existing_installation_on_2027_06_01": True})
        assert x["NR-10-ATE-2027"]["status"] == "NAO_APLICAVEL"
        assert x["NR-10-A-PARTIR-2027"]["status"] == "BLOQUEADO"
        assert "10_6_4_E_PRAZO_ESPECIFICO_INSTALACAO_EXISTENTE_ATE_2028_05_31" not in x["NR-10-A-PARTIR-2027"]["reasons"]


def test_nr10_effective_date_boundary_is_exact():
    previous = _rules({**BASE, "reference_date": "2027-05-31"})
    assert previous["NR-10-ATE-2027"]["status"] == "BLOQUEADO"
    assert previous["NR-10-A-PARTIR-2027"]["status"] == "NAO_APLICAVEL"
    starts = _rules({**BASE, "reference_date": "2027-06-01",
                     "existing_installation_on_2027_06_01": True})
    assert starts["NR-10-A-PARTIR-2027"]["status"] == "BLOQUEADO"
    assert starts["NR-10-ATE-2027"]["status"] == "PENDENTE"


def test_nr10_installation_existing_field_rejects_string_and_flag_injection():
    bad = _rules({**BASE, "existing_installation_on_2027_06_01": True})
    assert bad["NR-10-A-PARTIR-2027"]["normative_approved"] is False
    payload = {**BASE, "existing_installation_on_2027_06_01": "false"}
    # Pydantic bool coercion is permitted, but must never approve any rule.
    x = client.post("/api/v1/normas/aplicabilidade", json=payload)
    assert x.status_code == 200
    assert x.json()["release_allowed"] is False
