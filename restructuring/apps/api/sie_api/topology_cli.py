"""python -m sie_api.topology_cli document.json [--database local.sqlite]."""
import argparse
import json
from pathlib import Path
from .topology import Topology, inspect_topology, persist
from .storage import RepositorioProjetos

def main():
    parser = argparse.ArgumentParser(description='Inspecionar topologia declarada, sem homologação')
    parser.add_argument('file', type=Path)
    parser.add_argument('--database')
    parser.add_argument('--expected-revision', type=int, default=0)
    args = parser.parse_args()
    raw = json.loads(args.file.read_text(encoding='utf-8'))
    result = inspect_topology(raw)
    if result['valid'] and args.database:
        doc = Topology.model_validate(raw)
        result['save'] = persist(RepositorioProjetos(args.database), doc.installation.project.id, doc, args.expected_revision)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['valid'] else 1

if __name__ == '__main__':
    raise SystemExit(main())
