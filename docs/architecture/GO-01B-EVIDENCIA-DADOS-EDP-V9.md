# GO-01B — Proposta e Evidência Técnica de Dados EDP V9

**Produto:** SIE — Sistema de Instalações Elétricas  
**Escopo:** padrão de entrada EDP São Paulo V9  
**Autoridade do artefato:** Dara (@data-engineer)  
**Data:** 2026-07-26  
**PRD de origem:** `docs/prd/PRD-PADRAO-COMPATIVEL-EDP-V9.md`  
**ADR de origem:** `docs/architecture/ADR-EDP-V9-DP-10-CONTRATO-CANONICO.md`  
**Estado do artefato:** `PROPOSTA TÉCNICA — NÃO EXECUTADA`  
**Estado da contribuição de dados para GO-01B:** `PARCIAL`  
**Estado global de GO-01B:** `NÃO APROVADO`

## 1. Objetivo, limite de autoridade e conclusão

Este documento propõe a evolução física de dados e registra a evidência disponível para retenção, acesso/RLS, backup/restauração, snapshot, rollback semântico e migração idempotente. Ele atende ao handoff do PRD para @data-engineer sem aplicar DDL, executar migrations, acessar ambiente Supabase real, definir perfis organizacionais ou emitir parecer final de qualidade.

**Conclusão:** o desenho torna os requisitos de dados implementáveis e testáveis, mas não constitui evidência operacional. GO-01B permanece bloqueado até que políticas sejam aprovadas, migrations e testes existam em stories formais e os procedimentos sejam comprovados em ambiente autorizado.

## 2. Rastreabilidade obrigatória

| Tema | Requisitos e decisões |
|---|---|
| Decisão canônica versionada | FR20, FR27–FR30; NFR1, NFR2, NFR5, NFR7; AC-22, AC-25, AC-26, AC-32; DP-10 §§3.2, 3.5 |
| Migração não destrutiva | FR31; NFR6; CR2–CR5; AC-24, AC-33 |
| Remoção controlada | FR33; AC-35; DP-10 §§3.6, 6 |
| Autorização e auditoria | NFR13; DP-04, DP-07, GP-01; PRD §7.10 |
| Retenção e resiliência | NFR14; AC-32, AC-35; PRD §§5.5, 7.10 |
| Snapshot e rollback semântico | FR31; NFR6; AC-33; invariante do PRD §5.5 |
| Fonte oficial imutável e override separado | FR28, FR30; AC-23, AC-32; DP-10 §3.5 |

## 3. Evidência do estado atual

### 3.1 Persistência observada

- `projetos.padrao_entrada_config` armazena configuração genérica como `jsonb`, sem versão normativa e sem referência canônica imutável.
- `parametros_edp_overrides` armazena overrides separadamente, mas não possui a proveniência, o fluxo de aprovação e o histórico exigidos pelo PRD.
- `eventos_auditoria` contém referências textuais soltas, payload flexível e não demonstra, por schema, vínculo íntegro com decisão, catálogo ou snapshot.
- Não foram identificadas estruturas específicas para decisão EDP canônica, catálogo EDP versionado, snapshot semântico ou execução idempotente de migração.
- O versionamento de banco está dividido entre SQL documental em `sistema-de-instala-es-el-tricas-sie-main/docs/supabase/` e migrations em `supabase/migrations/`; não há neste snapshot evidência de aplicação uniforme em ambientes reais.

### 3.2 Acesso e RLS observados

- As tabelas do schema inicial habilitam RLS sem policies e concedem acesso a `service_role`.
- O cliente server-side usa `service_role`, que ignora RLS.
- Repositórios de projeto, auditoria e parâmetros EDP usam por padrão o cliente browser/anon.
- Migrations recentes criam policies irrestritas para `anon` e `authenticated` com `USING (true)` e `WITH CHECK (true)`.
- A migration de tabelas normativas concede `SELECT ON ALL TABLES IN SCHEMA public` para `anon` e `authenticated`, com alcance mais amplo que as tabelas criadas por ela.

**Achado bloqueante:** o modelo de acesso declarado e o efetivamente codificado não são coerentes. Não existe matriz aprovada que permita escrever policies finais. Policies permissivas universais não atendem NFR13.

### 3.3 Integridade e operação observadas

- A auditoria atual não é demonstravelmente append-only.
- Não há evidência de transação única entre decisão, evento, invalidação downstream e snapshot.
- Não há procedimento versionado e executado de backup/restauração semântica.
- Não há evidência de RPO, RTO, retenção, descarte, teste de restauração ou dry run do pacote 8.
- Há risco de drift de tipos entre migrations existentes, como referência `UUID` a uma chave de dependência documentada como `text`; isso deve ser validado em schema real antes de qualquer nova migration.

