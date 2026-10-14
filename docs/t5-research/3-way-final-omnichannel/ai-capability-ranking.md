# AI Capability Ranking — 3-Way Final Omnichannel

**Bench:** 3-way-final-omnichannel
**Data:** 2026-05-06
**Escopo:** Ranking comparativo das capacidades de IA (agentic AI + copilot + QA) entre os 4 players do bench: Zendesk AI Agents, Intercom Fin, Octadesk WOZ, Chatwoot Captain.
**Metodo:** Consolidacao da dimensao D2 (AI capability) dos 3 paired benches. Sem web research — apenas dados ja extraidos. Confidence H/M/L explicitada por celula.

## TL;DR

**Zendesk AI Agents lidera em maturity, Intercom Fin lidera em transparencia, WOZ lidera em BR-native, Captain promissor mas underprovado.**

| Rank | Player | Score D2 | AI Engine | Pricing model | Deflection publicado |
|------|--------|---------:|-----------|---------------|----------------------|
| 1 | **Zendesk AI Agents** | **87** | post-Ultimate.ai + Copilot + QA AI | per-resolution + $50/agent Copilot | 39-92% (varies, customer outcomes publicados) |
| 2 | **Intercom Fin** | **80** | Fin Apex 1.0 (proprietary, patenteado) | $0.99/resolution | **51-67% medio** (publico, multiplas fontes) |
| 3 | **Octadesk WOZ** | **70** | Generative AI (ChatGPT-based, declarado em G2) | sob consulta (gated) | nao publicado (claim marketing 80%) |
| 4 | **Chatwoot Captain** | **65** | Captain (LLM-backed, modelo nao disclosed) | credits ($20/1.000 + 300-800 incluso por tier) | **nao publicado** |

**Sumario:** Zendesk vence em breadth+outcomes publicados; Intercom vence em transparencia tecnica + deflection benchmarked; Octadesk vence em PT-BR nativo (unico entre os 4); Captain promissor mas opaco em outcomes.

---

## 1. Detalhamento por player

### 1.1 Zendesk AI Agents (post-Ultimate.ai)

**Score D2 consolidado:** 87 (Bench 1 deu 88; arbitragem D2 consolidado=87 reflete media com triangulacao)

#### Engine

- **Origem:** Aquisicao de Ultimate.ai (2024) + integracao no produto Zendesk Suite. Pre-aquisicao, "Answer Bot" da Zendesk tinha capabilities mais limitadas; pos-Ultimate.ai a capacidade subiu para nivel Agentic AI (autonomous resolution).
- **Modelo subjacente:** nao disclosed publicamente pos-aquisicao Ultimate.ai. Bolted-on (nao native from-scratch).
- **Tagline oficial:** "AI Agents for autonomous resolution + Copilot for agent productivity + QA AI for quality monitoring + WFM for forecasting/scheduling".

#### Customer outcomes publicados

- **Range publicado:** 39-92% deflection/autonomous resolution (varies por customer/use case).
- **Productivity claim:** 20% productivity gain via Copilot.
- **Maturidade:** ecossistema mais maduro entre os 4, com produtos AI especializados (Copilot, QA AI, WFM) cobrindo agent productivity + quality + workforce planning.

#### Ecossistema AI

| Produto | Funcao | Pricing |
|---|---|---|
| **AI Agents** | Autonomous resolution (deflection) | per-resolution (nao publico) |
| **Copilot** | Agent assist + draft replies + summarization | $50/agent/mo |
| **QA AI** | Conversation quality monitoring + scoring | $35/agent/mo |
| **WFM** | Workforce management (forecast + schedule) | $25/agent/mo |
| **ADPP** | Advanced Data Privacy & Protection (encryption, redaction) | $50/agent/mo |

#### Pontos fortes

- **Maturidade:** ecossistema mais amplo entre os 4 (AI Agents + Copilot + QA + WFM em produtos dedicados).
- **Outcomes publicados:** range 39-92% e o unico bench em que vendor publica % de deflection com customer cases.
- **Breadth:** unico player com QA AI dedicada e WFM nativa.
- **Compliance:** ADPP (Advanced Data Privacy) + SOC2 + ISO27001/27018/27701 + FedRAMP + HIPAA BAA.

#### Pontos fracos

