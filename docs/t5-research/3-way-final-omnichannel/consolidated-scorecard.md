# Consolidated Scorecard — 3-Way Final Omnichannel (Chatwoot vs Zendesk vs Intercom vs Octadesk)

**Bench:** 3-way-final-omnichannel
**Fase:** A (5 de 10 artefatos)
**Data:** 2026-05-06
**Metodo:** Reconciliacao de 3 paired benches (Chatwoot/Zendesk, Intercom/Chatwoot, Octadesk/Zendesk) em matriz unica 4 players × 9 dimensoes consolidadas. Score 0-100 por celula com source explicito + confidence H/M/L. Pesos neutros do `metadata.json`. Recalibracao para 4 personas.

## TL;DR

**Empate tecnico no eixo neutro entre Zendesk (74.95) e Chatwoot (74.40)** — delta 0.55, dentro do ruido estatistico. Octadesk (63.89) e Intercom (61.25) ficam abaixo no eixo neutro mas SAO competitivos em personas especificas.

**Decisao real e persona-driven:**

| Persona | 1o | 2o | Verdict |
|---|---|---|---|
| **SMB BR e-commerce** | Chatwoot 75.84 | Octadesk 70.43 | Chatwoot vence; Octadesk e alternativa zero-DevOps |
| **Mid-market BR** | Zendesk 75.13 | Chatwoot 74.48 | Empate tecnico (delta 0.65); decisao por compliance |
| **Enterprise BR multinacional** | Zendesk 79.44 | Chatwoot 70.16 | Zendesk clear winner (delta +9.28) |
| **Global SaaS B2B (EU+US)** | Zendesk 77.93 | Chatwoot 71.19 | Zendesk vence; Intercom 3o apesar de in-app premium |

---

## Dimensoes consolidadas (9 dimensoes, pesos neutros)

| Dim | Nome | Peso |
|---|---|---:|
| D1 | Canais nativos (incluindo WhatsApp depth) | 12% |
| D2 | AI capability + transparencia + deflection publicado | 18% |
| D3 | Pricing transparency + TCO real | 15% |
| D4 | Governance / Compliance | 12% |
| D5 | Ecosystem / Marketplace / integracoes | 8% |
| D6 | Comunidade / Maturidade / reviews | 8% |
| D7 | Flexibilidade (self-hosted, customizacao, sovereignty) | 10% |
| D8 | Brasil-fit (BSP local, BRL pricing, suporte PT-BR, integracoes BR) | 12% |
| D9 | In-app messaging strength | 5% |

---

## Matriz neutra 4 × 9

| Dim | Peso | Chatwoot | Zendesk | Intercom | Octadesk | Vencedor dim |
|---|---:|---:|---:|---:|---:|---|
| D1 | 12 | 93 | 88 | 60 | 92 | Chatwoot (Octadesk +0.5 atras) |
| D2 | 18 | 65 | **87** | 80 | 70 | **Zendesk (clear)** |
| D3 | 15 | **92** | 55 | 50 | 65 | **Chatwoot (clear)** |
| D4 | 12 | 55 | **95** | 80 | 45 | **Zendesk (clear)** |
| D5 | 8 | 65 | **95** | 85 | 60 | **Zendesk (clear)** |
| D6 | 8 | 78 | 91 | 85 | 55 | Zendesk |
| D7 | 10 | **100** | 35 | 0 | 25 | **Chatwoot (categorical)** |
| D8 | 12 | 60 | 60 | 35 | **95** | **Octadesk (clear)** |
| D9 | 5 | 50 | 70 | **95** | 40 | **Intercom (categorical)** |
| **TOTAL** | 100 | **74.40** | **74.95** | **61.25** | **63.89** | Empate tecnico Z/C |

### Decomposicao ponderada — totais neutros

