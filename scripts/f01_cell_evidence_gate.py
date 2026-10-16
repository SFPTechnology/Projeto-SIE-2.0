#!/usr/bin/env python3
"""F01: auditoria determinística de estrutura/proveniência das células.

--status (padrão): exit 0 se arquivo é íntegro e bloqueios são explícitos.
--strict: exit 1 se faltar cobertura, célula ou atestação obrigatória.
NENHUMA saída é homologação independente ou revisão humana.
"""
from __future__ import annotations

import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = "docs/implantacao-sie-2-0/F01/MATRIZ_CELULAS_NORMATIVAS_F01.json"
REQUIRED = frozenset({"RCA", "XL", "IZ", "FATORES_CORRECAO",
                      "EDP_DEMANDA", "EDP_MODALIDADE"})
STATES = frozenset({"BLOCKED_SOURCE", "READY_FOR_INDEPENDENT_REVIEW",
                    "EVIDENCE_RECONCILED"})
SHA256 = re.compile(r"^[0-9a-f]{64}$")


def _nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def _hash_file(root: Path, ref: object) -> bool:
    if not isinstance(ref, dict) or not _nonempty(ref.get("path")):
        return False
    path_value, claimed = ref["path"], ref.get("sha256")
    if not isinstance(claimed, str) or not SHA256.fullmatch(claimed):
        return False
    try:
        path = (root / path_value).resolve(strict=True)
        if not path.is_relative_to(root.resolve()) or not path.is_file():
            return False
        return sha256(path.read_bytes()).hexdigest() == claimed
    except (OSError, ValueError):
        return False


def inspect(root: Path, data: dict) -> dict:
    errors, blockers = [], []
    if data.get("schema_version") != 1 or data.get("phase") != "F01":
        errors.append("schema_version/phase invalidos")
    if data.get("normative_conformity_verified") is not False or data.get("release_allowed") is not False:
        errors.append("matriz nao pode autodeclarar liberacao normativa")
    if not isinstance(data.get("source_index"), list):
        errors.append("source_index ausente")
    source_ids = {s.get("id") for s in data.get("source_index", [])
                  if isinstance(s, dict)}
    entries = data.get("entries")
    if not isinstance(entries, list) or not entries:
        errors.append("entries precisa conter familias e celulas")
        entries = []
    groups, ids, reconciled = set(), set(), 0
    for raw in entries:
        if not isinstance(raw, dict):
            errors.append("Entrada normativa malformada")
            continue
        key, group = raw.get("id"), raw.get("group")
        if not _nonempty(key) or key in ids:
            errors.append(f"Identificador duplicado/ausente: {key}")
        ids.add(key)
        groups.add(group)
        if group not in REQUIRED:
            errors.append(f"{key}: familia nao prevista")
        if raw.get("source_id") not in source_ids:
            errors.append(f"{key}: fonte fora do inventario oficial")
        state = raw.get("status")
        if state not in STATES:
            errors.append(f"{key}: status invalido")
            continue
        if raw.get("automated_gate_claim") is not False:
            errors.append(f"{key}: alegacao de gate automatico nao permitida")
        if raw.get("mandatory") is not True:
            errors.append(f"{key}: familia obrigatoria nao pode ser omitida por automacao")
        if state == "BLOCKED_SOURCE":
            blockers.append(f"{key}: fonte/celula nao confirmada")
            continue
        if state == "READY_FOR_INDEPENDENT_REVIEW":
            blockers.append(f"{key}: segunda conferencia independente ausente")
            continue
        source, cell = raw.get("source"), raw.get("cell")
        if not isinstance(source, dict) or not isinstance(cell, dict):
            errors.append(f"{key}: fonte/celula reconciliada malformada")
            continue
        if not (_nonempty(source.get("document_id")) and
                _nonempty(source.get("edition")) and
                isinstance(source.get("original_sha256"), str) and
                SHA256.fullmatch(source["original_sha256"]) and
                source.get("original_confirmed") is True and
                source.get("authorised_use") is True):
            errors.append(f"{key}: original, edicao, hash ou direito de uso nao declarados")
        required_cell = ("table", "page", "row", "column", "unit",
                         "canonical_value", "notes", "installation_conditions")
        if any(not _nonempty(cell.get(k)) for k in required_cell):
            errors.append(f"{key}: celula requer tabela, pagina, linha, coluna, unidade, valor, notas e condicoes")
        reviewers = raw.get("reviewers")
        if not isinstance(reviewers, dict) or not all(
            isinstance(reviewers.get(k), dict) for k in ("A", "B")
        ):
            errors.append(f"{key}: revisores A e B ausentes")
        else:
            A, B = reviewers["A"], reviewers["B"]
            if not (_nonempty(A.get("reviewer_id")) and _nonempty(B.get("reviewer_id")) and
                    A["reviewer_id"] != B["reviewer_id"] and
                    _nonempty(A.get("independent_workflow_run")) and
                    _nonempty(B.get("independent_workflow_run")) and
                    A["independent_workflow_run"] != B["independent_workflow_run"]):
                errors.append(f"{key}: dois registros de conferentes distintos requeridos")
        refs = raw.get("artifacts")
        if not isinstance(refs, list) or len(refs) < 2 or not all(
            _hash_file(root, ref) for ref in refs
        ):
            errors.append(f"{key}: falta evidencia auditavel de duas leituras e checksums")
        external = raw.get("external_attestation")
        if not isinstance(external, dict) or external.get("professional_review") is not True or not _hash_file(root, external.get("artifact")):
            errors.append(f"{key}: atestacao profissional auditavel ausente")
        reconciled += 1
    if groups != REQUIRED:
        errors.append(f"Familias ausentes/extra: {sorted(REQUIRED - groups)} / {sorted(groups - REQUIRED)}")
    # Seis rastreadores de familia nao representam o universo de celulas usadas.
    policy = data.get("coverage_policy")
    if policy != "ALL_CELLS_USED_BY_ACTIVE_MOTORS_MUST_BE_ENUMERATED; THE_SIX_ROWS_ARE_FAMILY_TRACKERS_NOT_EXHAUSTIVE_CELLS":
        errors.append("Politica obrigatoria de inventario exaustivo alterada")
    coverage = data.get("active_motor_cells_inventory")
    if not isinstance(coverage, dict) or coverage.get("complete") is not True or not _hash_file(root, coverage.get("artifact")):
        blockers.append("Cobertura exaustiva de celulas consumidas nos motores ainda nao atestada")
    structurally_ready = not errors and not blockers and reconciled == len(entries)
    return {
        "phase": "F01", "status": "READY_FOR_EXTERNAL_AUDIT" if structurally_ready else "BLOCKED_EVIDENCE",
        "entries_total": len(entries), "families_covered": sorted(groups & REQUIRED),
        "reconciled_entries": reconciled,
        "blockers": blockers, "integrity_errors": errors,
        "structure_complete": structurally_ready,
        "normative_approval_granted_by_tool": False,
        "f02_release_allowed": False,
        "warning": "Arquivos, hashes e campos conferidos pelo script NAO comprovam autenticidade nem independencia factual."
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    data = json.loads((root / MATRIX_PATH).read_text(encoding="utf-8"))
    result = inspect(root, data)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    if result["integrity_errors"]:
        return 2
    if args.strict and not result["structure_complete"]:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
