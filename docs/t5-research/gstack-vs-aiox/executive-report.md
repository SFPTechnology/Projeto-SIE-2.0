# Executive Report: gstack vs AIOX (Sinkra Hub)

**Benchmark ID:** bench-gstack-vs-aiox-2026-04-13
**Type:** Codebase (Full Pipeline)
**Analyst:** bench-analyst (spy squad)
**Date:** 2026-04-13
**Confidence:** HIGH (both repos cloned locally, 25+ files analyzed per subject)

---

## 1. Executive Summary

We benchmarked **gstack** (Garry Tan, YC, MIT, 71K stars) against **AIOX/Sinkra Hub** (private, SINKRA v3.2) across 6 weighted dimensions. AIOX scores **88.1 vs gstack's 72.4** — a 15.7-point delta driven by architectural depth, governance, and automation.

gstack wins on **browser integration** (persistent daemon, ref system) and **multi-host parity** (8 AI hosts). These are tactical features, not structural advantages. AIOX's wins are structural: governance, process methodology, multi-business isolation, learning graduation, and orchestration depth.

**8 gstack patterns** are candidates for absorption into AIOX. **10 gstack patterns** were explicitly rejected. Estimated absorption cost: **49 story points over 3 sprints**.

---

## 2. Key Findings

### 2.1 Architecturally Different, Not Better/Worse

gstack and AIOX solve the same problem (structured AI-assisted development) from opposite ends:

- **gstack** = 37 flat skills for solo builders. Zero ceremony. Instant productivity.
- **AIOX** = 54 squads with 461 agents for organizations. Full governance. Process rigor.

Neither architecture is universally superior. gstack is better for a solo founder shipping a feature. AIOX is better for 4 businesses with shared infrastructure and formal quality gates.

### 2.2 gstack's Browser Daemon Is Genuinely Superior

The persistent Chromium daemon (`browse/src/`, 13,192 LOC) with ref system (@e1, @e2) is gstack's strongest technical innovation. It enables:
- <100ms per browser command (vs 2-3s per Playwright invocation)
- Stable element references across page mutations
- Ring buffer logging (50K entries, O(1) push)
- Tab persistence across commands within a session

This is the **#1 pattern to absorb** (ABS-GSTACK-001, priority P0).

### 2.3 AIOX's Governance Is Unreachable by gstack

AIOX's Constitutional governance (16 rules + 14 hooks + CODEOWNERS + mandatory gates) is structurally unreachable by gstack's flat architecture. Adding governance to gstack would require a fundamental redesign — it would become a different product.

This is AIOX's **permanent competitive advantage**.

### 2.4 Scale Metrics Tell the Story

| Metric | gstack | AIOX | Ratio |
|--------|-------:|-----:|------:|
| Agent/Skill files | 37 | 568 | 1:15 |
| Tasks defined | 0 | 1,629 | 0:1629 |
| Test files | 82 | 3,566 | 1:43 |
| Templates | 1 | 593 | 1:593 |
| Checklists | 0 | 446 | 0:446 |
| Workflows | 0 | 276 | 0:276 |
| Governance config lines | ~100 | 46,180 | 1:462 |

