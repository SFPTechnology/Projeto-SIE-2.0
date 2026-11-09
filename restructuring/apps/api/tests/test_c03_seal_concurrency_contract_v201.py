"""Guard against C03 electrical writes racing the A04 seal transaction.

This static contract complements PostgreSQL 17 isolated schema tests. It does
not claim real concurrent transaction verification or normative approval.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
MIGRATIONS = ROOT / "restructuring/supabase/migrations"


def test_c03_draft_guard_serializes_with_a04_seal_lock():
    a04 = (MIGRATIONS / "20261028102100_sie_a04_revision_lifecycle_v201.sql").read_text()
    c03 = (MIGRATIONS / "20261028203000_sie_c03_electrical_domain_v201.sql").read_text()
    assert "CREATE FUNCTION public.sie_a04_guard_revision_write()" in a04
    assert "CREATE FUNCTION public.sie_c03_guard_revision_edit()" in c03
    lock = "pg_catalog.hashtextextended("
    assert a04.count(lock) >= 2
    assert c03.count(lock) >= 1
    guard = c03.split("CREATE FUNCTION public.sie_c03_guard_revision_edit()", 1)[1].split("END $fn$;", 1)[0]
    assert "pg_catalog.pg_advisory_xact_lock(" in guard
    assert "pg_catalog.hashtextextended(r::text, 20261028)" in guard
    assert guard.index("pg_catalog.pg_advisory_xact_lock(") < guard.index("SELECT lifecycle_state INTO state")
    assert "state <> 'DRAFT'" in guard


def test_c03_guard_applies_to_all_nine_revision_child_tables():
    c03 = (MIGRATIONS / "20261028203000_sie_c03_electrical_domain_v201.sql").read_text()
    for name in (
        "sie_panels", "sie_feeders", "sie_circuit_technical",
        "sie_room_benches", "sie_floorplans", "sie_floorplan_vertices",
        "sie_graphical_bindings", "sie_legacy_results", "sie_distributor_overrides",
    ):
        assert "'" + name + "'" in c03
    assert "BEFORE INSERT OR UPDATE OR DELETE" in c03
    assert "EXECUTE FUNCTION public.sie_c03_guard_revision_edit()" in c03
