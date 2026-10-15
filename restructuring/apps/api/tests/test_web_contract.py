"""Lightweight regression for HTML/JS surface contracts, without browser dependency."""
from html.parser import HTMLParser
from pathlib import Path

WEB = Path(__file__).resolve().parents[2] / "web"


class IdCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if "id" in data:
            self.ids.add(data["id"])


def test_js_required_elements_exist_in_web_html():
    html = (WEB / "index.html").read_text(encoding="utf-8")
    parser = IdCollector()
    parser.feed(html)
    for element_id in (
        "health", "resultado", "analysis-form", "corrente",
        "project-status", "project-name", "project-id",
        "project-token", "project-revision", "project-save", "project-load",
    ):
        assert element_id in parser.ids, element_id


def test_no_user_normative_approval_controls():
    html = (WEB / "index.html").read_text(encoding="utf-8")
    assert 'name="dados_validados"' not in html
    assert 'name="testes_independentes"' not in html


def test_token_is_not_saved_in_web_storage():
    script = (WEB / "app.js").read_text(encoding="utf-8")
    assert "localStorage.setItem" not in script
    assert "sessionStorage.setItem" not in script
    assert "escapeHTML" in script


def test_f01_normative_governance_panel_is_explicitly_unverified():
    html = (WEB / "index.html").read_text(encoding="utf-8")
    parser = IdCollector()
    parser.feed(html)
    assert {"normas", "normas-status", "normas-lista"}.issubset(parser.ids)
    assert "nenhuma" in html.lower()
    js = (WEB / "app.js").read_text(encoding="utf-8")
    assert "/api/v1/normas/catalogo" in js
    assert "release_allowed !== false" in js
    assert "document.createElement('li')" in js
    assert "list.appendChild(item)" in js
    assert "item.innerHTML" not in js
