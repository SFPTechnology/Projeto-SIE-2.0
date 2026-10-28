"""New authenticated SIE 2.0 API namespace. Existing legacy routes unchanged."""
from __future__ import annotations

import json
import os
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from uuid import UUID

from fastapi import APIRouter, Depends, Header, HTTPException

from .auth_boundary_v201 import AuthIdentity, current_identity, require_project_owner, PROJECT_REF

router = APIRouter(prefix="/api/v2/sie", tags=["SIE2 authenticated development"])


@router.get("/auth/me")
def authenticated_user(identity: AuthIdentity = Depends(current_identity)):
    return {
        "user_id": str(identity.user_id),
        "expires_at": identity.expires_at,
        "auth_provider": "supabase",
        "authorization_source": "auth_server_verified",
        "normative_status": "NOT_EVALUATED",
    }


@router.get("/projects")
def list_owned_projects(
    identity: AuthIdentity = Depends(current_identity),
    authorization: str | None = Header(default=None),
):
    """B04 read-only, disabled by default; Supabase RLS + backend owner guard."""
    if os.environ.get("SIE_B04_READS_ENABLED") != "1":
        raise HTTPException(status_code=503, detail="Consulta de projetos nao habilitada")
    key = os.environ.get("SIE_SUPABASE_PUBLISHABLE_KEY", "").strip()
    if not key or key.startswith("sb_secret_"):
        raise HTTPException(status_code=503, detail="Verificacao de identidade indisponivel")
    params = urlencode({
        "select": "id,owner_id,name,created_at",
        "owner_id": "eq." + str(identity.user_id),
        "order": "created_at.desc",
        "limit": "100",
    })
    request = Request(
        f"https://{PROJECT_REF}.supabase.co/rest/v1/sie_projects?{params}",
        headers={
            "apikey": key,
            "Authorization": authorization,
            "Accept": "application/json",
        },
        method="GET",
    )
    try:
        with urlopen(request, timeout=5) as response:
            if response.status != 200:
                raise HTTPException(status_code=503, detail="Consulta indisponivel")
            result = json.loads(response.read(262144))
    except HTTPError as exc:
        if exc.code in (401, 403):
            raise HTTPException(status_code=401, detail="Sessao invalida") from None
        raise HTTPException(status_code=503, detail="Consulta indisponivel") from None
    except (URLError, TimeoutError, OSError, ValueError):
        raise HTTPException(status_code=503, detail="Consulta indisponivel") from None

    if not isinstance(result, list) or len(result) > 100:
        raise HTTPException(status_code=503, detail="Resposta invalida")
    projects = []
    for item in result:
        try:
            require_project_owner(identity, UUID(str(item["owner_id"])))
            projects.append({
                "id": str(UUID(str(item["id"]))),
                "name": str(item["name"]),
                "created_at": str(item["created_at"]),
            })
        except (ValueError, TypeError, KeyError, AttributeError):
            raise HTTPException(status_code=503, detail="Resposta invalida") from None
    return {"projects": projects, "count": len(projects), "read_only": True}
