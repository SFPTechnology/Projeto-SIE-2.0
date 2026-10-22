"""Independent exact-scope and fail-closed manufacturer binding tests."""
from copy import deepcopy
from decimal import Decimal
import pytest
from sie_api import protection_registry_f08 as registry


def test_one_real_product_with_separate_capacity_standard_and_provenance():
    row = registry.resolve(registry.KEY)
    assert row['model'] == 'A9F74116'
    assert row['nominal_current_a'] == '16'
    assert row['i2_a'] == '23.2'  # independent 16 × 145/100
    assert row['breaking_capacity_a'] == '6000'
    assert row['capacity_quantity'] == 'Icn'
    assert row['breaking_standard'] == 'IEC/EN 60898-1'
    assert row['professional_approval'] is False
    assert row['product_certification_verified'] is False
    assert row['let_through_energy_available'] is False
    assert row['selectivity_tables_available'] is False
    assert len(registry.catalog_hash()) == 64


@pytest.mark.parametrize('frequency', ['50', '60', Decimal('60')])
def test_exact_verified_application_scope(frequency):
    assert registry.applicable(registry.KEY, voltage_v='230', temperature_c='30', frequency_hz=frequency)


@pytest.mark.parametrize('overrides', [
    {'voltage_v': '220'}, {'voltage_v': '240'}, {'temperature_c': '40'},
    {'temperature_c': None}, {'frequency_hz': '55'}, {'frequency_hz': 'NaN'},
    {'network': 'DC'}, {'poles': 2}, {'poles': True},
])
def test_no_extrapolation_from_title_or_operating_temperature(overrides):
    params = {'voltage_v': '230', 'temperature_c': '30', 'frequency_hz': '60', **overrides}
    assert registry.applicable(registry.KEY, **params) is False


def test_unknown_product_is_not_verified_by_name():
    with pytest.raises(ValueError, match='fora do catálogo'):
        registry.resolve('A9F74116')


def test_snapshot_is_detached():
    row = registry.resolve(registry.KEY)
    row['i2_a'] = '1'
    row['provenance']['capacity_scope'] = 'fake'
    assert registry.resolve(registry.KEY)['i2_a'] == '23.2'
    snapshot = registry.catalog()
    snapshot['sources'].clear()
    assert len(registry.catalog()['sources']) == 2


@pytest.mark.parametrize('key,value', [
    ('breaking_capacity_a', '10000'), ('breaking_standard', 'IEC/EN 60947-2'),
    ('rated_voltage_v', '400'), ('i2_a', '20.8'), ('professional_approval', True),
    ('selectivity_tables_available', True), ('let_through_energy_available', True),
    ('poles', True),
])
def test_mixed_standard_or_fabricated_approval_fails_closed(monkeypatch, key, value):
    bad = deepcopy(registry.CATALOG)
    bad['devices'][0][key] = value
    monkeypatch.setattr(registry, 'CATALOG', bad)
    with pytest.raises(ValueError):
        registry.catalog()


@pytest.mark.parametrize('change', ['source_hash', 'source_url', 'other_official_url', 'missing', 'extra_device', 'certification'])
def test_incomplete_or_invented_provenance_rejected(monkeypatch, change):
    bad = deepcopy(registry.CATALOG)
    if change == 'source_hash': bad['sources'][0]['sha256'] = '0' * 64
    elif change == 'source_url': bad['sources'][0]['url'] = 'https://untrusted.example/product'
    elif change == 'other_official_url': bad['sources'][0]['url'] = 'https://www.se.com/other-product'
    elif change == 'missing': del bad['devices']
    elif change == 'extra_device': bad['devices'].append(deepcopy(bad['devices'][0]))
    else: bad['product_certification_verified'] = True
    monkeypatch.setattr(registry, 'CATALOG', bad)
    with pytest.raises(ValueError):
        registry.catalog()


def test_exact_manufacturer_pair_limit_is_not_total_selectivity():
    pair = registry.resolve_pair(registry.PAIR_KEY)
    assert pair['upstream']['model'] == pair['downstream']['model'] == 'iC60N'
    assert pair['upstream']['nominal_current_a'] == '32'
    assert pair['downstream']['nominal_current_a'] == '16'
    assert pair['selectivity_limit_a'] == '260'  # directly checked A-31 cell, amperes
    assert pair['total_selectivity'] is False
    assert pair['provenance']['table_certifies_installed_device'] is False
    assert pair['provenance']['limit_inclusive'] is True
    assert registry.coordination(registry.PAIR_KEY) == pair
    assert registry.catalog()['coordination_catalog']['source']['pages'] == 362


def test_unknown_pair_is_not_inferred_from_rating_ratios():
    with pytest.raises(ValueError, match='Par fora'):
        registry.resolve_pair('C63_C16')


@pytest.mark.parametrize('change', ['limit', 'total', 'curve', 'poles', 'source', 'edition', 'alias', 'installed'])
def test_pair_mismatch_fails_closed_and_prevents_new_result_hash(monkeypatch, change):
    bad = deepcopy(registry.PAIR_CATALOG)
    if change == 'limit': bad['pairs'][0]['selectivity_limit_a'] = '260000'
    elif change == 'total': bad['pairs'][0]['total_selectivity'] = True
    elif change == 'curve': bad['pairs'][0]['upstream']['curve'] = 'D'
    elif change == 'poles': bad['pairs'][0]['downstream']['poles'] = 2
    elif change == 'source': bad['source']['sha256'] = '0' * 64
    elif change == 'edition': bad['source']['edition'] = '2018'
    elif change == 'alias': bad['pairs'][0]['provenance']['series_aliases']['Fake'] = 'iC60N'
    else: bad['pairs'][0]['provenance']['table_certifies_installed_device'] = True
    monkeypatch.setattr(registry, 'PAIR_CATALOG', bad)
    with pytest.raises(ValueError): registry.resolve_pair(registry.PAIR_KEY)
    with pytest.raises(ValueError): registry.catalog_hash()


def test_pair_returned_identity_is_detached_from_server_registry():
    pair = registry.resolve_pair(registry.PAIR_KEY)
    pair['upstream']['nominal_current_a'] = '100'
    assert registry.resolve_pair(registry.PAIR_KEY)['upstream']['nominal_current_a'] == '32'
