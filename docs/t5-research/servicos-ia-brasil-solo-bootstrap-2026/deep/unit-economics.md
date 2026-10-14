# Deep Dive — Unit Economics para Solo Founder

**Princípio:** Solo founder não tem CFO. Unit economics aqui são simplificados: receita por cliente, custo direto, margem, payback, CAC plausível.

---

## Glossário

| Métrica | Definição |
|---|---|
| **Ticket de entrada** | Receita do 1° pagamento (setup, mensalidade, projeto) |
| **MRR/cliente** | Receita recorrente mensal por cliente após estabilização |
| **Custo direto/cliente** | Tooling + tempo do founder × custo-hora |
| **Margem operacional** | (Receita - Custo direto) / Receita |
| **CAC plausível solo** | Custo médio para fechar 1 cliente (anúncios + tempo de outbound) |
| **LTV ano 1** | Receita acumulada do cliente em 12 meses |
| **Payback** | Meses até CAC ser recuperado |
| **Breakeven cliente** | Quantos clientes para zerar custos fixos do operador (R$ 15-30k/mês de pró-labore) |

**Custo-hora do founder solo (assumido):** R$ 200-400/h (custo de oportunidade)
**Custo fixo mensal solo (assumido):** R$ 15-30k (pró-labore + ferramentas + marketing)

---

## Top 3 candidatos detalhados

### 1. Mentoria Premium IA

```
Tier         Ticket   Recur.   Custo direto   Margem   Tempo
Entry        R$ 5k    R$ 0     R$ 1-2k        70-80%   8h/aluno/mês
Mid          R$ 30k   R$ 0     R$ 4-6k        80%      15h/aluno/3m
Premium      R$ 100k  R$ 0     R$ 12-18k      82%      30h/aluno/6m
1:1 VIP      R$ 300k  R$ 0     R$ 30-50k      83%      100h/aluno/12m
```

**CAC plausível solo:**
- Entry: R$ 500-2k via LinkedIn orgânico + mini-curso 7d
- Mid: R$ 2-8k via webinar + retargeting
- Premium: R$ 10-30k via evento presencial + indicação

**LTV ano 1 médio:** R$ 25-80k (mistura entry+mid)

**Payback:** 1-3 meses (vista que ticket é cobrança upfront, payback é instantâneo)

**Breakeven clientes/mês:**
- Para R$ 15k/mês custo fixo: 1 mid OU 3 entry
- Para R$ 30k/mês custo fixo: 1 mid+1 entry OU 6 entry

**Veredicto unit economics:** **Excelente.** Margem 80%, payback instantâneo, ticket grande. Solo founder com 3-5 alunos mid já cobre custos.

---

### 2. Automação n8n Vertical

```
Tipo                       Setup      Recur.       Custo dir.   Margem  Tempo
Discovery pago             R$ 5k      R$ 0         R$ 200       96%     8h
Bot RPA simples            R$ 5-10k   R$ 1-2k      R$ 80/mês    85-90%  20h setup
Workflow completo n8n+LLM  R$ 15-30k  R$ 2-5k      R$ 100/mês   85-95%  40-80h setup
Workflow enterprise        R$ 50-80k  R$ 5-15k     R$ 200/mês   80-95%  80-160h setup
```

**Custo direto típico:**
- Hetzner + Coolify + n8n container: ~R$ 80/mês
- LLM API (GPT-4o/Claude Sonnet): R$ 100-500/mês por cliente
- Sem custo de pessoal extra (solo)

**CAC plausível solo:**
- Discovery via outbound LinkedIn: R$ 1-3k (tempo + ads)
- Projeto via discovery convertido: ~R$ 5k já recuperado no próprio discovery
- Projeto via indicação: R$ 0-500

**LTV ano 1:**
- Cliente médio: R$ 25k setup + R$ 3k × 9 meses (retenção) = R$ 52k

**Payback:** 1-3 meses (setup paga CAC imediatamente)

**Breakeven clientes/mês:**
- Para R$ 15k/mês custo fixo: 5 clientes em retainer R$ 3k OU 1 projeto novo/mês
- Para R$ 30k/mês custo fixo: 10 clientes em retainer OU 2 projetos novos/mês

**Veredicto:** **Excelente.** Margem mais alta do bench. Cap é tempo do solo founder (40-160h/projeto), não receita.

---

### 3. WhatsApp Vertical

```
Tier            Setup       Recur.     Custo dir.    Margem    Tempo
Self-service    R$ 500      R$ 187     R$ 50         60-70%    4h setup
Mid             R$ 1-3k     R$ 800-3k  R$ 80-150     65-80%    10h setup
Enterprise      R$ 5-15k    R$ 3-10k   R$ 200-500    70-85%    30h setup
```

