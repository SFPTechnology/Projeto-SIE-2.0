"""F01 snapshots: transaction, history, scope, immutability, auth and fail-closed."""
from dataclasses import replace
import json
import sqlite3
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from sie_api.main import app
from sie_api.storage import ConflitoRevisao, RepositorioProjetos
from sie_api.domain.normative import load_registry

client = TestClient(app)


def test_snapshot_pinned_by_project_revision_and_digest(tmp_path):
    repo = RepositorioProjetos(tmp_path / "new.sqlite3")
    id = str(uuid4())
    assert repo.salvar(id, "A", {"circuitos": []}, 0) == 1
    first = repo.snapshot_normativo(id, 1)
    assert first["revisao_projeto"] == 1
    assert first["catalogo_associado_na_gravacao"] is True
    assert first["regras_utilizadas_no_calculo_comprovadas"] is False
    assert first["snapshot"]["normative_conformity_verified"] is False
    assert first["snapshot"]["release_allowed"] is False
    assert first["snapshot"]["snapshot_kind"] == "CATALOG_METADATA_ONLY_NOT_RULES_USED"
    assert len(first["hash_sha256"]) == 64
    assert repo.salvar(id, "A2", {"circuitos": [{"nome": "X"}]}, 1) == 2
    second = repo.snapshot_normativo(id, 2)
    assert second["hash_sha256"] == first["hash_sha256"]
    assert repo.snapshot_normativo(id, 1) == first
    assert repo.carregar(id)["dados"]["circuitos"] == [{"nome": "X"}]


def test_existing_db_keeps_original_data_and_has_no_fake_backfill(tmp_path):
    path = tmp_path / "legacy.sqlite3"
    id = str(uuid4())
    with sqlite3.connect(path) as db:
        db.execute("CREATE TABLE projetos (id TEXT PRIMARY KEY, nome TEXT, dados_json TEXT, revisao INTEGER, atualizado_em TEXT)")
        db.execute("INSERT INTO projetos VALUES(?,?,?,?,?)", (id, "Legado", '{"original":true}', 1, "2026-10-01"))
    repo = RepositorioProjetos(path)
    assert repo.carregar(id)["dados"] == {"original": True}
    assert repo.snapshot_normativo(id, 1) is None
    assert repo.historico_snapshot_normativo(id) == []
    repo.salvar(id, "Legado-v2", {"original": True}, 1)
    assert repo.snapshot_normativo(id, 1) is None
    assert repo.snapshot_normativo(id, 2) is not None


def test_transaction_rejects_stale_revision_without_creating_snapshot(tmp_path):
    repo = RepositorioProjetos(tmp_path / "a.sqlite3")
    id = str(uuid4())
    repo.salvar(id, "A", {}, 0)
    with pytest.raises(ConflitoRevisao):
        repo.salvar(id, "Stale", {"corrente": 50}, 0)
    assert repo.snapshot_normativo(id, 2) is None
    assert len(repo.historico_snapshot_normativo(id)) == 1


def test_sqlite_triggers_protect_snapshot_and_audit_from_update_delete(tmp_path):
    repo = RepositorioProjetos(tmp_path / "a.sqlite3")
    id = str(uuid4())
    repo.salvar(id, "A", {}, 0)
    with pytest.raises(sqlite3.IntegrityError):
        with repo._conectar() as db:
            db.execute("UPDATE snapshots_normativos SET hash_sha256=? WHERE projeto_id=?", ("0"*64, id))
    with pytest.raises(sqlite3.IntegrityError):
        with repo._conectar() as db:
            db.execute("DELETE FROM snapshots_normativos WHERE projeto_id=?", (id,))
    with pytest.raises(sqlite3.IntegrityError):
        with repo._conectar() as db:
            db.execute("DELETE FROM eventos_snapshot_normativo WHERE projeto_id=?", (id,))
    assert repo.snapshot_normativo(id, 1) is not None


