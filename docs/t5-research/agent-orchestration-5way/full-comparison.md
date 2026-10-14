# Agent Orchestration 5-Way Benchmark

**BMAD-METHOD vs Paperclip vs GSD-2 vs CrewAI vs Get-Shit-Done (GSD-1)**

**Date:** 2026-04-04
**Analyst:** bench-analyst@spy
**Data Source:** Local clone analysis + SINKRA-MAP pipeline outputs + domain-decoder extractions (High Confidence)
**Methodology:** Exhaustive inventory of every agent orchestration, governance, and workflow practice in each repo, cross-referenced with SINKRA-MAP architecture.json, compliance_score.json, and score_card.json artifacts

---

## 1. Project Identity

| | **BMAD-METHOD** | **Paperclip** | **GSD-2** | **CrewAI** | **GSD-1** | **Sinkra Hub** |
|--|:-:|:-:|:-:|:-:|:-:|:-:|
| **Purpose** | AI Dev Methodology | AI Agent Control Plane | Autonomous Coding Agent | Agent Crew Orchestration | Spec-Driven Dev System | AI Orchestration Framework |
| **Version** | v6.2.2 | Latest (MIT) | v2.62.0 | v0.86.0 | v1.32.0 | v2.1 (Private) |
| **Primary Language** | JavaScript | TypeScript | TypeScript | Python | Node.js (CLI + SDK) | TS + Python + Shell + YAML |
| **License** | MIT | MIT | MIT | MIT | MIT | Private |
| **Agents** | ~8 (PM, Dev, Architect, etc.) | Dynamic per company | 1 agent + session dispatch | User-defined via YAML | 3 (Planner, Executor, Verifier) | 473 across 53 squads |
| **Bounded Contexts** | 6 | 5 | 4 | 7 | 5 | 8 layers |
| **Orchestration Pattern** | Pipeline + Quick Flow | Control plane + heartbeat | State machine + dispatch | Kickoff sync + delegation | Waves + phase verification | SINKRA compositional hierarchy |
| **Docs Site** | docs.bmad-method.org (Astro) | paperclip.ing/docs | gsd-build.github.io | docs.crewai.com | GitHub docs/ | None (CLI-first) |
| **i18n** | FR + ZH + VI | None | None | None | PT-BR + ZH-CN + JA-JP + KO-KR | PT-BR |
| **Community** | Discord | Discord | Discord | Discourse + Discord | Discord | Private (4 businesses) |
| **SINKRA Score** | **82/100** | **82/100** | **74/100** | **81/100** | N/A (incomplete) | N/A (is the reference) |
| **SINKRA Verdict** | MAP-READY | MAP-READY | REVIEW | MAP-READY | INCOMPLETE | Reference framework |

---

## 2. Agent Orchestration Practices -- Complete Practice-by-Practice Comparison

### 2.1 Agent Definition & Identity

| Practice | BMAD | Paperclip | GSD-2 | CrewAI | GSD-1 | Sinkra Hub |
|----------|:-:|:-:|:-:|:-:|:-:|:-:|
| **Named agent personas** | ✅ ~8 (Mary, John, Winston, Amelia, Sally, Murat) | ✅ Dynamic per company (CEO, CTO, IC, Manager) | ❌ Single agent, session dispatch | ✅ User-defined (role + goal + backstory) | ✅ 3 named (Planner, Executor, Verifier) | ✅ **473 agents** |
| **Role-based specialization** | ✅ By product lifecycle phase | ✅ By org role (title + reportsTo) | ⚠️ By unit type (plan/execute/verify) | ✅ By YAML role declaration | ✅ By function (plan/execute/verify) | ✅ By squad domain |
| **Agent config format** | Markdown skills + YAML manifests | TypeScript + DB schema | TypeScript dispatch tables | **YAML (agents.yaml)** | Markdown workflows + agents/ | Markdown + YAML config.yaml |
| **Dynamic agent creation** | ❌ Fixed set per module | ✅ Create agents at runtime | ❌ Single agent | ✅ Instantiate from YAML/code | ❌ Fixed set | ⚠️ Squad scaffolding (not runtime) |
| **Agent personality/backstory** | ✅ Per agent description | ✅ Title + department + role | ❌ No personality layer | ✅ **backstory field** (richest) | ⚠️ Agent role descriptions | ✅ Agent markdown descriptions |
| **Multi-model support** | ⚠️ IDE-dependent | ✅ Any provider via heartbeat | ✅ **Dynamic model routing** (cost + capability) | ✅ **LiteLLM** (broadest model support) | ⚠️ Runtime-dependent | ✅ Gateway-AI router |
| **Party/collaboration mode** | ✅ **Party Mode** (unique) | ✅ Org chart collaboration | ❌ | ✅ Crew collaboration | ❌ | ✅ Squad parallel delegation |

