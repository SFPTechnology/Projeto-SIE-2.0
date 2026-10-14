# Tech Research — 2026-04-29

**Subject:** Pipeline gaps + critical review of 6-phase plan
**Companion to:** [UPDATE-2026-04-29.md](UPDATE-2026-04-29.md), [gap-absorption-roadmap.md](gap-absorption-roadmap.md)
**Method:** WebFetch on canonical sources (ui.shadcn.com, github.com, npm) + direct read of pipeline source
**Audience:** Engineering decision on what to build, what to absorb from external tooling, what to defer

The 6-phase plan ("Plano De Avanço") proposes separating three concerns — `preview.html` as visual baseline, `render-contract.json` as canonical render contract, `DESIGN.md` as agent-facing artifact — then hardening each independently. This research validates the structural intuition, identifies real gaps the plan does not cover, and recommends which phases to invert or skip in favor of external tooling.

## 1. Tech Research

### 1.1 shadcn/ui theme convention

shadcn/ui v3 (current `latest`) standardized on **OKLCH color space** for theme tokens, replacing the earlier HSL space-separated convention. The canonical token set, per [ui.shadcn.com/docs/theming](https://ui.shadcn.com/docs/theming), is:

| Group | Tokens |
|---|---|
| Surfaces | `--background` / `--foreground`, `--card` / `--card-foreground`, `--popover` / `--popover-foreground` |
| Brand | `--primary` / `--primary-foreground`, `--secondary` / `--secondary-foreground` |
| Semantic | `--muted` / `--muted-foreground`, `--accent` / `--accent-foreground`, `--destructive` |
| Form | `--border`, `--input`, `--ring` |
| Geometry | `--radius` (one base; `lg/md/sm` derived in Tailwind config) |
| Charts | `--chart-1` … `--chart-5` |
| Sidebar | `--sidebar`, `--sidebar-foreground`, `--sidebar-primary`, etc. |

Dark mode is the same token names redeclared inside `.dark { … }`. There is **no separate dark file**; the cascade does the work. Lovable, v0, and Cursor consume this exact contract — when an agent sees a DESIGN.md describing `--background`, `--primary`, `--ring`, `--radius` in OKLCH, it can paste those values into `globals.css` and the resulting app inherits the source DS.

`components.json` (per [ui.shadcn.com/docs/components-json](https://ui.shadcn.com/docs/components-json)) carries CLI configuration, not theme values. The fields that matter for an agent:

- `style: "new-york"` (the only style still actively maintained)
- `tailwind.cssVariables: true` (must be true for the OKLCH/HSL var mode)
- `tailwind.baseColor` (one of `neutral`, `stone`, `zinc`, `gray`, `slate` — drives a starter scale that gets overridden by the explicit vars)

These three fields are **immutable post-init** — choosing them wrong forces a reinstall. So a DESIGN.md targeting shadcn must be opinionated.

#### Suggested `## Tailwind & shadcn Implementation` section

```markdown
## Tailwind & shadcn Implementation

**Configuration**

\`\`\`json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "new-york",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.ts",
    "css": "app/globals.css",
    "baseColor": "neutral",
    "cssVariables": true
  }
}
\`\`\`

**Theme tokens (OKLCH)**

\`\`\`css
:root {
  --radius: 0.5rem;                       /* maps to {rounded.md} */
  --background: oklch(0.99 0 0);          /* {colors.surface} */
  --foreground: oklch(0.18 0.01 60);      /* {colors.text} */
  --card: oklch(0.99 0 0);
  --card-foreground: oklch(0.18 0.01 60);
  --primary: oklch(0.65 0.18 35);         /* {colors.primary} */
  --primary-foreground: oklch(0.99 0 0);
  --secondary: oklch(0.95 0.01 80);
  --secondary-foreground: oklch(0.25 0.01 60);
  --muted: oklch(0.95 0.01 80);
  --muted-foreground: oklch(0.45 0.01 60);
  --accent: oklch(0.95 0.01 80);
  --accent-foreground: oklch(0.25 0.01 60);
  --destructive: oklch(0.55 0.22 28);
  --border: oklch(0.9 0.005 60);
  --input: oklch(0.9 0.005 60);
  --ring: oklch(0.65 0.18 35);
}

.dark { /* same names, dark values */ }
\`\`\`

**Component overrides** (cn() classes for shadcn primitives)

- `Button` (variant=default): `rounded-full px-6 py-2.5 font-medium transition-colors`
- `Card`: `rounded-2xl border bg-card shadow-sm`
- `Input`: `rounded-md border-input focus-visible:ring-2 focus-visible:ring-ring`

**Honest limits**

- Iconography not captured (no SVG inventory in extraction)
- Photography not captured
- Custom shadows: hex declared, alpha may need re-tuning by hand
- Proprietary fonts (e.g. Anthropic Sans) require licensing — fallback stack provided
```

The pipeline already emits `theme.surface`, `theme.text`, `theme.accent`, `theme.border`, `radius`, etc. in `render-contract.json`. The conversion step is a small color-space transform (hex → OKLCH) plus a token-name remap (`surface → --background`, `accent → --primary`, etc.). This is ~80 lines of code and zero new pipeline state.

### 1.2 Visual regression tooling for Phase 1

The plan proposes "save screenshots, build checklist, refuse changes that break 2+ DS." This is exactly the visual regression problem. Three real options surveyed:

| Tool | Setup | Browser dependency | HTML report | License | Fit |
|---|---|---|---|---|---|
| [reg-cli](https://github.com/reg-viz/reg-cli) | `npm i -D reg-cli` | **None** — pure image diff | Yes (`-R report.html`) | MIT | Direct fit |
| [BackstopJS](http://garris.github.io/BackstopJS/) | `npm i -g backstopjs` + Puppeteer/Playwright | Yes (Chromium) | Yes, with before/after scrubber | MIT | Heavy |
| [Playwright `toHaveScreenshot()`](https://playwright.dev/docs/test-snapshots) | `npm i @playwright/test` + browser install | Yes | Yes (test report) | Apache-2.0 | If already using Playwright |

The plan's constraint is "10 DS, comparing `preview.html` antes/depois sem ter browser headless instalado por default." That maps cleanly onto **reg-cli**, with screenshots produced by an external one-shot Playwright run that we trigger only in CI, not on every dev machine.

**Recommended setup:**

1. `scripts/snapshot-preview.cjs` (new): runs Playwright in CI only — `npx playwright install chromium` + page.goto each preview.html + `page.screenshot({ fullPage: true })`. Output: `outputs/.../snapshots/<slug>/<timestamp>.png`.
2. `scripts/visual-regression.cjs` (new): wraps `reg-cli` to compare `outputs/.../snapshots/<slug>/baseline.png` against newest. Fails the run on any DS where pixel diff exceeds threshold.
3. `scripts/snapshot-baseline.cjs`: explicit promote step (operator runs after intentional changes).

Cost: ~1.5h to wire the three scripts. Zero per-day runtime cost on dev (only runs in CI). The DS Detail React app, being a separate concern, gets its own snapshot suite if/when needed.

**Why not Percy/Chromatic:** both are excellent but require an account, internet during CI, and either pay or come with quota limits. For a 10-DS project we don't need their cloud features.

**Why not BackstopJS:** the report is great but it bundles its own browser invocation; reg-cli + ad-hoc Playwright keeps the layers separable.

### 1.3 Selector provenance / specificity-aware extraction

The Nubank Swiper bug (`button.transform = rotate(180deg)` from `.swiper-button-prev`) and Apple `--sk-button-color` (6 different values across selectors) both stem from **selector-blind aggregation**: the extractor pools all selectors that match `[class*="button"]` and emits the most-common value, with no awareness of where each value came from.

Three approaches surveyed:

**(a) [postcss-selector-parser](https://github.com/postcss/postcss-selector-parser)** — parses a selector into an AST (compound, pseudo, attribute, etc.). Good for semantic disambiguation: `.swiper-button-prev` is a class node whose head doesn't match `^button$` — rejectable. Already a transitive dep of many tools we'd use; ~30KB bundle. Adoption cost: ~3h to introduce a `selectorIsCanonical(component, selector)` helper that filters `^[\w-]*button[\w-]*$` against widget-prefix denylists.

**(b) [@csstools/selector-specificity](https://github.com/csstools/postcss-plugins/tree/main/packages/selector-specificity)** — calculates `(0,1,0)`-style specificity from a parsed selector. Useful as a tie-breaker when several selectors emit conflicting values: prefer the lowest-specificity (most "default") value over the highest (most "edge case"). This is the inverse of how CSS resolves at runtime — but for *token extraction*, the lowest-specificity declaration is closer to "what the component is by default."

**(c) [@projectwallace/css-design-tokens](https://github.com/projectwallace/css-design-tokens)** — generates stable token IDs via a "very simple hashing algorithm" (per their README). The hash makes drift mode 10× more useful (renames don't break diffs) but does **not** solve the disambiguation problem. Project Wallace explicitly does not do DOM-proximity clustering.

**No off-the-shelf library does DOM-proximity clustering.** The closest open work is the [Stitch](https://blog.google/innovation-and-ai/models-and-research/google-labs/stitch-design-md/) approach, which uses a real browser to compute layouts and group by section. Without a headless browser, the cheapest heuristic is **selector-name patterning**:

```
classify(selector):
  if matches /^(swiper|slick|carousel|owl|splide|gallery)-/: foreign-widget
  if matches /^(nav|header|footer|hamburger|menu|drawer|popover)-/: foreign-component
  if matches /^button$|\.btn$|\.btn-/: canonical-button
  if matches /\.cta\b|\.hero-button/: hero-button
  if matches /\.tab-button|\.toggle-button/: button-variant
  else: ambiguous
```

This is roughly what `lib/sanitize.cjs::FOREIGN_VARS` does today, but at the value-string level (rejects values containing `--swiper-`). Lifting it to the **selector level** — done at token-detection time, not after aggregation — would prevent the ambiguous merge before it happens. Estimated: 4h, including tests.

### 1.4 `@google/design.md` lint status

Latest published version on npm is **0.1.1** (per [github.com/google-labs-code/design.md/releases](https://github.com/google-labs-code/design.md/releases)), released April 21. Release notes mention "module loading issues that could cause crashes on import" but do not explicitly reference the `raw.match is not a function` bug. The 0.1.1 release notes focus on documentation and CLI command updates, not lint behavior.

The spec docs do not advertise an official `components:` schema for the frontmatter. The 12 sites that ship DESIGN.md today (Sinkra extracts) all have their `components:` block stripped at normalize time — meaning we have **never tested** whether the lint accepts a hand-shaped components block in 0.1.1. The Phase 2 proposal to "stop stripping components: and emit spec-compliant ones" has zero ground truth; it depends on running the linter against a candidate shape and discovering by trial which fields it accepts.

**Action:** before committing to Phase 2, regenerate one DESIGN.md against `0.1.1`, manually emit a minimal `components: { button: {...} }` block, and run `npx --yes @google/design.md@0.1.1 lint`. If it errors, `stripComponentsBlock()` is still a permanent path. If it warns gracefully, Phase 2 can proceed with confidence.

## 2. Critical review — 6-phase plan

| Phase | Worth doing? | Verdict |
|---|---|---|
| 1 — Lock visual baseline (10 DS) | **Yes, with ressalva** | Right concern, wrong tooling. Don't build a screenshot harness — install reg-cli + a one-shot Playwright snapshot script. Don't write a "checklist visual" by hand; encode it as pixel-diff thresholds. The plan undersells what already-built tools do for free. |
| 2 — Fix DESIGN.md pipeline (stop stripping `components:`) | **Conditional** | The motivation is correct (DESIGN.md is poorer than it could be). The premise that we can stop stripping is **untested** against `@google/design.md@0.1.1`. Run that test first. If lint accepts, do it. If not, the components knowledge moves to a `## Components` prose section, not the YAML frontmatter — still useful, doesn't fight the linter. |
| 3 — Harden render-contract.cjs | **Yes** | Highest-leverage phase. `preview_tokens` as primary + `extended.components` as evidence-only is exactly right — matches what we already learned the hard way (UPDATE 2026-04-29 bug #6, #11, #12). Add: scoring against `font-size <= 11px`, `bg === text`, `padding/radius reset`, `transparent without intent`. Also add `source: preview_tokens \| component_candidate \| fallback` provenance per field — internal only. |
| 4 — DS Detail consumes contract | **Yes, invert order** | The plan puts this after Phase 3, which is right. But within Phase 4, the React app should remove its defensive layer (`pickColorValue`, `safeNumeric`, etc — ~150 lines per UPDATE-2026-04-29) BEFORE adopting the contract, not after. Otherwise the two layers double-filter and produce ghosts. |
| 5 — shadcn/Tailwind agent contract | **Yes, but separate the two artifacts** | The plan conflates "DESIGN.md gets a shadcn section" with "we emit a shadcn-targeted contract." These are different shapes. Recommend: emit a separate `shadcn-config.json` (the `components.json` form + the OKLCH `globals.css` body) AND a Markdown summary in DESIGN.md. The JSON file is what Lovable/Cursor consume programmatically; the Markdown is for humans + agents that prefer prose. |
| 6 — Validation | **Yes** | But "rodar testes unitários + build + comparar visualmente" is what Phase 1's tooling already gives us. Phase 6 dissolves into "CI runs Phase 1's reg-cli + the existing extractor tests." Don't build a separate validation phase. |

**Suggested ordering inversion:**

1. Phase 3 (render-contract hardening — highest leverage, blocks others)
2. Phase 1 (visual baseline via reg-cli — cheap insurance, enables iteration)
3. Phase 2 lint test (15-min experiment to determine if `components:` block can survive)
4. Phase 5 (shadcn artifact — separate JSON + DESIGN.md prose)
5. Phase 4 (UI migrates to contract; removes defensive layer)
6. Phase 6 dissolves into CI on Phase 1's harness

The plan's stated order makes Phase 1 first; that's defensible (lock the baseline before mutating). The technical reason to start with Phase 3 is that the contract is what every other phase consumes — making Phase 3 the dependency root.

**Hidden risks not in the plan:**

- **No DOM-proximity disambiguation** — Nubank-style bugs will recur whenever a new third-party widget convention appears. The current denylist (`--swiper-`, `--carousel-`, …) is reactive. A selector-level filter (Section 1.3 (a)) is preventive and the plan does not include it.
- **`render-contract.json` schema versioning is not enforced** — `schema_version: "1.0"` is set but no consumer validates it. The plan doesn't enforce; the next breaking change will silently corrupt downstream.
- **No "synthetic test fixture"** — every bug we've fixed came from a real DS surfacing it. The plan is reactive. Synthetic CSS fixtures (`tests/fixtures/swiper-pollution.css`, `tests/fixtures/shadcn-not-where-light.css`, `tests/fixtures/all-unset.css`) would let us write regressions before they ship.
- **OpenAI render-contract still emits `theme.surface = "#ffffff"` despite `default_mode = "dark"`** (verified in `outputs/design-ops/url-extracts/openai/render-contract.json`). The contract picks surface from `pt.surface_bg` first; that field came from the LLM-extracted light theme. The plan's Phase 3 must also fix this — when `default_mode = "dark"`, surface should resolve from the dark scope of `nativeVars`, not `pt.surface_bg`.

## 3. Consolidated Recommendation

### Priorization (final, non-obvious)

| # | Action | Why this order |
|---|---|---|
| 1 | **15-min experiment**: run `@google/design.md@0.1.1 lint` against a hand-shaped `components:` block | Decides whether Phase 2 is feasible at all. Cheapest possible test. |
| 2 | **Fix `render-contract.cjs::theme.surface` resolution** (use `nativeScope` from start) | One-liner that closes a verified bug. No reason to wait. |
| 3 | **Install reg-cli + ad-hoc Playwright snapshot** | 1.5h. Locks the baseline before any further mutation. |
| 4 | **Add selector-level filter** (Section 1.3 (a)) at token-detection time | Preventive; future-proofs against the next widget convention. ~4h. |
| 5 | **Promote `preview_tokens` as primary in render-contract** + scoring filters | Phase 3 core. Touch nothing else until done. |
| 6 | **Emit `shadcn-config.json` sibling artifact** + add `## Tailwind & shadcn Implementation` Markdown section | Sized at ~80 LoC; high agent-facing value. |
| 7 | **DS Detail removes 150 lines of defensive code, adopts render-contract** | After (5) is stable for 7 days. |
| 8 | (If Phase 2 lint test passed) emit `components:` block; else move to prose section in DESIGN.md body |
| 9 | **Schema version enforcement** at consumer side | Cheap; prevents silent corruption later. |
| 10 | **Synthetic fixtures** for the 16 bugs in UPDATE-2026-04-29 | Locks the regressions in unit test form. |

### Where Sinkra should stop building

- **Visual regression.** Use `reg-cli`. The existing roadmap "Visual diff (without screenshot)" (Wave 2 #12) is now obsoleted — `reg-cli` does this with screenshots, and screenshots are strictly more informative.
- **Stable token IDs.** The Project Wallace approach (simple hash of name+value+context) is straightforward to reimplement (1h) but not strategic. Either absorb the `@projectwallace/css-design-tokens` package as a dep, or skip — drift mode is currently text-based and that's fine.
- **DOM-proximity clustering.** No library does this without a browser. The selector-name patterning (Section 1.3) is 80% of the value at 5% of the cost. Stop before building a real DOM clusterer until concrete need (more than 2 sites/quarter break from this).
- **Browser-based extraction (Playwright/Puppeteer).** Already a `gap-absorption-roadmap` item but never absorbed. The position should be permanent: Sinkra is **explicitly browser-free** and uses Claude Code for cognition. Sites that require runtime computed styles are a non-goal.

### What is missing from the 6-phase plan

1. **Selector provenance per emitted property.** UPDATE-2026-04-29 already flags this; it's not in the 6-phase plan but is the structural fix for the Nubank/Apple-multi-value class of bugs.
2. **`render-contract.json` schema versioning** — no plan to bump or enforce.
3. **Synthetic fixtures.** Every bug we found was production. Fixtures would let us prove the fix without re-running 11 extracts.
4. **Token diff between two DS** (token-level, not screenshot). Currently scoped under "Brands matrix" in the absorption roadmap. Belongs in Phase 6 validation.
5. **The `theme.surface` bug in render-contract.cjs** when `default_mode === "dark"` but the LLM tokens are light. Verified in OpenAI's output; not mentioned in the plan.

### 5 Takeaways

1. **Phase 3 (render-contract hardening) is the dependency root.** Every other phase consumes its output. Start there, not at Phase 1.
2. **Don't build visual regression tooling — install reg-cli + an ad-hoc CI Playwright snapshot.** Total cost ~1.5h vs. weeks for a homegrown harness.
3. **Phase 2's premise (stop stripping `components:`) is untested.** Run a 15-minute lint experiment against `@google/design.md@0.1.1` before committing — if the linter still rejects, the components knowledge moves to a `## Components` prose section, not YAML frontmatter.
4. **The shadcn convention is OKLCH custom properties + `components.json`.** The pipeline should emit a separate `shadcn-config.json` sibling artifact (machine-readable, agent-consumed) plus a `## Tailwind & shadcn Implementation` Markdown section in DESIGN.md (human + LLM-prose). Not the same shape; both have value.
5. **The structural blind spot is selector provenance.** No off-the-shelf library does DOM-proximity clustering without a browser; the selector-name patterning approach (denylist widget prefixes at token-detection time, not value-string time) prevents the Nubank-class bug at the source. Add this to Phase 3 — the 6-phase plan does not include it.
