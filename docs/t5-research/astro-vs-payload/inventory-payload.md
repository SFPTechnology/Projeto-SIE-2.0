# Inventory — Payload CMS 3.84.1

> Data: 2026-05-04 · Snapshot técnico

## Versioning
- **Stable:** `payload@3.84.1` (2026-04-23) [HIGH]
- **Payload 3.0 GA:** 2024-11-19
- **Payload 4 alpha/beta:** sem alpha pública
- **Cadence:** ~1 minor/semana (3.78 → 3.84 em 8 semanas); patches dentro de dias
- **Recent:** v3.83 — `definePlugin`, UUIDv7, profiling; v3.81 — LLM eval suite, admin caching; v3.79 — Lexical 0.41

## Core Architecture
- **Next.js coupling:** v15+ obrigatório; admin + HTTP layer em Next.js App Router
- **Standalone outside Next.js:** Local API only (scripts, separate backend, Remix/SvelteKit/Nuxt frontends consumindo Local API)
- **APIs:** Local API (in-process, sem HTTP) > REST > GraphQL — todas auto-geradas
- **DB drivers:**
  - `@payloadcms/db-postgres` (Drizzle, recomendado prod)
  - `@payloadcms/db-vercel-postgres` (Vercel-optimized)
  - `@payloadcms/db-sqlite` (Drizzle + libSQL)
  - `@payloadcms/db-mongodb` (Mongoose)
- **Admin UI:** React 19 RSC; Turbopack via `--turbo` (default desde v3.28)
- **Lexical:** rich-text default (substituiu Slate); plugins extensíveis

## Content Modeling
- **Collections / Globals / Fields** (text, number, select, relationship, array, blocks, upload, RichText, JSON, code, date, point, group, tabs, row, collapsible, UI)
- **TypeScript types:** `payload generate:types` → `payload-types.ts`
- **Zod nativo:** **NÃO**. Bridge community = `ts-to-zod` sobre `payload-types.ts`
- **Migrations:** `payload migrate:create`/`migrate`; Drizzle gera SQL diff (Postgres/SQLite); Mongoose script-based

## Multi-Tenant
- **Plugin oficial `@payloadcms/plugin-multi-tenant`:** GA jan/2025
- **Features:** `tenant` field auto, admin scoped, cleanup-on-delete, multi-tenant users com roles per tenant, global admins
- **Access control:** RBAC per tenant + global; query constraints automatic filter
- **Hub-and-Spoke fit:** Adequado — tenant = business; UI admin é única (sem subdomain auto); isolamento físico DB exige custom

## WYSIWYG / Editor
- **Live Preview:** iframe + `window.postMessage` nativo; hooks `useLivePreview` (client) + server-side roundtrip
- **Layout Builder:** Blocks field — fields tipados, drag-drop reorder, render server-side via `RenderBlocks`
- **Lexical features:** headings, lists, quote, link (internal/external), upload/media, table, HR, blocks inline + block-level, slash menu, floating toolbar
- **Tiptap/BlockNote:** não nativos; Lexical é canonical

## Performance
- **Local API:** sem HTTP overhead — ideal em RSC
- **GraphQL benchmark:** Payload superou Directus/Strapi em mega-menu query via DataLoader
- **Cold start serverless:** problemático em Vercel (designed for persistent Node)
- **Bundle admin:** sem número público; recomendação importar paths específicos de `@payloadcms/ui`

## Production Users
- **Confirmados oficial:** Microsoft, Disney, Bugatti, Accenture, Salesforce, **ASICS (26.000+ users/year, 25 idiomas)**, Kong, U.S. Air Force, SONOS, Blue Origin (Club for the Future)

## Pricing & License
- **License:** MIT (free self-host forever)
- **Payload Cloud:** **PAUSED** para new sign-ups pós-Figma; self-host inafetado
- **Self-host stack:** Node 20+, Postgres/Mongo/SQLite, S3-compat (opcional), reverse proxy
- **Figma acquisition:** jun/2025; core team integrou Figma

