"""Split static+API F12 checker: mock all network operations."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import pytest

ROOT = Path(__file__).resolve().parents[4]
SPEC = importlib.util.spec_from_file_location("f12_split", ROOT / "scripts/f12_split_preflight.py")
split = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(split)
SITE = "https://sie2-homologacao.applicationmanager.com.br"
API = "https://backend.example.net"


def fixture(url, origin):
    if url == SITE + "/":
        return 200, {"Content-Security-Policy": "default-src 'none'",
                     "X-Frame-Options": "DENY", "X-Content-Type-Options": "nosniff"}, (
                     "<html>AMBIENTE CONSULTIVO · Não homologado</html>".encode("utf-8"))
    if url == SITE + "/consultivo.js":
        return 200, {}, ('const SIE_F12_API_ORIGIN = "' + API + '";').encode()
    if url == SITE + "/consultivo.css":
        return 200, {}, b"body{}"
    if url == API + "/api/v1/health":
        return 200, {}, b'{"status":"ok"}'
    return 404, {}, b"{}"


def test_split_preview_is_readonly_smoke_not_production_go():
    r = split.audit(SITE, API, fixture)
    assert r["status"] == "BASIC_READONLY_SMOKE_PASSED", r["findings"]
    assert len(r["observed"]) == 7
    assert r["production_authorized"] is False
    assert r["cors_preflight_verified"] is False
    assert r["synthetic_post_verified"] is False


def test_backend_private_route_open_causes_fail_closed():
    def unsafe(url, origin):
        if url.endswith("/api/v1/local/projetos"):
            return 200, {}, b"[]"
        return fixture(url, origin)
    r = split.audit(SITE, API, unsafe)
    assert r["status"] == "UNVERIFIED_OR_NOT_READY"
    assert any("restrita" in x for x in r["findings"])


def test_frontend_is_bound_to_matching_backend_origin():
    def wrong_js(url, origin):
        if url.endswith("/consultivo.js"):
            return 200, {}, b'const SIE_F12_API_ORIGIN = "https://wrong.example";'
        return fixture(url, origin)
    r = split.audit(SITE, API, wrong_js)
    assert any("origem API" in x for x in r["findings"])


@pytest.mark.parametrize("site,api", [
    ("http://sie2.applicationmanager.com.br", API),
    ("https://evil.example.net", API),
    (SITE, "http://backend.example.net"),
    (SITE, "https://localhost"),
    (SITE, "https://127.0.0.1"),
    (SITE, "https://10.1.2.3"),
    (SITE, "https://server.localdomain"),
    (SITE, "https://backend.example.net/private"),
    (SITE, "https://backend.example.net:8080"),
    (SITE, "https://attacker@backend.example.net"),
])
def test_reject_bad_origins(site, api):
    with pytest.raises(ValueError):
        split.audit(site, api, fixture)


def test_offline_default_cli_makes_no_network_requests():
    r = subprocess.run([sys.executable, str(ROOT / "scripts/f12_split_preflight.py")],
                       capture_output=True, text=True, check=False)
    assert r.returncode == 0
    data = json.loads(r.stdout)
    assert data["status"] == "OFFLINE_TARGET_VALIDATED"
    assert data["live_probe_executed"] is False


def test_live_requires_both_origins():
    r = subprocess.run([sys.executable, str(ROOT / "scripts/f12_split_preflight.py"), "--live"],
                       capture_output=True, text=True, check=False)
    assert r.returncode == 2
    assert json.loads(r.stdout)["status"] == "INVALID_TARGET"
