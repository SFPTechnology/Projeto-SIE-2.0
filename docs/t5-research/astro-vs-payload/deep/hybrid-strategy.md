# Deep Dive — Hybrid Strategy (Payload + Astro)

> Análise da estratégia "Payload backend + Astro renderer" · 2026-05-04

## Source-of-Truth Notice

Este deep dive é **histórico** e só se aplica a uma futura plataforma CMS humana
com admin, WYSIWYG, live preview e marketing não-dev. Ele não governa
`apps/blog-template/`.

Para o template de blog GEO automatizado, a decisão vigente é Astro 6.2 +
Cloudflare Workers + D1 + Drizzle por fork `(business × idioma)`, conforme
ADR-023 a ADR-027.

## Tese

Payload e Astro **não são concorrentes diretos** — são **complementos arquiteturais**. Payload é um **CMS+admin completo** (governance, WYSIWYG, multi-tenant). Astro é um **renderer estático de elite** (SEO, performance, zero-JS). Hybrid Strategy combina os dois extraindo as vitórias de cada um.

## Arquitetura Proposta

```
┌─────────────────────────────────────────────────┐
│ apps/cms (Next.js 15.5+ + Payload 3)           │
│ ─ Admin React 19 RSC                            │
│ ─ Local API + REST + GraphQL                    │
│ ─ multi-tenant plugin (4 businesses)            │
│ ─ Live Preview iframe                           │
│ ─ Lexical rich text                             │
│ ─ Postgres (Supabase)                           │
└─────────────────┬───────────────────────────────┘
                  │ REST/GraphQL/Local API
                  │
       ┌──────────┼──────────┬──────────┬──────────┐
       ▼          ▼          ▼          ▼          ▼
┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐
│ apps/    │ │ apps/    │ │ apps/    │ │ apps/    │
│ site-    │ │ site-    │ │ site-    │ │ site-    │
│ allflu.  │ │ aiox     │ │ academia │ │ bilhon   │
│ (Astro)  │ │ (Astro)  │ │ (Astro)  │ │ (Astro)  │
│ Vite 7   │ │ Vite 7   │ │ Vite 7   │ │ Vite 7   │
│ SSG/ISR  │ │ SSG/ISR  │ │ SSG/ISR  │ │ SSG/ISR  │
└──────────┘ └──────────┘ └──────────┘ └──────────┘
       │
       └─→ Vercel (oficial Astro hosting partner)
           CWV >50% pass · Edge · Image API

apps/design (Vite + React 19) — INALTERADO
       │
       └─→ Reusa @sinkra/cms-types (gerados por Payload)
           para componentes que renderizam conteúdo
```

## Como Funciona

### 1. Content Authoring → Payload
- Marketing não-dev acessa `apps/cms.{business}.com/admin`
- Edita via Lexical + Layout Builder + Live Preview iframe
- Multi-tenant plugin garante isolation entre 4 businesses
- Salva em Postgres (Supabase)

### 2. Content Distribution → REST/GraphQL
- Sites Astro consomem Payload via REST `/api/{collection}` ou GraphQL
- Live Collections (Astro 6.0 GA) buscam request-time quando necessário
- SSG default: build sites a cada commit; ISR para conteúdo mutável

### 3. Render → Astro
- Astro pega payload de Payload, renderiza HTML estático
- Components React 19 onde precisa interatividade (Islands)
- SEO out-of-the-box: sitemap, hreflang, image, CSP, fonts
- Deploy Vercel (oficial partner) ou Cloudflare Pages (post-acquisition)

### 4. Type Sharing → @sinkra/cms-types
- `payload generate:types` gera `payload-types.ts` no Payload
- Package `@sinkra/cms-types` re-exporta + adiciona Zod schemas via `ts-to-zod`
- Astro Content Collections importa schemas Zod do package
- `apps/design` também consome para components

## Tradeoffs Aceitos

