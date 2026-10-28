# B03b — Matriz de isolamento A/B (API de desenvolvimento)

**Escopo dos ensaios:** TestClient FastAPI com autenticação substituída por fixtures `AuthIdentity(A)` e `AuthIdentity(B)`, base SQLite transacional `DEV` e nenhuma chamada externa ao Supabase. **Não é teste de JWT ou RLS remotos.** Os testes B01/B02 verificam a recusa de JWT falso usando mock da API Auth; os testes aqui se concentram no uso do owner já autenticado.

| Ameaça / operação | Resultado contratual esperado | Teste |
|---|---|---|
| Requisição sem bearer | 401 | `test_no_authenticated_session_fails_before_write` |
| `SIE_ENV=production` com flag indevida | 503 | `test_dev_api_is_disabled_in_production_even_with_flag` |
| Feature flag desligada | 503 | `test_dev_api_requires_explicit_flag_and_path` |
| Proprietário A cria projeto repetindo chave | 1 projeto, mesmo ID | `test_project_create_idempotency_and_conflicting_payload` |
| Proprietário B lista, renomeia ou cria revisão em projeto A | 404 ou lista vazia | `test_project_rename_lock_and_foreign_owner_denied`; `test_a_cannot_read_or_modify_project_b` |
| Alteração com versão obsoleta | 409 | `test_project_rename_lock_and_foreign_owner_denied` |
| Revisão selada alterada ou selada de novo | 409 | `test_revision_numbering_idempotency_lock_clone_and_restart` |
| UUID de ambiente/carga/circuito estranho ao escopo | 409, sem gravar nada | `test_cross_revision_room_and_circuit_fk_rejected_atomically` |
| Carga vinculada a mais de um circuito | 409 | `test_cross_revision_room_and_circuit_fk_rejected_atomically` |
| Alias inexistente durante lote B05 | 409, **rollback total** | `test_b05_bundle_bad_reference_rolls_back_everything` |
| Link duplicado durante lote B05 | 409, **rollback total** | `test_b05_bundle_duplicate_load_link_rolls_back_all` |
| Lote de B enviado contra projeto de A | 404, sem gravação | `test_b05_bundle_denied_for_foreign_owner` |
| Banco falha no meio de clone | 503, sem revisão parcial | `test_clone_is_all_or_nothing_on_database_error` |
| Documento com owner_id ou decimal inválido | 422 | `test_b05_rejects_invalid_geometry_and_extra_fields`; `test_b05_bundle_invalid_decimal_and_unknown_json_denied` |

**Status:** B03b coberto por contratos **locais** e testes de CI, sujeito à verificação do SHA final. A auditoria A/B **remota e efetiva** permanece bloqueada até autenticação e ambiente controlado autorizados. GB integral ainda requer B06, B07, B08 e integração persistente em PostgreSQL.
