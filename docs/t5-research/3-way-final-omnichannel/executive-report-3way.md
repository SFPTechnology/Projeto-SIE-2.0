# Executive Report — 3-Way Final Omnichannel

**Bench:** 3-way-final-omnichannel
**Data:** 2026-05-06
**Audiência:** decisores tecnicos (CTO/Head of CX/Tech Ops)
**Escopo:** sintese executiva consolidando 3 paired benches (Chatwoot/Zendesk, Intercom/Chatwoot, Octadesk/Zendesk) em verdict 4-way unico.
**Players:** Chatwoot, Zendesk, Intercom, Octadesk.

> **Disclaimer constitucional:** este documento e RESEARCH agregado, NAO recomendacao vinculante para nenhum negocio especifico do Sinkra Hub. Mapeia candidatos para POC; decisao final exige due diligence comercial + piloto + validacao com BSP local.

---

## 1. Sumario Executivo

O ciclo de research mapeou 21 players no segmento omnichannel + helpdesk + WhatsApp Cloud API; o `tech-research` (`docs/research/2026-05-06-omnichannel-helpdesk-landscape/03-recommendations.md`) selecionou **Top 6 finalistas** (Chatwoot, Zendesk, Octadesk, Intercom, Zammad, FreeScout) com base em 7 criterios ponderados. Tres paired benches foram executados sobre o quarteto critico — Chatwoot/Zendesk, Intercom/Chatwoot e Octadesk/Zendesk — e este artefato consolida os tres em **matriz unica 4 players × 9 dimensoes** com pesos neutros + 4 personas recalibradas (consolidated-scorecard.md).

O **achado central e empate tecnico no eixo neutro entre Zendesk (74.95) e Chatwoot (74.40)** — delta de 0.55 dentro do ruido estatistico (consolidated-scorecard.md TL;DR). Octadesk (63.89) e Intercom (61.25) ficam abaixo no neutro mas sao categorical em segmentos especificos. **Score neutro e diagnostico, nao decisao**: a decisao real e **persona-driven**. As 4 personas analisadas geram 4 recomendacoes diferentes (consolidated-scorecard.md sumario): Chatwoot vence SMB BR e-commerce (75.84); Zendesk vence Mid-market BR (75.13, empate tecnico delta 0.65 vs Chatwoot 74.48), Enterprise BR multinacional (79.44, delta +9.28) e Global SaaS B2B (77.93). Intercom NAO aparece em primeiro em nenhuma persona — paga D7=0 (sem self-host) e D8=35 (BR-fit fraco) caro mesmo com D9=95 in-app categorical.

**WhatsApp Cloud API e vetor critico do mercado 2026** (whatsapp-integration-ranking.md): Meta deprecou on-premise em out/2025 e baniu chatbots IA nao-BSP em jan/2026 — todos os 4 players sao BSP credenciados, mas as **arquiteturas divergem materialmente**: Octadesk Cloud-Direct (Meta passthrough sem markup), Chatwoot BYOC (3 providers nativos + qualquer BSP credenciado), Zendesk via Sunshine Conversations (broker proprietario com variable pricing layer) e Intercom Cloud direct (Meta-direct + outbound add-on $99/mo).

**AI deflection virou tablestakes mas pricing model importa mais que feature** (ai-capability-ranking.md): Zendesk lidera em maturity (87, breadth de produtos AI Agents + Copilot + QA + WFM); Intercom Fin lidera em transparencia (80, deflection 51-67% publicado + patentes + per-resolution honesto $0.99); WOZ Octadesk lidera em BR-native (70, PT-BR end-to-end); Chatwoot Captain (65) e promissor mas underprovado — deflection nao publicado e modelo nao disclosed.

---

## 2. Metodologia

A consolidacao usou **9 dimensoes ponderadas** (D1 canais incluindo WhatsApp depth 12%; D2 AI capability + transparencia + deflection 18%; D3 pricing transparency + TCO real 15%; D4 governance/compliance 12%; D5 ecosystem/marketplace 8%; D6 comunidade/maturidade 8%; D7 flexibilidade/sovereignty 10%; D8 Brasil-fit 12%; D9 in-app messaging 5%) recompostas a partir das dimensoes originais dos tres benches paired (consolidated-scorecard.md secao "Dimensoes consolidadas").