## Ecosystem
- **GitHub stars:** ~40.8k (mai/2026)
- **YoY star growth:** "+197%" não verificado oficialmente [LOW]
- **npm DL/week:** ~105-200k (variação fontes); 5M+ cumulative
- **Plugins oficiais:** form-builder, seo, search, redirects, nested-docs, cloud-storage, multi-tenant, stripe, sentry, import-export, **mcp** (AI agents, recém-GA)
- **Community:** payload-plugin-lexical, payload-tenancy (alt), payload-visual-editor (pemedia), sitemap (ainsleyclark), Payload Market

## SEO
- **`@payloadcms/plugin-seo`:** meta group (title, desc, image), preview SERP real-time, character counters, custom functions auto-gen
- **JSON-LD:** custom field config (não built-in)
- **Sitemap:** não embutido; padrão Next.js `sitemap.ts` + Local API; community `payload-sitemap-plugin`
- **Localization:** native via `localization` config; SEO plugin suporta `alternates` per locale

## React / Next.js
- **Next.js v15+ obrigatório**; v15.5+ OK; v16 suportado
- **React 19:** suportado; issue #14593 (RSC serialization em nested array) — pode estar resolvido
- **Router:** App Router only
- **Server Components:** Local API ideal; admin já é RSC
- **ISR/Cache:** `revalidatePath`/`revalidateTag` em afterChange hooks; v3.81 adicionou admin caching

## API Surface
- REST `/api/{collection}`, GraphQL `/api/graphql-playground`, Local API `payload.find/create/update/delete`
- **Hooks:** Collection (15+), Field-level, Global

## Auth & Access
- **Strategies:** Local, JWT, HTTP-only cookies, API Keys, OAuth 2.0/SAML, custom
- **Enterprise SSO:** Azure ID, Okta, Google (Enterprise plan)
- **2FA:** não built-in (custom strategy)
- **RBAC:** Collection + Field + Document level; function-based access

## Deploy Story
- **Vercel:** Next.js direto; `db-vercel-postgres` otimizado; cold start é caveat
- **Postgres:** Supabase compatible
- **Self-host recommended:** Docker standalone + Nginx + S3 + persistent Node
- **Cloudflare Workers:** suportado (release dedicado)
- **Env vars:** `DATABASE_URI`, `PAYLOAD_SECRET`, provider-specific

## Risks
- **Figma acquisition:** Cloud paused = self-host obrigatório curto/médio prazo; roadmap formal sem ETA pública
- **CVE-2026-25544:** SQL Injection em Drizzle JSON/RichText (Postgres/SQLite), affects < v3.73.0; patch existe — staying current obrigatório
- **Next.js lock-in:** HTTP layer + admin acoplados; mitigação parcial via Local API
- **Migrations breaking:** push vs migrations não mistura; v3 → v4 não anunciado
- **Roadmap:** sinais → plugin-mcp GA (AI agents), LLM eval suite (v3.81), profiling. Direção provável: integration Figma + AI-native CMS

## Sources
- https://github.com/payloadcms/payload/releases
- https://payloadcms.com/posts/blog/payload-30-the-first-cms-that-installs-directly-into-any-nextjs-app
- https://www.figma.com/blog/payload-joins-figma/
- https://payloadcms.com/docs/plugins/multi-tenant
- https://payloadcms.com/docs/local-api/outside-nextjs
- https://payloadcms.com/docs/database/overview
- https://payloadcms.com/docs/rich-text/overview
- https://payloadcms.com/docs/live-preview/overview
- https://payloadcms.com/case-studies
- https://payloadcms.com/docs/plugins/seo
- https://payloadcms.com/docs/access-control/overview
- https://advisories.gitlab.com/pkg/npm/@payloadcms/drizzle/CVE-2026-25544/
- https://payloadcms.com/posts/guides/setting-up-payload-with-supabase-for-your-nextjs-app-a-step-by-step-guide
- https://blog.cloudflare.com/payload-cms-workers/
