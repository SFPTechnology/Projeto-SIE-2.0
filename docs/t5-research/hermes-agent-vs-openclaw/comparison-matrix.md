# Comparison Matrix: Hermes Agent vs OpenClaw

**Date:** 2026-04-04 | **Type:** Codebase | **Source:** Local Clone (High Confidence)

---

## 1. Identity & Philosophy

| Dimension | Hermes Agent | OpenClaw |
|-----------|-------------|----------|
| **Tagline** | "The self-improving AI agent" | "Personal AI assistant you run on your own devices" |
| **Organization** | Nous Research (AI research lab) | Community-driven + corporate sponsors (OpenAI, GitHub, NVIDIA, Vercel) |
| **Language** | Python 3.11+ | TypeScript (Node 24+ / Bun) |
| **License** | MIT | MIT |
| **Core Philosophy** | Self-improving loop, research-ready, model-agnostic | Plugin-first, channel-first, security-conscious |
| **Primary Focus** | Learning & skill creation from experience | Multi-platform assistant with plugin ecosystem |
| **Origin** | Purpose-built by Nous Research | Evolved from personal project (Warelay → Clawdbot → Moltbot → OpenClaw) |

**Paridade:** `3/5` — Equivalente parcial. Both are personal AI assistants with messaging gateways, but philosophical DNA diverges significantly.

---

## 2. Scale & Maturity

| Metric | Hermes Agent | OpenClaw | Delta |
|--------|-------------|----------|-------|
| **Commits** | 3,207 | 26,602 | OC +8.3x |
| **Contributors** | 202 | 1,584 | OC +7.8x |
| **Python/TS files** | 681 .py | 9,601 .ts/.tsx | OC +14x |
| **Lines of code** | ~301K | ~1.84M | OC +6.1x |
| **Test files** | 400 | 3,534 | OC +8.8x |
| **Latest release** | v2026.4.3 (Apr 3) | v2026.4.2 (Apr 2) | Both active |
| **Release cadence** | 7 major releases (v0.1–v0.7) | Calendar versioning (vYYYY.M.D) | OC more frequent |
| **Native apps** | None | macOS, iOS, Android (608 Swift, 134 Kotlin) | OC exclusive |
| **Documentation files** | 438 .md | 889 .md | OC +2x |

**Paridade:** `2/5` — OpenClaw is significantly larger and more mature by every quantitative measure.

---

## 3. Architecture

| Dimension | Hermes Agent | OpenClaw |
|-----------|-------------|----------|
| **Pattern** | Monolith with module separation | Monorepo with plugin architecture |
| **Entry point** | `cli.py` (CLI), `gateway/run.py` (gateway) | `src/entry.ts` (CLI), gateway daemon |
| **Agent loop** | Synchronous `while` loop in `run_agent.py` | Async event-driven in `src/commands/agent.ts` |
| **Message format** | OpenAI-compatible (`role: system/user/assistant/tool`) | OpenAI-compatible |
| **Tool dispatch** | Central `tools/registry.py` → handler functions | Plugin SDK + tool registration |
| **Plugin system** | Toolsets (composable tool groups) + memory providers | Full plugin SDK (`openclaw/plugin-sdk/*`) with manifest, lifecycle, typed contracts |
| **Config format** | YAML (`~/.hermes/config.yaml`) | JSON/YAML + zod schema validation |
| **Config management** | `hermes config set` + setup wizard | `openclaw config set` + onboard wizard |
| **Extension model** | Tools register via `registry.register()` at import time | npm packages with `openclaw.plugin.json` manifest |
| **SDK boundary** | No formal SDK boundary | Strict `plugin-sdk/*` boundary with import guards |

**Paridade:** `3/5` — Both functional, but OpenClaw has significantly more mature architecture boundaries and plugin contracts.

---

## 4. Agent Loop & Intelligence

