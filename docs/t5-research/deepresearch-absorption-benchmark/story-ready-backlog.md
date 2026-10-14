# Story-Ready Backlog

| Story | Objetivo | AC principal |
| --- | --- | --- |
| DRB-001 | Implementar DeepResearchRunner contract | Outputs obrigatórios gerados para run dry-run |
| DRB-002 | Criar adapter dzhng baseline | 5 tasks públicas executam com trace sintético |
| DRB-003 | Criar evaluator wrapper LiveDRBench/DRBench | claims.yaml recebe score determinístico |
| DRB-004 | Projetar dashboard execution-results | Dash mostra planned/running/completed por task |

## Pós Dry-Run

| Story | Objetivo | AC principal |
| --- | --- | --- |
| DRB-005 | Substituir adapter dzhng stub por execução real | 40 tasks geram outputs normalizados sem quebrar contrato |
| DRB-006 | Substituir GPT-Researcher stub por execução real | `claims.yaml` e `sources.yaml` saem do run real, não do fixture stub |
| DRB-007 | Implementar evaluator deterministic pass | `rubric-results.yaml` calcula recall/support usando gold claims |
| DRB-008 | Atualizar dashboard execution mode | Dash separa `contract_dry_run`, `real_adapter_run` e `judge_evaluated` |
