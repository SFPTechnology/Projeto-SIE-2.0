"""Offline tests for deterministic Hostinger static preview package."""
import importlib.util
import json
from pathlib import Path
import zipfile

import pytest

ROOT = Path(__file__).resolve().parents[4]
SPEC = importlib.util.spec_from_file_location("hostinger_static", ROOT / "scripts/f12_hostinger_static.py")
package = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(package)


def test_static_disabled_without_approved_backend(tmp_path):
    result = package.build(tmp_path / "package")
    assert result["api_connected"] is False
    assert result["production_authorized"] is False
    with zipfile.ZipFile(tmp_path / "package" / package.ZIP_NAME) as zf:
        names = set(zf.namelist())
        assert names == {"index.html", "consultivo.js", "consultivo.css", ".htaccess", "MANIFEST.json"}
        html = zf.read("index.html").decode()
        js = zf.read("consultivo.js").decode()
        config = json.loads(zf.read("MANIFEST.json"))
        assert "./consultivo.js" in html and "./consultivo.css" in html
        assert "https://" not in js
        assert 'SIE_F12_API_ORIGIN = ""' in js
        assert "submit.disabled = true" in js
        assert config["deployment"] == "QA_PREVIEW_ONLY"
        assert not any(name.endswith((".py", ".db", ".sqlite", ".env")) for name in names)


def test_deterministic_bytes_checksum_and_csp(tmp_path):
    a = package.build(tmp_path / "a", "https://api.example.net/")
    b = package.build(tmp_path / "b", "https://api.example.net")
    ap = tmp_path / "a" / package.ZIP_NAME
    bp = tmp_path / "b" / package.ZIP_NAME
    assert ap.read_bytes() == bp.read_bytes()
    assert (tmp_path / "a" / (package.ZIP_NAME + ".sha256")).read_bytes() == (
        tmp_path / "b" / (package.ZIP_NAME + ".sha256")).read_bytes()
    with zipfile.ZipFile(ap) as zf:
        config = json.loads(zf.read("MANIFEST.json"))
        assert config["api_origin"] == "https://api.example.net"
        assert b"connect-src https://api.example.net;" in zf.read(".htaccess")
        assert b"SIE_F12_API_ORIGIN" in zf.read("consultivo.js")
        assert config["production_authorized"] is False


@pytest.mark.parametrize("url", [
    "http://api.example.net", "https://localhost", "https://127.0.0.1",
    "https://api.example.net:8000", "https://api.example.net/path",
    "https://user:pass@api.example.net", "https://api.example.net/?token=secret",
    "https://api.example.net#fragment", "https://example.local", "javascript:alert(1)",
])
def test_reject_insecure_api_target(url):
    with pytest.raises(ValueError):
        package.validate_api_origin(url)


def test_does_not_overwrite_existing_destination(tmp_path):
    path = tmp_path / "published-site"
    path.mkdir()
    (path / "index.html").write_text("original", encoding="utf-8")
    with pytest.raises(FileExistsError):
        package.build(path)
    assert (path / "index.html").read_text(encoding="utf-8") == "original"


def test_staging_redirect_and_artifact_are_isolated(tmp_path):
    stage = "https://sie2-homologacao.applicationmanager.com.br"
    package.build(tmp_path / "a", "https://api.example.net", stage)
    package.build(tmp_path / "b", "https://api.example.net/", stage + "/")
    a = tmp_path / "a" / package.ZIP_NAME
    assert a.read_bytes() == (tmp_path / "b" / package.ZIP_NAME).read_bytes()
    with zipfile.ZipFile(a) as zf:
        rules = zf.read(".htaccess").decode()
        data = json.loads(zf.read("MANIFEST.json"))
        assert "RewriteRule ^ " + stage + "%{REQUEST_URI}" in rules
        assert "RewriteRule ^ https://sie2.applicationmanager.com.br" not in rules
        assert data["site_origin"] == stage
        assert data["production_authorized"] is False


@pytest.mark.parametrize("origin", [
    "", "http://sie2-homologacao.applicationmanager.com.br",
    "https://evil.example", "https://localhost",
    "https://sie2-homologacao.applicationmanager.com.br:5000",
    "https://sie2-homologacao.applicationmanager.com.br/path",
    "https://*.applicationmanager.com.br"
])
def test_staging_rejects_unsafe_redirect_origin(origin):
    with pytest.raises(ValueError):
        package.validate_site_origin(origin)
