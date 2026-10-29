"""C12 machine report inventory cannot be rewritten as a normative approval."""
from pathlib import Path
import pytest
from sie_api.v201_c_e01_e11_evidence import EVALUATORS, run_suite

BASE=Path(__file__).resolve().parents[4]
DOSSIER=BASE/"docs/implantacao-sie-2-0/GREENFIELD/C12_DOSSIE_VALIDACAO_EVIDENCIAS_ELETRICAS_V201.md"

def test_c12_documents_eleven_actual_cases_and_retains_normative_block():
    body=DOSSIER.read_text(encoding="utf-8")
    result=run_suite(sha="offline-review")
    assert len(result["cases"])==11
    for code in sorted(EVALUATORS):
        assert "| "+code+" |" in body
    assert "40792906157" in body
    assert "12862776242" in body
    assert "NOT_EVALUATED" in body
    assert "PROFESSIONAL_APPROVAL=NOT_GRANTED" in body
    assert "NÃO é homologação integral" in body
    assert result["gc"]=="BLOCKED"
    assert result["professional_approval"]=="NOT_GRANTED"

def test_c12_rejects_missing_evidence_link_or_group(monkeypatch):
    body=DOSSIER.read_text(encoding="utf-8")
    assert "E01" in body and "E11" in body
    assert all(item["professional_signature"] is None for item in run_suite()["cases"])
