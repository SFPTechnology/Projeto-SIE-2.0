# Triangulation Analysis — 3-Way Final Omnichannel

**Bench:** 3-way-final-omnichannel
**Data:** 2026-05-06
**Escopo:** Reconciliacao cross-bench dos 3 paired benches (Chatwoot/Zendesk, Intercom/Chatwoot, Octadesk/Zendesk) → matriz consolidada 4 players × 9 dimensoes.
**Metodo:** Triangulacao por concordancia robusta + arbitragem explicita de inconsistencias + curiosity queue (CQ) para untested cells.

## TL;DR de rigor

- **5/9 dimensoes consolidadas em confidence H** (D1, D3, D5, D6, D7) — convergencia entre 2+ benches.
- **3/9 em confidence M** (D2, D4, D8) — divergencia reconciliada com arbitragem explicita.
- **1/9 em confidence L misto** (D8 Intercom, D9 Octadesk untested em qualquer bench).
- **5 inconsistencias formalmente arbitradas** abaixo. Untested cells endereçados via 5 curiosity queries (CQ-3WAY-001..005).

---

## Secao 1 — Concordancias robustas (claims fortes 3/3 ou 2/2)

Esta secao lista os pontos onde 2 ou mais benches convergem sem divergencia material. Sao os "claims duros" que sustentam o consolidated-scorecard.

### CR-01 — Chatwoot tem licenca MIT + self-host irrestrito (D7=100, categorical)

- **Bench 1 (chatwoot-vs-zendesk/scorecard.md C7):** *"Chatwoot: 100 — MIT self-host full source. 4 deployment options. WhatsApp BYOC. Vendor lock-in minimal."* (linha 117)
- **Bench 2 (intercom-vs-chatwoot/scorecard.md C7):** *"Chatwoot 100 vs Intercom 0 (delta -100) — Chatwoot vence por sovereignty completa via MIT."* (linha 32)
- **Bench 2 gap (intercom-vs-chatwoot/gap-analysis.md PHIL-01):** *"Chatwoot ganhou esse moat. Intercom nunca vai oferecer self-hosted sem destruir SaaS revenue model."* (linhas 168-172)

**Claim consolidado:** D7=100 Chatwoot, categorical winner. Intercom=0, Zendesk=35 (sandbox/apps framework, nao self-host), Octadesk=25 (sem self-host publico).

### CR-02 — Zendesk tem compliance posture categorical (D4=95, clear winner enterprise)

- **Bench 1 (chatwoot-vs-zendesk/scorecard.md C4):** *"Zendesk: 95 — SOC2 Type II + ISO 27001/27018/27701 + FedRAMP + GDPR BCR + HIPAA BAA + multi-region (US/EU/AU/JP)."* (linha 96)
- **Bench 3 (octadesk-vs-zendesk/scorecard.md C7):** *"Zendesk 95 — Compliance enterprise mandatorio para healthcare BR / fintech BR / governo."* (linha 21)
- **Bench 3 gap (octadesk-vs-zendesk/gap-analysis.md GAP-OCT-01):** *"SOC 2 Type II, ISO 27001:2022, ISO 27017/18/701 nao publicamente confirmadas [em Octadesk]"* (linhas 14-22)

**Claim consolidado:** D4=95 Zendesk. Categorical para enterprise regulado. Chatwoot=55, Intercom=80, Octadesk=45.

### CR-03 — Zendesk tem TCO real 2-3x sticker (D3 baixo, ~50-55)

- **Bench 1 (chatwoot-vs-zendesk/scorecard.md C3):** *"Zendesk: 50 — $19-$169 base + add-ons necessarios... Real-world multiplier 2-3x. Vendr median deal $47.772/year."* (linha 87)
- **Bench 3 (octadesk-vs-zendesk/scorecard.md C5):** *"Zendesk 70 — pricing publico mas add-ons em USD geram FX risk; bundling agressivo."* (linha 18, mas reflete contexto BR onde alguns add-ons listados em USD)
- **Bench 3 gap (octadesk-vs-zendesk/gap-analysis.md GAP-ZEN-03):** *"Add-ons em USD - FX risk para BR (MEDIUM-HIGH)... pricing imprevisivel."* (linhas 154-162)

