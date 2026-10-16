"""F01: server-executed trace is immutable and never becomes a normative approval."""
from uuid import uuid4
import sqlite3

import pytest
from fastapi.testclient import TestClient

from sie_api.main import app
from sie_api.storage import ConflitoRevisao, RepositorioProjetos

client = TestClient(app)


def example():
    return {
        "corrente_a": 20, "comprimento_m": 30, "tensao_v": 220,
        "resistencia_ohm_km": 7.41, "fator_correcao": .8,
        "tabela_condutores": [{"secao_mm2": 2.5, "capacidade_a": 24},
                             {"secao_mm2": 4, "capacidade_a": 32}],
        "evidencia": {
            "documento": "Fonte declarada pelo cliente", "edicao": "test-only",
            "referencia": "VALORES FICTICIOS de teste", "dados_validados": True,
            "testes_independentes": True,
        },
    }


def test_trace_proves_algorithm_used_not_normative_rule(tmp_path):
    repo = RepositorioProjetos(tmp_path / "t.sqlite")
    pid = str(uuid4())
    rev = repo.salvar(pid, "Teste", {
        "circuitos": [{"nome": "Iluminacao", "corrente_a": 20,
                       "tensao_v": 220, "comprimento_m": 30}]}, 0)
    saved = repo.registrar_ensaio(pid, rev, "Iluminacao", example())
    assert len(saved["algorithm_ids_executed"]) == 3
    row = saved["values_actually_used_by_algorithm"]
    assert row["selected_input_row"]["indice_entrada"] == 1
    assert row["selected_input_row"]["secao_mm2"] == 4
    assert row["selected_input_row"]["capacidade_a"] == 32
    assert row["capacity_for_breaker_decision_a"] == 25.6
    assert row["source_classification"] == "CLIENT_SUPPLIED_UNVERIFIED_NOT_NORMATIVE_CELL"
    assert saved["normative_cells_used_verified"] == []

    assert set(saved["algorithm_function_source_sha256"]) == {
        "selecionar_condutor", "selecionar_disjuntor",
        "calcular_queda_tensao_monofasica"}
    assert all(len(h) == 64 for h in saved["algorithm_function_source_sha256"].values())
    assert saved["resultado"]["status_engenharia"] == "PENDENTE"
    assert saved["resultado"]["liberado_para_uso_normativo"] is False
    assert saved["normative_rule_ids_used_verified"] == []
    assert saved["normative_cells_used_verified"] == []
    assert saved["source_values_verified"] is False
    assert saved["release_allowed"] is False
    assert len(saved["hash_sha256"]) == 64
    assert repo.consultar_ensaio(pid, saved["id"]) == saved
    assert len(repo.listar_ensaios(pid, rev)) == 1
    repo.salvar(pid, "Teste v2", {"circuitos": [{"nome": "Nova"}]}, rev)
    assert repo.consultar_ensaio(pid, saved["id"]) == saved
    assert repo.carregar_revisao(pid, 1)["dados"]["circuitos"][0]["nome"] == "Iluminacao"


def test_refuse_stale_revision_and_unmatched_circuit(tmp_path):
    repo = RepositorioProjetos(tmp_path / "t.sqlite")
    pid = str(uuid4())
    repo.salvar(pid, "Teste", {"circuitos": [{"nome": "C1"}]}, 0)
    with pytest.raises(ValueError, match="ausente"):
        repo.registrar_ensaio(pid, 1, "C2", example())
    repo.salvar(pid, "Teste 2", {"circuitos": [{"nome": "C1"}]}, 1)
    with pytest.raises(ConflitoRevisao):
        repo.registrar_ensaio(pid, 1, "C1", example())
    assert repo.listar_ensaios(pid, 1) == []


