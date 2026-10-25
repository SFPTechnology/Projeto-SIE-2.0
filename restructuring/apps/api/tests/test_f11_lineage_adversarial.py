"""Adversarial checks for F09 consultative metadata bound to F10."""

from copy import deepcopy

import pytest

from sie_api.persisted_source_f10 import publish_from_repository
from sie_api.representation_f10 import ArtifactError
from sie_api.installation_service import digest
from test_f11_f09_f10_bridge import integrated_project


@pytest.mark.parametrize('field, forged', [
    ('f07_status', 'APROVADO'),
    ('f08_status', 'APROVADO'),
    ('integration_state', 'NORMATIVE_APPROVED'),
])
def test_modified_f09_metadata_cannot_enter_f10_memorial(tmp_path, field, forged):
    repo, pid, rid, _ = integrated_project(tmp_path)
    saved = repo.carregar(pid)
    data = deepcopy(saved['dados'])
    data['distributor_assessments_f09'][-1]['result'][field] = forged
    data['floor_plan_f10']['revision_id'] = '9'
    repo.salvar(pid, saved['nome'], data, 8)
    repo.executar_calculo_f10(pid, 9, rid)
    with pytest.raises(ArtifactError):
        publish_from_repository(repo, pid, 9, rid, 'full-v1', tmp_path / 'forged' / 'bundle', full=True)


@pytest.mark.parametrize('engine,id_key', [
    ('F06', 'scenario_id'), ('F07', 'study_id'), ('F08', 'study_id'),
])
def test_rehashed_f09_evidence_still_needs_exact_study_identity(tmp_path, engine, id_key):
    repo, pid, rid, _ = integrated_project(tmp_path)
    saved = repo.carregar(pid)
    data = deepcopy(saved['dados'])
    row = data['distributor_assessments_f09'][-1]
    row['evidence'][engine][id_key] = '00000000-0000-0000-0000-000000000099'
    row['result']['evidence_provenance'] = deepcopy(row['evidence'])
    row['fingerprint'] = digest({'assessment': row['assessment'], 'evidence': row['evidence']})
    data['floor_plan_f10']['revision_id'] = '9'
    repo.salvar(pid, saved['nome'], data, 8)
    repo.executar_calculo_f10(pid, 9, rid)
    with pytest.raises(ArtifactError):
        publish_from_repository(repo, pid, 9, rid, 'full-v1', tmp_path / 'wrong-id' / 'bundle', full=True)
