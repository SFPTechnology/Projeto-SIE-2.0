"""CLI-first operations for local SIE test projects.

Examples:
 python -m sie_api.cli --database sie-local.sqlite3 salvar --nome "Casa" --arquivo dados.json
 python -m sie_api.cli --database sie-local.sqlite3 carregar --id <UUID>
 python -m sie_api.cli --database sie-local.sqlite3 historico --id <UUID>

Local-only; this tool neither approves electrical calculations nor contacts a server.
"""
import argparse
import json
import os
import sys
from pathlib import Path
from uuid import UUID, uuid4

from .storage import ConflitoRevisao, RepositorioProjetos

MAX_INPUT_BYTES = 1_048_576


def _strict_constant(value: str):
    raise ValueError(f"Valor JSON nao permitido: {value}")


def _read_json_object(path: str) -> dict:
    file = Path(path)
    if file.stat().st_size > MAX_INPUT_BYTES:
        raise ValueError("Arquivo JSON excede tamanho permitido (1 MiB)")
    content = json.loads(file.read_text(encoding="utf-8-sig"), parse_constant=_strict_constant)
    if not isinstance(content, dict):
        raise ValueError("O arquivo deve conter objeto JSON")
    return content


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m sie_api.cli",
        description="SIE 2.0: projetos locais versionados, sem aprovação normativa.",
    )
    parser.add_argument(
        "--database",
        default=os.environ.get("SIE_LOCAL_DB_PATH", ""),
        help="Caminho do SQLite local (ou SIE_LOCAL_DB_PATH).",
    )
    actions = parser.add_subparsers(dest="action", required=True)
    analyze = actions.add_parser("analisar", help="Ensaio de circuito com células e proteção parcial.")
    analyze.add_argument("--arquivo", required=True, help="JSON de análise de circuito.")
    save = actions.add_parser("salvar", help="Criar ou atualizar projeto com revisao esperada.")
    save.add_argument("--id", help="UUID existente; omitido gera UUID novo.")
    save.add_argument("--nome", required=True, help="Nome do projeto.")
    save.add_argument("--arquivo", required=True, help="Arquivo JSON com objeto de dados.")
    save.add_argument("--revisao-esperada", type=int, default=0)
    load = actions.add_parser("carregar", help="Consultar projeto salvo.")
    load.add_argument("--id", required=True)
    history = actions.add_parser("historico", help="Consultar trilha de revisoes.")
    history.add_argument("--id", required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    if args.action != "analisar" and (not args.database or args.database == ":memory:"):
        parser.error("Informe --database com caminho SQLite local persistente.")
    try:
        if args.action == "analisar":
            from .analysis_contracts import AnaliseCircuito
            from .application import analisar_circuito
            payload = AnaliseCircuito.model_validate(_read_json_object(args.arquivo))
            print(json.dumps(analisar_circuito(payload.model_dump(mode="json")),
                             ensure_ascii=False, allow_nan=False, sort_keys=True))
            return 0
        repo = RepositorioProjetos(args.database)
        if args.action == "salvar":
            project_id = str(UUID(args.id)) if args.id else str(uuid4())
            data = _read_json_object(args.arquivo)
            revision = repo.salvar(project_id, args.nome, data, args.revisao_esperada)
            output = {"id": project_id, "revisao": revision, "estado": "armazenado_localmente"}
        elif args.action == "carregar":
            output = repo.carregar(args.id)
            if output is None:
                print("Projeto nao encontrado.", file=sys.stderr)
                return 3
        else:
            output = {"id": args.id, "eventos": repo.historico(args.id)}
        print(json.dumps(output, ensure_ascii=False, allow_nan=False, sort_keys=True))
        return 0
    except ConflitoRevisao as exc:
        print(f"Conflito de revisao: {exc}", file=sys.stderr)
        return 4
    except (ValueError, OSError, UnicodeError, json.JSONDecodeError) as exc:
        print(f"Dados invalidos ou indisponiveis: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
