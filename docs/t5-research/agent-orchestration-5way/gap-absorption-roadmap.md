# Gap Absorption Roadmap

**30 agent orchestration practices to absorb from BMAD, Paperclip, GSD-2, CrewAI, and GSD-1**

**Date:** 2026-04-04
**Source:** Agent Orchestration 5-Way Benchmark

---

## Priority Matrix

### Wave 1 -- Immediate (P1, <1 day each, 8 items)

| # | Source | Practice | Effort | ROI |
|---|--------|----------|:------:|:---:|
| 1 | GSD-2 | **Fresh session per unit** | 2-3d | Eliminate context rot in long squad executions |
| 2 | GSD-2 | **Crash recovery with state rebuild** | 2-3d | Resume any runner from crash without data loss |
| 3 | GSD-1 | **Prompt injection scanner** | 1d | Prevent adversarial prompt attacks on agent inputs |
| 4 | GSD-1 | **Path traversal protection** | 1d | Prevent agents from reading/writing unauthorized paths |
| 5 | Paperclip | **Rollback script** | 2h | Safe release reversal for packages and deploys |
| 6 | CrewAI | **Guardrails with retry loop** | 1d | Post-execution validation with auto-retry before failing |
| 7 | Paperclip | **Atomic task checkout** | 1d | Prevent concurrent agents from working on same task |
| 8 | GSD-2 | **Capability-based model routing** | 2-3d | Dynamic model selection by capability + cost for Gateway-AI |

**Total effort:** ~12-15 days
**Impact:** Security hardening + execution resilience + cost optimization

---

### Wave 2 -- Short-term (P2, 1-2 weeks each, 11 items)

| # | Source | Practice | Effort | ROI |
|---|--------|----------|:------:|:---:|
| 9 | Paperclip | **Budget tracking per squad/run** | 1w | Visibility into LLM costs per execution |
| 10 | BMAD | **Scale-adaptive planning depth** | 1w | Auto-adjust story complexity by scope analysis |
| 11 | BMAD | **Context-aware routing agent** | 3-5d | "What's next" guidance for new users/agents |
| 12 | BMAD | **Track selection policy engine** | 3-5d | Formal eligibility rules for quick vs full flow |
| 13 | Paperclip | **Board/multi-stakeholder approvals** | 1w | Formal approval workflows for cross-business decisions |
| 14 | Paperclip | **Heartbeat liveness monitoring** | 1w | Detect and alert on stalled/dead agents |
| 15 | CrewAI | **Task replay from saved state** | 1w | Re-execute specific tasks without re-running pipeline |
| 16 | CrewAI | **Flow event listeners (AND/OR)** | 1w | Event-driven workflow orchestration patterns |
| 17 | CrewAI | **Knowledge + RAG integration** | 1-2w | Embedded knowledge base for squad agents |
| 18 | GSD-2 | **State machine with DB backing** | 1-2w | Derived state from DB + filesystem + git |
| 19 | GSD-1 | **Goal-backward verification** | 1w | Verify claims against code and stated objectives |

**Total effort:** ~10-14 weeks
**Impact:** Agent intelligence + workflow flexibility + cost visibility + knowledge management

---

### Wave 3 -- Medium-term (P2-P3, weeks to months, 7 items)

| # | Source | Practice | Effort | ROI |
|---|--------|----------|:------:|:---:|
| 20 | Paperclip | **React dashboard UI** | 2-4w | Visual monitoring of squad execution and agent status |
| 21 | GSD-2 | **Worktree isolation per squad execution** | 2-3w | Git worktree for parallel squad runs |
| 22 | CrewAI | **Three-tier memory (Short/Long/Entity)** | 2-3w | Persistent agent memory across sessions |
| 23 | GSD-2 | **Fetch safety (block private IPs)** | 2-3d | Network-level protection for tool calls |
| 24 | GSD-1 | **Schema drift detection** | 1w | Detect ORM changes missing migrations |
| 25 | BMAD | **Party Mode (multi-agent single session)** | 2-3w | Multiple agent personas collaborating live |
| 26 | Paperclip | **Org chart hierarchy (reportsTo)** | 2-3w | Agent authority chain for complex squads |

**Total effort:** ~10-16 weeks
**Impact:** Observability + parallel execution + advanced agent capabilities

---

### Wave 4 -- Long-term (P3, months, 4 items)

| # | Source | Practice | Effort | Impact |
|---|--------|----------|:------:|:------:|
| 27 | GSD-1 | **14+ runtime support** | Months | Run squads on any AI runtime (Codex, Copilot, Gemini, Cursor, etc.) |
| 28 | GSD-2 | **VS Code extension** | Months | IDE-native squad execution with status bar and tree |
| 29 | BMAD | **Module ecosystem** | Months | Extensible methodology modules for domain-specific squads |
| 30 | CrewAI | **YAML declarative agent definition** | 1-2w | Simplified agent creation without markdown |

**Total effort:** Ongoing
**Impact:** Ecosystem breadth and developer experience

