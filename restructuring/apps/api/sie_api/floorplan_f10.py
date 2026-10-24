"""Safe SVG base import, calibrated geometry and explicit versioned placements.

The retained original is evidence, never rendered as active arbitrary XML. Only a
small SVG geometry subset is accepted. Lengths are checked, never synthesized.
"""
from __future__ import annotations
import argparse
import base64
from copy import deepcopy
from datetime import datetime
from hashlib import sha256
from html import escape
import json
import math
from pathlib import Path
import re
from xml.etree import ElementTree as ET
from .representation_f10 import ArtifactContract, ArtifactError, _check_contract, _finite_number
from .symbols_f10 import CATALOG_VERSION, render_legend, render_symbol, symbol_catalog

MAX_ASSET_BYTES = 2 * 1024 * 1024
SCHEMA_VERSION = 'SIE_FLOOR_PLAN_V1'
_ALLOWED = {'svg', 'g', 'path', 'rect', 'line', 'polyline', 'polygon', 'circle', 'ellipse', 'title', 'desc'}
_ATTRS = {'viewBox','width','height','x','y','x1','y1','x2','y2','cx','cy','r','rx','ry','d','points','fill','stroke','stroke-width','transform','opacity','fill-rule'}


def _canonical(value):
    try:
        return json.dumps(value, ensure_ascii=False, allow_nan=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
    except (ValueError, TypeError) as exc:
        raise ArtifactError('floor plan must contain canonical finite JSON') from exc


def _text(value, field):
    if not isinstance(value, str) or not value.strip() or len(value) > 1000:
        raise ArtifactError(f'{field} is required and bounded')
    return value.strip()


def import_svg_asset(data: bytes, source_ref: str, authorization_reference: str) -> dict:
    """Import actual original SVG bytes, rejecting scripts, references and CSS."""
    if not isinstance(data, bytes) or not 0 < len(data) <= MAX_ASSET_BYTES:
        raise ArtifactError('SVG asset empty or exceeds 2 MiB')
    source_ref = _text(source_ref, 'source_ref')
    authorization_reference = _text(authorization_reference, 'authorization_reference')
    if re.search(br'<!DOCTYPE|<!ENTITY|<\?xml-stylesheet', data, re.I):
        raise ArtifactError('DTD/entities/stylesheets are forbidden')
    try:
        root = ET.fromstring(data)
    except ET.ParseError as exc:
        raise ArtifactError('malformed SVG asset') from exc
    if root.tag not in {'svg', '{http://www.w3.org/2000/svg}svg'}:
        raise ArtifactError('asset MIME is not SVG')
    nodes = list(root.iter())
    if len(nodes) > 10000:
        raise ArtifactError('SVG exceeds geometry element limit')
    for node in nodes:
        tag = node.tag.split('}')[-1]
        if tag not in _ALLOWED or (node.tag.startswith('{') and not node.tag.startswith('{http://www.w3.org/2000/svg}')):
            raise ArtifactError(f'unsupported SVG element: {tag}')
        for key, value in node.attrib.items():
            if key not in _ATTRS or re.search(r'url\s*\(|javascript:|data:|https?:|[<>\\]|//', value, re.I):
                raise ArtifactError(f'unsafe SVG attribute: {key}')
            if key in {'fill', 'stroke'} and not re.fullmatch(
                    r'(?:none|currentColor|transparent|black|white|red|green|blue|gray|grey|yellow|orange|purple|#[0-9a-fA-F]{3}|#[0-9a-fA-F]{6}|#[0-9a-fA-F]{8})', value):
                raise ArtifactError('SVG paint must be a simple approved color; references are forbidden')
            if len(value) > 100000 or re.search(r'\b(?:nan|inf(?:inity)?)\b', value, re.I):
                raise ArtifactError('invalid SVG geometry value')
        node.tag = tag
    viewbox = root.get('viewBox', '').replace(',', ' ').split()
    try:
        values = [float(value) for value in viewbox]
    except ValueError as exc:
        raise ArtifactError('SVG requires numeric viewBox') from exc
    if len(values) != 4 or not all(math.isfinite(v) for v in values) or values[:2] != [0, 0] or min(values[2:]) <= 0:
        raise ArtifactError('SVG requires finite viewBox starting at 0 0')
    root.set('xmlns', 'http://www.w3.org/2000/svg')
    return {'mime': 'image/svg+xml', 'sha256': sha256(data).hexdigest(),
            'original_base64': base64.b64encode(data).decode('ascii'),
            'sanitized_svg': ET.tostring(root, encoding='unicode'),
            'width': values[2], 'height': values[3], 'source_ref': source_ref,
            'authorization_reference': authorization_reference}


def _asset(raw):
    if not isinstance(raw, dict):
        raise ArtifactError('floor plan requires imported SVG asset')
    try:
        data = base64.b64decode(raw.get('original_base64', ''), validate=True)
    except (ValueError, TypeError) as exc:
        raise ArtifactError('invalid original asset encoding') from exc
    actual = import_svg_asset(data, raw.get('source_ref'), raw.get('authorization_reference'))
    if raw != actual:
        raise ArtifactError('asset hash/MIME/geometry does not match original bytes')
    return actual


def import_floor_plan(raw: dict, snapshot: dict, contract: ArtifactContract) -> dict:
    _check_contract(snapshot, contract)
    if not isinstance(raw, dict) or raw.get('schema_version') != SCHEMA_VERSION:
        raise ArtifactError('unsupported floor plan schema')
    plan = deepcopy(raw)
    _canonical(plan)
    for key in ('id', 'revision_id', 'source_ref', 'authorization_reference'):
        plan[key] = _text(plan.get(key), f'floor_plan.{key}')
    if plan['revision_id'] != contract.revision_id:
        raise ArtifactError('floor plan revision mismatch')
    if type(plan.get('geometry_revision')) is not int or plan['geometry_revision'] < 1:
        raise ArtifactError('geometry_revision requires positive integer')
    if plan.get('units') not in {'m', 'cm', 'mm'}:
        raise ArtifactError('unsupported floor plan unit')
    for key in ('width','height','model_units_per_canvas_unit'):
        if _finite_number(plan.get(key), key) <= 0:
            raise ArtifactError(f'{key} must be positive')
    asset = _asset(plan.get('asset'))
    if any(plan[key] != asset[key] for key in ('source_ref','authorization_reference','width','height')):
        raise ArtifactError('floor plan differs from imported base')
    cal = plan.get('calibration')
    if not isinstance(cal, dict):
        raise ArtifactError('calibration is required')
    for key in ('canvas_distance','model_distance'):
        if _finite_number(cal.get(key), key) <= 0:
            raise ArtifactError('calibration distances must be positive')
    tolerance = _finite_number(cal.get('relative_tolerance'), 'relative_tolerance')
    if not 0 <= tolerance <= .01:
        raise ArtifactError('relative_tolerance must be between zero and 0.01')
    _text(cal.get('confirmed_by'), 'calibration.confirmed_by')
    try:
        timestamp = datetime.fromisoformat(_text(cal.get('confirmed_at'), 'calibration.confirmed_at').replace('Z','+00:00'))
        if timestamp.tzinfo is None:
            raise ValueError('timezone missing')
    except ValueError as exc:
        raise ArtifactError('calibration confirmation requires ISO timestamp with timezone') from exc
    expected_scale = cal['model_distance'] / cal['canvas_distance']
    if not math.isclose(plan['model_units_per_canvas_unit'], expected_scale, rel_tol=tolerance, abs_tol=1e-12):
        raise ArtifactError('calibration inconsistent with scale')
    def point(point):
        if not isinstance(point, list) or len(point) != 2:
            raise ArtifactError('geometry requires [x,y] points')
        x, y = (_finite_number(point[i], 'coordinate') for i in range(2))
        if not 0 <= x <= plan['width'] or not 0 <= y <= plan['height']:
            raise ArtifactError('geometry outside plan bounds')
        return x, y
    ids = set()
    segments = {item['id']: item for item in snapshot.get('segments', [])}
    for group in ('walls', 'paths'):
        items = plan.get(group)
        if not isinstance(items, list) or len(items) > 10000:
            raise ArtifactError(f'{group} must be bounded list')
        for item in items:
            if not isinstance(item, dict):
                raise ArtifactError('geometry item must be object')
            identity = _text(item.get('id'), 'geometry.id')
            if identity in ids:
                raise ArtifactError('duplicate geometry id')
            ids.add(identity)
            points = item.get('points')
            if not isinstance(points, list) or not 2 <= len(points) <= 10000:
                raise ArtifactError('polyline requires bounded point list')
            coords = [point(p) for p in points]
            if group == 'paths' and 'segment_id' in item:
                segment = segments.get(item['segment_id'])
                if segment is None:
                    raise ArtifactError('path references unknown segment')
                length = sum(math.dist(a,b) for a,b in zip(coords,coords[1:]))
                length *= plan['model_units_per_canvas_unit'] * {'m':1,'cm':.01,'mm':.001}[plan['units']]
                declared = _finite_number(segment.get('length_m'), 'segment.length_m')
                if not math.isclose(length, declared, rel_tol=tolerance, abs_tol=1e-9):
                    raise ArtifactError('path geometry differs from authoritative segment length')
    placements = plan.get('placements')
    if not isinstance(placements, list) or len(placements) > 10000:
        raise ArtifactError('placements must be bounded list')
    known = {item['id'] for item in snapshot['elements']}
    used = set()
    catalog = {item['id'] for item in symbol_catalog()['symbols']}
    for item in placements:
        if not isinstance(item, dict) or item.get('element_id') not in known or item['element_id'] in used:
            raise ArtifactError('placement references unknown or repeated element')
        used.add(item['element_id'])
        point([item.get('x'), item.get('y')])
        if item.get('symbol_id') not in catalog:
            raise ArtifactError('placement requires catalog symbol')
        _text(item.get('label', item['element_id']), 'placement.label')
    fingerprint = {key: value for key,value in plan.items() if key != 'source_sha256'}
    digest = sha256(_canonical(fingerprint)).hexdigest()
    if 'source_sha256' in raw and raw['source_sha256'] != digest:
        raise ArtifactError('floor plan geometry fingerprint mismatch')
    plan['source_sha256'] = digest
    return plan


def validate_floor_plan(snapshot, contract):
    return import_floor_plan(snapshot.get('floor_plan'), snapshot, contract)


def render_floor_plan_svg(snapshot, contract):
    plan = validate_floor_plan(snapshot, contract)
    base_root = ET.fromstring(plan['asset']['sanitized_svg'])
    base_root.set('width', str(plan['width']))
    base_root.set('height', str(plan['height']))
    base_svg = ET.tostring(base_root, encoding='unicode')
    legend = render_legend(item['symbol_id'] for item in plan['placements'])
    drawing_height = plan['height'] + 38 + 24 * len(legend['items'])
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="plan-title plan-desc" viewBox="0 0 {max(plan["width"], 360):g} {drawing_height:g}">',
             f'<title id="plan-title">Planta {escape(plan["id"])}</title>',
             f'<desc id="plan-desc">Origem {escape(plan["source_ref"])}. Escala confirmada por {escape(plan["calibration"]["confirmed_by"])}. Unidade {plan["units"]}. Símbolos {CATALOG_VERSION}; não é homologação normativa.</desc>',
             '<g data-layer="base">', base_svg, '</g>']
    for group in ('walls','paths'):
        parts.append(f'<g data-layer="{group}" fill="none" stroke="{("#334155" if group == "walls" else "#155eef")}">')
        for item in plan[group]:
            points = ' '.join(f'{p[0]:g},{p[1]:g}' for p in item['points'])
            parts.append(f'<polyline data-geometry-id="{escape(item["id"],quote=True)}" points="{points}"/>')
        parts.append('</g>')
    parts.append('<g data-layer="placements" color="#172033">')
    for item in plan['placements']:
        parts.append(f'<g data-element-id="{escape(item["element_id"],quote=True)}">'+render_symbol(item['symbol_id'], item['x'], item['y'], item.get('label',item['element_id']))+'</g>')
    parts.append('</g>')
    parts.append(f'<g data-layer="legend"><text x="8" y="{plan["height"] + 18:g}" font-size="12">Legenda — {CATALOG_VERSION}</text>')
    for index, item in enumerate(legend['items']):
        parts.append(render_symbol(item['symbol_id'], 18, plan['height'] + 38 + index * 24, item['label']))
    parts.append('</g>')
    parts.append(f'<metadata>{escape(json.dumps({"source_sha256":plan["source_sha256"], "legend":legend},ensure_ascii=False,sort_keys=True))}</metadata></svg>')
    return ''.join(parts)


