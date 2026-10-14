"""Safe CLI interface to SIE task scheduler (no agent execution)."""
import argparse
import json
import os
from collections import Counter
from pathlib import Path
import sys

from .scheduler import (
    ConflitoEstado, WorkflowInvalido, load_state,
    promote_ready, ready_queue, save_state, transition,
)


def create_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m sie_api.scheduler_cli",
        description="Inspeciona, prioriza e registra tarefas do SIE (nao executa agentes).",
    )
    p.add_argument("--state", default=os.environ.get("SIE_ORCHESTRATOR_STATE", ""),
                   help="JSON local do estado operacional.")
    actions = p.add_subparsers(dest="action", required=True)
    actions.add_parser("inspect", help="Ver estados registrados.")
    actions.add_parser("queue", help="Listar atividades READY elegiveis.")
    actions.add_parser("promote", help="Promover PENDING elegiveis para READY.")
    t = actions.add_parser("transition", help="Registrar transicao de estado.")
    t.add_argument("--id", required=True, help="Identificador da story/atividade.")
    t.add_argument("--to", required=True, help="Novo estado operacional.")
    t.add_argument("--reason", required=True, help="Motivo verificavel da mudanca.")
    return p


def main(argv: list[str] | None = None) -> int:
    parser = create_parser()
    args = parser.parse_args(argv)
    if not args.state or args.state == "-":
        parser.error("Informe --state para um arquivo JSON de estado local.")
    try:
        path = Path(args.state)
        document = load_state(path)
        previous_revision = document["revision"]
        if args.action == "inspect":
            counts = Counter(t["state"] for t in document["tasks"])
            result = {
                "revision": previous_revision, "states": dict(sorted(counts.items())),
                "total_tasks": len(document["tasks"]),
            }
        elif args.action == "queue":
            result = {"revision": previous_revision, "ready": ready_queue(document)}
        elif args.action == "promote":
            new_doc = promote_ready(document)
            promoted = [
                t["id"] for t, before in zip(new_doc["tasks"], document["tasks"])
                if before["state"] == "PENDING" and t["state"] == "READY"
            ]
            if promoted:
                revision = save_state(path, new_doc, previous_revision)
            else:
                revision = previous_revision
            result = {"revision": revision, "promoted": promoted}
        else:
            new_doc = transition(document, args.id, args.to, args.reason)
            revision = save_state(path, new_doc, previous_revision)
            result = {"revision": revision, "activity": args.id, "state": args.to}
        print(json.dumps(result, sort_keys=True, ensure_ascii=False))
        return 0
    except (WorkflowInvalido, ConflitoEstado, OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"Falha segura: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
