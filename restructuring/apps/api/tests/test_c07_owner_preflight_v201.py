from uuid import UUID
import pytest
from sie_api.v201_c_legacy_owner_preflight import preflight_owners

ONE="11111111-1111-4111-8111-111111111111"
TWO="22222222-2222-4222-8222-222222222222"
def claims():
    return {"src-1":{"target_owner_auth_uuid":ONE,"approval_reference":"signed-external-01"},
            "src-2":{"target_owner_auth_uuid":TWO,"approval_reference":"signed-external-02"}}

def test_structurally_complete_never_authorizes_migration():
    result=preflight_owners(["src-1","src-2"],claims(),10)
    assert result["projects_mapped"]==2
    assert result["quarantined_audit_orphans"]==10
    assert result["structural_mapping"]=="PASS"
    assert len(result["mapping_sha256"])==64
    assert result["state"]=="HUMAN_REQUIRED"
    assert result["migration_authorized"] is False
    assert "HUMAN_ATTESTATION" in result["authority_status"]
    assert result==preflight_owners(["src-2","src-1"],claims(),10)

def test_rejects_owner_gaps_and_untrusted_identity_claims():
    with pytest.raises(ValueError):
        preflight_owners(["src-1","src-2"],{"src-1":claims()["src-1"]})
    with pytest.raises(ValueError):
        preflight_owners(["src-1","src-1"],claims())
    with pytest.raises(ValueError):
        preflight_owners([],claims())
    with pytest.raises(ValueError):
        preflight_owners(["src-1","src-2"],{**claims(),"other":claims()["src-1"]})
    bad=claims()
    bad["src-2"]={"target_owner_auth_uuid":"unknown","approval_reference":"fake-approval"}
    with pytest.raises(ValueError):
        preflight_owners(["src-1","src-2"],bad)

def test_claimed_approval_never_becomes_authority():
    fake=claims()
    fake["src-1"]["approval_reference"]="signed-by-me-APPROVED"
    r=preflight_owners(["src-1","src-2"],fake,0)
    assert r["migration_authorized"] is False
