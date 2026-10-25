"""F11 same-project provenance from F06-F09 to an F10 study bundle."""
import json
from copy import deepcopy
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from sie_api import conductor_f07, demand, protection_storage_f08
from sie_api.distributor_api_f09 import PersistedAssessment
from sie_api.distributor_persistence_f09 import enquadrar_persistido
from sie_api.domain.installation import Installation
from sie_api.installation_service import analyze_legacy, create_snapshot
from sie_api.persisted_source_f10 import publish_from_repository, verify_against_repository
from sie_api.protection_contracts_f08 import Study as ProtectionStudy
from sie_api.representation_f10 import ArtifactError
from sie_api.topology import load_document
from test_full_f10_integration import prepare_full


ROOT = Path(__file__).resolve().parents[3]


def integrated_project(tmp_path):
    repo, pid, rid = prepare_full(tmp_path)
    saved = repo.carregar(pid)
    data = saved['dados']
    inst = json.loads(data['installation_snapshot']['canonical_json'])
    inst['loads'][0]['active_power'] = {'value': '1200', 'unit': 'W'}
    inst['loads'][0]['reactive_power'] = {'value': '0', 'unit': 'var'}
    model = Installation.model_validate(inst)
    data['installation_snapshot'] = create_snapshot(model).model_dump(mode='json')
    data['floor_plan_f10']['revision_id'] = '3'
    repo.salvar(pid, saved['nome'], data, 2)
    topology = load_document(repo.carregar(pid)['dados'])
    raw = json.loads((ROOT / 'examples/f06_demanda_demo.json').read_text())
    source = str(topology.installation.supplies[0].id)
    load = str(topology.installation.loads[0].id)
    raw['id'] = str(uuid4())
    raw['topology'] = topology.model_dump(mode='json')
    raw['purpose'] = 'ENTRANCE'
    raw['assignments'] = {load: raw['assignments'][load]}
    raw['source_connections'] = {source: 'SINGLE_PHASE_FF'}
    raw['contexts'] = {source: {'utility': 'EDP_SP', 'locality': 'EDP-SP-TEST', 'edition': '09',
        'typology': 'RESIDENTIAL', 'concession_confirmed': True,
        'consumer_unit': 'INDIVIDUAL', 'reference_date': '2026-10-20'}}
    for rule in raw['rules']:
        rule.update(purpose='ENTRANCE', utility='EDP_SP', locality='EDP-SP-TEST',
                    edition='09', typology='RESIDENTIAL')
    scenario = demand.Scenario.model_validate(raw)
    demand.save_scenario(repo, UUID(pid), scenario, 3)
    conductor = conductor_f07.Study(id=uuid4(), topology=topology)
    conductor_f07.save(repo, UUID(pid), conductor, 4)
    protection_storage_f08.save(repo, UUID(pid), ProtectionStudy(id=uuid4(), conductor_study=conductor), 5)
    request = PersistedAssessment.model_validate({
        'distributor_id': 'EDP_SP', 'supply_id': source, 'modality': 'U',
        'context': {'uf': 'SP', 'distribuidora': 'EDP_SP', 'area_concessao_confirmada': True,
            'rede': 'AEREA_SECUNDARIA', 'sistema': 'ESTRELA', 'tensao_fase_neutro_v': 127,
            'tensao_linha_v': 220, 'frequencia_hz': 60, 'data_referencia': '2026-10-20',
            'isolacao_entrada': 'PVC', 'possui_mmgd': False, 'maior_motor_fn_cv': 0,
            'maior_motor_ff_cv': 0, 'maior_motor_fff_cv': 0, 'possui_cargas_especiais': False},
        'expected_revision': 6})
    enquadrar_persistido(repo, UUID(pid), request, 6)
    saved = repo.carregar(pid); data = saved['dados']
    inst = json.loads(data['installation_snapshot']['canonical_json'])
    run = inst['calculation_runs'][0]
    params = data['calculation_inputs_f10'][rid]
    from sie_api.analysis_contracts import AnaliseCircuito
    record = analyze_legacy(create_snapshot(Installation.model_validate(inst)),
                            UUID(run['circuit_id']), AnaliseCircuito.model_validate(params), run['rule_version'])
    run.update(state='VALID', input_sha256=record.input_sha256,
               output_sha256=record.result_sha256, algorithm_version=record.algorithm_version)
    data['installation_snapshot'] = create_snapshot(Installation.model_validate(inst)).model_dump(mode='json')
    data['floor_plan_f10']['revision_id'] = '8'
    data['f11_require_f09'] = True
    repo.salvar(pid, saved['nome'], data, 7)
    repo.executar_calculo_f10(pid, 8, rid)
    return repo, pid, rid, source


