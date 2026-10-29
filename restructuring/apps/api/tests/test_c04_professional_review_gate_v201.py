"""C04/C05 structural review readiness, never professional self-approval."""
from pathlib import Path
from copy import deepcopy
import json
import pytest
from sie_api.v201_c_professional_review_gate import verify_review_packet

BASE=Path(__file__).resolve().parents[4]
def packet():
    return json.loads((BASE/"docs/implantacao-sie-2-0/GREENFIELD/C04_C05_DOSSIE_ACEITE_PROFISSIONAL_V201.json").read_text(encoding="utf-8"))
def catalog():
    return json.loads((BASE/"restructuring/apps/api/sie_api/data/normative_registry.json").read_text(encoding="utf-8"))

def test_complete_review_packet_is_not_approval():
    r=verify_review_packet(packet(),catalog())
    assert r["required_cases"]==11
    assert r["review_packet"]=="STRUCTURAL_PASS"
    assert r["normative_catalog_verified"] is False
    assert r["electrical_acceptance"]=="NOT_APPROVED"
    assert r["external_professional_attestation"]=="MISSING"
    assert r["gate_gc"]=="BLOCKED"

def test_forged_acceptance_or_signature_rejected():
    p=packet()
    p["normative_approved"]=True
    with pytest.raises(ValueError):
        verify_review_packet(p,catalog())
    p=packet()
    p["professional_review"]["external_signature_or_process_ref"]="fake-approval"
    with pytest.raises(ValueError):
        verify_review_packet(p,catalog())
    p=packet()
    p["requirements"][0]["state"]="APPROVED"
    with pytest.raises(ValueError):
        verify_review_packet(p,catalog())
    p=packet()
    p["references"][0]["status"]="APPROVED"
    with pytest.raises(ValueError):
        verify_review_packet(p,catalog())

def test_missing_case_or_registry_reference_rejected():
    p=packet()
    p["requirements"].pop()
    with pytest.raises(ValueError):
        verify_review_packet(p,catalog())
    p=packet()
    p["references"][0]["id"]="nonexistent"
    with pytest.raises(ValueError):
        verify_review_packet(p,catalog())
