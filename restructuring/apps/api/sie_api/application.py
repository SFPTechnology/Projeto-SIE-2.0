"""Use cases joining structural validation, calculations and release gates."""
from decimal import Decimal
from .complementary_checks import verificar_complementos
from .cell_bindings import resolver_vinculo
from .protection_checks import verificar_sobrecarga
from .domain.engines import calcular_queda_tensao_monofasica, selecionar_condutor, selecionar_disjuntor
from .domain.gates import EvidenciaNormativa, StatusEngenharia, status_liberacao

CATALOGO_DISJUNTORES = tuple(Decimal(str(v)) for v in (6, 10, 16, 20, 25, 32, 40, 50, 63, 80, 100, 125))


def analisar_circuito(payload: dict) -> dict:
    payload, vinculo = resolver_vinculo(payload)
    evidencia = EvidenciaNormativa(**payload["evidencia"])
    status = status_liberacao(evidencia)
    corrente = Decimal(str(payload["corrente_a"]))
    tensao = Decimal(str(payload["tensao_v"]))
    comprimento = Decimal(str(payload["comprimento_m"]))
    # Validate the complete table and preserve the original no-capacity error.
    fator = Decimal(str(payload["fator_correcao"]))
    tabela = tuple((Decimal(str(i["secao_mm2"])), Decimal(str(i["capacidade_a"])))
                   for i in payload["tabela_condutores"])
    condutor = selecionar_condutor(corrente, fator, tabela)
    # For a section-independent catalog, the smallest In >= Ib is the minimum
    # Iz any admissible pair needs. Scan all table candidates against that limit.
    nominal_minimo = selecionar_disjuntor(
        corrente, max((corrente, *CATALOGO_DISJUNTORES)), CATALOGO_DISJUNTORES,
    ).corrente_disjuntor_comercial_a
    if condutor.capacidade_corrigida_a < nominal_minimo:
        if not any(capacidade * fator >= nominal_minimo for _, capacidade in tabela):
            # A section supports Ib, but none can also accommodate commercial In.
            # Keep the F00 diagnostic contract instead of calling this lack of Ib capacity.
            raise ValueError("Nenhum disjuntor comercial atende Ib ≤ In ≤ Iz")
        condutor = selecionar_condutor(nominal_minimo, fator, tabela)
    queda = calcular_queda_tensao_monofasica(corrente, comprimento, Decimal(str(payload["resistencia_ohm_km"])), tensao)
    disjuntor = selecionar_disjuntor(corrente, condutor.capacidade_corrigida_a, CATALOGO_DISJUNTORES)
    protecao = verificar_sobrecarga(corrente, disjuntor.corrente_disjuntor_comercial_a,
                                    condutor.capacidade_corrigida_a, payload.get("protecao_sobrecarga"))
    complementos = verificar_complementos(payload, condutor.secao_mm2,
                                         disjuntor.corrente_disjuntor_comercial_a, vinculo)
    return {
        **({"verificacoes_complementares": complementos} if complementos is not None else {}),
        "status_engenharia": status.value,
        "liberado_para_uso_normativo": status == StatusEngenharia.APROVADO,
        "aviso": None if status == StatusEngenharia.APROVADO else "Coordenação Ib ≤ In ≤ Iz calculada; consulte a verificação parcial de sobrecarga. Curto-circuito e coordenação completa pendentes. Uso normativo bloqueado até validação de fonte e testes independentes.",
        "condutor": {"secao_mm2": float(condutor.secao_mm2), "capacidade_corrigida_a": float(condutor.capacidade_corrigida_a.quantize(Decimal("0.01"))), "capacidade_decisao_a": float(condutor.capacidade_corrigida_a), "criterio": "Seção coordenada com In comercial: Ib ≤ In ≤ Iz; verificação de I2 no relatório de sobrecarga"},
        "disjuntor": {"corrente_a": float(disjuntor.corrente_disjuntor_comercial_a), "criterio": disjuntor.criterio},
        "queda_tensao": {"queda_v": float(queda.queda_v), "queda_percentual": float(queda.queda_percentual), "formula": queda.formula},
        "vinculo_celulas": vinculo,
        "protecao_sobrecarga": protecao,
        "rastreabilidade": {"fonte": evidencia.documento, "edicao": evidencia.edicao, "referencia": evidencia.referencia},
    }
