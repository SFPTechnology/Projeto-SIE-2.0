# Cross-Bench Matrix — 3-Way Final Omnichannel

**Bench:** 3-way-final-omnichannel
**Data:** 2026-05-06
**Metodo:** Para cada uma das 9 dimensoes consolidadas, expomos o score final (de `consolidated-scorecard.md`), o bench fonte primario que sustenta o score, a citacao textual extraida do bench original como evidencia e a confidence (H/M/L). Celulas marcadas como `untested` correspondem a players nao avaliados naquela dimensao em nenhum bench paired — score inferido a partir de tech-research + raciocinio explicitado.

**Como ler:** cada tabela representa uma dimensao. Linhas sao players. Colunas sao Score (numero do scorecard consolidado), Bench fonte primaria (caminho do bench paired que evidencia o score), Citacao textual (cita literal extraida do bench original — sem inferencia), Confidence (H = alto rigor evidencial, M = medium, L = inferido sem teste direto).

---

## D1 — Canais nativos incluindo WhatsApp depth (peso 12%)

| Player | Score | Bench fonte primaria | Citacao textual / evidencia | Confidence |
|---|---:|---|---|---|
| Chatwoot | 93 | `bench/chatwoot-vs-zendesk/scorecard.md` C1 + `bench/intercom-vs-chatwoot/comparison-matrix.md` sec.2 | "Chatwoot: 92 — 10 canais nativos incluindo Telegram + TikTok + 3 BSP options WhatsApp; voice e add-on Enterprise; X removido. WhatsApp BYOC e diferencial real" + "WhatsApp Cloud API: BYOC (cliente conecta WABA propria sem markup); outbound included Startups+" | H |
| Zendesk | 88 | `bench/chatwoot-vs-zendesk/scorecard.md` C1 + `bench/octadesk-vs-zendesk/inventory-zendesk.md` | "Zendesk: 95 — 10 canais nativos incluindo Apple Business Chat + voice Talk first-class; Telegram/TikTok via marketplace" — recalibrado para 88 no consolidado por ausencia de Telegram/TikTok nativos vs Chatwoot/Octadesk | H |
| Intercom | 60 | `bench/intercom-vs-chatwoot/inventory-intercom.md` + `comparison-matrix.md` sec.2 | "Channels [DEEP em-app, MODERATE omnichannel] ... Telegram NAO suportado nativamente"; matriz Intercom-vs-Chatwoot: "Telegram NAO suportado / TikTok NAO suportado / Line NAO suportado" — paridade 1 (sem equivalente) em 3 features de canais BR-relevantes | H |
| Octadesk | 92 | `bench/octadesk-vs-zendesk/inventory-octadesk.md` + `scorecard.md` C1 | "C1 WhatsApp Business API integration: 92 vs 78 (+14 Octadesk). Conversas omnichannel (deep): WhatsApp Business API oficial Meta + Instagram Direct + Facebook Messenger + Email + Webchat (site). Octadesk atua como BSP integrado a Cloud API Meta. Cloud API only: SIM (compatibilidade post-Oct-2025 sunset on-premise)" | H |

---

## D2 — AI capability + transparencia + deflection publicado (peso 18%)

| Player | Score | Bench fonte primaria | Citacao textual / evidencia | Confidence |
|---|---:|---|---|---|
| Chatwoot | 65 | `bench/chatwoot-vs-zendesk/scorecard.md` C2 + `bench/intercom-vs-chatwoot/comparison-matrix.md` sec.1 | "Chatwoot: 75 — Captain AI nativo, built-in. Trade-off: deflection rate nao publicada, credit consumption opaca, maturidade <2 anos" + "Captain — modelo nao disclosed, credits-based, deflection nao publicado". Score 75 no bench-1 recalibrado para 65 no consolidado por consistencia com bench-2 que cita 50 e por "Captain deflection real nao foi publicado nem testado em terceiros" | M |
| Zendesk | 87 | `bench/chatwoot-vs-zendesk/scorecard.md` C2 | "Zendesk: 88 — AI Agents (post-Ultimate.ai) + Copilot + QA AI + WFM. Customer outcomes publicados (39-92% resolucao). Productivity 20% Copilot. Trade-off: per-resolution AI Agents pricing nao publico" — recalibrado para 87 no consolidado | H |
| Intercom | 80 | `bench/intercom-vs-chatwoot/inventory-intercom.md` Fin AI deep specs + `comparison-matrix.md` sec.1 | "Modelo: Fin Apex 1.0 (proprietary, patented). Engine: Fin AI Engine — patented retrieval/reranker. Deflection rate publicado: 51% medio (research aggregators); ate 67% maduro; testimonial Lightspeed cita 65% end-to-end. Improvement claim: +1% resolution rate / mes" | H |
| Octadesk | 70 | `bench/octadesk-vs-zendesk/inventory-octadesk.md` WOZ Agent | "WOZ Agent. Engine declarado: ChatGPT-based (G2 product description). Modos: Autonomous answer, Copilot suggest, Audio transcription, Continuous learning. Deflection rate publicado: nao publico (claim 80% marketing geral, nao validado em benchmark independente). Pricing model: add-on separado, contato comercial" | M |