Cada celula 4×9 recebeu **score 0-100 + source explicito + confidence H/M/L**. Os pesos D1-D9 sao **neutros**; quatro personas com pesos recalibrados produzem rankings persona-driven: SMB BR e-commerce (D8=27, D3=20), Mid-market BR (D1=15, D2=15, D8=15), Enterprise BR multinacional (D4=22, D5=12), Global SaaS B2B (D2=20, D9=15). A logica de cada persona e a tabela de pesos esta em consolidated-scorecard.md secao "Personas — recalibracoes".

**Reconciliacao de inconsistencias** entre os tres benches foi formal e documentada em triangulation-analysis.md: 7 concordancias robustas (CR-01..07, claims fortes 2/2 ou 3/3), 6 inconsistencias arbitradas (INC-01..06) e 5 curiosity queries (CQ-3WAY-001..005) para untested cells. A distribuicao final de confidence e **~56% celulas em H, ~33% em M, ~11% em L** (triangulation-analysis.md secao 4) — o L se concentra em D8 Intercom e D9 Octadesk, nao tocados por bench algum, mas com impacto baixo no ranking persona porque outros vetores ja tomam a decisao.

---

## 3. Resultado por dimensao (D1-D9)

### D1 — Canais nativos incluindo WhatsApp depth (peso 12%)

**Vencedor: Chatwoot 93** (Octadesk 92 a 1pt; Zendesk 88; Intercom 60). Chatwoot vence pela **diversidade omnichannel** (WhatsApp + Insta + Telegram + Line + TikTok nativos) somada ao **BYOC genuino**. Octadesk vem coladissimo por Cloud-Direct oficial Meta + UX BR. **Quem perde:** Intercom (60) — WhatsApp Meta-direct disponivel desde Essential mas sem multi-BSP nem Telegram/Line/TikTok nativos, DNA in-app deixa omnichannel breadth fraco. Confidence H — fato verificavel em vendor docs (triangulation INC-06).

### D2 — AI capability + transparencia + deflection publicado (peso 18%)

**Vencedor: Zendesk 87** (Intercom 80; Octadesk 70; Chatwoot 65). Zendesk vence em **breadth + outcomes publicados** (39-92% deflection range) + ecossistema dedicado (Copilot $50, QA AI $35, WFM $25, ADPP $50). Intercom em segundo por **transparencia tecnica** — Fin Apex 1.0 nomeado, RAG pipeline 6 steps documentado, 2 patentes, deflection benchmarked Lightspeed 65% (ai-capability-ranking.md secoes 1.1-1.2). **Quem perde:** Chatwoot Captain (65) — modelo nao disclosed, deflection nao publicado, sem custom actions, sem simulation, NAO disponivel em self-hosted (quebra promessa OSS). Confidence M — INC-01 reconciliado entre Bench 1 (75) e Bench 2 (50).

### D3 — Pricing transparency + TCO real (peso 15%)

**Vencedor: Chatwoot 92** (Octadesk 65; Zendesk 55; Intercom 50). Chatwoot vence categorical: **self-host = $0**, tiers Cloud publicos ($19/$39/$99), sticker-to-real ratio 1.0-1.2x. Zendesk multiplier 2-3x sticker (Vendr median deal $47.772/year); Intercom Fin per-resolution explode em volume (5K conv/mo = $4.950/mo so AI). **Quem perde:** Intercom (50) — anchor pricing pulled em 2025, custom RFQ + Fin per-res cliffa exponencialmente em scale (tco-comparison secao 5.3). Confidence H — fontes Vendr + pricing pages oficiais + Fin Labs publico (CR-06, INC-03).

### D4 — Governance / Compliance (peso 12%)

**Vencedor: Zendesk 95** (Intercom 80; Chatwoot 55; Octadesk 45). Zendesk vence **categorical** para enterprise regulado: SOC2 Type II + ISO 27001/27018/27701 + FedRAMP + GDPR BCR + HIPAA BAA + multi-region (US/EU/AU/JP) (CR-02). Intercom em segundo (ISO27001/27018/27701 + GDPR + CCPA + Dublin region). **Quem perde:** Octadesk (45) — sem SOC2 / ISO27001 / SSO/SAML/SCIM publicamente confirmados, apenas LGPD via parent LWSA (gap-analysis Octadesk GAP-OCT-01..04). Confidence M para Octadesk (single-source — INC-05).

### D5 — Ecosystem / Marketplace / integracoes (peso 8%)

