"""Offline recovery of all registered F05/F10 roots, never a production restore."""

import os
from pathlib import Path
import sqlite3

import pytest
from fastapi.testclient import TestClient

from sie_api.local_bundle_backup_f11 import backup, restore, main
from sie_api.main import app
from test_artifacts_api_f10 import client_case


def _fixture(tmp_path, monkeypatch):
    client, base, body, auth = client_case(tmp_path, monkeypatch)
    assert client.post(base + '/execute', json=body, headers=auth).status_code == 200
    result = client.post(base + '/generate', json=body, headers=auth)
    assert result.status_code == 200, result.text
    return client, base, auth, result.json()['artifact_id'], Path(os.environ['SIE_LOCAL_DB_PATH'])


def test_backup_restores_all_registered_roots_and_api(tmp_path, monkeypatch):
    client, base, auth, aid, db = _fixture(tmp_path, monkeypatch)
    with sqlite3.connect(db) as connection:
        originals = {row[0] for row in connection.execute('SELECT DISTINCT artifact_root FROM artefatos_f10')}
    assert len(originals) == 2  # F05 export and F10 API artifacts.
    bundle = tmp_path / 'offline-backup'
    manifest = backup(db, bundle)
    assert {row['original'] for row in manifest['roots']} == originals
    restored = restore(bundle, tmp_path / 'restored.sqlite', tmp_path / 'restored-roots')
    assert set(restored['root_mapping']) == originals
    monkeypatch.setenv('SIE_LOCAL_DB_PATH', restored['database'])
    monkeypatch.setenv('SIE_F10_ARTIFACT_ROOT', restored['root_mapping'][os.environ['SIE_F10_ARTIFACT_ROOT']])
    with TestClient(app) as recovered:
        detail = recovered.get(base + '/artifacts/' + aid, headers=auth)
        assert detail.status_code == 200, detail.text
        assert detail.json()['verification']['integrity'] == 'VERIFIED'
        filename = next(iter(detail.json()['manifest']['files_sha256']))
        assert recovered.get(base + '/artifacts/' + aid + '/files/' + filename, headers=auth).status_code == 200
    with pytest.raises(FileExistsError):
        restore(bundle, tmp_path / 'restored.sqlite', tmp_path / 'other')


def test_corruption_and_missing_root_fail_without_partial_restore(tmp_path, monkeypatch):
    _, _, _, _, db = _fixture(tmp_path, monkeypatch)
    bundle = tmp_path / 'bundle'
    backup(db, bundle)
    victim = next(p for p in (bundle / 'roots').rglob('*') if p.is_file())
    victim.write_bytes(victim.read_bytes() + b'corrupt')
    target_db, target_roots = tmp_path / 'recovery.db', tmp_path / 'recovery-roots'
    with pytest.raises(ValueError, match='alterado'):
        restore(bundle, target_db, target_roots)
    assert not target_db.exists() and not target_roots.exists()
    victim.unlink()
    with pytest.raises(ValueError, match='alterado'):
        restore(bundle, target_db, target_roots)
    assert not target_db.exists() and not target_roots.exists()


def test_nonpublished_and_symlink_source_fail_closed(tmp_path, monkeypatch):
    _, _, _, _, db = _fixture(tmp_path, monkeypatch)
    with sqlite3.connect(db) as connection:
        row = connection.execute('SELECT artifact_id,artifact_root FROM artefatos_f10 LIMIT 1').fetchone()
        connection.execute("UPDATE artefatos_f10 SET state='RECOVERY_REQUIRED' WHERE artifact_id=?", (row[0],))
    with pytest.raises(ValueError, match='Publicacao'):
        backup(db, tmp_path / 'not-allowed')
    assert not (tmp_path / 'not-allowed').exists()
    with sqlite3.connect(db) as connection:
        connection.execute("UPDATE artefatos_f10 SET state='PUBLISHED' WHERE artifact_id=?", (row[0],))
    root = Path(row[1]); symlink = root / 'unexpected-link'
    symlink.symlink_to(db)
    with pytest.raises(ValueError, match='Link simbolico'):
        backup(db, tmp_path / 'symlink-refused')
    assert not (tmp_path / 'symlink-refused').exists()


def test_cli_backup_restore_and_bundle_symlink_rejection(tmp_path, monkeypatch, capsys):
    _, _, _, _, db = _fixture(tmp_path, monkeypatch)
    bundle = tmp_path / 'bundle'
    main(['backup', '--db', str(db), '--bundle', str(bundle)])
    assert 'SIE-F11-MULTI-ROOT-1' in capsys.readouterr().out
    copied_db, copied_roots = tmp_path / 'copy.sqlite', tmp_path / 'copy-roots'
    main(['restore', '--bundle', str(bundle), '--db', str(copied_db), '--roots', str(copied_roots)])
    assert 'root_mapping' in capsys.readouterr().out
    assert copied_db.is_file() and copied_roots.is_dir()
    (bundle / 'bundle.json').rename(bundle / 'manifest-real.json')
    (bundle / 'bundle.json').symlink_to(bundle / 'manifest-real.json')
    with pytest.raises(ValueError, match='Link simbolico'):
        restore(bundle, tmp_path / 'no.db', tmp_path / 'no-roots')


def test_restore_rejects_destinations_inside_bundle_or_original_root(tmp_path, monkeypatch):
    _, _, _, _, db = _fixture(tmp_path, monkeypatch)
    bundle = tmp_path / 'bundle'
    manifest = backup(db, bundle)
    inside_bundle = bundle / 'roots' / '0000' / 'recursive'
    with pytest.raises(ValueError, match='Destino dentro'):
        restore(bundle, tmp_path / 'safe.db', inside_bundle)
    assert not inside_bundle.exists() and not (tmp_path / 'safe.db').exists()
    original = Path(manifest['roots'][0]['original'])
    inside_live = original / 'accidental-restore'
    with pytest.raises(ValueError, match='Destino dentro'):
        restore(bundle, tmp_path / 'safe.db', inside_live)
    assert not inside_live.exists() and not (tmp_path / 'safe.db').exists()
