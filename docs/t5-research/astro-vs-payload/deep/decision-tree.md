# Deep Dive — Decision Tree

> Quando cada stack vence · 2026-05-04

## Decision Tree (root: "Quem edita o conteúdo?")

```
Quem edita o conteúdo?
│
├── Apenas dev (Markdown/MDX em git)
│   │
│   ├── Cardinalidade < 10k entries
│   │   └── Astro + Velite + Content Collections (Zod)
│   │       Score esperado: 9.5/10 SEO, $0 hosting
│   │       Adoção: shadcn/ui docs, Linear blog static
│   │
│   └── Cardinalidade ≥ 10k entries (vault, sessions)
│       └── Astro + Live Content Collections + Postgres direto
│           Score esperado: 8.5/10 SEO, $ Postgres
│
├── Marketing/business não-dev (WYSIWYG necessário)
│   │
│   ├── 1 tenant / 1 site
│   │   │
│   │   ├── SEO institucional crítico (CWV > 75)
│   │   │   └── Hybrid: Payload (admin) + Astro (renderer)
│   │   │       Score esperado: 86.5%
│   │   │
│   │   └── SEO não-crítico ou moderado
│   │       └── Payload single (Next.js render)
│   │           Score esperado: 75.9%
│   │
│   └── Multi-tenant 4+ businesses
│       │
│       ├── SEO crítico (caso Sinkra Hub)  ← VOCÊ ESTÁ AQUI
│       │   └── Hybrid: Payload + Astro
│       │       Score esperado: 86.5%
│       │       ADR: AIOX-CMS-001
│       │
│       └── SEO não-crítico
│           └── Payload single + multi-tenant plugin
│               Score esperado: 75.9%
│
└── Misto (dev + não-dev)
    │
    ├── Dev edita schemas/templates; não-dev edita conteúdo
    │   └── Hybrid: Payload + Astro (mesma decisão acima)
    │
    └── Não-dev raramente edita (overrides ocasionais)
        └── Astro + Velite + BlockNote inline para overrides
```

## Sinkra Hub Path

```
Quem edita?  → Marketing/business não-dev
              + Dev (workspace L0–L4 internal)
Tenants?     → 4 businesses Hub-and-Spoke
SEO crítico? → SIM (sites institucionais)
Política?    → Auto-hospedagem total
Stack?       → React 19 + Vite + Postgres + Vercel

  ↓

VEREDICTO: Hybrid (Payload + Astro)
ADR target: AIOX-CMS-001
Score: 86.5%
```

## Cenários Alternativos (sensitivity)

### Cenário A — "Reduzir complexidade aceitando SEO médio"
- Drop SEO obsession → Single-stack Payload
- Trade: -10pp em CWV/SEO mas -50% em manutenção infra
- Quando faz sentido: time pequeno (1-2 devs), prioridade time-to-market

### Cenário B — "Se Vite paridade for inegociável"
- Drop Payload, ficar com Astro + Sanity Studio embeddable (relax auto-host)
- Trade: Content Lake é managed (Sanity SaaS)
- Quando faz sentido: SEO obsession + WYSIWYG obrigatório + permissão para SaaS parcial

### Cenário C — "Se workspace L0–L4 for o único conteúdo"
- Astro + Velite (sem CMS), Markdown em git
- Trade: marketing não-dev fica fora; só dev edita
- Quando faz sentido: time 100% técnico; conteúdo é code-equivalent

### Cenário D — "Se todos os 4 businesses precisarem app fully-custom"
- Next.js puro + Payload Local API + custom render
- Trade: perde SSG benefits do Astro
- Quando faz sentido: cada business tem features custom além de marketing pages

## Decision Matrix por Persona

| Persona | Single Astro | Single Payload | Hybrid | Razão |
|---|---|---|---|---|
| **Dev solo, blog técnico** | ✅ | ❌ | ❌ | Astro+Velite cobre 100%, KISS |
| **Startup B2B 1 site marketing** | ❌ | ✅ | ⚠️ | Payload entrega WYSIWYG; hybrid é overengineering |
| **Mid-market 2-4 sites + admin** | ❌ | ✅ | ✅ | Payload single OK; hybrid se SEO crítico |
| **Enterprise multi-tenant + global** | ❌ | ⚠️ | ✅ | Hybrid é a única que escala em SEO + WYSIWYG |
| **Documentation site** | ✅ | ❌ | ❌ | Astro+Starlight é referência |
| **E-commerce com checkout** | ❌ | ❌ | ❌ | Use Medusa/Shopify Hydrogen |

**Sinkra Hub = "Mid-market multi-tenant com SEO crítico"** → **Hybrid wins**.

## Anti-decisions (não faça)

❌ **"Vou começar single Astro e migrar para Payload depois"** — você cria duas migrações: primeiro de "sem CMS" para "com CMS" (admin novo), depois de "Astro" para "Astro consumindo Payload" (refactor render). Custo total > 2x ir direto para Hybrid.

❌ **"Vou usar Payload no admin e cada business escolhe seu render"** — drift de DX, type sharing quebrado, marketing não-dev confuso entre 4 sites com UX diferentes.

❌ **"Vou usar Sanity self-host (Studio + Content Lake managed) e renderizar com Astro"** — fere política auto-hospedagem total. Sanity Content Lake é vendor lock.

❌ **"Vou usar Strapi 5 (mais stars que Payload)"** — Strapi não tem Live Preview iframe nativo, multi-tenant é manual via lifecycle hooks, Block Editor é Slate pre-1.0. Trade DL/week por ergonomia errada.

❌ **"Vou usar Keystatic (admin React, git-as-code)"** — sem WYSIWYG real (form-based), sem agendamento, risco Thinkmill (arquivou Keystone 5 em mar/2026). Já descartado em research anterior.
