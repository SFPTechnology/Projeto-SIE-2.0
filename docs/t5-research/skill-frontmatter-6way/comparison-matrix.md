# Skill Frontmatter Patterns — 8-Way Benchmark

**Date:** 2026-04-06
**Subjects:** Sinkra Hub, OpenClaw, BMAD-METHOD, GSD-2, Hermes Agent, Paperclip, Spec-Kit, Claude Code Source
**Method:** Source code extraction and frontmatter analysis
**Analyst:** claude-code-mastery (skill-craftsman + Explore agents)

---

## 1. Scope

Comparative analysis of SKILL.md and agent frontmatter patterns across 8 projects to identify best practices, gaps, and adoption opportunities for Sinkra Hub.

| Project | Skills | Agents | Architecture |
|---------|--------|--------|-------------|
| Sinkra Hub | 89 | 249 | Hub-and-spoke, multi-business |
| OpenClaw | 72+ | 0 | Marketplace (official CC plugin ecosystem) |
| BMAD-METHOD | 15+ | 0 | Workflow-driven (multi-step skills with steps/) |
| GSD-2 | 23+ | 5 | CLI product (headless build orchestrator) |
| Hermes Agent | 50+ | 0 | Python agent framework (non-CC native) |
| Paperclip | 11 | 0 | Agent company platform (multi-agent coordination) |
| Spec-Kit | 9 | 0 | Specification toolkit (template-driven workflows) |
| Claude Code (source) | N/A | N/A | Reference implementation (TypeScript) |

---

## 2. Native CC Fields — Adoption Matrix

| Field | CC Source | Sinkra | OpenClaw | BMAD | GSD-2 | Hermes |
|-------|----------|--------|----------|------|-------|--------|
| `name` | native | YES | YES | YES | YES | YES |
| `description` | native | YES | YES | YES | YES | YES |
| `version` | native | YES | - | - | - | YES |
| `user-invocable` | native | YES | YES | - | - | - |
| `allowed-tools` | native | - | YES | - | YES | - |
| `model` | native | - | - | - | YES | - |
| `effort` | native | YES | - | - | - | - |
| `context` | native | removed* | - | - | - | - |
| `agent` | native | YES | - | - | - | - |
| `paths` | native | - | - | - | - | - |
| `shell` | native | - | - | - | - | - |
| `hooks` | native | - | - | - | - | - |
| `arguments` | native | - | - | - | - | - |
| `argument-hint` | native | - | - | - | YES** | - |
| `when_to_use` | native | - | - | - | - | - |
| `disable-model-invocation` | native | - | - | - | - | - |
| `maxTurns` | native | YES | - | - | - | - | - | - |
| `memory` | native (agents) | - | - | - | YES | - | - | - |

\* Removed `context: "conversation"` (invalid value) in Story 117.3. No skills currently use `context: fork`.
\** GSD-2 uses `metadata.argument-hint` inside metadata, not as top-level field.

**Paperclip and Spec-Kit** use only `name` + `description` as native CC fields. Both extend with proprietary fields (see section 3).

---

## 3. Proprietary Extensions — Per Project

### Sinkra Hub (AIOX extensions)
```yaml
owner_squad: "squad-name"      # Governance: which squad owns this skill
sinkra_tier: "Tier1"           # Governance: Tier1/Tier2/Tier3
```
- Placed at root level (not namespaced under metadata)
- CC runtime ignores these (pass-through)

### OpenClaw (marketplace extensions)
```yaml
metadata:
  openclaw:
    emoji: "icon"
    homepage: "url"
    requires:
      bins: [binary1, binary2]     # Required CLI binaries (AND logic)
      anyBins: [bin1, bin2]        # Required CLI binaries (OR logic)
      config: [path1, path2]       # Required config files
    os: [darwin, linux]            # OS restrictions
    install:
      - id: "brew"
        kind: "brew"               # brew | go | npm | uv
        formula: "package-name"
        bins: [resulting-binary]
        label: "Human-readable label"
```
- Namespaced under `metadata.openclaw`
- Focus: dependency management and installation

