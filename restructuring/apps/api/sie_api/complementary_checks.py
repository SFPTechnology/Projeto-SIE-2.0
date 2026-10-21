"""Version 1 of conditional checks; keep semantics for historical trace replay."""
from decimal import Decimal
from .protection_extended import verificar_curto_circuito, verificar_coordenacao
from .voltage_checks import calcular_queda_impedancia

FIELDS = ('protecao_curto_circuito', 'estudo_coordenacao', 'queda_impedancia')
VERSION = 'F01_COMPLEMENTARY_V1'


def verificar_complementos(payload, secao_mm2, nominal, binding):
    if not any(payload.get(k) is not None for k in FIELDS):
        return None
    conditions = None if binding is None else binding['condicoes']
    short_data = payload.get('protecao_curto_circuito')
    short = verificar_curto_circuito(secao_mm2, short_data, conditions,
                                    corrente_nominal_a=nominal)
    overloaded = payload.get('protecao_sobrecarga')
    coordination = verificar_coordenacao(
        payload.get('estudo_coordenacao'),
        None if short_data is None else Decimal(str(short_data['corrente_curto_max_a'])),
        None if overloaded is None else overloaded['fonte']['dispositivo_id'],
        None if short_data is None else short_data['dispositivo_id'])
    voltage_data = payload.get('queda_impedancia')
    if voltage_data is not None and conditions is not None:
        if (voltage_data['material'] != conditions['material'] or
            voltage_data['isolacao'] != conditions['isolacao'] or
            Decimal(str(voltage_data['temperatura_condutor_c'])) !=
                Decimal(str(conditions['temperatura_condutor_c'])) or
            (voltage_data['tipo_circuito'] == 'TRIFASICO_EQUILIBRADO' and
             conditions['condutores_carregados'] != 3)):
            raise ValueError('Parâmetros de queda incompatíveis com as células de capacidade aplicadas')
    voltage = calcular_queda_impedancia(payload['corrente_a'], payload['comprimento_m'],
                                       payload['tensao_v'], voltage_data, secao_mm2=secao_mm2)
    return {'modelo_versao': VERSION, 'curto_circuito': short,
            'coordenacao_protecoes': coordination, 'queda_impedancia': voltage,
            'liberacao_normativa': False,
            'modelo_resistivo_legado': 'Resultado separado em queda_tensao, sem XL e com cos(phi)=1'}
