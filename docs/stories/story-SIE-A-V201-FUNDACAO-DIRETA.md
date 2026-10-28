# Story SIE-A-V201 — Fundação canônica sem serviços adicionais

**Plano:** SIE 2.0 V2.0, revisão 2.0.1 (28/10/2026).
**Branch de trabalho:** `feat/v201-bloco-a-desenvolvimento-direto`.
**Base de desenvolvimento:** `feat/gf02-supabase-foundation` @ `f8ea65224f1ad2baa791fa64caa2407d65eeef78`.
**Gate de entrada:** escopo ratificado somente para desenvolvimento. **Gate de saída:** GA verificável.
**Sem DDL remota, merge, deploy, cobrança ou alterações no SIE original.**

## Contexto
- GF02 `20261027195557_sie2_greenfield_foundation_owner_rls_v1` já aplicada no projeto de destino `fozrymsidnaxmuvxxfhh`.
- Não usar `supabase/migrations` na raiz do projeto (legado); somente `restructuring/supabase/migrations`.
- A política V2.0.1 permite desenvolvimento em Git sem laboratório/Docker/branch Supabase paga.
- Os avisos de FK são hipóteses de otimização, não evidência de regressão de desempenho; validar antes de aplicar índices.

## Critérios de aceite (desenvolvimento)
- [ ] A01: leitura atual de projeto, migrações, RLS, grants, índices, fontes e drift com hashes verificáveis.
- [ ] A02: catálogo canônico identifica exatamente a GF02; verificação local automática de hash Git, versionamento e exclusão de legados.
- [ ] A03: matriz de 13 FKs, 10 avisos e candidate de índices sem executar DDL no banco existente.
- [ ] A04: ADR de revisões, transições, idempotência e imutabilidade, sem confundir aprovação profissional com estados técnicos.
- [ ] A05: matriz de autorização e riscos `owner-only`, incluindo `service_role`.
- [ ] A06: runbook de backup/rollback e transferência do restore físico a E04.
- [ ] A07: executar testes reais no SHA final, verificar CI real e emitir contrato de GA validado; sem declarar PASS caso falte evidência.

## Restrições de publicação
Nenhuma migration nova é aplicada no Supabase `fozrymsidnaxmuvxxfhh` sem autorização separada de DDL, análise do diff, verificação de backup/reversão e read-back. Nenhum teste sintético será chamado de prova RLS A/B real.

## File list (atualização conforme implementação)
- `docs/stories/story-SIE-A-V201-FUNDACAO-DIRETA.md`
- `restructuring/supabase/greenfield/manifest.json`
- `restructuring/supabase/greenfield/check_catalog.py`
- `restructuring/apps/api/tests/test_a02_greenfield_catalog_v201.py`
- `docs/implantacao-sie-2-0/GREENFIELD/A01_ADR_BASELINE_V201.md`
- `docs/implantacao-sie-2-0/GREENFIELD/A03_INDICES_CANDIDATO.sql`
- `docs/implantacao-sie-2-0/GREENFIELD/A04_ADR_REVISOES_V201.md`
- `docs/implantacao-sie-2-0/GREENFIELD/A05_MATRIZ_SEGURANCA_V201.md`
- `docs/implantacao-sie-2-0/GREENFIELD/A06_RUNBOOK_RECUPERACAO_V201.md`

**Estado:** IN_PROGRESS; não equivale a GA PASS.
