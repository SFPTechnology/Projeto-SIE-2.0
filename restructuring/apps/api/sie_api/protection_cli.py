"""python -m sie_api.protection_cli study.json [--database local.sqlite]."""
import argparse
import json
from pathlib import Path
from .protection_contracts_f08 import Study
from .protection_f08 import analyze
from .protection_storage_f08 import save
from .storage import RepositorioProjetos


def main():
    parser = argparse.ArgumentParser(description='F08: memória de proteções; sem homologação normativa')
    parser.add_argument('file', type=Path, nargs='?')
    parser.add_argument('--catalog', action='store_true', help='Consultar catálogo e fontes do servidor')
    parser.add_argument('--database')
    parser.add_argument('--expected-revision', type=int, default=0)
    args = parser.parse_args()
    if args.catalog:
        from . import protection_registry_f08 as registry
        try:
            print(json.dumps({**registry.catalog(), 'catalog_sha256': registry.catalog_hash()}, ensure_ascii=False, indent=2))
        except ValueError as exc:
            parser.exit(2, f'Catálogo indisponível: {exc}\n')
        return 0
    if args.file is None:
        parser.error('Informe arquivo JSON ou --catalog')
    try:
        study = Study.model_validate_json(args.file.read_text(encoding='utf-8'))
        result = (save(RepositorioProjetos(args.database), study.conductor_study.topology.installation.project.id,
                       study, args.expected_revision) if args.database else analyze(study))
    except (OSError, ValueError) as exc:
        parser.exit(2, f'Não foi possível concluir o estudo: {exc}\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
