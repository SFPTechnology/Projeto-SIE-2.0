"""P04: modelo longitudinal de queda AC, sem substituir dados de fabricante.

Rca(theta) e XL são entradas explícitas para a seção, frequência e arranjo
indicados. Não há conversão automática de Rdc, temperatura ou unidades. Fórmula
aproximada de regime permanente: Schneider Electric, Electrical Installation
Guide, Calculation of voltage drop in steady load conditions, Fig. G29
(consultada em 20/10/2026). Não atribuir esta fórmula ao item 6.2.7 da NBR 5410.
"""
from decimal import Decimal, localcontext
from math import isfinite
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator, field_validator

MODEL_REFERENCE = 'https://www.electrical-installation.org/enwiki/Calculation_of_voltage_drop_in_steady_load_conditions'


class FonteParametroQueda(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True, allow_inf_nan=False)
    documento: str = Field(min_length=1, max_length=500)
    revisao: str = Field(min_length=1, max_length=100)
    referencia: str = Field(min_length=1, max_length=500)
    sha256: str = Field(pattern=r'^[0-9a-f]{64}$')

    @field_validator('documento', 'revisao', 'referencia')
    @classmethod
    def texto_nao_vazio(cls, value):
        if not value.strip():
            raise ValueError('Fonte do parâmetro de queda não pode ser vazia')
        return value.strip()


class QuedaImpedancia(BaseModel):
    """Todos os valores são declarados; min_length não autentica documento."""
    model_config = ConfigDict(extra='forbid', strict=True, allow_inf_nan=False)
    tipo_circuito: Literal['MONOFASICO_FASE_NEUTRO', 'MONOFASICO_FASE_FASE', 'TRIFASICO_EQUILIBRADO']
    regime: Literal['SENOIDAL_PERMANENTE']
    harmonicas_relevantes: bool
    secao_mm2: float = Field(gt=0)
    material: Literal['Cu', 'Al']
    isolacao: str = Field(min_length=1, max_length=100)
    temperatura_condutor_c: float = Field(gt=-273.15)
    frequencia_hz: float = Field(gt=0)
    arranjo: str = Field(min_length=1, max_length=500)
    rca_ohm_km: float = Field(gt=0)
    xl_ohm_km: float = Field(ge=0)
    fator_potencia: float = Field(gt=0, le=1)
    natureza_carga: Literal['INDUTIVA', 'RESISTIVA']
    fonte_rca: FonteParametroQueda
    fonte_xl: FonteParametroQueda
    limite_queda_percentual: float | None = Field(default=None, gt=0, le=100)
    fonte_limite: FonteParametroQueda | None = None
    escopo_limite: Literal['TRECHO', 'TOTAL_DESDE_ORIGEM'] | None = None
    queda_montante_percentual: float | None = Field(default=None, ge=0)

    @field_validator('isolacao', 'arranjo')
    @classmethod
    def condicao_nao_vazia(cls, value):
        if not value.strip():
            raise ValueError('Condição do parâmetro de queda não pode ser vazia')
        return value.strip()

    @model_validator(mode='after')
    def validar_modelo_e_limite(self):
        if self.harmonicas_relevantes:
            raise ValueError('Modelo de queda senoidal não cobre harmônicas relevantes')
        if self.natureza_carga == 'RESISTIVA' and self.fator_potencia != 1:
            raise ValueError('Carga resistiva exige fator de potência igual a 1')
        has_limit = self.limite_queda_percentual is not None
        if has_limit != (self.fonte_limite is not None) or has_limit != (self.escopo_limite is not None):
            raise ValueError('Limite de queda exige fonte e escopo explícitos')
        if self.escopo_limite == 'TOTAL_DESDE_ORIGEM':
            if self.queda_montante_percentual is None:
                raise ValueError('Limite total exige queda a montante na mesma base nominal')
        elif self.queda_montante_percentual is not None:
            raise ValueError('Queda a montante só é aceita para limite total desde a origem')
        return self


def _decimal(value, name, *, zero=False):
    if isinstance(value, bool):
        raise ValueError(f'{name} deve ser numérico, positivo e finito')
    try:
        result = Decimal(str(value))
    except Exception as exc:
        raise ValueError(f'{name} inválido') from exc
    if not result.is_finite() or result < 0 or (result == 0 and not zero):
        raise ValueError(f'{name} deve ser positivo e finito')
    return result