- **Per-resolution opaco:** AI Agents pricing per-resolution NAO e publico (negociado por contrato). Bench 1 cita Vendr median deal $47.772/year inclui mistura de tiers.
- **Bolted-on de aquisicao:** Ultimate.ai integrado pos-2024; algumas areas ainda mostram costuras (UI separada, terminologia divergente em alguns flows).
- **Add-on stack acumulativo:** Suite + Copilot + QA + WFM + ADPP rapidamente multiplica TCO 2-3x sticker.

#### Pricing

- AI Agents: per-resolution **nao publico** (gated em sales).
- Copilot: $50/agent/mo (publico).
- QA AI: $35/agent/mo (publico).
- WFM: $25/agent/mo (publico).
- ADPP: $50/agent/mo (publico).

**Source:** Bench 1 (`chatwoot-vs-zendesk/scorecard.md` C2) + `consolidated-scorecard.md` D2.

---

### 1.2 Intercom Fin

**Score D2 consolidado:** 80 (Bench 2 deu Intercom AI=85; consolidado=80 reflete arbitragem com peso para D2 redefinido como "AI capability + transparencia + deflection publicado")

#### Engine

- **Modelo:** **Fin Apex 1.0** — proprietary, patenteado.
- **Engine:** Fin AI Engine (patenteada).
- **Pipeline RAG documentado** (6 steps):
  1. Query refinement
  2. Content retrieval (`fin-cx-retrieval` model patenteado)
  3. Reranking (`fin-cx-reranker` model patenteado)
  4. Response generation (Fin Apex 1.0)
  5. Accuracy validation (safety standards)
  6. Engine optimization
- **Patentes:** Fin Engine + retrieval + reranker patenteados. Intercom investiu 3+ anos R&D em pipeline proprietary.
- **Tagline oficial:** "The highest-performing, fastest model for customer service".

#### Deflection metrics publicados

| Metrica | Valor | Source |
|---|---|---|
| Deflection medio | **51%** | Aggregadores Fin Labs |
| Deflection maduro | **65-67%** | Vendor + Lightspeed testimonial |
| Improvement claim | **+1%/mes** | fin.ai marketing |
| Conversation involvement | **99%** | Lightspeed testimonial publico |
| Industry benchmark Fin Labs | Agentic AI 70-85% range | Fin Labs (90 dias, 2.000+ queries, 10 industries) |

**Diferencial chave:** Intercom e o **unico player que publica deflection rate** entre os 4. Esse fato (nao opiniao) e a base do score D2=80 (penalizado vs Zendesk 87 apenas por menor breadth — sem QA AI nem WFM dedicadas).

#### Pontos fortes

- **Deflection publicada e benchmarked:** unico vendor com numeros validados publicamente (Lightspeed 65% end-to-end + 99% involvement).
- **Modelo honesto:** Fin Apex 1.0 nomeado, pipeline RAG documentado em 6 steps, patentes publicas.
- **In-app integration premium:** Intercom Messenger + Fin combinam para D9=95 (in-app messaging categorical winner).
- **Custom AI actions:** Fin pode executar ações reais (refunds, trial extensions, system calls) — feature ausente em Captain.
- **Pre-deploy simulation:** simulacao em ambiente sandbox antes de deploy live — feature ausente em Captain.
- **Hallucination control:** Step 5 explicito do pipeline + safety standards + ISO27001/27018/27701 + GDPR + CCPA compliance.
- **Standalone integrations:** Fin Standalone roda dentro de Zendesk, Salesforce, HubSpot, Freshdesk, Dixa, Front, Zoho, Sprinklr — clientes desses competitors escolheram Fin sobre os AI nativos.

#### Pontos fracos

- **BR-fit baixo:** pricing 100% USD, sem time produto BR, sem integracoes VTEX/RD/Bling, sem suporte PT-BR formal (CQ-3WAY-004).
- **Per-resolution explode em volume:** $0.99/resolution × 12k resolutions/mo = **$11.880/mo** apenas Fin (antes da Suite). Em scale 20k conv/mo, gap de pricing vs Chatwoot Captain pode pagar 5-8 agentes humanos extras.
- **Cloud-only:** Intercom inteiro e Cloud, sem self-host disponivel (D7=0). GDPR strict EU requer Dublin region (multi-region disponivel mas nao customer-controlled).
- **Sem QA AI nem WFM dedicadas:** apenas Fin (deflection) + Copilot, sem produtos especializados como Zendesk.