```
Chatwoot ponderado (74.40):
  D1 (canais)        11.16  ███████████░
  D2 (AI)            11.70  ████████████
  D3 (pricing)       13.80  ██████████████
  D4 (compliance)     6.60  ███████
  D5 (ecosystem)      5.20  █████░
  D6 (maturity)       6.24  ██████
  D7 (flexibility)   10.00  ██████████   <- categorical winner
  D8 (BR-fit)         7.20  ███████░
  D9 (in-app)         2.50  ██░
                    ───────
                     74.40

Zendesk ponderado (74.95):
  D1 (canais)        10.56  ██████████░
  D2 (AI)            15.66  ████████████████   <- forte
  D3 (pricing)        8.25  ████████░
  D4 (compliance)    11.40  ███████████   <- categorical
  D5 (ecosystem)      7.60  ████████   <- categorical
  D6 (maturity)       7.28  ███████
  D7 (flexibility)    3.50  ███░
  D8 (BR-fit)         7.20  ███████░
  D9 (in-app)         3.50  ███░
                    ───────
                     74.95

Intercom ponderado (61.25):
  D1 (canais)         7.20  ███████░
  D2 (AI)            14.40  ██████████████░   <- forte
  D3 (pricing)        7.50  ███████░
  D4 (compliance)     9.60  ██████████
  D5 (ecosystem)      6.80  ███████
  D6 (maturity)       6.80  ███████
  D7 (flexibility)    0.00      <- categorical loser
  D8 (BR-fit)         4.20  ████░
  D9 (in-app)         4.75  █████   <- categorical winner
                    ───────
                     61.25

Octadesk ponderado (63.89):
  D1 (canais)        11.04  ███████████
  D2 (AI)            12.60  ████████████░
  D3 (pricing)        9.75  █████████░
  D4 (compliance)     5.40  █████░
  D5 (ecosystem)      4.80  █████
  D6 (maturity)       4.40  ████░
  D7 (flexibility)    2.50  ██░
  D8 (BR-fit)        11.40  ███████████   <- categorical winner
  D9 (in-app)         2.00  ██
                    ───────
                     63.89
```

**Padroes visiveis:**

- Chatwoot e Zendesk somam **identicas** (74.40 vs 74.95) por **caminhos opostos**: Chatwoot via D3+D7 (pricing + flexibility) vs Zendesk via D2+D4+D5 (AI + compliance + ecosystem)
- Intercom paga D7=0 cara — e a unica explicacao para ficar atras de Octadesk no neutro
- Octadesk vive de D1+D8 (canais BR + BR-fit) — categorical vencedor em D8

---

## Personas — recalibracoes

### Persona A — SMB BR e-commerce (5-10 agents, <=1k conv/mes)

**Pesos recalibrados:** D1=14, D2=8, D3=20, D4=4, D5=8, D6=4, D7=10, D8=27, D9=5
**Logica:** WA depth + BR-fit + TCO dominam. Compliance enterprise quase irrelevante. AI moderado, in-app irrelevante.

| Player | Score | Delta vs lider |
|---|---:|---:|
| **Chatwoot** | **75.84** | — |
| Octadesk | 70.43 | -5.41 |
| Zendesk | 68.52 | -7.32 |
| Intercom | 52.40 | -23.44 |

```
Chatwoot 75.84  ███████████████░
Octadesk 70.43  ██████████████░
Zendesk  68.52  █████████████░
Intercom 52.40  ██████████░
```

**Veredito:** **Chatwoot** vence. Octadesk e a alternativa pragmatica zero-DevOps com BR-fit superior. Zendesk e Intercom inviaveis para esta persona por TCO BRL e ausencia BR-fit.

**Tiebreaker:** Se equipe tem DevOps interno → Chatwoot self-host ($0). Se NAO tem DevOps + bundle Locaweb (Bling/Tray/Vindi) → Octadesk.

---

### Persona B — Mid-market BR (50-100 agents, ~10k conv/mes)

