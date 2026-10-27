# F12 — Perfil WEB CONSULTIVO / instalação em hospedagem existente

**Decisão do titular (25/10/2026):** hospedagem já contratada/definida; primeira versão como **web consultiva**, sem uso profissional certificado, sem projeto persistido em servidor e sem login de cliente.

**ESTADO:** pacote de homologação em branch F12, **NÃO publicado**. O nome do provedor, domínio e destino técnico da hospedagem não aparecem em configuração/artefatos verificáveis até esta revisão. GitHub hospeda código, não constitui confirmação de hospedagem da aplicação. Não usar Supabase de outros projetos.

## Contrato técnico de implantação do preview

- **Entry point correto:** `sie_api.f12_consultative:app`, **não** `sie_api.main:app` na URL pública.
- **Frontend separado:** `docs/implantacao-sie-2-0/F12/consultivo-web/{index.html,consultivo.js,consultivo.css}`; somente mesma origem, sem credencial de usuário nem armazenamento persistente.
- **Rotas expostas:** `GET /`, `GET /index.html`, `GET /consultivo.js`, `GET /consultivo.css`, `GET /api/v1/health` e `POST /api/v1/circuitos/analisar`.
- **Rotas explicitamente indisponíveis:** `/api/v1/local/**`, `/api/v1/modelo/**`, `/api/v1/normas/**`, `/api/v1/projetos/**`, `/docs`, `/openapi.json`, `/artefatos.html`, listagens de arquivos, APIs de upload, contas e geração de documentos persistidos. Bloqueio também se houver token local no processo (teste adversarial).
- **Sem DB:** `SIE_LOCAL_DB_PATH` e `SIE_LOCAL_API_TOKEN` não devem ser configurados. Não criar schemas, buckets, usuários ou migrar dados de produção para esse modo.
- **Cabeçalhos:** CSP restritiva, no-store, nosniff, X-Frame-Options DENY, no-referrer. HTTPS/TLS deverá ser encerrado no proxy/serviço de hospedagem com certificado público válido antes de expor.
- **Limitação:** cálculo resistivo sintético não homologado, sem dimensionamento elétrico aprovado, ART ou parecer de conformidade. O usuário final vê avisos destacados.

## Instalação de ensaio em máquina/ambiente segregado com Python 3.12

No checkout da branch F12 correspondente ao SHA dos testes:

```bash
python -m venv .venv
. .venv/bin/activate
python -m pip install -e ./restructuring/apps/api
export SIE_ENV=production
export SIE_F12_WEB_ROOT="$PWD/docs/implantacao-sie-2-0/F12/consultivo-web"
python -m uvicorn sie_api.f12_consultative:app --host 127.0.0.1 --port 8080
```

**Atenção:** isto é para ambiente autorizado de **homologação/teste isolado**; `--host 127.0.0.1` limita acesso local. No caso de hospedagem por contêiner, o processo pode escutar na rede interna do contêiner, mas somente um proxy autenticado/configurado deve expor HTTPS. Não abrir a porta interna diretamente na Internet. Dependências do projeto ainda têm faixas sem lock completo; para liberação de produção será exigida imagem/dependências imutáveis e revisadas.

## Checklist técnico de verificação antes de conectar domínio

1. `GET http://127.0.0.1:8080/` → 200, texto `Não homologado` e ativos carregados.
2. `GET http://127.0.0.1:8080/api/v1/health` → 200 e `status=ok`.
3. `POST /api/v1/circuitos/analisar` com corpo sintético JSON → 200 somente se `liberado_para_uso_normativo=false`.
4. `GET /api/v1/local/projetos`, `/docs`, `/openapi.json`, `/api/v1/normas/catalogo` → 404, inclusive com token simulado.
5. Outros verbos e MIME incorretos → 404/415; corpo acima do limite → 413.
6. Proxy HTTPS externo: certificado público válido, HTTPS forçado, TLS seguro, registro sem dados sensíveis, rate-limit e limites para upload/memória/CPU do processo; simular falhas e registrar observabilidade real.
7. Guardar o pacote com SHA/checksum e evidenciar teste end-to-end, rollback, custo e decisão de liberação.

**Atenção à identidade:** como o preview é público anônimo e não armazena contas/projetos, não exige RBAC de clientes neste recorte. A infraestrutura, o CI/CD e o acesso administrativo **exigem** identidades específicas, MFA quando aplicável, mínimo privilégio e segregação. Se login, dados pessoais, persistência ou serviços multiusuários forem adicionados, abrir novo incremento e testar IAM/ACL/IDOR antes de qualquer exposição.

**Gates reais não satisfeitos:** provedor e domínio não identificados nos artefatos; HTTPS público, WAF/rate-limit, observabilidade e aprovações de mudança ausentes; release profissional sempre bloqueado. Não confundir rodar o processo em modo `SIE_ENV=production` com deploy validado em produção.

**Referências:** `docs/implantacao-sie-2-0/F12/RELATORIO_EXECUCAO.md`, `CHECKLIST_GO_NO_GO.md`; [issue de governança #7](https://github.com/SFPTechnology/Projeto-SIE-2.0/issues/7).
