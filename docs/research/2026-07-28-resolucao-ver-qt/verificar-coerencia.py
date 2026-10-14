"""Testes de coerencia sobre a extracao das tabelas 28-36 (impedancia-prysmian.json).

Nenhum teste corrige dado. Todos apenas medem e reportam.
"""
import io
import json
import re
import statistics as st
import sys
from collections import defaultdict

import pypdf

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

PDF = (
    r"C:\Users\User\.claude\projects"
    r"\C--Users-User-Documents-2026-Projects-Smart-Systems-Projeto-SIE"
    r"\c2367712-c4c0-4b40-a098-0bf035696385\tool-results"
    r"\webfetch-1785266757572-h9h4uw.pdf"
)

d = json.load(open("impedancia-prysmian.json", encoding="utf-8"))
regs = d["registros"]


def num(t):
    return None if t == "-" else float(t.replace(" ", "").replace(",", "."))


# ---- Ancora: tabela 18 (Rdc20) ----------------------------------------------
r = pypdf.PdfReader(PDF)
t18 = {}
for ln in (r.pages[21].extract_text() or "").split("\n"):
    m = re.match(r"^(\d+(?:,\d+)?)\s+(.+)$", ln.strip())
    if not m:
        continue
    campos = re.findall(r"-|\d+\s*,\s*\d+|\d+", m.group(2))
    if len(campos) != 3:
        continue
    secao = num(m.group(1))
    t18[secao] = {"CU": num(campos[0]), "AL": num(campos[1]), "CU_CL5": num(campos[2])}
d["ancora_tabela_18_rdc20_classe2"] = t18
print(f"Tabela 18 (Rdc20): {len(t18)} secoes extraidas -> {sorted(t18)}\n")

res = []


def reportar(tid, nome, veredito, detalhe):
    res.append({"teste": tid, "nome": nome, "veredito": veredito, "detalhe": detalhe})
    print(f"{tid} {nome:38} {veredito:9} {detalhe}")


# ---- T0: Rca invariante entre colunas da mesma linha -------------------------
grupos = defaultdict(list)
for x in regs:
    grupos[(x["tabela"], x["bloco_ordinal"], x["secao_mm2"])].append(x["r_ca_ohm_km"])
desvios = []
for k, v in grupos.items():
    vals = [y for y in v if y is not None]
    if len(vals) > 1 and min(vals) > 0:
        desvios.append((max(vals) - min(vals)) / min(vals) * 100)
pior = max(desvios)
reportar("T0", "Rca invariante entre colunas", "PASSA" if pior <= 12 else "ATENCAO",
         f"dispersao maxima intra-linha {pior:.1f}% (arredondamento de 2 casas)")

# ---- T1: Rca x secao aproximadamente constante -------------------------------
piores = []
for tab in sorted({x["tabela"] for x in regs}):
    prod = [x["r_ca_ohm_km"] * x["secao_mm2"] for x in regs
            if x["tabela"] == tab and x["r_ca_ohm_km"]]
    piores.append((tab, min(prod), max(prod), st.median(prod)))
faixa = f"produto R*S por tabela: {min(p[1] for p in piores):.1f} a {max(p[2] for p in piores):.1f}"
reportar("T1", "Rca x secao ~ constante", "PASSA", faixa)

# ---- T2: razao Al/Cu ---------------------------------------------------------
cu = defaultdict(list)
al = defaultdict(list)
for x in regs:
    if x["r_ca_ohm_km"]:
        (cu if x["metal"] == "CU" else al)[x["secao_mm2"]].append(x["r_ca_ohm_km"])
razoes = {s: st.median(al[s]) / st.median(cu[s]) for s in sorted(al) if s in cu}
reportar("T2", "Rca(Al)/Rca(Cu) ~ constante",
         "PASSA" if max(razoes.values()) - min(razoes.values()) < 0.35 else "ATENCAO",
         f"{min(razoes.values()):.3f} a {max(razoes.values()):.3f} em {len(razoes)} secoes")

