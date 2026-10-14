# Bench — Serviços de IA Brasil sob Lente Solo Bootstrap (2026)

**Bench ID:** `servicos-ia-brasil-solo-bootstrap-2026`
**Data:** 2026-05-17
**Operador:** @oalanicolas
**Analista:** bench-analyst v3.0
**Pesquisa-fonte:** [`docs/research/2026-05-11-servicos-ia-brasil-aceitacao-pagamento`](../../research/2026-05-11-servicos-ia-brasil-aceitacao-pagamento/)

---

## TL;DR — Veredicto em 1 linha

> Para solo founder querendo vender os primeiros serviços de IA no Brasil em 2026, comece por **Mentoria Premium** (negócio principal), **Automação n8n Vertical** (cross-sell de alta margem) e **WhatsApp Vertical** (cash anchor) — VETANDO Cyber IA, LGPD Governança, Preditivo Custom e SDR Voz+HITL no MVP.

---

## Ranking final

| # | Serviço | Score | Veredicto |
|---|---|---:|---|
| 🥇 | **Mentoria Premium IA** | 87,8 | PRIMARY_BET |
| 🥈 | **Automação n8n Vertical** | 76,7 | SECONDARY_BET |
| 🥉 | **WhatsApp Vertical** | 69,6 | CASH_ANCHOR |
| 4 | GenAI Conteúdo | 56,5 | Funil (não negócio) |
| 5 | SDR IA Voz+HITL | 54,3 | Defer ano 2 |
| 6 | Preditivo Custom | 50,4 ❌ | VETO_SOLO |
| 7 | LGPD Governança | 49,0 ❌ | VETO_SOLO |
| 8 | Cyber IA | 47,6 ❌ | VETO_SOLO |
| 9 | Chatbot Genérico | 47,5 ❌ | DO_NOT_ENTER |

---

## Contexto do bench

| Parâmetro | Valor |
|---|---|
| Tipo de bench | Product comparison (service offering) |
| Universo comparado | 9 serviços de IA Brasil 2026 |
| Lente de decisão | Solo founder · sem time · cash em 90d |
| Pesos | TTFR 25% · Margem 20% · Defensibilidade 20% · Solo 15% · MRR 10% · Anti-com. 5% · Reg-low 5% |
| Confiança global | ALTA no top-3; MEDIA nos vetados |
| Coverage da pesquisa-fonte | 88% |

---

## Artefatos

### Documentos de decisão (ler nesta ordem)

1. **[`battle-card.md`](./battle-card.md)** — Decisão executiva 1-page. Comece aqui.
2. **[`executive-report.md`](./executive-report.md)** — Plano operacional 90 dias com cenários e riscos.
3. **[`scorecard.md`](./scorecard.md)** — Ranking ponderado 0-100 + análise de sensibilidade.
4. **[`comparison-matrix.md`](./comparison-matrix.md)** — Matriz lado-a-lado dos 9 serviços × 16 dimensões.
5. **[`gap-analysis.md`](./gap-analysis.md)** — Gaps por serviço + tempo/custo de fechamento.

### Deep dives (consulta tópica)

6. **[`deep/ttfr-analysis.md`](./deep/ttfr-analysis.md)** — TTFR decomposto passo-a-passo por serviço.
7. **[`deep/unit-economics.md`](./deep/unit-economics.md)** — Margem, CAC, LTV, payback, breakeven solo.
8. **[`deep/defensibility-deep.md`](./deep/defensibility-deep.md)** — 6 dimensões + empilhamento composto.
9. **[`deep/solo-feasibility.md`](./deep/solo-feasibility.md)** — Onde quebra a operação por estágio (S0/S1/S2/S3).

### Machine-readable (input para outros squads)

10. `metadata.json` — schema do bench + audit trail
11. `comparison-matrix.json` — matriz comparativa
12. `scorecard.json` — scoring + sensibilidade
13. `gap-analysis.json` — gaps estruturados

---

## Universo comparado (9 candidatos)

Todos extraídos da pesquisa-fonte. Cobrem todos os 4 ICPs (A: Empresário-Dono, B: PME/Mid, C: Enterprise, D: Solo/Micro).

| ID | Serviço | ICP | Ticket (R$) | Composto pesquisa |
|---|---|---|---|---|
| mentoria-premium | Mentoria/Formação IA | A | 5k-300k | 5,0 |
| automacao-n8n-vertical | Automação n8n+RPA+LLM | B | 5k-80k | 4,7 |
| whatsapp-vertical | Bot WhatsApp vertical | B | 187-5k | 4,3 |
| sdr-ia-voice-hitl | SDR IA Voz+HITL | B | 2k-150k | 4,3 |
| lgpd-governanca | Governança LGPD+IA | C | 50k-2M | 4,3 |
| cyber-ia | Cybersecurity IA | C | 100k-1M | 4,7 |
| preditivo-customizado | Preditivo/DS custom | C | 200k-3M | 4,0 |
| genai-conteudo | GenAI conteúdo SaaS | D | 100-3k | 3,7 |
| chatbot-generico | Chatbot web genérico | D | 100-500 | 2,7 |

