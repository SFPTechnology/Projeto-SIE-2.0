"""F02 exact snapshot references, stale calculations and additive legacy adapter."""
from copy import deepcopy
from hashlib import sha256
import json
from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from sie_api.main import app
from sie_api.domain.installation import Installation
from sie_api.analysis_contracts import AnaliseCircuito
from sie_api.application import analisar_circuito
from sie_api.installation_service import (algorithm_identity, InstallationSnapshot, RevisionReference,
    CalculationRecord, create_snapshot, analyze_legacy, calculation_status, require_same_revision, digest)
from sie_api.installation_storage_api import SaveInstallation, persist_snapshot
from sie_api.storage import RepositorioProjetos, ConflitoRevisao
from test_installation_f02 import demo_installation


def legacy_case():
    data = demo_installation()
    # Deliberate homogeneous synthetic case supported by the monophase legacy engine.
    data['segments'][2]['conditions'] = deepcopy(data['segments'][1]['conditions'])
    data['cable_runs'][1]['section']['value'] = '2.5'
    installation = Installation.model_validate(data)
    parameters = AnaliseCircuito.model_validate({
        'corrente_a': 10.0, 'comprimento_m': 12.5, 'tensao_v': 220.0,
        'resistencia_ohm_km': 7.41, 'fator_correcao': .87,
        'tabela_condutores': [{'secao_mm2': 2.5, 'capacidade_a': 24.0},
                              {'secao_mm2': 4.0, 'capacidade_a': 32.0}],
        'evidencia': {'documento': 'Synthetic test, not normative', 'edicao': 'TEST', 'referencia': 'fixture'}})
    return installation, parameters


def test_adapter_matches_existing_engine_and_records_exact_revision_without_approval():
    installation, params = legacy_case()
    snap = create_snapshot(installation)
    record = analyze_legacy(snap, installation.circuits[1].id, params, 'declared-test-v1')
    assert json.loads(record.result_json) == analisar_circuito(params.model_dump(mode='json'))
    assert record.snapshot_sha256 == snap.snapshot_sha256
    assert record.normative_conformity_verified is False
    assert calculation_status(record, snap, algorithm_identity(), 'declared-test-v1', digest(params.model_dump(mode='json')))['status'] == 'VALID'


@pytest.mark.parametrize('changed', ['model', 'algorithm', 'rule', 'input'])
def test_each_dependency_change_invalidates_result_without_rewriting_history(changed):
    installation, params = legacy_case()
    snap = create_snapshot(installation)
    record = analyze_legacy(snap, installation.circuits[1].id, params, 'test-v1')
    before = record.model_dump_json()
    algorithm, rule, input_hash = algorithm_identity(), 'test-v1', record.input_sha256
    if changed == 'model':
        raw = installation.model_dump(mode='json')
        raw['loads'][0]['active_power']['value'] = '1001'
        snap = create_snapshot(Installation.model_validate(raw))
    elif changed == 'algorithm':
        algorithm = 'new-algorithm'
    elif changed == 'rule':
        rule = 'new-rule'
    else:
        input_hash = '0' * 64
    assert calculation_status(record, snap, algorithm, rule, input_hash)['status'] == 'STALE'
    assert record.model_dump_json() == before


def test_pending_and_invalid_project_and_exact_document_reference():
    installation, params = legacy_case()
    snap = create_snapshot(installation)
    record = analyze_legacy(snap, installation.circuits[1].id, params, 'test-v1')
    pending = CalculationRecord.model_validate({**record.model_dump(mode='json'), 'result_json': None, 'result_sha256': None})
    assert calculation_status(pending, snap, algorithm_identity(), 'test-v1', pending.input_sha256)['status'] == 'PENDING'
    invalid = CalculationRecord.model_validate({**record.model_dump(mode='json'), 'circuit_id': str(UUID(int=999))})
    assert calculation_status(invalid, snap, algorithm_identity(), 'test-v1', invalid.input_sha256)['status'] == 'INVALID'
    ref = RevisionReference(project_id=snap.project_id, revision=1, snapshot_sha256=snap.snapshot_sha256)
    require_same_revision(snap, ref)
    with pytest.raises(ValueError):
        require_same_revision(snap, ref.model_copy(update={'revision': 2}))


