# Deep Dive — Pricing Analysis

**Bench:** chatwoot-vs-zendesk | **Data:** 2026-05-06

TCO real para 5 / 20 / 50 agents, com e sem AI add-on.

Premissa: precos USD anuais, billing annual (Zendesk monthly = +25% premium). Numeros sao **sticker** vs **real cost** baseados em multipliers documentados.

---

## 1. Pricing reference cards

### Chatwoot (sticker = real, ratio ~1.0-1.2x)

| Tier | $/agent/mes | $/agent/ano | Captain credits/mes |
|------|------------:|------------:|--------------------:|
| Hacker | $0 (max 2 agents, 500 conv/mo, live chat only) | $0 | 0 |
| Startups | $19 | $228 | 300 |
| Business ⭐ | $39 | $468 | 500 |
| Enterprise | $99 | $1.188 | 800 |
| Self-host MIT | $0 license + infra ~$50-200/mo VPS | $600-2.400 + DevOps | Self-managed |
| Captain credits overage | $20 / 1.000 credits | — | — |

[Source: chatwoot.com/pricing fetched 2026-05-06]

### Zendesk (sticker → real 2-3x)

| Tier | $/agent/mes | $/agent/ano (sticker) |
|------|------------:|----------------------:|
| Support Team | $19 | $228 |
| Suite Team | $55 | $660 |
| Suite Growth | $89 | $1.068 |
| Suite Professional ⭐ | $115 | $1.380 |
| Suite Enterprise | $169 | $2.028 |

**Add-ons obrigatorios para parity (sticker / agent / mes):**

| Add-on | Preco |
|--------|------:|
| Copilot | $50 |
| Quality Assurance (QA AI) | $35 |
| Workforce Management (WFM) | $25 |
| Workforce Engagement (QA + WFM) | $50 |
| Advanced Data Privacy & Protection (ADPP) | $50 |
| Contact Center | $50 |

**Bundles com Copilot:**
- Suite Professional + Copilot: $155/agent/mes ($1.860/year)
- Suite Enterprise + Copilot: $209/agent/mes ($2.508/year)

**Vendr median deal:** $47.772/year per customer (com 15% negotiated discount tipico)

[Source: costbench.com/software/help-desk/zendesk/, eesel.ai pricing 2026, Vendr marketplace data]

---

## 2. TCO 5 agentes / 12 meses

### 2.1 Sem AI

| Cenario | Sticker | Real (multiplier) |
|---------|--------:|------------------:|
| **Chatwoot Cloud Startups** | $1.140 | $1.140 (× 1.0) |
| **Chatwoot Cloud Business** | $2.340 | $2.340 (× 1.0) |
| **Chatwoot self-host** ($150 VPS + $600 ops) | $750 | $750-1.500 |
| **Zendesk Suite Team** | $3.300 | $3.300-6.600 (× 1.0-2.0) |
| **Zendesk Suite Growth** | $5.340 | $5.340-10.680 |
| **Zendesk Suite Professional** | $6.900 | $6.900-13.800 |
| **Zendesk Suite Enterprise** | $10.140 | $10.140-20.280 |

### 2.2 Com AI/Copilot equivalente

| Cenario | Sticker | Real |
|---------|--------:|-----:|
| **Chatwoot Cloud Business + Captain 500 credits/mo (incluso)** | $2.340 | $2.340 + $0-200 overage |
| **Chatwoot Cloud Enterprise + Captain 800 credits + voice opt** | $5.940 + voice | $6.500-9.000 |
| **Zendesk Suite Pro + Copilot bundle ($155/agent)** | $9.300 | $9.300-14.000 |
| **Zendesk Suite Enterprise + Copilot bundle ($209)** | $12.540 | $12.540-18.800 |
| **Zendesk Suite Enterprise + Copilot + QA + WFM ($269)** | $16.140 | $16.140-25.000 |
| **Zendesk + AI Agents per-resolution (1.000 res/mo @ $0.85-1.20)** | +$10.200-14.400/year | — |

### 2.3 Side-by-side comparativo a 5 agentes/AI

```
                             Sticker     Real      Multiplier
Chatwoot Cloud Business      $2.340     $2.340     1.0x
Chatwoot Cloud Enterprise    $5.940     $6.500     1.1x
Zendesk Suite Pro+Copilot    $9.300     $11.000    1.2x (bundle)
Zendesk Enterprise+all       $16.140    $20.000+   1.2-1.5x

Delta Chatwoot vs Zendesk equivalent tier: 4-5x base; 3-7x real
```

---

## 3. TCO 20 agentes / 12 meses

### 3.1 Sem AI

