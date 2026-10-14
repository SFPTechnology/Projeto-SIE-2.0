# TCO Comparison — 4 Players Lado a Lado (Chatwoot vs Zendesk vs Intercom vs Octadesk)

**Bench:** 3-way-final-omnichannel
**Fase:** A (TCO consolidado)
**Data:** 2026-05-06
**Currency:** USD primario; BRL onde fonte oficial e BR (Octadesk). FX nao modelado (volatilidade ignorada).
**Confidence base:** H Chatwoot/Zendesk/Intercom (pricing oficial publico fetched 2026-05-06); M Octadesk (tier publico H, Suite gated L).

---

## TL;DR

**Em USD anual, ranking por cenario (somente do mais barato pro mais caro):**

| Cenario | 1o (mais barato) | 2o | 3o | 4o |
|---|---|---|---|---|
| **SMB** (5 agents, 1k conv, 30% deflection) | Chatwoot self-host ~$324-1.000/yr | Chatwoot Cloud Startups $1.140 | Octadesk Conversas ~$3.700/yr (R$1.542×12÷5) | Intercom Essential+Fin $5.304 / Zendesk Suite Team $3.300-6.600 |
| **Mid** (20 agents, 5k conv, 50% deflection) | Chatwoot self-host custom $7.428 | Chatwoot Cloud Business $9.840 | Octadesk Sea+AI ~$8.916/yr (R$2.972×12÷5) | Intercom Advanced+Fin $51.840-55.956 / Zendesk Suite Pro+Copilot $50K-75K |
| **Scale** (50 agents, 20k conv, 60% deflection) | Chatwoot self-host custom $16.800 | Chatwoot Cloud Enterprise $61.800 | Octadesk Suite (gated, estimate $50-100K) | Zendesk Suite Pro+Copilot $130K-186K real / Intercom Expert full $241.536 |

**Cliffs principais (1 frase por player):**

- **Chatwoot:** self-host pa ra de fazer sentido quando volume + complexidade exigem 0.3+ FTE DevOps a partir de ~50 agents — daí Cloud Business/Enterprise vira mais barato que manter infra própria.
- **Zendesk:** Suite Pro vira insuficiente sem Copilot+QA+WFM em scale, e Suite Enterprise+stack completo cliffa em $200K-300K real para 50 agents — buy-in só justifica se compliance enterprise (FedRAMP/HIPAA/BCR) for mandatory.
- **Intercom:** Fin AI per-resolution cliffa exponencialmente — 12.000 res/mo @ $0.99 = $11.880/mo *só em AI*, transformando scale em $241K/yr e tornando Intercom proibitivo acima de 5k conv/mo sem deflection delta sustentado >4pp vs concorrentes.
- **Octadesk:** Suite gated atinge gap enterprise (sem SSO/SAML/SCIM/SOC2 publicos confirmados) — cliente que cresce além de PME BR precisa migrar pra Zendesk ou Chatwoot self-host quando compliance regulado for exigido.

---

## 1. Tabela de pricing entry (4 players lado a lado)

| Player | Pricing entry oficial | Cloud | Self-hosted | Modelo | Currency | Confidence |
|---|---|:-:|:-:|---|---|---|
| **Chatwoot** | $0 self-host (MIT) / $19 agent/mo Cloud Startups / $39 Business / $99 Enterprise | ✓ | ✓ MIT | per-agent + Captain credits | USD | H |
| **Zendesk** | $19 Support Team / $55 Suite Team / $115 Suite Pro / $169 Suite Enterprise — billing annual; monthly +25% | ✓ | ✗ | per-agent + add-ons (Copilot $50, QA $35, WFM $25, ADPP $50) | USD | H |
| **Intercom** | $29 Essential / $85 Advanced / $132 Expert per seat — Fin $0.99/resolution | ✓ | ✗ | per-seat + per-resolution AI | USD | H |
| **Octadesk** | R$1.542/mo Conversas / R$2.205 Helpdesk / R$2.972 Sea+AI (G2 mirror, 30 users) / Suite "contato comercial" | ✓ | ✗ | per-conta (escalonamento de users + WA conv/mo) — agents NAO publico granular | BRL | H tier publico, M Sea+AI, L Suite |

