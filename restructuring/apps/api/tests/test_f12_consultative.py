"""Public consultative deployment boundary, independent from local F11 API."""
from fastapi.testclient import TestClient

from sie_api.f12_consultative import app, PUBLIC_ENDPOINTS

client = TestClient(app)
SYNTHETIC = {
    "corrente_a": 20, "comprimento_m": 30, "tensao_v": 220,
    "resistencia_ohm_km": 7.41, "fator_correcao": 0.8,
    "tabela_condutores": [
        {"secao_mm2": 2.5, "capacidade_a": 24},
        {"secao_mm2": 4, "capacidade_a": 32},
        {"secao_mm2": 6, "capacidade_a": 41},
        {"secao_mm2": 10, "capacidade_a": 57},
    ],
    "evidencia": {"documento": "F12 demo", "edicao": "DEMO", "referencia": "fictício"},
}


def test_landing_page_warnings_and_same_origin_js():
    page = client.get("/")
    assert page.status_code == 200
    assert "Não homologado" in page.text
    assert 'href="/consultivo.css"' in page.text
    assert 'src="/consultivo.js"' in page.text
    script = client.get("/consultivo.js")
    assert script.status_code == 200
    assert 'json("/api/v1/circuitos/analisar"' in script.text
    assert "localStorage" not in script.text
    assert "Bearer " not in script.text
    assert client.get("/consultivo.css").status_code == 200


def test_stateless_health_and_no_normative_approval():
    health = client.get("/api/v1/health")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"
    response = client.post("/api/v1/circuitos/analisar", json=SYNTHETIC)
    assert response.status_code == 200, response.text
    assert response.json()["liberado_para_uso_normativo"] is False
    assert client.get("/api/v1/normas/catalogo").status_code == 404


def test_never_expose_local_db_or_artifacts_even_with_configured_local_token(monkeypatch):
    monkeypatch.setenv("SIE_ENV", "dev")
    monkeypatch.setenv("SIE_LOCAL_API_TOKEN", "some-local-token-private-and-long")
    monkeypatch.setenv("SIE_LOCAL_DB_PATH", "/tmp/unused-f12-database.db")
    paths = [
        "/api/v1/local/projetos",
        "/api/v1/local/projetos/00000000-0000-0000-0000-000000000001",
        "/api/v1/local/projetos/00000000-0000-0000-0000-000000000001/f10/artifacts",
        "/api/v1/modelo/snapshots",
        "/api/v1/projetos/validar",
        "/docs", "/redoc", "/openapi.json", "/.env", "/.git/config",
        "/artefatos.html", "/index.php",
    ]
    for path in paths:
        response = client.get(path, headers={"Authorization": "Bearer some-local-token-private-and-long"})
        assert response.status_code == 404, (path, response.status_code)
    assert client.post("/api/v1/modelo/snapshots", json={}).status_code == 404
    assert client.post("/api/v1/projetos/validar", json={}).status_code == 404
    assert not client.get("/api/v1/health").json().get("production_authorized")


def test_strict_methods_type_and_size():
    assert PUBLIC_ENDPOINTS == {
        ("GET", "/api/v1/health"),
        ("POST", "/api/v1/circuitos/analisar"),
    }
    assert client.post("/api/v1/health").status_code == 404
    assert client.put("/api/v1/circuitos/analisar", json={}).status_code == 404
    assert client.post("/api/v1/circuitos/analisar", data="hi",
                       headers={"Content-Type": "text/plain"}).status_code == 415
    assert client.post("/api/v1/circuitos/analisar", data="x" * (1024 * 1024 + 1),
                       headers={"Content-Type": "application/json"}).status_code == 413


def test_security_headers_and_no_cors_data_leak():
    response = client.get("/")
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["content-security-policy"].startswith("default-src 'none'")
    assert response.headers["cache-control"] == "no-store"
    r = client.options("/api/v1/circuitos/analisar", headers={
        "Origin": "https://attacker.invalid", "Access-Control-Request-Method": "POST"
    })
    assert r.status_code != 200
    assert "access-control-allow-origin" not in r.headers


def test_hostinger_static_origin_can_call_stateless_api_only():
    origin = "https://sie2.applicationmanager.com.br"
    preflight = client.options("/api/v1/circuitos/analisar", headers={
        "Origin": origin, "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "content-type",
    })
    assert preflight.status_code == 200
    assert preflight.headers["access-control-allow-origin"] == origin
    response = client.post("/api/v1/circuitos/analisar",
                           json=SYNTHETIC, headers={"Origin": origin})
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == origin
    assert response.json()["liberado_para_uso_normativo"] is False
    denied = client.options("/api/v1/circuitos/analisar", headers={
        "Origin": "https://evil.example", "Access-Control-Request-Method": "POST",
    })
    assert denied.status_code == 400
    assert "access-control-allow-origin" not in denied.headers
    assert client.get("/api/v1/local/projetos",
                      headers={"Origin": origin}).status_code == 404


def test_stage_origin_configuration_rejects_insecure_values(monkeypatch):
    from sie_api.f12_consultative import browser_allowed_origins
    prod = "https://sie2.applicationmanager.com.br"
    stage = "https://sie2-homologacao.applicationmanager.com.br"
    monkeypatch.delenv("SIE_F12_STAGING_ORIGIN", raising=False)
    assert browser_allowed_origins() == [prod]
    monkeypatch.setenv("SIE_F12_STAGING_ORIGIN", stage)
    assert browser_allowed_origins() == [prod, stage]
    for origin in ("*", "http://sie2-homologacao.applicationmanager.com.br",
                   "https://evil.example", "https://localhost",
                   "https://sie2-homologacao.applicationmanager.com.br/path",
                   "https://sie2-homologacao.applicationmanager.com.br:444"):
        monkeypatch.setenv("SIE_F12_STAGING_ORIGIN", origin)
        with __import__("pytest").raises(ValueError):
            browser_allowed_origins()


def test_stage_cors_only_on_explicit_process_configuration():
    import os
    import subprocess
    import sys
    stage = "https://sie2-homologacao.applicationmanager.com.br"
    code = (
        "from fastapi.testclient import TestClient; from sie_api.f12_consultative import app;"
        "c=TestClient(app);r=c.options('/api/v1/circuitos/analisar',headers={"
        "'Origin':" + repr(stage) + ",'Access-Control-Request-Method':'POST',"
        "'Access-Control-Request-Headers':'content-type'});"
        "assert r.status_code==200 and r.headers['access-control-allow-origin']==" + repr(stage) + ";"
        "r=c.options('/api/v1/circuitos/analisar',headers={"
        "'Origin':'https://evil.example','Access-Control-Request-Method':'POST'});"
        "assert r.status_code==400 and 'access-control-allow-origin' not in r.headers"
    )
    run = subprocess.run([sys.executable, "-c", code],
                         env={**os.environ, "SIE_F12_STAGING_ORIGIN": stage},
                         capture_output=True, text=True, timeout=15, check=False)
    assert run.returncode == 0, run.stdout + run.stderr


def test_streamed_request_without_content_length_still_has_hard_limit():
    def body():
        yield b'{"padding":"'
        yield b"x" * (1024 * 1024 + 10)
        yield b'"}'
    result = client.post("/api/v1/circuitos/analisar", content=body(),
                         headers={"Content-Type": "application/json",
                                  "Transfer-Encoding": "chunked"})
    assert result.status_code == 413
    assert result.json()["detail"] == "Requisição acima do limite"