### 2.2 Task & Workflow Model

| Practice | BMAD | Paperclip | GSD-2 | CrewAI | GSD-1 | Sinkra Hub |
|----------|:-:|:-:|:-:|:-:|:-:|:-:|
| **Unit of work** | Story (from epics) | Issue (with checkout) | Unit (plan/execute/verify slice) | Task (desc + expected output) | Task in Plan Waves | Task (SINKRA 8-field anatomy) |
| **Task anatomy fields** | ⚠️ Implicit (story template) | ✅ Issue schema + status machine | ✅ **8 fields** (state-derived) | ✅ **6 fields** (desc, expected_output, agent, tools, context, output) | ✅ Must-haves + criteria | ✅ **8 mandatory fields** |
| **Pre/post conditions** | ⚠️ Readiness gate only | ⚠️ Status transitions | ✅ **15/15 tasks** with pre/post | ✅ Per-task via Pydantic | ✅ Phase completeness | ✅ **All tasks** with pre/post |
| **Error handling per task** | ❌ | ✅ Retry + fallback | ✅ **strategy + max_retries + fallback + alert_on_failure** | ✅ Guardrails with retry | ✅ Gap routing + replanning | ✅ Per-task error handling |
| **Acceptance criteria** | ✅ DoD per story | ⚠️ Implicit in issue | ✅ Per-task acceptance criteria | ✅ expected_output validation | ✅ Must-haves in plan | ✅ **Per-task ACs in stories** |
| **Task replay** | ❌ | ❌ | ❌ | ✅ **Task replay** (unique) | ❌ | ❌ |
| **Conditional tasks** | ⚠️ Quick Flow as branch | ✅ Status-based routing | ✅ Conditional dispatch branches | ✅ **ConditionalTask** class | ⚠️ Gate-based branching | ✅ Conditional edges in DAG |
| **DAG validation** | ❌ | ❌ | ✅ **0 cycles, validated** | ✅ Topological sort | ❌ | ✅ **DAG validation in all maps** |

### 2.3 Orchestration Patterns

| Practice | BMAD | Paperclip | GSD-2 | CrewAI | GSD-1 | Sinkra Hub |
|----------|:-:|:-:|:-:|:-:|:-:|:-:|
| **Sequential pipeline** | ✅ Step-files just-in-time | ✅ Status machine | ✅ Dispatch table | ✅ **Default mode** | ✅ Phase sequence | ✅ Workflow definitions |
| **Hierarchical orchestration** | ⚠️ Gates between phases | ✅ **Org chart hierarchy** (reportsTo) | ❌ | ✅ **Manager Agent mode** | ❌ | ✅ Chief parallel delegation |
| **Event-driven flows** | ❌ | ✅ Heartbeat runtime | ❌ | ✅ **Flows with listeners AND/OR** | ❌ | ⚠️ Event bus (limited) |
| **State machine** | ❌ | ✅ Issue status machine | ✅ **Full state machine** (gsd.db + .gsd/) | ❌ | ✅ STATE.md derived | ⚠️ Squad state (manual) |
| **Delegation between agents** | ⚠️ Handoff via artifacts | ✅ Chain of command | ❌ | ✅ **Native delegation** (allow_delegation) | ❌ | ✅ Chief-to-specialist delegation |
| **Pipeline branching** | ✅ Quick Flow alt-path | ⚠️ Priority routing | ✅ Conditional branches | ✅ ConditionalTask | ⚠️ Quick mode | ✅ SINKRA conditional edges |
| **Autonomous mode** | ❌ (human-driven) | ✅ 24/7 autonomous | ✅ **`gsd auto` walk-away** | ⚠️ Kickoff only | ✅ **`/gsd autonomous`** | ⚠️ Runner-based |
| **Manager dashboard** | ❌ | ✅ **React UI dashboard** | ✅ VS Code extension + Web UI | ❌ | ✅ `/gsd-manager` mode | ❌ (CLI-first) |
| **SDK/headless mode** | ✅ npx install (CLI) | ✅ API server | ✅ **Pi SDK headless** | ✅ Python API | ✅ **GSD SDK headless** | ✅ Squad-engine API |

