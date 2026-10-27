#!/usr/bin/env python3
"""Build deterministic, static-only SIE F12 Hostinger preview (NO DEPLOY).

Ships HTML/CSS/JS only. Python calculation engines remain on a separate HTTPS
service if one is approved. Empty API origin disables calculation safely.
"""
import argparse
import hashlib
import ipaddress
import json
from pathlib import Path
import re
from urllib.parse import urlsplit
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "docs/implantacao-sie-2-0/F12/consultivo-web"
HOST = "sie2.applicationmanager.com.br"
FILES = ("index.html", "consultivo.css", "consultivo.js")
SHA_DATE = (1980, 1, 1, 0, 0, 0)
ZIP_NAME = "sie-f12-hostinger-static-preview.zip"


def validate_api_origin(value):
    if not value:
        return ""
    parts = urlsplit(value)
    host = parts.hostname or ""
    if (parts.scheme != "https" or parts.username or parts.password
        or parts.path not in ("", "/") or parts.query or parts.fragment
        or parts.port not in (None, 443) or not host or len(host) > 253):
        raise ValueError("Origem da API precisa ser um host HTTPS sem credenciais, portas extras ou caminhos")
    try:
        ipaddress.ip_address(host)
    except ValueError:
        pass
    else:
        raise ValueError("Use um hostname público, não um IP")
    if (host.lower() in ("localhost", "host.docker.internal") or host.endswith(".local")
        or not re.fullmatch(r"[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+", host)):
        raise ValueError("Hostname público de API inválido")
    return "https://" + host.lower()


def validate_site_origin(value):
    """Prevent staging artifacts redirecting to unapproved external hosts."""
    origin = validate_api_origin(value)
    if not origin:
        raise ValueError("Informe origem HTTPS de staging ou produção")
    host = urlsplit(origin).hostname
    if host != HOST and not host.endswith(".applicationmanager.com.br"):
        raise ValueError("Origem estática fora do domínio autorizado")
    return origin


def html(src):
    marker = '<script defer src="/consultivo.js"></script>'
    if marker not in src or 'href="/consultivo.css"' not in src:
        raise ValueError("Template HTML alterado sem revisão F12")
    return src.replace('href="/consultivo.css"', 'href="./consultivo.css"').replace(
        marker, '<script defer src="./consultivo.js"></script>'
    ).encode("utf-8")


def client_js(src, api_origin):
    if 'fetch(path, {cache:' not in src or not src.rstrip().endswith('health();'):
        raise ValueError("Template JavaScript mudou; revisar adaptador de hospedagem estática")
    head = (
        '"use strict";\n'
        '// Backend externo configurado no build, sem dados sigilosos.\n'
        'const SIE_F12_API_ORIGIN = ' + json.dumps(api_origin) + ';\n'
        'function apiURL(path) {\n'
        '  if (!SIE_F12_API_ORIGIN) throw new Error("API não configurada");\n'
        '  return SIE_F12_API_ORIGIN + path;\n'
        '}\n'
    )
    js = src.replace('"use strict";\n', head, 1).replace(
        'fetch(path, {cache:', 'fetch(apiURL(path), {cache:', 1
    )
    js = js[:js.rfind('health();')] + (
        'if (!SIE_F12_API_ORIGIN) {\n'
        '  submit.disabled = true;\n'
        '  $("api").textContent = "Prévia estática: API Python não configurada.";\n'
        '  state.textContent = "Simulação indisponível até conectar API aprovada.";\n'
        '} else { health(); }\n'
    )
    return js.encode("utf-8")


def htaccess(api_origin, site_origin):
    csp = "default-src 'none'; script-src 'self'; style-src 'self'; "
    csp += "connect-src " + (api_origin if api_origin else "'none'") + "; "
    csp += "img-src 'self'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'"
    return (
        "# F12 site estático; testar suporte do Apache/Hostinger antes do GO\n"
        "<IfModule mod_headers.c>\n"
        'Header always set Content-Security-Policy "' + csp + '"\n'
        'Header always set X-Frame-Options "DENY"\n'
        'Header always set X-Content-Type-Options "nosniff"\n'
        'Header always set Referrer-Policy "no-referrer"\n'
        'Header always set Cache-Control "no-store"\n'
        "</IfModule>\n"
        "<IfModule mod_rewrite.c>\n"
        "RewriteEngine On\n"
        "RewriteCond %{HTTPS} !=on\n"
        "RewriteRule ^ " + site_origin + "%{REQUEST_URI} [R=302,L]\n"
        "</IfModule>\n"
    ).encode("utf-8")


def build(out, origin="", site_origin="https://" + HOST):
    origin = validate_api_origin(origin)
    site_origin = validate_site_origin(site_origin)
    out = Path(out)
    if out.exists() and any(out.iterdir()):
        raise FileExistsError("Diretório de saída precisa estar vazio")
    sources = {name: (SOURCE / name).read_text(encoding="utf-8") for name in FILES}
    contents = {
        "index.html": html(sources["index.html"]),
        "consultivo.js": client_js(sources["consultivo.js"], origin),
        "consultivo.css": sources["consultivo.css"].encode("utf-8"),
        ".htaccess": htaccess(origin, site_origin),
    }
    manifest = {
        "schema": "SIE-F12-HOSTINGER-STATIC-1",
        "deployment": "QA_PREVIEW_ONLY",
        "production_authorized": False,
        "host": urlsplit(site_origin).hostname,
        "site_origin": site_origin,
        "api_origin": origin or None,
        "features": ["stateless_consultative_ui"],
        "backend_required_for_calculation": True,
        "files": [
            {"path": p, "size": len(contents[p]),
             "sha256": hashlib.sha256(contents[p]).hexdigest()}
            for p in sorted(contents)
        ],
    }
    contents["MANIFEST.json"] = (json.dumps(manifest, ensure_ascii=False, sort_keys=True,
                             separators=(",", ":")) + "\n").encode("utf-8")
    out.mkdir(parents=True, exist_ok=True)
    zip_file = out / ZIP_NAME
    with zipfile.ZipFile(zip_file, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name in sorted(contents):
            info = zipfile.ZipInfo(name, SHA_DATE)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            archive.writestr(info, contents[name], compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    sha = hashlib.sha256(zip_file.read_bytes()).hexdigest()
    (out / (ZIP_NAME + ".sha256")).write_text(sha + "  " + ZIP_NAME + "\n", encoding="ascii")
    (out / "MANIFEST.json").write_bytes(contents["MANIFEST.json"])
    return {"status": "QA_PREVIEW_BUILT_NOT_DEPLOYED", "file_count": len(contents),
            "sha256": sha, "api_connected": bool(origin), "production_authorized": False}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--api-origin", default="",
                        help="HTTPS origin of separately approved Python backend; omit to disable calculations")
    parser.add_argument("--site-origin", default="https://" + HOST,
                        help="Exact HTTPS staging/production static origin")
    args = parser.parse_args(argv)
    print(json.dumps(build(args.out, args.api_origin, args.site_origin), sort_keys=True))


if __name__ == "__main__":
    main()
