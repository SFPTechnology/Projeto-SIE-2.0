# Workflow - Corrigir AGUARDANDO-CC com retorno MOD-CC

**Produto:** SIE - Sistema de Instalacoes Eletricas  
**Modulo:** MOD-DC / MOD-CC  
**Modo:** Dev YOLO documentado, com gate de story e sem inventar dados eletricos  
**Criado por:** Dex (@dev)  
**Data:** 2026-07-16  
**Status:** Draft operacional para execucao

---

## 1. Objetivo

Corrigir o fluxo que deixa C3 em `AGUARDANDO-CC` quando o retorno do modulo de curto-circuito ja pode ser obtido via MOD-CC.

O resultado esperado e que o circuito seja dimensionado com `retorno_cc` anexado antes de chamar `dimensionarCircuito()`/`dimensionarLote()`, usando o contrato `RetornoMODCC`.

Campos obrigatorios do retorno:

- `icc_presumida_a`
- `tempo_atuacao_s`
- `integral_joule_dispositivo`
- `aprovado`
- `fonte`

---

## 2. Entradas Obrigatorias

| Entrada | Caminho | Uso |
|---|---|---|
| Contrato MOD-CC | `sistema-de-instala-es-el-tricas-sie-main/src/domain/dimensionamento-condutores/contratos.ts` | `RetornoMODCC` e `CircuitoParaDimensionamento.retorno_cc` |
| Rota MOD-CC | `sistema-de-instala-es-el-tricas-sie-main/src/routes/api/v1/modulos.mod-cc.validar.ts` | Endpoint que valida, retorna e persiste o retorno downstream |
| Servico MOD-DC projeto | `sistema-de-instala-es-el-tricas-sie-main/src/domain/servicos/servico-dimensionamento-condutores.ts` | Fluxo atual Correntes -> MOD-DC |
| Teste de fluxo atual | `sistema-de-instala-es-el-tricas-sie-main/tests/api/dimensionamento-condutores-flow.test.ts` | Hoje espera `AGUARDANDO-CC` no lote |
| Testes MOD-CC | `sistema-de-instala-es-el-tricas-sie-main/tests/api/modulos-mod-cc.test.ts` | Referencia de contrato, persistencia e E2E isolado |
| Story associada | `docs/stories/` | Obrigatoria antes de editar codigo |
| Constitution | `.aiox-core/constitution.md` | Story-driven, no invention, quality gates |

---

## 3. Saidas Esperadas

| Saida | Conteudo |
|---|---|
| Orquestracao MOD-DC -> MOD-CC | Fluxo de projeto obtem retorno MOD-CC antes do dimensionamento |
| Circuito enriquecido | Cada circuito elegivel recebe `retorno_cc: RetornoMODCC` |
| Persistencia downstream | Retorno MOD-CC continua registrado em `dependencia_retornos_downstream` |
| Teste de regressao atualizado | Fluxo de lote deixa de esperar `AGUARDANDO-CC` quando dados CC existem |
| Story atualizada | Checkboxes, Dev Agent Record, File List e Change Log atualizados |

---

## 4. Regras de Execucao

1. Nao implementar codigo sem story valida em `docs/stories/`.
2. Nao inventar valores para `icc_presumida_a`, `tempo_atuacao_s` ou `integral_joule_dispositivo`.
3. A fonte dos dados de entrada do MOD-CC deve ser codigo, contrato ou artefato existente.
4. Se a fonte dos parametros CC nao existir, bloquear a implementacao e registrar lacuna na story.
5. A rota `modulos.mod-cc.validar.ts` continua sendo o contrato HTTP do MOD-CC.
6. O motor puro `dimensionarCircuito()` nao deve fazer I/O; ele apenas consome `circuito.retorno_cc`.
7. Timeout/erro do MOD-CC preserva degradacao graciosa: C3 permanece `PENDENTE` com `AGUARDANDO-CC`.

---

## 5. Diagnostico Inicial

Estado observado no codigo:

- `RetornoMODCC` ja existe em `contratos.ts`.
- `CircuitoParaDimensionamento` ja aceita `retorno_cc?: RetornoMODCC | null`.
- A rota `POST /api/v1/modulos/mod-cc/validar` ja retorna e persiste `RetornoMODCC`.
- O teste `modulos-mod-cc.test.ts` prova que um retorno do endpoint resolve C3 quando anexado manualmente ao circuito.
- O fluxo de projeto em `servico-dimensionamento-condutores.ts` adapta Correntes para circuitos e chama `dimensionarLote(circuitos, parametros)` sem enriquecer os circuitos com `retorno_cc`.
- O teste `dimensionamento-condutores-flow.test.ts` ainda espera `AGUARDANDO-CC`.

Conclusao: o gap provavel esta na orquestracao do fluxo de projeto/lote, nao no contrato puro de dominio.

---

## 6. Sequencia de Execucao

### Fase 0 - Gate de story

1. Localizar story relacionada a `AGUARDANDO-CC`, MOD-CC ou fluxo MOD-DC:

```bash
rg -n "AGUARDANDO-CC|retorno_cc|MOD-CC|dimensionamento-condutores" docs/stories
```

2. Se nao houver story apropriada, solicitar @sm/@po para criar uma story antes de editar codigo.
3. Se houver story `Done` que nao cobre o bug atual, criar/usar story de correcao separada.

