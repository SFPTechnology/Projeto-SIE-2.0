# Parecer de Dados da Fase 0 — Auto-otimização MOD-DC → S (mm²) no MOD-QT

**Decisão:** DATA-AUTO-OTI-1.3  
**Data:** 2026-08-02  
**Autoridade:** `@data-engineer` (Dara)  
**Status:** **APROVADO COM CONDIÇÕES DE GATE**  
**Escopo:** modelo persistente, migration, legado, atomicidade, idempotência, concorrência, rollback, índices, locks, RLS e pertencimento  
**Não executado neste parecer:** criação/aplicação de migration, alteração de código ou operação em banco

## 1. Fontes e evidências inspecionadas

Este parecer deriva exclusivamente de:

- `.aiox-core/constitution.md`;
- `docs/workflows/WORKFLOW-SDC-AUTO-OTIMIZACAO-S-QUEDA-TENSAO-YOLO.md`;
- `docs/PLANO-REESTRUTURACAO-AUTO-OTIMIZACAO-S-QUEDA-TENSAO.md`;
- `docs/stories/story-AUTO-OTI-1.2.md` e `docs/stories/story-MOD-QT-2-06-persistencia-secao-mod-dc.md` como predecessoras;
- `sistema-de-instala-es-el-tricas-sie-main/docs/supabase/0001_init.sql`;
- `sistema-de-instala-es-el-tricas-sie-main/docs/supabase/0010_dimensionamento_condutores_overrides.sql`;
- `sistema-de-instala-es-el-tricas-sie-main/docs/supabase/0011_dimensionamento_condutores_resultado.sql`;
- `sistema-de-instala-es-el-tricas-sie-main/docs/supabase/0012_queda_tensao_config.sql`;
- `sistema-de-instala-es-el-tricas-sie-main/src/infra/repositorios/repositorio-resultado-dimensionamento-condutores.ts`;
- `sistema-de-instala-es-el-tricas-sie-main/src/infra/supabase/repo-resultado-dimensionamento-condutores.supabase.ts` e seus testes;
- repositórios Supabase de projetos, overrides do MOD-DC e configuração do MOD-QT;
- `sistema-de-instala-es-el-tricas-sie-main/src/infra/supabase/client.ts`;
- `sistema-de-instala-es-el-tricas-sie-main/docs/supabase/SCHEMA.md` e `DB-AUDIT.md`.

Constatações do brownfield:

1. A `0011` possui uma linha por projeto e um mapa JSONB `circuito_id -> number`.
2. `salvarMuitos` lê o documento atual, faz merge no cliente e executa `upsert` do JSONB inteiro. Duas sessões podem sobrescrever atualizações uma da outra.
3. O registro legado não contém assinatura, origem, estado, versão ou `operacaoId`.
4. O fallback em memória usado quando a tabela não existe permite leitura na mesma sessão e devolve um registro indistinguível de uma gravação durável no contrato atual.
5. A `0011` habilita RLS, mas possui policies `FOR ALL` com `USING (true)` e `WITH CHECK (true)` para `anon` e `authenticated`.
6. O repositório da `0011` usa `supabaseBrowser()` com chave `anon`; portanto, o acesso permissivo é efetivamente utilizado pelo caminho SPA atual.
7. Não existe tabela persistente de circuitos. `Circuito` é um objeto derivado do projeto/dependências; logo, o banco não dispõe hoje de uma FK válida para `circuito_id`.
8. Já existe `0012`; por isso a migration aditiva seguinte na sequência documental deve ser `0013`, embora o requisito mínimo seja ser posterior à `0011`.
9. Há duas trilhas de migrations no repositório (`docs/supabase/` e `supabase/migrations/`) e a trilha timestamped não contém equivalente visível da `0011`. O apply deve ser bloqueado até a fonte canônica e o histórico aplicado serem reconciliados.

## 2. Decisão principal

Adotar a estratégia recomendada pelo plano: **uma linha normalizada por `(projeto_id, circuito_id)`**, acompanhada por um **registro de operação por `(projeto_id, operacao_id)`** e uma **RPC transacional** para aplicação/invalidação do lote.

O merge JSONB no cliente fica rejeitado para o novo fluxo porque não satisfaz AC6/AC7 sem introduzir uma função de merge e um protocolo de versão igualmente complexos, mantém contenção no documento inteiro do projeto e dificulta constraints e consultas por estado.

