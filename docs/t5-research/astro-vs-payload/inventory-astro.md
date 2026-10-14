# Inventory — Astro 6.2.2

> Data: 2026-05-04 · Snapshot técnico

## Versioning
- **Stable:** `astro@6.2.2` (2026-05-04) [HIGH]
- **Astro 6.0 GA:** 2026-03-10 [HIGH]
- **Astro 7.0.0-alpha.0:** 2026-04-30 (Vite 8 + Rust compiler default)
- **Cadence:** 113 releases em 2025; minor a cada 6-8 semanas

## Core Architecture
- **Runtime:** Vite 7.x (Astro 7 alpha = Vite 8 + Rolldown)
- **Rust compiler:** experimental em 6.x, default em 7.0
- **Server Islands:** GA (sem flag); props serializáveis (number/string/Array/Map/Set/RegExp/Date/BigInt/URL); POST fallback >2KB
- **Live Content Collections:** GA em 6.0 (era experimental em 5.10)
- **View Transitions:** API browser (Chromium) + `<ClientRouter />` fallback

## Output Modes
- Static (default) / SSR / Hybrid (per-route `prerender`)
- **Adapters oficiais:** `@astrojs/node`, `@astrojs/vercel`, `@astrojs/netlify`, `@astrojs/cloudflare`
- **ISR:** Vercel + Netlify; **Edge:** Vercel Edge + Cloudflare Workers (workerd)

## Content Layer
- **Content Collections:** estável desde Astro 2.0 (jan/2023); Content Layer API mandatory em v6
- **Loaders built-in:** `glob()` (MD/MDX/Markdoc/JSON/YAML/TOML), `file()`
- **Custom loaders:** npm-publishable
- **Zod:** v4, importado de `astro/zod`

## Performance
- **CWV pass rate (HTTP Archive):** Astro >50% (único framework acima do limiar) [MEDIA]
- **vs Next.js:** ~40% faster page load, ~90% less JS shipped, LCP 40-70% melhor vs Next SSG
- **Queued Rendering (6.0 experimental):** "up to 2x faster rendering"

## Ecosystem
- **npm DL/week:** ~1.25M [HIGH]
- **GitHub stars:** ~58k (2026), +7k em 2025
- **Stack Overflow 2025:** 4º framework mais admirado (62.2%)
- **Integrations oficiais (15):** react, vue, svelte, solid-js, preact, alpinejs, mdx, markdoc, sitemap, partytown, db, vercel, netlify, cloudflare, node
- **Starlight (docs theme):** 7.6k stars, 50 community plugins, 10k+ projects

## Production Users
- Cloudflare (docs), Google (Firebase docs), Microsoft, Netlify, OpenAI, WPEngine, Mux, Webflow, The Guardian Engineering, NordVPN, eBay Kleinanzeigen, StackBlitz, Trivago, IKEA — **30k+ teams em produção**

## Pricing & License
- **License:** MIT (preservada pós-Cloudflare)
- **Astro Studio:** DESCONTINUADO (bases deletadas pós 2025-03-01)
- **Astro DB:** mantido OSS, Turso recomendado
- **Self-host mínimo:** Node 22.12.0+ + adapter

## React Integration
- **`@astrojs/react`:** v5.0.4
- **React 19:** suportado (Astro Actions integra `useActionState`)
- **RSC:** **NÃO** suportado nativamente (Astro tem próprio modelo de Islands)
- **Hydration directives:** `client:load`, `client:idle`, `client:visible`, `client:media`, `client:only`, `server:defer`
- **Container API:** experimental (render fora de Astro)

## SEO Out-of-the-Box
- `@astrojs/sitemap`: i18n hreflang, canonical, custom filters
- `astro:assets`: AVIF/WebP/PNG/JPEG, lazy, fetchpriority, srcset, no-upscale (default v6)
- **i18n routing:** built-in com `redirectToDefaultLocale: false` (default v6)
- **Built-in Fonts API (6.0):** auto-host Google Fonts/fontsource/custom
- **CSP API (6.0):** Content Security Policy nativo

## CMS / WYSIWYG
- **Astro NÃO é CMS.** Integrações oficiais:
  - **Storyblok** (Official CMS Partner, real-time visual editing)
  - **Sanity** (`sanity-astro` oficial, Visual Editing overlays)
  - **Keystatic** (Git-native, melhor DX para Astro)
  - **TinaCMS** (visual editing inline)
- **Visual Editing nativo Astro:** NÃO existe — depende do CMS

## Multi-site / Multi-tenant
- **Sem suporte built-in.** Padrões: múltiplos builds + monorepo, `site` config per env, middleware host-detection (SSR), Content Layer custom

## Deploy Story
- **Vercel:** oficial hosting partner; ISR, Edge, Vercel Image API, skew protection, Web Analytics
- **Build time:** ~30-90s para 100 páginas static (CI cold) [LOW]
- **Runtime cost:** static = $0 hosting (CDN); SSR = serverless invocations padrão

## Risks & Roadmap
- **Cloudflare aquisição confirmada** 2026-01-16; MIT preservada
- **Risco:** alinhamento Cloudflare-first vs outros adapters longo prazo
- **Vite 8 + Rolldown:** RC 2026-01-21; Astro 7 dependência
- **Roadmap:** Astro 7 GA, Live Collections expansion, CSP first-class, Route Caching stable, Queued Rendering stable

## Sources
- https://astro.build/blog/astro-620/
- https://astro.build/blog/astro-6/
- https://docs.astro.build/en/guides/upgrade-to/v6/
- https://docs.astro.build/en/guides/server-islands/
- https://blog.cloudflare.com/astro-joins-cloudflare/
- https://astro.build/blog/goodbye-astro-studio/
- https://astro.build/blog/year-in-review-2025/
- https://npmtrends.com/astro
- https://astro.build/showcase/
