# Story: MOD-DC-HYBRID-1 - Backend Foundation: Parametros por Circuito

**Epic:** MOD-DC v3.0 - Dimensionador Hybrid (Toggle por Circuito)  
**Phase:** 1 de 4  
**Status:** **InReview**  
**Owner:** @dev (Backend)  
**Esforco Estimado:** 3-4 dias  

---

## Objetivo

Estruturar a base de dominio/API para suportar customizacao individual de parametros normativos por circuito, mantendo compatibilidade com o fluxo global existente.

Esta story implementa a fundacao CLI/backend-first do modelo Hybrid. Persistencia auditavel, historico visual, CRUD completo e UI ficam nas stories seguintes.

---

## Acceptance Criteria

- [x] **AC1: Contrato de override por circuito**
  - Existe `CircuitoOverride` com `useGlobal`, `customParams`, `justificativa` e campos opcionais de historico.
  - Existe um mapa `Record<circuitoId, CircuitoOverride>` aceito pelos contratos de dimensionamento.

- [x] **AC2: Merge deterministico global + override**
  - Circuito sem override usa exatamente os parametros globais.
  - Circuito com `useGlobal: true` ignora `customParams`.
  - Circuito com `useGlobal: false` mescla `parametrosGlobais + customParams`.

- [x] **AC3: Rastreabilidade no resultado**
  - Cada resultado de circuito inclui `baseadoEm: "GLOBAL" | "CUSTOMIZADO"`.
  - Cada resultado inclui `parametrosUsados`.
  - Resultado customizado preserva `justificativaOverride`.

- [x] **AC4: Validacao backend**
  - Override customizado sem justificativa e rejeitado.
  - Override customizado sem nenhum parametro e rejeitado.
  - Override customizado que viola validacoes obrigatorias existentes do MOD-DC e rejeitado.

- [x] **AC5: Integracao no servico existente**
  - `dimensionarLoteDireto`, `dimensionarLoteProjeto` e `dimensionarCircuitoProjeto` aceitam `circuitoOverrides` sem quebrar chamadas atuais.
  - Schemas Zod de dimensionamento aceitam `circuitoOverrides`.
  - Cliente interno `api.dimensionarCondutoresLote` aceita `circuitoOverrides` opcional.

- [x] **AC6: Testes**
  - Testes unitarios cobrem merge, origem GLOBAL/CUSTOMIZADO, justificativa obrigatoria e rejeicao por validacao normativa.

---

## Fora de Escopo Nesta Story

- CRUD persistente de overrides.
- Historico/auditoria persistida.
- UI de toggle/modal.
- Exportacao PDF/Excel com flagging.
- Persistencia no agregado de projeto.

---

## Dependencias

- MOD-DC existente em `sistema-de-instala-es-el-tricas-sie-main/src/domain/dimensionamento-condutores`.
- Servico de aplicacao `src/domain/servicos/servico-dimensionamento-condutores.ts`.
- Schemas existentes em `src/api/schemas/dimensionamento-condutores.ts`.

---

## Tarefas Tecnicas

- [x] Criar tipos `CircuitoOverride` e resultado com `parametrosUsados`.
- [x] Criar funcao pura para resolver parametros por circuito.
- [x] Criar funcao de lote com overrides.
- [x] Integrar overrides no servico de aplicacao.
- [x] Integrar overrides nos schemas Zod e cliente interno.
- [x] Adicionar testes unitarios.
- [x] Rodar verificacoes focadas e gates possiveis.
- [x] Atualizar File List, Change Log e status da story.

---

## Definition of Done

- [x] Typecheck limpo.
- [x] Testes focados passam.
- [x] `npm test` passa ou falhas pre-existentes sao documentadas.
- [x] File List atualizada.
- [x] Change Log atualizado.
- [x] Story pronta para QA.

---

## Referencias

- `docs/roadmap/ROADMAP-dimensionador-hybrid.md`
- `docs/stories/EPIC-MOD-DC-HYBRID.md`
- `docs/stories/HANDOFF-MOD-DC-HYBRID-to-DEV.md`
- `docs/stories/story-AUTO-OTI-1.2.md` - tech debt: cache de otimizacao nao invalida ao mudar parametros.

---

## Dev Agent Record

### Agent Model Used

GPT-5 Codex

### Debug Log References

- SDC Phase 1/2: story revisada a partir do estado Draft, com DoD anterior corrigida porque estava marcada como concluida sem evidencias.
- Teste focado: `npx vitest run tests/domain/dimensionamento-condutores/mod-dc.test.ts` - 18/18 PASS.
- Lint focado: `npx eslint ...arquivos-da-story...` - PASS.
- Typecheck: `npm run typecheck` - PASS.
- Testes dominio/API ampliados: `npx vitest run tests/domain/dimensionamento-condutores tests/api/dimensionamento-condutores-flow.test.ts` - 73/73 PASS.
- Suite completa: `npm test` - 709/709 PASS.
- Build: `npm run build` - PASS.
- Lint completo: `npm run lint` executado, mas excedeu timeout de 5 minutos sem diagnostico emitido; lint focado nos arquivos da story passou.

### Completion Notes List

- Implementado contrato `CircuitoOverride` e resultado rastreavel com `baseadoEm`, `parametrosUsados` e `justificativaOverride`.
- Adicionada funcao pura `dimensionarLoteComOverrides` para calcular circuitos com parametros globais ou customizados por circuito.
- Integrado `circuitoOverrides` nos schemas Zod, rotas existentes de dimensionamento e cliente interno.
- CRUD persistente, historico/auditoria e UI permanecem fora do escopo desta story e devem seguir nas stories 2-4.

### File List

- `docs/stories/story-MOD-DC-HYBRID-1-backend.md`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/dimensionamento-condutores/contratos.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/dimensionamento-condutores/overrides.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/dimensionamento-condutores/index.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/servicos/servico-dimensionamento-condutores.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/api/schemas/dimensionamento-condutores.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/routes/api/v1/projetos.$projetoId.dimensionamento-condutores.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/routes/api/v1/projetos.$projetoId.dimensionamento-condutores.lote.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/lib/api-client.ts`
- `sistema-de-instala-es-el-tricas-sie-main/tests/domain/dimensionamento-condutores/mod-dc.test.ts`

### Change Log

| Date | Version | Description | Author |
| --- | --- | --- | --- |
| 2026-07-17 | 1.0.0 | Story refinada e validada para escopo backend foundation; Status: Draft -> Ready -> InProgress. | @aiox-master/@dev |
| 2026-07-17 | 1.1.0 | Backend foundation implementado e validado; Status: InProgress -> InReview. | @dev |
