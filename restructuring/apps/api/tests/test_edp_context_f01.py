"""Contextual EDP candidate tests; no engineering or distributor approval."""
from copy import deepcopy
from decimal import Decimal
import json
import pytest
from fastapi.testclient import TestClient
from sie_api.main import app
from sie_api.edp_context import enquadrar_com_contexto


def context(system='ESTRELA',**changes):
    return {'uf':'SP','distribuidora':'EDP_SP','area_concessao_confirmada':True,
            'rede':'AEREA_SECUNDARIA','sistema':system,'tensao_fase_neutro_v':127 if system=='ESTRELA' else 120,
            'tensao_linha_v':220 if system=='ESTRELA' else 240,'frequencia_hz':60,
            'data_referencia':'2026-10-20','isolacao_entrada':'PVC','possui_mmgd':False,
            'maior_motor_fn_cv':0,'maior_motor_ff_cv':0,'maior_motor_fff_cv':0,
            'possui_cargas_especiais':False,**changes}


def check(mod='T',kw='30',three=False,ctx=None,current='50'):
    return enquadrar_com_contexto(mod,Decimal(current),Decimal(kw),three,ctx or context())


def test_star_triphase_supply_without_triphase_load_is_not_universally_vetoed():
    r=check();assert r['candidato_para_estudo'] is True
    assert r['categoria']['codigo']=='T2'
    assert r['liberado_para_padrao_entrada'] is False
    assert r['contexto_aplicado']['demanda_por_grupos_verificada'] is False
    assert not any(x['codigo']=='EDP-002' for x in r['alertas'])
    assert check(ctx=context('DELTA'))['candidato_para_estudo'] is False


@pytest.mark.parametrize('mod,system,kw,three,applicable',[
    ('U','ESTRELA','12',False,True),('U','DELTA','12.000001',False,False),
    ('D','ESTRELA','12',False,False),('D','ESTRELA','12.000001',False,True),
    ('D','ESTRELA','25',False,True),('D','ESTRELA','25.000001',False,False),
    ('D','DELTA','75',False,True),('D','DELTA','75.000001',False,False),
    ('T','ESTRELA','25',False,False),('T','ESTRELA','25.000001',False,True),
    ('T','DELTA','12',True,False),('T','DELTA','12.000001',True,True),
    ('T','DELTA','75',True,True),('T','DELTA','75.000001',True,False),
])
def test_normal_modality_boundaries(mod,system,kw,three,applicable):
    r=check(mod,kw,three,context(system))
    assert r['candidato_para_estudo'] is applicable
    assert r['liberado_para_padrao_entrada'] is False


def test_mmgd_uses_larger_current_and_requires_explicit_generation():
    r=check(ctx=context(possui_mmgd=True,corrente_geracao_a=120))
    assert r['categoria']['codigo']=='T6'
    assert Decimal(r['contexto_aplicado']['corrente_selecao_a'])==120
    r=check(ctx=context(possui_mmgd=True,corrente_geracao_a=40))
    assert r['categoria']['codigo']=='T2'
    payload={'modalidade':'T','corrente_demanda_a':50,'carga_instalada_kw':30,
             'tem_carga_trifasica':False,'contexto':context(possui_mmgd=True)}
    assert TestClient(app).post('/api/v1/edp/enquadrar',json=payload).status_code==422


@pytest.mark.parametrize('change',[
    {'uf':'RJ'},{'distribuidora':'OUTRA'},{'area_concessao_confirmada':False},
    {'rede':'OUTRA'},{'data_referencia':'2026-04-13'},
    {'tensao_linha_v':240},{'tensao_fase_neutro_v':120},{'frequencia_hz':50},
    {'possui_cargas_especiais':True},{'maior_motor_fn_cv':1.000001},
])
def test_context_failures_block_candidate(change):
    r=check(ctx=context(**change))
    assert r['categoria'] is None and r['candidato_para_estudo'] is False
    assert r['status_engenharia']=='BLOQUEADO'


@pytest.mark.parametrize('current,expected',[('150','T6'),('150.000001','T7'),('200.000001','T9')])
def test_apparent_source_conflict_blocks_epr_t7_t9_without_inventing_precedence(current,expected):
    r=check(ctx=context(isolacao_entrada='EPR_XLPE'),current=current)
    if expected=='T6':assert r['categoria']['codigo']==expected
    else:
        assert r['categoria'] is None
        assert any(x['codigo']=='EDP-CONFLITO-FONTE' for x in r['alertas'])


def test_api_and_cli_context_agree_and_preserve_legacy_route(tmp_path,capsys):
    payload={'modalidade':'T','corrente_demanda_a':50,'carga_instalada_kw':30,
             'tem_carga_trifasica':False,'contexto':context()}
    api=TestClient(app).post('/api/v1/edp/enquadrar',json=payload)
    assert api.status_code==200 and api.json()['candidato_para_estudo'] is True
    from sie_api.cli import main
    path=tmp_path/'edp.json';path.write_text(json.dumps(payload))
    assert main(['enquadrar-edp','--arquivo',str(path)])==0
    assert json.loads(capsys.readouterr().out)==api.json()
    payload.pop('contexto')
    legacy=TestClient(app).post('/api/v1/edp/enquadrar',json=payload).json()
    assert legacy['candidato_para_estudo'] is False
    assert legacy['liberado_para_padrao_entrada'] is False


def test_edp_nonfinite_json_is_rejected_by_cli_and_http(tmp_path, capsys):
    from sie_api.cli import main
    raw = '{"modalidade":"D","corrente_demanda_a":1e999,"carga_instalada_kw":20}'
    path = tmp_path / 'nonfinite.json'
    path.write_text(raw)
    assert main(['enquadrar-edp', '--arquivo', str(path)]) == 2
    assert 'Dados invalidos' in capsys.readouterr().err
    assert TestClient(app).post('/api/v1/edp/enquadrar', content=raw,
                               headers={'Content-Type': 'application/json'}).status_code == 422
