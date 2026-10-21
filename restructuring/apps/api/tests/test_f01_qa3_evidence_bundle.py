"""Offline structural tests; no real agent execution or normative approval."""
from copy import deepcopy
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[4]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))
spec = importlib.util.spec_from_file_location("f01_qa3_evidence_bundle", SCRIPTS / "f01_qa3_evidence_bundle.py")
bundle = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bundle)
SHA = "b" * 40


def make_mock_artifacts(tmp_path):
    """Fixture filenames mimic artifacts; must never count as real QA evidence."""
    first = tmp_path / "first"
    cross = tmp_path / "cross"
    for role in bundle.ROLES:
        folder = first / role
        folder.mkdir(parents=True)
        (folder / "PARECER_QA.md").write_text(
            f"{role} independent code review for {SHA}. " +
            "Fixture-only; no source verification, no professional attestation. " * 9,
            encoding="utf-8")
        doc = {"schema_version": 1, "phase": "F01", "agent": role,
               "baseline_sha": SHA, "independent_first_pass": True,
               "source_values_approved": False, "f02_release_allowed": False,
               "blockers": ["No primary ABNT source and no two independent readers."],
               "gates": [{"id": f"G{i:02d}", "status": "BLOCKED", "accepted": False,
                          "finding": "Fixture does not substantiate any normative requirement."}
                         for i in range(1, 7)]}
        (folder / "MATRIZ_6_GATES.json").write_text(json.dumps(doc), encoding="utf-8")
    for reviewer, author in bundle.PEERS.items():
        folder = cross / reviewer
        folder.mkdir(parents=True)
        (folder / f"CROSS_REVIEW_{author}.md").write_text(
            f"{reviewer} reviewing {author}, SHA {SHA}. " +
            "TEST ONLY. Neither sources nor technical validity certified. " * 10,
            encoding="utf-8")
    return first, cross


def test_bundle_requires_all_six_outputs_and_records_all_nine_hashes(tmp_path):
    first, cross = make_mock_artifacts(tmp_path)
    result = bundle.inspect(first, cross, SHA, "123456")
    assert result["first_passes_found"] == 3
    assert result["cross_reviews_found"] == 3
    assert len(result["files_sha256"]) == 9
    assert result["normative_cells_verified_by_bundle"] == 0
    assert result["accepted_normative_gates"] == 0
    assert result["independent_professional_signoff"] is False
    assert result["f02_release_allowed"] is False
    path = first / "QA-01" / "PARECER_QA.md"
    assert result["files_sha256"]["firstpass/QA-01/PARECER_QA.md"] == sha256(path.read_bytes()).hexdigest()


@pytest.mark.parametrize("missing", [
    "first/QA-01/PARECER_QA.md", "first/QA-02/MATRIZ_6_GATES.json",
    "cross/QA-03/CROSS_REVIEW_QA-02.md",
])
def test_missing_agent_artifact_never_counts_as_completed(tmp_path, missing):
    first, cross = make_mock_artifacts(tmp_path)
    (tmp_path / missing).unlink()
    with pytest.raises(OSError):
        bundle.inspect(first, cross, SHA, "123456")


def test_one_wrong_sha_blocks_aggregated_independence_claim(tmp_path):
    first, cross = make_mock_artifacts(tmp_path)
    file = first / "QA-01" / "MATRIZ_6_GATES.json"
    data = json.loads(file.read_text(encoding="utf-8"))
    data["baseline_sha"] = "f" * 40
    file.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="baseline_sha"):
        bundle.inspect(first, cross, SHA, "123456")


def test_no_qa_can_claim_approval(tmp_path):
    first, cross = make_mock_artifacts(tmp_path)
    file = first / "QA-02" / "MATRIZ_6_GATES.json"
    data = json.loads(file.read_text(encoding="utf-8"))
    data["gates"][5]["accepted"] = True
    file.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(ValueError, match="normatively approve"):
        bundle.inspect(first, cross, SHA, "123456")


def test_reject_mismatched_or_faked_actions_run_metadata(tmp_path):
    first, cross = make_mock_artifacts(tmp_path)
    with pytest.raises(ValueError, match="GitHub Actions"):
        bundle.inspect(first, cross, SHA, "not-a-real-run-id")
    with pytest.raises(ValueError, match="immutable Git SHA"):
        bundle.inspect(first, cross, SHA[:10], "123456")


def test_detect_token_in_report_and_refuse_unsafe_archive(tmp_path):
    first, cross = make_mock_artifacts(tmp_path)
    file = cross / "QA-01" / "CROSS_REVIEW_QA-03.md"
    file.write_text(file.read_text(encoding="utf-8") +
                    " ghp_ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz12",
                    encoding="utf-8")
    with pytest.raises(ValueError, match="credential"):
        bundle.inspect(first, cross, SHA, "123456")