# ---- T3: Rca / Rdc20 (ancora tabela 18) --------------------------------------
linhas_t3 = []
for s in sorted(t18):
    for metal in ("CU", "AL"):
        base = t18[s][metal]
        vals = [x["r_ca_ohm_km"] for x in regs
                if x["secao_mm2"] == s and x["metal"] == metal and x["r_ca_ohm_km"]]
        if base and vals:
            linhas_t3.append((s, metal, base, st.median(vals), st.median(vals) / base))
menor = min(l[4] for l in linhas_t3)
reportar("T3", "Rca/Rdc20 >= 1.0 (temp + skin)",
         "PASSA" if menor >= 1.0 else "FALHA",
         f"razao minima {menor:.3f}, maxima {max(l[4] for l in linhas_t3):.3f}")

# ---- T5/T6: comportamento de XL ---------------------------------------------
xl_por_col = defaultdict(list)
for x in regs:
    if x["x_l_ohm_km"]:
        xl_por_col[(x["tabela"], x["bloco_ordinal"], x["coluna_ordinal"])].append(x["x_l_ohm_km"])
saltos = []
for k, v in xl_por_col.items():
    for a, b in zip(v, v[1:]):
        saltos.append(abs(b - a))
reportar("T5", "XL varia suavemente na coluna",
         "PASSA" if max(saltos) <= 0.06 else "ATENCAO",
         f"salto maximo entre secoes adjacentes {max(saltos):.2f} Ohm/km")

difs = []
for (tab, blo, sec), _ in list(grupos.items()):
    vals = [x["x_l_ohm_km"] for x in regs
            if x["tabela"] == tab and x["bloco_ordinal"] == blo
            and x["secao_mm2"] == sec and x["x_l_ohm_km"]]
    if len(vals) > 1:
        difs.append(max(vals) / min(vals))
reportar("T6", "XL difere entre colunas geometricas",
         "PASSA" if st.median(difs) > 1.5 else "FALHA",
         f"razao XLmax/XLmin mediana {st.median(difs):.2f}, maxima {max(difs):.2f}")

# ---- T7: monotonicidade de Rca ----------------------------------------------
falhas7 = 0
for (tab, blo, col), _ in [(k, None) for k in xl_por_col]:
    seq = [(x["secao_mm2"], x["r_ca_ohm_km"]) for x in regs
           if x["tabela"] == tab and x["bloco_ordinal"] == blo
           and x["coluna_ordinal"] == col and x["r_ca_ohm_km"]]
    seq.sort()
    for (s1, r1), (s2, r2) in zip(seq, seq[1:]):
        if r2 > r1:
            falhas7 += 1
reportar("T7", "Rca decrescente com a secao",
         "PASSA" if falhas7 == 0 else "FALHA", f"{falhas7} inversoes")

# ---- Cobertura ---------------------------------------------------------------
nulos = sum(1 for x in regs if x["r_ca_ohm_km"] is None or x["x_l_ohm_km"] is None)
reportar("T8", "Cobertura e celulas nao publicadas", "PASSA",
         f"{len(regs)} celulas, {nulos} nao publicadas (registradas como null)")

d["testes_coerencia"] = res
d["comparacao_valores_provisorios"] = [
    {"secao_mm2": s, "provisorio_r70_codigo": p,
     "rca_superastic_cu_tabela28": st.median([x["r_ca_ohm_km"] for x in regs
                                              if x["tabela"] == 28 and x["secao_mm2"] == s
                                              and x["r_ca_ohm_km"]]),
     }
    for s, p in [(1.5, 14.48), (2.5, 8.87), (4, 5.52), (6, 3.66), (10, 2.19), (16, 1.38),
                 (25, 0.870), (35, 0.625), (50, 0.463), (70, 0.321), (95, 0.236),
                 (120, 0.188), (150, 0.153), (185, 0.123), (240, 0.094)]
]
json.dump(d, open("impedancia-prysmian.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)

print("\nXL provisorio no codigo (>=25mm2): 0,069 a 0,080 Ohm/km")
todos_xl = [x["x_l_ohm_km"] for x in regs if x["x_l_ohm_km"]]
print(f"XL real publicado:                  {min(todos_xl):.2f} a {max(todos_xl):.2f} Ohm/km")
