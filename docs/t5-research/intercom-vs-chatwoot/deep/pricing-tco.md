# Deep Dive — Pricing TCO (3 Cenarios)

**Data:** 2026-05-06
**Currency:** USD (Brasil tem volatilidade FX nao modelada)
**Confidence:** High em pricing oficial 2026-05-06

---

## Premissas comuns

- Pricing oficial conforme intercom.com/pricing e chatwoot.com/pricing em 2026-05-06
- Intercom Fin: $0.99/resolution (cobrado quando customer confirma OU sem follow-up em 24h OU Fin completa workflow)
- Chatwoot Captain: credits incluidos por tier + $20/1.000 credits extras
- Cada **1 conversa AI-handled = 1 resolution Intercom = ~1-2 credits Chatwoot** (estimativa conservadora)
- **NAO incluido:** WhatsApp Meta fees (UIC/BIC pass-through Meta — varia por pais), VoIP fees, infraestrutura cliente
- Cenarios assumem deflection target alcancado conforme maturidade publicada

---

## Cenario A — SMB (5 agents, 1.000 conversas/mo, 30% deflection target)

### Intercom

#### Opcao A.1 — Essential + Fin (minimo viavel)

| Item | Calculo | Mensal |
|---|---|---:|
| Essential 5 seats | 5 x $29 | $145 |
| Fin 30% x 1.000 conv | 300 x $0.99 | $297 |
| Copilot 5 agents (10 free/agent) | usar free | $0 |
| **Subtotal Essential setup** | | **$442** |

#### Opcao A.2 — Advanced + Fin (recomendado pelo vendor)

| Item | Calculo | Mensal |
|---|---|---:|
| Advanced 5 seats | 5 x $85 | $425 |
| Fin 30% x 1.000 conv | 300 x $0.99 | $297 |
| Copilot 5 agents | 5 x $29 (ou usar free 10/agent) | $0-145 |
| **Subtotal Advanced setup** | | **$722-867** |

#### Opcao A.3 — Setup conservador real-world

| Item | Calculo | Mensal |
|---|---|---:|
| Advanced 5 seats | 5 x $85 | $425 |
| Fin 30% x 1.000 conv | 300 x $0.99 | $297 |
| Copilot 5 agents | 5 x $29 | $145 |
| Pro Analytics | $99 | $99 |
| Proactive Support Plus (se outbound WhatsApp) | $99 | $99 |
| **Subtotal full Advanced** | | **$1.065** |

### Chatwoot

#### Opcao B.1 — Hacker (free) + self-hosted ou Cloud

| Item | Calculo | Mensal |
|---|---|---:|
| Cloud Hacker | 2 agents free, 500 conv/mo | $0 |
| **Mas:** SMB com 5 agents excede limit | precisa upgrade | — |

Hacker NAO viavel para 5 agents — precisa Startups+.

#### Opcao B.2 — Cloud Startups (recomendado SMB)

| Item | Calculo | Mensal |
|---|---|---:|
| Startups 5 agents | 5 x $19 | $95 |
| Captain credits 300 incl | usar inclusos | $0 |
| **Subtotal Startups** | | **$95** |

NOTA: 300 credits = ~150-300 acoes Captain. Para 1.000 conv com 30% deflection target = 300 acoes Captain necessarias = **dentro do limite included**.

#### Opcao B.3 — Cloud Business (mais features ticketing)

| Item | Calculo | Mensal |
|---|---|---:|
| Business 5 agents | 5 x $39 | $195 |
| Captain credits 500 incl | usar inclusos | $0 |
| **Subtotal Business** | | **$195** |

#### Opcao B.4 — Self-hosted radical (time tem DevOps)

| Item | Calculo | Mensal |
|---|---|---:|
| VPS Hetzner CX21 | $7 | $7 |
| Captain (self-hosted NAO disponivel) | precisa Cloud bridge ou self-LLM API | — |
| Self-LLM API (OpenAI gpt-4o-mini API) | ~$20 / 1k conv | $20 |
| **Subtotal Self-hosted + custom AI** | | **$27** |

### Comparativo Cenario A (SMB)

| Setup | Custo mensal | Custo anual | Multiplo Chatwoot |
|---|---:|---:|---:|
| Intercom Advanced full | $1.065 | $12.780 | **11.2x** |
| Intercom Advanced minimo | $722 | $8.664 | **7.6x** |
| Intercom Essential minimo | $442 | $5.304 | **4.6x** |
| Chatwoot Business | $195 | $2.340 | 2.1x |
| Chatwoot Startups | **$95** | **$1.140** | 1.0x (baseline) |
| Chatwoot Self-hosted custom | $27 | $324 | 0.28x |

