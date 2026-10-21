import sqlite3
from uuid import uuid4
import pytest
from fastapi.testclient import TestClient
from sie_api.storage import RepositorioProjetos, ConflitoRevisao
from sie_api.data_lifecycle import migrate, copy_database
from sie_api.main import app


def test_upgrade_downgrade_and_restore(tmp_path):
    path = tmp_path/'source.db'
    repo = RepositorioProjetos(path)
    pid = str(uuid4())
    data = {'precisao': '0.123456789012345678901234567890'}
    repo.salvar(pid, 'Projeto', data, 0)
    with sqlite3.connect(path) as db:
        migrate(db, 0)
        assert db.execute('SELECT dados_json FROM projetos').fetchone()
        migrate(db, 1)
        assert db.execute('SELECT criado_em FROM projetos').fetchone()[0]
    backup = copy_database(path, tmp_path/'backup.db')
    restored = copy_database(backup, tmp_path/'restored.db')
    assert RepositorioProjetos(restored).carregar_revisao(pid, 1)['dados'] == data
    with pytest.raises(FileExistsError):
        copy_database(path, restored)
    assert restored.stat().st_mode & 0o077 == 0


def test_atomic_incomplete_migration(tmp_path):
    path = tmp_path/'db'
    RepositorioProjetos(path)
    with sqlite3.connect(path) as db:
        migrate(db, 0)
        db.execute('ALTER TABLE projetos ADD COLUMN excluido_em TEXT')
        db.commit()
        with pytest.raises(sqlite3.OperationalError):
            migrate(db)
        assert 'criado_em' not in [r[1] for r in db.execute('PRAGMA table_info(projetos)')]


def test_archive_conflict_and_preserved_history(tmp_path):
    repo = RepositorioProjetos(tmp_path/'db')
    pid = str(uuid4())
    repo.salvar(pid, 'Projeto', {}, 0)
    repo.arquivar(pid, 1)
    assert repo.carregar(pid) is None
    assert repo.carregar_revisao(pid, 1)['dados'] == {}
    with pytest.raises(ConflitoRevisao):
        repo.salvar(pid, 'Projeto', {}, 2)
    with repo._conectar() as db:
        with pytest.raises(ValueError):
            migrate(db, 0)


def test_corrupt_backup_fails_without_output(tmp_path):
    source = tmp_path/'bad'
    source.write_bytes(b'corrupted sqlite')
    with pytest.raises(sqlite3.DatabaseError):
        copy_database(source, tmp_path/'output')
    assert not (tmp_path/'output').exists()


@pytest.mark.parametrize('peer', ['203.0.113.2', '10.0.0.1'])
def test_external_peer_rejected(peer, monkeypatch):
    monkeypatch.setenv('SIE_ENV', 'test')
    with TestClient(app, client=(peer, 50000)) as client:
        assert client.get('/api/v1/local/projetos/'+str(uuid4()), headers={'X-Forwarded-For':'127.0.0.1'}).status_code == 403


def test_production_disabled(monkeypatch):
    monkeypatch.setenv('SIE_ENV', 'prod')
    with TestClient(app) as client:
        assert client.get('/api/v1/local/projetos/'+str(uuid4())).status_code == 503


def test_migration_keeps_normative_bytes_and_legacy_author_unknown(tmp_path):
    path = tmp_path/'legacy.db'
    repo = RepositorioProjetos(path)
    pid = str(uuid4())
    repo.salvar(pid, 'Projeto', {'circuitos': []}, 0)
    with sqlite3.connect(path) as db:
        before = db.execute('SELECT * FROM snapshots_normativos').fetchall()
        migrate(db, 0)
        migrate(db, 1)
        assert db.execute('SELECT * FROM snapshots_normativos').fetchall() == before
        assert db.execute('SELECT autor FROM eventos_auditoria').fetchone()[0] == 'LEGACY_UNKNOWN'
    repo.salvar(pid, 'Projeto', {}, 1)
    with sqlite3.connect(path) as db:
        assert db.execute('SELECT autor FROM eventos_auditoria ORDER BY id DESC').fetchone()[0] == 'LOCAL_OWNER'
        with pytest.raises(sqlite3.IntegrityError):
            db.execute("UPDATE snapshots_normativos SET status='APROVADO'")
    restored = copy_database(path, tmp_path/'restored.db')
    with sqlite3.connect(restored) as db:
        assert db.execute('SELECT * FROM snapshots_normativos WHERE revisao_projeto=1').fetchall() == before


def test_failed_archive_has_no_partial_changes(tmp_path):
    path = tmp_path/'db'
    repo = RepositorioProjetos(path)
    pid = str(uuid4())
    repo.salvar(pid, 'Projeto', {}, 0)
    with pytest.raises(ConflitoRevisao):
        repo.arquivar(pid, 2)
    assert repo.carregar(pid)['revisao'] == 1
    assert len(repo.historico(pid)) == 1


def test_database_permissions_private_on_creation_existing_mode_preserved(tmp_path):
    path = tmp_path/'private.db'
    RepositorioProjetos(path)
    assert path.stat().st_mode & 0o077 == 0
    path.chmod(0o640)
    RepositorioProjetos(path)
    assert path.stat().st_mode & 0o777 == 0o640


def test_locked_database_fails_without_overwrite(tmp_path):
    path = tmp_path/'locked.db'
    repo = RepositorioProjetos(path)
    pid = str(uuid4())
    repo.salvar(pid, 'Original', {}, 0)
    with sqlite3.connect(path) as lock:
        lock.execute('BEGIN IMMEDIATE')
        with pytest.raises(sqlite3.OperationalError, match='locked'):
            repo.salvar(pid, 'Nao gravado', {}, 1)
        lock.rollback()
    assert repo.carregar(pid)['nome'] == 'Original'
    assert repo.carregar(pid)['revisao'] == 1
    assert len(repo.historico(pid)) == 1


def test_corrupt_database_api_returns_sanitized_failure(tmp_path, monkeypatch):
    path = tmp_path/'sensitive-private-path.db'
    path.write_bytes(b'corrupt')
    token = 'f03-private-test-only-token-value'
    monkeypatch.setenv('SIE_LOCAL_DB_PATH', str(path))
    monkeypatch.setenv('SIE_LOCAL_API_TOKEN', token)
    monkeypatch.setenv('SIE_ENV', 'test')
    with TestClient(app) as client:
        response = client.get('/api/v1/local/projetos/'+str(uuid4()),
                              headers={'Authorization': 'Bearer '+token})
    assert response.status_code == 503
    assert str(path) not in response.text
    assert token not in response.text
    assert path.read_bytes() == b'corrupt'
