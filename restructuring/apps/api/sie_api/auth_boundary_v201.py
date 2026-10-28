"""B01/B02 — Supabase Auth boundary for NEW SIE 2.0 v2 routes.

Verification is delegated to Supabase Auth /auth/v1/user via HTTPS.
Auth validates JWT signature/expiry using the project's configured signing
mode (asymmetric or legacy). Local unverified claims are used only as
ADDITIONAL fail-closed consistency checks, NEVER to grant authorization.
No service_role secret, local token fallback or user_metadata authorization.
"""
from __future__ import annotations

import base64
from dataclasses import dataclass
import json
import os
import time
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit
from uuid import UUID

from fastapi import Header, HTTPException

PROJECT_REF = "fozrymsidnaxmuvxxfhh"
AUTH_ISSUER = f"https://{PROJECT_REF}.supabase.co/auth/v1"
USER_ENDPOINT = AUTH_ISSUER + "/user"
MAX_TOKEN_LENGTH = 8192
ALLOWED_AUDIENCE = "authenticated"


@dataclass(frozen=True)
class AuthIdentity:
    user_id: UUID
    expires_at: int


def validate_redirect(value: str) -> str:
    """Redirects are exact-config allowlisted; never accept caller-added hosts."""
    try:
        url = urlsplit(value)
    except ValueError:
        raise ValueError("Invalid Auth redirect") from None
    valid_origins = {
        ("http", "localhost", 5173),
        ("http", "127.0.0.1", 5173),
        ("https", "sie2.applicationmanager.com.br", 443),
    }
    try:
        port = url.port or (443 if url.scheme == "https" else 80)
    except ValueError:
        raise ValueError("Invalid Auth redirect") from None
    if (url.scheme, url.hostname, port) not in valid_origins or url.username or url.password:
        raise ValueError("Auth redirect origin is not allowlisted")
    if url.fragment or url.query or url.path not in ("", "/", "/auth/callback"):
        raise ValueError("Auth redirect path is not allowlisted")
    return value


def _error(status: int, message: str) -> HTTPException:
    return HTTPException(status_code=status, detail=message)


def _unverified_claims(token: str) -> dict:
    """Format checks only. This is NOT signature verification."""
    parts = token.split(".")
    if len(parts) != 3 or not all(parts) or len(token) > MAX_TOKEN_LENGTH:
        raise _error(401, "Sessao invalida")
    try:
        raw = base64.urlsafe_b64decode(parts[1] + "=" * (-len(parts[1]) % 4))
        data = json.loads(raw)
        if not isinstance(data, dict):
            raise ValueError("claims must be object")
        return data
    except (ValueError, UnicodeError, TypeError):
        raise _error(401, "Sessao invalida") from None


def verify_supabase_token(token: str) -> AuthIdentity:
    """Require the real project's Auth service to authenticate the bearer."""
    claims = _unverified_claims(token)
    try:
        sub = UUID(str(claims["sub"]))
        expiry = claims["exp"]
        issued_at = claims.get("iat")
        if not isinstance(expiry, int) or isinstance(expiry, bool):
            raise ValueError("Bad expiry")
        if issued_at is not None and (not isinstance(issued_at, int) or issued_at > int(time.time()) + 60):
            raise ValueError("Bad issue timestamp")
        if expiry <= int(time.time()) or claims["iss"] != AUTH_ISSUER:
            raise ValueError("Expired or wrong issuer")
        audience = claims.get("aud")
        if audience != ALLOWED_AUDIENCE:
            raise ValueError("Wrong audience")
        if claims.get("role") != "authenticated" or claims.get("is_anonymous") is True:
            raise ValueError("Wrong role")
    except (KeyError, TypeError, ValueError, AttributeError):
        raise _error(401, "Sessao invalida") from None

    # Publishable/anon key is a PUBLIC client identifier; never use service_role.
    public_key = os.environ.get("SIE_SUPABASE_PUBLISHABLE_KEY", "").strip()
    if not public_key or public_key.startswith("sb_secret_") or len(public_key) > 2048:
        raise _error(503, "Verificacao de identidade indisponivel")
    request = Request(
        USER_ENDPOINT,
        method="GET",
        headers={"apikey": public_key, "Authorization": f"Bearer {token}",
                 "Accept": "application/json"},
    )
    try:
        with urlopen(request, timeout=5) as response:
            if response.status != 200:
                raise _error(401, "Sessao invalida")
            payload = json.loads(response.read(65536))
    except HTTPError as exc:
        if exc.code in (400, 401, 403):
            raise _error(401, "Sessao invalida") from None
        raise _error(503, "Verificacao de identidade indisponivel") from None
    except (URLError, TimeoutError, OSError, ValueError, json.JSONDecodeError):
        raise _error(503, "Verificacao de identidade indisponivel") from None

    # This data is trusted only because it was returned from the real Auth
    # endpoint over HTTPS for this exact bearer.
    try:
        remote_id = UUID(str(payload["id"]))
        if remote_id != sub or payload.get("is_anonymous") is True:
            raise ValueError("Identity mismatch / anonymous user")
    except (KeyError, AttributeError, TypeError, ValueError):
        raise _error(401, "Sessao invalida") from None
    return AuthIdentity(user_id=remote_id, expires_at=expiry)


def current_identity(authorization: str | None = Header(default=None)) -> AuthIdentity:
    if authorization is None:
        raise _error(401, "Autenticacao obrigatoria")
    prefix, separator, token = authorization.partition(" ")
    if not separator or prefix.lower() != "bearer" or not token or token != token.strip():
        raise _error(401, "Sessao invalida")
    return verify_supabase_token(token)


def require_project_owner(identity: AuthIdentity, owner_id: UUID) -> None:
    """Server-side ownership guard before any privileged service_role query."""
    if identity.user_id != owner_id:
        raise _error(404, "Recurso nao encontrado")