**Vencedor: Zendesk 95** (Intercom 85; Chatwoot 65; Octadesk 60). Zendesk **categorical** com 1.977 apps + 425+ AI-powered + Salesforce/NetSuite/Workday enterprise. Intercom App Store 300+ apps polished. **Quem perde:** Octadesk (60) e Chatwoot (65) — ecossistemas regionais (LWSA bundle Bling/Tray/Vindi para Octadesk; comunidade open para Chatwoot). Confidence H — numeros auditaveis.

### D6 — Comunidade / Maturidade / reviews (peso 8%)

**Vencedor: Zendesk 91** (Intercom 85; Chatwoot 78; Octadesk 55). Zendesk lidera por share 14.8% + ~6.000 reviews G2 + 10+ anos categoria. Chatwoot 29.1k GitHub stars (release v4.13.0 abril/2026) compete com OSS forte. **Quem perde:** Octadesk (55) — comunidade BR-only, reviews Capterra reportam aumento de outages no ultimo ano. Confidence H.

### D7 — Flexibilidade (self-hosted, customizacao, sovereignty) (peso 10%)

**Vencedor: Chatwoot 100** (Zendesk 35; Octadesk 25; Intercom 0). Chatwoot **categorical** com MIT + 4 deployment options (CR-01). Intercom 0 categorical loser — Cloud-only sem self-host, sovereignty zero (gap-analysis PHIL-01: "Intercom nunca vai oferecer self-hosted sem destruir SaaS revenue model"). **Quem perde:** Intercom — esse 0 mata score neutro mesmo com D9=95 categorical. Confidence H.

### D8 — Brasil-fit (BSP local, BRL pricing, suporte PT-BR, integracoes BR) (peso 12%)

**Vencedor: Octadesk 95** (Chatwoot 60; Zendesk 60; Intercom 35). Octadesk **categorical** com bundle LWSA (Bling/Tray/Vindi/Melhor Envio) + WOZ AI PT-BR nativo + audio transcription WhatsApp BR + suporte PT-BR formal (CR-04). Zendesk e Chatwoot empatam em 60. **Quem perde:** Intercom (35) — pricing 100% USD, sem time produto BR, sem integracoes VTEX/RD/Bling, sem suporte PT-BR formal (CQ-3WAY-004). Confidence M para Zendesk (INC-02 reconciliacao 80 vs 50 → 60), L para Intercom (untested).

### D9 — In-app messaging strength (peso 5%)

**Vencedor: Intercom 95** (Zendesk 70; Chatwoot 50; Octadesk 40). Intercom **categorical** — best-in-class SDK iOS/Android/Web/RN/Flutter + Product Tours + Checklists + Messenger polish (CR-05). **Quem perde:** Octadesk (40, untested CQ-3WAY-005) e Chatwoot (50) — widget funcional mas nao no nivel Intercom. Confidence H Intercom, L Octadesk.

---

## 4. Resultado por persona

### Persona A — SMB BR e-commerce (5-10 agents, ≤1k conv/mes)

**Pesos recalibrados:** D8=27, D3=20, D1=14, D7=10, D2=8, D5=8, D9=5, D4=4, D6=4. **Logica:** WhatsApp depth + BR-fit + TCO dominam; compliance enterprise quase irrelevante.

**Ranking final:**
1. **Chatwoot 75.84** (vencedor)
2. Octadesk 70.43 (delta -5.41)
3. Zendesk 68.52 (delta -7.32)
4. Intercom 52.40 (delta -23.44)

**Razao do vencedor:** Chatwoot combina D7=100 (self-host MIT) + D3=92 (pricing transparente) + D1=93 (omnichannel completo) — e o unico que vence em TCO sem perder BR-fit minimo. **Quando o 2o faria mais sentido:** Octadesk vence se equipe NAO tem DevOps interno + bundle LWSA (Bling/Tray/Vindi) e parte do stack — zero-DevOps + WOZ AI PT-BR nativo + audio transcription compensam o gap de R$2-3k/yr vs Chatwoot self-host. **Tiebreakers operacionais:** se equipe roda Docker → Chatwoot self-host ($324-600/yr); senao → Octadesk Conversas (R$1.542/mes ~$3.540/yr).

### Persona B — Mid-market BR (50-100 agents, ~10k conv/mes)

