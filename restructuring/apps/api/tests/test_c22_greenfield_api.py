from hashlib import sha256
import json

from fastapi.testclient import TestClient
from sie_api.main import app


def digest(payload):
    return sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def test_aggregate_is_synthetic_and_never_releases_normative_use():
    evidence = {"x": "synthetic"}
    response = TestClient(app).post("/api/v1/greenfield/e01-e11/evaluate", json={
        "e01_e05": {"room": {"area_m2": 10, "perimeter_m": 12, "type": "TEST"},
                    "loads": [{"kind": "TUE", "value": 1, "unit": "KVA", "power_factor": None}],
                    "voltage_v": 220, "phase_mode": "SINGLE"},
        "e11_payload": evidence, "e11_expected_sha256": digest(evidence),
        "e11_catalog_version": "synthetic-v1",
    })
    assert response.status_code == 200
    body = response.json()
    assert body["scope"] == "GREENFIELD_SYNTHETIC_ONLY"
    assert body["status"] == "PENDING_EVIDENCE"
    assert body["liberado_para_uso_normativo"] is False
    assert body["release_allowed"] is False
    assert body["checks"]["E01_E05"]["status"] == "PENDING_EVIDENCE"
    assert body["checks"]["E06"]["status"] == "BLOCKED"
    assert body["deferred"]["E10"] == "DEFERRED_OPTIONAL_LEGACY_IMPORT_ONLY"


def test_invalid_evidence_never_becomes_approval():
    response = TestClient(app).post("/api/v1/greenfield/e01-e11/evaluate", json={
        "e11_payload": {"x": 1}, "e11_expected_sha256": "0" * 64,
        "e11_catalog_version": "synthetic-v1",
    })
    assert response.status_code == 200
    body = response.json()
    assert body["checks"]["E11"]["status"] == "FAIL"
    assert body["release_allowed"] is False
