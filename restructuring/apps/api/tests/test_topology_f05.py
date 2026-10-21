"""F05 acceptance and hostile inputs; fixtures are explicitly non-normative."""
from copy import deepcopy
from decimal import Decimal
import json
from pathlib import Path
from uuid import UUID
import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from sie_api.main import app
from sie_api.topology import Topology, report, inspect_topology, persist, load_document, topology_hash
from sie_api.storage import RepositorioProjetos, ConflitoRevisao
from sie_api.installation_service import create_snapshot, calculation_status, CalculationRecord

FIXTURE = Path(__file__).resolve().parents[3] / 'examples/f05_topologia_demo.json'
@pytest.fixture
def raw():
    return json.loads(FIXTURE.read_text())


def test_qdg_qd1_heterogeneous_segments(raw):
    r = report(Topology.model_validate(raw))
    path = r['paths'][0]
    assert len(path['board_ids']) == 2
    assert [leg['kind'] for leg in path['legs']] == ['FEEDER', 'TERMINAL']
    assert Decimal(path['length_m']) == Decimal('22.5')
    segments = path['legs'][1]['runs'][0]['segments']
    assert [s['conditions']['installation_method'] for s in segments] == ['DECLARED_A', 'DECLARED_B']
    assert r['definitive_short_circuit_allowed'] is False
    assert any(w['code'] == 'SOURCE_UNCONFIRMED' for w in r['warnings'])


@pytest.mark.parametrize('change', ['orphan', 'cycle', 'duplicate_origin', 'missing_phases', 'bus', 'metadata', 'discontinuous', 'unit', 'negative_length', 'frequency'])
def test_invalid_scenarios(raw, change):
    i = raw['installation']
    if change == 'orphan': i['circuits'][1]['board_id'] = '99999999-0000-0000-0000-000000000001'
    if change == 'cycle':
        i['boards'][0]['supply_id'] = None
        i['circuits'][1].update(kind='FEEDER', load_ids=[], downstream_board_id=i['boards'][0]['id'])
        i['loads'].pop(0)
        i['supplies'] = []
        raw['source_details'] = {}
    if change == 'duplicate_origin': i['boards'][1]['supply_id'] = i['supplies'][0]['id']
    if change == 'missing_phases': del i['circuits'][1]['phases']
    if change == 'bus':
        list(raw['board_details'].values())[0]['buses'][0]['circuit_ids'].append(i['circuits'][1]['id'])
    if change == 'metadata': raw['segment_details']['99999999-0000-0000-0000-000000000001'] = next(iter(raw['segment_details'].values()))
    if change == 'discontinuous': raw['segment_details'][i['segments'][2]['id']]['route_from'] = 'disconnected'
    if change == 'unit': i['segments'][0]['length']['unit'] = 'km'
    if change == 'negative_length': i['segments'][0]['length']['value'] = '-1'
    if change == 'frequency':
        list(raw['source_details'].values())[0]['impedance'] = {'resistance':'0.1', 'reactance':'0.01', 'unit':'ohm', 'frequency_hz':'50', 'confirmed':True, 'origin':{'reference':'synthetic','method':'DOCUMENTED'}}
    r = inspect_topology(raw)
    assert not r['valid'] and r['errors']
    if change == 'cycle': assert 'acyclic' in r['errors'][0]['message']


@pytest.mark.parametrize('change', ['length', 'grouping', 'temperature', 'method', 'soil', 'influence', 'source'])
def test_changes_invalidate_fingerprint_and_results(raw, tmp_path, change):
    repo = RepositorioProjetos(str(tmp_path/'local.sqlite'))
    doc = Topology.model_validate(raw)
    project = doc.installation.project.id
    # Existing calculation remains a historical record, never silently overwritten.
    result = persist(repo, project, doc, 0)
    before = result['topology_sha256']
    raw['installation']['project']['revision'] = 2
    seg = raw['installation']['segments'][0]
    details = raw['segment_details'][seg['id']]
    if change == 'length': seg['length']['value'] = '11'
    if change == 'grouping': seg['conditions']['grouped_circuits'] = 2
    if change == 'temperature': seg['conditions']['ambient_temperature']['value'] = '41'
    if change == 'method': seg['conditions']['installation_method'] = 'OTHER_DECLARED'
    if change == 'soil': details['soil'] = 'Solo declarado diferente'
    if change == 'influence': details['external_influences']['water'] = 'declared humidity'
    if change == 'source': list(raw['source_details'].values())[0]['utility'] = 'Utility synthetic changed'
    saved = persist(repo, project, Topology.model_validate(raw), 1)
    assert saved['topology_sha256'] != before and saved['results_stale']
    data = repo.carregar(str(project))['dados']
    loaded = load_document(data)
    assert loaded.installation.calculation_runs[0].state == 'STALE'
    assert loaded.installation.project.revision == 2
    old = repo.carregar_revisao(str(project), 1)
    assert old['dados']['topology_sha256'] == before
    with pytest.raises(ConflitoRevisao): persist(repo, project, Topology.model_validate(raw), 1)


def test_revision_only_not_physical_change(raw):
    old = topology_hash(Topology.model_validate(raw))
    raw['installation']['project']['revision'] = 2
    assert topology_hash(Topology.model_validate(raw)) == old


