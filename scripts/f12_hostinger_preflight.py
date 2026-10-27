#!/usr/bin/env python3
"""Read-only SIE F12 host fingerprint. Never deploys or grants production.

Without --live, validates the target argument only: CI must not make external
requests. --live performs GET requests only against the owner-supplied HTTPS
host, without secrets, login, file writes, POST or redirecting off the host.
"""
import argparse
import json
import ssl
from urllib import error, parse, request

DEFAULT_URL = "https://sie2.applicationmanager.com.br"
EXPECTED_HOST = "sie2.applicationmanager.com.br"
MAX_BODY = 65536
PATHS = (
    "/",
    "/api/v1/health",
    "/api/v1/local/projetos",
    "/docs",
    "/openapi.json",
)


def validate_target(value):
    parts = parse.urlsplit(value)
    if (parts.scheme != "https" or parts.hostname != EXPECTED_HOST
            or parts.port not in (None, 443)
            or parts.username or parts.password
            or parts.path not in ("", "/") or parts.query or parts.fragment):
        raise ValueError("Somente a origem HTTPS exata do SIE cadastrada e permitida")
    return f"https://{EXPECTED_HOST}"


class SameHostHTTPS(request.HTTPRedirectHandler):
    """Never follow a redirect to another host or an insecure scheme."""
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        parts = parse.urlsplit(newurl)
        if parts.scheme != "https" or parts.hostname != EXPECTED_HOST or parts.port not in (None, 443):
            raise ValueError("Redirect fora da origem HTTPS cadastrada")
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch_readonly(url):
    client = request.build_opener(
        SameHostHTTPS(), request.HTTPSHandler(context=ssl.create_default_context())
    )
    req = request.Request(url, headers={"User-Agent": "SIE-F12-ReadOnly-Preflight/1", "Accept": "application/json,text/html,*/*"},
                          method="GET")
    try:
        with client.open(req, timeout=7) as response:
            return response.status, dict(response.headers), response.read(MAX_BODY + 1)
    except error.HTTPError as response:
        with response:
            return response.code, dict(response.headers), response.read(MAX_BODY + 1)


def audit(base, fetch=fetch_readonly):
    base = validate_target(base)
    found = {}
    findings = []
    for path in PATHS:
        try:
            status, headers, body = fetch(base + path)
            if len(body) > MAX_BODY:
                findings.append(path + ": resposta excedeu limite de leitura")
                continue
            headers = {k.lower(): v for k, v in headers.items()}
            found[path] = {"http_status": status}
            if path == "/":
                html = body.decode("utf-8", "replace")
                if status != 200 or "AMBIENTE CONSULTIVO" not in html or "Não homologado" not in html:
                    findings.append("/: não identificado o portal consultivo F12 esperado")
                for header in ("content-security-policy", "x-content-type-options", "x-frame-options"):
                    if not headers.get(header):
                        findings.append("/: cabeçalho ausente: " + header)
            elif path == "/api/v1/health":
                try:
                    payload = json.loads(body)
                except (ValueError, UnicodeError):
                    payload = {}
                if (status != 200 or payload.get("status") != "ok"
                    or payload.get("engineering_engine") != "calculation_available_normative_release_disabled"):
                    findings.append("/api/v1/health: contrato consultivo não comprovado")
            elif status != 404:
                findings.append(path + ": rota restrita não retornou 404")
        except (OSError, ValueError, ssl.SSLError, error.URLError, TimeoutError) as exc:
            findings.append(path + ": verificação não concluída (" + type(exc).__name__ + ")")
    if len(found) != len(PATHS):
        findings.append("Uma ou mais respostas HTTPS não puderam ser verificadas")
    return {
        "schema": "SIE-F12-HOSTINGER-READONLY-1",
        "origin": base, "method": "GET_ONLY",
        "observed": found,
        "status": "FACADE_READONLY_PROBE_PASSED" if not findings else "UNVERIFIED_OR_NOT_READY",
        "findings": findings,
        "production_authorized": False,
        "staging_approved": False,
        "technical_normative_approval": False,
        "hostinger_plan_verified": False,
        "admin_iam_verified": False,
        "ingress_rate_limit_verified": False,
        "monitoring_verified": False,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default=DEFAULT_URL)
    parser.add_argument("--live", action="store_true",
                        help="Opt-in: perform read-only HTTPS requests to the exact owner-supplied hostname")
    args = parser.parse_args(argv)
    try:
        origin = validate_target(args.url)
        if args.live:
            result = audit(origin)
            exit_status = 0 if not result["findings"] else 2
        else:
            result = {"status": "TARGET_CONFIG_VALIDATED_NO_NETWORK",
                      "origin": origin, "production_authorized": False,
                      "live_probe_executed": False}
            exit_status = 0
    except ValueError as exc:
        result, exit_status = {"status": "INVALID_TARGET", "reason": str(exc),
                               "production_authorized": False}, 2
    print(json.dumps(result, sort_keys=True, ensure_ascii=False, indent=2))
    return exit_status


if __name__ == "__main__":
    raise SystemExit(main())
