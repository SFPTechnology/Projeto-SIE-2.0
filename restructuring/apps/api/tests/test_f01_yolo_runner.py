"""F01 YOLO planner: dry run, source preservation and bounded activation."""
import importlib.util
import json
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[4]
spec = importlib.util.spec_from_file_location(
    "f01_yolo_runner", ROOT / "scripts" / "f01_yolo_runner.py")
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)


def test_planner_is_dry_run_and_keeps_f00_done_f01_blocked():
    preview = mod.planned_tasks(ROOT)
    assert preview["mode"] == "DRY_RUN"
    assert preview["f00"] == "DONE"
    assert preview["f01"] == "BLOCKED"
    assert preview["f02"] is False
    assert preview["agent_sessions_started"] == 0
    assert preview["gates_accepted"] == 0
    assert len(preview["workstreams"]) == 3


def test_yolo_must_have_sandbox_confirmation(capsys):
    assert mod.main(["--execute"]) == 2
    assert "BLOCKED_SECURITY" in capsys.readouterr().err


def test_no_execution_in_default_invocation(capsys, monkeypatch):
    def fail(*args, **kwargs):
        raise AssertionError("dry run must not invoke Git or Copilot")
    monkeypatch.setattr(mod, "exec_command", fail)
    assert mod.main([]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["mode"] == "DRY_RUN"


@pytest.mark.parametrize("changed", [
    "?? .env",
    " M docs/implantacao-sie-2-0/F00/RELATORIO_EXECUCAO.md",
    " M docs/sie-orchestrator/ORCHESTRATOR_STATE.json",
    " M docs/implantacao-sie-2-0/F01/QA3_MANIFEST.json",
    "?? api/prod-database.db",
    " M .github/workflows/sie-restructuring-api.yml",
])
def test_forbidden_modifications_fail_closed(monkeypatch, tmp_path, changed):
    monkeypatch.setattr(mod, "exec_command", lambda *args, **kwargs: (0, changed + "\n"))
    with pytest.raises(mod.Blocked, match="sensíveis"):
        mod.assert_allowed(tmp_path)


def test_code_changes_within_f01_workstream_are_allowed(monkeypatch, tmp_path):
    monkeypatch.setattr(mod, "exec_command", lambda *args, **kwargs: (
        0, " M restructuring/apps/api/sie_api/storage.py\n"
           "?? docs/implantacao-sie-2-0/F01/qa3-runs/QA-01/PARECER_QA.md\n"))
    found = mod.assert_allowed(tmp_path)
    assert len(found) == 2


def test_missing_first_pass_report_blocks_cross_review(tmp_path):
    assert set(mod.reports_present(tmp_path, "QA-01")) == {
        "PLANO_E_EXECUCAO.md", "MATRIZ_6_GATES.json", "PARECER_QA.md"}


def test_runner_never_commits_when_forbidden_changed(monkeypatch, tmp_path):
    called = []
    def fake(args, *rest, **kw):
        called.append(args)
        return 0, " M scripts/f00_golden.py\n"
    monkeypatch.setattr(mod, "exec_command", fake)
    with pytest.raises(mod.Blocked):
        mod.safe_git_commit(tmp_path, "attempt")
    assert not any("commit" in a for a in called)


def test_qa_branch_synchronization_fast_forward_only(monkeypatch, tmp_path):
    old = "a" * 40
    new = "b" * 40
    commands = []
    def fake_need(cmd, cwd, **kwargs):
        commands.append(cmd)
        if cmd[:3] == ["git", "branch", "--show-current"]:
            return "qa/f01-arquiteto"
        if cmd == ["git", "status", "--porcelain"]:
            return ""
        if cmd == ["git", "rev-parse", "HEAD"]:
            return new if any(c[:3] == ["git", "merge", "--ff-only"] for c in commands) else old
        return ""
    monkeypatch.setattr(mod, "need", fake_need)
    monkeypatch.setattr(mod, "exec_command", lambda *a, **kw: (0, ""))
    published = []
    monkeypatch.setattr(mod, "push_whitelisted",
                        lambda wt, br: published.append((wt, br)))
    assert mod.synchronize_qa_branch(
        tmp_path, tmp_path, "qa/f01-arquiteto", new
    ) == new
    assert ["git", "merge", "--ff-only", new] in commands
    assert len(published) == 1


def test_qa_branch_divergence_blocks_instead_of_force_push(monkeypatch, tmp_path):
    monkeypatch.setattr(
        mod, "need", lambda cmd, cwd, **kw:
        "qa/f01-arquiteto" if cmd[:3] == ["git", "branch", "--show-current"]
        else "a" * 40 if cmd == ["git", "rev-parse", "HEAD"]
        else "")
    monkeypatch.setattr(mod, "exec_command", lambda *a, **kw: (1, ""))
    monkeypatch.setattr(mod, "push_whitelisted",
                        lambda *a, **kw: pytest.fail("must not publish divergent branch"))
    with pytest.raises(mod.Blocked, match="ancestral"):
        mod.synchronize_qa_branch(tmp_path, tmp_path, "qa/f01-arquiteto", "b" * 40)


def test_synchronization_rejects_main_even_when_head_equal(monkeypatch, tmp_path):
    with pytest.raises(mod.Blocked, match="whitelist"):
        mod.synchronize_qa_branch(tmp_path, tmp_path, "main", "b" * 40)
