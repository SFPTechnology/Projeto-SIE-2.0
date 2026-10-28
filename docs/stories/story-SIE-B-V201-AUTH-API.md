# Story SIE-B-V201 — Auth, validação de sessão e API segura

**Plano:** SIE 2.0 V2.0 revisão 2.0.1; **entrada:** GA PASS **somente para desenvolvimento**; **base:** `fbf8b957015ba24dfd29167d9d3fe259db979876`; **branch:** `feat/v201-bloco-b-auth-api`.

## Critérios de aceite
- [ ] B01: especificar login/confirmar e-mail/recuperar/logout, redirect allowlist e configuração sem secrets no frontend.
- [ ] B02: novas rotas autenticadas falham fechadas sem bearer, tokens errados/expirados/forjados; usar Auth Supabase como verificador confiável e ignorar metadata do browser na autorização.
- [ ] B02: extrair sub UUID verificado e negar usuário Auth anônimo; nunca usar `service_role` no navegador; preservar rotas legadas fora do prefixo novo.
- [ ] B03a: conferir RLS/grants read-only e matriz negativa; nenhum teste de A/B real declarado sem identidades remotas.
- [ ] B04/B05: evolução de CRUD após contrato B02; não ativar escrita remota sem A03/A04 aplicadas e read-back.
- [ ] B06–B08: auditoria, hardening, E2E e handoff GB; não declarar GB PASS por só B01/B02.
- [ ] CI do SHA final; pelo menos os testes novos e regressão da API verificados.

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

**Estado inicial:** IN_PROGRESS.