**Nota Octadesk:** Tech-research listou "R$79/mes" — site oficial 2026-05-06 mostra entry R$1.542/mes (Conversas). Desvio de ~20x. Considera-se R$1.542 como entry real publicado; R$79 nao reproduzivel hoje.

---

## 2. TCO Cenario SMB — 5 agents, 1.000 conv/mo, 30% deflection target

### 2.1 Setup detalhado

| Item | Chatwoot self-host custom | Chatwoot Cloud Startups | Zendesk Suite Team (sem AI) | Zendesk Suite Team + Copilot | Intercom Essential + Fin | Octadesk Conversas |
|---|---:|---:|---:|---:|---:|---:|
| **Pricing base/mo** | $0 license | $95 (5×$19) | $275 (5×$55) | $275 + $250 (5×$50 Copilot) = $525 | $145 (5×$29) | R$1.542 = ~$295 USD |
| **AI add-on/mo** | OpenAI gpt-4o-mini ~$20 | Captain 300 credits incluso ($0) | — | Copilot bundle incluso acima | Fin: 300 res×$0.99 = $297 | WOZ pricing nao publico (~contato comercial) |
| **Hosting/Ops/mo** | $7 VPS Hetzner CX21 | incluso | incluso | incluso | incluso | incluso |
| **WhatsApp BSP** | Meta passthrough (cliente conecta WABA propria) | Meta passthrough | Meta + Sunshine passthrough | Meta + Sunshine | Meta direto passthrough | Meta direto (Octadesk = BSP integrado) |
| **TCO mes (USD)** | **~$27** | **$95** | **~$275** | **~$525** | **~$442** | **~$295** (sem WOZ) |
| **TCO ano (USD)** | **~$324** | **$1.140** | **~$3.300** | **~$6.300** | **~$5.304** | **~$3.540** (sem WOZ) |
| **TCO ano com multiplier real** | $324-600 (ops+ FTE 0.05) | $1.140 (× 1.0) | $3.300-6.600 (× 1.0-2.0 monthly billing) | $6.300-9.300 | $5.304 (sticker = real) | $3.540-5.000 (Suite WOZ adicional) |
| **Multiplo vs Chatwoot Cloud Startups** | 0.3x | **1.0x baseline** | 2.9x | 5.5x | 4.6x | 3.1x |

### 2.2 Insight SMB

- **Chatwoot self-host custom ($324/yr)** vence absolutamente em TCO se time tem competencia DevOps minima (0.05 FTE). Tradeoff: zero compliance certs publicos.
- **Chatwoot Cloud Startups ($1.140/yr)** = sweet spot SMB sem DevOps: 5-11x mais barato que Intercom, 3-6x mais barato que Zendesk, 3x mais barato que Octadesk.
- **Octadesk Conversas (~$3.540/yr)** competitivo em **BR-fit + zero DevOps + UX PT-BR nativa**. Vence Zendesk e Intercom em TCO; perde pra Chatwoot mas oferece bundle LWSA (Bling/Tray/Vindi) + WhatsApp BSP integrado.
- **Zendesk Suite Team ($3.300/yr sticker, ate $6.600 real)** + Copilot ($6.300) = 5-7x Chatwoot. Justifica-se SOMENTE se compliance enterprise ou ecosystem marketplace forem deal-breaker — em SMB raramente sao.
- **Intercom Essential+Fin ($5.304/yr)** = 4-5x Chatwoot. Per-resolution Fin ja consome 67% do TCO ($297/$442). Sem in-app messenger heavy use ou GDPR EU strict, gap economico nao se justifica.

### 2.3 Caveats SMB