def _number(value):
    return format(value.normalize(), 'f')


def calcular_queda_impedancia(corrente_a, comprimento_m, tensao_v, dados, *, secao_mm2=None):
    """L é comprimento de ida em metros; Rca/XL são por condutor em ohm/km.

    A corrente já é a corrente de projeto. Não aplicar cos(phi) novamente a I.
    Tensão é a nominal entre os dois condutores no monofásico (FN ou FF) e
    linha-linha no trifásico equilibrado. Ausência de dados não usa defaults.
    """
    if dados is None:
        return {'status': 'PENDENTE', 'motivo': 'Rca(theta), XL e condições não informados',
                'liberacao_normativa': False, 'fontes_parametros_verificadas': False}
    data = QuedaImpedancia.model_validate(dados).model_dump(mode='json')
    current = _decimal(corrente_a, 'Corrente de projeto')
    length = _decimal(comprimento_m, 'Comprimento de ida', zero=True)
    voltage = _decimal(tensao_v, 'Tensão nominal')
    if secao_mm2 is not None and _decimal(secao_mm2, 'Seção selecionada') != Decimal(str(data['secao_mm2'])):
        raise ValueError('Rca/XL declarados não correspondem à seção selecionada')
    with localcontext() as ctx:
        ctx.prec = 50
        rca, xl = Decimal(str(data['rca_ohm_km'])), Decimal(str(data['xl_ohm_km']))
        cos_phi = Decimal(str(data['fator_potencia']))
        sin_phi = (Decimal('1') - cos_phi * cos_phi).sqrt()
        three_phase = data['tipo_circuito'] == 'TRIFASICO_EQUILIBRADO'
        coefficient = Decimal('3').sqrt() if three_phase else Decimal('2')
        longitudinal = rca * cos_phi + xl * sin_phi
        drop = coefficient * (length / Decimal('1000')) * current * longitudinal
        percent = drop * Decimal('100') / voltage
        if not isfinite(float(drop)) or not isfinite(float(percent)):
            raise ValueError('Resultado de queda fora do intervalo numérico de saída')
        total = percent + Decimal(str(data['queda_montante_percentual'] or 0))
        compared = total if data['escopo_limite'] == 'TOTAL_DESDE_ORIGEM' else percent
        limit = data['limite_queda_percentual']
        within = None if limit is None else compared <= Decimal(str(limit))
        return {
            'status': ('CALCULADO_PARCIAL' if within is None else
                       'ATENDE_CALCULO_PARCIAL' if within else 'NAO_ATENDE_LIMITE_DECLARADO'),
            'queda_v': float(drop), 'queda_percentual': float(percent),
            'queda_decisao_v': _number(drop), 'queda_decisao_percentual': _number(percent),
            'queda_comparada_percentual': _number(compared),
            'limite_queda_percentual': None if limit is None else str(limit),
            'limite_declarado_atendido': within,
            'formula': ('sqrt(3)' if three_phase else '2') + ' × L(km) × Ib × (Rca(theta) × cos(phi) + XL × sin(phi))',
            'referencia_modelo': MODEL_REFERENCE,
            'comprimento_informado': 'IDA_EM_METROS',
            'base_tensao': 'LINHA_LINHA' if three_phase or data['tipo_circuito'] == 'MONOFASICO_FASE_FASE' else 'FASE_NEUTRO',
            'parametros_declarados': data,
            'origem_parametros': 'DECLARADA_NAO_VERIFICADA',
            'fontes_parametros_verificadas': False,
            'aplicabilidade_normativa_verificada': False,
            'modelo_aproximado': True,
            'limites_normativos_automaticos': False,
            'liberacao_normativa': False,
            'hipoteses': ['Regime permanente senoidal; carga resistiva ou indutiva',
                         'Parâmetros por condutor na frequência, temperatura e arranjo declarados',
                         'Trifásico apenas equilibrado; monofásico com ida e retorno equivalentes',
                         'Não calcula partida, harmônicas, rede a montante ou escolha automática do limite'],
        }
