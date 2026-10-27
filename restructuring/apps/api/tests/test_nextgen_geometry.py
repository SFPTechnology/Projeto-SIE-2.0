"""Greenfield geometry contract tests: no Supabase or electrical approval."""
import json
import subprocess
import sys
from decimal import Decimal
from pathlib import Path
from uuid import UUID
import pytest
from sie_api.nextgen_geometry import GeometryError, analyze_project

P = str(UUID("aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"))
V = str(UUID("bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"))
R = str(UUID("cccccccc-cccc-4ccc-8ccc-cccccccccccc"))
R2 = str(UUID("dddddddd-dddd-4ddd-8ddd-dddddddddddd"))

def base():
    return {"project_id": P, "revision_id": V, "rooms": [
        {"room_id": R, "name": " Sala ", "width_m": "3.2", "length_m": "4.1",
         "excluded_perimeter_m": "1.5"}]}

def test_geometry_area_perimeter_and_non_normative_status():
    result = analyze_project(base())
    assert result["rooms"] == [{"room_id": R, "name": "Sala", "area_m2": "13.12",
                                "gross_perimeter_m": "14.6", "useful_perimeter_m": "13.1"}]
    assert result["normative_status"] == "NOT_EVALUATED"
    assert result["geometry_assumption"] == "rectangular_only"
    assert len(result["source_sha256"]) == 64

def test_semantically_equivalent_decimals_hash_equally():
    p = base()
    q = base()
    q["rooms"][0]["width_m"] = Decimal("3.2000")
    assert analyze_project(p)["source_sha256"] == analyze_project(q)["source_sha256"]

def test_revision_change_changes_hash():
    q = base()
    q["revision_id"] = R2
    assert analyze_project(q)["source_sha256"] != analyze_project(base())["source_sha256"]

def test_input_not_mutated():
    p = base()
    before = json.dumps(p)
    analyze_project(p)
    assert json.dumps(p) == before

@pytest.mark.parametrize("bad", ["0", "-1", "NaN", "Infinity", True, None, []])
def test_bad_dimensions_rejected(bad):
    p = base()
    p["rooms"][0]["width_m"] = bad
    with pytest.raises(GeometryError):
        analyze_project(p)

@pytest.mark.parametrize("excluded", ["-1", "14.6", "14.61", "Infinity"])
def test_invalid_exclusion_rejected(excluded):
    p = base()
    p["rooms"][0]["excluded_perimeter_m"] = excluded
    with pytest.raises(GeometryError):
        analyze_project(p)

def test_duplicate_room_rejected():
    p = base()
    p["rooms"].append(dict(p["rooms"][0]))
    with pytest.raises(GeometryError, match="duplicado"):
        analyze_project(p)

def test_unknown_field_rejected():
    p = base()
    p["rooms"][0]["normative_approved"] = True
    with pytest.raises(GeometryError, match="desconhecidos"):
        analyze_project(p)

def test_missing_revision_rejected():
    p = base()
    del p["revision_id"]
    with pytest.raises(GeometryError):
        analyze_project(p)

def test_empty_and_oversized_project_rejected():
    p = base()
    p["rooms"] = []
    with pytest.raises(GeometryError):
        analyze_project(p)
    p["rooms"] = [dict(base()["rooms"][0], room_id=str(UUID(int=i + 1))) for i in range(501)]
    with pytest.raises(GeometryError):
        analyze_project(p)

def test_multiple_rooms():
    p = base()
    p["rooms"].append({"room_id": R2, "name": "Banheiro", "width_m": 2,
                       "length_m": 3})
    assert len(analyze_project(p)["rooms"]) == 2
    assert analyze_project(p)["rooms"][1]["useful_perimeter_m"] == "10"

def test_cli_success(tmp_path: Path):
    source = tmp_path / "in.json"
    source.write_text(json.dumps(base()), encoding="utf-8")
    run = subprocess.run([sys.executable, "-m", "sie_api.nextgen_geometry_cli", "--input", str(source)],
                         capture_output=True, text=True, check=False)
    assert run.returncode == 0, run.stderr
    assert json.loads(run.stdout)["rooms"][0]["area_m2"] == "13.12"

def test_cli_error_no_success_output(tmp_path: Path):
    source = tmp_path / "in.json"
    source.write_text('{"broken":', encoding="utf-8")
    run = subprocess.run([sys.executable, "-m", "sie_api.nextgen_geometry_cli", "--input", str(source)],
                         capture_output=True, text=True, check=False)
    assert run.returncode == 2
    assert not run.stdout
    assert "error" in json.loads(run.stderr)