def test_snapshot_does_not_share_mutable_input_and_rejects_changed_content_or_hash():
    installation, _ = legacy_case()
    snap = create_snapshot(installation)
    before = snap.canonical_json
    installation.loads[0].active_power.value = '2000'
    assert snap.canonical_json == before
    for patch in [{'revision': 2}, {'snapshot_sha256': '0' * 64},
                  {'canonical_json': snap.canonical_json.replace('Synthetic model', 'tampered')}]:
        with pytest.raises(ValidationError):
            InstallationSnapshot.model_validate({**snap.model_dump(mode='json'), **patch})


@pytest.mark.parametrize('problem', ['heterogeneous', 'section', 'current', 'length', 'three_phase'])
def test_adapter_rejects_inputs_that_cannot_represent_the_canonical_circuit(problem):
    installation, params = legacy_case()
    raw = installation.model_dump(mode='json')
    if problem == 'heterogeneous':
        raw['segments'][2]['conditions']['ambient_temperature']['value'] = '40'
    elif problem == 'section':
        raw['cable_runs'][1]['section']['value'] = '4'
    elif problem == 'current':
        raw['circuits'][1]['design_current']['value'] = '11'
    elif problem == 'length':
        raw['segments'][1]['length']['value'] = '6'
    else:
        raw['circuits'][1]['phases'] = 3
        for load in raw['loads']:
            if load['id'] in raw['circuits'][1]['load_ids']:
                load['connection'] = 'THREE_PHASE'
    with pytest.raises(ValueError):
        analyze_legacy(create_snapshot(Installation.model_validate(raw)), installation.circuits[1].id, params, 'test-v1')


def test_local_store_keeps_full_snapshots_legacy_data_and_optimistic_conflicts(tmp_path):
    installation, _ = legacy_case()
    repo = RepositorioProjetos(tmp_path / 'local.sqlite')
    pid = installation.project.id
    first = create_snapshot(installation)
    request = SaveInstallation(nome='Canonical project', snapshot=first, revisao_esperada=0)
    assert persist_snapshot(repo, pid, request)['revisao'] == 1
    old = repo.carregar_revisao(str(pid), 1)
    raw = installation.model_dump(mode='json')
    raw['project']['revision'] = 2
    raw['loads'][0]['active_power']['value'] = '1001'
    second = create_snapshot(Installation.model_validate(raw))
    request2 = SaveInstallation(nome='Canonical project', snapshot=second, revisao_esperada=1)
    assert persist_snapshot(repo, pid, request2)['revisao'] == 2
    assert repo.carregar_revisao(str(pid), 1) == old
    assert repo.carregar(str(pid))['dados']['installation_snapshot']['snapshot_sha256'] == second.snapshot_sha256
    with pytest.raises(ConflitoRevisao):
        persist_snapshot(repo, pid, request2)
    with pytest.raises(ValueError):
        persist_snapshot(repo, UUID(int=999), request2)


def test_explicit_model_adoption_preserves_existing_legacy_payload(tmp_path):
    installation, params = legacy_case()
    repo = RepositorioProjetos(tmp_path / 'adoption.sqlite')
    pid = str(installation.project.id)
    legacy = {'analise': params.model_dump(mode='json'), 'legacy_extra': {'keep': True}}
    repo.salvar(pid, 'Legacy', legacy, 0)
    raw = installation.model_dump(mode='json')
    raw['project']['revision'] = 2
    snapshot = create_snapshot(Installation.model_validate(raw))
    persist_snapshot(repo, installation.project.id,
        SaveInstallation(nome='Canonical', snapshot=snapshot, revisao_esperada=1))
    saved = repo.carregar(pid)['dados']
    assert saved['analise'] == legacy['analise']
    assert saved['legacy_extra'] == {'keep': True}
    assert repo.carregar_revisao(pid, 1)['dados'] == legacy