---

## D3 — Pricing transparency + TCO real (peso 15%)

| Player | Score | Bench fonte primaria | Citacao textual / evidencia | Confidence |
|---|---:|---|---|---|
| Chatwoot | 92 | `bench/chatwoot-vs-zendesk/scorecard.md` C3 + `bench/intercom-vs-chatwoot/scorecard.md` C5 | "Chatwoot: 95 — Tiers publicos claros. Self-host = $0. Sticker-to-real ratio 1.0-1.2x. Delta: +45. Chatwoot clear winner — gap mais expressivo do bench (45 pts)" + "Chatwoot Cloud Business: $95 + credits 300 incl + ~$10 extras = ~$105. Chatwoot Self-hosted: $30-50 infra + $0 license" | H |
| Zendesk | 55 | `bench/chatwoot-vs-zendesk/scorecard.md` C3 | "Zendesk: 50 — $19-$169 base + add-ons necessarios (Copilot $50, QA $35, WFM $25, ADPP $50). Real-world multiplier 2-3x. Vendr median deal $47.772/year. AI Agents per-resolution opaco" — recalibrado para 55 no consolidado | H |
| Intercom | 50 | `bench/intercom-vs-chatwoot/scorecard.md` C5 + `inventory-intercom.md` Pricing | "Intercom Essential $29 / Advanced $85 / Expert $132. Fin AI Agent: $0.99 por resolucao. Sem free tier permanente. 14-day trial only. Custos reais G2 reportam 60-80% acima do sticker — combinacao Fin per-resolution + Copilot + Proactive Support Plus + WhatsApp Meta fees" | H |
| Octadesk | 65 | `bench/octadesk-vs-zendesk/inventory-octadesk.md` Pricing | "Octa Conversas: R$ 1.542. Octadesk Helpdesk: R$ 2.205. Octa Suite: contato comercial. Sea + AI Plan: R$ 2.972 (30 users, 2.000 WA conv/mes). Discrepancia critica versus tech-research: tech-research listou 'a partir de R$79/mes'. Site oficial em 2026-05-06 mostra entry R$1.542/mes. Desvio de ~20x" — Octa Suite gated atras de contato comercial penaliza transparencia | H |

---

## D4 — Governance / Compliance (peso 12%)

| Player | Score | Bench fonte primaria | Citacao textual / evidencia | Confidence |
|---|---:|---|---|---|
| Chatwoot | 55 | `bench/chatwoot-vs-zendesk/scorecard.md` C4 + `bench/intercom-vs-chatwoot/comparison-matrix.md` sec.7 | "Chatwoot: 55 — GDPR DPA. SOC2 Cloud implicit. ISO/FedRAMP/HIPAA NAO listadas. EU residency Cloud nao user-selectable. Self-host = escape valve" + "Compliance certs: GDPR claims; sem SOC2/ISO Cloud publica" | H |
| Zendesk | 95 | `bench/chatwoot-vs-zendesk/scorecard.md` C4 | "Zendesk: 95 — SOC2 Type II + ISO 27001/27018/27701 + FedRAMP + GDPR BCR + HIPAA BAA + multi-region (US/EU/AU/JP). Delta: -40. Zendesk clear winner — gap quase categorical" | H |
| Intercom | 80 | `bench/intercom-vs-chatwoot/inventory-intercom.md` Compliance + `comparison-matrix.md` sec.7 | "SOC2 Type II, GDPR, HIPAA, ISO 27001/27018/27701, CCPA. SSO, SAML, audit logs (Expert). Data residency: EU + US options (Expert)" — falta FedRAMP + BCR + multi-region (US/EU/AU/JP) que Zendesk tem | M |
| Octadesk | 45 | `bench/octadesk-vs-zendesk/inventory-octadesk.md` Compliance + `scorecard.md` C7 | "Compliance publica: LGPD declarada via parent LWSA + pagina dedicada pt.octadesk.com/lgpd. GDPR declarada para WOZ. SOC 2 / ISO 27001: nao publicamente confirmado. Gaps enterprise versus Zendesk (CRITICOS): SSO/SAML/OIDC, SCIM provisioning, Custom agent roles, Audit logs detalhados, Sandbox environment, Multi-help-center, BYOK encryption, HIPAA BAA, PCI-DSS, SOC 2 Type II report, ISO 27001" | H |

