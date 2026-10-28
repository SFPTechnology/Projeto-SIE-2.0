# B07 — Playbook de segurança e resiliência V2.0.1 (DESENVOLVIMENTO)

**Perfil:** test/dev. Não autoriza produção, integrações remotas ou custos.

## Identidade e autorização
A origem confiável do identificador de usuário é `AuthIdentity.user_id` obtida de `GET /auth/v1/user` do projeto fixo; JWT não verificado, `user_metadata`, owner fornecido pelo navegador e `role` autodeclarado não concedem direitos. `service_role` nunca vai ao browser. API retorna:
- `401` token ausente/inválido ou conta anônima; não revelar a existência do recurso;
- `404` projeto, revisão ou entidade fora da titularidade, com mesma resposta do inexistente;
- `409` versão obsoleta, FK vinculada, idempotency key com payload diferente ou revisão lacrada;
- `422` campos fora do esquema, numerais inválidos, referência/escala incorreta;
- `503` Auth ou banco indisponível: **sem fallback de autenticação**; sem gravação;
- `429` excesso de chamadas DEV, cabeçalho Retry-After.

## Operação em caso de falha
1. Confirmar `source_sha`, ambiente, projeto, migrações e autorização antes de investigar.
2. Se Auth ficar indisponível: manter API fail-closed; não usar JWT decodificado sem validação criptográfica. Não aumentar permissões para contornar a falha.
3. Se houver conflito 409: buscar versão atual; nunca repetir mutação de entidade com versão anterior. Criar projeto ou revisão admite reenvio da **mesma chave e corpo**.
4. Se a transação falhar, verificar rollback completo: carga e eventos de auditoria não podem ficar pela metade. Dados sintéticos apenas.
5. Se houver erro de integridade referencial, corrigir relação no aplicativo. Não desabilitar FKs/RLS ou triggers A04.
6. Registros de correlação `X-Request-ID` e hora são aceitáveis; não coletar bearer, refresh token, service_role, emails e senhas.
7. Se ocorrer 503 por flag ausente, isso é comportamento seguro: DEV exige `SIE_V201_DEV_WRITES=1` + `SIE_ENV=dev/test` + host loopback + banco SQLite DEV absoluto.
8. Se o usuário solicitar implantação, passar pelos gates E02–E06: Auth A/B real, DDL aprovada, read-back, backup/restore, RLS e autorizações profissionais.

## Limites conhecidos de implementação
- O rate limiter é **por processo**, somente DEV; requer implementação distribuída/centralizada para uso exposto e revisão do proxy.
- SQLite é fixture de desenvolvimento, PostgreSQL 17 CI tem credenciais descartáveis. Não usar o código `Pg17DisposableAdapter` em Supabase real.
- O adaptador PG17 usa PostgreSQL sintético com Auth stubs; o isolamento RLS real do Supabase requer JWTs reais na E02/E06.
- Renovação de sessão no navegador é volátil, não mantém token após recarregar e não equivale a revogação instantânea do JWT.
- Artifatos de cálculo em B06 permanecem `NOT_EVALUATED`, sem certificação NBR nem atestado profissional.

## Evidências reexecutáveis
`test_b01_b02_auth_v201.py`, `test_b04_b05_dev_transactions_v201.py`, `test_b05_b06_b07_negative_v201.py`, `test_b06_server_writer_v201.py`, `test_b08_dev_journey_v201.py`, `test_b04_b05_pg17_disposable_v201.py`, `test_b01_auth_v201_browser.py`.
CI vinculante: **SHA HEAD** da PR #10; não extrapolar testes de um SHA anterior.
