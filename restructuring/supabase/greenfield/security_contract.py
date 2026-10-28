"""Conservative GF02 client-access contract used for development-only tests.

Not a replacement for PostgreSQL row-level security, real Auth or backend checks.
"""
from __future__ import annotations

from typing import Iterable

CLIENT_INSERT_COLUMNS = {
    "sie_projects": frozenset({"name", "owner_id"}),
    "sie_project_revisions": frozenset({"project_id", "version", "source_sha256"}),
    "sie_rooms": frozenset({"project_id", "revision_id", "name", "width_m", "length_m", "excluded_perimeter_m"}),
    "sie_loads": frozenset({"project_id", "revision_id", "room_id", "label", "kind", "apparent_power_va", "quantity"}),
    "sie_circuits": frozenset({"project_id", "revision_id", "code", "nominal_voltage_v"}),
    "sie_circuit_loads": frozenset({"project_id", "revision_id", "circuit_id", "load_id"}),
}
CLIENT_SELECT_TABLES = frozenset(CLIENT_INSERT_COLUMNS) | frozenset(
    {"sie_calculation_runs", "sie_artifacts", "sie_audit_events"})
CLIENT_UPDATE_COLUMNS = {"sie_projects": frozenset({"name"})}


class ClientAccessDenied(PermissionError):
    """A browser action not authorized by the GF02 development contract."""


def require_owner(subject_id: str | None, project_owner_id: str | None) -> None:
    """IDs must come from verified JWT and trusted DB row, not request metadata."""
    if not subject_id or not isinstance(subject_id, str) or not project_owner_id:
        raise ClientAccessDenied("authenticated identity and project owner required")
    if subject_id != project_owner_id:
        raise ClientAccessDenied("cross-owner access denied")


def require_client_action(
    subject_id: str | None,
    project_owner_id: str | None,
    table: str,
    operation: str,
    columns: Iterable[str] = (),
) -> None:
    """Static least-privilege check; real persistence must still enforce SQL RLS."""
    require_owner(subject_id, project_owner_id)
    requested = frozenset(columns)
    if table not in CLIENT_SELECT_TABLES:
        raise ClientAccessDenied("unknown or unexposed application table")
    if operation == "SELECT" and not requested:
        return
    if operation == "INSERT" and requested and requested <= CLIENT_INSERT_COLUMNS.get(table, frozenset()):
        return
    if operation == "UPDATE" and requested and requested <= CLIENT_UPDATE_COLUMNS.get(table, frozenset()):
        return
    raise ClientAccessDenied("client operation not permitted by GF02 grant contract")
