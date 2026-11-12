# C20 — Auditoria independente de leitura — 06/11/2026

**Escopo:** SIE 2.0 greenfield; somente leitura no Supabase de destino e GitHub. Sem consulta ou alteração no banco legado.  
**Referência de código inspecionada antes deste registro:** `c8cc2ed3a83d0295f02dcc9d2cf3bd42345bd604`.  
**Decisão de escopo:** `C08.current_delivery_scope.strategy=GREENFIELD_NO_LEGACY_IMPORT`.

## Evidências consultadas diretamente

1. **Supabase destino `fozrymsidnaxmuvxxfhh`:** `list_migrations` retornou exclusivamente `20261027195557_sie2_greenfield_foundation_owner_rls_v1`. As quatro migrations de schema `20261028102000` (A03), `20261028102100` (A04), `20261028153000` (B04) e `20261028203000` (C03) **não estão aplicadas remotamente**.
2. **SELECT agregada de leitura no destino:** `auth.users=1`, `auth.sessions=0`, `public.sie_projects=0`, `public.sie_project_revisions=0`. Isto não prova isolamento Auth A/B nem sessões reais.
3. **GitHub Actions:** no SHA `c8cc2ed3a83d0295f02dcc9d2cf3bd42345bd604`, cinco workflows concluídos com `success` em 05/11/2026: SIE modular API (run 41966589125), SIE Browser E2E Chromium (41966589127), SIE Orchestrator AIOX (41966589126), SIE A03/A04 PostgreSQL 17 isolado (41966589278) e SIE C03 PostgreSQL 17 descartável (41966589130). São evidências **de CI de desenvolvimento**, não prova de migrações remotas ou aceite profissional.
4. **Contrato C08:** `state=BLOCKED`, `remote_schema_apply_now=false`, `production_deploy_now=false`, `legacy_import_is_gc_blocker=false`. `preproduction_authorization.backup_real_state=MISSING`, `restore_real_state=MISSING`, `migration_application_permitted_now=false`.
5. **Validadores C16/C18:** verificações GREENFIELD excluem somente provas de migração legada; continuam a rejeitar liberação operacional automática sem Auth, evidência normativa, aceite C13 e recuperação do destino.

## Correção não destrutiva nesta auditoria

A descrição principal da PR #11 ainda começava com a decisão histórica de migrar os cinco projetos, em conflito com C08/C19. O texto principal da PR foi corrigido para **GREENFIELD_NO_LEGACY_IMPORT**, mantendo o histórico técnico no corpo e sem alterar `main` ou dados remotos.

## Pendências reais — ordem recomendada

1. Implementar e testar, sem tocar banco remoto, uma estratégia de recuperação **alternativa ao backup remoto C17** que seja realmente comprovável; até lá DDL remoto permanece bloqueado. Não substituir prova operacional por flags.
2. Preparar e validar fluxos Auth A/B e políticas RLS com testes negativos em ambiente isolado; realizar comprovação real em ambiente autorizado quando os gates de segurança permitirem.
3. Completar evidências técnicas e normativas independentes para motores elétricos E01–E11. Não interpretar testes sintéticos como homologação normativa.
4. Obter aceite humano profissional C13 autêntico, com referência à versão e aos resultados verificados.
5. Reexecutar cinco workflows sobre o SHA final de implementação, sem inferir aprovação do GC por CI.

## Veredito

- `GREENFIELD_SCOPE=CONFIRMED`
- `LEGACY_IMPORT=DEFERRED_OPTIONAL`
- `CI_DEV_5_OF_5=PASS` **apenas no SHA auditado acima**; a criação deste relatório produz um SHA posterior que deverá ser validado separadamente.
- `REMOTE_MIGRATIONS_A03_A04_B04_C03=NOT_APPLIED`
- `AUTH_REAL_AB=NOT_VERIFIED`
- `C13_HUMAN_ACCEPTANCE=NOT_VERIFIED`
- `DESTINATION_RECOVERY=NOT_VERIFIED`
- `GC=BLOCKED`

**Proteções:** nenhuma escrita em Supabase, nenhum backup remoto C17, nenhuma importação legada, nenhuma ação no PC do usuário, nenhum custo adicional, nenhum merge em `main` ou deploy.
