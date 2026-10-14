# Story AUTO-OTI-1.3 — Aplicar seção auto-otimizada do MOD-DC no MOD-QT

**Epic:** AUTO-OTI (Auto-otimização de Dimensionamento NBR 5410)  
**Status:** Ready  
**Prioridade:** P1  
**Tipo:** Brownfield fullstack — domínio, persistência, CLI/API, MOD-QT e UI  
**Criada em:** 2026-08-02  
**Predecessoras:** `AUTO-OTI-1.2` e `MOD-QT-2-06`  
**Fonte normativa:** `docs/PLANO-REESTRUTURACAO-AUTO-OTIMIZACAO-S-QUEDA-TENSAO.md`  
**Workflow:** `docs/workflows/WORKFLOW-SDC-AUTO-OTIMIZACAO-S-QUEDA-TENSAO-YOLO.md`

---

## Story

**Como** projetista que usa a Auto-otimização do MOD-DC e o MOD-QT,  
**quero** aplicar explicitamente, de forma individual ou em lote, as seções aprovadas por um caso de uso headless com persistência durável,  
**para que** `S (mm²)` seja preenchida no MOD-QT sem redigitação, sem perda concorrente e sem reutilizar valores voláteis, inválidos ou obsoletos.

## Contexto e rastreabilidade aos predecessores

- `AUTO-OTI-1.2` entregou o cálculo e a experiência de Auto-otimização, inclusive confirmação visual e retenção em React/`localStorage`, mas não grava a fonte durável consumida pelo MOD-QT. Esta story transforma a confirmação em aplicação real sem promover a retenção local.
- `MOD-QT-2-06` entregou persistência do dimensionamento base, leitura pelo MOD-QT e precedência do override manual. Sua implementação JSONB `SELECT → merge → UPSERT` e o fallback volátil revelaram riscos de concorrência e falso sucesso. Esta story é sucessora separada e não amplia retroativamente aquela story.
- A precedência existente no MOD-QT deve ser preservada sob autoridade de `servico-queda-tensao.ts`; o override manual auditado continua acima da seção automática vigente.
- A tentativa anteriormente revertida de inventar seção por parâmetros padrão não pode ser reintroduzida. Somente resultados reais, recalculados/validados pelo domínio, podem ser aplicados.

### Matriz de origem

| Requisito desta story | Origem |
|---|---|
| AC1–AC12 e NFRs | Plano v2, §§ 12–14; workflow, §§ 16–17 |
| Persistência atômica, idempotência e concorrência | Plano v2, §§ 7–8; diagnóstico de `MOD-QT-2-06` |
| Confirmação individual/lote e vocabulário de estado | Plano v2, §§ 4–5; legado de `AUTO-OTI-1.2` |
| Precedência e ausência `—`/`PEND` | Plano v2, § 5.4; predecessor `MOD-QT-2-06` |
| Contratos/fórmulas protegidos | Plano v2, AC12 e § 17; workflow, § 3 |

## Objetivo e vocabulário obrigatório

O mesmo caso de uso deve atender CLI/API e UI. A UI não é autoridade de cálculo, assinatura ou persistência. Os estados têm os significados abaixo:

| Termo | Significado |
|---|---|
| Calculado | O motor produziu resultado; ainda não é fonte vigente. |
| Aprovado | `status === "APROVADO"` e a seção final é finita e positiva. |
| Aplicado | Houve confirmação explícita individual ou do lote. |
| Persistido | O repositório confirmou gravação durável; não inclui fallback volátil. |
| Vigente | Persistido, não invalidado e compatível com a assinatura da última entrada aplicada. |
| Obsoleto | Registro histórico incompatível com a entrada aplicada ou com o ciclo de vida do circuito. |
| Manual MOD-QT | Override auditado em `config.secoes_aplicadas_mm2`, com precedência sobre o automático. |

## Acceptance Criteria

### AC1 — Operação headless individual