### BMAD-METHOD (workflow extensions)
```yaml
# In SKILL.md — minimal (name + description only)
# In workflow.md — workflow-specific fields:
main_config: "{project-root}/_bmad/bmm/config.yaml"
outputFile: "{planning_artifacts}/output.md"
validateWorkflow: "./steps-v/step-v-01-discovery.md"
context_file: ""
```
- Skills are minimal; complexity lives in workflow.md and step files
- Strict validation rules (SKILL-01 through SKILL-07, STEP-01 through STEP-07)
- Description MUST contain "Use when..." clause (enforced)

### GSD-2 (CLI product extensions)
```yaml
license: "MIT"
metadata:
  openclaw:                        # Inherited OpenClaw pattern
    requires:
      bins: [gsd]
    install:
      kind: "node"
      package: "gsd-pi"
      bins: [gsd]
  author: "author-name"
  version: "1.0.0"
  argument-hint: "<file-or-pattern>"
```
- Inherits OpenClaw metadata pattern for some skills
- Uses `allowed-tools` natively for browser automation scoping
- Agent .md files use `tools`, `model`, `memory` fields

### Hermes Agent (Python framework extensions)
```yaml
author: "author-name"
license: "MIT"
platforms: [macos, linux, windows]
category: "security"
dependencies: [package1, package2]
triggers:
  - "investigate this repository"
  - "check for supply chain compromise"
toolsets: [terminal, web, file, delegation]
metadata:
  hermes:
    tags: [tag1, tag2]
    related_skills: [skill1, skill2]
    category: "devops"
    homepage: "url"
    fallback_for_toolsets: [web]      # Show when web tools unavailable
    requires_toolsets: [terminal]     # Show only when terminal available
    fallback_for_tools: [web_search]  # Show when web_search unavailable
    requires_tools: [terminal]       # Show only when terminal available
required_environment_variables:
  - name: "API_KEY"
    prompt: "Enter your API key"
    help: "Get it from https://..."
    secret: true
setup:
  help: "Setup instructions"
  collect_secrets:
    - env_var: "TOKEN"
      prompt: "Enter token"
      provider_url: "https://..."
      secret: true
```
- Most advanced extension system
- Conditional activation based on toolset/tool availability
- Built-in secret management with prompts
- Explicit trigger phrases for routing

### Paperclip (agent company extensions)
```yaml
# Minimal: name + description only (multiline with >)
# No version, no tags, no metadata
# Key pattern: descriptions include "Do NOT use for..." negative cases
# Symlink architecture: .agents/skills/ and skills/ symlinked into .claude/skills/
```
- Ultra-minimal frontmatter (only name + description)
- Descriptions include explicit negative triggers ("Do NOT use for...")
- Skills organized across 3 directories with symlinks for deduplication

### Spec-Kit (template-driven workflow extensions)
```yaml
# Command templates (not standard SKILL.md, but same frontmatter concept):
description: "What the command does"
handoffs:                            # Agent-to-agent handoff definitions
  - label: "Build Technical Plan"
    agent: "speckit.plan"            # Dot-notation agent reference
    prompt: "Create a plan for..."
    send: true                       # Auto-send to next agent
scripts:                             # Platform-specific execution
  sh: "scripts/bash/script.sh --json"
  ps: "scripts/powershell/script.ps1 -Json"
agent_scripts:                       # Agent-specific update scripts
  sh: "scripts/bash/update-agent-context.sh __AGENT__"
  ps: "scripts/powershell/update-agent-context.ps1 -AgentType __AGENT__"
tools: ['github/github-mcp-server/issue_write']  # Required MCP tools
```
- Novel `handoffs` array for agent-to-agent workflow chaining
- Platform-aware scripts (bash/powershell) in frontmatter
- `send: true` for auto-routing to next agent
- `tools` array for MCP tool dependencies

---

## 4. Description Quality Patterns

| Project | Avg Length | Pattern | Trigger Clause |
|---------|-----------|---------|----------------|
| Sinkra (before fix) | 50-80 chars | Truncated mid-word | No |
| Sinkra (after fix) | 80-200 chars | Complete sentences | Some |
| OpenClaw | 100-300 chars | Action-oriented | Implicit |
| BMAD | 80-150 chars | "Use when..." enforced | YES (mandatory) |
| GSD-2 | 200-500 chars | Exhaustive trigger list | YES (extensive) |
| Hermes | 100-300 chars | Functional + separate triggers array | Via `triggers` field |

| Paperclip | 150-400 chars | "Use when..." + "Do NOT use for..." | YES (positive + negative) |
| Spec-Kit | 50-100 chars | Functional only | No |

