# Workflow - Corrigir AGUARDANDO-SECCIONAMENTO com retorno MOD-SEC

**Produto:** SIE - Sistema de Instalacoes Eletricas  
**Modulo:** MOD-DC / MOD-SEC  
**Modo:** Dev YOLO documentado, com gate de story e sem inventar dados eletricos  
**Criado por:** Dex (@dev)  
**Data:** 2026-07-16  
**Status:** Draft operacional para execucao

---

## 1. Objetivo

Corrigir o fluxo que deixa C4 em `AGUARDANDO-SECCIONAMENTO` quando o retorno do modulo MOD-SEC ja pode ser obtido e anexado ao circuito.

O resultado esperado e que circuitos em esquemas TN/IT sejam dimensionados com `retorno_seccionamento` antes de chamar `dimensionarCircuito()`/`dimensionarLote()`.

Observacao obrigatoria: se `parametros.esquema_aterramento === "TT"`, C4 deve virar `NAO-APLICAVEL` e a pendencia `AGUARDANDO-SECCIONAMENTO` nao deve existir. A rota MOD-SEC ja possui esse bypass em `sistema-de-instala-es-el-tricas-sie-main/src/routes/api/v1/modulos.mod-sec.validar.ts:26`.

Campos obrigatorios do retorno MOD-SEC:

- `aprovado`
- `tempo_seccionamento_s`
- `fonte`

---

## 2. Entradas Obrigatorias

| Entrada | Caminho | Uso |
|---|---|---|
| Contrato MOD-SEC | `sistema-de-instala-es-el-tricas-sie-main/src/domain/dimensionamento-condutores/contratos.ts` | `RetornoMODSEC` e `CircuitoParaDimensionamento.retorno_seccionamento` |
| Rota MOD-SEC | `sistema-de-instala-es-el-tricas-sie-main/src/routes/api/v1/modulos.mod-sec.validar.ts` | Endpoint que valida, aplica regra TT, retorna e persiste retorno downstream |
| Servico MOD-DC projeto | `sistema-de-instala-es-el-tricas-sie-main/src/domain/servicos/servico-dimensionamento-condutores.ts` | Fluxo atual Correntes -> MOD-DC |
| Motor C4 | `sistema-de-instala-es-el-tricas-sie-main/src/domain/dimensionamento-condutores/servico-dimensionamento-condutores.ts` | `resolverC4Seccionamento()` decide `NAO-APLICAVEL`, `PENDENTE`, `APROVADO` ou `REPROVADO` |
| Teste de fluxo atual | `sistema-de-instala-es-el-tricas-sie-main/tests/api/dimensionamento-condutores-flow.test.ts` | Fluxo de lote atual |
| Testes MOD-SEC | `sistema-de-instala-es-el-tricas-sie-main/tests/api/modulos-mod-sec.test.ts` | Referencia de contrato, persistencia, TT e E2E isolado |
| Story associada | `docs/stories/` | Obrigatoria antes de editar codigo |
| Constitution | `.aiox-core/constitution.md` | Story-driven, no invention, quality gates |

---

## 3. Saidas Esperadas

| Saida | Conteudo |
|---|---|
| Orquestracao MOD-DC -> MOD-SEC | Fluxo de projeto obtem retorno MOD-SEC para esquemas TN/IT antes do dimensionamento |
| Circuito enriquecido | Cada circuito elegivel recebe `retorno_seccionamento: RetornoMODSEC` |
| Regra TT preservada | Em TT, MOD-SEC nao e chamado, nao persiste retorno e C4 fica `NAO-APLICAVEL` |
| Persistencia downstream | Retorno MOD-SEC de TN/IT continua registrado em `dependencia_retornos_downstream` |
| Teste de regressao atualizado | Fluxo completo deixa de esperar `AGUARDANDO-SECCIONAMENTO` quando retorno MOD-SEC existe, e nunca espera essa pendencia em TT |
| Story atualizada | Checkboxes, Dev Agent Record, File List e Change Log atualizados |

---

## 4. Regras de Execucao

1. Nao implementar codigo sem story valida em `docs/stories/`.
2. Nao inventar `tempo_atuacao_s`, `tempo_seccionamento_s` ou limites normativos.
3. A fonte dos dados de entrada do MOD-SEC deve ser codigo, contrato ou artefato existente.
4. A rota `modulos.mod-sec.validar.ts` continua sendo o contrato HTTP do MOD-SEC.
5. O motor puro `dimensionarCircuito()` nao deve fazer I/O; ele apenas consome `circuito.retorno_seccionamento` e `parametros.esquema_aterramento`.
6. Em TT, nao chamar MOD-SEC, nao gravar `retorno_seccionamento` e nao emitir `AGUARDANDO-SECCIONAMENTO`.
7. Em TN/IT, timeout/erro/ausencia de dados preserva degradacao graciosa: C4 permanece `PENDENTE` com `AGUARDANDO-SECCIONAMENTO`.