---

## Absorption by Category

### Security (4 items -- Wave 1-3)

| # | Practice | Source | Wave | Current State |
|---|----------|--------|:----:|:-------------:|
| 3 | Prompt injection scanner | GSD-1 | 1 | ❌ No protection |
| 4 | Path traversal protection | GSD-1 | 1 | ❌ No protection |
| 23 | Fetch safety (IP blocking) | GSD-2 | 3 | ❌ No protection |
| 24 | Schema drift detection | GSD-1 | 3 | ❌ Not implemented |

**Current security posture:** PreToolUse hooks only. No agent-input sanitization.
**After absorption:** Defense in depth against 4 attack vectors.

### Execution Resilience (4 items -- Wave 1-2)

| # | Practice | Source | Wave | Current State |
|---|----------|--------|:----:|:-------------:|
| 1 | Fresh session per unit | GSD-2 | 1 | ❌ Sessions accumulate context |
| 2 | Crash recovery | GSD-2 | 1 | ❌ Failed runs require manual restart |
| 7 | Atomic task checkout | Paperclip | 1 | ❌ No concurrency control |
| 18 | State machine with DB | GSD-2 | 2 | ⚠️ Manual state via YAML |

**Current resilience:** Manual recovery. No concurrency control.
**After absorption:** Automatic crash recovery, context rot prevention, safe parallel execution.

### Cost & Observability (3 items -- Wave 1-2)

| # | Practice | Source | Wave | Current State |
|---|----------|--------|:----:|:-------------:|
| 8 | Model routing by capability + cost | GSD-2 | 1 | ⚠️ Gateway-AI exists but no dynamic routing |
| 9 | Budget tracking per squad/run | Paperclip | 2 | ❌ No cost tracking |
| 14 | Heartbeat liveness monitoring | Paperclip | 2 | ❌ No agent health monitoring |

**Current observability:** SYNAPSE engine-usage.jsonl only.
**After absorption:** Cost-aware model selection, per-squad budget, agent liveness.

### Agent Intelligence (6 items -- Wave 2-3)

| # | Practice | Source | Wave | Current State |
|---|----------|--------|:----:|:-------------:|
| 15 | Task replay | CrewAI | 2 | ❌ No replay capability |
| 16 | Flow event listeners | CrewAI | 2 | ❌ No event-driven workflows |
| 17 | Knowledge + RAG | CrewAI | 2 | ⚠️ Document Registry exists |
| 22 | Three-tier memory | CrewAI | 3 | ⚠️ Journey-log partial |
| 25 | Party Mode | BMAD | 3 | ❌ One agent per session |
| 19 | Goal-backward verification | GSD-1 | 2 | ⚠️ Story ACs exist but no claim verification |

**Current intelligence:** Stateless agents with artifact-based handoff.
**After absorption:** Persistent memory, knowledge retrieval, event-driven flows, claim verification.

---

## Suggested Epic

These 30 gaps form **Epic 113 -- Agent Orchestration Absorption** with 4 waves matching the priority matrix above.

**Wave 1:** 8 stories, ~12-15d -- Sprint 1-2
**Wave 2:** 11 stories, ~10-14w -- Sprints 3-8
**Wave 3:** 7 stories, ~10-16w -- Sprints 9-14
**Wave 4:** 4 stories, ongoing -- Continuous improvement

**Estimated total SP:** ~120-150 SP across 30 stories.

---

## Quick Win ROI: Wave 1 Only

If you implement only Wave 1 (12-15 days of work):

| Metric | Before | After Wave 1 |
|--------|:------:|:------------:|
| Context rot mitigation | None | Fresh session per unit |
| Crash recovery | Manual restart | Automatic state rebuild |
| Prompt injection defense | None | Scanner active |
| Path traversal defense | None | Protection active |
| Release safety | No rollback | Rollback script |
| Post-execution validation | Manual | Guardrails + retry |
| Concurrent task safety | None | Atomic checkout |
| Model cost optimization | Fixed model | Capability-based routing |
| **Practices absorbed** | 0/30 | **8/30 (27%)** |

---

## Cross-Reference with Quality Engineering Benchmark

This roadmap complements the Quality Engineering 4-Way Benchmark (see `docs/bench/quality-engineering-4way/gap-absorption-roadmap.md`). The two roadmaps are orthogonal:

| Benchmark | Focus | Gaps | Overlap |
|-----------|-------|:----:|:-------:|
| Quality Engineering 4-Way | CI/CD, testing, linting, formatting, observability | 34 | 0 |
| Agent Orchestration 5-Way | Agent patterns, workflows, security, parallelism, cost | 30 | 0 |
| **Combined** | **Full-spectrum** | **64** | **0** |

Zero overlap. Implementing both roadmaps absorbs 64 practices from 7 external projects (OpenClaw, BMAD, Paperclip, GSD-2, CrewAI, GSD-1).

---

*Generated from 5-Way Agent Orchestration Benchmark | 2026-04-04*
