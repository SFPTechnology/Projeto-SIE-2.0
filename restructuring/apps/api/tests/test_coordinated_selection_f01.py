"""Synthetic coordination cases; no normative or device I2 approval."""
from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from sie_api import application
from sie_api.domain.engines import selecionar_condutor
from sie_api.main import app


def scenario(ib=20.5, factor=.87, rows=None):
    return {'corrente_a': ib, 'fator_correcao': factor, 'tensao_v': 220,
            'comprimento_m': 30, 'resistencia_ohm_km': 7.41,
            'tabela_condutores': rows or [
                {'secao_mm2': 2.5, 'capacidade_a': 24},
                {'secao_mm2': 4, 'capacidade_a': 32}],
            'evidencia': {'documento': 'Synthetic software test',
                         'edicao': 'test-only', 'referencia': 'not approved'}}


def test_r4_upsize_until_breaker_pair_exists_and_primitive_is_unchanged():
    first = selecionar_condutor(Decimal('20.5'), Decimal('.87'),
                               ((Decimal('2.5'), Decimal('24')), (Decimal('4'), Decimal('32'))))
    assert first.secao_mm2 == Decimal('2.50')
    assert first.capacidade_corrigida_a == Decimal('20.88')
    result = application.analisar_circuito(scenario())
    assert result['condutor']['secao_mm2'] == 4
    assert result['condutor']['capacidade_decisao_a'] == 27.84
    assert result['disjuntor']['corrente_a'] == 25
    assert result['status_engenharia'] == 'PENDENTE'
    assert result['liberado_para_uso_normativo'] is False


@pytest.mark.parametrize('ib,factor,rows,section,nominal', [
    (20, .87, None, 2.5, 20),
    (20.5, .87, None, 4, 25),
    (25, 1, [{'secao_mm2': 4, 'capacidade_a': 25}], 4, 25),
    (19.99, 1, [{'secao_mm2': 2.5, 'capacidade_a': 19.996},
               {'secao_mm2': 4, 'capacidade_a': 20}], 4, 20),
])
def test_coordinated_pair_preserves_exact_ib_in_iz(ib, factor, rows, section, nominal):
    result = application.analisar_circuito(scenario(ib, factor, rows))
    assert result['condutor']['secao_mm2'] == section
    assert result['disjuntor']['corrente_a'] == nominal
    assert Decimal(str(ib)) <= Decimal(str(nominal)) <= Decimal(str(result['condutor']['capacidade_decisao_a']))
    assert result['liberado_para_uso_normativo'] is False


@pytest.mark.parametrize('catalog,rows,ib', [
    ((), None, 20.5),
    ((Decimal('20'),), None, 20.5),
    ((Decimal('25'),), [{'secao_mm2': 2.5, 'capacidade_a': 24}], 20.5),
    ((Decimal('25'),), [{'secao_mm2': 2.5, 'capacidade_a': 10}], 20.5),
])
def test_no_catalog_or_no_admissible_section_fails_closed(monkeypatch, catalog, rows, ib):
    monkeypatch.setattr(application, 'CATALOGO_DISJUNTORES', catalog)
    with pytest.raises(ValueError):
        application.analisar_circuito(scenario(ib, .87, rows))


def test_no_pair_preserves_f00_error_distinct_from_no_ib_capacity():
    # Rounding 19.996 to 20 for presentation must never allow In=20.
    rows = [{'secao_mm2': 2.5, 'capacidade_a': 19.996}]
    with pytest.raises(ValueError, match='Nenhum disjuntor comercial atende Ib ≤ In ≤ Iz'):
        application.analisar_circuito(scenario(19.99, 1, rows))
    with pytest.raises(ValueError, match='Tabela informada não possui seção suficiente'):
        application.analisar_circuito(scenario(20, 1, rows))


def test_http_r4_upsize_keeps_pending_and_table_without_pair_is_rejected():
    client = TestClient(app)
    response = client.post('/api/v1/circuitos/analisar', json=scenario())
    assert response.status_code == 200
    assert response.json()['condutor']['secao_mm2'] == 4
    assert response.json()['disjuntor']['corrente_a'] == 25
    assert response.json()['liberado_para_uso_normativo'] is False
    payload = scenario(rows=[{'secao_mm2': 2.5, 'capacidade_a': 24}])
    assert client.post('/api/v1/circuitos/analisar', json=payload).status_code == 422


def test_trace_records_coordinator_hash_without_backfilling_older_traces():
    from hashlib import sha256
    from inspect import getsource
    from uuid import uuid4
    from sie_api.calculation_traces import _canonical, preparar_registro, validar_registro
    payload = scenario()
    item, serial, digest = preparar_registro(str(uuid4()), 1, 'C1', payload,
                                             application.analisar_circuito(payload))
    assert item['orchestration_source']['function_source_sha256'] == sha256(
        getsource(application.analisar_circuito).encode()).hexdigest()
    assert validar_registro(serial, digest) == item
    item.pop('orchestration_source')
    legacy = _canonical(item)
    assert validar_registro(legacy, sha256(legacy.encode()).hexdigest()) == item
    item['orchestration_source'] = {'id': 'sie_api.application.analisar_circuito:v2',
                                    'function_source_sha256': 'invalid'}
    bad = _canonical(item)
    with pytest.raises(ValueError, match='Proveniencia da orquestracao'):
        validar_registro(bad, sha256(bad.encode()).hexdigest())
