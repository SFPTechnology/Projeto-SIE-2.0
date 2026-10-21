"""Registro imutável do aceite LIMITADO do lote 01; não homologa o motor."""
from decimal import Decimal
from hashlib import sha256
import json

# Versioned data is packaged separately from the calculation implementation.
# Keep this v1 resource/resolver when adding later revisions; never replace it.
from importlib.resources import files

_registry = json.loads(files('sie_api').joinpath('data/f01_lote01_cells_v1.json').read_text(encoding='utf-8'))
REVISION = _registry['registro_revisao']
SOURCE = _registry['fonte_sha256_declarada_rt']
ACCEPTANCE = _registry['aceite_sha256']
CELLS = tuple((c['id'], c['tabela'], c['linha'], c['valor'], c['isolacao'])
              for c in _registry['celulas'])
del _registry


def _canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False)


def resolver_vinculo(payload):
    """Validate all candidate cells and derive values on the server, fail closed."""
    binding = payload.get('vinculo_celulas')
    if binding is None:
        return payload, None
    # Apply the same strict contract to direct Python/CLI callers as HTTP callers.
    from .analysis_contracts import VinculoCelulas
    binding = VinculoCelulas.model_validate(binding).model_dump(mode='json')
    if binding['registro_revisao'] != REVISION:
        raise ValueError('Revisão de células desconhecida')
    ctx = binding['condicoes']
    if (ctx['material'] != 'Cu' or ctx['isolacao'] != 'PVC' or
        ctx['temperatura_condutor_c'] != 70 or ctx['metodo_referencia'] != 'B1' or
        ctx['condutores_carregados'] != 2 or ctx['meio'] != 'AR' or
        ctx['metodo_instalacao'] not in (3, 5, 7) or ctx['radiacao_solar'] or
        ctx['radiacao_infravermelha'] or
        ctx['temperatura_ambiente_c'] not in (30, 40)):
        raise ValueError('Condições fora do escopo das células de capacidade do lote 01')
    circuits = ctx['circuitos_agrupados']
    if circuits not in (1, 2, 3):
        raise ValueError('Agrupamento fora do escopo do lote 01')
    if circuits > 1 and (ctx['agrupamento'] != 'FEIXE' or
                        not ctx['grupo_homogeneo'] or not ctx['carga_uniforme']):
        raise ValueError('Células de agrupamento exigem feixe homogêneo uniformemente carregado')
    if circuits == 1 and ctx['agrupamento'] != 'ISOLADO':
        raise ValueError('Circuito único deve declarar instalação isolada')
    ids = binding['celulas_ids']
    if len(ids) != len(set(ids)):
        raise ValueError('IDs de células duplicados')
    expected = ['CEL-01', 'CEL-02', 'CEL-03', 'CEL-04']
    factor = Decimal('1')
    if ctx['temperatura_ambiente_c'] == 40:
        expected.append('CEL-05')
        factor *= Decimal('.87')
    if circuits > 1:
        expected.append('CEL-07' if circuits == 2 else 'CEL-08')
        factor *= Decimal('.80' if circuits == 2 else '.70')
    if set(ids) != set(expected):
        raise ValueError('IDs ausentes, extras ou incompatíveis com as condições (XLPE não combina com PVC)')
    table = [{'secao_mm2': float(section), 'capacidade_a': float(value)}
             for _, tab, section, value, _ in CELLS if tab == '36']
    received = sorted((Decimal(str(r['secao_mm2'])), Decimal(str(r['capacidade_a'])))
                      for r in payload['tabela_condutores'])
    server = [(Decimal(str(r['secao_mm2'])), Decimal(str(r['capacidade_a']))) for r in table]
    if received != server or Decimal(str(payload['fator_correcao'])) != factor:
        raise ValueError('Tabela ou fator diverge das células registradas no servidor')
    cells = [{'id': cid, 'tabela': tab, 'linha': line, 'valor': value, 'isolacao': insulation}
             for cid, tab, line, value, insulation in CELLS if cid in expected]
    snapshot = {'registro_revisao': REVISION, 'fonte_sha256_declarada_rt': SOURCE,
                'registro_sha256': sha256(_canonical(CELLS).encode()).hexdigest(),
                'aceite_sha256': ACCEPTANCE, 'escopo': 'ACEITE_LIMITADO_LOTE01',
                'condicoes': ctx, 'celulas': cells, 'fator_derivado': str(factor),
                'equivalencia_com_exemplar_anterior_verificada': False,
                'liberacao_normativa': False}
    snapshot['snapshot_sha256'] = sha256(_canonical(snapshot).encode()).hexdigest()
    return {**payload, 'tabela_condutores': table, 'fator_correcao': float(factor)}, snapshot
