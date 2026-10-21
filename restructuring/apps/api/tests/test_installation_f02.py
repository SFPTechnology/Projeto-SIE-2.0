"""Canonical model invariants, explicit units and separate spatial/electrical graphs."""
from copy import deepcopy
from decimal import Decimal
import json
from uuid import UUID

import pytest
from pydantic import ValidationError

from sie_api.domain.installation import (Installation, Voltage, ActivePower, ReactivePower,
                                         ApparentPower, Temperature)


def demo_installation():
    """Two boards: root feeder to child terminal circuit; synthetic, no normative values."""
    ids = {name: str(UUID(int=n)) for n, name in enumerate((
        'project', 'building', 'floor', 'room1', 'room2', 'supply', 'board1', 'board2',
        'point1', 'point2', 'load1', 'load2', 'device1', 'device2', 'feeder', 'terminal',
        'run1', 'run2', 'segment1', 'segment2', 'segment3', 'revision', 'calculation',
        'device3', 'terminal2', 'run3', 'segment4'), 1)}

    def entity(key, **fields):
        return {'id': ids[key], 'project_id': ids['project'], 'name': key, **fields}

    def voltage(value='220', basis='FF'):
        return {'value': value, 'unit': 'V', 'basis': basis}

    def condition(method, ambient):
        return {'installation_method': method, 'medium': 'AIR',
                'ambient_temperature': {'value': ambient, 'unit': 'degC'},
                'grouped_circuits': 1, 'solar_exposure': False}

    data = {
        'schema_version': 'SIE_INSTALLATION_V1',
        'project': {'id': ids['project'], 'name': 'Synthetic model', 'revision': 1},
        'buildings': [entity('building')],
        'floors': [entity('floor', building_id=ids['building'], level=0)],
        'rooms': [entity('room1', floor_id=ids['floor']), entity('room2', floor_id=ids['floor'])],
        'supplies': [entity('supply', phases=3, voltage_ff=voltage(), frequency_hz='60', earthing_system='DECLARED_TEST')],
        'boards': [entity('board1', room_id=ids['room1'], supply_id=ids['supply']),
                   entity('board2', room_id=ids['room2'])],
        'load_points': [entity('point1', room_id=ids['room1']), entity('point2', room_id=ids['room2'])],
        'loads': [entity('load1', load_point_id=ids['point1'], connection='SINGLE_PHASE_FF',
                         active_power={'value': '1000', 'unit': 'W'}),
                  entity('load2', load_point_id=ids['point2'], connection='SINGLE_PHASE_FF',
                         apparent_power={'value': '1200', 'unit': 'VA'},
                         reactive_power={'value': '-100', 'unit': 'var'})],
        'devices': [entity('device1', board_id=ids['board1'], kind='PROTECTION'),
                    entity('device2', board_id=ids['board2'], kind='PROTECTION_AND_SWITCHING')],
        'circuits': [entity('feeder', board_id=ids['board1'], device_id=ids['device1'], kind='FEEDER',
                            downstream_board_id=ids['board2'], design_current={'value': '20', 'unit': 'A'},
                            voltage=voltage()),
                     entity('terminal', board_id=ids['board2'], device_id=ids['device2'], kind='TERMINAL',
                            load_ids=[ids['load1'], ids['load2']], design_current={'value': '10', 'unit': 'A'},
                            voltage=voltage())],
        'cable_runs': [entity('run1', circuit_id=ids['feeder'], segment_ids=[ids['segment1']],
                              section={'value': '6', 'unit': 'mm2'}, material='Cu', insulation='DECLARED_TEST'),
                       entity('run2', circuit_id=ids['terminal'], segment_ids=[ids['segment2'], ids['segment3']],
                              section={'value': '4', 'unit': 'mm2'}, material='Cu', insulation='DECLARED_TEST')],
        'segments': [entity('segment1', cable_run_id=ids['run1'], length={'value': '10', 'unit': 'm'},
                            conditions=condition('DECLARED_A', '30')),
                     entity('segment2', cable_run_id=ids['run2'], length={'value': '5', 'unit': 'm'},
                            conditions=condition('DECLARED_A', '30')),
                     entity('segment3', cable_run_id=ids['run2'], length={'value': '7.5', 'unit': 'm'},
                            conditions=condition('DECLARED_B', '40'))],
        'revisions': [entity('revision', sequence=1, input_sha256='a' * 64)],
        'calculation_runs': [entity('calculation', revision_id=ids['revision'], project_revision=1,
                                    circuit_id=ids['terminal'], input_sha256='a' * 64,
                                    algorithm_version='synthetic-v1', rule_version='unverified-v1', state='PENDING')],
    }
    # A child board has two separate terminal circuits plus the upstream feeder.
    data['circuits'][1]['load_ids'] = [ids['load1']]
    data['devices'].append(entity('device3', board_id=ids['board2'], kind='PROTECTION'))
    data['circuits'].append(entity('terminal2', board_id=ids['board2'], device_id=ids['device3'],
        kind='TERMINAL', load_ids=[ids['load2']], design_current={'value': '5', 'unit': 'A'}, voltage=voltage()))
    data['cable_runs'].append(entity('run3', circuit_id=ids['terminal2'], segment_ids=[ids['segment4']],
        section={'value': '4', 'unit': 'mm2'}, material='Cu', insulation='DECLARED_TEST'))
    data['segments'].append(entity('segment4', cable_run_id=ids['run3'], length={'value': '5', 'unit': 'm'},
        conditions=condition('DECLARED_A', '30')))
    return data


