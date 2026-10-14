# The Three-Layer AI Platform: Architecture Vision

**Hermes Agent (Intelligence) × OpenClaw (Distribution) × Sinkra Hub (Governance)**

**Date:** 2026-04-04 | **Version:** 1.0
**Benchmark Sources:** `hermes-agent-vs-openclaw/`, `hermes-agent-vs-openclaw-vs-sinkra-hub/`
**SINKRA Maps:** `outputs/sinkra-squad/hermes-agent/`, `outputs/sinkra-squad/openclaw/`

---

## 1. The Problem: Three Dimensions, Two-Axis Thinking

The AI agent landscape is typically analyzed on two axes: **how smart** the agent is and **where it reaches users**. This misses the third — and arguably most critical — dimension: **how agents are organized and governed at scale**.

| Dimension | Question | Project That Answers |
|-----------|---------|---------------------|
| **Intelligence** | What does the agent know, learn, and improve? | Hermes Agent |
| **Distribution** | Where and how does the agent reach users? | OpenClaw |
| **Governance** | How are agents organized, quality-controlled, and scaled? | Sinkra Hub |

No single project covers all three. No pair covers all three. Only the triple does.

---

## 2. The Three Projects — By The Numbers

```
┌──────────────────────────────────────────────────────────────────────┐
│                                                                      │
│   HERMES AGENT              OPENCLAW               SINKRA HUB       │
│   ══════════════           ══════════              ═══════════       │
│                                                                      │
│   Python 3.11+             TypeScript              TS+Py+YAML+MD    │
│   301K LOC                 1.84M LOC               9.18M LOC*       │
│   681 files                12,150 files            32,357 files     │
│   202 contributors         1,584 contributors      4 contributors   │
│                                                                      │
│   1 agent (AIAgent)        ~5 agents               473 agents       │
│   49 tools                 93 extensions            53 squads        │
│   116 skills               53 skills                57 skills        │
│   17 platforms             23+ channels             0 (CLI-first)    │
│   0 native apps            3 native apps            0 native apps   │
│   400 tests                3,534 tests              204 tests        │
│   0 governance artifacts   ~266 boundaries          3,139 artifacts  │
│                                                                      │
│   * 556K code + 2.65M YAML + 5.97M Markdown                        │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 3. The Three-Axis Model

### 3.1 Axis Definitions

**Axis X — Distribution Reach (0-100)**
How broadly the system reaches end users. Measured by: messaging channels, native apps, plugin ecosystem, community size, deployment options.

**Axis Y — Intelligence Depth (0-100)**
How deeply the system learns, reasons, and improves. Measured by: self-improvement, memory sophistication, RL training, user modeling, skill creation.

**Axis Z — Governance Depth (0-100)**
How rigorously the system organizes, quality-controls, and scales agents. Measured by: constitutional rules, agent authority, templates, checklists, task anatomy, business isolation.

### 3.2 Each Project's Position

| Project | X (Distribution) | Y (Intelligence) | Z (Governance) | Dominant Axis |
|---------|:-----------------:|:-----------------:|:--------------:|:-------------:|
| Hermes Agent | 75 | **92** | 25 | Y — Intelligence |
| OpenClaw | **95** | 30 | 55 | X — Distribution |
| Sinkra Hub | 10 | 20 | **98** | Z — Governance |

### 3.3 Three-Axis Radar

```
                         Intelligence (Y)
                              100
                               │
                          90 ──┤── Hermes (92)
                               │╲
                          80 ──┤  ╲
                               │   ╲
                          70 ──┤    ╲
                               │     ╲
                          60 ──┤      ╲
                               │       ╲
                          50 ──┤        ╲
                               │    ·····╲·········
                          40 ──┤   ·      ╲       ·
                               │  ·   HYBRID·     ·
                          30 ──┤ · OpenClaw──╲────·─── Sinkra (98)
                               │·     (30)    ╲  ·
                          20 ──┤───────Sinkra───╲·
                               │  (20)          ╲
                          10 ──┤   Sinkra(10)    ╲── OpenClaw (95)
                               │                  ╲
                           0 ──┴───┬───┬───┬───┬───┬───┬───┬───┬───┬──
                               0  10  20  30  40  50  60  70  80  90 100
                                                          Distribution (X)
                                                    ╱
                                              Governance (Z)
                                         (perpendicular to page)
