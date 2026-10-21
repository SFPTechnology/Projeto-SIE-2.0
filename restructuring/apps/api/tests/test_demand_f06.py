"""Independent arithmetic expectations; synthetic study is never normative."""
import json
from copy import deepcopy
from decimal import Decimal
from pathlib import Path
from uuid import UUID, uuid4
import pytest
from pydantic import ValidationError
from fastapi.testclient import TestClient
from sie_api.main import app
from sie_api.demand import Scenario, calculate, fingerprint, save_scenario, scenario_history
from sie_api.topology import Topology, persist
from sie_api.storage import RepositorioProjetos, ConflitoRevisao

@pytest.fixture
def raw():
    topology = json.loads((Path(__file__).resolve().parents[3]/'examples/f05_topologia_demo.json').read_text())
    for load in topology['installation']['loads']:
        load.update(active_power={'value':'800','unit':'W'}, reactive_power={'value':'600','unit':'var'}, apparent_power={'value':'1000','unit':'VA'})
    return {'id':str(uuid4()), 'name':'Estudo sintético', 'purpose':'STUDY', 'topology':topology,
        'assignments':{x['id']:{'category':'TEST','criterion':'Classificação manual de teste', 'group':'G',
                               'rule_id':'R', 'condition_evidence':'Fixture sintética; uso coincidente declarado'} for x in topology['installation']['loads']},
        'rules':[{'id':'R','version':'1','category':'TEST','purpose':'STUDY','source':'Fixture não normativa',
                  'edition':'TEST','condition':'Exemplo sintético','status':'SYNTHETIC_STUDY',
                  'bands':[{'lower_va':'0','upper_va':'1000','factor':'1'}, {'lower_va':'1000','factor':'0.5'}]}]}

def test_reference_and_reconciliation(raw):
    sc=Scenario.model_validate(raw); r=calculate(sc)
    n=len(sc.topology.installation.loads)
    assert r['total']['installed']['p_w']['value']==str(800*n)
    assert Decimal(r['total']['demand']['s_va']['value'])==500*n
    assert Decimal(r['total']['demand']['p_w']['value'])==400*n
    assert Decimal(r['total']['demand']['q_var']['value'])==300*n
    assert r['normative_conformity_verified'] is False
    for row in r['by_circuit'].values():
        assert abs(Decimal(row['design_current']['value_a'])*Decimal(row['design_current']['voltage']['value'])-Decimal(row['demand']['s_va']['value'])) < Decimal('1e-24')
    root=sc.topology.installation.boards[0]
    assert r['by_board'][str(root.id)]==r['total']
    assert sum(Decimal(p['installed']['s_va']['value']) for p in r['parcels'])==1000*n

@pytest.mark.parametrize('change,code',[
 ('missing','CLASSIFICATION_PENDING'),('rule','RULE_PENDING_OR_CONFLICT'),('category','CATEGORY_MISMATCH'),
 ('purpose','PURPOSE_MISMATCH'),('evidence','CONDITION_EVIDENCE_PENDING'),('verified','TRUSTED_NORMATIVE_REGISTRY_PENDING'),
 ('pending','TRUSTED_NORMATIVE_REGISTRY_PENDING'),('range','OUTSIDE_RULE_BANDS'),('utility','UTILITY_SCOPE_MISMATCH')])
def test_fail_closed(raw,change,code):
    a=next(iter(raw['assignments'].values())); rule=raw['rules'][0]
    if change=='missing': raw['assignments']={}
    if change=='rule': a['rule_id']='absent'
    if change=='category': a['category']='OTHER'
    if change=='purpose': rule['purpose']='ENTRANCE'
    if change=='evidence': a.pop('condition_evidence')
    if change=='verified': rule['status']='VERIFIED'
    if change=='pending': rule['status']='PENDING'
    if change=='range': rule['bands']=[{'lower_va':'200000','factor':'0.5'}]
    if change=='utility': raw['purpose']=rule['purpose']='ENTRANCE'
    r=calculate(Scenario.model_validate(raw))
    assert code in {x['code'] for x in r['problems']}
    assert r['status']=='PENDING'
    assert any(row['design_current']['value_a'] is None for row in r['by_circuit'].values())

