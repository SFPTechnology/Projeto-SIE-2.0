# Scorecard — Intercom vs Chatwoot

**Data:** 2026-05-06
**Tipo:** Product
**Metodo:** Weighted multi-dimension 0-100 per axis. Pesos conforme contrato de mission.

## Pesos por dimensao

| ID | Dimensao | Peso |
|---|---|---:|
| C1 | AI deflection performance | 25% |
| C2 | AI pricing model honesty | 15% |
| C3 | Canais nativos diversidade | 15% |
| C4 | In-app messaging strength | 10% |
| C5 | Pricing total TCO 3 cenarios | 15% |
| C6 | Comunidade / Marketplace | 5% |
| C7 | Self-hosted / sovereignty | 10% |
| C8 | Time-to-value / setup | 5% |

---

## Tabela de scores

| Dimensao | Intercom | Chatwoot | Delta | Vencedor |
|---|---:|---:|---:|---|
| C1 — AI deflection performance | **85** | 50 | +35 | **Intercom** |
| C2 — AI pricing model honesty | 75 | **80** | -5 | Empate (Chatwoot leve) |
| C3 — Canais nativos diversidade | 60 | **95** | -35 | **Chatwoot** |
| C4 — In-app messaging strength | **95** | 50 | +45 | **Intercom** |
| C5 — Pricing total TCO | 50 | **90** | -40 | **Chatwoot** |
| C6 — Comunidade / Marketplace | **85** | 75 | +10 | Intercom |
| C7 — Self-hosted / sovereignty | 0 | **100** | -100 | **Chatwoot** |
| C8 — Time-to-value | **90** | 75 | +15 | Intercom |

## Calculo ponderado

### Intercom — 67.50 / 100

| Dim | Score | Peso | Contribuicao |
|---|---:|---:|---:|
| C1 | 85 | 25% | 21.25 |
| C2 | 75 | 15% | 11.25 |
| C3 | 60 | 15% | 9.00 |
| C4 | 95 | 10% | 9.50 |
| C5 | 50 | 15% | 7.50 |
| C6 | 85 | 5% | 4.25 |
| C7 | 0 | 10% | 0.00 |
| C8 | 90 | 5% | 4.50 |
| **Total** | | | **67.50** |

### Chatwoot — 75.00 / 100

| Dim | Score | Peso | Contribuicao |
|---|---:|---:|---:|
| C1 | 50 | 25% | 12.50 |
| C2 | 80 | 15% | 12.00 |
| C3 | 95 | 15% | 14.25 |
| C4 | 50 | 10% | 5.00 |
| C5 | 90 | 15% | 13.50 |
| C6 | 75 | 5% | 3.75 |
| C7 | 100 | 10% | 10.00 |
| C8 | 75 | 5% | 3.75 |
| **Total** | | | **75.00** |

---

## Veredito

**Vencedor:** Chatwoot **75.0 vs 67.5** (delta 7.5, magnitude moderada)

### Racional

Chatwoot vence por **dominio em pricing, canais nativos, sovereignty e AI cost predictability**. Intercom mantem vantagem absoluta em **AI sofisticacao (Fin Apex 1.0), in-app messaging e enterprise polish**.

Trade-off central que define adocao: cliente precisa decidir se Fin AI premium (deflection 51-67% publicado, custom actions, simulation) vale **2-5x do TCO**. Para SMB e mid-market sem regulatorio HIPAA/multibrand, Chatwoot oferece economia substancial. Para SaaS B2B mid-market com in-app heavy + budget definido, Intercom ainda justifica premium.

---

## Sub-veredito por cenario

### Cenario A — SMB (5 agents, ~1.000 conv/mo, 30% deflection target)

| Player | Custo mensal estimado | Verdict |
|---|---:|---|
| Intercom Essential + Fin | **$440-590** | Cobra premium injustificado para volume baixo |
| Chatwoot Cloud Business | **$95** + credits 300 incl + ~$10 extras = **~$105** | **Vencedor — 5-7x mais barato** |
| Chatwoot Self-hosted | **$30-50** infra + $0 license | Vencedor radical se time tem DevOps |

