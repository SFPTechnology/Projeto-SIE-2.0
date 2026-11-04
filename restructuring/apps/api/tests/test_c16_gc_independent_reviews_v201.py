"""C16: eight isolated review roles, negative GC release, and proof completeness."""
from __future__ import annotations

import copy
import importlib.util
import json
from pathlib import Path

import pytest

ROOT=Path(__file__).resolve().parents[4]
DOCS=ROOT/"docs/implantacao-sie-2-0/GREENFIELD"
SPEC=importlib.util.spec_from_file_location("c16_gate",ROOT/"scripts/c16_gc_independent_gate.py")
assert SPEC and SPEC.loader
gate=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)


def load():
    return (
        json.loads((DOCS/"C08_CONTRATO_ENTREGA_C_V201.json").read_text(encoding="utf-8")),
        json.loads((DOCS/"C16_RELATORIO_AUDITORIA_GC_20261104.json").read_text(encoding="utf-8"))
    )


def test_eight_independent_roles_have_unique_prompts_and_evidence():
    contract,reviews=load()
    result=gate.assess(contract,reviews)
    assert result["verdict"]=="BLOCKED"
    assert result["independent_reviewers"]==8
    assert "destination_real_restore_verified" in result["evidence_pending"]
    assert "professional_c13_signed_and_verified" in result["evidence_pending"]
    assert result["remote_ddl_permitted_by_this_check"] is False
    assert result["automatic_release"] is False
    for r in reviews["reviewers"]:
        path=ROOT/".github/agents"/(r["agent"]+".agent.md")
        assert path.is_file()
        content=path.read_text(encoding="utf-8")
        assert "20 anos de experiência" in content
        assert "GC" in content and "evidência" in content.lower()


@pytest.mark.parametrize("field",[
    "destination_real_backup_verified",
    "destination_real_restore_verified",
    "trusted_jwt_subject_verified",
    "professional_c13_signed_and_verified",
    "remote_migrations_4_of_4_applied",
    "independent_auditor_go",
])
def test_partial_bool_changes_do_not_grant_release(field):
    contract,reviews=load()
    reviews["mandatory_real_evidence"][field]=True
    result=gate.assess(contract,reviews)
    assert result["verdict"]=="BLOCKED"
    assert result["automatic_release"] is False


def test_self_declared_gc_pass_without_real_proof_is_rejected():
    contract,reviews=load()
    contract["state"]="PASS"
    with pytest.raises(ValueError,match="premature"):
        gate.assess(contract,reviews)
    contract["state"]="BLOCKED"
    reviews["overall_verdict"]="GC_PASS"
    with pytest.raises(ValueError,match="premature"):
        gate.assess(contract,reviews)


def test_no_bypass_by_claiming_authorized_migrations_without_backup():
    contract,reviews=load()
    contract["preproduction_authorization"]["migration_application_permitted_now"]=True
    with pytest.raises(ValueError,match="premature"):
        gate.assess(contract,reviews)


def test_missing_reviewer_or_malformed_proof_rejected():
    contract,reviews=load()
    reviews["reviewers"]=reviews["reviewers"][:-1]
    with pytest.raises(ValueError,match="reviewer"):
        gate.assess(contract,reviews)
    contract,reviews=load()
    reviews["mandatory_real_evidence"].pop("destination_real_backup_verified")
    with pytest.raises(ValueError,match="required real-evidence"):
        gate.assess(contract,reviews)


def test_all_editable_claims_still_require_independent_external_validation():
    contract,reviews=load()
    reviews["mandatory_real_evidence"]={k:True for k in gate.REAL}
    for role in reviews["reviewers"]:
        role["status"]="PASS_REAL_VERIFIED"
    assert gate.assess(contract,reviews)["verdict"]=="ELIGIBLE_FOR_EXTERNAL_HUMAN_AND_OPERATIONAL_VERIFICATION"
    assert not gate.assess(contract,reviews)["automatic_release"]


def test_real_legacy_etl_and_c13_not_yet_equivalent_to_test_fixture():
    _,reviews=load()
    assert reviews["mandatory_real_evidence"]["real_etl_pass"] is False
    assert reviews["mandatory_real_evidence"]["professional_c13_signed_and_verified"] is False
    assert reviews["read_only_live_inventory"]["origin_operational_rows"]==1934
    assert reviews["read_only_live_inventory"]["destination_auth_sessions"]==0
    assert reviews["read_only_live_inventory"]["destination_storage_objects"]==0
    code=(ROOT/"restructuring/apps/api/sie_api/v201_c_etl.py").read_text()
    assert 'value["source_kind"] != "SYNTHETIC_TEST"' in code