AIOX operates at **10-500x greater scale** in every structural dimension except raw TypeScript LOC (gstack's browser is 13K LOC of compiled binary).

---

## 3. Dimension Scores

| Dimension | Weight | gstack | AIOX | Delta | Winner |
|-----------|-------:|-------:|-----:|------:|--------|
| Architecture | 20% | 62 | 92 | -30 | AIOX |
| Testing & QA | 20% | 75 | 88 | -13 | AIOX |
| Documentation | 15% | 78 | 85 | -7 | AIOX |
| Automation | 20% | 70 | 90 | -20 | AIOX |
| Extensibility | 15% | 72 | 88 | -16 | AIOX |
| Code Quality | 10% | 82 | 80 | +2 | gstack |
| **TOTAL** | **100%** | **72.4** | **88.1** | **-15.7** | **AIOX** |

gstack's only dimension win is Code Quality (+2), driven by its agent-oriented error handling pattern (wrapError). AIOX dominates all other dimensions.

---

## 4. Absorption Recommendations

### Must-Do (P0, Sprint 1-2)

| Pattern | Decision | Target | Effort |
|---------|----------|--------|--------|
| Browser Daemon + Ref System | ADAPT | infra-ops | L (13 pts) |
| Post-Deploy Canary Monitoring | ADAPT | infra-ops | M (5 pts) |

### Should-Do (P1, Sprint 2)

| Pattern | Decision | Target | Effort |
|---------|----------|--------|--------|
| Performance Benchmarking | ADAPT | infra-ops | M (5 pts) |
| AI Slop Detection | CREATE | design-system | S (2 pts) |

### Could-Do (P2-P3, Sprint 3+)

| Pattern | Decision | Target | Effort |
|---------|----------|--------|--------|
| Skill Template Generation | ADAPT | sinkra-squad | M (8 pts) |
| Auto-Review Pipeline | ADAPT | c-level | M (5 pts) |
| Learnings Session Injection | REUSE | sinkra-squad | S (1 pt) |
| Safety Enhancement | REUSE | sinkra-squad | S (1 pt) |

### Explicitly Rejected (10 patterns)

Multi-host parity, Conductor parallelism, flat architecture, ETHOS model, voice triggers, cookie import, Bun runtime, telemetry UX, preamble tiers, worktree isolation.

---

## 5. Threat Assessment

| Threat | Severity | Probability | Mitigation |
|--------|----------|-------------|------------|
| gstack's browser daemon becomes industry standard | HIGH | MEDIUM | Absorb pattern (ABS-001, 3-sprint timeline) |
| YC distribution gives gstack market dominance | HIGH | LOW | Compete on depth, not awareness |
| gstack adds governance (becomes AIOX-lite) | MEDIUM | LOW | MIT + single maintainer makes this unlikely |
| Multi-host parity attracts enterprise customers | MEDIUM | MEDIUM | Strategic eval needed (separate decision) |
| gstack's MIT license enables commercial forks | LOW | LOW | Forks fragment, don't consolidate |

---

## 6. Strategic Recommendations

1. **Absorb browser daemon immediately** — This is gstack's strongest technical innovation and AIOX's biggest tactical gap. P0, Sprint 1-2.

2. **Do NOT flatten architecture** — Squad-deep hierarchy is AIOX's structural moat. gstack can't add governance; we shouldn't remove ours.

3. **Evaluate multi-host independently** — This is a business strategy question (vendor diversification), not an absorption question. Don't mix it with gstack analysis.

4. **Monitor gstack monthly** — With 71K stars and YC backing, gstack will evolve rapidly. Add to `/spy` watchlist for quarterly benchmark refresh.

5. **Consider "AIOX Lite" entry path** — gstack's UX advantage is zero-ceremony activation. An AIOX simplified mode for solo builders could capture that market without sacrificing governance depth for teams.

---

## 7. Artifacts Generated

| # | Artifact | Format |
|---|----------|--------|
| 1 | `metadata.json` | JSON |
| 2 | `inventory-gstack.json` | JSON |
| 3 | `inventory-aiox.json` | JSON |
| 4 | `comparison-matrix.json` | JSON |
| 5 | `scorecard.json` | JSON |
| 6 | `scorecard.md` | Markdown |
| 7 | `gap-analysis.json` | JSON |
| 8 | `gap-analysis.md` | Markdown |
| 9 | `battle-card.md` | Markdown |
| 10 | `executive-report.md` | Markdown (this file) |

**Cross-reference:** Full SINKRA pipeline output at `outputs/sinkra-squad/gstack-competitive-intel/` (7 artifacts from 7-phase process mapping).

---

*Generated by bench-analyst (spy squad) | Full Pipeline (10 phases) | 2026-04-13*
*Scoring method: bench-dimension-packs.yaml (type=codebase, 6 dimensions, weighted)*
*Sources: /Users/oalanicolas/Code/gstack (local clone), /Users/oalanicolas/Code/sinkra-hub (local)*
