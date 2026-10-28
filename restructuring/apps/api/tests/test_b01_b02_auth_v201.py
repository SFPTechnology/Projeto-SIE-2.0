"""B01/B02: mock Supabase Auth HTTP without claiming remote JWT validation."""
from __future__ import annotations

import base64
import json
import time
from urllib.error import HTTPError, URLError
from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from sie_api import auth_boundary_v201 as boundary
from sie_api.main import app

client = TestClient(app)
A = "11111111-1111-4111-8111-111111111111"
B = "22222222-2222-4222-8222-222222222222"


def token(**replacements):
    claims = {
        "sub": A,
        "exp": int(time.time()) + 3600,
        "iat": int(time.time()) - 5,
        "iss": boundary.AUTH_ISSUER,
        "aud": "authenticated",
        "role": "authenticated",
    }
    claims.update(replacements)
    encode = lambda value: base64.urlsafe_b64encode(
        json.dumps(value).encode("utf-8")).decode("ascii").rstrip("=")
    return encode({"alg": "RS256", "typ": "JWT"}) + "." + encode(claims) + ".signature"


class Response:
    status = 200

    def __init__(self, user):
        self.user = user

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def read(self, length):
        return json.dumps(self.user).encode("utf-8")


def mock_auth(monkeypatch, user=None, error=None):
    monkeypatch.setenv("SIE_SUPABASE_PUBLISHABLE_KEY", "sb_publishable_test_only")
    calls = []
    def open_mock(request, timeout):
        calls.append(request)
        assert request.full_url == boundary.USER_ENDPOINT
        assert timeout == 5
        assert request.get_header("Apikey") == "sb_publishable_test_only"
        if error:
            raise error
        return Response(user if user is not None else {"id": A, "is_anonymous": False})
    monkeypatch.setattr(boundary, "urlopen", open_mock)
    return calls


def test_no_bearer_is_401():
    assert client.get("/api/v2/sie/auth/me").status_code == 401


def test_bad_authorization_scheme_is_401():
    assert client.get("/api/v2/sie/auth/me",
                      headers={"Authorization": "Basic abc"}).status_code == 401


def test_invalid_token_format_is_401_and_no_network(monkeypatch):
    calls = mock_auth(monkeypatch)
    assert client.get("/api/v2/sie/auth/me",
        headers={"Authorization": "Bearer not-a-jwt"}).status_code == 401
    assert calls == []


@pytest.mark.parametrize("claim,wrong", [
    ("iss", "https://attacker.invalid/auth/v1"),
    ("aud", "service_role"),
    ("role", "service_role"),
    ("is_anonymous", True),
    ("exp", 1),
    ("iat", 9999999999),
])
def test_fail_closed_before_auth_http(monkeypatch, claim, wrong):
    calls = mock_auth(monkeypatch)
    res = client.get("/api/v2/sie/auth/me",
                     headers={"Authorization": "Bearer " + token(**{claim: wrong})})
    assert res.status_code == 401
    assert calls == []


def test_malformed_subject_is_401(monkeypatch):
    calls = mock_auth(monkeypatch)
    assert client.get("/api/v2/sie/auth/me",
       headers={"Authorization": "Bearer " + token(sub="attacker")}).status_code == 401
    assert not calls


def test_public_key_missing_fails_503_without_auth_fallback(monkeypatch):
    monkeypatch.delenv("SIE_SUPABASE_PUBLISHABLE_KEY", raising=False)
    assert client.get("/api/v2/sie/auth/me",
       headers={"Authorization": "Bearer " + token()}).status_code == 503


def test_secret_key_rejected_even_server_side(monkeypatch):
    monkeypatch.setenv("SIE_SUPABASE_PUBLISHABLE_KEY", "sb_secret_never_here")
    assert client.get("/api/v2/sie/auth/me",
       headers={"Authorization": "Bearer " + token()}).status_code == 503


def test_valid_auth_response_gates_success(monkeypatch):
    calls = mock_auth(monkeypatch)
    res = client.get("/api/v2/sie/auth/me",
                     headers={"Authorization": "Bearer " + token()})
    assert res.status_code == 200
    assert res.json()["user_id"] == A
    assert res.json()["authorization_source"] == "auth_server_verified"
    assert calls[0].get_header("Authorization").startswith("Bearer ")


def test_remote_identity_mismatch_denied(monkeypatch):
    mock_auth(monkeypatch, user={"id": B})
    assert client.get("/api/v2/sie/auth/me",
       headers={"Authorization": "Bearer " + token()}).status_code == 401


def test_remote_anonymous_account_denied(monkeypatch):
    mock_auth(monkeypatch, user={"id": A, "is_anonymous": True})
    assert client.get("/api/v2/sie/auth/me",
       headers={"Authorization": "Bearer " + token()}).status_code == 401


def test_auth_service_rejects_fake_signature(monkeypatch):
    mock_auth(monkeypatch,
              error=HTTPError(boundary.USER_ENDPOINT, 401, "unauthorized", {}, None))
    # A JWT-shaped token MUST be rejected when Auth says invalid.
    assert client.get("/api/v2/sie/auth/me",
       headers={"Authorization": "Bearer " + token()}).status_code == 401


def test_auth_service_unavailable_fails_closed(monkeypatch):
    mock_auth(monkeypatch, error=URLError("offline"))
    assert client.get("/api/v2/sie/auth/me",
       headers={"Authorization": "Bearer " + token()}).status_code == 503


def test_client_metadata_is_not_an_authority(monkeypatch):
    mock_auth(monkeypatch, user={"id": A, "user_metadata": {"role": "admin"}})
    res = client.get("/api/v2/sie/auth/me",
                     headers={"Authorization": "Bearer " + token()})
    assert res.status_code == 200
    assert "admin" not in json.dumps(res.json())


def test_owner_guard_uses_verified_identity():
    identity = boundary.AuthIdentity(UUID(A), expires_at=int(time.time()) + 100)
    boundary.require_project_owner(identity, UUID(A))
    with pytest.raises(Exception) as e:
        boundary.require_project_owner(identity, UUID(B))
    assert e.value.status_code == 404


@pytest.mark.parametrize("candidate", [
    "https://evil.invalid/auth/callback",
    "https://sie2.applicationmanager.com.br.evil.invalid/auth/callback",
    "https://sie2.applicationmanager.com.br@evil.invalid/auth/callback",
    "https://sie2.applicationmanager.com.br/reset",
    "http://sie2.applicationmanager.com.br/auth/callback",
    "http://localhost:5174/auth/callback",
    "https://sie2.applicationmanager.com.br/auth/callback#injected",
])
def test_redirect_rejects_untrusted_url(candidate):
    with pytest.raises(ValueError):
        boundary.validate_redirect(candidate)


def test_allowed_redirects():
    for url in ("http://localhost:5173/auth/callback",
                "http://127.0.0.1:5173/auth/callback",
                "https://sie2.applicationmanager.com.br/auth/callback"):
        assert boundary.validate_redirect(url) == url


def test_legacy_health_unmodified():
    assert client.get("/api/v1/health").status_code == 200
