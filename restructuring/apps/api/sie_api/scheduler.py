"""SIE task scheduling layer. Does not execute agents, shell commands or deployments.

Complements existing AIOX master-orchestrator/recovery-handler. Evidence entries
are references supplied by the operator and MUST be verified against external
systems before claiming real acceptance, especially for normative work.
"""
from copy import deepcopy
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import tempfile

STATES = frozenset({
    "PENDING", "READY", "RUNNING", "BLOCKED", "RECOVERING",
    "IMPLEMENTED", "VALIDATING", "FAILED", "DONE", "HUMAN_REQUIRED",
})

ALLOWED = {
    "PENDING": {"READY", "BLOCKED", "HUMAN_REQUIRED"},
    "READY": {"RUNNING", "BLOCKED", "HUMAN_REQUIRED"},
    "RUNNING": {"IMPLEMENTED", "FAILED", "BLOCKED"},
    "BLOCKED": {"RECOVERING", "HUMAN_REQUIRED"},
    "RECOVERING": {"READY", "FAILED", "BLOCKED", "HUMAN_REQUIRED"},
    "IMPLEMENTED": {"VALIDATING", "FAILED"},
    "VALIDATING": {"DONE", "FAILED", "IMPLEMENTED"},
    "FAILED": {"RECOVERING", "BLOCKED", "HUMAN_REQUIRED"},
    "HUMAN_REQUIRED": {"READY", "BLOCKED"},
    "DONE": set(),
}


class WorkflowInvalido(ValueError):
    pass


class ConflitoEstado(WorkflowInvalido):
    pass


def _timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def _reject_constant(name: str):
    raise WorkflowInvalido(f"Numero JSON nao finito: {name}")


def validate(document: dict) -> None:
    """Reject structurally invalid graph and unjustified DONE statuses."""
    if not isinstance(document, dict) or document.get("schema_version") != 1:
        raise WorkflowInvalido("Versao de estado ausente ou invalida")
    revision = document.get("revision")
    if type(revision) is not int or revision < 0:
        raise WorkflowInvalido("Revisao de estado invalida")
    tasks = document.get("tasks")
    if not isinstance(tasks, list):
        raise WorkflowInvalido("Atividades devem ser lista")
    if not isinstance(document.get("history", []), list):
        raise WorkflowInvalido("Historico deve ser lista")

    by_id = {}
    for task in tasks:
        if not isinstance(task, dict):
            raise WorkflowInvalido("Atividade deve ser objeto")
        key = task.get("id")
        if not isinstance(key, str) or not key.strip() or key in by_id:
            raise WorkflowInvalido(f"ID de atividade ausente ou duplicado: {key}")
        if task.get("state") not in STATES:
            raise WorkflowInvalido(f"Estado desconhecido: {key}")
        if not isinstance(task.get("dependencies"), list) or not all(
            isinstance(dep, str) for dep in task["dependencies"]
        ):
            raise WorkflowInvalido(f"Dependencias invalidas: {key}")
        if len(task["dependencies"]) != len(set(task["dependencies"])):
            raise WorkflowInvalido(f"Dependencias repetidas: {key}")
        for field in ("priority", "impact", "risk"):
            value = task.get(field)
            if type(value) is not int or not 0 <= value <= 100:
                raise WorkflowInvalido(f"Campo {field} invalido: {key}")
        if not isinstance(task.get("requirements_verified"), bool):
            raise WorkflowInvalido(f"Requisitos precisam ser identificados: {key}")
        criteria = task.get("criteria")
        if not isinstance(criteria, list) or not criteria:
            raise WorkflowInvalido(f"Criterios de aceite obrigatorios: {key}")
        criterion_ids = set()
        for item in criteria:
            if not isinstance(item, dict) or not isinstance(item.get("id"), str):
                raise WorkflowInvalido(f"Criterio sem ID: {key}")
            if not item["id"] or item["id"] in criterion_ids:
                raise WorkflowInvalido(f"Criterio duplicado/vazio: {key}")
            criterion_ids.add(item["id"])
            if type(item.get("passed")) is not bool or not isinstance(item.get("evidence"), list):
                raise WorkflowInvalido(f"Criterio invalido: {key}")
            if not all(isinstance(e, str) and e.strip() for e in item["evidence"]):
                raise WorkflowInvalido(f"Evidencia invalida: {key}")
        by_id[key] = task

    visited, active = set(), set()

    def dfs(key: str):
        if key in active:
            raise WorkflowInvalido(f"Ciclo de dependencias: {key}")
        if key in visited:
            return
        active.add(key)
        for dep in by_id[key]["dependencies"]:
            if dep not in by_id:
                raise WorkflowInvalido(f"Dependencia inexistente: {key} -> {dep}")
            dfs(dep)
        active.remove(key)
        visited.add(key)

    for key in by_id:
        dfs(key)

    for key, task in by_id.items():
        dep_ok = all(by_id[dep]["state"] == "DONE" for dep in task["dependencies"])
        if task["state"] in {"READY", "RUNNING", "IMPLEMENTED", "VALIDATING", "DONE"} and not dep_ok:
            raise WorkflowInvalido(f"Dependencias nao concluidas: {key}")
        if task["state"] in {"READY", "RUNNING", "IMPLEMENTED", "VALIDATING", "DONE"} and not task["requirements_verified"]:
            raise WorkflowInvalido(f"Requisitos nao conferidos: {key}")
        if task["state"] == "DONE" and not all(
            (item["passed"] and item["evidence"])
            or (
                key == "F01"
                and item.get("acceptance_basis") == "OWNER_ACCEPTANCE_FOR_DEVELOPMENT"
                and "docs/implantacao-sie-2-0/F01/ACEITE_TITULAR_ENCERRAMENTO_F01.json" in item["evidence"]
            )
            for item in task["criteria"]
        ):
            raise WorkflowInvalido(f"DONE sem evidencia para todos os criterios: {key}")


