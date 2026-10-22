"""Finite manufacturer facts, with no automatic product/installation approval.

The registry is server-owned. A client's document/hash or approval flag cannot
create another verified product. Values are strings to preserve decimal units.
"""
from copy import deepcopy
from decimal import Decimal
from importlib.resources import files
from urllib.parse import urlparse
import json

from .installation_service import digest

CATALOG = json.loads(files('sie_api').joinpath('data/protection_schneider_f08.json').read_text(encoding='utf-8'))
PAIR_CATALOG = json.loads(files('sie_api').joinpath('data/protection_coordination_schneider_f08.json').read_text(encoding='utf-8'))
KEY = 'SCHNEIDER_A9F74116_IEC60898_1'
PAIR_KEY = 'SCHNEIDER_IC60N_C32_C16_1P_230'
PAIR_SOURCE_HASH = '2cc52f0569eeef7323677dfee855c9ebf5bc0fb7ee7d370ad22fabfeda1b1fa3'
SOURCE_HASHES = {
    'product': '144a5c03662d0cf86653221d298664a370e9448b2d9d7c749efa49b3d3f9196e',
    'curves': 'e9665f22fd3e0ec6346a8e682090b2f118c83724df92e72b494a75ea74ec06d6',
}
SOURCE_URLS = {
    'product': 'https://www.se.com/hk/en/product/A9F74116/miniature-circuit-breaker-mcb-acti9-ic60n-1p-16a-c-curve-6000a-iec-en-608981-10ka-iec-en-609472/',
    'curves': 'https://ckm-content.se.com/ckmContent/sfc/servlet.shepherd/document/download/0691H00000DxLluQAF',
}


def catalog():
    """Return a detached validated snapshot; corrupt data fail closed."""
    try:
        result = deepcopy(CATALOG)
        if (result['schema_version'] != 1 or result['catalog_version'] != 'F08_SCHNEIDER_A9F74116_1'
                or result['status'] != 'SOURCE_LINKED_NOT_PROFESSIONAL_APPROVAL'
                or result['professional_approval'] is not False
                or result['product_certification_verified'] is not False):
            raise ValueError('Catálogo F08 incompatível')
        sources = result['sources']
        if len(sources) != 2 or {s['id'] for s in sources} != set(SOURCE_HASHES):
            raise ValueError('Fontes F08 ausentes ou duplicadas')
        for source in sources:
            if source['sha256'] != SOURCE_HASHES[source['id']]:
                raise ValueError('Integridade da referência F08 divergente')
            parsed = urlparse(source['url'])
            if parsed.scheme != 'https' or parsed.hostname not in {'www.se.com', 'ckm-content.se.com'}:
                raise ValueError('Fonte F08 fora do fabricante oficial')
            if source['url'] != SOURCE_URLS[source['id']]:
                raise ValueError('Referência F08 não corresponde ao documento conferido')
            if source['publisher'] != 'Schneider Electric' or not source['reference'].strip():
                raise ValueError('Proveniência F08 inválida')
        rows = result['devices']
        if len(rows) != 1:
            raise ValueError('Recorte finito F08 alterado')
        row = rows[0]
        expected = {'catalog_key': KEY, 'family': 'MCB', 'manufacturer': 'Schneider Electric',
                    'model': 'A9F74116', 'nominal_current_a': '16', 'i2_a': '23.2',
                    'rated_voltage_v': '230', 'breaking_capacity_a': '6000',
                    'breaking_standard': 'IEC/EN 60898-1', 'capacity_quantity': 'Icn',
                    'curve': 'C', 'poles': 1, 'reference_temperature_c': '30',
                    'frequency_hz': ['50', '60'], 'network': 'AC',
                    'conventional_trip_time_s': '3600', 'magnetic_band_in': ['5', '10'],
                    'full_time_current_curve_digitized': False,
                    'let_through_energy_available': False, 'selectivity_tables_available': False,
                    'source_verified': True, 'professional_approval': False,
                    'product_certification_verified': False}
        if any(row.get(key) != value for key, value in expected.items()):
            raise ValueError('Dado F08 diverge do recorte documental conferido')
        if type(row['poles']) is not int:
            raise ValueError('Número de polos F08 inválido')
        if Decimal(row['i2_a']) != Decimal('1.45') * Decimal(row['nominal_current_a']):
            raise ValueError('I2 F08 inconsistente')
        if row['evidence']['sha256'] != SOURCE_HASHES['curves'] or not result['boundaries']:
            raise ValueError('Limitações/proveniência F08 ausentes')
        if any(key not in expected for key in row['verified_fields']):
            raise ValueError('Campo F08 não conferido')
        result['coordination_catalog'] = pair_catalog()
        return result
    except (KeyError, TypeError, AttributeError) as exc:
        raise ValueError('Catálogo F08 incompleto ou inválido') from exc


