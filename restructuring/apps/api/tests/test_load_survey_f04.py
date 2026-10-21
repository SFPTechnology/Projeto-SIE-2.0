from copy import deepcopy
import json
from pathlib import Path
from uuid import UUID
import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError
from sie_api.main import app
from sie_api.load_survey import Survey, summarize, persist
from sie_api.storage import RepositorioProjetos, ConflitoRevisao

@pytest.fixture
def raw():
    return json.loads((Path(__file__).parents[2]/'web'/'levantamento-demo.json').read_text())

def test_independent_totals_and_unknowns(raw):
    s=summarize(Survey.model_validate(raw))
    assert s['total']['p_w']['valor']=='3100'
    assert s['total']['q_var']['valor']=='0'
    assert s['total']['s_va']['valor']=='300'
    assert s['total']['p_w']['cargas_sem_dado']==1
    assert s['total']['s_va']['cargas_sem_dado']==1
    assert s['conformidade_normativa'] is False
    assert s['fator_demanda_aplicado'] is False
    assert s['regras_minimas']=='PENDENTE_FONTE_VALIDADA'
    assert s['por_ambiente'][raw['ambientes'][0]['id']]['p_w']['valor']=='100'
    assert s['por_pavimento'][raw['pavimentos'][0]['id']]['p_w']['valor']=='3100'

@pytest.mark.parametrize('field,value',[('p_w','-1'),('q_var','NaN'),('s_va','Infinity'),('tensao_v','0'),('fases',4),('quantidade',0),('quantidade',1.5),('fator_potencia','1.01')])
def test_invalid_electrical_values(raw,field,value):
    raw['cargas'][0][field]=value
    with pytest.raises(ValidationError): Survey.model_validate(raw)

@pytest.mark.parametrize('field,value',[('area_m2','0'),('area_m2','-1'),('perimetro_m','NaN')])
def test_geometry(raw,field,value):
    raw['ambientes'][0][field]=value
    with pytest.raises(ValidationError): Survey.model_validate(raw)

@pytest.mark.parametrize('problem',['duplicate','missing_parent','archived_parent'])
def test_links(raw,problem):
    if problem=='duplicate': raw['cargas'][1]['id']=raw['cargas'][0]['id']
    elif problem=='missing_parent': raw['cargas'][0]['ambiente_id']=str(UUID(int=999))
    else: raw['ambientes'][0]['arquivado']=True
    with pytest.raises(ValidationError): Survey.model_validate(raw)

def test_archive_all_children_and_totals(raw):
    for group in ['edificacoes','pavimentos','ambientes','cargas']:
        for item in raw[group]: item['arquivado']=True
    assert summarize(Survey.model_validate(raw))['total']['p_w']['valor']=='0'

def test_duplicate_names_and_inconsistent_power(raw):
    raw['cargas'][1]['nome']=raw['cargas'][0]['nome']
    raw['cargas'][0].update(p_w='100',q_var='100',s_va='100')
    codes={x['codigo'] for x in summarize(Survey.model_validate(raw))['pendencias']}
    assert {'POSSIVEL_DUPLICIDADE','POTENCIAS_INCONSISTENTES','DADOS_INCOMPLETOS'}<=codes

def test_exact_decimal_and_plate_not_counted_twice(raw):
    raw['cargas'][0].update(p_w='0.123456789123456789',potencia_placa_w='999',potencia_atribuida_va='888')
    raw['cargas'][2]['p_w']=None
    assert summarize(Survey.model_validate(raw))['total']['p_w']['valor']=='0.123456789123456789'

def test_persistence_conflict_immutability_and_no_silent_delete(raw,tmp_path):
    repo=RepositorioProjetos(str(tmp_path/'test.db')); s=Survey.model_validate(raw)
    assert persist(repo,s.projeto_id,s,0)['revisao']==1
    before=repo.carregar(str(s.projeto_id))
    with pytest.raises(ConflitoRevisao): persist(repo,s.projeto_id,s,0)
    raw['cargas'][0]['p_w']='200';s2=Survey.model_validate(raw)
    persist(repo,s2.projeto_id,s2,1)
    assert repo.carregar_revisao(str(s.projeto_id),1)['dados']==before['dados']
    raw['cargas'].pop()
    with pytest.raises(ValueError,match='silenciosa'):persist(repo,s.projeto_id,Survey.model_validate(raw),2)
    assert repo.carregar(str(s.projeto_id))['revisao']==2

def test_other_project_and_preserve_legacy(raw,tmp_path):
    repo=RepositorioProjetos(str(tmp_path/'test.db'));s=Survey.model_validate(raw)
    repo.salvar(str(s.projeto_id),s.nome,{'legado':{'x':1}},0)
    persist(repo,s.projeto_id,s,1)
    assert repo.carregar(str(s.projeto_id))['dados']['legado']=={'x':1}
    with pytest.raises(ValueError):persist(repo,UUID(int=999),s,0)

def test_malformed_legacy_does_not_crash(raw,tmp_path):
    repo=RepositorioProjetos(str(tmp_path/'test.db'));s=Survey.model_validate(raw)
    repo.salvar(str(s.projeto_id),s.nome,{'levantamento':{'cargas':[None,7,{}]}},0)
    persist(repo,s.projeto_id,s,1)
    assert repo.carregar(str(s.projeto_id))['revisao']==2

def test_api_roundtrip_access_and_conflict(raw,tmp_path,monkeypatch):
    monkeypatch.setenv('SIE_LOCAL_DB_PATH',str(tmp_path/'api.db'));monkeypatch.setenv('SIE_LOCAL_API_TOKEN','t'*24)
    c=TestClient(app);url='/api/v1/local/projetos/'+raw['projeto_id']+'/levantamento';payload={'levantamento':raw,'revisao_esperada':0}
    assert c.put(url,json=payload).status_code==401
    h={'Authorization':'Bearer '+'t'*24}
    assert c.put(url,json=payload,headers=h).status_code==200
    assert c.put(url,json=payload,headers=h).status_code==409
    loaded=c.get(url.removesuffix('/levantamento'),headers=h).json()
    assert loaded['dados']['levantamento']['cargas'][2]['fases']==3
    monkeypatch.setenv('SIE_ENV','prod')
    assert c.put(url,json=payload,headers=h).status_code==503
    monkeypatch.setenv('SIE_ENV','test')
    with TestClient(app,client=('192.0.2.1',50000)) as remote:
        assert remote.put(url,json=payload,headers=h).status_code==403


def test_power_factor_contradiction(raw):
    raw['cargas'][0]['fator_potencia']='0.5'
    assert 'FATOR_POTENCIA_INCONSISTENTE' in {x['codigo'] for x in summarize(Survey.model_validate(raw))['pendencias']}


def test_untrusted_decimal_exponent_is_bounded(raw):
    raw['cargas'][0]['p_w']='1e-1000000000'
    with pytest.raises(ValidationError, match='24 casas'):
        Survey.model_validate(raw)


def test_zero_extreme_positive_exponent_is_canonicalized(raw):
    raw['cargas'][0]['p_w']='0E+1000000000'
    survey=Survey.model_validate(raw)
    assert str(survey.cargas[0].p_w)=='0'
    assert summarize(survey)['total']['p_w']['valor']=='3000'
