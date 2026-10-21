"""P03 numeric cases use synthetic sources/devices, never manufacturer approval."""
from copy import deepcopy
from decimal import Decimal

import pytest
from pydantic import ValidationError

from sie_api.protection_extended import (
    EstudoCoordenacao, ProtecaoCurtoCircuito, verificar_coordenacao,
    verificar_curto_circuito,
)


def source():
    return {'documento': 'SYNTHETIC software-test source, not manufacturer data',
            'revisao': 'fixture-v1', 'referencia': 'synthetic independent arithmetic',
            'sha256': 'c' * 64}


def short_case():
    # Independent arithmetic: k*S=100*10=1000; limit=1,000,000 A²s.
    return {'dispositivo_id': 'SYNTHETIC-Q1', 'corrente_nominal_a': 20,
            'corrente_curto_max_a': 6000, 'capacidade_interrupcao_a': 6000,
            'grandeza_capacidade': 'Icn', 'tempo_eliminacao_s': 1,
            'metodo_energia': 'I_EFICAZ_QUADRADO_TEMPO',
            'corrente_eficaz_atuacao_a': 1000,
            'assimetria_significativa': True, 'k_a_raiz_s_mm2': 100,
            'material': 'Cu', 'isolacao': 'PVC',
            'temperatura_inicial_c': 70, 'temperatura_final_c': 160,
            'fonte_dispositivo': source(), 'fonte_curto': source(), 'fonte_k': source()}


def study_case():
    return {'estudo_id': 'SYNTHETIC-STUDY', 'dispositivo_sobrecarga_id': 'SYNTHETIC-Q1',
            'dispositivo_curto_id': 'SYNTHETIC-Q1', 'corrente_curto_max_estudada_a': 6000,
            'conclusao_declarada': 'COMPATIVEL', 'seletividade_necessaria': True,
            'seletividade_demonstrada': True, 'abrange_dr': False,
            'escopo_estudo': 'Synthetic study; no real curves or manufacturer statement',
            'fonte': source()}


def test_equal_interrupting_and_energy_boundaries_pass_partial_only():
    r=verificar_curto_circuito(Decimal('10'), short_case(),
                             {'material': 'Cu', 'isolacao': 'PVC', 'temperatura_condutor_c': 70},
                             Decimal('20'))
    assert r['status']=='ATENDE_CALCULO_PARCIAL'
    assert r['limite_termico_a2s']==r['energia_passante_utilizada_a2s']=='1000000'
    assert r['capacidade_interrupcao_atendida'] is True
    assert r['fontes_verificadas'] is False and r['liberacao_normativa'] is False
    assert r['atuacao_ik_min_e_curvas']==r['coordenacao_completa']=='PENDENTE'


@pytest.mark.parametrize('change', ['interrupting', 'thermal'])
def test_epsilon_over_limits_fails_without_rounding(change):
    p=short_case()
    if change=='interrupting': p['corrente_curto_max_a']=6000.000001
    else: p['corrente_eficaz_atuacao_a']=1000.000001
    r=verificar_curto_circuito(Decimal('10'),p)
    assert r['status']=='NAO_ATENDE' and r['liberacao_normativa'] is False


@pytest.mark.parametrize('duration,asymmetry,method,expected', [
    (.1, True, 'I_EFICAZ_QUADRADO_TEMPO', 'ATENDE_CALCULO_PARCIAL'),
    (5, True, 'I_EFICAZ_QUADRADO_TEMPO', 'ATENDE_CALCULO_PARCIAL'),
    (5.000001, False, 'I_EFICAZ_QUADRADO_TEMPO', 'PENDENTE'),
    (.099999, True, 'I_EFICAZ_QUADRADO_TEMPO', 'PENDENTE'),
    (.001, None, 'I_EFICAZ_QUADRADO_TEMPO', 'PENDENTE'),
    (.001, False, 'I_EFICAZ_QUADRADO_TEMPO', 'ATENDE_CALCULO_PARCIAL'),
    (.001, True, 'INTEGRAL_JOULE_DECLARADA', 'ATENDE_CALCULO_PARCIAL'),
    (5.000001, False, 'INTEGRAL_JOULE_DECLARADA', 'PENDENTE'),
])
def test_time_domain_and_energy_source(duration,asymmetry,method,expected):
    p=short_case();p.update(tempo_eliminacao_s=duration,assimetria_significativa=asymmetry,
                           metodo_energia=method)
    p['corrente_eficaz_atuacao_a']=100 # 100²*5=50,000 <1,000,000
    if method=='INTEGRAL_JOULE_DECLARADA':
        p.pop('corrente_eficaz_atuacao_a');p['energia_passante_a2s']=1000000
    r=verificar_curto_circuito(Decimal('10'),p)
    assert r['status']==expected
    if expected=='PENDENTE': assert r['criterio_termico_atendido'] is None