def test_reject_input_mismatch_and_duplicate_name(tmp_path):
    repo = RepositorioProjetos(tmp_path / "t.sqlite")
    pid = str(uuid4())
    repo.salvar(pid, "Teste", {"circuitos": [{"nome": "C1", "corrente_a": 10}]}, 0)
    with pytest.raises(ValueError, match="incompatível"):
        repo.registrar_ensaio(pid, 1, "C1", example())
    pid2 = str(uuid4())
    repo.salvar(pid2, "B", {"circuitos": [{"nome": "C1"}, {"nome": "c1"}]}, 0)
    with pytest.raises(ValueError, match="ambiguamente"):
        repo.registrar_ensaio(pid2, 1, "C1", example())


def test_trace_triggers_prevent_mutations_and_digest_detects_tampering(tmp_path):
    repo = RepositorioProjetos(tmp_path / "t.sqlite")
    pid = str(uuid4())
    repo.salvar(pid, "Teste", {"circuitos": [{"nome": "C1"}]}, 0)
    result = repo.registrar_ensaio(pid, 1, "C1", example())
    with pytest.raises(sqlite3.IntegrityError):
        with repo._conectar() as db:
            db.execute("DELETE FROM ensaios_calculo WHERE id=?", (result["id"],))
    with pytest.raises(sqlite3.IntegrityError):
        with repo._conectar() as db:
            db.execute("UPDATE ensaios_calculo SET registro_json='{}' WHERE id=?", (result["id"],))
    with repo._conectar() as db:
        db.execute("DROP TRIGGER f01_ensaio_sem_update")
        db.execute("UPDATE ensaios_calculo SET registro_json='{}' WHERE id=?", (result["id"],))
    with pytest.raises(ValueError, match="Integridade"):
        repo.consultar_ensaio(pid, result["id"])


def test_http_trace_uses_same_token_and_rejects_claimed_approval(tmp_path, monkeypatch):
    token = "test-only-" + "c"*36
    monkeypatch.setenv("SIE_LOCAL_API_TOKEN", token)
    monkeypatch.setenv("SIE_LOCAL_DB_PATH", str(tmp_path / "api.sqlite"))
    pid = str(uuid4())
    url = f"/api/v1/local/projetos/{pid}"
    headers = {"Authorization": "Bearer " + token}
    assert client.put("/api/v1/local/projetos", headers=headers,
                      json={"id": pid, "nome": "Teste",
                            "dados": {"circuitos": [{"nome": "C1"}]},
                            "revisao_esperada": 0}).status_code == 200
    trace_url = url + "/revisoes/1/circuitos/C1/ensaios"
    assert client.post(trace_url, json=example()).status_code == 401
    assert client.post(trace_url, headers=headers,
                       json={**example(), "release_allowed": True}).status_code == 422
    res = client.post(trace_url, headers=headers, json=example())
    assert res.status_code == 200, res.text
    data = res.json()
    assert data["release_allowed"] is False
    assert data["normative_conformity_verified"] is False
    assert data["normative_rule_ids_used_verified"] == []
    read = client.get(url + "/ensaios/" + data["id"], headers=headers)
    assert read.status_code == 200
    assert read.json()["hash_sha256"] == data["hash_sha256"]
    listed = client.get(url + "/revisoes/1/ensaios", headers=headers)
    assert listed.status_code == 200
    assert listed.json()["ensaios"][0]["id"] == data["id"]
    assert client.get(url + "/revisoes/1/ensaios").status_code == 401
    assert client.get(url + "/ensaios/" + str(uuid4()), headers=headers).status_code == 404


def test_unverified_algorithms_are_not_accepted_as_normative_fixtures(tmp_path):
    repo = RepositorioProjetos(tmp_path / "t.sqlite")
    pid = str(uuid4())
    repo.salvar(pid, "Teste", {"circuitos": [{"nome": "C1"}]}, 0)
    trace = repo.registrar_ensaio(pid, 1, "C1", example())
    assert trace["calculation_trace_kind"].endswith("NOT_NORMATIVE_ATTESTATION")
    assert trace["normative_cells_used_verified"] == []
    assert trace["source_values_verified"] is False
