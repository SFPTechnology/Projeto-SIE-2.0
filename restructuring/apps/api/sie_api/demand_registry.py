"""Server-owned EDP V09 demand bindings; source-linked != professional approval."""
from datetime import date
from decimal import Decimal
from hashlib import sha256
from importlib.resources import files
import json

_RAW = files('sie_api').joinpath('data/demand_edp_v09.json').read_bytes()
CATALOG_HASH = sha256(_RAW).hexdigest()
_CATALOG = json.loads(_RAW)

def catalog():
    return json.loads(_RAW)

def specification(rule_id):
    return _CATALOG['rules'].get(rule_id)

def rule_document(rule_id):
    spec = specification(rule_id)
    if not spec: return None
    return dict(id=rule_id,version=_CATALOG['version'],category=spec['category'],purpose='ENTRANCE',
                scope='SUPPLY',mode='WHOLE_GROUP',source=f"PT.DT.PDN.00068 V09 p{spec['page']} tabela {spec['table']}; item {spec['section']}",
                edition='09',condition='Aplicação limitada às condições do catálogo confiável do servidor',status='VERIFIED',
                bands=[dict(lower_va='0',factor='1')],utility='EDP_SP',locality='SP_EDP_CONCESSION',typology=None)

def scope_error(spec, context, supply):
    if context is None or (context.utility,context.locality,context.edition) != ('EDP_SP','SP_EDP_CONCESSION','09') or not context.concession_confirmed:
        return 'UTILITY_SCOPE_MISMATCH'
    if context.consumer_unit != 'INDIVIDUAL': return 'CONSUMER_UNIT_SCOPE_MISMATCH'
    if context.reference_date is None or context.reference_date < date.fromisoformat(_CATALOG['source']['valid_from']) or context.reference_date > date.fromisoformat(_CATALOG['source']['checked_at']):
        return 'EDITION_DATE_NOT_VERIFIED'
    if context.typology not in spec.get('typologies',['RESIDENTIAL','COMMERCIAL']): return 'TYPOLOGY_MISMATCH'
    if spec.get('activity') and context.activity != spec['activity']: return 'ACTIVITY_MISMATCH'
    if supply.frequency_hz != 60: return 'SUPPLY_FREQUENCY_MISMATCH'
    if supply.voltage_ff is None or supply.voltage_ff.value not in (220,240): return 'SUPPLY_VOLTAGE_MISMATCH'
    expected_fn = 127 if supply.voltage_ff.value == 220 else 120
    if supply.voltage_fn is not None and supply.voltage_fn.value != expected_fn: return 'SUPPLY_VOLTAGE_MISMATCH'
    return None