def test_multiboard_spatial_graph_is_independent_and_roundtrip_preserves_units_and_precision():
    model = Installation.model_validate(demo_installation())
    assert model.loads[0].load_point_id != model.boards[1].room_id
    assert model.segments[1].conditions != model.segments[2].conditions
    data = model.model_dump(mode='json')
    assert data['segments'][2]['length'] == {'value': '7.5', 'unit': 'm'}
    assert data['circuits'][0]['voltage']['basis'] == 'FF'
    assert Installation.model_validate_json(model.model_dump_json()) == model
    assert json.loads(model.model_dump_json())['calculation_runs'][0]['normative_conformity_verified'] is False


@pytest.mark.parametrize('bad', [1.1, 220, True, 'NaN', 'Infinity', '-1', '0'])
def test_voltage_never_coerces_binary_floats_or_invalid_magnitudes(bad):
    with pytest.raises(ValidationError):
        Voltage(value=bad, unit='V', basis='FN')


def test_decimal_is_preserved_without_rounding_and_power_types_are_not_interchangeable():
    original = Decimal('220.000000000000000001')
    assert Voltage(value=original, unit='V', basis='FN').model_dump(mode='json')['value'] == str(original)
    with pytest.raises(ValidationError):
        ActivePower(value='100', unit='VA')
    with pytest.raises(ValidationError):
        ApparentPower(value='100', unit='W')
    assert ReactivePower(value='-50', unit='var').value == Decimal('-50')
    with pytest.raises(ValidationError):
        Temperature(value='-273.15', unit='degC')


@pytest.mark.parametrize('mutation', [
    lambda d: d['rooms'][0].update(floor_id=str(UUID(int=999))),
    lambda d: d['boards'][0].update(project_id=str(UUID(int=999))),
    lambda d: d['devices'][0].update(id=d['loads'][0]['id']),
    lambda d: d['circuits'][0].update(device_id=d['devices'][1]['id']),
    lambda d: d['circuits'][1]['load_ids'].append(str(UUID(int=999))),
    lambda d: d['boards'][1].update(supply_id=d['supplies'][0]['id']),
    lambda d: d['boards'][0].update(supply_id=None),
    lambda d: d['cable_runs'][0].update(segment_ids=[d['segments'][1]['id']]),
    lambda d: d['segments'][0].update(cable_run_id=str(UUID(int=999))),
    lambda d: d['calculation_runs'][0].update(revision_id=str(UUID(int=999))),
    lambda d: d['calculation_runs'][0].update(project_revision=2),
    lambda d: d['revisions'][0].update(parent_revision_id=d['revisions'][0]['id']),
    lambda d: d['loads'][0].update(connection='THREE_PHASE'),
    lambda d: d['circuits'][1].update(phases=3, voltage={'value': '127', 'unit': 'V', 'basis': 'FN'}),
    lambda d: d['circuits'][0].update(load_ids=[d['loads'][0]['id']]),
    lambda d: d['segments'][0]['conditions'].update(grouped_circuits=True),
    lambda d: d['supplies'][0].update(voltage_ff={'value': '220', 'unit': 'V', 'basis': 'FN'}),
    lambda d: d['project'].update(revision=0),
    lambda d: d['circuits'][0].update(normative_approved=True),
])
def test_aggregate_rejects_orphans_cross_project_identity_conflicts_and_ambiguous_conditions(mutation):
    data = demo_installation()
    mutation(data)
    with pytest.raises(ValidationError):
        Installation.model_validate(data)


def test_cycle_is_rejected_even_when_every_board_has_one_incoming_feeder():
    data = demo_installation()
    data['supplies'] = []
    data['boards'][0]['supply_id'] = None
    data['circuits'][1].update(kind='FEEDER', load_ids=[], downstream_board_id=data['boards'][0]['id'])
    data['circuits'][2]['load_ids'] = [load['id'] for load in data['loads']]
    with pytest.raises(ValidationError, match='acyclic'):
        Installation.model_validate(data)


