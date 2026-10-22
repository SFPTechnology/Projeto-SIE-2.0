"""QA-01: independent source-pair boundaries and contradictory identity rejection."""
from copy import deepcopy
import json
from pathlib import Path

import pytest

from sie_api.protection_f08 import analyze


@pytest.fixture
def pair_study():
    s = json.loads((Path(__file__).resolve().parents[3] / 'examples/f08_protecoes_demo.json').read_text())
    cs = s['conductor_study']; inst = cs['topology']['installation']
    for supply in inst['supplies']:
        supply['voltage_fn'] = {'value': '230', 'unit': 'V', 'basis': 'FN'}
    for circuit in inst['circuits']:
        circuit['voltage'] = {'value': '230', 'unit': 'V', 'basis': 'FN'}
    for load in inst['loads']:
        load['connection'] = 'SINGLE_PHASE_FN'
    for ci in cs['circuits'].values():
        ci.update(phase_set='L1_N', neutral_required=True, neutral_section_mm2='4')
    for segment in inst['segments']:
        segment['conditions']['ambient_temperature']['value'] = '30'
    for fault in s['fault_scenarios']:
        fault.update(voltage_v='230', source_voltage_basis='FN')
        if fault['fault_type'] == 'PHASE_PHASE':
            fault['fault_type'] = 'PHASE_NEUTRAL'
        if fault['kind'] == 'MAX':
            fault.update(source_r_ohm='0.92', voltage_factor='1.04')
        else:
            fault['source_r_ohm'] = '2'
    for cp in s['circuits'].values():
        cp['trip']['voltage_v'] = '230'
    upstream, downstream = inst['circuits'][:2]
    for device in s['devices']:
        device.update(manufacturer='Schneider Electric', model='iC60N', nominal_current_a='16',
                      i2_a='23.2', rated_voltage_v='230', curve='C', poles=1)
    s['devices'][0].update(nominal_current_a='32', i2_a='46.4')
    s['devices'][1].update(catalog_key='SCHNEIDER_A9F74116_IEC60898_1', model='A9F74116', edition=None,
                          breaking_standard='IEC/EN 60898-1')
    for device in inst['devices']:
        device['nominal_current'] = {'value': '32' if device['id'] == upstream['device_id'] else '16', 'unit': 'A'}
    s['coordination'] = [{'catalog_key': 'SCHNEIDER_IC60N_C32_C16_1P_230',
        'upstream_circuit_id': upstream['id'], 'downstream_circuit_id': downstream['id'],
        'upstream_device_id': upstream['device_id'], 'downstream_device_id': downstream['device_id'],
        'voltage_v': '230'}]
    return s


def pair_result(study):
    return analyze(study)['coordination'][0]


def test_official_pair_exact_boundary_260_a(pair_study):
    # Independent rational construction: 230 * 1.04 / 0.92 = 260 exactly.
    result = pair_result(pair_study)
    assert result['status'] == 'ATENDE_ESTUDO'
    assert result['source_verified'] is True
    assert result['limit_a'] == '260'


def test_official_pair_above_260_a_rejected(pair_study):
    downstream = pair_study['coordination'][0]['downstream_circuit_id']
    maximum_id = pair_study['circuits'][downstream]['fault_max_id']
    next(f for f in pair_study['fault_scenarios'] if f['id'] == maximum_id)['source_r_ohm'] = '0.91999999'
    assert pair_result(pair_study)['status'] == 'REPROVADO'


@pytest.mark.parametrize('field,value', [('manufacturer', 'ACME'), ('family', 'FUSE'), ('nominal_current_a', '15')])
def test_pair_does_not_overwrite_contradiction_into_verified_source(pair_study, field, value):
    pair_study['devices'][1][field] = value
    result = pair_result(pair_study)
    assert result['status'] == 'BLOQUEADO'
    assert result.get('source_verified') is not True


def test_pair_device_outside_temperature_scope_blocked(pair_study):
    for segment in pair_study['conductor_study']['topology']['installation']['segments']:
        segment['conditions']['ambient_temperature']['value'] = '40'
    assert pair_result(pair_study)['status'] == 'BLOQUEADO'


def test_pair_one_pole_not_applied_to_ff_circuit(pair_study):
    inst = pair_study['conductor_study']['topology']['installation']
    # All corresponding domain data change together; this is a valid topology,
    # but outside the registered single-pole phase-neutral pair.
    inst['supplies'][0]['voltage_ff']['value'] = '230'
    for circuit in inst['circuits']:
        circuit['voltage']['basis'] = 'FF'
    for load in inst['loads']:
        load['connection'] = 'SINGLE_PHASE_FF'
    for ci in pair_study['conductor_study']['circuits'].values():
        ci['phase_set'] = 'L1_L2'
    assert pair_result(pair_study)['status'] == 'BLOQUEADO'
