"""F01: histórico local íntegro, por revisão, sem backfill nem homologação inventada."""
import sqlite3
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from sie_api.main import app
from sie_api.storage import ConflitoRevisao, RepositorioProjetos

client = TestClient(app)


def test_full_revisions_are_persisted_atomically_and_not_recomputed(tmp_path):
    repo = RepositorioProjetos(tmp_path / "hist.sqlite")
    pid = str(uuid4())
    repo.salvar(pid, "Projeto 1", {"circuitos": [{"nome": "A", "corrente_a": 12}]}, 0)
    old = repo.carregar_revisao(pid, 1)
    repo.salvar(pid, "Projeto 2", {"circuitos": [{"nome": "B"}]}, 1)
    assert repo.carregar_revisao(pid, 1) == old
    assert repo.carregar_revisao(pid, 2)["nome"] == "Projeto 2"
    assert old["dados"]["circuitos"] == [{"nome": "A", "corrente_a": 12}]
    assert old["normative_conformity_verified"] is False
    assert old["regras_efetivamente_usadas_comprovadas"] is False
    assert [x["revisao"] for x in repo.listar_revisoes(pid)] == [1, 2]
    assert repo.carregar(pid)["revisao"] == 2
    assert repo.snapshot_normativo(pid, 1) is not None


def test_revision_conflict_leaves_all_history_unchanged(tmp_path):
    repo = RepositorioProjetos(tmp_path / "hist.sqlite")
    pid = str(uuid4())
    repo.salvar(pid, "A", {}, 0)
    with pytest.raises(ConflitoRevisao):
        repo.salvar(pid, "B", {"revisao": 2}, 0)
    assert [x["revisao"] for x in repo.listar_revisoes(pid)] == [1]
    assert repo.carregar_revisao(pid, 2) is None


def test_legacy_revision_is_not_backfilled(tmp_path):
    path = tmp_path / "legacy.sqlite"
    pid = str(uuid4())
    with sqlite3.connect(path) as db:
        db.execute("CREATE TABLE projetos (id TEXT PRIMARY KEY,nome TEXT NOT NULL,"
                   "dados_json TEXT NOT NULL,revisao INTEGER NOT NULL,"
                   "atualizado_em TEXT NOT NULL)")
        db.execute("INSERT INTO projetos VALUES(?,?,?,?,?)",
                   (pid, "Antigo", '{"v": 1}', 4, "2026-09-01"))
    repo = RepositorioProjetos(path)
    assert repo.carregar_revisao(pid, 4) is None
    assert repo.listar_revisoes(pid) == []
    repo.salvar(pid, "Atualizado", {"v": 5}, 4)
    assert repo.carregar_revisao(pid, 5)["dados"] == {"v": 5}
    assert repo.carregar_revisao(pid, 4) is None


def test_immutable_history_and_detects_tampering(tmp_path):
    repo = RepositorioProjetos(tmp_path / "hist.sqlite")
    pid = str(uuid4())
    repo.salvar(pid, "Original", {"x": 1}, 0)
    with pytest.raises(sqlite3.IntegrityError):
        with repo._conectar() as db:
            db.execute("UPDATE versoes_projeto SET dados_json='{}' WHERE projeto_id=?", (pid,))
    with pytest.raises(sqlite3.IntegrityError):
        with repo._conectar() as db:
            db.execute("DELETE FROM versoes_projeto WHERE projeto_id=?", (pid,))
    assert repo.carregar_revisao(pid, 1)["dados"] == {"x": 1}
    with repo._conectar() as db:
        db.execute("DROP TRIGGER f01_versao_sem_update")
        db.execute("UPDATE versoes_projeto SET dados_json='{}' WHERE projeto_id=?", (pid,))
    with pytest.raises(ValueError, match="Integridade"):
        repo.carregar_revisao(pid, 1)


@pytest.mark.parametrize("revision", [-1, 0, True, 1.5])
def test_reject_invalid_revision(tmp_path, revision):
    repo = RepositorioProjetos(tmp_path / "hist.sqlite")
    with pytest.raises(ValueError, match="Revisao"):
        repo.carregar_revisao(str(uuid4()), revision)


def test_api_history_token_revision_and_404(tmp_path, monkeypatch):
    token = "test-only-" + "b"*36
    monkeypatch.setenv("SIE_LOCAL_API_TOKEN", token)
    monkeypatch.setenv("SIE_LOCAL_DB_PATH", str(tmp_path / "api.sqlite"))
    pid = str(uuid4())
    headers = {"Authorization": "Bearer " + token}
    payload = {"id": pid, "nome": "Inicial", "dados": {"circuitos": [{"nome": "A"}]},
               "revisao_esperada": 0}
    assert client.put("/api/v1/local/projetos", json=payload, headers=headers).status_code == 200
    payload.update(nome="Atualizado", dados={"circuitos": [{"nome": "B"}]},
                   revisao_esperada=1)
    assert client.put("/api/v1/local/projetos", json=payload, headers=headers).status_code == 200
    base = f"/api/v1/local/projetos/{pid}/revisoes"
    assert client.get(base).status_code == 401
    assert client.get(base, headers={"Authorization": "Bearer " + "x"*36}).status_code == 401
    resp = client.get(base, headers=headers)
    assert resp.status_code == 200
    assert [x["revisao"] for x in resp.json()["revisoes"]] == [1, 2]
    assert client.get(base + "/1", headers=headers).json()["dados"] == {"circuitos": [{"nome": "A"}]}
    assert client.get(base + "/2", headers=headers).json()["dados"] == {"circuitos": [{"nome": "B"}]}
    assert client.get(base + "/3", headers=headers).status_code == 404
    assert client.get(base + "/0", headers=headers).status_code == 409
    assert client.get(f"/api/v1/local/projetos/{uuid4()}/revisoes", headers=headers).status_code == 404
