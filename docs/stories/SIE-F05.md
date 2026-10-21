# SIE-F05 — Topologia elétrica e condições por trecho
Status: Ready for Review. Fonte: F05_EXECUTAR.md, tasks 05.01–05.09.

- [x] Fonte declarada, confirmação e impedância sem inferência.
- [x] Quadros/barras e vínculos únicos sobre grafo F02, sem fonte paralela.
- [x] Percursos fonte → quadro → carga; trechos heterogêneos e comprimentos exatos.
- [x] Influências externas com origem/método; revisão e invalidação.
- [x] CLI, API local autenticada e editor técnico com recomposição.
- [x] Cenários válidos/inválidos, concorrência, regressão e E2E.
- [x] Pareceres QA-01, QA-02 e QA-03 e estado persistente.

## Arquitetura
Preservar contratos/snapshots F02: documento de transporte F05 associa metadados por UUID ao agregado canônico. Persistência mantém conectividade somente em installation_snapshot; metadados separados não duplicam arestas. F05 não dimensiona nem homologa; múltiplas fontes isoladas permitidas, paralelismo recusado pela F02.

## File list
- restructuring/apps/api/sie_api/topology.py
- restructuring/apps/api/sie_api/topology_api.py
- restructuring/apps/api/sie_api/topology_cli.py
- restructuring/apps/api/sie_api/main.py
- restructuring/apps/api/sie_api/installation_storage_api.py
- restructuring/apps/api/tests/test_topology_f05.py
- restructuring/apps/web/topologia.html
- restructuring/apps/web/topologia.js
- restructuring/apps/web/topologia-demo.json
- restructuring/apps/web/index.html
- restructuring/examples/f05_topologia_demo.json
- restructuring/e2e/test_browser_flow.py
- docs/implantacao-sie-2-0/F05/CONTRATO.md
- docs/implantacao-sie-2-0/F05/RELATORIO_EXECUCAO.md
- docs/implantacao-sie-2-0/F05/QA-01.md
- docs/implantacao-sie-2-0/F05/QA-02.md
- docs/implantacao-sie-2-0/F05/QA-03.md
- docs/sie-orchestrator/ORCHESTRATOR_STATE.json
- docs/sie-orchestrator/NEXT_ACTION.md
- docs/sie-orchestrator/PROJECT_STATE.md
- docs/sie-orchestrator/EXECUTION_HISTORY.md
- docs/sie-orchestrator/EXECUTION_QUEUE.md
- docs/sie-orchestrator/VALIDATION_MATRIX.md

## Checkpoint
Código local fb5e3e382db973a989fb499a07a62404d83d80eb pronto e validado. Publicação rejeitada por auto-review; CI remoto não executado; aprovação explícita da publicação F05 necessária. Story permanece Ready for Review, fase HUMAN_REQUIRED para esta operação.
- docs/sie-orchestrator/BLOCKER_REGISTRY.md
