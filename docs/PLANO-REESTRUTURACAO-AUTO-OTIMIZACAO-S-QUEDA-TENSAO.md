# Plano de Reestruturação v2 — Auto-otimização do MOD-DC para S (mm²) no MOD-QT

**Data:** 2026-08-02  
**Versão:** 2.0 — revisão pós-QA/Quinn  
**Status:** Draft condicionado a validação de arquitetura e dados  
**Prioridade sugerida:** P1  
**Story recomendada:** nova sucessora `AUTO-OTI-1.3` (identificador final sob autoridade de `@sm`/`@po`)  
**Módulos:** Dimensionamento de condutores (MOD-DC) e Queda de tensão (MOD-QT)

## 1. Artefatos de origem e governança

Este plano deriva de:

- solicitação do usuário para abastecer automaticamente `S (mm²)` com a seção exibida em **Auto-otimização**;
- `docs/stories/story-AUTO-OTI-1.2.md`, cuja QA registrou a persistência da seção confirmada como candidata a `AUTO-OTI-1.3`;
- `docs/stories/story-MOD-QT-2-06-persistencia-secao-mod-dc.md`, que implementa persistência do dimensionamento base e leitura pelo MOD-QT;
- análise QA de 2026-08-02, que identificou riscos de seção obsoleta, concorrência, falso sucesso do fallback, ambiguidade de aplicação em lote, RLS permissiva e ausência de operação headless.

### 1.1 Limite de story

Esta reestruturação não deve ampliar retroativamente o escopo de `MOD-QT-2-06`, atualmente em revisão. Deve ser criada uma nova story, vinculada a `AUTO-OTI-1.2` e `MOD-QT-2-06`, antes de qualquer alteração de código.

Autoridades:

- `@sm`/`@po`: criação e validação da nova story;
- `@architect`: decisão do contrato de aplicação e da estratégia de concorrência;
- `@data-engineer`: validação do modelo persistente, migration, operação atômica e RLS;
- `@dev`: implementação após story pronta;
- `@qa`: validação da rastreabilidade, testes e gate.

## 2. Objetivo

Garantir que a seção aprovada e aplicada pela Auto-otimização do MOD-DC seja persistida por projeto/circuito e consumida automaticamente pela coluna `S (mm²)` do MOD-QT, sem redigitação e sem aceitar valores obsoletos como vigentes.

O fluxo deve:

- funcionar por operação headless antes da integração de UI;
- permitir aplicação individual e em lote;
- distinguir resultado calculado, aprovado, aplicado, persistido, vigente e obsoleto;
- preservar a edição manual auditada no MOD-QT;
- impedir perda de atualização entre sessões concorrentes;
- impedir falso sucesso quando a persistência durável estiver indisponível;
- invalidar seções incompatíveis com novas entradas efetivamente aplicadas;
- não criar seção estimada, genérica ou padrão;
- não alterar fórmulas dos motores MOD-DC ou MOD-QT.

## 3. Diagnóstico confirmado

### 3.1 Fluxos já existentes

1. O dimensionamento em lote persiste `secao_fase_mm2` em `dimensionamento_condutores_resultado`.
2. O MOD-QT lê essa persistência antes de montar a entrada do motor.
3. A precedência atual já coloca o override manual do MOD-QT acima da seção persistida.
4. A edição manual de S já exige justificativa e reutiliza `aplicarCenario`.
5. A Auto-otimização é calculada por `otimizarCondutorDireto` e mantida em React/`localStorage`.
6. A confirmação individual e **Otimizar todos** ainda não gravam na fonte consumida pelo MOD-QT.

### 3.2 Falhas estruturais a corrigir

- O mapa persistente atual guarda apenas `circuitoId -> number` e não comprova com quais entradas a seção foi calculada.
- Resultados nulos são ignorados durante o merge; uma seção antiga pode sobreviver a uma nova tentativa incompatível.
- `salvarMuitos` executa leitura seguida de `upsert` do JSONB inteiro; duas sessões podem perder atualizações.
- O fallback volátil retorna como sucesso, embora não sobreviva a nova sessão.
- O endpoint atual de Auto-otimização calcula, mas não possui contrato para aplicar/persistir resultados.
- A migration `0011` concede acesso total a `anon` e `authenticated`, seguindo dívida de segurança existente.

