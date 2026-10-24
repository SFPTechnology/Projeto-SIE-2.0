"""Real F10 pipeline: parser, motor, SQLite, imported asset and PDF."""
import json
from io import BytesIO
import pytest
from pypdf import PdfReader
from test_persisted_source_f10_sqlite import test_real_f05_parser_run_and_sqlite_publish_without_parser_mocks as prepare_w1
from sie_api.storage import RepositorioProjetos
from sie_api.floorplan_f10 import import_svg_asset
from sie_api.persisted_source_f10 import publish_from_repository, verify_against_repository, recover_registered_artifacts
from sie_api.artifact_store_f10 import verify_verified_bundle
from sie_api.representation_f10 import ArtifactError


def prepare_full(tmp_path):
    prepare_w1(tmp_path)
    repo = RepositorioProjetos(tmp_path / 'real-f05.sqlite')
    with repo._conectar() as db:
        pid = db.execute('SELECT id FROM projetos').fetchone()[0]
    saved = repo.carregar(pid)
    data = saved['dados']
    installation = json.loads(data['installation_snapshot']['canonical_json'])
    rid = installation['calculation_runs'][0]['id']
    panel = installation['boards'][0]['id']
    svg = b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 80"><rect width="100" height="80" fill="white"/></svg>'
    data['calculation_runs_f10'] = {installation['circuits'][0]['id']: rid}
    data['floor_plan_f10'] = {
        'schema_version':'SIE_FLOOR_PLAN_V1','id':'fixture-plan','revision_id':'2','geometry_revision':1,
        'source_ref':'fixture-drawing','authorization_reference':'synthetic-owner-consent','units':'m',
        'width':100,'height':80,'model_units_per_canvas_unit':.1,
        'asset':import_svg_asset(svg,'fixture-drawing','synthetic-owner-consent'),
        'calibration':{'canvas_distance':50,'model_distance':5,'relative_tolerance':.001,
                       'confirmed_by':'test-owner','confirmed_at':'2026-10-24T12:00:00Z'},
        'walls':[],'paths':[],
        'placements':[{'element_id':panel,'x':10,'y':20,'symbol_id':'panel','label':'Fixture panel'}]}
    repo.salvar(pid,saved['nome'],data,1)
    repo.executar_calculo_f10(pid,2,rid)
    return repo,pid,rid


def test_full_real_pipeline_pdf_manifest_and_adulteration(tmp_path):
    repo,pid,rid=prepare_full(tmp_path)
    target=tmp_path/'full'/'bundle'
    manifest=publish_from_repository(repo,pid,2,rid,'full-v1',target,full=True)
    assert {'report.pdf','memorial.json','floor_plan.svg','equipment.json','symbols.json'} <= set(manifest['files_sha256'])
    pdf=PdfReader(BytesIO((target/'report.pdf').read_bytes()))
    assert pid in ''.join(page.extract_text() for page in pdf.pages)
    assert verify_verified_bundle(target)['integrity']=='VERIFIED'
    assert verify_against_repository(repo,target)['currentness']=='CURRENT'
    assert json.loads((target/'snapshot.json').read_text())['full_f10'] is True
    (target/'report.pdf').write_bytes(b'%PDF-corrupted')
    with pytest.raises(ArtifactError): verify_verified_bundle(target)


def test_full_recovery_retains_mode_before_files(tmp_path,monkeypatch):
    repo,pid,rid=prepare_full(tmp_path)
    target=tmp_path/'full-recovery'/'bundle'
    import sie_api.persisted_source_f10 as adapter
    original=adapter.publish_prebuilt_bundle
    monkeypatch.setattr(adapter,'publish_prebuilt_bundle',lambda *a,**k: (_ for _ in ()).throw(OSError('injected interruption')))
    with pytest.raises(ArtifactError): publish_from_repository(repo,pid,2,rid,'full-v1',target,full=True)
    monkeypatch.setattr(adapter,'publish_prebuilt_bundle',original)
    outcomes=recover_registered_artifacts(repo)
    assert any(o['state']=='PUBLISHED' for o in outcomes)
    assert (target/'report.pdf').exists()
    assert verify_against_repository(repo,target)['currentness']=='CURRENT'


