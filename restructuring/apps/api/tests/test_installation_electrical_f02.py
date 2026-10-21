"""QA-02 regressions for explicit electrical context at the F02 boundary."""
import pytest
from pydantic import ValidationError

from sie_api.domain.installation import Installation
from sie_api.installation_service import analyze_legacy, create_snapshot
from test_installation_f02 import demo_installation
from test_installation_integration_f02 import legacy_case


def test_explicit_segment_impedance_cannot_be_silently_replaced_by_legacy_global_resistance():
    installation, parameters = legacy_case()
    raw = installation.model_dump(mode='json')
    for index in (1, 2):
        raw['segments'][index]['impedance'] = {
            'resistance': '99', 'reactance': '20', 'unit': 'ohm/km',
            'frequency_hz': '60',
            'conductor_temperature': {'value': '90', 'unit': 'degC'},
            'source_reference': 'Explicit synthetic parameter; not normative',
        }
    model = Installation.model_validate(raw)
    assert str(parameters.resistencia_ohm_km) == '7.41'
    with pytest.raises(ValueError, match='[Ii]mped'):
        analyze_legacy(create_snapshot(model), model.circuits[1].id, parameters, 'test-v1')


def test_three_phase_terminal_requires_three_phase_availability_through_every_feeder():
    raw = demo_installation()
    raw['supplies'][0]['phases'] = 3
    raw['circuits'][0]['phases'] = 1
    raw['circuits'][1]['phases'] = 3
    for load in raw['loads']:
        if load['id'] in raw['circuits'][1]['load_ids']:
            load['connection'] = 'THREE_PHASE'
    with pytest.raises(ValidationError, match='ancestral feeder phases'):
        Installation.model_validate(raw)
    raw['circuits'][0]['phases'] = 3
    assert Installation.model_validate(raw).circuits[1].phases == 3


def test_impedance_frequency_is_checked_against_electrical_source_not_room():
    raw = demo_installation()
    raw['segments'][1]['impedance'] = {
        'resistance': '1', 'reactance': '0', 'unit': 'ohm/km', 'frequency_hz': '50',
        'conductor_temperature': {'value': '70', 'unit': 'degC'},
        'source_reference': 'Synthetic 50 Hz source',
    }
    with pytest.raises(ValidationError, match='frequency differs'):
        Installation.model_validate(raw)
