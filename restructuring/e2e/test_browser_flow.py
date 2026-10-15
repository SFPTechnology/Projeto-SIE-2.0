"""Real Chromium E2E against localhost API, static UI and temporary SQLite.

Run only in an isolated developer/CI environment. Does not contact Supabase
or modify a deployed instance; normative approval must always remain disabled.
"""
import os
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
        browser = playwright.chromium.launch(headless=True)
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