```

### 3.4 Projected Views (3 Quadrants)

**View 1: Intelligence × Distribution (looking down Z axis)**
```
    Intelligence
    100 ┤
     90 ┤  ★ Hermes
     80 ┤
     70 ┤                              ◆ HYBRID TARGET
     60 ┤
     50 ┤
     40 ┤
     30 ┤                         ★ OpenClaw
     20 ┤  ○ Sinkra
     10 ┤
      0 ┼──┬──┬──┬──┬──┬──┬──┬──┬──┬──
        0  10 20 30 40 50 60 70 80 90 100  Distribution

    ★ = project    ○ = off-plane (Z dominant)    ◆ = target
```
*Hermes e OpenClaw sao complementares neste plano. Sinkra e irrelevante aqui.*

**View 2: Intelligence × Governance (looking down X axis)**
```
    Intelligence
    100 ┤
     90 ┤  ★ Hermes
     80 ┤
     70 ┤                              ◆ HYBRID TARGET
     60 ┤
     50 ┤
     40 ┤
     30 ┤  ○ OpenClaw
     20 ┤                         ★ Sinkra
     10 ┤
      0 ┼──┬──┬──┬──┬──┬──┬──┬──┬──┬──
        0  10 20 30 40 50 60 70 80 90 100  Governance

    ○ = off-plane (X dominant)
```
*Hermes e Sinkra sao complementares neste plano. OpenClaw e irrelevante aqui.*

**View 3: Distribution × Governance (looking down Y axis)**
```
    Distribution
    100 ┤
     95 ┤                         ★ OpenClaw
     80 ┤
     70 ┤  ○ Hermes               ◆ HYBRID TARGET
     60 ┤
     50 ┤
     40 ┤
     30 ┤
     20 ┤
     10 ┤                         ★ Sinkra
      0 ┼──┬──┬──┬──┬──┬──┬──┬──┬──┬──
        0  10 20 30 40 50 60 70 80 90 100  Governance

    ○ = off-plane (Y dominant)
