from uuid import uuid4
import pytest
from sie_api.storage import ConflitoRevisao, RepositorioProjetos


def test_revisions_persist_and_audit(tmp_path):
    repo = RepositorioProjetos(tmp_path / "sie.sqlite3")
    projeto_id = str(uuid4())
    assert repo.salvar(projeto_id, "Projeto A", {"circuitos": [{"nome": "C1"}]}, 0) == 1
    assert repo.salvar(projeto_id, "Projeto A v2", {"circuitos": []}, 1) == 2
    assert repo.carregar(projeto_id)["revisao"] == 2
    assert repo.carregar(projeto_id)["dados"]["circuitos"] == []
    assert [x["acao"] for x in repo.historico(projeto_id)] == ["CRIAR", "ATUALIZAR"]


def test_optimistic_conflict_does_not_change_project(tmp_path):
    repo = RepositorioProjetos(tmp_path / "sie.sqlite3")
    projeto_id = str(uuid4())
    repo.salvar(projeto_id, "Original", {}, 0)
    with pytest.raises(ConflitoRevisao):
        repo.salvar(projeto_id, "Sobrescrito", {}, 0)
    assert repo.carregar(projeto_id)["nome"] == "Original"
    assert len(repo.historico(projeto_id)) == 1


def test_rejects_invalid_project_and_non_finite_json(tmp_path):
    repo = RepositorioProjetos(tmp_path / "sie.sqlite3")
    projeto_id = str(uuid4())
    with pytest.raises(ValueError):
        repo.salvar(projeto_id, "", {}, 0)
    with pytest.raises(ValueError):
        repo.salvar(projeto_id, "Dados", {"corrente": float("nan")}, 0)
    assert repo.carregar(projeto_id) is None


def test_existing_database_can_be_reopened(tmp_path):
    path = tmp_path / "sie.sqlite3"
    projeto_id = str(uuid4())
    RepositorioProjetos(path).salvar(projeto_id, "Persistente", {"v": 1}, 0)
    assert RepositorioProjetos(path).carregar(projeto_id)["dados"] == {"v": 1}


def test_current_revision_verification_distinguishes_historical_and_current(tmp_path):
    repo = RepositorioProjetos(tmp_path / "currentness.sqlite3")
    projeto_id = str(uuid4())
    repo.salvar(projeto_id, "Projeto v1", {"circuitos": ["C1"]}, 0)
    current_v1 = repo.verificar_revisao_atual(projeto_id, 1)
    assert current_v1["status"] == "CURRENT"
    assert len(current_v1["historical_sha256"]) == 64

    repo.salvar(projeto_id, "Projeto v2", {"circuitos": ["C2"]}, 1)
    assert repo.verificar_revisao_atual(projeto_id, 1)["status"] == "HISTORICAL"
    assert repo.verificar_revisao_atual(projeto_id, 2)["status"] == "CURRENT"
    assert repo.verificar_revisao_atual(projeto_id, 3)["status"] == "SOURCE_INVALID"


def test_current_revision_verification_does_not_reconstruct_missing_history(tmp_path):
    repo = RepositorioProjetos(tmp_path / "missing-history.sqlite3")
    projeto_id = str(uuid4())
    repo.salvar(projeto_id, "Projeto", {"v": 1}, 0)
    with repo._conectar() as db:
        db.execute("DROP TRIGGER f01_versao_sem_delete")
        db.execute("DELETE FROM versoes_projeto WHERE projeto_id=? AND revisao=1", (projeto_id,))
    assert repo.verificar_revisao_atual(projeto_id, 1)["status"] == "SOURCE_INVALID"


def test_rejects_oversized_payload(tmp_path):
    repo = RepositorioProjetos(tmp_path / "sie.sqlite3")
    projeto_id = str(uuid4())
    with pytest.raises(ValueError, match="1 MiB"):
        repo.salvar(projeto_id, "Projeto grande", {"texto": "x" * 1_048_576}, 0)
    assert repo.carregar(projeto_id) is None