| Feature | Hermes Agent | OpenClaw |
|---------|-------------|----------|
| **Self-improving loop** | ✅ Creates skills from experience, improves during use | ❌ No autonomous skill creation |
| **Skill system** | ✅ Procedural memory, Skills Hub (agentskills.io), auto-create | ✅ Skills + ClawHub marketplace |
| **Skill marketplace** | agentskills.io (open standard) | ClawHub (clawhub.ai) |
| **Memory nudges** | ✅ Agent nudges itself to persist knowledge | ❌ No self-nudging |
| **User modeling** | ✅ Honcho dialectic user modeling | ✅ Memory plugins |
| **Session search** | ✅ FTS5 + LLM summarization cross-session | ✅ Memory search |
| **Context compression** | ✅ Auto-compression with pressure detection | ✅ Context management |
| **Prompt caching** | ✅ Anthropic prompt caching support | ✅ Prompt cache stability (strict byte-level) |
| **Subagent delegation** | ✅ Isolated subagents for parallel workstreams | ✅ Agent delegation |
| **Max iterations** | 90 (configurable) | Configurable |
| **Thinking/reasoning** | ✅ Reasoning blocks preserved across tool turns | ✅ `--thinking high` flag |
| **Batch processing** | ✅ `batch_runner.py` for parallel trajectory generation | ❌ No batch runner |
| **RL training** | ✅ Atropos RL environments, trajectory compression | ❌ No RL infrastructure |
| **Smart model routing** | ✅ `smart_model_routing.py` with fallback | ✅ Model failover with auth rotation |

**Paridade:** `4/5` — Hermes advantage in self-improvement and research infrastructure. OpenClaw matches on core agent capabilities.

---

## 5. Messaging Platforms & Channels

### Hermes Agent Gateway Platforms (16)

| Platform | Status |
|----------|--------|
| Telegram | ✅ Full (bot commands, menus, media) |
| Discord | ✅ Full |
| Slack | ✅ Full |
| WhatsApp | ✅ Full |
| Signal | ✅ Full |
| Email | ✅ |
| DingTalk | ✅ |
| Feishu/Lark | ✅ |
| Matrix | ✅ |
| Mattermost | ✅ |
| Home Assistant | ✅ |
| SMS | ✅ |
| WeCom | ✅ |
| Webhook (generic) | ✅ |
| API Server (Open WebUI) | ✅ |
| Telegram Network | ✅ (multi-bot) |

### OpenClaw Channel Plugins (23+)

| Platform | Status |
|----------|--------|
| WhatsApp | ✅ (web) |
| Telegram | ✅ |
| Slack | ✅ |
| Discord | ✅ |
| Google Chat | ✅ |
| Signal | ✅ |
| iMessage | ✅ |
| BlueBubbles | ✅ |
| IRC | ✅ |
| Microsoft Teams | ✅ |
| Matrix | ✅ |
| Feishu/Lark | ✅ |
| LINE | ✅ |
| Mattermost | ✅ |
| Nextcloud Talk | ✅ |
| Nostr | ✅ |
| Synology Chat | ✅ |
| Tlon | ✅ |
| Twitch | ✅ |
| Zalo | ✅ |
| Zalo Personal | ✅ |
| WeChat | ✅ |
| WebChat | ✅ |
| QQ Bot | ✅ |
| Voice Call | ✅ |

**Paridade:** `3/5` — OpenClaw wins on raw channel count (23+ vs 16). Hermes has unique platforms (Email, SMS, Home Assistant, DingTalk). OpenClaw has unique platforms (iMessage, LINE, Twitch, Nostr, Google Chat, MS Teams, Nextcloud, QQ, Voice Call).

---

## 6. Model Provider Support

