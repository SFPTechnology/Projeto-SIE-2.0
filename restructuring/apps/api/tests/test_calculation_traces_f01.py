"""F01: server-executed trace is immutable and never becomes a normative approval."""
from uuid import uuid4
import sqlite3
from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from sie_api.main import app
from sie_api.storage import ConflitoRevisao, RepositorioProjetos

client = TestClient(app)


@pytest.mark.parametrize('field,value', [
    ('corrente_a', 21), ('tensao_v', 230), ('comprimento_m', 31),
    ('fator_correcao', .9), ('resistencia_ohm_km', 8),
    ('tabela_condutores', [{'secao_mm2': 2.5, 'capacidade_a': 40},
                           {'secao_mm2': 4, 'capacidade_a': 45}]),
    ('evidencia', {'documento': 'outra origem', 'edicao': 'test-only',
                   'referencia': 'VALORES FICTICIOS de teste',
                   'dados_validados': True, 'testes_independentes': True}),
])
def test_every_consumed_input_must_match_saved_revision(tmp_path, monkeypatch, field, value):
    import sie_api.storage as storage
    repo = RepositorioProjetos(tmp_path / 'bound.sqlite')
    pid = str(uuid4())
    repo.salvar(pid, 'Teste', {'circuitos': [{'nome': 'C1', **example()}]}, 0)
    payload = deepcopy(example())
    payload[field] = value
    calls = []
    monkeypatch.setattr(storage, 'analisar_circuito', lambda _: calls.append('executed'))
    with pytest.raises(ValueError, match='incompatível'):
        repo.registrar_ensaio(pid, 1, 'C1', payload)
    assert calls == []
    assert repo.listar_ensaios(pid, 1) == []


@pytest.mark.parametrize('field', [
    'corrente_a', 'tensao_v', 'comprimento_m', 'fator_correcao',
    'resistencia_ohm_km', 'tabela_condutores', 'evidencia',
])
def test_incomplete_legacy_circuit_is_readable_but_new_trace_blocked(tmp_path, monkeypatch, field):
    import sie_api.storage as storage
    repo = RepositorioProjetos(tmp_path / 'legacy.sqlite')
    pid = str(uuid4())
    circuit = {'nome': 'C1', **example()}
    del circuit[field]
    repo.salvar(pid, 'Legado', {'circuitos': [circuit]}, 0)
    before = repo.carregar_revisao(pid, 1)
    calls = []
    monkeypatch.setattr(storage, 'analisar_circuito', lambda _: calls.append('executed'))
    with pytest.raises(ValueError, match='Circuito salvo incompleto ou inválido'):
        repo.registrar_ensaio(pid, 1, 'C1', example())
    assert calls == []
    assert repo.carregar_revisao(pid, 1) == before
    assert repo.carregar(pid)['dados']['circuitos'] == [circuit]
    assert repo.listar_ensaios(pid, 1) == []


def test_calculation_uses_immutable_revision_not_mutable_current_copy(tmp_path):
    import json
    repo = RepositorioProjetos(tmp_path / 'immutable.sqlite')
    pid = str(uuid4())
    original = {'circuitos': [{'nome': 'C1', **example()}]}
    repo.salvar(pid, 'Teste', original, 0)
    mutated = deepcopy(original)
    mutated['circuitos'][0]['fator_correcao'] = .9
    with repo._conectar() as db:
        db.execute('UPDATE projetos SET dados_json=? WHERE id=?', (json.dumps(mutated), pid))
    trace = repo.registrar_ensaio(pid, 1, 'C1', example())
    assert trace['entrada']['fator_correcao'] == .8
    assert trace['entrada'] == example()
    with pytest.raises(ValueError, match='incompatível'):
        repo.registrar_ensaio(pid, 1, 'C1', {**example(), 'fator_correcao': .9})


def test_corrupt_revision_is_rejected_before_calculation(tmp_path, monkeypatch):
    import sie_api.storage as storage
    repo = RepositorioProjetos(tmp_path / 'tamper.sqlite')
    pid = str(uuid4())
    repo.salvar(pid, 'Teste', {'circuitos': [{'nome': 'C1', **example()}]}, 0)
    with repo._conectar() as db:
        db.execute('DROP TRIGGER f01_versao_sem_update')
        db.execute("UPDATE versoes_projeto SET dados_json='{}' WHERE projeto_id=?", (pid,))
    calls = []
    monkeypatch.setattr(storage, 'analisar_circuito', lambda _: calls.append('executed'))
    with pytest.raises(ValueError, match='Integridade da revisao historica'):
        repo.registrar_ensaio(pid, 1, 'C1', example())
    assert calls == []
    assert repo.listar_ensaios(pid, 1) == []


