"""Extrai as tabelas 28-36 (Resistencias Eletricas e Reatancias Indutivas) do
Guia de Dimensionamento de Cabos para Baixa Tensao - Prysmian.

Regras: transcricao literal. Nenhuma interpolacao, nenhuma inferencia de rotulo
de coluna, nenhuma celula preenchida por deducao.
"""
import io
import json
import re
import sys

import pypdf

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

PDF = (
    r"C:\Users\User\.claude\projects"
    r"\C--Users-User-Documents-2026-Projects-Smart-Systems-Projeto-SIE"
    r"\c2367712-c4c0-4b40-a098-0bf035696385\tool-results"
    r"\webfetch-1785266757572-h9h4uw.pdf"
)

# pagina PDF (0-indexed) -> numero da tabela impressa
PAGINAS = {32: 28, 33: 29, 34: 30, 35: 31, 36: 32, 37: 33, 38: 34, 39: 35, 40: 36}

NUM = re.compile(r"^\d+(?:,\d+)?$")

# Secoes nominais publicadas (serie do guia). Usada para ancorar o inicio da linha.
SECOES = ["1,5", "2,5", "500", "400", "300", "240", "185", "150", "120",
          "95", "70", "50", "35", "25", "16", "10", "6", "4"]

# Um valor de celula: parte inteira + virgula + exatamente 2 decimais, ou '-'
CELULA = re.compile(r"^(?:(\d+),(\d{2})|-)")


def segmentar_celulas(resto):
    """Segmenta a parte numerica da linha em celulas.

    O PDF fragmenta digitos de forma arbitraria dentro de um mesmo numero
    ('1 7, 0 0' = 17,00; '0,1 7' = 0,17). Como TODA celula de dado tem
    exatamente 2 casas decimais, remover os espacos e ancorar em ',dd'
    reconstroi os valores sem ambiguidade. '-' = celula nao publicada.

    Retorna (valores, sobra). Sobra nao vazia = anomalia.
    """
    s = resto.replace(" ", "")
    valores = []
    while s:
        m = CELULA.match(s)
        if not m:
            break
        if m.group(0) == "-":
            valores.append(None)
        else:
            valores.append(float(f"{m.group(1)}.{m.group(2)}"))
        s = s[m.end():]
    return valores, s


def linhas_com_y(page):
    """Agrupa os itens de texto da pagina em linhas por coordenada y."""
    itens = []

    def visitor(text, cm, tm, fd, fs):
        s = text.strip()
        if s:
            itens.append((round(tm[5], 1), round(tm[4], 1), s))

    page.extract_text(visitor_text=visitor)
    itens.sort(key=lambda t: (-t[0], t[1]))

    linhas, atual, y_atual = [], [], None
    for y, x, s in itens:
        if y_atual is None or abs(y - y_atual) > 2:
            if atual:
                linhas.append((y_atual, " ".join(atual)))
            atual, y_atual = [s], y
        else:
            atual.append(s)
    if atual:
        linhas.append((y_atual, " ".join(atual)))
    return linhas


def corrigir_digito_solto(tokens):
    """'0,1' '7' -> '0,17'. Artefato de extracao do PDF.

    Aplicado somente a partir do 2o token: o 1o e a secao nominal, que pode
    legitimamente ser um digito isolado (4, 6).
    """
    saida = [tokens[0]]
    for tok in tokens[1:]:
        if len(tok) == 1 and tok.isdigit() and saida and "," in saida[-1]:
            saida[-1] = saida[-1] + tok
        else:
            saida.append(tok)
    return saida


def extrair_pagina(page, tabela):
    linhas = linhas_com_y(page)
    familia = next(
        (t.split(" - ", 2)[-1] for _, t in linhas if t.startswith(f"Tabela {tabela} -")),
        None,
    )
    metal = next((t for _, t in linhas if t.startswith("Condutor de ")), "")
    rodape = next(
        (t for _, t in linhas if t.startswith("Valores válidos")
         or t.startswith("Valores validos")), None
    )
    rotulos = next(
        (t for _, t in linhas if "s = 2.D" in t or "s = 2,D" in t), ""
    )
    rotulos_col = re.findall(r"s = [^s]+?(?=\s+s = |$)", rotulos)

    blocos, atual = [], None
    for _y, txt in linhas:
        pares = len(re.findall(r"Rca XL", txt))
        if pares:
            if atual:
                blocos.append(atual)
            atual = {"n_colunas": pares, "linhas": [], "anomalias": []}
            continue
        if atual is None:
            continue
        secao = next((s for s in SECOES if txt.startswith(s + " ")), None)
        if secao is None:
            continue
        valores, sobra = segmentar_celulas(txt[len(secao):])
        esperado = 2 * atual["n_colunas"]
        if sobra or len(valores) != esperado:
            atual["anomalias"].append(
                {
                    "linha_bruta": txt,
                    "motivo": f"esperado {esperado} valores, obtido {len(valores)}"
                              + (f"; sobra nao parseada: {sobra!r}" if sobra else ""),
                }
            )
            continue
        atual["linhas"].append((secao, valores))
    if atual:
        blocos.append(atual)

    return {
        "tabela": tabela,
        "pagina_pdf": None,
        "familia_literal": familia,
        "metal_literal": metal,
        "rotulos_coluna_textuais": rotulos_col,
        "rodape": rodape,
        "blocos": blocos,
    }


