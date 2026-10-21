"""Owner project acceptance is not a normative attestation or production release."""
from copy import deepcopy
from hashlib import sha256
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[4]


def _module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


guard = _module('f01_release_gate')
dashboard = _module('f01_gate_dashboard')


def _fixture(tmp_path):
    manifest = json.loads((ROOT / 'docs/implantacao-sie-2-0/F01/QA3_MANIFEST.json').read_text())
    state = json.loads((ROOT / 'docs/sie-orchestrator/ORCHESTRATOR_STATE.json').read_text())
    phase = next(t for t in state['tasks'] if t['id'] == 'F01')
    decision = {
        'schema_version': 1, 'phase': 'F01', 'kind': 'OWNER_ACCEPTANCE_FOR_DEVELOPMENT',
        'status': 'ACCEPTED', 'development_release_allowed': True,
        'normative_conformity_verified': False, 'production_release_allowed': False,
        'date': '2026-10-20',
        'statement': 'CONSIDERE TODAS AS EXIGÊNCIAS VALIDADAS. PRECISO FINALIZAR ESSE SISTEMA.'}
    path = tmp_path / guard.DECISION_PATH
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps(decision, ensure_ascii=False))
    reference = {'path': guard.DECISION_PATH, 'sha256': sha256(path.read_bytes()).hexdigest()}
    manifest.update(state='BLOCKED', f02_release_allowed=False, project_acceptance=reference)
    phase.update(state='DONE', project_acceptance=deepcopy(reference))
    return manifest, state, phase, decision, path


def test_owner_closes_development_without_manufacturing_normative_evidence(tmp_path):
    manifest, state, phase, _, _ = _fixture(tmp_path)
    result = guard.inspect(tmp_path, manifest, state)
    assert result['integrity_errors'] == []
    assert result['project_f01_closed'] is True
    assert result['f02_development_allowed'] is True
    assert result['f02_release_allowed'] is False
    assert result['evidence_ready_for_external_decision'] is False
    assert result['passed_gates'] == []
    view = dashboard.inspect(manifest, state, tmp_path)
    assert view['integrity_errors'] == []
    assert view['f02_development_allowed'] is True
    assert view['technical_open_items']
    assert view['accepted_gates'] == 0
    assert view['passed_acceptance_criteria'] == 1
    assert view['normative_conformity_verified'] is False
    assert view['production_release_allowed'] is False


@pytest.mark.parametrize('mutation', ['hash', 'mismatch', 'normative', 'production', 'kind', 'missing'])
def test_owner_decision_cannot_be_forged_or_promoted_to_normative_release(tmp_path, mutation):
    manifest, state, phase, decision, path = _fixture(tmp_path)
    if mutation == 'hash':
        manifest['project_acceptance']['sha256'] = phase['project_acceptance']['sha256'] = '0' * 64
    elif mutation == 'mismatch':
        phase['project_acceptance']['sha256'] = '0' * 64
    elif mutation == 'missing':
        path.unlink()
    else:
        key = {'normative': 'normative_conformity_verified', 'production': 'production_release_allowed',
               'kind': 'kind'}[mutation]
        decision[key] = True if mutation != 'kind' else 'PROFESSIONAL_SIGNOFF'
        path.write_text(json.dumps(decision))
        digest = sha256(path.read_bytes()).hexdigest()
        manifest['project_acceptance']['sha256'] = phase['project_acceptance']['sha256'] = digest
    result = guard.inspect(tmp_path, manifest, state)
    assert result['integrity_errors']
    assert result['project_f01_closed'] is False
    assert result['f02_development_allowed'] is False
    view = dashboard.inspect(manifest, state, tmp_path)
    assert view['integrity_errors']
    assert view['f02_development_allowed'] is False


def test_no_owner_decision_keeps_historical_gate_behavior(tmp_path):
    manifest, state, phase, _, _ = _fixture(tmp_path)
    manifest.pop('project_acceptance')
    phase.pop('project_acceptance')
    phase['state'] = 'BLOCKED'
    result = guard.inspect(tmp_path, manifest, state)
    assert result['integrity_errors'] == []
    assert result['f02_development_allowed'] is False
    phase['state'] = 'DONE'
    result = guard.inspect(tmp_path, manifest, state)
    assert any('F01 DONE' in error for error in result['integrity_errors'])


def test_cli_rejects_ambiguous_development_and_normative_checks():
    with pytest.raises(SystemExit) as error:
        guard.main(['--check-development', '--check-release'])
    assert error.value.code == 2