| Cenario | Sticker | Real |
|---------|--------:|-----:|
| Chatwoot Cloud Startups | $4.560 | $4.560 |
| **Chatwoot Cloud Business** ⭐ | $9.360 | $9.360 |
| Chatwoot self-host produc-grade ($300/mo infra + 0.1 FTE DevOps ~$15K) | — | $18.600-21.000 |
| Zendesk Suite Team | $13.200 | $20.000-26.400 |
| **Zendesk Suite Pro** | $27.600 | $40.000-55.200 |
| Zendesk Suite Enterprise | $40.560 | $60.000-81.000 |

### 3.2 Com AI

| Cenario | Sticker | Real |
|---------|--------:|-----:|
| **Chatwoot Cloud Business + Captain incluso** | $9.360 | $9.360 + $200-800 overage = ~$10K |
| Chatwoot Cloud Enterprise + Captain | $23.760 | $23.760 + voice opt = ~$28-32K |
| **Zendesk Suite Pro + Copilot bundle** | $37.200 | $50K-75K |
| Zendesk Suite Enterprise + Copilot + WFM/QA/ADPP | $64.560 | $80K-120K |

**Vendr median deal $47.772/year:** valida ratio 2-3x para mid-market 20-30 agents.

### 3.3 Insight chave 20 agentes

Para 20 agents mid-market:
- **Chatwoot Cloud Business** = $9.360/year (sticker = real)
- **Zendesk Suite Pro+Copilot** = $50-75K real

**Delta absoluto: ~$40-65K/year.** Em 5 anos: $200-325K saving.

Para Sinkra businesses, esse delta pode financiar: 1 senior engineer FTE OU 4-6 mid-level FTEs OU multi-year AI infra investment.

---

## 4. TCO 50 agentes / 12 meses

### 4.1 Sem AI

| Cenario | Sticker | Real |
|---------|--------:|-----:|
| **Chatwoot Cloud Business** | $23.400 | $23.400 |
| Chatwoot Cloud Enterprise | $59.400 | $59.400 |
| Chatwoot self-host produc-grade ($500 infra + 0.2 FTE DevOps ~$30K) | — | $36.000-42.000 |
| Zendesk Suite Team | $33.000 | $50K-66K |
| **Zendesk Suite Pro** | $69.000 | $100K-138K |
| Zendesk Suite Enterprise | $101.400 | $150K-203K |

### 4.2 Com AI

| Cenario | Sticker | Real |
|---------|--------:|-----:|
| **Chatwoot Cloud Business + Captain** | $23.400 | $23.400 + $1-2K overage = ~$25K |
| Chatwoot Cloud Enterprise + Captain | $59.400 + voice opt | ~$65-75K |
| **Zendesk Suite Pro + Copilot bundle** | $93.000 | $130K-186K |
| Zendesk Suite Enterprise + Copilot full stack | $161.400 | $200K-300K |

### 4.3 Volume discounts

Vendr data: 25+ seats e multi-year commits = pricing below published. Estimate 15-30% discount viavel pra 50+ agents Zendesk.

Even with 30% discount Zendesk Suite Pro+Copilot 50 agents: $93K × 0.7 = $65K sticker → $90-130K real.

Chatwoot Cloud Business 50 agents: $23.4K (sem desconto). Delta ainda 4-5x.

### 4.4 Insight 50 agentes

Para 50 agents enterprise:
- **Chatwoot Cloud Business** = $23.400/year
- **Chatwoot Cloud Enterprise** (+SSO+audit+sandbox-like) = $59.400/year
- **Zendesk Suite Pro+Copilot real (sem QA/WFM)** = $130K-186K
- **Zendesk Suite Enterprise full stack real** = $200K-300K

Delta enterprise tier: **$140K-250K/year**.

Em 5 anos: **$700K-1.25M saving** pelo OSS path.

**Trade-off:** Chatwoot 50-agent operation precisa internal DevOps capacity (0.2-0.3 FTE) + accept compliance certs publicas absentes.

---

## 5. Captain credits — analise de overage

Premissa: 1 conversa average usa 5-10 Captain operations (auto-resolve attempt + 2-3 copilot suggestions + summary + maybe smart FAQ search). Sem documentacao oficial — modelo speculativo.

| Tier | Credits incl. | Conversas/mo cobertas (5 ops/conv) | Conversas/mo cobertas (10 ops/conv) |
|------|---------------|-----------------------------------:|-------------------------------------:|
| Startups (300) | 300/mo | 60 | 30 |
| Business (500) | 500/mo | 100 | 50 |
| Enterprise (800) | 800/mo | 160 | 80 |

