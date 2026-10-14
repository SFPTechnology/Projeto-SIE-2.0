# Inventory — AIOX Research Ecosystem

> Subject A do **Deepresearch Absorption Benchmark**.
> Topologia: **tri-component** (Squad + Skill + App) operando como um produto integrado.
> Confiança: **ALTA** (scan direto do codebase, ver `inventory-aiox-research-ecosystem.json`).

## Componentes

| Componente | Caminho | Versão | Papel |
|---|---|---|---|
| **Squad `research`** | `squads/research/` | 5.0.0 | Cognitive brain — orquestração, persona, metodologia, governance |
| **Skill `/tech-research`** | `.claude/skills/tech-research/` | 2.0.0 | Execution pipeline — 7 molecules, 17 atoms, 2 quality gates |
| **App `aiox-research`** | `apps/research/` | 0.1.0 | Research Observatory — console Next.js 16 local-first |

## 1. Squad `research` (Cognitive Brain)

**Renamed** de `spy` em 2026-05-16 para refletir escopo expandido. **Absorveu** `deep-research v1.0.0` (2026-04-13) e a skill standalone `tech-research v2.0.0` (2026-05-16).

### Métricas
- 14 agents (1 chief + 13 specialists)
- 6 workflows YAML (bench-comparison, competitive-intel, deep-research, product-discovery, quick-research + tech-research/ com 13 sub-phases)
- 129 arquivos `.md` totais no squad
- ~70 tasks declarados

### Lineage acadêmica/metodológica dos agentes
| Agent | Methodology DNA |
|---|---|
| `bench-analyst` | Framework benchmark especialista (este agent) |
| `booth` | Booth's "The Craft of Research" — research mechanics |
| `creswell` | John Creswell — research design qualitativo/quantitativo |
| `dr-orchestrator` | Deep Research orchestrator |
| `forsgren` | Nicole Forsgren — DORA metrics, DevOps research |
| `gilad` | Benjamin Gilad — competitive intelligence pioneer |
| `klein` | Naturalistic decision making |
| `sackett` | David Sackett — Evidence-Based Medicine (PICO/systematic reviews) |
| `marketing-deepdive` | 1-player marketing analysis specialist |
| `reference-competitor-clone` | Codebase recon helper |
| `research-chief` | Squad orchestrator (entry agent) |
| `research-operator` | Human-in-the-loop approver |
| `tech-research-agent` | Owns the /tech-research pipeline persona |
| `benchmark-runtime` | Codebase comparison runtime |

### Modos de Operação Suportados
1. Deep technical research (absorvido de tech-research)
2. Competitive intelligence (legacy spy)
3. Marketing deep-dive (1-player)
4. Product discovery (JTBD + Mom Test + Villain + WTP signals)
5. Universal benchmarking (codebase/llm/product/company/technology)
6. PICO/OSINT pipeline
7. Systematic reviews (Sackett heritage)
8. Decision science / bias detection (Klein heritage)

### Domain Model
```yaml
Strategic:  "Posicionamento competitivo, inteligência de mercado e decisões de benchmark"
Tactical:   "Orquestração de benchmarks, síntese de evidências e análise comparativa"
Operational:"Coleta, transcrição, publicação e automação de artefatos"
```

## 2. Skill `/tech-research` (Execution Pipeline)

Pipeline de 7 molecules × 17 atoms executando **inline persona-fidelity** (não spawna subagents — cada phase carrega persona + YAML protocol + prompt e executa em main context).

### Phase YAMLs (13)
```
phase-0-auto-clarify.yaml
phase-1-clarify.yaml
phase-1-5-decompose.yaml
phase-2-generate-prompt.yaml
phase-3-execute-research.yaml
phase-3-2-deep-read.yaml
phase-3-5-evaluate-coverage.yaml     ← COVERAGE_GATE
phase-3-6-compress-wave.yaml
phase-3-7-playwright-deep-research.yaml
phase-4-synthesize.yaml
phase-4-5-verify-citations.yaml      ← CITATION_GATE
phase-5-document.yaml
tech-research-pipeline.yaml          (master)
```

### Quality Gates (REAIS, não aspiracionais)
| Gate | Trigger | Action |
|---|---|---|
| **COVERAGE_GATE** | coverage < 50% após 3 waves | VETO — halt pipeline |
| **COVERAGE_GATE** | coverage ≥ 70% | APPROVE — proceed |
| **CITATION_GATE** | verified_ratio < 0.85 após 2 fix attempts | VETO — halt |
| **CITATION_GATE** | verified_ratio ≥ 0.85 | APPROVE |

### Scripts Python
- `scaffold.py` — bootstrap folder structure
- `next_followup_number.py` — follow-up file numbering
- `credibility_scorer.py` — source credibility scoring
- `output_validator.py` — output validation
- `metrics_collector.py` — pipeline metrics

### Modos
- default (deep technical research)
- `--product-discovery` / `--pd` (validate-product-idea)
- `--deep` (multi-LLM cross-reference)
- `--yolo` (autonomy)
- `--interactive` (default UI)