| Provider | Hermes Agent | OpenClaw |
|----------|-------------|----------|
| **Anthropic** | ✅ (prompt caching, thinking blocks) | ✅ (plugin) |
| **OpenAI** | ✅ | ✅ (plugin, OAuth sponsor) |
| **OpenRouter** | ✅ (200+ models) | ✅ (plugin) |
| **Google/Gemini** | ✅ | ✅ (plugin) |
| **Groq** | ✅ | ✅ (plugin) |
| **Ollama** | ✅ | ✅ (plugin) |
| **DeepSeek** | ✅ | ✅ (plugin) |
| **Mistral** | ✅ | ✅ (plugin) |
| **MiniMax** | ✅ (M2.7 support) | ✅ (plugin) |
| **Moonshot/Kimi** | ✅ | ✅ (plugin) |
| **z.ai/GLM** | ✅ | ✅ (zai plugin) |
| **Nous Portal** | ✅ (native) | ❌ |
| **Qwen/DashScope** | ✅ | ✅ (plugin) |
| **Amazon Bedrock** | ❌ | ✅ (plugin) |
| **Azure/Microsoft** | ❌ | ✅ (plugin + Foundry) |
| **NVIDIA** | ❌ | ✅ (plugin) |
| **Hugging Face** | ❌ | ✅ (plugin) |
| **Together** | ❌ | ✅ (plugin) |
| **Perplexity** | ❌ | ✅ (plugin) |
| **xAI/Grok** | ❌ | ✅ (plugin) |
| **vLLM/SGLang** | ❌ | ✅ (plugins) |
| **BytePlus/Volcengine** | ❌ | ✅ (plugins) |
| **Venice** | ❌ | ✅ (plugin) |
| **Chutes** | ❌ | ✅ (plugin) |
| **Custom endpoints** | ✅ (auto-detect from probe) | ✅ (litellm plugin) |
| **Credential pools** | ✅ (multi-key rotation, 401 failover) | ✅ (auth profile rotation) |
| **Total providers** | ~12 native | 35 plugins |

**Paridade:** `2/5` — OpenClaw's plugin model gives it ~3x more providers. Hermes covers essentials but lacks cloud-native providers (Bedrock, Azure, NVIDIA).

---

## 7. Tools & Capabilities

### Hermes Agent Tools (49 files)

| Category | Tools |
|----------|-------|
| **Terminal** | terminal_tool, process_registry, environments (6 backends) |
| **File** | file_tools (read/write/search/patch) |
| **Web** | web_tools (search + Firecrawl), url_safety |
| **Browser** | browser_tool, browser_camofox (anti-detection) |
| **Code** | code_execution_tool (sandbox) |
| **Delegation** | delegate_tool (subagents) |
| **MCP** | mcp_tool (~1050 lines) |
| **Skills** | skill_manager_tool, skills_tool, skills_guard, skills_hub, skills_sync |
| **Memory** | memory_tool |
| **Session** | session_search_tool |
| **Vision** | vision_tools |
| **TTS/STT** | tts_tool, neutts_synth, transcription_tools |
| **Cron** | cronjob_tools |
| **Todo** | todo_tool |
| **Messaging** | send_message_tool |
| **Image Gen** | image_generation_tool |
| **RL** | rl_training_tool |
| **Home Automation** | homeassistant_tool |
| **Security** | approval, tirith_security, credential_files |

### OpenClaw Tool Plugins (24)

| Category | Plugins |
|----------|---------|
| **Browser** | browser |
| **Search** | brave, duckduckgo, exa, searxng, tavily, firecrawl |
| **Media** | image-generation-core, video-generation-core, media-understanding-core, speech-core, elevenlabs, deepgram, fal |
| **Memory** | memory-core, memory-lancedb |
| **Code** | github-copilot, opencode, opencode-go, openshell |
| **Phone** | phone-control |
| **Diff** | diffs |
| **Prose** | open-prose |
| **Voice** | talk-voice, voice-call |
| **IDE** | acpx (ACP extension), copilot-proxy, kilocode |

**Paridade:** `4/5` — Hermes has more built-in tools (49 vs 24 plugins). OpenClaw has unique capabilities (video generation, phone control, LanceDB vector memory). Hermes has unique anti-detection browser, RL training, and Home Assistant integration.

---

## 8. Terminal & Execution Backends

