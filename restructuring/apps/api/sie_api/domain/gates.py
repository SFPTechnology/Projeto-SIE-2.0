from dataclasses import dataclass
from enum import Enum

class StatusEngenharia(str, Enum):
    BLOQUEADO = 'BLOQUEADO'
    PENDENTE = 'PENDENTE'
    APROVADO = 'APROVADO'

@dataclass(frozen=True)
class EvidenciaNormativa:
    documento: str
    edicao: str
    referencia: str
    dados_validados: bool = False
    testes_independentes: bool = False

def status_liberacao(evidencia: EvidenciaNormativa | None) -> StatusEngenharia:
    if evidencia is None:
        return StatusEngenharia.BLOQUEADO
    if not all((evidencia.documento.strip(), evidencia.edicao.strip(), evidencia.referencia.strip())):
        return StatusEngenharia.BLOQUEADO
    if not (evidencia.dados_validados and evidencia.testes_independentes):
        return StatusEngenharia.PENDENTE
    return StatusEngenharia.APROVADO
