"""Real Chromium E2E against localhost API, static UI and temporary SQLite.

Run only in an isolated developer/CI environment. Does not contact Supabase
or modify a deployed instance; normative approval must always remain disabled.
"""
import os
import json
from pathlib import Path
import secrets
import subprocess
import sys
import tempfile
import time
from urllib.request import urlopen

import pytest
from playwright.sync_api import expect, sync_playwright


ROOT = Path(__file__).resolve().parents[1]
API_DIR = ROOT / "apps" / "api"
WEB_DIR = ROOT / "apps" / "web"
API_URL = "http://127.0.0.1:8000"
WEB_URL = "http://127.0.0.1:5173"


def wait_for_server(url: str) -> None:
    for _ in range(100):
        try:
            with urlopen(url, timeout=0.5) as result:
                if result.status == 200:
                    return
        except OSError:
            time.sleep(0.1)
    raise RuntimeError(f"Local server did not start: {url}")


@pytest.fixture(scope="module")
def servers():
    with tempfile.TemporaryDirectory(prefix="sie-e2e-") as folder:
        token = secrets.token_hex(24)
        environment = os.environ.copy()
        environment["SIE_LOCAL_API_TOKEN"] = token
        environment["SIE_LOCAL_DB_PATH"] = str(Path(folder) / "projects.sqlite3")
        commands = [
            ([sys.executable, "-m", "uvicorn", "sie_api.main:app",
              "--host", "127.0.0.1", "--port", "8000"], API_DIR),
            ([sys.executable, "-m", "http.server", "5173",
              "--bind", "127.0.0.1"], WEB_DIR),
        ]
        processes = []
        try:
            for command, cwd in commands:
                processes.append(subprocess.Popen(
                    command, cwd=cwd, env=environment,
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                ))
            wait_for_server(API_URL + "/api/v1/health")
            wait_for_server(WEB_URL + "/")
            yield token
        finally:
            for process in processes:
                process.terminate()
            for process in processes:
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait(timeout=5)


@pytest.fixture
def page(servers):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, **({'executable_path': os.environ['SIE_E2E_BROWSER_PATH'], 'args': ['--no-zygote', '--single-process', '--disable-dev-shm-usage']} if os.environ.get('SIE_E2E_BROWSER_PATH') else {}))
        context = browser.new_context()
        browser_page = context.new_page()
        errors = []
        browser_page.on("pageerror", lambda error: errors.append(str(error)))
        browser_page.goto(WEB_URL, wait_until="networkidle")
        expect(browser_page.locator("#health")).to_contain_text("API online")
        yield browser_page
        assert not errors, "Browser JavaScript errors: " + "; ".join(errors)
        context.close()
        browser.close()


def test_full_browser_calculate_save_reload_recalculate(page, servers):
    page.locator("#project-token").fill(servers)
    page.locator("#project-name").fill("Ensaio E2E do SIE")
    page.locator('#analysis-form button[type="submit"]').click()

    expect(page.locator("#resultado")).to_contain_text("Gate normativo não aprovado")
    expect(page.locator("#resultado")).to_contain_text("PENDENTE")
    expect(page.locator("#resultado")).to_contain_text("4 mm²")
    page.locator("#project-save").click()

    expect(page.locator("#project-status")).to_contain_text("revisao 1")
    project_id = page.locator("#project-id").input_value()
    assert len(project_id) == 36
    assert page.locator("#project-revision").input_value() == "1"

    # Save an edited scenario, then ensure reload never implies revalidation.
    page.locator('input[name="corrente_a"]').fill("23")
    page.locator('#analysis-form button[type="submit"]').click()
    expect(page.locator("#resultado")).to_contain_text("PENDENTE")
    page.locator("#project-save").click()
    expect(page.locator("#project-status")).to_contain_text("revisao 2")

    page.reload(wait_until="networkidle")
    page.locator("#project-id").fill(project_id)
    page.locator("#project-token").fill(servers)
    page.locator("#project-load").click()
    expect(page.locator("#project-status")).to_contain_text("revisao 2")
    assert page.locator('input[name="corrente_a"]').input_value() == "23"
    expect(page.locator("#resultado")).to_contain_text("Execute uma nova analise")
    assert "Gate normativo aprovado." not in page.locator("#resultado").inner_text()

    page.locator('#analysis-form button[type="submit"]').click()
    expect(page.locator("#resultado")).to_contain_text("PENDENTE")
    assert page.evaluate("localStorage.getItem('sie.localToken')") is None
    assert page.evaluate("sessionStorage.length") == 0