def test_shared_terminal_load_or_unconnected_device_is_rejected():
    data = demo_installation()
    second = deepcopy(data['circuits'][1])
    second.update(id=str(UUID(int=999)), device_id=data['devices'][0]['id'], board_id=data['boards'][0]['id'])
    data['circuits'].append(second)
    with pytest.raises(ValidationError):
        Installation.model_validate(data)
    data = demo_installation()
    device = deepcopy(data['devices'][0])
    device['id'] = str(UUID(int=999))
    data['devices'].append(device)
    with pytest.raises(ValidationError, match='Every device'):
        Installation.model_validate(data)


def test_incomplete_empty_draft_does_not_invent_electrical_entities():
    model = Installation(project={'id': str(UUID(int=1)), 'name': 'Empty draft', 'revision': 1})
    assert not model.supplies and not model.circuits
    assert model.model_json_schema()['additionalProperties'] is False


def test_nominal_voltage_requires_ancestral_source_including_downstream_boards():
    data = demo_installation()
    data['circuits'][1]['voltage']['value'] = '230'
    with pytest.raises(ValidationError, match='ancestral supply'):
        Installation.model_validate(data)
    data = demo_installation()
    data['circuits'][1]['voltage'].update(value='127', basis='FN')
    data['loads'][0]['connection'] = 'SINGLE_PHASE_FN'
    with pytest.raises(ValidationError, match='ancestral supply'):
        Installation.model_validate(data)


def test_valid_run_requires_output_digest_and_never_claims_normative_conformity():
    data = demo_installation()
    data['calculation_runs'][0]['state'] = 'VALID'
    with pytest.raises(ValidationError, match='output digest'):
        Installation.model_validate(data)
    data['calculation_runs'][0]['output_sha256'] = 'b' * 64
    assert Installation.model_validate(data).calculation_runs[0].state == 'VALID'
    data['calculation_runs'][0]['normative_conformity_verified'] = True
    with pytest.raises(ValidationError):
        Installation.model_validate(data)


def test_json_schema_advertises_decimal_text_instead_of_rejected_binary_numbers():
    assert Voltage.model_json_schema()['properties']['value']['type'] == 'string'


@pytest.mark.parametrize('value', [True, False, 1.0, 3.0, '1', '3'])
def test_circuit_phases_requires_integer_without_boolean_numeric_or_text_coercion(value):
    data = demo_installation()
    data['circuits'][1]['phases'] = value
    with pytest.raises(ValidationError, match='without coercion'):
        Installation.model_validate(data)


@pytest.mark.parametrize('upstream', ['supply', 'feeder'])
def test_three_phase_load_requires_three_phase_supply_and_every_ancestral_feeder(upstream):
    data = demo_installation()
    data['circuits'][1]['phases'] = 3
    data['loads'][0]['connection'] = 'THREE_PHASE'
    data['circuits'][0]['phases'] = 3
    if upstream == 'supply':
        data['supplies'][0]['phases'] = 1
    else:
        data['circuits'][0]['phases'] = 1
    with pytest.raises(ValidationError, match='ancestral feeder phases'):
        Installation.model_validate(data)
    data['supplies'][0]['phases'] = 3
    data['circuits'][0]['phases'] = 3
    assert Installation.model_validate(data).circuits[1].phases == 3


def test_supply_phase_count_is_explicit_and_strict():
    data = demo_installation()
    data['supplies'][0].pop('phases')
    with pytest.raises(ValidationError):
        Installation.model_validate(data)
    data['supplies'][0]['phases'] = True
    with pytest.raises(ValidationError, match='without coercion'):
        Installation.model_validate(data)


def test_declared_segment_impedance_requires_ancestral_supply_frequency():
    data = demo_installation()
    data['segments'][1]['impedance'] = {
        'resistance': '4', 'reactance': '0.1', 'unit': 'ohm/km', 'frequency_hz': '50',
        'conductor_temperature': {'value': '70', 'unit': 'degC'}, 'source_reference': 'Synthetic'}
    with pytest.raises(ValidationError, match='impedance frequency'):
        Installation.model_validate(data)
    data['segments'][1]['impedance']['frequency_hz'] = '60'
    assert Installation.model_validate(data).segments[1].impedance.frequency_hz == Decimal('60')


@pytest.mark.parametrize('value', ['1e1001', '1e-1001', '1' * 1001, ' ' * 1101 + '1'])
def test_decimal_resource_limits_reject_unbounded_coefficients_exponents_and_input(value):
    with pytest.raises(ValidationError, match='supported text length|1000 digits'):
        Voltage(value=value, unit='V', basis='FF')


def test_decimal_resource_limit_boundaries_remain_exact():
    for value in ('1e1000', '1e-1000', '1' * 1000):
        assert Voltage(value=value, unit='V', basis='FF').value == Decimal(value)