### 2.4 Communication & Handoff

| Practice | BMAD | Paperclip | GSD-2 | CrewAI | GSD-1 | Sinkra Hub |
|----------|:-:|:-:|:-:|:-:|:-:|:-:|
| **Handoff mechanism** | Artifacts in `_bmad-output/` | REST API + Published Language | Filesystem state (`.gsd/`) | In-process objects + context | `.planning/` artifacts | **Formal handoff artifacts** |
| **Cross-domain handoff** | ⚠️ Implicit via artifacts | ✅ ACL for plugins/routines | ⚠️ State-derived | ⚠️ Task context chain | ⚠️ STATE.md updates | ✅ **QG-CROSS-01 enforced** |
| **Context passing** | ✅ project-context.md | ✅ Company context | ✅ Fresh session + injected context | ✅ **task.context from previous outputs** | ✅ CONTEXT.md per phase | ✅ SYNAPSE 8-layer context |
| **Published language** | ✅ workflow-map.md | ✅ Shared types | ✅ JSON-RPC for remote surfaces | ✅ **YAML as published language** | ✅ Markdown artifacts | ✅ Token registry + composition rules |
| **Human-in-the-loop** | ✅ Workflow checkpoints | ✅ Board approvals | ✅ Pause for review | ✅ **human_input=True on tasks** | ✅ UAT conversational | ✅ Elicitation points |
| **Inter-agent memory** | ✅ Shared artifacts | ⚠️ DB-mediated | ❌ Fresh sessions (by design) | ✅ **Memory + Knowledge subsystems** | ✅ `.planning/` shared | ✅ Journey-log + file-service |

### 2.5 Quality Gates & Governance

| Practice | BMAD | Paperclip | GSD-2 | CrewAI | GSD-1 | Sinkra Hub |
|----------|:-:|:-:|:-:|:-:|:-:|:-:|
| **Quality gates count** | 15 | 14 | 9 | 11 | ~5 (UAT, verify, schema) | **15+ per squad** |
| **Numeric thresholds** | ✅ **15/15 gates** | ✅ **14/14 gates** | ✅ **9/9 gates** | ✅ **11/11 gates** | ⚠️ Partial | ✅ All gates |
| **Veto power gates** | ✅ 5 gates | ✅ 12 gates | ✅ 3 gates | ✅ 5 gates | ❌ | ✅ Per-gate veto |
| **Readiness gate** | ✅ **Mandatory** before implementation | ⚠️ Implicit in status | ⚠️ Milestone validation | ❌ | ⚠️ Plan checker | ✅ Story validation |
| **Budget enforcement** | ❌ | ✅ **Hard-stop budget** (unique) | ⚠️ Cost tracking alerts | ❌ | ❌ | ❌ |
| **Board/approval system** | ❌ | ✅ **Formal Board approvals** (unique) | ❌ | ❌ | ❌ | ⚠️ CODEOWNERS |
| **Artifact contracts** | ✅ PRD 9 mandatory sections | ✅ Schema Drizzle + shared types | ✅ Append-only Decisions Register | ✅ **Output JSON/Pydantic schema** | ✅ Plan structure validation | ✅ Artifact classification rules |
| **Constitution/governance doc** | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ **322-line constitution** |
| **Agent authority matrix** | ❌ | ✅ Chain of command | ❌ | ❌ | ❌ | ✅ **Exclusive ops per agent** |
| **Story-driven enforcement** | ✅ DoD per story | ❌ | ❌ | ❌ | ❌ | ✅ **Commit hook WARN** |
| **Guardrails with retry** | ❌ | ❌ | ✅ Auto-fix + retry | ✅ **Guardrail + retry loop** | ❌ | ❌ |
| **10 Mandamentos compliance** | ✅ **10/10 PASS** | ⚠️ **7 PASS + 3 MAP-GAP** | ✅ **10/10 PASS** | ⚠️ **9 PASS + 1 REVIEW** | N/A | ✅ Reference framework |

### 2.6 Context Management