**Verdict SMB:** Chatwoot wins por margem larga. Captain credits 300/mo bastam para volume baixo; canais Telegram/Insta/WhatsApp nativos cobrem caso B2C; in-app messaging premium nao e diferencial pra SMB B2C.

### Cenario B — Mid-market (20 agents, ~5.000 conv/mo, 50% deflection target)

| Player | Custo mensal estimado | Verdict |
|---|---:|---|
| Intercom Advanced + Fin (50% x 5k x $0.99) + Copilot 5 agents | **$1.700 + $2.475 + $145 = $4.320** | TCO alto |
| Intercom + Pro Analytics + Proactive Support | + $99 + $99 = **$4.518** | Caro |
| Chatwoot Business + credits extras (1.000) | **$780 + $20 = $800** | Vencedor 5x mais barato |
| Chatwoot self-hosted + Cloud Captain bridge | **~$200-400** | Mais barato ainda mas exige eng |

**Verdict Mid-market:** Chatwoot wins **mas com caveat AI**. Se ops in-app B2B SaaS com Product Tours/banners polished obrigatorios, Intercom Advanced ainda compete pelo polish. Se ops B2C/e-commerce/WhatsApp-first, Chatwoot domina absoluto. Cenario com tensao real — exige deep dive no caso de uso.

### Cenario C — Scale (50 agents, ~20.000 conv/mo, 60% deflection target)

| Player | Custo mensal estimado | Verdict |
|---|---:|---|
| Intercom Expert + Fin (60% x 20k x $0.99) + Copilot 50 + add-ons | **$6.600 + $11.880 + $1.450 + $200 = $20.130** | TCO proibitivo se Fin nao entrega valor real superior |
| Chatwoot Enterprise + credits extras volume | **$4.950 + ~$1.000-2.000 = $6.000-7.000** | 3x menos custoso |
| Chatwoot Self-hosted + Cloud bridge para Captain | **$200-500 infra + Captain bridge** | Pode ser <$2.000/mo total |

**Verdict Scale:** Chatwoot self-hosted vence absoluto se time tem DevOps maturity. Cloud Enterprise tambem vence vs Intercom Expert. Intercom Expert so justifica em narrow case: SaaS enterprise B2B regulado (HIPAA + multibrand + ISO obrigatorios) que exige cert out-of-box. **Per-resolution Fin vira proibitivo em volume alto** — $11.880/mo so em AI vs $1.000-2.000 Chatwoot credits.

---

## Tensao critica que define vitoria

A unica dimensao que ainda pode reverter a vitoria de Chatwoot e **C1 (AI deflection performance)** se demonstrado em producao real para um caso especifico.

**Se Captain entrega 30% e Fin entrega 60% para o caso de uso do cliente:** TCO de Intercom pode ainda valer pena pelo deflection real entregue (math: $11.880/mo Fin entrega 12k resolucoes; $1.000 Chatwoot credits entregam 6k acoes mas com taxa real menor — diferenca pode justificar premium para certas ops).

**Se Captain entrega 40-50% e Fin entrega 55%:** Chatwoot wins em ROI absoluto pelo gap de pricing.

**Recomendacao:** Antes de adocao em volume, rodar piloto 30 dias em ambos para medir deflection real para o caso especifico. NAO confiar apenas em scores publicados (vendor-side).

---

## Confidence ponderada

| Dimensao | Confidence |
|---|---|
| C1 AI deflection | High em Intercom (multiple sources cite 51%); **Medium** em Chatwoot (vendor nao publica) |
| C2 AI pricing | High em ambos (pricing pages oficiais) |
| C3 Channels | High em ambos (docs oficiais + GitHub) |
| C4 In-app | High (consenso G2 + design history) |
| C5 TCO | High (calculo direto a partir de pricing oficial; ver deep/pricing-tco.md) |
| C6 Community | High |
| C7 Self-hosted | High (binario: existe ou nao) |
| C8 TTV | High |

**Overall confidence:** High em scores estruturais; **Medium em scores comparativos de AI deflection real** porque Chatwoot Captain nunca foi benchmarked em terceiros independentes.