## 4. Vocabulário obrigatório de estado

| Termo             | Definição                                                                                                          |
| ----------------- | ------------------------------------------------------------------------------------------------------------------ |
| **Calculado**     | O motor produziu um `ResultadoOtimizacao`; ainda não é fonte vigente.                                              |
| **Aprovado**      | `status === "APROVADO"` e `secaoFinal` é finita e positiva.                                                        |
| **Aplicado**      | O usuário confirmou a seção individualmente ou confirmou uma aplicação em lote.                                    |
| **Persistido**    | A operação durável foi confirmada pelo repositório; não inclui fallback volátil.                                   |
| **Vigente**       | Persistido, não invalidado e compatível com a assinatura da última entrada aplicada.                               |
| **Obsoleto**      | Existe historicamente, mas sua assinatura não corresponde à nova entrada aplicada ou o circuito deixou de existir. |
| **Manual MOD-QT** | Override auditado em `config.secoes_aplicadas_mm2`; prevalece sobre o automático.                                  |

A UI não deve usar cor, badge ou mensagem de “aplicado” quando o estado for somente **Calculado** ou armazenado apenas no fallback volátil.

## 5. Decisões funcionais revisadas

### 5.1 Aplicação individual

1. O usuário executa a Auto-otimização.
2. O resultado fica **Calculado**.
3. Se estiver aprovado, o usuário aciona **Confirmar seção {n} mm²**.
4. O caso de uso headless aplica e persiste a seção.
5. A UI só marca como aplicada depois da confirmação durável.
6. O MOD-QT passa a consumir a nova seção vigente.

### 5.2 Aplicação em lote

Para eliminar ambiguidade, o comando deve deixar explícita a aplicação. A solução preferencial é:

- renomear a ação para **Otimizar e aplicar todos ({n})**; ou
- manter **Otimizar todos** e exigir uma confirmação consolidada **Aplicar {n} seções aprovadas**.

A escolha visual final deve ser validada por `@po`/`@ux`, mas ambas obedecem à mesma regra funcional: apenas uma ação explicitamente confirmada persiste o lote.

O lote deve:

- coletar apenas resultados aprovados;
- informar calculados, aprovados, persistidos, ignorados e falhas;
- executar uma única operação atômica de aplicação;
- não marcar nenhum item como aplicado se a transação durável falhar;
- ser idempotente para a mesma chave de operação e mesma assinatura.

### 5.3 Resultado inválido e validade temporal

O comportamento depende da assinatura:

| Situação                                                                       | Resultado esperado                                                                   |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------ |
| Falha transitória com a mesma assinatura da seção vigente                      | Manter a seção vigente; registrar falha da tentativa.                                |
| Nova entrada aplicada com assinatura diferente e otimização sem seção aprovada | Invalidar a seção automática anterior; MOD-QT usa override manual ou retorna `PEND`. |
| Circuito removido                                                              | Invalidar/remover sua seção automática.                                              |
| Circuito renomeado ou recriado                                                 | Tratar como novo circuito; não reutilizar seção pela coincidência de descrição.      |
| Mudança apenas no formulário, sem aplicação                                    | Não altera a fonte persistente vigente.                                              |

### 5.4 Precedência no MOD-QT

1. override explícito da chamada/simulação;
2. edição manual auditada no MOD-QT;
3. seção automática MOD-DC vigente e compatível;
4. seção realmente disponível no contrato do circuito, quando existente;
5. ausência real: `null`, exibição `—` e status `PEND`.

Ao remover o override manual, o MOD-QT deve revelar a seção automática vigente mais recente. Se ela estiver obsoleta ou ausente, deve retornar `PEND`.

## 6. Contrato de aplicação headless — CLI First

Antes da UI, deve existir um caso de uso de aplicação independente de React e `localStorage`.

Contrato conceitual:

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

Regras:

