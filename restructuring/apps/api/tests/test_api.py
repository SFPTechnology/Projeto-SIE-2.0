from fastapi.testclient import TestClient
from sie_api.main import app

client = TestClient(app)


def test_health_reports_normative_block():
    res = client.get('/api/v1/health')
    assert res.status_code == 200
    assert res.json()['engineering_engine'] == 'calculation_available_with_release_gate'


def test_valid_project_is_only_structurally_validated():
    res = client.post('/api/v1/projetos/validar', json={'nome':'Casa', 'circuitos':[{'nome':'TUG 01', 'corrente_a':10, 'comprimento_m':23, 'tensao_v':127}]})
    assert res.status_code == 200
    assert res.json()['validacao_normativa'] == 'nao_realizada'


def test_reject_negative_current():
    res = client.post('/api/v1/projetos/validar', json={'nome':'Casa','circuitos':[{'nome':'C1','corrente_a':-2,'comprimento_m':1,'tensao_v':127}]})
    assert res.status_code == 422


def test_reject_duplicate_circuits():
    c = {'corrente_a': 10, 'comprimento_m': 1, 'tensao_v': 220}
    res = client.post('/api/v1/projetos/validar', json={'nome':'Casa','circuitos':[{'nome':'C1',**c},{'nome':'c1',**c}]})
    assert res.status_code == 422


def test_reject_unknown_field():
    res = client.post('/api/v1/projetos/validar', json={'nome':'Casa','extra':'invalid'})
    assert res.status_code == 422


def test_analysis_returns_result_but_preserves_release_gate():
    res = client.post('/api/v1/circuitos/analisar', json={
        'corrente_a': 20, 'comprimento_m': 30, 'tensao_v': 220, 'resistencia_ohm_km': 7.41,
        'fator_correcao': .8, 'tabela_condutores': [{'secao_mm2':2.5,'capacidade_a':24},{'secao_mm2':4,'capacidade_a':32}],
        'evidencia': {'documento':'NBR 5410','edicao':'2004','referencia':'A validar','dados_validados':False,'testes_independentes':False}
    })
    assert res.status_code == 200
    assert res.json()['status_engenharia'] == 'PENDENTE'
    assert res.json()['disjuntor']['corrente_a'] == 20


def test_edp_endpoint_exposes_verified_catalog_provenance():
    res = client.post('/api/v1/edp/enquadrar', json={
        'modalidade': 'T', 'corrente_demanda_a': 58.3,
        'carga_instalada_kw': 22.215, 'tem_carga_trifasica': True,
    })
    assert res.status_code == 200
    assert res.json()['categoria']['codigo'] == 'T2'
    assert res.json()['catalogo']['status'] == 'VERIFICADO'


def test_claimed_validation_cannot_approve_normative_use():
    res = client.post('/api/v1/circuitos/analisar', json={
        'corrente_a': 20, 'comprimento_m': 30, 'tensao_v': 220,
        'resistencia_ohm_km': 7.41, 'fator_correcao': .8,
        'tabela_condutores': [{'secao_mm2': 4, 'capacidade_a': 32}],
        'evidencia': {'documento': 'Fonte informada pelo usuario',
                     'edicao': '2026', 'referencia': 'Tabela declarada',
                     'dados_validados': True, 'testes_independentes': True}
    })
    assert res.status_code == 200
    assert res.json()['status_engenharia'] == 'PENDENTE'
    assert res.json()['liberado_para_uso_normativo'] is False


def test_cors_rejects_untrusted_browser_origin():
    res = client.options('/api/v1/circuitos/analisar', headers={
        'Origin': 'https://external.example',
        'Access-Control-Request-Method': 'POST',
    })
    assert res.status_code == 400
    assert res.headers.get('access-control-allow-origin') is None


def test_cors_accepts_local_ui_origin():
    res = client.options('/api/v1/circuitos/analisar', headers={
        'Origin': 'http://localhost:5173',
        'Access-Control-Request-Method': 'POST',
    })
    assert res.status_code == 200
    assert res.headers.get('access-control-allow-origin') == 'http://localhost:5173'
