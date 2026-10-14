# Deep Dive: Cross-Reference com Analises Internas do Claude Code

**Fontes cruzadas:**
1. `outputs/decoded/claude_code_main/` — Domain Decoder pipeline (125 regras extraidas)
2. `outputs/sinkra-squad/claude-code-discovery/` — SINKRA process discovery (25 tokens, 4 waves)
3. `outputs/sinkra-squad/claude-code-mastery/` — SINKRA mapping + validation (21.3/100 compliance)

---

## 1. O Que as Analises Internas Revelam sobre Claude Code

### 1.1 Arquitetura Decodificada (Domain Decoder)

Claude Code opera como **Service Layer with Transaction Scripts** — logica distribuida em funcoes procedurais, nao encapsulada em objetos de dominio.

**3 Bounded Contexts identificados:**
| Contexto | Tipo | Escopo |
|---|---|---|
| AI Orchestration & Agents | Core | QueryEngine, token budgets, generation loops |
| Tool Capabilities & MCP | Supporting | Security permissions, MCP integration |
| Session & Memory Management | Generic | API limits, rate limits, contextual state |

**Regras criticas decodificadas:**
- `RE-AIORCH-001`: Se agent ativo OU budget ≤ 0 → MUST stop generation
- `RE-AIORCH-002`: Diminishing returns quando continuation_count ≥ 3 AND delta_tokens < 500
- `RE-AIORCH-003`: Pode continuar com 90% budget se returns nao diminuindo
- `RE-SESSION-001`: Quota warning a 90% utilizacao dentro de 72% da janela

**Modelo de decisao chave:**
```
DEC-AIORCH-001: Model Generation Loop Status
  Inputs:  agent_status, token_budget, continuation_count, delta_tokens
  Output:  loop_action (Stop | Continue)
  Impact:  HIGH (controla custos API diretamente)
```

### 1.2 Mapa de Processos SINKRA (Discovery)

**25 tokens actionaveis** mapeados em **4 ondas de implementacao**:

| Wave | Sistemas | Tokens | Focus |
|---|---|---:|---|
| W1 | Context mgmt, Agent isolation | 6 | Fundacao |
| W2 | Tools, Commands, Permissions | 9 | Infraestrutura |
| W3 | Hooks, Skills, MCP | 6 | Extensibilidade |
| W4 | Tasks, Config, Optimization | 4 | Refinamento |

**Pipeline de compactacao 4-estagios:** snip → micro → auto → context-collapse

**Hierarquia de config 5-niveis:** Constitution → Hub → Spoke → Squad → Agent

### 1.3 Mastery Assessment (SINKRA Compliance)

**Score: 21.3/100 — NON-COMPLIANT**

| Condicao | Status |
|---|---|
| Diversidade de executores | ❌ AUTO-FAIL (todos 8 sao tipo "Agent") |
| Token de accountability | ❌ AUTO-FAIL (tasks fantasma) |
| Quality gates quantificados | ❌ 0/35 com thresholds numericos |
| Artefatos persistidos | ❌ ~50% perda (ficam na conversa, nunca commitados) |
| Estado cross-session | ❌ Zero persistencia de estado entre sessoes |

---

## 2. Cross-Reference: Gaps Hermes vs Gaps Internos do CC

### 2.1 Gaps CONFIRMADOS (analise interna valida gap Hermes)

| Gap Hermes | Evidencia Interna | Confirmacao |
|---|---|---|
| **G2: Self-Learning Skills** | Domain Decoder: "No domain-driven entities — transaction scripts prevent easy rule isolation". Mastery: "Zero state persistence between sessions forces re-briefing" | ✅ CONFIRMADO. CC nao tem mecanismo para aprender com experiencia. Cada sessao comeca do zero (exceto MEMORY.md declarativo) |
| **G3: Session Search** | Mastery: "~50% artifact loss — approved artefacts remain in conversation, never persisted". Discovery: "No context management directory, no compaction engine owned" | ✅ CONFIRMADO. CC perde metade dos artefatos gerados. Sem busca em sessoes passadas. Problema critico documentado |
| **G5: Remote Execution** | Discovery: "No background execution module. No scheduler for deferred task launching" | ✅ CONFIRMADO. Infra de execucao remota ausente na arquitetura interna |
| **G14: Model Lock-in** | Domain Decoder: "RE-SEC-004/005 — Permission availability tied to build-time feature flags". Toda arquitetura assume Anthropic API | ✅ CONFIRMADO. Lock-in e arquitetural, nao apenas comercial |

