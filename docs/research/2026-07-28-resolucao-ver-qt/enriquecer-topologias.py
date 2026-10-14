"""Preenche topologia_coluna_id, temperatura_operacao_c e notas de restricao.

Base: leitura visual das figuras das paginas 33-41 (renderizadas a 260-300 dpi) +
assinatura geometrica vetorial confirmando que todas as tabelas de cada grupo
possuem figuras identicas. Temperaturas: texto literal da p.21, secao 6.3.
"""
import io
import json
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# Layout GRUPO A (cabos unipolares): T28, T29, T34 -> 5 + 4 colunas
GRUPO_A = {
    1: ["2_UNIPOLARES_JUSTAPOSTOS", "2_UNIPOLARES_S_2D", "2_UNIPOLARES_S_13CM",
        "2_UNIPOLARES_S_20CM", "3_UNIPOLARES_JUSTAPOSTOS"],
    2: ["3_UNIPOLARES_S_2D", "3_UNIPOLARES_S_13CM", "3_UNIPOLARES_S_20CM",
        "3_UNIPOLARES_TREVO"],
}

# Layout GRUPO B (linha com versao multipolar): T30-33, T35, T36 -> 6 + 6 colunas
GRUPO_B = {
    1: ["2_UNIPOLARES_JUSTAPOSTOS", "CABO_BIPOLAR", "2_UNIPOLARES_S_2D",
        "2_UNIPOLARES_S_13CM", "2_UNIPOLARES_S_20CM", "3_UNIPOLARES_JUSTAPOSTOS"],
    2: ["3_UNIPOLARES_S_2D", "3_UNIPOLARES_S_13CM", "3_UNIPOLARES_S_20CM",
        "3_UNIPOLARES_TREVO", "CABO_TRIPOLAR", "3_UNIPOLARES_20CM_X_20CM"],
}

LAYOUT = {28: GRUPO_A, 29: GRUPO_A, 34: GRUPO_A,
          30: GRUPO_B, 31: GRUPO_B, 32: GRUPO_B, 33: GRUPO_B, 35: GRUPO_B, 36: GRUPO_B}

# Temperatura maxima de operacao por familia - p.21, secao 6.3 (texto literal):
# "70 oC para Superastic, Superastic Flex, Sintenax, Sintenax Flex e Afumex Green"
# "90 oC para GSette Easy, Voltenax, Voltalene e Afumex Flex"
TEMP = {28: 70, 29: 70, 30: 70, 31: 70, 32: 90, 33: 90, 34: 70, 35: 70, 36: 90}

# Nota (1) das tabelas 33 e 36: "Cabo Voltenax" -- a coluna multipolar vale
# apenas para o Voltenax, nao para o Voltalene.
NOTA_1 = {33: "Nota (1): Cabo Voltenax", 36: "Nota (1): Cabo Voltenax"}
COLUNAS_COM_NOTA = {"CABO_BIPOLAR", "CABO_TRIPOLAR"}

DESCRICAO = {
    "2_UNIPOLARES_JUSTAPOSTOS": "dois cabos unipolares justapostos (sem afastamento)",
    "2_UNIPOLARES_S_2D": "dois cabos unipolares afastados, s = 2.D",
    "2_UNIPOLARES_S_13CM": "dois cabos unipolares afastados, s = 13 cm",
    "2_UNIPOLARES_S_20CM": "dois cabos unipolares afastados, s = 20 cm",
    "3_UNIPOLARES_JUSTAPOSTOS": "tres cabos unipolares justapostos em linha",
    "3_UNIPOLARES_S_2D": "tres cabos unipolares em linha, s = 2.D",
    "3_UNIPOLARES_S_13CM": "tres cabos unipolares em linha, s = 13 cm",
    "3_UNIPOLARES_S_20CM": "tres cabos unipolares em linha, s = 20 cm",
    "3_UNIPOLARES_TREVO": "tres cabos unipolares em trevo/trifolio (triangulo justaposto)",
    "3_UNIPOLARES_20CM_X_20CM": "tres cabos unipolares afastados 20 cm x 20 cm",
    "CABO_BIPOLAR": "cabo multipolar de duas veias",
    "CABO_TRIPOLAR": "cabo multipolar de tres veias",
}

d = json.load(open("impedancia-prysmian.json", encoding="utf-8"))

for x in d["registros"]:
    layout = LAYOUT[x["tabela"]][x["bloco_ordinal"]]
    topo = layout[x["coluna_ordinal"] - 1]
    x["topologia_coluna_id"] = topo
    x["topologia_descricao"] = DESCRICAO[topo]
    x["temperatura_operacao_c"] = TEMP[x["tabela"]]
    x["nota_restricao"] = (
        NOTA_1[x["tabela"]]
        if x["tabela"] in NOTA_1 and topo in COLUNAS_COM_NOTA
        else None
    )

for inv in d["inventario"]:
    lay = LAYOUT[inv["tabela"]]
    inv["temperatura_operacao_c"] = TEMP[inv["tabela"]]
    inv["layout_grupo"] = "A" if lay is GRUPO_A else "B"
    for b in inv["blocos"]:
        b["topologias"] = lay[b["bloco_ordinal"]]

d["fonte"]["temperatura_operacao_fonte"] = (
    "p.21, secao 6.3: '70 oC para Superastic, Superastic Flex, Sintenax, "
    "Sintenax Flex e Afumex Green' / '90 oC para GSette Easy, Voltenax, "
    "Voltalene e Afumex Flex'"
)
d["fonte"]["coeficiente_temperatura_alfa20"] = {
    "CU": 0.00393, "AL": 0.00403,
    "fonte": "p.21, secao 6.3 (texto literal)",
}
d["topologias"] = {
    "metodo_identificacao": "leitura visual das figuras das paginas 33-41 renderizadas "
                            "a 260-300 dpi, confirmada por assinatura geometrica vetorial "
                            "identica entre as tabelas de cada grupo de layout",
    "grupo_A": {"tabelas": [28, 29, 34], "blocos": GRUPO_A},
    "grupo_B": {"tabelas": [30, 31, 32, 33, 35, 36], "blocos": GRUPO_B},
    "descricoes": DESCRICAO,
}

json.dump(d, open("impedancia-prysmian.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)

sem = sum(1 for x in d["registros"] if not x["topologia_coluna_id"])
print(f"registros: {len(d['registros'])}   sem topologia: {sem}")
print(f"topologias distintas: {len(set(x['topologia_coluna_id'] for x in d['registros']))}")
print(f"com nota de restricao: {sum(1 for x in d['registros'] if x['nota_restricao'])}")

# Amostra de validacao contra a leitura visual da T28 bloco 1, secao 1,5
print("\nValidacao T28 bloco1 secao 1,5 (esperado da imagem: 0,12 0,17 0,40 0,44 0,14):")
for x in d["registros"]:
    if x["tabela"] == 28 and x["bloco_ordinal"] == 1 and x["secao_mm2"] == 1.5:
        print(f"  col{x['coluna_ordinal']} XL={x['x_l_ohm_km']}  {x['topologia_coluna_id']}")
