# Slides Creator Open-Source Absorption — Index

**Data:** 2026-05-17 (Wave 1) · **Última atualização:** 2026-05-18 (Wave 3 spike)
**Tipo:** benchmark de absorção open-source + análise de stack interna
**Escopo:** `squads/slides-creator` vs 8 projetos open-source clonados em `../bench/`
**Score atual:** **81.07** (era 77.93 pré-Wave 3 spike) · líder, gap 6.28 para 2º (ppt-master 74.79)

## Wave 3 Spike — Artefatos Novos (2026-05-18)

| Documento | Conteúdo |
|---|---|
| [prior-art-search.md](prior-art-search.md) | Search formal antes de qualquer CREATE — 5 buscas, gates G1-G6, decisão REUSE/ADAPT/CREATE por frente. |
| [wave-3-promotions.json](wave-3-promotions.json) | 30 promotions de microdimensões com evidence_path e score_reason por linha. |
| [wave-3-score-delta.md](wave-3-score-delta.md) | Análise human-readable dos deltas + projeção próxima wave. |
| [apply-wave3-promotions.py](apply-wave3-promotions.py) | Script idempotente que aplica promotions ao comparison-matrix.json. |
| [apply-wave3-to-dash.py](apply-wave3-to-dash.py) | Script idempotente que sincroniza dash com matrix. |
| [generate-comparison-md.py](generate-comparison-md.py) | Regenera comparison-matrix.md do JSON. |
| [../../stories/epic-slides-w3/EPIC-SLIDES-W3.md](../../stories/epic-slides-w3/EPIC-SLIDES-W3.md) | Epic Wave 3 + 18 stories Draft. |
| [../../stories/epic-slides-w3/local-runtime.md](../../stories/epic-slides-w3/local-runtime.md) | 3 modos de execução local (CLI/REST/MCP). |

## Leitura Recomendada

| Ordem | Documento | Uso |
|---:|---|---|
| 1 | [executive-report.md](executive-report.md) | Decisão executiva e recomendação final. |
| 2 | [presentation-brief.md](presentation-brief.md) | Storyline curada para apresentar a tese em slides. |
| 3 | [bench-completeness-rubric.md](bench-completeness-rubric.md) | Por que o bench, como inteligência de decisão, está em 100/100. |
| 4 | [slide-creator-skill-blueprint.md](slide-creator-skill-blueprint.md) | Como o bench vira uma skill `slide-creator` autocontida, com bibliotecas, contracts e gates. |
| 5 | [implementation-readiness-gate.md](implementation-readiness-gate.md) | O que falta para o produto chegar a 100 operacional. |
| 6 | [deep/intelligence-graph.md](deep/intelligence-graph.md) | Como personas, dimensões, fontes, gaps e contratos conversam. |
| 7 | [full-comparison.md](full-comparison.md) | Comparação profunda por projeto, eixo e absorção. |
| 8 | [segmented-comparisons.md](segmented-comparisons.md) | Três comparações justas: Apps, Skills/Agentes e Engines/Runtime. |
| 9 | [comparison-matrix.md](comparison-matrix.md) | Mapa consolidado de absorção: 9 players × 108 microdimensões, sem vencedor absoluto. |
| 10 | [scenario-scorecards.md](scenario-scorecards.md) | Personas v4 por job-to-be-done recalculadas sobre a matriz 108D. |
| 11 | [scorecard.md](scorecard.md) | Scorecard e corte de MVP. |
| 12 | [gap-analysis.md](gap-analysis.md) | Gaps P0/P1/P2 e critérios de aceite. |
| 13 | [next-wave-absorption-plan.md](next-wave-absorption-plan.md) | Plano robusto da próxima wave para fechar gaps com evidência executável. |
| 14 | [absorption-roadmap.md](absorption-roadmap.md) | Sequência de implementação por fases. |
| 15 | [battle-card.md](battle-card.md) | Argumento competitivo contra Gamma. |
| 16 | [bench-output-dash.json](bench-output-dash.json) | Saída canônica para dashboard. |
| 17 | [quality-audit.md](quality-audit.md) | Auditoria final de completude e qualidade. |
| 18 | [MANIFEST.json](MANIFEST.json) | Manifest estruturado com todos os arquivos e papéis. |

## Inventários

