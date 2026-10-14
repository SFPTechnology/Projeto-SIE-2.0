# Risk Register

| ID | Risco | Prob. | Impacto | Severidade | Mitigação | Owner |
|---|---|---:|---:|---:|---|---|
| R-001 | Renderer gera PPTX que abre, mas não é editável | Alta | Crítico | 10 | `editability-report.json` obrigatório e fixture PowerPoint. | `design-renderer` |
| R-002 | UI/editor começa antes do core | Média | Alto | 8 | Gate: editor só depois de CLI/API/render. | `slide-chief` |
| R-003 | Código AGPL de banana-slides contamina produto | Média | Crítico | 9 | Usar como benchmark de UX; ADR antes de reuso. | `devops` + legal |
| R-004 | API duplica lógica da CLI | Média | Alto | 8 | Core único chamado por CLI/API/MCP. | `slides-api` |
| R-005 | QA vira checklist sem evidência | Média | Alto | 7 | Evidence ledger e reports obrigatórios. | `qa-inspector` |
| R-006 | Template import subestima PPTX corporativo | Alta | Médio | 7 | Subset inicial e unsupported-features report. | `template-curator` |
| R-007 | Ollama/local gera baixa qualidade | Alta | Médio | 6 | Separar smoke local de provider recomendado. | `slide-chief` |
| R-008 | PresentAgent-2 puxa escopo multimodal cedo demais | Média | Médio | 6 | P2 explícito, fora do MVP. | `slide-chief` |
| R-009 | Fontes quebram render em outra máquina | Média | Alto | 8 | Font registry, fallback e embed/subset policy. | `design-renderer` |
| R-010 | Claims sem fonte passam para deck executivo | Média | Crítico | 9 | Gate de fonte para claims críticos. | `content-architect` |

## Risco Existencial

O risco existencial é construir uma UI bonita que exporta slides ruins ou não editáveis. A mitigação é manter o caminho crítico em renderer + editability + QA antes de editor.