### 2.1 Tabela de estado atual por circuito

Nome recomendado: `public.dimensionamento_condutores_secao_automatica`.

| Campo | Regra |
|---|---|
| `projeto_id` | `text NOT NULL`, FK para `public.projetos(id) ON DELETE CASCADE` |
| `circuito_id` | `text NOT NULL`; chave estável do circuito, nunca nome/descrição |
| `secao_fase_mm2` | `numeric` positivo e finito; obrigatório para estado `VIGENTE` |
| `origem` | somente `DIMENSIONAMENTO_LOTE` ou `AUTO_OTIMIZACAO` |
| `assinatura_entrada` | `text`; obrigatória para estado `VIGENTE`, nula apenas no legado obsoleto |
| `assinatura_versao` | versão do contrato canônico da assinatura, inicialmente `1` |
| `estado` | somente `VIGENTE` ou `OBSOLETA` |
| `versao` | inteiro positivo, incrementado em toda mudança efetiva da linha |
| `ultima_operacao_id` | operação que produziu a versão atual; obrigatória para nova escrita vigente |
| `atualizado_em` | timestamp do banco, não confiado ao relógio do cliente |
| `criado_em` | timestamp do banco |

Chave primária lógica e física: `(projeto_id, circuito_id)`. Essa chave isola projetos mesmo quando IDs de circuito coincidirem e suporta a leitura por projeto/circuito sem JSONB.

Constraints obrigatórias:

- seção maior que zero e sem valores especiais (`NaN`, `Infinity`, `-Infinity`);
- `versao >= 1`;
- `VIGENTE` exige seção, assinatura e operação não nulas;
- `OBSOLETA` nunca é elegível para consumo pelo MOD-QT;
- `circuito_id`, assinatura e `operacaoId` não podem ser vazios após `trim`.

Não será criado histórico completo de iterações; a tabela representa somente o estado corrente exigido pelo plano. A versão e o recibo da operação fornecem rastreabilidade operacional mínima sem ampliar o escopo para event sourcing.

### 2.2 Tabela de idempotência da operação

Nome recomendado: `public.dimensionamento_condutores_aplicacao_operacao`.

| Campo | Regra |
|---|---|
| `projeto_id` | FK para `projetos(id) ON DELETE CASCADE` |
| `operacao_id` | chave idempotente fornecida ao caso de uso |
| `requisicao_hash` | hash canônico do projeto, itens, ações, assinaturas e versões esperadas |
| `resultado` | resposta tipada serializada: aplicados, ignorados, conflitos, falhas e persistência |
| `concluido_em` | timestamp do banco |

Chave primária: `(projeto_id, operacao_id)`.

Uma repetição com mesmo `operacaoId` e mesmo `requisicao_hash` retorna o recibo já confirmado, sem duplicar efeitos. O mesmo `operacaoId` com hash diferente retorna conflito determinístico e não grava seções.

## 3. Operação de lote atômica

O único caminho durável de escrita deve ser uma função PostgreSQL/RPC, com nome final alinhado à decisão arquitetural, executada em uma única transação. A função deve receber o projeto, o `operacaoId`, o hash canônico e os itens já recalculados/validados pelo caso de uso.

Cada item interno deve conter, no mínimo:

- `circuitoId`;
- ação `APLICAR` ou `OBSOLETAR`;
- seção aprovada quando a ação for `APLICAR`;
- origem;
- assinatura canônica e sua versão;
- `versaoEsperada`, usando `0` para ausência previamente observada.

`versaoEsperada` é metadado interno capturado pelo caso de uso/repositório no snapshot feito após validar projeto e circuitos. Ela não integra a autoridade do cliente/UI e não deve ser aceita do payload público como verdade concorrencial.

Sequência transacional aprovada:

1. validar forma, duplicidade de `circuitoId`, valores e existência do projeto;
2. reservar `(projeto_id, operacao_id)` na tabela de operações;
3. em colisão, comparar `requisicao_hash` e devolver o recibo anterior ou conflito de reutilização;
4. bloquear as linhas alvo em ordem lexical de `circuito_id`;
5. comparar todas as versões esperadas antes de qualquer alteração;
6. se houver conflito em um item, não alterar nenhum item do lote e persistir/devolver a resposta de conflito da operação;
7. se não houver conflito, inserir/atualizar/invalidar todas as linhas;
8. persistir o recibo final `DURAVEL` na mesma transação e retornar a resposta.

