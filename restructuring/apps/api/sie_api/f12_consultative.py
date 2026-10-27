"""F12 web consultative preview: narrow stateless read/calculation API only.

This entrypoint is deliberately NOT the local project app. It does not expose
project persistence, uploaded plans, artifact generation, administrative docs,
or client accounts. Never equate passing its CI with authorization to deploy.
"""
import os
from pathlib import Path
from urllib.parse import urlsplit
import re

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.routing import APIRoute

from .main import app as internal_application

# Strict method/path map. Every addition requires explicit security review.
PUBLIC_ENDPOINTS = frozenset({
    ("GET", "/api/v1/health"),
    ("POST", "/api/v1/circuitos/analisar"),
})
ASSETS = frozenset({"/", "/index.html", "/consultivo.js", "/consultivo.css"})
BODY_LIMIT = 1024 * 1024
DEFAULT_ROOT = Path(__file__).resolve().parents[4] / "docs/implantacao-sie-2-0/F12/consultivo-web"

app = FastAPI(
    title="SIE 2.0 — demonstração consultiva (sem homologação normativa)",
    docs_url=None, redoc_url=None, openapi_url=None,
)

for route in internal_application.routes:
    if isinstance(route, APIRoute) and any(
        (method, route.path) in PUBLIC_ENDPOINTS for method in route.methods
    ):
        if any((method, route.path) not in PUBLIC_ENDPOINTS for method in route.methods):
            raise RuntimeError("Método excedente em rota consultiva")
        app.router.routes.append(route)

if {(m, r.path) for r in app.routes if isinstance(r, APIRoute)
    for m in r.methods} != PUBLIC_ENDPOINTS:
    raise RuntimeError(f"Contrato consultivo divergente: observado={[(r.path, sorted(r.methods)) for r in app.routes if isinstance(r, APIRoute)]!r}; esperado={PUBLIC_ENDPOINTS!r}")


@app.middleware("http")
async def safety_boundary(request: Request, call_next):
    path = request.url.path
    method = request.method
    if path not in ASSETS and (method, path) not in PUBLIC_ENDPOINTS:
        response = JSONResponse({"detail": "Recurso não disponível na versão consultiva"}, status_code=404)
    elif path in ASSETS and method != "GET":
        response = JSONResponse({"detail": "Método não permitido"}, status_code=405)
    elif method == "POST" and request.headers.get("content-type", "").split(";", 1)[0].strip().lower() != "application/json":
        response = JSONResponse({"detail": "Somente JSON"}, status_code=415)
    elif method == "POST" and (request.headers.get("content-length", "").isdigit() and int(request.headers["content-length"]) > BODY_LIMIT):
        response = JSONResponse({"detail": "Requisição acima do limite"}, status_code=413)
    else:
        response = await call_next(request)
    response.headers["Cache-Control"] = "no-store"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Content-Security-Policy"] = (
        "default-src 'none'; script-src 'self'; style-src 'self'; connect-src 'self';"
        " img-src 'self'; form-action 'self'; base-uri 'none'; frame-ancestors 'none'"
    )
    return response


def web_root():
    return Path(os.environ.get("SIE_F12_WEB_ROOT", str(DEFAULT_ROOT))).resolve()


@app.get("/", include_in_schema=False)
@app.get("/index.html", include_in_schema=False)
async def landing():
    return FileResponse(web_root() / "index.html", media_type="text/html; charset=utf-8")


@app.get("/consultivo.js", include_in_schema=False)
async def javascript():
    return FileResponse(web_root() / "consultivo.js", media_type="text/javascript; charset=utf-8")


@app.get("/consultivo.css", include_in_schema=False)
async def stylesheet():
    return FileResponse(web_root() / "consultivo.css", media_type="text/css; charset=utf-8")


# Allow browsers on the owner's existing static Hostinger subdomain to call
# only the stateless API. Requests from arbitrary third-party origins never
# receive CORS permission. CORS is NOT rate limiting or authentication.
DEFAULT_PUBLIC_ORIGIN = "https://sie2.applicationmanager.com.br"


def browser_allowed_origins():
    """An invalid staging origin fails app import rather than widening CORS."""
    staging = os.environ.get("SIE_F12_STAGING_ORIGIN", "").strip()
    if not staging:
        return [DEFAULT_PUBLIC_ORIGIN]
    parts = urlsplit(staging)
    hostname = (parts.hostname or "").lower()
    if (parts.scheme != "https" or parts.username or parts.password
            or parts.port not in (None, 443)
            or parts.path not in ("", "/") or parts.query or parts.fragment
            or not hostname.endswith(".applicationmanager.com.br")
            or not re.fullmatch(r"[a-zA-Z0-9-]+(?:\\.[a-zA-Z0-9-]+)+", hostname)):
        raise ValueError("SIE_F12_STAGING_ORIGIN precisa ser subdomínio HTTPS exato")
    origin = "https://" + hostname
    return [DEFAULT_PUBLIC_ORIGIN] if origin == DEFAULT_PUBLIC_ORIGIN else [DEFAULT_PUBLIC_ORIGIN, origin]


app.add_middleware(
    CORSMiddleware,
    allow_origins=browser_allowed_origins(),
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
    allow_credentials=False,
    max_age=600,
)