def test_demo_defaults_are_explicit_and_do_not_claim_nbr_source(page):
    expect(page.locator('#demo-input-notice')).to_be_visible()
    expect(page.locator('#demo-input-notice')).to_contain_text('tabela interna de condutores são fictícios')
    assert page.locator('input[name="documento"]').input_value() == 'Demonstração sintética não homologada'
    assert page.locator('input[name="edicao"]').input_value() == 'EXEMPLO'
    page.locator('#analysis-form button[type="submit"]').click()
    expect(page.locator('#resultado')).to_contain_text('Demonstração sintética não homologada')
    expect(page.locator('#resultado .result-status.pending')).to_be_visible()


@pytest.mark.parametrize('server_status', ['PENDENTE', 'APROVADO'])
def test_isolated_true_flag_or_unexpected_approval_cannot_turn_ui_green(page, server_status):
    def fake_response(route):
        response = route.fetch()
        data = response.json()
        data.update(liberado_para_uso_normativo=True, status_engenharia=server_status,
                    aviso='Gate normativo aprovado por um booleano')
        route.fulfill(response=response, json=data)
    page.route('**/api/v1/circuitos/analisar', fake_response)
    page.locator('#analysis-form button[type="submit"]').click()
    expect(page.locator('#resultado .result-status.pending')).to_be_visible()
    expect(page.locator('#resultado')).to_contain_text('Liberação bloqueada')
    expect(page.locator('#resultado .tag')).to_have_text('PENDENTE')
    assert page.locator('#resultado .approved').count() == 0
    assert 'Gate normativo aprovado' not in page.locator('#resultado').inner_text()


@pytest.mark.parametrize('width', [390, 850])
def test_mobile_navigation_is_visible_and_keyboard_reachable(page, width):
    page.set_viewport_size({'width': width, 'height': 844})
    page.goto(WEB_URL, wait_until='networkidle')
    links = page.get_by_role('navigation', name='Navegação principal').get_by_role('link')
    assert links.count() == 6
    if width == 390:
        Path('run-artifacts').mkdir(exist_ok=True)
        page.screenshot(path='run-artifacts/f01-mobile-navigation-390.png')
    page.keyboard.press('Tab')
    for index in range(links.count()):
        link = links.nth(index)
        expect(link).to_be_visible()
        expect(link).to_be_focused()
        assert link.evaluate("e => getComputedStyle(e).outlineStyle") != 'none'
        if index < links.count() - 1:
            page.keyboard.press('Tab')
    page.keyboard.press('Enter')
    expect(page).to_have_url(WEB_URL + '/#guia')
    if width == 390:
        page.locator('#circuito').scroll_into_view_if_needed()
        page.screenshot(path='run-artifacts/f01-mobile-demo-390.png')


def test_wrong_token_and_stale_revision_are_visible(page, servers):
    page.locator("#project-token").fill(servers)
    page.locator('#analysis-form button[type="submit"]').click()
    expect(page.locator("#resultado")).to_contain_text("PENDENTE")
    page.locator("#project-save").click()
    expect(page.locator("#project-status")).to_contain_text("revisao 1")

    page.locator("#project-token").fill("invalid-but-long-enough-development-token")
    page.locator("#project-load").click()
    expect(page.locator("#project-status")).to_contain_text("Credencial")
    page.locator("#project-token").fill(servers)

    # A load attempt invalidates prior analysis even when authentication fails.
    page.locator('#analysis-form button[type="submit"]').click()
    expect(page.locator('#analysis-form button[type="submit"]')).to_be_enabled()
    expect(page.locator("#resultado")).to_contain_text("PENDENTE")
    # Simulate stale state and check explicit HTTP 409 handling in browser.
    page.locator("#project-revision").evaluate("(field) => { field.value = '0'; }")
    page.locator("#project-save").click()
    expect(page.locator("#project-status")).to_contain_text("Conflito")
    assert page.locator("#project-revision").input_value() == "0"


