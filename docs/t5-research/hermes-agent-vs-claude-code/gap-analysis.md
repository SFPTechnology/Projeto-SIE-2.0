# Gap Analysis — Hermes Agent v0.7 vs Claude Code

**Date:** 2026-04-04 | **Direction:** Bidirectional | **Focus:** Sinkra-Hub coverage assessment

---

## PART 1: Gaps Hermes Has → Claude Code Missing (14 gaps)

### Coverage com Sinkra-Hub + Claude Code Nativo

```
 FULL ████████████████  4 gaps (G6, G7, G8, G11)     — JA PREENCHIDOS
 PARTIAL ████████████  4 gaps (G1, G3, G9, G12)       — PREENCHÍVEIS
 NONE ████████████████  6 gaps (G2, G4, G5, G10, G13, G14) — ABERTOS
 ─────────────────────────────────────────────────
 Coverage total: 57% (8/14 full ou parcial)
```

### TIER 1 — Gaps Criticos

| # | Gap | Sinkra Coverage | CC Nativo | Remaining Gap | Absorption |
|---|---|---|---|---|---|
| G1 | **MoA Multi-Model** | ⚡ PARCIAL — ai-provider-factory.js (2 models), /roundtable, sinkra-map benchmark | Agent Teams (same model) | Falta consensus multi-model real | P1: Estender /roundtable com model override. 3-4 stories |
| G2 | **Self-Learning Skills** | 🔴 NONE — skill-creator-ops e manual | Auto-memory (declarativo) | **Gap critico.** Zero auto-generation | P0: Hook SessionEnd → SKILL.md draft → validator. 1 Epic |
| G3 | **Session Search FTS5** | ⚡ PARCIAL — journey-log.ts (squad events) | /resume (list only) | Journey-log nao indexa conversas CC | P1: Hook SessionEnd → Supabase transcript → FTS. 1 Epic |
| G4 | **Gateway 15 plataformas** | 🔴 NONE — webhook-handler inbound only | CLI/IDE/Web/Desktop | Zero messaging adapters | P2: Hermes como gateway front-end ou MCP bridges |
| G5 | **7 Execution Envs** | ⚡ PARCIAL — Docker (deploy only) | Local + Anthropic Cloud | Runners local-only. Sem SSH/Modal | P2: MCP Docker exec + SSH tunnel |

### TIER 2 — Gaps Significativos

| # | Gap | Sinkra Coverage | CC Nativo | Status |
|---|---|---|---|---|
| G6 | Voice TTS/STT | ✅ FULL — symphony/t2s.js + Whisper.cpp | Dictation (input) | **PREENCHIDO** |
| G7 | Image Generation | ✅ FULL — nano-banana-generator | None | **PREENCHIDO** |
| G8 | Checkpoint Manager | ✅ FULL — CC nativo + rollback-manager.js | Checkpointing nativo | **PREENCHIDO** |
| G9 | Cron/Scheduling | ⚡ PARCIAL — /loop + /schedule + CronCreate | Cron nativo | 80% coberto. Falta threat scanning |
| G10 | Home Automation | 🔴 NONE | None | Nicho. MCP server se necessario |

### TIER 3 — Gaps Menores

| # | Gap | Sinkra Coverage | Status |
|---|---|---|---|
| G11 | Browser Automation | ✅ FULL — playwright-ops + Chrome ext | **PREENCHIDO** |
| G12 | Skills Marketplace | ⚡ PARCIAL — *import-hub, codex-skills-sync | Falta trust tiers |
| G13 | Cross-Platform Msg | 🔴 NONE | Ligado ao G4 |
| G14 | Model Agnostic | ⚡ PARCIAL — factory (2 models) | CC locked. Extend factory |

---

## PART 2: Gaps Claude Code Has → Hermes Missing (8 gaps)

