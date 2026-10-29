# Story SIE-C-V201 — Migração do domínio elétrico, perfil DEVELOPMENT

**Entrada verificada:** GB=PASS em `63805c03c7146103cdd67eca4da3e369a751d379`.
**Branch:** `feat/v201-bloco-c-dominio-eletrico`. **PR:** #11 DRAFT, base Bloco B.
**Saída:** `GC=BLOCKED` (integral); escopo parcial de desenvolvimento implementado, sem extrapolar para Supabase remoto.

## Checklist de execução e provas
- [x] C01: inventário somente leitura do legado e declaração formal `LEGACY_SOURCE_UNVERIFIED`; contagens reais ainda não verificadas.
- [x] C02: matriz de 54 campos, quarentenas e contrato de transformação; mapeamento de owner real pendente.
- [x] C03: migration canônica `20261028203000` PENDING, 10 tabelas novas, FKs, RLS e triggers; PG17 descartável.
- [x] C04: gateway normativo versionado/hashed, nenhuma aprovação por flag/JSON.
- [x] C05: fluxo DEV de snapshot B selado, VA explícita, run e auditoria, API A/B sintética, histórico stale.
- [x] C06: CLI de ETL exclusivamente sintético com transação e replay por chave.
- [x] C07: reconciliação sintética, sem importação legada operacional.
- [x] C08: dossiê e contrato `GC=BLOCKED` emitidos.
- [ ] Homologação C01/C07 sobre origem real/ramo vazio comprovado.
- [ ] Motores C05 completos, condições normativas e testes golden liberados.
- [ ] Aplicação DDL autorizada, Auth/RLS real A/B e restore no destino após E02–E06.
- [ ] `GC=PASS` e handoff formal D.

## Entregáveis
`C01_INVENTARIO_FONTE_LEGADA_V201.md`,
`C02_MATRIZ_LEGADO_DESTINO_V201.csv`,
`C03_ADR_DOMINIO_ELETRICO_V201.md`,
`C03_SCHEMA_CANDIDATE_V201.sql`,
`restructuring/supabase/migrations/20261028203000_sie_c03_electrical_domain_v201.sql`,
`C04_CATALOGO_NORMATIVO_VERSIONADO_V201.md`,
`C06_CONTRATO_ETL_V201.md`,
`C08_GC_RELATORIO_V201.md`,
`C08_CONTRATO_ENTREGA_C_V201.json`, testes API, PG17, AIOX e Chromium.

**Constituição de segurança:** preservar `main`, F12, SIE original, DHT, `fozrymsidnaxmuvxxfhh` e produção. Nenhum resultado matemático é laudo normativo.
