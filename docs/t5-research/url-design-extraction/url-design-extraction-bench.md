# Bench — URL → DESIGN.md Design Extraction Tools

**Date:** 2026-04-26
**Subject of comparison:** Sinkra Hub `extract-from-url` (squads/design-ops/scripts/extract-from-url) vs the open-source landscape.
**Audience:** Sinkra Hub stakeholders evaluating positioning + roadmap for the URL extraction pipeline.
**Method:** Web research (WebSearch, WebFetch) on canonical repos and product pages; cross-checked against Sinkra Hub's actual implementation.

## TL;DR

The "URL → design tokens / DESIGN.md" space is **crowded as of April 2026**. There are at least three serious open-source CLIs (**dembrandt**, **designlang/design-extract**, **HyperDesign**) plus a curated catalog (**awesome-design-md**) and the official Google Stitch ecosystem. Most competitors use **Playwright + screenshot + Anthropic/OpenAI API** — a stack we explicitly rejected.

Our differentiation is **architectural, not visual**:

- **No headless browser** (axios + cheerio + computed-style-equivalent regex passes)
- **No Anthropic API** (uses local Claude Code subprocess via `claude -p`)
- **Single-file `preview.html`** (offline, no server, no build step)
- **Component-property override detection** (the `.btn { border-radius: 0 }` problem — most competitors miss this)
- **Lint-clean by construction** (normalize layer + Google `@google/design.md` lint with workaround for v0.1.0 nested-`components:` bug)
- **Provenance-first** (`extraction-log.yaml` + per-token `# from --var-name` comments + confidence scoring)

We **lack** screenshot-based visual fidelity, multi-page crawl, drift mode, MCP server, and multi-platform exporters (iOS/Android/Flutter). These are roadmap candidates.

## 1. Competitive landscape (April 2026)

### Tier 1 — Direct CLI competitors

| Tool | Repo | Stack | Output |
|---|---|---|---|
| **Dembrandt** | github.com/dembrandt/dembrandt | Playwright + DOM analysis | DTCG tokens + DESIGN.md (`--design-md` flag) + JSON. Multi-page sitemap crawl. Stealth + `--browser=firefox` for Cloudflare bypass. |
| **designlang / design-extract** | github.com/Manavarya09/design-extract | Playwright + computed styles | 17+ output files: DTCG, Tailwind, Figma vars, iOS SwiftUI, Android Compose, Flutter, WordPress, MCP server, drift mode (`designlang drift`), visual-diff (`designlang visual-diff`), shadcn/ui, motion tokens, anatomy stubs. |
| **HyperDesign** | github.com/hyperbrowserai/hyperbrowser-app-examples/hyperdesign | Hyperbrowser SDK + Playwright + `claude-opus-4-7` API | Next.js app with NDJSON streaming UI. Single URL → DESIGN.md + viewport screenshot + scraped markdown. |

### Tier 2 — Token extraction (no DESIGN.md)

| Tool | Type | Strength |
|---|---|---|
| **Project Wallace** (`@projectwallace/css-design-tokens`) | Open-source JS lib | **Stable token IDs** via hash, identifies removed/added tokens across runs |
| **Superposition** | Desktop app (Mac/Win/Linux) | Export to Figma/XD/Sketch/Swift/Android |
| **Design Token Extractor** | Chrome extension | Element-level inspection in browser |
| **Milten** | Web service (paid) | Migration/audit workflow service |

### Tier 3 — DESIGN.md catalogs

| Repo | Content |
|---|---|
| **VoltAgent/awesome-design-md** | Curated DESIGN.md files for Claude, Cohere, ElevenLabs, Mistral, Linear, Notion, Figma, Framer, Ollama, Replicate, RunwayML |
| **bergside/design-md-chrome** | Chrome extension that generates DESIGN.md + SKILL.md based on TypeUI format |

### Tier 4 — Official spec

| Project | Role |
|---|---|
| **google-labs-code/design.md** | Official Google CLI + linter for the DESIGN.md spec (Apache 2.0). We use this as our lint gate (`@google/design.md@0.1.0`). |
| **Stitch MCP Skills** | Google ships agent skills compatible with Claude Code/Cursor/Gemini CLI/Antigravity. The `design-md` skill auto-generates DESIGN.md from a Stitch project. |