def test_integrated_lineage_and_load_change_fail_closed(tmp_path):
    repo, pid, rid, source = integrated_project(tmp_path)
    target = tmp_path / 'f11-export' / 'bundle'
    manifest = publish_from_repository(repo, pid, 8, rid, 'full-v1', target, full=True)
    snapshot = json.loads((target / 'snapshot.json').read_text())
    lineage = snapshot['f09_consultative_lineage']
    assert lineage['evidence']['project_id'] == pid
    assert lineage['evidence']['supply_id'] == source
    assert {key for key in ('F06', 'F07', 'F08')} <= set(lineage['evidence'])
    assert manifest['dependencies']['f09_assessment_sha256'] == lineage['assessment_id_sha256']
    assert verify_against_repository(repo, target)['currentness'] == 'CURRENT'

    saved = repo.carregar(pid); data = deepcopy(saved['dados'])
    inst = json.loads(data['installation_snapshot']['canonical_json'])
    inst['loads'][0]['active_power']['value'] = '1100'
    inst['loads'][0]['apparent_power']['value'] = '1100'
    data['installation_snapshot'] = create_snapshot(Installation.model_validate(inst)).model_dump(mode='json')
    data['floor_plan_f10']['revision_id'] = '9'
    repo.salvar(pid, saved['nome'], data, 8)
    assert verify_against_repository(repo, target)['currentness'] == 'STALE'

    with pytest.raises(ArtifactError):
        publish_from_repository(repo, pid, 9, rid, 'full-v1', tmp_path / 'new' / 'bundle', full=True)

    # Re-establish every stored study from the changed canonical topology.
    current = repo.carregar(pid); topology = load_document(current['dados'])
    previous = current['dados']['demand_scenarios'][-1]['scenario']
    next_scenario = deepcopy(previous)
    next_scenario['id'] = str(uuid4())
    next_scenario['topology'] = topology.model_dump(mode='json')
    demand.save_scenario(repo, UUID(pid), demand.Scenario.model_validate(next_scenario), 9)
    conductor = conductor_f07.Study(id=uuid4(), topology=topology)
    conductor_f07.save(repo, UUID(pid), conductor, 10)
    protection_storage_f08.save(repo, UUID(pid), ProtectionStudy(id=uuid4(), conductor_study=conductor), 11)
    previous_assessment = current['dados']['distributor_assessments_f09'][-1]['assessment']
    request = PersistedAssessment.model_validate({
        'distributor_id': previous_assessment['distributor_id'], 'supply_id': source,
        'modality': previous_assessment['modality'], 'context': previous_assessment['context'],
        'expected_revision': 12})
    enquadrar_persistido(repo, UUID(pid), request, 12)

    saved = repo.carregar(pid); data = saved['dados']
    inst = json.loads(data['installation_snapshot']['canonical_json'])
    run = inst['calculation_runs'][0]
    from sie_api.analysis_contracts import AnaliseCircuito
    params = AnaliseCircuito.model_validate(data['calculation_inputs_f10'][rid])
    record = analyze_legacy(create_snapshot(Installation.model_validate(inst)),
                            UUID(run['circuit_id']), params, run['rule_version'])
    run.update(state='VALID', input_sha256=record.input_sha256,
               output_sha256=record.result_sha256, algorithm_version=record.algorithm_version)
    data['installation_snapshot'] = create_snapshot(Installation.model_validate(inst)).model_dump(mode='json')
    data['floor_plan_f10']['revision_id'] = '14'
    repo.salvar(pid, saved['nome'], data, 13)
    repo.executar_calculo_f10(pid, 14, rid)
    revised = tmp_path / 'recalculated' / 'bundle'
    updated = publish_from_repository(repo, pid, 14, rid, 'full-v1', revised, full=True)
    assert updated['dependencies']['f09_assessment_sha256'] != manifest['dependencies']['f09_assessment_sha256']
    assert verify_against_repository(repo, revised)['currentness'] == 'CURRENT'
    assert verify_against_repository(repo, target)['currentness'] == 'STALE'


def test_required_f09_rejects_missing_or_modified_assessment(tmp_path):
    repo, pid, rid = prepare_full(tmp_path)
    saved = repo.carregar(pid); data = saved['dados']
    data['f11_require_f09'] = True
    data['floor_plan_f10']['revision_id'] = '3'
    repo.salvar(pid, saved['nome'], data, 2)
    repo.executar_calculo_f10(pid, 3, rid)
    with pytest.raises(ArtifactError, match='requires current persisted F09'):
        publish_from_repository(repo, pid, 3, rid, 'full-v1', tmp_path / 'missing' / 'bundle', full=True)

    other = tmp_path / 'integrated'
    other.mkdir()
    repo, pid, rid, _ = integrated_project(other)
    saved = repo.carregar(pid); data = saved['dados']
    data['distributor_assessments_f09'][-1]['evidence']['F08']['result_sha256'] = '0' * 64
    data['floor_plan_f10']['revision_id'] = '9'
    repo.salvar(pid, saved['nome'], data, 8)
    repo.executar_calculo_f10(pid, 9, rid)
    with pytest.raises(ArtifactError):
        publish_from_repository(repo, pid, 9, rid, 'full-v1', tmp_path / 'modified' / 'bundle', full=True)
