# A04 — ADR de revisões e lifecycle (somente desenvolvimento)

**Estado:** decisão arquitetural proposta para implementação, sem mudança em PostgreSQL.
**Dependência:** A02. **Consumo futuro:** B04, mediante API transacional e migration aprovada.

## Máquina de estados
- Estados **internos da revisão**: `DRAFT`, `SEALED`, `SUPERSEDED`.
- Transições admitidas: `DRAFT -> SEALED` (snapshot/hash imutáveis válidos) e `SEALED -> SUPERSEDED` (nova revisão selada).
- Transições negadas: `SEALED -> DRAFT`, `SUPERSEDED -> DRAFT`, edição de revisão selada, aprovação implícita ao selar.
- `CALCULATED`, `REVIEW_REQUIRED`, `APPROVED`, `PUBLISHED`, `STALE` descrevem **resultados/artefatos/parecer externo**, não substituem estados internos de revisão.
- `APPROVED` exige evidência e autoridade profissional competente; nenhuma UI pode promovê-lo diretamente.

## Contrato de escrita futura
- Revisão inicial: `DRAFT` com numeração atômica por projeto e autor autenticado.
- Novo rascunho: clone copy-on-write do snapshot selado anterior, associado a `base_revision_id`.
- `version` é inteiro lógico por projeto; `lock_version` controla concorrência otimista; conflito devolve `409` sem perda silenciosa.
- `idempotency_key` única no escopo do projeto/titular: repetição devolve resultado prévio, nunca cria nova revisão adicional.
- Ao selar, registrar hash SHA-256 de JSON canônico e versão de motor, regra e template. Timestamp e autor registrados separadamente; não incluí-los no hash sem especificação.
- Após selagem, mutações no snapshot (incluindo rooms, loads, circuits, links) são proibidas; editar requer clone.
- Mudança do projeto/revisão deve sinalizar cálculos e artefatos dependentes como `STALE`, sem apagar evidências anteriores.

## Divergência real do banco
GF02 possui `sie_project_revisions(version,source_sha256)` e FKs, mas **NÃO** possui colunas `lifecycle_state`, `base_revision_id`, `lock_version`, `idempotency_key` nem gatilhos completos de imutabilidade. A migration `restructuring/supabase/migrations/20261028102100_sie_a04_revision_lifecycle_v201.sql` agora implementa as colunas, checks, FK da base, índice de idempotência, bloqueios das quatro tabelas filhas, snapshot/hash e transições no banco. Está `PENDING` no manifesto e só foi executada em PostgreSQL 17 descartável na CI, não no Supabase remoto. Antes de B04 operacional, aplicar de forma autorizada e verificar por read-back.

## Segurança
Criação/versionamento final por backend confiável, com verificação `auth.uid()`/ownership, constraint e transação; `service_role` nunca no browser. Políticas atuais de GF02 são mantidas enquanto a migration adicional não for aprovada.

## Testes necessários
Fluxos unitários e de contratos podem usar fixtures; concorrência e imutabilidade reais em banco devem ser demonstradas antes de ativar edição persistente para usuários.

## Controle transacional CAS (implementado na migration candidata)

O backend deverá chamar `sie_a04_transition_revision(project_id,revision_id,expected_lock_version,target_state)` com identidade e ownership comprovados. A função é `SECURITY INVOKER` e revogada de `PUBLIC`, `anon` e `authenticated`, com `EXECUTE` apenas para `service_role` no servidor. Ela realiza UPDATE condicional por `lock_version` esperado, retornando SQLSTATE `40001` para conflito; a UI não decide nem altera o estado. Os testes PostgreSQL 17 verificam CAS obsoleto, proibição ao navegador e preservação de hash. Aplicação à produção continua sujeita a autorização específica de DDL.
