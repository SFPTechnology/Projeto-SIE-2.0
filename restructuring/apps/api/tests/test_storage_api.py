from uuid import uuid4

from fastapi.testclient import TestClient
from sie_api.main import app

client = TestClient(app)


def test_storage_disabled_by_default(monkeypatch):
    monkeypatch.delenv("SIE_LOCAL_API_TOKEN", raising=False)
    monkeypatch.delenv("SIE_LOCAL_DB_PATH", raising=False)
    assert client.put("/api/v1/local/projetos", json={}).status_code == 422
    # Read operation reaches the security gate, and must refuse service.
    assert client.get(f"/api/v1/local/projetos/{uuid4()}").status_code == 503


def test_authentication_required_for_local_storage(tmp_path, monkeypatch):
    monkeypatch.setenv("SIE_LOCAL_API_TOKEN", "this-is-a-long-unique-test-only-token")
    monkeypatch.setenv("SIE_LOCAL_DB_PATH", str(tmp_path / "sie.db"))
    assert client.get(f"/api/v1/local/projetos/{uuid4()}").status_code == 401
    assert client.get(
        f"/api/v1/local/projetos/{uuid4()}",
        headers={"Authorization": "Bearer invalid"},
    ).status_code == 401


def test_local_project_create_update_conflict_and_audit(tmp_path, monkeypatch):
    token = "a-minimum-24-char-local-test-token"
    monkeypatch.setenv("SIE_LOCAL_API_TOKEN", token)
    monkeypatch.setenv("SIE_LOCAL_DB_PATH", str(tmp_path / "sie.db"))
    headers = {"Authorization": f"Bearer {token}"}
    pid = str(uuid4())
    body = {
        "id": pid, "nome": "Casa", "dados": {"circuitos": [{"nome": "TUG1"}]},
        "revisao_esperada": 0,
    }
    created = client.put("/api/v1/local/projetos", headers=headers, json=body)
    assert created.status_code == 200
    assert created.json()["revisao"] == 1
    assert client.get(f"/api/v1/local/projetos/{pid}", headers=headers).json()["nome"] == "Casa"
    assert client.put("/api/v1/local/projetos", headers=headers, json=body).status_code == 409
    updated = client.put("/api/v1/local/projetos", headers=headers, json={
        **body, "nome": "Casa revisada", "revisao_esperada": 1,
    })
    assert updated.status_code == 200
    assert updated.json()["revisao"] == 2
    historico = client.get(f"/api/v1/local/projetos/{pid}/historico", headers=headers)
    assert historico.status_code == 200
    assert [e["revisao"] for e in historico.json()["eventos"]] == [1, 2]


def test_local_storage_does_not_return_nonexistent_project(tmp_path, monkeypatch):
    token = "another-24-character-safe-test-token"
    monkeypatch.setenv("SIE_LOCAL_API_TOKEN", token)
    monkeypatch.setenv("SIE_LOCAL_DB_PATH", str(tmp_path / "sie.db"))
    result = client.get(
        f"/api/v1/local/projetos/{uuid4()}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert result.status_code == 404
