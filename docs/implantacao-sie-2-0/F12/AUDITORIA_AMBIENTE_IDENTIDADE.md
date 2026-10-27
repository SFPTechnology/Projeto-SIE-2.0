# F12 — inventário e auditoria de infraestrutura, HTTPS e identidade

**Escopo verificado:** checkout público de `SFPTechnology/Projeto-SIE-2.0` no SHA `d7b55a7f3a8ec3eb15ff06a9478b8936134f61ad`; catálogo read-only de projetos Supabase conectados; runner GitHub Actions sintético. **Não é auditoria de um servidor de produção SIE.**

## Estado observado
- API FastAPI em `restructuring/apps/api/sie_api/main.py`: `/api/v1/health` e `/api/v1/projetos/validar` não exigem autenticação. A política CORS aceita apenas origens localhost 5173, mas CORS não equivale a autenticação/IAM.
- Rotas `/api/v1/local/` usam limite de ambiente e peer loopback. `sie_api/storage_api.py` emprega token único de proprietário local; **não há prova de identidade multiusuário, perfis/ACL, MFA, OIDC ou isolamento por tenant aptos à Internet**.
- Requisitos de privacidade/segurança de produção: segredos segregados, autenticação/autorização por projeto, rotação, auditoria, Rate Limit, isolamento, backups e TLS externo pendentes de provedor/ambiente.
- Conector Supabase disponibilizou projetos com nomes `Diagnóstico_Habilitação`, `Projeto_Habilitação` e `Nuclear_Challenge`, **nenhum identificado como SIE 2.0**. Foram observados apenas nomes/metadados; bancos, tabelas, secrets e usuários **não foram consultados ou alterados**.
- Não há contrato de plataforma de deploy SIE (domínio, fornecedor, topologia, política de credenciais, custo e janela) ratificado no repositório desta fase.
- CI `40248897899` realizou smoke HTTPS **somente em 127.0.0.1**, com certificado autofirmado descartável, `SIE_ENV=production`, sem conectar base externa. Resultado `PASS_LOCAL_HTTPS_SYNTHETIC`; persistência local recebeu HTTP 503, rota de health ficou acessível e validação permaneceu declaradamente não normativa.
- CI `40248897906` validou Chromium local; isso não substitui E2E de homologação externa com identidades reais.

## Achados classificados
| ID | Severidade para produção | Evidência | Status / ação |
|---|---|---|---|
| INFRA-01 | CRÍTICA | Provedor, domínio, destino e infraestrutura SIE não comprovados | HUMAN_REQUIRED, identificar projeto/tenant e inventário |
| IAM-01 | CRÍTICA | Token local single-owner; API consultiva possui rotas sem autenticação | Implementar IAM/RBAC/ACL real antes de expor dados, validar acesso cruzado |
| TLS-01 | ALTA | SSL testado apenas com certificado autofirmado ephemeral | Certificado válido, renovação e DNS/HTTPS externo pendentes |
| SECRET-01 | ALTA | Sem acesso validado ao secret store do ambiente SIE, nem checklist IAM assinável | Auditar configuração real por identidade autorizada, nunca extrair valores |
| OBS-01 | ALTA | Playbook e métricas propostas, sem coleta/alerta da plataforma real | Dashboard, alarmes e runbook ensaiados com SLO/RPO/RTO |
| DB-01 | ALTA | F03/F11 SQLite local; Supabase do SIE não identificado | Definir banco, ACL, migrações, segregação e estratégia de restore real |

**Decisão:** testes locais de protocolo e fail-closed APROVADOS, infraestrutura/identidade PROD **NÃO APROVADAS**. Não selecionar por aproximação um projeto pertencente a outro sistema.

## Atualização de identificação Hostinger — 26/10/2026
**INFRA-01 parcialmente esclarecido:** provedor Hostinger; domínio-alvo https://sie2.applicationmanager.com.br/. O titular os informou diretamente. Continua **PENDENTE** tipo do plano (VPS versus Web/Cloud ou Web Apps), recursos de aplicação Python, permissões de administração, hostname de homologação, SSL real, logs e observabilidade.

A consulta web não forneceu conteúdo verificável (`cache miss`), e a ferramenta de execução não resolveu o hostname. Não classificar como falha de DNS/HTTPS do servidor real com base em limitações da ferramenta. Testes do `f12_hostinger_preflight.py` foram offline com fixtures; nenhum atestado de TLS público.

**Escopo IAM:** web consultiva anônima sem contas nem armazenamento de projetos; RBAC de clientes é inaplicável ao piloto sintético, mas identidade administrativa e controles do provedor continuam obrigatórios. O material de engenharia não está homologado para uso profissional.