Qualquer erro não tratado aborta a transação inteira. Não há estado `DURAVEL` sem commit do recibo e de todas as linhas. O fallback volátil pode existir apenas em adaptador de desenvolvimento/teste e deve retornar `VOLATIL`; ele não pode implementar a interface como se tivesse persistido.

## 4. Versionamento, conflito e idempotência

- A versão pertence à linha `(projeto_id, circuito_id)`, não ao projeto inteiro.
- Inserção exige `versaoEsperada = 0` e ausência da linha.
- Atualização ou invalidação exige igualdade entre `versaoEsperada` e a versão armazenada.
- Alteração efetiva incrementa `versao` exatamente uma vez.
- Retry da mesma operação não incrementa versão, mesmo após timeout do cliente, porque o recibo é a autoridade da idempotência.
- Uma nova tentativa após conflito usa novo `operacaoId`, novas versões esperadas e novo hash.
- Duas operações no mesmo circuito nunca são confirmadas silenciosamente com a mesma versão esperada.
- Falha transitória antes do commit não altera recibo nem seção. Falha do cliente após o commit é resolvida consultando/repetindo o mesmo `operacaoId`.

A assinatura de entrada identifica compatibilidade técnica; a versão identifica concorrência. Uma não substitui a outra.

## 5. Concorrência

### 5.1 Circuitos diferentes do mesmo projeto

As operações bloqueiam apenas as linhas dos circuitos afetados. Não existe leitura e sobrescrita de um documento JSONB do projeto. Assim, transações concorrentes em circuitos distintos podem concluir sem perda de chave, satisfazendo AC6.

### 5.2 Mesmo circuito

O lock de linha, combinado com `versaoEsperada`, serializa a decisão. A primeira transação válida incrementa a versão; a segunda observa divergência e retorna conflito, sem sobrescrever silenciosamente, satisfazendo AC7.

Para duas inserções concorrentes da mesma chave ainda inexistente, a PK composta arbitra a criação; após a espera, a perdedora reavalia a versão e retorna conflito. A implementação da RPC deve converter `unique_violation` esperada nesse resultado tipado, não em sucesso.

### 5.3 Lotes sobrepostos

As linhas devem ser bloqueadas em ordem estável de `(projeto_id, circuito_id)` para reduzir risco de deadlock. Um conflito em qualquer item invalida o lote inteiro. Retentativa automática por deadlock/erro transitório é permitida no máximo conforme o workflow e somente com o mesmo `operacaoId`.

## 6. Legado da `0011` sem assinatura

A `0011` não deve ser editada. A migration aditiva recomendada deve:

1. criar os novos objetos;
2. ler `dimensionamento_condutores_resultado.secoes` com `jsonb_each`;
3. importar somente pares estruturalmente válidos como linhas `OBSOLETA`, com `assinatura_entrada = NULL` e sem elegibilidade para o MOD-QT;
4. ignorar e contabilizar valores inválidos para relatório de migration;
5. usar `ON CONFLICT DO NOTHING` para permitir reapply em ambiente isolado sem sobrescrever linha já revalidada.

Nenhum valor legado será promovido automaticamente a `VIGENTE`. A promoção só ocorre por recálculo real e aplicação explícita pelo caso de uso headless, que gera a assinatura no domínio/aplicação. Dados de `localStorage` não participam do backfill.

Compatibilidade de transição:

- aplicar a migration não muda a tabela `0011`, portanto o binário antigo continua operando durante a etapa de schema-first;
- o binário novo lê exclusivamente a nova tabela para decidir vigência; legado importado aparece como obsoleto/revalidar e produz `PEND` quando não houver fonte superior;
- o binário novo grava somente pelo novo caminho transacional; dual-write para o JSONB legado fica proibido porque recriaria ambiguidade e perda de atualização;
- a ativação do novo consumidor deve ocorrer somente depois da migration confirmada. Ausência dos novos objetos retorna `FALHOU`, nunca sucesso volátil em produção.

