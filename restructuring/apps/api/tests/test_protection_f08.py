"""Independent arithmetic and fail-closed scenarios, synthetic data only."""
import json
from copy import deepcopy
from decimal import Decimal, localcontext
from pathlib import Path
import pytest
from pydantic import ValidationError
from sie_api.protection_contracts_f08 import Study, FaultScenario
from sie_api.protection_f08 import analyze, fault, fingerprint

EXAMPLE=Path(__file__).resolve().parents[3]/'examples/f08_protecoes_demo.json'
@pytest.fixture
def raw():return json.loads(EXAMPLE.read_text())

def first(raw):return next(iter(raw['circuits']))
def criterion(raw,name):return analyze(raw)['circuits'][first(raw)]['checks'][name]

def test_missing_all_stays_pending(raw):
 raw['circuits']={};raw['devices']=[];raw['fault_scenarios']=[]
 r=analyze(raw)
 assert r['status']=='PENDENTE'
 assert len(r['circuits'])==3
 assert all(c['criteria']['protection']['status']=='PENDENTE' for c in r['circuits'].values())
 assert r['normative_conformity_verified'] is False

def test_fault_loop_exact_independent(raw):
 f=raw['fault_scenarios'][0];f.update(source_r_ohm='0.03',source_x_ohm='0.04',path_r_ohm='0',path_x_ohm='0',voltage_factor='1')
 assert Decimal(fault(FaultScenario.model_validate(f))['current_a'])==Decimal('4400')

@pytest.mark.parametrize('r,x', [('0.1','0'),('0','0.2'),('0.3','0.4'),('0.00001','0')])
def test_fault_three_phase_independent(raw,r,x):
 f=raw['fault_scenarios'][0];f.update(fault_type='THREE_PHASE',source_r_ohm=r,source_x_ohm=x)
 with localcontext() as ctx:
  ctx.prec=100
  expected=Decimal('220')/(Decimal(3).sqrt()*(Decimal(r)**2+Decimal(x)**2).sqrt())
  got=Decimal(fault(FaultScenario.model_validate(f))['current_a'])
  assert abs(got-expected)<Decimal('1e-85')

def test_zero_impedance_rejected(raw):
 f=raw['fault_scenarios'][0];f.update(source_r_ohm='0')
 with pytest.raises(ValidationError):Study.model_validate(raw)

@pytest.mark.parametrize('field,value',[('voltage_v','1'),('source_r_ohm','NaN'),('voltage_factor','3')])
def test_invalid_fault_values_rejected(raw,field,value):
 raw['fault_scenarios'][0][field]=value
 with pytest.raises(ValidationError):Study.model_validate(raw)

def test_extra_contribution_blocks(raw):
 raw['fault_scenarios'][0]['additional_contributions']=True
 r=analyze(raw);assert r['fault_scenarios'][0]['status']=='BLOQUEADO';assert r['status']=='BLOQUEADO'

def test_missing_fn_no_inference(raw):
 raw['conductor_study']['topology']['installation']['supplies'][0]['voltage_fn']=None
 r=analyze(raw)
 assert r['fault_scenarios'][1]['status']=='BLOQUEADO'
 assert r['fault_scenarios'][1]['current_a'] is None

def test_device_maximum_required(raw):
 raw['fault_scenarios'][0]['location']='SEGMENT_END'
 raw['fault_scenarios'][0]['segment_id']=raw['conductor_study']['topology']['installation']['cable_runs'][0]['segment_ids'][-1]
 assert criterion(raw,'interruption')['status']=='PENDENTE'

def test_breaking_equality_and_failure(raw):
 raw['devices'][0]['breaking_capacity_a']='2200'
 assert criterion(raw,'interruption')['status']=='ATENDE_ESTUDO'
 raw['devices'][0]['breaking_capacity_a']='2199.999999999'
 assert criterion(raw,'interruption')['status']=='REPROVADO'

def test_wrong_voltage_no_extrapolation(raw):
 raw['devices'][0]['rated_voltage_v']='230'
 assert criterion(raw,'interruption')['status']=='BLOQUEADO'

def test_max_min_reversed(raw):
 raw['fault_scenarios'][1]['source_r_ohm']='0.001'
 assert criterion(raw,'fault_order')['status']=='BLOQUEADO'

def test_missing_thermal_link_pending(raw):
 raw['circuits'][first(raw)]['thermal'].pop('device_id')
 r=analyze(raw)['circuits'][first(raw)]
 assert all(s['checks']['thermal']['status']=='PENDENTE' for s in r['segments'])

@pytest.mark.parametrize('duration,energy,effective,asymmetry,expected',[
 ('5','1000',None,None,'ATENDE_ESTUDO'),('5.00001','1000',None,None,'BLOQUEADO'),
 ('0.01',None,'100',None,'PENDENTE'),('0.01',None,'100',False,'PENDENTE'),
 ('0.01',None,'100',True,'ATENDE_ESTUDO'),('0.1','1e20',None,None,'REPROVADO')])
