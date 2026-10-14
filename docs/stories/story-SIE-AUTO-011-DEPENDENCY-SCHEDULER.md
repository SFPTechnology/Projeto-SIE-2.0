# Story SIE-AUTO-011 — Escalonador determinístico de atividades do SIE

**Estado inicial:** READY. **Prioridade:** P1.
**Fonte:** META-PROMPT SIE-AUTO-ORCHESTRATOR v2.0 (seções 5–16), `AGENTS.md`, `.aiox-core/constitution.md`, `docs/sie-orchestrator/EXECUTION_QUEUE.md`.

## Análise de reutilização
O repositório já dispõe do `MasterOrchestrator`, `RecoveryHandler` e `SessionState` do AIOX, voltados à execução de histórias/epics. **Não criar segundo executor de agentes.** Esta story acrescenta somente uma camada de planejamento por tarefa e dependência, consumível pelo AIOX ou por comandos locais seguros.

## Critérios de aceite
- [ ] AC-01: modelar os dez estados definidos no protocolo (PENDING, READY, RUNNING, BLOCKED, RECOVERING, IMPLEMENTED, VALIDATING, FAILED, DONE, HUMAN_REQUIRED).
- [ ] AC-02: rejeitar IDs repetidos, dependências inexistentes e ciclos no grafo.
- [ ] AC-03: promover PENDING → READY apenas com dependências DONE; fila ordenada por prioridade, desbloqueio e risco.
- [ ] AC-04: transições somente quando permitidas, com histórico verificável e justificativa.
- [ ] AC-05: DONE exige critérios de aceite aprovados, evidências para cada critério e dependências DONE.
- [ ] AC-06: guardar e retomar estado em JSON local, sem executar scripts, rede, GitHub ou operações de produção.
- [ ] AC-07: CLI permite conferir o grafo/fila e aplicar transição validada ao arquivo.
- [ ] AC-08: testes cobrem casos normais, ciclos, bloqueio, DONE prematuro, ordenação, retomada e reentrância.
- [ ] AC-09: pipeline Python e gates AIOX passam na revisão validada; documentação explica limites.

## Dependências
- AIOX root existente e stories 001/002 já verificadas.
- Estado documental criado em `docs/sie-orchestrator/`; motor JSON é separado dos relatórios Markdown.
- Sem credenciais, fonte normativa externa ou execução irreversível.

## Arquivos previstos
- [ ] `restructuring/apps/api/sie_api/scheduler.py`
- [ ] `restructuring/apps/api/sie_api/scheduler_cli.py`
- [ ] `restructuring/apps/api/tests/test_scheduler.py`
- [ ] `docs/sie-orchestrator/SCHEDULER-GUIDE.md`
- [ ] `docs/sie-orchestrator/ORCHESTRATOR_STATE.json` (exemplo real de backlog, estado reconciliado)

## Nota de segurança
A fila indica atividades elegíveis; não implica que a LLM mantenha trabalho fora da sessão. O AIOX continua responsável pela execução de stories e pela política de agentes. A CLI não faz deploy, merge, git push, cálculos normativos ou aprovação técnica.

## Evidências
Pendente de implementação e execução de testes.
