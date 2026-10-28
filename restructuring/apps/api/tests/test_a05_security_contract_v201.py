"""Owner-only negative tests for development; NOT live Supabase Auth/RLS tests."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[4]
MODULE = ROOT / "restructuring" / "supabase" / "greenfield" / "security_contract.py"
spec = importlib.util.spec_from_file_location("sie2_v201_security_contract", MODULE)
assert spec is not None and spec.loader is not None
contract = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = contract
spec.loader.exec_module(contract)


def test_owner_can_read_owned_project():
    contract.require_client_action("A", "A", "sie_projects", "SELECT")


@pytest.mark.parametrize("subject,owner", [("B", "A"), (None, "A"), ("A", None), ("", "A")])
def test_foreign_or_anonymous_identity_denied(subject, owner):
    with pytest.raises(contract.ClientAccessDenied):
        contract.require_client_action(subject, owner, "sie_projects", "SELECT")


def test_client_may_insert_only_gf02_allowed_columns():
    contract.require_client_action("A", "A", "sie_rooms", "INSERT",
                                   {"project_id", "revision_id", "name", "width_m", "length_m"})
    with pytest.raises(contract.ClientAccessDenied):
        contract.require_client_action("A", "A", "sie_rooms", "INSERT", {"service_role_key"})


@pytest.mark.parametrize("table", ["sie_calculation_runs", "sie_artifacts", "sie_audit_events"])
def test_browser_cannot_create_server_origin_data(table):
    with pytest.raises(contract.ClientAccessDenied):
        contract.require_client_action("A", "A", table, "INSERT", {"project_id"})


def test_browser_cannot_change_owner_or_delete():
    with pytest.raises(contract.ClientAccessDenied):
        contract.require_client_action("A", "A", "sie_projects", "UPDATE", {"owner_id"})
    with pytest.raises(contract.ClientAccessDenied):
        contract.require_client_action("A", "A", "sie_projects", "DELETE")


def test_only_project_name_is_mutable_by_browser():
    contract.require_client_action("A", "A", "sie_projects", "UPDATE", {"name"})


def test_unknown_table_not_granted():
    with pytest.raises(contract.ClientAccessDenied):
        contract.require_client_action("A", "A", "secrets", "SELECT")
