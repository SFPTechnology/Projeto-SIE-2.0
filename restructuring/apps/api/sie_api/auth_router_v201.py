"""New authenticated SIE 2.0 API namespace. Existing legacy routes unchanged."""
from __future__ import annotations

from fastapi import APIRouter, Depends

from .auth_boundary_v201 import AuthIdentity, current_identity

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