def catalog_hash():
    return digest(catalog())


def pair_catalog():
    """One visually checked manufacturer pair, without rating-ratio inference."""
    try:
        result = deepcopy(PAIR_CATALOG)
        source = result['source']
        if (result['schema_version'] != 1 or result['catalog_version'] != 'F08_SCHNEIDER_COORDINATION_1'
                or result['professional_approval'] is not False
                or result['product_certification_verified'] is not False
                or source['sha256'] != PAIR_SOURCE_HASH
                or source['edition'] != '4.0 / 2026-08-03'
                or source['document_ref'] != 'LVPED318033EN'
                or source['url'] != 'https://download.schneider-electric.com/files?p_Doc_Ref=LVPED318033EN&p_File_Ext=.PDF'
                or source['publisher'] != 'Schneider Electric'
                or source['bytes'] != 11585539 or source['pages'] != 362):
            raise ValueError('Fonte de coordenação F08 incompatível')
        if len(result['pairs']) != 1 or not result['boundaries']:
            raise ValueError('Recorte de coordenação F08 inválido')
        row = result['pairs'][0]
        expected = {'catalog_key': PAIR_KEY, 'voltage_v': '230', 'network': 'AC',
                    'selectivity_limit_a': '260', 'total_selectivity': False,
                    'source_verified': True, 'professional_approval': False,
                    'product_certification_verified': False}
        if any(row.get(key) != value for key, value in expected.items()):
            raise ValueError('Par F08 diverge da tabela conferida')
        for direction, nominal in [('upstream', '32'), ('downstream', '16')]:
            device = row[direction]
            identity = {'family': 'MCB', 'manufacturer': 'Schneider Electric',
                        'model': 'iC60N', 'nominal_current_a': nominal, 'curve': 'C', 'poles': 1}
            if device != identity or type(device['poles']) is not int:
                raise ValueError('Identidade do par F08 incompatível')
        if (row['evidence']['sha256'] != PAIR_SOURCE_HASH
                or row['provenance']['table_certifies_installed_device'] is not False
                or row['provenance']['limit_inclusive'] is not True
                or row['provenance']['series_aliases'] != {'A9F74116': 'iC60N'}):
            raise ValueError('Proveniência do par F08 inválida')
        return result
    except (KeyError, TypeError, AttributeError) as exc:
        raise ValueError('Catálogo de pares F08 incompleto ou inválido') from exc


def resolve_pair(catalog_key):
    for row in pair_catalog()['pairs']:
        if row['catalog_key'] == catalog_key:
            return deepcopy(row)
    raise ValueError('Par fora do catálogo finito F08')


def coordination(catalog_key):
    return resolve_pair(catalog_key)


def resolve(catalog_key):
    """Resolve identity only. The caller must also check application conditions."""
    for row in catalog()['devices']:
        if row['catalog_key'] == catalog_key:
            return deepcopy(row)
    raise ValueError('Dispositivo fora do catálogo finito F08')


def applicable(catalog_key, *, voltage_v, temperature_c, frequency_hz, network='AC', poles=1):
    """Exact-scope check: no extrapolation, tolerance or invented derating."""
    row = resolve(catalog_key)
    try:
        values = [Decimal(str(x)) for x in (voltage_v, temperature_c, frequency_hz)]
        if not all(x.is_finite() for x in values):
            return False
        return (values[0] == Decimal(row['rated_voltage_v'])
                and values[1] == Decimal(row['reference_temperature_c'])
                and values[2] in [Decimal(x) for x in row['frequency_hz']]
                and network == row['network'] and type(poles) is int and poles == row['poles'])
    except (ValueError, ArithmeticError):
        return False