**Pesos recalibrados:** D1=15, D2=15, D3=12, D4=10, D5=10, D6=8, D7=10, D8=15, D9=5
**Logica:** Equilibrio. AI moderado, compliance moderado, BR-fit ainda dominante, TCO menos critico.

| Player | Score | Delta vs lider |
|---|---:|---:|
| **Zendesk** | **75.13** | — |
| Chatwoot | 74.48 | -0.65 |
| Octadesk | 65.75 | -9.38 |
| Intercom | 60.30 | -14.83 |

```
Zendesk  75.13  ███████████████░
Chatwoot 74.48  ██████████████░    <- empate tecnico
Octadesk 65.75  █████████████░
Intercom 60.30  ████████████░
```

**Veredito:** EMPATE TECNICO Zendesk vs Chatwoot (delta 0.65). Octadesk competitivo em terceiro mas atras em D2/D4/D5. Decisao depende de tiebreakers compliance + DevOps + WhatsApp volume.

**Tiebreaker:**
- SSO/SAML obrigatorio + sem DevOps → **Zendesk**
- DevOps maduro + cost-conscious → **Chatwoot self-host**
- BR-only operacao + bundle LWSA → **Octadesk** competitivo

---

### Persona C — Enterprise BR multinacional (100+ agents, regulado, multi-region)

**Pesos recalibrados:** D1=10, D2=12, D3=8, D4=22, D5=12, D6=10, D7=8, D8=10, D9=8
**Logica:** Compliance e ecosystem dominam. TCO baixo peso (orcamento existe). BR-fit baixo (multinacional aceita USA/EU).

| Player | Score | Delta vs lider |
|---|---:|---:|
| **Zendesk** | **79.44** | — |
| Chatwoot | 70.16 | -9.28 |
| Intercom | 67.00 | -12.44 |
| Octadesk | 60.10 | -19.34 |

```
Zendesk  79.44  ████████████████
Chatwoot 70.16  ██████████████
Intercom 67.00  █████████████░
Octadesk 60.10  ████████████
```

**Veredito:** **Zendesk** clear winner (delta +9.28 vs Chatwoot). Compliance posture (SOC2 + ISO + FedRAMP + HIPAA + BCR + multi-region) e categorical para enterprise regulado. Chatwoot self-host EU customer-controlled e backstop viavel mas exige DevOps maduro. Octadesk fora do segmento.

**Tiebreaker:**
- Healthcare BR / fintech BR regulado / governo → **Zendesk** mandatory
- Buyer aceita Chatwoot self-host EU + customer-controlled compliance → **Chatwoot self-host** (TCO 3-5x menor)

---

### Persona D — Global SaaS B2B (20-30 agents, EU+US, GDPR strict, in-app heavy)

**Pesos recalibrados:** D1=10, D2=20, D3=10, D4=15, D5=10, D6=8, D7=10, D8=2, D9=15
**Logica:** AI sofisticada + in-app messenger + compliance dominam. BR-fit quase zero. Self-host relevante por GDPR.

| Player | Score | Delta vs lider |
|---|---:|---:|
| **Zendesk** | **77.93** | — |
| Chatwoot | 71.19 | -6.74 |
| Intercom | 69.25 | -8.68 |
| Octadesk | 57.25 | -20.68 |

```
Zendesk  77.93  ███████████████░
Chatwoot 71.19  ██████████████░
Intercom 69.25  █████████████░    <- surpresa: 3o apesar de in-app premium
Octadesk 57.25  ███████████░
```

**Veredito:** **Zendesk** vence (77.93). **Surpresa diagnostica:** Intercom fica em 3o (69.25) apesar de in-app strength D9=95 e AI D2=80, porque self-host=0 + compliance moderado = penalidade composta. Chatwoot 2o (71.19) por self-host EU + AI razoavel + canais nativos.

