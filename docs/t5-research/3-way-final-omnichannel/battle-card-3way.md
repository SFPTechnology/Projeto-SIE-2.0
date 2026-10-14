# Battle Card — Omnichannel Helpdesk 2026

**Top 4 finalistas:** Chatwoot · Zendesk · Octadesk · Intercom
**Tese central:** decisao e persona-driven; nao ha vencedor unico. Empate tecnico Zendesk (74.95) vs Chatwoot (74.40) no eixo neutro; Octadesk (63.89) e Intercom (61.25) vencem em segmentos especificos.

---

## 1. Quadro 4 players

| | **Chatwoot** | **Zendesk** | **Octadesk** | **Intercom** |
|---|---|---|---|---|
| **Tipo** | OSS+Cloud (MIT) | SaaS Enterprise | SaaS BR | SaaS AI-first |
| **Score neutro** | 74.40 | **74.95** | 63.89 | 61.25 |
| **TCO 5 agents/ano** | ~$324 self-host / $1.140 Cloud | ~$3.300-6.600 | ~R$18,5k (~$3.540) | ~$5.304 |
| **TCO 50 agents/ano** | ~$16.800 self-host / $61.800 Cloud | ~$130k-300k real | ~$60k-120k (gated) | ~$241.536 |
| **AI engine** | Captain (credits, modelo nao disclosed) | Zendesk AI Agents (post-Ultimate.ai, breadth maior) | WOZ (ChatGPT-based, BR-native) | Fin Apex 1.0 (patenteado, RAG 6 steps) |
| **AI deflection publicado** | NAO publicado | 39-92% range (customer outcomes) | Marketing claim 80% (nao validado) | **51-67% benchmarked (Lightspeed 65%)** |
| **WhatsApp** | BYOC (Meta direct + 360Dialog + Twilio + qualquer BSP) | Sunshine broker ($495/mo + variable markup) | Cloud-Direct oficial Meta (BR turnkey) | Meta-direct (outbound exige add-on $99/mo) |
| **Compliance** | D4=55 (customer-controlled) | **D4=95 (SOC2+ISO+FedRAMP+HIPAA+BCR)** | D4=45 (LGPD apenas) | D4=80 (ISO27001+GDPR) |
| **Self-host** | **D7=100 (categorical)** | D7=35 | D7=25 | D7=0 |
| **BR-fit** | D8=60 | D8=60 | **D8=95 (categorical)** | D8=35 |
| **In-app messaging** | D9=50 | D9=70 | D9=40 | **D9=95 (categorical)** |
| **Vence em** | Pricing + flexibilidade + cost-conscious | Compliance + scale + multinacional | BR PME e-commerce | SaaS B2B in-app heavy |
| **NAO escolha se** | Compliance HIPAA/FedRAMP mandatory + sem DevOps | TCO BRL PME inviavel | Multinacional regulado | BR-only ou volume alto (Fin per-res cliffa) |

---

## 2. Ranking por persona

| Persona | 1o | 2o | Delta |
|---|---|---|---|
| **SMB BR e-commerce** (5-10 agents, <=1k conv/mo) | **Chatwoot 75.84** | Octadesk 70.43 | -5.41 |
| **Mid-market BR** (50-100 agents, compliance baixo) | **Chatwoot 74.48** | Octadesk 65.75 | empate tecnico c/ Zendesk |
| **Mid-market BR** (50-100 agents, compliance alto / SSO) | **Zendesk 75.13** | Chatwoot 74.48 | -0.65 (empate tecnico) |
| **Enterprise BR multinacional** (100+ agents, regulado) | **Zendesk 79.44** | Chatwoot 70.16 | -9.28 |
| **Global SaaS B2B** (in-app heavy, EN-first) | **Intercom** (apesar score 3o) | Zendesk 77.93 | tiebreaker D9=95 |
| **Global GDPR strict** (EU-residency mandatory) | **Chatwoot self-host EU** | Zendesk Dublin BCR | tiebreaker D7=100 |

