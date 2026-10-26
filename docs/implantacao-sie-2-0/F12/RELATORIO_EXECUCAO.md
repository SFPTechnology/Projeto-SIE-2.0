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
