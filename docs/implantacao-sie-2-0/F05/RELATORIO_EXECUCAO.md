# F05 — Topologia elétrica e condições de instalação
Data:21/10/2026. **ESTADO: HUMAN_REQUIRED — publicação bloqueada**. Implementação, regressão e QA3 locais aprovados. Falta autorização explícita para publicação da F05 e posterior conferência do CI.
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
Ainda não conferido: CI do commit publicado F05. Não declarar passagem enquanto essa conferência estiver pendente.
Sem cálculo normativo novo, aprovação ABNT, geometria inventada, curto-circuito definitivo, paralelismo de fontes, migração real, merge ou deploy. Cadastro completo de entidades e metadados ocorre por JSON técnico validado; não é editor gráfico de desenho. Regras normativas futuras permanecem explicitamente pendentes conforme o escopo.

## Checkpoint de publicação
Commit local de código e validação:`fb5e3e382db973a989fb499a07a62404d83d80eb`,24 arquivos. Parent/base:`f388dde204fd4e9870796ff6cdcf77f9606aebe8`.
A revisão automática de aprovação rejeitou `git push` da branch F05: considerou que o pedido de executar a fase não autorizava explicitamente a publicação deste conteúdo no destino. A autorização anterior de F04 cobre outro payload/fase. Nenhuma tentativa por conector foi feita após a rejeição. Branch F05 remota não existe; CI F05 NÃO EXECUTADO. Não há commit F05 publicado nem link de CI a anunciar.
Condição de desbloqueio: autorização explícita do usuário para publicar os commits F05 em SFPTechnology/Projeto-SIE-2.0, somente branch feat/f05-topologia-eletrica, e executar/conferir CI. O trabalho local já está concreto e revisável. Não é necessário repetir implementação nem aceites F01–F04. Somente após publicação/CI e fechamento do estado poderá ser declarada passagem.
