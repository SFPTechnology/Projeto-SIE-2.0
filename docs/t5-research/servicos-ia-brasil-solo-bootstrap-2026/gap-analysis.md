# Gap Analysis — Capacidade Solo vs. Exigências de Cada Serviço

**Princípio:** Cada serviço exige um conjunto de capacidades, ativos e credenciais. Solo founder chega com kit limitado. Esta análise expõe gaps, prioriza-os (P0/P1/P2/P3) e estima o esforço de fechamento.

**Kit inicial assumido:**
- Skills: operação digital, vendas B2B básica, redação, noção de IA / prompt engineering
- Tools: WhatsApp pessoal, domínio próprio, conta Stripe/Asaas, Notion, 1 LLM API key
- Rede: LinkedIn pessoal + 5-30 conversas pagantes anteriores
- Tempo: 20-40h/semana
- Capital marketing: R$ 1-5k/mês

Faltou esse contexto? Reabra o bench com `*bench-quick` reajustando o starting kit.

---

## Sumário executivo de gaps

| Serviço | Veredicto | Gaps fecháveis solo | Tempo p/ 1ª venda após fechar gaps |
|---|---|---|---|
| Mentoria Premium | ✅ GAP_FECHÁVEL_30D | 4/4 (100%) | 21-45 dias |
| Automação n8n | ✅ GAP_FECHÁVEL_30_45D | 5/5 (100%) | 30-60 dias |
| WhatsApp Vertical | ✅ GAP_FECHÁVEL_15D | 4/4 (100%) | 14-30 dias |
| SDR IA Voz+HITL | ⚠️ PARCIAL_DEFER | 1/3 (33%) | 60-120 dias |
| LGPD Governança | ❌ VETO_ESTRUTURAL | 0/2 (0%) | 365-720 dias |
| Cyber IA | ❌ VETO_ESTRUTURAL | 0/2 (0%) | 540-1095 dias |
| Preditivo Custom | ❌ VETO_ESTRUTURAL | 0/2 (0%) | 365-1095 dias |
| GenAI Conteúdo | ⚠️ VENDÁVEL_NÃO_NEGÓCIO | 1/1 (100%) | 1-7 dias |
| Chatbot Genérico | ❌ DO_NOT_ENTER | 0/1 (0%) | n/a |

---

## Mentoria Premium IA — gaps detalhados

**Veredicto:** Solo founder pode vender em 21-45 dias após fechar 4 gaps. Único bloqueante real é autoridade percebida.

| ID | Prioridade | Gap | Tempo p/ fechar | Custo | Mitigação |
|---|---|---|---|---|---|
| M-G01 | **P0** | Autoridade percebida | 15-30d | R$ 0-5k | QW-6 mini-curso + 3 lives + 1 caso documentado |
| M-G02 | P1 | Oferta premium packageada (Hormozi $100M) | 5-10d | R$ 0-1,5k | Acionar `/copy-chief` |
| M-G03 | P2 | Comunidade fechada + agenda + logística | 2-5d | R$ 200-800 | Circle.so ou Discord pronto |
| M-G04 | P2 | Funil de captação contínuo | 30-60d | R$ 1-5k | Cadência fixa LinkedIn+live+newsletter |

**Caminho crítico:** M-G01 é o único P0. Os demais paralelizam.

---

## Automação n8n Vertical — gaps detalhados

**Veredicto:** Solo founder pode vender em 30-60 dias. Bloqueantes são template + 1 caso de prova.

| ID | Prioridade | Gap | Tempo p/ fechar | Custo | Mitigação |
|---|---|---|---|---|---|
| A-G01 | **P0** | Template de entrega demonstrável | 7-14d | R$ 0-500 | QW-4 (templates boleto/cobrança) |
| A-G02 | **P0** | 1 caso entregue com métricas | 14-30d | R$ 0-2k | Entregar piloto gratuito/custo p/ testimonial |
| A-G03 | P1 | Infra de operação (host + logging + runbook) | 3-7d | R$ 50-200 | Hetzner + Coolify + n8n (~R$ 80/mês) |
| A-G04 | P1 | Discovery pago como gateway | 3-5d | R$ 0-500 | QW-1 template pronto |
| A-G05 | P2 | Vertical específico (financeiro/jurídico/logística) | 7-14d | R$ 0-1k | QW-7 reposicionamento |

**Caminho crítico:** A-G01 + A-G02 em paralelo (template + 1 piloto) = ~30 dias.

---

## WhatsApp Vertical — gaps detalhados

**Veredicto:** Solo founder pode vender em 14-30 dias. Mais rápido do bench.

| ID | Prioridade | Gap | Tempo p/ fechar | Custo | Mitigação |
|---|---|---|---|---|---|
| W-G01 | **P0** | Escolha de 1 vertical (não-genérico) | 3-7d | R$ 0-500 | QW-7 (clínica / restaurante / imob / advocacia) |
| W-G02 | **P0** | Conta WhatsApp Business API verificada | 5-14d | R$ 0-200 | Zenvia ou 360dialog ou Take Blip |
| W-G03 | P1 | Playbook de fluxos do vertical | 5-10d | R$ 0-500 | 10-15 intents + handoff + dashboard |
| W-G04 | P2 | Integração com 1-3 CRMs típicos | 3-7d | R$ 0-200 | Webhook n8n + Pipedrive/RD/HubSpot |

**Caminho crítico:** W-G01 → W-G02 → W-G03 sequencial = ~15 dias se otimizado.