**Best practice observed:** GSD-2 and Hermes provide the most routing-effective descriptions because they enumerate explicit trigger phrases. Paperclip adds a unique pattern: negative triggers ("Do NOT use for...") that prevent misrouting.

---

## 5. `context: fork` Usage

**Finding: Zero projects use `context: fork` in production skills.**

| Project | Fork Usage | Notes |
|---------|-----------|-------|
| Sinkra | Removed (was invalid "conversation") | All inline |
| OpenClaw | Never used | 72+ skills, all inline |
| BMAD | Never used | Workflow steps handle isolation differently |
| GSD-2 | Never used | Uses agent .md for isolation instead |
| Hermes | N/A (not CC native) | Uses own agent system |
| Paperclip | Never used | 11 skills, all inline |
| Spec-Kit | Never used | 9 commands, all inline |

**Conclusion:** Fork is a niche feature for truly stateless, argument-driven skills (e.g., PR summary with `gh` commands). Not suitable for persona/orchestration skills. **0 out of 8 projects use fork in production.**

---

## 6. `allowed-tools` Usage

| Project | Usage | Example |
|---------|-------|---------|
| OpenClaw | YES (1 skill) | `["message"]` in discord skill |
| GSD-2 | YES (1 skill) | `Bash(npx agent-browser:*)` in agent-browser |
| Others | No | — |

**Observation:** Underutilized across all projects. Could provide permission scoping without fork isolation.

---

## 7. Agent Frontmatter (agents/*.md) — Deep Comparison

Only **2 of 8 projects** use agent markdown files with frontmatter. The other 6 have no `.claude/agents/` directory.

### CC-Native Agent Fields (from source: `loadAgentsDir.ts:541-755`)

| Field | Type | Default | Purpose |
|-------|------|---------|---------|
| `name` | string | REQUIRED | Agent type identifier |
| `description` | string | REQUIRED | whenToUse — routing signal |
| `tools` | string[] | all tools | Allowlist of tools agent can use |
| `disallowedTools` | string[] | none | Blocklist (overrides allowlist) |
| `model` | string | inherit | Model override (haiku/sonnet/opus/inherit) |
| `effort` | string/int | - | Thinking effort (low/medium/high/max) |
| `permissionMode` | enum | - | default/acceptEdits/dontAsk/bypassPermissions/plan |
| `maxTurns` | int | - | Max agentic turns |
| `skills` | string[] | - | Skills to preload |
| `initialPrompt` | string | - | Text prepended to first turn |
| `memory` | enum | - | Persistent scope (user/project/local) |
| `background` | boolean | - | Always run as background task |
| `isolation` | enum | - | worktree (git isolation) |
| `color` | enum | - | UI badge color |
| `mcpServers` | array | - | MCP server references or inline defs |
| `hooks` | object | - | Session-scoped hooks |

**Note:** `context` and `agent` are **NOT recognized** in agent frontmatter (skills-only fields). CC source (`loadAgentsDir.ts`) never reads these fields from agent .md files.

### Sinkra Hub (249 agents) — Current State

```yaml
# Pattern found in ALL 249 agents:
---
name: "squad--agent-name"
description: "Agent description (Persona Name)"
context: fork          # NOT CC-native for agents — IGNORED by runtime
agent: "squad--agent-name"  # NOT CC-native for agents — IGNORED by runtime
model: opus
effort: high           # CC-native, used
maxTurns: 50           # CC-native, used
---
```

**Issues found:**
1. `context: fork` — CC runtime ignores this field in agents (only valid in skills). 249 agents have dead frontmatter
2. `agent: <name>` — Redundant copy of `name`. CC runtime ignores this field in agents
3. `description` — Many are generic/vague (e.g., "AIOX Agent (hormozi--hormozi-chief)")
4. No use of `tools` — All 249 agents get all tools (no scoping)
5. No use of `memory` — No persistent memory across sessions
6. No use of `permissionMode` — All inherit parent permissions
7. No use of `skills` — No skill preloading
8. No use of `initialPrompt` — No auto-greeting

### GSD-2 (5 agents) — CC-Native Compliant