**Gate:** prosseguir somente com story pronta para desenvolvimento.

### Fase 1 - Mapear fonte dos parametros CC

1. Procurar de onde devem vir:
   - `dependencia_id`
   - `icc_presumida_a`
   - `tempo_atuacao_s`
   - `integral_joule_dispositivo`
   - `origem`

```bash
rg -n "icc_presumida_a|tempo_atuacao_s|integral_joule_dispositivo|dependencia_id|retorno_cc" sistema-de-instala-es-el-tricas-sie-main/src sistema-de-instala-es-el-tricas-sie-main/tests
```

2. Confirmar se esses dados existem no contrato de Correntes, dependencia, projeto, padrao de entrada ou parametros.
3. Registrar a fonte no Dev Agent Record.

**BLOCK:** se os parametros nao existirem em artefato atual. Nao criar formula, default ou mock silencioso para producao.

### Fase 2 - Extrair cliente/orquestrador MOD-CC reutilizavel

1. Manter a rota como contrato HTTP.
2. Evitar acoplar servico de dominio puro a `Route`.
3. Se necessario, extrair a chamada MOD-CC para um servico compartilhado, por exemplo:
   - cliente que recebe request MOD-CC;
   - valida `RetornoMODCCSchema`;
   - registra em `retornosDownstream`;
   - retorna `RetornoMODCC | null` com motivo de pendencia em falhas esperadas.
4. Reusar a mesma validacao de schema ja usada pela rota.

**Criterio:** a rota e o fluxo de projeto usam a mesma semantica de contrato, timeout e persistencia.

### Fase 3 - Enriquecer circuitos antes do dimensionamento

1. No fluxo de projeto/lote, antes de `dimensionarLote(circuitos, parametros)`, obter o retorno MOD-CC para cada circuito elegivel.
2. Anexar o retorno assim:

```typescript
const circuitoComCc = {
  ...circuito,
  retorno_cc: retornoMODCC,
};
```

3. Preservar ordem e IDs dos circuitos.
4. Em timeout/erro/ausencia de dados, manter o circuito sem `retorno_cc`, permitindo que C3 continue `PENDENTE`.

**Criterio:** quando MOD-CC retorna sucesso, `resultado.criterios.C3` nao fica `PENDENTE` por ausencia de `retorno_cc`.

### Fase 4 - Atualizar testes

1. Adicionar teste de unidade/servico para o enriquecimento:
   - com retorno MOD-CC aprovado;
   - com retorno MOD-CC reprovado;
   - com timeout/erro mantendo `AGUARDANDO-CC`.
2. Atualizar `dimensionamento-condutores-flow.test.ts` ou criar teste novo para fluxo completo:
   - preparar projeto/dependencia;
   - executar dimensionamento de lote;
   - verificar que C3 usa `retorno_cc` quando dados CC existem.
3. Manter teste explicito para o comportamento parcial:
   - sem dados CC ou falha MOD-CC => `AGUARDANDO-CC` permanece.

**Criterio:** os testes provam o caminho real, nao apenas literais montados manualmente.

### Fase 5 - Validacoes

Executar a partir de `sistema-de-instala-es-el-tricas-sie-main`:

```bash
npm run lint
npm run typecheck
npm test
```

Executar tambem testes direcionados:

```bash
npx vitest run tests/api/modulos-mod-cc.test.ts
npx vitest run tests/api/dimensionamento-condutores-flow.test.ts
```

### Fase 6 - Atualizar story

Atualizar somente secoes permitidas da story:

- Tasks/Subtasks checkboxes
- Dev Agent Record
- Debug Log References
- Completion Notes
- File List
- Change Log
- Status, se todos os gates passarem

---

## 7. Criterios de Aceite

- [ ] O fluxo de projeto/lote obtem retorno MOD-CC antes de dimensionar.
- [ ] O circuito recebe `retorno_cc` com os campos obrigatorios.
- [ ] `RetornoMODCCSchema` valida o retorno antes do uso.
- [ ] `dimensionarCircuito()` continua puro e sem I/O.
- [ ] Sucesso MOD-CC resolve C3 como `APROVADO` ou `REPROVADO`.
- [ ] Timeout/erro/sem dados preserva `AGUARDANDO-CC`.
- [ ] Persistencia em `dependencia_retornos_downstream` continua coberta.
- [ ] `npm run lint`, `npm run typecheck` e `npm test` passam.

---

## 8. Comandos de Execucao Recomendados

```bash
@aiox-dev *develop-yolo <story-id>
```

Ou, se a story ainda precisar ser criada:

```bash
@aiox-sm criar story de correcao para AGUARDANDO-CC integrando MOD-DC ao retorno MOD-CC
@aiox-dev *develop-yolo <story-id>
```

---

## 9. Gates de Bloqueio

### PASS

O workflow passa quando C3 deixa de ficar `AGUARDANDO-CC` no fluxo completo sempre que MOD-CC retornar contrato valido, e todos os testes/quality gates passarem.

### BLOCK

Bloquear e reportar se:

- nao existir story valida para a correcao;
- nao houver fonte confiavel para os parametros de entrada do MOD-CC;
- a correcao exigir decisao arquitetural nova fora do escopo de @dev;
- os testes de regressao falharem;
- a solucao exigir inventar valores eletricos ou defaults normativos.