---

## SDR IA Voz + HITL — gaps detalhados

**Veredicto:** Parcial. Solo founder não fecha gap P0 sem contratar 2° pessoa OU receber HITL do cliente.

| ID | Prioridade | Gap | Tempo p/ fechar | Custo | Mitigação |
|---|---|---|---|---|---|
| S-G01 | **P0** | 2° humano obrigatório (HITL) | 30-90d | R$ 3-5k/mês | Defer ou PJ a partir do 3° cliente |
| S-G02 | **P0** | ICP+copy validados do cliente | 14-30d | R$ 2-8k | Discovery pago obrigatório antes do agente |
| S-G03 | P1 | Compliance Marco IA (PL 2338) | 5-10d | R$ 0-1k | Template policy + opt-out |

**Conclusão:** Defer para ano 2 quando solo founder tiver 1 PJ ou estrutura mínima.

---

## LGPD Governança — gaps detalhados

**Veredicto:** Veto estrutural. Solo founder não fecha gap de credencial jurídica em < 1 ano.

| ID | Prioridade | Gap | Tempo p/ fechar | Custo | Mitigação |
|---|---|---|---|---|---|
| L-G01 | **P0** | Credenciais jurídicas (OAB + DPO) | 365-1095d | R$ 50-200k | INVIÁVEL solo — só via parceria white-label com escritório |
| L-G02 | **P0** | Ciclo de venda comitê (4-5 decisores) | 180-540d | R$ 20-100k | Não viável solo |

**Conclusão:** Defer para ano 3+. Alternativa: parceria white-label com escritório existente.

---

## Cyber IA — gaps detalhados

**Veredicto:** Veto estrutural. Idênticos a LGPD + SOC 24/7.

| ID | Prioridade | Gap | Tempo p/ fechar | Custo |
|---|---|---|---|---|
| C-G01 | **P0** | Certificações (CISSP/CISM/ISO 27001) | 365-1095d | R$ 20-80k |
| C-G02 | **P0** | Infra SOC 24/7 ou parceria white-label | 180-540d | R$ 100-500k |

---

## Preditivo Customizado — gaps detalhados

**Veredicto:** Veto estrutural. Solo founder não entrega PoC 3-36 meses sem stack DS sênior.

| ID | Prioridade | Gap | Tempo p/ fechar | Custo |
|---|---|---|---|---|
| P-G01 | **P0** | Competência DS sênior (3-5 anos prod) | 365-1095d | R$ 50-150k |
| P-G02 | **P0** | Dado estruturado do cliente (60-80% do tempo) | 90-270d | R$ 30-150k |

---

## GenAI Conteúdo — gaps detalhados

**Veredicto:** Zero gap técnico — vendável já. Problema é estratégico (defensibilidade 1/5).

| ID | Prioridade | Gap | Recomendação |
|---|---|---|---|
| G-G01 | P2 | Diferenciação por nicho ou comunidade | Usar como **funil de Mentoria**, não como negócio principal |

**Strategic note:** Vender é fácil; construir negócio defensível é impossível. Cabe como canal de aquecimento, posicionando para upsell Mentoria/Automação.

---

## Chatbot Genérico — gaps detalhados

**Veredicto:** DO_NOT_ENTER. Categoria commoditizada, sem path-to-defensibility.

| ID | Prioridade | Gap | Recomendação |
|---|---|---|---|
| B-G01 | P0 | Categoria já commoditizada (R$ 199/mês, churn alto) | Reposicionar como WhatsApp Vertical (outro serviço deste bench) |

---

## Síntese estratégica de gap-closure

### Quem fecha gap mais rápido (TTFR pós-gap)

1. 🥇 **WhatsApp Vertical** — 14-30 dias
2. 🥈 **Mentoria Premium** — 21-45 dias
3. 🥉 **Automação n8n** — 30-60 dias

### Quem tem maior valor estratégico após gap-closure

1. 🥇 **Mentoria Premium** — defensibilidade 5 + margem 80% + LTV ano1 até R$ 300k
2. 🥈 **Automação n8n** — margem 95% + MRR recorrente + entrega templatável

---

## Recomendação composta (vai virar plano no `executive-report.md`)

**Stack temporal para solo founder:**

```
Semana 1-2:   WhatsApp Vertical (cash imediato se houver demanda óbvia)
Semana 3-6:   Mentoria Premium (lançamento principal)
Semana 4-8:   Automação n8n (oferta de entrada cross-sell)
Mês 6-12:    SDR IA Voz (quando houver 1 PJ ou time)
Ano 2-3:     LGPD/Cyber/Preditivo (parceria ou time formado)
```

**Anti-padrões a evitar:**
- ❌ Tentar entregar LGPD/Cyber/Preditivo solo no 1° ano → falência por escopo aberto
- ❌ Construir negócio em torno de GenAI Conteúdo bulk → commoditização em 6 meses
- ❌ Vender chatbot genérico — refazer como WhatsApp Vertical
- ❌ SDR IA Voz sem 2° pessoa → 40% projetos cancelados (Gartner)

---

## Confiança epistêmica

- Gaps P0 vetados (LGPD/Cyber/Preditivo): **ALTA** — estruturais, não conjunturais
- Tempo de fechamento de gaps fecháveis: **MEDIA** — depende de execução do operador
- Custo de fechamento de gaps: **MEDIA** — faixas baseadas em benchmark + experiência do mercado BR