def test_minimal_prospective_current_is_not_substituted_for_effective_actuation():
    p=short_case();p.pop('corrente_eficaz_atuacao_a')
    with pytest.raises(ValidationError): verificar_curto_circuito(Decimal('10'),p)


def test_context_and_nominal_binding_are_checked():
    p=short_case()
    ctx={'material': 'Cu', 'isolacao': 'PVC', 'temperatura_condutor_c': 70}
    with pytest.raises(ValueError, match='In selecionado'):
        verificar_curto_circuito(Decimal('10'),p,ctx,Decimal('25'))
    for field,value in [('material','Al'),('isolacao','XLPE'),('temperatura_inicial_c',60)]:
        bad=deepcopy(p);bad[field]=value
        with pytest.raises(ValueError,match='Condições de k'):
            verificar_curto_circuito(Decimal('10'),bad,ctx)


@pytest.mark.parametrize('bad', [0,-1,float('inf'),float('nan'),True,'1'])
def test_invalid_or_coerced_numeric_inputs_rejected(bad):
    p=short_case();p['tempo_eliminacao_s']=bad
    with pytest.raises(ValidationError): ProtecaoCurtoCircuito.model_validate(p)


def test_extra_fields_empty_source_and_ambiguous_energy_rejected():
    p=short_case();p['approved']=True
    with pytest.raises(ValidationError): ProtecaoCurtoCircuito.model_validate(p)
    p=short_case();p['fonte_k']['documento']='  '
    with pytest.raises(ValidationError): ProtecaoCurtoCircuito.model_validate(p)
    p=short_case();p['energia_passante_a2s']=100
    with pytest.raises(ValidationError): ProtecaoCurtoCircuito.model_validate(p)
    p=short_case();p['temperatura_final_c']=70
    with pytest.raises(ValidationError): ProtecaoCurtoCircuito.model_validate(p)


def test_missing_data_and_small_sections_preserve_pending_applicability():
    assert verificar_curto_circuito(Decimal('10'),None)['status']=='PENDENTE'
    r=verificar_curto_circuito(Decimal('2.5'),short_case())
    assert any('Pequenas seções' in warning for warning in r['ressalvas'])
    assert r['fontes_verificadas'] is False


def test_positive_declared_study_never_approves_coordination():
    r=verificar_coordenacao(study_case(),Decimal('6000'),'SYNTHETIC-Q1','SYNTHETIC-Q1')
    assert r['status']=='PENDENTE' and r['cobertura_corrente_curto'] is True
    assert r['estudo_verificado'] is False and r['liberacao_normativa'] is False
    assert verificar_coordenacao(None)['status']=='PENDENTE'


@pytest.mark.parametrize('change',['current','incompatible','selectivity'])
def test_study_with_explicit_incompatibility_fails(change):
    p=study_case()
    if change=='current': p['corrente_curto_max_estudada_a']=5999.99999
    elif change=='incompatible': p['conclusao_declarada']='INCOMPATIVEL'
    else: p['seletividade_demonstrada']=False
    assert verificar_coordenacao(p,Decimal('6000'))['status']=='NAO_ATENDE'


def test_study_identity_cannot_be_substituted():
    with pytest.raises(ValueError,match='sobrecarga'):
        verificar_coordenacao(study_case(),dispositivo_sobrecarga_id='OTHER')
    with pytest.raises(ValueError,match='curto'):
        verificar_coordenacao(study_case(),dispositivo_curto_id='OTHER')
    p=study_case();p['fonte']['referencia']=' '
    with pytest.raises(ValidationError): EstudoCoordenacao.model_validate(p)
