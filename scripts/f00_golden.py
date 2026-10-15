#!/usr/bin/env python3
"""F00 characterization, captured ONLY from an immutable Git revision.

These snapshots preserve behavior, including labeled defects. They are not
independent engineering reference values and never grant normative approval.
Capture refuses to overwrite an existing fixture; --verify replays the original
revision without modifying that fixture or contacting any external service.
"""
import argparse
from dataclasses import asdict, is_dataclass
from decimal import Decimal
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

BASELINE_SHA = "8d86db26f5e8675eaced4638af14bd84019e15e7"
ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "restructuring/apps/api/tests/fixtures/f00_legacy_golden.json"
API_PREFIX = "restructuring/apps/api"


def specs():
    cases = []

    def add(key, op, data, legacy, anomaly=None):
        cases.append(dict(id=key, operation=op, input=data,
                          legacy_ids=legacy, known_anomaly=anomaly))

    add("QT-MONO", "mono", ["20", "30", "7.41", "220"], ["LEGACY-005"])
    add("QT-MONO-ZERO", "mono", ["20", "0", "7.41", "220"], ["LEGACY-005"])
    add("QT-MONO-ROUND", "mono", ["1", "1", "2.5", "100"], ["LEGACY-005"])
    add("QT-MONO-INVALID", "mono", ["20", "-1", "7.41", "220"], ["LEGACY-005"])
    add("QT-TRI", "tri", ["20", "30", "7.41", "380"], ["LEGACY-006"])
    add("QT-TRI-ZERO", "tri", ["20", "0", "7.41", "380"], ["LEGACY-006"])
    add("CONDUTOR", "conductor", {"ib": "20", "factor": "0.8", "table": [["2.5", "24"], ["4", "32"]]}, ["LEGACY-003"])
    add("CONDUTOR-LIMIAR", "conductor", {"ib": "19.2", "factor": "0.8", "table": [["2.5", "24"], ["4", "32"]]}, ["LEGACY-003"])
    add("CONDUTOR-DUPLICADO", "conductor", {"ib": "10", "factor": "1", "table": [["4", "32"], ["4", "40"]]}, ["LEGACY-003"])
    add("DISJUNTOR", "breaker", {"ib": "20", "iz": "25", "catalog": ["32", "25", "16", "20", "20"]}, ["LEGACY-004"])
    add("DISJUNTOR-SEM-CANDIDATO", "breaker", {"ib": "21", "iz": "24", "catalog": ["20", "25"]}, ["LEGACY-004"])
    add("GATE-SEM-FONTE", "gate", None, ["LEGACY-007"])
    add("GATE-CLIENTE", "gate", {"documento": "Fixture sintética", "edicao": "teste", "referencia": "caso F00", "dados_validados": True, "testes_independentes": True}, ["LEGACY-007"])
    add("GATE-VAZIO", "gate", {"documento": " ", "edicao": "teste", "referencia": "caso F00"}, ["LEGACY-007"])
    data = dict(corrente_a=20, comprimento_m=30, tensao_v=220,
                resistencia_ohm_km=7.41, fator_correcao=0.8,
                tabela_condutores=[dict(secao_mm2=2.5, capacidade_a=24), dict(secao_mm2=4, capacidade_a=32)],
                evidencia=dict(documento="Fixture sintética F00", edicao="teste não normativo", referencia="dados ilustrativos"))
    add("ANALISE", "analysis", data, ["LEGACY-003", "LEGACY-004", "LEGACY-005", "LEGACY-007", "LEGACY-008"])
    edge = dict(data, corrente_a=19.99, fator_correcao=0.99975,
                tabela_condutores=[dict(secao_mm2=2.5, capacidade_a=20)])
    add("ANALISE-IZ-ARREDONDADO", "analysis", edge, ["LEGACY-003", "LEGACY-004", "LEGACY-008"], "ENG-001: In=20 exceeds unrounded Iz=19.995; preserve observation, NOT design approval")
    for mode, currents in {"U": ["70"], "D": ["63", "100", "150", "200", "300", "350"], "T": ["63", "100", "150", "200", "300", "350"]}.items():
        for current in currents:
            add(f"EDP-{mode}-{current}", "edp", [mode, current, "20", mode == "T"], ["LEGACY-009"])
    add("EDP-T-SEM-TRIFASICA", "edp", ["T", "58.3", "22.215", False], ["LEGACY-009"])
    add("EDP-75KW", "edp", ["D", "80", "75.01", False], ["LEGACY-009"])
    add("EDP-SEM-CATEGORIA", "edp", ["T", "351", "30", True], ["LEGACY-009"])
    add("EDP-U-CARGA-TRIFASICA", "edp", ["U", "20", "4.4", True], ["LEGACY-009"], "ENG-002: U/T load incompatibility is not rejected; candidate is NOT approval")
    add("STORAGE-REVISOES", "storage", {"id": "00000000-0000-4000-8000-000000000001", "nome": "Golden F00", "dados": {"circuitos": [{"nome": "TUG-1"}]}}, ["LEGACY-010", "LEGACY-011", "LEGACY-012"])
    return cases


