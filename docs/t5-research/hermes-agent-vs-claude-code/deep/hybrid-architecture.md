# Hybrid Architecture: Hermes Agent + Claude Code

**Date:** 2026-04-04 | **Pattern:** Gateway Delegation + MCP Sidecar

---

## Architecture Overview

```
┌═══════════════════════════════════════════════════════════════════════════┐
│                              USER LAYER                                 │
│                                                                         │
│  ┌──────┐ ┌───────┐ ┌─────┐ ┌────────┐ ┌──────┐ ┌─────┐ ┌───┐ ┌───┐  │
│  │ Tele │ │Discord│ │Slack│ │WhatsApp│ │Signal│ │Email│ │CLI│ │IDE│  │
│  │ gram │ │       │ │     │ │        │ │      │ │     │ │   │ │   │  │
│  └──┬───┘ └──┬────┘ └──┬──┘ └───┬────┘ └──┬───┘ └──┬──┘ └─┬─┘ └─┬─┘  │
│     └────────┴─────────┴────────┴─────────┴────────┘       │     │    │
│                         │ Gateway API                       │     │    │
└═════════════════════════╪═══════════════════════════════════╪═════╪════┘
                          │                                   │     │
┌═════════════════════════▼═══════════════════════════════════╪═════╪════┐
│                    HERMES AGENT (VPS/Docker)                │     │    │
│                                                             │     │    │
│  ┌──────────────────────────────────────────────┐           │     │    │
│  │              INTENT CLASSIFIER                │           │     │    │
│  │                                              │           │     │    │
│  │  coding? ──► delegate to CC                  │           │     │    │
│  │  general? ──► handle locally                 │           │     │    │
│  │  multimodal? ──► handle locally (voice/img)  │           │     │    │
│  │  complex? ──► MoA multi-model                │           │     │    │
│  └──────┬──────────┬──────────┬─────────┬───────┘           │     │    │
│         │          │          │         │                   │     │    │
│  ┌──────▼──┐ ┌─────▼────┐ ┌──▼───┐ ┌───▼────┐              │     │    │
│  │delegate │ │ local    │ │ MoA  │ │ skill  │              │     │    │
│  │ _tool   │ │ handler  │ │ tool │ │manager │              │     │    │
│  └────┬────┘ └──────────┘ └──────┘ └────────┘              │     │    │
│       │                                                     │     │    │
│       │ claude -p                              MCP Server   │     │    │
│       │                                    ┌────────────┐   │     │    │
│       │                                    │ Exposed:   │   │     │    │
│       │                                    │ • search   │   │     │    │
│       │                                    │ • skill    │   │     │    │
│       │                                    │ • voice    │   │     │    │
│       │                                    │ • image    │   │     │    │
│       │                                    │ • memory   │   │     │    │
│       │                                    └──────┬─────┘   │     │    │
│       │                                           │ MCP     │     │    │
└═══════╪═══════════════════════════════════════════╪═════════╪═════╪════┘
        │                                           │         │     │
        │              ┌────────────────────────────┤         │     │
        │              │                            │         │     │
┌═══════▼══════════════▼════════════════════════════▼═════════▼═════▼════┐
│                    CLAUDE CODE (Local/Cloud)                           │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────┐       │
│  │                    CORE ENGINE                             │       │
│  │                                                            │       │
│  │  ┌─────┐ ┌─────┐ ┌─────┐ ┌─────┐ ┌──────┐ ┌───────────┐ │       │
│  │  │Read │ │Write│ │Edit │ │Bash │ │Grep  │ │Extended   │ │       │
│  │  │     │ │     │ │     │ │     │ │/Glob │ │Thinking   │ │       │
│  │  └─────┘ └─────┘ └─────┘ └─────┘ └──────┘ └───────────┘ │       │
│  │                                                            │       │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────────┐ │       │
│  │  │Agent     │ │Git/gh    │ │Hooks     │ │MCP Client    │ │       │
│  │  │Teams     │ │CLI       │ │(15 types)│ │(Hermes tools)│ │       │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────────┘ │       │
│  └────────────────────────────────────────────────────────────┘       │
│                                                                       │
│  ┌────────────────────────────────────────────────────────────┐       │
│  │                    PERSISTENCE                             │       │
│  │  CLAUDE.md │ auto-memory │ .claude/rules/ │ .claude/skills/│       │
│  │            │             │                │  ← skill sync  │       │
│  └────────────────────────────────────────────────────────────┘       │
└═══════════════════════════════════════════════════════════════════════┘
```

---

## Data Flow: Task Lifecycle

