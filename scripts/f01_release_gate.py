#!/usr/bin/env python3
"""Guardião determinístico F01: detecta aprovação autodeclarada e perda de evidência.

Não valida conteúdo de normas, licença ou independência humana por si só.
Não altera ORCHESTRATOR_STATE.json, não concede homologação nem libera F02.
"""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
import sys

GATES = tuple(f"G{i:02d}" for i in range(1, 7))
AGENTS = ("QA-01", "QA-02", "QA-03")
REQUIRED_SKILLS = {
    "f01-qa-arquiteto": ("f01-arquitetura-integridade", "f01-verificacao-multigates"),
    "f01-qa-engenheiro-eletrico": ("f01-engenharia-fontes", "f01-calculo-independente"),
    "f01-qa-dados-ux-llm": ("f01-dados-evidencias", "f01-ux-llm-seguranca"),
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def evidence_ok(root: Path, obj: object) -> bool:
    """Conferência de integridade de arquivos do checkout; NÃO autenticidade da fonte."""
    if not isinstance(obj, dict):
        return False
    relative, claimed_hash = obj.get("path"), obj.get("sha256")
    if (not isinstance(relative, str) or not relative or
        not isinstance(claimed_hash, str) or not re.fullmatch(r"[0-9a-f]{64}", claimed_hash)):
        return False
    path = root / relative
    try:
        resolved = path.resolve(strict=True)
        if not resolved.is_file() or not resolved.is_relative_to(root.resolve()):
            return False
        return sha256(resolved.read_bytes()).hexdigest() == claimed_hash
    except (OSError, ValueError):
        return False


def inspect(root: Path, manifest: dict, state: dict) -> dict:
    faults = []
    if manifest.get("schema_version") != 1 or manifest.get("phase") != "F01":
        faults.append("Versão ou fase inválida")
    gates = manifest.get("gates")
    if not isinstance(gates, list) or len(gates) != 6:
        faults.append("Seis gates G01-G06 obrigatórios")
        gates = []
    if {x.get("id") for x in gates if isinstance(x, dict)} != set(GATES):
        faults.append("IDs de gates ausentes/duplicados")
    pass_gates = []
    for gate in gates:
        if not isinstance(gate, dict):
            faults.append("Gate malformado")
            continue
        name = gate.get("id")
        if gate.get("status") not in {"BLOCKED", "PARTIAL", "PASS"}:
            faults.append(f"{name}: status inválido")
        evidence = gate.get("evidence")
        if not isinstance(evidence, list):
            faults.append(f"{name}: evidências precisam ser lista")
            evidence = []
        evidence_valid = bool(evidence) and all(evidence_ok(root, e) for e in evidence)
        approved = gate.get("accepted") is True
        if approved and (gate.get("status") != "PASS" or not evidence_valid or
                         gate.get("independent_external_verification") is not True):
            faults.append(f"{name}: aprovação sem prova local íntegra + revisão externa declarada")
        if not approved and gate.get("status") == "PASS":
            faults.append(f"{name}: PASS incoerente sem accepted")
        if approved and evidence_valid and gate.get("status") == "PASS":
            pass_gates.append(name)
    agents = manifest.get("agents")
    if not isinstance(agents, list) or len(agents) != 3 or {
        a.get("id") for a in agents if isinstance(a, dict)
    } != set(AGENTS):
        faults.append("QA-01, QA-02 e QA-03 distintos obrigatórios")
        agents = []
    seen_commits = []
    for a in agents:
        if not isinstance(a, dict):
            faults.append("Agente malformado")
            continue
        if a.get("status") not in {"NOT_EXECUTED", "RUNNING", "REVIEWED"}:
            faults.append("Estado do agente desconhecido")
        if a.get("status") == "REVIEWED":
            sha = a.get("independent_first_pass_commit")
            if not isinstance(sha, str) or not re.fullmatch(r"[0-9a-f]{40}", sha):
                faults.append(f"{a.get('id')}: parecer sem commit congelado")
            else:
                seen_commits.append(sha)
            if not a.get("review_package"):
                faults.append(f"{a.get('id')}: ausência do relatório individual")
    if len(seen_commits) != len(set(seen_commits)):
        faults.append("Primeiras análises compartilham o mesmo commit: isolamento não demonstrado")
    cross = manifest.get("cross_reviews")
    if not isinstance(cross, list) or len(cross) != 3:
        faults.append("Três revisões cruzadas são obrigatórias")
        cross = []
    expected = {("QA-01", "QA-02"), ("QA-02", "QA-03"), ("QA-03", "QA-01")}
    observed = {(c.get("author"), c.get("reviewer")) for c in cross if isinstance(c, dict)}
    if observed != expected:
        faults.append("Matriz de revisão cruzada inválida")
    for c in cross:
        if c.get("status") not in {"NOT_EXECUTED", "RUNNING", "REVIEWED"}:
            faults.append("Revisão cruzada com estado inválido")
    phase = next((t for t in state.get("tasks", []) if t.get("id") == "F01"), {})
    precursor = next((t for t in state.get("tasks", []) if t.get("id") == "F00"), {})
    if precursor.get("state") != "DONE":
        faults.append("F00 precisa estar DONE")
    if not phase:
        faults.append("F01 inexistente no orquestrador")
    if manifest.get("state") not in {"BLOCKED", "PENDING_REVIEW", "DONE"}:
        faults.append("Estado F01 desconhecido no manifesto")
    if manifest.get("state") == "DONE" and phase.get("state") != "DONE":
        faults.append("Manifesto diz DONE mas orquestrador não")
    if phase.get("state") == "DONE" and manifest.get("state") != "DONE":
        faults.append("Orquestrador diz DONE mas manifesto não")
    if phase.get("state") != "DONE" and manifest.get("f02_release_allowed") is not False:
        faults.append("F02 não pode ser liberada com F01 bloqueada")
    signoff = manifest.get("external_normative_signoff", {})
    reviews_all = (len(agents) == 3 and all(a.get("status") == "REVIEWED" for a in agents) and
                   len(cross) == 3 and all(c.get("status") == "REVIEWED" for c in cross))
    evidence_ready = (len(pass_gates) == 6 and reviews_all and
                      signoff.get("status") == "VERIFIED" and
                      bool(signoff.get("signed_evidence")))
    if phase.get("state") == "DONE" and not evidence_ready:
        faults.append("F01 DONE sem 6 gates, três pareceres independentes e atestação externa")
    if manifest.get("f02_release_allowed") is True and not evidence_ready:
        faults.append("F02 liberada sem pré-requisitos")
    return {"phase": "F01", "passed_gates": sorted(pass_gates),
            "total_gates": 6, "evidence_ready_for_external_decision": evidence_ready,
            "f01_state": phase.get("state"), "f02_release_allowed": manifest.get("f02_release_allowed"),
            "integrity_errors": faults,
            "note": "Conferência estrutural e de hash NÃO certifica normas ou revisão humana."}


def verify_profiles(root: Path):
    errors = []
    for agent, skills in REQUIRED_SKILLS.items():
        profile = root / ".github" / "agents" / f"{agent}.agent.md"
        if not profile.is_file():
            errors.append(f"Perfil ausente: {agent}")
            continue
        contents = profile.read_text(encoding="utf-8")
        if not contents.startswith("---\n") or "description:" not in contents:
            errors.append(f"Frontmatter ausente em {agent}")
        for skill in skills:
            f = root / ".github" / "skills" / skill / "SKILL.md"
            if not f.is_file() or not f.read_text(encoding="utf-8").startswith(f"---\nname: {skill}\n"):
                errors.append(f"Skill ausente/malformada: {skill}")
            if skill not in contents:
                errors.append(f"{agent} não referencia {skill}")
    return errors


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--verify-invariants", action="store_true")
    parser.add_argument("--check-release", action="store_true")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    manifest = load_json(root / "docs/implantacao-sie-2-0/F01/QA3_MANIFEST.json")
    state = load_json(root / "docs/sie-orchestrator/ORCHESTRATOR_STATE.json")
    result = inspect(root, manifest, state)
    result["integrity_errors"].extend(verify_profiles(root))
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    if result["integrity_errors"]:
        return 2
    if args.check_release:
        # Revisão humana e homologação documental continuam sendo etapas externas.
        return 0 if result["evidence_ready_for_external_decision"] else 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
