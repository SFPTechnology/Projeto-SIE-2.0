"""Source-linked F07 reference cases: manufacturer tables, rational math and hostile scope."""
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
from sie_api import conductor_selection_f07 as s
from sie_api import conductor_registry_f07 as registry
from sie_api.conductor_f07 import voltage_drop
from sie_api.topology import Topology,persist,load_document
from sie_api.storage import RepositorioProjetos,ConflitoRevisao

D=Decimal
ROOT=Path(__file__).resolve().parents[3]
@pytest.fixture
def raw():return json.loads((ROOT/'examples/f07_selecao_fonte_vinculada.json').read_text())


def standalone(raw):
    """One real model path, but a synthetic 10A/100m/220V input for audit."""
    t=raw['topology'];i=t['installation'];c=i['circuits'][1];device=next(d for d in i['devices'] if d['id']==c['device_id'])
    c['board_id']=i['boards'][0]['id'];device['board_id']=c['board_id']
    i['boards']=i['boards'][:1];i['circuits']=[c];i['devices']=[device]
    i['loads']=[x for x in i['loads'] if x['id'] in c['load_ids']]
    i['cable_runs']=[r for r in i['cable_runs'] if r['circuit_id']==c['id']]
    segids=i['cable_runs'][0]['segment_ids'];i['segments']=[x for x in i['segments'] if x['id'] in segids]
    for seg in i['segments']:seg['length']['value']='50'
    i['calculation_runs']=[]
    t['board_details']={};t['segment_details']={k:v for k,v in t['segment_details'].items() if k in segids}
    raw['circuits']={c['id']:raw['circuits'][c['id']]};raw['segments']={k:v for k,v in raw['segments'].items() if k in segids}
    return raw


def test_catalog_is_server_owned_and_concordant():
    c=registry.catalog()
    assert c['source']['sha256']=='1729461681fa12bbfe03ea92d26dfb2299c148670d3133046a52f8caf311e4d7'
    assert c['scope']['frequency_hz']=='60'
    assert [(r['section_mm2'],r['iz_base_a']) for r in c['sections']]==[('2.5','24'),('4','32'),('6','41'),('10','57')]
    assert len(registry.catalog_hash())==64
    c['sections'][0]['iz_base_a']='999'
    assert registry.catalog()['sections'][0]['iz_base_a']=='24'

@pytest.mark.parametrize('section,r,x,expected',[
 ('2.5','8.87','0.12',Fraction(1792,125)),('4','5.52','0.11',Fraction(2241,250)),
 ('6','3.69','0.10',Fraction(753,125)),('10','2.19','0.10',Fraction(453,125))])
def test_independent_rational_reference(section,r,x,expected):
    with localcontext() as ctx:
        ctx.prec=200
        result=voltage_drop(D('10'),D('100'),D(r),D(x),D('0.8'),1)
        assert result==D(expected.numerator)/D(expected.denominator)
        assert result*100/D(220)==D((expected*Fraction(5,11)).numerator)/D((expected*Fraction(5,11)).denominator)

@pytest.mark.parametrize('section,pf,printed',[
 ('2.5','0.8','14.33'),('4','0.8','8.96'),('6','0.8','6.03'),('10','0.8','3.63'),
 ('2.5','0.95','16.93'),('4','0.95','10.56'),('6','0.95','7.07'),('10','0.95','4.23')])
def test_independent_manufacturer_precomputed_drop_table(section,pf,printed):
    # Independent expected values transcribed visually from p24/table19;
    # Rca/XL on p33/table28 are separately printed and rounded.
    row=next(r for r in registry.catalog()['sections'] if r['section_mm2']==section)
    with localcontext() as ctx:
        ctx.prec=200
        result=voltage_drop(D(1),D(1000),D(row['rca_ohm_km']),D(row['xl_ohm_km']),D(pf),1)
        rounding_bound=D('.005')*(2*(D(pf)+(1-D(pf)**2).sqrt())+1)
        assert abs(result-D(printed))<=rounding_bound<D('.02')


