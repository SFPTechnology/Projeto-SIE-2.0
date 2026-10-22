"""QA02: independent arithmetic and safety-domain counterexamples for F08.

The rational 3-4-5 and thermal equality cases derive their expected values
directly rather than copying a motor implementation or a manufacturer curve.
"""
from copy import deepcopy
from decimal import Decimal, localcontext
from fractions import Fraction
import json
from pathlib import Path
from types import SimpleNamespace
from uuid import UUID
import pytest

from sie_api import protection_f08 as m
from sie_api.protection_contracts_f08 import FaultScenario, Thermal, Residual, Surge

D = Decimal
DEVICE = UUID('00000000-0000-0000-0000-00000000000d')
FAULT = {'id':'test-scope','current_a':'1000'}
E = {'document':'QA02 synthetic arithmetic','edition':'TEST','reference':'Not product data','sha256':'0'*64}


def scenario(**changes):
    raw = dict(id='independent',circuit_id='00000000-0000-0000-0000-000000000010',
               kind='MAX',fault_type='PHASE_PHASE',voltage_v='220',voltage_factor='1',
               source_r_ohm='1',source_x_ohm='1',path_r_ohm='2',path_x_ohm='3',
               source_evidence=E,path_evidence=E,model='SINGLE_RADIAL_THEVENIN_NO_OTHER_CONTRIBUTIONS',
               additional_contributions=False,source_voltage_basis='FF',location='DEVICE')
    raw.update(changes)
    return FaultScenario.model_validate(raw)


def test_rational_fault_complete_loop_no_hidden_factor_two():
    result=m.fault(scenario())
    assert D(result['z_ohm']) == 5
    assert D(result['current_a']) == D(Fraction(220,5).numerator)/Fraction(220,5).denominator
    assert result['sources_verified'] is False


def test_three_phase_positive_sequence_model_independent_squared_identity():
    result=m.fault(scenario(fault_type='THREE_PHASE'))
    with localcontext() as ctx:
        ctx.prec=180
        # I² * 3 * |Z1|² = Uff², with relative precision guard for sqrt(3).
        residual=D(result['current_a'])**2*3*25-D(220)**2
        assert abs(residual) < D('1e-170')


def test_voltage_factor_applies_once_and_contributions_block():
    assert D(m.fault(scenario(voltage_factor='0.95'))['current_a']) == D('41.8')
    result=m.fault(scenario(additional_contributions=True))
    assert result['status']=='BLOQUEADO' and result['current_a'] is None


@pytest.mark.parametrize('hours_year,hours_life,expected', [('100','500','ATENDE_ESTUDO'),('100.001','500','REPROVADO'),('100','500.001','REPROVADO'),(None,None,'PENDENTE')])
def test_overload_duration_cutoffs_from_5410_note(hours_year,hours_life,expected):
    cp=SimpleNamespace(overload_hours_year=D(hours_year) if hours_year else None,
                       overload_hours_life=D(hours_life) if hours_life else None)
    result=m.overload(D(10),D(20),dict(nominal_current_a='16',i2_a='23.2'),cp)
    assert result['status']==expected


@pytest.mark.parametrize('energy,expected',[('1322500','ATENDE_ESTUDO'),('1322500.0001','REPROVADO')])
def test_adiabatic_equality_independently_115_squared_times_10_squared(energy,expected):
    thermal=Thermal.model_validate(dict(device_id=DEVICE,fault_scenario_id='test-scope',maximum_current_a='1000',k_a_sqrt_s_mm2='115',duration_s='1',energy_a2s=energy,
        evidence=E,material='Cu',insulation='PVC',initial_temperature_c='70',final_temperature_c='160'))
    result=m.thermal(D(10),dict(material='Cu',insulation='PVC'),SimpleNamespace(thermal=thermal,device_id=DEVICE),FAULT)
    assert D(result['limit_a2s'])==1322500
    assert result['status']==expected


