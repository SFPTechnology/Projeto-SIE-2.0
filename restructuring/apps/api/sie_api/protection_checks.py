"""Sobrecarga parcial, Decimal sem arredondamento; fonte do dispositivo declarada."""
from decimal import Decimal


def verificar_sobrecarga(ib, nominal, iz, dados):
    pending = {'curto_circuito': 'PENDENTE', 'coordenacao_protecoes': 'PENDENTE',
               'fonte_dispositivo_verificada': False, 'liberacao_normativa': False}
    if dados is None:
        return {**pending, 'status': 'PENDENTE', 'motivo': 'I2 e duração não informados',
                'criterio_ib_in_iz': ib <= nominal <= iz}
    from .analysis_contracts import ProtecaoSobrecarga
    data = ProtecaoSobrecarga.model_validate(dados).model_dump(mode='json')
    i2 = Decimal(str(data['corrente_atuacao_i2_a']))
    if Decimal(str(data['corrente_nominal_a'])) != nominal:
        raise ValueError('Dispositivo declarado não corresponde ao In selecionado')
    if i2 < nominal:
        raise ValueError('I2 de sobrecarga não pode ser inferior a In')
    yearly, life = data['duracao_sobrecarga_h_12_meses'], data['duracao_sobrecarga_h_vida']
    restricted = ((yearly is not None and Decimal(str(yearly)) > 100) or
                  (life is not None and Decimal(str(life)) > 500))
    known = restricted or (yearly is not None and life is not None)
    multiplier = Decimal('1') if restricted else Decimal('1.45')
    limit = iz * multiplier
    matches = ib <= nominal <= iz and i2 <= limit
    # An ordinary-limit failure is conclusive even when duration is unknown.
    status = 'NAO_ATENDE' if not matches else ('ATENDE_CALCULO_PARCIAL' if known else 'PENDENTE')
    return {**pending, 'status': status, 'criterio_ib_in_iz': ib <= nominal <= iz,
            'i2_a': format(i2.normalize(), 'f'), 'iz_a': format(iz.normalize(), 'f'),
            'limite_i2_a': format(limit.normalize(), 'f'),
            'criterio_i2': 'I2 ≤ Iz' if restricted else 'I2 ≤ 1,45 Iz',
            'condicao_duracao_determinada': known, 'nota_duracao_aplicada': restricted,
            'criterio_i2_atendido': i2 <= limit,
            'fonte_dispositivo': data['fonte'], 'origem_fonte': 'DECLARADA_NAO_VERIFICADA',
            'referencia_regra': 'NBR 5410:2004 corrigida 2008, 5.3.4.1 a)/b)/NOTA',
            'duracao_sobrecarga_h_12_meses': yearly, 'duracao_sobrecarga_h_vida': life}
