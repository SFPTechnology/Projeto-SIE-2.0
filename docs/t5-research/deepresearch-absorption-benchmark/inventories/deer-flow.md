# Inventory — DeerFlow

- Slug: `deer-flow`
- Repo: [bytedance/deer-flow](https://github.com/bytedance/deer-flow)
- Classe: `agentic_platform`
- Linguagem: `Python`
- Licença: `MIT`
- Stars/Forks/Issues: 68402 / 9106 / 819
- Score de absorção: **75.9**
- Decisão: `absorb_core_patterns`

## Classificação

Plataforma agentic com Gateway/FastAPI, LangGraph runtime, skills, MCP, sandbox e journaling.

## Padrão Absorvível

run_lifecycle_journal_skills

Sinal forte: Run lifecycle, skill frontmatter allowed-tools, RunJournal/StreamBridge.

## Risco Principal

docker_socket_process_local_state_skill_mutation

Risco da revisão: Estado process-local, Docker socket, mutação de skills e contexto vindo do cliente.

## Scores Por Dimensão

| Dimensão | Score |
| --- | --- |
| architecture_absorption | 96 |
| trace_observability | 84 |
| private_kb_grounding | 68 |
| evaluation_value | 42 |
| implementation_maturity | 98 |
| scientific_pipeline | 40 |
| training_methodology | 36 |
| product_ux_reference | 96 |
| compliance_safety | 86 |
| sinkra_fit | 96 |

## Artefatos Locais

| Arquivo |
| --- |
| `outputs/decoded/deer-flow/phase-2-extraction/deep-static-findings.yaml` |
| `outputs/decoded/deer-flow/phase-3-fusion/deep-component-map.md` |
| `outputs/decoded/deer-flow/phase-6-synthesis/absorption-patterns.md` |
| `outputs/decoded/deer-flow/phase-8-documentation/deep-anatomist-notes.md` |
