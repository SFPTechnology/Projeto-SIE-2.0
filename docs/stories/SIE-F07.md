# SIE-F07 — Condutores e queda por percurso

Status: Done — recorte computacional com fonte vinculada, seleção multicritério, QA3 e CI aprovados. Origem: F07_EXECUTAR.md, tasks 07.01–07.10.
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

Atualização especializada: itens 07.03/05/07/10 concluídos localmente no recorte finito fonte-vinculado. Sem reabertura das fases anteriores; CI do incremento conferido no encerramento abaixo.


## Histórico da publicação inicial de estudo

Incremento de estudo publicado em [69b533a9](https://github.com/SFPTechnology/Projeto-SIE-2.0/commit/69b533a9ea315022eecb247539a551950d81e5ed), árvore `f0a64095e1a7fad807fc97869d6eb1888e786c07` idêntica à local. CI do mesmo código: API 787/F00 34 (run 39720730426), Chromium 30 (39720730315), AIOX 18 + 4 gates (39720730305), todos completed/success. Encerramento documental não modifica código. Naquele checkpoint, a story integral estava Blocked e quatro itens permaneciam parciais. Esse estado histórico foi superado pela vinculação e pelo encerramento computacional abaixo; não houve liberação normativa de instalação.

## Continuação autorizada — especialista F07

Missão adicional derivada dos itens 07.03/05/07/10 já existentes: catálogo finito fonte-vinculada Prysmian Rev9, seleção conjunta por circuito e trecho, N/PE e limites de origem/terminal explícitos, referência independente tabulada, QA3 e CI. A fonte foi obtida no domínio oficial e as páginas 5/6/9/14/15/20/21/24/33 conferidas; arquivo temporário não é redistribuído. Aceites F01–F06 preservados. Decisão de arquitetura: DECISAO_ARQUITETURA_CATALOGO.md.

- [x] Vincular dados e condições do catálogo com hash/edição/páginas.
- [x] Implementar resolver do servidor e seleção conjunta monotônica.
- [x] Demonstrar casos tabulados/aritméticos independentes e transições.
- [x] Integrar CLI/API/UI e histórico/invalidação pelo catálogo.
- [x] Conferir CI do incremento publicado no SHA 14c64bbc; QA3, regressão local e três workflows remotos aprovados.

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

Validação local final: 864 API, 142 F07 (77 novos), 32 Chromium, 34 golden e 18 AIOX; QA-01/02/03 APROVADO no recorte.


## Encerramento computacional verificado — 22/10/2026

**DONE no recorte com fonte vinculada.** Código [14c64bbc](https://github.com/SFPTechnology/Projeto-SIE-2.0/commit/14c64bbcd615ba81d9d0eae60b91b3f24337402b), árvore `f4ac4d73c369a1f7360484cd2d0b307edea8816b` idêntica à local. CI do mesmo código: API 864 e F00 34 ([39775756669](https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39775756669)); Chromium 32 ([39775756799](https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39775756799)); AIOX 18 e quatro gates ([39775757139](https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39775757139)). Todos completed/success, com logs e etapas conferidos.

Os dez critérios desta fase foram verificados no recorte; não há achado QA impeditivo remanescente. O fechamento documental não altera código. F08 liberada para desenvolvimento; próximo arquivo `F08_EXECUTAR.md`. Conformidade profissional, uso definitivo de dimensionamento e proteção F08 não são presumidos; flags correspondentes permanecem falsas/pendentes. Nenhum PR, merge em main ou deploy.
