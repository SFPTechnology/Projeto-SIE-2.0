# Battle Card — Astro vs Payload

> Quick comparison · 1-page · 2026-05-04

## TL;DR (Sinkra Hub Context)

**Single-stack winner:** **Payload 3** (75.9% vs Astro 73.0%, **+12.2pp em pesos críticos**)
**Best stack:** **Hybrid** — Payload (backend/admin) + Astro (renderer sites institucionais)
**Avoid:** Astro standalone (sem CMS) — quebra para marketing não-dev

## One-Liners

| Subject | Pitch | Best for |
|---|---|---|
| **Astro 6.2** | "Static-first, zero-JS default, Vite-native, melhor SEO institucional do mercado em 2026" | Sites institucionais SEO-critical, blogs, docs, marketing pages onde conteúdo vem de CMS upstream |
| **Payload 3** | "TypeScript-first headless CMS Next.js-native com admin RSC, multi-tenant oficial, Live Preview, validação enterprise" | CMS schema-heavy com 4+ tenants, marketing não-dev editando WYSIWYG, admin app interno |

## Critical Numbers

| Métrica | Astro | Payload |
|---|---|---|
| Versão (mai/2026) | 6.2.2 | 3.84.1 |
| GitHub stars | 58k | 40.8k |
| npm DL/week | 1.25M | 150k |
| CWV pass rate | **>50% (best in class)** | ~25-50% (Next.js baseline) |
| Bundle JS default | **0 KB (estático)** | Next.js baseline |
| Multi-tenant nativo | NÃO | **SIM** (plugin oficial) |
| Live Preview | NÃO (depende CMS) | **SIM** (postMessage nativo) |
| Zod schemas | **NATIVO** v4 | NÃO (bridge ts-to-zod) |
| React 19 | Islands (sem RSC) | **RSC nativo** |
| License | MIT | MIT |
| Owner | Cloudflare (2026-01) | Figma (2025-06) |

## Validação Enterprise

| Subject | Production Users (validados) |
|---|---|
| **Astro** | Cloudflare, Google (Firebase docs), Microsoft, Netlify, OpenAI, IKEA, Trivago, eBay, The Guardian, NordVPN, StackBlitz — 30k+ teams |
| **Payload** | Microsoft, Disney, Bugatti, **ASICS (26k+ users, 25 idiomas em prod)**, Blue Origin, Sonos, Accenture, Salesforce, Kong, US Air Force |

## When Astro Wins

✅ Site institucional puro (≤500 páginas, marketing pages, landing)
✅ SEO crítico (CWV, hreflang, lighthouse scores)
✅ Zero-budget hosting (static = $0)
✅ Time dev tem React 19 mas conteúdo já vem de CMS externo
✅ Bundle JS pequeno é prioridade

## When Payload Wins

✅ Marketing não-dev editando conteúdo via WYSIWYG
✅ Multi-tenant 4+ businesses com RBAC
✅ Schemas content-modeling complexos com relações
✅ Live Preview real (cliente vê edição em tempo real)
✅ Admin app interno completo (auth, CRUD, hooks)
✅ Postgres já no stack (Supabase)

## When Hybrid Wins (Best Score)

✅ **Sinkra Hub default** — Payload entrega WYSIWYG/multi-tenant/admin; Astro entrega SEO/Vite/perf nos sites institucionais por business
✅ Aceita complexidade extra (2 stacks) em troca de **best-of-both**

## When Neither Fits

❌ App SaaS com auth complexo + dashboards realtime → use Next.js puro ou T3 stack
❌ E-commerce com checkout integrado → use Medusa, Shopify Hydrogen
❌ Forum / community → use Discourse, Lemmy

## Key Risks

| Subject | Top Risk |
|---|---|
| Astro | Cloudflare alignment longo prazo (rumor) + Vite 8/Rolldown 1.0 RC dependency cascade |
| Payload | Figma direction pós-acquisition + Cold start Vercel + CVE-2026-25544 (patch obrigatório) |

## Cost of Entry

| Stack | Spike | Pilot | Prod-ready |
|---|---|---|---|
| Astro single | S (~2h) | M (~6h) | L (~2d) |
| Payload single | M (~6h) | L (~2-3d) | XL (~1w) |
| **Hybrid** | M (~6h) | L (~3d) | XL (~1-2w) |

## Decisive Question for Sinkra Hub

> **"Marketing não-dev em 4 businesses precisa editar conteúdo via WYSIWYG?"**
> - **SIM** → Payload (single ou hybrid)
> - **NÃO** (só dev edita MD/MDX) → Astro single + Velite

A resposta para o Sinkra Hub é **SIM** — portanto **Payload é mandatório** (single ou em hybrid).

## Final Recommendation

**Phase 1 (Sprint 1-3):** Payload 3 single-stack em `apps/cms` (Next.js 15.5+ + Supabase Postgres), multi-tenant para 4 businesses. Spike em 1 business primeiro.
**Phase 2 (Sprint 4+):** Avaliar hybrid — adicionar Astro renderer para sites institucionais públicos consumindo Payload via REST/GraphQL. ADR explícito sobre CWV target.
**Phase 3 (Sprint 6+):** Migrar `apps/design` se houver performance gap mensurável vs Astro.
