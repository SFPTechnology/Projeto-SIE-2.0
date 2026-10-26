#!/usr/bin/env python3
"""F12 preparation gate: read-only, fail-closed, never authorizes production.

Usage: python scripts/f12_release_gate.py --check [--root path]
       python scripts/f12_release_gate.py --require-production  # always denied

This tool validates a pinned F11 handoff, the F12 candidate metadata and
required documentation in the checked-out Git tree. Passing means that
PREPARATION metadata is internally consistent, not GO/NO-GO authorization.
"""
import argparse
import json
import subprocess
from pathlib import Path

F11_SHA = "11643cf3ad7da2e6182183c6071148f924bfe741"
REQUIRED_DOCS = (
    "docs/implantacao-sie-2-0/F12/MANIFESTO_RELEASE.md",
    "docs/implantacao-sie-2-0/F12/NOTAS_VERSAO.md",
    "docs/implantacao-sie-2-0/F12/CHECKLIST_GO_NO_GO.md",
    "docs/implantacao-sie-2-0/F12/PLANO_IMPLANTACAO_ROLLBACK.md",
    "docs/implantacao-sie-2-0/F12/MANUAL_ADMINISTRACAO.md",
    "docs/implantacao-sie-2-0/F12/MANUAL_USUARIO_F12.md",
    "docs/implantacao-sie-2-0/F12/PLANO_MONITORAMENTO_SUPORTE.md",
    "docs/implantacao-sie-2-0/F12/POLITICA_NORMATIVA_ASBUILT.md",
    "docs/implantacao-sie-2-0/F12/RELATORIO_EXECUCAO.md",
)
ALLOWED_TASK_STATES = {"PENDENTE", "PREPARADO", "PARCIAL", "HUMAN_REQUIRED", "BLOQUEADO"}
ALLOWED_PATHS = {
    "scripts/f12_release_gate.py",
    "scripts/f12_bundle.py",
    "scripts/f12_staging_smoke.py",
    "restructuring/apps/api/sie_api/f12_consultative.py",
    "restructuring/apps/api/tests/test_f12_consultative.py",
    "restructuring/apps/api/tests/test_f12_release_gate.py",
    ".github/workflows/sie-f12-release-safety.yml",
    "docs/stories/story-SIE-F12-LIBERACAO-CONTROLADA.md",
    "docs/sie-orchestrator/ORCHESTRATOR_STATE.json",
    "docs/sie-orchestrator/NEXT_ACTION.md",
    "docs/sie-orchestrator/EXECUTION_QUEUE.md",
    "docs/sie-orchestrator/VALIDATION_MATRIX.md",
}


def scope_violations(changed):
    """Fail closed on changes to engines, norms, production or unrelated files."""
    return sorted(path for path in changed
                  if path not in ALLOWED_PATHS
                  and not path.startswith("docs/implantacao-sie-2-0/F12/"))



def assess(manifest, orchestrator, present):
    """Return actionable defects; this does NOT issue a release decision."""
    errors = []
    if not isinstance(manifest, dict) or not isinstance(orchestrator, dict):
        return ["manifesto ou orquestrador inválido"]
    if manifest.get("schema") != "sie-f12-preparation-1":
        errors.append("schema de candidato desconhecido")
    if manifest.get("base_sha") != F11_SHA:
        errors.append("SHA F11 não corresponde ao handoff fixado")
    if manifest.get("scope") != "LOCAL_SOFTWARE_QA_PREPARATION_ONLY":
        errors.append("escopo diferente da preparação local aprovada")
    for flag in ("production_release_allowed", "professional_approval",
                 "deployment_executed", "change_approved"):
        if manifest.get(flag) is not False:
            errors.append(f"{flag} deve ser false nesta fase")
    for key in ("api_version", "supported_candidate", "backup_contract"):
        if not isinstance(manifest.get(key), str) or not manifest[key]:
            errors.append(f"{key} não identificado")
    tasks = manifest.get("tasks")
    if not isinstance(tasks, dict) or set(tasks) != {f"12.{i:02d}" for i in range(1, 11)}:
        errors.append("inventário das dez tasks incompleto")
    elif any(value not in ALLOWED_TASK_STATES for value in tasks.values()):
        errors.append("estado de task inválido ou conclusão não comprovada")
    f11 = next((t for t in orchestrator.get("tasks", []) if t.get("id") == "F11"), None)
    if not f11 or f11.get("state") != "DONE":
        errors.append("F11 não está DONE no registro canônico")
    elif f11.get("checkpoint", {}).get("professional_approval") is not False:
        errors.append("contrato de homologação profissional F11 divergente")
    missing = sorted(set(REQUIRED_DOCS) - set(present))
    if missing:
        errors.append("documentos F12 ausentes: " + ", ".join(missing))
    return errors


def git_attestation(root):
    """Ensure base is a real ancestor, not merely a user-controlled string."""
    def run(*args):
        return subprocess.run(["git", "-C", str(root), *args],
                              capture_output=True, text=True, check=False)
    base = run("cat-file", "-e", F11_SHA + "^{commit}")
    if base.returncode:
        return ["commit base F11 ausente no checkout Git"]
    current = run("rev-parse", "HEAD")
    if current.returncode or len(current.stdout.strip()) != 40:
        return ["HEAD Git não verificável"]
    ancestor = run("merge-base", "--is-ancestor", F11_SHA, "HEAD")
    if ancestor.returncode:
        return ["HEAD não descende do commit F11 fixado"]
    diff = run("diff", "--name-only", F11_SHA, "HEAD")
    if diff.returncode:
        return ["não foi possível auditar a lista de arquivos alterados"]
    forbidden = scope_violations(diff.stdout.splitlines())
    return ["mudanças fora do escopo F12: " + ", ".join(forbidden)] if forbidden else []


def verify(root):
    try:
        manifest = json.loads((root / "docs/implantacao-sie-2-0/F12/MANIFESTO_RELEASE.json").read_text(encoding="utf-8"))
        state = json.loads((root / "docs/sie-orchestrator/ORCHESTRATOR_STATE.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return ["falha ao abrir/interpretar manifesto ou estado: " + str(exc)]
    found = [x for x in REQUIRED_DOCS if (root / x).is_file()]
    return assess(manifest, state, found) + git_attestation(root)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--check", action="store_true", help="validate preparation metadata (default)")
    parser.add_argument("--require-production", action="store_true",
                        help="fail closed: deployment is forbidden without separate human change control")
    args = parser.parse_args(argv)
    issues = verify(args.root.resolve())
    if args.require_production:
        issues.append("GO/NO-GO de produção requer autorização formal e ensaios externos; execução recusada")
    print(json.dumps({"status": "BLOCKED" if issues else "PREPARATION_VERIFIED_ONLY",
                      "production_authorized": False, "errors": issues},
                     ensure_ascii=False, indent=2))
    return 2 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
