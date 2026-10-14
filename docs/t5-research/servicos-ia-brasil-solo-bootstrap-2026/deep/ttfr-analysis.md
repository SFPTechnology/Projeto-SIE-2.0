# Deep Dive — TTFR (Time-to-First-Revenue) por Serviço

**Definição:** TTFR = dias entre `decidir vender este serviço` e `primeiro real depositado na conta`. Inclui setup, validação de oferta, primeira venda fechada.

**Lente:** Solo founder com kit inicial (LinkedIn, conta Stripe/Asaas, domínio, 5-30 conversas prévias).

---

## Tabela-resumo de TTFR

| Serviço | TTFR Realístico | Distribuição | Caminho crítico |
|---|---|---|---|
| GenAI Conteúdo SaaS | **1-14 dias** | mediana 5d | Setup tool + 1 venda Stripe |
| Chatbot Genérico | **1-14 dias** | mediana 5d | Mesmo de GenAI |
| WhatsApp Vertical | **3-21 dias** | mediana 14d | WBA + template + 1 cliente local |
| Mentoria Premium | **7-45 dias** | mediana 30d | Oferta + autoridade + 1 conversa fechada |
| Automação n8n | **14-45 dias** | mediana 30d | Template + caso + 1 discovery pago |
| SDR IA Voz+HITL | **21-90 dias** | mediana 60d | Discovery + setup + período de prova |
| LGPD Governança | **90-270 dias** | mediana 180d | RFP + comitê + contrato |
| Cyber IA | **120-365 dias** | mediana 240d | Idem + certificações |
| Preditivo Custom | **120-365 dias** | mediana 240d | PoC + dados + iteração |

---

## Decomposição passo-a-passo (top 5 candidatos)

### 1. WhatsApp Vertical — 3-21 dias

```
Dia 1-2     Escolha de vertical (clínica de odonto / restaurante de bairro / imob.)
Dia 3-5     Setup WhatsApp Business API via Zenvia ou 360dialog
Dia 4-7     Construção do bot template (10-15 intents + handoff humano)
Dia 6-10    Lista de 30-50 leads-alvo via Google Maps/Insta do vertical
Dia 7-14    Outreach direto (DM + Loom demo) → 3-5 reuniões
Dia 10-21   Fechamento + setup do 1° cliente → primeiro pagamento

Bottleneck #1: aprovação WBA pode levar 5-10 dias úteis
Bottleneck #2: cliente local pode pedir 3-7 dias para "pensar"
Atalho: oferecer 7 dias de trial pago R$ 500 (não trial gratuito)
```

**Primeiro pagamento típico:** R$ 500-3.000 setup + R$ 500-3.000 recorrente
**Veredicto:** TTFR mais rápido do bench com defensibilidade ≥ 3

---

### 2. Mentoria Premium — 7-45 dias

```
Dia 1-7     Definir oferta principal: promessa + entregáveis + garantia + preço
Dia 3-10    Produzir 3-5 conteúdos de autoridade (LinkedIn artigos, Loom, lives)
Dia 7-14    Mini-curso 7 dias (QW-6) para captar 100-300 emails
Dia 14-30   Webinar de fechamento OU 5-10 ligações 1:1 OU evento presencial
Dia 21-45   1° fechamento de R$ 5-30k (entry) ou R$ 30-300k (premium)

Bottleneck #1: autoridade percebida — se zero histórico, prolonga para 60-90d
Bottleneck #2: oferta sem âncora alta dificulta venda premium
Atalho: 1 evento presencial fechado (cobrança no ato com Asaas) acelera 30d
```

**Primeiro pagamento típico:** R$ 5-30k entry (cohort) ou R$ 30-300k premium (1:1)
**Veredicto:** TTFR moderado com maior LTV e defensibilidade do bench

---

### 3. Automação n8n Vertical — 14-45 dias

```
Dia 1-5     Escolher vertical de dor pagante (financeiro/jurídico/logística/imob)
Dia 3-7     Build template n8n principal (boleto+cobrança, follow-up, scraping)
Dia 7-14    Hospedar (Hetzner + Coolify + n8n container ~R$ 80/mês)
Dia 10-21   Caso-piloto: entregar 1 cliente atual gratuito/custo R$ 500 → testimonial
Dia 14-30   Pacote Discovery Pago R$ 5k → vender em 3-5 reuniões
Dia 21-45   Conversão discovery → projeto R$ 15-30k + retainer R$ 2-5k/mês

Bottleneck #1: sem caso documentado, cliente pede "mostra" antes
Bottleneck #2: discovery pago tem fricção inicial (mercado BR resiste)
Atalho: começar com QW-1 (discovery pago R$ 5k) — receita imediata
```