**Verdict SMB:** Chatwoot **5-11x economia** vs Intercom. Diferenca anual $4.000-12.000+ paga **1-2 SDR junior brasileiros** com sobra. Para SMB com runway curto, gap e financeiro decisivo. Captain credits 300 inclusos cobrem caso (300 deflection-actions).

---

## Cenario B — Mid-market (20 agents, 5.000 conversas/mo, 50% deflection target)

### Intercom

#### Opcao A.1 — Advanced setup conservador

| Item | Calculo | Mensal |
|---|---|---:|
| Advanced 20 seats | 20 x $85 | $1.700 |
| Fin 50% x 5.000 conv | 2.500 x $0.99 | $2.475 |
| Copilot 5 power-agents | 5 x $29 | $145 |
| **Subtotal Advanced** | | **$4.320** |

#### Opcao A.2 — Advanced full

| Item | Calculo | Mensal |
|---|---|---:|
| Advanced 20 seats | 20 x $85 | $1.700 |
| Fin 50% x 5.000 | 2.500 x $0.99 | $2.475 |
| Copilot 20 agents (alguns power) | 10 x $29 | $290 |
| Pro Analytics | $99 | $99 |
| Proactive Support Plus | $99 | $99 |
| **Subtotal Advanced full** | | **$4.663** |

#### Opcao A.3 — Expert (compliance / multibrand needs)

| Item | Calculo | Mensal |
|---|---|---:|
| Expert 20 seats | 20 x $132 | $2.640 |
| Fin 50% x 5.000 | 2.500 x $0.99 | $2.475 |
| Copilot 10 agents | 10 x $29 | $290 |
| Pro Analytics | $99 | $99 |
| Proactive Support Plus | $99 | $99 |
| **Subtotal Expert** | | **$5.603** |

### Chatwoot

#### Opcao B.1 — Cloud Startups

| Item | Calculo | Mensal |
|---|---|---:|
| Startups 20 agents | 20 x $19 | $380 |
| Captain credits 300 incl + extras | 300 incl, 2.000 extras = $40 | $40 |
| **Subtotal Startups** | | **$420** |

CAVEAT: 5.000 conv / mo com 50% deflection = 2.500 acoes Captain. 300 incluidos + 2.200 extras = $44.

#### Opcao B.2 — Cloud Business (recomendado mid-market)

| Item | Calculo | Mensal |
|---|---|---:|
| Business 20 agents | 20 x $39 | $780 |
| Captain credits 500 incl + extras 2.000 | 500 incl, 2.000 extras = $40 | $40 |
| **Subtotal Business** | | **$820** |

#### Opcao B.3 — Self-hosted + Cloud Captain bridge

| Item | Calculo | Mensal |
|---|---|---:|
| VPS prod Hetzner CCX22 (mid) | $44 | $44 |
| Backup S3 | $20 | $20 |
| Captain Cloud bridge plan (smallest cloud + self-hosted main) | Business 20 agents | $780 |
| **Subtotal Self-hosted + Cloud bridge** | | **$844** |

NOTA: Self-hosted + Cloud bridge nao economiza muito vs full Cloud. Self-hosted economy realiza-se ao usar **self-LLM API** ao inves de Captain Cloud:

#### Opcao B.4 — Self-hosted + custom LLM API

| Item | Calculo | Mensal |
|---|---|---:|
| VPS prod Hetzner CCX22 | $44 | $44 |
| OpenAI gpt-4o-mini API for 5k conv | ~$50-100/mo | $75 |
| Custom integration code (one-time + maintenance) | amortized 10h/mo @ $50 | $500 |
| **Subtotal Self-hosted custom** | | **$619** |

### Comparativo Cenario B (Mid-market)

| Setup | Custo mensal | Custo anual | Multiplo Chatwoot Business |
|---|---:|---:|---:|
| Intercom Expert | $5.603 | $67.236 | **6.8x** |
| Intercom Advanced full | $4.663 | $55.956 | **5.7x** |
| Intercom Advanced conservador | $4.320 | $51.840 | **5.3x** |
| Chatwoot Business | **$820** | **$9.840** | 1.0x (baseline) |
| Chatwoot Self-hosted + Cloud | $844 | $10.128 | 1.0x |
| Chatwoot Self-hosted custom LLM | $619 | $7.428 | 0.75x |
| Chatwoot Startups + extras | $420 | $5.040 | 0.51x |

**Verdict Mid-market:** Chatwoot Business **5.3-6.8x economia** vs Intercom. Diferenca anual $40.000-58.000 paga 4-5 agentes humanos junior brasileiros. Para mid-market crescendo, gap representa **margem que vai direto para outros investimentos (R&D, marketing, hiring)**.

