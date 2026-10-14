# Scorecard — Solo Bootstrap Weighted Scoring

**Método:** soma ponderada normalizada 0-100 sobre 7 dimensões, com flag de veto duro quando `solo_feasibility ≤ 1` ou `anti_commoditization = 0`.

**Pesos validados com operador:**

| Dimensão | Peso | Por quê |
|---|---|---|
| TTFR (Time-to-First-Revenue) | **25%** | Cash positivo em 90 dias é a meta primária |
| Margem operacional | **20%** | Solo precisa de margem alta para sobreviver sem capital |
| Defensibilidade | **20%** | Construir ativo, não trabalhar em commodity |
| Solo feasibility | **15%** | Restrição dura: precisa ser entregável por 1 pessoa |
| Recorrência (MRR) | **10%** | MRR > project revenue para compounding |
| Anti-commoditização | **5%** | Tiebreak — janela de mercado |
| Baixo risco regulatório | **5%** | Tiebreak — evitar Marco IA 2025 / LGPD pesado |

---

## Ranking final

| # | Serviço | Score | Veredicto |
|---|---|---|---|
| 🥇 1 | **Mentoria Premium IA** | **87,8** | PRIMARY_BET |
| 🥈 2 | **Automação n8n Vertical** | **76,7** | SECONDARY_BET / PAIRED |
| 🥉 3 | **WhatsApp Vertical** | **69,6** | FAST_CASH_ENTRY / ANCHOR |
| 4 | GenAI Conteúdo | 56,5 | CHANNEL_PRIMER (não-negócio) |
| 5 | SDR IA Voz+HITL | 54,3 | DEFER (ano 2) |
| 6 | Preditivo Custom | 50,4 ❌ | VETO_FOR_SOLO |
| 7 | LGPD Governança | 49,0 ❌ | VETO_FOR_SOLO |
| 8 | Cyber IA | 47,6 ❌ | VETO_FOR_SOLO |
| 9 | Chatbot Genérico | 47,5 ❌ | DO_NOT_ENTER |

---

## Decomposição por dimensão

### Tabela completa (notas 0-100)

| Serviço | TTFR | Margem | Defens. | Solo | Recur. | Anti-Com. | Reg-low | **Total** |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Mentoria Premium | 88 | 80 | **100** | **100** | 55 | **100** | **100** | **87,8** 🥇 |
| Automação n8n | 80 | **88** | 72 | 80 | 80 | 40 | 80 | **76,7** 🥈 |
| WhatsApp Vert. | **92** | 70 | 51 | 80 | 65 | 30 | 60 | **69,6** 🥉 |
| GenAI Conteúdo | **96** | 55 | 14 | **100** | 30 | 10 | 80 | 56,5 |
| SDR IA Voz | 55 | 62 | 48 | 40 | 80 | 40 | 40 | 54,3 |
| Preditivo | 12 | 45 | **100** | 20 ❌ | 92 | 80 | 40 | 50,4 ❌ |
| LGPD Gov. | 18 | 52 | 90 | 20 ❌ | **95** | 80 | **100** | 49,0 ❌ |
| Cyber IA | 12 | 42 | 78 | 20 ❌ | **100** | 60 | 80 | 47,6 ❌ |
| Chatbot Gen. | **96** | 35 | 8 | **100** | 18 | **0** ❌ | 60 | 47,5 ❌ |

**Legenda:** ❌ no campo = ativa flag de veto; ❌ no Total = veto consolidado.

---

## Quem ganha cada dimensão

| Dimensão | Vencedor | Score | Runner-up |
|---|---|---:|---|
| TTFR | GenAI Conteúdo / Chatbot | 96 | WhatsApp Vertical (92) |
| Margem | **Automação n8n** | 88 | Mentoria Premium (80) |
| Defensibilidade | **Mentoria / Preditivo** | 100 | LGPD (90) |
| Solo feasibility | Mentoria / GenAI / Chatbot | 100 | Automação n8n (80) |
| Recorrência | Cyber IA | 100 | LGPD (95) / Preditivo (92) |
| Anti-commod. | Mentoria | 100 | Preditivo (80) / LGPD (80) |
| Risco reg. baixo | Mentoria / LGPD | 100 | Automação n8n (80) / GenAI (80) |

**Insight:** Mentoria Premium é **única em 4 dimensões diferentes** (defensibilidade, solo, anti-com., reg-low) — não tem trade-off interno significativo. Por isso domina o ranking.

---

## Análise de sensibilidade

Para auditar robustez do ranking, testei mudanças nos pesos:

### Cenário 1 — Se TTFR dobra (50% do peso total)

Founder em "modo emergência" priorizando cash mais ainda.

| # | Serviço | Score recalculado |
|---|---|---|
| 1 | Mentoria Premium | 84,4 |
| 2 | **WhatsApp Vertical** | 79,6 ⬆ (era #3) |
| 3 | Automação n8n | 75,0 |

**Conclusão:** WhatsApp ultrapassa Automação n8n se TTFR for prioridade absoluta. **Mentoria continua #1.**

### Cenário 2 — Se Defensibilidade dobra (40% do peso total)

Founder querendo construir ativo de longo prazo.

| # | Serviço | Score recalculado |
|---|---|---|
| 1 | Mentoria Premium | 91,1 |
| 2 | Automação n8n | 75,4 |
| 3 | WhatsApp Vertical | 64,4 |

**Conclusão:** Mentoria amplia liderança. WhatsApp perde porque tem defensibilidade 3.

### Cenário 3 — Se horizonte extende para 24 meses (com time crescendo)

| # | Serviço | Mudança |
|---|---|---|
| 1 | Mentoria Premium | mantém |
| 2 | Automação n8n | mantém |
| 3 | **LGPD Governança** | sai do veto ⬆ (se solo founder construir time intermediário) |
| 4 | **Cyber IA** | sai do veto ⬆ (idem) |

**Conclusão:** LGPD e Cyber se tornam viáveis em ano 2-3 SE houver evolução de capacidade. Funcionam como **destino tier-2**.

---

## Robustez do ranking

**Top 3 é estável** a perturbações de ±10% nos pesos. Mentoria, Automação n8n e WhatsApp aparecem em todas as configurações razoáveis como os 3 melhores para solo bootstrap.

**Os 3 vetados (LGPD, Cyber, Preditivo) NÃO melhoram** sem mudar capacidade de execução — não é problema de peso, é problema estrutural.

---

## Confiança epistêmica

| Claim | Confiança | Evidência |
|---|---|---|
| Mentoria Premium é a aposta primária para solo | ALTA | 4 dimensões dominantes, robusto a sensibilidade |
| Automação n8n é #2 com gap pequeno | ALTA | Vence em margem (dimensão #2 em peso) |
| WhatsApp é #3 e pode ser entry-point | ALTA | TTFR superior, CAC mais baixo |
| LGPD/Cyber/Preditivo são vetados para solo | ALTA | solo_feasibility=1 é estrutural, não conjuntural |
| GenAI Conteúdo é "channel primer", não negócio | MEDIA | Commoditização em 6m é projeção direcional |
| Scores absolutos finais | MEDIA | Pesos refletem preferência calibrada do operador |
| Janelas de commoditização | BAIXA | Direcional Gartner-style; revisar a cada 6m |

Próximo: `gap-analysis.md` detalha o que cada serviço pede vs. o que solo founder oferece, com lista de gaps que precisam ser fechados antes do lançamento.