@pytest.mark.parametrize('field,value',[('load_va',9999),('breaker_id','other-device'),('conductor_id','other-cable'),('phases_count',3)])
def test_full_reconciliation_blocks_model_projection_divergence(tmp_path,field,value):
    from sie_api.persisted_source_f10 import resolve_persisted_source
    from sie_api.representation_f10 import artifact_bundle
    repo,pid,rid=prepare_full(tmp_path)
    snapshot,contract=resolve_persisted_source(repo,pid,2,rid,'full-v1',full=True)
    snapshot['circuits'][0][field]=value
    with pytest.raises(ArtifactError): artifact_bundle(snapshot,contract)


def test_full_cli_and_no_invented_phase_assignment(tmp_path):
    from sie_api.persisted_source_f10 import main
    repo,pid,rid=prepare_full(tmp_path)
    target=tmp_path/'cli-full'/'bundle'
    assert main(['generate','--full','--db',str(repo.caminho),'--project-id',pid,'--revision','2','--run-id',rid,'--template-version','full-v1','--output-dir',str(target)])==0
    schedule=json.loads((target/'schedule.json').read_text())
    assert schedule['rows'][0]['phase']=='UNSPECIFIED'
    assert schedule['rows'][0]['phases_count']==1
    assert schedule['rows'][0]['design_current_a']==5
    assert schedule['rows'][0]['voltage_v']==220
    assert schedule['rows'][0]['section_mm2']==4
    validation=json.loads((target/'cross_validation.json').read_text())
    assert validation['status']=='PASS'
    assert validation['diagram_availability']['multifilar']['status']=='UNAVAILABLE'
    assert validation['diagram_availability']['riser']['reason']


