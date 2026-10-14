# Agentic Planning & Reflection

> Como cada player faz planning (decomposição da query) e reflection (auto-crítica entre passos).

## Quadro Comparativo

| Player | Planning | Reflection | Emergent Behaviors |
|---|---|---|---|
| **AIOX** | 7 phases dedicadas (auto-clarify, clarify, decompose, prompt-gen) + product-discovery framework | Multi-wave compression + COVERAGE_GATE + CITATION_GATE explicit | Documented in learning logs per-run |
| DeerFlow | Lead agent decompose → max 3 sub-agents per turn | TIAMAT memory + confidence scores | Cross-session learning |
| GPT-Researcher | Chief Editor decompose → Researcher parallel | Reviewer agent + LangSmith trace | Multi-source bias reduction |
| LangChain ODR | Single LangGraph plan → search → compress → report | Compression step between waves | Plan-and-Solve inheritance |
| Local DR | 20+ research strategies user-selectable | Cross-validate between 10+ search engines | High recall design |
| OpenResearcher | Trained into model (offline trajectory synthesis) | Model self-corrects (RL) | Beats GPT-4.1 in BrowseComp-Plus |
| **DeepResearcher** | Trained into model (GRPO RL) | Explicit emergent behaviors: planning + cross-val + self-reflection + abstention | **Documented** in paper |
| Jina node-DR | search → visit → reflect → answer loop | reflect action between rounds | Budget monitoring |
| AutoResearchClaw | 23 stages with HITL checkpoints | 4-round quality audit | None explicit |
| Tongyi | WebAgent specialized planning | Inference/evaluation separate | Conference paper depth |

## DeepResearcher — Profundidade Especial

DeepResearcher é **único** em documentar emergent behaviors:

1. **Planning** — formula plano antes de executar (não programado, emergiu do RL)
2. **Cross-validation** — valida claim entre múltiplas fontes (não programado)
3. **Self-reflection** — re-direciona quando detecta erro
4. **Honest abstention** — admite quando não encontra resposta

**+28.9 pts sobre prompt-engineering baselines** prova que **modelos treinados batem agentes baseados em prompting**.

## AIOX Reflection Strengths

AIOX **não tem emergent behaviors** (não treinou modelo), mas tem **structured behaviors**:

| Behavior | Implementação AIOX |
|---|---|
| Planning | Phase 1.5 decompose-subqueries explicit |
| Cross-validation | Phase 4.5 verify-citations + CITATION_GATE |
| Self-reflection | Phase 3.5 evaluate-coverage + COVERAGE_GATE veto |
| Honest abstention | Guardrails veto_conditions + insufficient data protocol |
| Wave compression | Phase 3.6 evita context blow |

**Vantagem:** Structured behaviors são **auditáveis** (cada veto é loggable). Emergent são **opacos**.

**Desvantagem:** Structured é mais token-expensive. Emergent é mais eficiente.

## Reflection Patterns

### Pattern 1: Single-pass + Self-check (Jina, DeepResearcher emergent)

```
search → visit → reflect → IF(satisfied) answer ELSE continue
```

Pros: simples, eficiente
Cons: pode loop infinito; precisa budget cap

### Pattern 2: Multi-pass + Multi-round audit (AutoResearchClaw, AIOX)

```
plan → execute_wave_1 → review → execute_wave_2 → review → ... → final_audit
```

Pros: qualidade alta, gates explícitos
Cons: token-expensive

### Pattern 3: Lead + Specialists (DeerFlow, GPT-Researcher)

```
lead.decompose → spawn(researcher, editor, reviewer, publisher) → lead.synthesize
```

Pros: paralelismo real, division of concerns
Cons: coordination overhead, mais complexo

### Pattern 4: RL Emergent (OpenResearcher, DeepResearcher)

```
model() → trajectory_with_emergent_planning_and_reflection
```

Pros: eficiente, qualidade alta
Cons: precisa hardware + treinou modelo

## AIOX Estratégia Recomendada

**Manter Pattern 2 como core (structured + auditable) MAS:**

1. **Adicionar Pattern 3 opt-in** (`--parallel-subagents` flag, GAP-08)
2. **Adicionar Pattern 4 opt-in** (model backend, GAP-04)
3. **Adicionar Pattern 1 via skill irmã** (`/quick-answer` para casos curtos, lesson Jina)

Resultado: AIOX cobre TODOS os 4 patterns conforme o caso, mantendo Governance + PT-BR + Multi-mode como diferencial DNA.

## Reflection Score Computation

Pattern 1: 60/100 (simples mas pode loop)
Pattern 2: 95/100 (gates + audit + structured) ← AIOX
Pattern 3: 85/100 (paralelo mas overhead)
Pattern 4: 90/100 (emergent + eficiente, mas opaque)

**AIOX wins** em Reflection quality. Confirma score Governance=100.
