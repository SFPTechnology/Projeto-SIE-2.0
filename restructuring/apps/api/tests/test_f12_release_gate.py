"""F12 release preparation controls never grant production authorization."""
import importlib.util
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[4]
SPEC = importlib.util.spec_from_file_location("f12_release_gate", ROOT / "scripts/f12_release_gate.py")
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)

F11 = {"tasks": [{"id": "F11", "state": "DONE", "checkpoint": {"professional_approval": False}}]}


def candidate():
    return {"schema": "sie-f12-preparation-1", "base_sha": gate.F11_SHA,
            "scope": "LOCAL_SOFTWARE_QA_PREPARATION_ONLY", "production_release_allowed": False,
            "professional_approval": False, "deployment_executed": False,
            "change_approved": False, "api_version": "0.1.0",
            "supported_candidate": "F11-local-QA", "backup_contract": "offline-multi-root",
            "tasks": {f"12.{n:02d}": "PENDENTE" for n in range(1, 11)}}


def test_candidate_metadata_only_is_consistent():
    assert gate.assess(candidate(), F11, gate.REQUIRED_DOCS) == []


def test_rejects_falsified_authorizations_and_professional_claims():
    for flag in ("production_release_allowed", "professional_approval",
                 "deployment_executed", "change_approved"):
        value = candidate()
        value[flag] = True
        assert any(flag in e for e in gate.assess(value, F11, gate.REQUIRED_DOCS))


def test_rejects_mismatched_handoff_and_closed_gate():
    value = candidate()
    value["base_sha"] = "0" * 40
    assert any("SHA F11" in e for e in gate.assess(value, F11, gate.REQUIRED_DOCS))
    assert any("F11 não está DONE" in e for e in gate.assess(candidate(),
               {"tasks": [{"id": "F11", "state": "BLOCKED"}]}, gate.REQUIRED_DOCS))


def test_rejects_missing_document_and_unverified_done():
    value = candidate()
    value["tasks"]["12.08"] = "DONE"
    errors = gate.assess(value, F11, gate.REQUIRED_DOCS[:-1])
    assert any("estado de task" in e for e in errors)
    assert any("documentos F12 ausentes" in e for e in errors)


def test_cli_denies_production_even_when_preparation_passes():
    command = [sys.executable, str(ROOT / "scripts/f12_release_gate.py"),
               "--root", str(ROOT), "--require-production"]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    assert result.returncode == 2
    assert '"production_authorized": false' in result.stdout
    assert "execução recusada" in result.stdout


def test_cli_preparation_is_read_only():
    command = [sys.executable, str(ROOT / "scripts/f12_release_gate.py"), "--root", str(ROOT), "--check"]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    assert result.returncode == 0, result.stdout + result.stderr
    assert '"status": "PREPARATION_VERIFIED_ONLY"' in result.stdout


def test_cannot_hide_changes_to_engine_or_production():
    changed = ["docs/implantacao-sie-2-0/F12/MANIFESTO_RELEASE.md",
               "restructuring/apps/api/sie_api/protection_f08.py",
               "supabase/migrations/unauthorized.sql",
               ".github/workflows/prod-deploy.yml"]
    assert gate.scope_violations(changed) == sorted(changed[1:])
    assert gate.scope_violations(["docs/stories/story-SIE-F12-LIBERACAO-CONTROLADA.md"]) == []
