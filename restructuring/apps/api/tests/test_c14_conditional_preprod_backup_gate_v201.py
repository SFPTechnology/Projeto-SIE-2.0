"""C14 enforce conditional authorization: neither code nor documentation can grant unsafe remote GO."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[4]
CONTRACT = ROOT / "docs/implantacao-sie-2-0/GREENFIELD/C08_CONTRATO_ENTREGA_C_V201.json"
RUNBOOK = ROOT / "docs/implantacao-sie-2-0/GREENFIELD/C14_PREVOO_BACKUP_RESTORE_PREPROD_20261102.md"
SCRIPT = ROOT / "scripts/c14_backup_preprod_sie2.ps1"

def test_explicit_scope_does_not_bypass_real_backup_and_restore():
    doc = json.loads(CONTRACT.read_text(encoding="utf-8"))
    auth = doc["preproduction_authorization"]
    assert auth["received_on"] == "2026-11-02"
    assert auth["project_ref"] == "fozrymsidnaxmuvxxfhh"
    assert auth["migration_application_approved_conditionally"] is True
    assert auth["migration_application_permitted_now"] is False
    assert auth["legacy_import_permitted_now"] is False
    assert doc["remote_ddl_authorized"] is False
    assert doc["state"] == "BLOCKED"
    assert auth["backup_real_state"] == "MISSING"
    assert auth["restore_real_state"] == "MISSING"
    assert auth["zero_additional_cost_required"] is True
    assert "LOCAL_FULL_RESTORE_WITH_CONTENT_AND_SCHEMA_CHECKS_PASS" in auth["mandatory_preconditions"]

def test_private_windows_backup_does_only_readonly_dumps():
    source = SCRIPT.read_text(encoding="utf-8")
    assert "fozrymsidnaxmuvxxfhh" in source
    assert "supabase link --project-ref $expectedRef" in source
    assert "supabase db dump" in source
    assert "restore_state = 'NOT_VERIFIED'" in source
    assert "migration_go = $false" in source
    assert "Get-FileHash" in source
    assert "OneDrive" in source and ".git" in source
    for forbidden in ("supabase db push", "supabase db reset", "supabase db repair",
                      "supabase migration up", "apply_migration", "DROP DATABASE"):
        assert forbidden not in source
    assert RUNBOOK.exists()
