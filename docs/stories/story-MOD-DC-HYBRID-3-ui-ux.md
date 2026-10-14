# Story: MOD-DC-HYBRID-3 - UI + UX de Customizacao por Circuito

**Epic:** MOD-DC Hybrid - Parametros por Circuito  
**Phase:** 3 de 4  
**Status:** **InReview**  
**Owner:** @dev (Frontend + Backend)  
**Esforco Estimado:** 2-3 dias  
**Dependencia:** `story-MOD-DC-HYBRID-2-backend-operacoes.md` concluida

---

## Objetivo

Disponibilizar a customizacao por circuito na tela de dimensionamento, usando os fluxos persistentes entregues na story 2. O usuario deve conseguir alternar entre global e customizado, editar os parametros permitidos, justificar a excecao e recalcular apenas o circuito desejado.

---

## Acceptance Criteria

- [x] **AC1: Indicadores por circuito**
  - A tabela exibe controle por circuito para `Usar global` x `Customizar`.
  - A tabela exibe badge `GLOBAL` ou `CUSTOMIZADO`.
  - Circuito customizado fica visualmente distinguivel sem quebrar o layout atual.

- [x] **AC2: Modal ou drawer de customizacao**
  - O usuario consegue abrir uma superficie de edicao para um circuito especifico.
  - Os campos carregam valores globais e, se existir, override persistido.
  - O usuario pode salvar, recalcular o circuito ou descartar mudancas locais.

- [x] **AC3: Justificativa obrigatoria**
  - Customizacao exige justificativa nao vazia antes de salvar.
  - O texto de erro e claro e impede envio invalido.
  - Voltar para global nao exige justificativa adicional.

- [x] **AC4: Diff e feedback de validacao**
  - Cada campo alterado mostra diferenca vs. valor global.
  - O usuario recebe aviso quando nao houver mudanca real.
  - Erros normativos retornados pelo backend aparecem no contexto do formulario.

- [x] **AC5: Recalculo individual e limpeza**
  - O usuario consegue recalcular apenas o circuito aberto no modal.
  - Existe acao para reverter o circuito atual para os parametros globais.
  - Existe acao global para limpar customizacoes, com confirmacao.

- [x] **AC6: Consistencia de resultados**
  - A UI atualiza `baseadoEm`, status do circuito e demais resultados afetados sem reload manual.
  - O lote continua refletindo overrides ativos quando o usuario executar dimensionamento global.

- [x] **AC7: Testes**
  - Testes cobrem abrir modal, salvar override valido, bloquear override invalido, recalcular circuito e reverter para global.

---

## Fora de Escopo

- Historico visual detalhado.
- Exportacao PDF/Excel.
- Secao final de compliance no relatorio.

---

## Dependencias Tecnicas

- Estado global atual da rota de dimensionamento
- Cliente interno/API com persistencia operacional pronta
- Componentes e padroes existentes da tela de dimensionamento

---

## Tarefas Tecnicas

- [x] Criar controle visual por circuito.
- [x] Criar modal/drawer de edicao.
- [x] Integrar leitura, salvar, recalcular e reset via API.
- [x] Implementar validacao de formulario e diff visual.
- [x] Implementar acao global de limpeza de customizacoes.
- [x] Adicionar testes de interacao e regressao.
- [x] Atualizar File List e Change Log ao final.

---

## Definition of Done

- [x] Fluxo de customizacao funciona ponta a ponta na UI.
- [x] Validacoes impedem salvar estado invalido.
- [x] Recalculo individual atualiza a tela corretamente.
- [x] Responsividade e acessibilidade basica preservadas.
- [x] Story movida para `InReview`.

---

## Referencias

- `docs/roadmap/ROADMAP-dimensionador-hybrid.md`
- `docs/stories/EPIC-MOD-DC-HYBRID.md`
- `docs/stories/story-MOD-DC-HYBRID-2-backend-operacoes.md`

---

## Notas para Desenvolvimento

- A rota de dimensionamento passou a carregar overrides persistidos antes da execucao do lote.
- A tabela exibe `GLOBAL` x `CUSTOMIZADO`, possui acao por circuito e destaca linhas customizadas.
- O modal de customizacao valida justificativa, diff real e permite salvar, recalcular ou reverter para global.
- O recalc por circuito atualiza o quadro sem exigir reload manual.

---

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- `npm run typecheck` - PASS.
- `npx vitest run src/components/app/dimensionamento-condutores/customizacao-circuito-model.test.ts src/components/app/dimensionamento-condutores/CustomizarCircuitoModal.test.tsx tests/ui/dimensionamento-condutores.vrt.test.tsx tests/api/dimensionamento-condutores-flow.test.ts` - PASS.
- `npm run build` - PASS.

### Completion Notes List

- Estado da rota adaptado para overrides persistidos e recalc parcial por circuito.
- Criado `CustomizarCircuitoModal` com diff, validacao local e contexto de erro do backend.
- A tabela passou a oferecer badge `GLOBAL/CUSTOMIZADO`, acao `Customizar` e retorno imediato a `Usar global`.
- Incluida acao global para limpar customizacoes com confirmacao.

### File List

- `sistema-de-instala-es-el-tricas-sie-main/src/routes/projetos.$projetoId_.dimensionamento-condutores.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/dimensionamento-condutores/DimensionamentoCondutoresResumo.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/dimensionamento-condutores/CustomizarCircuitoModal.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/dimensionamento-condutores/customizacao-circuito-model.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/hooks/queries.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/lib/api-client.ts`
- `sistema-de-instala-es-el-tricas-sie-main/tests/ui/dimensionamento-condutores.vrt.test.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/dimensionamento-condutores/customizacao-circuito-model.test.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/dimensionamento-condutores/CustomizarCircuitoModal.test.tsx`

### Change Log

| Date       | Version | Description                                                             | Author |
| ---------- | ------- | ----------------------------------------------------------------------- | ------ |
| 2026-07-17 | 1.0.0   | Story criada como fase de UI/UX apos backend operacional.               | @pm    |
| 2026-07-18 | 1.1.0   | Fluxo de customizacao por circuito implementado e movido para InReview. | @dev   |

---

**Atualizado por:** Morgan (PM) / @dev  
**Data:** 2026-07-18
