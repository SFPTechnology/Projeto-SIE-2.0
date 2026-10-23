"""F09 read-through integration with the immutable local F06-F08 histories."""
from copy import deepcopy
from decimal import Decimal
from uuid import UUID

from . import conductor_f07, demand, protection_storage_f08
from .distributor_engine_f09 import (
    DistributorAssessment, catalogo_distribuidoras, diagnosticar_distribuidora,
)
from .edp_context import ContextoEDP
from .installation_service import digest
from .topology import load_document, report as topology_report


class F09EvidencePending(ValueError):
    pass


def _current_studies(data):
    demand_rows = demand.scenario_history(data)
    conductor_rows = conductor_f07.history(data)
    protection_rows = protection_storage_f08.history(data)
    current_demand = [row for row in demand_rows if not row['stale']]
    if not current_demand:
        raise F09EvidencePending('F06: salve um cenário atual de demanda antes do enquadramento.')
    if not conductor_rows or conductor_rows[-1]['stale']:
        raise F09EvidencePending('F07: o último estudo de condutores está ausente ou desatualizado.')
    if not protection_rows or protection_rows[-1]['stale']:
        raise F09EvidencePending('F08: o último estudo de proteções está ausente ou desatualizado.')

    # A history row is evidence only if its result still matches a fresh server
    # calculation from the exact immutable input stored with it.
    verified_demand = []
    for row in current_demand:
        scenario = demand.Scenario.model_validate(row['scenario'])
        if digest(demand.calculate(scenario)) == digest(row['result']):
            verified_demand.append(row)
    if not verified_demand:
        raise F09EvidencePending('F06: resultado persistido não confere com o recálculo do cenário atual.')

    c_row = conductor_rows[-1]
    c_study = conductor_f07.Study.model_validate(c_row['study'])
    if digest(conductor_f07.analyze(c_study)) != digest(c_row['result']):
        raise F09EvidencePending('F07: resultado persistido não confere com o recálculo do estudo atual.')
    p_row = protection_rows[-1]
    return verified_demand, c_row, p_row