**Pesos recalibrados:** D1=15, D2=15, D8=15, D3=12, D4=10, D5=10, D7=10, D6=8, D9=5. **Logica:** equilibrio com BR-fit ainda dominante mas compliance/AI subindo de relevancia.

**Ranking final:**
1. **Zendesk 75.13** (vencedor por delta 0.65 — empate tecnico)
2. Chatwoot 74.48
3. Octadesk 65.75 (delta -9.38)
4. Intercom 60.30 (delta -14.83)

**Razao do vencedor:** Zendesk vence pelo combo D2=87 (AI maturity) + D4=95 (compliance) + D5=95 (ecosystem); empata tecnicamente com Chatwoot que recupera pelo combo D3=92 + D7=100. **Quando o 2o faria mais sentido:** com DevOps maduro + cost-conscious + customizacao alta, Chatwoot self-host Enterprise vence em TCO 5-7x (tco-comparison Mid: Chatwoot Cloud Business $9.840/yr vs Zendesk Suite Pro+Copilot real $50-75K/yr). **Tiebreakers operacionais:** SSO/SAML obrigatorio sem DevOps → Zendesk; DevOps maduro + cost-conscious → Chatwoot; BR-only operacao + bundle LWSA → Octadesk competitivo (final-recommendation-matrix.md secao 1).

### Persona C — Enterprise BR multinacional (100+ agents, regulado, multi-region)

**Pesos recalibrados:** D4=22, D5=12, D2=12, D1=10, D6=10, D3=8, D7=8, D8=10, D9=8. **Logica:** compliance + ecosystem dominam; TCO baixo peso (orcamento existe).

**Ranking final:**
1. **Zendesk 79.44** (clear winner, delta +9.28)
2. Chatwoot 70.16
3. Intercom 67.00
4. Octadesk 60.10

**Razao do vencedor:** Zendesk vence categorical em D4 (95) + D5 (95) — SOC2 + ISO + FedRAMP + HIPAA + BCR + multi-region sao **mandatory** para healthcare BR / fintech BR / governo. Octadesk fora do segmento (D4=45). **Quando o 2o faria mais sentido:** se buyer aceita Chatwoot self-host EU + customer-controlled compliance posture, TCO 3-5x menor compensa overhead operacional — exige DevOps maduro + SRE rotation. **Tiebreakers operacionais:** healthcare BR / fintech BR / governo → Zendesk mandatory; buyer com DevOps maduro disposto a self-host customer-controlled → Chatwoot self-host EU + paid support partner.

### Persona D — Global SaaS B2B (20-30 agents, EU+US, GDPR strict, in-app heavy)

**Pesos recalibrados:** D2=20, D4=15, D9=15, D1=10, D3=10, D5=10, D7=10, D6=8, D8=2. **Logica:** AI sofisticada + in-app messenger + compliance dominam; BR-fit quase zero.

**Ranking final:**
1. **Zendesk 77.93** (vencedor)
2. Chatwoot 71.19
3. Intercom 69.25 (surpresa — apesar de D9=95 categorical)
4. Octadesk 57.25

**Razao do vencedor + surpresa diagnostica:** Zendesk vence pelo combo compliance + ecosystem + AI maturity. Intercom fica em **3o** apesar de in-app strength D9=95 e AI D2=80 porque **D7=0 + D8=35 = penalidade composta**. **Quando o 2o faria mais sentido:** se in-app messaging + AI sao DECISIVOS (parte do produto, nao add-on) + budget enterprise existe, Intercom polish em D9 e categorical e vale o trade-off no score (final-recommendation-matrix.md tabela sintese). **Tiebreakers operacionais:** in-app + AI decisivos + budget enterprise → Intercom; compliance + scale + ecosystem → Zendesk; GDPR strict EU residency + cost-conscious → Chatwoot self-host EU.

**Observacao agregada:** Chatwoot e o **unico player que mantem TOP-2 em TODAS as 4 personas** (consolidated-scorecard.md). Zendesk vence 3 de 4 mas perde em SMB BR. Intercom NAO aparece em primeiro em nenhuma. Octadesk em primeiro apenas como alternativa zero-DevOps em SMB BR.

---

## 5. AI capability — verdict