- o serviço carrega o circuito do projeto, recalcula/valida a Auto-otimização e usa a seção aprovada produzida pelo domínio;
- `secaoEsperadaMm2`, quando enviada pela UI, serve apenas para detectar divergência entre preview e aplicação, nunca como autoridade de cálculo;
- a assinatura é gerada no domínio/aplicação a partir do circuito real e dos parâmetros efetivos validados, nunca recebida pronta da UI;
- o serviço valida se cada circuito pertence ao projeto e se o resultado recalculado está aprovado;
- `operacaoId` suporta idempotência e retry seguro;
- a operação deve ser acessível por adaptador CLI/API definido na nova story;
- o nome e o entrypoint do comando em `bin/` serão definidos por `@architect`, mas o aceite exige execução completa sem navegador;
- a UI usa o mesmo caso de uso, sem criar um segundo caminho de gravação.

## 7. Contrato persistente e concorrência

### 7.1 Registro lógico mínimo por circuito

```ts
interface SecaoAutomaticaVigente {
  readonly projetoId: string;
  readonly circuitoId: string;
  readonly secaoFaseMm2: number;
  readonly origem: "DIMENSIONAMENTO_LOTE" | "AUTO_OTIMIZACAO";
  readonly assinaturaEntrada: string;
  readonly estado: "VIGENTE" | "OBSOLETA";
  readonly versao: number;
  readonly atualizadoEm: string;
}

type SecoesPorCircuito = Readonly<Record<string, SecaoAutomaticaVigente>>;
```

### 7.2 Decisão arquitetural obrigatória

Antes da implementação, `@architect` e `@data-engineer` devem escolher e registrar uma das estratégias:

1. **Recomendada — linha por projeto/circuito:** chave composta `(projeto_id, circuito_id)`, upsert por linha e versão para concorrência otimista.
2. **Compatível com JSONB — merge atômico no banco:** função/RPC que atualiza somente as chaves recebidas e seus metadados, sem ciclo cliente `SELECT → merge → UPSERT`.

Critérios obrigatórios para qualquer estratégia:

- duas sessões alterando circuitos diferentes não perdem dados;
- duas sessões alterando o mesmo circuito detectam conflito ou aplicam uma ordem explícita;
- o lote é atômico;
- retry com o mesmo `operacaoId` não duplica efeitos;
- exclusão/invalidação de circuito não deixa valor reutilizável por engano;
- leitura do MOD-QT retorna somente registros vigentes.

### 7.3 Migração

- Não editar destrutivamente a migration `0011` se ela já tiver sido aplicada.
- Criar migration aditiva após validação do modelo escolhido.
- Valores legados sem assinatura devem receber estado `REVALIDAR`/`OBSOLETA` ou passar por recálculo real antes de se tornarem vigentes.
- Não promover automaticamente valores do `localStorage` para persistência durável.
- Registrar estratégia de rollback e compatibilidade de leitura durante a transição.

## 8. Persistência durável e fallback

O resultado da gravação deve distinguir explicitamente:

- `DURAVEL`: persistido no banco e elegível para estado aplicado;
- `VOLATIL`: disponível somente na sessão local e nunca apresentado como persistido;
- `FALHOU`: nenhuma alteração aplicada.

Regras de release:

1. A migration é pré-requisito para ambiente produtivo.
2. Ausência de tabela em produção deve falhar de forma observável.
3. O fallback volátil pode permanecer apenas para desenvolvimento/testes, sinalizado na saída.
4. Reload, nova aba e nova sessão são evidências obrigatórias de persistência durável.

## 9. Segurança e RLS

A nova story não precisa resolver toda a autenticação do produto, mas deve impedir ampliação silenciosa do risco.

Requisitos:

- `@data-engineer` deve revisar as policies da migration vigente e da migration aditiva;
- o acesso não pode ser mais amplo que o modelo de projetos já aprovado;
- se `FOR ALL TO anon USING (true)` precisar ser mantido por compatibilidade, a exceção deve ser registrada como risco aceito com responsável e prazo de revisão;
- projeto/circuito enviados pelo cliente devem ser validados no serviço antes da gravação;
- testes devem cobrir tentativa de gravar circuito inexistente ou pertencente a outro projeto.

## 10. Fluxo-alvo

