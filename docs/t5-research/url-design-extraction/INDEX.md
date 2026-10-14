# URL → Design.md Extraction Benchmark

**Sinkra Hub `extract-from-url` vs Dembrandt vs designlang/design-extract vs HyperDesign vs Project Wallace vs Superposition**
**Date initial:** 2026-04-26
**Date last update:** 2026-04-29

## Documents

| # | Document | Description |
|---|----------|-------------|
| 1 | [full-comparison.md](full-comparison.md) | Complete capability matrix across 8 competitors, current Sinkra position, evidence per category, test runs (Anthropic / Apple / AIOX) |
| 2 | [gap-absorption-roadmap.md](gap-absorption-roadmap.md) | Prioritized 4-wave roadmap to close gaps + extend uniques |
| 3 | [scorecard.json](scorecard.json) | Machine-readable bench data + roadmap priorities |
| 4 | [url-design-extraction-bench.md](url-design-extraction-bench.md) | Original narrative report (April 26, kept for context) |
| 5 | [UPDATE-2026-04-29.md](UPDATE-2026-04-29.md) | **Latest update.** Pipeline hardening + dual-mode theming. New `lib/sanitize.cjs`, `lib/var-resolver.cjs`, `lib/render-contract.cjs`. New `themed` + `render-contract.json` artefacts. 16 visual regressions absorbed across 11 sites, all reproducible. |

## Subject

The Sinkra Hub URL-to-DESIGN.md extraction pipeline lives at:

- **Script:** `squads/design-ops/scripts/extract-from-url/run.cjs`
- **Task:** `squads/design-ops/tasks/extract-design-md-from-url.md`
- **Prompt:** `squads/design-ops/data/url-extract-prompt.txt`
- **Outputs:** `outputs/design-ops/url-extracts/{slug}/`

The pipeline takes any public URL, fetches HTML + CSS via axios + cheerio, runs static analysis to surface tokens / vars / fonts / shadows / motion, invokes Claude Code (`claude -p` headless) to author a Google-spec DESIGN.md, normalizes for spec compliance, runs `@google/design.md@0.1.0 lint`, and renders a single-file standalone `preview.html` with live component previews using the extracted tokens.

## Test Runs (verified 2026-04-27)

| URL | CSS vars | @font-face | Unique tokens | Lint | Score | Confidence (h/m/l) |
|---|---|---|---|---|---|---|
| https://www.anthropic.com/ | 1547 | 8 | 267 | 0E 0W | A 90/100 | 84/0/2 |
| https://www.apple.com/ | 2051 | 18 | 377 | 0E 0W | B 85/100 | 13/35/23 |
| https://brand.aioxsquad.ai/brandbook/guidelines | 1547 | 17 | 427 | 0E 0W | A 91/100 | 75/0/10 |

## Theme Classification (verified 2026-04-29)

11 hosts re-enriched with the new pipeline. `defaultMode` is what the live site renders by default; `toggle` ✓ means the renderer should expose a light/dark switch (light-default sites with explicit dark vars).

| Host | defaultMode | Toggle | Detector confidence |
|---|---|:---:|---|
| Apple, Anthropic, Shopify, Stripe, Mercado Livre | light | – | low (surface fallback) |
| Nubank | light | ✓ | low (dark vars present) |
| Redpine | light | ✓ | medium (`theme-color="#FFFFFF"`) |
| GitHub | light | ✓ | high (`meta color-scheme="light dark"`) |
| Linear | dark | – | high (`<html data-theme="dark">`) |
| Vercel | dark | – | high (`meta color-scheme="dark light"`) |
| **OpenAI** | **dark** | – | low (NEW signal: `:root:not(:where(.light)) { --color-background: #000 }`) |
| aioxsquad | dark | – | medium (`<html class*="dark*">`) |

## Cross-Reference With Other Sinkra Benchmarks

This bench complements the existing benchmarks in this directory:

| Benchmark | Focus | Subject | Overlap with this bench |
|---|---|---|---|
| `agent-orchestration-5way` | Agent patterns, workflows, security, parallelism | BMAD vs Paperclip vs GSD-1/2 vs CrewAI vs Sinkra | 0 |
| `quality-engineering-4way` | CI/CD, testing, linting, observability | Sinkra vs three orchestration tools | 1 (lint enforcement pattern shared) |
| `v0-design-pipeline` | Design generation pipeline (visual UI synthesis) | v0 vs Sinkra | 0 — v0 generates UI from prompt; we extract DS from URL |
| `skill-frontmatter-6way` | Frontmatter conventions across skill ecosystems | Sinkra vs 5 others | 0 |
| `gstack-vs-aiox` | Stack-level architectural comparison | GSD-2 vs AIOX | 0 |
| **url-design-extraction (this)** | **URL → DESIGN.md extraction** | **Sinkra vs Dembrandt, designlang, HyperDesign, Project Wallace, Superposition, Design Token Extractor, awesome-design-md, Stitch** | **n/a** |

Combined with the other benchmarks, Sinkra Hub now has comparative analysis covering: agent orchestration, quality engineering, design pipeline (generation), URL extraction, and skill conventions.

## Key Conclusions

1. **Sinkra is unique** in 5 capabilities no competitor advertises together: Claude Code subprocess (no API key), single-file offline `preview.html`, lint workaround for `@google/design.md@0.1.0` bug, `extraction-log.yaml` provenance, component-property override detection.
2. **Sinkra is ahead** in 13 capabilities total (see full-comparison matrix).
3. **Sinkra is behind** in 7 capabilities — primarily browser-based (multi-page, screenshots, stealth, real DOM computed styles) and ecosystem (MCP server, multi-platform exporters, IDE extensions).
4. **Recommended next moves** detailed in `gap-absorption-roadmap.md`, prioritized as 4 waves.
5. **(2026-04-29 update)** Pipeline now ships **renderer-grade contracts**: outputs are sanitised (debug outlines / hidden transforms / foreign-widget vars rejected), `var(--ds-x)` chains carry resolved fallbacks, and `themed.{light,dark,preferred,defaultMode,supportsDark}` lets downstream UIs render dual-mode without re-parsing CSS. See [UPDATE-2026-04-29.md](UPDATE-2026-04-29.md).
