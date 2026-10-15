"""Inventario offline, sem aprovar dados normativos.

SHA-256 comprova a integridade da copia digital identificada, nunca a
aplicabilidade da edicao, a fidelidade de OCR ou a validade de valores.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path, PurePosixPath
from typing import Sequence


# Caminhos observados no repositorio; somente metadados sao exportados.
SOURCE_SPECS = (
    ("EDP-SP-V09-PDF", "Arquivos_Diversos/Norma_EDP/PT.DT.PDN.00068_V9.pdf", "PDF_CANDIDATO_FONTE_PRIMARIA"),
    ("EDP-SP-V09-EXTRACAO", "Arquivos_Diversos/Norma_EDP/PT.DT.PDN.00068_V9_chunks.json", "EXTRACAO_DERIVADA"),
    ("EDP-SP-V09-CONFERENCIA", "Arquivos_Diversos/QA_CONFERENCIA_CERTFID_TABELAS_EDP.md", "REGISTRO_DE_CONFERENCIA"),
    ("NBR-5410-TEXTO", "Arquivos_Diversos/NBR_5410_original/NBR-5410.md", "TRANSCRICAO_DERIVADA"),
    ("NBR-5410-CHUNKS", "Arquivos_Diversos/NBR_5410_original/NBR_5410_chunks.json", "EXTRACAO_DERIVADA"),
    ("NBR-5410-COMENTADA-MANIFESTO", "Arquivos_Diversos/NBR_5410_comentada/chunks_json_16_pdfs_v2/manifesto_processamento.json", "MANIFESTO_DE_EXTRACAO"),
)


def _file_metadata(root: Path, relative: str) -> dict:
    part = PurePosixPath(relative)
    if not relative or part.is_absolute() or ".." in part.parts:
        raise ValueError("Caminho de fonte fora do repositorio")
    target = root.joinpath(*part.parts).resolve()
    if not target.is_relative_to(root):
        raise ValueError("Fonte aponta para fora do repositorio")
    if not target.is_file():
        return {"path": relative, "state": "MISSING", "sha256": None, "size_bytes": None}

    hasher = sha256()
    size = 0
    with target.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            hasher.update(block)
            size += len(block)
    return {"path": relative, "state": "PRESENT_UNVERIFIED", "sha256": hasher.hexdigest(), "size_bytes": size}


def inventory_sources(root: str | Path, specs: Sequence[tuple[str, str, str]] = SOURCE_SPECS) -> dict:
    base = Path(root).resolve()
    if not base.is_dir():
        raise ValueError("Diretorio do repositorio nao existe")
    identifiers = set()
    entries = []
    for source_id, relative, role in specs:
        if source_id in identifiers:
            raise ValueError("ID de fonte duplicado")
        identifiers.add(source_id)
        entry = _file_metadata(base, relative)
        entries.append({"id": source_id, "role": role, **entry, "normative_validation": "NOT_PERFORMED"})
    present = sum(item["state"] == "PRESENT_UNVERIFIED" for item in entries)
    return {
        "schema_version": 1,
        "scope": "SOURCE_INTEGRITY_INVENTORY_ONLY",
        "repository_approval": False,
        "normative_conformity_verified": False,
        "sources_present": present,
        "sources_missing": len(entries) - present,
        "entries": entries,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Inventario SHA256 de fontes normativas sem validacao normativa.")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[4])
    parser.add_argument("--output", type=Path, help="Destino JSON opcional para auditoria")
    parser.add_argument("--require-all", action="store_true", help="Falhar se artefatos conhecidos estiverem ausentes")
    args = parser.parse_args(argv)
    report = inventory_sources(args.root)
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "scope": report["scope"],
        "present": report["sources_present"],
        "missing": report["sources_missing"],
        "normative_conformity_verified": False,
        "output": str(args.output) if args.output is not None else None,
    }, ensure_ascii=False))
    return 2 if args.require_all and report["sources_missing"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
