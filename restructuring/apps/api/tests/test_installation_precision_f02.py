"""QA-01 adversarial regressions for exact canonical comparisons and JSON contracts."""
from decimal import localcontext
from hashlib import sha256

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from sie_api.main import app
from sie_api.domain.installation import Installation
from sie_api.installation_service import (CalculationRecord, analyze_legacy, create_snapshot)
from test_installation_integration_f02 import legacy_case


@pytest.mark.parametrize('precision', [6, 28, 50])
def test_adapter_never_rounds_canonical_segment_length_to_fit_legacy_input(precision):
    installation, parameters = legacy_case()
    data = installation.model_dump(mode='json')
    data['segments'][1]['length']['value'] = '5.0000000000000000000000000001'
    model = Installation.model_validate(data)
    snapshot = create_snapshot(model)
    # The canonical total is strictly greater than legacy 12.5 m at every
    # ambient Decimal context. A rounded equality must never pass the adapter.
    with localcontext() as context:
        context.prec = precision
        with pytest.raises(ValueError, match='Grandezas legadas divergem'):
            analyze_legacy(snapshot, model.circuits[1].id, parameters, 'qa-test-v1')


def test_adapter_cannot_ignore_canonical_impedance_in_resistive_comparison():
    installation, parameters = legacy_case()
    data = installation.model_dump(mode='json')
    for segment in data['segments'][1:3]:
        segment['impedance'] = {
            'resistance': '999', 'reactance': '0', 'unit': 'ohm/km',
            'frequency_hz': '60', 'conductor_temperature': {'value': '70', 'unit': 'degC'},
            'source_reference': 'Synthetic QA fixture, no normative source',
        }
    model = Installation.model_validate(data)
    with pytest.raises(ValueError, match='Impedância canônica'):
        analyze_legacy(create_snapshot(model), model.circuits[1].id, parameters, 'qa-test-v1')


@pytest.mark.parametrize('text', ['[]', 'null', '1', '"result"', '{}'])
def test_non_object_or_incomplete_result_returns_validation_error_and_http_422(text):
    installation, parameters = legacy_case()
    snapshot = create_snapshot(installation)
    original = analyze_legacy(snapshot, installation.circuits[1].id, parameters, 'qa-test-v1')
    record = original.model_dump(mode='json')
    record.update(result_json=text, result_sha256=sha256(text.encode()).hexdigest())
    with pytest.raises(ValidationError):
        CalculationRecord.model_validate(record)
    response = TestClient(app).post('/api/v1/modelo/invalidacao', json={
        'record': record, 'snapshot': snapshot.model_dump(mode='json'),
        'rule_version': 'qa-test-v1', 'input_sha256': original.input_sha256,
    })
    assert response.status_code == 422


@pytest.mark.parametrize('phases', [True, False, '1', '3', 1.0, 3.0])
def test_circuit_phase_count_never_accepts_coerced_bool_string_or_float(phases):
    installation, _ = legacy_case()
    data = installation.model_dump(mode='json')
    data['circuits'][1]['phases'] = phases
    with pytest.raises(ValidationError):
        Installation.model_validate(data)
