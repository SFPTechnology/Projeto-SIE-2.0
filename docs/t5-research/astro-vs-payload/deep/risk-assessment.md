# Deep Dive — Risk Assessment

> Top 5 riscos por stack + mitigação concreta · 2026-05-04

## Top 5 Riscos — Astro single

| # | Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|---|
| 1 | **Sem WYSIWYG = marketing não-dev bloqueado** | **Alta (certeza)** | **Crítico** | Não single-stack — combinar com CMS upstream (Payload em hybrid) |
| 2 | **Multi-tenant manual (4 builds)** | Alta | Alto | Usar monorepo + shared components; ou rever decisão para Payload single/hybrid |
| 3 | **Cloudflare alignment longo prazo** | Média | Médio | Acompanhar roadmap; manter stack adapter-agnostic; vendor diversification |
| 4 | **Vite 8 + Rolldown 1.0 RC dependency cascade** | Média | Médio | Pin Astro 6.x até Astro 7 GA estabilizar; validar build determinístico |
| 5 | **Sem REST/GraphQL auto-gen — APIs manuais** | Alta | Médio | Astro endpoints `.ts` + Drizzle; ou consumir Payload (hybrid) |

## Top 5 Riscos — Payload single

| # | Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|---|
| 1 | **Figma direção pós-acquisition (Cloud paused)** | Média | Alto | Self-host obrigatório; manter monitoramento de Payload Cloud replacement; ter plano B (Strapi 5 ou KeystoneJS) |
| 2 | **CVE-2026-25544 (SQL injection Drizzle)** | Alta (já existe) | Crítico | Manter Payload >=v3.73.0; CI scan vulnerabilidades; renovate-bot |
| 3 | **CWV pass rate Next.js (~25-50%) vs Astro (>50%)** | Média | Médio | Disciplina ISR + RSC + next/image; Lighthouse CI budget JS; considerar hybrid |
| 4 | **Cold start serverless Vercel** | Média | Médio | Persistent Node deploy (Railway/Fly/Docker); ou Vercel Pro; medir P95 first-byte |
| 5 | **Next.js lock-in (HTTP layer + admin)** | Baixa | Alto | Local API sobrevive a swap de frontend; ADR documentando coupling |

## Top 5 Riscos — Hybrid (Payload + Astro)

| # | Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|---|
| 1 | **Type drift (payload-types.ts ↔ Zod)** | Alta | Alto | CI gate: regenerate + diff a cada commit; `@sinkra/cms-types` package owner único |
| 2 | **Live preview cross-app complexo** | Média | Médio | iframe Payload aponta URL Astro com signed token JWT; spike no pilot |
| 3 | **2 stacks = 2x curva de aprendizado** | Alta | Médio | Documentação interna + onboarding pair-programming; aceitar período transição |
| 4 | **Auth shared (admin Payload ↔ sites Astro)** | Média | Médio | JWT shared secret + middleware Astro; ou Payload é único auth source |
| 5 | **Drift DX entre 2 projetos no monorepo** | Média | Baixo | Eslint/prettier compartilhados; turbo cache; CI matrix |

## Cross-Stack Riscos Comuns

| Risco | Quem afeta | Mitigação |
|---|---|---|
| **Vendor lock-in via aquisições recentes** | Astro (Cloudflare) + Payload (Figma) | Ambos MIT; OSS forking sempre possível; manter self-host |
| **Roadmap breaking changes** | Astro v6→v7 + Payload v3→v4 | Feature flags + canary deploys; major upgrades em sprint dedicado |
| **Supabase Postgres performance** | Payload backend + Astro Live Collections | Read replicas; PGBouncer; query budgets em CI |

## Risk-Adjusted Score

Aplicando penalty por risk severity (10% deduction por P0 não mitigado):

| Stack | Base Score | P0 não mitigados | Adjusted Score |
|---|---|---|---|
| Astro single | 73.0% | 1 (WYSIWYG) | 65.7% |
| Payload single | 75.9% | 0 (todos mitigáveis) | 75.9% |
| **Hybrid** | **86.5%** | 0 (todos mitigáveis) | **86.5%** |

## Conclusão de Riscos

- **Astro single tem 1 risco P0 não-mitigável** (sem WYSIWYG bloqueia marketing não-dev) → drop como single-stack
- **Payload single tem riscos altos mas todos mitigáveis** → viável com discipline
- **Hybrid tem mais riscos mas todos mitigáveis** → score líquido melhor, vale o investimento

## Risco Existencial Comparado

**O que aconteceria se cada owner descontinuasse hoje?**

| Subject | Owner | Cenário descontinuação | Recovery |
|---|---|---|---|
| Astro | Cloudflare | Fork pela comunidade; Astro tem 30k+ teams + community ativa | Recovery ~6 meses (fork ativo) |
| Payload | Figma | Fork pela comunidade; menor base mas core team técnico fortíssimo | Recovery ~12 meses (mais hard) |

**Mitigação universal:** Ambos OSS MIT — fork é sempre opção. Não há vendor lock-in puro em nenhum dos dois.