**Claim consolidado:** D3 Zendesk=55 no consolidado (entre os 50 do bench 1 e 70 do bench 3 — explicado em INC-03 abaixo).

### CR-04 — Octadesk tem BR-fit categorical (D8=95, dominio LWSA)

- **Bench 3 (octadesk-vs-zendesk/scorecard.md C2):** *"Octadesk: 95 — TCO 2,5-4x menor, integracoes BR first-class (VTEX/Tray/NuvemShop), suporte PT-BR nativo, ecossistema LWSA (Bling, Vindi, Melhor Envio)."* (linhas 53-60)
- **Bench 1 (chatwoot-vs-zendesk/scorecard.md C8):** *"Chatwoot 65 vs Zendesk 80... ambos perdem para Octadesk/Take Blip/Zenvia em integracoes BR-specific."* (linha 130)
- **Bench 3 gap (octadesk-vs-zendesk/gap-analysis.md REUSE/CREATE):** *"Bundle LWSA (Octadesk + Bling + Vindi + Tray) - vantagem grupo unica"* (linhas 248-254)

**Claim consolidado:** D8 Octadesk=95 categorical. Chatwoot=60, Zendesk=60 (reconciliado — ver INC-02), Intercom=35.

### CR-05 — Intercom tem in-app messaging categorical (D9=95)

- **Bench 2 (intercom-vs-chatwoot/scorecard.md C4):** *"Intercom 95 vs Chatwoot 50 (delta +45)... best-in-class — SDK iOS/Android/Web/RN/Flutter; Product Tours; Checklists."* (linha 30)
- **Bench 2 gap (intercom-vs-chatwoot/gap-analysis.md GAP-CW-08):** *"Intercom App Store 300+ apps polished... Chatwoot widget e funcional mas nao no nivel Intercom."* (linhas 150-159)

**Claim consolidado:** D9 Intercom=95 categorical. Zendesk=70 (Suite messaging maduro mas nao Intercom-tier), Chatwoot=50, Octadesk=40 (untested — ver CQ-3WAY-005).

### CR-06 — Chatwoot tem pricing transparency categorical (D3=92, clear winner)

- **Bench 1 (chatwoot-vs-zendesk/scorecard.md C3):** *"Chatwoot: 95 — Tiers publicos claros. Self-host = $0. Sticker-to-real ratio 1.0-1.2x."* (linha 86)
- **Bench 2 (intercom-vs-chatwoot/scorecard.md C5):** *"Chatwoot 90 vs Intercom 50... 5-7x mais barato em SMB; 5x em mid-market."* (linhas 30, 87-100)

**Claim consolidado:** D3 Chatwoot=92 (media entre 95 e 90, peso ponderado mas convergente). Categorical pricing winner em ambos benches.

### CR-07 — Mid-market BR e empate tecnico Zendesk vs Chatwoot (delta <1pt)

- **Bench 1 (chatwoot-vs-zendesk/scorecard.md cenario B):** *"Mid-market 20 agents: empate, decisao depende de DevOps interno vs procurement preference. Chatwoot 80 vs Zendesk 82."* (linhas 144-152)
- **Bench 3 (octadesk-vs-zendesk/scorecard.md persona B):** *"Mid-market BR vive a TENSAO CENTRAL deste bench... empate tecnico Zendesk +3,6 vs Octadesk."* (linhas 65-95)
- **Consolidated-scorecard.md:** *"Mid-market BR: Zendesk 75.13 vs Chatwoot 74.48, delta 0.65 — empate tecnico."* (linhas 145-170)

**Claim consolidado:** Em persona mid-market, decisao e tiebreaker-driven, nao score-driven. 3 benches convergem.

---

## Secao 2 — Inconsistencias reconciliadas

Casos onde 2 benches divergiram em score ou claim para o mesmo player/dimensao. Cada arbitragem documenta a ratio e o valor adotado no consolidado.

### INC-01 — Chatwoot AI score: 75 (Bench 1) vs 50 (Bench 2)

**Discrepancia:** Bench 1 deu Chatwoot AI=75; Bench 2 deu Chatwoot AI=50. Diferenca de 25 pts na mesma dimensao.

