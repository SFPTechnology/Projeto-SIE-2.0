"""Source-linked references: EDP V09 pp34–37 and worked example pp42–44.
Expected values are literals/rational arithmetic, never read from the registry.
"""
import json
from copy import deepcopy
from decimal import Decimal
from pathlib import Path
from uuid import uuid4
import pytest
from pydantic import ValidationError
from fastapi.testclient import TestClient
from sie_api.main import app
from sie_api.demand import Scenario, calculate, fingerprint, save_scenario, scenario_history
from sie_api.topology import persist
from sie_api.storage import RepositorioProjetos
from sie_api import demand_registry

BASE=Path(__file__).resolve().parents[3]/'examples/f06_demanda_demo.json'

def scenario(rows,typology='RESIDENTIAL',activity=None):
    """row: table suffix, kind, total active W, fp, count, optional extra conditions."""
    raw=json.loads(BASE.read_text());inst=raw['topology']['installation']
    remove={c['id'] for c in inst['circuits'] if c['kind']=='TERMINAL'}
    keep=next(c['id'] for c in inst['circuits'] if c['kind']=='TERMINAL');remove.remove(keep)
    run_ids={c['id'] for c in inst['cable_runs'] if c['circuit_id'] in remove}
    segment_ids={x['id'] for x in inst['segments'] if x['cable_run_id'] in run_ids}
    inst['circuits']=[c for c in inst['circuits'] if c['id'] not in remove]
    inst['cable_runs']=[c for c in inst['cable_runs'] if c['id'] not in run_ids]
    inst['segments']=[c for c in inst['segments'] if c['id'] not in segment_ids]
    raw['topology']['segment_details']={k:v for k,v in raw['topology']['segment_details'].items() if k not in segment_ids}
    for detail in raw['topology']['board_details'].values():
        for bus in detail['buses']:bus['circuit_ids']=[k for k in bus['circuit_ids'] if k not in remove]
    inst['devices']=[d for d in inst['devices'] if d['id'] in {c['device_id'] for c in inst['circuits']}]
    template=inst['loads'][0];inst['load_points']=[x for x in inst['load_points'] if x['id']==template['load_point_id']];inst['loads']=[];raw['assignments']={};raw['rules']=[]
    source=inst['supplies'][0]['id'];raw['purpose']='ENTRANCE'
    raw['contexts']={source:dict(utility='EDP_SP',locality='SP_EDP_CONCESSION',edition='09',typology=typology,
                               concession_confirmed=True,consumer_unit='INDIVIDUAL',reference_date='2026-10-21',activity=activity)}
    raw['source_connections']={source:'SINGLE_PHASE_FF'}
    category={'T005':'EDP_A','T007':'EDP_B','T008':'EDP_C','T009':'EDP_D','T010':'EDP_E','T012':'EDP_F','AC-RES':'EDP_F','T013':'EDP_G','T014':'EDP_H','T015':'EDP_I'}
    for row in rows:
        table,kind,power,fp,count,*extra=row
        load=deepcopy(template);load.update(id=str(uuid4()),name=kind,active_power={'value':str(power),'unit':'W'},reactive_power=None,apparent_power=None,design_current=None)
        inst['loads'].append(load)
        a=dict(category=category.get(table,'EDP_A'),criterion='Classificação explícita da referência',group='user-label',rule_id='EDP-SP-V09-'+table,target_id=source,
               condition_evidence='Referência da fonte; condições de uso declaradas',power_factor=str(fp),quantity=count,
               equipment_kind=kind,zone='NORMAL',minimum_load_confirmed=True,power_factor_confirmed=True)
        if extra:a.update(extra[0])
        raw['assignments'][load['id']]=a
    next(c for c in inst['circuits'] if c['kind']=='TERMINAL')['load_ids']=[x['id'] for x in inst['loads']]
    return raw


def test_source_worked_example_pages42_44():
    raw=scenario([('T005','LIGHTING',200,'.55',8),('T005','LIGHTING',600,1,6),('T005','SOCKET',2800,1,13),
                  ('T007','SHOWER',10800,1,2),('T007','TAP_HEATER',3000,1,1),('T007','IRON',1000,1,1),
                  ('T009','DRYER',2500,1,1),('T009','MICROWAVE',1500,'.8',1)])
    r=calculate(Scenario.model_validate(raw));assert r['status']=='CALCULATED_SOURCE_LINKED'
    byrule={p['rule']['id']:p for p in r['parcels']}
    assert set(byrule['EDP-SP-V09-T005']['per_load_factors'].values())=={'0.59'}
    assert set(byrule['EDP-SP-V09-T007']['per_load_factors'].values())=={'0.76'}
    assert set(byrule['EDP-SP-V09-T009']['per_load_factors'].values())=={'0.7'}
    # Source rounds a to 2221 VA; exact a=24426/11 VA. b=11248; d=3062.5.
    expected=Decimal(24426)/11+Decimal('11248')+Decimal('3062.5')
    actual=Decimal(r['total']['demand']['s_va']['value'])
    assert abs(actual-expected)<Decimal('1e-22')
    assert abs(actual-Decimal('16531.5'))<Decimal('.5')
    current=Decimal(next(iter(r['by_supply'].values()))['design_current']['value_a'])
    assert abs(current-Decimal('75.1'))<Decimal('.05')
    assert all(p['source_binding']['source']['official_pdf_sha256'] for p in r['parcels'])
    assert r['normative_conformity_verified'] is False

