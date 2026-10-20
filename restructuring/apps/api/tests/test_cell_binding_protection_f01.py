"""Accepted limited source binding; synthetic device data do not assert conformity."""
from copy import deepcopy
from decimal import Decimal
from hashlib import sha256
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sie_api.application import analisar_circuito
from sie_api.cell_bindings import REVISION
from sie_api.main import app
from sie_api.protection_checks import verificar_sobrecarga
from sie_api.storage import RepositorioProjetos
from sie_api.calculation_traces import preparar_registro, validar_registro, _canonical


def scenario():
    return {'corrente_a': 20.0, 'comprimento_m': 30.0, 'tensao_v': 220.0,
            'resistencia_ohm_km': 7.41, 'fator_correcao': .87,
            'tabela_condutores': [{'secao_mm2': s, 'capacidade_a': v}
                                  for s, v in [(2.5, 24), (4, 32), (6, 41), (10, 57)]],
            'evidencia': {'documento': 'metadados declarados', 'edicao': 'teste', 'referencia': 'teste'},
            'vinculo_celulas': {'registro_revisao': REVISION,
                'celulas_ids': ['CEL-01','CEL-02','CEL-03','CEL-04','CEL-05'],
                'condicoes': {'material': 'Cu', 'isolacao': 'PVC', 'temperatura_condutor_c': 70,
                    'metodo_referencia': 'B1', 'metodo_instalacao': 3,
                    'descricao_instalacao': 'Caso de ensaio: eletroduto aparente sobre parede',
                    'condutores_carregados': 2, 'meio': 'AR', 'temperatura_ambiente_c': 40,
                    'radiacao_solar': False, 'radiacao_infravermelha': False, 'circuitos_agrupados': 1, 'agrupamento': 'ISOLADO',
                    'grupo_homogeneo': True, 'carga_uniforme': True}}}


def device(i2=29, yearly=100, life=500):
    return {'corrente_nominal_a': 20.0, 'corrente_atuacao_i2_a': float(i2),
            'fonte': {'documento': 'SYNTHETIC TEST DEVICE, not a manufacturer',
                      'revisao': 'test', 'referencia': 'fixture', 'sha256': 'a'*64,
                      'dispositivo_id': 'SYNTHETIC-20'},
            'duracao_sobrecarga_h_12_meses': yearly, 'duracao_sobrecarga_h_vida': life}


def test_server_binding_contains_accepted_ids_conditions_hash_and_never_releases():
    p = scenario(); r = analisar_circuito(p)
    assert r['condutor']['capacidade_decisao_a'] == 20.88
    b = r['vinculo_celulas']; assert [x['id'] for x in b['celulas']] == p['vinculo_celulas']['celulas_ids']
    digest = b.pop('snapshot_sha256'); assert digest == sha256(_canonical(b).encode()).hexdigest()
    assert r['liberado_para_uso_normativo'] is False
    assert r['protecao_sobrecarga']['status'] == 'PENDENTE'


@pytest.mark.parametrize('mutation', ['unknown','duplicate','xlpe','capacity','factor','missing','extra',
                                     'material','method','loaded','solar','infrared','ambient','revision','group'])
def test_http_rejects_forged_values_and_incompatible_conditions(mutation):
    p=scenario(); b=p['vinculo_celulas']; c=b['condicoes']
    if mutation=='unknown': b['celulas_ids'][0]='CEL-99'
    elif mutation=='duplicate': b['celulas_ids'].append('CEL-01')
    elif mutation=='xlpe': b['celulas_ids'][-1]='CEL-06'; c['isolacao']='EPR_XLPE'
    elif mutation=='capacity': p['tabela_condutores'][0]['capacidade_a']=25
    elif mutation=='factor': p['fator_correcao']=.91
    elif mutation=='missing': b['celulas_ids'].pop()
    elif mutation=='extra': b['celulas_ids'].append('CEL-07')
    elif mutation=='material': c['material']='Al'
    elif mutation=='method': c['metodo_instalacao']=99
    elif mutation=='loaded': c['condutores_carregados']=3
    elif mutation=='solar': c['radiacao_solar']=True
    elif mutation=='infrared': c['radiacao_infravermelha']=True
    elif mutation=='ambient': c['temperatura_ambiente_c']=35
    elif mutation=='revision': b['registro_revisao']='not-registered'
    elif mutation=='group': c['circuitos_agrupados']=2
    assert TestClient(app).post('/api/v1/circuitos/analisar',json=p).status_code==422


@pytest.mark.parametrize('circuits,extra,factor', [(2,'CEL-07',.696),(3,'CEL-08',.609)])
def test_grouping_uses_server_derived_product(circuits,extra,factor):
    p=scenario(); b=p['vinculo_celulas']; b['celulas_ids'].append(extra)
    b['condicoes'].update(circuitos_agrupados=circuits,agrupamento='FEIXE')
    p['fator_correcao']=factor
    r=analisar_circuito(p)
    assert Decimal(r['vinculo_celulas']['fator_derivado'])==Decimal(str(factor))
    b['condicoes']['grupo_homogeneo']=False
    with pytest.raises(ValueError): analisar_circuito(p)