```
*OpenClaw e Sinkra sao complementares neste plano. Hermes e irrelevante aqui.*

### 3.5 Key Insight

**Em cada par, o terceiro projeto e "irrelevante" — mas no triple, todos sao essenciais.**

Isso prova que a sinergia e genuinamente 3-dimensional. Nao e Hermes+OpenClaw "com Sinkra por cima". Sao 3 projetos que cada um domina um eixo ortogonal.

---

## 4. The Layered Architecture

### 4.1 Conceptual Stack

```
╔══════════════════════════════════════════════════════════════════════╗
║                                                                      ║
║   LAYER 3: GOVERNANCE (Sinkra Hub)                                   ║
║   ─────────────────────────────────                                  ║
║   Constitution (322 lines) │ CODEOWNERS │ Agent Authority Matrix     ║
║   53 Squads │ 473 Agents │ Chief→Specialist hierarchy                ║
║   621 Templates │ 483 Checklists │ 1,834 Task Definitions            ║
║   8-Layer Framework (L1 Business → L8 Evolution)                     ║
║   4 Businesses │ Data Isolation │ Document Registry                  ║
║   META_AXIOMAS Quality Gates │ SINKRA v3.1 Composition               ║
║                                                                      ║
║   "HOW agents are organized, validated, and governed"                ║
║                                                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║   LAYER 2: INTELLIGENCE (Hermes Agent)                               ║
║   ────────────────────────────────────                               ║
║   AIAgent Core │ Self-Improving Skill Loop │ 116 Skills              ║
║   Honcho Dialectic User Modeling │ Memory Self-Nudging               ║
║   FTS5 Cross-Session Search │ Smart Model Routing                    ║
║   Credential Pool Rotation │ Context Compression                     ║
║   Mixture of Agents │ Prompt Caching │ Camofox Browser               ║
║                                                                      ║
║   RL Pipeline: Batch Runner → Atropos → Trajectory Compression       ║
║   11 Model-Specific Tool Call Parsers │ SWE-Bench Runner             ║
║                                                                      ║
║   "WHAT the agent knows, learns, and improves"                       ║
║                                                                      ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║   LAYER 1: DISTRIBUTION (OpenClaw)                                   ║
║   ────────────────────────────────                                   ║
║   23+ Messaging Channels │ Native Apps (macOS/iOS/Android)           ║
║   93 Extensions (35 Providers │ 23 Channels │ 24 Tools)              ║
║   Plugin SDK (50+ subpath exports) │ Manifest Lifecycle              ║
║   Gateway Protocol │ Bridge Protocol │ Canvas (a2ui)                 ║
║   ClawHub Marketplace │ 1,584 Contributors                           ║
║   Dev Channels (stable/beta/dev) │ 3,534 Tests │ 70% Coverage       ║
║                                                                      ║
║   "WHERE the agent reaches users"                                    ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
```

### 4.2 Data Flow (Top to Bottom)

```
                    ┌─────────────────────┐
                    │     END USERS        │
                    │  (4 businesses ×     │
                    │   23+ channels)      │
                    └────────┬────────────┘
                             │
                    ┌────────▼────────────┐
                    │  L1: DISTRIBUTION    │
                    │  (OpenClaw)          │
                    │                      │
                    │  Telegram ─┐         │
                    │  Discord  ─┤         │
                    │  Slack    ─┤         │
                    │  WhatsApp ─┼─► Gateway Protocol
                    │  iMessage ─┤         │
                    │  Teams    ─┤         │
                    │  iOS App  ─┤         │
                    │  Android  ─┤         │
                    │  macOS    ─┘         │
                    │          │           │
                    └──────────┼───────────┘
                               │ OpenAI-compatible JSON
                    ┌──────────▼───────────┐
                    │  L2: INTELLIGENCE     │
                    │  (Hermes Agent)       │
                    │                       │
                    │  ┌─────────────────┐  │
                    │  │  AIAgent Core   │  │
                    │  │  ┌───────────┐  │  │
                    │  │  │ Skill Loop│◄─┼──┼── Self-creates from experience
                    │  │  └─────┬─────┘  │  │
                    │  │        │         │  │
                    │  │  ┌─────▼─────┐  │  │
                    │  │  │  Honcho   │  │  │
                    │  │  │  Memory   │  │  │
                    │  │  └─────┬─────┘  │  │
                    │  │        │         │  │
                    │  │  ┌─────▼─────┐  │  │
                    │  │  │  49 Tools │  │  │
                    │  │  │  + 93 OC  │  │  │
                    │  │  │  plugins  │  │  │
                    │  │  └───────────┘  │  │
                    │  └─────────────────┘  │
                    │          │             │
                    └──────────┼─────────────┘
                               │ Trajectories + outputs
                    ┌──────────▼─────────────┐
                    │  L3: GOVERNANCE         │
                    │  (Sinkra Hub)           │
                    │                         │
                    │  ┌───────────────────┐  │
                    │  │  Constitution     │  │
                    │  │  ┌─────────────┐  │  │
                    │  │  │Authority    │  │  │
                    │  │  │Matrix      │  │  │
                    │  │  └──────┬──────┘  │  │
                    │  │         │          │  │
                    │  │  ┌──────▼──────┐   │  │
                    │  │  │Quality Gates│   │  │
                    │  │  │META_AXIOMAS │   │  │
                    │  │  └──────┬──────┘   │  │
                    │  │         │           │  │
                    │  │  ┌──────▼──────┐   │  │
                    │  │  │ 53 Squads   │   │  │
                    │  │  │ 473 Agents  │   │  │
                    │  │  └──────┬──────┘   │  │
                    │  │         │           │  │
                    │  │  ┌──────▼──────┐   │  │
                    │  │  │ Workspace   │   │  │
                    │  │  │ L0-L4 ×     │   │  │
                    │  │  │ 4 Business  │   │  │
                    │  │  └─────────────┘   │  │
                    │  └───────────────────┘  │
                    │          │               │
                    └──────────┼───────────────┘
                               │
                    ┌──────────▼───────────────┐
                    │  RL TRAINING FLYWHEEL     │
                    │                           │
                    │  Trajectories from 23     │
                    │  channels → Batch Runner  │
                    │  → Atropos RL → Better    │
                    │  Models → Deploy back     │
                    │  to L2 Intelligence       │
                    └──────────────────────────┘
