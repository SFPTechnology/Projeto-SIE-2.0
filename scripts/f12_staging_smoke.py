#!/usr/bin/env python3
"""Isolated HTTPS loopback smoke of *existing* SIE API, not a production test.

Creates a short-lived self-signed certificate, serves synthetic traffic on
127.0.0.1, confirms the dev-only persistence API remains inaccessible when
SIE_ENV=production. Does not validate enterprise IAM or public TLS.
"""
import argparse
import json
import os
from pathlib import Path
import socket
import ssl
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from uuid import UUID

PROJECT_ID = "00000000-0000-0000-0000-000000000001"


def ephemeral_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def fetch(url, context, method="GET", payload=None):
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(url, method=method, data=data,
                                     headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=3, context=context) as response:
            return response.status, json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return exc.code, json.loads(exc.read().decode("utf-8"))


def run():
    with tempfile.TemporaryDirectory(prefix="sie-f12-https-test-") as work:
        folder = Path(work)
        cert, key = folder / "staging.crt", folder / "staging.key"
        subprocess.run([
            "openssl", "req", "-x509", "-newkey", "rsa:2048", "-sha256",
            "-nodes", "-days", "1", "-subj", "/CN=localhost",
            "-addext", "subjectAltName=DNS:localhost,IP:127.0.0.1",
            "-keyout", str(key), "-out", str(cert)
        ], capture_output=True, check=True)
        key.chmod(0o600)
        port = ephemeral_port()
        environment = dict(os.environ)
        environment["SIE_ENV"] = "production"
        environment.pop("SIE_LOCAL_DB_PATH", None)
        environment.pop("SIE_LOCAL_API_TOKEN", None)
        proc = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "sie_api.main:app",
            "--host", "127.0.0.1", "--port", str(port),
            "--ssl-certfile", str(cert), "--ssl-keyfile", str(key)
        ], env=environment, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            ctx = ssl.create_default_context(cafile=str(cert))
            origin = f"https://127.0.0.1:{port}"
            for _ in range(45):
                if proc.poll() is not None:
                    raise RuntimeError("Test server exited before readiness")
                try:
                    code, health = fetch(origin + "/api/v1/health", ctx)
                    if code == 200:
                        break
                except (OSError, ValueError):
                    time.sleep(0.2)
            else:
                raise RuntimeError("HTTPS loopback health failed")
            assert health["status"] == "ok"
            assert health["engineering_engine"] == "calculation_available_normative_release_disabled"
            code, body = fetch(origin + "/api/v1/local/projetos/" + PROJECT_ID, ctx)
            assert code == 503 and "desabilitada" in body["detail"]
            code, body = fetch(origin + "/api/v1/projetos/validar", ctx, method="POST",
                               payload={"nome": "Synthetic F12", "circuitos": []})
            assert code == 200
            assert body["validacao_normativa"] == "nao_realizada"
            return {
                "status": "PASS_LOCAL_HTTPS_SYNTHETIC",
                "https_trusted_local_self_signed": True,
                "local_storage_disabled_in_production_mode": True,
                "normative_conformity_verified": False,
                "production_iam_tested": False,
                "public_tls_tested": False,
                "real_deployment_executed": False,
                "production_authorized": False
            }
        finally:
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()
                proc.wait(timeout=5)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args(argv)
    report = run()
    output = json.dumps(report, sort_keys=True, indent=2) + "\n"
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(output, encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