| Practice | BMAD | Paperclip | GSD-2 | CrewAI | GSD-1 | Sinkra Hub |
|----------|:-:|:-:|:-:|:-:|:-:|:-:|
| **Context persistence** | ✅ `_bmad-output/` artifacts | ✅ Database (PostgreSQL) | ✅ `.gsd/` + gsd.db (SQLite) | ⚠️ In-memory + optional ChromaDB | ✅ `.planning/` filesystem | ✅ Workspace L0-L4 + outputs/ |
| **Context freshness** | ⚠️ Manual refresh | ✅ Heartbeat-driven | ✅ **Fresh session per unit** (anti-rot) | ⚠️ No explicit freshness | ⚠️ STATE.md sync | ✅ **TTL governance (5 layers)** |
| **Context injection** | ✅ project-context.md | ✅ Company context + agent context | ✅ **Pre-loaded at dispatch time** | ✅ Crew inputs + task context | ✅ CONTEXT.md per phase | ✅ **SYNAPSE 8-layer engine** |
| **Context window management** | ⚠️ Step-files (implicit) | ❌ | ✅ **Session clearing between units** | ✅ **Summarize on overflow** | ✅ Context rot mitigation | ⚠️ Partial (skill boundaries) |
| **Knowledge system** | ❌ | ❌ | ❌ | ✅ **Knowledge + RAG (ChromaDB)** | ❌ | ⚠️ Document Registry |
| **Memory persistence** | ✅ Artifact-based | ✅ Database-based | ✅ DB + filesystem | ✅ **Short/Long/Entity memory** | ✅ Filesystem-based | ✅ Journey-log |
| **State reconciliation** | ❌ | ⚠️ DB-driven | ✅ **Derive from DB + filesystem + git** | ❌ | ✅ `state validate` + `state sync` | ⚠️ Config drift detection |
| **Context rot prevention** | ⚠️ fresh-chat discipline | ❌ | ✅ **Core design principle** | ✅ Summarize on overflow | ✅ **Primary product goal** | ⚠️ Partial |

### 2.7 Parallelism & Concurrency

| Practice | BMAD | Paperclip | GSD-2 | CrewAI | GSD-1 | Sinkra Hub |
|----------|:-:|:-:|:-:|:-:|:-:|:-:|
| **Native parallelism** | ❌ | ✅ Concurrent routines | ✅ **Parallel milestones + worktree isolation** | ✅ **Async tasks + Flow listeners** | ✅ **Tasks within waves** | ✅ Swarm-execute parallel |
| **Isolation mechanism** | ❌ | ✅ Company-scoped isolation | ✅ **Git worktree per milestone** | ❌ (in-process) | ✅ Branch/worktree | ✅ Squad boundaries |
| **Concurrency control** | ❌ | ✅ Coalescing policy | ✅ **Locks + heartbeats** | ❌ | ⚠️ Flag-based | ⚠️ Task-mode locking |
| **Wave-based execution** | ❌ | ❌ | ✅ Dispatch groups | ❌ | ✅ **Plan waves** (core concept) | ✅ Wave-execute epic pipeline |
| **Runtime adapter** | ⚠️ Multi-IDE (Claude Code, Cursor) | ✅ **6+ adapters** (OpenClaw, Claude, Codex, Cursor, Bash, HTTP) | ❌ (Pi SDK only) | ❌ (Python only) | ✅ **14+ runtimes** (broadest) | ⚠️ Claude Code primary |

### 2.8 Security & Safety

| Practice | BMAD | Paperclip | GSD-2 | CrewAI | GSD-1 | Sinkra Hub |
|----------|:-:|:-:|:-:|:-:|:-:|:-:|
| **Multi-tenant isolation** | ❌ | ✅ **Company scoping** (strongest) | ❌ | ❌ | ❌ | ✅ **4-business L0-L4 isolation** |
| **Budget/cost control** | ❌ | ✅ **Hard-stop per agent/run** | ✅ Budget alerts + model routing by cost | ❌ | ❌ | ❌ |
| **Prompt injection protection** | ❌ | ❌ | ❌ | ❌ | ✅ **Scanner** (unique among 5) | ❌ |
| **Path traversal protection** | ❌ | ❌ | ❌ | ❌ | ✅ **Protection** (unique) | ❌ |
| **Fetch safety (IP blocking)** | ❌ | ❌ | ✅ **Block private IPs** | ❌ | ❌ | ❌ |
| **Shell metachar protection** | ❌ | ❌ | ❌ | ❌ | ✅ **Protection** | ❌ |
| **Sandbox for tools** | ❌ | ❌ | ❌ | ✅ Tool sandbox | ❌ | ❌ |
| **RPM controller** | ❌ | ❌ | ❌ | ✅ **Rate limiting** | ❌ | ❌ |
| **Advisory hooks** | ❌ | ❌ | ❌ | ❌ | ✅ **Advisory safety hooks** | ✅ PreToolUse hooks |
| **Checkout atomicity** | ❌ | ✅ **Atomic issue checkout** | ❌ | ❌ | ❌ | ❌ |
| **Append-only audit** | ✅ stepsCompleted frontmatter | ❌ | ✅ **Decisions Register** | ❌ | ❌ | ✅ Journey-log |