```

---

## 5. SINKRA Compositional Mapping

### 5.1 How Each Project Maps to SINKRA Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│  SINKRA Level  │  Hermes Maps To     │  OpenClaw Maps To       │
├────────────────┼─────────────────────┼─────────────────────────┤
│                │                     │                         │
│  L6: Instance  │  Running AIAgent    │  Running Gateway        │
│                │  session            │  + active channels      │
│                │                     │                         │
│  L5: Template  │  Config profile     │  Plugin manifest        │
│                │  (config.yaml)      │  (openclaw.plugin.json) │
│                │                     │                         │
│  L4: Organism  │  Conversation flow  │  Gateway message cycle  │
│                │  Skill creation     │  Plugin lifecycle       │
│                │  loop               │  Onboarding flow        │
│                │  RL training        │  CI/CD pipeline         │
│                │  pipeline           │  Native app build       │
│                │                     │                         │
│  L3: Molecule  │  Tool dispatch      │  Channel routing        │
│                │  Memory flush       │  Provider failover      │
│                │  Context compress   │  Config migration       │
│                │  Gateway routing    │  Hook chain             │
│                │                     │                         │
│  L2: Atom      │  Single tool call   │  Single plugin load     │
│                │  Single LLM call    │  Single message deliver │
│                │  Memory write       │  Single model inference │
│                │  Skill execute      │  Config set             │
│                │                     │                         │
│  L1: Token     │  iteration_budget   │  node_version_check     │
│                │  status (idle/      │  status (initializing/  │
│                │   processing/       │   respawning/ready/     │
│                │   responding)       │   failed)               │
│                │  model_provider     │  plugin_state           │
│                │  platform_type      │  channel_type           │
│                │  compression_level  │  auth_method            │
└────────────────┴─────────────────────┴─────────────────────────┘
```

### 5.2 Executor Classification

```
┌────────────────────────────────────────────────────────────────────┐
│                    EXECUTOR TAXONOMY                                │
│                                                                    │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐      │
│  │  HUMAN   │   │  AGENT   │   │  WORKER  │   │  CLONE   │      │
│  │  #3B82F6 │   │  #10B981 │   │  #F59E0B │   │  #8B5CF6 │      │
│  └────┬─────┘   └────┬─────┘   └────┬─────┘   └────┬─────┘      │
│       │              │              │              │              │
│  HERMES:         HERMES:        HERMES:        HERMES:           │
│  • Approval      • AIAgent      • Tool reg     • N/A             │
│    callbacks     • Skill judge  • File I/O     (no clone         │
│  • Config        • Memory       • API calls     system)          │
│    decisions       nudge        • Cron jobs                      │
│                  • Content      • Session DB                     │
│                    gen                                            │
│                                                                   │
│  OPENCLAW:       OPENCLAW:      OPENCLAW:      OPENCLAW:         │
│  • Plugin dev    • Agent        • CLI entry    • N/A             │
│  • PR review       inference    • Config load  (no clone         │
│  • Security      • Skill        • Plugin disc   system)          │
│    triage          execute      • Gateway                        │
│  • Release       • Doctor         routing                        │
│    approval        diagnose     • Build/test                     │
│                                                                   │
│  SINKRA:         SINKRA:        SINKRA:        SINKRA:           │
│  • Story          • process-    • validate:    • PV mind clone   │
│    approval         discoverer    yaml           evaluates       │
│  • Business       • architect-  • validate:      checkpoints     │
│    decisions        designer      squads       • Methodology     │
│  • Checkpoint     • quality-    • pre-push       replication     │
│    review           gatekeeper    hooks                          │
│                   • copy-chief  • CI workflows                   │
│                   • (all 473)   • runner-lib                     │
│                                                                   │
└────────────────────────────────────────────────────────────────────┘
```

---

## 6. Integration Interfaces