| Documento | Conteúdo |
|---|---|
| [inventory-slides-creator.json](inventory-slides-creator.json) | Estado interno resumido do squad. |
| [inventory-open-source-stack.json](inventory-open-source-stack.json) | Inventário estruturado dos 8 projetos externos. |
| [repo-metrics.md](repo-metrics.md) | Métricas reais dos clones locais. |
| [repo-metrics.json](repo-metrics.json) | Métricas dos clones em formato estruturado. |
| [external-inventory.md](external-inventory.md) | Inventário narrativo dos projetos externos. |
| [internal-squad-audit.md](internal-squad-audit.md) | Auditoria do nosso `slides-creator`. |
| [inventories/ppt-master.md](inventories/ppt-master.md) | Dossiê de renderer nativo editável. |
| [inventories/presenton.md](inventories/presenton.md) | Dossiê de app/API/MCP/self-hosted. |
| [inventories/pptagent.md](inventories/pptagent.md) | Dossiê de planejamento/reflexão. |
| [inventories/banana-slides.md](inventories/banana-slides.md) | Dossiê de UX prompt-to-edit e vídeo. |
| [inventories/presentation-ai.md](inventories/presentation-ai.md) | Dossiê de editor web/outlines/temas. |
| [inventories/powerpoint-skill.md](inventories/powerpoint-skill.md) | Dossiê de skill técnica, OMML e diagramas. |
| [inventories/slide-deck-ai.md](inventories/slide-deck-ai.md) | Dossiê de CLI Python e providers. |
| [inventories/presentagent-2.md](inventories/presentagent-2.md) | Dossiê de multimodal research→vídeo. |

## Deep Dives

| Documento | Pergunta respondida |
|---|---|
| [deep/coverage-map.md](deep/coverage-map.md) | Quais capacidades faltam, em ordem de cobertura? |
| [deep/matrix-methodology.md](deep/matrix-methodology.md) | Como a matriz v4 pontua 108 microdimensões, pesos e evidências. |
| [deep/scoring-transparency.md](deep/scoring-transparency.md) | Fórmula, escala, bandas, confiança e regras de leitura da pontuação. |
| [deep/micro-capability-matrix.md](deep/micro-capability-matrix.md) | Espelho deep da matriz completa 108D com perguntas operacionais por linha. |
| [deep/slides-creator-micro-gap-map.md](deep/slides-creator-micro-gap-map.md) | Onde a skill SINKRA perde/vence em cada microcapacidade e o que absorver. |
| [deep/micro-leaderboard-by-group.md](deep/micro-leaderboard-by-group.md) | Quem lidera cada grupo e o gap médio contra a SINKRA. |
| [deep/segmented-methodology.md](deep/segmented-methodology.md) | Por que separar apps, skills/agentes e engines/runtime. |
| [deep/evidence-by-dimension.md](deep/evidence-by-dimension.md) | Evidência resumida, melhor referência e regra de absorção por dimensão. |
| [deep/evidence-strength-map.md](deep/evidence-strength-map.md) | Evidência por player com força de prova, limitações e caminhos locais. |
| [deep/segment-deep-analysis.md](deep/segment-deep-analysis.md) | Comparação profunda por segmento: apps, skills/agentes e engines/runtime. |
| [deep/absorption-decision-table.md](deep/absorption-decision-table.md) | Tabela operacional capability → fonte → prioridade → artifact alvo. |
| [deep/consolidated-research-archive.md](deep/consolidated-research-archive.md) | O que foi aproveitado da pesquisa antiga de `docs/research` e o que foi substituído. |
| [deep/renderer-native-pptx.md](deep/renderer-native-pptx.md) | Como fechar o gap de PPTX editável real? |
| [deep/api-mcp-runtime.md](deep/api-mcp-runtime.md) | Como transformar a skill em runtime/API? |
| [deep/agentic-planning-reflection.md](deep/agentic-planning-reflection.md) | Como absorver planejamento/reflexão sem perder SINKRA? |
| [deep/editor-ux-prompt-to-edit.md](deep/editor-ux-prompt-to-edit.md) | Como chegar em uma UX comparável ao Gamma? |
| [deep/design-100-gap-plan.md](deep/design-100-gap-plan.md) | Como gabaritar a categoria Design com artifacts, render review e brand/template manifest. |
| [deep/template-volume-benchmark.md](deep/template-volume-benchmark.md) | Quantidade real de templates, decks, temas e gaps de volume contra os players. |
| [deep/license-risk-assessment.md](deep/license-risk-assessment.md) | O que pode ser copiado, inspirado ou evitado? |
| [deep/implementation-playbook.md](deep/implementation-playbook.md) | Como executar a absorção em waves e stories? |
| [deep/acceptance-test-plan.md](deep/acceptance-test-plan.md) | Como provar que a stack ficou boa o suficiente? |
| [deep/reproducible-local-runs.md](deep/reproducible-local-runs.md) | Como rodar os projetos externos de forma reprodutível? |
| [deep/open-source-to-sinkra-map.md](deep/open-source-to-sinkra-map.md) | Como cada projeto vira componente SINKRA? |
| [deep/persona-weight-methodology.md](deep/persona-weight-methodology.md) | Por que cada persona valoriza dimensões diferentes? |
| [deep/intelligence-graph.md](deep/intelligence-graph.md) | Como os artefatos formam uma inteligência navegável? |
| [deep/repo-notes.md](deep/repo-notes.md) | Notas brutas de leitura dos repositórios. |

