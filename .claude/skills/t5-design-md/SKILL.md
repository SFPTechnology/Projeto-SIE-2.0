---
name: design-md
description: Extract a Google-spec DESIGN.md from any public URL using the canonical design-ops static extraction pipeline. Produces DESIGN.md, tokens.json, tokens-extended.json, render-contract.json, preview.html, provenance, quality score, drift report, and downstream sidecars for design generation. Triggers — "extract design from URL", "get DESIGN.md from URL", "design-md URL", "drift check this URL against my DESIGN.md", "rip the design system from a site".
version: 1.1.0
---

# /design-md — URL → DESIGN.md Pipeline

Extract a Google-spec `DESIGN.md` from any public URL using static HTML/CSS analysis plus a provider-agnostic LLM step. The slash skill is a thin launcher; the implementation source of truth is `squads/design-ops/scripts/extract-from-url/`.
Legacy snapshot files may remain under `.claude/skills/design-md/` during transition, but they are not authoritative. Do not edit or call them for extractor behavior.

## When To Invoke

- User asks to extract design from a public URL.
- User wants tokens, component properties, motion, stack/style fingerprints, or a render contract from a site.
- User wants drift detection between a live URL and a local `DESIGN.md`.
- User wants a downstream contract for UI generation tools such as Tailwind, shadcn, v0, Lovable, Cursor, or internal design-gallery surfaces.

Skip if the user wants finished TSX components directly; use the relevant build/generation workflow after `/design-md` has produced the contract.

## Quick Run

```bash
node .claude/skills/design-md/run.cjs --url https://www.anthropic.com/
```

The launcher delegates to:

```bash
node squads/design-ops/scripts/extract-from-url/run.cjs --url https://www.anthropic.com/
```

## Outputs

Output lands in `outputs/design-ops/url-extracts/{company}/` or `history/{timestamp}/` depending on promotion scoring.

### Run History + Promotion Immutability (NON-NEGOTIABLE)

Default runs write to a scratch directory first, then the canonical runner decides whether to promote that run to `outputs/design-ops/url-extracts/{company}/` or archive it under `outputs/design-ops/url-extracts/{company}/history/{timestamp}/`. Do not manually replace the canonical company root with a lower-quality or failed run.

- If there is no previous canonical root, the first valid run becomes the canonical root.
- If a new run is complete and scores better or equal, it is promoted and the previous canonical root is archived to `history/{previous_timestamp}/`.
- If a new run fails `GATE-FALLBACKS`, lacks `DESIGN.md`, is incomplete against a complete previous root, or scores worse than the previous root, it is archived to `history/{timestamp}/`.
- Historical/provenance details stay in sidecars and `history/`; never add changelog, revision history, or extraction-run metadata into `DESIGN.md`.
- `--out <dir>` is an explicit raw-output override and bypasses the company-layout promotion step; use it only when the caller intentionally wants unmanaged output.

```text
DESIGN.md                  # canonical visual source of truth
tokens.json                # parsed frontmatter plus deterministic enrichment
tokens-extended.json       # deeper extracted sidecar: components, shadows, motion, layout, dark slots
render-contract.json       # stable internal contract for rendering/generation
extraction-log.yaml        # provenance and confidence summary
extraction-class.json      # operational mode, coverage_real, status, and audit recommendations
lint-report.json           # @google/design.md lint result
quality-score.json         # A-F quality breakdown
agent-prompt.txt           # compact prompt for downstream UI agents
preview.html               # standalone visual preview
drift-report.json          # only with --compare
hygiene-report.json        # post-LLM hygiene pass summary (always emitted)
inputs/css-collected.css
inputs/tokens-detected.json
inputs/css-vars-detected.json
inputs/font-faces.json
inputs/embedded-fonts.json
inputs/component-properties.json
inputs/motion.json                       # NOW with transitions[] + keyframe_bodies{} (Wave 1)
inputs/token-usage-graph.json
inputs/theme-default.json
inputs/stack-summary.json
inputs/style/diagnostic sidecars
inputs/component-states.json             # Wave 1 — interaction state rules + state-value palette
inputs/extraction-asymmetries.json       # Wave 1 — brand identity flatness signals
inputs/selector-provenance.json          # Wave 2 — token value → source selector graph
inputs/atomic-classification.json        # Wave 2 — atoms/molecules/organisms/templates/pages
extraction-asymmetries.md                # Wave 1 — human-readable asymmetry report (root)
showcase.html                           # Wave 3 — opt-in via --emit-showcase (root)
```

## Flags

