"""Real F10 browser/API/SQLite/motor flow, isolated from production."""
import os
from pathlib import Path
import secrets
import subprocess
import sys
import time
from urllib.request import urlopen
import pytest
from playwright.sync_api import sync_playwright, expect
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'apps/api/tests'))
from test_full_f10_integration import prepare_full

@pytest.fixture(scope='module')
def f10_servers(tmp_path_factory):
    folder=tmp_path_factory.mktemp('f10-browser');repo,pid,rid=prepare_full(folder);token=secrets.token_hex(24)
    env={**os.environ,'SIE_LOCAL_API_TOKEN':token,'SIE_LOCAL_DB_PATH':repo.caminho,'SIE_F10_ARTIFACT_ROOT':str(folder/'artifacts')}
    processes=[]
    try:
        for command,cwd in [([sys.executable,'-m','uvicorn','sie_api.main:app','--host','127.0.0.1','--port','8000'],ROOT/'apps/api'),([sys.executable,'-m','http.server','5173','--bind','127.0.0.1'],ROOT/'apps/web')]:
            processes.append(subprocess.Popen(command,cwd=cwd,env=env,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL))
        for url in ['http://127.0.0.1:8000/api/v1/health','http://127.0.0.1:5173/artefatos.html']:
            for _ in range(100):
                try:
                    if urlopen(url,timeout=.5).status==200:break
                except OSError:time.sleep(.1)
            else:raise RuntimeError('server unavailable')
        yield token,pid,rid
    finally:
        for process in processes:process.terminate()
        for process in processes:
            try:process.wait(timeout=5)
            except subprocess.TimeoutExpired:process.kill();process.wait()


def test_f10_editor_real_generation_keyboard_mobile_preview_print(f10_servers):
    token,pid,rid=f10_servers
    with sync_playwright() as pw:
        kwargs={'executable_path':os.environ['SIE_E2E_BROWSER_PATH'],'args':['--no-zygote','--single-process','--disable-dev-shm-usage']} if os.environ.get('SIE_E2E_BROWSER_PATH') else {}
        browser=pw.chromium.launch(headless=True,**kwargs);page=browser.new_page(viewport={'width':1200,'height':900})
        errors=[];page.on('pageerror',lambda err:errors.append(str(err)))
        page.goto('http://127.0.0.1:5173/artefatos.html')
        for key,value in [('token',token),('project',pid),('run',rid)]:page.locator('#'+key).fill(value)
        page.locator('#open').click();expect(page.locator('#status')).to_contain_text('Projeto aberto')
        expect(page.locator('#drawing svg')).to_be_visible()
        for key in ['fit','zoom-in','left']:page.locator('#'+key).click()
        page.locator('#layer-base').uncheck();page.locator('#layer-base').check()
        page.locator('#search').fill('00000000');assert page.locator('#element option').count()>0
        page.locator('#x').fill('12');page.locator('#y').fill('14');page.locator('#place').focus();page.keyboard.press('Enter')
        expect(page.locator('#dirty')).to_contain_text('não salvas')
        page.locator('#undo').click();page.locator('#redo').click()
        page.locator('#save').click();expect(page.locator('#status')).to_contain_text('Nova revisão salva')
        expect(page.locator('#revision')).to_have_value('3')
        page.locator('#generate').click();expect(page.locator('#status')).to_contain_text('recusada')
        page.locator('#execute').click();expect(page.locator('#status')).to_contain_text('Execução server-side')
        page.locator('#generate').click();expect(page.locator('#status')).to_contain_text('Pacote gerado')
        page.locator('#artifacts button').last.click();expect(page.locator('#verification')).to_contain_text('VERIFIED')
        page.locator('#files button').filter(has_text='Prévia').first.click()
        expect(page.locator('#preview')).to_have_attribute('src',__import__('re').compile('^blob:'))
        page.emulate_media(media='print');assert page.locator('#preview').is_visible();page.emulate_media(media='screen')
        page.set_viewport_size({'width':390,'height':844});assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')
        output=ROOT.parent/'run-artifacts';output.mkdir(exist_ok=True)
        page.locator('#token').fill('');page.screenshot(path=str(output/'f10-mobile-preview.png'),full_page=True)
        page.locator('#history').click();expect(page.locator('#status')).to_contain_text('obrigatoria')
        assert not errors,errors
        browser.close()