## Contratos e Execução

| Documento | Conteúdo |
|---|---|
| [contracts/api-contract.md](contracts/api-contract.md) | Contrato API P0 para geração, review, export e import de templates. |
| [contracts/mcp-contract.md](contracts/mcp-contract.md) | Ferramentas MCP e limites de segurança. |
| [contracts/native-ir-contract.md](contracts/native-ir-contract.md) | IR nativo entre DeckSpec e renderer PPTX. |
| [contracts/qa-rubric.md](contracts/qa-rubric.md) | Rubrica QA de narrativa, fontes, design, editabilidade e técnica. |
| [contracts/qa-rubric.json](contracts/qa-rubric.json) | Rubrica QA estruturada. |
| [architecture-blueprint.md](architecture-blueprint.md) | Arquitetura alvo. |
| [architecture-blueprint.mmd](architecture-blueprint.mmd) | Diagrama Mermaid da arquitetura. |
| [dependency-graph.md](dependency-graph.md) | Dependências de implementação. |
| [implementation-readiness-gate.md](implementation-readiness-gate.md) | Gate P0/P1/P2 para transformar bench 100 em produto 100. |
| [implementation-readiness-gate.json](implementation-readiness-gate.json) | Gate de implementação estruturado para dashboard e backlog. |

## Decisão, Riscos e Backlog

| Documento | Conteúdo |
|---|---|
| [ADR-001-absorption-strategy.md](ADR-001-absorption-strategy.md) | Decisão de absorção modular em vez de fork único. |
| [risk-register.md](risk-register.md) | Registro de riscos narrativo. |
| [risk-register.json](risk-register.json) | Registro de riscos estruturado. |
| [bench-completeness-rubric.md](bench-completeness-rubric.md) | Rubrica que separa completude do bench de implementação do produto. |
| [bench-completeness-rubric.json](bench-completeness-rubric.json) | Rubrica de completude estruturada. |
| [scenario-scorecards.md](scenario-scorecards.md) | Scores por cenário de uso. |
| [scenario-scorecards.json](scenario-scorecards.json) | Scores por cenário estruturados. |
| [next-wave-absorption-plan.md](next-wave-absorption-plan.md) | Plano Wave 3 para converter gaps 108D em entregas executáveis, gates e meta de score. |
| [next-wave-absorption-plan.json](next-wave-absorption-plan.json) | Plano Wave 3 estruturado para automação/dashboard. |
| [presentation-brief.md](presentation-brief.md) | Roteiro para apresentação executiva. |
| [presentation-brief.json](presentation-brief.json) | Storyline estruturada consumível pelo dashboard. |
| [dashboard-intelligence.md](dashboard-intelligence.md) | Regras para o dash apresentar tese, prova, contexto e execução. |
| [slide-creator-skill-blueprint.md](slide-creator-skill-blueprint.md) | Blueprint bench→skill: absorção por projeto, decision tree, artifact contract, scorecard e killer items. |
| [slide-creator-skill-blueprint.json](slide-creator-skill-blueprint.json) | Blueprint estruturado para dash/automação/skill sync. |
| [story-ready-backlog.md](story-ready-backlog.md) | Backlog pronto para virar stories formais. |
| [evidence-ledger.md](evidence-ledger.md) | Claims ligados a evidências locais. |
| [evidence-ledger.json](evidence-ledger.json) | Evidence ledger estruturado. |

## Veredito

Não existe um único projeto open-source que seja “o Gamma open-source completo” e também respeite nossas exigências de editabilidade, governança e rastreabilidade. A resposta correta é uma composição:

`slides-creator` + `ppt-master` + Presenton + PPTAgent + padrões de UX de banana-slides/presentation-ai + disciplina técnica de powerpoint-skill.