@pytest.mark.parametrize('w,factor',[('1000','.86'),('1000.000001','.75'),('2000','.75'),('2000.1','.66'),('3000','.66'),('4000','.59'),('5000','.52'),('6000','.45'),('7000','.40'),('8000','.35'),('9000','.31'),('10000','.27'),('10000.1','.24')])
def test_table005_upper_inclusive_active_w_not_va(w,factor):
    r=calculate(Scenario.model_validate(scenario([('T005','LIGHTING',w,'.5',1)])))
    assert r['status']=='CALCULATED_SOURCE_LINKED'
    assert Decimal(next(iter(r['parcels'][0]['per_load_factors'].values())))==Decimal(factor)

@pytest.mark.parametrize('table,count,expected',[
 ('T007',1,'1'),('T007',2,'.9'),('T007',4,'.76'),('T007',7,'.55'),('T007',13,'.3'),('T007',14,'.29'),('T007',15,'.29'),('T007',16,'.28'),('T007',20,'.28'),('T007',21,'.27'),('T007',25,'.27'),('T007',26,'.26'),
 ('T008',1,'1'),('T008',2,'.76'),('T008',3,'.62'),('T008',4,'.62'),('T009',1,'1'),('T009',2,'.7'),('T009',4,'.7'),('T009',5,'.6'),('T009',7,'.5'),('T009',9,'.5'),
 ('T010',2,'.6'),('T010',7,'.33'),('T010',10,'.30'),('T010',11,'.30'),('T010',12,'.28'),('T010',15,'.28'),('T010',16,'.26'),
 ('T012',10,'1'),('T012',11,'.9'),('T012',21,'.82'),('T012',31,'.8'),('T012',41,'.77'),('T012',51,'.75'),('T015',1,'1'),('T015',2,'.56'),('T015',3,'.47'),('T015',4,'.39')])
def test_count_tables(table,count,expected):
    kind={'T007':'SHOWER','T008':'BOILER','T009':'OVEN','T010':'ELECTRIC_STOVE','T012':'AIR_CONDITIONER','T015':'HYDROMASSAGE'}[table]
    r=calculate(Scenario.model_validate(scenario([(table,kind,1000,1,count,{'central_air_conditioning':False})],'COMMERCIAL' if table=='T012' else 'RESIDENTIAL')))
    assert r['status']=='CALCULATED_SOURCE_LINKED'
    assert Decimal(r['total']['demand']['s_va']['value'])==1000*Decimal(expected)

@pytest.mark.parametrize('table,activity,power,expected',[
 ('T006-SCHOOL','SCHOOL',15000,13500),('T006-OFFICE','OFFICE',25000,23500),
 ('T006-HOSPITAL','HOSPITAL',60000,22000),('T006-HOTEL','HOTEL',25000,12000)])
def test_table006_progressive_active_w(table,activity,power,expected):
    r=calculate(Scenario.model_validate(scenario([(table,'LIGHTING',power,1,1)],'COMMERCIAL',activity)))
    assert r['status']=='CALCULATED_SOURCE_LINKED'
    assert Decimal(r['total']['demand']['s_va']['value'])==expected


def test_exceptions_and_maximum_ties():
    cases=[([('T007','SHOWER',20000,1,4,{'zone':'LOCKER_ROOM'})],'RESIDENTIAL',20000),
           ([('T012','AIR_CONDITIONER',20000,1,30,{'central_air_conditioning':True})],'COMMERCIAL',20000),
           ([('T006-SCHOOL','LIGHTING',15000,1,1,{'zone':'KITCHEN'})],'COMMERCIAL',15000),
           ([('T013','MOTOR',2000,1,2,{'ranking_power_w':'1000','coincident_start_confirmed':True})],'RESIDENTIAL',1500)]
    # Two independent 1000 W motors: only one receives factor 1 on a tie.
    for rows,typology,expected in cases:
        r=calculate(Scenario.model_validate(scenario(rows,typology,'SCHOOL' if rows[0][0]=='T006-SCHOOL' else None)))
        assert r['status']=='CALCULATED_SOURCE_LINKED'
        assert Decimal(r['total']['demand']['s_va']['value'])==expected

