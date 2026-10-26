"""Chromium end-to-end test for isolated public consultative SIE F12 facade."""
import os
from pathlib import Path
import socket
import subprocess
import sys
import time
from urllib.error import URLError
from urllib.request import urlopen

import pytest
from playwright.sync_api import expect, sync_playwright

API_DIR = Path(__file__).resolve().parents[1] / "apps/api"


def _port():
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


@pytest.fixture(scope="module")
def consultative_url():
    port = _port()
    url = f"http://127.0.0.1:{port}"
    env = dict(os.environ)
    env["SIE_ENV"] = "production"
    env.pop("SIE_LOCAL_API_TOKEN", None)
    env.pop("SIE_LOCAL_DB_PATH", None)
    process = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "sie_api.f12_consultative:app",
         "--host", "127.0.0.1", "--port", str(port)],
        env=env, cwd=API_DIR, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    try:
        for _ in range(80):
            if process.poll() is not None:
                raise RuntimeError("Consultative facade stopped before readiness")
            try:
                if urlopen(url + "/api/v1/health", timeout=0.5).status == 200:
                    break
            except (OSError, URLError):
                time.sleep(.1)
        else:
            raise RuntimeError("Consultative facade not ready")
        yield url
    finally:
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)


def test_web_consultative_real_chromium_has_no_project_storage_and_runs_demo(consultative_url):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True, **(
            {"executable_path": os.environ["SIE_E2E_BROWSER_PATH"],
             "args": ["--no-zygote", "--single-process", "--disable-dev-shm-usage"]}
            if os.environ.get("SIE_E2E_BROWSER_PATH") else {}
        ))
        page = browser.new_page(viewport={"width": 1280, "height": 800})
        errors = []
        page.on("pageerror", lambda error: errors.append(str(error)))
        page.goto(consultative_url + "/", wait_until="networkidle")
        expect(page.locator(".warning")).to_contain_text("Não homologado")
        expect(page.locator("#api")).to_contain_text("Motor consultivo acessível")
        assert page.locator('input[type="password"]').count() == 0
        assert page.locator("#project-save").count() == 0
        assert "127.0.0.1:8000" not in page.content()
        page.locator("#execute").click()
        expect(page.locator("#state")).to_contain_text(
            "Análise demonstrativa concluída", timeout=12000
        )
        expect(page.locator("#results")).to_contain_text("NÃO HOMOLOGADO")
        assert page.evaluate("localStorage.length") == 0
        assert page.evaluate("sessionStorage.length") == 0
        negative = page.request.get(consultative_url + "/api/v1/local/projetos")
        assert negative.status == 404
        docs = page.request.get(consultative_url + "/docs")
        assert docs.status == 404
        assert not errors, errors
        browser.close()
