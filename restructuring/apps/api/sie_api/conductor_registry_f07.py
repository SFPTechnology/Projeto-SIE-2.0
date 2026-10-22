"""Finite server-owned F07 bindings. Manufacturer data do not confer ABNT approval."""
from copy import deepcopy
from decimal import Decimal,InvalidOperation
from datetime import date
import re
from urllib.parse import urlparse
from importlib.resources import files
import json
from .installation_service import digest
from . import cell_bindings

CATALOG=json.loads(files('sie_api').joinpath('data/conductor_prysmian_rev9_f07.json').read_text(encoding='utf-8'))

def _text(value,maximum=500):
    if not isinstance(value,str) or not value.strip() or len(value)>maximum:raise ValueError('Texto obrigatório do catálogo ausente')
    return value

def _number(value):
    _text(value)
    number=Decimal(value)
    if not number.is_finite() or number<=0 or len(number.as_tuple().digits)>30 or abs(number.as_tuple().exponent)>30:
        raise ValueError('Grandeza do catálogo inválida ou fora da precisão')
    return number

def _structure(c):
    for key in ('catalog_version','status'):_text(c[key])
    source=c['source']
    for key in ('document','publisher','normative_basis'):_text(source[key])
    _text(source['edition'],100)
    if not re.fullmatch('[0-9a-f]{64}',source['sha256']):raise ValueError('SHA256 da fonte inválido')
    url=urlparse(_text(source['url']))
    if url.scheme!='https' or url.hostname!='br.prysmian.com' or not url.path.endswith('.pdf'):
        raise ValueError('URL fora da fonte oficial do catálogo')
    date.fromisoformat(source['verified_on'])
    if type(source['pages']) is not int or source['pages']<=0 or source['normative_publisher_document_reproduced'] is not False:
        raise ValueError('Metadados da fonte inválidos')
    scope=c['scope']
    for key in ('product','material','insulation','method','medium','arrangement','containment','neutral_policy','regime','origin','rating_reference'):_text(scope[key])
    for key in ('conductor_temperature_c','frequency_hz','min_voltage_v','max_voltage_v','max_phase_section_mm2','insulation_rating_uo_v','insulation_rating_u_v'):_number(scope[key])
    if scope['loaded_conductors']!=2 or scope['installation_numbers']!=[3,5,7]:raise ValueError('Escopo do catálogo incompatível')
    expected_scope={'product':'PRYSMIAN_SUPERASTIC','material':'Cu','insulation':'PVC','conductor_temperature_c':'70','frequency_hz':'60','method':'B1','medium':'AIR','arrangement':'TWO_LOADED_TOUCHING','containment':'PVC','max_phase_section_mm2':'10','insulation_rating_uo_v':'450','insulation_rating_u_v':'750','neutral_policy':'SAME_SECTION_SAME_METAL_NO_REDUCTION','regime':'SINUSOIDAL_STEADY_NO_RELEVANT_HARMONICS','origin':'LV_UTILITY_POINT_OF_DELIVERY'}
    if any(scope[key]!=value for key,value in expected_scope.items()):raise ValueError('Escopo não corresponde à política implementada F07')
    if _number(scope['min_voltage_v'])!=50 or _number(scope['max_voltage_v'])!=750:raise ValueError('Faixa de tensão incompatível')
    rows=c['sections']
    if not isinstance(rows,list) or not rows:raise ValueError('Tabela vazia')
    for row in rows:
        for key in ('section_mm2','iz_base_a','rca_ohm_km','xl_ohm_km'):_number(row[key])
        for key in ('capacity_reference','impedance_reference'):_text(row[key])
        _text(source['url']+'#page=33; '+row['impedance_reference']+'; seção='+row['section_mm2'])
    for key in ('temperature_reference','grouping_reference'):_text(c['corrections'][key])
    for key in ('30','40'):_number(c['corrections']['temperature'][key])
    for key in ('1','2','3'):_number(c['corrections']['grouping'][key])
    if Decimal(c['corrections']['temperature']['30'])!=1 or Decimal(c['corrections']['grouping']['1'])!=1:
        raise ValueError('Fatores de referência devem ser1')
    mins=c['minimums']
    for key in ('LIGHTING','POWER'):
        if _number(mins['phase'][key])>max(Decimal(r['section_mm2']) for r in rows):raise ValueError('Mínimo de fase fora do catálogo comercial')
    for key in ('phase_reference','neutral_reference','pe_same_metal_phase_up_to_16','pe_reference'):_text(mins[key])
    for key in ('pe_separate_protected_floor_mm2','pe_separate_unprotected_floor_mm2'):_number(mins[key])
    for key in ('total_origin_limit_percent','terminal_local_limit_percent'):_number(c['voltage'][key])
    if any(Decimal(c['voltage'][key])>100 for key in ('total_origin_limit_percent','terminal_local_limit_percent')):raise ValueError('Limite de queda fora da faixa')
    if mins['pe_same_metal_phase_up_to_16']!='S':raise ValueError('Regra PE incompatível com política')
    if any(Decimal(mins[key])>max(Decimal(r['section_mm2']) for r in rows) for key in ('pe_separate_protected_floor_mm2','pe_separate_unprotected_floor_mm2')):raise ValueError('Mínimo PE fora do catálogo comercial')
    for key in ('reference','formula_reference'):_text(c['voltage'][key])
    independent=c['independent_reference']
    for key in ('table_reference','unit','rounding_basis'):_text(independent[key])
    _number(independent['rounding_bound_v_a_km'])
    if not isinstance(independent['rows'],list) or not independent['rows']:raise ValueError('Casos independentes ausentes')
    for row in independent['rows']:
        for key in ('section_mm2','pf_0.80','pf_0.95'):_number(row[key])
    if not isinstance(c['boundaries'],list) or not c['boundaries']:raise ValueError('Limites de escopo ausentes')
    for value in c['boundaries']:_text(value)

