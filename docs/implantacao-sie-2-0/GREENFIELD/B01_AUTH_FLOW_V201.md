# B01 — Jornadas de identidade e sessão (V2.0.1)

**Estado:** Implementado no boundary backend; fluxos browser futuros ainda pendentes.
**Projeto autorizado:** `fozrymsidnaxmuvxxfhh`; emissor fixo `https://fozrymsidnaxmuvxxfhh.supabase.co/auth/v1`.

## Contrato
1. Browser utiliza Supabase Auth (SDK publicável) para login, confirmação de e-mail, recuperação e logout; **não** recebe `service_role` ou `sb_secret_*`.
2. Redirecionamentos devem passar na allowlist de origem e caminho: localhost/127.0.0.1:5173 para desenvolvimento e `https://sie2.applicationmanager.com.br/auth/callback` para web autorizada. Nunca permitir origin por parâmetro sem comparação estrita.
3. Novas rotas `/api/v2/sie/*` dependem de bearer JWT. Para suportar Supabase JWT legado e chaves assimétricas, o serviço verifica token usando `GET /auth/v1/user` no **host Supabase fixo**, por HTTPS e com chave publicável. O serviço Auth valida assinatura e expiração. A API rejeita discrepâncias de `sub`, issuer, audience, expiração e role. Claims locais antes da verificação são apenas checks adicionais, **não** autorização.
4. Rejeitar sessões anônimas do Supabase para recursos privados mesmo quando portam role `authenticated`. `user_metadata` nunca decide permissões.
5. Dados reais do usuário ou e-mails não aparecem em erros; `Authorization` nunca entra em logs.
6. MFA/reauth: para ações privilegiadas futuras, exigir `aal2` e sessão recente validados pelo Auth. Não presumir MFA ativado apenas porque existe JWT.
7. Logout e troca de credenciais devem invalidar token no Auth; revogação absoluta requer verificar sessão ativa na plataforma quando necessário.
8. Clientes antigos `/api/v1/*` conservam comportamento para não quebrar a F12; esta adição **não** expõe CRUD.

## Variáveis de ambiente da API
- `SIE_SUPABASE_PUBLISHABLE_KEY`: chave **publicável** do projeto Supabase, somente no ambiente de execução. Necessária para verificar bearer pelo endpoint Auth. Sem configuração, serviço responde 503 (fail closed).
- `SIE_ENV`: continua governando limites das rotas legadas.

## Estado de validação
Testes B01/B02 no CI exercitam o verificador com Auth HTTP simulado, tokens falsos/expirados, audience/issuer errados, identidade cruzada e falta de configuração. **Não comprova Auth real no Supabase**; B03a/B03b remotos continuam pendentes para E02/E06. Nenhuma conta foi criada.