#### Pricing

- Fin Resolutions: **$0.99/resolution** (transparente, publicado).
- Intercom Suite base: $39-$139/agent/mo (varies por tier).
- TCO exemplo SMB 5k conv/mo: $5k Fin + Suite ~$10k/mo.

**Source:** Bench 2 (`intercom-vs-chatwoot/deep/ai-capability.md`) + `consolidated-scorecard.md` D2.

---

### 1.3 Octadesk WOZ

**Score D2 consolidado:** 70 (Bench 3 deu Octadesk AI=70; preservado no consolidado com confidence M — single-source bench, sem cross-validation)

#### Engine

- **Modelo:** Generative AI **ChatGPT-based** (declarado em G2 product description).
- **Capabilities:**
  - Atendimento autonomo IA generativa 24/7
  - Sugestao de respostas em tempo real (copilot)
  - Transcricao automatica de audios em texto (canal WhatsApp BR heavy)
  - Identifica lacunas de conhecimento e melhora respostas continuamente
  - Isolamento de dados entre clientes (declarado vendor-side)

#### Diferencial unico (categorical)

- **PT-BR nativo end-to-end** — UNICO entre os 4 players. UX, copilot suggestions, audio transcription, training data: tudo treinado em portugues brasileiro nativo, nao traducao de SaaS gringo.
- **Audio transcription nativa:** essencial para canal WhatsApp BR (audio messages sao 30-50% do volume em e-commerce BR PME).
- **Bundle LWSA:** integrado com pipeline atendimento + Bling ERP + Tray e-com + Vindi assinaturas + Melhor Envio logistica + Yapay (mesmo grupo controlador).

#### Deflection publicado

- **Marketing claim:** "Resolva 8 a cada 10 atendimentos automaticamente, 24h por dia" = 80% deflection.
- **Realidade benchmarked:** **NAO publicado** — sem benchmark independente.
- **Hipotese consolidada (CQ-3WAY-002):** WOZ entrega 50-70% deflection em casos WhatsApp B2C BR (caso de uso primario), <40% em casos cross-channel ou B2B. Marketing claim de 80% provavelmente inflado.

#### Pontos fortes

- **BR-native:** UX + AI training + audio transcription tudo em PT-BR nativo. Diferencial categorical.
- **Integrado com pipeline atendimento:** pipeline Octadesk (omnichannel + ticketing) ja usa WOZ embedded, sem segunda configuracao.
- **Bundle LWSA:** ecossistema BR proprio (Bling/Tray/Vindi/Melhor Envio) acelera ROI para PME e-commerce.
- **Audio transcription:** essencial para canais WhatsApp BR voice-heavy.

#### Pontos fracos

- **Deflection NAO publicado:** sem outcomes auditados, marketing claim 80% nao validado.
- **Pricing gated:** WOZ pricing nao publico — contato comercial obrigatorio.
- **Engine nao proprietary:** ChatGPT-based (declarado em G2) — vulneravel a OpenAI pricing/API changes, sem moat tecnologico.
- **Sem custom AI actions documentadas:** nao publicado se WOZ pode executar refunds, system calls, etc (vs Fin que documenta explicitamente).
- **Sem simulation mode:** sem sandbox pre-deploy documentado.
- **Sem QA AI dedicada:** apenas autonomous + copilot, sem produto QA separado.
- **Reviews G2 sinalizam instabilidade:** 4+ anos de uso reportam outages com frequencia aumentada no ultimo ano.
- **Estrutura enterprise minima:** sem SOC2/ISO27001 publicamente confirmado (apenas LGPD via parent LWSA).

#### Pricing

- **WOZ pricing:** sob consulta (gated) — contato comercial obrigatorio.
- **Plano Octadesk Sea + AI:** R$2.972/mo (30 users, 2.000 WA conv/mo, 1 numero) — inclui WOZ basico (escopo exato gated).
- **Higher Tier:** R$ nao publico, 50 users, 5.000 WA conv/mo.

**Source:** Bench 3 (`octadesk-vs-zendesk/inventory-octadesk.md` + scorecard) + `consolidated-scorecard.md` D2.

---

### 1.4 Chatwoot Captain

