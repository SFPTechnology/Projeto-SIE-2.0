# Deep Dive: Skills, Internals & Enriched Data

**Source:** Inventory agent deep analysis | **Confidence:** High

---

## Skills Ecosystem Comparison

### Hermes Agent: 116 Built-in Skills (73 core + 43 optional)

**Core skills (73 across 26 categories):** Apple Notes, GitHub, Obsidian, coding workflows, RL training skills, and more. Skills are JSON-based procedural memory that the agent can auto-create from experience.

**Optional skills (43 across 14 categories):** Extended integrations installed via `hermes skills`.

**Key property:** Skills self-improve during use. The agent can autonomously create new skills after completing complex tasks.

**Distribution:** Skills Hub at agentskills.io (open standard).

### OpenClaw: 53 Bundled Skills

**Bundled skills (53):** 1Password, Apple Notes, Obsidian, GitHub, Notion, Trello, Spotify, Discord, Slack, coding-agent, and more.

**Distribution:** ClawHub at clawhub.ai (marketplace model).

**Key property:** Skills are static — created manually, not auto-generated.

| Metric | Hermes | OpenClaw |
|--------|--------|----------|
| Total bundled skills | 116 | 53 |
| Auto-creation from experience | ✅ | ❌ |
| Self-improvement during use | ✅ | ❌ |
| Marketplace | agentskills.io | clawhub.ai |
| Format | JSON-based procedural | Markdown-based |

**Paridade:** `4/5` — Hermes advantage. 2.2x more skills AND self-creation capability.

---

## Core Agent Internals

### Hermes Agent Core Files (by LOC)

| File | Lines | Purpose |
|------|------:|---------|
| `run_agent.py` | 8,948 | AIAgent class — core conversation loop |
| `cli.py` | 8,280 | HermesCLI — interactive TUI |
| `trajectory_compressor.py` | 1,518 | Trajectory compression for RL |
| `batch_runner.py` | 1,285 | Parallel batch processing |
| `hermes_state.py` | 1,270 | SQLite session store + FTS5 |
| `mcp_serve.py` | 868 | MCP server (expose conversations) |
| `toolsets.py` | 641 | Toolset composition |
| `model_tools.py` | 466 | Tool orchestration + dispatch |
| **Total core** | **~23,276** | |

**Note:** Hermes is a **single-agent** system. `run_agent.py` contains the entire AIAgent class. Subagent delegation is done via `tools/delegate_tool.py` which spawns isolated AIAgent instances.

### OpenClaw Core Modules

| Module | Files | Purpose |
|--------|------:|---------|
| `src/commands/` | 325 | All CLI commands |
| `src/cli/` | 180 | CLI wiring |
| `src/channels/` | ~80 | Core channel implementations |
| `src/plugins/` | ~40 | Plugin discovery, loader, registry |
| `src/plugin-sdk/` | 50+ | Public SDK with 50+ subpath exports |
| `src/gateway/` | ~30 | Gateway + protocol |
| `src/agents/` | ~20 | Agent runtime |
| `src/hooks/` | ~15 | Hook system |

**Note:** OpenClaw's agent logic is distributed across `src/commands/agent.ts`, `src/agents/`, and plugin hooks. Not a single class but a pipeline.

---

## MCP Support Comparison

| Feature | Hermes | OpenClaw |
|---------|--------|----------|
| MCP Client | ✅ `tools/mcp_tool.py` (~1050 LOC) | ✅ via `mcporter` bridge |
| MCP Server | ✅ `mcp_serve.py` (expose messaging) | ❌ |
| IDE MCP passthrough | ✅ ACP passes editor MCP servers to agent | ✅ via ACPX extension |
| MCP approach | Native (both client + server) | Bridge model (decoupled) |

**Hermes is bidirectional MCP** — both consumes and exposes. OpenClaw consumes only via bridge.

---

## RL / Research Infrastructure Detail

### Hermes Agent

| Component | Files | Purpose |
|-----------|------:|---------|
| `environments/` | 12+ | Atropos-compatible RL environments |
| `environments/hermes_swe_env/` | — | SWE-bench environment |
| `environments/terminal_test_env/` | — | Terminal testing environment |
| `environments/benchmarks/` | 3 | tblite, terminalbench_2, yc_bench |
| `environments/tool_call_parsers/` | 11 | Model-specific parsers (DeepSeek, GLM, Kimi, Llama, Mistral, Qwen, etc.) |
| `batch_runner.py` | 1,285 | Parallel processing with checkpointing |
| `trajectory_compressor.py` | 1,518 | Compress trajectories for training |
| `mini_swe_runner.py` | ~600 | SWE-bench compatible runner |
| `rl_cli.py` | ~400 | RL training CLI |
| `datagen-config-examples/` | — | Dataset generation configs |

### OpenClaw

None. Zero research/training infrastructure.

---

## Configuration Complexity

### Hermes

- `cli-config.yaml.example`: **41,060 bytes** — extensive config with versioned migration (currently version 5)
- `.env.example`: **16,085 bytes** — comprehensive env vars
- Config managed via `hermes_cli/config.py` with `DEFAULT_CONFIG` dict

### OpenClaw

- `package.json`: 206 npm scripts
- 40+ vitest config files for scoped testing
- Config schema validated with zod
- Drift detection via SHA-256 hashes
- `openclaw config set` + `openclaw doctor --fix` for config management

---

## CI/CD Comparison

### Hermes (6 workflows)

| Workflow | Purpose |
|----------|---------|
| tests | Test suite |
| docker-publish | Docker image |
| deploy-site | Docs site |
| docs-site-checks | Doc validation |
| nix | Nix build |
| supply-chain-audit | Dependency security |

### OpenClaw (13 workflows)

| Workflow | Purpose |
|----------|---------|
| ci.yml | Main CI |
| codeql.yml | CodeQL security |
| docker-release.yml | Docker release |
| install-smoke.yml | Install smoke tests |
| macos-release.yml | macOS app release |
| openclaw-npm-release.yml | npm release |
| plugin-clawhub-release.yml | ClawHub release |
| plugin-npm-release.yml | Plugin npm release |
| sandbox-common-smoke.yml | Sandbox tests |
| stale.yml | Issue management |
| workflow-sanity.yml | Self-validation |
| auto-response.yml | Auto-responses |
| labeler.yml | PR labeling |

**Paridade:** `2/5` — OpenClaw has 2.2x more CI workflows with broader coverage.

---

## Unique Hermes Feature: Mixture of Agents

`tools/mixture_of_agents_tool.py` — sends the same prompt to multiple LLMs and synthesizes the results. This is absent in OpenClaw.

## Unique Hermes Feature: Skin Engine

4 built-in skins + user YAML skins. Data-driven theming for:
- Banner colors
- Spinner faces/verbs/wings (KawaiiSpinner)
- Tool prefix
- Response box
- Branding text

## Unique OpenClaw Feature: Canvas

Live, controllable rendering surface (`src/canvas-host/`, `a2ui` system). Agent can render interactive UI elements. No equivalent in Hermes.

## Unique OpenClaw Feature: 11 AGENTS.md Boundary Files

Progressive architectural disclosure — each subsystem has its own boundary guide:
- Root, extensions, plugin-sdk, channels, plugins, gateway/protocol, gateway/server-methods, test/helpers, docs templates, zh-CN docs

---

*Generated by bench-analyst inventory enrichment | 2026-04-04*
