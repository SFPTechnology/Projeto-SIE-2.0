"""F12 Hostinger preflight tests use fake responses: zero live network traffic."""
import importlib.util
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[4]
SPEC = importlib.util.spec_from_file_location("hostinger_check", ROOT / "scripts/f12_hostinger_preflight.py")
host = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(host)


def test_hostinger_owner_supplied_url_is_only_allowed_origin():
    assert host.validate_target("https://sie2.applicationmanager.com.br/") == host.DEFAULT_URL
    for value in (
        "http://sie2.applicationmanager.com.br",
        "https://other.example",
        "https://sie2.applicationmanager.com.br@evil.example",
        "https://sie2.applicationmanager.com.br:8443",
        "https://sie2.applicationmanager.com.br/api/v1/health",
        "https://sie2.applicationmanager.com.br/?token=secret",
        "https://sie2.applicationmanager.com.br#secret",
    ):
        with pytest.raises(ValueError):
            host.validate_target(value)


def success_get(url):
    path = url.removeprefix(host.DEFAULT_URL)
    if path == "/":
        return 200, {
            "Content-Security-Policy": "default-src 'none'",
            "X-Frame-Options": "DENY",
            "X-Content-Type-Options": "nosniff",
        }, b"<html>AMBIENTE CONSULTIVO - NÃ£o homologado</html>"
    if path == "/api/v1/health":
        return 200, {"Content-Type": "application/json"}, (
            b'{"status":"ok","engineering_engine":"calculation_available_normative_release_disabled"}'
        )
    return 404, {"Content-Type": "application/json"}, b'{"detail":"Not Found"}'


def test_success_is_not_a_release_authorization():
    result = host.audit(host.DEFAULT_URL, fetch=success_get)
    assert result["status"] == "FACADE_READONLY_PROBE_PASSED"
    assert result["production_authorized"] is False
    assert result["hostinger_plan_verified"] is False
    assert result["staging_approved"] is False
    assert result["observed"]["/api/v1/local/projetos"]["http_status"] == 404


def test_old_site_or_exposed_persistence_blocks_the_audit():
    def unsafe(url):
        if url.endswith("/api/v1/local/projetos"):
            return 200, {}, b"[]"
        if url.endswith("/"):
            return 200, {}, b"<html>Old site</html>"
        return success_get(url)
    result = host.audit(host.DEFAULT_URL, fetch=unsafe)
    assert result["status"] == "UNVERIFIED_OR_NOT_READY"
    assert any("rota restrita" in finding for finding in result["findings"])
    assert any("não identificado" in finding for finding in result["findings"])
    assert result["production_authorized"] is False


def test_network_or_invalid_cert_is_not_a_false_positive():
    def unreachable(url):
        raise TimeoutError("network")
    report = host.audit(host.DEFAULT_URL, fetch=unreachable)
    assert len(report["observed"]) == 0
    assert report["status"] == "UNVERIFIED_OR_NOT_READY"
    assert not report["production_authorized"]


def test_default_cli_is_offline():
    process = subprocess.run(
        [sys.executable, str(ROOT / "scripts/f12_hostinger_preflight.py")],
        capture_output=True, text=True, check=False,
    )
    assert process.returncode == 0, process.stderr
    assert '"live_probe_executed": false' in process.stdout
    assert '"production_authorized": false' in process.stdout
