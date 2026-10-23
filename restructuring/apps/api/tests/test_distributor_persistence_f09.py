"""F09 binds its consultative result to current persisted F06-F08 evidence."""
import json
from pathlib import Path
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from sie_api.main import app
from sie_api.storage import RepositorioProjetos
from sie_api.topology import persist
from sie_api.demand import Scenario, save_scenario
from sie_api import conductor_f07, protection_storage_f08
from sie_api.protection_contracts_f08 import Study as ProtectionStudy
from sie_api import distributor_engine_f09

ROOT = Path(__file__).resolve().parents[3]
TOKEN = 'f09-local-test-token-with-more-than-24-chars'


@pytest.fixture
def ready_project(tmp_path, monkeypatch):
    monkeypatch.setenv('SIE_ENV', 'test')
    monkeypatch.setenv('SIE_LOCAL_API_TOKEN', TOKEN)
    db_path = str(tmp_path / 'f09.sqlite')
    monkeypatch.setenv('SIE_LOCAL_DB_PATH', db_path)
    repo = RepositorioProjetos(db_path)
    raw = json.loads((ROOT / 'examples/f06_demanda_demo.json').read_text())
    source = raw['topology']['installation']['supplies'][0]['id']
    raw['purpose'] = 'ENTRANCE'
    raw['source_connections'] = {source: 'SINGLE_PHASE_FF'}
    raw['contexts'] = {source: {
        'utility': 'EDP_SP', 'locality': 'EDP-SP-TEST', 'edition': '09',
        'typology': 'RESIDENTIAL', 'concession_confirmed': True,
        'consumer_unit': 'INDIVIDUAL', 'reference_date': '2026-10-20',
    }}
    for rule in raw['rules']:
        rule['purpose'] = 'ENTRANCE'
        rule.update(utility='EDP_SP', locality='EDP-SP-TEST', edition='09', typology='RESIDENTIAL')
    for load in raw['topology']['installation']['loads']:
        load['apparent_power'] = {'value': '1000', 'unit': 'VA'}
    scenario = Scenario.model_validate(raw)
    project_id = scenario.topology.installation.project.id
    persist(repo, project_id, scenario.topology, 0)
    save_scenario(repo, project_id, scenario, 1)

    conductor = conductor_f07.Study(id=uuid4(), topology=scenario.topology)
    conductor_f07.save(repo, project_id, conductor, 2)
    protection = ProtectionStudy(id=uuid4(), conductor_study=conductor)
    protection_storage_f08.save(repo, project_id, protection, 3)
    project = repo.carregar(str(project_id))
    return repo, project_id, source, project['revisao']


def request(source, revision, **changes):
    context = {
        'uf': 'SP', 'distribuidora': 'EDP_SP', 'area_concessao_confirmada': True,
        'rede': 'AEREA_SECUNDARIA', 'sistema': 'ESTRELA',
        'tensao_fase_neutro_v': 127, 'tensao_linha_v': 220, 'frequencia_hz': 60,
        'data_referencia': '2026-10-20', 'isolacao_entrada': 'PVC',
        'possui_mmgd': False, 'maior_motor_fn_cv': 0, 'maior_motor_ff_cv': 0,
        'maior_motor_fff_cv': 0, 'possui_cargas_especiais': False,
    }
    context.update(changes)
    return {'distributor_id': 'EDP_SP', 'supply_id': str(source), 'modality': 'U',
            'context': context, 'expected_revision': revision}


def test_local_assessment_derives_f06_and_links_current_f07_f08(ready_project):
    _, project_id, source, revision = ready_project
    client = TestClient(app)
    response = client.put(
        f'/api/v1/local/projetos/{project_id}/distribuidoras/enquadrar',
        json=request(source, revision), headers={'Authorization': f'Bearer {TOKEN}'})
    assert response.status_code == 200, response.text
    result = response.json()
    assert result['integration_state'] == 'PERSISTED_EVIDENCE_LINKED_CONSULTATIVE'
    assert result['evidence_provenance']['F06']['result_sha256']
    assert result['evidence_provenance']['F07']['input_sha256']
    assert result['evidence_provenance']['F08']['result_sha256']
    assert result['normative_conformity_verified'] is False
    assert result['utility_approval'] is False
    stored = client.get(
        f'/api/v1/local/projetos/{project_id}/distribuidoras/enquadramentos',
        headers={'Authorization': f'Bearer {TOKEN}'})
    assert stored.status_code == 200
    assert len(stored.json()['items']) == 1
    assert stored.json()['items'][0]['stale'] is False


def test_local_assessment_rejects_missing_f08_and_wrong_revision(ready_project):
    repo, project_id, source, revision = ready_project
    data = repo.carregar(str(project_id))['dados']
    data.pop('protection_studies')
    repo.salvar(str(project_id), 'Synthetic model', data, revision)
    client = TestClient(app)
    payload = request(source, revision + 1)
    response = client.put(
        f'/api/v1/local/projetos/{project_id}/distribuidoras/enquadrar',
        json=payload, headers={'Authorization': f'Bearer {TOKEN}'})
    assert response.status_code == 409
    assert 'F08' in response.json()['detail']


def test_local_assessment_rejects_unconfirmed_or_mismatched_f06_context(ready_project):
    _, project_id, source, revision = ready_project
    client = TestClient(app)
    payload = request(source, revision)
    payload['context']['distribuidora'] = 'OTHER_DSO'
    response = client.put(
        f'/api/v1/local/projetos/{project_id}/distribuidoras/enquadrar',
        json=payload, headers={'Authorization': f'Bearer {TOKEN}'})
    assert response.status_code == 409


def test_local_assessment_requires_local_authentication(ready_project):
    _, project_id, source, revision = ready_project
    response = TestClient(app).put(
        f'/api/v1/local/projetos/{project_id}/distribuidoras/enquadrar',
        json=request(source, revision))
    assert response.status_code == 401


def test_saved_assessment_becomes_stale_if_f06_result_changes(ready_project):
    repo, project_id, source, revision = ready_project
    client = TestClient(app)
    headers = {'Authorization': f'Bearer {TOKEN}'}
    route = f'/api/v1/local/projetos/{project_id}/distribuidoras/enquadrar'
    saved = client.put(route, json=request(source, revision), headers=headers)
    assert saved.status_code == 200, saved.text

    current = repo.carregar(str(project_id))
    data = current['dados']
    data['demand_scenarios'][-1]['result']['by_supply'][str(source)]['design_current']['value_a'] = '999'
    repo.salvar(str(project_id), current['nome'], data, current['revisao'])
    history = client.get(
        f'/api/v1/local/projetos/{project_id}/distribuidoras/enquadramentos', headers=headers)
    assert history.status_code == 200
    assert history.json()['items'][-1]['stale'] is True


def test_saved_assessment_becomes_stale_when_distributor_edition_changes(ready_project, monkeypatch):
    _, project_id, source, revision = ready_project
    client = TestClient(app)
    headers = {'Authorization': f'Bearer {TOKEN}'}
    saved = client.put(
        f'/api/v1/local/projetos/{project_id}/distribuidoras/enquadrar',
        json=request(source, revision), headers=headers)
    assert saved.status_code == 200, saved.text
    monkeypatch.setitem(distributor_engine_f09._EDP_V09, 'edition', '10')
    history = client.get(
        f'/api/v1/local/projetos/{project_id}/distribuidoras/enquadramentos', headers=headers)
    assert history.status_code == 200
    assert history.json()['items'][-1]['stale'] is True