def test_thermal_domains(raw,duration,energy,effective,asymmetry,expected):
 t=raw['circuits'][first(raw)]['thermal'];t.update(duration_s=duration,energy_a2s=energy,effective_current_a=effective,asymmetry_negligible=asymmetry)
 r=analyze(raw)['circuits'][first(raw)]
 assert all(s['checks']['thermal']['status']==expected for s in r['segments'])

def test_it_not_generic_tn(raw):
 raw['circuits'][first(raw)]['earthing']='IT'
 assert criterion(raw,'shock')['status']=='PENDENTE'

def test_tt_no_dr_not_overcurrent(raw):
 raw['circuits'][first(raw)]['earthing']='TT'
 assert criterion(raw,'shock')['status']=='PENDENTE'

def test_fault_wrong_circuit_rejected(raw):
 raw['fault_scenarios'][0]['circuit_id']=list(raw['circuits'])[1]
 with pytest.raises(ValidationError):Study.model_validate(raw)

def test_duplicate_device_rejected(raw):
 raw['devices'].append(deepcopy(raw['devices'][0]))
 with pytest.raises(ValidationError):Study.model_validate(raw)

def test_source_change_fingerprint(raw):
 before=fingerprint(raw);raw['devices'][0]['edition']='TEST-2'
 assert before!=fingerprint(raw)

def test_variant_recalculates_and_finite(raw):
 v=deepcopy(raw);v['id']='88888888-0000-0000-0000-000000000009';v['fault_scenarios'][0]['source_r_ohm']='0.2'
 raw['selection_variants']=[v]
 r=analyze(raw)['selection']['variants']
 assert r['iterations']==1
 assert r['evaluations'][0]['fault_scenarios'][0]['current_a']=='1.10E+3'
 assert r['applied'] is False

def test_nested_variant_rejected(raw):
 v=deepcopy(raw);v['selection_variants']=[deepcopy(raw)];raw['selection_variants']=[v]
 with pytest.raises(ValidationError):Study.model_validate(raw)

def test_iteration_limit(raw):
 raw['max_iterations']=1
 v1=deepcopy(raw);v1['id']='88888888-0000-0000-0000-000000000009'
 v2=deepcopy(raw);v2['id']='88888888-0000-0000-0000-000000000010'
 raw['selection_variants']=[v1,v2]
 assert analyze(raw)['selection']['variants']['status']=='ITERATION_LIMIT'

def test_balance_both_ff_phases_preserves_design(raw):
 r=analyze(raw)
 assert all(b['designer_decision_preserved'] for b in r['boards'])
 assert r['input_snapshot']==Study.model_validate(raw).model_dump(mode='json')
 assert all('não fasorial' in b['method'] for b in r['boards'])

def aux(raw,family):
 cid=first(raw);c=next(c for c in raw['conductor_study']['topology']['installation']['circuits'] if c['id']==cid)
 did='99999999-0000-0000-0000-000000000001' if family=='RCD' else '99999999-0000-0000-0000-000000000002'
 raw['devices'].append({'id':did,'board_id':c['board_id'],'family':family,'evidence':raw['devices'][0]['evidence']})
 return did,raw['circuits'][cid],raw['devices'][0]['evidence']

def rcd(raw):
 did,cp,ev=aux(raw,'RCD');cp['rcd_required']=True
 cp['rcd']={'device_id':did,'sensitivity_a':'0.03','required_max_sensitivity_a':'0.03','nominal_current_a':'40','required_type':'A','actual_type':'A','all_live_conductors':True,'pe_separated_upstream':True,'max_time_s':'0.1','conditional_short_circuit_a':'6000','backup_device_id':cp['device_id'],'backup_voltage_v':'220','backup_protection_verified':True,'evidence':ev}
 return cp

@pytest.mark.parametrize('change,expected',[
 ({},'ATENDE_ESTUDO'),({'nominal_current_a':'10'},'REPROVADO'),({'conditional_short_circuit_a':'2199'},'REPROVADO'),
 ({'backup_protection_verified':False},'REPROVADO'),({'backup_protection_verified':None},'PENDENTE'),({'backup_voltage_v':'230'},'PENDENTE'),
 ({'required_type':'B'},'REPROVADO'),({'all_live_conductors':False},'REPROVADO')])
def test_dr_specific_conditions(raw,change,expected):
 cp=rcd(raw);cp['rcd'].update(change)
 assert criterion(raw,'rcd')['status']==expected

def test_dr_tn_c_forbidden(raw):
 cp=rcd(raw);cp['earthing']='TN_C'
 assert criterion(raw,'rcd')['status']=='REPROVADO'

def test_tt_equality_and_fail(raw):
 cp=rcd(raw);cp.update(earthing='TT',earth_resistance_ohm='1000',touch_limit_v='30')
 assert criterion(raw,'shock')['status']=='ATENDE_ESTUDO'
 cp['earth_resistance_ohm']='1000.00001'
 assert criterion(raw,'shock')['status']=='REPROVADO'

