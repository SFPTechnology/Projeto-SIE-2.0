# Workflow SDC T2 SEM-MOTOR — Remediação QA automática (YOLO)

## Objetivo

Executar, sem prompts intermediários, a remediação completa do gate `FAIL` da story
`T2-SEM-MOTOR-1`: fechar as lacunas de teste, eliminar as 11 falhas globais, tornar
o lint integral reproduzível, recuperar o CodeRabbit no WSL, repetir todos os gates,
concluir a Task 6, mover a story para `InReview` e acionar uma nova validação do QA.

O contrato executável está em:
`.aiox-core/development/workflows/story-development-cycle-t2-sem-motor-qa-remediation-yolo.yaml`.

## Fontes de verdade

- Story: `docs/stories/story-T2-SEM-MOTOR-1-ausencia-motor-tipado.md`
- Gate vigente: `docs/qa/gates/T2-SEM-MOTOR-1-ausencia-motor-tipado.yml`
- Plano: `Arquivos_Diversos/Correção_2/plano-T2-sem-motor.md`
- Subapp: `sistema-de-instala-es-el-tricas-sie-main/`

Não há elicitação em runtime. Falta de artefato, ambiguidade de escopo, necessidade
de credencial nova ou esgotamento das iterações resulta em `block_and_log`.

## Fluxo

```text
@aiox-master  baseline + trava de escopo
      |
      v
@dev          testes MOD-CC/MOD-SEC + 11 falhas + lint
      |
      v
@devops       reparo e execução do CodeRabbit no WSL
      |
      v
@dev          findings bloqueantes do CodeRabbit
      |
      v
@dev          lint -> typecheck -> test -> build -> build:spa
      |                    qualquer falha: remediar e repetir (máx. 3)
      v
@dev          Task 6 + registros + status InReview
      |
      v
@qa           nova revisão + QA Results + gate
```

## Política YOLO

- `interaction_policy: never_prompt`
- Continuação automática somente quando o passo anterior termina com sucesso.
- Até três ciclos de remediação dos quality gates.
- Até duas iterações de auto-fix para finding CodeRabbit `CRITICAL`.
- Falhas não são convertidas em aprovação por baseline presumido, timeout maior ou
  atualização indiscriminada de snapshots.
- O worktree existente é preservado; nenhum arquivo alheio pode ser revertido.
- Não há autorização para commit, push, PR, merge, release, deploy ou migration.

## Regras específicas das correções

1. Os testes novos devem injetar `aprovado: false` em MOD-CC e MOD-SEC e demonstrar
   o caminho de veredito real, inclusive validação e persistência. Os clientes devem
   ser restaurados após cada cenário.
2. A troca da expectativa `SUGESTAO` por `MOD-PROT` só ocorre depois de confirmar o
   contrato aceito nos artefatos existentes; snapshots não são atualizados às cegas.
3. O timeout do catálogo exige causa-raiz. Aumentar o limite só é válido quando a
   medição justificar e a decisão ficar registrada.
4. O lint deve terminar com código 0 sem desativar regra ou excluir escopo para
   esconder erros.
5. O reparo do CodeRabbit deve verificar arquitetura/runtime do WSL, preservar
   credenciais e impedir vazamento de tokens. Se nova autenticação for necessária,
   o workflow bloqueia e registra a dependência externa.

## Gates obrigatórios

Executados no diretório `sistema-de-instala-es-el-tricas-sie-main/`, nesta ordem:

```powershell
npm run lint
npm run typecheck
npm test
npm run build
npm run build:spa
```

Todos precisam retornar código 0 na mesma revisão. O relatório deve registrar
comando, duração, código de saída e resumo.

## Transição e autoridade

- `@dev` conclui a Task 6 e move a story para `InReview` somente após todos os gates
  passarem e não existir `CRITICAL` aberto no CodeRabbit.
- `@dev` atualiza apenas as seções autorizadas da story e preserva `QA Results`.
- `@qa` faz a revisão independente, atualiza `QA Results` e o arquivo de gate.
- A nova revisão pode resultar em `PASS`, `CONCERNS` ou `FAIL`; o workflow nunca move
  a story automaticamente para `Done`.

## Validação do workflow

O YAML deve passar no `WorkflowValidator` do projeto sem erros. Warnings estruturais
devem ser revisados antes da execução. A execução deve persistir estado e evidências
para retomada segura se ocorrer `block_and_log`.

## Registro da decisão

- Data: 2026-08-06
- Responsável: `aiox-master (Orion)`
- Decisão: `ADAPT`
- Base: `story-development-cycle-headless-yolo`
- Justificativa: a base genérica cria story e inclui operações remotas. Esta variante
  começa no gate QA `FAIL`, mantém execução local e termina na nova validação QA.