| Tradeoff | Impacto | Mitigação |
|---|---|---|
| **2 stacks de framework** (Next.js + Astro) | Mais complexidade, 2 build pipelines | Workspace pnpm com shared packages; CI matrix |
| **2 deploys por business** (cms + site) | Mais infra para gerenciar | Vercel mono-repo deploy; turborepo cache |
| **REST/GraphQL latency** (vs Local API) | Round-trip extra em SSG/ISR | Build-time = 1 fetch por página; runtime = cache CDN |
| **Type sync drift risk** | payload-types.ts ↔ Zod schemas podem dessincronizar | CI gate: regenerate types + Zod cada commit + diff check |
| **Bundle 2x** (Next + Astro deps) | Maior `node_modules` | Aceitar — disco é barato; CI cache resolve |

## Tradeoffs Rejeitados

❌ **Single Astro + Sanity Studio embeddable** — fere auto-hospedagem total (Content Lake é managed)
❌ **Single Payload sem renderer otimizado** — CWV pior, perde 18-24pp em SEO scorecard
❌ **Single Astro sem CMS** — bloqueia marketing não-dev (deal-breaker)
❌ **Dois sistemas independentes (sem type sharing)** — drift garantido, retrabalho

## Effort Estimate

| Phase | Escopo | Effort |
|---|---|---|
| **Spike** | Payload `apps/cms` em 1 business + 1 collection (offerbook) + admin funcional | M (~6h) |
| **Pilot** | + Astro `apps/site-{business}` consumindo Payload via REST + Live Preview cross-app + 1 business completo | L (~2-3d) |
| **Prod-ready** | + 4 businesses + multi-tenant plugin + `@sinkra/cms-types` package + CI gates | XL (~1-2w) |
| **Migration** | + Migrar workspace L0–L4 atual para Payload collections OR manter Velite para layers internos + Payload só para public | XL (~2-3w) |

## Quem Faz Isso na Prática

### ⚠️ Payload + Astro especificamente: SEM cases enterprise verificáveis (mai/2026)

**Casos públicos confirmados (todos personal/agency, NÃO enterprise):**
- **chrislema.com** [HIGH] — blog dinâmico Astro hybrid + Payload + Cloudflare Worker (Chris Lema, ex-Liquid Web/WP)
- **proto.cool** [HIGH] — site pessoal Mike Aparicio; footer "Built with astro & payload"
- **jhb.software** [MEDIA] — agency alemã que mantém o template OSS `jhb-software/payload-astro-website-template` (26 stars)

**Plugins OSS nascentes:**
- `coxmi/astro-payload-plugin` (3 stars, 0 issues, alpha) [LOW]
- `lorenzowijtman/payload-astro` (express bundle) [LOW]

**Payload official case studies** [HIGH] — Microsoft, Disney, ASICS, Bugatti, Blue Origin: **todos rodam Next.js, NÃO Astro**.

**Veredito:** combinação **emergente**. Pattern tecnicamente sólido (Payload Local API + Astro hybrid) mas **ainda não atravessou o chasm** para enterprise.

### "Headless CMS + Astro" (pattern geral) — VALIDADO em enterprise

**Sanity + Astro** (parceria oficial, 18 projetos públicos):
- **UNDP Global Fund for Coral Reefs** (United Nations) [HIGH]
- **Steambase** (Steam analytics) [HIGH]
- **ValorX** (Salesforce SaaS) [HIGH]
- **AmeXio Fuse** (B2B europeu) [HIGH]
- **SCC France** (IT enterprise) [HIGH]

**Storyblok + Astro** (Official CMS Partner):
- **Bejamas × Storyblok Global Financial Starter** [HIGH] — template oficial endossado
- SDK `@storyblok/astro` mantido oficialmente

**Strapi/Contentful/DatoCMS/Hygraph + Astro** [MEDIA] — guides oficiais e tutoriais; sem logos enterprise específicos retornados.

**Astro standalone enterprise** [HIGH]: NASA, Porsche, IKEA, Netlify, Cloudflare docs.

### Implicação para o veredicto Sinkra Hub

A recomendação Hybrid **continua tecnicamente válida**, mas:
- Você seria **early adopter** de Payload+Astro especificamente
- Sem precedente enterprise testado para herdar lições
- Risco de descobrir edge cases não-documentados (live preview cross-app, type sharing)