def test_selection_100m_needs_6mm2_by_terminal_limit(raw):
    raw=standalone(raw);req=s.Selection.model_validate(raw);r=s.select(req)
    assert r['status']=='SELECTED_SOURCE_LINKED'
    cid=raw['topology']['installation']['circuits'][0]['id']
    assert r['selected_sections_by_circuit'][cid]=={'phase_mm2':'6','neutral_mm2':None,'pe_mm2':'6'}
    assert [it['sections'][cid]['phase_mm2'] for it in r['iterations']]==['2.5','4','6']
    assert r['iterations'][1]['failures']==[{'circuit_id':cid,'criterion':'voltage_terminal'}]
    assert not r['normative_conformity_verified'] and not r['professional_approval'] and not r['authoritative_for_sizing']
    assert r['f08_protection_checks_pending']
    assert r['memory']['circuits'][cid]['voltage_total']['status']=='ATENDE_FONTE_VINCULADA'


def test_all_segments_and_feed_total_limit(raw):
    i=raw['topology']['installation'];i['segments'][0]['length']['value']='80'
    i['segments'][1]['length']['value']='50';i['segments'][2]['length']['value']='50'
    # Feeder own drop and terminal global drop jointly force growth.
    r=s.select(s.Selection.model_validate(raw))
    assert r['status']=='SELECTED_SOURCE_LINKED' and len(r['iterations'])>1
    assert any(f['criterion']=='voltage_total' for it in r['iterations'] for f in it['failures'])
    assert all(cr['voltage_total']['status']=='ATENDE_FONTE_VINCULADA' for cr in r['memory']['circuits'].values())
    assert all(check['status'] in ('ATENDE_FONTE_VINCULADA','NAO_APLICAVEL') for row in r['memory']['segments'] for check in row['criteria'].values())


def test_all_four_capacity_transitions_and_exact_bound(raw):
    raw=standalone(raw);i=raw['topology']['installation'];cid=i['circuits'][0]['id']
    for seg in i['segments']:seg['length']['value']='0.01'
    for current,section in [('24','2.5'),('24.000000000000000001','4'),('32.000000000000000001','6'),('41.000000000000000001','10')]:
        i['circuits'][0]['design_current']['value']=current
        result=s.select(s.Selection.model_validate(raw))
        assert result['status']=='SELECTED_SOURCE_LINKED'
        assert result['selected_sections_by_circuit'][cid]['phase_mm2']==section
    i['circuits'][0]['design_current']['value']='57.00000000000000000000001'
    r=s.select(s.Selection.model_validate(raw))
    assert r['status']=='NO_SOLUTION_IN_CATALOG' and r['selected_sections_by_circuit'] is None

@pytest.mark.parametrize('temperature,expected',[('30','24'),('40','20.88')])
def test_temperature_exact_cells(raw,temperature,expected):
    raw=standalone(raw)
    for seg in raw['topology']['installation']['segments']:
        seg['length']['value']='0.01';seg['conditions']['ambient_temperature']['value']=temperature
    result=s.select(s.Selection.model_validate(raw))
    assert all(D(r['criteria']['capacity']['iz_a'])==D(expected) for r in result['memory']['segments'])

@pytest.mark.parametrize('layout,expected_count,expected_pe',[('SAME_CLOSED_CONDUIT',3,'2.5'),('SEPARATE_MECHANICALLY_PROTECTED',2,'2.5'),('SEPARATE_UNPROTECTED',2,'4')])
def test_pe_installation_minimums(raw,layout,expected_count,expected_pe):
    for ci in raw['circuits'].values():ci['pe_layout']=layout
    for meta in raw['topology']['segment_details'].values():meta['conductor_count']=expected_count
    r=s.select(s.Selection.model_validate(raw))
    assert r['status']=='SELECTED_SOURCE_LINKED'
    assert all(row['pe_mm2']==expected_pe for row in r['selected_sections_by_circuit'].values())


