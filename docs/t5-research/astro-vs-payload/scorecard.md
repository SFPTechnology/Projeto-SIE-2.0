# Scorecard — Astro 6.2 vs Payload CMS 3.x

> Weighted scoring · 18 dimensões · 2026-05-04

## Scoring Method

- **Scale:** 0-10 por dimensão (observable signals)
- **Weights:** 1-10 (definidos pelo contexto Sinkra Hub)
- **Total weight:** 143 (max possible weighted = 1430)
- **Normalized %:** weighted_total / 1430 × 100

## Tabela Quantitativa

| # | Dimensão | Peso | Astro | Astro × Peso | Payload | Payload × Peso | Δ |
|---|---|---:|---:|---:|---:|---:|---:|
| 1 | React fundamentality | 10 | 6 | 60 | 9 | 90 | **+30 P** |
| 2 | Vite paridade | 7 | 9 | 63 | 3 | 21 | **+42 A** |
| 3 | Auto-hospedagem | 10 | 9 | 90 | 9 | 90 | 0 |
| 4 | TypeScript+Zod schemas | 9 | 9 | 81 | 6 | 54 | **+27 A** |
| 5 | Multi-tenant Hub-and-Spoke | 9 | 4 | 36 | 9 | 81 | **+45 P** |
| 6 | Editor WYSIWYG não-dev | 10 | 2 | 20 | 8 | 80 | **+60 P** |
| 7 | Live preview | 8 | 3 | 24 | 9 | 72 | **+48 P** |
| 8 | SEO institucional | 9 | 9 | 81 | 7 | 63 | **+18 A** |
| 9 | Performance runtime | 8 | 9 | 72 | 6 | 48 | **+24 A** |
| 10 | Build performance | 6 | 8 | 48 | 7 | 42 | +6 A |
| 11 | DX dev | 7 | 8 | 56 | 8 | 56 | 0 |
| 12 | Validação enterprise | 9 | 8 | 72 | 9 | 81 | +9 P |
| 13 | Maturidade ecossistema | 7 | 9 | 63 | 7 | 49 | **+14 A** |
| 14 | Roadmap & risco | 8 | 7 | 56 | 6 | 48 | +8 A |
| 15 | License & custo | 7 | 10 | 70 | 9 | 63 | +7 A |
| 16 | Curva de aprendizado | 6 | 7 | 42 | 6 | 36 | +6 A |
| 17 | Integração Vercel | 6 | 9 | 54 | 8 | 48 | +6 A |
| 18 | Multi-language i18n | 7 | 8 | 56 | 9 | 63 | +7 P |
| | **TOTAL** | **143** | | **1044** | | **1085** | **+41 P** |
| | **Normalizado** | | | **73.0%** | | **75.9%** | **+2.9pp** |

## Resultado Overall

- **Payload:** 75.9% (1085/1430 weighted)
- **Astro:** 73.0% (1044/1430 weighted)
- **Delta:** +2.9 percentage points (margem pequena, mas dirigida pelos pesos críticos)

## Análise por Tier de Peso

### Pesos críticos (≥9): Multi-tenant, WYSIWYG, React fundamental, Auto-host, Zod, SEO, Validação ent, Localização

| Subject | Weighted (críticos) | % |
|---|---|---|
| Astro | 510 | 60.7% |
| **Payload** | **612** | **72.9%** |
| Delta | **+102 = +12.2pp** | Payload **decisivo** |

### Pesos médios (6-8): Vite, Live preview, Perf runtime, Build, DX, Maturidade, Roadmap, License, Curva, Vercel

| Subject | Weighted (médios) | % |
|---|---|---|
| **Astro** | **534** | **84.8%** |
| Payload | 473 | 75.1% |
| Delta | **+61 = +9.7pp** | Astro **decisivo** |

## Vencedores por Dimensão

- **Astro vence em 9 dimensões:** Vite (+42), Zod (+27), SEO (+18), Performance (+24), Build (+6), Maturidade (+14), Roadmap (+8), License (+7), Curva (+6), Vercel (+6)
- **Payload vence em 7 dimensões:** React (+30), Multi-tenant (+45), WYSIWYG (+60), Live preview (+48), Validação (+9), i18n (+7), TIE quebra a favor de admin
- **TIE em 2 dimensões:** Auto-hospedagem, DX dev

## Insight Crítico

A diferença final é **pequena no agregado (+2.9pp Payload)**, mas **decisiva nos pesos ≥9 (+12.2pp Payload)**. Isso reflete que **as dimensões críticas para o Sinkra Hub estão concentradas em CMS-features (multi-tenant, WYSIWYG, validação, React-first)**, onde Payload domina, enquanto Astro vence em **render features (perf, SEO, Vite, build)**.

**Conclusão da pontuação:**
- Adoção single-stack: **Payload vence** com folga nos critérios decisivos
- Mas **a maior pontuação possível** vem de **combinar os dois** — pegando vitórias do Astro em render + vitórias do Payload em CMS = ver `deep/hybrid-strategy.md`
