# SIE-F07 — Condutores e queda por percurso

Status: Ready for Review — recorte fonte-vinculado completo localmente, QA3 aprovado; CI do incremento em conferência. Origem: F07_EXECUTAR.md, tasks 07.01–07.10.
Base: d83fff44af4a543e66065c3c8423cc8a339ae060 (F06). Aceites F00–F06 preservados.

- [x] 07.01 Inventário e matriz de equivalência.
- [x] 07.02 Critérios independentes e testados.
- [x] 07.03 Resolução por versão e rejeição de condições incompatíveis.
- [x] 07.04 Todos os trechos e percursos considerados.
- [x] 07.05 Queda AC e acumulação topológica restrita ao modelo suportado.
- [x] 07.06 Precisão interna separada da apresentação.
- [x] 07.07 Critérios obrigatórios explícitos, sem aprovação por falta de dados.
- [x] 07.08 Histórico e invalidação em cascata.
- [x] 07.09 Memória, CLI e API.
- [x] 07.10 Referência independente, regressão e QA3.

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

Atualização especializada: itens07.03/05/07/10 concluídos localmente no recorte finito fonte-vinculado. Sem reabertura das fases anteriores; CI do incremento deve ser conferido antes do encerramento.


## Publicação e verificação

Incremento de estudo publicado em [69b533a9](https://github.com/SFPTechnology/Projeto-SIE-2.0/commit/69b533a9ea315022eecb247539a551950d81e5ed), árvore `f0a64095e1a7fad807fc97869d6eb1888e786c07` idêntica à local. CI do mesmo código: API 787/F00 34 (run 39720730426), Chromium 30 (39720730315), AIOX 18 + 4 gates (39720730305), todos completed/success. Encerramento documental não modifica código. Story integral continua Blocked e os quatro itens parciais continuam abertos; nenhuma liberação normativa ou da fase seguinte.

## Continuação autorizada — especialista F07

Missão adicional derivada dos itens07.03/05/07/10 já existentes: catálogo finito fonte-vinculada PrysmianRev9, seleção conjunta por circuito e trecho, N/PE e limites de origem/terminal explícitos, referência independente tabulada, QA3 e CI. A fonte foi obtida no domínio oficial e as páginas5/6/9/14/15/20/21/24/33 conferidas; arquivo temporário não é redistribuído. Aceites F01–F06 preservados. Decisão de arquitetura: DECISAO_ARQUITETURA_CATALOGO.md.

- [x] Vincular dados e condições do catálogo com hash/edição/páginas.
- [x] Implementar resolver do servidor e seleção conjunta monotônica.
- [x] Demonstrar casos tabulados/aritméticos independentes e transições.
- [x] Integrar CLI/API/UI e histórico/invalidação pelo catálogo.
- [ ] Conferir CI do incremento publicado (QA3 e regressão locais concluídos).

## File list da vinculação final

- docs/implantacao-sie-2-0/F07/DECISAO_ARQUITETURA_CATALOGO.md
- docs/implantacao-sie-2-0/F07/VINCULACAO_FONTES.md
- docs/implantacao-sie-2-0/F07/CONTRATO.md
- docs/implantacao-sie-2-0/F07/RELATORIO_EXECUCAO.md
- docs/implantacao-sie-2-0/F07/QA-01_VINCULACAO.md
- docs/implantacao-sie-2-0/F07/QA-02_VINCULACAO.md
- docs/implantacao-sie-2-0/F07/QA-03_VINCULACAO.md
- docs/sie-orchestrator/ORCHESTRATOR_STATE.json
- docs/stories/SIE-F07.md
- restructuring/apps/api/sie_api/conductor_registry_f07.py
- restructuring/apps/api/sie_api/conductor_selection_f07.py
- restructuring/apps/api/sie_api/data/conductor_prysmian_rev9_f07.json
- restructuring/apps/api/sie_api/conductor_api.py
- restructuring/apps/api/sie_api/conductor_cli.py
- restructuring/apps/api/tests/test_conductor_binding_f07.py
- restructuring/examples/f07_selecao_fonte_vinculada.json
- restructuring/apps/web/condutores-selecao-demo.json
- restructuring/apps/web/condutores.html
- restructuring/apps/web/condutores.js
- restructuring/e2e/test_browser_flow.py

Validação local final:864API/142F07(77novos),32Chromium,34golden,18AIOX;QA01/02/03APROVADO no recorte.
