# Story SIE-B-V201 — Auth, validação de sessão e API segura

**Plano:** SIE 2.0 V2.0 revisão 2.0.1; **entrada:** GA PASS **somente para desenvolvimento**; **base:** `fbf8b957015ba24dfd29167d9d3fe259db979876`; **branch:** `feat/v201-bloco-b-auth-api`.

## Critérios de aceite
- [x] B01: especificar login/confirmar e-mail/recuperar/logout, redirect allowlist e configuração sem secrets no frontend.
- [x] B02: novas rotas autenticadas falham fechadas sem bearer, tokens errados/expirados/forjados; usar Auth Supabase como verificador confiável e ignorar metadata do browser na autorização.
- [x] B02: extrair sub UUID verificado e negar usuário Auth anônimo; nunca usar `service_role` no navegador; preservar rotas legadas fora do prefixo novo.
- [x] B03a: conferir RLS/grants read-only e matriz negativa; nenhum teste de A/B real declarado sem identidades remotas. **B03a documental, não B03b.**
- [x] B04 **em DEV**: criar/listar/renomear projetos owner-only, versão otimista, revisões idempotentes, clone com remapeamento de 4 entidades, selagem, histórico e read-back persistente. Recurso local opt-in, não remoto.
- [ ] B05 **parcial em DEV**: criar ambientes, cargas, circuitos e vínculos, lote transacional com rollback; atualização/exclusão granular, API PostgreSQL e persistência remota ainda pendentes.
- [ ] B03b **parcial em DEV**: testes negativos A/B simulados sobre rotas B04/B05, sem JWT real remoto. B03b completo exige concluir B05.
- [ ] Integração remota: não ativar escrita no Supabase sem A03/A04 aplicadas, read-back e autorização específica.
- [ ] B06–B08: auditoria, hardening, E2E e handoff GB; não declarar GB PASS por só B01/B02.
- [ ] CI do SHA final; pelo menos os testes novos e regressão da API verificados. **API do SHA 91adafa... aprovada com 1308 testes; novo SHA de handoff ainda em verificação.**

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

**Estado:** IN_REVIEW — B04 desenvolvimento implementado; B05 base e lote transacional implementados com dados sintéticos, B03b testes negativos locais. B05 restante, B06–B08, integração PostgreSQL/Auth A/B real e gate GB permanecem pendentes. DEV exige `SIE_V201_DEV_WRITES=1`, `SIE_ENV` dev/test e DB SQLite absoluto; produção desabilitada. GF02 é a única migration aplicada remotamente.