- Chatwoot self-host assume time com 1 dev capaz de manter VPS + DB + Redis + monitoramento — sem isso, Cloud Startups e a opcao real.
- Octadesk WOZ AI add-on com pricing oculto pode adicionar R$500-2000/mo conforme volume — TCO real Octadesk com AI = R$2.000-3.500/mo = ~$385-675 USD/mo = $4.620-8.100 USD/yr — daria ranking diferente vs Cloud Startups.
- Captain credits 300 incluso cobre 1.000 conv × 30% deflection = 300 acoes — exatamente no limite. Se deflection real subir a 40%+ em SMB, overage de $20/1k credits add-on.
- Zendesk monthly billing tem premium +25% (Vendr data); annual billing sticker e o usado aqui.

---

## 3. TCO Cenario Mid-market — 20 agents, 5.000 conv/mo, 50% deflection target

### 3.1 Setup detalhado

| Item | Chatwoot self-host custom | Chatwoot Cloud Business | Zendesk Suite Pro + Copilot | Intercom Advanced + Fin (full) | Octadesk Sea+AI |
|---|---:|---:|---:|---:|---:|
| **Pricing base/mo** | $0 license | $780 (20×$39) | $2.300 (20×$115) | $1.700 (20×$85) | R$2.972 (30 users tier) = ~$570 USD |
| **AI add-on/mo** | OpenAI gpt-4o-mini ~$75 | Captain 500 incl + 2.000 extras = $40 | Copilot bundle add 5×$50×20 = $1.000 | Fin: 2.500 res×$0.99 = $2.475 | WOZ pricing oculto (~$500-1.500 estimate) |
| **Copilot/Pro Analytics/extras** | — | — | — | Copilot 10 agents $290 + Pro $99 + Proactive $99 = $488 | — |
| **Hosting/Ops/mo** | $44 VPS CCX22 + $300 managed DB + $100 backup + 10h DevOps = $944 | incluso | incluso | incluso | incluso |
| **TCO mes (USD)** | **~$619** | **~$820** | **~$3.300 sticker / $5.000 real (× 2.0)** | **~$4.663** | **~$1.070-2.070** (com WOZ estimado) |
| **TCO ano (USD)** | **~$7.428** | **~$9.840** | **~$50.000-75.000 real** | **~$55.956** | **~$12.840-24.840** (com WOZ) |
| **Multiplo vs Chatwoot Cloud Business** | 0.75x | **1.0x baseline** | 5.1x-7.6x | **5.7x** | 1.3x-2.5x |

### 3.2 Insight Mid-market

- **Chatwoot self-host custom ($7.428/yr)** segue mais barato, mas DevOps 10h/mo @ $50 ja pesa. Acima de 30 agents, time interno precisa ser 0.2 FTE → ponto de cliff onde Cloud Business equipara.
- **Chatwoot Cloud Business ($9.840/yr)** = sweet spot mid-market. Captain 500 credits + extras $40/mo cobre 2.500 deflection-actions/mo. Sem DevOps, sem surprises.
- **Octadesk Sea+AI (~$13K-25K/yr)** competitivo se BR-only operacao + bundle LWSA. Perde pra Chatwoot Cloud em $3K-15K/yr mas ganha em BR-fit + PT-BR + WA BSP integrado oficial.
- **Zendesk Suite Pro+Copilot ($50K-75K real/yr)** = 5-8x Chatwoot. Vendr median deal $47.772/yr valida ratio 2-3x sticker → real para mid-market 20-30 agents.
- **Intercom Advanced+Fin ($55.956/yr)** = 5.7x Chatwoot. Fin ja consome $2.475/mo (53% TCO).

### 3.3 Cliff insight

- **Delta Chatwoot Cloud vs Zendesk/Intercom em mid-market: $40K-65K/year**. Em 5 anos: $200K-325K saving. Esse delta financia 1 senior engineer FTE OU 4-6 mid-level FTEs OU multi-year AI infra investment.
- **Para Intercom Fin justificar economicamente:** delta deflection vs Captain precisa ser sustentado >4pp consistentemente. Industry estimates sugerem plausivel mas nao provado — exige piloto.

