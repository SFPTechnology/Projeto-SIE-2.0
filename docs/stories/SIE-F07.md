# SIE-F07 — Condutores e queda por percurso

Status: Blocked — incremento computacional Ready for Review; gates normativos pendentes. Origem: F07_EXECUTAR.md, tasks 07.01–07.10.
Base: d83fff44af4a543e66065c3c8423cc8a339ae060 (F06). Aceites F00–F06 preservados.

- [x] 07.01 Inventário e matriz de equivalência.
- [x] 07.02 Critérios independentes e testados.
- [ ] 07.03 Resolução por versão e rejeição de condições incompatíveis.
- [x] 07.04 Todos os trechos e percursos considerados.
- [ ] 07.05 Queda AC e acumulação topológica restrita ao modelo suportado.
- [x] 07.06 Precisão interna separada da apresentação.
- [ ] 07.07 Critérios obrigatórios explícitos, sem aprovação por falta de dados.
- [x] 07.08 Histórico e invalidação em cascata.
- [x] 07.09 Memória, CLI e API.
- [ ] 07.10 Referência independente, regressão e QA3.

## File list

- docs/stories/SIE-F07.md
- docs/sie-orchestrator/ORCHESTRATOR_STATE.json
- docs/implantacao-sie-2-0/F07/F07_EXECUTAR.md
- docs/implantacao-sie-2-0/F07/RELATORIO_EXECUCAO.md
- docs/implantacao-sie-2-0/F07/MATRIZ_LEGADO.md
- docs/implantacao-sie-2-0/F07/CONTRATO.md
- docs/implantacao-sie-2-0/F07/QA-01.md
- docs/implantacao-sie-2-0/F07/QA-02.md
- docs/implantacao-sie-2-0/F07/QA-03.md
- restructuring/apps/api/sie_api/conductor_f07.py
- restructuring/apps/api/sie_api/conductor_api.py
- restructuring/apps/api/sie_api/conductor_cli.py
- restructuring/apps/api/sie_api/main.py
- restructuring/apps/api/tests/test_conductor_f07.py
- restructuring/apps/web/condutores.html
- restructuring/apps/web/condutores.js
- restructuring/apps/web/condutores-demo.json
- restructuring/apps/web/index.html
- restructuring/examples/f07_condutores_demo.json
- restructuring/e2e/test_browser_flow.py

Casos computacionais aprovados não concluem os itens07.03/05/07/10 integrais. Ver relatório para evidências e bloqueios, sem reabrir fases anteriores.