**Score D2 consolidado:** 65 (INC-01 reconciliado: Bench 1 deu 75, Bench 2 deu 50; consolidado=65 e media ponderada com peso para "deflection nao publicado" como fato confirmado em ambos benches)

#### Engine

- **Modelo:** **NAO disclosed** — vendor opaco. eesel.ai third-party review sugere wrapper sobre OpenAI/Anthropic API + Chatwoot RAG + UX layer.
- **Engine name:** Captain (sem brand publicada de engine).
- **Tagline oficial:** "AI Agent for Customer Support".
- **Disponibilidade:** Cloud-only (NAO disponivel em self-hosted Community edition — quebra promessa OSS para sovereignty buyers).

#### Capabilities

- Reply suggestions
- Summarization (conversation summary)
- Co-pilot (draft replies + suggestions)
- Smart FAQs
- Memories (per-conversation context)
- Content gap analysis (identifica artigos que faltam no help center)

#### Deflection publicado

- **Vendor-side:** **NAO publicado oficialmente**.
- **Third-party assessment:**
  - eesel.ai blog 2025: "functional but more basic" / "lacks deep knowledge ingestion"
  - atomixweb article 2026: "fancy FAQ bot tier"
- **Estimativa consolidada (INC-01 + CQ-3WAY-001):**
  - Conservative: 25-35% deflection (RAG-only tier)
  - Aggressive: 40-50% (RAG-strong tier)
  - Gap vs Fin (55-65%): 10-35 pontos percentuais

#### Pontos fortes

- **Built-in:** Captain e nativo do Chatwoot, sem integracao adicional necessaria.
- **Credit pricing transparente:** 300-800 credits/mes incluso por tier; $20/1.000 credits extras (modelo previsivel vs Fin per-resolution opaco em escalas grandes — mas vide ressalva abaixo).
- **8 linguagens demonstradas:** English, Spanish, French, German, **Portuguese**, Japanese, Chinese, Arabic + Malayalam (marketing-shown). Comunidade Brasil ativa.
- **Pricing 5x menor que Fin** em mid-market: economia em scale 5k conv/mo paga 1-2 agentes humanos extras com sobra.

#### Pontos fracos (P0 segundo Bench 2 GAP-CW-01)

- **Modelo NAO disclosed:** sem auditing, predictability, debugging em producao.
- **Deflection rate NAO publicado:** P0 gap competitivo. Sem outcomes benchmarked, Captain perde batalhas pre-sale para Fin.
- **Sem custom AI actions:** Captain nao executa refunds, trial extensions, system calls (Fin executa).
- **Sem simulation mode:** sem sandbox pre-deploy.
- **Hallucination control NAO endereado publicamente:** sem mention de safety standards, accuracy validation steps, ou governance.
- **NAO disponivel em self-hosted Community:** quebra promessa OSS — sovereignty buyers nao podem rodar Captain on-prem.
- **Maturidade <2 anos:** comparado a Fin Apex 1.0 (3+ anos R&D) e Zendesk AI (post-Ultimate.ai 2024).
- **RAG basico:** help center + chats apenas; sem "procedures formais" como source (vs Fin que treina em policies textuais).

#### Pricing

- **Credits inclusos por tier:** Startups 300/mo, Business 500/mo, Enterprise 800/mo.
- **Credits extras:** $20/1.000.
- **Self-host:** Captain **NAO disponivel** (limitacao critica para OSS users).
- TCO exemplo SMB 5k conv/mo Cloud Business: ~$2k/mo (incluindo creditos) — **5-7x menor que Intercom Fin** equivalente.

**Source:** Bench 2 (`intercom-vs-chatwoot/deep/ai-capability.md`) + Bench 1 (`chatwoot-vs-zendesk/scorecard.md` C2) + `triangulation-analysis.md` INC-01.

---

## 2. Tabela comparativa head-to-head

