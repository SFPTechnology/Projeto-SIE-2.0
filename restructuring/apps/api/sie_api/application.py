"""Use cases joining structural validation, calculations and release gates."""
from decimal import Decimal
from .domain.engines import calcular_queda_tensao_monofasica, selecionar_condutor, selecionar_disjuntor
from .domain.gates import EvidenciaNormativa, StatusEngenharia, status_liberacao

CATALOGO_DISJUNTORES = tuple(Decimal(str(v)) for v in (6, 10, 16, 20, 25, 32, 40, 50, 63, 80, 100, 125))


def analisar_circuito(payload: dict) -> dict:
    evidencia = EvidenciaNormativa(**payload["evidencia"])
    status = status_liberacao(evidencia)
    corrente = Decimal(str(payload["corrente_a"]))
    tensao = Decimal(str(payload["tensao_v"]))
    comprimento = Decimal(str(payload["comprimento_m"]))
    condutor = selecionar_condutor(corrente, Decimal(str(payload["fator_correcao"])), tuple((Decimal(str(i["secao_mm2"])), Decimal(str(i["capacidade_a"]))) for i in payload["tabela_condutores"]))
    queda = calcular_queda_tensao_monofasica(corrente, comprimento, Decimal(str(payload["resistencia_ohm_km"])), tensao)
    disjuntor = selecionar_disjuntor(corrente, condutor.capacidade_corrigida_a, CATALOGO_DISJUNTORES)
    return {
        "status_engenharia": status.value,
        "liberado_para_uso_normativo": status == StatusEngenharia.APROVADO,
        "aviso": None if status == StatusEngenharia.APROVADO else "Resultado técnico calculado; uso normativo bloqueado até validação de fonte e testes independentes.",
        "condutor": {"secao_mm2": float(condutor.secao_mm2), "capacidade_corrigida_a": float(condutor.capacidade_corrigida_a), "criterio": condutor.criterio},
        "disjuntor": {"corrente_a": float(disjuntor.corrente_disjuntor_comercial_a), "criterio": disjuntor.criterio},
        "queda_tensao": {"queda_v": float(queda.queda_v), "queda_percentual": float(queda.queda_percentual), "formula": queda.formula},
        "rastreabilidade": {"fonte": evidencia.documento, "edicao": evidencia.edicao, "referencia": evidencia.referencia},
    }
