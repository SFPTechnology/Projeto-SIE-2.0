"""Static safety checks for the isolated B01 browser authentication prototype."""
from pathlib import Path

WEB=Path(__file__).resolve().parents[3]/"web"


def test_login_page_is_development_only_and_accessible():
    html=(WEB/"auth-v201.html").read_text(encoding="utf-8")
    assert 'lang="pt-BR"' in html
    assert 'id="login-form"' in html
    assert 'id="signed-in"' in html
    assert 'role="status"' in html
    assert 'type="password"' in html
    assert "auth-v201.js" in html


def test_public_config_has_no_privileged_key_or_token():
    config=(WEB/"auth-v201.public-config.js").read_text(encoding="utf-8")
    assert 'publishableKey: ""' in config
    assert 'https://fozrymsidnaxmuvxxfhh.supabase.co' in config
    assert "eyJ" not in config


def test_browser_stores_bearer_only_in_memory_and_checks_backend_auth():
    js=(WEB/"auth-v201.js").read_text(encoding="utf-8")
    assert "localStorage" not in js
    assert "sessionStorage" not in js
    assert "document.cookie" not in js
    assert "auth/v1/token?grant_type=password" in js
    assert "/api/v2/sie/auth/me" in js
    assert "authorization_source" in js
    assert "BroadcastChannel" in js
    assert "location.origin" in js
    assert "apiAllowed" in js
