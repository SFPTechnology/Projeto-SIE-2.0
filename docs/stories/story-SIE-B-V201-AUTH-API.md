# Story SIE-B-V201 — Auth, validação de sessão e API segura

**Plano:** SIE 2.0 V2.0 revisão 2.0.1; **entrada:** GA PASS **somente para desenvolvimento**; **base:** `fbf8b957015ba24dfd29167d9d3fe259db979876`; **branch:** `feat/v201-bloco-b-auth-api`.

## Critérios de aceite
- [x] B01: especificar login/confirmar e-mail/recuperar/logout, redirect allowlist e configuração sem secrets no frontend.
- [x] B02: novas rotas autenticadas falham fechadas sem bearer, tokens errados/expirados/forjados; usar Auth Supabase como verificador confiável e ignorar metadata do browser na autorização.
- [x] B02: extrair sub UUID verificado e negar usuário Auth anônimo; nunca usar `service_role` no navegador; preservar rotas legadas fora do prefixo novo.
- [x] B03a: conferir RLS/grants read-only e matriz negativa; nenhum teste de A/B real declarado sem identidades remotas. **B03a documental, não B03b.**
- [x] B04 **em DEV**: criar/listar/renomear projetos owner-only, versão otimista, revisões idempotentes, clone com remapeamento de 4 entidades, selagem, histórico e read-back persistente. Recurso local opt-in, não remoto.
- [x] B05 **DEV**: criação, edição, exclusão granular CAS, bundle transacional e rollback, com FKs e proteção de revisão selada. PostgreSQL remoto ainda pendente.
- [x] B03b **DEV**: testes negativos A/B sintéticos com CRUD B04/B05 e rollback; testes JWT/Data API reais permanecem em E02/E06.
- [ ] Integração remota: não ativar escrita no Supabase sem A03/A04 aplicadas, read-back e autorização específica.
- [x] B06 **DEV**: trilha append-only e runs/artefatos internos, com hash, owner e rollback.
- [x] B07 **DEV**: CORS restrito, tamanho de payload, rate limit local, trace ID e respostas no-store.
- [x] B08 **DEV**: jornada integrada 2 ambientes/3 cargas/2 circuitos com reabertura de SQLite e tentativas A/B simuladas.
- [ ] GB: verificar checks no HEAD, validar contrato e delimitar pendências reais (Auth browser, PostgreSQL remoto, B08 real).
- [ ] CI do SHA final: API, AIOX e Chromium no mesmo HEAD; não reutilizar resultados de SHAs anteriores.

## Fronteiras
- Supabase `fozrymsidnaxmuvxxfhh` permanece GF02; A03/A04 **PENDING**.
- **Sem** migração remota, criação de usuários, merge, deploy, F12, alteração do SIE original ou novo serviço pago.
- Validação real A/B via Data API/Auth antes de E06 GO, não pré-condição de desenvolvimento.
- PR a ser aberta em rascunho contra `feat/v201-bloco-a-desenvolvimento-direto`, não contra `main`.

## File list
- `docs/stories/story-SIE-B-V201-AUTH-API.md`
- `docs/implantacao-sie-2-0/GREENFIELD/GA_DESENVOLVIMENTO_V201.md`
- `docs/implantacao-sie-2-0/GREENFIELD/B01_AUTH_FLOW_V201.md`
- `restructuring/apps/api/sie_api/auth_boundary_v201.py`
- `restructuring/apps/api/sie_api/auth_router_v201.py`
- `restructuring/apps/api/sie_api/main.py`
- `restructuring/apps/api/tests/test_b01_b02_auth_v201.py`
- `docs/implantacao-sie-2-0/GREENFIELD/GA_DESENVOLVIMENTO_V201.json`
- `docs/implantacao-sie-2-0/GREENFIELD/GA_DESENVOLVIMENTO_V201.md`
- `docs/implantacao-sie-2-0/GREENFIELD/B03a_MATRIZ_RLS_V201.md`
- `docs/implantacao-sie-2-0/GREENFIELD/B04_READONLY_V201.md`
- `restructuring/apps/api/tests/test_b04_owned_read_v201.py`
- `restructuring/apps/api/sie_api/v201_dev_store.py`
- `restructuring/apps/api/sie_api/v201_dev_api.py`
- `restructuring/apps/api/tests/test_b04_b05_dev_transactions_v201.py`
- `docs/implantacao-sie-2-0/GREENFIELD/B04_B05_PERSISTENCIA_DEV_V201.md`
- `docs/implantacao-sie-2-0/GREENFIELD/B03b_MATRIZ_AB_API_DEV_V201.md`
- `restructuring/apps/api/sie_api/v201_dev_audit.py`
- `restructuring/apps/api/sie_api/v201_dev_server_writer.py`
- `restructuring/apps/api/sie_api/v201_dev_rate.py`
- `restructuring/apps/api/sie_api/v201_postgres_contract.py`
- `restructuring/apps/api/tests/test_b05_b06_b07_negative_v201.py`
- `restructuring/apps/api/tests/test_b06_server_writer_v201.py`
- `restructuring/apps/api/tests/test_b04_pg_contract_v201.py`
- `restructuring/apps/api/tests/test_b08_dev_journey_v201.py`
- `docs/implantacao-sie-2-0/GREENFIELD/B05_B08_DESENVOLVIMENTO_YOLO_V201.md`

**Estado:** IN_REVIEW — B04/B05 DEV incluindo edição/exclusão, B03b sintético, B06 auditoria, B07 proteção local e B08 jornada DEV implementados. A aprovação exige checks no SHA final; integração de escrita PostgreSQL, Auth A/B real e GO continuam pendentes, sem migrations adicionais aplicadas no destino.
