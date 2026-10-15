# F01 — Snapshots de catálogo e impacto histórico (SQLite local)

**Implementação limitada ao protótipo local.** A captura é feita ao salvar um projeto pela CLI/API existente, sem Supabase ou banco de produção.

O módulo `sie_api/normative_snapshots.py` serializa o catálogo de metadados confiável do servidor, calcula SHA-256 e compara versões. `sie_api/storage.py` insere uma linha por (projeto, revisão) em `snapshots_normativos` e um evento em `eventos_snapshot_normativo`, na mesma transação do salvamento. Triggers impedem UPDATE/DELETE usuais desses registros.

Consulta autenticada por token de desenvolvimento (somente ambiente local):
- `GET /api/v1/local/projetos/{uuid}/snapshots-normativos/{revisao}`
- `GET /api/v1/local/projetos/{uuid}/impacto-normativo/{revisao}`
- `GET /api/v1/local/projetos/{uuid}/historico-normativo`

Testes: `restructuring/apps/api/tests/test_normative_snapshots_f01.py`. Cobertura de escrita atômica, conflito de revisão, imutabilidade, digest, alteração de edição em dados fictícios, token, banco antigo, ausência de backfill e não aprovação pelo cliente.

**Limites críticos:** trata-se do snapshot **do catálogo disponível na gravação**, não da lista das regras/células utilizadas pelo motor no cálculo. Não recupera dados anteriores do projeto, não contém documentos licenciados, não equivale a homologação, não é prova criptográfica contra administrador capaz de alterar digest e dados, nem resolve identidade multiusuário. Um projeto legado sem snapshot permanece sem ele; não há retroatividade fictícia.

A versão F01 não migra banco remoto nem altera `main`. Para concluir integralmente a task 01.06, vincular revisões/IDs e fontes de cada regra aplicada por circuito, memória de cálculo, entrada e saída históricas, responsáveis/revisão, eventos de impacto e restauração, sempre com autorização segura e fontes normativas homologadas. **01.06 permanece PARCIAL e F01 BLOCKED.**