def test_neutral_same_section_for_fn(raw):
    i=raw['topology']['installation'];i['supplies'][0]['voltage_fn']={'value':'220','unit':'V','basis':'FN'};i['supplies'][0]['voltage_ff']['value']='380'
    for circuit in i['circuits']:circuit['voltage']['basis']='FN'
    for load in i['loads']:load['connection']='SINGLE_PHASE_FN'
    for ci in raw['circuits'].values():ci.update(phase_set='L1_N',neutral_required=True)
    r=s.select(s.Selection.model_validate(raw))
    assert r['status']=='SELECTED_SOURCE_LINKED'
    assert all(x['phase_mm2']==x['neutral_mm2'] for x in r['selected_sections_by_circuit'].values())


def group_two(raw):
    i=raw['topology']['installation'];members=[i['segments'][1]['id'],i['segments'][3]['id']]
    for circuit in i['circuits'][1:]:circuit['design_current']['value']='20'
    for seg in i['segments']:
        seg['length']['value']='0.01'
        if seg['id'] in members:
            seg['conditions'].update(grouped_circuits=2,ambient_temperature={'value':'40','unit':'degC'})
    raw['groups']={'G1':{'segment_ids':members}}
    return raw


def test_grouping_verified_members_grow_together(raw):
    raw=group_two(raw);i=raw['topology']['installation'];i['segments'][1]['length']['value']='100'
    result=s.select(s.Selection.model_validate(raw))
    assert result['status']=='SELECTED_SOURCE_LINKED'
    ids=[c['id'] for c in i['circuits'][1:]]
    for it in result['iterations']:
        assert it['sections'][ids[0]]['phase_mm2']==it['sections'][ids[1]]['phase_mm2']
    assert result['selected_sections_by_circuit'][ids[0]]['phase_mm2']==result['selected_sections_by_circuit'][ids[1]]['phase_mm2']

@pytest.mark.parametrize('change,code',[('missing','GROUP_MEMBERS'),('current','GROUP_CURRENT'),('count','GROUP_COUNT')])
def test_grouping_cannot_reuse_stale_homogeneous_declaration(raw,change,code):
    raw=group_two(raw)
    if change=='missing':raw['groups']={}
    if change=='current':raw['topology']['installation']['circuits'][2]['design_current']['value']='21'
    if change=='count':raw['topology']['installation']['segments'][1]['conditions']['grouped_circuits']=3
    r=s.select(s.Selection.model_validate(raw))
    assert r['status']=='BLOQUEADO' and code in {x['code'] for x in r['problems']}
    assert r['selected_sections_by_circuit'] is None

@pytest.mark.parametrize('change,code',[
 ('catalog','CATALOG_VERSION'),('future','REFERENCE_DATE'),('past','REFERENCE_DATE'),('frequency','FREQUENCY'),
 ('earth','EARTHING'),('method','METHOD'),('medium','ENVIRONMENT'),('solar','ENVIRONMENT'),('infrared','ENVIRONMENT'),
 ('ambient','TEMPERATURE'),('thermal','CONDUCTOR_TEMPERATURE'),('material','MATERIAL_INSULATION'),('insulation','MATERIAL_INSULATION'),
 ('metal','PHYSICAL_SCOPE'),('influence','PHYSICAL_SCOPE'),('count','PHYSICAL_SCOPE'),('mixed_pf','ACCUMULATION_MODEL'),
 ('ci','CIRCUIT_DATA'),('si','SEGMENT_DATA'),('phase','CONNECTION'),('group4','GROUP_RANGE')])