**Players em TOP-2 em pelo menos 1 persona:** Chatwoot (5/5 — unico) · Zendesk (4/5) · Octadesk (1/5) · Intercom (0/5 neutro, vence apenas Persona D por tiebreaker D9).

---

## 3. Decision tree (5 linhas)

1. **BR-only?** Sim -> leque Chatwoot/Octadesk/Zendesk (descartar Intercom).
2. **SMB BR com DevOps interno?** -> Chatwoot self-host ($324-600/yr).
3. **SMB BR sem DevOps?** -> Octadesk (turnkey BR + bundle LWSA Bling/Tray/Vindi).
4. **Mid-market+ regulado (HIPAA/FedRAMP/SOC2)?** -> Zendesk; senao Chatwoot self-host (TCO 3-5x menor).
5. **Global in-app heavy?** -> Intercom; **GDPR strict EU?** -> Chatwoot self-host EU.

---

## 4. Tiebreakers criticos (top 5)

1. **SSO/SAML/SCIM mandatorio?** -> **Zendesk** (nativo Pro+).
2. **DevOps interno disponivel (1+ pessoa Docker/K8s)?** -> **Chatwoot** viabilizado.
3. **Bundle Bling/Tray/Vindi/iFood BR e dependencia hard?** -> **Octadesk**.
4. **In-app messenger (web SDK + mobile SDK + product tours) e core do produto?** -> **Intercom** (D9=95 categorical).
5. **HIPAA/FedRAMP/SOC2 Type II ou EU residency strict?** -> **Zendesk** OU **Chatwoot self-host EU**.

---

## 5. Cliffs economicos chave

- **Chatwoot self-host:** para de fazer sentido >100-150 agents (precisa SRE dedicado 0.5+ FTE + uptime SLA 99.9%).
- **Zendesk Suite Pro -> Enterprise:** forcado quando sandbox/multi-brand/HIPAA-BAA/audit detalhado entram.
- **Intercom Fin per-resolution:** cliffa exponencialmente >5.000 res/mo ($60k/yr so AI); 50k res/mo = $300k/yr so AI.
- **Octadesk:** sem caminho intra-Octadesk para enterprise regulado ou multi-region -> forced migration para Zendesk/Chatwoot.

---

## 6. Confidence global

- **5/9 dimensoes High** (D1, D3, D5, D6, D7) — todos os players.
- **3/9 dimensoes Medium** (D2 deflection Captain/WOZ nao publicado; D4 Intercom inferido; D8 Zendesk reconciliacao).
- **1/9 dimensao Low misto** (D8 Intercom untested; D9 Octadesk untested).
- **5 curiosity queries pendentes** (Captain deflection real; WOZ deflection real; Captain-vs-Fin head-to-head; Zendesk AI Agents per-res publico; hallucination rate cross-vendor).

---

## 7. Proximo passo

```
1. Decisor classifica operacao em 1 das 4 personas (SMB BR / Mid BR / Enterprise BR / Global)
2. Aplica decision tree (secao 3) -> top-2 candidatos
3. Cruza com tiebreakers (secao 4) -> finalist
4. POC 30 dias do top-2 da persona com:
   - Deflection AI real (Captain vs Fin vs Zendesk AI Agents vs WOZ)
   - TCO real medido (incluindo add-ons + Meta passthrough + DevOps hours)
   - WhatsApp delivery rate + latency + template approval flow
5. Decisao final via dados de POC, NUNCA via scorecard isolado
```

---

**Disclaimer:** RESEARCH agregado, nao recomendacao vinculante. Cenarios "estilo Hub" sao perfis genericos. Decisao final exige due diligence comercial + POC + validacao com BSP local.

**Cross-refs:** `consolidated-scorecard.md` · `final-recommendation-matrix.md` · `tco-comparison-4-players.md` · `ai-capability-ranking.md` · `whatsapp-integration-ranking.md`

*Battle Card 3-way | Bench 3-way-final-omnichannel | 2026-05-06*