def motor_revision(repo, *, wrong_output=False, missing_input=False):
    from test_installation_integration_f02 import legacy_case
    from sie_api.installation_service import create_snapshot, analyze_legacy
    from sie_api.domain.installation import CalculationRun
    installation, params = legacy_case()
    record = analyze_legacy(create_snapshot(installation), installation.circuits[1].id, params, 'test-rule')
    run = CalculationRun(id=uuid4(), name='Motor test run', project_id=installation.project.id, revision_id=installation.revisions[0].id, project_revision=installation.project.revision,
                         circuit_id=installation.circuits[1].id, input_sha256=record.input_sha256,
                         output_sha256='0'*64 if wrong_output else record.result_sha256,
                         algorithm_version=record.algorithm_version, rule_version=record.rule_version, state='VALID')
    installation.calculation_runs = [run]
    data = {'installation_snapshot': create_snapshot(installation).model_dump(mode='json')}
    if not missing_input:
        data['calculation_inputs_f10'] = {str(run.id): params.model_dump(mode='json')}
    pid = str(installation.project.id)
    repo.salvar(pid, 'Motor fixture', data, 0)
    return pid, str(run.id)


def test_motor_f10_executes_real_engine_persists_and_retries(tmp_path):
    import sqlite3
    repo = RepositorioProjetos(tmp_path / 'motor.sqlite3')
    pid, run = motor_revision(repo)
    assert repo.consultar_calculo_f10(pid, 1, run) is None
    evidence = repo.executar_calculo_f10(pid, 1, run)
    assert evidence['record']['result_json']
    assert evidence['record']['normative_conformity_verified'] is False
    reopened = RepositorioProjetos(tmp_path / 'motor.sqlite3')
    assert reopened.consultar_calculo_f10(pid, 1, run) == evidence
    assert reopened.executar_calculo_f10(pid, 1, run) == evidence
    with sqlite3.connect(repo.caminho) as db:
        assert db.execute('SELECT count(*) FROM execucoes_motor_f10').fetchone()[0] == 1
        with pytest.raises(sqlite3.IntegrityError):
            db.execute('DELETE FROM execucoes_motor_f10')
    assert repo.consultar_calculo_f10(str(uuid4()), 1, run) is None


@pytest.mark.parametrize('kwargs', [{'wrong_output': True}, {'missing_input': True}])
def test_motor_f10_rejects_unverified_run_and_rolls_back(tmp_path, kwargs):
    import sqlite3
    repo = RepositorioProjetos(tmp_path / 'motor.sqlite3')
    pid, run = motor_revision(repo, **kwargs)
    with pytest.raises(ValueError):
        repo.executar_calculo_f10(pid, 1, run)
    with sqlite3.connect(repo.caminho) as db:
        assert db.execute('SELECT count(*) FROM execucoes_motor_f10').fetchone()[0] == 0


def test_motor_f10_detects_persisted_evidence_tampering(tmp_path):
    import sqlite3
    repo = RepositorioProjetos(tmp_path / 'motor.sqlite3')
    pid, run = motor_revision(repo)
    repo.executar_calculo_f10(pid, 1, run)
    with sqlite3.connect(repo.caminho) as db:
        db.execute('DROP TRIGGER f10_execucao_sem_update')
        db.execute("UPDATE execucoes_motor_f10 SET hash_sha256=?", ('0'*64,))
    with pytest.raises(ValueError, match='Integridade'):
        repo.consultar_calculo_f10(pid, 1, run)


def test_motor_f10_failure_cannot_leave_success_row(tmp_path, monkeypatch):
    import sqlite3
    from sie_api import installation_service
    repo = RepositorioProjetos(tmp_path / 'motor.sqlite3')
    pid, run = motor_revision(repo)
    def interrupted(*args, **kwargs):
        raise RuntimeError('injected motor interruption')
    monkeypatch.setattr(installation_service, 'analyze_legacy', interrupted)
    with pytest.raises(RuntimeError, match='interruption'):
        repo.executar_calculo_f10(pid, 1, run)
    with sqlite3.connect(repo.caminho) as db:
        assert db.execute('SELECT count(*) FROM execucoes_motor_f10').fetchone()[0] == 0
