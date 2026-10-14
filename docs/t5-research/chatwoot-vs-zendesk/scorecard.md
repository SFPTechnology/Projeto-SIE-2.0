# Scorecard — Chatwoot vs Zendesk

**Bench:** chatwoot-vs-zendesk
**Data:** 2026-05-06
**Metodo:** Score 0-100 por dimensao × peso → soma ponderada (escala 0-100).

## TL;DR

**Empate tecnico** (Chatwoot 78.85 vs Zendesk 79.05 — delta 0.2 pts em escala 100).

Confirma a hipotese central: **no-clear-winner overall**. A escolha depende de cenario:

- **SMB / PME / e-commerce sem burden compliance:** Chatwoot vence
- **Enterprise / regulated industries / scale enterprise:** Zendesk vence
- **Mid-market 20 agents:** empate, decisao depende de preferencia procurement vs DevOps

---

## Tabela consolidada

| Dim | Nome | Peso | Chatwoot | Zendesk | Delta | Vencedor dim | Confidence |
|-----|------|-----:|---------:|--------:|------:|--------------|-----------|
| C1 | Canais nativos | 15% | 92 | 95 | -3 | Zendesk (small) | H |
| C2 | AI capability | 20% | 75 | 88 | -13 | Zendesk (clear) | H/M |
| C3 | Pricing transparency / TCO | 15% | **95** | 50 | +45 | **Chatwoot (clear)** | H |
| C4 | Governance / Compliance | 10% | 55 | **95** | -40 | **Zendesk (clear)** | H |
| C5 | Ecosystem / Marketplace | 10% | 60 | **95** | -35 | **Zendesk (clear)** | H |
| C6 | Comunidade / Maturidade | 10% | 78 | 92 | -14 | Zendesk (scale) | H/M |
| C7 | Flexibilidade | 10% | **100** | 35 | +65 | **Chatwoot (no equiv)** | H |
| C8 | Brasil-fit | 10% | 65 | 80 | -15 | Zendesk (turnkey) | H |
| | **TOTAL ponderado** | 100% | **78.85** | **79.05** | -0.20 | **Empate tecnico** | — |

### Visualizacao de ponderacao

```
Chatwoot weighted:
  C1: 13.80   ████████████░
  C2: 15.00   ███████████████
  C3: 14.25   ██████████████░
  C4:  5.50   █████░
  C5:  6.00   ██████
  C6:  7.80   ████████
  C7: 10.00   ██████████
  C8:  6.50   ██████░
  ─────────
  78.85

Zendesk weighted:
  C1: 14.25   ██████████████░
  C2: 17.60   █████████████████░
  C3:  7.50   ███████░
  C4:  9.50   █████████░
  C5:  9.50   █████████░
  C6:  9.20   █████████
  C7:  3.50   ███░
  C8:  8.00   ████████
  ─────────
  79.05
```

**Padrao visivel:** Chatwoot ganha em C3+C7 (pricing+flex). Zendesk ganha em C2+C4+C5 (AI+compliance+ecosystem). Score total quase identico — confirma trade-off categorical.

---

## Detalhamento por dimensao

### C1 — Canais nativos (15%)

**Chatwoot: 92** — 10 canais nativos incluindo Telegram + TikTok + 3 BSP options WhatsApp; voice e add-on Enterprise; X removido. WhatsApp BYOC e diferencial real.

**Zendesk: 95** — 10 canais nativos incluindo Apple Business Chat + voice Talk first-class; Telegram/TikTok via marketplace.

**Delta:** -3. Zendesk ganha por margem pequena (Voice + Apple BC + Twitter ainda nativo), Chatwoot ganha em Telegram + TikTok + BSP-flexibility.

### C2 — AI capability (20%)

**Chatwoot: 75** — Captain AI nativo, built-in. Trade-off: deflection rate nao publicada, credit consumption opaca, maturidade <2 anos.

**Zendesk: 88** — AI Agents (post-Ultimate.ai) + Copilot + QA AI + WFM. Customer outcomes publicados (39-92% resolucao). Productivity 20% Copilot. Trade-off: per-resolution AI Agents pricing nao publico.

**Delta:** -13. Zendesk vence em outcomes publicados e breadth de produtos AI especializados (QA, WFM dedicated). Chatwoot vence em simplicidade e built-in nature.

### C3 — Pricing transparency e TCO real (15%)

**Chatwoot: 95** — Tiers publicos claros. Self-host = $0. Sticker-to-real ratio 1.0-1.2x.

**Zendesk: 50** — $19-$169 base + add-ons necessarios (Copilot $50, QA $35, WFM $25, ADPP $50). Real-world multiplier 2-3x. Vendr median deal $47.772/year. AI Agents per-resolution opaco.

**Delta:** +45. Chatwoot **clear winner** — gap mais expressivo do bench (45 pts).

### C4 — Governance / Compliance (10%)

**Chatwoot: 55** — GDPR DPA. SOC2 Cloud implicit. ISO/FedRAMP/HIPAA NAO listadas. EU residency Cloud nao user-selectable. Self-host = escape valve.

**Zendesk: 95** — SOC2 Type II + ISO 27001/27018/27701 + FedRAMP + GDPR BCR + HIPAA BAA + multi-region (US/EU/AU/JP).

**Delta:** -40. Zendesk **clear winner** — gap quase categorical.

### C5 — Ecosystem / Marketplace (10%)

**Chatwoot: 60** — Tens of named integrations + API + DB access self-host. Sem marketplace curado.

**Zendesk: 95** — 1.977 apps de 1.136 vendors. 75% ARR marketplace-impacted. AI 21.54%. Sandbox Enterprise.