## 2. Capability matrix

| Capability | Sinkra | Dembrandt | designlang | HyperDesign |
|---|---|---|---|---|
| No headless browser | ✅ | ❌ | ❌ | ❌ |
| Screenshot capture | ❌ | ✅ | ✅ | ✅ |
| DTCG output | ✅ | ✅ | ✅ | ❌ |
| DESIGN.md output | ✅ | ✅ | ✅ | ✅ |
| Lint enforcement (`@google/design.md`) | ✅ + workaround | ❓ | ❓ | ❌ |
| Component-property override detection | ✅ | ❓ | ❓ | ❌ |
| Confidence scoring per token | ✅ (high/medium/low) | ✅ | ❓ | ❌ |
| Single-file preview HTML | ✅ | ❓ | ✅ (visual HTML) | ❌ (Next app required) |
| Live component preview with tokens | ✅ | ❓ | ❓ | ❌ |
| WCAG contrast matrix | ✅ | ❓ | ❓ | ❌ |
| Runs via Claude Code subprocess (no SDK) | ✅ (unique) | ❌ | ❌ | ❌ |
| Multi-page crawling | ❌ | ✅ (sitemap) | ✅ | ❌ |
| MCP server | ❌ | ❓ | ✅ | ❌ |
| Drift detection | ❌ | ❓ | ✅ (`drift`) | ❌ |
| Multi-platform exporters (iOS/Android/Flutter) | ❌ | ❌ | ✅ | ❌ |
| Stealth/captcha solver | ❌ | ✅ | ❓ | ✅ (Hyperbrowser) |
| Stable token IDs across runs | ❌ | ✅ | ❓ | ❌ |

### Capabilities we have that nobody else (publicly) advertises

1. **Component-property override detection** — `detectComponentProperties()` walks every CSS rule whose selector matches `.btn`/`.card`/`.input`/`.badge` and emits `most_common` value per (component × property). This is what made the AIOX brandbook render correctly with square buttons (`border-radius: 0`) instead of falling for the `--radius-md: 8px` token.

2. **Lint workaround for the Google v0.1.0 nested-`components:` bug** — captured the upstream crash (`raw.match is not a function`) and built a strip-and-retry path. Not advertised by competitors.

3. **`extraction-log.yaml` provenance schema** — machine-readable confidence summary linked to specific CSS sources per token. Competitors output tokens; we output tokens **plus** epistemic trail.

4. **Single-file `preview.html`** with embedded WCAG contrast matrix, component preview, hero, KPI, code block, type hierarchy. Most competitors either have no preview or require a server.

## 3. Gaps to close (roadmap candidates)

### High-impact, mid-effort

| Idea | Inspiration | Effort | Notes |
|---|---|---|---|
| **Drift mode** — `extract-from-url --compare apps/aiox-brandbook/DESIGN.md` | designlang `drift` | ~3h | Compare local DESIGN.md vs URL extraction, emit verdict (in-sync / minor / notable / major drift). High strategic value: lets us monitor brand drift across the AIOX ecosystem. |
| **Multi-page crawl** | dembrandt sitemap | ~2h | Accept multiple URLs or `--crawl 2` flag, merge tokens + identify per-page divergences. |
| **Stable token IDs** | Project Wallace | ~1h | Hash each token to a stable ID, makes diffs across re-runs deterministic. |
| **Save buttons → `apps/{slug}/DESIGN.md`** | (our A1 backlog) | ~45min | Closes loop extraction → adoption. |
| **MCP server** | designlang | ~4h | Expose extraction as a Claude Code tool via MCP. Aligns with `aiox-stage` MCP strategy. |

### Lower-impact, low-effort

| Idea | Effort | Notes |
|---|---|---|
| **Stealth fallback via opt-in flag** | ~2h | `--stealth` or `--use-hyperbrowser` for sites with Cloudflare. Keep no-browser as default. |
| **Multi-platform exporters (iOS/Android)** | ~2h each | Add Style Dictionary platforms for SwiftUI, Compose. We already export DTCG; transformation is mechanical. |
| **Visual diff between two URLs** | ~3h | Without screenshots, this would be a token-only diff. Pair with stable IDs for clean output. |

### Strategic — would change the product