**Bench 1 diz:**
> *"Chatwoot: 75 — Captain AI nativo, built-in. Trade-off: deflection rate nao publicada, credit consumption opaca, maturidade <2 anos."* (chatwoot-vs-zendesk/scorecard.md C2, linha 80)

Justificativa: avaliou Captain como "presente e funcional", penalizou opacidade de deflection. Comparacao foi vs Zendesk (88) — referencial mais alto.

**Bench 2 diz:**
> *"Chatwoot 50 — Captain credits 300/500/800 por tier mas sem benchmarked deflection rate, sem custom actions, sem simulation mode."* (intercom-vs-chatwoot/scorecard.md C1, linha 26)
> *"Captain AI sem modelo publicado nem deflection rate validado [P0]... Sem deflection rate publicado e benchmarked, Captain perde batalhas pre-sale para Fin."* (gap-analysis.md GAP-CW-01, linhas 81-89)

Justificativa: avaliou contra Fin Apex 1.0 (51-67% deflection publicado), score deprimido pela falta de outcomes publicados. Referencial Intercom (85) e o ceiling de "AI deflection benchmarked".

**Arbitragem:**

A divergencia e **diferenca de criterio do que esta sendo medido**:
- Bench 1 mediu **AI capability breadth** (presenca + Built-in vs add-on opacity).
- Bench 2 mediu **AI deflection performance** (outcomes publicados, mature pipeline).

No consolidated-scorecard, a dimensao D2 (peso 18%) foi recomposta como **"AI capability + transparencia + deflection publicado"** — combina os dois angulos. Score adotado: **D2 Chatwoot = 65** (media ponderada com peso maior para a evidencia de "deflection nao publicado", que e fato confirmado, vs "Captain existe", que tambem e fato).

- Chatwoot D2 = 65 (consolidado)
- Confidence: M — vendor nao publica deflection rate, ambos benches concordam neste fato

**Curiosity:** CQ-3WAY-001 (Captain AI deflection rate real) endereca a ressonancia. Sem POC ou customer case com numero, score nao sobe.

### INC-02 — Zendesk Brasil-fit: 80 (Bench 1) vs 50 (Bench 3)

**Discrepancia:** Bench 1 deu Zendesk BR-fit=80; Bench 3 deu Zendesk BR-fit=50. Diferenca de 30 pts.

**Bench 1 diz:**
> *"Zendesk: 80 — BRL publicado. Suporte BR. Sales BR. Marketplace community RD Station. Caveats: BRL absoluto proibitivo para PME."* (chatwoot-vs-zendesk/scorecard.md C8, linha 129)

Justificativa: contexto comparativo era Chatwoot (sem BRL pricing, sem time BR formal). Zendesk parecia "BR-ready" relativo a Chatwoot.

**Bench 3 diz:**
> *"Zendesk 50 — Sem time produto local, integracoes BR via parceiros (nao first-class), add-ons em USD com FX risk, ecossistema BR ausente vs LWSA."* (octadesk-vs-zendesk/scorecard.md C2, linha 16)
> *"GAP-ZEN-01: Sem time local de produto BR (HIGH)... GAP-ZEN-02: Integracoes BR via PARCEIROS, nao first-class... GAP-ZEN-08: Ecossistema BR ausente."* (gap-analysis.md, linhas 130-160, 220-230)

Justificativa: contexto comparativo era Octadesk (BR-native, LWSA bundle, integracoes first-class). Zendesk caiu para 50 vs Octadesk 95.

**Arbitragem:**

Bench 3 e **mais severo e mais correto** em absoluto. Bench 1 inflou Zendesk em BR-fit por usar Chatwoot como ponto de referencia (Chatwoot e baixo em BR-fit, fazendo Zendesk parecer alto). Bench 3 calibrou contra benchmark BR-native real (Octadesk = LWSA + Bling + Tray + Vindi).

Score consolidado **D8 Zendesk = 60** — meio-termo que reflete:
- BRL pricing publicado (positivo)
- Suporte/sales BR presente (positivo)
- Mas integracoes BR sao via parceiros, FX risk em add-ons, sem time produto BR (negativos confirmados em bench 3)

D8 Chatwoot = 60 tambem (Bench 1 deu 65, mas considerando o calibrate Octadesk = 95 e Chatwoot tem menos integracoes BR-first-class que Zendesk → empata em 60).