@pytest.mark.parametrize('path,value', [
    (('tabela_condutores', 0, 'secao_mm2'), 3),
    (('tabela_condutores', 1, 'capacidade_a'), 33),
    (('evidencia', 'edicao'), 'outra-edicao'),
    (('evidencia', 'referencia'), 'outra-referencia'),
    (('evidencia', 'dados_validados'), False),
    (('evidencia', 'testes_independentes'), False),
])
def test_nested_table_and_evidence_mutations_are_rejected(tmp_path, path, value):
    repo = RepositorioProjetos(tmp_path / 'nested.sqlite')
    pid = str(uuid4())
    repo.salvar(pid, 'Teste', {'circuitos': [{'nome': 'C1', **example()}]}, 0)
    changed = deepcopy(example())
    node = changed
    for key in path[:-1]:
        node = node[key]
    node[path[-1]] = value
    with pytest.raises(ValueError, match='incompatível'):
        repo.registrar_ensaio(pid, 1, 'C1', changed)
    assert repo.listar_ensaios(pid, 1) == []


@pytest.mark.parametrize('field,value', [
    ('corrente_a', True), ('corrente_a', '20'), ('tensao_v', float('inf')),
    ('comprimento_m', float('nan')),
    ('tabela_condutores', [{'secao_mm2': 4, 'capacidade_a': True}]),
    ('evidencia', {'documento': 'Fonte', 'edicao': 'teste', 'referencia': 'teste',
                   'dados_validados': 'true'}),
])
def test_saved_circuit_rejects_coercion_and_nonfinite_inputs(tmp_path, field, value):
    repo = RepositorioProjetos(tmp_path / 'typed.sqlite')
    pid = str(uuid4())
    circuit = {'nome': 'C1', **example(), field: value}
    if isinstance(value, float):
        # Persisting nonfinite JSON is already forbidden, before any revision.
        with pytest.raises(ValueError):
            repo.salvar(pid, 'Teste', {'circuitos': [circuit]}, 0)
        assert repo.carregar(pid) is None
    else:
        repo.salvar(pid, 'Teste', {'circuitos': [circuit]}, 0)
        with pytest.raises(ValueError, match='Circuito salvo incompleto ou inválido'):
            repo.registrar_ensaio(pid, 1, 'C1', example())
        assert repo.listar_ensaios(pid, 1) == []


def test_http_incomplete_legacy_and_mismatch_preserve_read_access(tmp_path, monkeypatch):
    token = 'test-only-' + 'd' * 36
    monkeypatch.setenv('SIE_LOCAL_API_TOKEN', token)
    monkeypatch.setenv('SIE_LOCAL_DB_PATH', str(tmp_path / 'bound-api.sqlite'))
    pid = str(uuid4())
    headers = {'Authorization': 'Bearer ' + token}
    base = f'/api/v1/local/projetos/{pid}'
    save = {'id': pid, 'nome': 'Legado', 'dados': {'circuitos': [{'nome': 'C1'}]},
            'revisao_esperada': 0}
    assert client.put('/api/v1/local/projetos', headers=headers, json=save).status_code == 200
    url = base + '/revisoes/1/circuitos/C1/ensaios'
    blocked = client.post(url, headers=headers, json=example())
    assert blocked.status_code == 422
    assert 'salve uma nova revisão' in blocked.json()['detail']
    assert client.get(base + '/revisoes/1', headers=headers).json()['dados'] == save['dados']
    save.update(dados={'circuitos': [{'nome': 'C1', **example()}]}, revisao_esperada=1)
    assert client.put('/api/v1/local/projetos', headers=headers, json=save).status_code == 200
    url = base + '/revisoes/2/circuitos/C1/ensaios'
    assert client.post(url, headers=headers, json={**example(), 'fator_correcao': .9}).status_code == 422
    assert client.post(url, headers=headers, json={**example(), 'corrente_a': True}).status_code == 422
    assert client.get(base + '/revisoes/2/ensaios', headers=headers).json()['ensaios'] == []
    assert client.post(url, headers=headers, json=example()).status_code == 200
    assert client.get(base + '/revisoes/1', headers=headers).json()['dados']['circuitos'] == [{'nome': 'C1'}]