| # | Gap | CC Score | Hermes Score | Delta | Impact |
|---|---|---:|---:|---:|---|
| CG1 | **SWE-bench Coding** | 95 | 55 | -40 | Hermes não foi feito para coding profundo |
| CG2 | **IDE Integration** | 92 | 10 | -82 | Hermes e terminal-only |
| CG3 | **Native Git/GitHub** | 95 | 35 | -60 | Hermes usa shell git apenas |
| CG4 | **Extended Thinking** | 90 | 30 | -60 | CC tem chain-of-thought controlado |
| CG5 | **Permission Sandboxing** | 88 | 65 | -23 | CC tem 5 modes + fine-grained rules |
| CG6 | **Hooks System** | 85 | 50 | -35 | CC tem 15+ event types com matchers |
| CG7 | **Agent Teams** | 75 | 60 | -15 | CC tem teammates com task list |
| CG8 | **200K Context** | 95 | 40 | -55 | CC tem Opus 200K nativo |

---

## PART 3: Absorption Roadmap

### Prioridade P0 — Fazer AGORA

#### Epic: Self-Learning Skills (G2)
```
Objetivo: Agente cria SKILL.md autonomamente apos resolver tasks complexas
Estimativa: 8 stories

STORY-1: Hook SessionEnd que detecta "task resolvida com sucesso"
STORY-2: Template SKILL.md com frontmatter padrao
STORY-3: Gerador de SKILL.md a partir do transcript da solucao
STORY-4: skills_guard equivalente (security scan regex antes de persistir)
STORY-5: Persist em squads/*/skills/ com naming convention
STORY-6: Integrar com skill-validator para quality gate
STORY-7: CLI para listar/editar/deletar skills auto-gerados
STORY-8: Metricas de reutilizacao (quantas vezes skill foi invocado)
```

### Prioridade P1 — Proximo Sprint

#### Epic: Session Search (G3)
```
Objetivo: Busca full-text em todas as sessoes Claude Code passadas
Estimativa: 5 stories

STORY-1: Hook SessionEnd → persist transcript em Supabase (ou SQLite local)
STORY-2: FTS index (Supabase pg_trgm ou SQLite FTS5)
STORY-3: MCP server para query tool ("buscar em sessoes passadas")
STORY-4: Summarization com modelo barato (Gemini Flash / Haiku)
STORY-5: Integrar com auto-memory (atualizar MEMORY.md com insights)
```

#### Epic: MoA Generalizado (G1)
```
Objetivo: Multi-model reasoning como tool callable
Estimativa: 3-4 stories

STORY-1: Estender ai-provider-factory para OpenRouter (GPT, DeepSeek)
STORY-2: Tool MoA: query → N models paralelo → aggregator Opus
STORY-3: Integrar como opcao no /roundtable
STORY-4: Metricas de consenso e divergencia entre modelos
```

### Prioridade P2 — Backlog

| Epic | Gap | Effort | Approach |
|---|---|---|---|
| Messaging Gateway | G4 + G13 | HIGH | Hermes como front-end gateway, CC como backend. Ou MCP bridges |
| Remote Execution | G5 | MEDIUM | MCP server Docker exec + SSH. Modal via API |
| Model Factory v2 | G14 | LOW | Extend ai-provider-factory para OpenRouter |

### Prioridade P3 — Nice to Have

| Gap | Approach |
|---|---|
| G9: Cron threat scanning | Hook pre-cron com regex de seguranca |
| G10: Home Automation | MCP server para HA (nicho) |
| G12: Skills trust tiers | Adicionar metadata trust_level em SKILL.md |

---

## Coverage Projection

```
                     HOJE           APOS P0+P1        APOS P0+P1+P2
FULL:                 4/14 (29%)     7/14 (50%)        10/14 (71%)
PARTIAL:              4/14 (29%)     4/14 (29%)         2/14 (14%)
NONE:                 6/14 (43%)     3/14 (21%)         2/14 (14%)
Coverage total:       57%            79%                86%

Gaps residuais apos P0+P1+P2:
- G9 (cron threat scan) — minor
- G10 (home automation) — nicho
- G12 (skills marketplace trust) — minor  
- G14 (model agnostic CC) — CC locked by design
```

---

*Generated by bench-analyst v3.0 | 2026-04-04*