### 2.9 Infrastructure & Deployment

| Practice | BMAD | Paperclip | GSD-2 | CrewAI | GSD-1 | Sinkra Hub |
|----------|:-:|:-:|:-:|:-:|:-:|:-:|
| **Installation method** | `npx bmad-method install` | `pnpm install` + server | `npm install -g gsd-pi` | `pip install crewai` | `npx get-shit-done-cc` | `npm install` (monorepo) |
| **Server component** | ❌ (file-based) | ✅ **Node.js server + React UI** | ⚠️ VS Code extension | ❌ (library) | ❌ (CLI) | ✅ Apps (squad-engine, gateway-ai) |
| **Database** | ❌ | ✅ **PostgreSQL** (embedded or external) | ✅ SQLite (gsd.db) | ⚠️ SQLite (logs) + ChromaDB (knowledge) | ❌ | ⚠️ Supabase (per business) |
| **Docker support** | ❌ | ✅ Docker + Playwright smoke | ✅ Docker (overhauled) | ❌ | ❌ | ❌ |
| **VS Code extension** | ❌ | ❌ | ✅ **Full extension** (status bar, file decorations, tree) | ❌ | ❌ | ❌ |
| **Web UI** | ❌ | ✅ **React dashboard** | ✅ **Web UI** (dark mode, auth) | ❌ | ❌ | ❌ |
| **Telemetry** | ❌ | ❌ | ✅ Metrics + audit log | ✅ **OpenTelemetry + AgentOps** | ❌ | ✅ SYNAPSE engine-usage |
| **Crash recovery** | ❌ | ❌ | ✅ **Lock recovery + state rebuild** | ❌ | ❌ | ❌ |
| **Release automation** | ✅ npm publish + Discord | ✅ **Canary auto + stable manual** | ✅ npm publish | ✅ PyPI publish | ✅ npm publish | ❌ Manual |
| **Rollback** | ❌ | ✅ **rollback-latest.sh** | ❌ | ❌ | ❌ | ❌ |

### 2.10 Business Rules Density

Data sourced from domain-decoder pipeline extractions and deep-research comparison.

| Metric | BMAD | Paperclip | GSD-2 | CrewAI | GSD-1 | Sinkra Hub |
|--------|:-:|:-:|:-:|:-:|:-:|:-:|
| **Total extracted rules** | 35 | 25 | 36 | 24 | ~25+ | 100+ |
| **Rule categories** | 8 families | 6 families | 7 families | 5 families | 4+ families | 15+ families |
| **Complexity rating** | High | Very High | High | Medium | High | Very High |
| **Key rule families** | Config, DocScan, PRD Quality, Classification, Sprint, Story DoD, Workflow, Brainstorm | Governance, Org, Approvals, Work, Labels, Budget | Workflow, Decisions/State, Git/Delivery, Parallel, Verification, Routing, CI/CD | Agent Identity, Task Contract, Crew Orchestration, Flow Runtime, Project Scaffold | Safety, Planning, Execution, Verification | Constitution, Agent Authority, TTL, Artifact, Story, CODEOWNERS, SINKRA Composition |
| **Unique rule strength** | PRD quality (9 mandatory sections) + information density discipline | **Budget hard-stop** + multi-tenant governance | **Parallelism isolation** (9 rules) + model routing (6 rules) | **Flow runtime** (event-driven state) | **Safety rules** (6 attack types covered) | **Constitutional enforcement** (11 articles) |

---

## 3. SINKRA Compatibility Matrix

Scores from SINKRA-MAP pipeline (sinkra-qa agent, score_card.json).