**Zendesk lidera em maturity** (D2=87) — breadth de produtos dedicados (AI Agents para deflection + Copilot $50/agent + QA AI $35/agent + WFM $25/agent + ADPP $50/agent) + customer outcomes range publicado (39-92%) + compliance posture categorical. Default para mid-market+ e enterprise regulado. Trade-off: TCO 2-3x sticker + per-resolution AI Agents pricing **NAO publico** (gated em sales) + bolted-on de aquisicao Ultimate.ai (ai-capability-ranking.md secao 1.1).

**Intercom Fin lidera em transparencia** (D2=80) — modelo nomeado (Fin Apex 1.0 patenteado), RAG pipeline 6 steps documentado, 2 patentes publicas (Fin Engine + retrieval + reranker), deflection benchmarked publicamente (51-67% medio, Lightspeed 65% end-to-end + 99% involvement), per-resolution **honesto** ($0.99/res publico), custom AI actions (refunds/system calls), pre-deploy simulation, hallucination control documentado, Fin Standalone integravel a Zendesk/Salesforce/HubSpot/Freshdesk (ai-capability-ranking.md secao 1.2). Categorical para Global SaaS B2B in-app heavy.

**Octadesk WOZ lidera em BR-native** (D2=70) — UNICO entre os 4 com PT-BR nativo end-to-end (UX + AI training + audio transcription) + bundle LWSA. Trade-off: deflection NAO publicado (claim marketing 80% sem benchmark — CQ-3WAY-002), pricing gated, ChatGPT-based sem moat tecnologico, sem custom actions documentadas, sem simulation mode, sem QA AI dedicada (ai-capability-ranking.md secao 1.3).

**Chatwoot Captain promissor mas underprovado** (D2=65) — built-in + credit pricing transparente (300-800 credits/tier + $20/1.000 extras) + 5-7x mais barato que Fin em mid-market + 8 linguagens demonstradas. Trade-off P0: deflection NAO publicado, modelo NAO disclosed, sem custom actions, sem simulation, sem hallucination control documentado, NAO disponivel em self-hosted Community (quebra promessa OSS), maturidade <2 anos (CQ-3WAY-001).

**Pricing model e decisivo, nao feature em isolado:** per-resolution Fin honesto cliffa em volume ($11.880/mo so AI em 12k res/mo); credits Captain transparente mas opaco em volume real; per-resolution Zendesk AI Agents NAO publico; WOZ pricing gated. Curiosity queries CQ-3WAY-001 (Captain deflection real) e CQ-3WAY-002 (WOZ deflection real) sao os dois maiores moves de subir confidence — POCs 30 dias resolvem em fase B (ai-capability-ranking.md secao 5).

---

## 6. WhatsApp integration — verdict

A depreciacao on-premise out/2025 + ban chatbots IA nao-BSP jan/2026 sao compativeis com os 4 (todos BSP credenciados), mas as **arquiteturas divergem materialmente** (whatsapp-integration-ranking.md secao 1):

**Octadesk Cloud-Direct oficial Meta (rank 1)** — transparencia categorical: Meta passthrough sem markup adicional, Octadesk como BSP credenciado, declarado oficial no site. Setup turnkey BR (~horas a 1-3 dias), time PT-BR, WOZ audio transcription nativa, integracoes VTEX/Tray BR. Trade-off: vendor lock-in alto, status page nao auditavel publicamente, tier WhatsApp granular nao 100% publico (whatsapp-integration-ranking.md secao 2.1).

**Chatwoot BYOC (rank 3)** — flexibilidade categorical: 3 providers nativos (Meta Cloud direct + 360Dialog + Twilio) + qualquer BSP credenciado Meta via API (Take Blip, Sinch, Zenvia, Gupshup). Cliente escolhe BSP, negocia pricing direto, sem markup Chatwoot. Trade-off: exige DevOps moderate-high para BSP shopping; Twilio + WA templates **known limitation** (forca migracao 360Dialog ou Cloud direct para outbound marketing) (whatsapp-integration-ranking.md secao 2.3 + 6.4).

**Zendesk Sunshine Conversations (rank 4)** — markup turnkey enterprise: broker proprietario (post-Smooch.io) que adiciona variable pricing layer ($495/mo Starter + $0.15/notification + per-MAU + edition tiering), latencia adicional, ponto de falha extra. Em troca, multi-channel via uma camada (Apple BC, LINE, Viber, custom in-app) que os outros 3 nao cobrem nativamente — para enterprises multi-canal globais, justifica markup; para WhatsApp-only BR ops, e overhead puro. **Hidden positive enterprise:** BSP-flex permite trocar BSP underlying mantendo Sunshine + Zendesk (whatsapp-integration-ranking.md secao 2.4 + 6.6).