---

## Metodologia em 1 página

1. **Tipo:** comparação de produtos/serviços (não codebase). Aplica framework `bench-analyst` v3.0 com dimensões customizadas via `bench-dimension-packs.yaml`.
2. **Lente:** restrição de operador (solo founder) re-pondera dimensões padrão e ativa vetos estruturais.
3. **Pesos:** validados em interação com operador (TTFR 25%, Margem 20%, Defensibilidade 20%, Solo 15%, MRR 10%, Anti-com. 5%, Reg-low 5%).
4. **Vetos duros:** `solo_feasibility ≤ 1` OU `anti_commoditization = 0` → score válido mas verdict = VETO/DO_NOT_ENTER.
5. **Análise de sensibilidade:** testar robustez do top-3 em 3 cenários de re-ponderação.
6. **Cross-reference:** validar conclusões contra `quick-wins.md` da pesquisa-fonte (Stack QW-1, QW-4, QW-6, QW-7).

---

## Como usar este bench

### Se você é o operador (Alan / solo founder BR)

1. Ler `battle-card.md` (5 min)
2. Ler `executive-report.md` (15 min) e marcar a checklist de "próximos passos sugeridos"
3. Acionar `/aiox-pm *epic` com este bench como insumo para criar plano executável de 90d

### Se você é outro squad (PM, Copy, Analyst)

- **PM:** input para epic de 13 semanas → `executive-report.md` § 5
- **Copy Chief:** input para oferta Mentoria → `gap-analysis.md` M-G02 (Hormozi $100M)
- **Analyst:** input para 5-10 entrevistas de validação → `executive-report.md` § 10
- **Roundtable:** input para multi-lens review → `scorecard.md` (mostrar pesos para debate)

### Se você quer customizar o veredicto

- Mudou capacidade (contratou time)? → rodar `*bench-score` com `solo_feasibility` removido
- Mudou horizonte (12 meses+)? → rodar `*bench` com pesos diferentes (defensibilidade↑)
- Mudou ICP-alvo? → rodar `*bench-quick` filtrando por 1 ICP

---

## Diferença vs pesquisa-fonte

A pesquisa-fonte `2026-05-11-servicos-ia-brasil-aceitacao-pagamento` rankeou serviços assumindo **execução irrestrita**. Este bench aplica **lente solo-bootstrap** e revela:

| Serviço | Score-fonte | Score-bench | Mudança | Motivo |
|---|---:|---:|---|---|
| Mentoria Premium | 5,0 (#1) | 87,8 (#1) | ✅ confirma | Solo-friendly + alto LTV |
| Automação n8n | 4,7 (#2) | 76,7 (#2) | ✅ confirma | Margem brutal |
| WhatsApp Vertical | 4,3 (#4) | 69,6 (#3) | ⬆ | TTFR superior na lente solo |
| Cyber IA | 4,7 (#3) | 47,6 (#8) ❌ | ⬇⬇⬇ veto | Solo feasibility 1 |
| LGPD Governança | 4,3 (#5) | 49,0 (#7) ❌ | ⬇⬇⬇ veto | Comitê + ciclo 540d |
| Preditivo Custom | 4,0 (#6) | 50,4 (#6) ❌ | ⬇ veto | PoC zumbi + DS sênior |

---

## Caveats e limites

- **Sem validação primária:** decisão calibrada em pesquisa documental, não entrevistas BR. Validar com 10-15 entrevistas antes de commit total.
- **Confiança por dimensão:**
  - ALTA nas faixas de ticket, ciclo, decisor (triangulado em 15+ fontes)
  - MEDIA nos TTFR, CAC, margem derivados (heurísticas calibradas)
  - BAIXA nas janelas de commoditização (projeção direcional Gartner-style)
- **Janela:** vale para 2026; revisar quando Marco IA 2025 evoluir ou commoditização acelerar
- **Operador único:** scores assumem perfil generalista solo. Founder técnico-puro, advogado, vendedor podem reordenar top-3.

---

## Próximos benches sugeridos

- **`*bench-quick` por vertical:** comparar 2-3 verticais específicos de WhatsApp (clínica vs restaurante vs imob)
- **`*bench-product` por ferramenta:** comparar n8n vs Make vs Zapier para escolha do template de Automação
- **`*bench-llm` para SDR Voz:** comparar Vapi vs Bland.ai vs Retell quando chegar a hora
- **`*bench` revisão 90d:** atualizar este bench com dados reais após execução do Q1

---

## Trilha de auditoria

| Evento | Data | Owner |
|---|---|---|
| Bench criado | 2026-05-17 | bench-analyst v3.0 |
| Pesos calibrados com operador | 2026-05-17 | @oalanicolas (4 perguntas) |
| Pesquisa-fonte consumida | 2026-05-11 | /tech-research |
| Próxima revisão recomendada | 2026-08-17 (após 90d execução) | @oalanicolas |

---

**Próximo comando sugerido:** abrir `battle-card.md` e responder a checklist final ("qual perfil sou?") para escolher onde começar amanhã.
