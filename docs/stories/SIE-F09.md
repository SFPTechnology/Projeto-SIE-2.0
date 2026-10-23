# Story SIE-F09 — Concessionárias e aplicações especializadas

**Estado:** DONE (integração essencial implementada; CI remoto aprovado)
**Branch:** `feat/f09-concessionarias-especializadas`
**Objetivo:** produzir diagnóstico consultivo por distribuidora, vinculado a evidências correntes do projeto, sem aprovar conexão ou conformidade.

## Decisões do responsável

- Itens 1 e 2 previamente apontados pelo executor foram aceitos pelo responsável; não reabrir sua validação nesta execução.
- As extensões SPDA, FV/outras fontes, VE e ambientes especiais do item 3 foram excluídas e não são gate de F09.
- Preservar `main`; sem merge, deploy ou alteração de banco real.

## Critérios de aceite

- [x] Catálogo candidato EDP mantém identificador, edição, escopo e fonte; não há herança para outra distribuidora.
- [x] Diagnóstico consultivo preserva bloqueios e nunca significa aprovação da concessionária.
- [x] Enquadramento local usa corrente e potência instalada derivadas de cenário de entrada F06 persistido.
- [x] Exige último F07 e F08 atuais e compara resultados/hash com seus registros de origem.
- [x] Grava proveniência de projeto, revisão, fonte, entradas e resultados F06–F08.
- [x] Evidências alteradas, ausentes, incompatíveis ou revisão concorrente bloqueiam ou tornam resultado obsoleto.
- [x] Extensões do item 3 não implementadas por decisão do responsável; não bloqueiam o núcleo F09.
- [x] QA local, API e AIOX gates executados; pareceres registrados.
- [x] CI remoto do commit `59ba39c3ba1f9875c7092300cc6b8045bb3bc7e6` concluído: API, Chromium e AIOX PASS.

## Implementação desta retomada

- `restructuring/apps/api/sie_api/distributor_persistence_f09.py`: leitura validada das histórias F06–F08, derivação dos valores, hashes e invalidação.
- `restructuring/apps/api/sie_api/distributor_api_f09.py`: rotas locais autenticadas para criar e consultar histórico de enquadramentos.
- `restructuring/apps/api/tests/test_distributor_persistence_f09.py`: casos de integração, ausência, incompatibilidade, revisão, autorização e obsolescência.

## Testes

- 6 testes focados de integração F09: PASS.
- Suíte API: 1033 passed.
- `npm run lint`, `npm run typecheck`, `npm test` (18) e `npm run build`: PASS.
- CI remoto: API run 39880107120, Chromium run 39880107058 e AIOX run 39880107092: PASS.

## Limites

As flags `normative_conformity_verified`, `utility_approval` e `connection_release` permanecem falsas. O aceite dos itens 1 e 2 é decisão do responsável, não assinatura profissional independente. A API não prova a situação física da instalação nem aprovação de conexão.