**Intercom Cloud direct (rank 2)** — Meta-direct sem markup desde Essential ($29/seat), pricing transparente seat-based + usage. Hidden cost relevante: **outbound campaigns exige Proactive Support Plus add-on $99/mo** (~$1.200/yr extra fora do sticker). Sem suporte nativo a Telegram/Line/TikTok (whatsapp-integration-ranking.md secao 2.2 + 6.5).

**TCO 10 agents / 5K conv/mes (whatsapp-integration-ranking.md secao 4):** Chatwoot self-host $250-600/mo (lowest, exige DevOps); Chatwoot Cloud Business $590-890/mo; Intercom Advanced $1.149-1.449/mo; Zendesk Suite Pro+Sunshine $1.845-2.345/mo (highest); Octadesk Higher R$6.500-11.500/mo (lowest BR turnkey).

---

## 7. TCO findings

**SMB (5 agents, 1k conv/mo, 30% deflection)** — gap Chatwoot self-host vs Intercom = **16x** (tco-comparison secao 6.1):
- Chatwoot self-host custom **$324-600/yr** (1.0x baseline)
- Chatwoot Cloud Startups $1.140/yr (1.9-3.5x)
- Octadesk Conversas ~$3.540/yr (5.9-11x)
- Zendesk Suite Team sem AI $3.300-6.600/yr (5.5-20x)
- Intercom Essential+Fin $5.304/yr (8.8-16x — Fin per-res ja consome 67% do TCO)

**Mid (20 agents, 5k conv/mo, 50% deflection)** — gap chega a **5x** com self-host vencendo absolutamente (tco-comparison secao 6.2):
- Chatwoot self-host custom **$7.428/yr**
- Chatwoot Cloud Business $9.840/yr
- Octadesk Sea+AI $12.840-24.840/yr (com WOZ estimate)
- Zendesk Suite Pro+Copilot real $50-75K/yr (6.7-10x)
- Intercom Advanced+Fin full $55.956/yr (7.5x — Fin consome 53% do TCO)

**Scale (50 agents, 20k conv/mo, 60% deflection)** — gap chega a **14.4x** Intercom vs Chatwoot self-host (tco-comparison secao 6.3):
- Chatwoot self-host custom **$16.800/yr** (baseline)
- Octadesk Suite gated estimate $60-120K/yr
- Chatwoot Cloud Enterprise $61.800/yr (3.7x)
- Zendesk Suite Pro+Copilot real $130-186K/yr (7.7-11x)
- Zendesk Suite Enterprise full $200-300K/yr (12-18x)
- Intercom Expert full $241.536/yr (**14.4x** — Fin AI sozinho $142.560/yr = 59% do TCO)

**Cliffs principais** (tco-comparison secao 5):
- **Chatwoot DevOps cliff:** self-host para de fazer sentido em ~50-100 agents quando volume + complexidade exigem 0.3+ FTE DevOps + on-call rotation; Cloud Enterprise vira competitivo.
- **Octadesk gap enterprise:** sem caminho dentro de Octadesk para SSO/SAML/SCIM/SOC2 publicamente confirmados — clientes que crescem alem de PME BR e precisam compliance regulado (healthcare/fintech/governo) ou multi-region forcam migracao para Zendesk ou Chatwoot self-host EU.
- **Intercom Fin per-resolution explode:** acima de 5.000 resolutions/mo ($60K/yr so AI), per-resolution model cliffa contra qualquer alternativa per-seat ou flat-fee. Em 50K conv/mo, Fin sozinho custa $300K/yr (= Zendesk Enterprise full stack 50 agents). Para Intercom valer math em scale, delta deflection vs Captain precisa ser **>4pp consistentemente** — plausivel mas nao provado.
- **Zendesk Suite Pro insuficiente sem add-ons:** sandbox + custom roles + audit logs detalhados + HIPAA BAA + FedRAMP + multi-brand sao Enterprise-tier-only — quando esses requirements entram, salto Pro→Enterprise full stack vai a $200-300K/yr real para 50 agents.

---

## 8. Inconsistencias reconciliadas

A consolidacao formalizou 5 inconsistencias materiais entre os 3 paired benches (triangulation-analysis.md secao 2):

