# C02/C06/C07 — Contrato ETL V2.0.1, perfil DEVELOPMENT

**Entrada:** `C01` está `LEGACY_SOURCE_UNVERIFIED`, portanto a transferência **REAL_LEGACY** é recusada programaticamente. Em testes, `source_kind=SYNTHETIC_TEST` é a única origem aceita.

**Matriz:** `MATRIZ_LEGADO_DESTINO.csv` contém 54 campos das oito tabelas do SQL legado mapeados/condicionados/quarentenados. `DIRECT` nesta matriz indica conversão pretendida, não autorização de executar sem identidade ou validação de origem.

**Algoritmo DEV:** JSON canônico com `rooms`, `loads`, `circuits`, `links`; B04 owner+project+revision existente em DRAFT; lote de até 4.000 entidades e 256 KiB no CLI; mapeamento UUID determinístico UUID5 a partir do owner/projeto/revisão/key/tipo/id de origem sintética; ledger SQLite transacional de `idempotency_key` + digest; segundo replay retorna exatamente o mesmo mapa; key igual, conteúdo diferente => conflito; órfãos => erro; transação é revertida e nenhuma carga parcial é confirmada.

**CLI:** `SIE_ENV=test SIE_V201_C_ETL_DEV=1 python -m sie_api.v201_c_cli stage --database /abs/fixture.sqlite3 --manifest /abs/fixture.json --owner <uuid> --project <uuid> --revision <uuid> --idempotency-key c06-fixture-001`. O banco deve ser explicitamente SQLite de desenvolvimento, com projeto pré-existente. Nenhuma conexão Supabase/legacy ou `service_role` aceita.

**Reconciliação:** contagens e IDs do lote aceito são comparados ao snapshot persistido owner-scoped. Isso prova apenas os lotes sintéticos, não equivalência dos oito agregados legados. Origens reais, escrita no PostgreSQL final, cross-database A/B, restore e cutover são tarefas pendentes expressas de C01/C07/E02–E06.

**Retomada/rollback:** lote commit atômico ou rollback integral, sem apagar nem alterar origem. Em caso de falha externa, reexecutar mesma key+hash; mudança de payload exige nova chave e avaliação de deduplicação. Staging de produção e mapa definitivo só após governança de proprietário e backup.

**Categorias e resultados:** não inferir TUG/TUE, fase, método de instalação, licenciamento ou aprovação; resultados `LEGACY_RESULT` permanecem `NOT_EVALUATED`. `autor` textual não corresponde a `auth.uid()`.