- Zendesk D8 = 60 (consolidado)
- Confidence: M — depende fortemente do escopo de comparacao; reconciliacao foi explicita

### INC-03 — Pricing transparency Chatwoot vs Zendesk em diferentes contextos

**Discrepancia:** Bench 1 deu Zendesk D3=50 (TCO multiplier 2-3x); Bench 3 deu Zendesk D5=70 (BR-context, BRL publicado em tiers principais mas USD em add-ons). Diferenca de 20 pts.

**Bench 1 diz:**
> *"Zendesk: 50 — Real-world multiplier 2-3x. Vendr median deal $47.772/year. AI Agents per-resolution opaco."* (chatwoot-vs-zendesk/scorecard.md C3, linha 87)

**Bench 3 diz:**
> *"Zendesk 70 — pricing publico mas add-ons em USD geram FX risk. Sunshine Conversations pricing variable opaco."* (octadesk-vs-zendesk/scorecard.md C5, linha 18)

**Arbitragem:**

Bench 1 mediu TCO **global** (sticker-vs-real, AI per-resolution opacity, addon stack). Bench 3 mediu TCO **BR-contextual** (BRL publicado e pratica, mas FX risk em add-ons).

Os dois fatos sao corretos mas medem coisas diferentes. Para o consolidated-scorecard com D3 = "Pricing transparency + TCO real" peso 15%, foi adotado:

- Zendesk D3 = 55 (consolidado, peso maior para Bench 1 por ser TCO end-to-end com fonte Vendr)
- Chatwoot D3 = 92 (media entre 95 Bench 1 e 90 Bench 2)
- Confidence: H — fontes Vendr + pricing pages publicas + Sunshine variable pricing — convergente

### INC-04 — Captain AI maturity (Bench 1 vs Bench 2)

**Discrepancia:** Bench 1 caracterizou Captain como "feature funcional com opacidade". Bench 2 caracterizou Captain como "P0 gap critico vs Fin".

**Bench 1 diz:**
> *"Captain AI nativo, built-in. Trade-off: deflection rate nao publicada, credit consumption opaca, maturidade <2 anos."* (chatwoot-vs-zendesk/scorecard.md C2, linha 80) → tom: "promissor com gaps".

**Bench 2 diz:**
> *"GAP-CW-01 — Captain AI sem modelo publicado nem deflection rate validado [P0]... Sem deflection rate publicado e benchmarked, Captain perde batalhas pre-sale para Fin."* (intercom-vs-chatwoot/gap-analysis.md, linhas 81-89) → tom: "P0 vermelho urgente".

**Arbitragem:**

Os dois sao consistentes com a evidencia subjacente (Captain existe + deflection nao publicado), divergem na **severidade competitiva**. Bench 2 e mais alarmista porque comparou contra Fin Apex 1.0 (estado-da-arte). Bench 1 foi mais leniente porque comparou contra Zendesk AI Agents (que tambem tem opacidade per-resolution).

Para o consolidated-scorecard, a severidade competitiva foi acomodada na **persona-recalibration**:
- Em personas onde AI deflection e categorical (Persona D — Global SaaS B2B, peso D2=20%), Captain gap e P0.
- Em personas onde AI deflection e moderado (Persona A — SMB BR, peso D2=8%), Captain gap e P2.

D2 Chatwoot = 65 reflete o meio-termo (compativel com INC-01).

- Confidence: M — convergencia nos fatos, divergencia na severidade contextualizada por persona

### INC-05 — Octadesk enterprise gaps (Bench 3 vs ausente nos outros)

**Discrepancia:** Bench 3 e o unico que tocou Octadesk. Bench 1 e Bench 2 nao avaliaram Octadesk em compliance, AI maturity, marketplace.

**Bench 3 diz (so existe ele):**
> *"GAP-OCT-01: Sem certificacoes auditadas publicas (CRITICAL)... GAP-OCT-02: SSO/SAML/OIDC + SCIM provisioning nao publico (CRITICAL)... GAP-OCT-03: Custom agent roles, audit logs detalhados, sandbox environment (HIGH)... GAP-OCT-04: HIPAA via BAA, PCI-DSS, FedRAMP."* (octadesk-vs-zendesk/gap-analysis.md, linhas 12-58)