---

## 4. TCO Cenario Scale — 50 agents, 20.000 conv/mo, 60% deflection target

### 4.1 Setup detalhado

| Item | Chatwoot self-host custom | Chatwoot Cloud Enterprise | Zendesk Suite Pro + Copilot bundle | Zendesk Suite Enterprise full stack | Intercom Expert full | Octadesk Suite (gated estimate) |
|---|---:|---:|---:|---:|---:|---:|
| **Pricing base/mo** | $0 license | $4.950 (50×$99) | $5.750 (50×$115) | $8.450 (50×$169) | $6.600 (50×$132) | nao publico — RFQ only |
| **AI add-on/mo** | OpenAI ~$400 (~12k conv) | Captain 800 incl + 11.200 extras = $224 | Copilot $2.500 (50×$50) | Copilot $2.500 + QA $1.750 + WFM $1.250 + ADPP $2.500 = $8.000 | Fin: 12.000 res×$0.99 = **$11.880** | WOZ pricing oculto (estimate $2K-5K/mo) |
| **Extras/mo** | — | — | — | — | Copilot 50 agents $1.450 + Pro $99 + Proactive $99 = $1.648 | — |
| **Hosting/Ops/mo** | $200 VPS cluster + $300 managed DB + $100 backup + $500 DevOps 10h = $1.100 | incluso | incluso | incluso | incluso | incluso |
| **TCO mes (USD)** | **~$1.400** | **~$5.150** | **~$8.250 sticker / ~$11.000-15.500 real (× 1.3-1.9)** | **~$16.450 sticker / ~$25K real** | **~$20.128** | **~$5K-10K estimate** |
| **TCO ano (USD)** | **~$16.800** | **~$61.800** | **~$130K-186K real** | **~$200K-300K real** | **~$241.536** | **~$60K-120K estimate** |
| **Multiplo vs Chatwoot self-host** | **1.0x baseline** | 3.7x | 7.7x-11x | 12x-18x | 14.4x | 3.6x-7.1x |
| **Multiplo vs Chatwoot Cloud Enterprise** | 0.27x | **1.0x baseline** | 2.1x-3.0x | 3.2x-4.9x | 3.9x | 1.0x-1.9x |

### 4.2 Insight Scale

- **Chatwoot self-host custom ($16.800/yr)** absolute champion em TCO — 14x mais barato que Intercom Expert. Trade-off: precisa 0.2-0.3 FTE DevOps + accept compliance certs publicos absentes (customer-controlled compliance no max).
- **Chatwoot Cloud Enterprise ($61.800/yr)** = SaaS premium do open-source. SSO incluso, audit, sandbox-like. 3-4x mais barato que Zendesk equivalente.
- **Zendesk Suite Pro+Copilot real $130K-186K** ou Enterprise full $200K-300K = enterprise pricing **plausivel** quando compliance certs publicos (SOC2 + ISO + FedRAMP + HIPAA + BCR) sao mandatory. Para Sinkra businesses mid-market BR sem regulacao critica, gap proibitivo.
- **Intercom Expert full $241.536/yr** = **Fin AI consome 59% do TCO** ($142.560/yr). Per-resolution model cliffa exponencialmente em scale. Justifica-se apenas em SaaS B2B in-app heavy ocidental + budget enterprise + product-tour requirements.
- **Octadesk Suite gated** = unknown precisa RFQ. Estimate $60K-120K/yr seria competitivo se entregar SSO/SAML + audit logs + multi-help-center publicamente. Hoje gaps prevalecem.

### 4.3 Cliff insight scale

