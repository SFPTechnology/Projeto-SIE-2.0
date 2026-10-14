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