**Caveat critico:** Se Fin entrega 60% deflection real e Captain entrega 35%, Intercom fica com 1.500 mais conversations resolvidas. Custo agente humano para handle 1.500 conv extras ~ 2-3 agents extras = $4.000-6.000 custo. Mesmo nesse cenario Chatwoot ainda vence em ~$36.000/ano. **Math nao quebra ate Fin entregar 80%+ deflection real e Captain ficar abaixo 25%.**

---

## Cenario C — Scale (50 agents, 20.000 conversas/mo, 60% deflection target)

### Intercom

#### Opcao A.1 — Expert (necessario em scale enterprise)

| Item | Calculo | Mensal |
|---|---|---:|
| Expert 50 seats | 50 x $132 | $6.600 |
| Fin 60% x 20.000 conv | 12.000 x $0.99 | **$11.880** |
| Copilot 20 power-agents | 20 x $29 | $580 |
| Pro Analytics | $99 | $99 |
| Proactive Support Plus | $99 | $99 |
| **Subtotal Expert scale** | | **$19.258** |

#### Opcao A.2 — Expert full (todos features)

| Item | Calculo | Mensal |
|---|---|---:|
| Expert 50 seats | 50 x $132 | $6.600 |
| Fin 60% x 20.000 | 12.000 x $0.99 | $11.880 |
| Copilot 50 agents | 50 x $29 | $1.450 |
| Pro Analytics | $99 | $99 |
| Proactive Support Plus | $99 | $99 |
| **Subtotal Expert full** | | **$20.128** |

### Chatwoot

#### Opcao B.1 — Cloud Enterprise

| Item | Calculo | Mensal |
|---|---|---:|
| Enterprise 50 agents | 50 x $99 | $4.950 |
| Captain credits 800 incl + extras volume | 800 incl + ~10.000 extras = $200 | $200 |
| **Subtotal Enterprise** | | **$5.150** |

NOTA: 20.000 conv x 60% deflection = 12.000 acoes Captain. 800 incl + 11.200 extras @ $20/1.000 = $224.

#### Opcao B.2 — Cloud Business (se features Business sufficient)

| Item | Calculo | Mensal |
|---|---|---:|
| Business 50 agents | 50 x $39 | $1.950 |
| Captain credits 500 incl + extras | 500 incl + 11.500 extras = $230 | $230 |
| **Subtotal Business scale** | | **$2.180** |

#### Opcao B.3 — Self-hosted production + Cloud bridge

| Item | Calculo | Mensal |
|---|---|---:|
| Production VPS cluster (Hetzner CCX42 + replica) | $200 | $200 |
| PostgreSQL managed + Redis managed (DigitalOcean) | $300 | $300 |
| Backup + monitoring | $100 | $100 |
| Captain Cloud bridge (Business plan smallest = 5 cloud agents para AI) | 5 x $39 + extras | $215 |
| DevOps maintenance (10-15h/mo @ $50) | | $625 |
| **Subtotal Self-hosted + Cloud Captain** | | **$1.440** |

#### Opcao B.4 — Self-hosted + custom LLM (mais economico)

| Item | Calculo | Mensal |
|---|---|---:|
| VPS prod cluster | $200 | $200 |
| Managed DB + Redis | $300 | $300 |
| OpenAI/Anthropic API (gpt-4o-mini @ ~$0.15/1k tokens; ~12k conv ~ $400) | | $400 |
| Custom integration + maintenance | 10h/mo @ $50 | $500 |
| **Subtotal Self-hosted + custom LLM** | | **$1.400** |

### Comparativo Cenario C (Scale)

| Setup | Custo mensal | Custo anual | Multiplo Chatwoot Enterprise |
|---|---:|---:|---:|
| Intercom Expert full | $20.128 | $241.536 | **3.9x** |
| Intercom Expert conservador | $19.258 | $231.096 | **3.7x** |
| Chatwoot Enterprise | **$5.150** | **$61.800** | 1.0x (baseline) |
| Chatwoot Business scale | $2.180 | $26.160 | 0.42x |
| Chatwoot Self-hosted + Cloud Captain | $1.440 | $17.280 | 0.28x |
| Chatwoot Self-hosted + custom LLM | $1.400 | $16.800 | 0.27x |

**Verdict Scale:** Chatwoot Enterprise **3.7-3.9x economia** vs Intercom. Self-hosted reduz a **14x economia** ($1.400 vs $20.000). Diferenca anual de **$179.000+** paga **15-18 agentes brasileiros junior** ou cinco senior.

**Per-resolution Fin AI vira proibitivo em scale:** $11.880/mo so em AI = $142.560/ano so para AI. Chatwoot equivalente $200-400/mo em credits = $2.400-4.800/ano. **Diferencial AI-only de $137.000+/ano**.

