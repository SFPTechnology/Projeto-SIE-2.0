"""No lost received acceptances and no invented global coverage or current QA."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]


def _load(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_limited_lot_counts_do_not_claim_complete_phase_denominator():
    result = _load('f01_inventory_audit').limited_lot_metrics(ROOT)
    assert result['errors'] == []
    assert (result['accepted_cells'], result['lot_cells_total']) == (8, 8)
    assert (result['accepted_cases'], result['lot_cases_total']) == (6, 6)
    assert result['complete_f01_cells_total'] is None
    assert result['complete_f01_cases_total'] is None
    assert result['complete_f01_denominator_known'] is False
    assert len(result['pending_items']) == 8


def test_limited_receipt_cannot_authorize_release_or_change_source(tmp_path):
    module = _load('f01_inventory_audit')
    paths = ['docs/implantacao-sie-2-0/F01/ACEITE_PROFISSIONAL_LOTE01_RECEBIDO_2026-10-20.json',
             'restructuring/apps/api/sie_api/data/f01_lote01_cells_v1.json']
    for path in paths:
        target = tmp_path / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes((ROOT / path).read_bytes())
    receipt = json.loads((tmp_path / paths[0]).read_text())
    for mutation in ('release', 'source'):
        bad = deepcopy(receipt)
        if mutation == 'release': bad['release_flags_declared_in_submission']['f01_release_allowed'] = True
        else: bad['source_sha256_declared_by_reviewer'] = '0' * 64
        (tmp_path / paths[0]).write_text(json.dumps(bad))
        result = module.limited_lot_metrics(tmp_path)
        assert result['errors'] and result['accepted_cells'] == 0


def test_historical_qa_counts_are_separate_from_current_gates_and_manifest():
    module = _load('f01_gate_dashboard')
    folder = ROOT / 'docs/implantacao-sie-2-0/F01'
    evidence = json.loads((folder / 'QA3_EXECUTION_EVIDENCE_39289599183.json').read_text())
    history = module.historical_execution_metrics(evidence)
    assert history['document_structure_consistent'] is True
    assert history['documented_first_passes'] == history['documented_cross_reviews'] == 3
    assert history['source_sha'] == '29c506cbd4f0045c4d54e4f50098d989d7260194'
    assert history['current_gate_acceptance_granted'] is False
    assert history['artifacts_retrieved_and_reverified_this_invocation'] is False
    manifest = json.loads((folder / 'QA3_MANIFEST.json').read_text())
    state = json.loads((ROOT / 'docs/sie-orchestrator/ORCHESTRATOR_STATE.json').read_text())
    current = module.inspect(manifest, state)
    assert current['accepted_gates'] == 0
    assert current['verified_qa_first_passes'] == current['verified_cross_reviews'] == 0
    for mutation in ('hash', 'duplicate', 'release'):
        bad = deepcopy(evidence)
        if mutation == 'hash': bad['files_sha256'][next(iter(bad['files_sha256']))] = 'invalid'
        elif mutation == 'duplicate': bad['agents'][0] = deepcopy(bad['agents'][1])
        else: bad['f01_released'] = True
        assert module.historical_execution_metrics(bad)['document_structure_consistent'] is False
