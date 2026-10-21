"""python -m sie_api.demand_cli scenario.json — deterministic study memory."""
import argparse
import json
from pathlib import Path
from uuid import UUID
from .demand import Scenario, calculate, compare, project_survey, save_scenario
from .load_survey import Survey
from .storage import RepositorioProjetos

def main():
    parser = argparse.ArgumentParser(description='Memória F06 de estudo; não homologa norma')
    parser.add_argument('file', type=Path,nargs='?')
    parser.add_argument('--catalog',action='store_true')
    actions = parser.add_mutually_exclusive_group()
    actions.add_argument('--compare', type=Path)
    actions.add_argument('--survey', type=Path)
    actions.add_argument('--database')
    parser.add_argument('--links', type=Path)
    parser.add_argument('--expected-revision', type=int, default=0)
    args = parser.parse_args()
    if args.catalog:
        from .demand_registry import catalog,CATALOG_HASH
        print(json.dumps({**catalog(),'catalog_sha256':CATALOG_HASH},ensure_ascii=False,indent=2))
        return 0
    if args.file is None: parser.error('Informe cenário JSON ou --catalog')
    scenario = Scenario.model_validate_json(args.file.read_text(encoding='utf-8'))
    if args.survey:
        if args.links is None: parser.error('--survey exige --links (mapa UUID F04 para UUID F02)')
        survey = Survey.model_validate_json(args.survey.read_text(encoding='utf-8'))
        links = {UUID(k):UUID(v) for k,v in json.loads(args.links.read_text(encoding='utf-8')).items()}
        result = project_survey(survey, scenario.topology, links)
    elif args.compare:
        result = compare(scenario, Scenario.model_validate_json(args.compare.read_text(encoding='utf-8')))
    elif args.database:
        result = save_scenario(RepositorioProjetos(args.database), scenario.topology.installation.project.id, scenario, args.expected_revision)
    else:
        result = calculate(scenario)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result.get('status') == 'PENDING' else 0

if __name__ == '__main__':
    raise SystemExit(main())