- **Delta enterprise tier (Chatwoot Cloud Enterprise vs Zendesk Suite Enterprise full): $140K-250K/year**. Em 5 anos: $700K-1.25M saving via OSS path.
- **Per-resolution Fin AI vira proibitivo em scale:** $11.880/mo so em AI = $142.560/yr **so para AI**. Chatwoot Captain equivalente $200-400/mo em credits = $2.400-4.800/yr. **Diferencial AI-only de $137.000+/yr.**
- **Math do justificavel Intercom em scale:** Para Intercom Expert valer pena vs Chatwoot Enterprise, deflection Fin precisaria ser **dramaticamente** superior a Captain — algo como 75-80% Fin vs 30-35% Captain. Mesmo nesse cenario hipotetico, 12.000 deflection-actions/mo de delta = ~10 humanos handling overflow @ $4k/mo = $40k/mo cost extra Chatwoot. Ainda assim Chatwoot wins por $135K+/ano.

---

## 5. Analise de breakeven e cliffs por player

### 5.1 Chatwoot — onde self-host PARA de fazer sentido

| Volume | DevOps cost estimate | Chatwoot self-host TCO/yr | Chatwoot Cloud Business TCO/yr | Verdict |
|---|---|---:|---:|---|
| 5 agents | 0.05 FTE | ~$324-600 | $1.140 | **Self-host wins by 2x-3.5x** |
| 20 agents | 0.10-0.15 FTE = $7K-10K | ~$7.428 | $9.840 | **Self-host wins by ~25%** (mas margem fina) |
| 50 agents | 0.20-0.30 FTE = $15K-22K | ~$16.800 | $61.800 | **Self-host wins by 3.7x** se DevOps competente |
| 100 agents | 0.30-0.50 FTE = $22K-37K | estimate $35K-50K | est. ~$120K | Self-host ainda wins ~2.5x mas precisa SRE dedicado |
| 200+ agents | 0.5+ FTE + on-call rotation | $50K-100K | $250K+ | Cliff: precisa avaliar SRE rotation + uptime SLA — Cloud Enterprise pode equiparar |

**Cliff Chatwoot self-host:** quando volume + complexidade exigem SRE dedicado com on-call rotation (>0.5 FTE), TCO real começa a equiparar Cloud Enterprise. Tipicamente >100-150 agents OR uptime SLA 99.9%+ contratual.

### 5.2 Zendesk — onde Suite Pro precisa virar Enterprise

| Trigger | Cliff |
|---|---|
| **Sandbox extra environments** | Enterprise tier only — Pro nao tem |
| **Custom agent roles + audit logs detalhados** | Enterprise tier |
| **HIPAA BAA / FedRAMP / BCR multi-region** | Enterprise tier |
| **>50 agents + SSO/SAML/SCIM obrigatorio + multi-brand** | Enterprise tier |
| **Volume discount kick-in** | 25+ seats + multi-year commit; estimate 15-30% discount viavel pra Enterprise |

**Cliff Zendesk:** Suite Pro+Copilot ($93K-186K real para 50 agents) vira insuficiente quando compliance + multi-brand + audit + sandbox sao mandatory → forca Suite Enterprise full ($200K-300K real). Sem esses requirements, Suite Pro ja e enterprise-grade pricing pra mid-market — math nao fecha vs Chatwoot.

### 5.3 Intercom — onde Fin per-resolution VIRA proibitivo

| Conv/mo | Deflection 50% | Fin cost/mo | Fin cost/yr |
|---:|---:|---:|---:|
| 1.000 | 500 res | $495 | $5.940 |
| 5.000 | 2.500 res | $2.475 | $29.700 |
| 10.000 | 5.000 res | $4.950 | $59.400 |
| 20.000 | 10.000 res | $9.900 | $118.800 |
| 50.000 | 25.000 res | $24.750 | $297.000 |
| 100.000 | 50.000 res | $49.500 | $594.000 |

**Cliff Intercom Fin:** acima de **5.000 resolutions/mo** ($5K/mo = $60K/yr **so em AI**), per-resolution model cliffa contra qualquer alternativa per-seat ou flat-fee. Em scale 50.000+ conv/mo, Fin sozinho custa $300K/yr — equivale a custo total Zendesk Enterprise full stack em 50 agents.

