# F12 — relatório de execução e checkpoint

**FASE:** F12 — Liberação, implantação e operação controlada  
**ESTADO:** HUMAN_REQUIRED para o gate de produção; preparação técnica parcialmente implementada e em validação. Não declarar DONE.  
**ORIGEM:** `feat/f11-qa-integrado` / `11643cf3ad7da2e6182183c6071148f924bfe741`.  
**BRANCH:** `feat/f12-liberacao-controlada`. Sem merge na `main`, sem deploy ou migração real.

## Evidência do handoff
GitHub consultado em 25/10/2026: F11 SHA documental com workflows API `40183189791`, AIOX `40183189740` e Chromium `40183189754`, todos `completed/success`; registro canônico F11 `DONE` para software local. Homologação normativa e produção continuam rejeitadas pela F11.

## Tarefas e evidências (status, não alegação de aceite)
| Task | Status | Evidência / condição faltante |
|---|---|---|
| 12.01 Manifesto | PREPARADO | `MANIFESTO_RELEASE.md/.json` com SHA base; conferir HEAD final, locks e checksums de build |
| 12.02 Secrets/permissões | PARCIAL | `CHECKLIST_GO_NO_GO.md`, identidade local conhecida; credenciais, IAM, segregação e logs PROD não auditáveis nesta sessão |
| 12.03 Migração/restore | PARCIAL | `PLANO_IMPLANTACAO_ROLLBACK.md`, F03 reversible e F11 restore offline; repetir ensaio isolado no workflow F12, homologação representativa pendente |
| 12.04 Infra e observabilidade | PARCIAL | `PLANO_MONITORAMENTO_SUPORTE.md`; HTTPS real, dashboard e alarmes não demonstrados |
| 12.05 Pacote e documentação | PARCIAL | manuais, notas, manifesto; build reproduzível, checksum e assinatura não produzidos |
| 12.06 Pré-produção | PENDENTE | Sem ambiente de homologação externo aprovado; smoke/E2E/restore próprios ausentes |
| 12.07 Autorização | HUMAN_REQUIRED | `REGISTRO_MUDANCA.md` é NO-GO; falta autorização específica |
| 12.08 Deploy | BLOQUEADO | NÃO EXECUTADO; requer 12.06/07 e gates aprovados |
| 12.09 Operação | PENDENTE | Playbook criado, nenhum indicador pós-deploy real; `RELATORIO_POS_IMPLANTACAO.md` não executado |
| 12.10 Política normativa | PREPARADO | `POLITICA_NORMATIVA_ASBUILT.md`; calendário e homologação profissional pendentes |

## Implementações e testes
- Story F12 criada antes do código e branch aberta no SHA F11 exato.
- `scripts/f12_release_gate.py`: valida manifesto, estado F11 e ancestralidade Git e recusa pedidos de produção.
- `restructuring/apps/api/tests/test_f12_release_gate.py`: sete testes focados de invariantes/negação; não confundir adição com execução.
- `.github/workflows/sie-f12-release-safety.yml`: CI read-only, sem deploy, com testes negativos e ensaio de recuperação em fixtures.
- **Situação dos testes F12 neste checkpoint:** CI confirmado no SHA de código `436edb321ec52a0ee8b7971a698641306692de2a`: API `40246991785` **1.209 passed, 1 warning**; Chromium `40246991743` **36 passed**; AIOX `40246991728` **lint/typecheck/test/build success**; F12 safety `40246991712` **7 testes de release + 19 lifecycle/backup/restore/segurança passaram**. A geração de documentos após esse SHA exige recheck do SHA final. Não houve execução local do repositório completo nesta sessão; GitHub Actions é a evidência.

## Gates e blockers
G01–G08: pendências conforme `CHECKLIST_GO_NO_GO.md`; G09/G10 não executados. Dev/QA local F11 não substitui identidade, TLS, restore de produção, caso de engenharia profissional, autorização, rollout ou saúde pós-deploy. Operação real e homologação elétrica não liberadas.

## QA3
Três pareceres separados estão em `QA-01.md`, `QA-02.md` e `QA-03.md`. QA-01 APROVADO para controles de preparação e BLOQUEADO para release; QA-02 PENDENTE/BLOQUEADO para homologação profissional; QA-03 APROVADO para recuperação/negação local e BLOQUEADO para infraestrutura/identidade de produção. As três avaliações são perspectivas da mesma LLM, não auditorias humanas independentes. 

**Correções após a primeira execução:** verificação de escopo dos arquivos alterados no Git e exigência de código de saída 2 no teste de recusa de produção. Regressão reexecutada com sucesso no run `40246991712`.

**Commit de código testado:** `436edb321ec52a0ee8b7971a698641306692de2a`; última documentação/estado deverá obter novos CI no próprio SHA antes de ser considerada íntegra.

## Próximo marco
Retomar **F12** após comprovar controles faltantes; **não iniciar encerramento F00–F12** como versão liberada. Nenhuma tarefa requer preenchimento manual de planilha pelo usuário.