**Para 20 agents mid-market com ~1.000 conversas/mo:**
- Captain Business 500/mo cobre ~50-100 conversas/mo
- Overage: 900-950 conversas/mo NAO cobertas
- Credits adicionais necessarios: 4.500-9.500/mo
- Custo overage: $90-190/mo = $1.080-2.280/year

**TCO atualizado Chatwoot Business 20 agents real:** $9.360 + $1-2K overage = ~$10-11K/year.

**Concern aberto:** sem documentacao do consumo real, este modelo e estimativa. Buyer **deveria exigir** disclosure ou testar em pilot Chatwoot Cloud antes de commit Business 20+ agents.

---

## 6. Hidden costs

### 6.1 Chatwoot

| Cost | Trigger |
|------|---------|
| Meta WhatsApp message fees | Passthrough (sem markup Chatwoot) |
| Captain credits overage | Volume > tier inclusive |
| Voice/Video addon | Only Enterprise (preco sob consulta) |
| Self-host: DevOps time | 0.05-0.3 FTE depending on scale |
| Self-host: Infra | $50-500/mo |
| Self-host: Captain LLM (OpenAI key cliente) | Consumed at OpenAI rates separate |
| Migration in/out | Free (self-host = full control DB) |

### 6.2 Zendesk

| Cost | Trigger |
|------|---------|
| Meta WhatsApp message fees | Passthrough |
| Voice Talk minute fees | Carrier costs extra |
| Per-resolution AI Agents | NAO publico; estimate $0.85-1.20/res |
| Add-ons (Copilot, QA, WFM, ADPP, Contact Center) | $25-50/agent each |
| Implementation services | Custom pricing (Professional Services) |
| Sandbox extra environments | Enterprise tier only |
| Switching cost off-platform | Historicamente alto (data export limits) |
| Annual price increase | Documented 5-10% YoY |

---

## 7. Multipliers de cenario

| Cenario | Chatwoot multiplier | Zendesk multiplier |
|---------|--------------------:|-------------------:|
| Solo / 2-agent founder | 1.0× ($0 Hacker) | inviavel ($55+/agent min) |
| PME 5 agents | 1.0× | 2.0× |
| Mid-market 20 agents | 1.0× | 2.0-2.7× |
| Enterprise 50+ agents | 1.0-1.2× | 2.5-3.0× (mas com volume discount 15-30%) |
| Self-host all scenarios | depends on DevOps cost | N/A |

---

## 8. Recomendacao por scale

### 8.1 1-10 agents

**Chatwoot Cloud Hacker → Startups path** = TCO mais baixo do mercado.
- Hacker $0 ate 2 agents
- Startups $228/agent/year
- Captain incluso 300 credits

Zendesk Support Team $19/agent/year e proximo no entry mas missing omnichannel (so email+ticketing+FB+X).

### 8.2 10-50 agents (PME → mid-market)

**Chatwoot Cloud Business** ⭐ = sweet spot.
- $39/agent/mo = $468/agent/year sticker = real
- 500 Captain credits/mo + Teams + Automation + SLA

Zendesk Suite Pro+Copilot bundle e 4-6x mais expensive em real cost. Justifica-se apenas se compliance/marketplace sao must.

### 8.3 50-200 agents (mid-market → enterprise)

**Empate categorical.**
- Chatwoot Cloud Business OR Cloud Enterprise = $23K-119K/year
- Chatwoot self-host EE w/ paid support = $36K-50K/year com customer-controlled compliance
- Zendesk Suite Pro+Copilot OR Enterprise = $130K-300K/year real

Decisao: capacidade DevOps interna + compliance posture necessaria + procurement preference SaaS vs OSS.

### 8.4 200+ agents (enterprise)

Beyond this benchmark scope. Both have enterprise contracts negotiated. Volume discounts kick in. Real comparison requires RFQ.

---

## 9. Sources

- https://www.chatwoot.com/pricing (fetched 2026-05-06)
- https://www.zendesk.com/pricing/ (via WebSearch 2026-05-06)
- costbench.com/software/help-desk/zendesk/
- eesel.ai/blog/zendesk-support-pricing-explained-in-2025 (2026 series)
- Vendr marketplace data ($47.772 median)
- chatsy.app/blog/zendesk-pricing-breakdown-2026
- saasworthy.com/blog/zendesk-pricing-plans

---

## 10. Caveat — bench-score 3-way

Para o consolidado 3-way (Chatwoot vs Zendesk vs Octadesk):
- Octadesk pricing entry **R$79/mo** (exato per-agent nao detalhado publicamente)
- Octadesk com 10 agents BR estimated R$500-1.000/mo = $1.000-2.000/year — competitivo com Chatwoot Cloud
- **Tensao:** Octadesk pode ser superior em **TCO + BR-fit** combined para PME BR. Validar em par 3.