| Idea | Effort | Notes |
|---|---|---|
| **Headless browser as opt-in module** | ~6h | Keep current default (axios + cheerio), add `npm install @sinkra/extract-from-url-browser` peer that adds Playwright support. Best of both worlds. |
| **Conversational `/design-system extract-from-url` skill** | ~1h | Wire into Claude Design persona for natural-language flow. |
| **Web playground at brand.aioxsquad.ai/extract** | ~1 day | Take the preview.html template, wrap in Next route, expose for prospects. Marketing artifact. |

## 4. Risks and observations

### Spec churn

The `@google/design.md` spec is at **alpha (v0.1.1 as of 2026-04)**. Behavior changes will continue. Our normalize layer absorbs some of this, but a major spec rewrite would force prompt + parser changes.

### "Pure CSS analysis" vs runtime computed styles

Without a headless browser, we miss:
- Tokens injected via JS (styled-components, emotion, CSS-in-JS at runtime)
- Theme switching (light/dark) when not declared as separate selectors
- Animations / transitions resolved at runtime

For static-CSS-heavy sites (Anthropic = Webflow, AIOX = Tailwind v4 + shadcn, Apple = SK design system) we land >85% fidelity. For SPA-heavy targets (Figma editor, Linear app interior) the gap widens.

### Claude Code dependency

Our cognition layer is `claude -p` headless. Pros: zero API key management, runs on the operator's existing Claude Code install. Cons: depends on Claude Code being installed and at compatible version (`2.1.119+`). For CI use, this means each agent box needs Claude Code provisioned — different from `pip install` of an SDK.

### Max-turns ceiling

Apple required `--max-turns 30` (vs Anthropic at ~20) due to higher token volume (2051 CSS vars vs 1547). Larger sites may push past 30. We may need adaptive sizing or chunking strategy.

## 5. Recommendations

1. **Position as "Claude Code-native, lint-clean, single-file"** — three properties no competitor advertises together.
2. **Build drift mode next** — closes the most strategic loop (extraction → governance) and is a feature designlang has but not dembrandt/hyperdesign.
3. **Defer Playwright integration** unless we see concrete failures on important targets. Most current targets (Anthropic, Apple, AIOX) work without it.
4. **Don't compete on platform exporters** — designlang covers iOS/Android/Flutter exhaustively. Our Style Dictionary + Tailwind + CSS-vars + DTCG covers 90% of Sinkra Hub's actual consumers.
5. **Land the live preview.html as a marketing artifact** — share the AIOX run as a tweet, drive interest. The component preview with live tokens is genuinely a "wow" output.

## 6. Sources

- [github.com/dembrandt/dembrandt](https://github.com/dembrandt/dembrandt)
- [dembrandt.com/blackpaper](https://www.dembrandt.com/blackpaper)
- [designlang.manavaryasingh.com](https://designlang.manavaryasingh.com/)
- [github.com/Manavarya09/design-extract](https://github.com/Manavarya09/design-extract)
- [superposition.design](https://superposition.design/)
- [projectwallace.com/design-tokens](https://www.projectwallace.com/design-tokens)
- [github.com/projectwallace/css-design-tokens](https://github.com/projectwallace/css-design-tokens)
- [github.com/VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)
- [github.com/bergside/design-md-chrome](https://github.com/bergside/design-md-chrome)
- [github.com/google-labs-code/design.md/releases](https://github.com/google-labs-code/design.md/releases)
- [blog.google — Stitch DESIGN.md open-source](https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-design-md/)
- [the-decoder.com — Google open-source DESIGN.md](https://the-decoder.com/googles-open-source-design-md-gives-ai-agents-a-prompt-ready-blueprint-for-brand-consistent-design/)
- [dev.to — I Built Dembrandt](https://dev.to/thevangelist/i-built-dembrandt-extract-any-websites-design-system-in-seconds-open-source-2n6d)
- [open-design-app.vercel.app](https://open-design-app.vercel.app/)
- [chromewebstore — Design Token Extractor](https://chromewebstore.google.com/detail/design-token-extractor/iibemocnockckccgcihcmjkciicfoclh)
- [tokencss.com](https://tokencss.com/)
- [github.com/hyperbrowserai/hyperbrowser-app-examples/tree/main/hyperdesign](https://github.com/hyperbrowserai/hyperbrowser-app-examples/tree/main/hyperdesign)