## Execução adicional — preparação automatizada multiagente, 25/10/2026
**Base de retomada:** `d12d7ee14a4b3a7ef658beea63740d834b241487`. **Plano:** `PLANO_EXECUTIVO_FECHAMENTO_GATES.md` (A01–A08; papéis automatizados especializados, não oito operadores humanos).

**Código W1–W4:** `scripts/f12_bundle.py`, `scripts/f12_staging_smoke.py`, workflow F12, testes adversariais de empacotamento e revisão do gate de escopo. São mudanças restritas à branch F12, sem alteração do motor, bancos ou produção. Pacote de fonte não é release profissional.

**SHA de código com CI completo:** `d7b55a7f3a8ec3eb15ff06a9478b8936134f61ad`. API `40248897962` (**1210 passed, 1 warning**); Chromium `40248897906` (**36 passed**); AIOX `40248897831` (**success**); F12 `40248897899` (**8 testes F12, 19 de lifecycle/restore, dois builds determinísticos, verificação e recusa de adulteração, smoke HTTPS loopback, success**). Bundle de 127 arquivos e SHA-256 `6e29e1f980d50b4a0d394d863915f6660bfba029a1b797eff0f85deebc7bdcfa`. **O commit documental posterior precisa do seu próprio CI**; o hash citado pertence apenas ao pacote do commit de código.
 
**Auditoria da realidade:** não há projeto Supabase conectado identificado como SIE 2.0, somente nomes de outras aplicações. DNS/domínio real, identidades, HTTPS externo, acesso por usuário/projeto, dashboard, custo e janela de deploy não foram demonstrados. Foram testados apenas fixtures/loopback, com `SIE_ENV=production` para confirmar negação da persistência local. Ver `AUDITORIA_AMBIENTE_IDENTIDADE.md`.

**Pontos externos, issue #7:** completar G02–G08 com fatos e autoridades pertinentes; G09–G10 (deploy e pós-deploy) NÃO EXECUTADOS. `DOSSIER_AUTORIZACAO_RELEASE.md` registra critérios de aceite sem inventar laudos, assinaturas, custos ou aprovação. Pareceres QA-01/02/03 atualizados: preparação técnica local aprovada onde testada; produção/homologação profissional bloqueadas.

**Decisão:** `F12 = HUMAN_REQUIRED`, `NO-GO` para release real, preservados `main`, produção e homologação elétrica. Não avançar para encerramento F00–F12 como sistema publicado.

## Complemento: Etapa 1 em perfil WEB CONSULTIVO — execução 25/10/2026

**Decisão:** o titular declarou já possuir hospedagem e selecionou primeira versão `web consultiva`. Não há evidência do URL/provedor SIE nas configurações acessíveis, portanto não foi possível testar nem alterar o ambiente externo. Isso **não** invalida o aceite local: redefine o alvo como *web anônima sintética sem persistência*, diferenciado de uso profissional.

**Implementado no commit de código `270fa3c1e9589479d79c38b50da89100719b62ae`:**
- `sie_api.f12_consultative:app`, entrada de navegador desacoplada da API local, permite exclusivamente `GET /api/v1/health` e `POST /api/v1/circuitos/analisar`, além de `/` e arquivos estáticos da página. Recusa `/api/v1/local/**`, `/docs`, `/openapi.json`, emissão/recuperação de artefatos e demais rotas, mesmo com token local configurado.
- Página `consultivo-web/`, responsive/dark, apenas sintética; sem credenciais, sessões de cliente, projetos, persistência, conformidade ABNT ou aprovação.
- Política de CSP/no-store/nosniff/anti-iframe, MIME/limite de corpo e teste de segurança negativo. Há risco de abuso de tráfego sem ingress com rate-limit e limite de tamanho no provedor: exigência G03.
- Guia específico `PERFIL_WEB_CONSULTIVO_IMPLANTACAO.md`: comando de ensaio em loopback, parâmetros, porta privada, integração com proxy HTTPS e critérios de saúde.

**Verificado em CI no SHA de código `270fa3c1e9589479d79c38b50da89100719b62ae`:**
- `40259295509` API **1215 passed, 3 warnings**.
- `40259295504` Chromium **37 passed**; inclui browser real da página consultiva, simulação e negação de projetos locais.
- `40259295562` AIOX quality success.
- `40259295533` F12 safety **8 + 19 + 5 passed**; pacote QA 134 arquivos, dois builds iguais, SHA-256 `d01b6a04334a36c82e98141a1c0b37e8dc5bd5a86341dde93ec3cfe66daa10d8`, checksum verificado e alteração de pacote recusada. O SHA-256 é específico do commit de código; documentos de acompanhamento posteriores geram checksum diferente.

**Risco residual:** Etapa 1 IMPLEMENTADA e TESTADA como componente local de homologação, mas **não concluída quanto à integração com a hospedagem existente**. TLS público, hostname, identidade de operação, observabilidade, defesa contra abuso, pacote de contêiner/lock, backup representativo e liberação formal permanecem pendentes. Não houve deploy, DNS, atualização de secrets, banco ou `main`. G09/G10 nunca foram simulados como real.

**Decisão:** manter `F12 HUMAN_REQUIRED` / `NO-GO` para produção, sem reabrir F11 ou etapas aprovadas da F12.