@pytest.mark.parametrize('power', ['P_ONLY','S_ONLY','Q_ONLY','CONFLICT','NEGATIVE_Q'])
def test_powers(raw,power):
    load=raw['topology']['installation']['loads'][0]
    a=raw['assignments'][load['id']]
    if power=='P_ONLY': load['reactive_power']=load['apparent_power']=None; a['power_factor']='0.8'
    if power=='S_ONLY': load['active_power']=load['reactive_power']=None
    if power=='Q_ONLY': load['active_power']=load['apparent_power']=None
    if power=='CONFLICT': load['active_power']['value']='2000'
    if power=='NEGATIVE_Q': load['reactive_power']['value']='-600'
    r=calculate(Scenario.model_validate(raw))
    if power=='Q_ONLY': assert r['status']=='PENDING'
    elif power=='CONFLICT': assert any(x['code']=='POWER_CONFLICT' for x in r['problems'])
    else: assert r['status']=='CALCULATED_STUDY'

@pytest.mark.parametrize('factor', ['-0.1','1.01','NaN','Infinity','0.1234567890123456789012345'])
def test_invalid_factors(raw,factor):
    raw['rules'][0]['bands'][0]['factor']=factor
    with pytest.raises(ValidationError): Scenario.model_validate(raw)

def test_bands_no_overlap_and_boundary(raw):
    sc=Scenario.model_validate(raw)
    assert calculate(sc)['parcels'][0]['factor']=='0.5'
    raw['rules'][0]['bands'][1]['lower_va']='999'
    with pytest.raises(ValidationError): Scenario.model_validate(raw)

def test_current_three_phase_needs_balanced(raw):
    inst=raw['topology']['installation']
    for c in inst['circuits']: c['phases']=3;c['voltage']={'value':'400','unit':'V','basis':'FF'}
    for l in inst['loads']: l['connection']='THREE_PHASE'
    for supply in inst['supplies']:
        supply['phases']=3; supply['voltage_ff']={'value':'400','unit':'V','basis':'FF'}
    r=calculate(Scenario.model_validate(raw))
    assert all(x['design_current']['value_a'] is None for x in r['by_circuit'].values())
    raw['balanced_three_phase']=True
    r=calculate(Scenario.model_validate(raw))
    current=Decimal(next(iter(r['by_circuit'].values()))['design_current']['value_a'])
    s=Decimal(next(iter(r['by_circuit'].values()))['demand']['s_va']['value'])
    assert abs(current-s/Decimal('692.8203230275509174109785366'))<Decimal('1e-25')

def test_fingerprint_and_history(raw,tmp_path):
    sc=Scenario.model_validate(raw); repo=RepositorioProjetos(str(tmp_path/'db.sqlite'))
    pid=sc.topology.installation.project.id
    persist(repo,pid,sc.topology,0)
    save_scenario(repo,pid,sc,1)
    data=repo.carregar(str(pid))['dados']
    assert not scenario_history(data)[0]['stale']
    with pytest.raises(ValueError,match='histórico'): save_scenario(repo,pid,sc,2)
    raw['id']=str(uuid4()); raw['rules'][0]['bands'][1]['factor']='0.7'
    sc2=Scenario.model_validate(raw)
    assert fingerprint(sc)!=fingerprint(sc2)
    save_scenario(repo,pid,sc2,2)
    data=repo.carregar(str(pid))['dados']
    assert len(scenario_history(data))==2
    data['levantamento']={'changed':True}
    assert all(x['stale'] for x in scenario_history(data))
    data=repo.carregar(str(pid))['dados']
    snapshot=json.loads(data['installation_snapshot']['canonical_json'])
    snapshot['loads'][0]['active_power']['value']='900'
    from sie_api.installation_service import create_snapshot
    from sie_api.domain.installation import Installation
    data['installation_snapshot']=create_snapshot(Installation.model_validate(snapshot)).model_dump(mode='json')
    assert all(x['stale'] for x in scenario_history(data))