**Tiebreaker:**
- In-app messaging + AI sao DECISIVOS + budget enterprise → **Intercom** (apesar do score mais baixo, polish em D9 e categorical)
- Compliance + scale + ecosystem → **Zendesk**
- GDPR strict EU residency + cost-conscious → **Chatwoot self-host EU**

---

## Sumario de rankings — visao agregada

| Persona | 1o | 2o | 3o | 4o |
|---|---|---|---|---|
| Neutral | Zendesk 74.95 | Chatwoot 74.40 | Octadesk 63.89 | Intercom 61.25 |
| SMB BR e-com | **Chatwoot 75.84** | Octadesk 70.43 | Zendesk 68.52 | Intercom 52.40 |
| Mid-market BR | **Zendesk 75.13** | Chatwoot 74.48 | Octadesk 65.75 | Intercom 60.30 |
| Enterprise BR multi | **Zendesk 79.44** | Chatwoot 70.16 | Intercom 67.00 | Octadesk 60.10 |
| Global SaaS B2B | **Zendesk 77.93** | Chatwoot 71.19 | Intercom 69.25 | Octadesk 57.25 |

**Players que aparecem em TOP-2 em pelo menos 1 persona:**

| Player | TOP-2 personas | Verdict |
|---|---|---|
| Chatwoot | 5 (todas) | Unico que mantem competitividade em TODAS as personas |
| Zendesk | 4 (todas exceto SMB BR) | Default para mid-market+ |
| Octadesk | 1 (SMB BR) | Especialista BR PME |
| Intercom | 0 | Fica 3o ou 4o em todas as personas |

---

## Confidence summary

| Confidence | Dimensoes | Players afetados |
|---|---|---|
| **H (high)** | D1, D3, D5, D6, D7 | Todos |
| **M (medium)** | D2 (Captain/WOZ deflection nao publicado), D4 (Intercom inferido), D8 (Zendesk reconciliacao bench-1 vs bench-3) | Chatwoot, Octadesk, Intercom, Zendesk |
| **L (low)** | D8 Intercom (untested), D9 Octadesk (untested) | Intercom, Octadesk |

**Bench tem alto rigor evidencial (5/9 dimensoes H, 3/9 M, 1/9 L misto).** Untested cells documentados em `triangulation-analysis.md` para resolucao em fase B.

---

## Observacoes globais

1. **Persona-neutrality nao existe neste mercado.** Os 4 players ocupam 4 segmentos diferentes; score neutro e diagnostico, nao decisao.
2. **Octadesk e categorical em D8 (BR-fit=95)** mas perde em D2/D4/D5. Vence SMB BR; perde enterprise multinacional por delta -19.
3. **Intercom e categorical em D9 (in-app=95)** mas paga D7=0 caro. Atende SaaS B2B in-app heavy ocidental, NAO BR.
4. **Chatwoot mantem D7=100 + D3=92** competitivos em TODAS as personas — unico player no top-2 de todas.
5. **Zendesk vence em 3 de 4 personas** pela combinacao D4+D5+D6, mas fica atras em SMB BR pelo TCO BRL inviavel (R$359/agent Suite Team = 5x Octadesk).

---

## Anti-patterns evitados

- ❌ Inflar Chatwoot por preferencia OSS
- ❌ Deflar Zendesk em compliance porque "OSS sempre vence"
- ❌ Premiar Intercom por marketing premium quando D7=0 mata score
- ❌ Sumarizar Octadesk como "BR pequeno" quando vence SMB BR objetivamente
- ❌ Misturar bench-1 (mais severo) com bench-3 (mais generoso) sem reconciliar
- ❌ Inventar scores em celulas untested sem flag explicita

## Cross-refs

- Reconciliacoes detalhadas → `triangulation-analysis.md`
- Scores por dimensao com citacoes textuais → `cross-bench-matrix.md`
- Decisao final por persona → `final-recommendation-matrix.md`
- Dados estruturais → `consolidated-scorecard.json`