def test_untrusted_evidence_is_rendered_as_text_not_markup(page):
    payload = '<img src=x onerror="window.sieInjected=true">'
    page.locator('input[name="documento"]').fill(payload)
    page.locator('#analysis-form button[type="submit"]').click()
    expect(page.locator("#resultado")).to_contain_text(payload)
    assert page.locator("#resultado img").count() == 0
    assert page.evaluate("window.sieInjected === true") is False


def test_f01_normative_catalog_ui_is_explicitly_unverified(page):
    """Catálogo F01 legível no Chromium; nenhuma linha implica aprovação."""
    expect(page.locator("#normas-status")).to_contain_text("8 fontes cadastradas")
    expect(page.locator("#normas-lista li")).to_have_count(8)
    labels = page.locator("#normas-lista li").all_inner_texts()
    assert all("NÃO VERIFICADA" in item for item in labels)
    assert "concede conformidade" in page.locator("#normas").inner_text().lower()
    assert page.locator("#normas button").count() == 0


def test_local_immutable_revision_history_visible_without_normative_approval(page, servers):
    page.locator("#project-token").fill(servers)
    page.locator("#project-name").fill("Histórico E2E com duas revisões")
    page.locator('#analysis-form button[type="submit"]').click()
    page.locator("#project-save").click()
    expect(page.locator("#project-status")).to_contain_text("revisao 1")
    page.locator('input[name="corrente_a"]').fill("21")
    page.locator('#analysis-form button[type="submit"]').click()
    page.locator("#project-save").click()
    expect(page.locator("#project-status")).to_contain_text("revisao 2")

    page.locator("#project-history-refresh").click()
    expect(page.locator("#project-history-status")).to_contain_text("2 revisões locais")
    expect(page.locator("#project-history-list button")).to_have_count(2)
    page.locator("#project-history-list button").first.click()
    expect(page.locator("#project-history-summary")).to_contain_text("Revisão 1 recuperada integralmente")
    expect(page.locator("#project-history-summary")).to_contain_text("Fonte normativa não homologada")
    assert "recálculo automático" in page.locator("#project-history-summary").inner_text()

    page.locator("#project-token").fill("invalid-but-long-enough-development-token")
    page.locator("#project-history-refresh").click()
    expect(page.locator("#project-history-status")).to_contain_text("Credencial")
    expect(page.locator("#project-history-list button")).to_have_count(0)
    assert page.evaluate("localStorage.getItem('sie.localToken')") is None


def test_import_conditional_case_trace_save_reload_and_stale_result_block(page,servers):
    import json
    fixture=ROOT/'examples'/'f01_verificacoes_complementares_demo.json'
    page.locator('#analysis-case-file').set_input_files(str(fixture))
    expect(page.locator('#analysis-case-status')).to_contain_text('Caso carregado')
    page.locator('#analysis-form button[type="submit"]').click()
    expect(page.locator('#resultado')).to_contain_text('CEL-01')
    expect(page.locator('#resultado')).to_contain_text('I2=29 A')
    expect(page.locator('#resultado')).to_contain_text('Queda com Rca e XL')
    expect(page.locator('#resultado')).to_contain_text('coordenação completa permanecem pendentes')
    page.locator('#project-token').fill(servers)
    page.locator('#project-save').click()
    expect(page.locator('#project-status')).to_contain_text('revisao 1')
    pid=page.locator('#project-id').input_value()
    saved=page.request.get(API_URL+'/api/v1/local/projetos/'+pid,
                           headers={'Authorization':'Bearer '+servers}).json()
    case=saved['dados']['circuitos'][0]
    assert case['nome']=='Circuito 01'
    assert case['queda_impedancia']['secao_mm2']==2.5
    response=page.request.post(API_URL+'/api/v1/local/projetos/'+pid+'/revisoes/1/circuitos/Circuito%2001/ensaios',
                               data=json.loads(fixture.read_text()),headers={'Authorization':'Bearer '+servers})
    assert response.status==200
    assert response.json()['trace_schema_version']==4
    page.reload(wait_until='networkidle')
    page.locator('#project-token').fill(servers);page.locator('#project-id').fill(pid)
    page.locator('#project-load').click()
    expect(page.locator('#project-status')).to_contain_text('revisao 1')
    page.locator('#analysis-form button[type="submit"]').click()
    expect(page.locator('#resultado')).to_contain_text('Queda com Rca e XL')
    page.locator('input[name="corrente_a"]').fill('20.5')
    page.locator('#analysis-form button[type="submit"]').click()
    expect(page.locator('#resultado')).to_contain_text('Dispositivo declarado não corresponde ao In selecionado')
    page.locator('#project-save').click()
    expect(page.locator('#project-status')).to_contain_text('Execute uma analise antes de salvar')


