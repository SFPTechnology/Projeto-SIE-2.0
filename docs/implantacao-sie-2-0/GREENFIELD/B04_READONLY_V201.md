# B04 — Consulta de projetos com isolamento owner-only (incremento inicial)

**Estado:** IN_PROGRESS — leitura implementada e testada com doubles; CRUD transacional ainda pendente.

## Recurso
`GET /api/v2/sie/projects`:
- Depende de `current_identity` B02, com verificação criptográfica pelo serviço Supabase Auth e checagem de `iss/aud/exp/sub`.
- Consulta PostgREST pelo **JWT do próprio usuário**, nunca usando chave `service_role`.
- Filtra por `owner_id` extraído da sessão verificada; RLS real no banco é a segunda barreira; cada linha retornada recebe conferência extra de titularidade.
- Restringe a 100 registros e projeta apenas id/nome/data. Dados malformados ou indisponibilidade retornam erro seguro.
- Chave `SIE_B04_READS_ENABLED=1` **necessária**; padrão ausente=503 para impedir ativação inadvertida. `SIE_SUPABASE_PUBLISHABLE_KEY` é também exigida.
- A função não faz INSERT, UPDATE ou DELETE nem cria usuário/bucket. Nenhum teste remoto foi executado.

## Limites
- Não equivale a B04 concluída: ainda é necessária criação/renomeação de projeto, revisão atômica, clone, CAS no banco real, testes de persistência e idempotência.
- A03/A04 continuam migrations `PENDING` no Supabase atual. Nenhum fluxo de escrita é habilitado enquanto a migração não for aplicada com autorização específica.
- Auth A/B real só pode ser aferido com usuários autorizados; o teste de proprietário B04 existente é com mock e não prova a Data API real.
- Fluxos B05–B08 continuam dependentes do DAG. GB permanece BLOCKED.

## Teste automatizado
`restructuring/apps/api/tests/test_b04_owned_read_v201.py`: rota desativada=503 sem REST; leitura com titular; leitura cruzada negada=404; falta de bearer=401; resposta malformada=503.
