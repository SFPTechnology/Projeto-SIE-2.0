# SIE-F08 — Proteções e distribuição

Estado: Ready for Review — QA3 local aprovado, CI remoto pendente. Base: F07 5402ca7. Criada antes do código F08.

Requisitos: F08_EXECUTAR.md tasks 08.01–08.10. Não altera aceites anteriores nem produção.

## Critérios de aceite
- [x] Dispositivos tipados e origem explícita, sem produto fictício certificado.
- [x] Curtos máximo/mínimo por impedância declarada e caminhos de falta explícitos.
- [x] Sobrecarga I2, interrupção e energia térmica com domínio limitado.
- [x] TN/TT/IT, DR, DPS e seletividade dependem de dados aplicáveis; faltantes ficam pendentes.
- [x] Balanceamento preserva decisão do projetista; seleção finita termina.
- [x] Quadro e memória vinculados ao F07 e revisão, com invalidação e API/CLI.
- [x] Testes independentes, regressão e QA-01/02/03 registrados.

## Arquivos

- docs/implantacao-sie-2-0/F08/F08_EXECUTAR.md
- docs/implantacao-sie-2-0/F08/FONTES.md
- docs/implantacao-sie-2-0/F08/QA-01.md
- docs/implantacao-sie-2-0/F08/QA-02.md
- docs/implantacao-sie-2-0/F08/QA-03.md
- docs/implantacao-sie-2-0/F08/RELATORIO_EXECUCAO.md
- docs/stories/SIE-F08.md
- restructuring/apps/api/sie_api/data/protection_coordination_schneider_f08.json
- restructuring/apps/api/sie_api/data/protection_schneider_f08.json
- restructuring/apps/api/sie_api/protection_api.py
- restructuring/apps/api/sie_api/protection_cli.py
- restructuring/apps/api/sie_api/protection_contracts_f08.py
- restructuring/apps/api/sie_api/protection_f08.py
- restructuring/apps/api/sie_api/protection_registry_f08.py
- restructuring/apps/api/sie_api/protection_storage_f08.py
- restructuring/apps/api/tests/test_protection_adversarial_f08.py
- restructuring/apps/api/tests/test_protection_f08.py
- restructuring/apps/api/tests/test_protection_independent_f08.py
- restructuring/apps/api/tests/test_protection_integration_f08.py
- restructuring/apps/api/tests/test_protection_pair_adversarial_f08.py
- restructuring/apps/api/tests/test_protection_registry_f08.py
- restructuring/apps/web/protecoes-demo.json
- restructuring/apps/web/protecoes.html
- restructuring/apps/web/protecoes.js
- restructuring/examples/f08_protecoes_demo.json
- docs/sie-orchestrator/ORCHESTRATOR_STATE.json
- restructuring/apps/api/sie_api/main.py
- restructuring/apps/web/index.html
- restructuring/e2e/test_browser_flow.py

## Limites
Fontes e valores declarados pelo cliente não são homologação. Não substitui inspeções, ensaios ou aprovação profissional.
