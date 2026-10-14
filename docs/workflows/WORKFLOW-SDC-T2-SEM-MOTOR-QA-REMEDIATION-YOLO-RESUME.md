# SDC T2 SEM-MOTOR — Retomada final YOLO

Este workflow retoma a execução bloqueada de `T2-SEM-MOTOR-1` no ponto exato em
que o CodeRabbit falhou. Ele não repete os testes, lint ou typecheck já comprovados
no estado fonte.

Workflow: `.aiox-core/development/workflows/story-development-cycle-t2-sem-motor-qa-remediation-yolo-resume.yaml`

## Pré-condições obrigatórias

- Estado fonte `.aiox/story-development-cycle-t2-sem-motor-qa-remediation-yolo-2026-08-06-state.yaml` permanece `blocked` por `CODERABBIT-WSL-AVX2`.
- Runner Linux/WSL compatível com o binário oficial CodeRabbit, preferencialmente
  com AVX2, já autenticado.
- Diff T2 isolado por commit/worktree autorizado ou método oficial equivalente.
- Nenhum segredo novo, binário não oficial ou emulação.

Se qualquer condição falhar, o workflow registra `block_and_log` e preserva a story
em `InProgress`.

## Sequência

```text
estado bloqueado + runner compatível
              |
              v
@devops: CodeRabbit real + relatório sanitizado
              |
              v
@dev: resolver CRITICAL (máx. 2 iterações)
              |
              v
@dev: lint -> typecheck -> test -> build -> build:spa
              |
              v
@dev: concluir Task 6 + InReview
              |
              v
@qa: nova revisão + gate formal
```

## Critérios de término

O workflow só termina com sucesso quando CodeRabbit, os cinco gates, Task 6, status
`InReview` e a nova revisão QA tiverem evidência correspondente. `CONCERNS` ou `FAIL`
do QA são resultados formais, não aprovação implícita.

## Retomada

```text
$aiox-master execute o workflow story-development-cycle-t2-sem-motor-qa-remediation-yolo-resume em modo YOLO
```

O workflow original continua preservado como histórico; este arquivo é a continuação
auditável e não deve ser confundido com uma nova implementação da story.
