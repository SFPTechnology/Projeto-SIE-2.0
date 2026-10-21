"""F01 normative evidence: structural integrity is not regulatory approval."""
from copy import deepcopy
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[4]
P = ROOT / "scripts" / "f01_cell_evidence_gate.py"
spec = importlib.util.spec_from_file_location("f01_cell_evidence_gate", P)
guard = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = guard
spec.loader.exec_module(guard)


def baseline():
    return json.loads((ROOT / guard.MATRIX_PATH).read_text(encoding="utf-8"))


def test_current_f01_cells_are_explicitly_blocked_without_fake_approval():
    out = guard.inspect(ROOT, baseline())
    assert out["status"] == "BLOCKED_EVIDENCE"
    assert out["entries_total"] >= 6
    assert set(out["families_covered"]) == set(guard.REQUIRED)
    assert out["integrity_errors"] == []
    assert out["normative_approval_granted_by_tool"] is False
    assert out["f02_release_allowed"] is False


def test_default_status_is_valid_even_when_strict_release_is_blocked(capsys):
    assert guard.main(["--root", str(ROOT)]) == 0
    assert guard.main(["--root", str(ROOT), "--strict"]) == 1
    assert "BLOCKED_EVIDENCE" in capsys.readouterr().out


def test_cannot_claim_reconciled_without_primary_source_and_two_readers():
    doc = baseline()
    doc["entries"][0]["status"] = "EVIDENCE_RECONCILED"
    out = guard.inspect(ROOT, doc)
    assert out["integrity_errors"]
    assert out["status"] == "BLOCKED_EVIDENCE"
    assert out["normative_approval_granted_by_tool"] is False


def test_cannot_drop_problematic_normative_family_to_claim_full_coverage():
    doc = baseline()
    doc["entries"] = [x for x in doc["entries"] if x["group"] != "RCA"]
    out = guard.inspect(ROOT, doc)
    assert any("Familias ausentes" in x for x in out["integrity_errors"])


def test_gate_rejects_normative_verified_or_release_client_flags():
    for key in ("normative_conformity_verified", "release_allowed"):
        doc = baseline()
        doc[key] = True
        out = guard.inspect(ROOT, doc)
        assert any("autodeclarar" in e for e in out["integrity_errors"])


def test_two_review_artifacts_require_distinct_workflow_ids_and_real_hashes(tmp_path):
    doc = baseline()
    item = doc["entries"][0]
    item["status"] = "EVIDENCE_RECONCILED"
    item["source"].update(
        edition="Edição fictícia apenas para ensaio", original_sha256="a" * 64,
        original_confirmed=True, authorised_use=True)
    item["cell"].update(table="synthetic", page="1", row="2", column="3",
                        unit="ohm/km", canonical_value="0.010",
                        notes="hypothetical", installation_conditions="test only")
    item["reviewers"] = {
        "A": {"reviewer_id": "one", "independent_workflow_run": "x"},
        "B": {"reviewer_id": "two", "independent_workflow_run": "x"},
    }
    item["artifacts"] = [{"path": "missing-one", "sha256": "a"*64},
                         {"path": "missing-two", "sha256": "b"*64}]
    item["external_attestation"] = {"professional_review": True,
                                    "artifact": {"path": "missing", "sha256": "a"*64}}
    out = guard.inspect(tmp_path, doc)
    assert any("conferentes distintos" in e for e in out["integrity_errors"])
    assert any("checksums" in e for e in out["integrity_errors"])
    assert any("atestacao" in e for e in out["integrity_errors"])


def test_hash_rejects_external_path_and_corrupted_proof(tmp_path):
    path = tmp_path / "test.md"
    path.write_text("demo only", encoding="utf-8")
    proof = {"path": "test.md", "sha256": sha256(path.read_bytes()).hexdigest()}
    assert guard._hash_file(tmp_path, proof)
    assert not guard._hash_file(tmp_path, {**proof, "sha256": "0"*64})
    assert not guard._hash_file(tmp_path, {**proof, "path": "../test.md"})