| Dimension | Max | BMAD | Paperclip | GSD-2 | CrewAI | GSD-1 |
|-----------|:---:|:----:|:---------:|:-----:|:------:|:-----:|
| **Four Executors** | 15 | 8 | 11 | 8 | 12 | N/A |
| **Compositional Hierarchy** | 15 | 10 | 12 | 15 | 15 | N/A |
| **Task-First** | 15 | 10 | 12 | 12 | 15 | N/A |
| **Tokens** | 12 | 6 | 9 | 7 | 7 | N/A |
| **Domains** | 10 | 10 | 10 | 10 | 10 | N/A |
| **Quality Gates** | 12 | 9 | 10 | 8 | 8 | N/A |
| **10 Mandamentos** | 15 | 10 | 10 | 10 | 9 | N/A |
| **Meta-Axiomas** | 10 | 9 | 6 | 2 | 5 | N/A |
| **Infrastructure** | 10 | 10 | 2 | 2 | 0 | N/A |
| **Overall** | **100** | **82** | **82** | **74** | **81** | **N/A** |
| **Verdict** | | MAP-READY | MAP-READY | REVIEW | MAP-READY | INCOMPLETE |

### Key SINKRA Findings

| Project | Strengths | Gaps |
|---------|-----------|------|
| **BMAD** | Best Meta-Axiomas (7.83/10 compliance), full infrastructure mapping (10/10), 10/10 Mandamentos | Token families limited (2/9), four executors missing Clone justification |
| **Paperclip** | Highest Four Executors (11/15), strong hierarchy (12/15), robust task anatomy | Infrastructure scaffold empty (2/10), 3 Mandamentos in MAP-GAP (schemas, KPIs, handoffs) |
| **GSD-2** | Perfect compositional hierarchy (15/15), 10/10 Mandamentos, robust DAG | META_AXIOMAS VETO (parsing bug, not design), infrastructure empty (2/6), token families incomplete |
| **CrewAI** | Perfect hierarchy + task-first (15/15 each), best four executors (12/15) | Infrastructure completely empty (0/10), Mandamento 6 (KPIs) in REVIEW, token families incomplete |
| **GSD-1** | Pipeline stopped at Phase 5 -- architecture mapped but no quality gates, compliance, or score card | Cannot be scored -- needs pipeline completion |

### Compliance Score (Phase 6 META_AXIOMAS)

| Dimension | BMAD | Paperclip | GSD-2 | CrewAI |
|-----------|:----:|:---------:|:-----:|:------:|
| Truthfulness | 8.0 | 8.2 | 8.5 | 7.5 |
| Coherence | 8.5 | 7.5 | 8.8 | 9.0 |
| Strategic Alignment | 8.0 | 8.0 | 8.0 | 8.0 |
| Operational Excellence | 7.5 | 7.0 | 7.8 | 7.5 |
| Innovation Capacity | 7.0 | 7.2 | 7.5 | 7.0 |
| Risk Management | 7.0 | 6.2 | 7.8 | 7.0 |
| Resource Optimization | 8.0 | 7.0 | 8.2 | 8.5 |
| Stakeholder Value | 8.5 | 7.5 | 8.0 | 8.0 |
| Sustainability | 7.5 | 6.1 | 7.5 | 7.0 |
| Adaptability | 7.5 | 6.5 | 7.2 | 7.5 |
| **Overall** | **7.83** | **7.18** | **8.05** | **7.92** |
| **Compliance %** | **78.3%** | **71.8%** | **80.5%** | **79.2%** |

---

## 4. Gap Summary Per Project

### 4.1 What Each Project Does That Nobody Else Does

#### BMAD: 5 Exclusive Practices

| # | Practice | Detail |
|---|----------|--------|
| 1 | **Party Mode** | Multiple agent personas collaborating in one session |
| 2 | **Scale-Domain-Adaptive planning** | Automatically adjusts depth based on project complexity |
| 3 | **Module ecosystem** (BMM, BMB, TEA, BMGD, CIS) | Extensible methodology with domain-specific modules |
| 4 | **bmad-help routing agent** | Context-aware "what's next" guidance |
| 5 | **Information density discipline** | Micro-file architecture with mandatory artifact density |

#### Paperclip: 6 Exclusive Practices

| # | Practice | Detail |
|---|----------|--------|
| 1 | **Budget hard-stop per agent/run** | Only framework with financial governance |
| 2 | **Org chart hierarchy (reportsTo)** | Full organizational simulation with chain of command |
| 3 | **Board approval system** | Formal governance with Board as authority |
| 4 | **Atomic issue checkout** | Prevents concurrent work on same issue |
| 5 | **Company-scoped multi-tenant** | Each company is isolated with own agents, budget, org |
| 6 | **Clipmart templates** (coming soon) | Pre-built company templates for download |

