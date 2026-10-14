# Checkpoint P5 — local_quality (cycle 0)

- Run ID: `sdc-yolo-dep-ux-01-2026-08-03T01-34-05-127-03-00`
- Manifest fingerprint: `a96a39eb597981b8c1e5dd6213c21b991dacf4f468e39d02c53852d05e9c9c63`
- Responsável: `@dev`
- Resultado: `FAIL — remediação P4 requerida`

## Resultados

- Contrato de ações: `PASS`.
  - `Detalhe`, `Calcular`, `Historico` e `Duplicar` permanecem visíveis no rodapé de cada card.
  - Handlers preservados: `setDetalhe(item.dep)`, `calcular.mutate(item.dep.id)`, `setHist(item.dep.id)` e `duplicar.mutate(item.dep)`.
- Typecheck: `PASS`.
  - `npx tsc --noEmit` — exit 0, 96,4 s.
- Teste focado: `FAIL`.
  - `npx vitest run src/components/app/__tests__/dependencias-table-view-model.test.ts src/components/app/__tests__/status-badge.test.tsx`
  - 6/7 testes passaram; um teste ainda espera o texto legado `Tabela de dependências`.
  - A regressão é exclusivamente da expectativa de teste após a migração tabela → cards; a renderização inclui as quatro ações protegidas.
- Lint focado: `BLOCKED`.
  - O comando de ESLint não produziu saída em aproximadamente 42 s e foi interrompido; não deve ser contado como PASS ou FAIL.

## Ação automática

Retornar à P4 para atualizar exclusivamente a asserção legada e cobrir a superfície de card com as quatro ações. Depois, repetir o teste focado e a revisão P5.

## Cycle 1 — resultado após remediação

- Resultado: `PASS`.
- Teste focado: `npx vitest run src/components/app/__tests__/dependencias-table-view-model.test.ts src/components/app/__tests__/status-badge.test.tsx`.
- Evidência: exit 0; 2 arquivos e 7 testes passaram; wall time 40,7 s.
- Contrato de ações reconfirmado no código:
  - `Detalhe` → `setDetalhe(item.dep)`.
  - `Calcular` → `calcular.mutate(item.dep.id)`.
  - `Historico` → `setHist(item.dep.id)`.
  - `Duplicar` → `duplicar.mutate(item.dep)`.
- Advisory não bloqueante: `vite-tsconfig-paths` passou a ser nativo do Vite.
- Próximo estado: `qa_review`.

## Cycle 3 — resultado após acessibilidade e formatação

- Resultado: `PASS`.
- ESLint focado: exit 0 em 25,5 s para `TabelaDependencias.tsx` e os dois testes de Dependências.
- Vitest focado: exit 0; 2 arquivos e 7 testes passaram; wall time 47,3 s.
- A busca mantém `labelText="Buscar dependências"` com rótulo oculto visualmente.
- Bindings protegidos reconfirmados:
  - `Detalhe` → `setDetalhe(item.dep)`;
  - `Calcular` → `calcular.mutate(item.dep.id)`;
  - `Historico` → `setHist(item.dep.id)`;
  - `Duplicar` → `duplicar.mutate(item.dep)`.
- Advisory não bloqueante: aviso de depreciação de `vite-tsconfig-paths`.
- Próximo estado: `qa_review` (cycle 1).
