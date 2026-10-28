# B03a — Matriz RLS e verificações negativas de desenvolvimento

**Perfil:** DEV, versão 2.0.1. **Consulta realizada:** 28/10/2026 no Supabase `fozrymsidnaxmuvxxfhh` via SQL **somente leitura**. B03b ainda depende de B05.
**Não existe conta de teste criada no ambiente remoto.**

| Alvo | Leitura real | Interpretação e pendência |
|---|---|---|
| `public.sie_*` | 9 tabelas; **9/9 RLS habilitada** | RLS ligada não prova isolamento entre identidades reais |
| `pg_policies` | 16 políticas; todas `TO authenticated` | FKs compostas e predicates owner-only exigem testes A/B por JWT |
| `anon` | nenhum GRANT de tabela no readback | Supabase Auth usuário anônimo pode possuir role `authenticated`: negar no backend |
| `authenticated` | SELECT em 9 tabelas; INSERT em 6 com grants de colunas; UPDATE de `sie_projects.name` | Verificar proprietário e propriedade da revisão em todos os endpoints |
| `service_role` | privilegios efetivos amplos em todas as 9 tabelas | Bypass RLS: exigir ownership no backend antes da query, chave nunca em browser |
| A03/A04 | **PENDING** no destino remoto | Em PostgreSQL 17 descartável passaram 2 rebuilds e testes de invariantes |
| A/B reais | **não executados** | E02/E06 necessários para GO; fixture não equivale a isolamento remoto |

## Casos negativos
1. Sem bearer/malformado/expirado: 401 antes de qualquer chamada Auth.
2. Issuer/audience/role forjados: 401.
3. Rejeição ou indisponibilidade de Supabase Auth: 401/503, sem fallback inseguro.
4. Resposta Auth com outro UUID: 401; usuário `is_anonymous=true`: 401.
5. Projeto de outro proprietário no backend: 404 sem revelar UUID legítimo.
6. Redirect externo ou parecido com o domínio permitido: rejeição.
7. Testes SQL locais da GF02 incluídos no pacote A, com identidades sintéticas; não são prova A/B remota.
8. B03b: **pendente**, só após B04/B05 e seus endpoints de projetos/ambientes/cargas/circuitos.

## Situação
**B03a: IN_REVIEW** até conferir testes B01/B02 no SHA final. **B03b: NOT_STARTED.**
**Proibição:** não usar dados reais como fixtures, não escrever em Supabase, não declarar `GB PASS` nem `GO`.