| Aspecto | Zendesk AI Agents | Intercom Fin | Octadesk WOZ | Chatwoot Captain | Vencedor |
|---|---|---|---|---|---|
| **Score D2 consolidado** | **87** | 80 | 70 | 65 | Zendesk |
| Modelo publicado | NAO disclosed (post-Ultimate.ai) | **Fin Apex 1.0 (proprietary)** | ChatGPT-based (declarado G2) | NAO disclosed | Intercom |
| RAG pipeline detalhado | Parcial (pos-aquisicao) | **6 steps documentados + 2 patentes** | Nao publicado | NAO publicado | Intercom |
| Patentes | Nenhuma publica | **Fin Engine + retrieval + reranker** | Nenhuma | Nenhuma | Intercom |
| Deflection rate publicado | **39-92% range (customer outcomes)** | **51-67% medio + maduro** | NAO publicado (claim 80% marketing) | NAO publicado | Empate Zendesk/Intercom |
| Improvement claim | Nao publico | +1%/mo | Continuous learning declarado | Nao publico | Intercom |
| Custom AI actions (refunds, system calls) | Sim | **Sim** | Nao documentado | NAO suportado | Intercom |
| Pre-deploy simulation | Sim | **Sim** | Nao documentado | NAO suportado | Intercom |
| Hallucination control | Standards + ADPP | **Step 5 explicito + ISO27001/27018/27701** | Nao endereado | NAO endereado | Intercom |
| Persona / tom granular | Sim (Copilot guidance) | **Sim (Fin Persona formal)** | Customizavel basico | Mais basico (instructions) | Intercom |
| Escalation logic | Documentado (workflow rules) | **Documentado granular (4 triggers)** | Nao publicado | Basico | Intercom |
| QA AI dedicada | **Sim (QA AI $35/agent)** | Nao | Nao | Nao | Zendesk |
| WFM dedicada | **Sim (WFM $25/agent)** | Nao | Nao | Nao | Zendesk |
| PT-BR nativo end-to-end | Suportado (BRL pricing + sales BR) | Suportado (configuracao adicional) | **Nativo (treinamento + UX + audio)** | Suportado (8 langs marketing) | **Octadesk** |
| Audio transcription nativa | Sim (via Talk addon) | Limitada | **Sim (WhatsApp BR voice)** | Nao publico | Octadesk |
| Built-in vs add-on | Add-on (post-aquisicao) | Native (Cloud-only) | **Native (integrado pipeline)** | **Native (built-in, Cloud-only)** | Empate Octadesk/Captain |
| Disponivel em self-hosted | N/A (Cloud-only) | N/A (Cloud-only) | N/A (Cloud-only) | NAO disponivel | Nenhum |
| Pricing model | per-resolution (opaco) + add-ons fixos | **$0.99/resolution (transparente)** | sob consulta (gated) | **credits 300-800/tier + $20/1k extras (transparente)** | Empate Intercom/Captain |
| TCO 5k conv/mo | ~$8-15k/mo (Suite + AI Agents + Copilot + QA) | ~$10k/mo (Fin + Suite) | ~R$3-5k/mo (BRL, gated quote) | **~$2k/mo (Business + creditos)** | Captain |
| Customer base AI publico | 39-92% range com customer cases | **Lightspeed 65% deflection + 99% involvement** | 2.500+ empresas (claim global, sem AI-specific) | Sem testimonials publicos com numeros | Intercom |

---

## 3. Analise por persona

| Persona | Top AI | Por que |
|---------|--------|---------|
| **SMB BR e-com** | **WOZ ou Captain** | TCO baixo + BR-native (WOZ) ou credit-friendly (Captain). WOZ vence se equipe nao tem DevOps + bundle LWSA. Captain vence se equipe tem DevOps + cost-conscious + multi-channel ja consolidado. |
| **Mid-market BR** | **Zendesk AI Agents** | Outcomes publicados + breadth (Copilot + QA + WFM). Para mid-market que precisa AI confiavel + agent productivity + quality monitoring, breadth Zendesk vence Captain underprovado e WOZ single-channel-heavy. |
| **Enterprise BR multinacional** | **Zendesk AI Agents** | Compliance (SOC2 + ISO27001/27018/27701 + FedRAMP + HIPAA + ADPP) + maturity + customer outcomes range publicado. Mandatory para healthcare BR / fintech BR / governo. Fin chega proximo mas in-app focus + sem WFM/QA dedicadas reduz fit. |
| **Global SaaS B2B in-app** | **Intercom Fin** | Per-res transparente ($0.99) + in-app native (D9=95 categorical) + deflection benchmarked (51-67%) + custom actions + simulation + hallucination control documentado + Fin Standalone disponivel em Zendesk/Salesforce/HubSpot. Para SaaS B2B onde in-app messaging e core do produto, Fin domina. |

