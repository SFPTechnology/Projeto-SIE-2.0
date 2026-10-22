"""F08 immutable local study history, bound to the current F07 input and topology."""
from . import conductor_f07 as conductors
from .installation_service import digest
from .topology import load_document, topology_hash


def _dependency(data, study):
    """Return the stored, current F07 dependency, never a client approval flag."""
    items = conductors.history(data)
    if not items or items[-1]['stale']:
        raise ValueError('Salve um estudo de condutores F07 atual antes das proteções')
    latest = items[-1]
    if latest['result']['input_sha256'] != conductors.fingerprint(study.conductor_study):
        raise ValueError('Proteções devem usar exatamente o último estudo F07 salvo')
    return latest['result']['input_sha256']


def save(repo, project_id, study, expected):
    from .protection_f08 import analyze
    from .protection_contracts_f08 import Study
    study = Study.model_validate(study)
    topology = study.conductor_study.topology
    if topology.installation.project.id != project_id:
        raise ValueError('Estudo de proteções pertence a outro projeto')
    previous = repo.carregar(str(project_id))
    if previous is None:
        raise ValueError('Cadastre topologia e condutores antes das proteções')
    data = dict(previous['dados'])
    if topology_hash(load_document(data)) != topology_hash(topology):
        raise ValueError('Topologia divergente; reabra o projeto')
    dependency = _dependency(data, study)
    items = list(data.get('protection_studies', []))
    if any(x['study']['id'] == str(study.id) for x in items):
        raise ValueError('Histórico imutável; novo UUID obrigatório')
    result = analyze(study)
    items.append({'study': study.model_dump(mode='json'), 'result': result,
                  'conductor_sha256': dependency,
                  'survey_sha256': digest(data.get('levantamento')),
                  'result_sha256': digest(result)})
    data['protection_studies'] = items
    data['protection_results_stale'] = False
    data['documents_stale'] = True
    # A new protection proposal invalidates previously issued calculation records.
    from .installation_service import create_snapshot
    from .domain.installation import Installation
    raw = load_document(data).installation.model_dump(mode='json')
    for run in raw['calculation_runs']:
        if run['state'] in ('VALID', 'PENDING'):
            run['state'] = 'STALE'
    data['installation_snapshot'] = create_snapshot(Installation.model_validate(raw)).model_dump(mode='json')
    revision = repo.salvar(str(project_id), previous['nome'], data, expected)
    return {'revision': revision, 'result': result}


def history(data):
    from .protection_f08 import analyze
    from .protection_contracts_f08 import Study
    current = topology_hash(load_document(data))
    items = data.get('protection_studies', [])
    rows = []
    for index, item in enumerate(items):
        try:
            study = Study.model_validate(item['study'])
            dependency = _dependency(data, study)
            stale = (index != len(items)-1 or
                     current != topology_hash(study.conductor_study.topology) or
                     item['survey_sha256'] != digest(data.get('levantamento')) or
                     item['conductor_sha256'] != dependency or
                     item.get('result_sha256') != digest(item['result']) or
                     digest(analyze(study)) != item['result_sha256'] or
                     data.get('protection_results_stale', True))
        except (ValueError, KeyError, TypeError):
            stale = True
        rows.append({**item, 'stale': bool(stale),
                     'dependent_documents_stale': bool(stale or data.get('documents_stale', True))})
    return rows