**Custo direto típico:**
- WhatsApp Business API via BSP: R$ 50-200/mês (mensageria) + R$ 0,05-0,15 por conversa
- LLM API: R$ 50-200/mês por cliente
- Hetzner: R$ 80/mês compartilhado entre N clientes

**CAC plausível solo:**
- Outbound local (físico/Google Maps): R$ 300-1.500
- Indicação: R$ 0
- Anúncios geo-targeted: R$ 500-2k

**LTV ano 1:**
- Cliente self-service: R$ 500 + R$ 187 × 11 = R$ 2.557 (mas churn alto)
- Cliente mid: R$ 2k + R$ 1.500 × 11 = R$ 18.500
- Cliente enterprise: R$ 8k + R$ 6k × 11 = R$ 74.000

**Payback:** 2-5 meses

**Breakeven clientes/mês:**
- Para R$ 15k/mês custo fixo: 10 clientes mid OU 3 clientes enterprise
- Para R$ 30k/mês custo fixo: 20 clientes mid OU 6 enterprise

**Veredicto:** **Bom para volume.** Margem menor que automação mas escalável por templatização. Risco de churn em entry.

---

## Comparação consolidada — quanto rende cada serviço para um solo founder

Cenário: 90 dias de operação, 1 founder dedicado 30h/semana.

| Serviço | # clientes plausíveis 90d | Receita 90d | MRR ao fim de 90d | Margem média |
|---|---|---|---|---|
| Mentoria Premium | 2-5 entry + 1-2 mid | R$ 30-90k | R$ 0-3k (se cohort) | 80% |
| Automação n8n | 1-3 projetos + retainer | R$ 20-90k | R$ 3-15k | 88% |
| WhatsApp Vertical | 3-10 clientes | R$ 10-40k | R$ 3-15k | 70% |
| SDR IA Voz | 0-1 prova → conversão tardia | R$ 5-20k | R$ 0-5k | 62% |
| LGPD/Cyber/Preditivo | 0 (ciclo longo) | R$ 0 | R$ 0 | — |
| GenAI Conteúdo | 5-30 self-serve | R$ 1-15k | R$ 0,5-5k | 55% |
| Chatbot Genérico | 3-10 (alto churn) | R$ 1-5k | R$ 0,3-2,5k | 35% |

---

## Capacidade vs receita — quantos clientes solo founder consegue manter?

Premissa: 40h/semana = 160h/mês útil. Reserva 60h para vendas/marketing → 100h para entrega.

| Serviço | Horas/cliente/mês | Cap solo (100h) | Receita cap solo |
|---|---|---|---|
| Mentoria Premium | 8-15h (mid) | 6-12 alunos mid | R$ 30-90k/mês (alunos antigos amortizados) |
| Automação n8n retainer | 5-10h | 10-20 retainers | R$ 20-100k MRR + projetos |
| WhatsApp Vertical | 1-3h | 30-100 clientes | R$ 15-150k MRR |
| SDR IA Voz HITL | 20-40h | 2-5 clientes | R$ 10-40k MRR (limitado) |

**Insight crítico:** **WhatsApp Vertical tem maior cap teórico** mas exige templatização extrema; **Mentoria Premium tem maior receita por hora do founder**; **Automação n8n é o melhor equilíbrio receita-cap-margem**.

---

## Sensibilidade — e se solo virar dupla?

Se solo founder contrata 1 implementador júnior (R$ 5-8k/mês CLT-equivalente):

| Serviço | Antes (solo) | Depois (+1 implementador) | Multiplicador |
|---|---|---|---|
| Mentoria Premium | 6-12 alunos | 12-25 alunos | 2x |
| Automação n8n | 10-20 retainers | 20-40 retainers | 2x |
| WhatsApp Vertical | 30-100 clientes | 60-200 clientes | 2x |
| SDR IA Voz | 2-5 clientes | 5-12 clientes | 2.5x (HITL escalável) |

**Conclusão:** SDR IA Voz tem maior multiplicador com contratação. Justifica defer para ano 2 quando solo founder pode investir em time.

---

## Confiança epistêmica

- Margens (70-95%) para Mentoria/Automação: **ALTA** — alinhada com benchmarks pesquisa-fonte (margem 80-95% documentada para n8n)
- LTV ano 1: **MEDIA** — derivado de payback × retenção esperada
- Capacidade horas/cliente: **MEDIA** — assume templatização e operador eficiente
- Multiplicador com contratação: **BAIXA** — assume contratação acerta primeira vez (não é norma)