---

## D5 — Ecosystem / Marketplace / integracoes (peso 8%)

| Player | Score | Bench fonte primaria | Citacao textual / evidencia | Confidence |
|---|---:|---|---|---|
| Chatwoot | 65 | `bench/chatwoot-vs-zendesk/scorecard.md` C5 + `bench/intercom-vs-chatwoot/comparison-matrix.md` sec.9 | "Chatwoot: 60 — Tens of named integrations + API + DB access self-host. Sem marketplace curado" + "Marketplace: NAO formal" — recalibrado para 65 por API Channels open + source code MIT modificavel | H |
| Zendesk | 95 | `bench/chatwoot-vs-zendesk/scorecard.md` C5 | "Zendesk: 95 — 1.977 apps de 1.136 vendors. 75% ARR marketplace-impacted. AI 21.54%. Sandbox Enterprise. Delta: -35. Zendesk clear winner — network effects sao moat" | H |
| Intercom | 85 | `bench/intercom-vs-chatwoot/inventory-intercom.md` Integracoes | "API: REST + GraphQL. Webhooks: Sim. App Store: 300+ apps. Key: Salesforce, HubSpot, Slack, Stripe, GitHub, Jira, Zapier, Segment, Mixpanel. SDKs: JavaScript, iOS, Android, React Native, Flutter. In-app SDK: Best-in-class — Messenger SDK roda em qualquer SaaS" | H |
| Octadesk | 60 | `bench/octadesk-vs-zendesk/inventory-octadesk.md` Integrations | "Pagina /integracoes ativa. Estimativa: 20-30 integracoes catalogadas. E-commerce BR: VTEX, Tray, NuvemShop, Shopify, Magento. CRM: Salesforce, HubSpot, Pipedrive, RD Station. Ecossistema LWSA: Bling (ERP, mesmo grupo), Vindi (assinaturas), Melhor Envio (logistica), Tray (e-com)" — small marketplace mas LWSA bundle distintivo | H |

---

## D6 — Comunidade / Maturidade / reviews (peso 8%)

| Player | Score | Bench fonte primaria | Citacao textual / evidencia | Confidence |
|---|---:|---|---|---|
| Chatwoot | 78 | `bench/chatwoot-vs-zendesk/scorecard.md` C6 + `bench/intercom-vs-chatwoot/comparison-matrix.md` sec.10 | "Chatwoot: 78 — GitHub 29.1k stars. G2 4.4. 9 anos. Monthly minor releases" + "GitHub stars: 29.100 stars, 7.200 forks. G2 reviews count: 200+. G2 rating: 4.4/5. Release cadence: Monthly publicas (v4.13.0 Apr 2026)" | H |
| Zendesk | 91 | `bench/chatwoot-vs-zendesk/scorecard.md` C6 | "Zendesk: 92 — G2 6.000+ reviews 4.3. 14.8% market share. 19 anos. 88% ease of use cite. BR team" — recalibrado para 91 no consolidado | H |
| Intercom | 85 | `bench/intercom-vs-chatwoot/inventory-intercom.md` Reviews + `comparison-matrix.md` sec.10 | "G2: 4.5/5, 5.000+ reviews. Capterra: 4.5/5, 1.000+. Market share: 12.77%. Top praise (G2): Fin feels human-like, not typical AI; Beautiful, modern interface; Quick escalation; Polished workflows" | H |
| Octadesk | 55 | `bench/octadesk-vs-zendesk/inventory-octadesk.md` Reviews | "G2 Reviews: 55 (G2 product page; rating exato bloqueado por 403). Capterra Brasil — Rating: 4.0/5, Reviews: 6, Recommendation rate: 80%. Top complaints: Stability issues / disconnections / slowdowns reportados (long-term user 4+ anos), Outages com frequencia aumentada no ultimo ano" | M |

---

## D7 — Flexibilidade (self-hosted, customizacao, sovereignty) (peso 10%)

