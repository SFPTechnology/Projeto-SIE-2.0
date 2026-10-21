# F05 — Topologia elétrica e condições de instalação
Data:21/10/2026. **ESTADO: DONE — implementação, QA3, publicação e CI aprovados**. Autorização explícita de publicação recebida em21/10/2026; bloqueio anterior resolvido. Passagem liberada para F06.
Branch:`feat/f05-topologia-eletrica`. Base observada local e no GitHub:`f388dde204fd4e9870796ff6cdcf77f9606aebe8` (F04 DONE). F02/F04 e aceites F01 preservados. Fonte canônica de estado:`docs/sie-orchestrator/ORCHESTRATOR_STATE.json`.

|Task|Implementação e evidência|
|---|---|
|05.01|Fonte F02 + SourceDetails/SourceImpedance com origem, confirmação e desconhecidos null; testes de frequência e fonte pendente|
|05.02|Quadros/localização F02, barras F05 com UUID e circuitos do mesmo quadro; testes bus e duplicate_origin|
|05.03|Grafo autoritativo F02; validação ciclos/órfãos/origem única via inspect_topology; teste cycle exige diagnóstico acyclic|
|05.04|Circuitos terminais/alimentadores e dispositivos F02 preservados; vínculos na API/editor e fases explícitas F05|
|05.05|Trechos com condições próprias, passagem física, material, condutores e origem; teste heterogêneo|
|05.06|Influências externas declaradas, ambiente e solo com origem/método; fingerprint e testes parametrizados de invalidação|
|05.07|report recompõe caminho fonte/quadro/carga, trechos ordenados e soma decimal exata; alternativas não somadas como série|
|05.08|CLI primeiro, API tipada/autenticada e editor técnico; inclusão via documento JSON, edição guiada e recomposição;3 E2E F05|
|05.09|Fixtures heterogêneas, árvores de fontes isoladas e casos inválidos;28 testes F05|

## Testes observados
- `python -m pytest -q restructuring/apps/api/tests`:604 passed,1 aviso StarletteDeprecationWarning,11,95s.
- `python -m pytest -q restructuring/apps/api/tests/test_topology_f05.py`:28 passed,0,73s.
- `SIE_E2E_BROWSER_PATH=/tmp/f05-browser-run python -m pytest -q restructuring/e2e`:25 passed,44,72s; inclui22 cenários anteriores e3 F05. Chromium153 local, GPU desativada; download padrão Playwright retornou ZIP truncado e foi substituído por instalação temporária isolada para os testes.
- `python scripts/f00_golden.py --verify`:34 casos,fixture intacta.
- `npm run lint`, `npm run typecheck`, `npm test`, `npm run build`:PASS,18 testes AIOX.
- `node --check restructuring/apps/web/topologia.js` e `git diff --check`:PASS.
- CLI validou exemplo sintético e produziu percursos. Inspeção visual desktop e móvel sem overflow horizontal.

## QA3 e correções
|Perspectiva|Veredito local|Registro|
|---|---|---|
|QA-01|APROVADO|QA-01.md — grafo único, proteção contra shadowing, alternativas de percurso, invalidação|
|QA-02|APROVADO,modelagem preliminar|QA-02.md — fases explícitas, precisão, trechos, bloqueio de cálculo definitivo|
|QA-03|APROVADO,ambiente local|QA-03.md — concorrência, autenticidade local, rascunhos, unidades, UX/E2E|
Os três pareceres são perspectivas do mesmo assistente; não auditorias humanas independentes. Sem achado impeditivo local aberto.

## Gates e limites
Gates locais demonstrados: QDG→QD1→circuitos; ciclos e órfãos recusados; comprimento/agrupamento/influências invalidam resultados dependentes. Snapshot F02 histórico sem alteração de schema. Persistência mantém uma única conectividade e preserva levantamento F04/histórico F03.
CI conferido: API, AIOX e Chromium completed/success no mesmo SHA publicado7c5547af06e6b569f493473ceb61cd6d224603da. Todos os gates aplicáveis à F05 demonstrados; passagem liberada para F06.
Sem cálculo normativo novo, aprovação ABNT, geometria inventada, curto-circuito definitivo, paralelismo de fontes, migração real, merge ou deploy. Cadastro completo de entidades e metadados ocorre por JSON técnico validado; não é editor gráfico de desenho. Regras normativas futuras permanecem explicitamente pendentes conforme o escopo.

## Publicação e encerramento
A rejeição inicial por falta de autorização explícita foi resolvida pelo usuário nesta conversa: **“Está autorizado!”**. A tentativa autorizada por Git não encontrou credencial de terminal; publicação concluída pelo conector GitHub, com igualdade exata das árvores locais/remotas.

|Registro|SHA / evidência|
|---|---|
|Código publicado|`78c54c07e2660974dcca3ffb4bdfbdf6474edc43`; árvore00cdc6e2870b3730073dd888be34a328a28363c8 idêntica ao código local fb5e3e382db973a989fb499a07a62404d83d80eb|
|Checkpoint publicado e validado no CI|`7c5547af06e6b569f493473ceb61cd6d224603da`; árvore5fd07e89d09e3e449b577d8906b44ae25bea31c4 idêntica ao local a5c6974acc533e4b687702c23023381b16bd4842|
|API / F00|[39662901530](https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39662901530):completed/success;604 testes,1 aviso,11,85s;34 golden,fixture intacta|
|AIOX|[39662901277](https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39662901277):completed/success;lint,typecheck,18 testes e build|
|Chromium|[39662901273](https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39662901273):completed/success;25 cenários,44,49s|

Os três runs e seus jobs/logs foram conferidos no mesmo head_sha. Não houve falha de CI nem correção adicional de código. Avisos de depreciação de Starlette/httpx e ações Node não impediram os gates.
O commit de encerramento posterior altera somente documentação e estado; o código permanece exatamente o validado pelo CI. Branch local alinhada ao remoto sem perda dos commits locais, preservados também na ref checkpoint/f05-local-before-publication. run-artifacts não integra os commits.

**Próximo arquivo: F06_EXECUTAR.md.** A fase F06 não foi executada nesta entrega. Sem merge em main, deploy, alteração de banco real ou aprovação normativa; permanecem os limites técnicos descritos no contrato.