## 7. Migration aditiva, locks e índices

Nome documental recomendado: `docs/supabase/0013_dimensionamento_condutores_secao_automatica.sql`. Se a trilha canônica escolhida for `supabase/migrations/`, deve existir um único arquivo timestamped correspondente e a sequência aplicada deve registrar a `0011`; não se devem manter duas migrations executáveis divergentes para a mesma mudança.

Objetos previstos na migration:

- as duas tabelas descritas neste parecer;
- PKs, FK para projetos, CHECKs e comentários;
- função RPC transacional;
- grants/revokes e RLS;
- backfill legado como `OBSOLETA`;
- notificação de reload do schema PostgREST se esse for o mecanismo já adotado no ambiente.

Índices:

- a PK `(projeto_id, circuito_id)` cobre leitura pontual e listagem por prefixo de projeto;
- um índice parcial em `(projeto_id, circuito_id) WHERE estado = 'VIGENTE'` pode ser criado para o hot path do MOD-QT e deve ser validado com `EXPLAIN`; não criar índice redundante apenas em `projeto_id` sem evidência;
- a PK `(projeto_id, operacao_id)` cobre idempotência e consulta de recibo;
- índices de retenção/tempo em operações ficam fora desta story até existir consulta ou política de purge que os justifique.

Impacto de locks:

- `CREATE TABLE`, constraints e índices em tabelas novas não reescrevem nem bloqueiam a `0011` para DML;
- o backfill mantém `ACCESS SHARE` na `0011` e escreve somente na tabela nova;
- não executar `ALTER` destrutivo, conversão de coluna ou update do JSONB legado;
- medir contagem/tamanho da `0011` antes do apply e definir timeout operacional. Em volume alto, separar o backfill em etapa idempotente controlada, sem promover registros;
- a RPC usa locks de linha somente nos circuitos do lote e deve rejeitar lotes com IDs duplicados.

## 8. RLS e pertencimento projeto/circuito

### 8.1 Novos objetos

A decisão aprovada é **server-only** para o caminho durável:

- `ENABLE ROW LEVEL SECURITY` nos novos objetos;
- nenhuma policy permissiva para `anon` ou `authenticated`;
- `REVOKE` explícito de acesso direto desses papéis;
- DML e execução da RPC somente para `service_role` pelo adaptador CLI/API;
- função RPC como `SECURITY INVOKER`, `search_path` controlado e sem SQL dinâmico;
- a UI chama o caso de uso pela API e não usa `supabaseBrowser()` para gravar a nova fonte.

Esse desenho é mais restritivo que a `0011` e evita ampliar silenciosamente o risco. A chave `service_role` permanece exclusivamente no servidor.

### 8.2 Validação de pertencimento

O banco garante que `projeto_id` existe e separa identidades iguais de circuito pela PK composta. Entretanto, como não há tabela canônica de circuitos, não é possível criar FK de `circuito_id` nem uma policy RLS que prove pertencimento do circuito.

O caso de uso headless deve, antes da RPC:

1. carregar o projeto real;
2. derivar seus circuitos pelo fluxo canônico existente;
3. localizar cada `circuitoId` dentro desse conjunto;
4. rejeitar circuito inexistente ou pertencente a outro projeto;
5. recalcular/validar o resultado aprovado e gerar a assinatura;
6. enviar à RPC somente os itens validados.

A RPC repete as validações que o banco consegue impor: existência do projeto, não duplicidade, valores, versões e escopo de todas as chaves pelo mesmo `projeto_id`. A ausência de FK de circuito é risco estrutural conhecido, mitigado pelo serviço e por testes negativos cross-project; criar uma tabela de circuitos apenas para resolver essa FK está fora do plano e não foi inventado neste parecer.

### 8.3 Policy permissiva legada

As policies abertas da `0011` são dívida preexistente e não serão copiadas para os novos objetos. Durante a janela schema-first, mantê-las evita quebrar o binário antigo, mas preserva acesso irrestrito à fonte legada.

Antes do rollout final, uma das seguintes condições deve estar documentada:

1. retirada das policies/grants legados depois que nenhum cliente depender da `0011`; ou
2. waiver formal com risco, autoridade responsável, prazo de expiração e evidência de monitoramento.