### 6.1 The Five Bridges

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   BRIDGE 1: Message Protocol (L1↔L2)                                │
│   ═══════════════════════════════════                                │
│   OpenClaw Gateway ──OpenAI JSON──► Hermes AIAgent                  │
│   (Both already use OpenAI-compatible format — ZERO friction)       │
│                                                                     │
│   BRIDGE 2: Tool Discovery (L2↔L1)                                  │
│   ═══════════════════════════════════                                │
│   Hermes Tools ──MCP Server──► OpenClaw mcporter ──► OC Runtime     │
│   (Hermes is bidirectional MCP — server already exists)             │
│                                                                     │
│   BRIDGE 3: Skill Sync (L2↔L1)                                     │
│   ═══════════════════════════════════                                │
│   Hermes Skills ──converter──► agentskills.io ──sync──► ClawHub     │
│   (Format: Hermes JSON ↔ OpenClaw Markdown)                         │
│                                                                     │
│   BRIDGE 4: Governance Overlay (L3↔L2, L3↔L1)                      │
│   ═══════════════════════════════════                                │
│   Sinkra Constitution ──rules──► Both runtimes                      │
│   Quality Gates ──validate──► All outputs                           │
│   Task Anatomy ──structure──► All operations                        │
│   (SINKRA YAML consumed by both Python and TypeScript)              │
│                                                                     │
│   BRIDGE 5: Training Pipeline (L1→L2→L3)                           │
│   ═══════════════════════════════════                                │
│   OC Conversations ──JSONL──► Hermes Batch Runner ──► RL Training   │
│   Sinkra Quality Gates ──validate──► Training data quality          │
│   (23 channels × conversations = massive training corpus)           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### 6.2 Protocol Compatibility Matrix

```
┌──────────────────┬──────────────┬──────────────┬──────────────┐
│    Protocol      │   Hermes     │   OpenClaw   │   Sinkra     │
├──────────────────┼──────────────┼──────────────┼──────────────┤
│ OpenAI Chat JSON │   ✅ Native  │   ✅ Native  │   N/A        │
│ MCP              │   ✅ Client  │   ✅ Client  │   N/A        │
│                  │   + Server   │   (mcporter) │              │
│ ACP (IDE)        │   ✅ Native  │   ✅ ACPX    │   N/A        │
│ YAML Config      │   ✅ Native  │   ✅ + zod   │   ✅ Native  │
│ SINKRA Tokens    │   ❌         │   ❌         │   ✅ Native  │
│ Plugin SDK       │   ❌         │   ✅ Native  │   N/A        │
│ Skill Format     │   JSON       │   Markdown   │   YAML+MD    │
│ Memory Format    │   Flat files │   Plugin API │   Doc Reg.   │
│ Test Framework   │   pytest     │   Vitest     │   Shell      │
└──────────────────┴──────────────┴──────────────┴──────────────┘

Green path (zero friction):  OpenAI Chat JSON — both speak it natively
Yellow path (adapter needed): Skills, Memory, Config — format converters
Red path (architectural):    SINKRA governance — requires new integration
```

---

## 7. The Flywheel

### 7.1 The Self-Reinforcing Loop

```
                    ┌─────────────────────┐
                    │  23 OpenClaw         │
                    │  Channels deliver    │◄──────────────────┐
                    │  to users            │                    │
                    └─────────┬───────────┘                    │
                              │                                │
                              │ Conversations                  │
                              ▼                                │
                    ┌─────────────────────┐                    │
                    │  Hermes Agent       │                    │
                    │  processes with     │                    │
                    │  self-improving     │                    │
                    │  intelligence       │                    │
                    └─────────┬───────────┘                    │
                              │                                │
                    ┌─────────┴──────────┐                     │
                    │                    │                     │
                    ▼                    ▼                     │
          ┌──────────────┐    ┌──────────────────┐            │
          │ Skills auto- │    │ Trajectories     │            │
          │ created from │    │ exported for     │            │
          │ experience   │    │ RL training      │            │
          └──────┬───────┘    └────────┬─────────┘            │
                 │                     │                      │
                 │                     ▼                      │
                 │           ┌──────────────────┐             │
                 │           │ Sinkra Quality   │             │
                 │           │ Gates validate   │             │
                 │           │ training data    │             │
                 │           └────────┬─────────┘             │
                 │                    │                       │
                 ▼                    ▼                       │
          ┌──────────────┐  ┌──────────────────┐             │
          │ ClawHub +    │  │ Better models    │             │
          │ agentskills  │  │ from RL training │             │
          │ marketplace  │  └────────┬─────────┘             │
          └──────┬───────┘           │                       │
                 │                   │                       │
                 │                   ▼                       │
                 │          ┌──────────────────┐             │
                 └─────────►│ Deploy improved  │─────────────┘
                            │ models + skills  │
                            │ back to all      │
                            │ 23 channels      │
                            └──────────────────┘

              EACH CYCLE:
              • More conversations (from 23 channels)
              • → Better skills (auto-created by Hermes)
              • → Better training data (validated by Sinkra)
              • → Better models (from RL pipeline)
              • → Better responses (deployed everywhere)
              • → More conversations (users stay engaged)
              • → REPEAT
```