**INC-01 — Chatwoot AI score:** Bench 1 deu 75 ("presente e funcional, opacidade penalizada"); Bench 2 deu 50 ("P0 vermelho urgente vs Fin Apex 1.0"). Reconciliacao: divergencia de **criterio do que esta sendo medido** (breadth vs deflection performance). D2 consolidado = **65** com confidence M; severidade competitiva acomodada na persona-recalibration (P0 em Persona D, P2 em Persona A).

**INC-02 — Zendesk Brasil-fit:** Bench 1 deu 80 (vs Chatwoot baixo, Zendesk parecia BR-ready); Bench 3 deu 50 (vs Octadesk LWSA, Zendesk caiu). Bench 3 **mais severo e mais correto** em absoluto. D8 Zendesk consolidado = **60** (meio-termo refletindo BRL pricing + suporte/sales BR positivos mas integracoes BR via parceiros + FX risk em add-ons + sem time produto BR negativos confirmados).

**INC-03 — Pricing transparency Zendesk:** Bench 1 deu D3=50 (TCO global multiplier 2-3x); Bench 3 deu D5=70 (BR-context BRL publicado tiers principais). Os dois fatos sao corretos mas medem coisas diferentes. D3 Zendesk consolidado = **55** (peso maior para Bench 1 por TCO end-to-end com fonte Vendr); confidence H.

**INC-04 — Captain maturity (severidade):** Bench 1 ("promissor com gaps"); Bench 2 ("P0 vermelho"). Reconciliacao: severidade contextualizada por persona — P0 em Persona D (peso D2=20%), P2 em Persona A (peso D2=8%). D2 Chatwoot = 65 reflete meio-termo compativel com INC-01.

**INC-05 — Octadesk single-source:** Bench 3 e o unico que tocou Octadesk em compliance/AI/marketplace. Sem cross-validation, scores Octadesk em D2 (70), D4 (45), D5 (60) tem confidence M-L. Resolucao: scores preservados como Bench 3 reportou, com flag de confidence + 2 curiosity queries (CQ-3WAY-002 deflection real + CQ-3WAY-003 pricing detalhado tier).

**INC-06 — WhatsApp arquiteturas:** os 3 benches descreveram WhatsApp de formas estruturalmente diferentes (Chatwoot BYOC vs Octadesk Cloud-Direct vs Zendesk Sunshine vs Intercom Meta-direct). 4 modelos distintos preservados em D1, todos validos, confidence H — fato verificavel em vendor docs.

---

## 9. Decision tree consolidado

Resumo das 5-7 perguntas decisivas extraidas de final-recommendation-matrix.md secao 2:

```
1. Operacao e exclusivamente Brasil?
   ├── SIM → segue (2)
   └── NAO (global/multi-region/EN-first) → segue (5)

2. Volume da operacao (agents)?
   ├── ≤10 agents (SMB BR e-commerce/DTC) → segue (3)
   ├── 50-100 agents (mid-market BR) → segue (4)
   └── 100+ agents (enterprise BR regulado healthcare/fintech/governo)
       └── HIPAA/FedRAMP/SOC2 mandatory → ZENDESK Enterprise
           senao → buyer aceita customer-controlled (self-host EU)?
               SIM → CHATWOOT self-host EU + paid support partner
               NAO → ZENDESK Enterprise

3. SMB BR — tem DevOps interno (1+ pessoa Docker/K8s, 10+h/mes)?
   ├── SIM → CHATWOOT self-host community ($0 license + ~R$300-800/mes infra)
   └── NAO → OCTADESK (zero-DevOps + bundle Bling/Tray/Vindi via LWSA)

4. Mid-market BR — SSO/SAML mandatory por compliance?
   ├── SIM → ZENDESK Suite Professional/Enterprise
   └── NAO → DevOps maduro + cost-conscious + customizacao alta?
       SIM → CHATWOOT self-host Enterprise (TCO ~3-5x menor que Zendesk)
       NAO → ZENDESK Suite Team/Pro (default seguro) ou OCTADESK se BR-only + bundle LWSA

5. Global — in-app messaging (web SDK + mobile SDK + product tours) e DECISIVO?
   ├── SIM + budget enterprise → INTERCOM (D9=95 categorical)
   └── NAO → GDPR strict + EU residency mandatory?
       SIM + DevOps EU → CHATWOOT self-host (data sovereignty 100%)
       SIM + sem DevOps EU → ZENDESK (Dublin + BCR)
       NAO + compliance enterprise + multi-region → ZENDESK Enterprise (default global)
       NAO + cost-conscious + DevOps maduro → CHATWOOT self-host
```

