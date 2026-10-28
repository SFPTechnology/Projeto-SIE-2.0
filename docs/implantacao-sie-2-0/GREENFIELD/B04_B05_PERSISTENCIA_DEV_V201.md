# B04/B05 — CRUD transacional de desenvolvimento (revisão 2.0.1)

**Escopo implementado:** backend FastAPI `/api/v2/sie/dev` conectado a arquivo SQLite local, **não ao banco Supabase remoto**. É um adaptador de desenvolvimento deliberadamente isolado, compatível com o fluxo de escrita da F12 sem alterar F12. O contrato de PostgreSQL remoto continua pendente até aplicação autorizada das migrations A03/A04.

## Liberação operacional segura
Para habilitar exclusivamente no computador de desenvolvimento:
- `SIE_ENV=test` ou `SIE_ENV=dev`.
- `SIE_V201_DEV_WRITES=1` explicitamente.
- `SIE_V201_DEV_DB_PATH=/caminho/absoluto/sie2-dev.sqlite3`.
- Host HTTP deve ser loopback (ou `testclient` na suíte). Qualquer acesso externo rejeitado.
- Um bearer **real** continua obrigatório na rota: `current_identity` verifica assinatura no Supabase Auth via HTTPS. Testes usam dependency override sintético **somente no TestClient**.
- **Nunca** configurar a flag na hospedagem de produção. O nome da rota deixa explícito `/dev`.

## Contratos B04 implementados (DEV)
- Criar projeto de `owner_id` derivado da identidade, sem campo arbitrário no corpo; chave idempotente owner+key. Replay de mesma chave e mesmo corpo retorna o projeto original; corpo divergente recebe 409.
- Listar e renomear projetos próprios com `lock_version` e conflito 409.
- Criar revisão `DRAFT` com versão numerada atomicamente e chave idempotente projeto+key. Bloquear dois drafts simultâneos.
- Selar `DRAFT -> SEALED` com `lock_version` esperado, snapshot JSON canônico (SHA-256) e estado imutável; clonagem de `SEALED` cria novo draft.
- Clone remapeia identidades de ambientes, cargas, circuitos e vínculos em **uma transação**; reinício da API preserva projeto e snapshot.
- Superceder `SEALED -> SUPERSEDED` só após sucessora selada.

## Contratos B05 implementados (DEV)
- Ambientes: `width_m`, `length_m` e `excluded_perimeter_m` em Decimal sem arredondamento silencioso; escala 4.
- Cargas: `LIGHTING/TUG/TUE/OTHER`, quantidade positiva e potência aparente Decimal (3 casas), com FK de ambiente, projeto e revisão.
- Circuitos: `code` único por revisão e tensão nominal Decimal (3 casas).
- Vínculo: carga exclusiva de um circuito por revisão; rejeitar associações cruzadas.
- `POST .../bundle` insere todas as entidades do mesmo lote com aliases `ref`/referências internas em transação `BEGIN IMMEDIATE`; uma referência inválida ou duplicada provoca rollback **integral**, não parcial.

## Proibições e pendências
- **Não executado:** integração PostgreSQL real, Supabase Auth com usuários A/B reais, importação GF01, edição completa de entidade existente, histórico server-only B06, QA B08 e prova de recuperação após rollback do Supabase.
- **Não é uma migration:** o esquema SQLite é apenas para fixture/desenvolvimento; não migrar seus dados para a produção nem confundir com o catálogo greenfield SQL.
- A03/A04 continuam `PENDING` em `fozrymsidnaxmuvxxfhh`; nenhuma operação remota de escrita foi efetuada, nenhuma chave service_role foi incorporada ao código.
- Nenhuma assinatura de conformidade elétrica ou liberação normativa é inferida.
- Futuro adaptador PostgreSQL deve obedecer o contrato das migrations A03/A04, CAS, FKs compostas, RLS, owner-only e rollback transacional; autenticação por JWT real antes de executar operações privilegiadas.

## Evidências de QA
`restructuring/apps/api/tests/test_b04_b05_dev_transactions_v201.py`: idempotência, concorrência, lock, isolamento A/B simulado, clonagem de quatro entidades, imutabilidade de snapshot, persistência após reinício, rejeição de dados inválidos, rollback de clone, sucesso/rollback do lote, proibição de acesso cruzado e bloqueio fora de DEV.