| Backend | Hermes Agent | OpenClaw |
|---------|-------------|----------|
| **Local** | ✅ | ✅ |
| **Docker** | ✅ | ✅ (Dockerfile + sandbox variants) |
| **SSH** | ✅ | ❌ |
| **Daytona** | ✅ (serverless persistence) | ❌ |
| **Modal** | ✅ (serverless GPU) | ❌ |
| **Singularity** | ✅ (HPC containers) | ❌ |
| **Podman** | ❌ | ✅ (openclaw.podman.env) |
| **Fly.io** | ❌ | ✅ (fly.toml) |
| **Sandbox (browser)** | ❌ | ✅ (Dockerfile.sandbox-browser) |

**Paridade:** `4/5` — Hermes advantage in execution diversity (6 backends). SSH + Modal + Daytona = "not tied to your laptop" vision. OpenClaw focuses on container-first deployment.

---

## 9. Security

| Feature | Hermes Agent | OpenClaw |
|---------|-------------|----------|
| **Command approval** | ✅ (dangerous command detection, sudo callbacks) | ✅ (command gating, allowlists) |
| **Secret exfiltration blocking** | ✅ (URL scanning, base64 detection, prompt injection) | ✅ (security-conscious defaults) |
| **Credential directory protection** | ✅ (.docker, .azure, .config/gh) | ✅ |
| **DM pairing** | ✅ (platform pairing) | ✅ (device-pair plugin) |
| **Container isolation** | ✅ (Docker, Singularity) | ✅ (Docker sandbox variants) |
| **Code sandbox** | ✅ (execute_code sandbox with redaction) | ✅ (sandbox Dockerfiles) |
| **Website policy** | ✅ (website_policy.py) | ❌ |
| **CODEOWNERS security** | ❌ | ✅ (security-focused CODEOWNERS rules) |
| **GHSA process** | ❌ | ✅ (GHSA maintainer skill) |
| **Prompt injection defense** | ✅ (secret scanning in LLM responses) | ✅ (latest-gen model recommended) |

**Paridade:** `4/5` — Both strong. Hermes has deeper runtime secret scanning. OpenClaw has more formal security governance (GHSA, CODEOWNERS).

---

## 10. Memory & Persistence

| Feature | Hermes Agent | OpenClaw |
|---------|-------------|----------|
| **Architecture** | Pluggable provider ABC | Plugin slot (one active) |
| **Built-in memory** | ✅ SQLite + FTS5 search | ✅ memory-core plugin |
| **Vector memory** | ❌ native (via Honcho) | ✅ memory-lancedb |
| **User modeling** | ✅ Honcho dialectic profiling | ✅ via memory plugins |
| **Cross-session recall** | ✅ FTS5 + LLM summarization | ✅ |
| **Memory nudges** | ✅ (agent self-nudges) | ❌ |
| **Profile isolation** | ✅ (per-host, per-peer) | ✅ |
| **Session persistence** | ✅ SessionDB (SQLite) | ✅ |
| **Memory flush state** | ✅ (prevents re-flush on restart) | ✅ |
| **Skill as memory** | ✅ (skills = procedural memory) | ✅ (skills) |

**Paridade:** `4/5` — Hermes advantage in self-nudging memory and Honcho integration. OpenClaw advantage in LanceDB vector store.

---

## 11. Developer Experience

| Feature | Hermes Agent | OpenClaw |
|---------|-------------|----------|
| **Install** | `curl | bash` one-liner | `npm install -g openclaw` |
| **Setup wizard** | `hermes setup` (interactive) | `openclaw onboard` (step-by-step) |
| **Doctor** | `hermes doctor` | `openclaw doctor` |
| **Update** | `hermes update` | `openclaw update --channel stable|beta|dev` |
| **Dev channels** | Single branch | stable / beta / dev channels |
| **Migration tool** | `hermes claw migrate` (FROM OpenClaw) | N/A |
| **IDE integration** | ACP adapter (VS Code, Zed, JetBrains) | ACPX + Copilot proxy + Kilocode |
| **CLI TUI** | Rich + prompt_toolkit (multiline, autocomplete, KawaiiSpinner) | Full TUI |
| **Skin/theme engine** | ✅ (data-driven CLI theming) | ❌ |
| **Pre-commit hooks** | ❌ | ✅ (prek install) |
| **Type checking** | Python type hints | Strict TypeScript (no `any`) |
| **Linting** | ❌ documented | Oxlint + Oxfmt |
| **Build system** | uv (pip install -e) | pnpm + Bun |
| **AGENTS.md** | ✅ (project structure guide) | ✅ (per-boundary AGENTS.md files) |

