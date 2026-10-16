#!/usr/bin/env python3
"""SIE F01 YOLO — executor autocontido e fail-closed para sandbox descartável.

Modo padrão: somente plano; nenhum agente é iniciado. --execute --sandbox-confirmed
inicia Copilot CLI em sessões SEPARADAS; --yolo só é adequado em VM/container
sem credenciais de produção. O executor NUNCA homologa normas nem libera F02.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import traceback
from typing import Sequence

ROOT = Path(__file__).resolve().parents[1]
PHASE = "feat/f01-governanca-normativa"
PLAN = "docs/implantacao-sie-2-0/F01/PLANO_EXECUCAO_AUTONOMA_YOLO.md"
MANIFEST = "docs/implantacao-sie-2-0/F01/QA3_MANIFEST.json"
STATE = "docs/sie-orchestrator/ORCHESTRATOR_STATE.json"
PREFLIGHT_LOGIC = ("scripts/f01_release_gate.py", "--verify-invariants")
QA = (
    ("QA-01", "f01-qa-arquiteto", "qa/f01-arquiteto", "QA-03"),
    ("QA-02", "f01-qa-engenheiro-eletrico", "qa/f01-engenheiro-eletrico", "QA-01"),
    ("QA-03", "f01-qa-dados-ux-llm", "qa/f01-dados-ux-llm", "QA-02"),
)
# No tool/prompt instruction overrides these controls. See sandbox limitations.
DENY_PREFIXES = (
    ".env", ".github/workflows/", "docs/implantacao-sie-2-0/F00/",
    "docs/sie-orchestrator/ORCHESTRATOR_STATE.json",
    MANIFEST, "scripts/f00_golden.py",
)
DENY_PARTS = {"secrets", ".aws", ".ssh", ".git", ".venv", "node_modules"}
SENSITIVE_MARKERS = (".pem", ".p12", ".pfx", ".key", ".sqlite", ".db")
PASS_STATES = {"BLOCKED", "PENDING_REVIEW"}
MAX_AGENT_ROUNDS = 3
MAX_INTEGRATION_ROUNDS = 2
TIMEOUT_SECONDS = 2400


class Blocked(RuntimeError):
    def __init__(self, code: str, reason: str):
        super().__init__(reason)
        self.code = code


@dataclass
class AgentResult:
    agent: str
    branch: str
    first_sha: str
    tests_passed: bool
    report_complete: bool
    blockers: list[str]


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def frozen_state(root: Path = ROOT) -> dict:
    state = load(root / STATE)
    manifest = load(root / MANIFEST)
    tasks = {item["id"]: item for item in state["tasks"]}
    if tasks["F00"]["state"] != "DONE":
        raise Blocked("BLOCKED_PREDECESSOR", "F00 não está DONE; abortar sem reabri-la")
    if tasks["F01"]["state"] != "BLOCKED" or manifest["state"] not in PASS_STATES:
        raise Blocked("BLOCKED_STATE", "Estado inicial F01 inesperado")
    if manifest.get("f02_release_allowed") is not False:
        raise Blocked("BLOCKED_STATE", "F02 indevidamente liberada no manifesto")
    if len(manifest["gates"]) != 6 or len(manifest["agents"]) != 3:
        raise Blocked("BLOCKED_STATE", "QA3/gates divergentes")
    return {"f00": "DONE", "f01": "BLOCKED", "f02": False,
            "gates_accepted": sum(g["accepted"] is True for g in manifest["gates"]),
            "agent_baseline_sha": manifest["agent_baseline_sha"]}


def planned_tasks(root: Path = ROOT) -> dict:
    result = frozen_state(root)
    missing = [p for p in (PLAN, MANIFEST, STATE,
                           "scripts/f01_release_gate.py",
                           "scripts/f01_cell_evidence_gate.py",
                           "docs/implantacao-sie-2-0/F01/MATRIZ_CELULAS_NORMATIVAS_F01.json",
                           "docs/implantacao-sie-2-0/F01/PLANO_YOLO_DESBLOQUEIO_F01_V2.md")
               if not (root / p).is_file()]
    missing += [f".github/agents/{a}.agent.md" for _, a, _, _ in QA
                if not (root / ".github/agents" / f"{a}.agent.md").is_file()]
    if missing:
        raise Blocked("BLOCKED_ENVIRONMENT", f"Arquivos ausentes: {missing}")
    result.update({"mode": "DRY_RUN", "agent_sessions_started": 0,
                   "workstreams": [{"id": q, "profile": profile, "branch": br}
                                   for q, profile, br, _ in QA],
                   "stages": ["E00-preflight", "E01-worktrees", "E02-agent-first-pass",
                              "E03-autoheal", "E04-freeze", "E05-cross-review",
                              "E06-integration", "E07-regression",
                              "E08-gates", "E09-evidence-report"],
                   "note": "DRY_RUN não abre sessões nem declara aprovação normativa"})
    return result


def exec_command(args: Sequence[str], cwd: Path, *, timeout: int = 120,
                 environment: dict | None = None) -> tuple[int, str]:
    try:
        proc = subprocess.run(list(map(str, args)), cwd=cwd,
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                              text=True, encoding="utf-8", errors="replace",
                              timeout=timeout, env=environment, check=False)
        return proc.returncode, proc.stdout
    except subprocess.TimeoutExpired as err:
        return 124, f"TIMEOUT ({timeout}s): {err.cmd}"


def need(args: Sequence[str], cwd: Path, code="FAILED_TECHNICAL", timeout=120) -> str:
    rc, out = exec_command(args, cwd, timeout=timeout)
    if rc != 0:
        raise Blocked(code, f"{' '.join(map(str, args))} falhou ({rc}):\n{out[-2200:]}")
    return out.strip()


def check_clean(worktree: Path):
    status = need(["git", "status", "--porcelain"], worktree)
    if status:
        raise Blocked("BLOCKED_SECURITY", f"Worktree possui alterações não revisadas: {worktree}\n{status[:900]}")


def assert_allowed(worktree: Path):
    _, changed = exec_command(["git", "status", "--porcelain", "-uall"], worktree)
    files = []
    for row in changed.splitlines():
        if len(row) < 4:
            continue
        name = row[3:].strip().replace("\\", "/")
        if " -> " in name:
            name = name.split(" -> ", 1)[1]
        name = name.strip('"')
        files.append(name)
    forbidden = []
    for item in files:
        lower = item.casefold()
        segments = set(lower.split("/"))
        if (item.startswith("/") or ".." in item.split("/") or
            any(lower.startswith(x.casefold()) for x in DENY_PREFIXES) or
            segments.intersection(DENY_PARTS) or
            lower.endswith(SENSITIVE_MARKERS) or
            any(s in lower for s in ("token", "credential", "private_key", "apikey"))):
            forbidden.append(item)
    if forbidden:
        raise Blocked("BLOCKED_SECURITY", f"Arquivos sensíveis/controlados alterados: {forbidden}")
    return files


def safe_git_commit(worktree: Path, message: str) -> str:
    changes = assert_allowed(worktree)
    if changes:
        need(["git", "add", "--all"], worktree)
        need(["git", "commit", "-m", message], worktree)
    return need(["git", "rev-parse", "HEAD"], worktree)


def push_whitelisted(worktree: Path, branch: str):
    """Publica apenas branches de trabalho explícitas; nunca main/force-push."""
    allowed = {PHASE} | {item[2] for item in QA}
    if branch not in allowed:
        raise Blocked("BLOCKED_SECURITY", f"Push fora do escopo F01: {branch}")
    actual = need(["git", "branch", "--show-current"], worktree)
    if actual != branch:
        raise Blocked("BLOCKED_SECURITY", f"Push: checkout {actual} difere de {branch}")
    # Nunca usar --force; rejeição non-fast-forward encerra a operação.
    need(["git", "push", "origin", f"HEAD:refs/heads/{branch}"],
         worktree, code="FAILED_TECHNICAL", timeout=300)


def copy_env() -> dict:
    """Reduz vazamento acidental de vars de serviço; isolamento real é externo."""
    env = os.environ.copy()
    for key in tuple(env):
        upper = key.upper()
        if any(mark in upper for mark in ("SUPABASE", "OPENAI_API", "STRIPE",
                                          "DATABASE_URL", "AWS_", "AZURE_",
                                          "SECRET", "PASSWORD", "PRIVATE_KEY")):
            if upper not in {"COPILOT_GITHUB_TOKEN"}:
                env.pop(key, None)
    return env


def run_agent(worktree: Path, profile: str, prompt: str,
              logdir: Path, label: str) -> tuple[int, str]:
    if shutil.which("copilot") is None:
        raise Blocked("BLOCKED_ENVIRONMENT", "GitHub Copilot CLI não instalado")
    # --autopilot continua a tarefa; --no-ask-user suprime perguntas;\n    # --yolo so permitido em VM isolada. Limite evita creditos/loops sem fim.
    cmd = ["copilot", f"--agent={profile}", "-p", prompt,
           "--autopilot", "--yolo", "--no-ask-user",
           "--max-autopilot-continues=10",
           "--secret-env-vars=GH_TOKEN,GITHUB_TOKEN,COPILOT_GITHUB_TOKEN"]
    status, out = exec_command(cmd, worktree, timeout=TIMEOUT_SECONDS,
                               environment=copy_env())
    logdir.mkdir(parents=True, exist_ok=True)
    (logdir / f"{label}.log").write_text(out, encoding="utf-8")
    return status, out


def local_tests(worktree: Path, logdir: Path, prefix: str) -> tuple[bool, str]:
    tests = [
        ([sys.executable, "scripts/f01_release_gate.py", "--verify-invariants"], worktree, 80),
        ([sys.executable, "scripts/f01_cell_evidence_gate.py"], worktree, 80),
        ([sys.executable, "scripts/f00_golden.py", "--verify"], worktree, 240),
        ([sys.executable, "-m", "pytest", "-q"], worktree / "restructuring/apps/api", 900),
    ]
    if shutil.which("node"):
        tests.append((["node", "--check", "restructuring/apps/web/app.js"], worktree, 60))
    else:
        return False, "node ausente; checagem JavaScript necessária"
    reports = []
    for cmd, cwd, timeout in tests:
        rc, out = exec_command(cmd, cwd, timeout=timeout)
        reports.append(f"$ {' '.join(cmd)}\nrc={rc}\n{out[-5000:]}")
    report = "\n\n".join(reports)
    logdir.mkdir(parents=True, exist_ok=True)
    (logdir / f"{prefix}-tests.log").write_text(report, encoding="utf-8")
    return all("rc=0\n" in s for s in reports), report


def reports_present(worktree: Path, qa: str) -> list[str]:
    base = worktree / "docs/implantacao-sie-2-0/F01/qa3-runs" / qa
    required = ["PLANO_E_EXECUCAO.md", "MATRIZ_6_GATES.json", "PARECER_QA.md"]
    missing = [name for name in required if not (base / name).is_file()]
    if not missing:
        try:
            report = load(base / "MATRIZ_6_GATES.json")
            # Não autentica decisão de agente: somente confirma existência de dados parseáveis.
            if not isinstance(report, (list, dict)):
                missing.append("MATRIZ_6_GATES.json inválida")
        except (OSError, ValueError):
            missing.append("MATRIZ_6_GATES.json inválida")
    return missing


def create_worktree(root: Path, target: Path, branch: str):
    if target.exists():
        existing = need(["git", "branch", "--show-current"], target)
        if existing != branch:
            raise Blocked("BLOCKED_SECURITY", f"Worktree inesperado em {target}")
        check_clean(target)
        return
    rc, _ = exec_command(["git", "show-ref", "--verify", "--quiet",
                          f"refs/heads/{branch}"], root)
    if rc == 0:
        need(["git", "worktree", "add", str(target), branch], root)
    else:
        need(["git", "worktree", "add", "-b", branch, str(target),
              f"origin/{branch}"], root)
    check_clean(target)


def synchronize_qa_branch(root: Path, worktree: Path, branch: str, base_sha: str) -> str:
    """Avança cada QA apenas por fast-forward para a MESMA F01 atual.

    Detecta branches com trabalho não integrado; jamais reescreve histórico.
    """
    allowed = {a[2] for a in QA}
    if branch not in allowed:
        raise Blocked("BLOCKED_SECURITY", "Branch QA fora da whitelist")
    if need(["git", "branch", "--show-current"], worktree) != branch:
        raise Blocked("BLOCKED_SECURITY", "A branch do worktree não confere")
    check_clean(worktree)
    previous = need(["git", "rev-parse", "HEAD"], worktree)
    if previous != base_sha:
        ancestor, _ = exec_command(
            ["git", "merge-base", "--is-ancestor", previous, base_sha], worktree)
        if ancestor != 0:
            raise Blocked(
                "BLOCKED_BRANCH_DIVERGENCE",
                f"{branch} não é ancestral da F01 {base_sha[:12]}; "
                "não sobrescrever commits independentes existentes",
            )
        need(["git", "merge", "--ff-only", base_sha], worktree,
             code="BLOCKED_BRANCH_DIVERGENCE", timeout=120)
        check_clean(worktree)
        push_whitelisted(worktree, branch)
    final = need(["git", "rev-parse", "HEAD"], worktree)
    if final != base_sha:
        raise Blocked("BLOCKED_BRANCH_DIVERGENCE", "QA não alcançou baseline comum")
    return final


def preflight(root: Path):
    planned_tasks(root)
    if not Path(root / ".git").exists():
        raise Blocked("BLOCKED_ENVIRONMENT", "Clone Git não encontrado")
    branch = need(["git", "branch", "--show-current"], root)
    if branch != PHASE:
        raise Blocked("BLOCKED_SECURITY", f"Esperado branch F01, encontrado: {branch}")
    check_clean(root)
    need([sys.executable, "scripts/f01_cell_evidence_gate.py"], root,
         code="BLOCKED_EVIDENCE_SCHEMA")
    for item in ["git", "copilot", "node"]:
        if not shutil.which(item):
            raise Blocked("BLOCKED_ENVIRONMENT", f"Pré-requisito ausente: {item}")
    return frozen_state(root)


def verify_no_fake_done(root: Path):
    return frozen_state(root)


def run(root: Path, args) -> dict:
    start = preflight(root)
    workdir = root.parent / "SIE_F01_QA3_WORKTREES"
    runid = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    logdir = root.parent / "SIE_F01_YOLO_LOGS" / runid
    logdir.mkdir(parents=True, exist_ok=False)
    history = [{"stage": "E00", "state": start}]
    # Baseline F01 atual, nunca o SHA antigo do primeiro pacote QA3.
    base_sha = need(["git", "rev-parse", "HEAD"], root)
    need(["git", "fetch", "origin"], root, timeout=300)
    for qa, profile, branch, _ in QA:
        create_worktree(root, workdir / qa, branch)
        synchronize_qa_branch(root, workdir / qa, branch, base_sha)
    history.append({"stage": "E01", "branches": [br for _, _, br, _ in QA],
                    "common_f01_baseline": base_sha, "sync_mode": "FAST_FORWARD_ONLY"})
    by_id = {}
    for qa, profile, branch, reviewer_target in QA:
        wt = workdir / qa
        frozen = None
        missing = []
        report = ""
        ok = False
        for round_idx in range(1, MAX_AGENT_ROUNDS + 1):
            feedback = (f"Corrija o ciclo anterior, sem mudar F00/golden/gates. "
                        f"Relatórios faltando: {missing}. Testes: {report[-4500:]}"
                        if round_idx > 1 else "")
            prompt = (
                f"Você é {qa}, executando SOLO na branch {branch} (sem ler branches QA de outros). "
                f"Leia .github/agents/{profile}.agent.md e suas skills; "
                f"leia docs/implantacao-sie-2-0/F01/QA3_MULTIAGENTES_PLANO_EXECUCAO.md "
                "e PLANO_YOLO_DESBLOQUEIO_F01_V2.md. "
                "Trabalhe sobre a F01 atual sem reimplementar versões anteriores. "
                "Leia MATRIZ_CELULAS_NORMATIVAS_F01.json: trate Iz, Rca, XL, "
                "fatores e EDP com fontes primárias e dupla conferência factual; "
                "se faltar documento, registrar BLOCKED_EVIDENCE. "
                "Implemente todas as cinco etapas E01-E05 da F01, com testes e revisão dos seis "
                "gates G01..G06. Fontes normativas não verificadas devem continuar NÃO HOMOLOGADAS; "
                "faça mudanças de engenharia e documentação seguras, sem falsa aprovação, sem "
                "mudanças em manifestos/gates oficiais, F00, main ou produção. "
                f"Gere docs/implantacao-sie-2-0/F01/qa3-runs/{qa}/PLANO_E_EXECUCAO.md, "
                f"MATRIZ_6_GATES.json e PARECER_QA.md. "
                f"Este é ciclo {round_idx}/{MAX_AGENT_ROUNDS}; {feedback} "
                "Não solicite confirmação; registre BLOCKED_EVIDENCE quando necessário.")
            rc, output = run_agent(wt, profile, prompt, logdir,
                                   f"{qa}-implementacao-{round_idx}")
            if rc != 0:
                report = f"Copilot CLI rc={rc}: {output[-3500:]}"
                if round_idx == MAX_AGENT_ROUNDS:
                    break
                continue
            missing = reports_present(wt, qa)
            ok, report = local_tests(wt, logdir,
                                     f"{qa}-implementacao-{round_idx}")
            if ok and not missing:
                frozen = safe_git_commit(wt, f"feat(f01): first independent QA pass {qa}")
                break
        if frozen is None:
            # Guardamos eventual trabalho seguro, mas sem declarar parecer concluído.
            frozen = safe_git_commit(wt, f"wip(f01): partial QA implementation {qa}")
        by_id[qa] = AgentResult(qa, branch, frozen, ok, not missing,
                                ([f"reports: {missing}"] if missing else []) +
                                ([] if ok else [report[-1400:]]))
        history.append({"stage": "E02-E04", "qa": qa, "sha": frozen,
                        "tests_passed": ok, "reports_complete": not missing,
                        "blocking_findings": by_id[qa].blockers})
    # Exigir três first-pass tecnicamente completos antes de abrir revisão cruzada.
    if not all(x.tests_passed and x.report_complete for x in by_id.values()):
        raise Blocked("FAILED_TECHNICAL",
                      "Primeira rodada QA inconclusa; não fazer revisão cruzada fictícia")
    # Cada branch independente recebe apenas commits que passaram testes e relatório.
    for qa, profile, branch, _ in QA:
        push_whitelisted(workdir / qa, branch)
    history.append({"stage": "E04", "qa_branches_pushed": True})
    for qa, profile, branch, target_id in QA:
        reviewer_wt = workdir / qa
        source_wt = workdir / target_id
        source_sha = by_id[target_id].first_sha
        target_branch = by_id[target_id].branch
        prompt = (
            f"REVISAO CRUZADA F01: você é {qa}. Seu parecer inicial foi congelado em "
            f"{by_id[qa].first_sha}. Agora audite SOMENTE a implementação de {target_id} "
            f"branch {target_branch}, commit {source_sha}, usando git diff/git show "
            "sem editar a branch alvo. Compare arquitetura, cálculos NBR 5410/EDP, "
            "rastreabilidade, testes e UX; busque erros e tentativas de autoaprovação. "
            "Registre divergências/falhas com ID, severidade, arquivo/linha e correção em "
            f"docs/implantacao-sie-2-0/F01/qa3-runs/{qa}/REVISAO_CRUZADA.md. "
            "Não presuma validação profissional externa. Não mude F00, manifesto nem main."
        )
        rc, output = run_agent(reviewer_wt, profile, prompt, logdir,
                               f"{qa}-cruzado-{target_id}")
        if rc != 0:
            raise Blocked("FAILED_TECHNICAL",
                          f"Revisão cruzada {qa}->{target_id} rc={rc}: {output[-750:]}")
        if not (reviewer_wt / f"docs/implantacao-sie-2-0/F01/qa3-runs/{qa}/REVISAO_CRUZADA.md").is_file():
            raise Blocked("FAILED_TECHNICAL", f"Revisão cruzada não produzida por {qa}")
        verified, cross_log = local_tests(reviewer_wt, logdir,
                                          f"{qa}-revisao-cruzada")
        if not verified:
            raise Blocked("FAILED_TECHNICAL",
                          f"Revisor {qa} alterou projeto sem regressão verde: {cross_log[-800:]}")
        sha = safe_git_commit(reviewer_wt, f"docs(f01): independent cross-review {qa} audits {target_id}")
        push_whitelisted(reviewer_wt, branch)
        history.append({"stage": "E05", "reviewer": qa, "target": target_id,
                        "first_pass_target_sha": source_sha, "review_commit": sha})
    # Integração é feita com outro contexto CLI; não mesclar branches cegamente.
    integration_log = ""
    for idx in range(1, MAX_INTEGRATION_ROUNDS + 1):
        refs = "; ".join(f"{qa}={need(['git', 'rev-parse', 'HEAD'], workdir / qa)}"
                         for qa, _, _, _ in QA)
        prompt = (
            "COORDENADOR DE INTEGRAÇÃO F01, não é revisor independente: "
            "leia docs/implantacao-sie-2-0/F01/PLANO_EXECUCAO_AUTONOMA_YOLO.md e os "
            "dossiês QA-01/02/03 congelados e revisões cruzadas nas branches, via git show. "
            f"Branches verificadas: {refs}. Escolha e integre na branch ATUAL F01 "
            "somente soluções comprovadas e compatíveis, resolvendo conflitos pela "
            "engenharia e evidências, não por votação. Não altere F00, manifesto, "
            "ORCHESTRATOR_STATE, main, licenças, dados profissionais, nem force aprovação "
            "ou inicie F02. Implementar correções seguras, criar/atualizar relatórios "
            "de inconsistências em docs/implantacao-sie-2-0/F01. "
            f"Ciclo {idx}/{MAX_INTEGRATION_ROUNDS}; testes anteriores: {integration_log[-3200:]}. "
            "Se normas originais faltarem, preservar bloqueio e produzir dossiê objetivo.")
        rc, output = run_agent(root, "f01-qa-arquiteto", prompt,
                               logdir, f"integracao-{idx}")
        if rc != 0:
            integration_log = f"Copilot integração rc={rc}: {output[-2800:]}"
            continue
        good, integration_log = local_tests(root, logdir, f"integracao-{idx}")
        verify_no_fake_done(root)
        if good:
            final_sha = safe_git_commit(root, "feat(f01): integrate independent QA3 verified changes")
            push_whitelisted(root, PHASE)
            history.append({"stage": "E06-E07", "commit": final_sha,
                            "local_tests_passed": True})
            break
    else:
        raise Blocked("FAILED_TECHNICAL", "Integração ou regressão sem aprovação local")
    rc, chk = exec_command([sys.executable, "scripts/f01_release_gate.py",
                            "--check-release"], root)
    outcome = ("READY_FOR_EXTERNAL_VERIFICATION" if rc != 0
               else "PENDING_FORMAL_CI_AND_PROFESSIONAL_SIGNOFF")
    history.append({"stage": "E08", "guard_exit": rc,
                    "guard_result": chk[-3000:],
                    "ci_same_sha_verified": False,
                    "normative_external_signoff_verified": False,
                    "f02_started": False})
    return {"outcome": outcome, "branch": PHASE, "commit": final_sha,
            "logs": str(logdir), "agent_results": [vars(x) for x in by_id.values()],
            "history": history, "f00_reopened": False, "f02_started": False,
            "push_performed": True, "merge_performed": False,
            "note": "Somente branches QA/F01 atualizadas; CI no SHA final e evidências normativas externas ainda devem ser verificadas."}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true",
                        help="Iniciar trabalho YOLO somente em sandbox com Copilot autenticado")
    parser.add_argument("--sandbox-confirmed", action="store_true",
                        help="Confirmar previamente que a VM/container descartável não contém secrets")
    args = parser.parse_args(argv)
    try:
        if not args.execute:
            print(json.dumps(planned_tasks(), indent=2, ensure_ascii=False))
            return 0
        if not args.sandbox_confirmed:
            raise Blocked("BLOCKED_SECURITY",
                          "YOLO requer confirmação inicial de sandbox isolado")
        result = run(ROOT, args)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["outcome"].startswith("READY_FOR_") else 1
    except Blocked as exc:
        print(json.dumps({"outcome": exc.code, "reason": str(exc),
                          "f00_reopened": False, "f02_started": False},
                         ensure_ascii=False, indent=2), file=sys.stderr)
        return 2
    except Exception:
        traceback.print_exc()
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