def catalog():
    try:
        return _validated_catalog()
    except (KeyError,TypeError,InvalidOperation,AttributeError) as exc:
        raise ValueError('Catálogo F07 incompleto ou inválido') from exc

def _validated_catalog():
    result=deepcopy(CATALOG)
    _structure(result)
    if result.get('schema_version')!=1 or result.get('status')!='SOURCE_LINKED_NOT_PROFESSIONAL_APPROVAL':
        raise ValueError('Catálogo F07 incompatível')
    rows=result.get('sections',[])
    if not rows or [Decimal(r['section_mm2']) for r in rows]!=sorted({Decimal(r['section_mm2']) for r in rows}):
        raise ValueError('Seções F07 ausentes, duplicadas ou fora de ordem')
    for row in rows:
        for key in ('section_mm2','iz_base_a','rca_ohm_km','xl_ohm_km'):
            number=Decimal(row[key])
            if not number.is_finite() or number<=0: raise ValueError('Dado F07 inválido')
    # Existing accepted F01 cells are an additional concordance check, never edited.
    accepted={Decimal(c[2]):Decimal(c[3]) for c in cell_bindings.CELLS if c[1]=='36'}
    if any(accepted.get(Decimal(r['section_mm2']))!=Decimal(r['iz_base_a']) for r in rows):
        raise ValueError('Catálogo F07 diverge das células de capacidade aceitas F01')
    expected={'CEL-05':result['corrections']['temperature']['40'],
              'CEL-07':result['corrections']['grouping']['2'],
              'CEL-08':result['corrections']['grouping']['3']}
    if any(next((Decimal(c[3]) for c in cell_bindings.CELLS if c[0]==key),None)!=Decimal(value) for key,value in expected.items()):
        raise ValueError('Fatores F07 divergem das células aceitas F01')
    # The conservative search uses monotonic improvement of section, ampacity and R/X.
    for a,b in zip(rows,rows[1:]):
        if Decimal(b['iz_base_a'])<Decimal(a['iz_base_a']) or Decimal(b['rca_ohm_km'])>Decimal(a['rca_ohm_km']) or Decimal(b['xl_ohm_km'])>Decimal(a['xl_ohm_km']):
            raise ValueError('Catálogo sem monotonicidade exigida pela política F07')
    return result

def catalog_hash():
    return digest({'catalog':catalog(),'f01_revision':cell_bindings.REVISION,'f01_source':cell_bindings.SOURCE,
                   'f01_acceptance':cell_bindings.ACCEPTANCE,'f01_cells':cell_bindings.CELLS})

def evidence(reference):
    c=catalog();s=c['source']
    return {'document':s['document'],'edition':s['edition'],'reference':reference,'sha256':s['sha256']}
