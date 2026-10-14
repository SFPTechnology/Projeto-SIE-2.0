# Deep Dive — Cost of Switching

> Custo real de migração entre stacks · 2026-05-04

## Premissa

Cada decisão de stack carrega um **switching cost** se 12 meses depois descobrimos que escolhemos errado. Esta análise mede o custo real de migração entre as 3 opções.

## Switching Costs (12-month horizon)

### A → B: Astro single → Payload single

| Item migrado | Custo |
|---|---|
| Conteúdo Markdown/MDX → Payload Collections (Postgres) | XL (~2-3 semanas) — script ETL + schema mapping |
| Templates Astro → React components Next.js | L (~1 semana) — reescrita de `.astro` para `.tsx` |
| Setup admin Payload + multi-tenant | L (~3 dias) — partindo do zero |
| Build pipeline (CI/CD) | M (~1 dia) — re-config Vercel |
| Time learning curve Payload | M (~1 semana) ramp-up |
| **TOTAL** | **~5-6 semanas (XL+)** |

**Drag adicional:** Site fica fora-do-ar ou em paralelo durante migração. Marketing não-dev precisa retraining.

### A → B: Astro single → Hybrid

| Item migrado | Custo |
|---|---|
| Manter conteúdo Markdown como source-of-truth temporário | $0 |
| Adicionar Payload `apps/cms` + multi-tenant | L (~3 dias) |
| Migrar conteúdo MD → Payload collections (script) | M (~2 dias) |
| Astro endpoints consumindo Payload (REST) | M (~1 dia) |
| Type sharing `@sinkra/cms-types` | M (~1 dia) |
| **TOTAL** | **~1.5-2 semanas (L)** |

**Drag adicional:** Mínimo — sites continuam servindo conteúdo durante transição. Paralelo possível.

### B → A: Payload single → Astro single

| Item migrado | Custo |
|---|---|
| Export collections Postgres → Markdown/MDX em git | L (~3 dias) — script Payload Local API + git import |
| Reescrever Next.js render → Astro pages | L (~1 semana) |
| Re-implementar admin (não há — só dev edita) | **Bloqueante** — marketing não-dev fica sem ferramenta |
| Decommission Payload + Postgres | M (~1 dia) |
| **TOTAL** | **~2 semanas + bloqueio organizacional** |

**Drag adicional:** **Não viável** se marketing não-dev depende do CMS. Switching cost real = "perder produto" + custo política/cultural.

### B → A: Payload single → Hybrid

| Item migrado | Custo |
|---|---|
| Manter Payload (zero migration) | $0 |
| Adicionar `apps/site-{business}` Astro consumindo Payload | M (~2 dias por business) |
| Type sharing | M (~1 dia) |
| Live preview cross-app | M (~2 dias) |
| **TOTAL** | **~1.5 semanas (M+)** |

**Drag adicional:** Mínimo. Payload existing fica intacto.

### Hybrid → Single (downgrade)

Caso 12 meses depois decidirmos que hybrid é overengineered:

| De Hybrid → | Para Payload single | Para Astro single |
|---|---|---|
| Custo | Drop apps/site-{business} | **Não viável** (marketing fica sem CMS) |
| Effort | M (~1 semana cleanup) | XL (~3-4 semanas + bloqueio cultural) |

## Switching Cost Matrix

| De \ Para | Astro single | Payload single | Hybrid |
|---|---|---|---|
| **Astro single** | — | XL (5-6w) | L (1.5-2w) |
| **Payload single** | Bloqueado | — | M+ (1.5w) |
| **Hybrid** | Bloqueado | M (1w cleanup) | — |

## Insights

### 1. **Hybrid é a opção mais flexível**
- De Hybrid → Payload single: M (1 semana cleanup)
- De Hybrid → Astro single: bloqueado (ok, mas raro caso)
- Hybrid mantém **opções abertas**. Single-stack não.

### 2. **Astro single é a opção mais cara para sair**
- A → B (Payload): XL (5-6 semanas)
- A → Hybrid: L (1.5-2 semanas)
- Astro single tem maior **lock-in cultural** (ninguém quer voltar para "sem CMS")

### 3. **Payload single → Hybrid é o caminho natural**
- Custo M+ (~1.5 semanas)
- Sem bloqueios culturais
- Pode ser feito 1 business por vez

### 4. **A pior decisão é Astro single em multi-tenant + marketing não-dev**
- Switching cost para sair = XL
- Bloqueio cultural se marketing depender do site
- Score baixo nas dimensões críticas (60.7% em pesos ≥9)

## Recomendação Estratégica de Path

**Path recomendado para minimizar switching cost ao longo de 12-24 meses:**

```
T+0:   Payload single (1 business spike) ─────┐
T+1m:  Payload single (4 businesses + multi-tenant)
T+3m:  Adicionar Astro renderer (1 business) ─┼─→ Hybrid pilot
T+6m:  Hybrid completo (4 businesses)         ─┘
T+12m: Avaliar — manter Hybrid ou simplificar?
```

**Por quê:** Começar Payload single garante baseline funcionando. Adicionar Astro depois é incremental (M+ effort), não disruptivo. Se em T+12m descobrirmos que Astro renderer não trouxe gain mensurável em CWV, drop para Payload single (M cleanup, sem bloqueio).

## Anti-paths

❌ **Spike-implement-discard** — começar Astro single, ver que falha, jogar fora e começar Payload do zero. Custo XL desperdiçado.

❌ **Big-bang Hybrid** — pular Payload single e ir direto para Hybrid em 4 businesses simultâneos. Risco de drift entre componentes não testados.

❌ **2-track parallel** — manter Astro + criar Payload em paralelo "para comparar". Dilui foco; ninguém acaba uma das tracks; switching cost dobrado.

## Final Take

Switching cost favorece **Payload single como ponto de partida**, com **Hybrid como destino** ao longo de 6 meses. Isso minimiza:
- **Switching cost forward:** ~M+ por adição de Astro
- **Switching cost reverse:** ~M se Hybrid for overengineered
- **Bloqueios culturais:** zero (marketing tem CMS desde dia 1)
- **Risco técnico:** validado por business antes de roll-out
