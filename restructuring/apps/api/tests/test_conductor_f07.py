"""Independent rational arithmetic and adversarial F07 scope tests; NOT normative fixtures."""
from copy import deepcopy
from decimal import Decimal,localcontext
from fractions import Fraction
import json
from pathlib import Path
from uuid import uuid4
import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from sie_api.main import app
from sie_api import conductor_f07 as m
from sie_api.topology import Topology,persist
from sie_api.storage import RepositorioProjetos,ConflitoRevisao

D=Decimal
FIXTURE=Path(__file__).resolve().parents[3]/'examples/f07_condutores_demo.json'
@pytest.fixture
def raw(): return json.loads(FIXTURE.read_text())

def test_two_segments_reference(raw):
    r=m.analyze(m.Study.model_validate(raw))
    assert r['status']=='PENDENTE' and r['selected_commercial_section_mm2'] is None
    assert not r['normative_conformity_verified'] and not r['authoritative_for_sizing']
    for row in r['segments']:
        cap=row['criteria']['capacity']
        assert D(cap['iz_a'])==D('22.272') # 32 × 87/100 × 80/100, independently rational
        drop=row['criteria']['voltage']
        ref=Fraction(2)*Fraction(drop['length_m'])/1000*Fraction(drop['ib_a'])*(Fraction(5)*Fraction(4,5)+Fraction(1,10)*Fraction(3,5))
        with localcontext() as ctx:
            ctx.prec=110
            assert abs(D(drop['drop_v'])-D(ref.numerator)/D(ref.denominator))<D('1e-90')
    assert all(p['voltage_total']['status']=='ATENDE_ESTUDO' for p in r['paths'])

@pytest.mark.parametrize('phases,fp,r,x,expected',[(1,'1','2','7','4'),(1,'0.8','2','1','4.4'),(1,'0.6','2','1','4'),(3,'1','2','0',None)])
def test_formula_independent(phases,fp,r,x,expected):
    with localcontext() as ctx:
        ctx.prec=100
        v=m.voltage_drop(D('10'),D('100'),D(r),D(x),D(fp),phases)
        if expected: assert v==D(expected)
        else: assert abs(v*v-D('12'))<D('1e-90')
        assert m.voltage_drop(D('10'),D(0),D(r),D(x),D(fp),phases)==0

@pytest.mark.parametrize('args',[(0,1,1,1,1,1),(1,-1,1,1,1,1),(1,1,-1,1,1,1),(1,1,1,-1,1,1),(1,1,1,1,0,1),(1,1,1,1,2,1)])
def test_invalid_formula(args):
    with pytest.raises(ValueError): m.voltage_drop(*(D(v) for v in args[:-1]),args[-1])

@pytest.mark.parametrize('change',['material','insulation','method','temperature','grouping','sun','infrared','homogeneous','section','medium','extra','influence','count','revision','fractional_temp'])
def test_no_fallback(raw,change):
    seg=raw['topology']['installation']['segments'][0];run=raw['topology']['installation']['cable_runs'][0]
    si=raw['segments'][seg['id']];cond=seg['conditions']
    if change=='material':run['material']='Al'
    if change=='insulation':run['insulation']='XLPE'
    if change=='method':cond['installation_method']='B2'
    if change=='temperature':cond['ambient_temperature']['value']='41'
    if change=='fractional_temp':cond['ambient_temperature']['value']='30.0001'
    if change=='grouping':cond['grouped_circuits']=4
    if change=='sun':cond['solar_exposure']=True
    if change=='infrared':si['infrared']=True
    if change=='homogeneous':si['homogeneous']=False
    if change=='section':run['section']['value']='16'
    if change=='medium':cond['medium']='GROUND'
    if change=='extra':cond['additional_conditions']='uncovered'
    if change=='influence':raw['topology']['segment_details'][seg['id']]['external_influences']={'water':'wet'}
    if change=='count':raw['topology']['segment_details'][seg['id']]['conductor_count']=1
    if change=='revision':raw['cell_revision']='unknown'
    r=m.analyze(m.Study.model_validate(raw))
    assert r['segments'][0]['criteria']['capacity']['status']=='BLOQUEADO'
    assert r['segments'][0]['criteria']['capacity']['reason']