def test_api_and_auth(raw):
    client=TestClient(app)
    result=client.post('/api/v1/demanda/calcular',json=raw)
    assert result.status_code==200 and result.json()['status']=='CALCULATED_STUDY'
    assert client.get('/api/v1/local/projetos/'+raw['topology']['installation']['project']['id']+'/demanda').status_code in (401,503)


def test_comparison_and_changed_equipment(raw):
    from sie_api.demand import compare
    before=Scenario.model_validate(raw)
    changed=deepcopy(raw); changed['id']=str(uuid4())
    changed['topology']['installation']['loads'][0].update(active_power={'value':'1600','unit':'W'},reactive_power={'value':'1200','unit':'var'},apparent_power={'value':'2000','unit':'VA'})
    after=Scenario.model_validate(changed)
    result=compare(before,after)
    assert result['inputs_changed']
    assert Decimal(result['after']['total']['demand']['s_va']['value'])-Decimal(result['before']['total']['demand']['s_va']['value'])==500
    changed['topology']['installation']['project']['id']=str(uuid4())
    with pytest.raises(ValidationError): Scenario.model_validate(changed)


def test_storage_concurrency_and_canonical_divergence(raw,tmp_path):
    sc=Scenario.model_validate(raw); repo=RepositorioProjetos(str(tmp_path/'db.sqlite'))
    pid=sc.topology.installation.project.id
    persist(repo,pid,sc.topology,0)
    with pytest.raises(ConflitoRevisao): save_scenario(repo,pid,sc,0)
    changed=deepcopy(raw); changed['topology']['installation']['loads'][0]['active_power']['value']='900'
    with pytest.raises(ValueError,match='diverge'): save_scenario(repo,pid,Scenario.model_validate(changed),1)


def test_xss_and_false_normative_status(raw):
    raw['assignments'][next(iter(raw['assignments']))]['group']='<img src=x onerror=alert(1)>'
    r=TestClient(app).post('/api/v1/demanda/calcular',json=raw)
    assert r.status_code==200 and not r.json()['normative_conformity_verified']
    raw['rules'][0]['source']='   '
    assert TestClient(app).post('/api/v1/demanda/calcular',json=raw).status_code==422


@pytest.mark.parametrize('scope',['BOARD','SUPPLY'])
def test_explicit_scope_global_aggregation(raw,scope):
    inst=raw['topology']['installation']
    target=inst['boards'][1]['id'] if scope=='BOARD' else inst['supplies'][0]['id']
    raw['rules'][0]['scope']=scope
    for a in raw['assignments'].values(): a['target_id']=target
    r=calculate(Scenario.model_validate(raw))
    assert r['status']=='CALCULATED_STUDY'
    assert len(r['parcels'])==1 and r['parcels'][0]['target_id']==target
    assert Decimal(r['parcels'][0]['installed']['s_va']['value'])==2000
    # Diversity on a board/supply never sets final branch Ib.
    terminal=next(c for c in inst['circuits'] if c['kind']=='TERMINAL')
    assert r['by_circuit'][terminal['id']]['design_current']['value_a'] is None
    feeder=next(c for c in inst['circuits'] if c['kind']=='FEEDER')
    assert (r['by_circuit'][feeder['id']]['design_current']['value_a'] is not None)==(scope=='BOARD')