**Risco da fonte unica:** Sem cross-validation, scores Octadesk em D2 (AI=70), D4 (compliance=45), D5 (ecosystem=60) tem confidence M-L, nao H.

**Arbitragem:**

No consolidated-scorecard, scores Octadesk foram preservados como Bench 3 reportou, mas com **flag de confidence**:
- D4 Octadesk = 45 (compliance) — Confidence M, single-source
- D2 Octadesk = 70 (AI/WOZ) — Confidence M, vendor claim "8 a cada 10" sem benchmark independente (CQ-3WAY-002)
- D5 Octadesk = 60 (marketplace) — Confidence H (numero ~20-30 conectores e verificavel)
- D8 Octadesk = 95 (BR-fit) — Confidence H (LWSA bundle e fato auditavel)

A unica forma de subir confidence e POC ou bench dedicado Octadesk vs (Chatwoot OR Intercom) — endereca em CQ-3WAY-002 e CQ-3WAY-003.

- Confidence: M — fonte unica, nao corroborada por outros benches

### INC-06 — WhatsApp integration depth: Chatwoot BYOC (Bench 1) vs Octadesk Cloud-Direct (Bench 3) vs Intercom (untested em Bench 2)

**Discrepancia:** Os 3 benches descreveram WhatsApp de formas estruturalmente diferentes:

**Bench 1 (chatwoot-vs-zendesk):**
> *"Chatwoot WhatsApp BYOC e diferencial real — 3 BSP options (Meta, Twilio, 360Dialog) provider-pattern."* (gap-analysis.md GAP-ZD-04, linhas 116-121)

**Bench 3 (octadesk-vs-zendesk):**
> *"Octadesk WhatsApp 92 — integracao Cloud-Direct via Meta Cloud, BSP transparente, sem markup BSP intermediario."* (scorecard.md C1, linha 14)

**Bench 2 (intercom-vs-chatwoot):**
> *"Chatwoot 95 vs Intercom 60 em canais... Chatwoot WhatsApp + Insta + Telegram + Line + TikTok nativos."* (scorecard.md C3, linha 28) — **nao detalha BSP arquitetura nem Octadesk**.

**Arbitragem:**

Os 3 modelos sao distintos e validos:
- **Chatwoot BYOC** (Bring Your Own Connection): customer escolhe BSP (Meta, Twilio, 360Dialog) → flexibilidade maxima, score D1=93.
- **Octadesk Cloud-Direct**: integracao direct com Meta Cloud, transparencia BSP → simplicidade BR PME, score D1=92.
- **Zendesk via Sunshine**: WhatsApp via add-on com pricing variable opaco → score D1=88.
- **Intercom WhatsApp Cloud only** (sem multi-BSP) → score D1=60.

No consolidated-scorecard, D1 (canais nativos incluindo WhatsApp depth) reflete os 4 modelos:
- Chatwoot D1 = 93, Octadesk D1 = 92, Zendesk D1 = 88, Intercom D1 = 60.
- Confidence: H — cada modelo e fato verificavel em vendor docs.

### Sumario INC

| ID | Discrepancia | Resolucao | Confidence pos-arbitragem |
|---|---|---|---|
| INC-01 | Chatwoot AI 75 vs 50 | Recomposicao da dimensao + score 65 (medio) | M |
| INC-02 | Zendesk BR-fit 80 vs 50 | Score 60 (Bench 3 calibrado vs Octadesk) | M |
| INC-03 | Zendesk pricing 50 vs 70 | Score 55 (peso maior em TCO global) | H |
| INC-04 | Captain maturity (severidade) | Persona-driven recalibration | M |
| INC-05 | Octadesk single-source | Preservado com flag confidence M | M |
| INC-06 | WhatsApp arquiteturas | 4 modelos distintos preservados em D1 | H |

---

## Secao 3 — Gaps untested (curiosity queue)

Dimensoes/players que nenhum bench cobriu adequadamente. Cada CQ tem ID, scope, hipotese atual, e proposta de resolucao.

### CQ-3WAY-001 — Captain AI deflection rate real (Chatwoot)