```gherkin
Given um circuito pertencente ao projeto e uma otimização aprovada
When a seção é aplicada por CLI/API sem navegador
Then o sistema persiste uma seção automática vigente com assinatura canônica
And retorna persistência DURAVEL
```

### AC2 — Aplicação individual pela UI

```gherkin
Given uma Auto-otimização aprovada
When o usuário confirma a seção
Then a UI chama o mesmo caso de uso headless
And somente exibe estado aplicado após persistência DURAVEL
And o MOD-QT exibe a seção sem redigitação
```

### AC3 — Aplicação em lote explícita

```gherkin
Given vários resultados calculados
When o usuário confirma explicitamente a aplicação do lote
Then somente resultados aprovados são enviados
And a operação persiste o lote atomicamente
And informa aplicados, ignorados, conflitos e falhas
```

### AC4 — Invalidação por nova assinatura

```gherkin
Given uma seção automática vigente
When uma nova entrada diferente é aplicada ao mesmo circuito
And não produz seção aprovada
Then a seção anterior torna-se obsoleta
And o MOD-QT não a utiliza como vigente
```

### AC5 — Falha transitória com mesma assinatura

```gherkin
Given uma seção vigente com a mesma assinatura da tentativa atual
When a tentativa falha por erro transitório sem aplicar nova entrada
Then a seção vigente é preservada
And a falha é registrada sem criar novo valor
```

### AC6 — Concorrência entre circuitos

```gherkin
Given duas sessões atualizando circuitos diferentes do mesmo projeto
When as operações são executadas concorrentemente
Then ambas as seções permanecem persistidas
And nenhuma chave é perdida
```

### AC7 — Concorrência no mesmo circuito

```gherkin
Given duas sessões atualizando o mesmo circuito
When as versões esperadas divergem
Then o sistema detecta conflito ou aplica uma ordem explicitamente definida
And não confirma silenciosamente ambos os resultados
```

### AC8 — Precedência e remoção manual

```gherkin
Given uma seção automática vigente e um override manual auditado no MOD-QT
When o lote é calculado
Then o override manual prevalece
When o override manual é removido
Then a seção automática vigente reaparece
```

### AC9 — Persistência indisponível

```gherkin
Given a migration ausente ou o banco indisponível
When o usuário tenta aplicar uma seção
Then a UI não apresenta o resultado como persistido
And a saída diferencia VOLATIL de FALHOU
And nova sessão não assume que o valor é vigente
```

### AC10 — Ciclo de vida do circuito

```gherkin
Given uma seção persistida
When o circuito é removido, renomeado ou recriado com outro id
Then a seção antiga não é reutilizada pelo novo circuito
```

### AC11 — Ausência real

```gherkin
Given um circuito sem override manual e sem seção automática vigente
When o MOD-QT calcula o lote
Then S permanece como —
And o status permanece PEND
```

### AC12 — Não regressão normativa e contratual

```gherkin
Given a integração implementada
When os gates são executados
Then as fórmulas dos motores MOD-DC e MOD-QT permanecem inalteradas
And RetornoMODQT, ValidarMODQTSchema, RetornoMODQTSchema
And POST /api/v1/modulos/mod-qt/validar permanecem compatíveis
```

## Requisitos não funcionais

| ID | Requisito | Evidência mínima |
|---|---|---|
| NFR-REL-01 | Gravação em lote atômica e sem perda entre sessões. | AC6/AC7 e teste concorrente real. |
| NFR-REL-02 | Operação idempotente e retry seguro. | Retry com o mesmo `operacaoId`. |
| NFR-DUR-01 | Somente persistência durável gera estado aplicado. | AC9, reload, nova aba e nova sessão. |
| NFR-OBS-01 | Saída informa aplicados, ignorados, conflitos, falhas e tipo de persistência. | Contratos CLI/API, logs e UI. |
| NFR-SEC-01 | Serviço valida pertencimento projeto/circuito e RLS é revisada. | Testes negativos e parecer `@data-engineer`. |
| NFR-COMP-01 | Contratos públicos protegidos permanecem compatíveis. | AC12, typecheck, testes, build e inspeção por símbolo. |
| NFR-CLI-01 | Fluxo completo funciona sem UI. | AC1 sem React, navegador ou `localStorage`. |