def normalize(value):
    if isinstance(value, Decimal):
        return str(value)
    if is_dataclass(value):
        return normalize(asdict(value))
    if isinstance(value, dict):
        return {key: normalize(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [normalize(item) for item in value]
    return value


def evaluate(case):
    from sie_api.domain import engines
    from sie_api.application import analisar_circuito
    from sie_api.domain.edp import enquadrar_edp
    from sie_api.domain.gates import EvidenciaNormativa, status_liberacao
    from sie_api.storage import RepositorioProjetos, ConflitoRevisao

    op, data = case["operation"], case["input"]
    try:
        if op in {"mono", "tri"}:
            fun = engines.calcular_queda_tensao_monofasica if op == "mono" else engines.calcular_queda_tensao_trifasica_resistiva
            result = fun(*(Decimal(x) for x in data))
        elif op == "conductor":
            result = engines.selecionar_condutor(Decimal(data["ib"]), Decimal(data["factor"]), tuple(tuple(Decimal(x) for x in row) for row in data["table"]))
        elif op == "breaker":
            result = engines.selecionar_disjuntor(Decimal(data["ib"]), Decimal(data["iz"]), tuple(Decimal(x) for x in data["catalog"]))
        elif op == "gate":
            result = status_liberacao(None if data is None else EvidenciaNormativa(**data)).value
        elif op == "analysis":
            result = analisar_circuito(data)
        elif op == "edp":
            result = enquadrar_edp(data[0], Decimal(data[1]), Decimal(data[2]), data[3])
        elif op == "storage":
            with tempfile.TemporaryDirectory(prefix="f00-golden-") as folder:
                db = Path(folder) / "golden.sqlite3"
                repo = RepositorioProjetos(db)
                first = repo.salvar(data["id"], data["nome"], data["dados"], 0)
                conflict = None
                try:
                    repo.salvar(data["id"], "stale", {}, 0)
                except ConflitoRevisao as exc:
                    conflict = str(exc)
                second = repo.salvar(data["id"], data["nome"], {"circuitos": []}, 1)
                repo = RepositorioProjetos(db)
                loaded = repo.carregar(data["id"])
                del loaded["atualizado_em"]  # nondeterministic clock, not hidden business data
                result = dict(revisions=[first, second], loaded=loaded, conflict=conflict,
                              history=[{k: row[k] for k in ("acao", "revisao")} for row in repo.historico(data["id"])],
                              omitted_fields=["atualizado_em", "criado_em"])
        else:
            raise AssertionError(f"Unknown characterization operation: {op}")
        return dict(result=normalize(result))
    except ValueError as exc:
        return dict(error_type=type(exc).__name__, error_message=str(exc))


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def replay_baseline():
    paths = git("ls-tree", "-r", "--name-only", BASELINE_SHA, f"{API_PREFIX}/sie_api").decode().splitlines()
    hashes = {}
    with tempfile.TemporaryDirectory(prefix="f00-original-") as folder:
        base = Path(folder)
        for path in paths:
            content = git("show", f"{BASELINE_SHA}:{path}")
            hashes[path] = hashlib.sha256(content).hexdigest()
            target = base / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        run = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--evaluate", str(base / API_PREFIX)],
                             cwd=base, env=os.environ.copy(), capture_output=True, text=True, timeout=45, check=True)
        cases = json.loads(run.stdout)
    return dict(baseline_sha=BASELINE_SHA, output_class="characterization_only_not_normative_validation",
                source_sha256=hashes, cases=cases)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--capture", type=Path, help="new destination; never overwrites")
    group.add_argument("--verify", action="store_true", help="replay original Git revision and compare immutable fixture")
    group.add_argument("--evaluate", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.evaluate:
        sys.path.insert(0, str(args.evaluate))
        import sie_api
        if not Path(sie_api.__file__).resolve().is_relative_to(args.evaluate.resolve()):
            raise RuntimeError("Refusing source outside extracted baseline")
        print(json.dumps([dict(case, expected=evaluate(case)) for case in specs()], ensure_ascii=False, sort_keys=True))
        return
    if args.capture and args.capture.exists():
        parser.error("Refusing to overwrite frozen expectations")
    document = replay_baseline()
    if args.verify:
        expected = json.loads(FIXTURE.read_text(encoding="utf-8"))
        if document != expected:
            raise SystemExit("Baseline replay differs from frozen fixture; investigate, do not rewrite expectations")
        print(f"PASS: {len(document['cases'])} cases replayed from {BASELINE_SHA}; fixture unchanged")
    else:
        args.capture.parent.mkdir(parents=True, exist_ok=True)
        with args.capture.open("x", encoding="utf-8") as file:
            json.dump(document, file, ensure_ascii=False, indent=2, sort_keys=True)
            file.write("\n")
        print(f"Captured {len(document['cases'])} cases from {BASELINE_SHA}")


if __name__ == "__main__":
    main()