#### GSD-2: 6 Exclusive Practices

| # | Practice | Detail |
|---|----------|--------|
| 1 | **Capability-based model routing** | Dynamic model selection by capability metadata + cost |
| 2 | **Fresh session per unit** (context rot prevention) | Clears context window between tasks by design |
| 3 | **Crash recovery with lock rebuild** | Resumes from any crash state automatically |
| 4 | **VS Code extension** (full) | Status bar, file decorations, session tree, conversation history |
| 5 | **Fetch safety (IP blocking)** | Blocks private IP access in tool calls |
| 6 | **RPC protocol v2** | Typed init handshake with version detection |

#### CrewAI: 5 Exclusive Practices

| # | Practice | Detail |
|---|----------|--------|
| 1 | **Task replay** | Re-execute specific tasks from saved state |
| 2 | **Flow listeners with AND/OR** | Event-driven state machine for complex workflows |
| 3 | **Knowledge + RAG system** (ChromaDB) | Embedded knowledge base with retrieval |
| 4 | **Short/Long/Entity memory** | Three-tier memory system for agents |
| 5 | **Training mode** | Train agents with human feedback |

#### GSD-1: 4 Exclusive Practices

| # | Practice | Detail |
|---|----------|--------|
| 1 | **Prompt injection scanner** | Only framework with explicit prompt injection defense |
| 2 | **Path traversal protection** | Prevents agents from accessing unauthorized paths |
| 3 | **14+ runtime support** | Broadest runtime compatibility (Claude Code, Codex, Copilot, Cursor, Gemini, etc.) |
| 4 | **4-language README** (PT-BR, ZH-CN, JA-JP, KO-KR) | Most i18n of any framework in the set |

### 4.2 Sinkra Hub Gaps by Source

#### From BMAD (5 gaps)

| # | Practice | What Sinkra Lacks | Priority |
|---|----------|--------------------|:--------:|
| BM-1 | Party Mode | Multi-agent collaboration in single session | P3 |
| BM-2 | Scale-adaptive planning | Auto-adjust depth by project complexity | P2 |
| BM-3 | Module ecosystem | Extensible methodology modules | P3 |
| BM-4 | bmad-help routing | Context-aware "what's next" agent | P2 |
| BM-5 | Track selection policy engine | Formal full-vs-quick flow eligibility | P2 |

#### From Paperclip (7 gaps)

| # | Practice | What Sinkra Lacks | Priority |
|---|----------|--------------------|:--------:|
| PC-1 | Budget hard-stop | Cost control per agent/run/squad | P1 |
| PC-2 | Org chart hierarchy | reportsTo chain for agent authority | P3 |
| PC-3 | Board approval system | Formal multi-stakeholder approvals | P2 |
| PC-4 | React dashboard UI | Visual monitoring of agent work | P2 |
| PC-5 | Heartbeat runtime | Agent liveness monitoring | P2 |
| PC-6 | Atomic checkout | Prevent concurrent work on same task | P1 |
| PC-7 | Rollback script | Safe release reversal | P1 |

#### From GSD-2 (7 gaps)

| # | Practice | What Sinkra Lacks | Priority |
|---|----------|--------------------|:--------:|
| GS-1 | Capability-based model routing | Dynamic model selection by capability + cost | P1 |
| GS-2 | Fresh session per unit | Context window clearing between tasks | P1 |
| GS-3 | Crash recovery | Automatic resume from any crash state | P1 |
| GS-4 | VS Code extension | IDE integration with status, tree, history | P3 |
| GS-5 | Fetch safety | Block private IP access | P2 |
| GS-6 | State machine with DB | Derived state from DB + filesystem + git | P2 |
| GS-7 | Worktree isolation per milestone | Git worktree for parallel execution | P2 |

#### From CrewAI (6 gaps)

| # | Practice | What Sinkra Lacks | Priority |
|---|----------|--------------------|:--------:|
| CR-1 | Task replay | Re-execute specific tasks from saved state | P2 |
| CR-2 | Flow listeners (AND/OR) | Event-driven state machine for workflows | P2 |
| CR-3 | Knowledge + RAG | Embedded knowledge base with retrieval | P2 |
| CR-4 | Three-tier memory | Short/Long/Entity memory system | P2 |
| CR-5 | Guardrails with retry loop | Post-execution validation with auto-retry | P1 |
| CR-6 | YAML agent declaration | Declarative agent definition | P3 |

