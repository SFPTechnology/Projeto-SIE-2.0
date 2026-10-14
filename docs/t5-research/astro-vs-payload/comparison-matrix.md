# Comparison Matrix — Astro 6.2 vs Payload CMS 3.x

> Side-by-side comparativo · 18 dimensões · 2026-05-04

## Top-line

| Atributo | Astro 6.2.2 | Payload CMS 3.84.1 |
|---|---|---|
| Categoria | Static-first SSG + Server Islands + Content Collections | Headless CMS + Next.js-native admin + Local API |
| License | MIT | MIT |
| Owner | Cloudflare (acquired 2026-01-16) | Figma (acquired 2025-06) |
| Stars | ~58k | ~40.8k |
| DL/week | ~1.25M | ~150k |
| Stack mínimo | Node 22.12+ + adapter | Node 20+ + Next.js 15+ + Postgres/Mongo/SQLite |
| Render principal | HTML estático + Islands hydratadas | Next.js App Router (SSR/SSG/ISR) |
| Identidade React | Islands (componentes opt-in) | Admin RSC + Local API React-first |

## Matriz Side-by-Side (18 dimensões)

| # | Dimensão | Astro 6.2 | Payload 3.x | Vencedor |
|---|---|---|---|---|
| 1 | **React fundamentality** | Islands (R19 OK, sem RSC) | Admin RSC + Local API React-first; Next.js obrigatório | **Payload** |
| 2 | **Vite paridade** | Vite 7 (Vite 8 + Rolldown em alpha) | Next.js + Turbopack (não-Vite) | **Astro** |
| 3 | **Auto-hospedagem** | MIT, Studio descontinuado mas Astro DB OSS via Turso | MIT, Cloud paused (Figma acq) mas self-host total | TIE |
| 4 | **TypeScript+Zod schemas** | **Zod nativo v4** em Content Collections (`astro/zod`) | Sem Zod nativo; bridge `ts-to-zod` sobre `payload-types.ts` | **Astro** |
| 5 | **Multi-tenant Hub-and-Spoke** | Sem suporte built-in (multi-build / monorepo / middleware host-detection) | **Plugin oficial `plugin-multi-tenant`** GA jan/2025 (tenant field, RBAC per tenant, cleanup) | **Payload** |
| 6 | **Editor WYSIWYG não-dev** | NÃO é CMS (depende Storyblok/Sanity/Keystatic/Tina) | **Live Preview iframe + Layout Builder + Lexical embutido** | **Payload** |
| 7 | **Live preview** | Depende CMS (Sanity/Storyblok têm; Astro não) | **postMessage nativo + `useLivePreview`** | **Payload** |
| 8 | **SEO institucional** | **CWV >50% pass (HTTP Archive)**, sitemap+i18n+image nativos, CSP API, Fonts API auto-host | `plugin-seo` (meta+SERP preview), JSON-LD via custom, sitemap não built-in (Next.js `sitemap.ts`); Localization native | **Astro** |
| 9 | **Performance runtime** | Zero JS por default; ~90% menos JS que Next.js; LCP 40-70% melhor vs Next SSG | Next.js baseline; Local API rápido; cold start serverless é caveat | **Astro** |
| 10 | **Build performance** | Vite 7 (Vite 8/Rolldown em 7-alpha = 10-30x faster Rollup) | Turbopack default (`--turbo` em v3.28+); admin caching v3.81 | Astro (slight) |
| 11 | **DX dev** | HMR rápido, error msgs OK, sintaxe `.astro` curva inicial | Local API DX excelente; Next.js conhecido pelo time React | TIE |
| 12 | **Validação enterprise** | Cloudflare/Google/Microsoft/Netlify/OpenAI docs, IKEA, Trivago, eBay, The Guardian — 30k+ teams | **Microsoft, Disney, Bugatti, ASICS (26k+/25 idiomas), Blue Origin, Sonos, Accenture, Salesforce, Kong, US Air Force** | Payload (slight) |
| 13 | **Maturidade ecossistema** | 1.25M DL/week, 58k stars, 15 integrations oficiais, Starlight 7.6k stars | 150k DL/week, 40.8k stars, 11+ plugins oficiais (mcp recém-GA), Payload Market | **Astro** |
| 14 | **Roadmap & risco** | Cloudflare acq (MIT preserved), Vite 8 dependency, Astro 7 GA roadmap claro | Figma acq + Cloud paused; sem roadmap público formal pós-aquisição; sinais AI-native + Figma integration | Astro (slight) |
| 15 | **License & custo** | MIT; static = $0 hosting; SSR = serverless padrão | MIT; precisa Postgres + Node persistente (custo operacional maior) | **Astro** |
| 16 | **Curva de aprendizado** | Sintaxe `.astro` + Islands mental model | Payload fields + Next.js + Drizzle/Mongoose schemas | Astro (slight) |
| 17 | **Integração Vercel** | Oficial hosting partner; ISR, Edge, Image API, skew protection | Next.js direto + `db-vercel-postgres`; cold start caveat conhecido | Astro (slight) |
| 18 | **Multi-language i18n** | Built-in routing + hreflang via `@astrojs/sitemap` (default v6) | Localization plugin native — ASICS roda 25 idiomas em produção | Payload (slight) |

## Equivalence Levels (3-tier)

| Aspecto | Equivalência | Justificativa |
|---|---|---|
| Content modeling | **Parcial** (3/5) | Astro = Zod build-time; Payload = Fields runtime + admin |
| API surface | **Sem equivalente** (1/5) | Astro = build artifacts + endpoints; Payload = REST/GraphQL/Local |
| Admin UI | **Sem equivalente** (1/5) | Astro não tem admin; Payload é admin-first |
| Renderer | **Sem equivalente** (1/5) | Astro é renderer; Payload depende de Next.js |
| Multi-site | **Parcial** (3/5) | Astro = multi-build pattern; Payload = multi-tenant plugin |
| SEO | **Parcial alta** (4/5) | Astro entrega out-of-box mais; Payload via plugin |
| WYSIWYG | **Sem equivalente** (1/5) | Astro = nenhum; Payload = Live Preview + Lexical |

## Verdict-by-Dimension Summary

- **Astro vence em 8 dimensões:** Vite paridade, TS+Zod, SEO, Performance runtime, Build performance, Maturidade ecossistema, License & custo, Curva de aprendizado, Integração Vercel
- **Payload vence em 7 dimensões:** React fundamentality, Multi-tenant, WYSIWYG, Live preview, Validação enterprise, Roadmap (slight), Multi-language i18n
- **TIE em 3 dimensões:** Auto-hospedagem, DX dev, (mais variabilidade)

**Insight crítico:** Vitórias do Astro estão concentradas em **render/perf/SEO**; vitórias do Payload em **content management/multi-tenant/admin**. **São complementares, não concorrentes diretos**. Hybrid Strategy é candidata natural — ver `deep/hybrid-strategy.md`.
