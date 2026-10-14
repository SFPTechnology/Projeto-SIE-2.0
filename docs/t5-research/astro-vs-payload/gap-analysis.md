# Gap Analysis — Astro 6.2 vs Payload CMS 3.x

> Bidirectional gaps · severidade · mitigação · 2026-05-04

## Astro Gaps (o que Payload tem e Astro não)

| ID | Gap | Severidade | Impacto Sinkra Hub | Mitigação |
|---|---|---|---|---|
| AG-01 | **Sem admin UI nativo** — Astro não é CMS | **P0** | Marketing não-dev não pode editar conteúdo sem CMS upstream | Combinar com Storyblok (SaaS — fora política) ou Sanity (Content Lake managed) ou Keystatic (sem WYSIWYG) ou Payload |
| AG-02 | **Sem multi-tenant built-in** | **P0** | 4 businesses Hub-and-Spoke exigem isolation custom | Multi-build pattern + monorepo (1 Astro project per business) — overhead de 4 deploys |
| AG-03 | **Sem Live Preview** | **P0** | Marketing não vê edição em tempo real | Depende do CMS provider (Sanity/Storyblok têm; Payload via integration custom) |
| AG-04 | **Sem RSC nativo** | P1 | Reuso de componentes React 19 com server-side state requer wrapping em Islands | `client:load` directive + state via Astro Actions |
| AG-05 | **Sem REST/GraphQL auto-gerado** | P1 | Não há API CMS pronta; precisa Astro DB + endpoints manuais ou backend separado | Astro endpoints `.ts` + Drizzle/Prisma manual |
| AG-06 | **Sem RBAC granular** | P1 | Time marketing precisa permissões per-business; sem solução nativa | Auth via Lucia/Clerk + middleware custom |
| AG-07 | **Sem hooks (beforeChange/afterRead)** | P2 | Validação custom no save é manual em endpoints | Implementação manual em endpoint handlers |
| AG-08 | **Sem field-level validation runtime** | P2 | Zod cobre Content Collections build-time, mas form submissions runtime são manuais | Zod schemas reuso em endpoints + zod-form-data |
| AG-09 | **Sem auth strategies built-in** (JWT, API Keys, OAuth) | P2 | Self-host requer setup auth completo | Lucia v3, Auth.js, Clerk integration |

## Payload Gaps (o que Astro tem e Payload não)

| ID | Gap | Severidade | Impacto Sinkra Hub | Mitigação |
|---|---|---|---|---|
| PG-01 | **Não roda em Vite — força Next.js** | **P0** | Quebra paridade Vite com `apps/design` | ADR explícito: "React fundamental via Next.js App Router para CMS apps; Vite mantido em apps/design" |
| PG-02 | **Sem Zod nativo nas collections** | **P0** | Schemas `@sinkra/content-schemas` não são reusados diretamente | Bridge `ts-to-zod` + CI gate validando paridade payload-types ↔ Zod |
| PG-03 | **CWV pass rate Next.js (~25-50%) vs Astro (>50%)** | P1 | SEO institucional pior por default | App Router + ISR + Server Components + next/image disciplina; Lighthouse CI budget |
| PG-04 | **Cold start serverless em Vercel** | P1 | First request lenta em produção Vercel | Persistent Node deploy (Railway/Fly/Docker); ou Vercel Pro com pre-warming |
| PG-05 | **Bundle JS admin maior** | P2 | Página admin pesada para usuários remote | Aceitar (admin é interno); manter `--turbo` |
| PG-06 | **Sem Server Islands equivalente** | P2 | Reuso de componentes server-rendered exige RSC discipline | Padrão React Server Components (já maduro) |
| PG-07 | **Sem multi-build standalone** | P2 | Não há padrão "1 build per business + shared components" como Astro | Multi-tenant plugin atende com 1 deploy só |
| PG-08 | **Sem View Transitions API embutida** | P3 | UX transitions menos polida | Implementar via `next/view-transitions` ou React 19 useTransition |
| PG-09 | **Sem CMS-agnostic — admin acoplado** | P3 | Não é "renderer", é CMS+admin completo | Aceitar (essa é a categoria do produto) |

## Gap Severity Legend

- **P0** — Bloqueante, afeta critério não-negociável Sinkra Hub
- **P1** — Significativo, afeta qualidade de vida ou perfil de risco
- **P2** — Mitigável com effort razoável (S-M)
- **P3** — Polimento; não afeta decisão

## Critical-path Analysis

### Para Astro adoção single-stack (sem CMS):
**P0 gaps:** AG-01, AG-02, AG-03 (admin/multi-tenant/live-preview)
**Single-stack viabilidade:** **NÃO viável** sem combinar com CMS upstream. Marketing não-dev fica bloqueado.

### Para Payload adoção single-stack (com Next.js):
**P0 gaps:** PG-01, PG-02 (Vite paridade quebrada, Zod via bridge)
**Single-stack viabilidade:** **Viável** com ADR aceitando trade-offs:
1. Vite paridade limitada a apps/design (já justificável)
2. Zod via bridge ts-to-zod com CI gate

### Para Hybrid Strategy (Payload backend + Astro renderer):
**Cobre AG-01/02/03 via Payload + PG-03/04 via Astro**.
Resta: PG-01 (Vite paridade) — apenas admin é Next.js, render dos sites volta a Vite/Astro.
**Best-of-both** detalhado em `deep/hybrid-strategy.md`.

## Bidirectional Severity Matrix

| Severidade | Astro Gaps | Payload Gaps |
|---|---|---|
| P0 (bloqueantes) | 3 (admin, multi-tenant, live preview) | 2 (Vite paridade, Zod nativo) |
| P1 (significativos) | 3 (RSC, API auto-gen, RBAC) | 2 (CWV, cold start) |
| P2 (mitigáveis) | 3 (hooks, validation runtime, auth) | 3 (admin bundle, server islands, multi-build) |
| P3 (polimento) | 0 | 2 (view transitions, CMS-agnostic) |

**Insight:** Astro tem **mais P0s para uso CMS** (não foi desenhado pra isso). Payload tem **menos P0s mas mais críticos** (Vite paridade + Zod nativo). Hybrid resolve **5 de 5 P0s**.

## Recommended Closure Roadmap

### Se single-stack Payload:
1. **PG-02 (Zod nativo):** EPIC com bridge ts-to-zod + CI gate paridade — Effort M (~6h)
2. **PG-03 (CWV):** Lighthouse CI + budget JS + ISR discipline — Effort L (~2-3d setup)
3. **PG-04 (cold start):** Avaliar Railway/Fly persistent Node ou Vercel Pro — Effort M (~1d)

### Se Hybrid (Payload + Astro):
1. **Bridge Astro → Payload:** Astro endpoints consomem Payload REST/GraphQL — Effort M (~8h)
2. **Type sharing:** `@sinkra/cms-types` package gerado por `payload generate:types` consumido pelo Astro Content Collections com Zod schemas re-derivados — Effort M (~6h)
3. **Live preview cross-app:** iframe Payload aponta para preview Astro com URL signed — Effort L (~2d)
