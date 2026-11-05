# Story SIE-C-V201 — Migração do domínio elétrico, perfil DEVELOPMENT

**Entrada verificada:** GB=PASS em `63805c03c7146103cdd67eca4da3e369a751d379`.
**Branch:** `feat/v201-bloco-c-dominio-eletrico`. **PR:** #11 aberta para revisão, base Bloco B.
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
- [x] C19: importação C01/C07 e revisão E10 legadas diferidas, sem bloquear GREENFIELD.
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

## Continuidade C20 — critérios e evidências GREENFIELD (04/11/2026)

Critérios: preservar o legado; remover apenas bloqueios exclusivos da importação; corrigir concorrência de sessão; provar rollback transacional do pacote de migrations em PG17 isolado, sem conceder GO remoto.

- [x] Reconciliar bloqueios ativos C08 e aplicabilidade E10 em C04/C05 e C12.
- [x] Diagnóstico C18 respeita recusa C17 e exige alternativa recuperável comprovada.
- [x] Implementar testes PG17 de falha após cada migration e reaplicação limpa.
- [x] Regressão de Auth executa JavaScript real com rede simulada; story B registra correções.
- [ ] Prova PG17 C20 no GitHub Actions do commit final (ver run associado ao commit).
- [ ] Recuperação operacional pós-commit, DDL destino, Auth A/B real e aceite elétrico permanecem pendentes.

### File list C20
- `scripts/c18_real_migration_readiness.py`
- `restructuring/apps/api/tests/test_c18_real_migration_readiness.py`
- `restructuring/apps/api/tests/test_c20_migration_atomicity_pg17_v201.py`
- `.github/workflows/sie-c03-pg17.yml`
- `docs/implantacao-sie-2-0/GREENFIELD/C08_CONTRATO_ENTREGA_C_V201.json`
- `docs/implantacao-sie-2-0/GREENFIELD/C04_C05_DOSSIE_ACEITE_PROFISSIONAL_V201.json`
- `docs/implantacao-sie-2-0/GREENFIELD/C12_DOSSIE_VALIDACAO_EVIDENCIAS_ELETRICAS_V201.md`
- `docs/implantacao-sie-2-0/GREENFIELD/C20_CONTINUIDADE_GREENFIELD_20261104.md`

Estado: incremento pronto para revisão; GC=BLOCKED, sem handoff D.


CI final SHA verification trigger: 05/11/2026.