def test_import_negative_i2_and_incompatible_context_never_claim_approval(page):
    import json
    fixture=json.loads((ROOT/'examples'/'f01_verificacoes_complementares_demo.json').read_text())
    fixture['protecao_sobrecarga']['corrente_atuacao_i2_a']=100
    page.locator('#analysis-case-file').set_input_files({'name':'negative.json','mimeType':'application/json',
                                                      'buffer':json.dumps(fixture).encode()})
    expect(page.locator('#analysis-case-status')).to_contain_text('Caso carregado')
    page.locator('#analysis-form button[type="submit"]').click()
    expect(page.locator('#resultado')).to_contain_text('Verificação não atendida')
    expect(page.locator('#resultado')).to_contain_text('NAO_ATENDE')
    expect(page.locator('#resultado .result-status.pending')).to_be_visible()
    fixture['vinculo_celulas']['condicoes']['isolacao']='EPR_XLPE'
    page.locator('#analysis-case-file').set_input_files({'name':'bad-context.json','mimeType':'application/json',
                                                      'buffer':json.dumps(fixture).encode()})
    page.locator('#analysis-form button[type="submit"]').click()
    expect(page.locator('#resultado')).to_contain_text('fora do escopo')
    assert 'Gate normativo aprovado.' not in page.locator('#resultado').inner_text()


def test_invalid_import_discards_previous_case_and_mobile_keyboard_remains_usable(page):
    page.set_viewport_size({'width':390,'height':844})
    page.locator('#analysis-case-file').set_input_files({'name':'bad.json','mimeType':'application/json','buffer':b'[]'})
    expect(page.locator('#analysis-case-status')).to_contain_text('Caso descartado')
    page.locator('#analysis-case-file').locator('xpath=ancestor::details').locator('summary').click()
    page.locator('#analysis-case-reset').focus()
    assert page.locator('#analysis-case-reset').evaluate('(node)=>node===document.activeElement')
    page.locator('#analysis-case-reset').click()
    expect(page.locator('#analysis-case-status')).to_contain_text('Tabela sintética')
    assert page.evaluate('document.documentElement.scrollWidth <= window.innerWidth')