```
1. User sends message via Telegram
   │
2. Hermes Gateway receives, identifies user session
   │
3. Intent Classifier analyzes message
   │
   ├─── [CODING] ──────────────────────────────────────┐
   │                                                     │
   │    4a. Hermes searches past sessions (FTS5)         │
   │        "Have I solved something similar before?"    │
   │        │                                            │
   │    4b. If skill exists → inject into prompt         │
   │        │                                            │
   │    4c. delegate_tool calls:                         │
   │        claude -p "Fix the auth bug in              │
   │        src/middleware.ts. Context from past          │
   │        session: [FTS5 summary]. Skill hint:         │
   │        [SKILL.md content]"                          │
   │        │                                            │
   │    4d. CC processes with full coding power           │
   │        (Read/Edit/Grep + extended thinking)         │
   │        │                                            │
   │    4e. CC returns structured result                  │
   │        │                                            │
   │    4f. Hermes skill_manager evaluates:              │
   │        "Was this a novel solution? Create skill?"   │
   │        │                                            │
   │    4g. If novel → create SKILL.md + sync to CC      │
   │                                                     │
   ├─── [GENERAL] ──────────────────┐                    │
   │    Hermes handles directly      │                    │
   │                                 │                    │
   ├─── [MULTIMODAL] ───────────────┤                    │
   │    Hermes voice/image/TTS       │                    │
   │                                 │                    │
   ├─── [COMPLEX] ──────────────────┤                    │
   │    Hermes MoA → 4 models        │                    │
   │    → aggregator → result        │                    │
   │                                 │                    │
   └─────────────────────────────────┘                    │
                                                          │
5. Hermes formats result for platform (markdown→telegram) │
   │                                                      │
6. Hermes sends result back to user                       │
   │                                                      │
7. Hermes persists: session log + memory update           │
```

---

## MCP Bridge Specification

### Hermes Tools Exposed to CC

```yaml
mcp_server:
  name: hermes-bridge
  transport: stdio
  command: hermes mcp-serve
  
  tools:
    - name: hermes_session_search
      description: "Search past conversations via FTS5"
      input:
        query: string
        max_sessions: int (default 3)
      output:
        sessions: [{session_id, date, summary}]
    
    - name: hermes_skill_create
      description: "Create a reusable SKILL.md from current solution"
      input:
        name: string
        description: string
        content: string
      output:
        path: string
        status: created|failed
    
    - name: hermes_skill_list
      description: "List available skills matching a query"
      input:
        query: string (optional)
        category: string (optional)
      output:
        skills: [{name, category, description}]
    
    - name: hermes_send_message
      description: "Send a message to a specific platform"
      input:
        platform: telegram|discord|slack|...
        recipient: string
        message: string
      output:
        status: sent|failed
    
    - name: hermes_image_generate
      description: "Generate an image using FLUX 2 Pro"
      input:
        prompt: string
        size: string (optional)
      output:
        image_path: string
```

### CC Tools Exposed to Hermes (via standard MCP)

```yaml
mcp_server:
  name: claude-code-bridge
  transport: stdio
  command: claude mcp-serve  # hypothetical
  
  tools:
    - name: cc_codebase_query
      description: "Query codebase using CC's Read/Grep/Glob"
      input:
        query: string
        scope: string (file pattern)
      output:
        results: [{file, line, content}]
    
    - name: cc_edit_file
      description: "Surgical file edit using CC's Edit tool"
      input:
        file_path: string
        old_string: string
        new_string: string
      output:
        status: success|failed
    
    - name: cc_git_operation
      description: "Git operations via CC's native gh CLI"
      input:
        operation: commit|push|pr_create|...
        params: object
      output:
        result: object
```

---

## Deployment Topology

```
┌─────────────────────────────────┐
│         VPS ($5/mo)             │
│                                 │
│  ┌──────────────────────────┐   │
│  │ Hermes Agent (daemon)    │   │
│  │ • Gateway process        │   │
│  │ • MCP server process     │   │
│  │ • SQLite DB              │   │
│  │ • Skills directory       │   │
│  └──────────────────────────┘   │
│                                 │
│  Port 8080: Gateway API         │
│  Port 8081: MCP server          │
└────────────┬────────────────────┘
             │ SSH/API
             │
┌────────────▼────────────────────┐
│    Developer Machine (local)    │
│                                 │
│  ┌──────────────────────────┐   │
│  │ Claude Code (CLI/IDE)    │   │
│  │ • MCP client → Hermes    │   │
│  │ • .claude/skills/ (sync) │   │
│  │ • auto-memory            │   │
│  └──────────────────────────┘   │
│                                 │
│  ┌──────────────────────────┐   │
│  │ IDE (VS Code/JetBrains)  │   │
│  │ • CC extension           │   │
│  └──────────────────────────┘   │
└─────────────────────────────────┘
```

---

*Generated by bench-synergy task | 2026-04-04*
