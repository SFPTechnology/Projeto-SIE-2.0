# F12 — Execução do Prompt Mestre 2.0 (checkpoint técnico)

Data: 2026-10-26 (America/Sao_Paulo). Repositório: `SFPTechnology/Projeto-SIE-2.0`. Branch: `feat/f12-liberacao-controlada`.
Plano-base da conversa: `PLANO_IMPLEMENTACAO_DESBLOQUEIO_F12_SIE_2_0.md` (SHA-256 `0d65ef49cf6b3999c40163e0c5bbeda19822bb494140e38560838659aa38fd74`). Especificação complementar `F12_EXECUTAR.md`.

## 1. Reconhecimento: modo e autoridade

**MODO B — papéis especializados sequenciais, não subagentes independentes.** A sessão dispõe de leitura/escrita GitHub na branch de trabalho, consulta de workflows e testes no CI. Não há acesso autenticado comprovado ao hPanel Hostinger, ao DNS, a ambiente externo FastAPI, a secrets de produção nem a equipe humana certificadora. **NÃO** executar push em main, merge, publicação, migração de produção, contratação ou alteração DNS.

Constituição `AGENTS.md`/AIOX: papéis de autoria separados logicamente; operações de GitHub exercidas no escopo de trabalho de release/DevOps. Story existente foi reaproveitada, sem novo escopo normativo.

## 2. Candidato técnico e alterações verificáveis

SHA integrado de implementação (pré-documentação): `ff23f0e8a5c9d1e845e5e998df5984866b58ae3d`.
- `scripts/f12_hostinger_static.py`: parâmetro `--site-origin` validador de subdomínio HTTPS da organização; `.htaccess` redireciona ao **próprio ambiente** e não força homologação para produção; manifesto registra origem.
- `restructuring/apps/api/sie_api/f12_consultative.py`: `SIE_F12_STAGING_ORIGIN` opt-in; CORS de um backend de homologação aceita **somente staging** e backend de produção **somente domínio definitivo**. URLs inválidas impedem boot.
- No mesmo backend, corpo JSON POST transmitido em partes passa por limite efetivo antes da desserialização, além do controle prévio por Content-Length; limites de proxy/rate-limit continuam exigidos.
- `scripts/f12_split_preflight.py`: sondagem read-only **separada** da página Hostinger e do serviço Python; prova HTML/assets, vínculo JS à API, health e negativas de rotas privadas. Modo offline por padrão; `--live` demanda dois hosts HTTPS reais; **não** testa POST/CORS/latência/certificado de renovação/rate-limit, nem autoriza produção.
- Testes adversariais: `test_f12_hostinger_static.py`, `test_f12_consultative.py`, `test_f12_split_preflight.py`; F12 Safety CI expandido para nova sonda offline.

## 3. Matriz de execução 12.01–12.10 / agentes

| Task | Responsável funcional | Resultado local | Estado integral / pendência externa |
|---|---|---|---|
| 12.01 manifesto/release | Arquitetura + DevOps | Código/CI rastreados; pacote estático de QA existente | PREPARADO: release frontend+API com dependências imutáveis ainda pendente |
| 12.02 segurança/segredos | Segurança | CORS por ambiente, limite body e testes negativos | PARCIAL: IAM admin, TLS, proxy/rate-limit reais pendentes |
| 12.03 migração/restore | Dados | 19 testes offline F11/F12 reaproveitados | PARCIAL: backup/rollback de infra real não ensaiado; banco de clientes possivelmente N/A para piloto stateless |
| 12.04 infraestrutura/operação | DevOps + SRE | Sonda cindida do frontend/backend pronta em código | PARCIAL: DNS/TLS/health/alertas ao vivo inexistentes |
| 12.05 pacote/manual | DevOps | ZIP estático reproduzível, instrução staging protegida | PARCIAL: artefato backend imutável/SBOM, lock de dependências e runbook final pendentes |
| 12.06 pré-produção | Integração + QA | Testes de API/browser em runner sintético | PENDENTE: staging Hostinger + API externa não implantados |
| 12.07 autorização | Governança | Dossiê, issue #7 | HUMAN_REQUIRED: mudança/escopo/custo/janela/GO assinados ausentes |
| 12.08 implantação | DevOps | Não executada | BLOQUEADO por G01–G08 não atendidos |
| 12.09 pós-deploy | SRE | Playbook planejado | PENDENTE: métricas/alertas/saúde em serviço real |
| 12.10 política normativa | Engenharia | escopo demonstrativo não normativo preservado | PREPARADO: QA aplicável sem parecer profissional para uso real |