```text
CLI/API/UI
   |
   v
Otimizar circuito(s)
   |
   v
Resultado Calculado
   |
   v
Confirmação individual ou consolidada
   |
   v
Caso de uso headless aplicarSecoesOtimizadasProjeto
   |  - valida projeto/circuito
   |  - valida seção aprovada
   |  - gera assinatura canônica
   |  - controla idempotência/conflito
   v
Persistência atômica durável
   |
   v
Seção automática VIGENTE
   |
   v
MOD-QT resolve precedência
manual auditado > automática vigente > ausência/PEND
```

## 11. Plano de execução por fases

### Fase 0 — Decisões e baseline

1. Criar a nova story sucessora.
2. Reproduzir o cenário dos screenshots.
3. Registrar seção base, seção otimizada, assinatura, persistência e valor no MOD-QT.
4. Decidir estratégia de concorrência e migration.
5. Decidir a confirmação explícita do lote com `@po`/`@ux`.
6. Definir entrypoint CLI/API e schemas.

**Gate:** nenhuma implementação começa sem story Ready e decisões registradas.

### Fase 1 — Assinatura e ciclo de validade

1. Criar função canônica e determinística de assinatura no domínio/aplicação.
2. Incluir circuito, parâmetros efetivos e retornos downstream que afetem o resultado.
3. Remover a UI como autoridade da assinatura persistente.
4. Implementar estados `VIGENTE` e `OBSOLETA`.
5. Implementar invalidação por nova entrada aplicada, remoção ou recriação de circuito.

### Fase 2 — Persistência atômica

1. Criar migration aditiva.
2. Implementar operação atômica e controle de versão/idempotência.
3. Implementar leitura somente de seções vigentes.
4. Diferenciar persistência durável, volátil e falha.
5. Cobrir concorrência real no repositório Supabase.

### Fase 3 — Operação headless

1. Implementar o caso de uso de aplicação no serviço.
2. Expor o mesmo caso de uso por CLI/API.
3. Validar input/output por schema.
4. Testar sem navegador, React ou `localStorage`.
5. Registrar auditoria operacional: operação, projeto, circuitos, contagens e conflitos.

### Fase 4 — Auto-otimização individual e em lote

1. Ligar **Confirmar seção** ao caso de uso headless.
2. Implementar a decisão de confirmação consolidada do lote.
3. Atualizar estado visual somente após `DURAVEL`.
4. Exibir calculados, aprovados, aplicados, ignorados, conflitos e falhas.
5. Não converter resultados parciais em vigentes.

### Fase 5 — Consumo no MOD-QT

1. Manter `servico-queda-tensao.ts` como autoridade da precedência.
2. Consultar apenas seção automática vigente.
3. Invalidar/refazer a query após aplicação na mesma sessão.
4. Preservar edição manual, justificativa e auditoria.
5. Ao remover edição manual, revelar a automática vigente ou `PEND`.

### Fase 6 — Segurança, migração e rollout

1. Validar migration, rollback, RLS e compatibilidade.
2. Aplicar migration antes da funcionalidade de UI.
3. Validar ambiente sem migration e falha observável.
4. Validar reload, nova aba e nova sessão.
5. Executar rollout controlado com métrica de sucesso/falha de persistência.

### Fase 7 — Gates e handoff

```bash
npm run lint
npm run typecheck
npm test
npm run build
```

Também devem ser executados:

- testes focados dos arquivos alterados;
- teste headless do caso de uso;
- teste de concorrência no Supabase;
- validação da migration/RLS por `@data-engineer`;
- verificação por símbolo dos contratos protegidos;
- atualização de checklist, File List e Dev Agent Record da nova story.

## 12. Critérios de aceite revisados

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

## 13. Rastreabilidade AC → testes

