"""End-to-end subprocess tests of the offline CLI."""
import json
import subprocess
import sys
from uuid import UUID


def invoke(db, *args):
    return subprocess.run(
        [sys.executable, "-m", "sie_api.cli", "--database", str(db), *args],
        capture_output=True,
        text=True,
        check=False,
        timeout=15,
    )


def test_cli_help_does_not_require_database():
    run = subprocess.run(
        [sys.executable, "-m", "sie_api.cli", "--help"],
        capture_output=True, text=True, check=False, timeout=15,
    )
    assert run.returncode == 0
    assert "salvar" in run.stdout
    assert "carregar" in run.stdout
    assert "historico" in run.stdout


def test_cli_save_load_update_and_audit(tmp_path):
    db = tmp_path / "sie-local.sqlite3"
    source = tmp_path / "project.json"
    source.write_text('{"circuitos":[{"nome":"TUG-1"}]}', encoding="utf-8")
    created = invoke(db, "salvar", "--nome", "Casa", "--arquivo", str(source))
    assert created.returncode == 0, created.stderr
    first = json.loads(created.stdout)
    UUID(first["id"])
    assert first["revisao"] == 1
    loaded = invoke(db, "carregar", "--id", first["id"])
    assert loaded.returncode == 0
    assert json.loads(loaded.stdout)["dados"]["circuitos"][0]["nome"] == "TUG-1"

    source.write_text('{"circuitos":[]}', encoding="utf-8")
    updated = invoke(
        db, "salvar", "--id", first["id"], "--nome", "Casa 2",
        "--arquivo", str(source), "--revisao-esperada", "1",
    )
    assert updated.returncode == 0, updated.stderr
    assert json.loads(updated.stdout)["revisao"] == 2
    audit = invoke(db, "historico", "--id", first["id"])
    assert audit.returncode == 0
    assert [e["acao"] for e in json.loads(audit.stdout)["eventos"]] == ["CRIAR", "ATUALIZAR"]


def test_cli_conflict_preserves_existing_revision(tmp_path):
    db = tmp_path / "sie-local.sqlite3"
    source = tmp_path / "project.json"
    source.write_text("{}", encoding="utf-8")
    created = invoke(db, "salvar", "--nome", "Casa", "--arquivo", str(source))
    identifier = json.loads(created.stdout)["id"]
    conflict = invoke(
        db, "salvar", "--id", identifier,
        "--nome", "Tentativa antiga", "--arquivo", str(source),
        "--revisao-esperada", "0",
    )
    assert conflict.returncode == 4
    assert "Conflito de revisao" in conflict.stderr
    loaded = invoke(db, "carregar", "--id", identifier)
    assert json.loads(loaded.stdout)["nome"] == "Casa"
    assert json.loads(loaded.stdout)["revisao"] == 1


def test_cli_missing_project(tmp_path):
    from uuid import uuid4
    run = invoke(tmp_path / "db.sqlite3", "carregar", "--id", str(uuid4()))
    assert run.returncode == 3
    assert "nao encontrado" in run.stderr


def test_cli_rejects_non_object_json(tmp_path):
    db = tmp_path / "db.sqlite3"
    source = tmp_path / "invalid.json"
    source.write_text("[1, 2]", encoding="utf-8")
    run = invoke(db, "salvar", "--nome", "Casa", "--arquivo", str(source))
    assert run.returncode == 2
    assert "objeto JSON" in run.stderr


def test_cli_rejects_nonfinite_json(tmp_path):
    db = tmp_path / "db.sqlite3"
    source = tmp_path / "invalid.json"
    source.write_text('{"a":NaN}', encoding="utf-8")
    run = invoke(db, "salvar", "--nome", "Casa", "--arquivo", str(source))
    assert run.returncode == 2
    assert "nao permitido" in run.stderr


def test_cli_rejects_oversize_input(tmp_path):
    db = tmp_path / "db.sqlite3"
    source = tmp_path / "large.json"
    source.write_text('{"a":"' + "x" * 1_048_576 + '"}', encoding="utf-8")
    run = invoke(db, "salvar", "--nome", "Casa", "--arquivo", str(source))
    assert run.returncode == 2
    assert "1 MiB" in run.stderr


def test_cli_requires_database_file(tmp_path):
    source = tmp_path / "project.json"
    source.write_text("{}", encoding="utf-8")
    run = subprocess.run(
        [sys.executable, "-m", "sie_api.cli", "--database", ":memory:",
         "salvar", "--nome", "Casa", "--arquivo", str(source)],
        capture_output=True, text=True, check=False, timeout=15,
    )
    assert run.returncode == 2
    assert "SQLite local persistente" in run.stderr
