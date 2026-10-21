"""Independent arithmetic with synthetic cable data, not normative reference cases."""
from copy import deepcopy
from decimal import Decimal, localcontext

import pytest
from pydantic import ValidationError

from sie_api.voltage_checks import QuedaImpedancia, calcular_queda_impedancia


def source():
    return {'documento': 'SYNTHETIC TEST CABLE; NOT MANUFACTURER DATA',
            'revisao': 'test-v1', 'referencia': 'synthetic arithmetic fixture', 'sha256': 'b'*64}


def cable(**changes):
    result = {'tipo_circuito': 'MONOFASICO_FASE_NEUTRO', 'regime': 'SENOIDAL_PERMANENTE',
              'harmonicas_relevantes': False, 'secao_mm2': 4.0, 'material': 'Cu',
              'isolacao': 'PVC', 'temperatura_condutor_c': 70.0, 'frequencia_hz': 60.0,
              'arranjo': 'synthetic two equivalent conductors', 'rca_ohm_km': 2.0,
              'xl_ohm_km': .1, 'fator_potencia': .8, 'natureza_carga': 'INDUTIVA',
              'fonte_rca': source(), 'fonte_xl': source()}
    return {**result, **changes}


def test_monophase_expected_is_independent_and_current_is_not_multiplied_twice_by_pf():
    # sin = .6; Rcos+Xsin=1.6+.06=1.66; 2*.1km*10A*1.66=3.32V.
    r=calcular_queda_impedancia(10,100,220,cable(),secao_mm2=4)
    assert Decimal(r['queda_decisao_v'])==Decimal('3.32')
    with localcontext() as ctx:
        ctx.prec=50
        assert Decimal(r['queda_decisao_percentual'])==Decimal('332')/Decimal('220')
    assert r['status']=='CALCULADO_PARCIAL'
    assert r['base_tensao']=='FASE_NEUTRO'
    assert r['fontes_parametros_verificadas'] is False
    assert r['liberacao_normativa'] is False


def test_three_phase_expected_and_line_line_voltage_base():
    r=calcular_queda_impedancia(10,100,380,cable(tipo_circuito='TRIFASICO_EQUILIBRADO',
            rca_ohm_km=1.0,xl_ohm_km=1.0,fator_potencia=.6),secao_mm2=4)
    # .6+.8=1.4; sqrt(3)*1.4 V. A float comparison is independent of production Decimal sqrt.
    assert float(r['queda_decisao_v'])==pytest.approx(2.424871130596428,rel=1e-14)
    assert r['base_tensao']=='LINHA_LINHA'
    assert r['limite_declarado_atendido'] is None


def test_phase_phase_uses_same_loop_formula_but_distinct_nominal_voltage():
    r=calcular_queda_impedancia(10,100,220,cable(tipo_circuito='MONOFASICO_FASE_FASE'))
    assert Decimal(r['queda_decisao_v'])==Decimal('3.32')
    assert r['base_tensao']=='LINHA_LINHA'


def test_resistive_zero_length_and_no_reactance_default():
    d=cable(fator_potencia=1.0,natureza_carga='RESISTIVA')
    assert Decimal(calcular_queda_impedancia(10,100,200,d)['queda_decisao_v'])==4
    assert Decimal(calcular_queda_impedancia(10,0,200,d)['queda_decisao_v'])==0
    d.pop('xl_ohm_km')
    with pytest.raises(ValidationError): calcular_queda_impedancia(10,100,200,d)


@pytest.mark.parametrize('value,within',[(2.0,True),(2.0000000000000004,False)])
def test_exact_limit_and_epsilon_do_not_use_rounded_display(value,within):
    d=cable(rca_ohm_km=value,xl_ohm_km=0.0,fator_potencia=1.0,natureza_carga='RESISTIVA',
            limite_queda_percentual=2.0,fonte_limite=source(),escopo_limite='TRECHO')
    r=calcular_queda_impedancia(10,100,200,d)
    assert r['limite_declarado_atendido'] is within
    assert r['liberacao_normativa'] is False
    assert r['aplicabilidade_normativa_verificada'] is False


def test_total_limit_includes_explicit_upstream_and_missing_upstream_is_rejected():
    d=cable(rca_ohm_km=2.0,xl_ohm_km=0.0,fator_potencia=1.0,
            limite_queda_percentual=3.0,fonte_limite=source(),escopo_limite='TOTAL_DESDE_ORIGEM',
            queda_montante_percentual=1.0)
    r=calcular_queda_impedancia(10,100,200,d)
    assert r['limite_declarado_atendido'] is True
    assert Decimal(r['queda_comparada_percentual'])==3
    d['queda_montante_percentual']=1.0000000001
    assert calcular_queda_impedancia(10,100,200,d)['limite_declarado_atendido'] is False
    d.pop('queda_montante_percentual')
    with pytest.raises(ValidationError): calcular_queda_impedancia(10,100,200,d)


@pytest.mark.parametrize('change', [
    {'fator_potencia':0.0}, {'fator_potencia':1.01}, {'fator_potencia':True},
    {'xl_ohm_km':-.1}, {'rca_ohm_km':0.0}, {'rca_ohm_km':float('inf')},
    {'xl_ohm_km':float('nan')}, {'harmonicas_relevantes':True},
    {'natureza_carga':'CAPACITIVA'}, {'tipo_circuito':'TRIFASICO_DESEQUILIBRADO'},
    {'regime':'PARTIDA'}, {'isolacao':'   '}, {'arranjo':'   '},
    {'fonte_rca':None}, {'frequencia_hz':0.0}, {'liberacao_normativa':True},
    {'limite_queda_percentual':4.0}, {'fonte_limite':source()},
    {'queda_montante_percentual':1.0}, {'natureza_carga':'RESISTIVA'},
])
def test_unsupported_conditions_missing_sources_and_forged_flags_are_rejected(change):
    with pytest.raises(ValidationError): calcular_queda_impedancia(10,100,220,cable(**change))


def test_wrong_selected_section_is_rejected_and_data_are_not_mutated():
    d=cable();saved=deepcopy(d)
    with pytest.raises(ValueError,match='seção selecionada'):
        calcular_queda_impedancia(10,100,220,d,secao_mm2=6)
    assert d==saved
    assert calcular_queda_impedancia(10,100,220,None)['status']=='PENDENTE'


@pytest.mark.parametrize('i,l,v',[(True,100,220),(0,100,220),(10,-1,220),(10,100,0),
                                 (float('nan'),100,220),(10,float('inf'),220)])
def test_direct_function_rejects_invalid_base_parameters(i,l,v):
    with pytest.raises(ValueError): calcular_queda_impedancia(i,l,v,cable())


def test_extreme_finite_inputs_cannot_emit_infinite_json_floats():
    with pytest.raises(ValueError,match='intervalo numérico'):
        calcular_queda_impedancia(1e308,1e308,1,cable(rca_ohm_km=1e308))