@pytest.mark.parametrize('duration,asymmetry,status',[('0.099',None,'PENDENTE'),('0.099',False,'PENDENTE'),('0.099',True,'ATENDE_ESTUDO'),('5.001',True,'BLOQUEADO')])
def test_adiabatic_time_domain_without_hidden_asymmetry_assumption(duration,asymmetry,status):
    thermal=Thermal.model_validate(dict(device_id=DEVICE,fault_scenario_id='test-scope',maximum_current_a='1000',k_a_sqrt_s_mm2='115',duration_s=duration,effective_current_a='100',
        asymmetry_negligible=asymmetry,evidence=E,material='Cu',insulation='PVC',initial_temperature_c='70',final_temperature_c='160'))
    result=m.thermal(D(10),dict(material='Cu',insulation='PVC'),SimpleNamespace(thermal=thermal,device_id=DEVICE),FAULT)
    assert result['status']==status


def test_no_default_shock_release_for_it_or_tt_without_rcd():
    assert m.shock(SimpleNamespace(earthing='IT'),None,None)['status']=='PENDENTE'
    cp=SimpleNamespace(earthing='TT',bonding_verified=True,rcd=None)
    assert m.shock(cp,None,None)['status']=='PENDENTE'


def rcd(**changes):
    raw=dict(device_id=DEVICE,sensitivity_a='0.03',required_max_sensitivity_a='0.03',
             nominal_current_a='40',actual_type='A',required_type='A',all_live_conductors=True,
             pe_separated_upstream=True,conditional_short_circuit_a='6000',backup_device_id=DEVICE,
             backup_voltage_v='220',backup_protection_verified=True,max_time_s='0.2',evidence=E)
    raw.update(changes)
    return Residual.model_validate(raw)


@pytest.mark.parametrize('name,value,expected', [('conditional_short_circuit_a','999','REPROVADO'),('conditional_short_circuit_a','1000','ATENDE_ESTUDO'),('conditional_short_circuit_a',None,'PENDENTE'),('nominal_current_a','10','REPROVADO')])
def test_rcd_conditional_short_and_upstream_current(name,value,expected):
    cp=SimpleNamespace(rcd=rcd(**{name:value}),earthing='TN_S',bonding_verified=True,
                       device_id=DEVICE,rcd_required=True)
    assert m.residual(cp,dict(nominal_current_a='16',rated_voltage_v='220'),D(8),FAULT)['status']==expected


def spd(**changes):
    raw=dict(device_id=DEVICE,uc_v='275',minimum_uc_v='275',up_v='1500',equipment_withstand_v='2500',
             spd_type='T2',required_type='T2',backup_coordinated=True,bonding_verified=True,
             connection_length_verified=True,nominal_discharge_a='20000',required_nominal_discharge_a='20000',
             max_discharge_a='40000',required_max_discharge_a='40000',earthing='TT',
             required_connection_scheme='DECLARED_3_PLUS_1',connection_scheme_declared='DECLARED_3_PLUS_1',evidence=E)
    raw.update(changes)
    return Surge.model_validate(raw)


@pytest.mark.parametrize('name,value,expected',[('nominal_discharge_a','19999','REPROVADO'),('nominal_discharge_a',None,'PENDENTE'),('max_discharge_a','39999','REPROVADO'),('earthing','TN_S','REPROVADO'),('connection_scheme_declared','OTHER','REPROVADO'),('uc_v','275','ATENDE_ESTUDO')])
def test_spd_t2_requires_distinct_in_imax_and_compatible_scheme(name,value,expected):
    cp=SimpleNamespace(spd=spd(**{name:value}),spd_required=True,earthing='TT')
    assert m.surge(cp)['status']==expected


def test_spd_t1_impulse_not_substituted_by_imax_and_t3_stays_pending():
    cp=SimpleNamespace(spd=spd(spd_type='T1',required_type='T1'),spd_required=True,earthing='TT')
    assert m.surge(cp)['status']=='PENDENTE'
    cp.spd=spd(spd_type='T1',required_type='T1',impulse_current_a='12500',required_impulse_current_a='12500')
    assert m.surge(cp)['status']=='ATENDE_ESTUDO'
    cp.spd=spd(spd_type='T3',required_type='T3')
    assert m.surge(cp)['status']=='PENDENTE'