**Primeiro pagamento típico:** R$ 5k discovery (15d) → R$ 15-30k projeto (45d)
**Veredicto:** TTFR moderado com melhor margem do bench (80-95%)

---

### 4. SDR IA Voz+HITL — 21-90 dias

```
Dia 1-7     Discovery pago R$ 5-15k com cliente B2B mid-market
Dia 7-21    Mapeamento ICP + copy + cadência (5 variações)
Dia 14-30   Setup voice agent (Vapi / Bland.ai / Retell) + integração CRM
Dia 21-45   Período de prova 2-4 semanas (HITL revisando cada interação)
Dia 45-90   Conversão prova → contrato R$ 5-15k/mês recorrente

Bottleneck #1: solo founder não escala HITL além do 1° cliente
Bottleneck #2: cliente desliga se ROI não aparecer em 30d
Bottleneck #3: Marco IA 2025 exige transparência obrigatória
Atalho: vender discovery primeiro, agente depois (escopo controlado)
```

**Primeiro pagamento típico:** R$ 5-15k discovery + recorrente vem em 60-90d
**Veredicto:** TTFR aceitável mas solo-feasibility = 2 → defer

---

### 5. GenAI Conteúdo SaaS (revenda) — 1-14 dias

```
Dia 1       Inscrição em Jasper/Copy.ai/Writesonic/produto white-label BR
Dia 2-3     Setup landing page + 3 ofertas (mensal/anual/agência)
Dia 3-7     Outreach direto + grupo WhatsApp + Insta
Dia 7-14    1° venda self-serve R$ 100-3k

Bottleneck #1: ChatGPT free é concorrente direto — diferenciação difícil
Bottleneck #2: commoditização em 6 meses
Atalho: posicionar como funil para Mentoria (não negócio principal)
```

**Primeiro pagamento típico:** R$ 100-500/mês recorrente
**Veredicto:** TTFR rápido mas LTV baixo + defensibilidade 1 → não-negócio principal

---

## Análise de bottlenecks transversais

Quais bottlenecks aparecem em múltiplos serviços e como mitigá-los?

| Bottleneck | Aparece em | Mitigação universal |
|---|---|---|
| **Falta de caso documentado** | Automação, SDR, WhatsApp | Entregar 1 piloto gratuito/custo em troca de testimonial + métricas |
| **Discovery pago resistência** | Automação, SDR, LGPD, Cyber | Posicionar como "auditoria/diagnóstico" não "discovery"; bundle com garantia |
| **Comitê de decisão** | LGPD, Cyber, Preditivo | Veto solo — só viável com sponsor interno forte |
| **Autoridade percebida** | Mentoria | Mini-curso 7d (QW-6) + 1 evento presencial + estudo de caso |
| **Compliance Marco IA** | SDR, Preditivo | Template policy + opt-out + identificação IA visível |
| **Escolha de vertical** | WhatsApp, Automação, SDR | Escolher 1 vertical em ≤7 dias, não procrastinar com "vamos validar" |

---

## TTFR otimizado — playbook 90 dias

Para solo founder otimizando os 3 vencedores em paralelo:

```
Semana 1-2   WhatsApp Vertical (cash em 14-21 dias)
              └─> Vertical escolhido + WBA + template + 5 outreaches/dia
Semana 2-4   Discovery Pago R$ 5k para Automação n8n
              └─> Oferta cross-sell para clientes WhatsApp + LinkedIn outbound
Semana 4-6   Mini-curso 7d (Mentoria)
              └─> Captação 100-300 emails + webinar fechamento
Semana 6-10  Fechamento Mentoria + Automação completa
              └─> 1° venda Mentoria R$ 5-30k + 1° projeto Automação R$ 15-30k
Semana 10-13 Compounding
              └─> Estudos de caso + indicações + segundo cliente cada
```

**Resultado esperado em 90 dias (cenário conservador):**
- WhatsApp: 2-5 clientes × R$ 800/mês = R$ 1,6-4k MRR
- Automação: 1-2 projetos × R$ 15k + retainer = R$ 15-30k receita + R$ 2-5k MRR
- Mentoria: 1-3 vendas × R$ 5-15k = R$ 5-45k receita

**Total 90 dias:** R$ 21-79k receita projetada + R$ 3,6-9k MRR

---

## Confiança epistêmica

- TTFR mínimos (3, 7, 14, 21 dias) — **ALTA** — derivados de cases documentados e quick-wins do `quick-wins.md`
- TTFR máximos (21, 45, 90 dias) — **MEDIA** — assumem execução solo competente
- Projeção 90 dias receita — **BAIXA** — depende de execução, sorte, tração; é cenário direcional

Caveat principal: TTFR pressupõe que o operador executa cada gap-closure no prazo. Atraso composto multiplica.
