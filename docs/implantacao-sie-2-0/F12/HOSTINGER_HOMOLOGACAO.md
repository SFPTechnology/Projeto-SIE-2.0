# Atualização prioritária — 26/10/2026

**Novo fato fornecido pelo titular:** seus projetos, inclusive o SIE 1.0, utilizam arquivos **estáticos na Hostinger em subdomínios**. **Não exigir VPS Hostinger para hospedar a interface F12.** A solução é site estático + backend Python opcional e separado. A orientação anterior de VPS aplica-se apenas se o próprio backend FastAPI for executado no provedor.

A decisão e os comandos vigentes estão em [ARQUITETURA_HOSTINGER_ESTATICA.md](ARQUITETURA_HOSTINGER_ESTATICA.md). Este texto anterior abaixo é preservado como histórico; em caso de conflito, prevalece a arquitetura estática acima.

---

# SIE 2.0 — Hostinger / plano de homologação consultiva F12

**Origem informada pelo titular em 26/10/2026:** Hostinger, URL pretendida `https://sie2.applicationmanager.com.br/`.
**Uso escolhido:** portal web consultivo **anônimo, sem armazenamento de projetos**, somente demonstração sintética.
**Estado:** HOST_IDENTIFIED / PLAN_NOT_VERIFIED / EXTERNAL_HTTPS_NOT_VERIFIED / STAGING_NOT_DEPLOYED / PRODUCTION_NO_GO.

## 1. O que se sabe e o que não se sabe

| Item | Evidência | Estado |
|---|---|---|
| Provedor | declaração explícita do titular | CONFIRMADO |
| URL | declaração explícita do titular | CONFIRMADO COMO DESTINO PRETENDIDO |
| Domínio responde, certificado e conteúdo | consulta pública nesta sessão não retornou resposta verificável; isso não prova falha do site | NÃO VERIFICADO |
| Tipo do plano Hostinger (Web, Cloud, Web Apps ou VPS) | não disponível | NÃO VERIFICADO |
| Servidor Python/FastAPI e acesso técnico | não disponível | NÃO VERIFICADO |
| Acesso administrativo, SSH, DNS, firewall e logs | não disponível | NÃO VERIFICADO |
| Homologação técnica/GO | não fornecido | BLOQUEADO |

**Compatibilidade:** documentação oficial da Hostinger limita Python com controle do runtime aos planos VPS; plano Web/Cloud tradicional não permite usar este backend FastAPI. A oferta gerenciada Web Apps descreve runtimes JavaScript/Node, não garante execução de FastAPI. Portanto, **não instalar** o backend na hospedagem existente sem confirmar qual é o produto contratado. Fontes: https://www.hostinger.com/support/which-programming-languages-and-frameworks-are-supported-at-hostinger/ e https://www.hostinger.com/web-apps-hosting .

## 2. Fluxo escolhido, sem substituir o site atual

- Reutilizar branch F12 isolada, nunca a `main`, dados de clientes ou banco existente.
- Solicitar/inventariar plano Hostinger no hPanel em acesso autenticado. **Não enviar senhas nem tokens na conversa.**
- **Se VPS com Python:** provisionar diretório/usuário de homologação isolado, ambiente Python 3.12 e virtualenv, variáveis `SIE_ENV=production`, `SIE_F12_WEB_ROOT`. Executar `sie_api.f12_consultative:app` em `127.0.0.1:8080` atrás de proxy HTTPS; o endereço externo definitivo só após aceite.
- **Se Web/Cloud/Managed Web Apps sem Python:** é possível apresentar HTML estático, porém **a simulação não funcionará** sem API FastAPI em VPS/serviço Python separado. Não fingir que o site completo está implantado. Avaliar VPS ou integração explícita com backend isolado antes de avançar.
- Registrar domínio, IP/identificador do serviço, SSL/TLS, portas, MFA e usuários administradores no hPanel ou inventário seguro. Nunca copiar segredo ao GitHub.
- Identificar subdomínio/ambiente **real de homologação** sem redirecionar nem modificar o domínio `sie2.applicationmanager.com.br` atualmente em uso.
- Implantar apenas após checagem dos gates e autorização de mudança. Instalação em homologação não valida engenharia elétrica.

## 3. Contrato de segurança e verificações

O entrypoint **único** para o portal consultivo é `sie_api.f12_consultative:app`, não `sie_api.main:app`.
Rotas expostas: `GET /`, arquivos `consultivo.js`/`consultivo.css`, `GET /api/v1/health`, `POST /api/v1/circuitos/analisar`.
`/docs`, `/openapi.json`, `/api/v1/local/projetos` e demais APIs de escrita devem retornar 404. O cálculo sempre retorna `liberado_para_uso_normativo=false`. Não configurar `SIE_LOCAL_DB_PATH` ou `SIE_LOCAL_API_TOKEN`.

SSL público, redirecionamento HTTPS, limites do proxy e WAF/rate-limit, logs, backups das configurações, monitoramento/alertas e autorização administrativa continuam exigíveis. O portal é anônimo por desenho; a hospedagem/CI/CD não pode ter acesso administrativo anônimo.

### Preflight de endereço — sem implantação nem escrita

No checkout F12, **primeiro** validar o alvo sem acessar a rede:

```bash
python scripts/f12_hostinger_preflight.py
```

Para ler **somente** HTTPS da origem informada, após configurar um ambiente autorizado:

```bash
python scripts/f12_hostinger_preflight.py --live --url https://sie2.applicationmanager.com.br/
```

Esse comando usa apenas GET, rejeita redirecionamentos para outros hosts e **não** toca DNS/SSH, hPanel, backups ou serviços instalados. Ele verifica se o portal consultivo já existe e se rotas restritas estão inacessíveis. Se o site antigo estiver no ar, o resultado esperado é `UNVERIFIED_OR_NOT_READY`, **não** um pedido para sobrescrevê-lo.

O comando `--live` **não deve ser executado no CI** nem usado sozinho como aceitação de produção. O resultado mesmo bem-sucedido nunca altera `production_authorized=false` e `staging_approved=false`.

## 4. Aceitação da Etapa 1 no provedor

- [x] Provedor e URL pretendida identificados pelo responsável.
- [x] Entry point minimalista consultivo construído, QA local API/Chromium/segurança concluído antes da hospedagem.
- [ ] Plano do produto Hostinger, runtime e acesso técnico identificados (VPS ou alternativa).
- [ ] Ambiente de homologação independente existente e URL real documentada.
- [ ] Certificado confiável, HTTPS público e renovação testados, sem alteração do site existente.
- [ ] Segregação e permissões administrativas verificadas; backups de configuração, logs, firewall e ingress avaliados.
- [ ] Smoke com sessão de navegador sobre a URL de homologação e validação de rotas restritas.
- [ ] Decisão GO/NO-GO institucional, com rollback, antes da futura implantação controlada.

**Estado da F12:** HUMAN_REQUIRED. A escolha de hospedagem e URL removeu apenas a dúvida sobre o destino pretendido; **não** comprova funcionamento, DNS, SSL, identidade, capacidade Python, permissão de alteração ou homologação.
