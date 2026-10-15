"""Tests for SIE-specific DAG scheduling. No agent or network execution."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys

import pytest

from sie_api.scheduler import (
    ConflitoEstado, WorkflowInvalido, STATES, load_state, promote_ready,
    ready_queue, save_state, transition, validate,
)


def item(id="A", state="PENDING", deps=(), requirements=True, passed=False,
         evidence=None, priority=50, impact=5, risk=3):
    return {
        "id": id, "title": id, "state": state, "dependencies": list(deps),
        "priority": priority, "impact": impact, "risk": risk,
        "requirements_verified": requirements,
        "criteria": [{"id": "AC1", "passed": passed, "evidence": list(evidence or [])}],
    }


def snapshot(*tasks):
    return {"schema_version": 1, "revision": 0, "tasks": list(tasks), "history": []}


def test_all_protocol_states_present():
    assert STATES == {
        "PENDING", "READY", "RUNNING", "BLOCKED", "RECOVERING",
        "IMPLEMENTED", "VALIDATING", "FAILED", "DONE", "HUMAN_REQUIRED",
    }


def test_graph_rejects_missing_dependency():
    with pytest.raises(WorkflowInvalido, match="inexistente"):
        validate(snapshot(item("A", deps=("UNKNOWN",))))


def test_graph_rejects_duplicate_id():
    with pytest.raises(WorkflowInvalido, match="duplicado"):
        validate(snapshot(item("A"), item("A")))


def test_graph_rejects_dependency_cycle():
    with pytest.raises(WorkflowInvalido, match="Ciclo"):
        validate(snapshot(item("A", deps=("B",)), item("B", deps=("A",))))


def test_pending_unblocks_only_after_verified_dependencies():
    doc = snapshot(
        item("A", state="DONE", passed=True, evidence=["CI-run"]),
        item("B", deps=("A",)),
        item("C", deps=("BLOCK",)),
        item("BLOCK", state="BLOCKED", requirements=False),
    )
    promoted = promote_ready(doc)
    assert {t["id"]: t["state"] for t in promoted["tasks"]} == {
        "A": "DONE", "B": "READY", "C": "PENDING", "BLOCK": "BLOCKED",
    }
    assert [x["to"] for x in promoted["history"]] == ["READY"]
    assert doc["tasks"][1]["state"] == "PENDING"


def test_queue_orders_priority_unlock_count_and_risk():
    doc = snapshot(
        item("A", state="DONE", passed=True, evidence=["CI-run"]),
        item("B", state="READY", deps=("A",), priority=80, risk=5),
        item("C", state="READY", deps=("A",), priority=80, risk=1),
        item("D", deps=("B",)),
        item("E", state="READY", deps=("A",), priority=90),
    )
    assert ready_queue(doc) == ["E", "B", "C"]


def test_transition_requires_justification_and_follows_matrix():
    doc = snapshot(item("A", state="READY"))
    with pytest.raises(WorkflowInvalido, match="justificativa"):
        transition(doc, "A", "RUNNING", "")
    with pytest.raises(WorkflowInvalido, match="proibida"):
        transition(doc, "A", "DONE", "Tentativa sem teste")
    result = transition(doc, "A", "RUNNING", "Iniciada story verificada")
    assert result["tasks"][0]["state"] == "RUNNING"
    assert result["history"][0]["from"] == "READY"
    assert doc["tasks"][0]["state"] == "READY"


def test_done_requires_individual_pass_and_evidence():
    doc = snapshot(item("A", state="VALIDATING"))
    with pytest.raises(WorkflowInvalido, match="DONE sem evidencia"):
        transition(doc, "A", "DONE", "Nao houve validacao")
    doc["tasks"][0]["criteria"][0] = {
        "id": "AC1", "passed": True, "evidence": ["workflow-run-123"],
    }
    finished = transition(doc, "A", "DONE", "Resultados e referencias conferidos")
    assert finished["tasks"][0]["state"] == "DONE"
    assert ready_queue(finished) == []


def test_done_from_json_without_evidence_is_invalid():
    with pytest.raises(WorkflowInvalido, match="DONE sem evidencia"):
        validate(snapshot(item("A", state="DONE", passed=True)))


def test_human_required_does_not_block_independent_activity():
    doc = snapshot(
        item("A", state="HUMAN_REQUIRED", requirements=False),
        item("B", state="READY"),
        item("C", deps=("A",)),
    )
    assert ready_queue(doc) == ["B"]


def test_recovery_does_not_auto_approve():
    doc = snapshot(item("A", state="FAILED"))
    recovered = transition(doc, "A", "RECOVERING", "Investigacao com nova hipotese")
    assert recovered["tasks"][0]["state"] == "RECOVERING"
    assert recovered["tasks"][0]["criteria"][0]["passed"] is False


def test_persistent_revision_and_reopen(tmp_path):
    path = tmp_path / "operational.json"
    original = snapshot(item("A"))
    revision = save_state(path, original, 0)
    assert revision == 1
    loaded = load_state(path)
    assert loaded["revision"] == 1
    assert loaded["tasks"][0]["id"] == "A"
    with pytest.raises(ConflitoEstado):
        save_state(path, original, 0)
    updated = promote_ready(loaded)
    assert save_state(path, updated, 1) == 2
    assert load_state(path)["tasks"][0]["state"] == "READY"


def test_nonfinite_snapshot_is_rejected(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text('{"schema_version":1,"revision":NaN,"tasks":[]}', encoding="utf-8")
    with pytest.raises(WorkflowInvalido):
        load_state(path)


def test_scheduler_cli_inspect_queue_and_promote(tmp_path):
    path = tmp_path / "state.json"
    save_state(path, snapshot(item("A")), 0)
    base = [sys.executable, "-m", "sie_api.scheduler_cli", "--state", str(path)]
    result = subprocess.run(base + ["inspect"], capture_output=True, text=True, timeout=15)
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["states"] == {"PENDING": 1}
    promoted = subprocess.run(base + ["promote"], capture_output=True, text=True, timeout=15)
    assert promoted.returncode == 0, promoted.stderr
    assert json.loads(promoted.stdout)["promoted"] == ["A"]
    ready = subprocess.run(base + ["queue"], capture_output=True, text=True, timeout=15)
    assert json.loads(ready.stdout)["ready"] == ["A"]


def test_scheduler_cli_rejects_unjustified_done(tmp_path):
    path = tmp_path / "state.json"
    save_state(path, snapshot(item("A", state="READY")), 0)
    args = [
        sys.executable, "-m", "sie_api.scheduler_cli", "--state", str(path),
        "transition", "--id", "A", "--to", "DONE", "--reason", "Nao validado",
    ]
    result = subprocess.run(args, capture_output=True, text=True, timeout=15)
    assert result.returncode == 2
    assert load_state(path)["tasks"][0]["state"] == "READY"


def test_repository_backlog_is_structurally_valid():
    root = Path(__file__).resolve().parents[4]
    path = root / "docs" / "sie-orchestrator" / "ORCHESTRATOR_STATE.json"
    state = load_state(path)
    assert state["schema_version"] == 1
    assert "SIE-AUTO-011" in {t["id"] for t in state["tasks"]}
