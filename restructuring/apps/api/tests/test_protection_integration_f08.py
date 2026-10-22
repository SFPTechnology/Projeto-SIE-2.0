"""Independent persistence/security/cascade tests for F08 integration."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
from uuid import uuid4
import pytest
from fastapi.testclient import TestClient
from sie_api.main import app
from sie_api import conductor_f07 as f07
from sie_api.protection_contracts_f08 import Study
from sie_api import protection_storage_f08 as storage
from sie_api.storage import RepositorioProjetos, ConflitoRevisao
from sie_api.topology import persist

ROOT = Path(__file__).resolve().parents[3]


@pytest.fixture
def raw():
    return {'id':str(uuid4()), 'conductor_study':json.loads((ROOT/'examples/f07_condutores_demo.json').read_text())}


def setup_repo(tmp_path, raw):
    repo = RepositorioProjetos(str(tmp_path/'f08.sqlite'))
    study = Study.model_validate(raw)
    pid = study.conductor_study.topology.installation.project.id
    persist(repo, pid, study.conductor_study.topology, 0)
    f07.save(repo, pid, study.conductor_study, 1)
    return repo, study, pid


def test_requires_saved_current_conductor(tmp_path, raw):
    repo = RepositorioProjetos(str(tmp_path/'empty.sqlite'))
    study = Study.model_validate(raw); pid = study.conductor_study.topology.installation.project.id
    with pytest.raises(ValueError, match='Cadastre'): storage.save(repo,pid,study,0)
    persist(repo,pid,study.conductor_study.topology,0)
    with pytest.raises(ValueError, match='F07 atual'): storage.save(repo,pid,study,1)


def test_immutable_history_conflict_and_cascade(tmp_path,raw):
    repo,study,pid = setup_repo(tmp_path,raw)
    saved=storage.save(repo,pid,study,2)
    assert saved['revision']==3
    assert storage.history(repo.carregar(str(pid))['dados'])[0]['stale'] is False
    with pytest.raises(ValueError,match='imutável'): storage.save(repo,pid,study,3)
    new = deepcopy(raw);new['id']=str(uuid4())
    with pytest.raises(ConflitoRevisao): storage.save(repo,pid,Study.model_validate(new),2)
    assert len(repo.carregar(str(pid))['dados']['protection_studies'])==1
    new['conductor_study']['id']=str(uuid4())
    next(iter(new['conductor_study']['circuits'].values()))['power_factor']='0.7'
    with pytest.raises(ValueError,match='exatamente'): storage.save(repo,pid,Study.model_validate(new),3)
    f07.save(repo,pid,f07.Study.model_validate(new['conductor_study']),3)
    assert storage.history(repo.carregar(str(pid))['dados'])[0]['stale'] is True
    storage.save(repo,pid,Study.model_validate(new),4)
    rows=storage.history(repo.carregar(str(pid))['dados'])
    assert rows[0]['stale'] and not rows[1]['stale']
    assert rows[1]['dependent_documents_stale']


def test_foreign_project_and_tampered_memory(tmp_path,raw):
    repo,study,pid=setup_repo(tmp_path,raw)
    with pytest.raises(ValueError,match='outro projeto'): storage.save(repo,uuid4(),study,2)
    storage.save(repo,pid,study,2)
    data=repo.carregar(str(pid))['dados'];data['protection_studies'][0]['result']['status']='APROVADO'
    assert storage.history(data)[0]['stale']


def test_api_auth_environment_and_revision(tmp_path,raw,monkeypatch):
    client=TestClient(app)
    repo,study,pid=setup_repo(tmp_path,raw)
    monkeypatch.setenv('SIE_LOCAL_DB_PATH',repo.caminho if hasattr(repo,'caminho') else str(tmp_path/'f08.sqlite'))
    token='f08-test-token-with-more-than-24-characters'
    monkeypatch.setenv('SIE_LOCAL_API_TOKEN',token)
    monkeypatch.setenv('SIE_ENV','test')
    url=f'/api/v1/local/projetos/{pid}/protecoes'
    assert client.get(url).status_code==401
    assert client.put(url,json={'study':raw,'expected_revision':2}).status_code==401
    headers={'Authorization':'Bearer '+token}
    response=client.put(url,json={'study':raw,'expected_revision':2},headers=headers)
    assert response.status_code==200, response.text
    assert client.get(url,headers=headers).json()['studies'][0]['stale'] is False
    assert client.get(f'/api/v1/local/projetos/{uuid4()}/protecoes',headers=headers).status_code==404
    altered=deepcopy(raw);altered['id']=str(uuid4())
    assert client.put(url,json={'study':altered,'expected_revision':2},headers=headers).status_code==409
    monkeypatch.setenv('SIE_ENV','production')
    assert client.get(url,headers=headers).status_code==503
    monkeypatch.setenv('SIE_ENV','test')
    external=TestClient(app,client=('198.51.100.1',1234))
    assert external.get(url,headers=headers).status_code==403


def test_api_analysis_cli_and_invalid_input(raw,tmp_path):
    response=TestClient(app).post('/api/v1/protecoes/analisar',json=raw)
    assert response.status_code==200,response.text
    assert response.json()['normative_conformity_verified'] is False
    raw['unexpected_approval']=True
    assert TestClient(app).post('/api/v1/protecoes/analisar',json=raw).status_code==422
    del raw['unexpected_approval']
    path=tmp_path/'study.json';path.write_text(json.dumps(raw))
    proc=subprocess.run([sys.executable,'-m','sie_api.protection_cli',str(path)],capture_output=True,text=True)
    assert proc.returncode==0,proc.stderr
    assert json.loads(proc.stdout)==response.json()


def test_server_algorithm_change_invalidates_saved_history(tmp_path,raw,monkeypatch):
    from sie_api import protection_f08
    repo,study,pid=setup_repo(tmp_path,raw)
    storage.save(repo,pid,study,2)
    monkeypatch.setattr(protection_f08,'VERSION','SIE-F08-next')
    assert storage.history(repo.carregar(str(pid))['dados'])[0]['stale']


def test_protection_save_invalidates_canonical_calculation(tmp_path,raw):
    from sie_api.topology import load_document
    from sie_api.installation_service import create_snapshot
    from sie_api.domain.installation import Installation
    repo,study,pid=setup_repo(tmp_path,raw)
    previous=repo.carregar(str(pid));data=previous['dados']
    canonical=load_document(data).installation.model_dump(mode='json')
    canonical['calculation_runs'][0].update(state='VALID',output_sha256='a'*64)
    data['installation_snapshot']=create_snapshot(Installation.model_validate(canonical)).model_dump(mode='json')
    repo.salvar(str(pid),previous['nome'],data,2)
    storage.save(repo,pid,study,3)
    saved=repo.carregar(str(pid))['dados']
    assert load_document(saved).installation.calculation_runs[0].state=='STALE'
    assert storage.history(saved)[0]['stale'] is False


def test_catalog_api_cli_and_corruption_fail_closed(monkeypatch):
    from sie_api import protection_registry_f08 as registry
    response=TestClient(app).get('/api/v1/protecoes/catalogo')
    assert response.status_code==200
    assert response.json()['product_certification_verified'] is False
    cli=subprocess.run([sys.executable,'-m','sie_api.protection_cli','--catalog'],capture_output=True,text=True)
    assert cli.returncode==0 and json.loads(cli.stdout)==response.json()
    monkeypatch.setattr(registry,'CATALOG',{})
    assert TestClient(app).get('/api/v1/protecoes/catalogo').status_code==422


def test_corrupt_registry_blocks_analysis_and_cli(raw,tmp_path,monkeypatch,capsys):
    from sie_api import protection_registry_f08 as registry
    from sie_api.protection_cli import main
    monkeypatch.setattr(registry,'CATALOG',{})
    assert TestClient(app).post('/api/v1/protecoes/analisar',json=raw).status_code==422
    path=tmp_path/'study.json';path.write_text(json.dumps(raw))
    monkeypatch.setattr(sys,'argv',['protection_cli',str(path)])
    with pytest.raises(SystemExit) as error: main()
    assert error.value.code==2
    assert 'Não foi possível concluir' in capsys.readouterr().err
