"""Versioned SIE schematic symbols; no normative certification is asserted."""
from html import escape
from .representation_f10 import ArtifactError, _finite_number

CATALOG_VERSION = 'SIE_F10_SYMBOLS_V1'
_ORIGIN = 'SIE schematic drawing convention; not an ABNT normative symbol catalogue'
_LICENSE = {'status': 'INTERNAL_ORIGINAL_NO_EXTERNAL_LICENSE_CLAIM',
            'source_reference': 'sie_api/symbols_f10.py',
            'license_reference': 'Internal original SIE shapes; no repository license grant was found; no third-party license asserted'}
_SHAPES = {
    'panel': ('Quadro', '<rect x="-8" y="-10" width="16" height="20" fill="white" stroke="currentColor"/>'),
    'load': ('Carga', '<circle r="7" fill="white" stroke="currentColor"/><path d="M-5 -5L5 5M-5 5L5 -5" stroke="currentColor"/>'),
    'protection': ('Proteção', '<rect x="-5" y="-10" width="10" height="20" fill="white" stroke="currentColor"/><path d="M-5 5L5 -5" stroke="currentColor"/>'),
    'switch': ('Comando', '<path d="M0 10V3L7 -7M0 -10V-7" fill="none" stroke="currentColor"/>'),
    'junction': ('Junção', '<circle r="4" fill="currentColor"/>'),
    'supply': ('Alimentação', '<path d="M0 -10L9 7H-9Z" fill="white" stroke="currentColor"/>'),
}

def symbol_catalog():
    return {'version': CATALOG_VERSION, 'origin': _ORIGIN, 'license': dict(_LICENSE),
            'symbols': [{'id': key, 'version': CATALOG_VERSION, 'label': val[0], 'origin': _ORIGIN, 'license': dict(_LICENSE)}
                        for key, val in _SHAPES.items()]}

def render_symbol(symbol_id, x, y, label=''):
    if symbol_id not in _SHAPES:
        raise ArtifactError(f'unknown symbol: {symbol_id}')
    x, y = _finite_number(x, 'symbol.x'), _finite_number(y, 'symbol.y')
    return (f'<g transform="translate({x:g} {y:g})" data-symbol-id="{symbol_id}" '
            f'data-symbol-version="{CATALOG_VERSION}" aria-label="{escape(str(label), quote=True)}">'
            f'{_SHAPES[symbol_id][1]}<text x="12" y="-8" font-size="12">{escape(str(label))}</text></g>')

def render_legend(symbol_ids):
    ids = sorted(set(symbol_ids))
    if any(key not in _SHAPES for key in ids):
        raise ArtifactError('legend contains unknown symbol')
    return {'version': CATALOG_VERSION, 'origin': _ORIGIN, 'license': dict(_LICENSE),
            'items': [{'symbol_id': key, 'label': _SHAPES[key][0]} for key in ids]}
