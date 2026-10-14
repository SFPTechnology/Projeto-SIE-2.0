# Gap Absorption Roadmap — URL Design Extraction

**Date:** 2026-04-27 (update)
**Source:** URL Design Extraction Benchmark (8 competitors)
**Status:** 5 features absorbed / 13 unique-or-better / 7 gaps to close

---

## Recently Absorbed (DONE 2026-04-26 → 2026-04-27)

| # | Feature | Source of inspiration | Effort actual | Status |
|---|---|---|---|---|
| 1 | Drift mode (`--compare`) | designlang `drift` | 3h | ✅ shipped |
| 2 | Quality score A-F (7 categories) | designlang `score` | 2h | ✅ shipped |
| 3 | Token usage count nos swatches | Project Wallace `usage-count` | 30min | ✅ shipped |
| 4 | Breakpoints + dark mode auto-detect | designlang `--dark` | 1.5h | ✅ shipped |
| 5 | Logo extraction with priority hierarchy | designlang | 2h | ✅ shipped |
| 6 | Shadow extraction (elevation ladder) | designlang | 45min | ✅ shipped |
| 7 | Motion / animation tokens | designlang | 1h | ✅ shipped |
| 8 | Component variant matrix | (own — D6) | 2h | ✅ shipped |
| 9 | Self-hosted font embedding (data: URL) | (own — solution) | 1.5h | ✅ shipped |
| 10 | Lint workaround for `@google/design.md@0.1.0` | (own — bug capture) | 1h | ✅ shipped |
| 11 | Hero zone with brand identity | (own — preview redesign) | 1h | ✅ shipped |
| 12 | Live motion demo (animated bouncing balls) | (own — visualization) | 30min | ✅ shipped |

**Total effort applied:** ~17h spread across 2 days.
**Output growth:** 6 input files → 13 input files. Preview html: 40KB → ~300KB-1.2MB (varies by font embed).

---

## Priority Matrix — Remaining Gaps

### Wave 1 — Quick wins (≤2h each)

| # | Practice | Source | Effort | ROI |
|---|---|---|:---:|:---:|
| 1 | **Stable token IDs (hash determinístico)** | Project Wallace | 1h | Drift mode 10× mais útil — IDs sobrevivem renames, dão diff determinístico |
| 2 | **Auth/cookie support** (`--cookie`, `--cookie-file`) | designlang | 1h | Acessar páginas internas autenticadas (`brand.aioxsquad.ai` privado) |
| 3 | **`brands` matrix** (compare N URLs) | designlang | 1.5h | Comparar 4 businesses AIOX (allfluence, aiox, academia, bilhon) num único `brands.html` |
| 4 | **`--mobile` viewport hint** | Dembrandt | 30min | Não temos browser, mas detectamos `@media (max-width)` e sinalizamos mobile-specific tokens |
| 5 | **Stack fingerprint detection** | designlang | 1.5h | Detectar Webflow / Next.js / Tailwind v4 / shadcn no source. Já temos pistas via fontes/vars |
| 6 | **Z-index map** | designlang | 30min | Tabela de layers do source. Util pra arquitetura de modals |
| 7 | **Gradient extraction** | designlang | 30min | `linear-gradient` / `radial-gradient` agrupados como tokens |

**Total Wave 1:** ~6.5h
**Impact:** Drift determinismo + governance de auth + AIOX-specific brands view + 4 detecções extras

### Wave 2 — Strategic features (3-6h each)