Sem retirada ou waiver, o gate `RLS_OR_OWNERSHIP_FAILED` permanece bloqueante. O parecer não atribui silenciosamente responsável ou prazo inexistentes nos artefatos.

## 9. Rollback e reversibilidade

O rollback técnico deve ser entregue em script separado e testado em ambiente isolado na sequência `apply → validar → rollback → reapply`.

Ordem de rollback:

1. desabilitar o novo caso de uso/consumidor e confirmar que nenhuma instância grava nos novos objetos;
2. exportar/snapshotar tabelas novas e recibos de operação;
3. revogar execução da RPC;
4. remover a função;
5. remover primeiro a tabela de operações e depois a tabela por circuito;
6. manter a `0011` intacta.

Como o backfill é somente leitura da `0011`, o reapply reconstrói novamente os legados como `OBSOLETA`. Dados novos não devem ser copiados de volta automaticamente ao JSONB da `0011`, pois isso descartaria assinatura/versão e poderia apresentá-los como vigentes. Rollback de aplicação deve sinalizar a funcionalidade como indisponível; não pode declarar dados legados sem assinatura como atuais.

Em produção, `DROP` só ocorre com autorização de migration destrutiva e snapshot confirmado. Na ausência dessa autorização, o rollback seguro é de aplicação/feature flag, mantendo as tabelas novas inativas para investigação.

## 10. Gates obrigatórios para implementação e rollout

O status **APROVADO COM CONDIÇÕES** autoriza a story a incorporar esta decisão, mas não autoriza apply. A Fase 2/Fase 6 deve bloquear se faltar qualquer evidência abaixo:

- [ ] migration canônica posterior à `0011` e histórico de migrations reconciliado;
- [ ] migration e rollback idempotentes em ambiente isolado;
- [ ] backfill legado gera apenas `OBSOLETA`, nunca `VIGENTE`;
- [ ] RPC confirma lote inteiro ou nenhum item;
- [ ] retry do mesmo `operacaoId`/hash não altera versões e devolve o mesmo recibo;
- [ ] reutilização de `operacaoId` com hash diferente retorna conflito;
- [ ] concorrência real em circuitos diferentes preserva ambos;
- [ ] concorrência real no mesmo circuito detecta versão divergente;
- [ ] lotes sobrepostos não deixam efeito parcial e não entram em deadlock não tratado;
- [ ] leitura do MOD-QT filtra `VIGENTE` e assinatura compatível;
- [ ] tabela/RPC ausente ou banco indisponível retorna `FALHOU` em produção;
- [ ] fallback de teste retorna explicitamente `VOLATIL` e não gera estado Aplicado;
- [ ] tentativas com circuito inexistente e cross-project são rejeitadas;
- [ ] RLS possui testes positivos via servidor e negativos para `anon`/`authenticated`;
- [ ] policies abertas da `0011` foram retiradas ou possuem waiver formal válido;
- [ ] plano de lock, timeout, snapshot e observabilidade foi anexado ao runbook;
- [ ] apply remoto ocorre somente com `migrations_authorized: true` e por autoridade autorizada.

## 11. Resultado da decisão

| Tema | Decisão |
|---|---|
| Modelo | Linha por `(projeto_id, circuito_id)` |
| Persistência legada | `0011` preservada; backfill somente `OBSOLETA` |
| Lote | RPC única e transacional |
| Idempotência | recibo único por `(projeto_id, operacao_id)` + hash canônico |
| Concorrência | versão esperada por circuito + locks em ordem determinística |
| Leitura MOD-QT | somente `VIGENTE` com assinatura compatível |
| Fallback | nunca durável; permitido apenas como `VOLATIL` em dev/teste |
| RLS nova | server-only, deny-by-default para `anon`/`authenticated` |
| Pertencimento | FK de projeto + validação canônica de circuitos no caso de uso |
| Migration | aditiva, recomendada como `0013`, sem editar a `0011` |
| Rollback | app/feature primeiro; schema somente autorizado e com snapshot |

**Parecer final:** a estratégia de dados está suficientemente definida para a story sucessora prosseguir à consolidação da Fase 0. A implementação e qualquer rollout permanecem condicionados aos gates acima, em especial reconciliação da trilha de migrations, evidência de concorrência real e resolução formal da policy permissiva legada.

— Dara, arquitetando dados
