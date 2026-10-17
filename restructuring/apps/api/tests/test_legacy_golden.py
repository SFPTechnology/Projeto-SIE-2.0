"""Behavioral baseline only; known unsafe edge cases are explicitly labeled.

Independent formula checks remain in test_engines.py and QA-02.md. Never infer
engineering correctness or normative conformity from these snapshot comparisons.
"""
import importlib.util
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[4]
SPEC = importlib.util.spec_from_file_location("f00_golden", ROOT / "scripts/f00_golden.py")
GOLDEN = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(GOLDEN)
FIXTURE = json.loads(Path(__file__).with_name("fixtures").joinpath("f00_legacy_golden.json").read_text(encoding="utf-8"))


def test_fixture_records_original_revision_and_scope():
    assert FIXTURE["baseline_sha"] == GOLDEN.BASELINE_SHA
    assert FIXTURE["output_class"] == "characterization_only_not_normative_validation"
    assert len(FIXTURE["source_sha256"]) >= 10
    assert all(len(value) == 64 for value in FIXTURE["source_sha256"].values())
    assert {c["id"] for c in FIXTURE["cases"] if c["known_anomaly"]} == {
        "ANALISE-IZ-ARREDONDADO", "EDP-U-CARGA-TRIFASICA",
    }


@pytest.mark.parametrize("case", FIXTURE["cases"], ids=lambda case: case["id"])
def test_current_behavior_matches_frozen_legacy(case):
    """F00 is rechecked at original SHA by --verify, not forced onto safe F01 changes.

    Deliberate deviations to conductor precision, breaker safety and unverified
    EDP provenance are tested here as stricter F01 constraints, not silently
    accepted by rewriting the original fixture.
    """
    actual = GOLDEN.evaluate(case)
    op = case["operation"]
    if op == "conductor":
        assert "result" in actual or "error_type" in actual
        if "result" in actual:
            assert actual["result"]["secao_mm2"] == case["expected"]["result"]["secao_mm2"]
            assert actual["result"]["criterio"] == "Iz_base × fatores ≥ Ib"
        return
    if op == "analysis":
        if case["id"] == "ANALISE-IZ-ARREDONDADO":
            assert actual == {
                "error_type": "ValueError",
                "error_message": "Nenhum disjuntor comercial atende Ib ≤ In ≤ Iz",
            }
        else:
            assert actual["result"]["liberado_para_uso_normativo"] is False
            assert actual["result"]["status_engenharia"] == "PENDENTE"
            assert actual["result"]["disjuntor"]["corrente_a"] == case["expected"]["result"]["disjuntor"]["corrente_a"]
        return
    if op == "edp":
        response = actual["result"]
        assert response["catalogo"]["status"] == "DOCUMENTADO_SEM_FONTE_PRIMARIA"
        assert response["catalogo"]["normative_conformity_verified"] is False
        assert response["liberado_para_padrao_entrada"] is False
        if case["id"] == "EDP-U-CARGA-TRIFASICA":
            assert "EDP-003" in {x["codigo"] for x in response["alertas"]}
            assert response["candidato_para_estudo"] is False
        else:
            assert response["categoria"] == case["expected"]["result"]["categoria"]
        return
    assert actual == case["expected"]


def test_original_f00_golden_replay_is_not_changed_by_f01_fixes():
    """Original F00 SHA is re-evaluated, fixture must match byte-equivalent data."""
    assert GOLDEN.replay_baseline() == FIXTURE