### Governance Rules (10 NON-NEGOTIABLE)
1. Guardrails first (Phase 00 reads `checklists/tech-research/guardrails.yaml`)
2. Checkpoints absolutos (no override)
3. **Incremental learning log** (write on every phase start AND end)
4. Prior-art before absence claim
5. **NO implementation** (research outputs only — redirect to @aiox-pm/@aiox-dev for code)
6. Outputs only under `docs/research/{date}-{slug}/`
7. Follow-up reuses existing folder
8. No partial reads of workflow files
9. Sequential by default; waves bounded (max 3)
10. CLI next-command suggestion at completion

### Caller Contract
Invoked by:
- `/research-chief` (validate-product-idea Wave 0 atoms 3+4)
- `/skill-creator` (optional prior-art evidence)
- `/aiox-architect` (research-before-decision)

## 3. App `aiox-research` (Research Observatory)

Console Next.js 16 local-first para executar pesquisas e visualizar artefatos.

### Stack
- Next.js 16.2.6 (App Router, webpack flag explícita)
- React 19.2.3
- Tailwind v4 (`@tailwindcss/postcss`)
- TypeScript 5 strict
- yaml 2.8.2, react-markdown 10.1.0, remark-gfm 4.0.1
- Geist fonts, lucide-react icons

### License
**Elastic License v2** (source-available, NOT OSI open-source).
- ✅ Clone/modify/distribute, internal use (incluindo commercial)
- ❌ SaaS competidor (managed service para terceiros)
- ❌ Remover marca/copyright AIOX

### Routes — UI
| Path | Purpose |
|---|---|
| `/observatory` | Browse research/bench/SINKRA Maps |
| `/observatory/demo` | Visitante público (dataset embutido) |
| `/observatory/[source]` | Drill into a specific source |
| `/research` | Active research console (cria runs) |
| `/research/status` | Status dashboard |

### Routes — API
| Path | Purpose |
|---|---|
| `/api/observatory` | List sources & artifacts |
| `/api/observatory/open-folder` | Open folder in OS |
| `/api/research` | Research orchestration |
| `/api/research/runs` | List/create research runs |
| `/api/research/runs/[runId]` | Run details |
| `/api/research/runs/[runId]/stream` | **SSE streaming** of run progress |
| `/api/research/uploads/audio` | Audio upload (Whisper transcription) |
| `/api/research/uploads/files` | File uploads |
| `/api/research/clis` | Local CLI detection (Claude/Codex/Gemini/OpenRouter) |
| `/api/research/consolidations` | Aggregate runs |

### Tiers
| Tier | Access | What Works |
|---|---|---|
| Visitante público | Clone + `npm install` + `npm run dev` | Apenas `/observatory/demo` |
| AIOX Pro | Workspace AIOX provisionado | Demo + Research + Bench + SINKRA Maps |
| AIOX Enterprise | Workspace completo + suporte + integrações | Tudo + ServiceBus/ClickUp/GWS/ETL |

## Pontos Fortes do Ecossistema

1. **Tri-layer separation** — brain (squad) / execution (skill) / observability (app)
2. **Methodology governance** — COVERAGE + CITATION gates são reais e VETO halt
3. **Incremental learning log** — escreve a cada phase (vs post-hoc only)
4. **Multi-mode** — tech-research + competitive intel + product discovery + benchmarking + marketing
5. **PT-BR/LatAm-first** — workflow verticals para PRD/BMC/battle-card
6. **Local-first app** — lê filesystem, sem DB required
7. **9 bench tasks dedicados** — codebase comparison estruturado
8. **14 specialist personas** com lineage acadêmico claro (Booth/Creswell/Forsgren/Gilad/Klein/Sackett)
9. **Tight SINKRA integration** — entry agent, ecosystem-registry, learning logs
10. **App License v2** — proteção comercial (não SaaS-hijackable)

## Pontos Fracos do Ecossistema (vs Open-Source 2026)

1. **Sem modelo treinado para research** — OpenResearcher (30B), DeepResearcher (7B), Kimi têm purpose-trained models que superam GPT-4 em BrowseComp-Plus
2. **Sem Docker sandbox de execução** — DeerFlow e AutoResearchClaw têm Docker hardened para code execution durante research
3. **Sem memória persistente cross-session** — DeerFlow tem TIAMAT (cross-device sync com confidence scores)
4. **Sem exposição MCP nativa** — LangChain Open DR é MCP-native; GPT-Researcher tem MCP Server
5. **App License v2** — atrito para contribuição community (vs MIT/Apache-2.0 dos competidores)
6. **Sem progressive skill loading** — DeerFlow carrega skills dinâmicamente conforme necessário
7. **Sem score público em benchmarks** — Deep Research Bench / BrowseComp-Plus / SimpleQA não testados
8. **Sem modo headless API standalone** — só via skill invocation (vs GPT-Researcher REST + WS)
9. **CITATION_GATE sem scholarly DB nativa** — Local Deep Research tem 10+ engines (arXiv, PubMed, Semantic Scholar, SearXNG)
10. **Multi-agent inline, não paralelo real** — research phases executam em main context (apenas bench-comparison usa subagent spawn paralelo)

## Sources

- Direct codebase scan via `Bash(find/ls)` em 2026-05-18
- `squads/research/config.yaml` (v5.0.0, 70 linhas mapeadas)
- `.claude/skills/tech-research/SKILL.md` (v2.0.0)
- `apps/research/package.json` + `apps/research/README.md`
- `apps/research/src/app/**` (routes via Glob)