## Escopo

### IN

- Caso de uso headless único para aplicar seções auto-otimizadas individualmente e em lote.
- Assinatura canônica no domínio/aplicação e ciclo `VIGENTE`/`OBSOLETA`.
- Migration aditiva posterior à `0011`, persistência atômica, versão/conflito e idempotência por `operacaoId`.
- Contrato CLI/API validado por schema, auditoria operacional e consumo pela UI.
- Confirmação individual e confirmação explícita consolidada do lote, conforme decisão `@po`/`@ux`.
- MOD-QT consumindo somente seção automática vigente, mantendo override manual auditado.
- Tratamento explícito de `DURAVEL`, `VOLATIL` e `FALHOU`.
- Revisão de RLS, pertencimento projeto/circuito, rollback e rollout controlado.
- Testes automatizados rastreáveis a AC1–AC12 e NFRs.

### OUT

- Alterar fórmulas C1–C6 ou fórmulas de queda de tensão.
- Inventar seção estimada, genérica ou padrão para circuito sem resultado real.
- Remover a edição manual auditada do MOD-QT.
- Usar ou promover `localStorage` como fonte compartilhada/durável.
- Criar histórico completo de todas as iterações da Auto-otimização.
- Resolver toda a autenticação/autorização do produto além do controle de risco RLS requerido.
- Alterar `RetornoMODQT`, `ValidarMODQTSchema`, `RetornoMODQTSchema` ou `POST /api/v1/modulos/mod-qt/validar` de forma incompatível.
- Reabrir ou ampliar retroativamente `MOD-QT-2-06`.

## Decisões condicionantes — bloqueiam transição para Ready

- [ ] `@architect` define e registra o nome/fronteira do caso de uso, entrypoint CLI/API, schemas e composição da assinatura.
- [ ] `@architect` + `@data-engineer` escolhem entre linha por `(projeto_id, circuito_id)` e merge JSONB atômico, incluindo concorrência, versionamento e idempotência.
- [ ] `@data-engineer` valida migration aditiva, dados legados, rollback, índices, locks, compatibilidade e RLS.
- [ ] `@po` + `@ux-design-expert` aprovam uma semântica inequívoca: “Otimizar e aplicar todos ({n})” ou “Otimizar todos” seguido de “Aplicar {n} seções aprovadas”.
- [ ] `@qa` registra a estratégia de testes AC/NFR antes do desenvolvimento.
- [ ] `@po` valida a story consolidada; somente então o status pode mudar de `Draft` para `Ready`.

## Tasks / Subtasks

- [ ] **Task 0 — Baseline e decisões da Fase 0** (AC: todos)
  - [ ] Reproduzir o cenário de origem e registrar seção base, seção otimizada, assinatura, persistência e valor no MOD-QT.
  - [ ] Registrar as decisões condicionantes de arquitetura, dados, CLI/API e UX sem iniciar código antes de `Ready`.
  - [ ] Consolidar a matriz AC/NFR → testes e obter validação `@po`.
- [ ] **Task 1 — Assinatura e validade** (AC: 4, 5, 10)
  - [ ] Criar assinatura canônica e determinística com circuito, parâmetros efetivos e retornos downstream relevantes.
  - [ ] Implementar `VIGENTE`/`OBSOLETA` e regras de invalidação/preservação.
  - [ ] Rejeitar seção `0`, negativa, `NaN`, infinita ou fora do contrato.
