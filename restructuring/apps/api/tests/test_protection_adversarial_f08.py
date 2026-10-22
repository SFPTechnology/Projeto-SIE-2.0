"""QA-01 adversarial checks, independent of implementation fixtures' expected output."""
from copy import deepcopy
from decimal import Decimal, localcontext
from fractions import Fraction
import json
from pathlib import Path
from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError

from sie_api.protection_contracts_f08 import Study, FaultScenario
from sie_api import protection_f08 as motor

EXAMPLE = Path(__file__).resolve().parents[3] / 'examples/f08_protecoes_demo.json'

@pytest.fixture
def study_raw():
    return json.loads(EXAMPLE.read_text())


def test_missing_protections_never_approve(study_raw):
    study_raw.update(circuits={}, devices=[], fault_scenarios=[])
    result = motor.analyze(study_raw)
    assert result['status'] == 'PENDENTE'
    assert not result['normative_conformity_verified']
    assert not result['authoritative_for_sizing']
    assert all(r['checks']['protection']['status'] == 'PENDENTE' for r in result['circuits'].values())


@pytest.mark.parametrize('value', ['NaN', 'Infinity', '-Infinity', 0.1, True, '1e-31', '1e31'])
def test_fault_magnitude_adversarial_rejected(study_raw, value):
    study_raw['fault_scenarios'][0]['path_r_ohm'] = value
    with pytest.raises(ValidationError):
        Study.model_validate(study_raw)


def test_fault_three_four_five_reference(study_raw):
    raw = deepcopy(study_raw['fault_scenarios'][0])
    raw.update(source_r_ohm='0.12', path_r_ohm='0.18',
               source_x_ohm='0.15', path_x_ohm='0.25',
               voltage_v='220', voltage_factor='1.1')
    result = motor.fault(FaultScenario.model_validate(raw))
    # Independent rational triangle: |0.3+j0.4|=0.5; 1.1*220/0.5=484 A.
    reference = Fraction(11, 10) * Fraction(220) / Fraction(1, 2)
    assert Decimal(result['current_a']) == Decimal(reference.numerator) / reference.denominator


def test_three_phase_square_reference(study_raw):
    raw = deepcopy(study_raw['fault_scenarios'][0])
    raw.update(fault_type='THREE_PHASE', source_voltage_basis='FF',
               source_r_ohm='0.3', source_x_ohm='0.4', path_r_ohm='0', path_x_ohm='0',
               voltage_v='220', voltage_factor='1')
    result = motor.fault(FaultScenario.model_validate(raw))
    with localcontext() as ctx:
        ctx.prec = 180
        # I² = 220² / (3*(0.3²+0.4²)), independent of sqrt evaluation.
        reference = Decimal(220)**2 / (Decimal(3) * Decimal('0.25'))
        assert abs(Decimal(result['current_a'])**2 - reference) < Decimal('1e-170')


def test_missing_fault_cannot_pass_thermal(study_raw):
    cid, cp = next(iter(study_raw['circuits'].items()))
    cp['fault_max_id'] = None
    result = motor.analyze(study_raw)
    assert all(s['checks']['thermal']['status'] in ('PENDENTE', 'BLOQUEADO')
               for s in result['circuits'][cid]['segments'])


def test_restricted_overload_candidate_reuses_same_rule(study_raw):
    cid, cp = next(iter(study_raw['circuits'].items()))
    cp.update(overload_hours_year='101', overload_hours_life='0')
    device = next(d for d in study_raw['devices'] if d['id'] == cp['device_id'])
    # Existing Iz is22.272 A; I2=23.2 fails restricted I2<=Iz but passes1.45Iz.
    study_raw['candidate_device_ids'] = {cid: [device['id']]}
    result = motor.analyze(study_raw)
    assert result['circuits'][cid]['segments'][0]['checks']['overload']['status'] == 'REPROVADO'
    assert not result['selection'][cid]['steps'][0]['basic_overload_candidate']


def test_topology_rejected_conductor_cannot_be_hidden(study_raw):
    # F07 rejects1e-7% voltage-drop limit; F08 must retain that failure.
    ci = next(iter(study_raw['conductor_study']['circuits'].values()))
    ci['total_drop_limit_percent'] = '0.0000001'
    result = motor.analyze(study_raw)
    assert result['status'] in ('REPROVADO', 'BLOQUEADO')


def test_catalog_identity_cannot_certify_different_family(study_raw):
    from sie_api.protection_contracts_f08 import Device
    device = Device.model_validate({'id': study_raw['devices'][0]['id'],
        'family': 'FUSE', 'catalog_key': 'SCHNEIDER_A9F74116_IEC60898_1'})
    resolved = motor._device(device)
    assert resolved.get('registry_error')


def test_physical_scenario_unchanged_by_relabel_cannot_validate_new_conductor(study_raw):
    variant = deepcopy(study_raw)
    variant['id'] = str(uuid4())
    variant['conductor_study']['id'] = str(uuid4())
    variant['conductor_study']['topology']['installation']['segments'][0]['length']['value'] = '21'
    # The sole change to fault inputs is a label, not recalculated loop impedances.
    remap = {f['id']: 'renamed-' + f['id'] for f in variant['fault_scenarios']}
    for fault in variant['fault_scenarios']:
        fault['id'] = remap[fault['id']]
    for cp in variant['circuits'].values():
        for field in ('fault_max_id', 'fault_min_id'):
            if cp.get(field): cp[field] = remap[cp[field]]
        if cp.get('thermal', {}).get('fault_scenario_id'):
            cp['thermal']['fault_scenario_id'] = remap[cp['thermal']['fault_scenario_id']]
    study_raw['selection_variants'] = [variant]
    result = motor.analyze(study_raw)
    evaluations = result['selection']['variants']['evaluations']
    assert evaluations[0]['status'] == 'BLOQUEADO'
    assert 'imped' in evaluations[0].get('reason', '').lower()


def test_smaller_pe_cannot_inherit_phase_thermal_pass(study_raw):
    cid, cp = next(iter(study_raw['circuits'].items()))
    conductor = study_raw['conductor_study']['circuits'][cid]
    conductor['pe_section_mm2'] = '2.5'
    # Deliberately choose an energy between k²*2.5² and k²*4².
    cp['thermal']['energy_a2s'] = '100000'
    scenario = deepcopy(next(f for f in study_raw['fault_scenarios'] if f['id'] == cp['fault_max_id']))
    scenario.update(id='pe-maximum', fault_type='PHASE_PE', source_voltage_basis='FN', voltage_v='127')
    study_raw['fault_scenarios'].append(scenario)
    cp['pe_thermal'] = deepcopy(cp['thermal'])
    cp['pe_thermal'].update(fault_scenario_id='pe-maximum', maximum_current_a='3000')
    result = motor.analyze(study_raw)['circuits'][cid]
    for segment in result['segments']:
        checks = segment['checks']
        assert checks['thermal']['status'] == 'ATENDE_ESTUDO'
        assert checks['thermal_pe']['status'] == 'REPROVADO'
        assert Decimal(checks['thermal_pe']['limit_a2s']) == Decimal('82656.25')


def test_missing_pe_thermal_is_explicitly_pending(study_raw):
    cid, cp = next(iter(study_raw['circuits'].items()))
    cp.pop('pe_thermal', None)
    result = motor.analyze(study_raw)['circuits'][cid]
    assert all(s['checks']['thermal_pe']['status'] == 'PENDENTE' for s in result['segments'])