@pytest.mark.parametrize('action', ['reset', 'edit', 'import', 'load_empty'])
def test_delayed_analysis_cannot_restore_stale_input(page, servers, action):
    page.evaluate("""() => {
      const original = window.fetch.bind(window);
      window.fetch = async (...args) => {
        const response = await original(...args);
        if (String(args[0]).endsWith('/circuitos/analisar')) {
          await new Promise(resolve => { window.releaseAnalysis = resolve; });
        }
        return response;
      };
    }""")
    page.locator('#analysis-form button[type="submit"]').click()
    page.wait_for_function('typeof window.releaseAnalysis === "function"')
    if action == 'reset':
        page.locator('#analysis-case-reset').locator('xpath=ancestor::details').evaluate('(node) => node.open = true')
        page.locator('#analysis-case-reset').click()
    elif action == 'edit':
        page.locator('input[name="corrente_a"]').fill('21')
    elif action == 'load_empty':
        from uuid import uuid4
        pid = str(uuid4())
        response = page.request.put(API_URL + '/api/v1/local/projetos',
            data={'id': pid, 'nome': 'Empty', 'dados': {'circuitos': []}, 'revisao_esperada': 0},
            headers={'Authorization': 'Bearer ' + servers})
        assert response.status == 200
        page.locator('#project-token').fill(servers)
        page.locator('#project-id').fill(pid)
        page.locator('#project-load').click()
        expect(page.locator('#project-status')).to_contain_text('Projeto recuperado')
    else:
        page.locator('#analysis-case-file').set_input_files(
            str(ROOT / 'examples' / 'f01_verificacoes_complementares_demo.json'))
        expect(page.locator('#analysis-case-status')).to_contain_text('Caso carregado')
    page.evaluate('window.releaseAnalysis()')
    expect(page.locator('#analysis-form button[type="submit"]')).to_be_enabled()
    page.locator('#project-save').click()
    expect(page.locator('#project-status')).to_contain_text('Execute uma analise antes de salvar')
    assert 'Condutor selecionado' not in page.locator('#resultado').inner_text()


def test_f04_demo_save_reload_and_distinct_units(page, servers):
    page.goto(WEB_URL+'/levantamento.html')
    page.locator('#demo').click()
    expect(page.locator('#status')).to_contain_text('Demonstração sintética carregada')
    page.locator('#token').fill(servers)
    page.locator('#save').click()
    expect(page.locator('#status')).to_contain_text('Salvo · revisão 1')
    project_id=page.locator('#project-id').input_value()
    page.reload()
    page.locator('#token').fill(servers)
    page.locator('#project-id').fill(project_id)
    page.locator('#reopen').click()
    expect(page.locator('#status')).to_contain_text('Reaberto · revisão 1')
    expect(page.locator('#records')).to_contain_text('Tomadas sala')
    expect(page.locator('#summary')).to_contain_text('3100')
    expect(page.locator('#summary')).to_contain_text('PENDENTE_FONTE_VALIDADA')


def test_f04_editor_invalid_values_preserved_and_undo(page):
    page.goto(WEB_URL+'/levantamento.html')
    page.locator('#demo').click()
    expect(page.locator('#status')).to_contain_text('Demonstração sintética carregada')
    page.get_by_role('button',name='Editar Luz sala',exact=True).click()
    page.locator('#field-quantidade').fill('1.5')
    page.get_by_role('button',name='Aplicar registro',exact=True).click()
    expect(page.locator('#status')).to_contain_text('Registro não aplicado')
    expect(page.locator('#field-quantidade')).to_have_value('1.5')
    page.locator('#field-quantidade').fill('2')
    page.get_by_role('button',name='Aplicar registro',exact=True).click()
    expect(page.locator('#status')).to_contain_text('Alteração local aplicada')
    expect(page.locator('#summary')).to_contain_text('3200')
    page.locator('#undo').click()
    expect(page.locator('#summary')).to_contain_text('3100')


def test_f04_protect_unsaved_and_wrong_token(page):
    page.goto(WEB_URL+'/levantamento.html')
    page.locator('#nome').fill('Edição protegida')
    page.once('dialog',lambda dialog:dialog.dismiss())
    page.locator('#reopen').click()
    expect(page.locator('#nome')).to_have_value('Edição protegida')
    page.locator('#token').fill('wrong')
    page.locator('#save').click()
    expect(page.locator('#status')).to_contain_text('Não salvo; dados locais preservados')
    expect(page.locator('#nome')).to_have_value('Edição protegida')


