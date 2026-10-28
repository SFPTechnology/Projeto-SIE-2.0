"""B04 read-only adapter tests. Both HTTP boundaries are mocks; no real DB."""
from __future__ import annotations

import base64
import json
import time
from uuid import UUID

from fastapi.testclient import TestClient

from sie_api import auth_boundary_v201 as auth
from sie_api import auth_router_v201 as router
from sie_api.main import app

A = "11111111-1111-4111-8111-111111111111"
B = "22222222-2222-4222-8222-222222222222"
client = TestClient(app)


class Response:
    status = 200
    def __init__(self, data):
        self.data = data
    def __enter__(self):
        return self
    def __exit__(self, *_):
        return False
    def read(self, n):
        return json.dumps(self.data).encode()


def jwt():
    def b64(data):
        return base64.urlsafe_b64encode(json.dumps(data).encode()).decode().rstrip("=")
    return b64({"typ": "JWT", "alg": "RS256"}) + "." + b64({
        "sub": A, "exp": int(time.time())+3600, "iss": auth.AUTH_ISSUER,
        "aud": "authenticated", "role": "authenticated",
    }) + ".fake"


def setup(monkeypatch, projects, enabled=True):
    monkeypatch.setenv("SIE_SUPABASE_PUBLISHABLE_KEY", "sb_publishable_fixture")
    if enabled:
        monkeypatch.setenv("SIE_B04_READS_ENABLED", "1")
    else:
        monkeypatch.delenv("SIE_B04_READS_ENABLED", raising=False)
    monkeypatch.setattr(auth, "urlopen",
                        lambda request, timeout: Response({"id": A, "is_anonymous": False}))
    calls=[]
    def fake_rest(request, timeout):
        calls.append(request)
        assert request.full_url.startswith(
            f"https://{auth.PROJECT_REF}.supabase.co/rest/v1/sie_projects?")
        assert "owner_id=eq." in request.full_url
        assert request.get_header("Apikey") == "sb_publishable_fixture"
        assert request.get_header("Authorization").startswith("Bearer ")
        return Response(projects)
    monkeypatch.setattr(router, "urlopen", fake_rest)
    return calls


def test_read_disabled_without_flag_and_no_external_query(monkeypatch):
    calls=setup(monkeypatch, [], enabled=False)
    result=client.get("/api/v2/sie/projects", headers={"Authorization":"Bearer "+jwt()})
    assert result.status_code==503
    assert calls == []


def test_owned_projects_read_uses_rls_and_owner_guard(monkeypatch):
    calls=setup(monkeypatch, [{
        "id":"aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
        "owner_id":A, "name":"Residencia A", "created_at":"2026-10-28T11:00:00Z"}])
    result=client.get("/api/v2/sie/projects",headers={"Authorization":"Bearer "+jwt()})
    assert result.status_code==200
    assert result.json()["read_only"] is True
    assert result.json()["count"]==1
    assert "owner_id" not in result.json()["projects"][0]
    assert len(calls)==1


def test_cross_owner_row_from_broken_adapter_fails_closed(monkeypatch):
    setup(monkeypatch, [{
        "id":"aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa",
        "owner_id":B,"name":"Projeto B", "created_at":"2026-10-28"}])
    result=client.get("/api/v2/sie/projects",headers={"Authorization":"Bearer "+jwt()})
    assert result.status_code==404


def test_unverified_request_never_reaches_rest_adapter(monkeypatch):
    calls=setup(monkeypatch, [])
    result=client.get("/api/v2/sie/projects")
    assert result.status_code==401
    assert calls == []


def test_malformed_rest_payload_fails_closed(monkeypatch):
    setup(monkeypatch, [{"id":"not-a-uuid","owner_id":A,"name":"x", "created_at":"now"}])
    assert client.get("/api/v2/sie/projects",
        headers={"Authorization":"Bearer "+jwt()}).status_code==503