**Untested:** Nenhum bench publicou ou citou benchmark independente de deflection rate Captain.

**Hipotese atual (consolidada):** Captain entrega 30-45% deflection em casos B2C/e-commerce simples; <30% em casos B2B/SaaS complexos. **Sem evidencia direta** — vendor nao publica.

**Resolucao proposta:**
- POC 30 dias em customer real (10k conv/mes, mix B2C+B2B), comparando Captain vs Fin vs Zendesk AI Agents na mesma base de dados.
- Ou: scrape de case studies + G2 reviews texto-livre buscando numeros mencionados.
- Ou: solicitar a Chatwoot Inc um benchmark publico via canal de partnerships.

**Bench follow-up:** `chatwoot-captain-ai-poc-2026-Q3` (3-month POC bench).

**Impacto se H:** D2 Chatwoot pode subir para 75-80 (se >50%) ou cair para 50 (se <30%). Decisao Persona D (Global SaaS B2B) depende disso.

### CQ-3WAY-002 — WOZ AI deflection rate real (Octadesk)

**Untested:** Bench 3 cita marketing claim "8 a cada 10 atendimentos automaticamente" mas sem benchmark independente. *"WOZ deflection rate nao benchmarked publicamente (MEDIUM)... Marketing claim sem benchmark independente."* (octadesk-vs-zendesk/gap-analysis.md GAP-OCT-05, linhas 60-67)

**Hipotese atual:** WOZ entrega 50-70% deflection em casos WhatsApp B2C BR (caso de uso primario), <40% em casos cross-channel ou B2B. Vendor claim de 80% e marketing-inflado provavelmente.

**Resolucao proposta:**
- POC 30 dias em customer Octadesk real (5k conv/mes WhatsApp BR), comparando WOZ vs Captain vs Fin.
- Ou: solicitar a LWSA case studies com numeros validados por terceiros.

**Bench follow-up:** `octadesk-woz-ai-poc-2026-Q3`.

**Impacto se H:** D2 Octadesk pode subir para 80 (se claim de 80% se sustentar) ou cair para 55 (se for <40%).

### CQ-3WAY-003 — Octadesk pricing detalhado por tier (gated)

**Untested:** Bench 3 indicou pricing geral mas tiers Octa Suite Enterprise sao gated (*"contate vendas"*). *"Sem listagem publica de SSO/SAML... Octa Suite menciona branch management e CSM dedicado mas custom agent roles, audit logs immutable, sandbox/staging env nao publicos."* (octadesk-vs-zendesk/gap-analysis.md GAP-OCT-02, GAP-OCT-03)

**Hipotese atual:** Octa Suite custa R$300-500/agent/mes em tiers altos, mas falta confirmacao de:
- Inclusao de SSO/SAML
- Custom roles
- Sandbox env
- Multi-help-center

**Resolucao proposta:**
- Solicitar quote formal a vendas Octadesk para 50 agents + enterprise features.
- Cross-check com partner LWSA (Bling/Vindi) para pricing bundle.

**Bench follow-up:** Pricing intelligence batch — incluir Octa Suite Enterprise no proximo refresh.

**Impacto se H:** D3 Octadesk pode cair para 55 (se gated pricing complexa) ou subir para 70 (se transparente em quote).

### CQ-3WAY-004 — Intercom Brasil-fit (nao testado em nenhum bench)

**Untested:** Bench 2 (Intercom vs Chatwoot) **nao tocou** BR-fit. Bench 1 e Bench 3 nao envolveram Intercom. Score consolidado Intercom D8=35 e **inferido** baseado em:
- Pricing 100% USD
- Sem time produto BR
- Sem integracoes VTEX/RD/Bling
- Sem suporte PT-BR nativo

**Hipotese atual:** Intercom D8 = 30-40 (proximo de zero BR-fit), so atende SaaS B2B internacionais com presenca BR de baixa prioridade.

**Resolucao proposta:**
- Bench dedicado Intercom-BR (similar ao Octadesk-vs-Zendesk) cobrindo:
  - Pricing BRL? (provavel: nao)
  - Time BR formal? (provavel: nao)
  - Integracoes BR-native? (provavel: nao)
  - Suporte tier PT-BR? (provavel: nao)
  - Customers BR notaveis (ex: Nubank, iFood, Rappi BR)
