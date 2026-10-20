"""P03: verificações condicionais de curto e estudo de coordenação declarado.

Fonte inspecionada: NBR 5410:2004 corrigida 2008, exemplar 45f246e3…aa3d,
5.3.5.5.1/2, 5.3.6, 6.3.4.3 e 6.3.6. Não é o exemplar e1c02… do
aceite do lote 01. Nenhum parâmetro de fabricante ou k é presumido aqui.
Fontes de entrada são declarações, não documentos autenticados pelo servidor.
"""
from decimal import Decimal, localcontext
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

FONTE_REGRA_SHA256 = '45f246e3e33db1bf18dd60743ac93b6ac1ec0796742e169a8014682bfb19aa3d'


class FonteProtecao(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True, allow_inf_nan=False)
    documento: str = Field(min_length=1, max_length=500)
    revisao: str = Field(min_length=1, max_length=100)
    referencia: str = Field(min_length=1, max_length=500)
    sha256: str = Field(pattern=r'^[0-9a-f]{64}$')

    @field_validator('documento', 'revisao', 'referencia')
    @classmethod
    def texto_nao_vazio(cls, value):
        if not value.strip():
            raise ValueError('Fonte declarada não pode conter texto vazio')
        return value.strip()


class ProtecaoCurtoCircuito(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True, allow_inf_nan=False)
    dispositivo_id: str = Field(min_length=1, max_length=200)
    corrente_nominal_a: float = Field(gt=0)
    corrente_curto_max_a: float = Field(gt=0)
    capacidade_interrupcao_a: float = Field(gt=0)
    grandeza_capacidade: Literal['Icn', 'Icu', 'OUTRA_DECLARADA']
    tempo_eliminacao_s: float = Field(gt=0)
    metodo_energia: Literal['INTEGRAL_JOULE_DECLARADA', 'I_EFICAZ_QUADRADO_TEMPO']
    energia_passante_a2s: float | None = Field(default=None, gt=0)
    corrente_eficaz_atuacao_a: float | None = Field(default=None, gt=0)
    assimetria_significativa: bool | None = None
    k_a_raiz_s_mm2: float = Field(gt=0)
    material: str = Field(min_length=1, max_length=100)
    isolacao: str = Field(min_length=1, max_length=100)
    temperatura_inicial_c: float
    temperatura_final_c: float
    fonte_dispositivo: FonteProtecao
    fonte_curto: FonteProtecao
    fonte_k: FonteProtecao

    @field_validator('dispositivo_id', 'material', 'isolacao')
    @classmethod
    def texto_nao_vazio(cls, value):
        if not value.strip():
            raise ValueError('Identificação de proteção não pode ser vazia')
        return value.strip()

    @model_validator(mode='after')
    def dados_coerentes(self):
        if self.temperatura_final_c <= self.temperatura_inicial_c:
            raise ValueError('Temperatura final de curto deve exceder a inicial')
        if self.metodo_energia == 'INTEGRAL_JOULE_DECLARADA':
            if self.energia_passante_a2s is None or self.corrente_eficaz_atuacao_a is not None:
                raise ValueError('Integral declarada exige energia e não admite corrente eficaz alternativa')
        elif self.corrente_eficaz_atuacao_a is None or self.energia_passante_a2s is not None:
            raise ValueError('Modelo I eficaz²t exige corrente eficaz e não admite energia alternativa')
        return self


class EstudoCoordenacao(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True, allow_inf_nan=False)
    estudo_id: str = Field(min_length=1, max_length=200)
    dispositivo_sobrecarga_id: str = Field(min_length=1, max_length=200)
    dispositivo_curto_id: str = Field(min_length=1, max_length=200)
    corrente_curto_max_estudada_a: float = Field(gt=0)
    conclusao_declarada: Literal['COMPATIVEL', 'INCOMPATIVEL', 'INCONCLUSIVO']
    seletividade_necessaria: bool
    seletividade_demonstrada: bool | None = None
    abrange_dr: bool
    escopo_estudo: str = Field(min_length=1, max_length=2000)
    fonte: FonteProtecao

    @field_validator('estudo_id', 'dispositivo_sobrecarga_id', 'dispositivo_curto_id', 'escopo_estudo')
    @classmethod
    def texto_nao_vazio(cls, value):
        if not value.strip():
            raise ValueError('Identificação/escopo do estudo não pode ser vazio')
        return value.strip()


def _positive_decimal(value, name):
    if not isinstance(value, Decimal) or not value.is_finite() or value <= 0:
        raise ValueError(f'{name} deve ser Decimal positivo e finito')


def _text(value):
    text = format(value, 'f')
    return text.rstrip('0').rstrip('.') if '.' in text else text