def test_full_multicircuit_independent_motor_runs_and_missing_map_rejected(tmp_path):
    from copy import deepcopy
    from uuid import uuid4
    from sie_api.domain.installation import Installation
    from sie_api.installation_service import create_snapshot, analyze_legacy
    from sie_api.analysis_contracts import AnaliseCircuito
    repo,pid,first_run=prepare_full(tmp_path)
    saved=repo.carregar(pid); data=saved['dados']
    inst=json.loads(data['installation_snapshot']['canonical_json'])
    # Explicit second terminal circuit, device, load point, load, cable and segment.
    keys={k:str(uuid4()) for k in ('circuit','device','point','load','cable','segment','run','board','bus')}
    old_circuit=inst['circuits'][0]['id']; old_segment=inst['segments'][0]['id']
    new_board=deepcopy(inst['boards'][0]); new_board.update(id=keys['board'],name='Synthetic second board'); inst['boards'].append(new_board)
    for collection,kind in [('devices','device'),('load_points','point'),('loads','load'),('cable_runs','cable'),('segments','segment'),('circuits','circuit'),('calculation_runs','run')]:
        item=deepcopy(inst[collection][0]); item['id']=keys[kind]; item['name']=f'Synthetic second {kind}'
        if collection=='devices': item['board_id']=keys['board']
        if collection=='loads': item['load_point_id']=keys['point']
        if collection=='cable_runs': item.update(circuit_id=keys['circuit'],segment_ids=[keys['segment']])
        if collection=='segments': item['cable_run_id']=keys['cable']
        if collection=='circuits': item.update(board_id=keys['board'],device_id=keys['device'],load_ids=[keys['load']])
        if collection=='calculation_runs': item['circuit_id']=keys['circuit']
        inst[collection].append(item)
    params=AnaliseCircuito.model_validate(data['calculation_inputs_f10'][first_run])
    model=Installation.model_validate(inst)
    for run in inst['calculation_runs']:
        from uuid import UUID
        record=analyze_legacy(create_snapshot(model),UUID(run['circuit_id']),params,run['rule_version'])
        run.update(input_sha256=record.input_sha256,output_sha256=record.result_sha256,algorithm_version=record.algorithm_version)
    data['installation_snapshot']=create_snapshot(Installation.model_validate(inst)).model_dump(mode='json')
    data['calculation_inputs_f10'][keys['run']]=params.model_dump(mode='json')
    data['calculation_runs_f10'][keys['circuit']]=keys['run']
    metadata=data['topology_metadata']
    metadata['segment_details'][keys['segment']]=deepcopy(metadata['segment_details'][old_segment])
    board=inst['boards'][0]['id']
    metadata['board_details'][keys['board']]=deepcopy(metadata['board_details'][board])
    metadata['board_details'][keys['board']]['buses'][0].update(id=keys['bus'],circuit_ids=[keys['circuit']])
    data['floor_plan_f10']['revision_id']='3'
    data['floor_plan_f10'].pop('source_sha256',None)
    repo.salvar(pid,saved['nome'],data,2)
    repo.executar_calculo_f10(pid,3,first_run); repo.executar_calculo_f10(pid,3,keys['run'])
    target=tmp_path/'multi'/'bundle'
    manifest=publish_from_repository(repo,pid,3,first_run,'full-v1',target,full=True)
    schedule=json.loads((target/'schedule.json').read_text())
    assert len(schedule['rows'])==2
    assert {row['panel_id'] for row in schedule['rows']}=={board,keys['board']}
    svg=(target/'diagram.svg').read_text()
    first_group=svg.split(f'data-panel-id="{board}"',1)[1].split('</g>',1)[0]
    assert old_circuit in first_group and keys['circuit'] not in first_group
    assert len(json.loads((target/'memorial.json').read_text())['calculations'])==2
    assert {r['calculation_run_id'] for r in schedule['rows']}=={first_run,keys['run']}
    assert len(manifest['dependencies']['calculation_dependencies_f10'])==2
    assert verify_against_repository(repo,target)['currentness']=='CURRENT'
    # New authoritative revision with omitted mapping cannot claim complete output.
    data['calculation_runs_f10'].pop(keys['circuit'])
    data['floor_plan_f10']['revision_id']='4'
    repo.salvar(pid,saved['nome'],data,3)
    with pytest.raises(ArtifactError,match='per-circuit'):
        publish_from_repository(repo,pid,4,first_run,'full-v1',tmp_path/'bad'/'bundle',full=True)


def test_full_rejects_phase_assignment_contradicting_model(tmp_path):
    repo,pid,rid=prepare_full(tmp_path)
    saved=repo.carregar(pid); data=saved['dados']
    circuit=next(iter(data['calculation_runs_f10']))
    data['phase_assignments_f10']={circuit:'L1-L2-L3'}
    data['floor_plan_f10']['revision_id']='3'
    repo.salvar(pid,saved['nome'],data,2); repo.executar_calculo_f10(pid,3,rid)
    with pytest.raises(ArtifactError,match='phase assignment contradicts'):
        publish_from_repository(repo,pid,3,rid,'full-v1',tmp_path/'bad-phase'/'bundle',full=True)


def test_full_low_level_blocks_contradictory_phase_even_with_matching_projection(tmp_path):
    from sie_api.persisted_source_f10 import resolve_persisted_source
    from sie_api.representation_f10 import artifact_bundle
    repo,pid,rid=prepare_full(tmp_path)
    snapshot,contract=resolve_persisted_source(repo,pid,2,rid,'full-v1',full=True)
    cid=snapshot['circuits'][0]['id']
    snapshot['phase_assignments_f10']={cid:'L1-L2-L3'}
    snapshot['circuits'][0]['phase']='L1-L2-L3'
    with pytest.raises(ArtifactError,match='phase assignment contradicts'):
        artifact_bundle(snapshot,contract)
