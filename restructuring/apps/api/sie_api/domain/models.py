from dataclasses import dataclass
from decimal import Decimal

@dataclass(frozen=True)
class CircuitoEletrico:
    identificador: str
    corrente_a: Decimal
    comprimento_m: Decimal
    tensao_v: Decimal

    def __post_init__(self):
        if not self.identificador.strip():
            raise ValueError('Identificador obrigatorio')
        if not self.corrente_a.is_finite() or self.corrente_a <= 0:
            raise ValueError('Corrente invalida')
        if not self.comprimento_m.is_finite() or self.comprimento_m < 0:
            raise ValueError('Comprimento invalido')
        if not self.tensao_v.is_finite() or self.tensao_v <= 0:
            raise ValueError('Tensao invalida')
