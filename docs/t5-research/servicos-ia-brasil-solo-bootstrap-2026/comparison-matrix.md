# Comparison Matrix — 9 Serviços de IA sob Lente Solo-Bootstrap (BR 2026)

**Bench ID:** servicos-ia-brasil-solo-bootstrap-2026
**Lente de decisão:** solo founder, sem time, objetivo cash positivo em 90 dias
**Fonte primária:** `docs/research/2026-05-11-servicos-ia-brasil-aceitacao-pagamento/`
**Confiança:** ALTA nos rankings ordinais — MEDIA nos TTFR e CAC absolutos (heurísticas derivadas)

---

## Como ler esta matriz

Cada coluna é um serviço. Cada linha é uma dimensão de decisão. Valores entre colchetes representam intervalos `[mín, máx]`. Setas indicam direção do "bom":

- ⬆ higher is better
- ⬇ lower is better
- 🟰 contextual

---

## Matriz 1 — Comercial (ticket × ciclo × CAC × LTV)

| Dimensão | ⬆⬇ | Mentoria Premium | Automação n8n | WhatsApp Vert. | SDR IA Voz | LGPD Gov. | Cyber IA | Preditivo | GenAI Cont. | Chatbot Gen. |
|---|---|---|---|---|---|---|---|---|---|---|
| **Ticket entrada (R$)** | ⬆ | **5k–300k** | 5k–80k | 1k–5k | 2k–30k | 50k–200k | **100k–1M** | **200k–3M** | 100–3k | 100–500 |
| **Recorrência (R$/mês)** | ⬆ | 0–5k | 2k–15k | 500–5k | 2k–15k | 15k–50k | 30k–100k | 20k–80k | 100–1,5k | 100–500 |
| **Ciclo de venda (dias)** | ⬇ | **7–45** | 30–90 | **7–30** | 30–90 | 180–540 | 180–540 | 180–540 | **0–14** | **0–14** |
| **CAC plausível solo (R$)** | ⬇ | 5–30k | 2–10k | **0,5–3k** | 3–15k | 20–150k | 20–100k | 30–200k | **0,05–0,5k** | **0,05–0,5k** |
| **LTV ano 1 (R$)** | ⬆ | 25–300k | 30–150k | 12–50k | 25–180k | 200k–2M | 300k–2M | **500k–3M** | 0,5–3k | 0,3–2k |
| **LTV:CAC alvo** | ⬆ | **5–10:1** | **5–10:1** | 4–8:1 | 4–8:1 | 3–6:1 | 4–6:1 | 3–5:1 | 3–5:1 | 2–3:1 |
| **Decisor** | 🟰 | Pessoa (empresário) | Sócio/COO+CFO | Dono local | Head Vendas | Comitê 4-5 pess. | CISO+exec | C-Level+comitê | Self-serve | Self-serve |

**Leitura comercial:**
- **Mentoria Premium** vence em LTV:CAC e ciclo curto com ticket alto — empresário-dono decide sozinho.
- **WhatsApp Vertical** vence em CAC baixo e ciclo curto — mas ticket menor.
- **Cyber/Preditivo/LGPD** têm ticket gigante mas ciclo 6-18 meses + comitê = inviável solo no MVP.

---

## Matriz 2 — Entrega operacional

| Dimensão | ⬆⬇ | Mentoria Premium | Automação n8n | WhatsApp Vert. | SDR IA Voz | LGPD Gov. | Cyber IA | Preditivo | GenAI Cont. | Chatbot Gen. |
|---|---|---|---|---|---|---|---|---|---|---|
| **TTFR solo (dias)** | ⬇ | **7–45** | 14–45 | **3–21** | 21–90 | 90–270 | 120–365 | 120–365 | **1–14** | **1–14** |
| **Complexidade técnica (1-5)** | ⬇ | **2** | 3 | **2** | 4 | 5 | 5 | 5 | **1** | **1** |
| **Equipe mínima** | ⬇ | **1** | **1** | **1** | 2 | 3 | 4 | 3 | **1** | **1** |
| **Solo feasibility (1-5)** | ⬆ | **5** | 4 | 4 | 2 | **1** ❌ | **1** ❌ | **1** ❌ | **5** | **5** |
| **Discovery obrigatório?** | ⬇ | Não | Sim | Não | Sim | Sim | Sim | Sim | Não | Não |
| **Margem operacional (%)** | ⬆ | **70–90** | **80–95** | 60–80 | 50–75 | 40–65 | 30–55 | 30–60 | 40–70 | 20–50 |

**Leitura operacional:**
- Os 3 candidatos enterprise (LGPD/Cyber/Preditivo) têm **solo_feasibility = 1**: literalmente não dá para entregar sozinho. Veto duro pela lente solo-bootstrap.
- **Automação n8n** lidera margem (80-95%) com solo-feasibility 4 — sweet spot técnico.
- **Mentoria Premium** lidera solo-feasibility (5) — produto é o próprio operador.

---

## Matriz 3 — Defensibilidade e risco