def test_multiple_runs_not_added_as_series(raw):
    i = raw['installation']; run = deepcopy(i['cable_runs'][1]); seg = deepcopy(i['segments'][1])
    run['id'] = '99999999-0000-0000-0000-000000000001'
    seg['id'] = '99999999-0000-0000-0000-000000000002'
    seg['cable_run_id'] = run['id']; run['segment_ids'] = [seg['id']]
    i['cable_runs'].append(run);i['segments'].append(seg)
    r=report(Topology.model_validate(raw))
    assert r['paths'][0]['length_m'] is None
    assert r['paths'][0]['length_status'] == 'AMBIGUOUS_RUNS'


def test_missing_metadata_explicit_pending(raw):
    raw['source_details']={};raw['segment_details']={};raw['board_details']={}
    r=report(Topology.model_validate(raw))
    assert r['valid'] and len(r['warnings']) == 7


def test_api_auth_revision_roundtrip_and_preserve_f04(raw, monkeypatch, tmp_path):
    token='synthetic-test-token-1234567890'
    monkeypatch.setenv('SIE_LOCAL_API_TOKEN',token)
    monkeypatch.setenv('SIE_LOCAL_DB_PATH',str(tmp_path/'api.sqlite'))
    c=TestClient(app);pid=raw['installation']['project']['id'];url=f'/api/v1/local/projetos/{pid}/topologia'
    headers={'Authorization':'Bearer '+token}
    assert c.post('/api/v1/topologia/validar',json=raw).json()['valid']
    assert c.put(url,json={'document':raw,'expected_revision':0}).status_code==401
    repo=RepositorioProjetos(str(tmp_path/'api.sqlite'))
    repo.salvar(pid,'fixture',{'levantamento':{'sentinel':'F04 intacta'}},0)
    raw['installation']['project']['revision']=2
    payload={'document':raw,'expected_revision':1}
    assert c.put(url,json=payload,headers=headers).status_code==200
    assert c.put(url,json=payload,headers=headers).status_code==409
    saved=c.get(url,headers=headers).json()
    assert saved['revision']==2 and saved['document']['segment_details']==raw['segment_details']
    assert repo.carregar(pid)['dados']['levantamento']=={'sentinel':'F04 intacta'}
    raw['installation']['segments'][0]['length']['value']='-9'
    assert c.put(url,json={'document':raw,'expected_revision':2},headers=headers).status_code==422
    assert c.get(url,headers=headers).json()['revision']==2


def test_old_snapshot_serialization_unchanged(raw):
    # F05 metadata does not alter or invalidate historical F02 canonical bytes.
    from sie_api.installation_service import InstallationSnapshot
    doc=Topology.model_validate(raw)
    snap=create_snapshot(doc.installation)
    assert InstallationSnapshot.model_validate_json(snap.model_dump_json())==snap


def test_exact_decimal_path_without_context_rounding(raw):
    raw['installation']['segments'][0]['length']['value']='1000000000000000000000000000000000000000'
    path=report(Topology.model_validate(raw))['paths'][0]
    assert path['length_m']=='1000000000000000000000000000000000000012.5'


def test_isolated_multiple_sources_no_parallelism(raw):
    i=raw['installation']
    source=deepcopy(i['supplies'][0]);source['id']='30000000-0000-0000-0000-000000000001'
    i['supplies'].append(source)
    i['boards'][1]['supply_id']=source['id']
    feeder=i['circuits'].pop(0)
    i['devices']=[d for d in i['devices'] if d['id']!=feeder['device_id']]
    run=i['cable_runs'].pop(0)
    i['segments']=[s for s in i['segments'] if s['id'] not in run['segment_ids']]
    raw['segment_details']={key:value for key,value in raw['segment_details'].items() if key not in run['segment_ids']}
    root=raw['board_details'][i['boards'][0]['id']]
    root['buses'][0]['circuit_ids']=[]
    r=report(Topology.model_validate(raw))
    assert r['paths'][0]['source_id']==source['id']
    assert r['paths'][0]['length_m']=='12.5'
    # Reintroducing two simultaneous origins is not supported.
    i['circuits'].append(feeder)
    with pytest.raises(ValidationError): Topology.model_validate(raw)


def test_actual_concurrent_writers_one_wins(raw, tmp_path):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier
    path=str(tmp_path/'concurrent.sqlite');repo=RepositorioProjetos(path)
    doc=Topology.model_validate(raw)
    persist(repo,doc.installation.project.id,doc,0)
    raw['installation']['project']['revision']=2
    barrier=Barrier(2)
    def write(length):
        data=deepcopy(raw);data['installation']['segments'][0]['length']['value']=length
        local=RepositorioProjetos(path);barrier.wait()
        try:
            persist(local,doc.installation.project.id,Topology.model_validate(data),1)
            return 'saved'
        except ConflitoRevisao:
            return 'conflict'
    with ThreadPoolExecutor(2) as pool:
        assert sorted(pool.map(write,['11','12']))==['conflict','saved']
    assert repo.carregar(str(doc.installation.project.id))['revisao']==2


def test_metadata_cannot_shadow_authoritative_graph(raw):
    doc=Topology.model_validate(raw)
    data={'installation_snapshot': create_snapshot(doc.installation).model_dump(mode='json'),
          'topology_metadata': {'installation': raw['installation']}}
    with pytest.raises(ValueError, match='conectividade canônica'):
        load_document(data)


def test_source_unknown_is_null_not_blank(raw):
    next(iter(raw['source_details'].values()))['utility']='  '
    assert inspect_topology(raw)['valid'] is False