| AC   | Camada                | Evidência automatizada mínima                                      |
| ---- | --------------------- | ------------------------------------------------------------------ |
| AC1  | Serviço + CLI/API     | Aplicação individual headless persiste registro vigente e durável. |
| AC2  | UI + integração       | Confirmação individual usa o caso de uso comum e preenche S.       |
| AC3  | Serviço + UI          | Lote explícito filtra inválidos, é atômico e retorna contagens.    |
| AC4  | Domínio + integração  | Assinatura diferente invalida valor anterior e produz `PEND`.      |
| AC5  | Domínio + serviço     | Falha transitória com mesma assinatura preserva a vigente.         |
| AC6  | Repositório Supabase  | Duas gravações concorrentes em circuitos diferentes permanecem.    |
| AC7  | Repositório Supabase  | Conflito de versão no mesmo circuito é detectado.                  |
| AC8  | Serviço MOD-QT + API  | Manual prevalece; remoção revela automática vigente.               |
| AC9  | Repositório + UI      | Tabela ausente/banco indisponível não produz falso sucesso.        |
| AC10 | Serviço + repositório | Exclusão/renomeação não ressuscita seção antiga.                   |
| AC11 | Serviço MOD-QT + UI   | Sem fonte válida exibe `—` e `PEND`.                               |
| AC12 | Contrato + regressão  | Verificação por símbolo, typecheck, testes e build.                |

Casos adicionais obrigatórios:

- seção `0`, negativa, `NaN`, infinita ou fora do contrato é rejeitada;
- circuito inexistente ou de outro projeto é rejeitado;
- retry com o mesmo `operacaoId` é idempotente;
- sucesso parcial de cálculo não vira sucesso parcial de transação sem regra explícita;
- reload, nova aba e nova sessão preservam somente valores duráveis;
- parâmetros efetivos diferentes produzem assinaturas diferentes;
- ordem das propriedades não altera a assinatura canônica.

## 14. Requisitos não funcionais

| ID          | Requisito                                                                     | Evidência                                    |
| ----------- | ----------------------------------------------------------------------------- | -------------------------------------------- |
| NFR-REL-01  | Gravação em lote atômica e sem perda entre sessões.                           | Testes AC6/AC7.                              |
| NFR-REL-02  | Operação idempotente e com retry seguro.                                      | Teste por `operacaoId`.                      |
| NFR-DUR-01  | Somente persistência durável gera estado aplicado.                            | AC9 + teste de nova sessão.                  |
| NFR-OBS-01  | Saída informa aplicados, ignorados, conflitos, falhas e tipo de persistência. | Testes de contrato e UI.                     |
| NFR-SEC-01  | Serviço valida pertencimento projeto/circuito e RLS é revisada.               | Testes negativos + parecer `@data-engineer`. |
| NFR-COMP-01 | Contratos públicos protegidos permanecem compatíveis.                         | AC12.                                        |
| NFR-CLI-01  | Fluxo completo funciona sem UI.                                               | AC1.                                         |

## 15. Arquivos com impacto previsto

### Domínio e aplicação

- `sistema-de-instala-es-el-tricas-sie-main/src/domain/servicos/servico-dimensionamento-condutores.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/domain/servicos/servico-queda-tensao.ts`
- novo helper de assinatura canônica no domínio/aplicação, com caminho definido pela nova story

### Contrato headless

- `sistema-de-instala-es-el-tricas-sie-main/src/api/schemas/otimizar-condutor.schema.ts` ou schema novo compatível
- `sistema-de-instala-es-el-tricas-sie-main/src/routes/api/v1/otimizar-condutor.ts` ou rota nova de aplicação
- `sistema-de-instala-es-el-tricas-sie-main/src/lib/api-client.ts`
- entrypoint em `bin/` definido por `@architect`

### Persistência

- `sistema-de-instala-es-el-tricas-sie-main/src/infra/repositorios/repositorio-resultado-dimensionamento-condutores.ts`
- `sistema-de-instala-es-el-tricas-sie-main/src/infra/supabase/repo-resultado-dimensionamento-condutores.supabase.ts`
- migration aditiva posterior a `docs/supabase/0011_dimensionamento_condutores_resultado.sql`

### UI

- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/dimensionamento-condutores/DimensionamentoCondutoresResumo.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/src/routes/projetos.$projetoId_.queda-tensao.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/queda-tensao/TabelaResultadosQuedaTensao.tsx`

### Testes

- `sistema-de-instala-es-el-tricas-sie-main/tests/api/dimensionamento-condutores-flow.test.ts`
- `sistema-de-instala-es-el-tricas-sie-main/tests/api/queda-tensao-endpoints.test.ts`
- `sistema-de-instala-es-el-tricas-sie-main/tests/ui/queda-tensao.vrt.test.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/src/components/app/dimensionamento-condutores/DimensionamentoCondutoresResumo.test.tsx`
- `sistema-de-instala-es-el-tricas-sie-main/src/infra/supabase/__tests__/repo-resultado-dimensionamento-condutores.test.ts`
- novos testes do caso de uso headless e de concorrência real

## 16. Riscos e mitigação

| Risco                                       | Probabilidade | Impacto | Mitigação obrigatória                                                |
| ------------------------------------------- | ------------- | ------- | -------------------------------------------------------------------- |
| Seção antiga usada com parâmetros novos     | Média         | Crítico | Assinatura canônica, estado obsoleto e AC4.                          |
| Perda de chave por concorrência             | Média         | Alto    | Operação atômica e AC6/AC7.                                          |
| Resultado calculado confundido com aplicado | Média         | Alto    | Vocabulário de estado e confirmação explícita.                       |
| Fallback volátil tratado como durável       | Média         | Alto    | Saída tipada e AC9.                                                  |
| Lote aplicado sem consentimento inequívoco  | Média         | Alto    | Decisão `@po`/`@ux` na Fase 0.                                       |
| Circuito removido ressuscitar valor antigo  | Baixa         | Alto    | Invalidação e AC10.                                                  |
| RLS permitir alteração indevida             | Média         | Alto    | Revisão `@data-engineer`, validação de pertencimento e risco aceito. |
| Expansão da story em revisão                | Alta          | Médio   | Nova story sucessora antes do desenvolvimento.                       |
| Regressão de contrato/fórmula               | Baixa         | Crítico | AC12 e verificação por símbolo.                                      |

## 17. Fora de escopo

- alterar fórmulas C1–C6 ou fórmulas de queda de tensão;
- inventar seção para circuito sem resultado real;
- remover a edição manual auditada do MOD-QT;
- usar `localStorage` como fonte compartilhada;
- criar histórico completo de todas as iterações da Auto-otimização;
- resolver toda a autenticação/autorização do produto, sem deixar de registrar e controlar o risco de RLS;
- alterar contratos públicos protegidos do MOD-QT.

## 18. Definition of Done

- [ ] Nova story criada e validada, sem ampliar `MOD-QT-2-06`.
- [ ] Decisão arquitetural de concorrência registrada por `@architect`/`@data-engineer`.
- [ ] Semântica de confirmação em lote aprovada por `@po`/`@ux`.
- [ ] Caso de uso headless funciona antes da UI.
- [ ] Assinatura canônica e ciclo `VIGENTE`/`OBSOLETA` implementados.
- [ ] Aplicação individual e em lote usam o mesmo caminho de gravação.
- [ ] Persistência é atômica, idempotente e resistente a concorrência.
- [ ] UI diferencia calculado, aplicado, durável, volátil e falhou.
- [ ] MOD-QT usa apenas seção automática vigente.
- [ ] Override manual prevalece e sua remoção revela a automática vigente.
- [ ] Migration aditiva, rollback e RLS foram validados.
- [ ] AC1–AC12 possuem testes automatizados rastreáveis.
- [ ] Contratos protegidos e fórmulas permanecem intactos.
- [ ] `npm run lint`, `npm run typecheck`, `npm test` e `npm run build` passam.
- [ ] Checklist, File List, Dev Agent Record e QA Results da nova story estão atualizados.

## 19. Decisão de prontidão

O plano v2 resolve as preocupações funcionais e de qualidade identificadas por Quinn, mas permanece **condicionado** a três decisões antes do desenvolvimento:

1. estratégia persistente/atômica aprovada por `@architect` e `@data-engineer`;
2. semântica de confirmação do lote aprovada por `@po`/`@ux`;
3. criação e validação da nova story sucessora por `@sm`/`@po`.

Após essas decisões, o fluxo pode seguir para implementação com rastreabilidade, operação headless e proteção contra seção obsoleta ou perda concorrente.