**Volume break-even** (vs Chatwoot Captain $20/1k credits):
- 1pp delta deflection = ~$200-4.000/mo extra agente humano dependendo do scale
- Para Intercom vencer math em scale: **delta deflection >4pp consistentemente** + sustained advantage Fin. Plausivel mas nao provado sem piloto.

### 5.4 Octadesk — onde HITS gap enterprise e precisa migrar

| Trigger | Cliff |
|---|---|
| **SSO/SAML/SCIM obrigatorio publicamente confirmado** | Octadesk Suite gated, nao confirmado em fonte primaria |
| **SOC 2 Type II ou ISO 27001 audit report** | Nao publicamente confirmado — apenas LGPD declarada |
| **Multi-help-center / multi-brand** | Octa Suite "branch management" mas profundidade nao auditada |
| **HIPAA BAA / PCI-DSS / FedRAMP** | Nao oferecido (esperado) |
| **WhatsApp >5.000 conv/mo** | Tier Higher cap; Suite contato comercial; overage policy nao publica |
| **Multi-region / data residency fora BR** | Locaweb hosting BR conhecido; multi-region nao confirmado |

**Cliff Octadesk:** quando cliente cresce alem de PME BR e precisa compliance regulado (healthcare, fintech regulado, governo) ou multi-region, **nao ha caminho** dentro de Octadesk hoje → forced migration para Zendesk (compliance + ecosystem) ou Chatwoot self-host EU (sovereignty + cost-control).

**Outage frequency** (Capterra reviews): "outages com frequencia aumentada no ultimo ano" — pode acelerar cliff antes do tier upgrade.

---

## 6. TCO ranking final por cenario (visao agregada)

### 6.1 SMB (5 agents, 1.000 conv/mo, 30% deflection)

| Rank | Setup | TCO/yr USD | TCO/yr BRL (FX 5.20) | Multiplo vs lider |
|---|---|---:|---:|---:|
| **1o** | Chatwoot self-host custom | **$324-600** | R$1.685-3.120 | 1.0x baseline |
| **2o** | Chatwoot Cloud Startups | $1.140 | R$5.928 | 1.9x-3.5x |
| **3o** | Octadesk Conversas (sem WOZ) | ~$3.540 | R$18.504 (R$1.542×12) | 5.9x-11x |
| **4o** | Zendesk Suite Team (sem AI) | $3.300-6.600 | R$17.160-34.320 | 5.5x-20x |
| **5o** | Intercom Essential+Fin | $5.304 | R$27.581 | 8.8x-16x |

### 6.2 Mid-market (20 agents, 5.000 conv/mo, 50% deflection)

| Rank | Setup | TCO/yr USD | Multiplo vs lider |
|---|---|---:|---:|
| **1o** | Chatwoot self-host custom | **$7.428** | 1.0x baseline |
| **2o** | Chatwoot Cloud Business | $9.840 | 1.32x |
| **3o** | Octadesk Sea+AI (com WOZ estimate) | $12.840-24.840 | 1.7x-3.3x |
| **4o** | Intercom Advanced+Fin full | $55.956 | **7.5x** |
| **5o** | Zendesk Suite Pro+Copilot real | $50.000-75.000 | 6.7x-10x |

### 6.3 Scale (50 agents, 20.000 conv/mo, 60% deflection)

| Rank | Setup | TCO/yr USD | Multiplo vs lider |
|---|---|---:|---:|
| **1o** | Chatwoot self-host custom | **$16.800** | 1.0x baseline |
| **2o** | Octadesk Suite gated (estimate) | $60.000-120.000 | 3.6x-7.1x |
| **3o** | Chatwoot Cloud Enterprise | $61.800 | 3.7x |
| **4o** | Zendesk Suite Pro+Copilot real | $130.000-186.000 | 7.7x-11x |
| **5o** | Zendesk Suite Enterprise full | $200.000-300.000 | 12x-18x |
| **6o** | Intercom Expert full | $241.536 | **14.4x** |