## 4. Proposta de evolução aditiva do schema

Os nomes abaixo são contratuais para o plano, não DDL aprovado. Tipos, constraints e nomes finais devem ser confirmados na story de banco após inspeção do schema real.

| Estrutura proposta | Responsabilidade mínima | Invariantes |
|---|---|---|
| `edp_catalogos_oficiais` | Manifesto central da versão oficial: distribuidora, documento, versão normativa, versão de schema, referência do artefato e hash | Imutável após publicação; identificador/hash único; nunca duplicado por projeto; não pode ser descartado enquanto referenciado |
| `edp_contextos_projeto` | Rede, topologia, tensões nomeadas, origem/autoria/confiança e versão/hash das entradas | Um contexto corrente versionado por projeto; 120/240 e 127/220 não equivalentes; 380 não válido na rota EDP |
| `edp_decisoes_canonicas` | Decisão corrente e versões anteriores: estado, categoria mínima/solicitada, subcategoria, catálogo, input hash, versão de schema e controle de concorrência | No máximo uma decisão corrente por projeto; FK ao catálogo; gravação condicionada ao mesmo catálogo/input hash da avaliação |
| `edp_overrides` | Override separado da fonte oficial, com alvo, valor, autoria, justificativa, estado e proveniência | Nunca altera catálogo oficial; nunca herda status “verificado”; ações bloqueadas até matriz de perfis aprovada |
| `edp_eventos_decisao` | Eventos append-only de seleção, confirmação, override, invalidação, migração, recálculo e rollback | Sem update/delete pelo fluxo normal; antes/depois, autoria, justificativa, correlação e catálogo/snapshot referenciados |
| `edp_snapshots_semanticos` | Snapshot pré-migração/rollback: legado original, decisão canônica anterior, catálogo, hashes, versão de schema e estado downstream | Imutável; verificável por hash; suficiente para reconstruir significado, não apenas linhas |
| `edp_execucoes_migracao` | Controle por projeto/lote: classificação, source hash, target version, snapshot, status, resultado e chave idempotente | Unicidade da operação lógica; retry retorna o mesmo resultado quando a entrada não mudou |
| `edp_invalidacoes_downstream` | Consumidor, versão afetada, motivo e estado da invalidação | Retomada bloqueada enquanto houver resultado incompatível não invalidado/recalculado |

### 4.1 Constraints e índices mínimos

- FKs de decisão, evento, snapshot e migração para `projetos` e para o catálogo oficial.
- Constraint única parcial para uma decisão corrente por projeto.
- Unicidade de `(projeto_id, operacao, source_hash, target_schema_version)` ou chave idempotente equivalente.
- Checks para estados do contrato ratificado; lacunas normativas permanecem estados explícitos, nunca valores presumidos.
- Índices para decisão corrente por projeto, eventos por projeto/ordem, catálogo por identidade normativa e migrations por status/idempotência.
- Timestamps de banco e controle otimista de versão/hash.
- `COMMENT ON` documentando significado e requisito de origem.

### 4.2 Consistência transacional

Uma operação de migração/salvamento deve ocorrer em uma única transação de banco:

1. adquirir lock lógico do projeto;
2. validar versão/hash das entradas e catálogo;
3. criar ou validar o snapshot;
4. gravar uma única decisão canônica;
5. anexar o evento;
6. registrar invalidações downstream;
7. finalizar a execução de migração.

Falha em qualquer passo aborta toda a operação. O legado nunca é atualizado. Não há dual-write.

## 5. Proposta de acesso e RLS

### 5.1 Postura segura

- `REVOKE` explícito de acesso não necessário; nenhuma policy universal `USING (true)` nas estruturas EDP.
- RLS habilitada e default-deny em todas as tabelas EDP.
- Catálogo oficial: somente leitura para consumidores aprovados; publicação restrita a um fluxo administrativo ainda não definido.
- Decisão/contexto: leitura e escrita limitadas ao escopo de projeto autorizado.
- Eventos e snapshots: leitura autorizada; inserção somente por operação transacional; sem update/delete pelo fluxo normal.
- Migração e rollback: somente por função transacional controlada, com auditoria e chave idempotente.
- Funções privilegiadas, se adotadas, devem ter owner dedicado, `search_path` fixo, nomes qualificados, `REVOKE EXECUTE FROM PUBLIC` e grants mínimos.
- `service_role` não deve ser tratado como identidade do autor; a identidade efetiva deve vir de contexto autenticado validado no servidor.