### 2.2 Gaps AMPLIADOS (analise interna revela que gap e MAIOR do que parecia)

| Gap Hermes | O que parecia | O que a analise interna revela |
|---|---|---|
| **G1: MoA Multi-Model** | CC tem Agent Teams como alternativa parcial | Domain Decoder: Agent Teams operam sob o MESMO token budget, MESMO generation loop. Nao ha mecanismo para agregar respostas de modelos diferentes. Gap e 100%, nao parcial |
| **G8: Checkpoints** | Marcamos como FULL (CC tem checkpointing) | Mastery: "Manual context rebuild — zero state persistence between sessions". Checkpointing e de CONVERSA, nao de WORKFLOW. Hermes checkpoint_manager faz snapshots de FILESYSTEM via shadow git. Sao coisas diferentes |

### 2.3 Gaps NOVOS (encontrados nas analises internas, nao no bench original)

| # | Gap Novo | Fonte | Hermes Tem? | Impacto |
|---|---|---|---|---|
| **G15** | **Artifact Persistence** — CC perde ~50% dos artefatos gerados (ficam na conversa) | Mastery GAP-001, GAP-002 | Sim (skills_sync + session DB) | ALTO — trabalho desperdicado |
| **G16** | **Concurrency Classification** — CC nao tem sistema para determinar safe parallel vs serial | Discovery infra gaps | Sim (delegate_tool com isolated toolsets) | MEDIO — afeta qualidade de sub-agents |
| **G17** | **Agent Isolation** — CC agents compartilham contexto global, sem isolation module | Discovery: "No isolation module" | Sim (delegate_tool spawn com contexto isolado) | MEDIO — cross-contamination entre agents |
| **G18** | **Hook Diversity** — `.aiox-core/hooks/` near-empty, apenas command-type hooks | Discovery: "Near-empty hooks directory" | Hermes: gateway builtin_hooks + platform hooks | BAIXO — hooks CC sao poderosos mas poucos pre-built |
| **G19** | **Knowledge Auto-Update** — Roadmap knowledge statico, sem auto-update | Mastery GAP-003 | Hermes: skills self-improve during use | MEDIO — conhecimento fica stale |

---

## 3. Mapa Revisado de Gaps (18 → Hermes, 8 �� CC)

### Gaps Hermes → CC (Original 14 + 5 Novos = 19, deduplicated = 18)

```
TIER 1 — CRITICOS (confirmados + ampliados pelas analises internas):
  G1:  MoA Multi-Model          → Gap AMPLIADO para 100% (sem mecanismo de agregacao)
  G2:  Self-Learning Skills      → CONFIRMADO (zero aprendizado cross-session)
  G3:  Session Search FTS5       → CONFIRMADO + AMPLIADO (~50% artifact loss)
  G4:  Gateway Multi-Plataforma  → Sem evidencia interna (gap externo apenas)
  G5:  Remote Execution Envs     → CONFIRMADO (no background execution module)
  G15: Artifact Persistence      → NOVO (Mastery: 50% perda de artefatos)

TIER 2 — SIGNIFICATIVOS:
  G6:  Voice TTS/STT             → PREENCHIDO (sinkra-hub)
  G7:  Image Generation          → PREENCHIDO (sinkra-hub)
  G8:  Checkpoints               → RECLASSIFICADO: CC=conversa, Hermes=filesystem. Gap PARCIAL
  G9:  Cron/Scheduling           → PARCIAL (CC tem /schedule mas sem threat scanning)
  G16: Concurrency Classification→ NOVO (sem safe parallel vs serial)
  G17: Agent Isolation            → NOVO (sem isolation module)
  G19: Knowledge Auto-Update     → NOVO (conhecimento stale entre versoes)

TIER 3 — MENORES:
  G10: Home Automation           → Nicho
  G11: Browser Automation        → PREENCHIDO
  G12: Skills Marketplace        → PARCIAL
  G13: Cross-Platform Messaging  → Ligado a G4
  G14: Model Agnostic            → CONFIRMADO (lock-in arquitetural)
  G18: Hook Diversity            → Poucos hooks pre-built
```

---

## 4. Sinkra-Hub Coverage Revisado

### Antes (14 gaps, sem analise interna)

