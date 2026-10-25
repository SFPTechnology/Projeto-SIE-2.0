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
- `restructuring/apps/api/tests/test_f12_release_gate.py`: cinco testes focados de invariantes/negação; não confundir adição com execução.
- `.github/workflows/sie-f12-release-safety.yml`: CI read-only, sem deploy, com testes negativos e ensaio de recuperação em fixtures.
- **Situação dos testes F12 neste checkpoint:** CI e QA da F12 ainda a confirmar no SHA final. Não há execução local do repositório completo na sessão; GitHub é a fonte das execuções remotas.

## Gates e blockers
G01–G08: pendências conforme `CHECKLIST_GO_NO_GO.md`; G09/G10 não executados. Dev/QA local F11 não substitui identidade, TLS, restore de produção, caso de engenharia profissional, autorização, rollout ou saúde pós-deploy. Operação real e homologação elétrica não liberadas.

## QA3
QA-01, QA-02 e QA-03 requerem pareceres e evidências próprias ao fim da preparação elegível. Não declarar aprovados antecipadamente.

## Próximo marco
Retomar **F12** após comprovar controles faltantes; **não iniciar encerramento F00–F12** como versão liberada. Nenhuma tarefa requer preenchimento manual de planilha pelo usuário.