@pytest.mark.parametrize('change',['ci','si','imp','evidence','thermal','negative_x','kind','phase_path','origin','limit','minimum','neutral','pe'])
def test_missing_criteria_pending(raw,change):
    inst=raw['topology']['installation'];sid=inst['segments'][0]['id'];cid=inst['circuits'][0]['id']
    if change=='ci':raw['circuits'].pop(cid)
    if change=='si':raw['segments'].pop(sid)
    if change=='imp':inst['segments'][0]['impedance']=None
    if change=='evidence':raw['segments'][sid]['impedance_evidence']=None
    if change=='thermal':inst['segments'][0]['impedance']['conductor_temperature']['value']='60'
    if change=='negative_x':inst['segments'][0]['impedance']['reactance']='-0.1'
    if change=='kind':raw['segments'][sid]['impedance_kind']=None
    if change=='phase_path':raw['circuits'][cid]['phase_set']=None
    if change=='origin':raw['origin_drop_percent']=raw['origin_evidence']=None
    if change=='limit':
        for c in raw['circuits'].values(): c['total_drop_limit_percent']=c['limit_evidence']=None
    if change in ('minimum','neutral','pe'):
        for c in raw['circuits'].values():c[{'minimum':'phase_minimum','neutral':'neutral_minimum','pe':'pe_minimum'}[change]]=None
    result=m.analyze(m.Study.model_validate(raw))
    assert result['status']=='PENDENTE' and result['selected_commercial_section_mm2'] is None
    if change in ('ci','si','imp','evidence','thermal','negative_x','kind'): assert result['segments'][0]['criteria']['voltage']['status']=='BLOQUEADO'
    if change in ('phase_path','origin','limit'): assert result['paths'][0]['voltage_total']['status']=='PENDENTE'

def test_exact_threshold_no_early_rounding(raw):
    inst=raw['topology']['installation'];inst['circuits'][0]['design_current']['value']='22.27200000000000000000000001'
    result=m.analyze(m.Study.model_validate(raw))
    assert result['segments'][0]['criteria']['capacity']['status']=='REPROVADO'
    assert m.presentation(D('22.27200000000000000000000001'))==m.presentation(D('22.272'))
    assert result['status']=='REPROVADO'

def test_drop_threshold_no_rounding(raw):
    for ci in raw['circuits'].values():ci['total_drop_limit_percent']='1.1995'
    r=m.analyze(m.Study.model_validate(raw))
    assert r['paths'][0]['voltage_total']['status']=='REPROVADO'
    assert m.presentation(D(r['paths'][0]['voltage_total']['total_percent']))=='1.20'

def test_worst_segment_not_average(raw):
    seg=raw['topology']['installation']['segments'][2]
    seg['conditions']['grouped_circuits']=3
    c=raw['topology']['installation']['circuits'][1];c['design_current']['value']='20'
    result=m.analyze(m.Study.model_validate(raw))
    rows=[r for r in result['segments'] if r['circuit_id']==c['id']]
    assert [r['criteria']['capacity']['status'] for r in rows]==['ATENDE_LOTE_LIMITADO','REPROVADO']
    assert result['status']=='REPROVADO'

@pytest.mark.parametrize('change',['false_approval','float','nan','orphan','neutral_fn','phase_set'])
def test_invalid_contract(raw,change):
    ci=next(iter(raw['circuits'].values()))
    if change=='false_approval':raw['normative_conformity_verified']=True
    if change=='float':ci['power_factor']=0.8
    if change=='nan':ci['power_factor']='NaN'
    if change=='orphan':raw['circuits'][str(uuid4())]=deepcopy(ci)
    if change=='neutral_fn':ci.update(neutral_required=False,neutral_section_mm2=None,neutral_minimum=None); raw['topology']['installation']['circuits'][0]['voltage']['basis']='FN'
    if change=='phase_set':ci['phase_set']='L1_L2_L3'
    assert TestClient(app).post('/api/v1/condutores/analisar',json=raw).status_code==422

@pytest.mark.parametrize('change',['section','length','current','method','table','power_factor','minimum'])
def test_history_cascade_and_recalculate(raw,tmp_path,change,monkeypatch):
    repo=RepositorioProjetos(str(tmp_path/'test.sqlite'));study=m.Study.model_validate(raw);pid=study.topology.installation.project.id
    persist(repo,pid,study.topology,0);m.save(repo,pid,study,1)
    assert not m.history(repo.carregar(str(pid))['dados'])[0]['stale']
    old=deepcopy(raw);raw['id']=str(uuid4())
    if change=='table':
        monkeypatch.setattr(m.cell_bindings,'CELLS',m.cell_bindings.CELLS+(('TEST','99','1','1','PVC'),))
        assert m.history(repo.carregar(str(pid))['dados'])[0]['stale'];return
    if change in ('power_factor','minimum'):
        next(iter(raw['circuits'].values()))['power_factor']='0.7' if change=='power_factor' else '0.8'
        if change=='minimum':next(iter(raw['circuits'].values()))['phase_minimum']['section_mm2']='6'
    else:
        inst=raw['topology']['installation'];inst['project']['revision']=3
        if change=='section':inst['cable_runs'][0]['section']['value']='6'
        if change=='length':inst['segments'][0]['length']['value']='25'
        if change=='current':inst['circuits'][0]['design_current']['value']='25'
        if change=='method':inst['segments'][0]['conditions']['installation_method']='B2'
        persist(repo,pid,Topology.model_validate(raw['topology']),2)
        assert m.history(repo.carregar(str(pid))['dados'])[0]['stale']
    expected=2 if change in ('power_factor','minimum') else 3
    saved=m.save(repo,pid,m.Study.model_validate(raw),expected)
    items=m.history(repo.carregar(str(pid))['dados'])
    assert items[0]['stale'] and not items[1]['stale']
    assert items[0]['dependent_documents_stale'] and items[1]['dependent_protection_stale']
    assert saved['result']['input_sha256']!=m.fingerprint(m.Study.model_validate(old))
    with pytest.raises(ValueError):m.save(repo,pid,m.Study.model_validate(raw),expected+1)