| Dimensão | ⬆⬇ | Mentoria Premium | Automação n8n | WhatsApp Vert. | SDR IA Voz | LGPD Gov. | Cyber IA | Preditivo | GenAI Cont. | Chatbot Gen. |
|---|---|---|---|---|---|---|---|---|---|---|
| **Defensibilidade 5y (1-5)** | ⬆ | **5** | 4 | 3 | 3 | **5** | 4 | **5** | 1 | 1 |
| **Meses até commoditização** | ⬆ | **60** | 24 | 18 | 24 | 48 | 36 | 48 | **6** ❌ | **3** ❌ |
| **Risco regulatório (1-5)** | ⬇ | **1** | 2 | 3 | **4** | **1** | 2 | **4** | 2 | 3 |
| **Anti-commoditization moat** | 🟰 | Reputação+rede | Templates+vertical | Vertical+integração | Voz+verticalização | Compliance+setor | Setor+ferramenta | Vertical+dado | Quase nulo | Nulo |

**Leitura defensibilidade:**
- **Mentoria Premium** é o único com defensibilidade 5 + risco regulatório 1 + commoditização 60 meses → tripla coroa.
- **Automação n8n** tem defensibilidade decente (4) mas commoditização em 24 meses — janela.
- **GenAI Conteúdo** e **Chatbot Genérico** comoditizam em 3-6 meses — não construir negócio aqui.

---

## Matriz 4 — Match dos 9 contra os 7 Quick Wins da pesquisa

Cross-reference entre os 9 candidatos do bench e os 7 quick-wins do `quick-wins.md`.

| Serviço | QW-1 Discovery pago | QW-2 Reclassificar base | QW-3 Anti-LGPD LP | QW-4 Templates n8n | QW-5 AI Audit 7d | QW-6 Mini-curso 7d | QW-7 Reposicionar vertical |
|---|---|---|---|---|---|---|---|
| Mentoria Premium | ✓ gateway | ✓ qualifica | — | — | — | ✓✓ funil direto | ✓ |
| Automação n8n | ✓✓ ideal | ✓ | — | ✓✓ ideal | ✓ | — | ✓ |
| WhatsApp Vert. | ✓ | ✓ | — | — | — | — | ✓✓ ideal |
| SDR IA Voz | ✓ | ✓ | — | — | ✓ | — | ✓ |
| LGPD Gov. | ✓ | — | ✓✓ ideal | — | ✓ | — | — |
| Cyber IA | ✓ | — | ✓ | — | ✓ | — | — |
| Preditivo | ✓✓ ideal | — | — | — | ✓✓ ideal | — | — |
| GenAI Cont. | — | — | — | — | — | — | — |
| Chatbot Gen. | — | — | — | — | — | — | — |

Vencedores em síntese-quick-win:
- **Automação n8n** combina com QW-1 + QW-4 (oferta+produto) → fluxo completo em ≤14 dias
- **Mentoria Premium** combina com QW-6 (funil de captura) → mini-curso vira porta para premium
- **WhatsApp Vertical** combina com QW-7 (reposicionamento) → mesma entrega, 2-3x ticket

---

## Veto duro (sob lente solo-bootstrap)

Três serviços recebem **veto** mesmo com score-fonte alto:

| Serviço | Veto razão | Score-fonte | Veredicto solo |
|---|---|---|---|
| **LGPD Governança** | Comitê de 4-5 decisores, ciclo 180-540 dias, exige advogado + DPO + arquiteto | 4,3 | ❌ NÃO COMEÇAR AQUI |
| **Cyber IA** | Compete com IBM/MS/Big-4, exige SOC 24/7 e seguro cyber | 4,7 | ❌ NÃO COMEÇAR AQUI |
| **Preditivo Customizado** | 40% projetos cancelados (Gartner), exige cientista de dados sênior + eng dados | 4,0 | ❌ NÃO COMEÇAR AQUI |

Esses serviços continuam atrativos como **destino-tier-2** (ano 2-3), depois que o solo founder construir time e reputação com Tier-1.

---

## Diferencial face à matriz original da pesquisa

A matriz composta `02-research-report.md § 2` e a matriz 7 `05-comparative-matrix.md` rankearam os serviços **assumindo execução irrestrita** (time disponível, capital, paciência). Esta matriz aplica a **lente solo-bootstrap** e revela:

- Cyber IA cai de #3 (composto 4,7) para **veto** (solo_feasibility 1).
- LGPD cai de #5 para **veto** (comitê + ciclo 12-18m).
- Preditivo cai de #6 para **veto** (PoC 3-36 meses).
- WhatsApp Vertical **sobe** porque tem TTFR 3-21 dias e CAC sub-R$3k.
- Mentoria Premium **continua #1** — defensibilidade + TTFR + solo-fit alinham.
- Automação n8n **mantém #2** mas com gap menor para WhatsApp.

A próxima view (`scorecard.md`) aplica pesos quantitativos para fechar o ranking.

---

## Caveats epistêmicos (ALTA / MEDIA / BAIXA)

- **ALTA:** Faixas de ticket, ciclo de venda macro, decisor — todos triangulados com 15+ fontes na pesquisa-fonte.
- **MEDIA:** TTFR solo, CAC plausível solo, margem operacional — derivados de benchmark global ajustados por constraint solo.
- **BAIXA:** Janela de commoditização em 24/48/60 meses — projeção direcional Gartner-style, ajustar a cada 6 meses.

Faltam: entrevistas primárias com decisores BR; validação live de oferta; medições reais de TTFR em ambiente próprio.