def test_preexisting_trace_on_incomplete_legacy_revision_remains_readable(tmp_path):
    from hashlib import sha256
    from sie_api.application import analisar_circuito
    from sie_api.calculation_traces import _canonical, preparar_registro
    repo = RepositorioProjetos(tmp_path / 'existing-legacy.sqlite')
    pid = str(uuid4())
    repo.salvar(pid, 'Legado', {'circuitos': [{'nome': 'C1'}]}, 0)
    item, _, _ = preparar_registro(pid, 1, 'C1', example(), analisar_circuito(example()))
    item.pop('trace_schema_version')
    item['values_actually_used_by_algorithm'].pop('input_row_sha256')
    item['values_actually_used_by_algorithm'].pop('source_parameter_kinds')
    serial = _canonical(item)
    digest = sha256(serial.encode()).hexdigest()
    # Fixture represents a real pre-fix stored v1 trace, not a new allowed write.
    with repo._conectar() as db:
        db.execute('INSERT INTO ensaios_calculo VALUES(?,?,?,?,?,?,?)',
                   (item['id'], pid, 1, 'C1', serial, digest, '2026-10-01T00:00:00Z'))
    assert repo.consultar_ensaio(pid, item['id'])['entrada'] == example()
    assert len(repo.listar_ensaios(pid, 1)) == 1
    with pytest.raises(ValueError, match='Circuito salvo incompleto ou inválido'):
        repo.registrar_ensaio(pid, 1, 'C1', example())
    assert len(repo.listar_ensaios(pid, 1)) == 1


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
        "circuitos": [{"nome": "Iluminacao", **example()}]}, 0)
    saved = repo.registrar_ensaio(pid, rev, "Iluminacao", example())
    assert len(saved["algorithm_ids_executed"]) == 3
    row = saved["values_actually_used_by_algorithm"]
    assert saved["trace_schema_version"] == 2
    assert len(row["input_row_sha256"]) == 64
    assert row["source_parameter_kinds"] == {
        "conductor_base_iz": "CLIENT_DECLARED",
        "correction_factor": "CLIENT_DECLARED",
        "resistance_ohm_km": "CLIENT_DECLARED",
    }
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
    repo.salvar(pid, "Teste", {"circuitos": [{"nome": "C1", **example()}]}, 0)
    with pytest.raises(ValueError, match="ausente"):
        repo.registrar_ensaio(pid, 1, "C2", example())
    repo.salvar(pid, "Teste 2", {"circuitos": [{"nome": "C1", **example()}]}, 1)
    with pytest.raises(ConflitoRevisao):
        repo.registrar_ensaio(pid, 1, "C1", example())
    assert repo.listar_ensaios(pid, 1) == []


def test_reject_input_mismatch_and_duplicate_name(tmp_path):
    repo = RepositorioProjetos(tmp_path / "t.sqlite")
    pid = str(uuid4())
    repo.salvar(pid, "Teste", {"circuitos": [{"nome": "C1", **example(), "corrente_a": 10}]}, 0)
    with pytest.raises(ValueError, match="incompatível"):
        repo.registrar_ensaio(pid, 1, "C1", example())
    pid2 = str(uuid4())
    repo.salvar(pid2, "B", {"circuitos": [{"nome": "C1"}, {"nome": "c1"}]}, 0)
    with pytest.raises(ValueError, match="ambiguamente"):
        repo.registrar_ensaio(pid2, 1, "C1", example())


def test_trace_triggers_prevent_mutations_and_digest_detects_tampering(tmp_path):
    repo = RepositorioProjetos(tmp_path / "t.sqlite")
    pid = str(uuid4())
    repo.salvar(pid, "Teste", {"circuitos": [{"nome": "C1", **example()}]}, 0)
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
                            "dados": {"circuitos": [{"nome": "C1", **example()}]},
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
    repo.salvar(pid, "Teste", {"circuitos": [{"nome": "C1", **example()}]}, 0)
    trace = repo.registrar_ensaio(pid, 1, "C1", example())
    assert trace["calculation_trace_kind"].endswith("NOT_NORMATIVE_ATTESTATION")
    assert trace["normative_cells_used_verified"] == []
    assert trace["source_values_verified"] is False

def test_exact_decimal_section_matching_and_hash_protects_parameter_origin():
    from copy import deepcopy
    from hashlib import sha256
    from sie_api.application import analisar_circuito
    from sie_api.calculation_traces import _canonical, preparar_registro, validar_registro

    payload = example()
    payload["tabela_condutores"][1]["secao_mm2"] = 4.0000
    item, serial, digest = preparar_registro(
        str(uuid4()), 1, "C1", payload, analisar_circuito(payload))
    assert validar_registro(serial, digest) == item
    assert item["values_actually_used_by_algorithm"]["selected_input_row"]["indice_entrada"] == 1

    modified = deepcopy(item)
    modified["values_actually_used_by_algorithm"]["selected_input_row"]["capacidade_a"] = 40
    forged_serial = _canonical(modified)
    forged_digest = sha256(forged_serial.encode("utf-8")).hexdigest()
    with pytest.raises(ValueError, match="Hash da linha"):
        validar_registro(forged_serial, forged_digest)

    modified = deepcopy(item)
    modified["values_actually_used_by_algorithm"]["source_parameter_kinds"]["correction_factor"] = "PRIMARY_SOURCE_VERIFIED"
    forged_serial = _canonical(modified)
    with pytest.raises(ValueError, match="Fonte de parametros"):
        validar_registro(forged_serial, sha256(forged_serial.encode("utf-8")).hexdigest())


def test_versioned_trace_keeps_legacy_v1_readable():
    from copy import deepcopy
    from hashlib import sha256
    from sie_api.application import analisar_circuito
    from sie_api.calculation_traces import _canonical, preparar_registro, validar_registro

    payload = example()
    current, _, _ = preparar_registro(str(uuid4()), 1, "C1", payload, analisar_circuito(payload))
    legacy = deepcopy(current)
    legacy.pop("trace_schema_version")
    legacy["values_actually_used_by_algorithm"].pop("input_row_sha256")
    legacy["values_actually_used_by_algorithm"].pop("source_parameter_kinds")
    body = _canonical(legacy)
    assert validar_registro(body, sha256(body.encode("utf-8")).hexdigest()) == legacy