**Atalho mental (3 perguntas):** (1) BR-only? Sim → descartar Intercom. (2) Tem DevOps maduro? Sim → Chatwoot competitivo; Nao → SaaS. (3) Compliance enterprise mandatory? Sim → Zendesk default; Nao → abrir leque.

---

## 10. Recomendacao final + proximos passos

**Nao ha vencedor unico.** O scorecard neutro aponta empate tecnico Zendesk (74.95) vs Chatwoot (74.40), mas a decisao real e **persona-driven** (final-recommendation-matrix.md secao 6):

- **SMB BR e-commerce** → Chatwoot self-host (com DevOps) ou Octadesk (sem DevOps)
- **Mid-market BR baixo compliance** → Chatwoot self-host
- **Mid-market BR SSO/SAML mandatory** → Zendesk Suite Pro
- **Enterprise BR regulado** → Zendesk Enterprise (Chatwoot self-host EU como backstop)
- **Global SaaS B2B in-app heavy** → Intercom (apesar do score 3o)
- **Global SaaS B2B GDPR strict** → Chatwoot self-host EU (Zendesk Dublin como alternativa)

**Proximo passo obrigatorio:** **POC 30 dias do top-2 da persona** antes de decisao final. As 5 curiosity queries (CQ-3WAY-001..005) endereçam exatamente o que o scorecard nao consegue resolver sem dado novo: Captain deflection real, WOZ deflection real, Octadesk pricing detalhado, Intercom Brasil-fit, Chatwoot self-host EU vs Zendesk Dublin GDPR head-to-head. POC deve mensurar **3 metricas duras**: deflection rate real (com mesma base de dados, mesma janela, mesmo dataset), TCO real medido (sticker + multiplier), WhatsApp delivery (latencia, template approval, BSP wallet flow).

**Disclaimer constitucional (final-recommendation-matrix.md preambulo):** este artefato e RESEARCH agregado. Cenarios "estilo Hub" sao perfis genericos, nao mapping 1:1 a AllFluence/AIOX/Academia Lendaria/Bilhon. Decisao final exige due diligence comercial + POC + validacao com BSP local + alinhamento com `@pm` do business especifico do Sinkra Hub.

---

## 11. Curiosity queue

Cinco queries documentadas em triangulation-analysis.md secao 3 endereçam gaps untested:

- **CQ-3WAY-001** — Captain AI deflection rate real (Chatwoot): POC 30 dias 10K conv/mes mix B2C+B2B vs Fin vs Zendesk AI Agents na mesma base. Impacto: D2 Chatwoot 50-80 (range largo).
- **CQ-3WAY-002** — WOZ AI deflection rate real (Octadesk): POC 30 dias 5K conv/mes WhatsApp BR. Vendor claim 80% provavelmente inflado.
- **CQ-3WAY-003** — Octadesk pricing detalhado por tier (gated): solicitar quote formal 50 agents + enterprise features (SSO/SAML, custom roles, sandbox). Cross-check com partner LWSA.
- **CQ-3WAY-004** — Intercom Brasil-fit: bench dedicado Intercom-BR (pricing BRL, time BR, integracoes BR, customers notaveis Nubank/iFood/Rappi).
- **CQ-3WAY-005** — Chatwoot self-host EU vs Zendesk Dublin GDPR: customer-driven decision tree (compliance posture, ops cost, audit overhead) — nao precisa bench dedicado.

---

## Cross-refs

- Matriz consolidada → `consolidated-scorecard.md`
- Reconciliacoes paired benches → `triangulation-analysis.md`
- Decisao por persona → `final-recommendation-matrix.md`
- TCO 4 players → `tco-comparison-4-players.md`
- AI capability deep dive → `ai-capability-ranking.md`
- WhatsApp arquiteturas → `whatsapp-integration-ranking.md`
- Top 6 selection → `docs/research/2026-05-06-omnichannel-helpdesk-landscape/03-recommendations.md`

*Executive Report 3-Way Final Omnichannel | Bench 3-way-final-omnichannel | 2026-05-06*
