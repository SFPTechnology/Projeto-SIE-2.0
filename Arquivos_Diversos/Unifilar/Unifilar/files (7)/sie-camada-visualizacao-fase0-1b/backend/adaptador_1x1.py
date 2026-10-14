"""
SIE — Adaptador 1:1 (PRD Seção 5 e Fase 0).

Wrapper provisório: enquanto a Divisão de Circuitos não existe, cada ponto de
carga vira um circuito de 1 ponto. Mecanicamente correto, mas todo circuito
sai marcado `provisorio=True` (risco R-04: nota visual 'Árvore provisória'
obrigatória em todo artefato pré-Divisão).

Decisões do operador incorporadas (Anexo A, 08/07/2026):
- CONF-01: convenção oficial de fases é R/S/T. O sistema legado exibe A/B/C;
  o loader converte com `mapear_fase_abc_para_rst` ANTES de montar PontoCarga.
- CONF-02: o id do circuito é o id REAL do banco (ex.: ILUM-Dormitorio-1,
  ADD-Banheiro-2-Chuveiro-2) — o adaptador NÃO inventa ids.
- CONF-03: ILU/TUG com tensão resolvida pela Saída A (contrato de integração,
  default 127 V) entram com tensao_v=127 e fonte rastreável — status INFO.
  TUE JAMAIS pode ter tensão resolvida por contrato (INC-04): sem tensaoFixa
  declarada → tensao_v=None + ATENÇÃO + [VERIFICAR].

Regras permanentes:
- Não recalcula nada: corrente_projeto_a é copiada do IB do módulo de cálculo.
- INC-03: zona molhada não classificada => requisito_dr=None + pendência.
- Ordenação determinística (tipo, id) — pré-requisito do RNF-03 (SVG diffable).
"""

from __future__ import annotations

from .contrato_circuito import (
    VERIFICAR,
    CircuitoCanonico,
    DerivacaoRegistro,
    Fase,
    PontoCarga,
    StatusLinha,
    TipoCircuito,
)

_ORDEM_TIPO = {
    TipoCircuito.ILUMINACAO: 0,
    TipoCircuito.TUG: 1,
    TipoCircuito.TUE: 2,
    TipoCircuito.OUTRA: 3,
}

# CONF-01 — mapeamento da convenção legada de tela (A/B/C) para a oficial (R/S/T).
_ABC_PARA_RST = {"A": Fase.R, "B": Fase.S, "C": Fase.T,
                 "R": Fase.R, "S": Fase.S, "T": Fase.T}

FONTE_TENSAO_SAIDA_A = (
    "Saída A — contrato de integração EDP-SP (default ILU/TUG 127 V)"
)


def mapear_fase_abc_para_rst(letra: str) -> Fase:
    """Converte fase da convenção de tela (A/B/C) para a oficial (R/S/T).

    Uso: no loader, ao ler a coluna `balanceamento` do banco. Idempotente
    para entradas já em R/S/T.
    """
    try:
        return _ABC_PARA_RST[letra.strip().upper()]
    except KeyError:
        raise ValueError(
            f"Fase '{letra}' não reconhecida — esperado A/B/C (tela) ou R/S/T (oficial)."
        )


def adaptar_ponto(ponto: PontoCarga) -> CircuitoCanonico:
    """Converte 1 ponto de carga em 1 circuito canônico provisório.

    O id do circuito é `ponto.id`, preservado do banco (CONF-02).
    """
    pendencias: list[str] = []
    status = StatusLinha.INFO
    fonte_linha = f"IB:{ponto.id}"

    # CONF-03 — guarda INC-04: TUE nunca recebe tensão por contrato de integração.
    if ponto.tensao_resolvida_por_contrato and ponto.tipo in (
        TipoCircuito.TUE,
        TipoCircuito.OUTRA,
    ):
        raise ValueError(
            f"INC-04 violada no loader: '{ponto.id}' é {ponto.tipo.value} com tensão "
            "resolvida por contrato de integração. TUE/outra exigem tensaoFixa "
            "declarada; sem declaração, envie tensao_v=None."
        )

    # INC-04 — tensão pendente nunca vira 127 V
    if ponto.tensao_v is None:
        pendencias.append(f"{VERIFICAR} Tensão não declarada — IB indisponível (INC-04)")
        status = StatusLinha.ATENCAO
        corrente = None
    else:
        corrente = ponto.corrente_ib_a  # copiado do módulo IB, jamais recalculado
        if ponto.tensao_resolvida_por_contrato:
            # CONF-03: resolução rastreável pela Saída A — não é fallback silencioso.
            fonte_linha += f" | tensão: {FONTE_TENSAO_SAIDA_A}"

    # INC-03 — DR só é resolvível com classificação de zona molhada
    if ponto.zona_molhada is None:
        pendencias.append(
            f"{VERIFICAR} Zona molhada não classificada — requisito DR pendente (INC-03)"
        )
        if status is StatusLinha.INFO:
            status = StatusLinha.ATENCAO
        requisito_dr = None
    else:
        requisito_dr = ponto.zona_molhada

    derivacao = DerivacaoRegistro(
        regra_id="SIE-IB-01",
        referencia_normativa="ABNT NBR 5410:2004 §6.2.7 (corrente de projeto)",
        formula="IB = S / V (S em VA direto — disciplina INC-01)",
        entradas={"S_va": ponto.va, "V_v": ponto.tensao_v, "IB_a": corrente},
    )

    return CircuitoCanonico(
        id=ponto.id,  # CONF-02: id real do banco, preservado
        tipo=ponto.tipo,
        pontos=(ponto.id,),
        dependencias=(ponto.dependencia_id,),
        va_total=ponto.va,  # VA direto — sem divisão por FP (INC-01)
        tensao_v=ponto.tensao_v,
        corrente_projeto_a=corrente,
        fases=ponto.fases,
        requisito_dr=requisito_dr,
        grupo_edp=ponto.grupo_edp,
        disjuntor_a=None,   # aguarda P1/proteção
        secao_mm2=None,     # aguarda P1/condutor
        fonte_linha=fonte_linha,
        status_linha=status,
        provisorio=True,    # árvore provisória (R-04)
        derivacao=derivacao,
        pendencias=tuple(pendencias),
    )


def adaptar_projeto(pontos: list[PontoCarga]) -> list[CircuitoCanonico]:
    """Adapta todos os pontos com ordenação determinística (tipo, id)."""
    circuitos = [adaptar_ponto(p) for p in pontos]
    circuitos.sort(key=lambda c: (_ORDEM_TIPO[c.tipo], c.id))
    return circuitos
