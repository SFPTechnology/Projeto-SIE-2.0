from fastapi.testclient import TestClient
from sie_api.main import app

client = TestClient(app)


def test_health_reports_normative_block():
    res = client.get('/api/v1/health')
    assert res.status_code == 200
    assert res.json()['engineering_engine'] == 'blocked_pending_validation'


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
