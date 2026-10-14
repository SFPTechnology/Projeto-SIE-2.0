# Slides Creator Open-Source Absorption Benchmark

Data: 2026-05-18

## TL;DR

Baixamos e analisamos os principais projetos open-source de slides com IA. A direção recomendada é criar uma stack própria em cima do nosso `squads/slides-creator`, absorvendo:

- `ppt-master` para PPTX nativo editável;
- Presenton para API/MCP/self-hosting;
- PPTAgent para planejamento/reflexão;
- banana-slides/presentation-ai para UX prompt-to-edit;
- powerpoint-skill para regras de skill, math e diagramas.

## Arquivos

- `ADR-001-absorption-strategy.md`
- `INDEX.md`
- `MANIFEST.json`
- `README.md`
- `TODO-coverage.json`
- `TODO-coverage.md`
- `absorption-roadmap.md`
- `architecture-blueprint.md`
- `architecture-blueprint.mmd`
- `battle-card.md`
- `bench-completeness-rubric.json`
- `bench-completeness-rubric.md`
- `bench-contract.json`
- `bench-output-dash.json`
- `capability-matrix.md`
- `comparison-matrix.json`
- `comparison-matrix.md`
- `contracts/api-contract.md`
- `contracts/mcp-contract.md`
- `contracts/native-ir-contract.md`
- `contracts/qa-rubric.json`
- `contracts/qa-rubric.md`
- `dashboard-intelligence.md`
- `deep/absorption-decision-table.json`
- `deep/absorption-decision-table.md`
- `deep/acceptance-test-plan.md`
- `deep/agentic-planning-reflection.md`
- `deep/api-mcp-runtime.md`
- `deep/consolidated-research-archive.md`
- `deep/coverage-map.md`
- `deep/design-100-gap-plan.json`
- `deep/design-100-gap-plan.md`
- `deep/editor-ux-prompt-to-edit.md`
- `deep/evidence-by-dimension.md`
- `deep/evidence-strength-map.json`
- `deep/evidence-strength-map.md`
- `deep/implementation-playbook.md`
- `deep/intelligence-graph.json`
- `deep/intelligence-graph.md`
- `deep/license-risk-assessment.md`
- `deep/macro-comparison-matrix.json`
- `deep/macro-comparison-matrix.md`
- `deep/matrix-methodology.md`
- `deep/micro-capability-matrix.json`
- `deep/micro-capability-matrix.md`
- `deep/micro-leaderboard-by-group.md`
- `deep/open-source-to-sinkra-map.md`
- `deep/persona-weight-methodology.json`
- `deep/persona-weight-methodology.md`
- `deep/renderer-native-pptx.md`
- `deep/repo-notes.md`
- `deep/reproducible-local-runs.md`
- `deep/segment-deep-analysis.md`
- `deep/segmented-methodology.md`
- `deep/slides-creator-micro-gap-map.json`
- `deep/slides-creator-micro-gap-map.md`
- `deep/template-volume-benchmark.json`
- `deep/template-volume-benchmark.md`
- `dependency-graph.md`
- `evidence-ledger.json`
- `evidence-ledger.md`
- `executive-report.md`
- `external-inventory.md`
- `full-comparison.md`
- `gap-analysis.json`
- `gap-analysis.md`
- `implementation-readiness-gate.json`
- `implementation-readiness-gate.md`
- `internal-squad-audit.md`
- `inventories/banana-slides.md`
- `inventories/powerpoint-skill.md`
- `inventories/ppt-master.md`
- `inventories/pptagent.md`
- `inventories/presentagent-2.md`
- `inventories/presentation-ai.md`
- `inventories/presenton.md`
- `inventories/slide-deck-ai.md`
- `inventory-open-source-stack.json`
- `inventory-slides-creator.json`
- `metadata.canonical.json`
- `metadata.json`
- `next-wave-absorption-plan.json`
- `next-wave-absorption-plan.md`
- `presentation-brief.json`
- `presentation-brief.md`
- `quality-audit.md`
- `repo-metrics.json`
- `repo-metrics.md`
- `risk-register.json`
- `risk-register.md`
- `scenario-scorecards.json`
- `scenario-scorecards.md`
- `scorecard.json`
- `scorecard.md`
- `segmented-comparisons.json`
- `segmented-comparisons.md`
- `slide-creator-skill-blueprint.json`
- `slide-creator-skill-blueprint.md`
- `story-ready-backlog.md`

## Cobertura Dashboard

- `coverage`: `complete`
- `coverage_sort_key`: `100`
- `bench_intelligence_score`: `100`
- `score_semantics`: `100` significa bench completo como inteligência de decisão, não produto já implementado.
- `readiness.matrix`: `complete`
- `readiness.persona_methodology`: `complete`
- `readiness.intelligence_graph`: `complete`
- `readiness.presentation_brief`: `complete`
- `readiness.gaps`: `complete`
- `readiness.sources`: `complete`
- `readiness.bench_completeness`: `complete`
- `readiness.implementation_readiness`: `planned_not_implemented`

O bench agora segue o contrato `bench-output-dash.v1` e pode ser ordenado por cobertura junto com os outros benches.

## Status de Completude

- Total atual: `100` arquivos.
- Maior bench em `docs/bench/` por volume e cobertura de camadas.
- Inclui análise executiva, dados estruturados, inventários individuais, contratos, riscos, arquitetura, backlog story-ready, evidence ledger, auditoria de qualidade, matriz consolidada v4 com `108` microdimensões e `972` células, comparações segmentadas com `3` rankings justos, `72` dimensões segmentadas, `264` células, `12` personas v4 recalculadas por job-to-be-done, metodologia auditável de pesos por persona, grafo de inteligência, briefing de apresentação, blueprint bench→skill, plano da próxima wave de absorção, mapa de força de evidência, análise profunda por segmento, tabela de decisão de absorção, rubrica de completude `100/100`, gate de implementação P0/P1/P2 e consolidação da pesquisa antiga removida de `docs/research`.

## Camada de Inteligência

- `deep/intelligence-graph.md/json`: conecta persona → microdimensão → player → gap → contrato → artefato.
- `deep/micro-capability-matrix.md/json`: espelho completo da matriz 108D.
- `deep/slides-creator-micro-gap-map.md/json`: mapa de gaps micro da nossa skill contra os líderes.
- `presentation-brief.md/json`: storyline curada para apresentar a tese de slide creator skill stack.
- `slide-creator-skill-blueprint.md/json`: tradução do bench em skill autocontida com bibliotecas, artifacts, gates e killer items.
- `dashboard-intelligence.md`: regras de UX para o dash mostrar tese, prova, contexto, fontes e execução sem repetir dado.
- `bench-completeness-rubric.md/json`: critérios que justificam o score `100/100` do bench.
- `implementation-readiness-gate.md/json`: separa o que falta para o produto chegar a `100` operacional.

## Clones Locais

Todos estão em `../bench/`.

## Decisão

Não forkear um projeto único. Criar **slide creator skill stack**: governança e narrativa do nosso squad + runtime/render/UX absorvidos dos melhores projetos open-source.
