"""Gate conservador: declaração do cliente nunca é aprovação normativa.

Uma futura liberação requer registro de evidência verificado pelo servidor,
com controle de acesso, versão do cálculo e auditoria. Até lá: PENDENTE.
"""
from dataclasses import dataclass
from enum import Enum


class StatusEngenharia(str, Enum):
    BLOQUEADO = "BLOQUEADO"
    PENDENTE = "PENDENTE"
    APROVADO = "APROVADO"


@dataclass(frozen=True)
class EvidenciaNormativa:
    documento: str
    edicao: str
    referencia: str
    # Campos legados são metadados não confiáveis: nunca concedem aprovação.
    dados_validados: bool = False
    testes_independentes: bool = False


def status_liberacao(evidencia: EvidenciaNormativa | None) -> StatusEngenharia:
    if evidencia is None:
        return StatusEngenharia.BLOQUEADO
    if not all((evidencia.documento.strip(), evidencia.edicao.strip(), evidencia.referencia.strip())):
        return StatusEngenharia.BLOQUEADO
    # Nenhuma via de aprovação por dados enviados na requisição.
    return StatusEngenharia.PENDENTE