**Caminho crítico**: W0 escopo → W1 serviço Python/Hostinger staging reais → W2 pacote completo revisado → W3 smoke integração externo → W4 rollback → W5 alertas reais → W6 QA3/CI SHA final → W7 GO específico → W8 deploy → W9 pós-deploy.

## 4. QA3 — perspectivas especializadas, não pareceres humanos

- **QA-01 arquitetura/código/testes:** favorável ao *incremento local*, com evidências de testes CI; falta a imagem/backend pinado e instalação real. Estado `APROVADO_PREPARACAO`, `BLOQUEADO_RELEASE`.
- **QA-02 engenharia elétrica:** não foram alterados motores/normas, interface continua demonstrativa sem aprovação profissional. Verificar texto e números de exemplo antes do site público. Estado `PENDENTE_RELEASE_NORMATIVO`, sem laudo humano.
- **QA-03 segurança/integridade/UX:** correções em staging, CORS, corpo chunked e sonda dual host; testes negativos exigidos. Falta prova SSL público, ingress/rate-limit, identidade administrativa, logs, backups, alertas e E2E real. Estado `APROVADO_PREPARACAO`, `BLOQUEADO_OPERACAO_REAL`.

## 5. Gates e evidências

| Gate | Estado nesta execução |
|---|---|
| G01 SHA/código/CI | PARCIAL; verificar resultado final dos quatro workflows no commit documental |
| G02 uso profissional/escopo | somente DEMO não normativa; sem aprovação para projeto elétrico |
| G03 segurança/TLS/IAM | PARCIAL local; externo pendente |
| G04 restore/rollback | PARCIAL fixture; staging pendente |
| G05 banco/migração | NAO_APLICAVEL **proposto** ao recorte stateless, não ratificado; rollback de arquivos obrigatório |
| G06 observabilidade | PENDENTE real |
| G07 produto/pacote | PARCIAL: frontend estático QA, backend release não preparado |
| G08 mudança | HUMAN_REQUIRED |
| G09 deploy | NÃO EXECUTADO |
| G10 pós-deploy | NÃO EXECUTADO |

**Regra decisória mantida:** `F12 HUMAN_REQUIRED`, `production_release_allowed=false`, `deployment_executed=false`, `change_approved=false`. QA/CI em branch não fecha G03–G10. Não tratar homologação elétrica como consequência de teste de software.

## 6. Próxima ação única e bloqueio essencial

**Provisionar e autorizar o ambiente segregado de homologação para a API FastAPI e para os arquivos estáticos da Hostinger**, com os endereços HTTPS reais, responsável administrativo, limite de recursos, proxy/rate-limit e logs. Só então executar a sonda cindida:
```bash
python scripts/f12_split_preflight.py --live \
  --site-origin https://<subdominio-de-homologacao>.applicationmanager.com.br \
  --api-origin https://<api-python-https-real>
```
Os valores entre sinais angulares acima são **marcadores ilustrativos**, não hosts criados. Essa sonda faz GET; complementar obrigatoriamente com E2E de browser/POST/CORS/cenários adversariais no staging real.

Sem esses acessos/autorizações, a execução avançou até as tarefas de código comprováveis **e para no gate externo real**, sem deploy/merge.
