# Inventory — MiroFlow

- Slug: `miroflow`
- Repo: [MiroMindAI/MiroFlow](https://github.com/MiroMindAI/MiroFlow)
- Classe: `agentic_benchmark_runtime`
- Linguagem: `Python`
- Licença: `Apache-2.0`
- Stars/Forks/Issues: 2977 / 312 / 24
- Score de absorção: **69.5**
- Decisão: `absorb_trace_tool_registry`

## Classificação

Runtime agentic benchmark por YAML com Orchestrator/ToolManager/TaskTracer.

## Padrão Absorvível

tasktracer_toolmanager_mcp_registry

Sinal forte: TaskTracer, sub-agent as tool, MCP registry declarativo, pass@k harness.

## Risco Principal

missing_config_broken_tool_boxed_output

Risco da revisão: Config ausente, tool-browsing quebrado, output boxed sem claims/sources.

## Scores Por Dimensão

| Dimensão | Score |
| --- | --- |
| architecture_absorption | 86 |
| trace_observability | 84 |
| private_kb_grounding | 68 |
| evaluation_value | 42 |
| implementation_maturity | 86.7 |
| scientific_pipeline | 40 |
| training_methodology | 36 |
| product_ux_reference | 42 |
| compliance_safety | 90 |
| sinkra_fit | 88 |

## Artefatos Locais

| Arquivo |
| --- |
| `outputs/decoded/miroflow/phase-2-extraction/deep-static-findings.yaml` |
| `outputs/decoded/miroflow/phase-3-fusion/deep-component-map.md` |
| `outputs/decoded/miroflow/phase-6-synthesis/absorption-patterns.md` |
| `outputs/decoded/miroflow/phase-8-documentation/deep-anatomist-notes.md` |