### 5.2 Decisões pendentes

| Decisão | Estado | Autoridade necessária |
|---|---|---|
| Identidades e papéis reais | `PENDENTE` | DP-04/DP-07/GP-01 — @po/@architect |
| Vínculo usuário–projeto/tenant | `PENDENTE` | @po/@architect |
| Quem publica catálogo oficial | `PENDENTE` | @po/@architect e responsável técnico, conforme governança |
| Quem solicita/confirma/override/migra/rollback | `PENDENTE` | DP-04/DP-07/GP-01 |
| Acesso de suporte e break-glass | `PENDENTE` | @devops/@architect, com política organizacional |

Até essas decisões serem aprovadas, ações privilegiadas EDP devem permanecer bloqueadas; não é seguro preencher a lacuna com policies permissivas.

## 6. Proposta de retenção e descarte

Não há base aprovada para inventar prazos. A política deve usar as classes abaixo e receber duração, responsável e base de retenção formais.

| Classe | Dados | Regra mínima derivada do PRD | Prazo |
|---|---|---|---|
| R1 — referência normativa | catálogos oficiais referenciados | Imutáveis e disponíveis enquanto qualquer decisão/relatório puder referenciá-los | `PENDENTE` |
| R2 — decisão e proveniência | decisões, contextos e overrides | Preservar reconstrução de toda decisão persistida | `PENDENTE` |
| R3 — auditoria | eventos privilegiados e de migração/rollback | Append-only; autoria, antes/depois, justificativa e resultado preservados | `PENDENTE` |
| R4 — recuperação | snapshots semânticos e manifestos de backup | Manter pelo menos até validação de rollback e durante a janela formal de recuperação | `PENDENTE` |
| R5 — operação | execuções, diagnósticos e invalidações | Retenção suficiente para incidente, reconciliação e dry run | `PENDENTE` |
| R6 — legado | configuração original | Somente leitura durante transição; remoção da rota não autoriza descarte físico | `PENDENTE` |

O descarte deve ser suspenso quando quebrar FK/referência histórica, reconstrução normativa, investigação de incidente ou obrigação formal. A ordem proposta é: verificar referências → gerar relatório de impacto → aprovar lote → backup verificável → descarte idempotente → evento de auditoria. A política de privacidade/legal e os prazos exigem aprovação externa ao @data-engineer.

## 7. Backup, restauração e prova do significado

### 7.1 Unidade mínima recuperável

O backup aceito para GO-01B precisa incluir, no mesmo ponto lógico:

- DDL/migrations e versão do schema;
- catálogo oficial e seu hash/artefato;
- projeto, contexto e decisão canônica;
- overrides separados;
- eventos append-only;
- snapshots e execuções de migração;
- invalidações/resultados downstream necessários para saber o que pode ser retomado;
- configuração legada original somente leitura.

Restaurar somente o schema ou somente `projetos.padrao_entrada_config` não preserva significado.

### 7.2 Procedimento de validação proposto

1. registrar identificador do backup, timestamp, versão de schema e hashes;
2. restaurar em ambiente isolado autorizado;
3. executar migrations até a versão registrada;
4. validar FKs, constraints, contagens e hashes;
5. reconstruir decisão e relatório histórico usando o catálogo referenciado;
6. comparar estado, categoria, topologia, tensões, subcategoria, proveniência e bloqueios;
7. confirmar que eventos posteriores permanecem auditáveis quando o rollback semântico é exercitado;
8. registrar resultado, duração e aprovadores.

**RPO, RTO, frequência, criptografia, localização, número de cópias e responsável operacional:** `PENDENTE — @devops/@architect e política do ambiente real`.

## 8. Snapshot e rollback semântico idempotente

### 8.1 Conteúdo do snapshot

O snapshot pré-migração deve armazenar: `projeto_id`, versão/hash do legado, payload legado original, decisão canônica anterior quando existir, catálogo e schema referenciados, hashes das entradas, estado downstream, autoria/correlação, timestamp e hash do próprio snapshot.

### 8.2 Algoritmo de rollback

1. localizar snapshot por ID e validar hash;
2. adquirir lock do projeto;
3. verificar se a restauração continua semanticamente segura;
4. restaurar como **nova versão canônica** o último estado comprovadamente válido;
5. se não for segura, marcar escrita canônica como bloqueada e exigir intervenção autorizada;
6. invalidar resultados downstream incompatíveis;
7. anexar evento de rollback referenciando snapshot e estado anterior/novo;
8. nunca gravar no legado nem reativar cálculo genérico EDP.

