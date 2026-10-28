# Checkpoint — B04/B05 PostgreSQL 17 e B01 navegador — SIE V2.0.1

**Ramo:** `feat/v201-bloco-b-auth-api` • **PR:** #10 (rascunho) • **Data:** 28/10/2026

## Implementado no código

### Adaptador PG17 exclusivamente descartável
Arquivo `restructuring/apps/api/sie_api/v201_pg_dev_adapter.py`, invocado por conexão externa já aberta pelo CI, com os controles cumulativos:
- `GITHUB_ACTIONS=true` e `SIE_PG17_DISPOSABLE_TEST=1`;
- host `localhost/127.0.0.1/::1` ou socket local e banco `sie2_gf02_ci`/`sie2_gf02_second`;
- PostgreSQL com IP de serviço loopback ou privado Docker;
- `read_only_preflight` valida GF02+A03+A04 e colunas da revisão, incluindo retorno de migrations registradas;
- nenhum DSN, segredo Supabase ou configurador de conexão remota no módulo.

Operações transacionais implementadas e testadas: criação de projeto de titular conhecido (ainda **sem idempotência de projeto**), criação de revisão idempotente, clone com remapeamento das quatro tabelas, criação de lote com rollback, transição CAS/selagem e edição/exclusão granular apenas em `DRAFT` com incremento de `lock_version`, rejeição de FKs e conflitos. Conexões SQL são injetadas e parametrizadas. Escopos por proprietário são verificados antes de ações privilegiadas.

**Importante:** esse adaptador é uma **prova operacional de implementação PostgreSQL**, não um driver seguro para ser habilitado no Supabase remoto. A GF02 não contém chave de idempotência persistente para a criação de projeto; o contrato completo ainda exigirá migration aditiva ou outra solução governada. `service_role` em GF02 possui grants de DELETE insuficientes para alguns fluxos; o teste usa `postgres` no banco descartável. Não promover seu papel ou privilégios a produção sem análise e aprovação separadas.

### Prova CI PostgreSQL
- `.github/workflows/sie-b04-b05-pg17.yml`: monta serviço PostgreSQL 17 descartável no GitHub Actions, instala GF02+A03+A04 no banco `sie2_gf02_ci`, cria **histórico de migrations apenas sintético nesse banco** e roda a suíte `test_b04_b05_pg17_disposable_v201.py` usando `psycopg[binary]`.
- Cobertura de identidade A/B sintética, isolamento owner, revisão, idempotência, clone e FKs, alterações com CAS, rollback, falha em revisão selada e rejeição de conexões remotas. **Não é ensaio no Supabase**.

### Login de navegador DEV
- `restructuring/apps/web/auth-v201.html`: interface escura acessível, isolada, não incluída na navegação de produção.
- `auth-v201.js`: autenticação de e-mail/senha pela API Auth do projeto configurado, com confirmação posterior em `/api/v2/sie/auth/me`, logout local, evento de encerramento entre guias e recuperação de conta sujeita à allowlist de redirects.
- `auth-v201.public-config.js`: arquivo com **chave pública em branco**, sem segredo. Somente localhost:5173 e API loopback:8000 são autorizados. JWT em memória volátil; o carregamento da página perde a sessão. Não executa criação de usuários nem writes no Supabase.
- `test_b01_browser_auth_contract_v201.py` e `restructuring/e2e/test_b01_auth_v201_browser.py`: verificações estáticas e Chromium com Auth API simulada. **Testar a própria integração Auth real requer usuário autorizado e redirects configurados; ainda pendente.** O callback de recuperação e persistência/refresh de sessão de produto continuam pendentes. Não é pronto para produção.

## Gate e riscos restantes
- **GA PASS exclusivamente DEV** da revisão V2.0.1 não autoriza migrations remotas.
- **GB BLOCKED para integração/produção**, mesmo que os testes de desenvolvimento estejam aprovados.
- Migrações A03/A04 e eventuais B04 continuam `PENDING` para o projeto remoto.
- Antes de E06 GO: Auth A/B real, RLS real por sessão, backup/rollback, concessões de privilégios mínimas, idempotência persistente de projetos, escrita B04/B05 no backend remoto, callbacks e renovação de sessão, testes de segurança e aprovação técnica profissional.

**Proibição operacional:** sem push de migrations, merge, deploy, reconfiguração de Auth, criação de usuários ou contratação Supabase. Preservar `main`, F12, SIE original e GF02.
