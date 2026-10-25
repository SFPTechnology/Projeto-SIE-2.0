"""Browser-driven F11 consultative lineage and stale-document journey."""
import json
import os
from pathlib import Path
import secrets
import socket
import subprocess
import sys
import time
from urllib.request import urlopen

import pytest
from playwright.sync_api import expect, sync_playwright

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'apps/api/tests'))
from test_f11_f09_f10_bridge import integrated_project  # noqa: E402
from sie_api.domain.installation import Installation  # noqa: E402
from sie_api.installation_service import create_snapshot  # noqa: E402


def _port():
    with socket.socket() as listener:
        listener.bind(('127.0.0.1', 0))
        return listener.getsockname()[1]


@pytest.fixture(scope='module')
def f11_servers(tmp_path_factory):
    folder = tmp_path_factory.mktemp('f11-browser')
    repo, pid, rid, supply = integrated_project(folder)
    token = secrets.token_hex(24)
    api_port, web_port = _port(), _port()
    env = {**os.environ, 'SIE_LOCAL_API_TOKEN': token,
           'SIE_LOCAL_DB_PATH': str(repo.caminho),
           'SIE_F10_ARTIFACT_ROOT': str(folder / 'artifacts')}
    processes = []
    try:
        processes.append(subprocess.Popen(
            [sys.executable, '-m', 'uvicorn', 'sie_api.main:app', '--host', '127.0.0.1', '--port', str(api_port)],
            cwd=ROOT / 'apps/api', env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
        processes.append(subprocess.Popen(
            [sys.executable, '-m', 'http.server', str(web_port), '--bind', '127.0.0.1'],
            cwd=ROOT / 'apps/web', env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL))
        for url in (f'http://127.0.0.1:{api_port}/api/v1/health',
                    f'http://127.0.0.1:{web_port}/artefatos.html'):
            for _ in range(100):
                try:
                    if urlopen(url, timeout=.5).status == 200:
                        break
                except OSError:
                    time.sleep(.1)
            else:
                raise RuntimeError('F11 local server unavailable')
        yield repo, pid, rid, supply, token, api_port, web_port
    finally:
        for process in processes:
            process.terminate()
        for process in processes:
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()


def test_f11_browser_generates_consultative_document_then_marks_load_change_stale(f11_servers):
    repo, pid, rid, supply, token, api_port, web_port = f11_servers
    with sync_playwright() as playwright:
        kwargs = ({'executable_path': os.environ['SIE_E2E_BROWSER_PATH'],
                   'args': ['--no-zygote', '--single-process', '--disable-dev-shm-usage']}
                  if os.environ.get('SIE_E2E_BROWSER_PATH') else {})
        browser = playwright.chromium.launch(headless=True, **kwargs)
        page = browser.new_page(viewport={'width': 1200, 'height': 900})
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.goto(f'http://127.0.0.1:{web_port}/artefatos.html')
        page.locator('#api').fill(f'http://127.0.0.1:{api_port}')
        for key, value in (('token', token), ('project', pid), ('run', rid)):
            page.locator('#' + key).fill(value)
        page.locator('#open').click()
        expect(page.locator('#status')).to_contain_text('Projeto aberto')
        expect(page.locator('#revision')).to_have_value('8')
        page.locator('#generate').click()
        expect(page.locator('#status')).to_contain_text('Pacote gerado')
        row = page.locator('#artifacts button').last
        artifact_id = row.inner_text().split(' · ')[0]
        row.click()
        expect(page.locator('#verification')).to_contain_text('VERIFIED · CURRENT')
        url = f'http://127.0.0.1:{api_port}/api/v1/local/projetos/{pid}/f10/artifacts/{artifact_id}'
        headers = {'Authorization': f'Bearer {token}'}
        manifest = page.request.get(url, headers=headers).json()['manifest']
        assert len(manifest['dependencies']['f09_assessment_sha256']) == 64
        snapshot = page.request.get(url + '/files/snapshot.json', headers=headers).json()
        lineage = snapshot['f09_consultative_lineage']
        assert lineage['evidence']['project_id'] == pid
        assert lineage['evidence']['supply_id'] == supply
        assert {'F06', 'F07', 'F08'} <= set(lineage['evidence'])
        assert lineage['assessment_id_sha256'] == manifest['dependencies']['f09_assessment_sha256']
        assert lineage['status'] == 'CONSULTATIVE_NOT_NORMATIVE'
        assert manifest['normative_conformity_verified'] is False

        saved = repo.carregar(pid)
        data = saved['dados']
        installation = json.loads(data['installation_snapshot']['canonical_json'])
        installation['loads'][0]['active_power']['value'] = '1100'
        installation['loads'][0]['apparent_power']['value'] = '1100'
        data['installation_snapshot'] = create_snapshot(Installation.model_validate(installation)).model_dump(mode='json')
        data['floor_plan_f10']['revision_id'] = '9'
        repo.salvar(pid, saved['nome'], data, 8)
        page.locator('#history').click()
        page.locator('#artifacts button').last.click()
        expect(page.locator('#verification')).to_contain_text('STALE')
        page.locator('#token').fill('')
        assert not errors, errors
        browser.close()