- [ ] **Task 2 — Persistência atômica e segura** (AC: 6, 7, 9, 10)
  - [ ] Criar migration aditiva, operação atômica, versão/conflito e idempotência por `operacaoId`.
  - [ ] Ler somente registros vigentes e tratar legados sem assinatura sem promoção automática.
  - [ ] Diferenciar `DURAVEL`, `VOLATIL` e `FALHOU`; validar RLS e pertencimento.
  - [ ] Provar apply → rollback → reapply e concorrência real no Supabase.
- [ ] **Task 3 — Caso de uso headless e CLI/API** (AC: 1, 3, 9)
  - [ ] Recalcular/validar circuito real e usar `secaoEsperadaMm2` somente para detectar divergência de preview.
  - [ ] Expor o mesmo caso de uso por CLI/API com schemas e auditoria operacional.
  - [ ] Testar sem React, navegador ou `localStorage`.
- [ ] **Task 4 — Aplicação individual e em lote na UI** (AC: 2, 3, 9)
  - [ ] Ligar “Confirmar seção” ao caso de uso comum.
  - [ ] Implementar a semântica de lote aprovada e enviar apenas resultados aprovados.
  - [ ] Exibir calculados, aprovados, aplicados, ignorados, conflitos, falhas e persistência; marcar aplicado somente após `DURAVEL`.
- [ ] **Task 5 — Consumo e precedência no MOD-QT** (AC: 2, 4, 8, 10, 11)
  - [ ] Consultar somente seção automática vigente e refazer a query após aplicação na mesma sessão.
  - [ ] Preservar precedência manual, justificativa e auditoria.
  - [ ] Ao remover manual, revelar automática vigente ou `—`/`PEND`.
- [ ] **Task 6 — Segurança, rollout e observabilidade** (AC: 6, 7, 9, 10)
  - [ ] Validar migration, rollback, RLS, ambiente sem migration e novas sessões.
  - [ ] Garantir que policy não fique mais ampla sem risco aceito, responsável e prazo.
  - [ ] Registrar `operacaoId`, projeto, circuitos, assinaturas, versão, contagens, conflitos e persistência sem segredos.
- [ ] **Task 7 — Não regressão e gates** (AC: 12; NFRs: todos)
  - [ ] Executar testes focados, headless, concorrência, migration/RLS e reload/nova sessão.
  - [ ] Verificar por símbolo os contratos protegidos e a ausência de mudanças nas fórmulas.
  - [ ] Executar `npm run lint`, `npm run typecheck`, `npm test` e `npm run build` na raiz e na aplicação quando aplicável.
  - [ ] Atualizar checkboxes, Dev Agent Record, Change Log, File List e QA Results.

## Rastreabilidade AC → testes

| AC | Camada | Evidência automatizada mínima |
|---|---|---|
| AC1 | Serviço + CLI/API | Aplicação individual headless persiste vigente e retorna `DURAVEL`. |
| AC2 | UI + integração | Confirmação usa o caso comum e preenche `S` após durabilidade. |
| AC3 | Serviço + UI | Lote explícito filtra inválidos, é atômico e retorna contagens. |
| AC4 | Domínio + integração | Assinatura diferente invalida anterior e produz `PEND`. |
| AC5 | Domínio + serviço | Falha transitória com mesma assinatura preserva vigente. |
| AC6 | Repositório Supabase | Escritas concorrentes em circuitos distintos permanecem. |
| AC7 | Repositório Supabase | Conflito no mesmo circuito é detectado/ordenado. |
| AC8 | Serviço MOD-QT + API | Manual prevalece; remoção revela automática vigente. |
| AC9 | Repositório + UI | Ausência/indisponibilidade não produz falso sucesso. |
| AC10 | Serviço + repositório | Ciclo de vida não ressuscita seção antiga. |
| AC11 | Serviço MOD-QT + UI | Sem fonte válida exibe `—` e `PEND`. |
| AC12 | Contrato + regressão | Símbolos, typecheck, testes e build compatíveis. |

Casos adicionais: ordem de propriedades não muda a assinatura; parâmetros efetivos diferentes mudam a assinatura; circuito inexistente/cross-project é rejeitado; retry idêntico não duplica efeitos; falha transacional não deixa aplicação parcial; somente valores duráveis sobrevivem a reload/nova aba/nova sessão.

