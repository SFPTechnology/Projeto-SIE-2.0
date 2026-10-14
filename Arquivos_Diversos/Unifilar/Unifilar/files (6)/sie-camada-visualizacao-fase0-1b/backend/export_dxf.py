"""
SIE — Exportação do Unifilar para DXF (PRD 4.1 / UF-05 / R-05).

Emissão via ezdxf:
- DXF R2010 (AC1024) — compatível com AutoCAD LT ≥ 2010 (mitigação R-05).
- Seção BLOCKS com definições BLK_* (espelho canônico dos componentes React).
- Condutores como LWPOLYLINE; anotações como MTEXT.
- Cada família em layer própria (ligar/desligar no AutoCAD).

Layout determinístico idêntico ao DT-02 do renderizador SVG:
linha do circuito i em Y = -(TOP + i·ROW_H); colunas fixas DR/disjuntor/carga.
"""

from __future__ import annotations

import ezdxf
from ezdxf.document import Drawing

from .contrato_circuito import CircuitoCanonico, StatusLinha, TipoCircuito

# --- Constantes de layout (mesmos valores do UnifilarHero.tsx, em unidades DXF = mm) ---
TOP = 60.0
ROW_H = 18.0
X_BARRAMENTO = 40.0
X_DR = 90.0
X_DISJUNTOR = 130.0
X_CARGA = 180.0

LAYERS = {
    "SIE_RAMAL": 5,       # azul
    "SIE_MEDICAO": 3,     # verde
    "SIE_PROTECAO": 1,    # vermelho
    "SIE_DR": 6,          # magenta
    "SIE_CARGAS": 7,      # branco/preto
    "SIE_CONDUTORES": 8,  # cinza
    "SIE_ANOTACOES": 2,   # amarelo
    "SIE_PENDENCIAS": 1,  # vermelho — elementos [VERIFICAR]
}

_BLOCO_CARGA = {
    TipoCircuito.ILUMINACAO: "BLK_ILU",
    TipoCircuito.TUG: "BLK_TUG",
    TipoCircuito.TUE: "BLK_TUE",
    TipoCircuito.OUTRA: "BLK_TUE",
}


def _definir_blocos(doc: Drawing) -> None:
    """Definições canônicas dos blocos IEC 60617 (espelham simbolos_iec.tsx)."""
    # Medidor kWh: círculo com texto
    b = doc.blocks.new("BLK_MEDIDOR")
    b.add_circle((0, 0), radius=5)
    b.add_mtext("kWh", dxfattribs={"char_height": 2.2}).set_location((0, 0), attachment_point=5)

    # Disjuntor termomagnético (IEC 60617-07-02-04 simplificado)
    b = doc.blocks.new("BLK_DISJUNTOR")
    b.add_lwpolyline([(-5, 0), (-2, 0)])
    b.add_lwpolyline([(-2, 0), (3, 3)])          # contato aberto
    b.add_lwpolyline([(3, 0), (5, 0)])
    b.add_lwpolyline([(-2, 0), (-2, 1.5), (-0.5, 1.5)])  # traço de disparo

    # Dispositivo DR: disjuntor + elipse do toroide
    b = doc.blocks.new("BLK_DR")
    b.add_lwpolyline([(-5, 0), (-2, 0)])
    b.add_lwpolyline([(-2, 0), (3, 3)])
    b.add_lwpolyline([(3, 0), (5, 0)])
    b.add_ellipse((0.5, -2.5), major_axis=(3, 0), ratio=0.45)

    # Luminária: círculo com X (IEC 60617-11)
    b = doc.blocks.new("BLK_ILU")
    b.add_circle((0, 0), radius=3.5)
    d = 3.5 * 0.7071
    b.add_lwpolyline([(-d, -d), (d, d)])
    b.add_lwpolyline([(-d, d), (d, -d)])

    # Tomada TUG (semicírculo com haste)
    b = doc.blocks.new("BLK_TUG")
    b.add_arc((0, 0), radius=3.5, start_angle=270, end_angle=90)
    b.add_lwpolyline([(-3.5, 0), (-6, 0)])

    # Carga específica TUE (tomada + traço duplo)
    b = doc.blocks.new("BLK_TUE")
    b.add_arc((0, 0), radius=3.5, start_angle=270, end_angle=90)
    b.add_lwpolyline([(-3.5, 0), (-6, 0)])
    b.add_lwpolyline([(1.2, -4.8), (1.2, 4.8)])

    # Barramento trifásico
    b = doc.blocks.new("BLK_BARR")
    for i, dy in enumerate((2.0, 0.0, -2.0)):
        b.add_lwpolyline([(0, dy), (10, dy)])
    b.add_mtext("R S T", dxfattribs={"char_height": 1.8}).set_location((5, 5), attachment_point=5)

    # Motor (círculo com M)
    b = doc.blocks.new("BLK_MOTOR")
    b.add_circle((0, 0), radius=4)
    b.add_mtext("M", dxfattribs={"char_height": 3}).set_location((0, 0), attachment_point=5)