def test_unsupported_scope_has_explicit_block(raw,change,code):
    i=raw['topology']['installation'];seg=i['segments'][0];cid=i['circuits'][0]['id'];sid=seg['id']
    if change=='catalog':raw['catalog_version']='unknown'
    if change=='future':raw['reference_date']='2027-01-01'
    if change=='past':raw['reference_date']='2005-01-01'
    if change=='frequency':i['supplies'][0]['frequency_hz']='50'
    if change=='earth':i['supplies'][0]['earthing_system']='TN-C'
    if change=='method':seg['conditions']['installation_method']='B2'
    if change=='medium':seg['conditions']['medium']='GROUND'
    if change=='solar':seg['conditions']['solar_exposure']=True
    if change=='infrared':raw['segments'][sid]['infrared']=True
    if change=='ambient':seg['conditions']['ambient_temperature']['value']='30.0001'
    if change=='thermal':seg['conditions']['conductor_temperature']['value']='69'
    if change=='material':i['cable_runs'][0]['material']='Al'
    if change=='insulation':i['cable_runs'][0]['insulation']='XLPE'
    if change=='metal':raw['topology']['segment_details'][sid]['containment_material']='aço'
    if change=='influence':raw['topology']['segment_details'][sid]['external_influences']={'water':'wet'}
    if change=='count':raw['topology']['segment_details'][sid]['conductor_count']=4
    if change=='mixed_pf':raw['circuits'][cid]['power_factor']='0.9'
    if change=='ci':raw['circuits'].pop(cid)
    if change=='si':raw['segments'].pop(sid)
    if change=='phase':raw['circuits'][cid]['phase_set']='L1_N'
    if change=='group4':seg['conditions']['grouped_circuits']=4
    result=s.select(s.Selection.model_validate(raw))
    assert result['status']=='BLOQUEADO' and code in {x['code'] for x in result['problems']}
    assert result['selected_sections_by_circuit'] is None


def test_fn_insulation_uo_over450_rejected(raw):
    i=raw['topology']['installation'];i['supplies'][0]['voltage_fn']={'value':'600','unit':'V','basis':'FN'}
    for c in i['circuits']:c['voltage']={'value':'600','unit':'V','basis':'FN'}
    for load in i['loads']:load['connection']='SINGLE_PHASE_FN'
    for ci in raw['circuits'].values():ci.update(phase_set='L1_N',neutral_required=True)
    r=s.select(s.Selection.model_validate(raw))
    assert r['status']=='BLOQUEADO' and 'INSULATION_UO' in {x['code'] for x in r['problems']}


def test_no_solution_and_boundary_not_false_pass(raw):
    raw=standalone(raw);i=raw['topology']['installation'];i['circuits'][0]['voltage']['value']='358.4';i['supplies'][0]['voltage_ff']['value']='358.4'
    r=s.select(s.Selection.model_validate(raw))
    assert r['status']=='PENDENTE' and r['selected_sections_by_circuit'] is None
    # Separate scenario: avoid retaining the exact local boundary above.
    i['circuits'][0]['voltage']['value']='220';i['supplies'][0]['voltage_ff']['value']='220'
    raw['origin_drop_percent']='5.1'
    r=s.select(s.Selection.model_validate(raw))
    assert r['status']=='NO_SOLUTION_IN_CATALOG' and r['selected_sections_by_circuit'] is None

@pytest.mark.parametrize('change',['float','extra_approval','override_table','product','harmonics','duplicate_group','orphan_group','special_application'])
def test_selection_api_rejects_injected_contract(raw,change):
    ci=next(iter(raw['circuits'].values()));si=next(iter(raw['segments'].values()))
    if change=='float':ci['power_factor']=0.8
    if change=='extra_approval':raw['normative_conformity_verified']=True
    if change=='override_table':raw['sections']=[{'section_mm2':'1','iz_base_a':'9999'}]
    if change=='product':si['product']='PRYSMIAN_SUPERASTIC_FLEX'
    if change=='harmonics':ci['regime']='HARMONIC'
    if change=='duplicate_group':raw['groups']={'G':{'segment_ids':[next(iter(raw['segments']))]*2}}
    if change=='orphan_group':raw['groups']={'G':{'segment_ids':[next(iter(raw['segments'])),str(uuid4())]}}
    if change=='special_application':raw['application']='PUBLIC_HIGH_OCCUPANCY_SPECIAL_ESCAPE'
    assert TestClient(app).post('/api/v1/condutores/selecionar',json=raw).status_code==422


def test_api_catalog_and_selection(raw):
    client=TestClient(app);c=client.get('/api/v1/condutores/catalogo')
    assert c.status_code==200 and len(c.json()['sections'])==4
    result=client.post('/api/v1/condutores/selecionar',json=raw)
    assert result.status_code==200 and result.json()['status']=='SELECTED_SOURCE_LINKED'
    assert result.json()['catalog_sha256']==c.json()['catalog_sha256']
    assert not result.json()['normative_conformity_verified']