### 7.2 Flywheel Metrics

| Cycle | Input | Process | Output | Compound Effect |
|:-----:|-------|---------|--------|----------------|
| 1 | User conversations | Hermes processes | Responses + trajectories | Baseline |
| 2 | Trajectories | RL training | Improved model | +5% response quality |
| 3 | Better responses | More user engagement | More conversations | +10% volume |
| 4 | More conversations | More skill creation | Richer skill library | +15% capability |
| 5 | Richer skills | Better task handling | Higher satisfaction | +20% retention |
| N | Compounding... | All layers improve | Network effects | Exponential |

**Key insight:** Without Sinkra's quality gates, the flywheel can amplify errors (bad trajectories → worse models). Governance is the **brake that makes the flywheel safe to accelerate.**

---

## 8. Business Model Mapping

### 8.1 How It Serves 4 Businesses

```
┌─────────────────────────────────────────────────────────────────────┐
│                   SINKRA HUB (Governance)                           │
│                                                                     │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌────────────┐│
│  │  AllFluence   │ │    AIOX      │ │  Academia    │ │  Billion   ││
│  │  L0-L4       │ │  L0-L4       │ │  Lendaria    │ │  L0-L4     ││
│  │              │ │              │ │  L0-L4       │ │            ││
│  │  Channels:   │ │  Channels:   │ │  Channels:   │ │  Channels: ││
│  │  WhatsApp    │ │  Telegram    │ │  Discord     │ │  Email     ││
│  │  Instagram   │ │  Slack       │ │  WhatsApp    │ │  WhatsApp  ││
│  │  Telegram    │ │  Discord     │ │  Telegram    │ │  Telegram  ││
│  │              │ │              │ │              │ │            ││
│  │  ┌────────┐ │ │  ┌────────┐ │ │  ┌────────┐ │ │ ┌────────┐ ││
│  │  │ Hermes │ │ │  │ Hermes │ │ │  │ Hermes │ │ │ │ Hermes │ ││
│  │  │ Brain  │ │ │  │ Brain  │ │ │  │ Brain  │ │ │ │ Brain  │ ││
│  │  │(learns │ │ │  │(learns │ │ │  │(learns │ │ │ │(learns │ ││
│  │  │ THIS   │ │ │  │ THIS   │ │ │  │ THIS   │ │ │ │ THIS   │ ││
│  │  │business│ │ │  │business│ │ │  │business│ │ │ │business│ ││
│  │  │ only)  │ │ │  │ only)  │ │ │  │ only)  │ │ │ │ only)  │ ││
│  │  └────────┘ │ │  └────────┘ │ │  └────────┘ │ │ └────────┘ ││
│  └──────────────┘ └──────────────┘ └──────────────┘ └────────────┘│
│                                                                     │
│  DATA ISOLATION: Each Hermes instance learns ONLY its business.     │
│  Sinkra's L0-L4 workspace governs what knowledge each brain sees.   │
│  Cross-business intelligence goes through squads, never directly.   │
│                                                                     │
│  SHARED: Models (RL-trained), Skills (marketplace), Tools (plugins) │
│  ISOLATED: Memory (per-business), Context (L0-L4), Users (Honcho)  │
└─────────────────────────────────────────────────────────────────────┘
```

