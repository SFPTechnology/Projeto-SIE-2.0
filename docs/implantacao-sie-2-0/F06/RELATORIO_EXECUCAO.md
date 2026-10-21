# F06 — Cálculo de demanda e alimentação elétrica

Data: 21/10/2026. **ESTADO: BLOCKED — incremento de estudo implementado e testado; gate normativo não atendido.**
Branch: `feat/f06-demanda-alimentacao`. Base local e remota F05: `9e1e50c428324a04280f937a6097f94c831e90e6`. F05 DONE e passagem para F06 conferidos no GitHub e no estado canônico. Sem reabrir aceites F01/F00/F05.
Fonte de estado: `docs/sie-orchestrator/ORCHESTRATOR_STATE.json`. Código em `restructuring/apps/api/sie_api/demand*.py`; contrato em CONTRATO.md.

|Task|Resultado real / evidência|
|---|---|
|06.01|IMPLEMENTED: categoria, critério e regra independentes; ausência e conflito geram pendência. Testes de classificação/finalidade.|
|06.02|IMPLEMENTED: P/Q/S por ambiente, circuito, quadro, fonte e empreendimento; quantidade F04 uma vez por mapa bijetivo; soma VA escalar explicitada.|
|06.03|BLOCKED para regras normativas: algoritmo versionado, fatores por grupo ou blocos progressivos, faixas [inferior,superior), escopo e evidências implementados; nenhum coeficiente normativo habilitado.|
|06.04|IMPLEMENTED: FINAL_CIRCUIT/FEEDER/ENTRANCE/STUDY separados; fator a montante não libera Ib de ramo abaixo do alvo.|
|06.05|IMPLEMENTED para estudo: Ib mono/trifásico e fonte, tensão/conexão/equilíbrio explícitos, precisão e fórmula registradas. Integração definitiva com dimensionamento aguarda gate normativo; não substitui Ib canônica.|
|06.06|IMPLEMENTED: grafo F05 único, alvos circuito/quadro/fonte, propagação sem dupla contagem e ponte F04→F02 por identidade explícita; rascunho projetado exige salvar revisão F05.|
|06.07|IMPLEMENTED: UUID histórico imutável, comparação de cenário/equipamento, fatores/configuração no fingerprint; mudança de topologia ou levantamento marca histórico stale.|
|06.08|IMPLEMENTED: memória por grupo, parcela, fator, regra/fonte/edição, hipóteses, dados ausentes e pendências; CLI, API e interface técnica com exportação.|
|06.09|PARCIAL: comparação exata de distribuidora/localidade/tipologia/edição e área confirmada bloqueia escopo incompatível. Vigência e conformidade oficial não habilitadas.|

## Testes observados

- `PYTHONPATH=restructuring/apps/api python -m pytest -q restructuring/apps/api/tests`: **637 passed**, 12,36 s; um aviso de depreciação Starlette/httpx.
- `... pytest -q restructuring/apps/api/tests/test_demand_f06.py`: **33 passed**, 0,50 s.
- `SIE_E2E_BROWSER_PATH=/tmp/f06-chrome/run PYTHONPATH=restructuring/apps/api python -m pytest -xq restructuring/e2e`: **26 passed**, 45,18 s; inclui 25 anteriores e um fluxo F06 com cálculo, edição, stale, exportação bloqueada, VERIFIED recusado e tela de 390 px.
- Chromium 153 temporário. Download padrão Playwright truncado; primeira inicialização falhou por GPU/GL. Execução passou com wrapper temporário desativando GPU/rasterizador/composição/GL; nenhuma alteração no navegador pessoal.
- `python scripts/f00_golden.py --verify`: **34 casos**, fixture intacta.
- `npm run lint`, `npm run typecheck`, `npm test` (**18 testes**), `npm run build`: **PASS**, após instalar dependências locais faltantes sem alterar manifests.
- CLI calculou exemplo sintético e comparou cenário ao próprio cenário, com saída JSON real. `node --check .../demanda.js` e `git diff --check`: PASS.
- Não houve deploy, merge, banco real ou uso de serviço pago. CodeRabbit não disponível; análise automatizada externa não executada.

## QA3 e correções

|Perspectiva|Veredito sobre incremento|Evidência|
|---|---|---|
|QA-01|APROVADO para código de estudo|QA-01.md: escopos, ponte F04/F02, identidade, parcelas, persistência, concorrência e testes|
|QA-02|BLOQUEADO para liberação normativa|QA-02.md: matemática sintética aprovada; falta vínculo confiável de coeficientes/condições e fixtures normativas independentes|
|QA-03|APROVADO para integração/interface de estudo|QA-03.md: autenticação local, memória segura, invalidação, exportação e navegador|

Três perspectivas críticas do mesmo assistente; não equivalem a três auditorias humanas independentes. DevOps delegado apenas para publicação conforme AGENTS.md/constituição.

Corrigidos no ciclo: escopos globais sem extrapolar fator a ramos; ponte explícita com quantidade única e conflitos de tensão/fase; Ib de fonte com conexão declarada; modelo progressivo com referência sintética independente; memória antiga invalidada ao editar; regra VERIFIED do cliente não promove confiança; texto não interpretado como HTML. Não foi relaxado resultado esperado para ocultar falha de cálculo.

## Gate aberto e retomada

**Gate não atendido: regras normativas verificadas em fixtures independentes.** Não é falta de autorização para desenvolver: o registro atual não contém os fatores e condições comprovados para o motor novo.

Fonte primária local encontrada: `Arquivos_Diversos/Norma_EDP/PT.DT.PDN.00068_V9.pdf`, SHA256 `b14f414001d9831f91bbef84f022c5164f367431cc6a209e5fb34b4e48f20810`. Texto derivado aponta item 5.5.2, grupos a–i e tabelas 005–009+, mas não foi usado como coeficiente homologado. F01 já registra EDP-DEMANDA-GRUPOS como não homologado no inventário. Preservar os aceites anteriores não cria células ausentes.

Próxima ação nesta mesma F06: conferir células/notas/condições das fontes aplicáveis, implementar expressões específicas necessárias, conectar registro confiável do servidor e casos de referência independentes, revalidar QA-02 e só então habilitar consumo definitivo de Ib pelos motores. Não é necessário copiar prompt nem preencher CSV. Passagem à fase seguinte **não liberada**.

## Versionamento e publicação

Código e registros publicados em [`b7f782d1c9d274c6e7c5fe9c00460edca74b02fc`](https://github.com/SFPTechnology/Projeto-SIE-2.0/commit/b7f782d1c9d274c6e7c5fe9c00460edca74b02fc). Árvore remota `36b5ffbb8b51ba654bee562bbf7d8b8bd6b6ea47` exatamente igual ao commit local `206f1a97ad4feb308dd97d8f65e14681430a3148`. Publicação sem rejeição; sem PR, merge ou deploy. Os três workflows de CI foram conferidos como completed/success no mesmo head_sha publicado. Main e ambiente publicado preservados.


CI do mesmo SHA de código publicado:

|Workflow|Run|Resultado observado|
|---|---|---|
|API/F00|[39666801001](https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39666801001)|completed/success; 637 testes, 1 aviso, 11,75 s; 34 golden intactos|
|AIOX|[39666800987](https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39666800987)|completed/success; 18 testes, lint, typecheck e build|
|Chromium|[39666801008](https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39666801008)|completed/success; 26 testes, 45,53 s; todas as etapas do job aprovadas|

O checkpoint posterior atualiza somente documentação e estado, sem alterar o código validado. CI verde não encerra o gate normativo: F06 permanece BLOCKED.
