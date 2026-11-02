"""Five-project *synthetic shape* rehearsal on isolated disposable PG17 only.

Counts reproduce the declared structure of the five legacy projects, not the
real records, audit trail, 99-column inventory or professional verification.
The project names and test owners are generated placeholders. No source
Supabase data are read or migrated by this suite.
"""
from __future__ import annotations
import os
from uuid import UUID
import pytest
from sie_api.v201_pg_dev_adapter import Pg17DisposableAdapter, PgMissing

pytestmark=pytest.mark.skipif(
    os.environ.get("SIE_PG17_DISPOSABLE_TEST") != "1",
    reason="No remote DB; PostgreSQL 17 Docker service in CI only",
)
OWNER = UUID("11111111-1111-4111-8111-111111111111")
OTHER = UUID("22222222-2222-4222-8222-222222222222")
PROJECT_SHAPES = ((15, 18), (9, 13), (4, 3), (12, 17), (1, 1))


def _pg():
    import psycopg
    return psycopg.connect(
        "host=localhost port=5432 dbname=sie2_gf02_ci "
        "user=postgres password=postgres_ci_only connect_timeout=5",
        autocommit=True,
    )


def _bundle(rooms, loads):
    assert rooms >= 1
    return {
        "rooms": [
            {"ref": f"r{i}", "name": f"Ambiente sintético {i}",
             "width_m": "4.0000", "length_m": "5.0000"}
            for i in range(rooms)
        ],
        "circuits": [
            {"ref": "c1", "code": "C1", "nominal_voltage_v": "220.000"}
        ],
        "loads": [
            {"ref": f"l{i}", "room_ref": f"r{i % rooms}",
             "label": f"Carga sintética {i}", "kind": "TUE",
             "apparent_power_va": "100.000"}
            for i in range(loads)
        ],
        "links": [
            {"circuit_ref": "c1", "load_ref": f"l{i}"}
            for i in range(loads)
        ],
    }


def test_five_project_shape_rehearsal_and_isolation():
    with _pg() as conn:
        adapter = Pg17DisposableAdapter(conn)
        ids = []
        for i, (rooms, loads) in enumerate(PROJECT_SHAPES, 1):
            key = f"c08-isolated-five-project-{i}"
            project = adapter.create_project(OWNER, f"C08 synthetic {i}", key)
            replay = adapter.create_project(OWNER, f"C08 synthetic {i}", key)
            assert replay["id"] == project["id"]
            assert replay["replayed"] is True
            pid = project["id"]
            ids.append(pid)
            revision = adapter.create_revision(
                OWNER, pid, f"c08-synthetic-revision-{i}"
            )["id"]
            result = adapter.add_bundle(
                OWNER, pid, revision, _bundle(rooms, loads)
            )
            assert result == {
                "rooms": rooms, "loads": loads, "circuits": 1, "links": loads,
            }
            with pytest.raises(PgMissing):
                adapter.create_revision(OTHER, pid, f"c08-forbidden-{i}")
            seal = adapter.seal(OWNER, pid, revision, 0)
            assert seal["state"] == "SEALED"
            assert len(seal["snapshot_sha256"]) == 64

        assert len(set(ids)) == 5
        assert sum(r for r, _ in PROJECT_SHAPES) == 41
        assert sum(l for _, l in PROJECT_SHAPES) == 52
        with conn.cursor() as cur:
            cur.execute(
                """SELECT
                       (SELECT count(*) FROM public.sie_rooms WHERE project_id=ANY(%s::uuid[])),
                       (SELECT count(*) FROM public.sie_loads WHERE project_id=ANY(%s::uuid[])),
                       (SELECT count(*) FROM public.sie_circuit_loads WHERE project_id=ANY(%s::uuid[])),
                       (SELECT count(*) FROM public.sie_project_revisions WHERE project_id=ANY(%s::uuid[])
                """, (ids, ids, ids, ids)
            )
            assert cur.fetchone() == (41, 52, 52, 5)


def test_five_project_bundle_invalid_link_rolls_back():
    with _pg() as conn:
        adapter = Pg17DisposableAdapter(conn)
        p = adapter.create_project(
            OWNER, "C08 negative synthetic", "c08-negative-create-01"
        )["id"]
        r = adapter.create_revision(
            OWNER, p, "c08-negative-revision"
        )["id"]
        b = _bundle(1, 1)
        b["links"][0]["load_ref"] = "nonexistent"
        with pytest.raises(Exception):
            adapter.add_bundle(OWNER, p, r, b)
        with conn.cursor() as cur:
            cur.execute(
                "SELECT count(*) FROM public.sie_rooms WHERE project_id=%s",
                (p,)
            )
            assert cur.fetchone()[0] == 0
