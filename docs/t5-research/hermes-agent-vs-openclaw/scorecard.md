# Scorecard: Hermes Agent vs OpenClaw

**Date:** 2026-04-04 | **Source:** Local Clone | **Confidence:** High

## Scoring Method

Each dimension scored 0-100 based on observable structural signals from local clone analysis: file counts, feature presence, architecture patterns, and documented capabilities. No estimation — all data verified from source.

---

## Radar Summary

```
                        Hermes    OpenClaw    Delta
Architecture            ██████▏   ████████▊   -26
Agent Intelligence      ████████▌ ███████▏    +13
Messaging & Channels    ███████▏  █████████   -18
Tools & Capabilities    ████████▏ ███████▊    +4
Memory & Learning       ████████▊ ███████     +18
Security & Safety       ████████  ████████▏   -2
Developer Experience    ███████   ████████▌   -15
Testing & Quality       █████▌    █████████   -35
Native & Multi-Platform ██▌       █████████   -65
Community & Ecosystem   █████▌    █████████▏  -37
```

---

## Dimension Scores

| # | Dimension | Hermes | OpenClaw | Delta | Winner |
|---|-----------|-------:|--------:|------:|--------|
| 1 | Architecture & Extensibility | 62 | 88 | -26 | OpenClaw |
| 2 | Agent Loop & Intelligence | **85** | 72 | +13 | **Hermes** |
| 3 | Messaging & Channels | 72 | **90** | -18 | OpenClaw |
| 4 | Tools & Capabilities | **82** | 78 | +4 | **Hermes** |
| 5 | Memory & Learning | **88** | 70 | +18 | **Hermes** |
| 6 | Security & Safety | 80 | **82** | -2 | OpenClaw |
| 7 | Developer Experience | 70 | **85** | -15 | OpenClaw |
| 8 | Testing & Quality | 55 | **90** | -35 | OpenClaw |
| 9 | Native & Multi-Platform | 25 | **90** | -65 | OpenClaw |
| 10 | Community & Ecosystem | 55 | **92** | -37 | OpenClaw |
| | **TOTAL** | **674** | **837** | **-163** | **OpenClaw** |
| | **AVERAGE** | **67.4** | **83.7** | **-16.3** | **OpenClaw** |

---

## Where Hermes Wins (3 dimensions)

### 1. Memory & Learning (88 vs 70, delta +18)

Hermes's memory architecture is more sophisticated:
- **Self-nudging**: Agent autonomously decides when to persist knowledge
- **Honcho dialectic user modeling**: Builds a deepening model of who you are
- **Pluggable provider ABC**: Clean interface for custom memory backends
- **FTS5 cross-session search**: Full-text search with LLM summarization

OpenClaw has memory-core + LanceDB (vector advantage) but no self-improvement loop.

### 2. Agent Loop & Intelligence (85 vs 72, delta +13)

Hermes is built for self-improvement:
- **Skill creation from experience**: Agent creates skills after complex tasks
- **Skills self-improve during use**: Iterative refinement
- **Batch runner**: Parallel trajectory generation with checkpointing
- **RL environments**: Atropos integration for training next-gen models
- **Trajectory compression**: Training data pipeline

OpenClaw matches on core agent capabilities but lacks the research/training infrastructure.

### 3. Tools & Capabilities (82 vs 78, delta +4)

Narrow advantage:
- **49 built-in tools** vs 24 plugins
- **Camofox anti-detection browser**: Stealth browsing with VNC debugging
- **6 terminal backends**: SSH, Modal, Daytona, Singularity enable "not tied to your laptop"
- **Home Assistant integration**: IoT control

OpenClaw counters with video generation, phone control, and broader media pipeline.

---

## Where OpenClaw Wins (7 dimensions)

### 1. Native & Multi-Platform (90 vs 25, delta +65) — LARGEST GAP

OpenClaw's biggest differentiator:
- **macOS app** (583 Swift files, packaged via script)
- **iOS app** (Swift, shared code layer)
- **Android app** (134 Kotlin files)
- **Swabble** (shared Swift library, 25 files)
- **Live Canvas** rendering
- **Voice Call** plugin

Hermes is CLI + gateway only. No native app strategy.

### 2. Community & Ecosystem (92 vs 55, delta +37)

Scale difference is dramatic:
- **1,584 vs 202 contributors** (7.8x)
- **26,602 vs 3,207 commits** (8.3x)
- **Corporate sponsors**: OpenAI, GitHub, NVIDIA, Vercel, Blacksmith, Convex
- **ClawHub** marketplace for community plugins
- Calendar versioning with stable/beta/dev channels

### 3. Testing & Quality (90 vs 55, delta +35)

OpenClaw's testing infrastructure is significantly more mature:
- **3,534 vs 400 test files** (8.8x)
- **70% coverage threshold** enforced
- **E2E test infrastructure** (`*.e2e.test.ts`)
- **SHA-256 drift detection** for config and SDK
- **Documented performance guardrails** for tests
- Multiple CI workflows

### 4. Architecture & Extensibility (88 vs 62, delta +26)

OpenClaw's plugin architecture is a generation ahead:
- **Plugin SDK** with typed contracts and import boundaries
- **93 extensions** prove the model works
- **Manifest-based** plugin registration (`openclaw.plugin.json`)
- **Per-boundary AGENTS.md** files for progressive disclosure
- **Config contract boundary** with zod schema validation

### 5. Messaging & Channels (90 vs 72, delta +18)

Raw channel count: 23+ vs 16. Unique OpenClaw channels:
- iMessage, Google Chat, Microsoft Teams, LINE, Twitch, Nostr, QQ Bot, Voice Call, Nextcloud Talk, Synology Chat, Tlon

### 6. Developer Experience (85 vs 70, delta +15)

- **Dev channels** (stable/beta/dev) with `openclaw update --channel`
- **Strict linting** (Oxlint + Oxfmt)
- **Pre-commit hooks** with `prek`
- **Multiple boundary AGENTS.md** files
- **Config drift detection** with SHA-256

### 7. Security & Safety (82 vs 80, delta +2)

Marginal. OpenClaw edges ahead on governance:
- **CODEOWNERS** security rules
- **GHSA advisory** workflow
- **Formal security policy** (SECURITY.md)

Hermes has stronger runtime scanning (secret exfiltration blocking, URL pattern detection).

---

## Conclusion

**OpenClaw leads overall (83.7 vs 67.4)** driven by superior scale, community, plugin architecture, testing, and native apps.

**Hermes leads on intelligence** — the self-improving loop, memory sophistication, and research infrastructure represent a fundamentally different approach to AI agents. Where OpenClaw is a product, Hermes is a research platform that also serves as a product.

The delta is closing: Hermes v0.7.0 (168 PRs) shows rapid iteration, and the `hermes claw migrate` tool suggests Hermes positions itself as the evolutionary successor to OpenClaw.