def spd(raw):
 did,cp,ev=aux(raw,'SPD');cp['spd_required']=True
 cp['spd']={'device_id':did,'uc_v':'275','minimum_uc_v':'253','up_v':'1200','equipment_withstand_v':'1500','spd_type':'T2','required_type':'T2','backup_coordinated':True,'bonding_verified':True,'connection_length_verified':True,'nominal_discharge_a':'20000','required_nominal_discharge_a':'20000','max_discharge_a':'40000','required_max_discharge_a':'40000','earthing':'TN_S','connection_scheme_declared':'3+0','required_connection_scheme':'3+0','evidence':ev}
 return cp

@pytest.mark.parametrize('change,expected',[
 ({},'ATENDE_ESTUDO'),({'nominal_discharge_a':'19999'},'REPROVADO'),({'max_discharge_a':None},'PENDENTE'),
 ({'earthing':'TT'},'REPROVADO'),({'connection_scheme_declared':'3+1'},'REPROVADO'),({'backup_coordinated':False},'REPROVADO'),
 ({'spd_type':'T3','required_type':'T3'},'PENDENTE'),({'spd_type':'T1','required_type':'T1'},'PENDENTE')])
def test_dps_specific_requirements(raw,change,expected):
 cp=spd(raw);cp['spd'].update(change)
 assert criterion(raw,'spd')['status']==expected

def test_pe_not_proved_by_phase(raw):
 r=analyze(raw)['circuits'][first(raw)]
 assert all(s['checks']['thermal_pe']['status']=='PENDENTE' for s in r['segments'])

def test_variant_relabel_cannot_bypass_physical_recalc(raw):
 v=deepcopy(raw);v['id']='88888888-0000-0000-0000-000000000009'
 v['conductor_study']['topology']['installation']['segments'][0]['length']['value']='21'
 for f in v['fault_scenarios']:f['id']='new'+f['id']
 for cp in v['circuits'].values():
  cp['fault_max_id']='new'+cp['fault_max_id'];cp['fault_min_id']='new'+cp['fault_min_id'];cp['thermal']['fault_scenario_id']='new'+cp['thermal']['fault_scenario_id']
 raw['selection_variants']=[v]
 assert 'antigas' in analyze(raw)['selection']['variants']['evaluations'][0]['reason']

def complete_single(raw):
 """Independent positive fixture; one radial circuit, no coordination pair."""
 s=deepcopy(raw);cs=s['conductor_study'];inst=cs['topology']['installation'];cid=first(s)
 c=inst['circuits'][0];c.update(kind='TERMINAL',downstream_board_id=None,load_ids=[l['id'] for l in inst['loads']])
 inst['calculation_runs']=[]
 inst['circuits']=[c];inst['devices']=inst['devices'][:1];inst['cable_runs']=inst['cable_runs'][:1];inst['segments']=inst['segments'][:1];inst['boards']=inst['boards'][:1]
 for name in ('board_details','segment_details'):
  ids={x['id'] for x in inst['boards' if name=='board_details' else 'segments']};cs['topology'][name]={k:v for k,v in cs['topology'][name].items() if k in ids}
 cs['circuits']={cid:cs['circuits'][cid]};cs['segments']={k:v for k,v in cs['segments'].items() if k==inst['segments'][0]['id']}
 ci=cs['circuits'][cid];ci.update(neutral_required=False,neutral_section_mm2=None,neutral_minimum=None)
 s['devices']=s['devices'][:1];s['devices'][0].update(nominal_current_a='20',i2_a='29')
 s['circuits']={cid:s['circuits'][cid]};s['fault_scenarios']=s['fault_scenarios'][:2]
 pe=deepcopy(s['fault_scenarios'][1]);pe.update(id='pe_max',kind='MAX',source_r_ohm='0.1',location='DEVICE',segment_id=None)
 s['fault_scenarios'].append(pe)
 cp=s['circuits'][cid];cp['pe_thermal']=deepcopy(cp['thermal']);cp['pe_thermal']['fault_scenario_id']='pe_max'
 return s

def test_complete_computational_convergence_preserves_normative_pending(raw):
 base=complete_single(raw);variant=deepcopy(base);variant['id']='88888888-0000-0000-0000-000000000009'
 base['selection_variants']=[variant]
 r=analyze(base)
 assert r['computational_state']=='ATENDE_ESTUDO'
 assert r['selection']['variants']['status']=='CONVERGED_STUDY'
 assert r['selection']['variants']['converged'] is True
 assert r['status']=='PENDENTE'
 assert r['professional_approval'] is False
 assert r['normative_conformity_verified'] is False

def test_extra_blocked_fault_prevents_convergence(raw):
 base=complete_single(raw);extra=deepcopy(base['fault_scenarios'][0]);extra.update(id='extra',additional_contributions=True);base['fault_scenarios'].append(extra)
 v=deepcopy(base);v['id']='88888888-0000-0000-0000-000000000009';base['selection_variants']=[v]
 r=analyze(base)
 assert r['status']=='BLOQUEADO'
 assert r['selection']['variants']['converged'] is False