def test_f04_create_hierarchy_and_three_classes_from_empty(page, servers):
    page.goto(WEB_URL+'/levantamento.html')
    def apply(kind, name, **values):
        page.locator('#kind').select_option(kind)
        page.locator('#field-nome').fill(name)
        for key,value in values.items():
            node=page.locator('#field-'+key)
            if node.evaluate('(e)=>e.tagName')=='SELECT':node.select_option(value)
            else:node.fill(value)
        page.get_by_role('button',name='Aplicar registro',exact=True).click()
        expect(page.locator('#status')).to_contain_text('Alteração local aplicada')
    apply('edificacoes','Casa')
    apply('pavimentos','Térreo')
    apply('ambientes','Sala',tipo='sala',area_m2='20')
    apply('ambientes','Banheiro',tipo='banheiro',condicao='molhado')
    apply('cargas','Luz',classe='ILUMINACAO',p_w='100',tensao_v='127',fases='1')
    apply('cargas','Tomada',classe='TUG',s_va='100')
    apply('cargas','Equipamento',classe='TUE',p_w='1000',tensao_v='220',fases='1',regime='intermitente',dedicado='sim')
    page.locator('#token').fill(servers)
    page.locator('#save').click()
    expect(page.locator('#status')).to_contain_text('Salvo · revisão 1')
    page.locator('#reopen').click()
    expect(page.locator('#status')).to_contain_text('Reaberto · revisão 1')
    expect(page.locator('#records')).to_contain_text('Equipamento')


def test_f04_edit_defaulted_load_and_keep_form_draft(page):
    page.goto(WEB_URL+'/levantamento.html')
    page.locator('#demo').click()
    expect(page.locator('#status')).to_contain_text('Demonstração sintética carregada')
    page.get_by_role('button',name='Editar Equipamento trifásico de teste',exact=True).click()
    expect(page.locator('#field-quantidade')).to_have_value('1')
    page.get_by_role('button',name='Aplicar registro',exact=True).click()
    expect(page.locator('#status')).to_contain_text('Alteração local aplicada')
    page.locator('#field-nome').fill('Rascunho')
    page.once('dialog',lambda dialog:dialog.dismiss())
    page.locator('#kind').select_option('ambientes')
    expect(page.locator('#kind')).to_have_value('cargas')
    expect(page.locator('#field-nome')).to_have_value('Rascunho')
    page.locator('#archive').click()
    expect(page.locator('#status')).to_contain_text('Aplique ou cancele')
    expect(page.locator('#field-nome')).to_have_value('Rascunho')


def test_f05_edit_save_reopen_and_recompose(page, servers):
    page.goto(WEB_URL + '/topologia.html')
    page.locator('#token').fill(servers)
    page.locator('#demo').click()
    expect(page.locator('#status')).to_contain_text('Integridade válida')
    expect(page.locator('#result')).to_contain_text('22.5')
    page.locator('#length').fill('11')
    page.locator('#edit').click()
    expect(page.locator('#result')).to_contain_text('23.5')
    page.locator('#save').click()
    expect(page.locator('#status')).to_contain_text('Nova revisão salva')
    page.locator('#length').fill('99')
    page.locator('#edit').click()
    expect(page.locator('#result')).to_contain_text('111.5')
    page.locator('#open').click()
    expect(page.locator('#status')).to_contain_text('Reaberto')
    expect(page.locator('#length')).to_have_value('11')
    page.locator('#validate').click()
    expect(page.locator('#result')).to_contain_text('23.5')


def test_f05_invalid_link_no_save_and_undo(page, servers):
    page.goto(WEB_URL + '/topologia.html')
    page.locator('#token').fill(servers)
    page.locator('#demo').click()
    expect(page.locator('#status')).to_contain_text('Integridade válida')
    # Select device from a descendant board for the feeder: invalid ownership.
    page.locator('#device').select_option('00000000-0000-0000-0000-00000000000e')
    page.locator('#link').click()
    expect(page.locator('#status')).to_contain_text('Vínculos inválidos')
    expect(page.locator('#result')).to_contain_text('Circuit device must belong')
    page.locator('#save').click()
    expect(page.locator('#status')).to_contain_text('Vínculos inválidos')
    page.locator('#undo').click()
    page.locator('#validate').click()
    expect(page.locator('#status')).to_contain_text('Integridade válida')