**Alternativas honestas se quiser pattern Hybrid validado:**

| Alternativa | Trade-off | Score |
|---|---|---|
| **Payload single** (Next.js render) | Aceita CWV ~25-50% baseline; perde Vite paridade total | 75.9% |
| **Sanity + Astro** | **Relax auto-host** (Content Lake managed); ganha cases UNDP/Steambase | ~82% |
| **Storyblok + Astro** | **Relax auto-host** (Storyblok SaaS); ganha Bejamas template oficial | ~82% |
| **Payload + Astro Hybrid** | Auto-host total preservada; **early adopter risk** | 86.5% (teórico) |

## Decision Logic

```
SE (marketing não-dev edita) AND (4 businesses) AND (SEO crítico):
  ENTÃO Hybrid (Payload + Astro)

SENÃO SE (marketing não-dev edita) AND (não preciso CWV top):
  ENTÃO Payload single

SENÃO SE (só dev edita) AND (SEO crítico):
  ENTÃO Astro + Velite single

SENÃO SE (só dev edita) AND (cardinalidade alta):
  ENTÃO Astro + Live Collections + Postgres
```

Para uma futura **plataforma CMS humana** do Sinkra Hub, todas as 3 condições do primeiro ramo podem ser verdadeiras → **Hybrid**.

Para `apps/blog-template/`, essas condições **não** são verdadeiras: não há editor humano não-dev nem WYSIWYG; o fluxo é squad/CLI/API. Logo, este ramo não se aplica ao blog GEO canônico.

## Hybrid Score Estimado

Pegando o **máximo de cada dimensão** (best-of-both achievable):

| Dimensão | Score Hybrid (max(Astro, Payload)) | × Peso |
|---|---|---|
| React fundamentality | 9 (Payload admin RSC) | 90 |
| Vite paridade | 9 (Astro renderer Vite) | 63 |
| Auto-hospedagem | 9 | 90 |
| TS+Zod | 9 (Astro Zod nativo) | 81 |
| Multi-tenant | 9 (Payload plugin) | 81 |
| WYSIWYG | 8 (Payload) | 80 |
| Live preview | 9 (Payload) | 72 |
| SEO | 9 (Astro renderer) | 81 |
| Performance | 9 (Astro) | 72 |
| Build | 8 | 48 |
| DX | 8 | 56 |
| Validação ent | 9 | 81 |
| Maturidade | 9 | 63 |
| Roadmap | 7 | 56 |
| License | 10 | 70 |
| Curva | 6 (mais stacks) | 36 |
| Vercel | 9 | 54 |
| i18n | 9 | 63 |
| **TOTAL** | | **1237 / 1430 = 86.5%** |

**Hybrid Score: 86.5%** — vs Payload single 75.9% e Astro single 73.0%.
**Ganho líquido: +10.6pp vs Payload single, +13.5pp vs Astro single.**

## Risks Específicos do Hybrid

1. **Type drift** entre Payload e Astro — CI gate obrigatório
2. **Live preview cross-app** — iframe Payload → URL Astro com signed token
3. **Auth shared** entre admin Payload e sites Astro — JWT shared secret + middleware
4. **Imagens** — decidir se ficam no Payload (S3-compat) ou Astro (`astro:assets` + CDN)
5. **Curva** — time precisa aprender Payload + Astro (mas ambos têm docs maduros)

## Recomendação Final

**Para CMS humano futuro, adotar Hybrid Strategy como target arquitetural** com **roll-out faseado**:
1. **Sprint 1-2:** Payload single para 1 business (spike + pilot)
2. **Sprint 3-4:** Adicionar Astro renderer para o site público desse business (mantém Payload preview)
3. **Sprint 5-8:** Replicar para os 4 businesses + multi-tenant plugin + type sharing
4. **Sprint 9+:** Migração progressiva de workspace L0–L4 atual

ADR a ser escrito: **"AIOX-CMS-001: Hybrid Headless Architecture (Payload + Astro)"**.