```yaml
# Pattern 1: Specialist agent (typescript-pro, javascript-pro)
---
name: typescript-pro
description: "TypeScript specialist for advanced type system patterns..."
model: sonnet
memory: project
---

# Pattern 2: Utility agent (researcher, scout)
---
name: researcher
description: "Web researcher that finds and synthesizes current information"
tools: search-the-web, bash
---

# Pattern 3: Worker agent (worker)
---
name: worker
description: "General-purpose subagent with full capabilities, isolated context"
---
```

**Best practices from GSD-2:**
1. Zero non-native fields — strict CC compliance
2. `tools` used for scoping (researcher only gets search + bash)
3. `memory: project` for specialists that benefit from cross-session state
4. Short, actionable descriptions
5. No redundant fields

### Adoption Matrix — Agent Fields

| Field | Sinkra (249) | GSD-2 (5) | Others (0) |
|-------|-------------|-----------|------------|
| `name` | ALL | ALL | - |
| `description` | ALL | ALL | - |
| `model` | ALL (opus) | 2/5 (sonnet) | - |
| `effort` | ~200 (high) | 0 | - |
| `maxTurns` | ALL (25 or 50) | 0 | - |
| `tools` | 0 | 2/5 | - |
| `memory` | 0 | 2/5 (project) | - |
| `permissionMode` | 0 | 0 | - |
| `skills` | 0 | 0 | - |
| `initialPrompt` | 0 | 0 | - |
| `background` | 0 | 0 | - |
| `isolation` | 0 | 0 | - |
| `color` | 0 | 0 | - |
| `mcpServers` | 0 | 0 | - |
| `hooks` | 0 | 0 | - |
| `context` (dead) | ALL | 0 | - |
| `agent` (dead) | ALL | 0 | - |

### Extended Ecosystem — 12 Additional Projects Analyzed

Research identified 12 more projects with agent patterns (none were cloned locally — analysis via documentation and README):

| Project | Agents | Key Pattern | URL |
|---------|--------|-------------|-----|
| Everything Claude Code | 36 | `permissionMode`, `disallowedTools`, `memory`, MCP integration | affaan-m/everything-claude-code |
| Claude Swarm | N/A | Opus for planning + Haiku for workers, dependency-aware scheduling | affaan-m/claude-swarm |
| Pied Piper | N/A | Playbook YAML specs, agent-agent handoff with task labels | sathish316/pied-piper |
| Claude Code Agent Farm | 20-50 | Distributed lock coordination via `/coordination/` dir, stale lock detection | Dicklesworthstone/claude_code_agent_farm |
| Awesome CC Subagents | 130+ | 10 categories, auto-delegation patterns | VoltAgent/awesome-claude-code-subagents |
| Build with Claude | 117 | `tools` field for permission scoping, standardized naming | davepoon/claude-code-subagents-collection |
| 0xfurai subagents | 100+ | Minimal frontmatter (name + description + model only) | 0xfurai/claude-code-subagents |
| Awesome Claude Agents | 24 | Stack detection + auto-routing, team configurator | vijaythecoder/awesome-claude-agents |
| WSHobson agents | 48 | Enterprise orchestration with 75 plugins | wshobson/agents |
| AIRIS MCP Gateway | N/A | MCP multiplexing: 60 tools behind 7 meta-tools, 97% token reduction | agiletec-inc/airis-mcp-gateway |
| framework | 8 types | Queen-led hierarchy, 5 consensus algorithms, anti-drift safeguards | ruvnet/framework |
| Taskade MCP | N/A | OpenAPI-to-MCP conversion for agent tool generation | taskade/mcp |

### Why We Have 249 Agents (Root Cause Analysis)

**Cause:** `ide-sync-hook.js` auto-generates a `.claude/agents/{squad}--{agent}.md` projection for every agent in every squad. These are activation stubs, not configured agents.

**Evidence:** All 249 share the same template (context: fork, agent: name, model: opus, effort: high, maxTurns: 50). Zero customization per agent. Zero use of `tools`, `memory`, `permissionMode`, `skills`, `hooks`, `mcpServers`.

**What mature projects do differently:**

| Approach | Projects | Agent Count | Philosophy |
|----------|----------|-------------|-----------|
| Few, highly specialized | GSD-2, Vijaythecoder | 5-24 | Each agent is hand-crafted with specific tools, model, memory |
| Many, minimal frontmatter | 0xfurai, Build with Claude | 100-130 | Specialization via prompt body, not frontmatter fields |
| Hierarchy-based | framework, Claude Swarm | 8 types | Queen/worker topology with consensus protocols |
| Auto-generated stubs | **Sinkra Hub** | 249 | Bulk projection from squad configs (current state) |

