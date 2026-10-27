"""CLI-first geometry: python -m sie_api.nextgen_geometry_cli --input file.json."""
from __future__ import annotations
import argparse
import json
import sys
from decimal import Decimal
from pathlib import Path
from .nextgen_geometry import GeometryError, analyze_project

def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="SIE 2.0: geometria, sem validacao normativa")
    parser.add_argument("--input", required=True, type=Path, help="Projeto em JSON")
    args = parser.parse_args(argv)
    try:
        with args.input.open("r", encoding="utf-8") as stream:
            source = json.load(stream, parse_float=Decimal, parse_int=Decimal)
        report = analyze_project(source)
    except (OSError, UnicodeError, json.JSONDecodeError, GeometryError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