def test_version_change_produces_audit_diff_and_does_not_modify_old_snapshot(tmp_path, monkeypatch):
    import sie_api.normative_snapshots as snapshots
    repo = RepositorioProjetos(tmp_path / "project.sqlite3")
    id = str(uuid4())
    repo.salvar(id, "A", {}, 0)
    original = repo.snapshot_normativo(id, 1)
    canonical = load_registry()
    modified = tuple(
        replace(r, revision=2, edition="EDICAO-FICTICIA-APENAS-TESTE")
        if r.id == "ABNT-NBR-5410" else r for r in canonical
    )
    monkeypatch.setattr(snapshots, "load_registry", lambda: modified)
    impact = repo.impacto_normativo(id, 1)
    assert impact["changed"] is True
    assert impact["requires_technical_revalidation"] is True
    assert impact["release_allowed"] is False
    assert impact["recalculated_automatically"] is False
    assert impact["changes"] == [{
        "id": "ABNT-NBR-5410", "type": "ALTERADA",
        "old_revision": 1, "new_revision": 2,
    }]
    repo.salvar(id, "B", {}, 1)
    assert repo.snapshot_normativo(id, 1) == original
    assert repo.snapshot_normativo(id, 2)["hash_sha256"] != original["hash_sha256"]
    ev = repo.historico_snapshot_normativo(id)
    assert [e["revisao_projeto"] for e in ev] == [1, 2]
    assert ev[1]["impacto_no_salvamento"]["changed"] is True


def test_client_claim_of_normative_approval_cannot_modify_trusted_snapshot(tmp_path):
    repo = RepositorioProjetos(tmp_path / "safe.sqlite3")
    id = str(uuid4())
    repo.salvar(id, "Teste", {
        "approved": True, "verified_data": True, "release_allowed": True,
        "normative_conformity_verified": True,
    }, 0)
    snapshot = repo.snapshot_normativo(id, 1)["snapshot"]
    assert snapshot["release_allowed"] is False
    assert snapshot["normative_conformity_verified"] is False
    assert all(r["verified_data"] is False for r in snapshot["rules"])


def test_negative_snapshot_revision_rejected(tmp_path):
    repo = RepositorioProjetos(tmp_path / "safe.sqlite3")
    with pytest.raises(ValueError):
        repo.snapshot_normativo(str(uuid4()), -1)
    with pytest.raises(ValueError):
        repo.snapshot_normativo(str(uuid4()), True)


def test_snapshot_http_requires_local_bearer_and_returns_immutable_copy(tmp_path, monkeypatch):
    token = "test-only-" + "a"*35
    monkeypatch.setenv("SIE_LOCAL_API_TOKEN", token)
    monkeypatch.setenv("SIE_LOCAL_DB_PATH", str(tmp_path / "api.sqlite3"))
    id = str(uuid4())
    headers = {"Authorization": "Bearer " + token}
    response = client.put("/api/v1/local/projetos", headers=headers,
                          json={"id": id, "nome": "Exemplo",
                                "dados": {"release_allowed": True}, "revisao_esperada": 0})
    assert response.status_code == 200, response.text
    url = f"/api/v1/local/projetos/{id}/snapshots-normativos/1"
    assert client.get(url).status_code == 401
    assert client.get(url, headers={"Authorization": "Bearer " + "x"*35}).status_code == 401
    snapshot = client.get(url, headers=headers)
    assert snapshot.status_code == 200, snapshot.text
    assert snapshot.json()["snapshot"]["release_allowed"] is False
    assert snapshot.json()["regras_utilizadas_no_calculo_comprovadas"] is False
    assert client.get(f"/api/v1/local/projetos/{id}/snapshots-normativos/2", headers=headers).status_code == 404
    impact = client.get(f"/api/v1/local/projetos/{id}/impacto-normativo/1", headers=headers)
    assert impact.status_code == 200
    assert impact.json()["changed"] is False
    audit = client.get(f"/api/v1/local/projetos/{id}/historico-normativo", headers=headers)
    assert audit.status_code == 200
    assert len(audit.json()["eventos"]) == 1
    assert audit.json()["normative_conformity_verified"] is False


def test_integrity_verification_fails_closed_after_external_db_tampering(tmp_path):
    repo = RepositorioProjetos(tmp_path / "db.sqlite3")
    id = str(uuid4())
    repo.salvar(id, "A", {}, 0)
    with repo._conectar() as db:
        db.execute("DROP TRIGGER f01_snapshot_sem_update")
        db.execute("UPDATE snapshots_normativos SET catalogo_json='{}' WHERE projeto_id=?", (id,))
    with pytest.raises(ValueError, match="Hash"):
        repo.snapshot_normativo(id, 1)