def verificar_curto_circuito(secao_mm2, dados, condicoes=None, corrente_nominal_a=None):
    """Compare interrupção direta e energia, sem selecionar dispositivo ou atestar projeto.

    Integral fornecida exige característica declarada. O modo I eficaz²t não usa
    automaticamente a corrente presumida máxima: exige corrente eficaz própria.
    O recorte implementado é adiabático de até 5 s; acima disso não extrapola k.
    Para t<0,1 s o modo I²t só é aplicado se a assimetria foi explicitamente
    declarada não significativa; do contrário é necessária a integral passante.
    """
    _positive_decimal(secao_mm2, 'Seção')
    if corrente_nominal_a is not None:
        _positive_decimal(corrente_nominal_a, 'In selecionado')
    base = {'fontes_verificadas': False, 'liberacao_normativa': False,
            'fonte_regra_sha256': FONTE_REGRA_SHA256,
            'origem_fontes': 'DECLARADA_NAO_VERIFICADA',
            'referencia_regra': 'NBR 5410:2004 corrigida 2008, 5.3.5.5.1/2',
            'atuacao_ik_min_e_curvas': 'PENDENTE',
            'coordenacao_completa': 'PENDENTE'}
    if dados is None:
        return {**base, 'status': 'PENDENTE', 'motivo': 'Dados de curto, dispositivo e k não informados'}
    data = ProtecaoCurtoCircuito.model_validate(dados).model_dump(mode='json')
    nominal = Decimal(str(data['corrente_nominal_a']))
    if corrente_nominal_a is not None and nominal != corrente_nominal_a:
        raise ValueError('Dispositivo de curto não corresponde ao In selecionado')
    if condicoes is not None:
        if (data['material'] != condicoes['material'] or data['isolacao'] != condicoes['isolacao'] or
                Decimal(str(data['temperatura_inicial_c'])) < Decimal(str(condicoes['temperatura_condutor_c']))):
            raise ValueError('Condições de k incompatíveis com o condutor selecionado')
    current = Decimal(str(data['corrente_curto_max_a']))
    breaking = Decimal(str(data['capacidade_interrupcao_a']))
    duration = Decimal(str(data['tempo_eliminacao_s']))
    k = Decimal(str(data['k_a_raiz_s_mm2']))
    with localcontext() as ctx:
        ctx.prec = 100
        limit = k * k * secao_mm2 * secao_mm2
    interruption = breaking >= current
    result = {**base, 'dispositivo_id': data['dispositivo_id'], 'entrada_declarada': data,
              'secao_mm2': _text(secao_mm2), 'capacidade_interrupcao_atendida': interruption,
              'corrente_curto_max_a': _text(current), 'capacidade_interrupcao_a': _text(breaking),
              'limite_termico_a2s': _text(limit), 'energia_passante_utilizada_a2s': None,
              'criterio_termico_atendido': None, 'metodo_energia': data['metodo_energia'],
              'dominio_termico': 'PENDENTE', 'compatibilidade_condutor':
                  'DECLARADA_E_COMPARADA' if condicoes is not None else 'SEM_VINCULO_DE_CELULAS',
              'ressalvas': ['Interrupção verificada pela via direta; associação de retaguarda não presumida.',
                            'k, tempo e energia exigem fonte e aplicabilidade técnica; não são valores homologados.']}
    if secao_mm2 < 10:
        result['ressalvas'].append('Pequenas seções, especialmente abaixo de 10 mm², exigem atenção à aplicabilidade de k (nota de 5.3.5.5.2).')
    if duration > 5:
        result['motivo'] = 'Duração superior a 5 s fora do recorte térmico implementado; não extrapolar k'
    elif (data['metodo_energia'] == 'I_EFICAZ_QUADRADO_TEMPO' and duration < Decimal('.1') and
          data['assimetria_significativa'] is not False):
        result['motivo'] = 'Abaixo de 0,1 s com assimetria significativa/desconhecida, usar integral passante rastreável'
    else:
        if data['metodo_energia'] == 'INTEGRAL_JOULE_DECLARADA':
            energy = Decimal(str(data['energia_passante_a2s']))
        else:
            effective = Decimal(str(data['corrente_eficaz_atuacao_a']))
            with localcontext() as ctx:
                ctx.prec = 100
                energy = effective * effective * duration
        result.update(energia_passante_utilizada_a2s=_text(energy),
                      criterio_termico_atendido=energy <= limit, dominio_termico='NO_RECORTE_IMPLEMENTADO')
    if not interruption or result['criterio_termico_atendido'] is False:
        result['status'] = 'NAO_ATENDE'
    elif result['criterio_termico_atendido'] is True:
        result['status'] = 'ATENDE_CALCULO_PARCIAL'
    else:
        result['status'] = 'PENDENTE'
    return result


def verificar_coordenacao(dados, corrente_curto_max_a=None, dispositivo_sobrecarga_id=None,
                          dispositivo_curto_id=None):
    """Check study identity/scope only; positive client conclusion is not approval."""
    result = {'status': 'PENDENTE', 'estudo_verificado': False,
              'fonte_regra_sha256': FONTE_REGRA_SHA256,
              'liberacao_normativa': False, 'referencia_regra':
                  'NBR 5410:2004 corrigida 2008, 5.3.6 e 6.3.6'}
    if dados is None:
        return {**result, 'motivo': 'Estudo de coordenação não informado'}
    if corrente_curto_max_a is not None:
        _positive_decimal(corrente_curto_max_a, 'Icc máxima')
    data = EstudoCoordenacao.model_validate(dados).model_dump(mode='json')
    if (dispositivo_sobrecarga_id is not None and
            dispositivo_sobrecarga_id != data['dispositivo_sobrecarga_id']):
        raise ValueError('Estudo não corresponde ao dispositivo de sobrecarga')
    if dispositivo_curto_id is not None and dispositivo_curto_id != data['dispositivo_curto_id']:
        raise ValueError('Estudo não corresponde ao dispositivo de curto')
    covers_current = (None if corrente_curto_max_a is None else
                      Decimal(str(data['corrente_curto_max_estudada_a'])) >= corrente_curto_max_a)
    result.update(estudo_declarado=data, cobertura_corrente_curto=covers_current,
                  origem_estudo='DECLARADO_NAO_VERIFICADO',
                  motivo='Estudo declarado requer revisão técnica; não valida curvas, energia ou seletividade automaticamente')
    if (data['conclusao_declarada'] == 'INCOMPATIVEL' or covers_current is False or
            (data['seletividade_necessaria'] and data['seletividade_demonstrada'] is False)):
        result['status'] = 'NAO_ATENDE'
    return result