def test_algorithm_body_fingerprint_changes_invalidation_without_faking_version(monkeypatch):
    from sie_api import installation_service as service
    installation, params = legacy_case()
    snapshot = create_snapshot(installation)
    record = analyze_legacy(snapshot, installation.circuits[1].id, params, 'test-v1')
    original = service.getsource
    monkeypatch.setattr(service, 'getsource', lambda obj: original(obj) + '\n# different implementation')
    assert service.algorithm_identity() != record.algorithm_version
    assert calculation_status(record, snapshot, service.algorithm_identity(), 'test-v1', record.input_sha256)['status'] == 'STALE'


def test_http_openapi_cli_and_authenticated_persistence(tmp_path, monkeypatch, capsys):
    installation, params = legacy_case()
    client = TestClient(app)
    raw = installation.model_dump(mode='json')
    assert client.post('/api/v1/modelo/validar', json=raw).json()['valid'] is True
    snap = client.post('/api/v1/modelo/snapshots', json=raw).json()
    record = client.post('/api/v1/modelo/ensaiar-legado', json={
        'snapshot': snap, 'circuit_id': str(installation.circuits[1].id),
        'parameters': params.model_dump(mode='json'), 'rule_version': 'test-v1'})
    assert record.status_code == 200
    result = client.post('/api/v1/modelo/invalidacao', json={
        'record': record.json(), 'snapshot': snap,
        'rule_version': 'changed', 'input_sha256': record.json()['input_sha256']})
    assert result.json()['status'] == 'STALE'
    ref = {key: snap[key] for key in ('project_id', 'revision', 'snapshot_sha256')}
    assert client.post('/api/v1/modelo/referencias/validar', json={'snapshot': snap, 'reference': ref}).status_code == 200
    bad = deepcopy(raw)
    bad['circuits'][1]['voltage']['unit'] = 'kV'
    assert client.post('/api/v1/modelo/validar', json=bad).status_code == 422
    token = 'f02-local-test-' + 'x' * 32
    monkeypatch.setenv('SIE_LOCAL_API_TOKEN', token)
    monkeypatch.setenv('SIE_LOCAL_DB_PATH', str(tmp_path / 'api.sqlite'))
    path = '/api/v1/local/projetos/' + str(installation.project.id) + '/modelo'
    request = {'nome': 'Local', 'snapshot': snap, 'revisao_esperada': 0}
    assert client.put(path, json=request).status_code == 401
    assert client.put(path, json=request, headers={'Authorization': 'Bearer ' + token}).status_code == 200
    assert client.put(path, json=request, headers={'Authorization': 'Bearer ' + token}).status_code == 409
    file = tmp_path / 'installation.json'
    file.write_text(json.dumps(raw))
    from sie_api.cli import main
    assert main(['modelo', '--arquivo', str(file), '--operacao', 'snapshot']) == 0
    assert json.loads(capsys.readouterr().out)['snapshot_sha256'] == snap['snapshot_sha256']
    file.write_text(json.dumps({'snapshot': snap, 'circuit_id': str(installation.circuits[1].id),
                               'parameters': params.model_dump(mode='json'), 'rule_version': 'test-v1'}))
    assert main(['modelo', '--arquivo', str(file), '--operacao', 'ensaiar-legado']) == 0
    cli_record = json.loads(capsys.readouterr().out)
    assert cli_record == record.json()
    file.write_text(json.dumps({'record': cli_record, 'snapshot': snap, 'rule_version': 'test-v1',
                               'input_sha256': cli_record['input_sha256']}))
    assert main(['modelo', '--arquivo', str(file), '--operacao', 'invalidacao']) == 0
    assert json.loads(capsys.readouterr().out)['status'] == 'VALID'
    file.write_text(json.dumps({'snapshot': snap, 'reference': ref}))
    assert main(['modelo', '--arquivo', str(file), '--operacao', 'referencia']) == 0
    assert json.loads(capsys.readouterr().out)['valid'] is True
    assert '/api/v1/modelo/ensaiar-legado' in app.openapi()['paths']