@pytest.mark.parametrize('yearly,life,i2,status,restricted', [
    (100,500,29,'ATENDE_CALCULO_PARCIAL',False),
    (100,500,29.0000001,'NAO_ATENDE',False),
    (100.000001,500,20,'ATENDE_CALCULO_PARCIAL',True),
    (100,500.000001,20.000001,'NAO_ATENDE',True),
    (None,None,29,'PENDENTE',False),
    (None,500,29,'PENDENTE',False),
    (101,None,20,'ATENDE_CALCULO_PARCIAL',True),
    (None,None,30,'NAO_ATENDE',False),
])
def test_overload_boundaries_without_rounding(yearly,life,i2,status,restricted):
    r=verificar_sobrecarga(Decimal('19'),Decimal('20'),Decimal('20'),device(i2,yearly,life))
    assert r['status']==status and r['nota_duracao_aplicada']==restricted
    assert r['fonte_dispositivo_verificada'] is False
    assert r['curto_circuito']==r['coordenacao_protecoes']=='PENDENTE'
    assert r['liberacao_normativa'] is False


def test_explicit_device_source_and_nominal_are_required_and_no_i2_inference():
    p=scenario(); p['protecao_sobrecarga']=device()
    r=TestClient(app).post('/api/v1/circuitos/analisar',json=p)
    assert r.status_code==200
    assert r.json()['protecao_sobrecarga']['status']=='ATENDE_CALCULO_PARCIAL'
    for field in ['fonte','corrente_atuacao_i2_a']:
        bad=deepcopy(p); bad['protecao_sobrecarga'].pop(field)
        assert TestClient(app).post('/api/v1/circuitos/analisar',json=bad).status_code==422
    p['protecao_sobrecarga']['corrente_nominal_a']=25
    assert TestClient(app).post('/api/v1/circuitos/analisar',json=p).status_code==422


def test_bound_trace_rejects_adulteration_even_with_rehashed_outer_digest():
    p=scenario();p['protecao_sobrecarga']=device()
    trace,serialized,digest=preparar_registro(str(uuid4()),1,'C1',p,analisar_circuito(p))
    assert validar_registro(serialized,digest)==trace
    assert trace['trace_schema_version']==3
    assert trace['source_values_verified'] is False
    for kind in ['binding','protection','downgrade']:
        bad=deepcopy(trace)
        if kind=='binding': bad['limited_cell_binding']['celulas'][0]['valor']='99'
        elif kind=='protection': bad['resultado']['protecao_sobrecarga']['status']='APROVADO'
        else: bad['trace_schema_version']=2
        serial=_canonical(bad)
        with pytest.raises(ValueError): validar_registro(serial,sha256(serial.encode()).hexdigest())


def test_immutable_project_binds_new_optional_inputs_and_legacy_stays_readable(tmp_path):
    repo=RepositorioProjetos(str(tmp_path/'p.sqlite')); pid=str(uuid4()); p=scenario()
    repo.salvar(pid,'Ensaios',{'circuitos':[{'nome':'C1',**p}]},0)
    result=repo.registrar_ensaio(pid,1,'C1',p)
    assert result['trace_schema_version']==3
    assert repo.consultar_ensaio(pid,result['id'])==result
    for field in ['vinculo_celulas','protecao_sobrecarga']:
        bad=deepcopy(p)
        if field=='vinculo_celulas': bad[field]=None
        else: bad[field]=device()
        with pytest.raises(ValueError,match='campo salvo'): repo.registrar_ensaio(pid,1,'C1',bad)


def test_cli_runs_same_bound_calculation_without_database(tmp_path,capsys):
    import json
    from sie_api.cli import main
    path=tmp_path/'analysis.json';path.write_text(json.dumps(scenario()))
    assert main(['analisar','--arquivo',str(path)])==0
    out=json.loads(capsys.readouterr().out)
    assert out['vinculo_celulas']['registro_revisao']==REVISION
    assert out['liberado_para_uso_normativo'] is False


def test_reference_temperature_needs_no_ambient_cell_and_rejects_whitespace_source():
    p=scenario();p['fator_correcao']=1
    p['vinculo_celulas']['condicoes']['temperatura_ambiente_c']=30
    p['vinculo_celulas']['celulas_ids'].remove('CEL-05')
    assert analisar_circuito(p)['condutor']['capacidade_decisao_a']==24
    p['protecao_sobrecarga']=device();p['protecao_sobrecarga']['fonte']['documento']='   '
    assert TestClient(app).post('/api/v1/circuitos/analisar',json=p).status_code==422


def test_protection_only_trace_cannot_drop_verifier_provenance():
    p=scenario();p.pop('vinculo_celulas');p['protecao_sobrecarga']=device()
    trace,serial,digest=preparar_registro(str(uuid4()),1,'C1',p,analisar_circuito(p))
    assert validar_registro(serial,digest)==trace
    trace.pop('additional_implementation_sources')
    trace['resultado']['protecao_sobrecarga']['status']='APROVADO'
    forged=_canonical(trace)
    with pytest.raises(ValueError,match='proveniência'):
        validar_registro(forged,sha256(forged.encode()).hexdigest())
