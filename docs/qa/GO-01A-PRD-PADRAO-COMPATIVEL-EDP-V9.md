# GO-01A — Prontidão Operacional da Release 1 EDP V9

**Data da avaliação:** 2026-07-26  
**Escopo:** `docs/prd/PRD-PADRAO-COMPATIVEL-EDP-V9.md`  
**Autoridade desta avaliação:** @devops (CI/CD e operação)  
**Decisão:** **REPROVADO PARA ATIVAÇÃO — BLOCK**

## 1. Resumo executivo

O gate GO-01A não pode ser aprovado no estado observado. Existem scripts locais de qualidade e um procedimento manual de publicação em produção, mas faltam evidências aprovadas de CI, CodeRabbit, homologação isolada, rollout controlado por feature flag, rollback operacional exercitado e observabilidade ativa. A Release 1 deve permanecer desativada, conforme AC-37 e a seção 5.4 do PRD.

Esta decisão cobre somente a autoridade de @devops. As aprovações correspondentes de @architect e @qa também permanecem necessárias.

## 2. Matriz de evidências

| Domínio GO-01A | Status | Evidência observada | Bloqueio para aprovação |
|---|---|---|---|
| CI e gates | **REPROVADO** | O app declara `lint`, `typecheck`, `test` e `build` em `sistema-de-instala-es-el-tricas-sie-main/package.json`; não há workflow em `.github/workflows/` no workspace nem no app. A árvore do app está com dezenas de alterações não commitadas, portanto não representa baseline liberável. | Implantar CI reproduzível e registrar execução verde de todos os gates sobre o candidato exato da Release 1. |
| CodeRabbit constitucional | **REPROVADO** | `.aiox-core/core/quality-gates/quality-gate-config.yaml` habilita CodeRabbit e bloqueia severidade `CRITICAL`; não foi localizado relatório aplicável ao candidato EDP V9 comprovando zero `CRITICAL`. | Executar CodeRabbit contra o candidato da release, resolver todos os `CRITICAL` e anexar relatório rastreável. |
| Ambiente de homologação | **PENDENTE** | Existe `hostinger-staging/`, porém seu README descreve SSR com `srvx`; `docs/DEPLOY-SPA-HOSTINGER.md` declara que produção usa SPA estática e classifica esse README como desatualizado. Não há evidência de ambiente isolado, configuração validada, dados de teste, responsáveis ou homologação EDP V9. | Formalizar ambiente equivalente à produção, segregado, com configuração, acesso, dados, smoke e aceite registrados. |
| Rollout / feature flag | **REPROVADO** | O procedimento vigente é upload manual com substituição dos arquivos no Hostinger. Não foi encontrada flag operacional para ativar/desativar a Release 1 EDP V9 nem plano de rollout progressivo com critérios de avanço/parada. | Implementar controle de ativação reversível, ownership, segmentos/percentuais, critérios de avanço e kill switch testado. |
| Rollback operacional | **REPROVADO** | `docs/DEPLOY-SPA-HOSTINGER.md` orienta apagar os arquivos existentes antes do upload e documenta incidentes anteriores, mas não define rollback EDP V9 versionado, atômico, com RTO/RPO, gatilhos, responsável e evidência de ensaio. | Criar runbook de rollback do artefato e da configuração, preservar versão anterior recuperável e comprovar ensaio em homologação. O rollback não pode reativar escrita legada ou dual-write. |
| Observabilidade | **REPROVADO** | O procedimento contém verificações manuais por `curl`, console e smoke; `.env.example` apenas reserva configuração de Sentry. Não há evidência de instrumentação ativa, dashboards, alertas, SLI/SLO ou sinais específicos para divergências, migração, estados obsoletos e bloqueios EDP V9. | Instrumentar sinais do PRD, definir alertas/limiares, dashboards, retenção, correlação e responsáveis; validar detecção em homologação. |

## 3. Condições mínimas para nova avaliação

1. Candidato de Release 1 identificável e estável, com `npm run lint`, `npm run typecheck`, `npm test` e `npm run build` verdes.
2. CodeRabbit concluído com zero issues `CRITICAL`, conforme a Constituição.
3. Homologação equivalente à produção aprovada por @qa e arquitetura operacional aprovada por @architect.
4. Feature flag/kill switch e rollout progressivo exercitados.
5. Rollback operacional ensaiado, com evidência, RTO/RPO, gatilhos e ownership.
6. Observabilidade EDP V9 ativa e teste de alerta realizado.

## 4. Decisão operacional

- **Ativar Release 1:** **NÃO AUTORIZADO**
- **Manter desenvolvimento e validação interna:** **AUTORIZADO**, sem exposição a usuários
- **Reavaliação:** obrigatória quando qualquer evidência de build, ambiente, rollout ou risco operacional mudar
- **GO-01B:** não avaliável como aprovado enquanto GO-01A permanecer inválido

## 5. Referências

- `docs/prd/PRD-PADRAO-COMPATIVEL-EDP-V9.md` — GO-01A, AC-37, NFR9 e NFR12
- `docs/prd/RV-01-PRD-PADRAO-COMPATIVEL-EDP-V9.md` — infraestrutura `FAIL/BLOCK` e GO-01A pendente
- `sistema-de-instala-es-el-tricas-sie-main/docs/DEPLOY-SPA-HOSTINGER.md`
- `sistema-de-instala-es-el-tricas-sie-main/hostinger-staging/README-HOSTINGER.md`
- `.aiox-core/constitution.md` — Quality First
- `.aiox-core/core/quality-gates/quality-gate-config.yaml`

## 6. Reexecução operacional

**Data:** 2026-07-26  
**Decisão:** **REPROVADO PARA ATIVAÇÃO — BLOCK**

O repositório continua sem workflow em `.github/workflows/` tanto na raiz
quanto no aplicativo. Os scripts locais `lint`, `typecheck`, `test` e `build`
existem, mas não há candidato EDP V9 concluído, story aprovada ou execução CI
rastreável. O workspace e o aplicativo também contêm mudanças preexistentes
sem baseline liberável.

```yaml
devops_handoff:
  candidate_story: null
  qa_pass: false
  pre_push_started: false
  remote_operations_authorized: false
  deploy_runbook: null
  deploy_authorized: false
  push_executed: false
  pull_request_created: false
  deployment_executed: false
```

Pre-push, push, PR, release e deploy não foram iniciados. Além do gate
operacional reprovado, o manifesto headless mantém operações remotas e deploy
sem autorização.

---

Relatório emitido por @devops (Gage). Nenhum push, PR, deploy ou alteração operacional foi executado.
