# Presentation Brief — Slides Creator Open-Source Absorption

Data: 2026-05-18

## Objetivo

Apresentar por que construir slide creator skill stack por absorção modular e como o benchmark prova essa decisão.

## Audiência

founders, product, engineering, design

## Tese

slide creator skill stack deve ser uma composição, não um fork: narrativa governada do squad, renderer ppt-master, runtime Presenton, QA PPTAgent/powerpoint-skill e UX aprendida de presentation-ai/banana-slides.

## Storyline Recomendada

### 01 — Não vamos vencer copiando um Gamma open-source

O benchmark mostra que nenhum projeto isolado cobre app, skill, renderer, compliance, prompt-to-edit e multimodal com profundidade suficiente. A estratégia vencedora é slide creator skill stack por composição modular.

**Métrica:** COMPOSTO decisão.

**Score do bench:** 100.

- SINKRA mantém narrativa e governança
- ppt-master cobre PPTX nativo
- Presenton cobre runtime/API/MCP
- PPTAgent e powerpoint-skill fecham QA e técnica

### 02 — A comparação justa tem três arenas

Apps, skills/agentes e engines têm naturezas diferentes. O dashboard precisa mostrar rankings segmentados antes de forçar um vencedor único.

**Métrica:** 3 arenas.

- Apps: Presenton, presentation-ai, banana-slides
- Skills/agentes: SINKRA, PPTAgent, PresentAgent-2, powerpoint-skill
- Engines/runtime: ppt-master, Presenton, slide-deck-ai

### 03 — O vencedor muda quando o trabalho muda

Personas v4 amarram job-to-be-done, must-haves e anti-goals a pesos explícitos sobre a matriz de 108 microdimensões. Isso evita que o bench vire opinião disfarçada de ranking.

**Métrica:** 12 cenários.

- Presenton: vence 4 persona(s)
- presentation-ai: vence 3 persona(s)
- ppt-master: vence 2 persona(s)
- powerpoint-skill: vence 1 persona(s)
- banana-slides: vence 1 persona(s)
- PresentAgent-2: vence 1 persona(s)

### 04 — A stack alvo é uma cadeia de absorção

A inteligência entre arquivos aponta uma arquitetura concreta: Brief → Research → Plan → DeckSpec → Native IR → PPTX/PDF/QA → Share/Analytics.

**Métrica:** 108D / 972 células.

- DeckSpec governa conteúdo
- Native IR governa editabilidade
- QA governa confiança
- API/MCP governa automação

### 05 — O bench agora entrega a skill blueprint, não só ranking

`slide-creator-skill-blueprint.md` transforma cada vencedor parcial em regra de uso: quando absorver Presenton, ppt-master, PPTAgent, presentation-ai, banana-slides, powerpoint-skill, slide-deck-ai, PresentAgent-2 e Gamma.

**Métrica:** SKILL blueprint.

- Cada capability tem fonte benchmark
- Cada capability vira artifact
- Cada risco/licença tem regra de não-cópia
- Cada slide precisa roteiro + estrutura + função

### 06 — Os gaps agora são microações, não recomendações genéricas

`deep/slides-creator-micro-gap-map.md` mostra onde a slide creator skill perde em cada microcapacidade: DrawingML, roundtrip PowerPoint, canvas web, undo/redo, state management, vídeo, analytics e colaboração.

**Métrica:** 86 gaps / 22 vantagens.

- Cada gap aponta líder externo
- Cada gap tem peso e impacto
- Cada gap tem modo de absorção
- Cada vantagem vira regressão positiva da skill

### 07 — Bench 100; produto chega a 100 executando P0/P1

A inteligência comparativa está completa. O próximo salto não é mais pesquisa: é implementação de renderer nativo, CLI/API/MCP, reflection log, PPTEval e fixtures reais.

**Métrica:** 100 bench.

- P0: Criar native-slide-ir.schema.json
- P0: Criar renderer PPTX nativo básico
- P0: Criar editability-report.json
- P0: Criar CLI slides:generate
- P0: Criar API POST /slides/generate
- P0: Criar MCP slides.generate/review/export

### 08 — Próximo movimento: transformar bench em epic

A apresentação deve fechar com uma decisão clara: construir slide creator skill stack, usando este bench como matriz de absorção e contrato de aceite.

**Métrica:** EPIC handoff.

- Materializar stories do backlog
- Implementar contratos Native IR/API/MCP/QA
- Rodar fixtures reais de deck
- Manter bench 100 e abrir epic de implementação para produto 100

## Apêndice

- `comparison-matrix.md`
- `segmented-comparisons.md`
- `scenario-scorecards.md`
- `deep/slides-creator-micro-gap-map.md`
- `deep/micro-capability-matrix.md`
- `slide-creator-skill-blueprint.md`
- `deep/intelligence-graph.md`
- `TODO-coverage.md`
