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
    assert GOLDEN.evaluate(case) == case["expected"]
