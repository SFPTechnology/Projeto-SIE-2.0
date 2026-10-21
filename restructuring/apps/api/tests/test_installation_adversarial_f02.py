"""QA-03 regressions: malformed result, effective configuration and canonical mismatch."""
from decimal import Decimal
from hashlib import sha256
import json

import pytest
from fastapi.testclient import TestClient

from sie_api import application
from sie_api.domain.installation import Installation
from sie_api.installation_service import (create_snapshot, analyze_legacy,
    calculation_status, algorithm_identity)
from sie_api.main import app
from test_installation_integration_f02 import legacy_case


@pytest.mark.parametrize('malformed', [[], None, 'not-a-result', {'liberado_para_uso_normativo': False}])
def test_invalid_result_shape_is_http_422_instead_of_server_failure(malformed):
    installation, parameters = legacy_case()
    snapshot = create_snapshot(installation)
    record = analyze_legacy(snapshot, installation.circuits[1].id, parameters, 'test-v1')
    raw = record.model_dump(mode='json')
    text = json.dumps(malformed, sort_keys=True, separators=(',', ':'))
    raw.update(result_json=text, result_sha256=sha256(text.encode()).hexdigest())
    response = TestClient(app, raise_server_exceptions=False).post('/api/v1/modelo/invalidacao', json={
        'record': raw, 'snapshot': snapshot.model_dump(mode='json'),
        'rule_version': 'test-v1', 'input_sha256': record.input_sha256})
    assert response.status_code == 422


def test_effective_breaker_catalog_change_marks_historical_calculation_stale(monkeypatch):
    installation, parameters = legacy_case()
    snapshot = create_snapshot(installation)
    record = analyze_legacy(snapshot, installation.circuits[1].id, parameters, 'test-v1')
    before = record.model_dump_json()
    monkeypatch.setattr(application, 'CATALOGO_DISJUNTORES', (Decimal('999'),))
    assert algorithm_identity() != record.algorithm_version
    assert calculation_status(record, snapshot, algorithm_identity(), 'test-v1',
                              record.input_sha256)['status'] == 'STALE'
    assert record.model_dump_json() == before


def test_canonical_impedance_cannot_be_silently_ignored_by_resistive_adapter():
    installation, parameters = legacy_case()
    raw = installation.model_dump(mode='json')
    impedance = {'resistance': '999', 'reactance': '2', 'unit': 'ohm/km',
                 'frequency_hz': '60',
                 'conductor_temperature': {'value': '70', 'unit': 'degC'},
                 'source_reference': 'Synthetic mismatch, no normative source'}
    for segment in raw['segments'][1:3]:
        segment['impedance'] = impedance
    snapshot = create_snapshot(Installation.model_validate(raw))
    with pytest.raises(ValueError, match='Impedância canônica'):
        analyze_legacy(snapshot, installation.circuits[1].id, parameters, 'test-v1')


def test_selected_breaker_cannot_override_explicit_canonical_device_rating():
    installation, parameters = legacy_case()
    raw = installation.model_dump(mode='json')
    raw['devices'][1]['nominal_current'] = {'value': '6', 'unit': 'A'}
    snapshot = create_snapshot(Installation.model_validate(raw))
    with pytest.raises(ValueError, match='dispositivo canônico'):
        analyze_legacy(snapshot, installation.circuits[1].id, parameters, 'test-v1')