### Decision tree por persona

```
Tenho cliente PME BR e-commerce com volume 1-5k conv/mo?
├── SIM → WOZ (BR-native + bundle LWSA + audio transcription PT-BR) OU Captain ($2k/mo Cloud Business)
│       └── Tiebreaker: equipe tem DevOps interno? SIM → Captain. NAO → WOZ.
│
Tenho cliente mid-market BR 50-100 agents com volume 10k+ conv/mo?
├── SIM → Zendesk AI Agents (breadth + outcomes + Copilot + QA + WFM)
│       └── Caveat: TCO 2-3x sticker ($45-75k/year all-in) — validar budget upfront.
│
Tenho cliente enterprise BR regulado (healthcare/fintech/governo) multi-region?
├── SIM → Zendesk AI Agents mandatory (compliance posture categorical)
│
Tenho cliente Global SaaS B2B in-app heavy EU+US 20-30 agents?
├── SIM → Intercom Fin (in-app + per-res transparente + deflection publicado)
│       └── Caveat: BR-fit baixo (D8=35) — descartar se cliente tem operacao BR significativa.
```

---

## 4. Inconsistencias resolvidas

### INC-01 — Chatwoot AI score: 75 (Bench 1) vs 50 (Bench 2) → consolidado **65**

**Discrepancia raw:**

- **Bench 1 (`chatwoot-vs-zendesk/scorecard.md` C2):** Chatwoot AI=75. Justificativa: "Captain AI nativo, built-in. Trade-off: deflection rate nao publicada, credit consumption opaca, maturidade <2 anos." Avaliou Captain como "presente e funcional", penalizou opacidade. Comparacao foi vs Zendesk (88) — referencial mais alto.
- **Bench 2 (`intercom-vs-chatwoot/scorecard.md` C1):** Chatwoot AI=50. Justificativa: "Captain credits 300/500/800 por tier mas sem benchmarked deflection rate, sem custom actions, sem simulation mode." Avaliou contra Fin Apex 1.0 (51-67% deflection publicado), score deprimido pela falta de outcomes. Bench 2 GAP-CW-01 classificou como **P0** ("Captain perde batalhas pre-sale para Fin").

**Reconciliacao:**

A divergencia e **diferenca de criterio do que esta sendo medido**:

- Bench 1 mediu **AI capability breadth** (presenca + Built-in vs add-on opacity).
- Bench 2 mediu **AI deflection performance** (outcomes publicados, mature pipeline).

No consolidated-scorecard, dimensao D2 (peso 18%) foi **recomposta como "AI capability + transparencia + deflection publicado"** — combina os dois angulos. Score adotado: **D2 Chatwoot = 65** (media ponderada com peso maior para "deflection nao publicado", que e fato confirmado em ambos benches, vs "Captain existe", que tambem e fato).

**Severidade competitiva e persona-driven:**

- Em Persona D (Global SaaS B2B, peso D2=20%): Captain gap e **P0**. Sem deflection benchmarked, perde pre-sale para Fin.
- Em Persona A (SMB BR e-com, peso D2=8%): Captain gap e **P2**. TCO 5x menor compensa underperformance moderada.

**Confidence pos-arbitragem:** M — vendor nao publica deflection rate, ambos benches concordam neste fato.

**Curiosity query:** CQ-3WAY-001 (Captain AI deflection rate real via POC 30 dias) endereca a ressonancia. Sem POC ou customer case com numero, score nao sobe acima de 65.

---

## 5. Pendencias (curiosity queue)

### CQ-3WAY-001 — Captain AI deflection rate real (Chatwoot)

**Status:** untested em todos os benches.

**Hipotese atual:**
- Conservative: 25-35% deflection (RAG-only tier)
- Aggressive: 40-50% (RAG-strong tier)
- Gap vs Fin (55-65%): 10-35 pontos percentuais

**Resolucao proposta:**
- POC 30 dias em customer real (10k conv/mes, mix B2C+B2B), comparando Captain vs Fin vs Zendesk AI Agents na mesma base de dados.
- OU: scrape de case studies + G2 reviews texto-livre buscando numeros mencionados.
- OU: solicitar a Chatwoot Inc um benchmark publico via canal de partnerships.

