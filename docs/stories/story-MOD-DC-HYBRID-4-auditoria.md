# Story: MOD-DC-HYBRID-4 - Auditoria e Exportacao: Rastreabilidade Completa

**Epic:** MOD-DC Hybrid - Parametros por Circuito  
**Phase:** 4 de 4  
**Status:** **InReview**  
**Owner:** @dev (Backend + Frontend de apoio)  
**Esforco Estimado:** 1-2 dias  
**Dependencia:** `story-MOD-DC-HYBRID-3-ui-ux.md` concluida

---

## Objetivo

Fechar a funcionalidade com trilha de auditoria consultavel e exportacoes que mostrem claramente quando um circuito foi calculado com parametros globais ou customizados.

---

## Acceptance Criteria

- [x] **AC1: Historico por circuito**
  - O sistema expoe historico de customizacoes por circuito com acao, data/hora, usuario e mudancas relevantes.
  - O historico ordena do mais recente para o mais antigo.
  - O frontend consegue consumir esse historico.

- [x] **AC2: Sumario de auditoria do projeto**
  - Existe visao agregada com total de circuitos, quantidade customizada e principais desvios.
  - O payload identifica claramente `GLOBAL` x `CUSTOMIZADO`.

- [x] **AC3: Exportacao com fonte de calculo**
  - PDF e/ou Excel do dimensionador exibem coluna ou secao `Fonte de Calculo`.
  - Circuitos customizados ficam identificados visualmente.
  - A justificativa do override aparece no relatorio quando aplicavel.

- [x] **AC4: Secao de desvios**
  - O relatorio inclui secao com parametro alterado, valor global, valor usado e justificativa.
  - A secao deriva dos `parametrosUsados` e nao de heuristica de UI.

- [x] **AC5: Conformidade**
  - O relatorio informa quantos circuitos usaram customizacao individual.
  - O texto de conformidade referencia a existencia de desvios justificados.

- [x] **AC6: Testes**
  - Testes cobrem historico, payload agregado e exportacao com `Fonte de Calculo`.

---

## Fora de Escopo

- Novo motor de relatorio fora do padrao atual do projeto.
- Workflow de assinatura digital alem do que o projeto ja suportar.

---

## Dependencias Tecnicas

- Story 2 com persistencia operacional pronta
- Story 3 com fluxo de customizacao em uso
- Infraestrutura atual de relatorios/exportacao do projeto

---

## Tarefas Tecnicas

- [x] Expor consulta de historico por circuito e resumo do projeto.
- [x] Integrar historico na UI onde fizer sentido.
- [x] Ajustar exportacao para exibir `Fonte de Calculo` e justificativas.
- [x] Adicionar secao de desvios no relatorio.
- [x] Cobrir com testes de regressao e exportacao.
- [x] Atualizar File List e Change Log ao final.

---

## Definition of Done

- [x] Historico consultavel e coerente com as alteracoes feitas.
- [x] Relatorio identifica claramente circuitos customizados.
- [x] Exportacao reflete os parametros realmente usados no calculo.
- [x] Story movida para `InReview`.

---

## Referencias

- `docs/roadmap/ROADMAP-dimensionador-hybrid.md`
- `docs/stories/EPIC-MOD-DC-HYBRID.md`
- `docs/stories/story-MOD-DC-HYBRID-3-ui-ux.md`

---

## Notas para Desenvolvimento

- O historico por circuito e derivado de `repoAud`, sem depender de snapshot de UI.
- O sumario de auditoria e a exportacao usam `parametrosUsados` como fonte canonica.
- Foi adicionada exportacao CSV compativel com Excel e exportacao JSON da auditoria do dimensionador.
- A secao de conformidade informa explicitamente a quantidade de circuitos customizados.

---

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- `npm run typecheck` - PASS.
- `npx vitest run src/components/app/dimensionamento-condutores/auditoria-dimensionamento-condutores.test.ts tests/api/dimensionamento-condutores-flow.test.ts tests/ui/dimensionamento-condutores.vrt.test.tsx` - PASS.
- `npm run build` - PASS.

### Completion Notes List

- Implementado historico por circuito no servico de dimensionamento com ordenacao reversa e diff relevante.
- A UI passou a exibir o historico no modal do circuito.
- Criado payload de auditoria com resumo, desvios, justificativa e `Fonte de Calculo`.
- Disponibilizada exportacao JSON e CSV (Excel) para o dimensionador.

### File List

- `sistema-de-instala-es-el-tricas-sie-main/src/domain/servicos/servico-dimensionamento-condutores.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/lib/api-client.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/hooks/queries.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/dimensionamento-condutores/auditoria-dimensionamento-condutores.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/dimensionamento-condutores/DimensionamentoCondutoresResumo.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/tests/api/dimensionamento-condutores-flow.test.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/dimensionamento-condutores/auditoria-dimensionamento-condutores.test.ts`

### Change Log

| Date       | Version | Description                                                                                             | Author |
| ---------- | ------- | ------------------------------------------------------------------------------------------------------- | ------ |
| 2026-07-17 | 1.0.0   | Story criada como fase final de auditoria e exportacao.                                                 | @pm    |
| 2026-07-18 | 1.1.0   | Historico, sumario de auditoria e exportacao do dimensionador implementados; Status: Ready -> InReview. | @dev   |

---

**Atualizado por:** Morgan (PM) / @dev  
**Data:** 2026-07-18