**Conclusion:** Our 249 agents are an anti-pattern. Two better paths exist:
1. **Reduce to ~20-30 hand-crafted agents** with real `tools` scoping, `memory`, and `permissionMode` (GSD-2/Vijaythecoder approach)
2. **Keep many but minimize frontmatter** — let prompt body handle specialization, use only name + description + model (0xfurai approach)

### Agent Frontmatter Recommendations

**Phase 1: Cleanup (immediate)**
1. **Remove `context` and `agent` from all 249 agents** — Dead frontmatter ignored by CC runtime
2. **Fix generic descriptions** — "AIOX Agent (name)" is useless for routing

**Phase 2: Hardening (next story)**
3. **Add `tools` scoping** — GSD-2/Build-with-Claude pattern. Read-only agents get `tools: Read, Grep, Glob`
4. **Add `memory: project`** for long-lived specialists — architect, pm, analyst benefit from cross-session state
5. **Add `permissionMode: plan`** for auditor/reviewer agents — Prevents accidental writes

**Phase 3: Architecture decision (requires roundtable)**
6. **Decide: 249 stubs vs ~30 hand-crafted agents** — The auto-generation model produces quantity without quality. Need architectural decision on whether to keep bulk generation or curate a smaller, more capable set

---

## 8. Validation & Enforcement

| Project | Enforcement Level | Method |
|---------|------------------|--------|
| BMAD | HIGH | 14 validation rules with CRITICAL/HIGH severity |
| Sinkra | MEDIUM | validate:skill-sync, validate-skill skill |
| GSD-2 | LOW | Convention-based, no automated validation |
| OpenClaw | LOW | PR review only |
| Hermes | MEDIUM | CONTRIBUTING.md conventions, manual review |

**BMAD rules worth adopting:**
- SKILL-06: Description MUST state both what AND when (max 1024 chars)
- SKILL-07: SKILL.md must have non-empty body after frontmatter
- WF-03: Frontmatter variables must resolve to config or runtime vars

---

## 9. Recommendations for Sinkra Hub

### Adopt Now (Low Effort, High Value)
1. **Enforce "Use when..." in descriptions** — BMAD pattern. Add to validate-skill
2. **Add negative triggers ("Do NOT use for...")** — Paperclip pattern. Prevents misrouting
3. **Use `allowed-tools` for sensitive skills** — OpenClaw/GSD-2 pattern. Scope permissions inline

### Evaluate (Medium Effort)
4. **Add `handoffs` for workflow skills** — Spec-Kit pattern. Explicit agent-to-agent chaining
5. **Add `triggers` array** — Hermes pattern. Explicit trigger phrases improve routing
6. **Namespace AIOX extensions under `metadata.sinkra`** — Follow OpenClaw/Hermes convention
7. **Add `requires` field** — For skills that need external tools (whisper, gh, etc.)

### Skip (Not Applicable)
8. **`context: fork`** — No production usage found anywhere (0/8 projects). Keep all inline
9. **`platforms`** — We're macOS-only for now
10. **`setup.collect_secrets`** — We use .env, not skill-level secrets
11. **`scripts.sh/ps`** — Spec-Kit pattern, but CC native hooks handle this better

---

## 10. Source References

| Project | Path | Files Analyzed |
|---------|------|---------------|
| Sinkra Hub | `/Users/oalanicolas/Code/sinkra-hub/.claude/skills/` | 89 SKILL.md |
| OpenClaw | `/Users/oalanicolas/Code/openclaw/.claude/skills/` | 72+ SKILL.md |
| BMAD-METHOD | `/Users/oalanicolas/Code/BMAD-METHOD/` | 15+ SKILL.md |
| GSD-2 | `/Users/oalanicolas/Code/gsd-2/src/resources/skills/` | 23+ SKILL.md |
| Hermes Agent | `/Users/oalanicolas/Code/hermes-agent/optional-skills/` | 50+ SKILL.md |
| Paperclip | `/Users/oalanicolas/Code/paperclip/` | 11 SKILL.md |
| Spec-Kit | `/Users/oalanicolas/Code/spec-kit/templates/commands/` | 9 command .md |
| CC Source | `/Users/oalanicolas/Code/claude-code-main/src/` | TypeScript source |