def test_f05_concurrent_revision_rejected(page, servers):
    page.goto(WEB_URL + '/topologia.html')
    page.locator('#token').fill(servers)
    import json
    seeded = json.loads((ROOT / 'examples/f05_topologia_demo.json').read_text())
    pid = '20000000-0000-0000-0000-000000000001'
    seeded['installation']['project']['id'] = pid
    for rows in seeded['installation'].values():
        if isinstance(rows, list):
            for entity in rows:
                entity['project_id'] = pid
    seeded_response = page.request.put(API_URL + '/api/v1/local/projetos/' + pid + '/topologia',
        headers={'Authorization': 'Bearer ' + servers},
        data={'document': seeded, 'expected_revision': 0})
    assert seeded_response.status == 200
    page.locator('#project').fill(pid)
    page.locator('#open').click()
    expect(page.locator('#status')).to_contain_text('Reaberto')
    # Another tab/user writes a full validated next revision first.
    import json
    document = json.loads(page.locator('#json').input_value())
    revision = document['installation']['project']['revision']
    document['installation']['project']['revision'] = revision + 1
    response = page.request.put(API_URL + '/api/v1/local/projetos/' + pid + '/topologia',
        headers={'Authorization': 'Bearer ' + servers},
        data={'document': document, 'expected_revision': revision})
    assert response.status == 200
    page.locator('#save').click()
    expect(page.locator('#status')).to_contain_text('409')
    expect(page.locator('#status')).to_contain_text('Revisão concorrente')


def test_demand_study_and_invalidation(page, servers):
    page.goto(WEB_URL+'/demanda.html',wait_until='networkidle')
    page.locator('#demo').click()
    expect(page.locator('#status')).to_contain_text('carregado')
    page.locator('#calculate').click()
    expect(page.locator('#summary')).to_contain_text('CALCULATED_STUDY')
    expect(page.locator('#memory')).to_contain_text('normative_conformity_verified')
    assert page.locator('#parcels tr').count()>0
    data=json.loads(page.locator('#document').input_value())
    data['rules'][0]['status']='VERIFIED'
    page.locator('#document').fill(json.dumps(data))
    expect(page.locator('#summary')).to_contain_text('desatualizados')
    page.locator('#export').click()
    expect(page.locator('#status')).to_contain_text('Recalcule')
    page.locator('#calculate').click()
    expect(page.locator('#summary')).to_contain_text('PENDING')
    expect(page.locator('#memory')).to_contain_text('TRUSTED_NORMATIVE_REGISTRY_PENDING')
    page.set_viewport_size({'width':390,'height':844})
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth')


def test_demand_edp_source_binding_and_catalog(page,servers):
    page.goto(WEB_URL+'/demanda.html',wait_until='networkidle')
    page.locator('#source-demo').click()
    expect(page.locator('#status')).to_contain_text('Referência EDP V09 carregada')
    page.locator('#calculate').click()
    expect(page.locator('#summary')).to_contain_text('CALCULATED_SOURCE_LINKED')
    expect(page.locator('#memory')).to_contain_text('catalog_sha256')
    expect(page.locator('#parcels')).to_contain_text('0.59')
    expect(page.locator('#parcels')).not_to_contain_text('Pendente')
    page.locator('#catalog').click()
    expect(page.locator('#status')).to_contain_text('22 regras')
    expect(page.locator('#memory')).to_contain_text('official_pdf_sha256')


