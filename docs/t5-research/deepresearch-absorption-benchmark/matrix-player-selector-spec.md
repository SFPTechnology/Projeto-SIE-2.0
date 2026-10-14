# Matrix Player Selector — Component Specification

> Founder feedback (2026-05-18): "A matriz corta e não consigo ver os 24 players, eu devia poder na matriz selecionar quais players quero visualizar ou não, independente se for 5 ou 30."

## Problem (current state)

`apps/research/src/components/observatory/organisms/matrix-view.tsx` renders ALL players in fixed 140px columns.

With 25 players: `gridTemplateColumns: minmax(320px,1fr) repeat(25, 140px) 100px` → minWidth = 320 + 25×140 + 100 = **3920px**. Container is `max-w-[1540px]`. Horizontal scroll cuts after column 9. **16 players invisible without aggressive scroll.**

This blocks comparison readability regardless of bench size (5 players cramped, 30 players truncated).

## Required Component

### Inputs

- `matrix.players[]` — all available player keys
- `matrix.totals[]` — per-player aggregate scores
- `players[]` (top-level dash) — full player profiles with name/color/category
- `summary.anchor` — the anchor player (e.g. `aiox_research`) — ALWAYS visible by default
- URL search param `?players=key1,key2,key3` — persisted selection

### UI Surface — Inline Player Chips (NOT a separate panel)

**No separate selector panel.** Each player is a **clickable chip** in the matrix column header. Click a chip to toggle that player's column on/off. The chip is the toggle.

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│  DIMENSÃO                  │ ●AIOX │ ●DRB │ ●Deer │ ●ARC │ ○Storm │ ●GPT │ ○LDR │..│
│                            │ 🟢anc │      │       │       │       │      │       │  │
│  ←chip ativada=opaco       │  ↑    │ ↑    │  ↑    │  ↑    │  ↑    │  ↑   │  ↑    │  │
│  ←chip desativada=fade     │ click │ click│ click │ click │ click │ click│ click │  │
│  ←anchor=lime border        │ to   │ to   │ to    │ to    │ to    │ to   │ to    │  │
│                             │toggle│toggle│toggle │toggle │toggle │toggle│toggle │  │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

### Behavior

| Action | Effect |
|---|---|
| Default load (no `?players=`) | Anchor + top 8 by score visible (active state) |
| Click chip of inactive player | Activates → column appears in grid |
| Click chip of active player | Deactivates → column hides (chip stays visible faded) |
| Click chip of anchor | No-op (anchor is locked, lime border indicates locked state) |
| All chips inactive (theoretically) | Force-fallback to anchor only |

**Chip states (visual):**

| State | Visual |
|---|---|
| Active (visible in matrix) | Full color (player accent color), 100% opacity, bg-saturated |
| Inactive (hidden from matrix) | Faded — 40% opacity, dashed border, color desaturated |
| Anchor (always active) | Full color + lime accent border + 🟢 dot prefix + cursor: not-allowed |

### Why chips and not a panel

The chip header IS the column header. Clicking the column header itself to toggle is the most direct affordance — zero context switch, zero new UI surface, zero clicks to find the toggle. The faded chip stays in place as a visual record of "this player exists but I'm not looking at it right now."

This pattern is borrowed from Linear's filter chips, Notion's table column toggles, and Grafana's series chips.

### URL Persistence

Same as before — visible set persists to `?players=key1,key2,key3` for shareable links.

### Implementation Sketch (matrix-view.tsx)

```tsx
const [visiblePlayers, setVisiblePlayers] = usePlayerSelection({
  allPlayers: matrix.players,
  anchor: summary.anchor,
  defaultLimit: 9, // anchor + top 8
  totals: matrix.totals,
})

const visibleMatrix = useMemo(() => ({
  ...matrix,
  players: visiblePlayers,
  rows: matrix.rows.map(row => ({
    ...row,
    cells: row.cells.filter(c => visiblePlayers.includes(c.player))
  })),
  totals: matrix.totals.filter(t => visiblePlayers.includes(t.player))
}), [matrix, visiblePlayers])
```

### URL-as-State (per `.claude/rules/url-as-state-frontend.md`)

Visibility selection MUST persist in URL:

```
/observatory/bench?slug=deepresearch-absorption-benchmark&players=aiox_research,deer-flow,gpt-researcher,autoresearchclaw
```

Shareable link arrives at exact filtered state. Refresh preserves selection. Back/forward navigation works.

### Layout Trade-Offs

- **5-9 players visible:** comfortable 140-180px columns, full text
- **10-15 players visible:** 100-120px columns, abbreviated header
- **16+ visible:** horizontal scroll required, but user explicitly opted in

The selector ALWAYS shows total count: "Showing 9 of 25 — 16 hidden, click to add"

## Cross-Cutting Improvements

While editing matrix-view.tsx, also add:

1. **Column drag-reorder** — user can pin AIOX next to a specific competitor for direct comparison
2. **Sort selector** — `Sort by: score desc | score asc | alphabetical | category`
3. **Group by category filter** — show only `framework-multiagent` or `purpose-trained-model`
4. **Anchor highlight** — AIOX column has subtle lime tint border so user always sees where the anchor sits

## Test Cases

| Scenario | Expected |
|---|---|
| Bench with 5 players | All 5 visible by default, no selector needed |
| Bench with 9 players | All 9 visible by default |
| Bench with 25 players, no `?players=` URL param | Anchor + top 8 visible (9 total) |
| User unchecks AIOX | AIOX stays visible (locked), warning toast |
| URL `?players=deer-flow,gpt-researcher` (no anchor) | Anchor force-included → 3 visible |
| URL `?players=invalid_key,another_invalid` | Fallback to default (anchor + top 8) |
| `Top 5` clicked | Anchor + 4 highest-scoring non-anchor visible |
| `All` clicked | All 25 visible, horizontal scroll active |

## Out of Scope (for now)

- Saved presets (e.g. "My favorite comparison")
- Multi-user shared presets
- Heatmap density toggle (compressed view)

## Acceptance

When this spec lands:
- Founder can compare AIOX vs any 4-8 chosen competitors on screen without scrolling
- 25-player benches don't require horizontal scroll for the typical use case
- URL is shareable with exact filtered state

## Where to Implement

- Primary edit: `apps/research/src/components/observatory/organisms/matrix-view.tsx`
- New file: `apps/research/src/hooks/use-player-selection.ts`
- New molecule: `apps/research/src/components/observatory/molecules/player-selector.tsx`

## Story Reference

To be created as **STORY-OBS-MATRIX-SELECTOR** in `apps/research` repo.