class PlanHistory:
    """Local explicit edits; undo/redo never mutate the originally saved plan."""
    def __init__(self, plan):
        self.current, self._undo, self._redo = deepcopy(plan), [], []
    def apply(self, plan):
        self._undo.append(deepcopy(self.current)); self._redo.clear()
        self.current = deepcopy(plan)
        self.current['geometry_revision'] = self._undo[-1]['geometry_revision'] + 1
        self.current.pop('source_sha256', None)
        return deepcopy(self.current)
    def undo(self):
        if not self._undo:
            raise ArtifactError('no geometry edit to undo')
        self._redo.append(deepcopy(self.current)); self.current = self._undo.pop()
        return deepcopy(self.current)
    def redo(self):
        if not self._redo:
            raise ArtifactError('no geometry edit to redo')
        self._undo.append(deepcopy(self.current)); self.current = self._redo.pop()
        return deepcopy(self.current)


def main(argv=None):
    parser = argparse.ArgumentParser(description='Import a safe SVG original and render a calibrated SIE floor plan')
    parser.add_argument('--input', required=True, help='JSON with snapshot and artifact_contract')
    parser.add_argument('--svg', required=True, help='Original SVG base; never remote URL')
    parser.add_argument('--output', required=True, help='New normalized floor plan JSON')
    args = parser.parse_args(argv)
    data = json.loads(Path(args.input).read_text(encoding='utf-8'))
    snapshot = data['snapshot']; contract = ArtifactContract(**data['artifact_contract'])
    raw = deepcopy(snapshot['floor_plan'])
    raw['asset'] = import_svg_asset(Path(args.svg).read_bytes(), raw['source_ref'], raw['authorization_reference'])
    normalized = import_floor_plan(raw, snapshot, contract)
    target = Path(args.output)
    with target.open('x', encoding='utf-8') as output:
        json.dump(normalized, output, ensure_ascii=False, allow_nan=False, sort_keys=True)
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