---

## 7. Notas de confidence

| Player | Pricing publico | AI pricing | Volume discounts | Hidden costs | Confidence global |
|---|---|---|---|---|---|
| **Chatwoot** | H (chatwoot.com/pricing fetched) | M Captain credits-per-action vaga | N/A (sticker = real) | M Captain overage estimativo | **H** |
| **Zendesk** | H (zendesk.com/pricing) | M Per-resolution AI Agents nao publico ($0.85-1.20 estimado) | M (Vendr 15-30% pra 25+ seats) | H multipliers documentados | **H** |
| **Intercom** | H (intercom.com/pricing) | H ($0.99/res publico) | M (anchor pricing pulled, custom RFQ) | M Fin trigger semantics (24h follow-up) | **H** |
| **Octadesk** | H Conversas/Helpdesk; M Sea+AI G2 mirror; **L Suite (gated)** | L (WOZ pricing nao publico) | L (sem dados publicos) | M (overage WA conv nao publico) | **M** |

**Confidence summary do TCO consolidado:**
- **H (high):** Chatwoot, Zendesk, Intercom — pricing oficial publico fetched 2026-05-06; multipliers Vendr e benchmarks externos cross-referenciados.
- **M (medium):** Octadesk — tier publico H mas Suite gated + WOZ pricing oculto adiciona incerteza ±50% no TCO scale.
- **L (low):** Octadesk Suite estimate $60K-120K/yr — RFQ obrigatorio para validacao real.

---

## 8. Cross-refs

- Chatwoot vs Zendesk pricing detalhado: `docs/bench/chatwoot-vs-zendesk/deep/pricing-analysis.md`
- Intercom vs Chatwoot pricing detalhado: `docs/bench/intercom-vs-chatwoot/deep/pricing-tco.md`
- Octadesk inventario + pricing publico: `docs/bench/octadesk-vs-zendesk/inventory-octadesk.md`
- Octadesk feature gap enterprise (cliffs SSO/SAML/SOC2): `docs/bench/octadesk-vs-zendesk/deep/feature-gap-enterprise.md`
- Landscape 4 players consolidado: `docs/research/2026-05-06-omnichannel-helpdesk-landscape/comparison-table.md`
- Decisao por persona: `docs/bench/3-way-final-omnichannel/consolidated-scorecard.md` + `final-recommendation-matrix.md`

---

## 9. Disclaimer

1. **FX cambial** nao modelada — BRL→USD usa 5.20 fixo (volatilidade real ±15% pode mover ranking Octadesk).
2. **WhatsApp Meta fees** NAO incluidas — variam por pais (UIC/BIC); pass-through em todos players.
3. **VoIP/voice fees** NAO incluidas — Zendesk Talk + Intercom Talk + Chatwoot voice (Enterprise) tem custos extra.
4. **Custos infra Chatwoot self-hosted** estimativos — variam por provedor (AWS/GCP 20-50% mais caros que Hetzner usado aqui).
5. **Tempo DevOps maintenance** estimativo $50/h junior; senior pode ser 2-3x mais caro.
6. **Octadesk Suite + WOZ pricing** OCULTOS — TCO Octadesk em scale e estimativa que requer RFQ para validacao.
7. **Zendesk Suite Enterprise volume discount** estimativo 15-30% para 25+ seats + multi-year commit (Vendr data).
8. **Intercom anchor pricing pulled em 2025** — alguns reports indicam custom RFQ pricing diferente do listado; usado oficial publico aqui.
9. **Volume conv assumido linear** — picos sazonais (Black Friday, etc) podem dobrar AI cost Intercom em mes pico via per-resolution Fin.
10. **Custom LLM API costs** estimativos com gpt-4o-mini para Chatwoot self-host custom; usar Claude Haiku ou GPT-4o full pode multiplicar 5-10x.

---

*TCO Comparison 4-players consolidado | Bench 3-way-final-omnichannel | 2026-05-06*
