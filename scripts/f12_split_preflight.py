#!/usr/bin/env python3
"""F12 split-host preflight: Hostinger static frontend + external Python API.

Offline by default. --live requires both HTTPS origins and performs GET only.
Never deploys, contacts hPanel, changes DNS, tests POST, or grants a GO.
"""
import argparse
import json
import re
import ssl
from urllib import error, parse, request

SITE_DOMAIN = "applicationmanager.com.br"
DEFAULT_SITE = "https://sie2.applicationmanager.com.br"
MAX_BODY = 65536


def valid_origin(value, is_site=False):
    parts = parse.urlsplit(value)
    host = (parts.hostname or "").lower()
    if (parts.scheme != "https" or parts.username or parts.password
            or parts.port not in (None, 443) or parts.query or parts.fragment
            or parts.path not in ("", "/")
            or not re.fullmatch(r"[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+", host)):
        raise ValueError("Origem deve ser um hostname HTTPS sem caminho, porta extra ou segredo")
    if (is_site and host != SITE_DOMAIN and not host.endswith("." + SITE_DOMAIN)):
        raise ValueError("Site estático deve pertencer ao domínio Hostinger do titular")
    if not is_site and (host.endswith(".local") or host.endswith(".internal")
                        or host.endswith(".invalid")):
        raise ValueError("Origem externa de API deve possuir hostname público")
    return "https://" + host


class KeepSameOrigin(request.HTTPRedirectHandler):
    def __init__(self, origin):
        self.origin = origin

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if valid_origin(parse.urlunsplit((
                parse.urlsplit(newurl).scheme, parse.urlsplit(newurl).netloc, "", "", ""
        )), is_site=False) != self.origin:
            raise ValueError("Redirecionamento para outra origem foi recusado")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def get_readonly(url, origin):
    client = request.build_opener(
        KeepSameOrigin(origin), request.HTTPSHandler(context=ssl.create_default_context())
    )
    req = request.Request(url, method="GET", headers={
        "User-Agent": "SIE-F12-Split-ReadOnly/1", "Accept": "text/html,application/json,*/*"
    })
    try:
        with client.open(req, timeout=7) as response:
            return response.status, dict(response.headers), response.read(MAX_BODY + 1)
    except error.HTTPError as response:
        with response:
            return response.code, dict(response.headers), response.read(MAX_BODY + 1)


def audit(site_origin, api_origin, fetch=get_readonly):
    site = valid_origin(site_origin, is_site=True)
    api = valid_origin(api_origin)
    found, findings = {}, []
    checks = (
        ("frontend_html", site, "/"),
        ("frontend_js", site, "/consultivo.js"),
        ("frontend_css", site, "/consultivo.css"),
        ("backend_health", api, "/api/v1/health"),
        ("backend_local_forbidden", api, "/api/v1/local/projetos"),
        ("backend_docs_forbidden", api, "/docs"),
        ("backend_openapi_forbidden", api, "/openapi.json"),
    )
    for name, origin, path in checks:
        try:
            status, headers, body = fetch(origin + path, origin)
            if len(body) > MAX_BODY:
                findings.append(name + ": resposta excedeu o limite de leitura")
                continue
            found[name] = {"status": status}
            headers = {k.lower(): v for k, v in headers.items()}
            if name == "frontend_html":
                html = body.decode("utf-8", "replace")
                if status != 200 or "Não homologado" not in html or "AMBIENTE CONSULTIVO" not in html:
                    findings.append(name + ": portal consultivo não identificado")
                for header in ("content-security-policy", "x-content-type-options", "x-frame-options"):
                    if not headers.get(header):
                        findings.append(name + ": cabeçalho de proteção ausente " + header)
            elif name == "frontend_js":
                js = body.decode("utf-8", "replace")
                if status != 200 or ("SIE_F12_API_ORIGIN = " + json.dumps(api)) not in js:
                    findings.append(name + ": origem API esperada não foi encontrada no build")
            elif name == "frontend_css" and status != 200:
                findings.append(name + ": stylesheet indisponível")
            elif name == "backend_health":
                try:
                    payload = json.loads(body)
                except ValueError:
                    payload = {}
                if status != 200 or payload.get("status") != "ok":
                    findings.append(name + ": backend FastAPI não comprovado")
            elif name.startswith("backend_") and status != 404:
                findings.append(name + ": rota restrita não retornou 404")
        except (OSError, ValueError, ssl.SSLError, error.URLError, TimeoutError) as exc:
            findings.append(name + ": falha de consulta (" + type(exc).__name__ + ")")
    return {
        "schema": "SIE-F12-SPLIT-READONLY-1",
        "site_origin": site,
        "api_origin": api,
        "mode": "GET_ONLY",
        "observed": found,
        "status": "BASIC_READONLY_SMOKE_PASSED" if not findings else "UNVERIFIED_OR_NOT_READY",
        "findings": findings,
        "production_authorized": False,
        "staging_approved": False,
        "cors_preflight_verified": False,
        "synthetic_post_verified": False,
        "rate_limit_verified": False,
        "administrative_iam_verified": False,
        "observability_verified": False,
    }


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--site-origin", default=DEFAULT_SITE)
    p.add_argument("--api-origin", default="")
    p.add_argument("--live", action="store_true", help="Opt-in HTTPS GET only (no write/POST)")
    args = p.parse_args(argv)
    try:
        site = valid_origin(args.site_origin, is_site=True)
        api = valid_origin(args.api_origin) if args.api_origin else ""
        if args.live:
            if not api:
                raise ValueError("--live requer a URL HTTPS efetiva da API externa")
            result = audit(site, api)
            code = 0 if not result["findings"] else 2
        else:
            result = {"status": "OFFLINE_TARGET_VALIDATED", "site_origin": site,
                      "api_origin": api or None, "live_probe_executed": False,
                      "production_authorized": False}
            code = 0
    except ValueError as exc:
        result = {"status": "INVALID_TARGET", "error": str(exc), "production_authorized": False}
        code = 2
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
    return code


if __name__ == "__main__":
    raise SystemExit(main())