def enquadrar_persistido(repo, project_id: UUID, request, expected_revision: int):
    project = repo.carregar(str(project_id))
    if project is None:
        raise KeyError('Projeto não encontrado.')
    if project['revisao'] != expected_revision:
        raise RuntimeError('Revisão concorrente; reabra o projeto antes do enquadramento.')
    data = project['dados']
    d_rows, c_row, p_row = _current_studies(data)
    supply_id = str(request.supply_id)
    matches = []
    for row in d_rows:
        scenario = demand.Scenario.model_validate(row['scenario'])
        if scenario.purpose != 'ENTRANCE' or supply_id not in {str(key) for key in scenario.contexts}:
            continue
        matches.append((row, scenario))
    if not matches:
        raise F09EvidencePending('F06: não há cenário atual de entrada para a fonte selecionada.')
    d_row, scenario = matches[-1]
    f06_context = scenario.contexts[UUID(supply_id)]
    context = ContextoEDP.model_validate(request.context)
    if (not f06_context.concession_confirmed or f06_context.utility != context.distribuidora or
            f06_context.edition != '09' or context.distribuidora != request.distributor_id):
        raise F09EvidencePending('F06: concessionária/edição não confirmada ou incompatível com o contexto F09.')

    demand_result = d_row['result']
    supply = demand_result.get('by_supply', {}).get(supply_id)
    if not supply:
        raise F09EvidencePending('F06: resultado não contém a fonte selecionada.')
    current_a = supply.get('design_current', {}).get('value_a')
    installed = supply.get('installed', {})
    installed_w = installed.get('p_w', {}).get('value')
    if current_a is None or installed_w is None or installed.get('p_w', {}).get('missing', 1) != 0:
        raise F09EvidencePending('F06: corrente de demanda ou potência ativa instalada está ausente/incompleta.')

    topology = load_document(data)
    paths = topology_report(topology)['paths']
    by_load = {str(load.id): load for load in topology.installation.loads}
    supply_loads = [by_load[path['load_id']] for path in paths if path['source_id'] == supply_id]
    if not supply_loads:
        raise F09EvidencePending('Topologia atual não contém cargas ligadas à fonte selecionada.')
    three_phase = any(load.connection == 'THREE_PHASE' for load in supply_loads)

    assessment = DistributorAssessment(
        distributor_id=request.distributor_id,
        modality=request.modality,
        demand_current_a=Decimal(current_a),
        installed_load_kw=Decimal(installed_w) / Decimal(1000),
        has_three_phase_load=three_phase,
        context=context,
    )
    result = diagnosticar_distribuidora(assessment)
    source_refs = {
        'project_id': str(project_id),
        'project_revision': project['revisao'],
        'supply_id': supply_id,
        'F09_catalog_sha256': digest(catalogo_distribuidoras()),
        'F06': {'scenario_id': str(scenario.id), 'input_sha256': demand.fingerprint(scenario),
                'topology_sha256': d_row['topology_sha256'], 'result_sha256': digest(d_row['result'])},
        'F07': {'study_id': str(c_row['study']['id']), 'input_sha256': c_row['result']['input_sha256'],
                'topology_sha256': c_row['result']['topology_sha256'], 'result_sha256': digest(c_row['result'])},
        'F08': {'study_id': str(p_row['study']['id']), 'result_sha256': p_row['result_sha256'],
                'conductor_sha256': p_row['conductor_sha256']},
    }
    result['evidence_provenance'] = source_refs
    result['integration_state'] = 'PERSISTED_EVIDENCE_LINKED_CONSULTATIVE'
    result['f07_status'] = c_row['result'].get('status')
    result['f08_status'] = p_row['result'].get('status')
    result['normative_conformity_verified'] = False
    result['utility_approval'] = False

    history = list(data.get('distributor_assessments_f09', []))
    fingerprint = digest({'assessment': assessment.model_dump(mode='json'), 'evidence': source_refs})
    result['persisted_revision'] = expected_revision + 1
    record = {'fingerprint': fingerprint, 'assessment': assessment.model_dump(mode='json'),
              'result': result, 'evidence': source_refs, 'stale': False}
    for old in history:
        old['stale'] = True
    history.append(record)
    updated = dict(data)
    updated['distributor_assessments_f09'] = history
    repo.salvar(str(project_id), project['nome'], updated, expected_revision)
    return result


def history_f09(data):
    rows = deepcopy(data.get('distributor_assessments_f09', []))
    current = rows[-1]['fingerprint'] if rows else None
    for row in rows:
        row['stale'] = row.get('fingerprint') != current
    try:
        d_rows, c_row, p_row = _current_studies(data)
        current_catalog_hash = digest(catalogo_distribuidoras())
        for row in rows:
            if row.get('evidence', {}).get('F09_catalog_sha256') != current_catalog_hash:
                row['stale'] = True
            supply_id = row['evidence']['supply_id']
            candidates = [item for item in d_rows
                          if item['result'].get('purpose') == 'ENTRANCE'
                          and supply_id in item['result'].get('by_supply', {})]
            if not candidates:
                row['stale'] = True
                continue
            latest = candidates[-1]
            expected = {
                'F06': {'input_sha256': latest['result']['input_sha256'],
                        'topology_sha256': latest['topology_sha256'],
                        'result_sha256': digest(latest['result'])},
                'F07': {'input_sha256': c_row['result']['input_sha256'],
                        'topology_sha256': c_row['result']['topology_sha256'],
                        'result_sha256': digest(c_row['result'])},
                'F08': {'result_sha256': p_row['result_sha256'],
                        'conductor_sha256': p_row['conductor_sha256']},
            }
            if any(row['evidence'].get(key, {}).get(field) != value
                   for key, values in expected.items() for field, value in values.items()):
                row['stale'] = True
    except (F09EvidencePending, KeyError, ValueError, TypeError):
        for row in rows:
            row['stale'] = True
    return rows
