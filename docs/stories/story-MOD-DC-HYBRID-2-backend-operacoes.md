# Story: MOD-DC-HYBRID-2 - Backend Operations: Persistencia e Recalculo por Circuito

**Epic:** MOD-DC Hybrid - Parametros por Circuito  
**Phase:** 2 de 4  
**Status:** **InReview**  
**Owner:** @dev (Backend)  
**Esforco Estimado:** 2-3 dias  
**Dependencia:** `story-MOD-DC-HYBRID-1-backend.md` disponivel para continuidade

---

## Objetivo

Transformar a fundacao de overrides em uma capacidade operacional do sistema. Ao final desta story, o projeto deve conseguir salvar, carregar, remover e recalcular overrides por circuito sem depender da interface grafica.

Esta story existe para cumprir `CLI First`. A UI so deve consumir fluxos que ja funcionem via servico/API.

---

## Acceptance Criteria

- [x] **AC1: Persistencia de override por projeto/circuito**
  - O sistema persiste `useGlobal`, `customParams` e `justificativa` por `projetoId + circuitoId`.
  - O contrato persistido e compativel com `CircuitoOverride`.
  - Reabrir o contexto do projeto preserva os overrides salvos.

- [x] **AC2: Operacoes de salvar, remover e consultar**
  - Existe fluxo de aplicacao/API para salvar um override de circuito.
  - Existe fluxo de aplicacao/API para remover override e voltar ao comportamento global.
  - Existe fluxo de aplicacao/API para listar overrides ativos de um projeto.

- [x] **AC3: Recalculo individual por circuito**
  - O sistema recalcula apenas o circuito alvo usando o override persistido ou payload recebido.
  - O resultado recalculado informa `baseadoEm`, `parametrosUsados` e `justificativaOverride` quando aplicavel.
  - Recalculo individual nao altera outros circuitos do lote.

- [x] **AC4: Integracao com lote e projeto**
  - O carregamento do projeto aplica overrides salvos no dimensionamento em lote.
  - Circuito sem override continua usando os parametros globais.
  - Fluxos existentes de lote permanecem backward compatible.

- [x] **AC5: Integracao com AUTO-OTI**
  - Quando houver override ativo no circuito, a auto-otimizacao considera os parametros realmente aplicados naquele circuito.
  - O resultado de AUTO-OTI nao perde a rastreabilidade de origem dos parametros.

- [x] **AC6: Erros e validacoes**
  - Override invalido continua sendo rejeitado no backend.
  - Tentar salvar override vazio ou sem justificativa retorna erro claro.
  - Remover override retorna o circuito ao comportamento global sem residuos persistidos.

- [x] **AC7: Testes**
  - Testes cobrem persistencia, remocao, recalculo individual, leitura em lote e integracao com AUTO-OTI.

---

## Fora de Escopo

- Toggle/modal na UI.
- Diff visual e validacao em tempo real no frontend.
- Historico visual e exportacao PDF/Excel.

---

## Dependencias Tecnicas

- Contratos em `src/domain/dimensionamento-condutores/contratos.ts`
- Funcoes em `src/domain/dimensionamento-condutores/overrides.ts`
- Servico `src/domain/servicos/servico-dimensionamento-condutores.ts`
- Estrategia de persistencia ja usada pelo projeto para dados operacionais

---

## Tarefas Tecnicas

- [x] Definir repositorio/modelo de persistencia para override por circuito.
- [x] Implementar leitura/escrita/remocao no servico de aplicacao.
- [x] Expor operacoes em schemas/rotas/cliente interno.
- [x] Integrar recalculo individual com override persistido.
- [x] Ajustar AUTO-OTI para respeitar override ativo.
- [x] Adicionar testes de dominio, integracao e regressao.
- [x] Atualizar File List e Change Log ao final.

---

## Definition of Done

- [x] `npm run typecheck` passa.
- [x] Testes focados da story passam.
- [x] Fluxo sem UI funciona ponta a ponta.
- [x] Compatibilidade com dimensionamento global preservada.
- [x] Story movida para `InReview`.

---

## Referencias

- `docs/roadmap/ROADMAP-dimensionador-hybrid.md`
- `docs/stories/EPIC-MOD-DC-HYBRID.md`
- `docs/stories/story-MOD-DC-HYBRID-1-backend.md`

---

## Notas para Desenvolvimento

- Repositorio de overrides foi implementado como mapa por projeto, preservando o contrato `CircuitoOverride`.
- O lote do MOD-DC agora mescla overrides persistidos com overrides informados em runtime.
- A AUTO-OTI passou a usar os `parametrosUsados` do resultado quando existirem.

---

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- `npx vitest run tests/api/dimensionamento-condutores-flow.test.ts tests/domain/dimensionamento-condutores/mod-dc.test.ts` - 25/25 PASS.
- `npm run typecheck` - PASS.
- `npm run build` - PASS.

### Completion Notes List

- Implementado repositorio de persistencia para overrides de dimensionamento por projeto.
- Integrados servico, schemas, rotas e cliente interno para salvar, listar e remover overrides.
- O lote de dimensionamento carrega overrides persistidos automaticamente.
- AUTO-OTI agora respeita os parametros efetivos usados no circuito quando o resultado ja estiver customizado.
- Migration `0010_dimensionamento_condutores_overrides.sql` adicionada para Supabase.

### File List

- `sistema-de-instala-es-el-tricas-sie-main/src/infra/repositorios/repositorio-dimensionamento-condutores-overrides.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/infra/supabase/repo-dimensionamento-condutores-overrides.supabase.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/infra/contexto.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/estado/eventos.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/api/http.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/servicos/servico-dimensionamento-condutores.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/api/schemas/dimensionamento-condutores.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/routes/api/v1/projetos.$projetoId.dimensionamento-condutores.overrides.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/routes/api/v1/projetos.$projetoId.dimensionamento-condutores.overrides.$circuitoId.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/lib/api-client.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/dimensionamento-condutores/auto-otimizacao-retencao.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/dimensionamento-condutores/DimensionamentoCondutoresResumo.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/tests/api/dimensionamento-condutores-flow.test.ts`
- `sistema-de-instala-es-el-tricas-sie-main/docs/supabase/0010_dimensionamento_condutores_overrides.sql`

### Change Log

| Date | Version | Description | Author |
| --- | --- | --- | --- |
| 2026-07-17 | 1.0.0 | Story criada no backlog corrigido como fase operacional de backend. | @pm |
| 2026-07-17 | 1.1.0 | Persistencia, CRUD operacional, integracao com lote e ajuste AUTO-OTI implementados; Status: Ready -> InReview. | @dev |

---

**Atualizado por:** Morgan (PM) / @dev  
**Data:** 2026-07-17