**Delta:** -35. Zendesk **clear winner** — network effects sao moat.

### C6 — Comunidade / Maturidade (10%)

**Chatwoot: 78** — GitHub 29.1k stars. G2 4.4. 9 anos. Monthly minor releases.

**Zendesk: 92** — G2 6.000+ reviews 4.3. 14.8% market share. 19 anos. 88% ease of use cite. BR team.

**Delta:** -14. Zendesk vence em scale, Chatwoot vence em transparencia/dev cadence.

### C7 — Flexibilidade (10%)

**Chatwoot: 100** — MIT self-host full source. 4 deployment options. WhatsApp BYOC. Vendor lock-in minimal.

**Zendesk: 35** — Cloud-only proprietary. Self-host impossivel. Vendor lock-in maximum. Sandbox Enterprise e paliativo (positivo) mas dentro de guardrails Zendesk.

**Delta:** +65. **Sem equivalente categorical** — gap mais profundo do bench. O score de 35 do Zendesk reflete que sandbox + apps framework + API openness existem (nao zera), mas nao se aproxima de self-host MIT.

### C8 — Brasil-fit (10%)

**Chatwoot: 65** — BYOC permite BR BSP. PT-BR UI. Shopify nativa. Sem BRL pricing, VTEX, RD, Pix, BR team.

**Zendesk: 80** — BRL publicado. Suporte BR. Sales BR. Marketplace community RD Station. Caveats: BRL absoluto proibitivo para PME (R$359 = 5x Octadesk).

**Delta:** -15. Zendesk vence em turnkey BR; ambos perdem para Octadesk/Take Blip/Zenvia em integracoes BR-specific.

---

## Scores ajustados por cenario

### Cenario A: SMB / PME / 5 agents / no compliance burden

| Player | Score |
|--------|------:|
| Chatwoot | **89** |
| Zendesk | 65 |

**Razao:** TCO e flexibility dominam para PME. Zendesk Suite Team ($55 × 5 × 12 = $3.300) ja e 3x Chatwoot Startups ($1.140), antes de add-ons. Compliance posture do Zendesk e overkill para PME.

### Cenario B: Mid-market / 20 agents / some compliance

| Player | Score |
|--------|------:|
| Chatwoot | 80 |
| Zendesk | 82 |

**Razao:** Empate. Decisao depende de capacidade DevOps interna (favorece Chatwoot) vs preferencia procurement por SaaS (favorece Zendesk).

### Cenario C: Enterprise / 50 agents / regulated industry (HIPAA, FedRAMP, EU)

| Player | Score |
|--------|------:|
| Chatwoot Cloud | 65 |
| Zendesk | **92** |

**Razao:** Compliance certs publicas + ecosystem + scale enterprise. **EXCETO** se cliente roda Chatwoot self-host Enterprise edition com paid support em sua propria region — ai equipara compliance posture customer-controlled.

### Cenario D: BR / PME / e-commerce

| Player | Score |
|--------|------:|
| Chatwoot | **75** |
| Zendesk | 60 |

**Razao:** Pricing BRL Zendesk (R$359/agent Suite Team) inviabiliza PME. Chatwoot self-host = $0. **Mas:** Octadesk/Take Blip podem ser superiores ainda — pares 2/3 do pipeline vao validar.

### Cenario E: Global SaaS / 30 agents / EU GDPR strict + multi-region

| Player | Score |
|--------|------:|
| Chatwoot self-host EU | 88 |
| Chatwoot Cloud | 60 |
| **Zendesk (com Data Center Location addon ativado)** | **95** |

**Razao:** Para SaaS multi-region com burden de GDPR strict, Zendesk Dublin + multi-region + BCR aprovada e o caminho turnkey. Chatwoot self-host EU e equivalente em compliance posture mas exige ops.

---

## Confidence summary

| Confidence level | Dimensions |
|------------------|------------|
| **H (high)** | C1 (canais), C3 (pricing), C5 (marketplace numbers), C7 (flex), C8 (BR-fit) |
| **M (medium)** | C2 (AI per-resolution opacity Zendesk + Chatwoot maturity), C4 (compliance absence inferred for Chatwoot), C6 (Chatwoot G2 review count estimated) |
| **L (low)** | None |

5/8 dimensions H, 3/8 M, 0/8 L. **Bench tem alto rigor evidencial.**

---

## Tiebreakers para o bench-score 3-way

Se o bench-score 3-way (Chatwoot vs Zendesk vs Octadesk) precisar quebrar empates entre Chatwoot e Zendesk, considerar:

1. **Diversidade de modelo:** se o set ja inclui um SaaS BR-native (Octadesk), Chatwoot adiciona mais diversidade categorial (OSS) que Zendesk (mais um SaaS proprietary)
2. **Modelo economico oposto:** Chatwoot $0-99 vs Zendesk $19-169+addons cobrem a curva de pricing inteira — Octadesk no meio (R$79+)
3. **Tensao compliance:** se decisor tem requirement HIPAA/FedRAMP, Zendesk e mandatory; senao Chatwoot tem TCO advantage 3-5x

## Anti-patterns evitados neste scorecard

- ❌ Inflar Chatwoot porque foi o "preferido" do tech-research (92.5)
- ❌ Deflar Zendesk em compliance porque "OSS sempre vence"
- ❌ Sumarizar TCO em vez de mostrar contas detalhadas
- ❌ Claim equivalencia sem citar fonte
- ❌ Ignorar diferenciais reais do Zendesk (marketplace, compliance, voice)
- ❌ Ignorar weaknesses do Chatwoot (Captain credit opacity, no enterprise certs)