**Paridade:** `3/5` — OpenClaw has more mature DX tooling (dev channels, strict linting, boundary AGENTS.md). Hermes has unique migration tool and skin engine.

---

## 12. Testing & Quality

| Metric | Hermes Agent | OpenClaw |
|--------|-------------|----------|
| **Framework** | pytest | Vitest |
| **Test files** | 400 | 3,534 |
| **Test ratio** | 0.59 tests/py file | 0.37 tests/ts file |
| **Coverage threshold** | Not documented | 70% (lines/branches/functions/statements) |
| **E2E tests** | ❌ documented | ✅ (`*.e2e.test.ts`) |
| **Test naming** | `test_*` / `*_test.py` | `*.test.ts` / `*.spec.ts` |
| **CI** | Not documented in AGENTS.md | GitHub Actions (multiple workflows) |
| **Drift detection** | ❌ | ✅ (SHA-256 baseline drift for config/SDK) |
| **Performance guards** | ❌ | ✅ (test performance guardrails documented) |

**Paridade:** `2/5` — OpenClaw is significantly more rigorous in testing infrastructure with formal coverage thresholds and drift detection.

---

## 13. Native & Multi-Platform

| Platform | Hermes Agent | OpenClaw |
|----------|-------------|----------|
| **CLI (Linux)** | ✅ | ✅ |
| **CLI (macOS)** | ✅ | ✅ |
| **CLI (Windows/WSL)** | ✅ (WSL2) | ✅ (WSL2) |
| **macOS app** | ❌ | ✅ (583 Swift files, `scripts/package-mac-app.sh`) |
| **iOS app** | ❌ | ✅ (Swift, shared code) |
| **Android app** | ❌ | ✅ (134 Kotlin files) |
| **Swabble (Swift lib)** | ❌ | ✅ (25 Swift files, shared Swift package) |
| **Canvas** | ❌ | ✅ (live Canvas rendering) |
| **Voice** | ✅ (TTS via NeuTTS, STT via transcription) | ✅ (speech-core, talk-voice, voice-call) |
| **Nix** | ✅ (`flake.nix`) | ✅ (separate nix-openclaw repo) |

**Paridade:** `1/5` — OpenClaw exclusive native app ecosystem. Hermes is CLI/gateway-only.

---

## 14. Cron & Scheduling

| Feature | Hermes Agent | OpenClaw |
|---------|-------------|----------|
| **Built-in scheduler** | ✅ (`cron/scheduler.py`, `cron/jobs.py`) | ✅ (`src/cron/`) |
| **Natural language scheduling** | ✅ | ✅ |
| **Platform delivery** | ✅ (deliver to any connected platform) | ✅ |
| **Unattended execution** | ✅ | ✅ |

**Paridade:** `5/5` — Equivalente forte. Both have mature cron systems with platform delivery.

---

## 15. Research & Training Infrastructure

| Feature | Hermes Agent | OpenClaw |
|---------|-------------|----------|
| **Batch runner** | ✅ (parallel processing, checkpointing, trajectory saving) | ❌ |
| **RL environments** | ✅ (Atropos integration) | ❌ |
| **Trajectory compression** | ✅ (for training next-gen tool-calling models) | ❌ |
| **Datagen configs** | ✅ (`datagen-config-examples/`) | ❌ |
| **Training data export** | ✅ | ❌ |

**Paridade:** `1/5` — Hermes exclusive. This reflects Nous Research's AI research DNA — OpenClaw is product-focused, not research-focused.