| # | Practice | Source | Effort | ROI |
|---|---|---|:---:|:---:|
| 8 | **MCP server** (resources + tools) | designlang | 4h | Diferencial de produto. Claude Code/Cursor consomem extração nativamente. Alinha com aiox-stage strategy |
| 9 | **`watch` mode + history dir** | designlang | 2h | Re-roda diariamente, salva em `outputs/.../history/<date>/`. Combina com drift = monitor de regressão |
| 10 | **GitHub Action workflow** | (gap genérico no mercado) | 3h | Workflow YAML pronto que roda extração + drift no PR, posta verdict em comment. CI gate |
| 11 | **`apply` direct write to project** | designlang | 6h | `--apply --target apps/aiox-brandbook` escreve `globals.css`/`tailwind.config.js` direto. Adoção em 1 comando |
| 12 | **Visual diff (without screenshot)** | designlang | 3h | Compara 2 URLs, gera HTML com tokens diff lado-a-lado. Sem screenshot — só tokens |
| 13 | **Multi-page crawl via static link discovery** | Dembrandt `--pages` | 2h | Sem browser: lê `<a>` no header/footer, segue até depth N. Não cobre SPAs mas cobre site multipágina simples |

**Total Wave 2:** ~20h
**Impact:** Produto integrado (MCP + Action) + observability (watch) + adoção (apply) + cobertura (multi-page)

### Wave 3 — Differentiator (1-2h each)

| # | Practice | Source | Effort | ROI |
|---|---|---|:---:|:---:|
| 14 | **Brand DNA fingerprint (radar 5D)** | (own — único) | 2h | Saturação · Densidade · Modernidade · Formalidade · Contraste. Linguagem que designers usam. Único — nenhum competidor faz. |
| 15 | **Theme remix sliders** | (own — único) | 1.5h | Sliders hue/sat/light/radius no preview. Aplica em real-time. Visualiza elasticidade do DS |
| 16 | **AI prompt-ready output** | (own — único) | 1h | Gera `agent-prompt.txt` com DESIGN.md embedded + instrução pra colar em v0/Lovable/Cursor |
| 17 | **Color blindness simulator** | (gap genérico) | 1h | Filter CSS pra simular protanopia/deuteranopia/tritanopia no component preview |
| 18 | **Component anatomy spec (Material-style)** | (own — único) | 2h | Diagrama anatômico tipo Figma annotations: padding, gaps, line-height marcados sobre cada componente |
| 19 | **Story/slide view mode** | (own — único) | 1.5h | Modo apresentação slide-by-slide do DS extraído. Use case: pitch a stakeholder |

**Total Wave 3:** ~9h
**Impact:** 6 features únicas no mercado, pura diferenciação

### Wave 4 — Ecosystem (1+ dia cada)

| # | Practice | Source | Effort | Impact |
|---|---|---|:---:|:---:|
| 20 | **Multi-platform exporters (iOS SwiftUI, Android Compose)** | designlang | 2h cada | Cobre platforms onde Sinkra Hub tem ambição mobile |
| 21 | **VS Code extension** | designlang | 3-5d | "Extract from URL" command. IDE-native |
| 22 | **Figma plugin** | designlang | 5-7d | Paste URL → Figma Variables collection |
| 23 | **Web playground** (`brand.aioxsquad.ai/extract`) | (own — marketing) | 1d | Wrappa preview.html em Next.js route, expõe pro mercado |

---

## Absorption by Category

### Drift & Observability (4 items — Wave 1 + 2)

| # | Practice | Source | Wave | Current State |
|---|---|---|:---:|:---:|
| 1 | Stable token IDs | Project Wallace | 1 | ❌ Drift mode usa key-by-name |
| 9 | Watch mode + history dir | designlang | 2 | ❌ Único point-in-time |
| 10 | GitHub Action CI gate | (gap mercado) | 2 | ❌ Sem CI integration |
| 12 | Visual diff (token-level) | designlang | 2 | ❌ Drift textual apenas |

**Estado atual:** drift point-in-time único.
**Após absorção:** observability nativa, regressão automática, governance via PR.

### Integration & Ecosystem (5 items — Wave 2 + 4)