def test_f07_memory_criteria_export_and_edit_invalidation(page, tmp_path):
    page.goto(WEB_URL+'/condutores.html',wait_until='networkidle')
    page.locator('#demo').click()
    expect(page.locator('#document')).to_have_value(__import__('re').compile('.*SIE_TOPOLOGY_V1.*',__import__('re').S))
    page.locator('#calculate').click()
    expect(page.locator('#status')).to_contain_text('Memória calculada')
    expect(page.locator('#summary')).to_contain_text('PENDENTE')
    expect(page.locator('#criteria')).to_contain_text('Atende ao lote limitado')
    assert page.locator('#criteria tr').count()==20
    with page.expect_download() as download:
        page.locator('#export').click()
    exported=tmp_path/'memory.json';download.value.save_as(str(exported))
    memory=json.loads(exported.read_text())
    assert memory['normative_conformity_verified'] is False
    assert memory['input_snapshot']['cell_revision']
    page.screenshot(path=str(tmp_path/'f07-ui.png'),full_page=False)
    # Print surface exercised; PDF is an intermediate browser verification artifact.
    page.emulate_media(media='print')
    assert len(page.pdf())>1000
    page.emulate_media(media='screen')
    raw=json.loads(page.locator('#document').input_value())
    raw['topology']['installation']['cable_runs'][0]['section']['value']='6'
    page.locator('#document').fill(json.dumps(raw))
    expect(page.locator('#export')).to_be_disabled()
    expect(page.locator('#memory')).to_have_text('')
    page.locator('#calculate').click()
    expect(page.locator('#status')).to_contain_text('Memória calculada')
    expect(page.locator('#criteria')).to_contain_text('Bloqueado')


def test_f07_api_history_cascade_in_browser(page,servers):
    raw=json.loads((ROOT/'examples/f07_condutores_demo.json').read_text())
    pid=raw['topology']['installation']['project']['id']
    def call(method,path,data=None):
        return page.evaluate('''async ({method,path,data,token}) => {
            const r=await fetch('http://127.0.0.1:8000'+path,{method,headers:{'Content-Type':'application/json','Authorization':'Bearer '+token},body:data?JSON.stringify(data):undefined});
            return {status:r.status,body:await r.json()};
        }''',{'method':method,'path':path,'data':data,'token':servers})
    topology='/api/v1/local/projetos/'+pid+'/topologia';study='/api/v1/local/projetos/'+pid+'/condutores'
    # Use distinct project for isolation from prior scenarios in the module.
    original=pid;pid='77777777-7777-4777-8777-777777777777'
    raw=json.loads(json.dumps(raw).replace(original,pid))
    topology='/api/v1/local/projetos/'+pid+'/topologia';study='/api/v1/local/projetos/'+pid+'/condutores'
    assert call('PUT',topology,{'document':raw['topology'],'expected_revision':0})['status']==200
    assert call('PUT',study,{'study':raw,'expected_revision':1})['status']==200
    assert not call('GET',study)['body']['studies'][0]['stale']
    raw['topology']['installation']['project']['revision']=3
    raw['topology']['installation']['segments'][0]['length']['value']='26'
    assert call('PUT',topology,{'document':raw['topology'],'expected_revision':2})['status']==200
    history=call('GET',study)['body']['studies']
    assert history[0]['stale'] and history[0]['dependent_documents_stale']
    raw['id']='77777777-7777-4777-8777-777777777778'
    assert call('PUT',study,{'study':raw,'expected_revision':3})['status']==200
    history=call('GET',study)['body']['studies']
    assert history[0]['stale'] and not history[-1]['stale']


def test_f07_api_change_discards_pending_response(page):
    page.goto(WEB_URL+'/condutores.html',wait_until='networkidle')
    page.locator('#demo').click()
    expect(page.locator('#document')).to_have_value(__import__('re').compile('.*SIE_TOPOLOGY_V1.*',__import__('re').S))
    pending=[]
    page.route('**/api/v1/condutores/analisar',lambda route: pending.append(route))
    page.locator('#calculate').click()
    expect(page.locator('#calculate')).to_be_disabled()
    page.locator('#api').fill('http://localhost:8000')
    # Fetch directly through Playwright request context, then release stale UI response.
    response=page.request.post(API_URL+'/api/v1/condutores/analisar',data=json.loads(page.locator('#document').input_value()))
    assert response.status==200
    assert pending
    pending[0].fulfill(status=200,content_type='application/json',headers={'Access-Control-Allow-Origin':WEB_URL},body=response.text())
    expect(page.locator('#calculate')).to_be_enabled()
    expect(page.locator('#export')).to_be_disabled()
    expect(page.locator('#print')).to_be_disabled()
    expect(page.locator('#memory')).to_have_text('')