**Impacto se H:** D2 Chatwoot pode subir para 75-80 (se >50%) ou cair para 50 (se <30%). Decisao Persona D depende disso.

**Bench follow-up:** `chatwoot-captain-ai-poc-2026-Q3`.

---

### CQ-3WAY-002 — WOZ AI deflection rate real (Octadesk)

**Status:** vendor publica claim marketing 80% mas sem benchmark independente. Bench 3 GAP-OCT-05 classifica como MEDIUM.

**Hipotese atual:**
- WOZ entrega 50-70% deflection em casos WhatsApp B2C BR (caso de uso primario), <40% em casos cross-channel ou B2B.
- Vendor claim de 80% provavelmente inflado.

**Resolucao proposta:**
- POC 30 dias em customer Octadesk real (5k conv/mes WhatsApp BR), comparando WOZ vs Captain vs Fin.
- OU: solicitar a LWSA case studies com numeros validados por terceiros.

**Impacto se H:** D2 Octadesk pode subir para 80 (se claim de 80% se sustentar) ou cair para 55 (se for <40%).

**Bench follow-up:** `octadesk-woz-ai-poc-2026-Q3`.

---

### CQ-3WAY-AI-001 — Comparativo head-to-head Captain vs Fin em mesmas queries

**Status:** untested em todos os benches.

**Hipotese atual:**
- Em queries simples (FAQ deflection 1k conv/mo B2C): Captain e Fin convergem em deflection (~40-55%).
- Em queries complexas (multi-step troubleshooting, policy-aware decisions, custom actions): Fin domina por 20-30 pontos percentuais.

**Resolucao proposta:**
- Bench dedicado side-by-side em customer com volume real, dataset identico, mesma janela temporal.
- Minimum: 1.000 queries, distribuicao FAQ + multi-step + complex equilibrada.

**Impacto se H:** Se gap real for <15pp em queries simples, narrative "Captain e fancy FAQ bot" cai. Se >25pp, narrative se confirma e Captain D2 cai para 50.

**Bench follow-up:** `captain-vs-fin-headhead-bench-2026-Q3`.

---

### CQ-3WAY-AI-002 — Zendesk AI Agents per-resolution pricing publico

**Status:** Zendesk nao publica pricing per-resolution AI Agents. Bench 1 cita Vendr median deal $47.772/year mas mistura tiers.

**Hipotese atual:** $0.50-$1.50/resolution range, varies por tier + commitment + use case.

**Resolucao proposta:**
- Solicitar quote formal a Zendesk vendas para 50 agents + 10k resolutions/mo.
- Cross-check com Vendr/Tropic/Sastrify (pricing intelligence platforms) para benchmarks reais.

**Impacto se H:** TCO Zendesk fica predictable. Comparison head-to-head com Fin $0.99/res se torna mensuravel.

**Bench follow-up:** Pricing intelligence batch — incluir AI Agents per-resolution no proximo refresh.

---

### CQ-3WAY-AI-003 — Hallucination rate real (todos os 4)

**Status:** untested em todos os benches. Apenas Intercom publica step explicito + standards.

**Hipotese atual:**
- Fin: hallucination rate <5% (inferencia conservadora vs vendor positioning).
- Zendesk AI Agents: hallucination rate 5-10% (post-Ultimate.ai, sem benchmark publico).
- WOZ: hallucination rate desconhecido (sem benchmark, ChatGPT-based dependente OpenAI quality).
- Captain: hallucination rate desconhecido (RAG basico, third-party sugere "lacks deep knowledge ingestion").

**Resolucao proposta:**
- POC com 500 queries customizadas + ground truth dataset, medir taxa de respostas factualmente incorretas.
- Para regulated industries (legal, medical, finance), gating pre-deploy obrigatorio.

**Impacto se H:** Para Persona C (Enterprise BR multinacional regulado), hallucination rate >10% pode ser blocker categorical mesmo com compliance certificada.

**Bench follow-up:** `ai-hallucination-bench-2026-Q4` (cross-vendor, ground-truth driven).

---

## 6. Confidence summary

