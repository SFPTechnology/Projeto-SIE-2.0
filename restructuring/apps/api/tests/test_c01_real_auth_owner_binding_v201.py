"""C01: prove real Auth is not replaceable by fabricated UUID or JSON."""
from pathlib import Path
from uuid import UUID
import json
import pytest
from sie_api.v201_c_auth_owner_binding import (
    check_real_auth_user,check_owner_selection,EXPECTED_IDS,DEST)

P=Path(__file__).resolve().parents[4]/"docs/implantacao-sie-2-0/GREENFIELD/C01_C07_SELECTION_ALL_FIVE_V201.json"
OWNER="11111111-1111-4111-8111-111111111111"

class FakeCursor:
    def __init__(self,rows):self.rows=rows
    def __enter__(self):return self
    def __exit__(self,*args):pass
    def execute(self,query,args):
        assert query.lstrip().startswith("SELECT id")
        assert "FROM auth.users WHERE id=%s" in query
        assert args==(UUID(OWNER),)
    def fetchone(self):return self.rows

class FakeDb:
    def __init__(self,rows):self.rows=rows
    def cursor(self):return FakeCursor(self.rows)

def manifest():
    return json.loads(P.read_text(encoding="utf-8"))

def selection_binding():
    return {key:OWNER for key in EXPECTED_IDS}

def test_missing_user_readback_never_grants_identity_or_migration():
    proof=check_real_auth_user(FakeDb(None),project_ref=DEST,verified_jwt_subject=OWNER)
    assert proof["identity_status"]=="NOT_FOUND"
    assert proof["auth_user_verified"] is False
    status=check_owner_selection(manifest(),selection_binding(),proof)
    assert status["project_scope_status"]=="FIVE_OF_FIVE_SELECTED"
    assert status["auth_readback_required"] is True
    assert status["binding_applied"] is False
    assert status["migration_authorized"] is False

def test_verified_mock_user_is_not_a_real_import_go():
    proof=check_real_auth_user(FakeDb((UUID(OWNER),True)),
          project_ref=DEST,verified_jwt_subject=OWNER)
    assert proof["identity_status"]=="AUTH_CONFIRMED"
    status=check_owner_selection(manifest(),selection_binding(),proof)
    assert status["auth_readback_required"] is False
    assert status["independent_owner_attestation_required"] is True
    assert status["binding_applied"] is False
    assert status["migration_authorized"] is False

def test_rejects_other_destination_and_unconfirmed_auth():
    with pytest.raises(ValueError):
        check_real_auth_user(FakeDb(None),project_ref="another",verified_jwt_subject=OWNER)
    proof=check_real_auth_user(FakeDb((UUID(OWNER),False)),
          project_ref=DEST,verified_jwt_subject=OWNER)
    assert proof["identity_status"]=="AUTH_EMAIL_UNCONFIRMED"
    assert proof["auth_user_verified"] is False

def test_partial_or_mixed_owner_and_forged_source_rejected():
    subset=selection_binding()
    subset.pop("proj-1")
    with pytest.raises(ValueError):
        check_owner_selection(manifest(),subset,{})
    split=selection_binding()
    split["proj-1"]="22222222-2222-4222-8222-222222222222"
    with pytest.raises(ValueError):
        check_owner_selection(manifest(),split,{})
    document=manifest()
    document["source"]["project_ref"]="fake"
    with pytest.raises(ValueError):
        check_owner_selection(document,selection_binding(),{})