## Dev Notes

### Contrato conceitual mínimo

```ts
interface AplicarSecoesOtimizadasInput {
  readonly projetoId: string;
  readonly operacaoId: string;
  readonly itens: ReadonlyArray<{
    readonly circuitoId: string;
    readonly parametrosEfetivos: ParametrosDimensionamento;
    readonly secaoEsperadaMm2?: number;
  }>;
}

interface AplicarSecoesOtimizadasOutput {
  readonly persistencia: "DURAVEL" | "VOLATIL" | "FALHOU";
  readonly aplicados: ReadonlyArray<string>;
  readonly ignorados: ReadonlyArray<{ circuitoId: string; motivo: string }>;
  readonly conflitos: ReadonlyArray<string>;
}
```

O nome e o entrypoint finais permanecem sob decisão de `@architect`. A assinatura é sempre produzida no domínio/aplicação; a UI nunca fornece uma assinatura autoritativa. O lote é uma única transação: sucesso parcial de cálculo não autoriza sucesso parcial de aplicação sem regra explicitamente aprovada.

### Precedência protegida no MOD-QT

1. override explícito da chamada/simulação;
2. edição manual auditada no MOD-QT;
3. seção automática MOD-DC vigente e compatível;
4. seção real existente no contrato do circuito;
5. ausência `null` → `—` e `PEND`.

### Contratos e áreas protegidas

- `RetornoMODQT`
- `ValidarMODQTSchema`
- `RetornoMODQTSchema`
- `POST /api/v1/modulos/mod-qt/validar`
- fórmulas C1–C6 do MOD-DC
- fórmulas dos motores de queda de tensão

### Arquivos de impacto previsto

- Domínio/aplicação: `src/domain/servicos/servico-dimensionamento-condutores.ts`, `src/domain/servicos/servico-queda-tensao.ts` e helper novo de assinatura em caminho aprovado por `@architect`.
- Contrato headless: `src/api/schemas/otimizar-condutor.schema.ts` ou schema compatível novo, `src/routes/api/v1/otimizar-condutor.ts` ou rota de aplicação nova, `src/lib/api-client.ts` e entrypoint em `bin/` definido na Fase 0.
- Persistência: repositório em memória, repositório Supabase e migration aditiva posterior a `docs/supabase/0011_dimensionamento_condutores_resultado.sql`.
- UI: `DimensionamentoCondutoresResumo.tsx`, rota de queda de tensão e `TabelaResultadosQuedaTensao.tsx`.
- Testes: fluxo MOD-DC, endpoints MOD-QT, VRT, resumo de Auto-otimização, repositório Supabase e testes novos de caso headless/concorrência.

> Os paths acima são previsões do plano. Caminhos novos e alternativas “ou” devem ser fixados pelas decisões da Fase 0 antes da implementação.

### Testing

- Framework existente: Vitest; testes de componente seguem o padrão atual de `renderToStaticMarkup` quando não houver browser/jsdom.
- Reexecutar evidências independentemente no QA gate; não aceitar apenas o log do desenvolvimento.
- Cobrir teste real de concorrência Supabase, apply/rollback/reapply da migration, RLS/cross-project, banco ausente, reload/nova aba/nova sessão, precedência manual/automática e compatibilidade por símbolo.
- Gates obrigatórios: `npm run lint`, `npm run typecheck`, `npm test`, `npm run build`, além dos focados.

## Riscos e mitigações