| Player | D2 score | Confidence | Fonte primaria | Dependencias para subir |
|---|---:|---|---|---|
| Zendesk AI Agents | 87 | M-H | Bench 1 + customer outcomes range publico | CQ-AI-002 (per-res pricing) + CQ-AI-003 (hallucination) |
| Intercom Fin | 80 | **H** | Bench 2 deep dive + Lightspeed + Fin Labs + patentes publicas | CQ-AI-001 (head-to-head) opcional |
| Octadesk WOZ | 70 | M | Bench 3 single-source (sem cross-validation) | CQ-3WAY-002 (deflection real) + CQ-AI-003 |
| Chatwoot Captain | 65 | M | Bench 1 + Bench 2 INC-01 reconciliado | CQ-3WAY-001 (deflection real) + CQ-AI-001 |

**Distribuicao:** 1/4 H (Intercom Fin), 3/4 M (Zendesk, Octadesk, Captain). Nenhum L. Bench tem rigor evidencial razoavel para suportar ranking persona-driven, com gates claros para resolucao em fase B.

---

## 7. Veredito final

**Zendesk AI Agents lidera em maturity** — breadth (AI Agents + Copilot + QA AI + WFM) + customer outcomes range publicado (39-92%) + compliance posture categorical (SOC2/ISO/FedRAMP/HIPAA/ADPP). Default para mid-market+ e enterprise regulado. Trade-off: TCO 2-3x sticker + per-resolution opaco + bolted-on de aquisicao.

**Intercom Fin lidera em transparencia** — modelo nomeado (Fin Apex 1.0) + pipeline RAG documentado em 6 steps + 2 patentes publicas + deflection benchmarked (51-67% medio, 65% Lightspeed) + per-res transparente ($0.99) + custom actions + simulation + hallucination control documentado. Categorical para Global SaaS B2B in-app heavy. Trade-off: BR-fit baixo + per-res explode em volume + Cloud-only.

**Octadesk WOZ lidera em BR-native** — UNICO entre os 4 com PT-BR nativo end-to-end (UX + AI training + audio transcription) + bundle LWSA (Bling/Tray/Vindi/Melhor Envio). Categorical para SMB BR e-commerce. Trade-off: deflection nao publicado + pricing gated + ChatGPT-based sem moat tecnologico + reviews sinalizam instabilidade.

**Chatwoot Captain promissor mas underprovado** — built-in + credit pricing transparente + 5x mais barato que Fin + 8 linguagens demonstradas. Funcional para casos simples (FAQ deflection B2C). Trade-off P0: deflection NAO publicado + modelo NAO disclosed + sem custom actions + sem simulation + sem hallucination control + NAO disponivel em self-hosted (quebra promessa OSS) + maturidade <2 anos.

**Sinal estrategico:** Captain parity em 12-18 meses (modelo publicado + deflection benchmarked + custom actions + simulation + self-hosted via BYOLM) fechara janela competitiva e dominacao OSS sera total. Fin Apex 2.0 + investimento sustained em AI lock-in e a unica defesa Intercom contra Chatwoot pricing pressure. Se Fin parar evoluir, Chatwoot fecha gap em 24 meses.

---

## Cross-refs

- `consolidated-scorecard.md` — matriz neutra 4x9 + persona recalibrations
- `triangulation-analysis.md` — INC-01 reconciliacao Chatwoot AI 75 vs 50 + 5 CQs
- `cross-bench-matrix.md` — scores com citacoes textuais (artefato relacionado)
- `final-recommendation-matrix.md` — decisao final por persona (artefato relacionado)

## Fontes

- **Bench 1** — `docs/bench/chatwoot-vs-zendesk/scorecard.md` C2 (Chatwoot 75 vs Zendesk 88)
- **Bench 2 deep dive** — `docs/bench/intercom-vs-chatwoot/deep/ai-capability.md` (Fin Apex 1.0 + RAG 6 steps + deflection 51-67% + Captain opacidade)
- **Bench 3** — `docs/bench/octadesk-vs-zendesk/inventory-octadesk.md` (WOZ Agent ChatGPT-based + claim 80%)
- **Consolidated** — `docs/bench/3-way-final-omnichannel/consolidated-scorecard.md` D2 (Chatwoot 65, Zendesk 87, Intercom 80, Octadesk 70)
- **Triangulation** — `docs/bench/3-way-final-omnichannel/triangulation-analysis.md` INC-01 + CQ-3WAY-001 + CQ-3WAY-002
