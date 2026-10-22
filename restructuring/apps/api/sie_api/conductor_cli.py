"""python -m sie_api.conductor_cli study.json [--database local.sqlite]."""
import argparse
import json
from pathlib import Path
from .conductor_f07 import Study,analyze,save
from .storage import RepositorioProjetos

def main():
    parser=argparse.ArgumentParser(description='F07: memória por trecho; sem homologação normativa')
    parser.add_argument('file',type=Path)
    parser.add_argument('--database')
    parser.add_argument('--expected-revision',type=int,default=0)
    args=parser.parse_args()
    study=Study.model_validate_json(args.file.read_text(encoding='utf-8'))
    result=save(RepositorioProjetos(args.database),study.topology.installation.project.id,study,args.expected_revision) if args.database else analyze(study)
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0
if __name__=='__main__': raise SystemExit(main())
