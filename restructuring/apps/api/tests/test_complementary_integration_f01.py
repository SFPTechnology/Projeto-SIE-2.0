"""Integrated optional engineering checks: synthetic fixtures, no source approval."""
from copy import deepcopy
from hashlib import sha256
from uuid import uuid4
import json

import pytest
from fastapi.testclient import TestClient
from sie_api.main import app
from sie_api.application import analisar_circuito
from sie_api.storage import RepositorioProjetos
from sie_api.calculation_traces import preparar_registro, validar_registro, _canonical
from test_cell_binding_protection_f01 import scenario, device
from test_protection_extended_f01 import short_case, study_case
from test_voltage_impedance_f01 import cable


def complete():
    p=scenario();p['protecao_sobrecarga']=device()
    p['protecao_curto_circuito']=short_case()
    p['protecao_curto_circuito'].update(dispositivo_id='SYNTHETIC-20',corrente_eficaz_atuacao_a=100)
    p['estudo_coordenacao']=study_case()
    p['estudo_coordenacao'].update(dispositivo_sobrecarga_id='SYNTHETIC-20',dispositivo_curto_id='SYNTHETIC-20')
    p['queda_impedancia']=cable(secao_mm2=2.5)
    return p


def test_api_runs_conditional_checks_and_distinguishes_legacy_model():
    response=TestClient(app).post('/api/v1/circuitos/analisar',json=complete())
    assert response.status_code==200
    r=response.json();c=r['verificacoes_complementares']
    assert c['curto_circuito']['status']=='ATENDE_CALCULO_PARCIAL'
    assert c['coordenacao_protecoes']['status']=='PENDENTE'
    assert c['queda_impedancia']['status']=='CALCULADO_PARCIAL'
    assert 'XL' not in r['queda_tensao']['formula']
    assert 'XL' in c['queda_impedancia']['formula']
    assert r['status_engenharia']=='PENDENTE' and r['liberado_para_uso_normativo'] is False


@pytest.mark.parametrize('kind',['material','temperature','isolation','section','threephase','device'])
def test_reject_mixing_conditions_between_capacity_and_new_parameters(kind):
    p=complete()
    if kind=='material':p['queda_impedancia']['material']='Al'
    elif kind=='temperature':p['queda_impedancia']['temperatura_condutor_c']=20
    elif kind=='isolation':p['queda_impedancia']['isolacao']='EPR_XLPE'
    elif kind=='section':p['queda_impedancia']['secao_mm2']=4
    elif kind=='threephase':p['queda_impedancia']['tipo_circuito']='TRIFASICO_EQUILIBRADO'
    else:p['estudo_coordenacao']['dispositivo_curto_id']='another-device'
    assert TestClient(app).post('/api/v1/circuitos/analisar',json=p).status_code==422


@pytest.mark.parametrize('bound',[True,False])
def test_v4_roundtrip_and_tamper_resistance(bound):
    p=complete()
    if not bound:p.pop('vinculo_celulas')
    item,serial,digest=preparar_registro(str(uuid4()),1,'C1',p,analisar_circuito(p))
    assert item['trace_schema_version']==4
    assert validar_registro(serial,digest)==item
    for kind in ['result','proof','downgrade','hash']:
        bad=deepcopy(item)
        if kind=='result':bad['resultado']['verificacoes_complementares']['queda_impedancia']['queda_v']=0
        elif kind=='proof':bad.pop('complementary_provenance')
        elif kind=='downgrade':bad['trace_schema_version']=3 if bound else 2
        else:bad['complementary_provenance']['module_source_sha256']['voltage_checks']='invalid'
        raw=_canonical(bad)
        with pytest.raises(ValueError):validar_registro(raw,sha256(raw.encode()).hexdigest())


def test_new_inputs_bound_to_immutable_revision_and_cli_matches(tmp_path,capsys):
    p=complete();repo=RepositorioProjetos(str(tmp_path/'p.sqlite'));pid=str(uuid4())
    repo.salvar(pid,'Synthetic',{'circuitos':[{'nome':'C1',**p}]},0)
    trace=repo.registrar_ensaio(pid,1,'C1',p)
    assert trace['trace_schema_version']==4
    assert repo.consultar_ensaio(pid,trace['id'])==trace
    for field in ['queda_impedancia','protecao_curto_circuito','estudo_coordenacao']:
        bad=deepcopy(p);bad.pop(field)
        with pytest.raises(ValueError,match='campo salvo'):repo.registrar_ensaio(pid,1,'C1',bad)
    from sie_api.cli import main
    path=tmp_path/'scenario.json';path.write_text(json.dumps(p))
    assert main(['analisar','--arquivo',str(path)])==0
    assert json.loads(capsys.readouterr().out)['verificacoes_complementares']==trace['resultado']['verificacoes_complementares']


def test_new_missing_values_never_backfill_legacy_circuit(tmp_path):
    p=scenario();repo=RepositorioProjetos(str(tmp_path/'p.sqlite'));pid=str(uuid4())
    repo.salvar(pid,'Legacy',{'circuitos':[{'nome':'C1',**p}]},0)
    assert repo.registrar_ensaio(pid,1,'C1',p)['trace_schema_version']==3
    with pytest.raises(ValueError,match='campo salvo'):repo.registrar_ensaio(pid,1,'C1',complete())
