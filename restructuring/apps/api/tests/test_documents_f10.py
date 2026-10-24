from copy import deepcopy
from io import BytesIO
import json
import pytest
from pypdf import PdfReader
from sie_api.documents_f10 import engineering_documents, technical_memorial, equipment_ledger
from sie_api.representation_f10 import ArtifactContract, ArtifactError

@pytest.fixture
def verified_source():
    from test_installation_integration_f02 import legacy_case
    from sie_api.installation_service import create_snapshot, analyze_legacy
    installation, parameters = legacy_case()
    saved = create_snapshot(installation)
    circuit = installation.circuits[1]
    record = analyze_legacy(saved, circuit.id, parameters, 'test-rule').model_dump(mode='json')
    pid, cid = str(installation.project.id), str(circuit.id)
    source = {'project_id':pid,'revision_id':'1','calculation_run_id':'run-real','rule_version':'test-rule',
      'elements':[{'id':'panel','kind':'panel'}], 'circuits':[{'id':cid,'panel_id':'panel','load_va':1200,'phase':'L1','breaker_id':'breaker','conductor_id':'cable'}],
      'segments':[{'id':'segment','circuit_id':cid,'length_m':10,'status':'MEASURED','origin':'levantamento explícito'}],
      'verified_calculation_f10':{'record':record,'parameters':parameters.model_dump(mode='json'),'execution_sha256':'a'*64},
      'source_evidence_f10':{'calculation_output_sha256':record['result_sha256'],'algorithm_version':record['algorithm_version'],
      'installation_snapshot_sha256':saved.snapshot_sha256,'installation_revision':saved.revision,'motor_execution_sha256':'a'*64}}
    return source, ArtifactContract(pid,'1','run-real','test-rule','template-real')

def test_real_engine_memorial_formula_and_intermediates(verified_source):
    snapshot, contract = verified_source
    memorial = technical_memorial(snapshot, contract)
    original = json.loads(snapshot['verified_calculation_f10']['record']['result_json'])
    assert memorial['result'] == original
    assert memorial['formulas'][0]['value'] == original['queda_tensao']['formula']
    assert any(r['source_path'].endswith('condutor.capacidade_decisao_a') for r in memorial['result_facts'])
    assert memorial['normative_conformity_verified'] is False

def test_real_pdf_roundtrip_toc_and_determinism(verified_source):
    snapshot, contract = verified_source
    bundle = engineering_documents(snapshot, contract)
    assert bundle['report.pdf'].startswith(b'%PDF-')
    assert bundle['report.pdf'] == engineering_documents(snapshot, contract)['report.pdf']
    reader = PdfReader(BytesIO(bundle['report.pdf']))
    text = '\n'.join(page.extract_text() for page in reader.pages)
    assert len(reader.pages) >= 3
    for required in ['Sumário','Entradas persistidas','Resultados, intermediários','Quantitativos','Página',contract.project_id]:
        assert required in text

@pytest.mark.parametrize('field', ['parameters','record','execution_sha256'])
def test_missing_evidence_blocks(verified_source, field):
    snapshot, contract = verified_source
    del snapshot['verified_calculation_f10'][field]
    with pytest.raises(ArtifactError): engineering_documents(snapshot, contract)

def test_tampered_input_and_result_block(verified_source):
    snapshot, contract = verified_source
    for changed in ('input','result'):
        broken = deepcopy(snapshot)
        if changed == 'input': broken['verified_calculation_f10']['parameters']['corrente_a'] += 1
        else:
            record = broken['verified_calculation_f10']['record']
            record['result_json'] = record['result_json'].replace('PENDENTE','APROVADO')
        with pytest.raises(ArtifactError): engineering_documents(broken, contract)

def test_equipment_deduplicates_without_length_multiplier(verified_source):
    snapshot, contract = verified_source
    ledger = equipment_ledger(snapshot, contract)
    assert len(ledger) == 3
    assert all(row['quantity'] == 1 for row in ledger)
    snapshot['elements'].append({'id':'breaker','kind':'panel'})
    with pytest.raises(ArtifactError, match='incompatible'): equipment_ledger(snapshot, contract)

def test_equipment_csv_has_contract_and_neutralizes_formulas(verified_source):
    import csv
    import io
    snapshot, contract = verified_source
    snapshot['elements'].append({'id':'=HYPERLINK("evil")','kind':'load'})
    rows = list(csv.DictReader(io.StringIO(engineering_documents(snapshot,contract)['equipment.csv'])))
    assert all(row['project_id'] == contract.project_id for row in rows)
    assert next(row['item_id'] for row in rows if 'HYPERLINK' in row['item_id']).startswith("'=")

def test_memorial_multicircuit_exact_coverage_and_independent_lineage(verified_source):
    from uuid import uuid4
    source, contract = verified_source
    first = deepcopy(source['verified_calculation_f10'])
    cid1=source['circuits'][0]['id']; cid2=str(uuid4())
    second=deepcopy(first); second['record']['circuit_id']=cid2
    source['circuits'].append(dict(source['circuits'][0],id=cid2,breaker_id='breaker2',conductor_id='cable2'))
    items=[dict(first,circuit_id=cid1,run_id='run-real'),dict(second,circuit_id=cid2,run_id='run-second')]
    dependencies=[]
    for item in items:
        record=item['record']
        dependencies.append({'circuit_id':item['circuit_id'],'run_id':item['run_id'],'rule_version':record['rule_version'],
            'algorithm_version':record['algorithm_version'],'input_sha256':record['input_sha256'],
            'output_sha256':record['result_sha256'],'snapshot_sha256':record['snapshot_sha256'],'execution_sha256':item['execution_sha256']})
    source.update(verified_calculations_f10=items,calculation_dependencies_f10=dependencies,calculation_scope_f10='PER_CIRCUIT_RUN_MAP_V1')
    memorial=technical_memorial(source,contract)
    assert len(memorial['calculations'])==2
    assert {item['calculation_run_id'] for item in memorial['calculations']} == {'run-real','run-second'}
    from sie_api.pdf_f10 import render_engineering_pdf
    from sie_api.representation_f10 import load_schedule,quantity_ledger
    pdf=render_engineering_pdf(memorial,load_schedule(source,contract),quantity_ledger(source,contract),equipment_ledger(source,contract))
    text='\n'.join(page.extract_text() for page in PdfReader(BytesIO(pdf)).pages)
    assert 'run-second' in text and cid1 in text and cid2 in text
    broken=deepcopy(source);broken['verified_calculations_f10'].pop()
    with pytest.raises(ArtifactError,match='per-circuit'): technical_memorial(broken,contract)
    broken=deepcopy(source);broken['calculation_dependencies_f10'][1]['run_id']='run-real'
    with pytest.raises(ArtifactError,match='per-circuit'): technical_memorial(broken,contract)