#### From GSD-1 (5 gaps)

| # | Practice | What Sinkra Lacks | Priority |
|---|----------|--------------------|:--------:|
| GD-1 | Prompt injection scanner | Defense against prompt injection attacks | P1 |
| GD-2 | Path traversal protection | Prevent unauthorized path access | P1 |
| GD-3 | 14+ runtime support | Broad runtime compatibility | P3 |
| GD-4 | Schema drift detection | Detect ORM changes missing migrations | P2 |
| GD-5 | Goal-backward verification | Verify claims against code and objectives | P2 |

---

## 5. Quantitative Scorecard

| Metric | BMAD | Paperclip | GSD-2 | CrewAI | GSD-1 | Sinkra Hub |
|--------|:----:|:---------:|:-----:|:------:|:-----:|:----------:|
| **Orchestration practices** | 18 | 21 | 22 | 19 | 17 | **28** |
| **Quality gates** | 15 | 14 | 9 | 11 | ~5 | 15+ |
| **Extracted business rules** | 35 | 25 | 36 | 24 | ~25 | 100+ |
| **Exclusive practices** | 5 | 6 | 6 | 5 | 4 | **16** |
| **SINKRA Score** | 82 | 82 | 74 | 81 | N/A | Reference |
| **Compliance Score** | 78.3% | 71.8% | 80.5% | 79.2% | N/A | Reference |
| **Runtime adapters** | 2+ IDEs | 6+ | 1 (Pi SDK) | 1 (Python) | **14+** | 1 (Claude Code) |
| **Memory/persistence** | File | DB | DB + File | Memory + DB + RAG | File | File + DB |
| **Security practices** | 1 | 3 | 2 | 2 | **5** | 3 |
| **Parallelism support** | None | Routines | **Worktree isolation** | Async tasks | Waves | Swarm |

---

## 6. Verdict by Category

| Category | Leader | Why |
|----------|--------|-----|
| **Agent Definition** | **Sinkra Hub** | 473 agents across 53 squads -- unmatched scale |
| **Task Model** | **CrewAI = GSD-2** | Both have 8-field anatomy with pre/post conditions |
| **Orchestration Patterns** | **Paperclip** | Only one with org hierarchy + heartbeat + dashboard + API |
| **Quality Gates** | **BMAD** | 15 gates, all with numeric thresholds, 5 with veto power |
| **Context Management** | **GSD-2** | Fresh sessions per unit solves context rot structurally |
| **Parallelism** | **GSD-2** | Worktree isolation per milestone with locks and heartbeats |
| **Security** | **GSD-1** | Only framework with prompt injection + path traversal defense |
| **Budget/Cost** | **Paperclip** | Hard-stop budget enforcement -- nobody else has this |
| **Runtime Support** | **GSD-1** | 14+ runtimes -- broadest compatibility |
| **Infrastructure** | **Paperclip** | Full stack: server, DB, React UI, Docker, rollback |
| **Business Rules Density** | **Sinkra Hub** | 100+ rules across 15+ families |
| **SINKRA Compatibility** | **BMAD = Paperclip** | Both at 82/100 MAP-READY |
| **Compliance Rigor** | **GSD-2** | Highest META_AXIOMAS overall (8.05/10) |
| **Governance** | **Sinkra Hub** | 322-line constitution, agent authority matrix, TTL governance |

---

## 7. The Composite Ideal

If you could combine the best of each project:

```
IDEAL = Sinkra Hub Governance (constitution, agent authority, TTL, 473 agents)
      + Paperclip Infrastructure (server, DB, React UI, budget, org chart, rollback)
      + GSD-2 Execution Engine (fresh sessions, crash recovery, model routing, worktree isolation)
      + CrewAI Composition API (YAML agents, task replay, knowledge/RAG, flow listeners)
      + BMAD Methodology (party mode, scale-adaptive, module ecosystem, artifact discipline)
      + GSD-1 Security (prompt injection, path traversal, 14+ runtimes)

Total unique practices: ~90+
```

No single project has more than 28 (Sinkra Hub in orchestration practices). The composite ideal has 90+. There is massive opportunity for cross-pollination across the ecosystem.

---

*Generated by bench-analyst@spy | 5-Way Agent Orchestration Benchmark | 2026-04-04*
*Data sources: 5 local clones, SINKRA-MAP pipeline artifacts, domain-decoder extractions, deep-research comparison*