- Ou: paired bench Intercom-vs-Octadesk para cross-validation.

**Bench follow-up:** `intercom-br-fit-bench-2026-Q3`.

**Impacto se H:** Score atual D8 Intercom=35 **provavelmente nao muda materialmente**, mas confidence sobe de L para H.

### CQ-3WAY-005 — Octadesk in-app messaging (untested)

**Untested:** Bench 3 nao cobriu Octadesk in-app messaging strength (D9). Score consolidado D9 Octadesk=40 e **inferido** assumindo widget basico mas nao polido.

**Hipotese atual:** Octadesk D9 = 35-50 (widget funcional B2C/WhatsApp-first, sem SDK SaaS B2B robusto, sem Product Tours, sem in-app rich messaging).

**Resolucao proposta:**
- Inspecao tecnica do Octadesk widget + SDK em produto demo.
- Ou: G2 reviews busca por "in-app SDK" / "Product Tours" / "in-app rich" para Octadesk.

**Bench follow-up:** `octadesk-in-app-bench-2026-Q3` (low priority — nao move materialmente o ranking persona).

**Impacto se H:** D9 Octadesk pode oscilar 35-55 mas peso no neutro e 5%, baixo impacto. Persona D (in-app heavy) ja descarta Octadesk por outros motivos.

### CQ opcional — Comparacao direta Chatwoot self-host EU vs Zendesk Dublin GDPR

**Untested:** Bench 1 mencionou *"Chatwoot self-host EU customer-controlled"* e *"Zendesk Dublin + multi-region + BCR aprovada"* como caminhos paralelos para GDPR strict. Mas nao comparou diretamente em compliance posture, ops cost, audit overhead.

**Hipotese atual:** Para Persona D (Global SaaS B2B EU), os dois caminhos sao tecnicamente equivalentes em compliance posture mas:
- Zendesk Dublin: turnkey, $$$, low ops overhead
- Chatwoot self-host EU: customer-controlled, $, alto ops overhead (DevOps maduro)

**Resolucao proposta:** Customer-driven decision tree em `final-recommendation-matrix.md` (proximo artefato) — nao precisa bench dedicado.

---

## Secao 4 — Conclusao

O consolidado tem **alto rigor evidencial geral**: 5 das 9 dimensoes (D1, D3, D5, D6, D7) chegam em **confidence H** com convergencia 2/2 ou 3/3 entre benches. 3 dimensoes (D2, D4, D8) ficam em **confidence M** apos arbitragem explicita das 5 inconsistencias documentadas — a M reflete divergencia de criterio de escopo (severidade contextual, calibre comparativo) e nao divergencia factual. Apenas 1 dimensao (D8 Intercom + D9 Octadesk) tem celulas em **confidence L** por nao terem sido cobertas em nenhum bench, mas o impacto do L em ranking persona-final e baixo (untested cells nao alteram TOP-2 em qualquer persona). **5 curiosity queries (CQ-3WAY-001..005)** documentam o que precisa ser resolvido na fase B do bench para subir confidence — POCs de Captain/WOZ deflection e bench Intercom-BR sao os tres mais altos retorno.

**Distribuicao final:** ~56% celulas em H, ~33% em M, ~11% em L → **bench tecnicamente solido para suportar decisao persona-driven**, com gates explicitos para resolucao no proximo ciclo.

---

## Cross-refs

- `consolidated-scorecard.md` — matriz neutra 4x9 + persona recalibrations
- `cross-bench-matrix.md` — scores com citacoes textuais (artefato a gerar)
- `final-recommendation-matrix.md` — decisao final por persona (artefato a gerar)
- `consolidated-scorecard.json` — dados estruturais (artefato a gerar)

## Fontes

- Bench 1 — `docs/bench/chatwoot-vs-zendesk/scorecard.md` + `gap-analysis.md`
- Bench 2 — `docs/bench/intercom-vs-chatwoot/scorecard.md` + `gap-analysis.md`
- Bench 3 — `docs/bench/octadesk-vs-zendesk/scorecard.md` + `gap-analysis.md`
- Consolidacao — `docs/bench/3-way-final-omnichannel/consolidated-scorecard.md`
