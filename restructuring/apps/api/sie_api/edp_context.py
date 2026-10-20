"""EDP context v1: partial source-based screening, never distributor approval."""
from datetime import date
from decimal import Decimal
from hashlib import sha256
import json
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
from .domain.edp import enquadrar_edp

SOURCE_SHA256 = 'b14f414001d9831f91bbef84f022c5164f367431cc6a209e5fb34b4e48f20810'
# Equipment thresholds transcribed by two source readers; pending professional review.
from importlib.resources import files
_registry_text = files('sie_api').joinpath('data/edp_context_v1.json').read_text(encoding='utf-8')
_RULES = json.loads(_registry_text)
REGISTRY_HASH = sha256(_registry_text.encode()).hexdigest()
MOTOR_LIMITS = _RULES['motor_limits_cv_fn_ff_fff']


class ContextoEDP(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True, allow_inf_nan=False)
    uf: str
    distribuidora: str
    area_concessao_confirmada: bool
    rede: Literal['AEREA_SECUNDARIA', 'OUTRA']
    sistema: Literal['ESTRELA', 'DELTA']
    tensao_fase_neutro_v: float = Field(gt=0)
    tensao_linha_v: float = Field(gt=0)
    frequencia_hz: float = Field(gt=0)
    data_referencia: str
    isolacao_entrada: Literal['PVC', 'EPR_XLPE']
    possui_mmgd: bool
    corrente_geracao_a: float | None = Field(default=None, gt=0)
    maior_motor_fn_cv: float = Field(ge=0)
    maior_motor_ff_cv: float = Field(ge=0)
    maior_motor_fff_cv: float = Field(ge=0)
    possui_cargas_especiais: bool

    @field_validator('data_referencia')
    @classmethod
    def data_iso(cls, value):
        date.fromisoformat(value)
        return value

    @model_validator(mode='after')
    def geracao_explicita(self):
        if self.possui_mmgd != (self.corrente_geracao_a is not None):
            raise ValueError('MMGD exige corrente de geração explícita; sem MMGD não informar geração')
        return self


def enquadrar_com_contexto(modalidade, corrente_demanda_a, carga_instalada_kw, tem_carga_trifasica, contexto):
    if (not isinstance(corrente_demanda_a, Decimal) or not corrente_demanda_a.is_finite() or corrente_demanda_a<=0 or
            not isinstance(carga_instalada_kw, Decimal) or not carga_instalada_kw.is_finite() or carga_instalada_kw<=0):
        raise ValueError('Corrente e carga devem ser Decimal positivos e finitos')
    data = ContextoEDP.model_validate(contexto).model_dump(mode='json')
    current = corrente_demanda_a
    if data['possui_mmgd']:
        current = max(current, Decimal(str(data['corrente_geracao_a'])))
    result = enquadrar_edp(modalidade,current,carga_instalada_kw,tem_carga_trifasica)
    # The prior blanket prohibition is not the rule for the star row on p15.
    if data['sistema']=='ESTRELA':
        result['alertas']=[a for a in result['alertas'] if a['codigo']!='EDP-002']
    errors=[]
    if (data['uf']!='SP' or data['distribuidora']!='EDP_SP' or
            not data['area_concessao_confirmada'] or data['rede']!='AEREA_SECUNDARIA'):
        errors.append(('EDP-CONTEXTO','Território/rede fora do recorte EDP São Paulo aéreo secundário'))
    if date.fromisoformat(data['data_referencia'])<date(2026,4,14):
        errors.append(('EDP-DATA','Data anterior ao início do documento V09 inspecionado'))
    nominal=_RULES['nominal_voltages'][data['sistema']]
    if ((Decimal(str(data['tensao_fase_neutro_v'])),Decimal(str(data['tensao_linha_v'])))!=
            tuple(Decimal(str(v)) for v in nominal) or Decimal(str(data['frequencia_hz']))!=Decimal(str(_RULES['frequency_hz']))):
        errors.append(('EDP-TENSAO','Tensão/frequência incompatível com item 5.3.1 do recorte'))
    power=carga_instalada_kw
    limits=_RULES['load_limits_kw']
    if modalidade=='U':
        applicable=power<=Decimal(str(limits['U_max']))
    elif modalidade=='D':
        applicable=Decimal(str(limits['D_min']))<power<=Decimal(str(limits['D_'+data['sistema']+'_max']))
    else:
        applicable=(Decimal(str(limits['T_'+data['sistema']+'_min']))<power<=Decimal(str(limits['T_max']))
                    and (data['sistema']=='ESTRELA' or tem_carga_trifasica))
    if not applicable:
        errors.append(('EDP-FAIXA','Fora da faixa normal da modalidade/sistema; exceções exigem análise da distribuidora'))
    if not tem_carga_trifasica and data['maior_motor_fff_cv']>0:
        errors.append(('EDP-MOTOR-DECLARACAO','Motor trifásico contradiz a declaração de cargas'))
    if data['possui_cargas_especiais']:
        errors.append(('EDP-ESPECIAIS','Cargas especiais exigem critérios específicos ainda não automatizados'))
    category=result['categoria']
    if category:
        code=category['codigo']; limits=MOTOR_LIMITS[code]
        motors=[data[k] for k in ('maior_motor_fn_cv','maior_motor_ff_cv','maior_motor_fff_cv')]
        if any(Decimal(str(m))>Decimal(str(limit)) for m,limit in zip(motors,limits)):
            errors.append(('EDP-MOTORES','Potência de motor excede o limite da categoria candidata'))
        if data['isolacao_entrada']=='EPR_XLPE' and code in ('T7','T9'):
            errors.append(('EDP-CONFLITO-FONTE','Tabela 002 e exemplo p52 têm orientações distintas de proteção/aterramento EPR; esclarecer antes de dimensionar'))
    result['alertas'] += [{'codigo':k,'nivel':'BLOQUEANTE','mensagem':v} for k,v in errors]
    result['candidato_para_estudo']=not result['alertas'] and category is not None
    result['status_engenharia']='PENDENTE' if result['candidato_para_estudo'] else 'BLOQUEADO'
    if errors:
        result['categoria']=None
    snapshot={'versao_modelo':'EDP_CONTEXT_V1','registro_sha256':REGISTRY_HASH,
              'entrada_efetiva':{'modalidade':modalidade,'carga_instalada_kw':str(carga_instalada_kw),
                                'tem_carga_trifasica':tem_carga_trifasica},'condicoes_declaradas':data,
              'fonte_local_sha256':SOURCE_SHA256,'conferencia':'DUAS_LEITURAS_IA_PENDENTE_ACEITE',
              'corrente_carga_a':str(corrente_demanda_a),'corrente_selecao_a':str(current),
              'criterio_mmgd':'maior corrente entre geração e carga',
              'inicio_documento':'2026-04-14','fim_documento':'CONDICIONADO',
              'identidade_binaria_com_publicacao_remota_verificada':False,
              'demanda_por_grupos_verificada':False,'vigencia_caso_verificada':False,
              'liberacao_normativa':False}
    snapshot['snapshot_sha256']=sha256(json.dumps(snapshot,sort_keys=True,ensure_ascii=False,
                                    separators=(',',':'),allow_nan=False).encode()).hexdigest()
    result['contexto_aplicado']=snapshot
    result['liberado_para_padrao_entrada']=False
    return result