@pytest.mark.parametrize('change,code',[
 ('unit','CONSUMER_UNIT_SCOPE_MISMATCH'),('purpose','PURPOSE_MISMATCH'),('date','EDITION_DATE_NOT_VERIFIED'),('territory','UTILITY_SCOPE_MISMATCH'),
 ('typology','TYPOLOGY_MISMATCH'),('kind','EQUIPMENT_KIND_MISMATCH'),('count','EQUIPMENT_COUNT_PENDING'),
 ('conditions','APPLICATION_CONDITIONS_PENDING')])
def test_bound_scope_failures(change,code):
    raw=scenario([('T005','LIGHTING',1000,1,1)]);a=next(iter(raw['assignments'].values()));context=next(iter(raw['contexts'].values()))
    if change=='unit':context['consumer_unit']='COLLECTIVE'
    if change=='purpose':raw['purpose']='FEEDER'
    if change=='date':context['reference_date']='2026-01-01'
    if change=='territory':context['locality']='OTHER'
    if change=='typology':context['typology']='COMMERCIAL'
    if change=='kind':a['equipment_kind']='MOTOR'
    if change=='count':a['quantity']=None
    if change=='conditions':a['minimum_load_confirmed']=False
    r=calculate(Scenario.model_validate(raw));assert code in {p['code'] for p in r['problems']}


def test_no_client_override_and_catalog_api_and_invalidation(tmp_path,monkeypatch):
    raw=scenario([('T005','SOCKET',1000,1,1)])
    client=TestClient(app);catalog=client.get('/api/v1/demanda/catalogo').json()
    assert len(catalog['rules'])==22
    raw['rules']=[demand_registry.rule_document('EDP-SP-V09-T005')]
    with pytest.raises(ValidationError,match='controlados'):Scenario.model_validate(raw)
    raw['rules']=[];sc=Scenario.model_validate(raw);repo=RepositorioProjetos(str(tmp_path/'db'))
    pid=sc.topology.installation.project.id;persist(repo,pid,sc.topology,0);save_scenario(repo,pid,sc,1)
    data=repo.carregar(str(pid))['dados'];assert not scenario_history(data)[0]['stale']
    old=fingerprint(sc);monkeypatch.setattr(demand_registry,'CATALOG_HASH','0'*64)
    assert fingerprint(sc)!=old and scenario_history(data)[0]['stale']


def test_simultaneous_starts_and_special_equipment_maximum():
    motor={'ranking_power_w':'1000','coincident_start_confirmed':True,'simultaneous_start_group':'START_A'}
    raw=scenario([('T013','MOTOR',1000,1,1,motor),('T013','MOTOR',1000,1,1,motor),
                  ('T013','MOTOR',1500,1,1,{'ranking_power_w':'1500','coincident_start_confirmed':True})])
    r=calculate(Scenario.model_validate(raw))
    assert Decimal(r['total']['demand']['s_va']['value'])==2750
    special={'ranking_power_w':'1000','equipment_subtype':'X'}
    raw=scenario([('T014','SPECIAL_EQUIPMENT',2000,1,2,special)])
    r=calculate(Scenario.model_validate(raw))
    assert Decimal(r['total']['demand']['s_va']['value'])==1600


def test_registered_rule_group_cannot_be_split_by_user_labels():
    raw=scenario([('T007','SHOWER',10000,1,2),('T007','SHOWER',10000,1,2)])
    for i,a in enumerate(raw['assignments'].values()):a['group']=str(i)
    r=calculate(Scenario.model_validate(raw))
    assert len(r['parcels'])==1
    assert Decimal(r['total']['demand']['s_va']['value'])==15200


@pytest.mark.parametrize('count,factor',[(3,'.84'),(5,'.68'),(6,'.61'),(8,'.49'),(9,'.44'),(10,'.4'),(11,'.36'),(12,'.32')])
def test_table007_remaining_literal_cells(count,factor):
    r=calculate(Scenario.model_validate(scenario([('T007','SHOWER',100000,1,count)])))
    assert Decimal(r['total']['demand']['s_va']['value'])==100000*Decimal(factor)

@pytest.mark.parametrize('count,factor',[(1,'1'),(3,'.48'),(4,'.4'),(5,'.37'),(6,'.35'),(8,'.32'),(9,'.31')])
def test_table010_remaining_literal_cells(count,factor):
    r=calculate(Scenario.model_validate(scenario([('T010','ELECTRIC_STOVE',100000,1,count)])))
    assert Decimal(r['total']['demand']['s_va']['value'])==100000*Decimal(factor)


def test_maximum_requires_declared_ranking():
    raw=scenario([('T013','MOTOR',1000,1,1,{'ranking_power_w':'1000','coincident_start_confirmed':True}),
                  ('T013','MOTOR',2000,1,1,{'ranking_power_w':'2000','coincident_start_confirmed':True})])
    raw['assignments'][next(iter(raw['assignments']))]['ranking_power_w']=None
    r=calculate(Scenario.model_validate(raw))
    assert 'RANKING_POWER_PENDING' in {p['code'] for p in r['problems']}