| Risco | Prob. | Impacto | Mitigação obrigatória |
|---|---|---|---|
| Seção antiga usada com parâmetros novos | Média | Crítico | Assinatura canônica, estado obsoleto e AC4. |
| Perda de chave por concorrência | Média | Alto | Operação atômica, versionamento e AC6/AC7. |
| Calculado confundido com aplicado | Média | Alto | Vocabulário obrigatório e confirmação explícita. |
| Fallback volátil tratado como durável | Média | Alto | Saída tipada, UI sem falso sucesso e AC9. |
| Lote aplicado sem consentimento inequívoco | Média | Alto | Decisão `@po`/`@ux` antes de Ready. |
| Circuito removido ressuscitar valor antigo | Baixa | Alto | Invalidação e AC10. |
| RLS permitir alteração indevida | Média | Alto | Parecer `@data-engineer`, pertencimento e risco aceito formal. |
| Expansão de `MOD-QT-2-06` | Alta | Médio | Story sucessora isolada e File List própria. |
| Regressão de contrato/fórmula | Baixa | Crítico | AC12 e inspeção por símbolo. |

## Estratégia de rollback

- Criar apenas migration aditiva; não editar destrutivamente a `0011` já aplicada.
- Definir e testar scripts/passos de rollback e reapply em ambiente isolado antes de rollout.
- Durante transição, manter leitura compatível sem promover legados sem assinatura; classificá-los para revalidação/obsolescência ou recalculá-los realmente.
- Se migration, health ou smoke falhar, desabilitar o caminho novo de aplicação conforme runbook autorizado, reverter a migration pela estratégia aprovada e manter o comportamento anterior sem apresentar valores voláteis como vigentes.
- Não remover nem corromper overrides manuais auditados; após rollback, a ausência de fonte automática válida deve resultar em `—`/`PEND`.
- Rollback remoto, deploy e efeitos externos permanecem sob autoridade exclusiva de `@devops` e flags do manifesto.

## CodeRabbit Integration

**Primary Type:** Architecture / Database / API / Integration  
**Secondary Types:** Frontend, Security, Deployment  
**Complexity:** Alta

**Agentes previstos:** `@dev` (implementação/pre-commit), `@architect`, `@data-engineer`, `@ux-design-expert`, `@qa` e `@devops` para operações remotas.

- [ ] Pre-Commit (`@dev`): qualidade, segurança básica, atomicidade, contratos e testes focados.
- [ ] Pre-PR (`@devops`): compatibilidade, migration/RLS, regressões e CodeRabbit sem issue CRITICAL.
- [ ] Pre-Deployment (`@devops`): autorização, rollback, configuração, smoke e observabilidade.

**Self-healing esperado:** `@dev` em modo light, máximo 2 iterações/15 minutos para CRITICAL; HIGH documentado. `@qa` reexecuta o gate completo. Nenhuma correção automática pode inventar decisão condicionante, alterar fórmula protegida ou transformar `BLOCK` em `PASS`.

**Focos:** SQL/migration reversível, RLS, concorrência, idempotência, validação de input/output, ownership projeto/circuito, estados acessíveis sem depender apenas de cor, ausência de segredo e contratos protegidos.

## Checklist de Draft

### Goal & Context

- [x] Objetivo, valor e fluxo do sistema estão explícitos.
- [x] Predecessoras e limite de não ampliação estão identificados.
- [x] AC1–AC12 e NFRs são testáveis e rastreáveis.

### Guidance & Self-containment

- [x] Vocabulário, contrato conceitual, precedência e áreas protegidas estão resumidos.
- [x] Arquivos de impacto, edge cases, segurança, riscos e rollback estão descritos.
- [x] Decisões ainda não aprovadas estão marcadas como bloqueantes, sem invenção.

### Testing & Quality

- [x] Matriz AC → teste e casos adicionais estão definidos.
- [x] Gates de lint, typecheck, testes e build estão definidos.
- [x] CodeRabbit e agentes especializados estão previstos.

### Prontidão

- [x] Decisões condicionantes da Fase 0 registradas em ADR, parecer de dados, decisão UX e matriz QA.
- [x] Validação de escopo e rastreabilidade concluída com nota 10/10 pelo orquestrador, com gate QA independente posterior.
- [x] Status alterado para `Ready` após consolidação dos artefatos da Fase 0.