| Player | Score | Bench fonte primaria | Citacao textual / evidencia | Confidence |
|---|---:|---|---:|---|
| Chatwoot | 100 | `bench/chatwoot-vs-zendesk/scorecard.md` C7 + `bench/intercom-vs-chatwoot/scorecard.md` C7 | "Chatwoot: 100 — MIT self-host full source. 4 deployment options. WhatsApp BYOC. Vendor lock-in minimal. Delta: +65. Sem equivalente categorical — gap mais profundo do bench" + "Self-hosted / sovereignty: 100 vs 0 (delta -100). Source code MIT modificavel" | H |
| Zendesk | 35 | `bench/chatwoot-vs-zendesk/scorecard.md` C7 | "Zendesk: 35 — Cloud-only proprietary. Self-host impossivel. Vendor lock-in maximum. Sandbox Enterprise e paliativo (positivo) mas dentro de guardrails Zendesk. O score de 35 do Zendesk reflete que sandbox + apps framework + API openness existem (nao zera), mas nao se aproxima de self-host MIT" | H |
| Intercom | 0 | `bench/intercom-vs-chatwoot/scorecard.md` C7 + `inventory-intercom.md` Fraquezas | "Self-hosted / sovereignty: 0 (Chatwoot 100 vs Intercom 0, delta -100). Self-host = NAO disponivel. Sem self-hosted / OSS option — total vendor lock-in. Sem licenca aberta. Sem comunidade open-source" | H |
| Octadesk | 25 | `untested em bench paired (nao houve par Octadesk vs Chatwoot)`; inferido de `inventory-octadesk.md` + tech-research | Octadesk e SaaS proprietary BR-cloud (LWSA hosting BR). Sem self-host, sem source code aberto. Gap APIs publicos disponiveis (REST + Webhooks) e marketplace LWSA bundle dao alguma flexibilidade operacional. Score 25 reflete: APIs abertas para integracao mas zero data sovereignty / source modification | L |

---

## D8 — Brasil-fit (BSP local, BRL pricing, suporte PT-BR, integracoes BR) (peso 12%)

| Player | Score | Bench fonte primaria | Citacao textual / evidencia | Confidence |
|---|---:|---|---|---|
| Chatwoot | 60 | `bench/chatwoot-vs-zendesk/scorecard.md` C8 | "Chatwoot: 65 — BYOC permite BR BSP. PT-BR UI. Shopify nativa. Sem BRL pricing, VTEX, RD, Pix, BR team" — recalibrado para 60 no consolidado por ausencia de marketplace BR e BR team | H |
| Zendesk | 60 | `bench/chatwoot-vs-zendesk/scorecard.md` C8 + `bench/octadesk-vs-zendesk/scorecard.md` C2 | Bench-1: "Zendesk: 80 — BRL publicado. Suporte BR. Sales BR. Marketplace community RD Station. Caveats: BRL absoluto proibitivo para PME (R$359 = 5x Octadesk)". Bench-3: "C2 Brasil-fit operacional: Octadesk 95 vs Zendesk 50 (+45 Octadesk)". Reconciliacao 3-way: 60 (penalizado por TCO BRL inviavel para PME) | M |
| Intercom | 35 | `untested em bench paired direto contra player BR`; inferido de `bench/intercom-vs-chatwoot/inventory-intercom.md` | Intercom inventory nao cita BRL pricing, BR team, BR sales, BR marketplace. UI multilinguistica generica (pt-PT vs pt-BR exige tooling adicional conforme Fin AI specs). Sem BSP BR oficial. "Linguagens: Multiple (lista oficial nao publicada); pt-BR vs pt-PT requer tooling adicional" — penaliza BR-fit. Score 35 inferido como floor para SaaS US-only sem BR localization | L |
| Octadesk | 95 | `bench/octadesk-vs-zendesk/scorecard.md` C2 + `inventory-octadesk.md` | "C2 Brasil-fit operacional: 95 vs 50 (+45 Octadesk). Idioma nativo PT-BR: SIM (vantagem clara vs incumbents traduzidos). Pacote LWSA group: ecossistema BR de e-commerce (Bling ERP, Tray e-com, Vindi, Melhor Envio, Yapay). UX em portugues nativo end-to-end (sem traducao de SaaS gringo). Tracao com e-commerce BR (logos Pfizer, Locaweb, QuintoAndar)" | H |

---

## D9 — In-app messaging strength (peso 5%)

