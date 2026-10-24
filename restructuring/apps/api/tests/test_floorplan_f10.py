import base64
from copy import deepcopy
import json
import pytest
from sie_api.floorplan_f10 import import_svg_asset, import_floor_plan, render_floor_plan_svg, PlanHistory, main
from sie_api.representation_f10 import ArtifactContract, ArtifactError
from sie_api.symbols_f10 import symbol_catalog, render_legend, render_symbol
SVG = b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 80"><rect x="0" y="0" width="100" height="80" fill="white" stroke="black"/></svg>'
def fixture():
    contract = ArtifactContract('p','1','run','rule','template')
    snapshot = {'project_id':'p','revision_id':'1','calculation_run_id':'run','rule_version':'rule','elements':[{'id':'Q1','kind':'panel'}], 'circuits':[], 'segments':[{'id':'s1','length_m':5}]}
    snapshot['floor_plan'] = {'schema_version':'SIE_FLOOR_PLAN_V1','id':'floor1','revision_id':'1','geometry_revision':1,'source_ref':'drawing-1','authorization_reference':'owner-approval-1','units':'m','width':100,'height':80,'model_units_per_canvas_unit':.1,'asset':import_svg_asset(SVG,'drawing-1','owner-approval-1'),'calibration':{'canvas_distance':50,'model_distance':5,'relative_tolerance':.001,'confirmed_by':'owner','confirmed_at':'2026-10-24T12:00:00Z'},'walls':[{'id':'wall1','points':[[0,0],[100,0]]}],'paths':[{'id':'path1','segment_id':'s1','points':[[0,10],[50,10]]}],'placements':[{'element_id':'Q1','x':10,'y':20,'symbol_id':'panel','label':'Quadro <Q1>'}]}
    return snapshot, contract

def test_original_import_calibration_render_round_trip():
    snapshot, contract = fixture(); plan=import_floor_plan(snapshot['floor_plan'],snapshot,contract)
    assert base64.b64decode(plan['asset']['original_base64']) == SVG
    assert import_floor_plan(plan,snapshot,contract) == plan
    svg = render_floor_plan_svg(snapshot,contract)
    assert 'data-layer="base"' in svg and 'SIE_F10_SYMBOLS_V1' in svg
    assert 'Quadro &lt;Q1&gt;' in svg and '<Q1>' not in svg

@pytest.mark.parametrize('svg', [b'<svg viewBox="0 0 10 10"><script>alert(1)</script></svg>',b'<svg viewBox="0 0 10 10" onload="alert(1)"/>',b'<svg viewBox="0 0 10 10"><image href="https://evil"/></svg>',b'<svg viewBox="0 0 10 10"><path fill="url(#evil)"/></svg>',b'<!DOCTYPE svg [<!ENTITY x "evil">]><svg viewBox="0 0 10 10"/>',b'<html/>',b'<svg viewBox="0 0 nan 10"/>',b'<svg viewBox="0 0 10 10"><style>x</style></svg>'])
def test_rejects_unsafe_assets(svg):
    with pytest.raises(ArtifactError): import_svg_asset(svg,'src','approval')

@pytest.mark.parametrize('mutation', [lambda p:p.update(revision_id='2'),lambda p:p.update(authorization_reference=''),lambda p:p.update(model_units_per_canvas_unit=.2),lambda p:p.update(units='px'),lambda p:p['calibration'].update(confirmed_by=''),lambda p:p['calibration'].update(confirmed_at='2026-10-24'),lambda p:p['calibration'].update(relative_tolerance=.5),lambda p:p['placements'][0].update(x=101),lambda p:p['placements'][0].update(element_id='missing'),lambda p:p['placements'][0].update(symbol_id='unknown'),lambda p:p['paths'][0].update(points=[[0,10],[60,10]]),lambda p:p['paths'][0].update(segment_id='missing'),lambda p:p['asset'].update(sha256='0'*64),lambda p:p.update(source_sha256='0'*64)])
def test_rejects_incompatible_geometry(mutation):
    snapshot,contract=fixture(); mutation(snapshot['floor_plan'])
    with pytest.raises(ArtifactError): import_floor_plan(snapshot['floor_plan'],snapshot,contract)

def test_units_no_invented_length_and_history():
    snapshot,contract=fixture(); original=deepcopy(snapshot['floor_plan']); history=PlanHistory(original)
    changed=deepcopy(original); changed['placements'][0]['x']=15
    assert history.apply(changed)['geometry_revision']==2
    assert history.undo()==original
    assert history.redo()['placements'][0]['x']==15
    assert original==snapshot['floor_plan']
    plan=snapshot['floor_plan']; plan.update(units='cm',model_units_per_canvas_unit=10); plan['calibration']['model_distance']=500
    assert import_floor_plan(plan,snapshot,contract)['units']=='cm'
    assert snapshot['segments'][0]['length_m']==5

def test_catalog_legend_and_escape():
    assert symbol_catalog()['version']=='SIE_F10_SYMBOLS_V1'
    assert symbol_catalog()['license']['status']=='INTERNAL_ORIGINAL_NO_EXTERNAL_LICENSE_CLAIM'
    assert len(render_legend(['panel','panel'])['items'])==1
    assert '&lt;script&gt;' in render_symbol('panel',0,0,'<script>')
    with pytest.raises(ArtifactError): render_symbol('unknown',0,0)

def test_cli_real_import_no_overwrite(tmp_path):
    snapshot,contract=fixture(); snapshot['floor_plan'].pop('asset')
    source=tmp_path/'input.json'; source.write_text(json.dumps({'snapshot':snapshot,'artifact_contract':contract.__dict__}))
    svg=tmp_path/'plan.svg'; svg.write_bytes(SVG); output=tmp_path/'normalized.json'
    args=['--input',str(source),'--svg',str(svg),'--output',str(output)]
    assert main(args)==0
    assert json.loads(output.read_text())['asset']['mime']=='image/svg+xml'
    with pytest.raises(FileExistsError): main(args)

@pytest.mark.parametrize('paint', [r'u\72l(//example.invalid/paint.svg#x)', '//example.invalid/paint.svg', 'url(#paint)', 'var(--paint)', 'rgb(0,0,0)', 'red;fill:url(//evil)'])
def test_svg_paint_grammar_rejects_css_and_references(paint):
    asset = ('<svg viewBox="0 0 10 10"><rect width="10" height="10" fill="'+paint+'"/></svg>').encode()
    with pytest.raises(ArtifactError):
        import_svg_asset(asset, 'source', 'authorization')
