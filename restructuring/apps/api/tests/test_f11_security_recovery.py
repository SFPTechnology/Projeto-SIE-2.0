"""F11 negative paths across local authentication, artifact bytes and recovery."""

import os
from pathlib import Path

from fastapi.testclient import TestClient

from sie_api.artifact_registry_f10 import ArtifactRegistryF10
from sie_api.main import app
from sie_api.storage import RepositorioProjetos
from test_artifacts_api_f10 import client_case


def test_f10_rejects_remote_peer_and_production_even_with_valid_token(tmp_path, monkeypatch):
    _, base, body, auth = client_case(tmp_path, monkeypatch)
    with TestClient(app, client=('203.0.113.10', 51234)) as remote:
        assert remote.post(base + '/execute', json=body, headers=auth).status_code == 403
        assert remote.get(base + '/artifacts', headers=auth).status_code == 403
    monkeypatch.setenv('SIE_ENV', 'production')
    with TestClient(app) as production:
        assert production.post(base + '/generate', json=body, headers=auth).status_code == 503


def test_f10_artifact_tamper_blocks_inspect_and_download(tmp_path, monkeypatch):
    client, base, body, auth = client_case(tmp_path, monkeypatch)
    assert client.post(base + '/execute', json=body, headers=auth).status_code == 200
    response = client.post(base + '/generate', json=body, headers=auth)
    assert response.status_code == 200, response.text
    aid = response.json()['artifact_id']
    name = next(iter(client.get(base + '/artifacts/' + aid, headers=auth).json()['manifest']['files_sha256']))
    # The actual path is determined by the registry, never by client input.
    repo = RepositorioProjetos(os.environ['SIE_LOCAL_DB_PATH'])
    row = ArtifactRegistryF10(repo).get(aid)
    path = Path(row['artifact_root']) / row['destination_relative'] / name
    path.write_bytes(path.read_bytes() + b'changed')
    inspected = client.get(base + '/artifacts/' + aid, headers=auth)
    assert inspected.status_code in (200, 409)
    if inspected.status_code == 200:
        assert inspected.json()['verification']['integrity'] != 'VERIFIED'
    assert client.get(base + '/artifacts/' + aid + '/files/' + name, headers=auth).status_code == 409