def test_invalid_target_and_scope(raw):
    raw['rules'][0]['scope']='BOARD'
    for a in raw['assignments'].values(): a['target_id']=str(uuid4())
    r=calculate(Scenario.model_validate(raw))
    assert any(p['code']=='INVALID_AGGREGATION_TARGET' for p in r['problems'])
    target=raw['topology']['installation']['boards'][1]['id']
    for a in raw['assignments'].values(): a['target_id']=target
    raw['purpose']=raw['rules'][0]['purpose']='FINAL_CIRCUIT'
    r=calculate(Scenario.model_validate(raw))
    assert any(p['code']=='SCOPE_NOT_ALLOWED_FOR_FINAL_CIRCUIT' for p in r['problems'])


def test_explicit_survey_bridge_and_quantity_once(raw):
    from sie_api.demand import project_survey
    from sie_api.load_survey import Survey
    inst=raw['topology']['installation']; project=inst['project']['id']
    building,floor,room=str(uuid4()),str(uuid4()),str(uuid4())
    loads=[{'id':str(uuid4()),'nome':'Carga '+str(i),'ambiente_id':room,'classe':'TUE','quantidade':2,
            'p_w':'400','q_var':'300','s_va':'500'} for i,_ in enumerate(inst['loads'])]
    survey=Survey.model_validate({'projeto_id':project,'nome':'Ponte explícita',
        'edificacoes':[{'id':building,'nome':'B'}], 'pavimentos':[{'id':floor,'nome':'F','edificacao_id':building}],
        'ambientes':[{'id':room,'nome':'R','pavimento_id':floor,'tipo':'TEST'}], 'cargas':loads})
    links={UUID(a['id']):UUID(b['id']) for a,b in zip(loads,inst['loads'])}
    result=project_survey(survey,Topology.model_validate(raw['topology']),links)
    assert all(x['active_power']['value']=='800' for x in result['topology']['installation']['loads'])
    assert all(x['quantity_applied_once']==2 for x in result['audit'])
    with pytest.raises(ValueError,match='bijeção'): project_survey(survey,Topology.model_validate(raw['topology']),{})
    survey.cargas[0].tensao_v=Decimal('999')
    with pytest.raises(ValueError,match='Tensão'): project_survey(survey,Topology.model_validate(raw['topology']),links)


def test_entrance_scope_and_explicit_source_current(raw):
    source=raw['topology']['installation']['supplies'][0]['id']
    raw['purpose']=raw['rules'][0]['purpose']='ENTRANCE'
    raw['rules'][0].update(scope='SUPPLY',utility='TEST',locality='CITY',typology='HOUSE',edition='TEST')
    raw['contexts']={source:{'utility':'TEST','locality':'CITY','typology':'HOUSE','edition':'TEST','concession_confirmed':True}}
    for a in raw['assignments'].values(): a['target_id']=source
    raw['source_connections']={source:'THREE_PHASE'};raw['balanced_three_phase']=True
    r=calculate(Scenario.model_validate(raw))
    assert r['status']=='CALCULATED_STUDY'
    assert r['by_supply'][source]['design_current']['value_a'] is not None
    assert all(c['design_current']['value_a'] is None for c in r['by_circuit'].values())
    raw['contexts'][source]['edition']='OTHER'
    assert calculate(Scenario.model_validate(raw))['status']=='PENDING'


def test_progressive_bands_reference(raw):
    raw['rules'][0]['mode']='PROGRESSIVE'
    raw['rules'][0]['scope']='SUPPLY'
    target=raw['topology']['installation']['supplies'][0]['id']
    for a in raw['assignments'].values(): a['target_id']=target
    r=calculate(Scenario.model_validate(raw))
    # Independent example: 1000 VA * 1 + remaining 1000 VA * 0.5 = 1500 VA.
    assert Decimal(r['total']['demand']['s_va']['value'])==1500
    assert Decimal(r['parcels'][0]['factor'])==Decimal('0.75')
    raw['rules'][0]['bands'][1]['lower_va']='1001'
    with pytest.raises(ValidationError): Scenario.model_validate(raw)