def factors(spec, ids, assignments, powers):
    """Return per-load factors and audit; all choices/conditions remain explicit."""
    items = [assignments[key] for key in ids]
    for key,a in zip(ids,items):
        if a.equipment_kind not in spec['equipment_kinds']: raise ValueError('EQUIPMENT_KIND_MISMATCH')
        if a.quantity is None: raise ValueError('EQUIPMENT_COUNT_PENDING')
        if not a.minimum_load_confirmed or not a.power_factor_confirmed or a.zone is None:
            raise ValueError('APPLICATION_CONDITIONS_PENDING')
        if any(powers[key][field] is None for field in ('p_w','s_va')): raise ValueError('POWER_BASIS_PENDING')
    # Source item b/c/e specifies unity power factor; it is checked, not invented.
    if spec['category'] in ('EDP_B','EDP_C','EDP_E'):
        if any(abs(powers[k]['p_w']-powers[k]['s_va'])>Decimal('0.01') for k in ids):
            raise ValueError('SOURCE_POWER_FACTOR_MISMATCH')
    if spec['category']=='EDP_H' and any(a.simultaneous_start_group for a in items): raise ValueError('START_GROUP_NOT_APPLICABLE_TO_SPECIAL_EQUIPMENT')
    if spec['category']=='EDP_H' and len({a.equipment_subtype for a in items})!=1:
        raise ValueError('SPECIAL_EQUIPMENT_TYPES_MUST_BE_SEPARATE')
    if spec['category']=='EDP_H' and not items[0].equipment_subtype: raise ValueError('EQUIPMENT_SUBTYPE_PENDING')
    exempt = set()
    if spec['table']=='006': exempt={k for k in ids if assignments[k].zone=='KITCHEN'}
    if spec['table']=='007':
        water={k for k in ids if assignments[k].zone=='LOCKER_ROOM' and assignments[k].equipment_kind!='IRON'}
        if water and len(water)!=len(ids): raise ValueError('MIXED_LOCKER_EXCEPTION_REQUIRES_REVIEW')
        exempt=water
    if spec['table']=='012':
        if any(assignments[k].central_air_conditioning is None for k in ids): raise ValueError('CENTRAL_AC_DECLARATION_PENDING')
        exempt={k for k in ids if assignments[k].central_air_conditioning}
    normal=[k for k in ids if k not in exempt]
    result={k:Decimal(1) for k in exempt}
    if not normal: return result,{'exception':'ALL_EXEMPT_100_PERCENT','basis':None}
    mode=spec['mode']
    active=sum((powers[k]['p_w'] for k in normal),Decimal(0))
    count=sum(assignments[k].quantity for k in normal)
    basis=active if mode in ('ACTIVE_W','PROGRESSIVE_ACTIVE_W') else Decimal(count)
    if mode=='MAXIMUM_PLUS_REST':
        if spec['table']=='013' and any(not assignments[k].coincident_start_confirmed for k in normal): raise ValueError('COINCIDENT_STARTS_PENDING')
        # Explicitly sized/ranked input; never guess CV/HP-to-VA or mechanical efficiency.
        if any(assignments[k].ranking_power_w is None for k in normal): raise ValueError('RANKING_POWER_PENDING')
        terms={}
        for k in normal:
            a=assignments[k]
            for n in range(a.quantity):
                group='declared:'+a.simultaneous_start_group if a.simultaneous_start_group else 'individual:'+str(k)+':'+str(n)
                terms.setdefault(group,[]).append((k,a.ranking_power_w))
        maximum=max(terms,key=lambda g:(sum(v for _,v in terms[g]),sum(powers[k]['s_va']/assignments[k].quantity for k,_ in terms[g])))
        rest=Decimal(spec['rest_factor'])
        weights={k:Decimal(0) for k in normal}
        for group,parts in terms.items():
            for k,_ in parts: weights[k]+=Decimal(1) if group==maximum else rest
        result.update({k:weights[k]/assignments[k].quantity for k in normal})
        return result,{'basis':'EXPLICIT_UNIT_RANKING_W','maximum_group':maximum,'rest_factor':str(rest),'equal_ranking_tie_policy':'MAX_APPARENT_POWER_CONSERVATIVE'}
    if mode=='PROGRESSIVE_ACTIVE_W':
        previous=Decimal(0); demanded=Decimal(0)
        for upper,factor in spec['rows']:
            end=min(active,Decimal(upper)) if upper is not None else active
            demanded+=max(Decimal(0),end-previous)*Decimal(factor)
            if upper is not None: previous=Decimal(upper)
        factor=demanded/active if active else Decimal(spec['rows'][0][1])
    else:
        factor=next(Decimal(f) for upper,f in spec['rows'] if upper is None or basis<=Decimal(upper))
    result.update({k:factor for k in normal})
    return result,{'basis':'ACTIVE_W' if mode in ('ACTIVE_W','PROGRESSIVE_ACTIVE_W') else 'EQUIPMENT_COUNT',
                   'value':str(basis),'boundary':'UPPER_INCLUSIVE','excluded_load_ids':list(map(str,exempt))}