### 8.2 Revenue Model Alignment

| Layer | Revenue Source | Current State |
|-------|--------------|---------------|
| L1 Distribution (OpenClaw) | Channel reach → user acquisition | 23+ channels × 4 businesses |
| L2 Intelligence (Hermes) | Self-improvement → user retention | Agent gets better → users stay |
| L3 Governance (Sinkra) | Multi-business → shared products | 33/33/33 split on shared products |

---

## 9. Coverage Analysis

### 9.1 Total Capability Space

```
                    SINGLE           PAIR              TRIPLE

Hermes alone:       ████████████████░░░░░░░░░░░░░░░░░░  62%
OpenClaw alone:     ██████████████████░░░░░░░░░░░░░░░░  72%
Sinkra alone:       █████████░░░░░░░░░░░░░░░░░░░░░░░░░  45%

Hermes + OpenClaw:  ██████████████████████████████░░░░░  93%
Hermes + Sinkra:    ████████████████████████░░░░░░░░░░░  78%
OpenClaw + Sinkra:  ██████████████████████████░░░░░░░░░  85%

ALL THREE:          █████████████████████████████████░░  97%
                                                         │
                                                    3% = uncovered
                                                    (mainly: native
                                                     RL hardware,
                                                     real-time voice
                                                     in governance)
```

### 9.2 What Each Adds to the Pair

| When You Add... | To the Pair... | You Gain... | Coverage Jump |
|-----------------|---------------|-------------|:-------------:|
| **Sinkra** | H + OC (93%) | Governance, business isolation, quality gates, task anatomy | 93% → 97% (+4%) |
| **Hermes** | OC + S (85%) | Self-improvement, RL pipeline, Honcho memory, 6 backends | 85% → 97% (+12%) |
| **OpenClaw** | H + S (78%) | 23 channels, native apps, 93 plugins, 1,584 contributors | 78% → 97% (+19%) |

**OpenClaw adds the most to any pair** — because distribution reach is the hardest to replicate. But Hermes adds the most *unique* value — self-improvement can't be bought, only built.

---

## 10. Implementation Priority

### Phase 0: Foundation (Weeks 1-2)
- Skill format converter (Hermes JSON ↔ OpenClaw MD)
- Memory bridge adapter (MEMORY.md ↔ memory-core)
- SINKRA squad definition for Hermes (`squads/hermes-intelligence/config.yaml`)

### Phase 1: Brain-Body (Weeks 3-8)
- Hermes as OpenClaw provider plugin (`@openclaw/hermes-provider`)
- Trajectory JSONL exporter from OpenClaw conversations
- SINKRA quality gates on training data

### Phase 2: Governed Intelligence (Weeks 9-16)
- Honcho as OpenClaw memory plugin (`@openclaw/memory-honcho`)
- Unified skill marketplace (agentskills.io + ClawHub API sync)
- Per-business Hermes instances under Sinkra workspace governance

### Phase 3: Full Flywheel (Weeks 17-24)
- RL training pipeline from 23-channel corpus
- Self-improvement loop in OpenClaw TypeScript runtime
- Unified governance dashboard (Sinkra monitors all layers)

---

## Appendix: Diagram Sources

All diagrams in this document are ASCII-based for maximum portability. For rendered versions:

| Diagram | Mermaid Source | Render Command |
|---------|---------------|----------------|
| Three-Layer Stack | `architecture-vision.mmd` | `d2 architecture-vision.d2 architecture-vision.svg` |
| Data Flow | `data-flow.mmd` | Generate via `squads/sinkra-squad/scripts/generate-pipeline-diagram.js` |
| Flywheel | `flywheel.mmd` | `d2 flywheel.d2 flywheel.svg` |

Color convention follows SINKRA executor taxonomy:
- Human: `#3B82F6` (blue)
- Agent: `#10B981` (green)
- Worker: `#F59E0B` (amber)
- Clone: `#8B5CF6` (violet)
- Gate: `#EF4444` (red)

---

*Generated by bench-analyst@spy | Architecture Vision v1.0 | 2026-04-04*
*Data sources: 3 local clones, 2 benchmarks, 2 SINKRA maps, 1 synergy analysis*