---

## 5. Diagnostico Inicial

Estado observado no codigo:

- `RetornoMODSEC` ja existe em `contratos.ts`.
- `CircuitoParaDimensionamento` ja aceita `retorno_seccionamento?: RetornoMODSEC | null`.
- A rota `POST /api/v1/modulos/mod-sec/validar` ja retorna e persiste `RetornoMODSEC` para esquemas nao-TT.
- A rota ja trata TT antes de chamar o cliente MOD-SEC e retorna `NAO-APLICAVEL` sem persistir.
- `modulos-mod-sec.test.ts` prova tres comportamentos importantes:
  - TN/IT com retorno resolve C4;
  - TT sem retorno marca C4 `NAO-APLICAVEL` sem pendencia;
  - TN-S sem retorno mantem `AGUARDANDO-SECCIONAMENTO`.
- O gap provavel esta na orquestracao do fluxo de projeto/lote: enriquecer circuitos com `retorno_seccionamento` quando aplicavel e garantir que TT nao gere pendencia.

---

## 6. Sequencia de Execucao

### Fase 0 - Gate de story

1. Localizar story relacionada a `AGUARDANDO-SECCIONAMENTO`, MOD-SEC ou fluxo MOD-DC:

```bash
rg -n "AGUARDANDO-SECCIONAMENTO|retorno_seccionamento|MOD-SEC|dimensionamento-condutores" docs/stories
```

2. Se nao houver story apropriada, solicitar @sm/@po para criar uma story antes de editar codigo.
3. Se houver story `Done` que nao cobre o bug atual, criar/usar story de correcao separada.

**Gate:** prosseguir somente com story pronta para desenvolvimento.

### Fase 1 - Mapear fonte dos parametros SEC

1. Procurar de onde devem vir:
   - `dependencia_id`
   - `esquema_aterramento`
   - `tempo_atuacao_s`
   - `origem`

```bash
rg -n "tempo_atuacao_s|tempo_seccionamento_s|esquema_aterramento|dependencia_id|retorno_seccionamento" sistema-de-instala-es-el-tricas-sie-main/src sistema-de-instala-es-el-tricas-sie-main/tests
```

2. Confirmar se `tempo_atuacao_s` existe no projeto, dependencia, protecao, parametros ou outro retorno downstream.
3. Registrar a fonte no Dev Agent Record.

**BLOCK:** se `tempo_atuacao_s` nao existir em artefato atual. Nao criar default silencioso para producao.

### Fase 2 - Preservar a regra TT no orquestrador

1. Antes de qualquer chamada MOD-SEC, verificar `parametros.esquema_aterramento`.
2. Se for `TT`:
   - nao chamar MOD-SEC;
   - nao persistir registro `MOD-SEC`;
   - nao anexar `retorno_seccionamento`;
   - deixar `dimensionarCircuito()` resolver C4 como `NAO-APLICAVEL`.
3. Adicionar teste que falha se `AGUARDANDO-SECCIONAMENTO` aparecer em TT no fluxo completo.

**Criterio:** TT nao passa pela rota/cliente MOD-SEC e nao gera pendencia.

### Fase 3 - Extrair cliente/orquestrador MOD-SEC reutilizavel

1. Manter a rota como contrato HTTP.
2. Evitar acoplar servico de dominio puro a `Route`.
3. Se necessario, extrair a chamada MOD-SEC para um servico compartilhado, por exemplo:
   - cliente que recebe request MOD-SEC;
   - aplica a mesma regra TT;
   - valida `RetornoMODSECSchema`;
   - registra em `retornosDownstream` para TN/IT;
   - retorna `RetornoMODSEC | null` com motivo de pendencia em falhas esperadas.
4. Reusar a mesma validacao de schema ja usada pela rota.

**Criterio:** a rota e o fluxo de projeto usam a mesma semantica de contrato, bypass TT, timeout e persistencia.

### Fase 4 - Enriquecer circuitos antes do dimensionamento

1. No fluxo de projeto/lote, antes de `dimensionarLote(circuitos, parametros)`, obter o retorno MOD-SEC para cada circuito elegivel em TN/IT.
2. Anexar o retorno assim:

```typescript
const circuitoComSec = {
  ...circuito,
  retorno_seccionamento: retornoMODSEC,
};
```

3. Preservar ordem e IDs dos circuitos.
4. Em timeout/erro/ausencia de dados em TN/IT, manter o circuito sem `retorno_seccionamento`, permitindo que C4 continue `PENDENTE`.
5. Em TT, manter o circuito sem `retorno_seccionamento`, porque o proprio motor deve retornar `NAO-APLICAVEL`.

**Criterio:** quando MOD-SEC retorna sucesso, `resultado.criterios.C4` nao fica `PENDENTE` por ausencia de `retorno_seccionamento`.

### Fase 5 - Atualizar testes

1. Adicionar teste de unidade/servico para o enriquecimento:
   - TN-S com retorno MOD-SEC aprovado;
   - TN-S com retorno MOD-SEC reprovado;
   - TN-S com timeout/erro mantendo `AGUARDANDO-SECCIONAMENTO`;
   - TT sem chamada MOD-SEC e sem `AGUARDANDO-SECCIONAMENTO`.
2. Atualizar `dimensionamento-condutores-flow.test.ts` ou criar teste novo para fluxo completo:
   - preparar projeto/dependencia;
   - executar dimensionamento de lote com `esquema_aterramento: "TN-S"`;
   - verificar que C4 usa `retorno_seccionamento` quando dados SEC existem;
   - executar dimensionamento com `esquema_aterramento: "TT"`;
   - verificar `criterios.C4 === "NAO-APLICAVEL"` e ausencia de `AGUARDANDO-SECCIONAMENTO`.
3. Manter teste explicito para o comportamento parcial:
   - TN/IT sem dados SEC ou falha MOD-SEC => `AGUARDANDO-SECCIONAMENTO` permanece.

**Criterio:** os testes provam o caminho real, incluindo o bypass TT.

### Fase 6 - Validacoes

Executar a partir de `sistema-de-instala-es-el-tricas-sie-main`:

```bash
npm run lint
npm run typecheck
npm test
```

Executar tambem testes direcionados:

```bash
npx vitest run tests/api/modulos-mod-sec.test.ts
npx vitest run tests/api/dimensionamento-condutores-flow.test.ts
```

### Fase 7 - Atualizar story

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

- [ ] O fluxo de projeto/lote obtem retorno MOD-SEC antes de dimensionar em TN/IT.
- [ ] O circuito recebe `retorno_seccionamento` com os campos obrigatorios.
- [ ] `RetornoMODSECSchema` valida o retorno antes do uso.
- [ ] `dimensionarCircuito()` continua puro e sem I/O.
- [ ] Sucesso MOD-SEC resolve C4 como `APROVADO` ou `REPROVADO`.
- [ ] Timeout/erro/sem dados em TN/IT preserva `AGUARDANDO-SECCIONAMENTO`.
- [ ] TT resolve C4 como `NAO-APLICAVEL`.
- [ ] TT nao chama MOD-SEC, nao persiste retorno MOD-SEC e nao emite `AGUARDANDO-SECCIONAMENTO`.
- [ ] Persistencia em `dependencia_retornos_downstream` continua coberta para TN/IT.
- [ ] `npm run lint`, `npm run typecheck` e `npm test` passam.

---

## 8. Comandos de Execucao Recomendados

```bash
@aiox-dev *develop-yolo <story-id>
```

Ou, se a story ainda precisar ser criada:

```bash
@aiox-sm criar story de correcao para AGUARDANDO-SECCIONAMENTO integrando MOD-DC ao retorno MOD-SEC e preservando TT como NAO-APLICAVEL
@aiox-dev *develop-yolo <story-id>
```

---

## 9. Gates de Bloqueio

### PASS

O workflow passa quando C4 deixa de ficar `AGUARDANDO-SECCIONAMENTO` no fluxo completo sempre que MOD-SEC retornar contrato valido em TN/IT, TT nunca produzir essa pendencia, e todos os testes/quality gates passarem.

### BLOCK

Bloquear e reportar se:

- nao existir story valida para a correcao;
- nao houver fonte confiavel para `tempo_atuacao_s`;
- a correcao exigir decisao arquitetural nova fora do escopo de @dev;
- TT ainda chamar MOD-SEC ou persistir retorno MOD-SEC;
- os testes de regressao falharem;
- a solucao exigir inventar valores eletricos ou defaults normativos.