def test_api_memory_and_auth(raw):
    client=TestClient(app)
    r=client.post('/api/v1/condutores/analisar',json=raw)
    assert r.status_code==200 and r.json()['input_snapshot']==m.Study.model_validate(raw).model_dump(mode='json')
    pid=raw['topology']['installation']['project']['id']
    assert client.get(f'/api/v1/local/projetos/{pid}/condutores').status_code in (401,503)

@pytest.mark.parametrize('change',['unequal_neutral','section_binding','material_binding','insulation_binding'])
def test_impedance_scope_no_inference(raw,change):
    inst=raw['topology']['installation'];sid=inst['segments'][0]['id'];ci=raw['circuits'][inst['circuits'][0]['id']]
    if change=='unequal_neutral':
        for c in inst['circuits']:
            c['voltage']={'value':'127','unit':'V','basis':'FN'}
            raw['circuits'][c['id']]['phase_set']='L1_N'
        for load in inst['loads']:load['connection']='SINGLE_PHASE_FN'
        inst['supplies'][0]['voltage_fn']={'value':'127','unit':'V','basis':'FN'}
        ci['neutral_section_mm2']='2.5'
    if change=='section_binding':raw['segments'][sid]['impedance_section_mm2']='6'
    if change=='material_binding':raw['segments'][sid]['impedance_material']='Al'
    if change=='insulation_binding':raw['segments'][sid]['impedance_insulation']='XLPE'
    result=m.analyze(m.Study.model_validate(raw))
    assert result['segments'][0]['criteria']['voltage']['status']=='BLOQUEADO'

def test_feeder_limit_enforced(raw):
    cid=raw['topology']['installation']['circuits'][0]['id']
    raw['circuits'][cid]['total_drop_limit_percent']='0.0000001'
    r=m.analyze(m.Study.model_validate(raw))
    assert r['circuits'][cid]['voltage_total']['status']=='REPROVADO'
    assert r['status']=='REPROVADO'

def test_precision_scope_rejects_unrepresentable_boundaries(raw):
    raw['origin_drop_percent']='4.'+'0'*109+'1'
    with pytest.raises(ValidationError,match='30 dígitos'):m.Study.model_validate(raw)

def test_irrational_boundary_pending(raw):
    # Formula uncertainty at exact boundary may not yield a pass.
    for seg in raw['topology']['installation']['segments']:
        seg['impedance']['resistance']=seg['impedance']['reactance']='0'
    raw['origin_drop_percent']='4'
    r=m.analyze(m.Study.model_validate(raw))
    assert all(c['voltage_total']['status']=='PENDENTE' for c in r['circuits'].values())

def test_sizing_marks_canonical_results_stale(raw,tmp_path):
    from sie_api.installation_service import create_snapshot
    from sie_api.topology import load_document
    repo=RepositorioProjetos(str(tmp_path/'s.sqlite'));study=m.Study.model_validate(raw);pid=study.topology.installation.project.id
    persist(repo,pid,study.topology,0)
    item=repo.carregar(str(pid));data=item['dados'];doc=load_document(data)
    canonical=doc.installation.model_dump(mode='json');canonical['calculation_runs'][0].update(state='VALID',output_sha256='a'*64)
    from sie_api.domain.installation import Installation
    data['installation_snapshot']=create_snapshot(Installation.model_validate(canonical)).model_dump(mode='json')
    repo.salvar(str(pid),item['nome'],data,1)
    assert load_document(repo.carregar(str(pid))['dados']).installation.calculation_runs[0].state=='VALID'
    m.save(repo,pid,study,2)
    assert load_document(repo.carregar(str(pid))['dados']).installation.calculation_runs[0].state=='STALE'


def test_server_revision_change_invalidates_memory(raw,tmp_path,monkeypatch):
    repo=RepositorioProjetos(str(tmp_path/'revision.sqlite'));study=m.Study.model_validate(raw);pid=study.topology.installation.project.id
    persist(repo,pid,study.topology,0);m.save(repo,pid,study,1)
    monkeypatch.setattr(m.cell_bindings,'REVISION','NEW_SOURCE_REVISION')
    assert m.history(repo.carregar(str(pid))['dados'])[0]['stale']
