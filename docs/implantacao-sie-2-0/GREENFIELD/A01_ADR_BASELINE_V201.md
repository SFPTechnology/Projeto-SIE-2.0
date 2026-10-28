# A01 — ADR de baseline GF02 / leitura real / revisão V2.0.1

**Decisão:** CONCILIADO PARA DESENVOLVIMENTO; sem autorização de alteração em produção.
**Leitura:** 28/10/2026; fontes: Supabase (get_project/list_migrations/execute_sql/get_advisors), GitHub (arquivo GF02 e branch), protocolo G0 anterior.
**Responsáveis de trabalho:** DADOS; revisão QA documental, não assinatura profissional independente.

## Identidade verificada
- Supabase ref: `fozrymsidnaxmuvxxfhh`; nome `SIE_2.0`; org `takynlbrhcdenqsrxhps`; região `sa-east-1`; PostgreSQL `17.11.0.003`; saúde `ACTIVE_HEALTHY`.
- Migration efetivamente registrada: `20261027195557_sie2_greenfield_foundation_owner_rls_v1` (apenas ela).
- GitHub branch base `feat/gf02-supabase-foundation`: `f8ea65224f1ad2baa791fa64caa2407d65eeef78`.
- Fonte canônica: `restructuring/supabase/migrations/20261027195557_sie2_greenfield_foundation_owner_rls_v1.sql`, blob Git SHA-1 `6714a9e18e04f06e2d249de56c26b7a2ca9dd9d2`.
- Repo raiz `supabase/migrations` contém histórico legado distinto; não incluir em catálogo greenfield.

## Read-back PostgreSQL (grupo de objetos; **não** schema dump completo)
| Classe | Objetos | MD5 de lista ordenada |
|---|---:|---|
| Colunas | 63 | `088dec51d639f9a7863421168dc5a941` |
| Constraints | 53 | `ce02191392eb0e9385db288849330d94` |
| Índices | 26 | `e3cf2d5b815756bcf60b74a49582fa66` |
| Políticas RLS | 16 | `db19893bca1174dde384e2b3ff91f637` |

Os quatro hashes concordam com o checkpoint G0. Isto demonstra estabilidade desses grupos e nomes; **não demonstra ausência absoluta de drift** em triggers, funções, defaults avançados, owners, grants ou extensões. Divergência nessas categorias permanece risco de DDL remota.

## Segurança e dados
- `public.sie_*`: 9 tabelas, 9 com RLS ligada e 16 políticas; `anon` sem GRANT de tabela.
- `authenticated`: SELECT em 9 tabelas; INSERT por colunas em 6; UPDATE somente de `sie_projects.name`.
- `auth.users`: 0 identidades; buckets Storage: 0; funções públicas nomeadas `sie_*`: 0.
- Advisors de segurança: 0 alertas. Advisors de desempenho: 10 FKs não indexadas *segundo a heurística do advisor* e 8 índices ainda não usados (base vazia).
- Não existe evidência de login real A/B nem de isolamento via Data API.

## Observações e riscos
- 13 FKs examinadas; quatro não encontram índice cujo prefixo contenha todas as colunas da FK: `sie_projects.owner_id`, `sie_project_revisions.created_by`, `sie_audit_events.actor_id`, `sie_audit_events(revision_id,project_id)`. Ver A03 para proposta de índices sem DDL.
- Seis avisos adicionais podem ter índices compostos utilizáveis em predicados de igualdade, embora a ordem/prefixo difira do padrão do advisor. É necessário plano de execução representativo antes de afirmar ganho de performance.
- Ausência de Auth real e ambiente isolado **não bloqueia codificação** pela política V2.0.1; permanece pendência de validação antes da publicação.

## Decisão
Aceitar esta linha de base para A02 no fluxo de desenvolvimento, sem reinstalar GF02; bloquear apenas DDL remota sem pré-condições verificadas. A01 NÃO valida backup, restore, segurança real A/B ou igualdade bit-a-bit de todo o esquema.
