"""Proof that Copilot review schema stays blocked until real external verification."""
import importlib.util
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[4]
spec = importlib.util.spec_from_file_location("f01_copilot_reports_gate",
                                             ROOT / "scripts/f01_copilot_reports_gate.py")
gate = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = gate
spec.loader.exec_module(gate)

SHA = "a"*40


def example(role="QA-01"):
    return {
        "schema_version": 1, "phase": "F01", "agent": role,
        "baseline_sha": SHA, "independent_first_pass": True,
        "source_values_approved": False, "f02_release_allowed": False,
        "blockers": ["Não existe documentação original ABNT autorizada e dupla conferência das células."],
        "gates": [{"id": f"G{i:02d}", "status": "BLOCKED", "accepted": False,
                   "finding": f"Não há evidência profissional para homologação gate {i}."}
                  for i in range(1, 7)],
    }


def prepare(tmp_path, role="QA-01", data=None):
    folder = tmp_path / role
    folder.mkdir()
    (folder / "PARECER_QA.md").write_text(
        f"{role} — parecer independente, código {SHA}. " +
        "Fonte primária e conferência de células não aprovadas. " * 12, encoding="utf-8"
    )
    (folder / "MATRIZ_6_GATES.json").write_text(
        json.dumps(example(role) if data is None else data), encoding="utf-8"
    )
    return folder


def test_accept_substantive_separate_qa_report_but_not_signoff(tmp_path):
    prepare(tmp_path)
    r = gate.first_pass(tmp_path, "QA-01", SHA)
    assert r["professional_signoff"] is False
    assert r["normative_cells_approved"] == 0
    assert r["gates"] == 6


@pytest.mark.parametrize("attr,bad", [
    ("independent_first_pass", False),
    ("f02_release_allowed", True),
    ("source_values_approved", True),
    ("agent", "QA-02"),
    ("baseline_sha", "b"*40),
    ("phase", "F02"),
])
def test_reject_false_or_mismatched_qa_attributes(tmp_path, attr, bad):
    doc = example()
    doc[attr] = bad
    prepare(tmp_path, data=doc)
    with pytest.raises(ValueError, match="Invalid/unsafe"):
        gate.first_pass(tmp_path, "QA-01", SHA)


def test_cannot_homologate_any_gate_by_model_output(tmp_path):
    doc = example()
    doc["gates"][0]["accepted"] = True
    prepare(tmp_path, data=doc)
    with pytest.raises(ValueError, match="normatively approve"):
        gate.first_pass(tmp_path, "QA-01", SHA)


def test_cannot_omit_g02_cell_check(tmp_path):
    doc = example()
    doc["gates"] = [x for x in doc["gates"] if x["id"] != "G02"]
    prepare(tmp_path, data=doc)
    with pytest.raises(ValueError, match="Exactly six"):
        gate.first_pass(tmp_path, "QA-01", SHA)


def test_reject_secrets_in_report(tmp_path):
    folder = prepare(tmp_path)
    (folder / "PARECER_QA.md").write_text(
        "QA-01" + " " * 300 + "github_pat_ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789",
        encoding="utf-8")
    with pytest.raises(ValueError, match="credential"):
        gate.first_pass(tmp_path, "QA-01", SHA)


def test_cross_review_requires_frozen_peer_and_sha(tmp_path):
    folder = tmp_path / "QA-02"
    folder.mkdir()
    (folder / "CROSS_REVIEW_QA-01.md").write_text(
        "Revisão cruzada QA-02 de QA-01 com SHA " + SHA +
        ". Falta confirmação de fonte primária e revisão profissional." * 10,
        encoding="utf-8")
    assert gate.cross_review(tmp_path, "QA-02", SHA)["author"] == "QA-01"
    (folder / "CROSS_REVIEW_QA-01.md").write_text(
        "QA-02 e QA-01 sem baseline " + "texto" * 90, encoding="utf-8")
    with pytest.raises(ValueError, match="Incomplete"):
        gate.cross_review(tmp_path, "QA-02", SHA)