```
FULL:    4/14 (29%)
PARTIAL: 4/14 (29%)
NONE:    6/14 (43%)
Total:   57%
```

### Depois (18 gaps, com analise interna)

| Gap | Coverage | Mudança |
|---|---|---|
| G1: MoA | ⚡ PARCIAL → 🔴 REBAIXADO (gap e 100%) | Piorou |
| G2: Self-Learning | 🔴 NONE | Igual |
| G3: Session Search | ⚡ PARCIAL (journey-log ajuda mas nao resolve) | Igual |
| G4: Gateway | 🔴 NONE | Igual |
| G5: Remote Exec | ⚡ PARCIAL (30%) | Igual |
| G6: Voice | ✅ FULL | Igual |
| G7: Image Gen | ✅ FULL | Igual |
| G8: Checkpoints | �� PARCIAL → RECLASSIFICADO (CC=conversa, shadow git=diferente) | Piorou |
| G9: Cron | ⚡ PARCIAL (80%) | Igual |
| G10: Home Auto | 🔴 NONE | Igual |
| G11: Browser | ✅ FULL | Igual |
| G12: Skills Hub | ⚡ PARCIAL | Igual |
| G13: Messaging | 🔴 NONE | Igual |
| G14: Model Lock | 🔴 NONE (arquitetural) | Igual |
| G15: Artifact Persist | ⚡ PARCIAL — hooks pre-commit + validate ajudam | **NOVO** |
| G16: Concurrency Class | 🔴 NONE | **NOVO** |
| G17: Agent Isolation | ⚡ PARCIAL — worktrees ajudam | **NOVO** |
| G18: Hook Diversity | ⚡ PARCIAL — temos hooks customizados | **NOVO** |
| G19: Knowledge Update | 🔴 NONE | **NOVO** |

```
REVISADO:
  ✅ FULL:     3/18 (17%)   — G6, G7, G11
  ⚡ PARCIAL:  7/18 (39%)   — G3, G5, G8, G9, G12, G15, G17, G18
  🔴 NONE:     8/18 (44%)   — G1, G2, G4, G10, G13, G14, G16, G19
  Coverage:    56%
```

---

## 5. Absorption Roadmap Revisado

### P0 — Impacto Imediato

| Epic | Gaps | Effort | Justificativa Interna |
|---|---|---|---|
| **Self-Learning Skills** | G2 + G19 | 1 Epic (8 stories) | Mastery confirma: "zero state persistence", "manual context rebuild". Skill auto-gen resolve AMBOS |
| **Artifact Persistence** | G15 | 3-4 stories | Mastery: "~50% artifact loss". Hook SessionEnd → persist outputs → registry. Quick win |

### P1 — Proximo Sprint

| Epic | Gaps | Effort | Justificativa Interna |
|---|---|---|---|
| **Session Search FTS** | G3 | 1 Epic (5 stories) | Discovery + Mastery confirmam: nenhuma busca cross-session. Journey-log base existente |
| **MoA Multi-Model** | G1 | 1 Epic (4 stories) | Domain Decoder confirma: Agent Teams ≠ multi-model. Gap e 100% |
| **Agent Isolation Module** | G16 + G17 | 4-5 stories | Discovery: "No isolation module, agents share global context". Worktrees sao paliativo |

### P2 — Backlog

| Epic | Gaps | Effort |
|---|---|---|
| Gateway Multi-Platform | G4 + G13 | HIGH |
| Remote Execution | G5 | MEDIUM |
| Filesystem Checkpoints | G8 | LOW (shadow git pattern simples) |

---

## 6. Key Insight

As analises internas revelam que o gap entre Claude Code e Hermes e **MAIOR do que aparentava** no benchmark externo:

1. **Artifact loss (50%)** e um problema critico que Hermes resolve com persistence layer
2. **Agent isolation** ausente explica por que sub-agents CC as vezes se contaminam
3. **Model lock-in** e arquitetural (feature flags, build-time), nao apenas comercial
4. **MoA gap** e 100%, nao parcial — Agent Teams operam sob o MESMO budget/loop

A arquitetura CC e **otimizada para coding seguro e controlado**, mas **sacrifica autonomia, learning e flexibilidade** que Hermes oferece.

---

*Generated by bench-analyst v3.0 | Cross-referenced with domain-decoder, sinkra-discovery, and mastery pipelines | 2026-04-04*