@pytest.mark.parametrize('change',['section','current','route','method','catalog_version','source_hash','parameter'])
def test_source_selection_history_invalidation(raw,tmp_path,change,monkeypatch):
    repo=RepositorioProjetos(str(tmp_path/'selection.sqlite'));request=s.Selection.model_validate(raw);pid=request.topology.installation.project.id
    persist(repo,pid,request.topology,0);s.save_selection(repo,pid,request,1)
    assert not s.selection_history(repo.carregar(str(pid))['dados'])[0]['stale']
    if change in ('catalog_version','source_hash'):
        new=deepcopy(registry.CATALOG)
        if change=='catalog_version':new['catalog_version']='NEW_VERIFIED_REVISION'
        if change=='source_hash':new['source']['sha256']='b'*64
        monkeypatch.setattr(registry,'CATALOG',new)
        h=s.selection_history(repo.carregar(str(pid))['dados'])[0]
        assert h['stale'] and h['dependent_documents_stale'] and h['dependent_protection_stale'];return
    raw['id']=str(uuid4())
    if change=='parameter':
        for ci in raw['circuits'].values():ci['power_factor']='0.7'
        expected=2
    else:
        i=raw['topology']['installation'];i['project']['revision']=3
        if change=='section':i['cable_runs'][0]['section']['value']='6'
        if change=='current':i['circuits'][0]['design_current']['value']='25'
        if change=='route':i['segments'][0]['length']['value']='25'
        if change=='method':i['segments'][0]['conditions']['installation_method']='B2'
        persist(repo,pid,Topology.model_validate(raw['topology']),2);expected=3
        assert s.selection_history(repo.carregar(str(pid))['dados'])[0]['stale']
    saved=s.save_selection(repo,pid,s.Selection.model_validate(raw),expected)
    h=s.selection_history(repo.carregar(str(pid))['dados'])
    assert h[0]['stale'] and not h[-1]['stale']
    assert all(cr.state=='STALE' for cr in load_document(repo.carregar(str(pid))['dados']).installation.calculation_runs)
    assert saved['revision']==expected+1
    with pytest.raises(ValueError):s.save_selection(repo,pid,s.Selection.model_validate(raw),expected+1)


@pytest.mark.parametrize('change',['missing_iz','invalid_source_hash','missing_minimum','missing_factor','nonfinite_impedance','invalid_date','incompatible_frequency','pe_outside_catalog','limit_outside_range','long_edition','long_reference','phase_outside_catalog'])
def test_invalid_catalog_is_rejected_without_http500(raw,monkeypatch,change):
    c=deepcopy(registry.CATALOG)
    if change=='missing_iz':c['sections'][0].pop('iz_base_a')
    if change=='invalid_source_hash':c['source']['sha256']='invalid'
    if change=='missing_minimum':c['minimums']['phase'].pop('POWER')
    if change=='missing_factor':c['corrections']['grouping'].pop('1')
    if change=='nonfinite_impedance':c['sections'][0]['rca_ohm_km']='NaN'
    if change=='invalid_date':c['source']['verified_on']='invalid'
    if change=='incompatible_frequency':c['scope']['frequency_hz']='50'
    if change=='pe_outside_catalog':c['minimums']['pe_separate_unprotected_floor_mm2']='100'
    if change=='limit_outside_range':c['voltage']['total_origin_limit_percent']='101'
    if change=='long_edition':c['source']['edition']='x'*101
    if change=='long_reference':c['sections'][0]['impedance_reference']='x'*500
    if change=='phase_outside_catalog':c['minimums']['phase']['POWER']='1000'
    monkeypatch.setattr(registry,'CATALOG',c)
    r=TestClient(app).post('/api/v1/condutores/selecionar',json=raw)
    assert r.status_code==200 and r.json()['status']=='BLOQUEADO'
    assert r.json()['problems'][0]['code']=='CATALOG_INVALID'
    assert TestClient(app).get('/api/v1/condutores/catalogo').status_code==422
