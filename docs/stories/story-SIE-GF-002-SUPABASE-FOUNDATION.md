# Story SIE-GF-002 — Fundação PostgreSQL/Supabase segura (owner-only)

**Escopo autorizado:** desenvolvimento incremental do SIE 2.0, branch isolada; Supabase alvo exclusivo `fozrymsidnaxmuvxxfhh` (`SIE_2.0`, organização Applicationmanager). O banco foi confirmado vazio no schema `public` e sem migrations registradas. **Nunca aplicar no SIE original nem usar o banco do projeto DHT.**

## Decisão arquitetural
- PostgreSQL/Supabase Auth como identidade; `auth.uid()` para proprietário autenticado. Sem duplicar senhas, sem chave `service_role` no navegador.
- Modelo multi-projeto **por proprietário único** nesta primeira entrega. Compartilhamento/organizações/RBAC são etapas futuras, não permissões implícitas.
- Entidades `sie_projects`, `sie_project_revisions`, `sie_rooms`, `sie_loads`, `sie_circuits`, `sie_circuit_loads`, `sie_calculation_runs`, `sie_artifacts` e `sie_audit_events`.
- FK compostas asseguram `project_id` e `revision_id` consistentes entre as entidades.
- RLS em toda tabela exposta e GRANTs explícitos: `anon` sem permissões; `authenticated` vê exclusivamente projetos próprios. Inserção permitida apenas nos cadastros; cálculos/artefatos/auditoria são **server-only**.
- Cadastros e revisões são append-only exceto nome do projeto; nenhum DELETE/UPDATE de circuitos/cargas/revisões por usuários. Não prometer selo imutável de snapshot enquanto não houver mecanismo de fechamento de revisão.
- Normas e concessionárias NÃO homologadas; migração de metadados não concede aprovação técnica.

## Critérios de aceite
- [ ] GF02-01: modelo e migração versionados no repositório, separados das migrations legadas de qualidade.
- [ ] GF02-02: pré-validação do alvo por ID, organização, schemas/migrations vazios.
- [ ] GF02-03: aplicar DDL apenas no projeto `fozrymsidnaxmuvxxfhh`, guardar versão retornada pelo Supabase.
- [ ] GF02-04: provar tabela por tabela que RLS está ativo, políticas autenticadas restritivas e `anon` sem privilégios.
- [ ] GF02-05: verificar FKs compostas, constraints, índices e rollback seguro definido (sem execução de DROP).
- [ ] GF02-06: suíte de testes estáticos e CI da branch no próprio commit de código.
- [ ] GF02-07: testes de autenticação real e isolamento entre dois usuários — **pendentes** até haver identidades de teste; nenhum aceite falso.
- [ ] GF02-08: integração API e UI autenticadas — fase seguinte, não implementada neste lote.

## Restrições
Preservar `main`, F00–F12, repositórios do SIE 1.0 e Hostinger. Não implantar funções externas, não criar usuários reais, não excluir dados, não fazer merge/deploy. Banco destino já inspecionado em modo leitura. Nenhum teste SQL deve gravar dados operacionais reais.

## Arquivos
- `docs/stories/story-SIE-GF-002-SUPABASE-FOUNDATION.md`
- `docs/implantacao-sie-2-0/GREENFIELD/GF02_SCHEMA_CANDIDATE.sql`
- `restructuring/apps/api/tests/test_gf02_schema_contract.py`
- Migração versionada dentro de `restructuring/supabase/migrations/` após implantação.
- `docs/implantacao-sie-2-0/GREENFIELD/GF02_RESULTADO.md`

**Gate:** F12 mantém `HUMAN_REQUIRED` e `NO-GO` para produção profissional.
