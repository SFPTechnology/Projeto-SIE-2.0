"""Real local API + SQLite + motor + full bundle; no parser/motor doubles."""
from fastapi.testclient import TestClient
from sie_api.main import app
from test_full_f10_integration import prepare_full


def client_case(tmp_path, monkeypatch):
    repo, pid, rid = prepare_full(tmp_path)
    monkeypatch.setenv('SIE_LOCAL_API_TOKEN', 'x'*32)
    monkeypatch.setenv('SIE_LOCAL_DB_PATH', repo.caminho)
    monkeypatch.setenv('SIE_F10_ARTIFACT_ROOT', str(tmp_path/'artifacts'))
    client = TestClient(app)
    base = f'/api/v1/local/projetos/{pid}/f10'
    body = {'revision':2,'calculation_run_id':rid,'template_version':'F10_FULL_V1'}
    return client, base, body, {'Authorization':'Bearer '+'x'*32}


def test_full_api_generate_history_inspect_download(tmp_path, monkeypatch):
    client, base, body, auth = client_case(tmp_path,monkeypatch)
    assert client.get(base+'/artifacts').status_code == 401
    assert client.post(base+'/execute',json=body,headers=auth).status_code == 200
    response = client.post(base+'/generate',json=body,headers=auth)
    assert response.status_code == 200, response.text
    aid=response.json()['artifact_id']
    history=client.get(base+'/artifacts',headers=auth)
    assert history.status_code==200 and aid in {row['artifact_id'] for row in history.json()['artifacts']}
    details=client.get(base+'/artifacts/'+aid,headers=auth)
    assert details.status_code==200,details.text
    assert details.json()['verification']['integrity']=='VERIFIED'
    names=details.json()['manifest']['files_sha256']
    assert any(name.endswith('.pdf') for name in names)
    name=next(iter(names))
    download=client.get(base+'/artifacts/'+aid+'/files/'+name,headers=auth)
    assert download.status_code==200
    assert download.headers['x-content-type-options']=='nosniff'
    assert 'attachment' in download.headers['content-disposition']
    wrong=base.replace(base.split('/')[5], 'ffffffff-ffff-ffff-ffff-ffffffffffff')
    assert client.get(wrong+'/artifacts/'+aid,headers=auth).status_code==404
    assert client.get(base+'/artifacts/'+aid+'/files/not-registered.html',headers=auth).status_code==404


def test_geometry_cas_requires_reexecute_and_real_generation(tmp_path, monkeypatch):
    client,base,body,auth=client_case(tmp_path,monkeypatch)
    opened=client.get(base+'/geometry',headers=auth).json()
    plan=opened['floor_plan']; plan['geometry_revision']+=1
    saved=client.put(base+'/geometry',json={**body,'floor_plan':plan},headers=auth)
    assert saved.status_code==200,saved.text
    assert saved.json()['revision']==3 and saved.json()['motor_execution_required']
    assert client.put(base+'/geometry',json={**body,'floor_plan':plan},headers=auth).status_code==409
    nextbody={**body,'revision':3}
    assert client.post(base+'/generate',json=nextbody,headers=auth).status_code==422
    assert client.post(base+'/execute',json=nextbody,headers=auth).status_code==200
    generated=client.post(base+'/generate',json=nextbody,headers=auth)
    assert generated.status_code==200,generated.text


def test_import_rejects_active_svg_and_client_paths(tmp_path, monkeypatch):
    import base64
    client,base,body,auth=client_case(tmp_path,monkeypatch)
    data={'source_ref':'test','authorization_reference':'test-owner','content_base64':base64.b64encode(b'<svg viewBox="0 0 10 10"><script>evil()</script></svg>').decode()}
    assert client.post(base+'/import',json=data,headers=auth).status_code==422
    assert client.post(base+'/generate',json={**body,'destination':'/tmp/unsafe'},headers=auth).status_code==422