| Player | Score | Bench fonte primaria | Citacao textual / evidencia | Confidence |
|---|---:|---|---|---|
| Chatwoot | 50 | `bench/intercom-vs-chatwoot/scorecard.md` C4 + `comparison-matrix.md` sec.2 | "C4 In-app messaging strength: Intercom 95 vs Chatwoot 50 (+45 Intercom). In-app Messenger: Best-in-class (SDK iOS/Android/Web/RN/Flutter polido) vs Widget chat customizavel; SDK menos profundo (paridade 3)" | H |
| Zendesk | 70 | `untested em bench paired focado em in-app messaging`; inferido de `bench/chatwoot-vs-zendesk/inventory-zendesk.md` + comparison-matrix | Zendesk Messaging + Web Widget oferecem in-app messaging proprio mas sem o polish do Intercom Messenger. SDK iOS/Android disponiveis. Score 70 reflete: in-app existe e e enterprise-grade, mas nao e categorical winner como Intercom. Recalibrado a partir de bench-1 indices de canais (95) reduzido para 70 no consolidado focando especificamente em in-app messaging strength (nao breadth de canais) | M |
| Intercom | 95 | `bench/intercom-vs-chatwoot/scorecard.md` C4 + `inventory-intercom.md` Channels | "C4 In-app messaging strength: Intercom 95 vs Chatwoot 50, delta +45 Intercom. In-app Messenger (best-in-class — sem rival). In-app SDK: Best-in-class — Messenger SDK roda em qualquer SaaS. SDKs: JavaScript, iOS, Android, React Native, Flutter" — paridade 1 (sem equivalente) em Product Tours | H |
| Octadesk | 40 | `untested — Octadesk nao foi avaliado em bench focado em in-app messaging` | Inventory Octadesk lista "Webchat (site)" como canal omnichannel mas sem feature dedicada de in-app messenger SDK. Foco da plataforma e WhatsApp + canais BR, nao in-app SaaS B2B. Score 40 inferido: webchat basico existe (>0) mas sem SDK polished iOS/Android/RN/Flutter, sem Product Tours, sem outbound polished — penalizado vs Intercom polish e Zendesk enterprise SDK | L |

---

## Sumario de cobertura

| Dimensao | Players com bench-evidencia direta | Players com inferencia (untested) | Confidence dominante |
|---|---|---|---|
| D1 Canais | Chatwoot, Zendesk, Intercom, Octadesk | — | H |
| D2 AI | Chatwoot, Zendesk, Intercom, Octadesk | — | H/M |
| D3 Pricing | Chatwoot, Zendesk, Intercom, Octadesk | — | H |
| D4 Compliance | Chatwoot, Zendesk, Intercom, Octadesk | — | H/M |
| D5 Ecosystem | Chatwoot, Zendesk, Intercom, Octadesk | — | H |
| D6 Maturidade | Chatwoot, Zendesk, Intercom, Octadesk | — | H/M |
| D7 Flexibilidade | Chatwoot, Zendesk, Intercom | Octadesk | H/L |
| D8 BR-fit | Chatwoot, Zendesk, Octadesk | Intercom | H/M/L |
| D9 In-app | Chatwoot, Intercom | Zendesk, Octadesk | H/M/L |

**Cells com confidence L (untested):**
1. **D7 Octadesk** — sem bench paired contra OSS/self-host; score 25 inferido de inventory + tech-research
2. **D8 Intercom** — sem bench paired contra player BR-native; score 35 inferido como floor SaaS US-only
3. **D9 Zendesk** — sem bench paired focado especificamente em in-app messaging; score 70 inferido de breadth-channels-strength
4. **D9 Octadesk** — sem bench paired focado em in-app; score 40 inferido de inventory canais

**Resumo:** 4 dimensoes (D1, D2, D3, D5) tem evidencia direta para os 4 players. 5 dimensoes tem ao menos 1 player com confidence L (inferencia). Resolucao das celulas L recomendada em fase B (validation pass).

---

## Cross-refs

- Scorecard consolidado com pesos e personas → `consolidated-scorecard.md`
- Triangulacao de reconciliacoes (bench-1 vs bench-3 para Zendesk; bench-1 vs bench-2 para Chatwoot) → `triangulation-analysis.md` (fase B)
- Decisao final por persona → `final-recommendation-matrix.md` (fase B)
- Dados estruturais → `consolidated-scorecard.json`
- Benches fonte:
  - `docs/bench/chatwoot-vs-zendesk/`
  - `docs/bench/intercom-vs-chatwoot/`
  - `docs/bench/octadesk-vs-zendesk/`
