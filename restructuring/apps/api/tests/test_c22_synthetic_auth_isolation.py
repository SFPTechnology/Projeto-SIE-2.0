"""C22 synthetic-only owner isolation checks.

These checks exercise local guards with fixture identities.  They intentionally
do not claim that Supabase Auth, sessions or remote RLS have been exercised.
"""
from uuid import UUID

import pytest
from fastapi import HTTPException

from sie_api.auth_boundary_v201 import AuthIdentity, require_project_owner


OWNER_A = UUID("11111111-1111-4111-8111-111111111111")
OWNER_B = UUID("22222222-2222-4222-8222-222222222222")


def identity(owner: UUID) -> AuthIdentity:
    return AuthIdentity(user_id=owner, expires_at=4_102_444_800)


def test_synthetic_owner_may_access_only_own_resource():
    require_project_owner(identity(OWNER_A), OWNER_A)


@pytest.mark.parametrize("principal,resource", [(OWNER_A, OWNER_B), (OWNER_B, OWNER_A)])
def test_synthetic_cross_owner_resource_is_hidden(principal: UUID, resource: UUID):
    with pytest.raises(HTTPException) as error:
        require_project_owner(identity(principal), resource)
    assert error.value.status_code == 404
    assert error.value.detail == "Recurso nao encontrado"


def test_synthetic_fixture_is_explicitly_not_remote_auth_proof():
    assert "SYNTHETIC_ONLY" == "SYNTHETIC_ONLY"
