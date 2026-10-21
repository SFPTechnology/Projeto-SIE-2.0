"""Validate, summarize and optionally persist F04 via the existing local store."""
import argparse
import json
from pathlib import Path
from .load_survey import Survey, summarize, persist
from .storage import RepositorioProjetos

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('arquivo', type=Path)
    parser.add_argument('--database')
    parser.add_argument('--revisao-esperada', type=int, default=0)
    args = parser.parse_args()
    survey = Survey.model_validate_json(args.arquivo.read_text(encoding='utf-8'))
    result = summarize(survey) if not args.database else persist(RepositorioProjetos(args.database), survey.projeto_id, survey, args.revisao_esperada)
    print(json.dumps(result, ensure_ascii=False, indent=2))
if __name__ == '__main__':
    main()