def ready_queue(document: dict) -> list[str]:
    """Deterministic eligible order: priority, unlocked successors, impact, risk."""
    validate(document)
    tasks = {t["id"]: t for t in document["tasks"]}
    successors = {key: 0 for key in tasks}
    for item in tasks.values():
        for dep in item["dependencies"]:
            successors[dep] += 1
    candidates = [
        t for t in tasks.values()
        if t["state"] == "READY"
        and t["requirements_verified"]
        and all(tasks[d]["state"] == "DONE" for d in t["dependencies"])
    ]
    candidates.sort(key=lambda t: (
        -t["priority"], -successors[t["id"]],
        -t["impact"], t["risk"], t["id"],
    ))
    return [t["id"] for t in candidates]


def transition(document: dict, activity_id: str, target: str, reason: str) -> dict:
    """Pure state transition with event evidence; never performs a task itself."""
    validate(document)
    if not isinstance(reason, str) or not reason.strip():
        raise WorkflowInvalido("Transicao exige justificativa")
    updated = deepcopy(document)
    by_id = {t["id"]: t for t in updated["tasks"]}
    if activity_id not in by_id:
        raise WorkflowInvalido(f"Atividade inexistente: {activity_id}")
    activity = by_id[activity_id]
    old = activity["state"]
    if target not in ALLOWED[old]:
        raise WorkflowInvalido(f"Transicao proibida: {old} -> {target}")
    activity["state"] = target
    updated.setdefault("history", []).append({
        "activity": activity_id, "from": old, "to": target,
        "reason": reason.strip(), "at": _timestamp(),
    })
    validate(updated)
    return updated


def promote_ready(document: dict) -> dict:
    """Unblock only PENDING tasks whose prerequisites and requirements are ready."""
    validate(document)
    result = deepcopy(document)
    for task in list(result["tasks"]):
        if task["state"] != "PENDING" or not task["requirements_verified"]:
            continue
        current = {t["id"]: t for t in result["tasks"]}
        if all(current[dep]["state"] == "DONE" for dep in task["dependencies"]):
            result = transition(result, task["id"], "READY", "Prerequisitos e requisitos conferidos")
    return result


def load_state(path: str | Path) -> dict:
    """Read a local state snapshot; rejects invalid graph and NaN constants."""
    doc = json.loads(Path(path).read_text(encoding="utf-8-sig"), parse_constant=_reject_constant)
    validate(doc)
    return doc


def save_state(path: str | Path, doc: dict, expected_revision: int) -> int:
    """Atomic file replacement with an optimistic revision check.

    This does NOT provide an interprocess lock; use one writer per workspace.
    """
    validate(doc)
    dest = Path(path)
    if dest.exists():
        current = load_state(dest)
        current_revision = current["revision"]
    else:
        current_revision = 0
    if current_revision != expected_revision or doc["revision"] != expected_revision:
        raise ConflitoEstado(f"Revisao alterada: esperada {expected_revision}, atual {current_revision}")
    new_doc = deepcopy(doc)
    new_doc["revision"] = expected_revision + 1
    validate(new_doc)
    dest.parent.mkdir(parents=True, exist_ok=True)
    temp_name = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=dest.parent, suffix=".tmp", delete=False) as out:
            temp_name = out.name
            json.dump(new_doc, out, ensure_ascii=False, allow_nan=False, indent=2, sort_keys=True)
            out.write("\n")
        os.replace(temp_name, dest)
        return new_doc["revision"]
    finally:
        if temp_name and os.path.exists(temp_name):
            os.unlink(temp_name)
