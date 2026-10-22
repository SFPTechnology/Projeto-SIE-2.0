"""python -m sie_api.conductor_cli study.json [--database local.sqlite]."""
import argparse
import json
from pathlib import Path
from .conductor_f07 import Study,analyze,save
from .storage import RepositorioProjetos
from .conductor_selection_f07 import Selection,select,save_selection
from . import conductor_registry_f07 as registry

def main():
    parser=argparse.ArgumentParser(description='F07: memória por trecho; sem homologação normativa')
    parser.add_argument('file',type=Path,nargs='?')
    parser.add_argument('--select',action='store_true',help='Selecionar no catálogo finito fonte-vinculado')
    parser.add_argument('--catalog',action='store_true',help='Consultar catálogo e referências do servidor')
    parser.add_argument('--database')
    parser.add_argument('--expected-revision',type=int,default=0)
    args=parser.parse_args()
    if args.catalog:
        print(json.dumps({**registry.catalog(),'catalog_sha256':registry.catalog_hash()},ensure_ascii=False,indent=2))
        return 0
    if args.file is None: parser.error('Informe arquivo JSON ou --catalog')
    model=Selection if args.select else Study
    study=model.model_validate_json(args.file.read_text(encoding='utf-8'))
    calculate=select if args.select else analyze
    persist=save_selection if args.select else save
    result=persist(RepositorioProjetos(args.database),study.topology.installation.project.id,study,args.expected_revision) if args.database else calculate(study)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0
if __name__=='__main__': raise SystemExit(main())
