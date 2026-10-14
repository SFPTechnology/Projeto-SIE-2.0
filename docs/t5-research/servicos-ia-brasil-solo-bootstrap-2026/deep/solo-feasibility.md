# Deep Dive — Solo Feasibility (onde quebra a operação sem time)

**Pergunta-chave:** Em que ponto cada serviço deixa de ser viável para 1 pessoa? Quais são os limites duros?

**Lente:** Founder solo, 30-40h/semana dedicado, sem capital para contratar antes do 4° cliente.

---

## Framework — 4 estágios de capacidade

| Estágio | # clientes | Ponto crítico |
|---|---|---|
| **S0 — Setup** | 0 | Posso construir o produto/oferta sozinho? |
| **S1 — Primeiro cliente** | 1 | Posso entregar 1 cliente de ponta-a-ponta sozinho? |
| **S2 — Operação inicial** | 2-5 | Posso operar com 5 clientes mantendo qualidade? |
| **S3 — Escala** | 10-20 | Sem time, o que quebra antes? |

---

## Avaliação por serviço

### Mentoria Premium

| Estágio | Viável solo? | O que quebra |
|---|---|---|
| S0 — Setup | ✅ Sim | Material + landing + comunidade montáveis em 2-4 semanas |
| S1 — Primeiro cliente | ✅ Sim | 1:1 ou cohort pequena é literalmente o produto |
| S2 — 2-5 clientes | ✅ Sim | Mentoria 1:1 vs grupo escolhe trade-off |
| S3 — 10-20 clientes | ⚠️ Tensão | Mentoria 1:1 trava em 6-8 alunos; grupo escala melhor; precisa ops |

**Quebra em:** 10+ alunos 1:1 ou 50+ alunos em cohort sem suporte de community manager.
**Mitigação:** Pivotar para format de cohort + assistente part-time (R$ 3-5k/mês).
**Veredicto solo:** ✅ Excelente até ~30 alunos cohort com 1 assistente part-time.

---

### Automação n8n Vertical

| Estágio | Viável solo? | O que quebra |
|---|---|---|
| S0 — Setup | ✅ Sim | Template+host+playbook em 2-3 semanas |
| S1 — Primeiro cliente | ✅ Sim | Projeto de 40-80h cabe em 30-45 dias |
| S2 — 2-5 clientes | ⚠️ Tensão | Retainer + novo projeto + suporte = 100-120h/mês — limite |
| S3 — 10-20 clientes | ❌ Quebra | Suporte + monitoramento + novos projetos = 180h+/mês |

**Quebra em:** 6-8 clientes simultâneos com retainer ativo + novos projetos.
**Mitigação:** Templatizar agressivamente + contratar implementador júnior no 4-5° cliente (R$ 5-8k/mês).
**Veredicto solo:** ✅ Viável até ~6 clientes em retainer; depois precisa time.

---

### WhatsApp Vertical

| Estágio | Viável solo? | O que quebra |
|---|---|---|
| S0 — Setup | ✅ Sim | WBA + template em 5-10 dias |
| S1 — Primeiro cliente | ✅ Sim | Setup 4-10h, depois 1-3h/mês manutenção |
| S2 — 2-5 clientes | ✅ Sim | 10-15h/mês total |
| S3 — 10-30 clientes | ✅ Sim | Templatização extrema cabe em 1 pessoa |
| S3+ — 30-100 clientes | ⚠️ Tensão | Vendas + suporte saturam 1 pessoa |

**Quebra em:** 50+ clientes simultâneos. Vendas é o gargalo, não entrega.
**Mitigação:** Self-service tier R$ 199-500/mês + 1 SDR humano part-time.
**Veredicto solo:** ✅ Maior capacidade solo do bench. Pode escalar até 30-50 sozinho.

---

### SDR IA Voz + HITL

| Estágio | Viável solo? | O que quebra |
|---|---|---|
| S0 — Setup | ✅ Sim | Voice agent + integração 2-3 semanas |
| S1 — Primeiro cliente | ⚠️ Tensão | HITL exige presença constante (revisar cada ligação) |
| S2 — 2-3 clientes | ❌ Quebra | Solo não escala HITL para múltiplos clientes simultâneos |
| S3 — 5+ clientes | ❌ Quebra | Impossível solo |