| Flag | Notes |
|---|---|
| `--url <url>` | Required public `http(s)` URL |
| `--out <dir>` | Override output directory |
| `--prompt <file>` | Override prompt template |
| `--compare <file>` | Emit drift report against local `DESIGN.md` |
| `--provider <id>` | `claude-cli`, `codex-cli`, `openrouter`, `openai`, `anthropic-api`, or `generic-http` |
| `--model <id>` | Provider-specific model override |
| `--budget <tier>` | `cheap`, `standard`, or `premium` profile |
| `--max-cache-age <h>` | Static phase reuse TTL |
| `--max-llm-cache-age <h>` | LLM phase reuse TTL |
| `--scaffold` | Emit a v2.2 design.md scaffold from extracted sidecars |
| `--gallery` / `--bundle-force` | Opt into derived `apps/design` materialization |
| `--emit-showcase` | Wave 3 — emit `showcase.html` (Tailwind v4 Browser CDN + @theme block + `.preview-*` component classes) alongside preview.html |
| `--emit-tailwind` | Deprecated alias for `--emit-showcase`; kept for older local invocations |
| `--no-content-gate` | Rare override for thin-content gate |
| `--no-llm-retry` | CI mode: fail hard on first LLM failure |
| `--no-hygiene` | Skip the post-LLM hygiene pass (keeps log/audit comments — debug only) |

## Contract For Downstream Generators

Downstream HTML/Tailwind/gold-standard builders should consume `/design-md` as the evidence layer, not re-scrape or reinterpret the brand. Use this priority:

1. `render-contract.json` for theme mode, renderable component props, and warnings.
2. `tokens.json.preview_tokens` for concrete visual values used in live previews.
3. `tokens-extended.json` for extracted candidates, states, motion, shadows, spacing, and dark slots.
4. `inputs/component-properties.json`, `inputs/motion.json`, `inputs/font-faces.json`, and `inputs/css-collected.css` only when a generator needs raw evidence.
5. `DESIGN.md` for human-readable design intent, Do/Don't rules, and prompt context.

For Tailwind v4 Browser-CDN consumers:

- Emit literal values in `@theme`; do not use `var()` alias chains.
- Preserve commas inside arbitrary values such as `linear-gradient(...)` and `rgba(...)`.
- Prefer plain scoped CSS for component classes when `@apply` depends on custom theme tokens.
- Restore Tailwind preflight casualties intentionally: headings, lists, margins, and form control defaults.

## Tests

Run the canonical test suite:

```bash
node --test squads/design-ops/scripts/extract-from-url/lib/*.test.cjs \
  squads/design-ops/scripts/extract-from-url/lib/providers/*.test.cjs \
  squads/design-ops/scripts/extract-from-url/run.test.cjs
```

## DESIGN.md Comment & Log Hygiene (NON-NEGOTIABLE)

`DESIGN.md` is the consumer contract for LLM code generation — not a changelog, not an audit log, not provenance.

Forbidden in any `DESIGN.md` produced or edited by this skill:

- Frontmatter keys: `fidelity_audit`, `changelog`, `history`, `revisions`, `extracted_at`, `extraction_run`, `removed_fallbacks`, `added_extracted`, `provenance`, `source_files`.
- Inline `#` comments matching: `# count=`, `# matches `, `# was `, `# renamed `, `# Removed `, `# See review`, `# derived from `, `# extracted verbatim`.
- Block comments narrating what changed between versions.

Allowed `#` comments answer one of: semantic role, usage rule, disambiguation, anti-pattern guard. If a comment does not change downstream rendering behavior, it does not ship in `DESIGN.md`.

Logs and provenance live elsewhere:

| Concern | Canonical home |
|---|---|
| Per-token provenance | `inputs/selector-provenance.json` |
| Fallback flags, coverage | `extraction-class.json` |
| Run telemetry (model/cost/turns) | `telemetry.json` |
| Phase log, retries | `extraction-log.yaml` |
| Bakeoff run metadata | `.bakeoff/{model}.meta.json` |
| Audit findings, comparative review | `review-report.md` |
| Version diffs | git commit message + `design.md diff` |

Targets: ≤ 30 KB total, ≤ 20% of frontmatter lines carrying comments, zero inline comments without explanatory value.

Canonical rule: `squads/design-ops/rules/design-md-convention.md` § "Comment & Provenance Hygiene".

## Anti-Patterns

- Do not maintain a second implementation inside `.claude/skills/design-md/`; the launcher must delegate to `squads/design-ops/scripts/extract-from-url/`.
- Do not add browser automation to this extractor. Visual diffing and screenshot validation are downstream workflows.
- Do not write canonical business data to `workspace/` from this skill; extracted runs live under `outputs/design-ops/url-extracts/`.
- Do not fabricate fallback tokens. Missing evidence should remain explicit as an extraction gap.
- Do not embed audit/changelog/provenance metadata into `DESIGN.md` itself — see the Comment & Log Hygiene section above.

## References

- Maintenance source: `squads/design-ops/scripts/extract-from-url/`
- Task contract: `squads/design-ops/tasks/extract-design-md-from-url.md`
- Schema: `squads/design-ops/templates/design-md.schema.json`
- Regression set: `squads/design-ops/data/regression-ds-set.yaml`
- Wave 1+2 extractor protocols:
  - `squads/design-ops/rules/component-state-coverage.md`
  - `squads/design-ops/rules/extraction-asymmetries-protocol.md`
  - `squads/design-ops/rules/motion-extraction-policy.md`
