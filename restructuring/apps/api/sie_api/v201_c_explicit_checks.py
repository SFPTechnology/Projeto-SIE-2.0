"""C05 complementary engineering arithmetic, explicit data only, NOT a normative check."""
from decimal import Decimal, InvalidOperation, localcontext
from .domain.engines import selecionar_condutor, selecionar_disjuntor

def d(value, label, zero=False):
    if isinstance(value,bool):
        raise ValueError(label)
    try:
        n=Decimal(str(value))
    except (InvalidOperation,ValueError,TypeError):
        raise ValueError(label) from None
    if not n.is_finite() or (n<0 if zero else n<=0) or n>=Decimal("1e9"):
        raise ValueError(label)
    return n

def analyze_explicit(va,voltage,phase,technical):
    """Pure calculation. Input values are NOT inferred from missing DB fields."""
    if type(technical) is not dict:
        raise ValueError("technical mapping required")
    allowed={"correction_factor","cable_catalog","selected_mm2","breaker_a",
             "length_m","resistance_ohm_km","reactance_ohm_km","power_factor",
             "phase_label","demand_factor"}
    if set(technical)-allowed or phase not in ("SINGLE","THREE"):
        raise ValueError("unrecognized input/phase")
    with localcontext() as ctx:
        ctx.prec=60
        s,v=d(va,"VA"),d(voltage,"V")
        ib=s/(v if phase=="SINGLE" else Decimal("3").sqrt()*v)
        result={"apparent_power_va":str(s),"design_current_a":str(ib),
                "phase":phase,"normative_status":"EVIDENCE_PENDING",
                "liberado_para_uso_normativo":False}
        pending=[]
        if phase=="SINGLE" and technical.get("phase_label") not in ("A","B","C"):
            pending.append("PHASE_ASSIGNMENT_REQUIRED")
        if phase=="THREE" and technical.get("phase_label") is not None:
            raise ValueError("three phase cannot be assigned to one phase")
        demand=technical.get("demand_factor")
        if demand is None:
            pending.append("DEMAND_FACTOR_UNVERIFIED")
        else:
            factor=d(demand,"demand_factor")
            if factor>1: raise ValueError("demand_factor")
            result["demand_va"]=str(s*factor)
        table=technical.get("cable_catalog")
        correction=technical.get("correction_factor")
        chosen=technical.get("selected_mm2")
        breaker=technical.get("breaker_a")
        if None in (table,correction,chosen,breaker):
            pending.append("CABLE_AMPACITY_BREAKER_INPUTS_MISSING")
        else:
            if not isinstance(table,(tuple,list)) or not table or len(table)>100:
                raise ValueError("cable_catalog")
            entries=tuple((d(x,"section"),d(y,"ampacity")) for x,y in table)
            factor=d(correction,"correction_factor")
            if factor>1:raise ValueError("correction_factor")
            min_cable=selecionar_condutor(ib,factor,entries)
            selected=d(chosen,"selected_mm2")
            by_section=dict(entries)
            if len(by_section)!=len(entries) or selected not in by_section:
                raise ValueError("selected section not from catalog")
            iz=by_section[selected]*factor
            nom=d(breaker,"breaker_a")
            result["conductor"]={"selected_mm2":str(selected),
                "minimum_mm2":str(min_cable.secao_mm2),
                "corrected_ampacity_a":str(iz)}
            result["overcurrent"]={"ib_le_in_le_iz":ib<=nom<=iz,
                "short_circuit_i2":"REVIEW_REQUIRED"}
            if not result["overcurrent"]["ib_le_in_le_iz"]:
                pending.append("OVERLOAD_INEQUALITY_FAILED")
        keys=("length_m","resistance_ohm_km","reactance_ohm_km","power_factor")
        if any(technical.get(k) is None for k in keys):
            pending.append("RX_LENGTH_PF_UNVERIFIED")
        else:
            length=d(technical["length_m"],"length_m",zero=True)
            r=d(technical["resistance_ohm_km"],"R",zero=True)
            x=d(technical["reactance_ohm_km"],"X",zero=True)
            pf=d(technical["power_factor"],"PF")
            if pf>1:raise ValueError("power_factor")
            scalar=Decimal(2) if phase=="SINGLE" else Decimal(3).sqrt()
            delta=scalar*(length/1000)*ib*(r*pf+x*(1-pf*pf).sqrt())
            result["voltage_drop"]={"drop_v":str(delta),"percent":str(delta*100/v),
                "assumption":"explicit R/X, balanced three-phase when THREE"}
            pending.append("VOLTAGE_DROP_NORMATIVE_LIMIT_UNVERIFIED")
        pending.extend(("DR_DPS_EARTHING_UNVERIFIED",
                        "SHORT_CIRCUIT_AND_I2_UNVERIFIED","APPLICATION_CONDITIONS_UNVERIFIED"))
        result["pending"]=sorted(set(pending))
        result["mathematical_status"]="REVIEW_REQUIRED" if "OVERLOAD_INEQUALITY_FAILED" in pending else "PARTIAL"
        return result
