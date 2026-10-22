# SIE-F06 — Demanda e alimentação
Estado: DONE (implementação/vinculação computacional, QA3 e CI aprovados). Requisitos: F06_EXECUTAR.md, tasks 06.01–06.09.

- [x] Classificação explícita, distinta da regra; escopo e faixas verificáveis.
- [x] Totalização P/Q/S e agregação pela conectividade F05, sem dupla contagem.
- [x] Motor versionado e Ib com fórmula/hipóteses, sem fator padrão.
- [x] Cenários históricos, memória e invalidação por alteração de entrada.
- [x] Compatibilidade de distribuidora sem aprovação normativa automática.
- [x] Testes, regressão e QA3 registrados.
- [x] Coeficientes/condições do recorte EDP V09 no registro confiável e fixtures independentes. Consumo definitivo de Ib não é homologado automaticamente.

Arquivos: ver lista abaixo. Normas/fatores não confirmados bloqueiam o cálculo correspondente.


## Arquivos do incremento

- `docs/stories/SIE-F06.md`
- `docs/sie-orchestrator/ORCHESTRATOR_STATE.json`
- `docs/implantacao-sie-2-0/F06/F06_EXECUTAR.md`
- `docs/implantacao-sie-2-0/F06/CONTRATO.md`
- `docs/implantacao-sie-2-0/F06/RELATORIO_EXECUCAO.md`
- `docs/implantacao-sie-2-0/F06/QA-01.md`
- `docs/implantacao-sie-2-0/F06/QA-02.md`
- `docs/implantacao-sie-2-0/F06/QA-03.md`
- `restructuring/apps/api/sie_api/demand.py`
- `restructuring/apps/api/sie_api/demand_api.py`
- `restructuring/apps/api/sie_api/demand_cli.py`
- `restructuring/apps/api/sie_api/main.py`
- `restructuring/apps/api/tests/test_demand_f06.py`
- `restructuring/apps/web/demanda.html`
- `restructuring/apps/web/demanda.js`
- `restructuring/apps/web/demanda-demo.json`
- `restructuring/apps/web/index.html`
- `restructuring/examples/f06_demanda_demo.json`
- `restructuring/e2e/test_browser_flow.py`

## Incremento de vinculação autorizado

- [x] Registrar fonte oficial, hashes, páginas/tabelas/células e condições.
- [x] Resolver IDs de regras no servidor; recusar coeficientes enviados como substituição.
- [x] Aplicar base kW/quantidade e exceções do documento sem extrapolar finalidade.
- [x] Conferir exemplos da própria fonte por valores esperados independentes.
- [x] Regressão e QA3 da vinculação; checkpoint publicado e três workflows CI aprovados no SHA 45cbfba3.

Arquivos adicionais: `demand_registry.py`, `data/demand_edp_v09.json`, `test_demand_binding_f06.py`, `f06_demanda_edp_v09_referencia.json`, `demanda-edp-demo.json`, `VINCULACAO_FONTES.md`; API/CLI/interface/testes E2E e registros anteriores atualizados.