A repetição com o mesmo snapshot e sem nova entrada retorna a versão já restaurada e não cria nova decisão divergente. Eventos posteriores não são apagados.

## 9. Plano de migration idempotente

| Fase | Ação | Evidência de saída |
|---|---|---|
| M0 | Inventário somente leitura e captura do schema real | hash do schema, contagens, tipos, policies/grants e lista de projetos |
| M1 | DDL aditivo transacional | dry run, revisão de ordem, constraints e rollback estrutural |
| M2 | Classificação sem escrita | mapeável, pendente, incompatível, customizado ou sem seleção; `TRI-220-380` bloqueado |
| M3 | Snapshot por projeto | snapshot íntegro, hash e referência normativa |
| M4 | Escrita canônica única | decisão + evento + invalidações na mesma transação |
| M5 | Retry idempotente | segunda execução sem nova entrada produz zero mudança semântica |
| M6 | Reconciliação | legado intacto, decisão reconstruível, sem dual-write e sem 380 V reinterpretado |
| M7 | Rollback semântico | restauração/bloqueio seguro e eventos preservados |
| M8 | Dry run de remoção | inventário zero de dependências EDP genéricas e todos os itens GO-01B válidos |

O rollback de DDL é distinto do rollback semântico. Mudanças destrutivas e remoção física não pertencem às fases M1–M7.

## 10. Matriz de evidência GO-01B

| Evidência exigida | Estado em 2026-07-26 | Evidência disponível / bloqueio |
|---|---|---|
| Proposta de schema e consistência | `PROPOSTA PRODUZIDA` | Este documento; ainda sem DDL, story, review ou execução |
| Inventário final | `PENDENTE` | Não executado em ambiente real; consumidores ainda não migrados |
| Política de retenção/descarte | `PARCIAL` | Classes e invariantes propostas; prazos e aprovações ausentes |
| Política de acesso/RLS | `PARCIAL COM ACHADO CRÍTICO` | Default-deny proposto; perfis pendentes e policies permissivas atuais precisam remediação |
| Backup/restauração semântica | `PROCEDIMENTO PROPOSTO` | Sem backup restaurado e sem RPO/RTO aprovados |
| Snapshot pré-migração | `MODELO PROPOSTO` | Sem implementação ou evidência de integridade |
| Rollback semântico idempotente | `ALGORITMO PROPOSTO` | Sem teste repetido em ambiente autorizado |
| Migration idempotente | `PLANO PROPOSTO` | Sem migration, dry run ou segunda execução comprovada |
| GO-01A válido | `PENDENTE` | Dependência externa e bloqueante |
| Suporte/resposta a incidente | `PENDENTE` | Autoridade @devops/@architect; política inexistente no snapshot |
| Dry run do pacote 8 | `PENDENTE` | Depende de implementação, inventário e gates anteriores |
| Pareceres @devops/@architect/@qa | `PENDENTE` | @data-engineer não emite aprovação global |

## 11. Riscos e bloqueadores

| Severidade | Risco | Tratamento requerido |
|---|---|---|
| Crítica | Escrita anônima/autenticada irrestrita em tabelas recentes | Revogar policies permissivas e aprovar modelo real de identidade antes de dados EDP privilegiados |
| Crítica | `service_role` usado como bypass sem identidade/autorização comprovada | API server-side autenticada, autorização explícita e auditoria do ator real |
| Crítica | Rollback restaurar linhas sem catálogo, eventos e estado downstream | Backup/snapshot semântico e teste de reconstrução |
| Alta | Drift entre SQL documental, migrations e schema implantado | Inventário M0 e baseline único antes do DDL |
| Alta | Migração parcial criar decisão sem evento/invalidação | RPC/transação única e teste de falha |
| Alta | Catálogo referenciado ser alterado ou descartado | Imutabilidade, hash e bloqueio de descarte enquanto referenciado |
| Alta | Retry duplicar decisões/eventos | Chave idempotente, lock e unicidade |
| Alta | Tipos/FKs divergirem do ambiente real | Inspeção e dry run obrigatórios |

## 12. Parecer de @data-engineer

**Parecer:** `NO-GO DE DADOS PARA REMOÇÃO DO LEGADO`.

É possível prosseguir apenas com stories formais de implementação aditiva, revisão e testes, quando autorizadas pelos gates do PRD. Não é possível afirmar GO-01B porque a evidência existente é documental: faltam políticas aprovadas, schema físico implementado, inventário real, migrations testadas, backup restaurado, rollback repetido, dry run e pareceres das autoridades globais.

Nenhuma migration foi aplicada e nenhum dado foi alterado na produção deste artefato.

— Dara, arquitetando dados