def main():
    r = pypdf.PdfReader(PDF)
    registros, inventario, anomalias = [], [], []

    for idx, tabela in PAGINAS.items():
        info = extrair_pagina(r.pages[idx], tabela)
        info["pagina_pdf"] = idx + 1
        pagina_impressa = idx + 1  # rodape do guia confirma numeracao identica

        metal = "AL" if "alumínio" in (info["familia_literal"] or "").lower() else "CU"
        n_cel = 0
        for b_i, bloco in enumerate(info["blocos"], start=1):
            for secao_txt, valores in bloco["linhas"]:
                secao = float(secao_txt.replace(",", "."))
                for c in range(bloco["n_colunas"]):
                    rca = valores[2 * c]
                    xl = valores[2 * c + 1]
                    registros.append(
                        {
                            "fonte_id": "PRYSMIAN_BT_GUIA",
                            "tabela": tabela,
                            "pagina_impressa": pagina_impressa,
                            "pagina_pdf": idx + 1,
                            "familia_literal": info["familia_literal"],
                            "metal": metal,
                            "bloco_ordinal": b_i,
                            "coluna_ordinal": c + 1,
                            "topologia_coluna_id": None,
                            "secao_mm2": secao,
                            "r_ca_ohm_km": rca,
                            "x_l_ohm_km": xl,
                            "frequencia_hz": 60,
                        }
                    )
                    n_cel += 1
            anomalias.extend(
                {"tabela": tabela, "bloco": b_i, **a} for a in bloco["anomalias"]
            )

        inventario.append(
            {
                "tabela": tabela,
                "pagina_impressa": pagina_impressa,
                "familia_literal": info["familia_literal"],
                "metal": metal,
                "metal_literal": info["metal_literal"],
                "blocos": [
                    {"bloco_ordinal": i, "n_colunas": b["n_colunas"], "n_linhas": len(b["linhas"])}
                    for i, b in enumerate(info["blocos"], start=1)
                ],
                "rotulos_coluna_textuais": info["rotulos_coluna_textuais"],
                "secoes": sorted({float(s.replace(",", ".")) for b in info["blocos"] for s, _ in b["linhas"]}),
                "rodape": info["rodape"],
                "celulas_extraidas": n_cel,
            }
        )

    saida = {
        "fonte": {
            "documento": "Guia de Dimensionamento de Cabos para Baixa Tensão",
            "editor": "Prysmian Brasil",
            "conformidade_declarada": "De acordo com a NBR 5410",
            "url": "https://br.prysmian.com/sites/default/files/atoms/files/"
                   "Guia_de_Dimensionamento-Baixa_Tensao_Rev10.pdf",
            "data_acesso": "2026-07-28",
            "paginas_pdf_total": len(r.pages),
            "definicao_rca": "Resistência elétrica máxima do condutor em corrente "
                             "alternada na temperatura de operação",
            "definicao_xl": "Reatância Indutiva",
            "modelo": "Z = Rca + jXL (impedâncias de sequência positiva ou negativa)",
            "frequencia_hz": 60,
        },
        "inventario": inventario,
        "anomalias": anomalias,
        "registros": registros,
    }

    with open("impedancia-prysmian.json", "w", encoding="utf-8") as f:
        json.dump(saida, f, ensure_ascii=False, indent=2)

    print(f"tabelas: {len(inventario)}  registros: {len(registros)}  anomalias: {len(anomalias)}")
    for inv in inventario:
        blocos = " + ".join(f"{b['n_colunas']}col x {b['n_linhas']}lin" for b in inv["blocos"])
        print(f"  T{inv['tabela']} p{inv['pagina_impressa']} {inv['metal']:2} "
              f"{blocos:24} secoes {inv['secoes'][0]}-{inv['secoes'][-1]} "
              f"= {inv['celulas_extraidas']:3} cel | {inv['familia_literal']}")
    if anomalias:
        print("\nANOMALIAS:")
        for a in anomalias:
            print(" ", a)


main()