| # | Practice | Source | Wave | Current State |
|---|---|---|:---:|:---:|
| 8 | MCP server | designlang | 2 | ❌ Sem MCP |
| 11 | `apply` direct write | designlang | 2 | ❌ Manual cp |
| 20 | iOS / Android exporters | designlang | 4 | ❌ Apenas web |
| 21 | VS Code extension | designlang | 4 | ❌ Apenas CLI |
| 22 | Figma plugin | designlang | 4 | ❌ Sem Figma |

**Estado atual:** CLI + preview.html.
**Após absorção:** ecosystem multi-surface, integração com toolchain do operador.

### Auth & Coverage (3 items — Wave 1 + 2)

| # | Practice | Source | Wave | Current State |
|---|---|---|:---:|:---:|
| 2 | Auth/cookie support | designlang | 1 | ❌ Apenas público |
| 13 | Multi-page crawl (sem browser) | Dembrandt | 2 | ❌ Single page |
| 5 | Stack fingerprint | designlang | 1 | ⚠️ Pistas dispersas |

**Estado atual:** uma URL pública por run.
**Após absorção:** cobertura ampliada — privado + multi-página + arquitetura inferida.

### Differentiators (6 items — Wave 3)

Únicos no mercado: Brand DNA fingerprint, Theme remix sliders, AI prompt-ready output, Color blindness simulator, Component anatomy spec, Story/slide view mode.

**Posicionamento:** transforma Sinkra de "mais uma extração" em "mais rica visualização + único conceitualmente".

---

## Recommended Sprint (4h, immediate value)

Bundle escolhido por máxima velocidade × ROI × diferenciação:

| Ordem | Feature | Tempo | Por que |
|---|---|---|---|
| 1 | **Stable token IDs** (Wave 1, #1) | 1h | Drift mode 10× mais útil. Determinismo. |
| 2 | **`brands` matrix** (Wave 1, #3) | 1.5h | Use case AIOX-específico (4 businesses). Imediato. |
| 3 | **Brand DNA fingerprint** (Wave 3, #14) | 1.5h | Único — nenhum competidor faz radar 5D. |

**Soma:** 4h, 3 features, 1 use case AIOX-específico + 1 melhoria estrutural + 1 diferencial inédito.

## Alternative Sprint (7h, strategic depth)

| Ordem | Feature | Tempo |
|---|---|---|
| 1 | **MCP server** (Wave 2, #8) | 4h |
| 2 | **GitHub Action workflow** (Wave 2, #10) | 3h |

**Soma:** 7h, 2 features que mudam a categoria do produto (de CLI para ecosystem-aware tool).

---

## Cross-Reference With Other Sinkra Benchmarks

| Benchmark | Focus | Gaps | Overlap with this |
|---|---|:---:|:---:|
| `agent-orchestration-5way` | Agent patterns, security, parallelism | 30 | 0 |
| `quality-engineering-4way` | CI/CD, testing, linting | 34 | 1 (lint enforcement pattern) |
| `v0-design-pipeline` | Design generation (synthesis) | n/a | 0 (we extract; v0 generates) |
| `skill-frontmatter-6way` | Frontmatter conventions | n/a | 0 |
| **url-design-extraction (this)** | **URL → DESIGN.md extraction** | **22 (12 done + 10 backlog)** | n/a |
| **Combined coverage** | **Full-spectrum** | **86+** | **1** |

Quase zero overlap entre os benchmarks. Implementar este roadmap junto com os outros absorve **86+ practices** de **12+ external projects**.

---

## Suggested Epic

These 22 gaps form **Epic 130 — URL Design Extraction Maturation** with 4 waves matching the priority matrix above.

**Wave 1:** 7 features, ~6.5h
**Wave 2:** 6 features, ~20h
**Wave 3:** 6 features, ~9h
**Wave 4:** 4 features, ~3-5 weeks

**Estimated total SP:** ~50-70 SP across 23 stories (incl. 12 already shipped).

---

*Generated from URL Design Extraction Benchmark | 2026-04-27*
