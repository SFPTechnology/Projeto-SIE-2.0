"""B04/B05 PostgreSQL integration contract; read-only and DISABLED for writes.

No connection, env credential, migration, or Supabase remote SQL is performed here.
This checks the presence of GF02+A03+A04, then offers parameterized *reads*
to a trusted backend holding an injected, already-authorized PG connection.
The actual migration/DDL deployment and write adapter require separate approval.
"""
from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID


REQUIRED_MIGRATIONS=frozenset({
    "20261027195557",  # GF02 installed
    "20261028102000",  # A03 (currently PENDING)
    "20261028102100",  # A04 (currently PENDING)
})
PROJECT_REF="fozrymsidnaxmuvxxfhh"
REQUIRED_SCHEMA_COLUMNS=frozenset({
    "lifecycle_state","base_revision_id","lock_version",
    "idempotency_key","sealed_snapshot","sealed_snapshot_sha256"
})


class IntegrationNotReady(RuntimeError):
    pass


@dataclass(frozen=True)
class PgReadiness:
    current_project: str
    versions: tuple[str, ...]
    missing: tuple[str, ...]
    ready: bool


def read_only_preflight(conn, project_ref: str) -> PgReadiness:
    """Check schema history and revision columns without writing remote state."""
    if project_ref != PROJECT_REF:
        raise IntegrationNotReady("wrong target Supabase project")
    with conn.cursor() as cur:
        cur.execute("SELECT version FROM supabase_migrations.schema_migrations")
        versions={str(row[0]) for row in cur.fetchall()}
        cur.execute("""SELECT column_name FROM information_schema.columns
                       WHERE table_schema='public'
                       AND table_name='sie_project_revisions'""")
        columns={str(row[0]) for row in cur.fetchall()}
        missing=sorted(REQUIRED_MIGRATIONS - versions)
        if not REQUIRED_SCHEMA_COLUMNS<=columns:
            missing.append("sie_project_revisions.columns")
    return PgReadiness(project_ref,tuple(sorted(versions)),tuple(missing),
                       not missing)


def list_owned_projects(conn, project_ref: str, owner_id: UUID):
    """Read-only backend query, with ownership even if service role bypasses RLS.

    conn is INJECTED from a trusted backend. No connection-string parsing
    or automatic service_role selection is permitted in this module.
    """
    ready=read_only_preflight(conn,project_ref)
    if not ready.ready:
        raise IntegrationNotReady(
            "A03/A04 not installed; backend integration remains disabled")
    user=str(UUID(str(owner_id)))
    with conn.cursor() as cur:
        cur.execute("""SELECT id,owner_id,name,created_at
                    FROM public.sie_projects
                    WHERE owner_id=%s ORDER BY created_at DESC LIMIT %s""",
                    (user,100))
        result=cur.fetchall()
    for row in result:
        if str(row[1])!=user:
            raise IntegrationNotReady("ownership mismatch from DB")
    return [{"id":str(r[0]),"name":r[2],"created_at":str(r[3])} for r in result]


def deny_remote_write(*_args, **_kwargs):
    """Remote writes must not be enabled by code alone."""
    raise IntegrationNotReady(
        "remote PostgreSQL writes need approved migrations, readback, "
        "authenticated ownership and separate DDL authorization")