**Avaliação do SM:** Draft completo e auto-contido; **não Ready** enquanto arquitetura/dados, UX/PO, contrato CLI/API e estratégia QA permanecerem pendentes.

## Definition of Done

- [ ] Story validada sem ampliar `MOD-QT-2-06`.
- [ ] Decisões de arquitetura/dados e confirmação do lote aprovadas.
- [ ] Caso de uso headless funciona antes da UI.
- [ ] Assinatura canônica e ciclo `VIGENTE`/`OBSOLETA` implementados.
- [ ] Aplicação individual e em lote usam o mesmo caminho.
- [ ] Persistência atômica, idempotente e resistente a concorrência.
- [ ] UI distingue calculado, aplicado, durável, volátil e falhou.
- [ ] MOD-QT usa apenas automática vigente; manual prevalece e sua remoção revela automática ou `PEND`.
- [ ] Migration aditiva, rollback e RLS validados.
- [ ] AC1–AC12 e NFRs possuem evidências automatizadas.
- [ ] Contratos protegidos e fórmulas permanecem intactos.
- [ ] `npm run lint`, `npm run typecheck`, `npm test` e `npm run build` passam.
- [ ] Checklist, File List, Dev Agent Record, Change Log e QA Results atualizados.

## File List inicial

**Criado nesta etapa:**

- `docs/stories/story-AUTO-OTI-1.3-aplicar-secao-auto-otimizada-no-mod-qt.md`

**Impacto previsto — confirmar/atualizar durante implementação:**