def exportar_unifilar_dxf(circuitos: list[CircuitoCanonico], caminho: str, projeto_id: str = "") -> str:
    """Gera o DXF do unifilar e retorna o caminho gravado."""
    doc = ezdxf.new("R2010")  # AC1024 — mitigação R-05
    for nome, cor in LAYERS.items():
        doc.layers.add(nome, color=cor)
    _definir_blocos(doc)
    msp = doc.modelspace()

    # Cabeçalho: Rede EDP → Medição → Proteção Geral → Barramento
    y0 = 0.0
    msp.add_mtext(
        f"SIE — Diagrama Unifilar {projeto_id}".strip(),
        dxfattribs={"layer": "SIE_ANOTACOES", "char_height": 4},
    ).set_location((X_BARRAMENTO, y0 + 30), attachment_point=1)
    if any(c.provisorio for c in circuitos):
        msp.add_mtext(
            "ÁRVORE PROVISÓRIA — adaptador 1:1 (pré-Divisão de Circuitos)",
            dxfattribs={"layer": "SIE_PENDENCIAS", "char_height": 2.5},
        ).set_location((X_BARRAMENTO, y0 + 22), attachment_point=1)

    msp.add_lwpolyline([(0, y0), (X_BARRAMENTO - 20, y0)], dxfattribs={"layer": "SIE_RAMAL"})
    msp.add_mtext("Rede EDP", dxfattribs={"layer": "SIE_ANOTACOES", "char_height": 2}) \
        .set_location((0, y0 + 4), attachment_point=1)
    msp.add_blockref("BLK_MEDIDOR", (X_BARRAMENTO - 14, y0), dxfattribs={"layer": "SIE_MEDICAO"})
    msp.add_lwpolyline([(X_BARRAMENTO - 9, y0), (X_BARRAMENTO - 5, y0)],
                       dxfattribs={"layer": "SIE_CONDUTORES"})
    msp.add_blockref("BLK_DISJUNTOR", (X_BARRAMENTO, y0), dxfattribs={"layer": "SIE_PROTECAO"})
    msp.add_mtext("Geral", dxfattribs={"layer": "SIE_ANOTACOES", "char_height": 2}) \
        .set_location((X_BARRAMENTO, y0 + 5), attachment_point=1)
    msp.add_blockref("BLK_BARR", (X_BARRAMENTO + 8, y0 - 1), dxfattribs={"layer": "SIE_RAMAL"})

    # Tronco vertical do barramento
    y_fim = -(TOP + (len(circuitos) - 1) * ROW_H)
    msp.add_lwpolyline([(X_BARRAMENTO, y0 - 3), (X_BARRAMENTO, y_fim)],
                       dxfattribs={"layer": "SIE_CONDUTORES"})

    # Circuitos (layout determinístico DT-02)
    for i, c in enumerate(circuitos):
        y = -(TOP + i * ROW_H)
        pendente = c.tensao_v is None
        layer_cond = "SIE_PENDENCIAS" if pendente else "SIE_CONDUTORES"

        x_cursor = X_BARRAMENTO
        if c.requisito_dr:
            msp.add_lwpolyline([(x_cursor, y), (X_DR - 5, y)], dxfattribs={"layer": layer_cond})
            msp.add_blockref("BLK_DR", (X_DR, y), dxfattribs={"layer": "SIE_DR"})
            x_cursor = X_DR + 5
        msp.add_lwpolyline([(x_cursor, y), (X_DISJUNTOR - 5, y)], dxfattribs={"layer": layer_cond})
        msp.add_blockref("BLK_DISJUNTOR", (X_DISJUNTOR, y), dxfattribs={"layer": "SIE_PROTECAO"})
        msp.add_lwpolyline([(X_DISJUNTOR + 5, y), (X_CARGA - 7, y)], dxfattribs={"layer": layer_cond})
        msp.add_blockref(_BLOCO_CARGA[c.tipo], (X_CARGA, y), dxfattribs={"layer": "SIE_CARGAS"})

        ib = f"{c.corrente_projeto_a:.2f} A" if c.corrente_projeto_a is not None else "[VERIFICAR]"
        v = f"{c.tensao_v} V" if c.tensao_v is not None else "[VERIFICAR]"
        rotulo = f"{c.id} — {c.va_total} VA · {v} · IB {ib}"
        if c.status_linha is not StatusLinha.INFO:
            rotulo += f"  ({c.status_linha.value})"
        msp.add_mtext(rotulo, dxfattribs={"layer": "SIE_ANOTACOES", "char_height": 2}) \
            .set_location((X_CARGA + 10, y), attachment_point=4)

    doc.saveas(caminho)
    return caminho