@pytest.mark.parametrize('resistance,expected',[('5000','ATENDE_ESTUDO'),('5000.0001','REPROVADO')])
def test_tt_touch_voltage_equality_uses_sensitivity_not_nominal_current(resistance,expected):
    cp=SimpleNamespace(earthing='TT',bonding_verified=True,rcd=rcd(sensitivity_a='0.01'),
                       earth_resistance_ohm=D(resistance),touch_limit_v=D(50),
                       disconnection_limit_s=D('0.2'),disconnection_evidence=E)
    assert m.shock(cp,None,None)['status']==expected


def test_spd_inconsistent_maximum_below_nominal_does_not_pass():
    # Even low declared requirements cannot make Imax < In coherent for T2.
    cp=SimpleNamespace(spd=spd(nominal_discharge_a='20000',required_nominal_discharge_a='1000',
                               max_discharge_a='10000',required_max_discharge_a='1000'),
                       spd_required=True,earthing='TT')
    assert m.surge(cp)['status'] in ('BLOQUEADO','REPROVADO')


def test_selectivity_catalog_requires_fault_at_downstream_device():
    from copy import deepcopy
    import json
    from pathlib import Path
    raw=json.loads((Path(__file__).resolve().parents[3]/'examples/f08_protecoes_demo.json').read_text())
    cs=raw['conductor_study']; inst=cs['topology']['installation']
    inst['supplies'][0]['voltage_fn']['value']='230'
    inst['supplies'][0]['voltage_ff']['value']='400'
    for circuit in inst['circuits']:
        circuit['voltage']={'value':'230','unit':'V','basis':'FN'}
        cs['circuits'][circuit['id']]['phase_set']='L1_N'
    for load in inst['loads']:load['connection']='SINGLE_PHASE_FN'
    for segment in inst['segments']:segment['conditions']['ambient_temperature']['value']='30'
    for fault in raw['fault_scenarios']:
        fault.update(fault_type='PHASE_NEUTRAL' if fault['kind']=='MAX' else 'PHASE_PE',
                     source_voltage_basis='FN',voltage_v='230')
    up,down=inst['circuits'][:2]
    for circuit,nominal in ((up,'32'),(down,'16')):
        device=next(d for d in raw['devices'] if d['id']==circuit['device_id'])
        device.update(family='MCB',manufacturer='Schneider Electric',model='iC60N',
                      nominal_current_a=nominal,curve='C',poles=1,rated_voltage_v='230')
        next(d for d in inst['devices'] if d['id']==circuit['device_id'])['nominal_current']={'value':nominal,'unit':'A'}
    mx=next(f for f in raw['fault_scenarios'] if f['id']==raw['circuits'][down['id']]['fault_max_id'])
    mx.update(source_r_ohm='1',source_x_ohm='0',path_r_ohm='0',path_x_ohm='0',voltage_factor='1')
    raw['coordination']=[dict(upstream_circuit_id=up['id'],downstream_circuit_id=down['id'],
        upstream_device_id=up['device_id'],downstream_device_id=down['device_id'],voltage_v='230',
        catalog_key='SCHNEIDER_IC60N_C32_C16_1P_230')]
    result=m.analyze(raw)['coordination'][0]
    assert result['status']=='ATENDE_ESTUDO' and result['source_verified'] is True
    # The same smaller current at the remote end does not establish selectivity
    # at the downstream protective device, where prospective fault is greatest.
    mx.update(location='SEGMENT_END',segment_id=next(r for r in inst['cable_runs'] if r['circuit_id']==down['id'])['segment_ids'][-1])
    result=m.analyze(raw)['coordination'][0]
    assert result['status']=='PENDENTE'
    assert result.get('source_verified') is not True