- `sistema-de-instala-es-el-tricas-sie-main/src/domain/servicos/servico-dimensionamento-condutores.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/servicos/servico-queda-tensao.ts`
- helper novo de assinatura canônica, path a definir por `@architect`
- schema/rota/entrypoint CLI/API a definir na Fase 0
- `sistema-de-instala-es-el-tricas-sie-main/src/lib/api-client.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/infra/repositorios/repositorio-resultado-dimensionamento-condutores.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/infra/supabase/repo-resultado-dimensionamento-condutores.supabase.ts`
- migration aditiva posterior a `sistema-de-instala-es-el-tricas-sie-main/docs/supabase/0011_dimensionamento_condutores_resultado.sql`
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/dimensionamento-condutores/DimensionamentoCondutoresResumo.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/src/routes/projetos.$projetoId_.queda-tensao.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/queda-tensao/TabelaResultadosQuedaTensao.tsx`
- testes existentes listados no plano e testes novos do caso headless/concorrência.

## Change Log

| Data | Versão | Descrição | Autor |
|---|---|---|---|
| 2026-08-02 | 0.1 | Story sucessora criada em Draft a partir do plano v2 e workflow SDC YOLO, com AC1–AC12, NFRs, riscos, rollback, checklists, File List inicial e rastreabilidade às predecessoras. | @sm (River) |
| 2026-08-02 | 0.2 | Fase 0 consolidada: ADR de contrato headless, parecer de dados/concorrência, decisão UX de aplicação em duas etapas e matriz QA registrados. Escopo validado 10/10; status Draft → Ready. | @aiox-master (Orion) |

## Dev Agent Record

### Recovery implementation — 2026-08-02

- Replaced the shared `node:crypto` SHA-256 import with asynchronous Web Crypto, preserving deterministic hashes while keeping the domain module browser-safe.
- Normalized the validated API payload so `parametrosEfetivos` remains mandatory at the application boundary despite Zod inferring `unknown` as optional.
- Rebuilt the SPA artifact. The local `dist` bundle no longer contains `node:crypto`; its CSS includes the SIE and Command Center design tokens.
- Validation passed: `npm run typecheck`, focused headless Vitest (2/2), the MOD-QT endpoint suite (20/20), and `npm run build:spa`. `npm run lint` exceeded 180 seconds without a conclusive diagnostic and remains pending. The full suite still has eight visual snapshot mismatches outside this recovery scope.

### Agent Model Used

Codex @dev (Dex)

### Debug Log References

2026-08-02: MOD-QT passou a consultar exclusivamente `repoSecoesOtimizadas.vigentes/obterVigente`; UI deixou de carregar/gravar resultados em localStorage; confirmação individual e lote usam o caso de uso `aplicarSecoesOtimizadasProjeto` e só marcam aplicado após `DURAVEL`.
2026-08-02: `npm run typecheck -- --pretty false` excedeu o timeout operacional; gates completos e validações Supabase permanecem pendentes.

### Completion Notes List

- Leitura vigente e precedência manual corrigidas no MOD-QT.
- Fluxo UI em duas etapas, sem localStorage como fonte, com contagens de aprovados/aplicados.
- Confirmação individual usa o caso headless e exige persistência DURAVEL.

### File List final

- `sistema-de-instala-es-el-tricas-sie-main/src/domain/servicos/servico-queda-tensao.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/lib/api-client.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/dimensionamento-condutores/DimensionamentoCondutoresResumo.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/src/application/aplicar-secoes-otimizadas-projeto.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/dimensionamento-condutores/assinatura-secao-otimizada.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/infra/repositorios/repositorio-secoes-otimizadas.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/api/schemas/aplicar-secoes-otimizadas.schema.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/routes/api/v1/projetos.$projetoId.dimensionamento-condutores.aplicar-secoes-otimizadas.ts`
- `sistema-de-instala-es-el-tricas-sie-main/bin/aplicar-secoes-otimizadas.mjs`
- `sistema-de-instala-es-el-tricas-sie-main/docs/supabase/0013_secoes_otimizadas.sql`
- `sistema-de-instala-es-el-tricas-sie-main/tests/domain/dimensionamento-condutores/aplicar-secoes-otimizadas.test.ts`
- `docs/stories/story-AUTO-OTI-1.3-aplicar-secao-auto-otimizada-no-mod-qt.md`

## QA Results

**Veredito:** CONCERNS (2026-08-02, revisão do orquestrador aguardando reexecução independente).

- Evidência estrutural presente: caso headless, assinatura, idempotência em memória, endpoint, CLI, UI em duas etapas e leitura vigente-only no MOD-QT.
- `node --check bin/aplicar-secoes-otimizadas.mjs` e `git diff --check` passaram para os arquivos tocados.
- `npm run typecheck`, Vitest focado e lint completo excederam o timeout operacional sem saída conclusiva.
- Migration/RLS, concorrência real Supabase, apply/rollback/reapply e validação de recálculo no domínio ainda bloqueiam `PASS` e qualquer rollout.

---

### Registro de implementação local — @dev / @aiox-master

- Núcleo headless, assinatura canônica, repositório em memória, rota/schema, CLI e migration aditiva foram implementados.
- A UI recebeu confirmação individual e lote em duas etapas; MOD-QT consulta a fonte automática vigente antes da fonte legada.
- Arquivos principais: `src/application/aplicar-secoes-otimizadas-projeto.ts`, `src/domain/dimensionamento-condutores/assinatura-secao-otimizada.ts`, `src/infra/repositorios/repositorio-secoes-otimizadas.ts`, `src/api/schemas/aplicar-secoes-otimizadas.schema.ts`, rota API, `src/lib/api-client.ts`, `src/infra/contexto.ts`, `src/domain/servicos/servico-queda-tensao.ts`, `DimensionamentoCondutoresResumo.tsx`, `docs/supabase/0013_secoes_otimizadas.sql`, `bin/aplicar-secoes-otimizadas.mjs` e teste focado.
- `npm run typecheck` e Vitest focado excederam 120s sem saída neste ambiente. O gate permanece **CONCERNS** até validação independente de migration/RLS, concorrência real e recalculo de autoridade.

**Story created by:** @sm (River)  
**Status de handoff:** Ready; Fase 0 consolidada, próxima etapa `@dev` para implementação condicionada aos gates de dados e segurança.