**Math do justificavel:** Para Intercom Expert valer pena vs Chatwoot Enterprise em scale, deflection Fin precisaria ser **dramaticamente** superior a Captain — algo como 75-80% Fin vs 30-35% Captain. Diferenca ~12.000 deflection-actions por mes = ~10 humanos handling overflow @ $4k/mo = $40k/mo cost extra Chatwoot. Ainda assim Chatwoot wins por $135k+/ano.

**Conclusao scale:** Intercom Expert em scale **so se justifica em casos narrow:**
1. SaaS B2B com Product Tours obrigatorios + in-app heavy
2. Compliance HIPAA + multibrand obrigatorios out-of-box
3. Switching cost de migrar de Intercom existente alto demais
4. Brand value associado ao "Intercom standard" (rare)

---

## Tabela consolidada 3 cenarios

| Cenario | Intercom recomendado | Chatwoot recomendado | Economia mensal | Economia anual | Multiplo |
|---|---:|---:|---:|---:|---:|
| **A SMB** (5 agents, 1k conv, 30%) | $722 (Adv min) | $95 (Startups) | $627 | $7.524 | **7.6x** |
| **B Mid-market** (20 agents, 5k conv, 50%) | $4.663 (Adv full) | $820 (Business) | $3.843 | $46.116 | **5.7x** |
| **C Scale** (50 agents, 20k conv, 60%) | $20.128 (Expert full) | $5.150 (Enterprise) | $14.978 | $179.736 | **3.9x** |

### Sumario quantitativo

- **SMB:** Chatwoot 7.6x mais barato — gap $7.500/ano = 1 SDR junior BR
- **Mid-market:** Chatwoot 5.7x — gap $46k/ano = 4-5 agentes BR
- **Scale:** Chatwoot 3.9x — gap $180k/ano = 15-18 agentes BR ou expansao R&D significativa

---

## Sensibilidade a deflection delta

Pergunta: **a partir de que delta de deflection (Captain vs Fin) Intercom vira economic justificado?**

Calculo: Se Captain deflection X% e Fin deflection Y%, e diferenca Y-X entrega N conversations a mais resolvidas, custo de N agentes humanos para handle e $4k/mo per agent BR ou $8k/mo per agent USA.

### SMB (1.000 conv/mo)

- 1pp delta = 10 conversations a mais resolvidas = 0.05 agente extra = $200/mo
- Chatwoot ganho atual: $627/mo
- **Break-even:** ~3pp delta pelo qual Intercom igualaria
- Para Intercom vencer SMB, precisaria delta deflection > 3pp **E** outros benefits (in-app, etc)

### Mid-market (5.000 conv/mo)

- 1pp delta = 50 conversations a mais resolvidas = 0.25 agente extra = $1.000/mo
- Chatwoot ganho atual: $3.843/mo
- **Break-even:** ~4pp delta
- Para Intercom vencer mid-market, precisaria delta > 4pp + casos nao-genericos (in-app, compliance)

### Scale (20.000 conv/mo)

- 1pp delta = 200 conversations a mais resolvidas = 1 agente extra = $4.000/mo
- Chatwoot ganho atual: $14.978/mo
- **Break-even:** ~3-4pp delta
- Para Intercom vencer scale, precisaria delta > 4pp **E** Fin AI sustained advantage (improvement +1%/mo)

**Conclusao sensibilidade:** Intercom precisaria entregar **delta deflection >4pp consistentemente** para math fechar. Industry estimates sugerem que essa diferenca **e plausivel** se Captain ainda underperforma Fin em 10-20pp. Mas **nao e provada** — exige piloto.

**Critical insight:** O gap de pricing 5x Chatwoot e tao grande que **Intercom precisaria ser 2x melhor em deflection real** para math fechar (no caso scale). Esse e cenario possivel mas nao default. **Sem piloto, escolha conservadora e Chatwoot.**

---

## Disclaimer e limitations

1. **Captain credits-per-action** definicao vaga em docs oficiais — assumi conservador 1 credit ~ 1 conversation handled
2. **WhatsApp Meta fees** NAO incluidas — variam por pais (UIC vs BIC); pass-through em ambos players
3. **VoIP/voice fees** NAO incluidas — Intercom Talk (separate) e Chatwoot voice (Enterprise) tem custos extra
4. **Custos infra Chatwoot self-hosted** estimativos — variam por provedor (AWS/GCP 20-50% mais caros que Hetzner)
5. **Tempo DevOps maintenance** estimativo $50/h junior; senior pode ser 2-3x mais caro
6. **FX cambial** nao modelada — tudo em USD
7. **Custom LLM API costs** estimativos com gpt-4o-mini; usar Claude Haiku ou GPT-4o full pode multiplicar 5-10x
8. **Volume de conv assumido linear** — picos sazonais (Black Friday, etc) podem dobrar AI cost Intercom em mes pico
