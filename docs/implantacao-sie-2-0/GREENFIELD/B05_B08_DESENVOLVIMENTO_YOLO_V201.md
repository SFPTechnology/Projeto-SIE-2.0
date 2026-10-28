# B05–B08 — execução de desenvolvimento V2.0.1 (28/10/2026)

**Projeto:** SIE 2.0, `SFPTechnology/Projeto-SIE-2.0`, branch `feat/v201-bloco-b-auth-api`. **Escopo:** somente desenvolvimento, sem deploy, merge, escrita em Supabase, serviço pago ou alteração de SIE 1.0/F12.

## B05 — cadastro e alterações no simulador DEV
- Persistência em `v201_dev_store.py` com transações SQLite reais, projeção sobre GF02 por projeto/revisão.
- Criação de ambientes, cargas, circuitos, vínculos e bundles atômicos; clonagem com remapeamento de todos os UUIDs e FKs.
- Edição `PATCH` e exclusão `DELETE` de entidades somente em revisão `DRAFT`; `expected_revision_lock_version` obrigatório, CAS atômico e resposta 409 em obsolescência. Campos `project_id/revision_id/id/owner` não são alteráveis. FKs bloqueiam exclusão com dependências; excluir vínculos primeiro.
- Controle de precisão decimal, perímetro excluído, carga e tensão; rejeitar `NaN`, IDs externos, vínculos cruzados e duplicidades; rollback sem gravações parciais.
- **Limitação técnica:** apenas rota `/api/v2/sie/dev` em localhost, `SIE_ENV` dev/test, `SIE_V201_DEV_WRITES=1` e SQLite absoluto. Nenhum PUT/DELETE remoto.

## Adaptador PostgreSQL: preparação
- `v201_postgres_contract.py` implementa preflight read-only de migrations `GF02/A03/A04`, colunas A04, destino fixo e leitura parametrizada por owner. Bloqueia alterações remotas.
- **Não é o adaptador de escrita definitivo:** implementação real requer migrations A03/A04 aplicadas após autorização de DDL, usuário/canal backend seguros, read-back, testes SQL integrados e decisão de ativação. `service_role` não deve chegar ao browser.
- SQLite não pode ser usado como comprovação de comportamento/ACL de PostgreSQL.

## B06 — serviço interno e trilha auditável DEV
- `v201_dev_audit.py`: eventos automáticos de INSERT/UPDATE/DELETE sobre entidades de projeto/revisão, dentro da transação original, com campos mínimos, hash SHA-256 e bloqueio de UPDATE/DELETE na trilha.
- `v201_dev_server_writer.py`: gravação Python **não exposta como rota HTTP** de cálculo e artefato, vinculada a revisão `SEALED`, com hash de entrada, output JSON finito, status normativo `NOT_EVALUATED`, idempotência e relação com execução.
- Eventos `calculation.created`/`artifact.created` gravados na mesma transação; owner sempre verificado. A trilha SQLite é **detector de corrupção, não antiviolação por administrador do sistema de arquivos**. O writer remoto ainda deve ser implementado.

## B07 — hardening de desenvolvimento
- CORS de origens locais explícitas, incluindo PATCH/DELETE; sem wildcard.
- Exigir Content-Length para POST/PATCH/PUT V2, limite de 256 KiB; em `/dev`, rate limit local (padrão 600 chamadas de escrita por IP/60 s, configurável) com 429/Retry-After.
- Cabeçalhos `Cache-Control: no-store`, `X-Content-Type-Options: nosniff` e `X-Request-ID` gerado pelo servidor. Sem gravar Authorization, tokens ou segredo em trilhas.
- Middleware de limite é apenas DEV; uso distribuído/produção exigirá rate limiter centralizado, revisão de proxy confiável e segurança adicional.

## B08 — teste integrado DEV
- `test_b08_dev_journey_v201.py`: usuário A cria um projeto, revisão, **2 ambientes, 3 cargas, 2 circuitos, 3 vínculos**, sela, gera run/artefato internos, confere audit e reabre a base. Usuário B tenta listar, editar, consultar snapshots e eventos de A e é rejeitado.
- Também há testes específicos de reenvio idempotente, concorrência, recuperação após falha, CAS de revisão, logs append-only, CORS e rate limit.
- **Limitação:** clientes A/B são fixtures do TestClient. Não houve signin real, Data API real, restore PG, aprovação normativa ou deploy.

## Evidências e gate
Os resultados verificáveis são os checks do GitHub Actions do SHA final da PR #10; nenhuma execução de SHA intermediário substitui o HEAD. Antes de concluir GB, anexar resultado API+AIOX+Chromium e revisar blockers remotos/UX completos.

**Sem autorização de produção:** GF02 é única migration aplicada em `fozrymsidnaxmuvxxfhh`; A03/A04 continuam PENDING. PR #10 permanece DRAFT.