**Quebra em:** 2° cliente simultâneo. Solo founder não consegue ser HITL para 2 fluxos.
**Mitigação:** Defer ou contratar 1 PJ-HITL imediato (R$ 3-5k/mês) → o que viola a premissa solo bootstrap.
**Veredicto solo:** ❌ **Não recomendado solo no MVP.** Defer para ano 2.

---

### LGPD Governança / Cyber IA / Preditivo Custom

| Estágio | Viável solo? |
|---|---|
| S0 — Setup | ❌ Já quebra (credenciais ausentes) |

**Veredicto:** Veto estrutural já no estágio S0. Não é questão de escala — é questão de credenciais que solo founder não tem.

---

### GenAI Conteúdo / Chatbot Genérico

| Estágio | Viável solo? | O que quebra |
|---|---|---|
| S0 — Setup | ✅ Sim | 1-3 dias |
| S1 — Primeiro cliente | ✅ Sim | Self-serve |
| S3 — Escala | ✅ Tecnicamente sim | Mas não há defensibilidade — não é negócio |

**Veredicto:** Tecnicamente viável solo em qualquer escala — mas defensibilidade 1 → não construir aqui.

---

## Matriz consolidada — onde solo founder pode operar?

| Serviço | S0 Setup | S1 1° cliente | S2 2-5 | S3 10-20 | Cap teórico solo |
|---|---:|---:|---:|---:|---:|
| Mentoria Premium | ✅ | ✅ | ✅ | ✅ | ~30 cohort + 1 PA |
| Automação n8n | ✅ | ✅ | ⚠️ | ❌ | ~6 retainers |
| WhatsApp Vertical | ✅ | ✅ | ✅ | ✅ | ~30-50 clientes |
| SDR IA Voz | ✅ | ⚠️ | ❌ | ❌ | 1-2 clientes (não viável) |
| LGPD / Cyber / Preditivo | ❌ | — | — | — | 0 |
| GenAI Conteúdo | ✅ | ✅ | ✅ | ✅ | ilimitado mas baixo LTV |
| Chatbot Genérico | ✅ | ✅ | ✅ | ✅ | ilimitado mas commodity |

---

## Estratégia de capacidade composta

Como solo founder pode operar 3 serviços simultâneos sem quebrar?

### Distribuição de tempo (semana de 30h)

```
12h  Mentoria Premium (1 cohort de 10 + 2 1:1)
      ├─ 4h conteúdo
      ├─ 4h calls de grupo
      ├─ 2h 1:1
      └─ 2h comunidade
10h  Automação n8n (3 retainers + 1 projeto)
      ├─ 4h retainer support
      ├─ 4h novo projeto
      └─ 2h pré-vendas
 5h  WhatsApp Vertical (10 clientes self-service+mid)
      ├─ 2h monitoramento
      ├─ 2h onboarding novo
      └─ 1h vendas
 3h  Marketing/conteúdo (LinkedIn + newsletter)
```

**Receita projetada em estado estacionário (mês 6-12):**
- Mentoria: R$ 30-60k/mês (mistura cohort+1:1)
- Automação: R$ 15-30k/mês (retainers+projetos)
- WhatsApp: R$ 8-25k/mês (mix self+mid)
- **Total:** R$ 53-115k/mês de receita

**Margem ponderada:** 75-82%
**Custos:** R$ 8-12k/mês (tooling + ads + 1 PA part-time eventual)
**Margem líquida solo:** R$ 41-103k/mês

---

## Sinais de "hora de contratar"

Watch list para solo founder identificar quando time vira necessidade:

| Sinal | Resposta |
|---|---|
| > 35h/semana 4 semanas seguidas | Contratar 1 PA (R$ 3-5k/mês) |
| > 6 clientes Automação retainer | Contratar implementador júnior (R$ 5-8k/mês) |
| > 30 clientes WhatsApp ativos | Contratar 1 SDR + 1 suporte (R$ 6-10k/mês) |
| > 30 alunos cohort Mentoria | Contratar community manager (R$ 3-5k/mês) |
| 2° cliente SDR IA Voz | Contratar 1 HITL PJ (R$ 3-5k/mês) ANTES de fechar |

**Regra:** Não contratar antes de R$ 30k/mês de receita estável. Antes disso, dizer "não" ou aumentar preço.

---

## Confiança epistêmica

- Cap solo por serviço: **MEDIA** — baseada em benchmarks de operadores BR similares
- Distribuição de tempo: **MEDIA** — assume founder eficiente, sem retrabalho excessivo
- Receita estacionária projetada: **BAIXA** — depende de execução de 6+ meses contínuos
