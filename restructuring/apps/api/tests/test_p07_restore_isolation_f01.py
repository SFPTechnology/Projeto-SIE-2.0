"""P07 local recovery and project boundaries; shared token is NOT tenant RBAC."""
import sqlite3
from uuid import uuid4

from fastapi.testclient import TestClient
from sie_api.cell_bindings import REVISION
from sie_api.main import app
from sie_api.storage import RepositorioProjetos


def _input():
    return {
        'corrente_a': 20.0, 'comprimento_m': 30.0, 'tensao_v': 220.0,
        'resistencia_ohm_km': 7.41, 'fator_correcao': .87,
        'tabela_condutores': [{'secao_mm2': s, 'capacidade_a': a}
                              for s, a in [(2.5, 24), (4, 32), (6, 41), (10, 57)]],
        'evidencia': {'documento': 'declared test', 'edicao': 'test', 'referencia': 'test'},
        'vinculo_celulas': {'registro_revisao': REVISION,
            'celulas_ids': ['CEL-01', 'CEL-02', 'CEL-03', 'CEL-04', 'CEL-05'],
            'condicoes': {'material': 'Cu', 'isolacao': 'PVC', 'temperatura_condutor_c': 70,
                'metodo_referencia': 'B1', 'metodo_instalacao': 3,
                'descricao_instalacao': 'Local recovery test fixture',
                'condutores_carregados': 2, 'meio': 'AR', 'temperatura_ambiente_c': 40,
                'radiacao_solar': False, 'radiacao_infravermelha': False,
                'circuitos_agrupados': 1, 'agrupamento': 'ISOLADO',
                'grupo_homogeneo': True, 'carga_uniforme': True}}}


def test_sqlite_online_backup_restores_revision_snapshot_and_bound_trace(tmp_path):
    source, backup = tmp_path / 'source.sqlite', tmp_path / 'backup.sqlite'
    repo = RepositorioProjetos(source)
    first, second = str(uuid4()), str(uuid4())
    params = _input()
    repo.salvar(first, 'First', {'circuitos': [{'nome': 'C1', **params}]}, 0)
    trace = repo.registrar_ensaio(first, 1, 'C1', params)
    old_revision = repo.carregar_revisao(first, 1)
    old_snapshot = repo.snapshot_normativo(first, 1)
    old_events = repo.historico_snapshot_normativo(first)
    old_trace_listing = repo.listar_ensaios(first, 1)
    repo.salvar(second, 'Second', {'circuitos': []}, 0)
    with sqlite3.connect(source) as src, sqlite3.connect(backup) as dest:
        src.backup(dest)
    # Subsequent writes establish that recovery reads the backup, not source.
    repo.salvar(first, 'After backup', {'circuitos': []}, 1)
    restored = RepositorioProjetos(backup)
    assert restored.carregar(first)['revisao'] == 1
    assert restored.carregar_revisao(first, 1) == old_revision
    assert restored.snapshot_normativo(first, 1) == old_snapshot
    assert restored.historico_snapshot_normativo(first) == old_events
    assert restored.consultar_ensaio(first, trace['id']) == trace
    assert restored.listar_ensaios(first, 1) == old_trace_listing
    assert restored.consultar_ensaio(second, trace['id']) is None
    assert restored.listar_ensaios(second, 1) == []
    assert trace['release_allowed'] is False
    with sqlite3.connect(backup) as db:
        assert db.execute('PRAGMA integrity_check').fetchall() == [('ok',)]
        assert db.execute('PRAGMA foreign_key_check').fetchall() == []


def test_local_routes_require_credential_and_do_not_cross_project_trace_ids(tmp_path, monkeypatch):
    path = tmp_path / 'api.sqlite'
    token = 'p07-test-only-' + 'x' * 32
    monkeypatch.setenv('SIE_LOCAL_DB_PATH', str(path))
    monkeypatch.setenv('SIE_LOCAL_API_TOKEN', token)
    repo = RepositorioProjetos(path)
    owner, other = str(uuid4()), str(uuid4())
    params = _input()
    repo.salvar(owner, 'First', {'circuitos': [{'nome': 'C1', **params}]}, 0)
    repo.salvar(other, 'Second', {'circuitos': []}, 0)
    trace = repo.registrar_ensaio(owner, 1, 'C1', params)
    root = f'/api/v1/local/projetos/{owner}'
    routes = [root, root + '/historico', root + '/revisoes', root + '/revisoes/1',
              root + '/snapshots-normativos/1', root + '/impacto-normativo/1',
              root + '/historico-normativo', root + '/revisoes/1/ensaios',
              root + '/ensaios/' + trace['id']]
    client = TestClient(app)
    for url in routes:
        assert client.get(url).status_code == 401
        assert client.get(url, headers={'Authorization': 'Bearer wrong'}).status_code == 401
        assert client.get(url, headers={'Authorization': 'Bearer ' + token}).status_code == 200
    wrong_project = f'/api/v1/local/projetos/{other}/ensaios/{trace["id"]}'
    assert client.get(wrong_project, headers={'Authorization': 'Bearer ' + token}).status_code == 404
    # This is project-key isolation inside one local trust domain, NOT user/tenant authorization.
