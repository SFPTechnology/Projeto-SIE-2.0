# Story SIE-AUTO-011 — Escalonador determinístico de atividades do SIE

**Estado inicial:** READY. **Estado validado:** DONE (somente escopo do escalonador). **Prioridade:** P1.
**Fonte:** META-PROMPT SIE-AUTO-ORCHESTRATOR v2.0 (seções 5–16), `AGENTS.md`, `.aiox-core/constitution.md`, `docs/sie-orchestrator/EXECUTION_QUEUE.md`.

## Análise de reutilização
O repositório já dispõe do `MasterOrchestrator`, `RecoveryHandler` e `SessionState` do AIOX, voltados à execução de histórias/epics. **Não criar segundo executor de agentes.** Esta story acrescenta somente uma camada de planejamento por tarefa e dependência, consumível pelo AIOX ou por comandos locais seguros.

## Critérios de aceite
- [x] AC-01: modelar os dez estados definidos no protocolo (PENDING, READY, RUNNING, BLOCKED, RECOVERING, IMPLEMENTED, VALIDATING, FAILED, DONE, HUMAN_REQUIRED).
- [x] AC-02: rejeitar IDs repetidos, dependências inexistentes e ciclos no grafo.
- [x] AC-03: promover PENDING → READY apenas com dependências DONE; fila ordenada por prioridade, desbloqueio e risco.
- [x] AC-04: transições somente quando permitidas, com histórico verificável e justificativa.
- [x] AC-05: DONE exige critérios de aceite aprovados, evidências para cada critério e dependências DONE.
- [x] AC-06: guardar e retomar estado em JSON local, sem executar scripts, rede, GitHub ou operações de produção.
- [x] AC-07: CLI permite conferir o grafo/fila e aplicar transição validada ao arquivo.
- [x] AC-08: testes cobrem casos normais, ciclos, bloqueio, DONE prematuro, ordenação, retomada e reentrância.
- [x] AC-09: pipeline Python e gates AIOX passam na revisão validada; documentação explica limites.

## Dependências
- AIOX root existente e stories 001/002 já verificadas.
- Estado documental criado em `docs/sie-orchestrator/`; motor JSON é separado dos relatórios Markdown.
- Sem credenciais, fonte normativa externa ou execução irreversível.

## Arquivos previstos
- [x] `restructuring/apps/api/sie_api/scheduler.py`
- [x] `restructuring/apps/api/sie_api/scheduler_cli.py`
- [x] `restructuring/apps/api/tests/test_scheduler.py`
- [x] `docs/sie-orchestrator/SCHEDULER-GUIDE.md`
- [x] `docs/sie-orchestrator/ORCHESTRATOR_STATE.json` (exemplo real de backlog, estado reconciliado)

## Nota de segurança
A fila indica atividades elegíveis; não implica que a LLM mantenha trabalho fora da sessão. O AIOX continua responsável pela execução de stories e pela política de agentes. A CLI não faz deploy, merge, git push, cálculos normativos ou aprovação técnica.

## Evidências
**Código:** `sie_api/scheduler.py`, `sie_api/scheduler_cli.py`; testes `tests/test_scheduler.py`; JSON `docs/sie-orchestrator/ORCHESTRATOR_STATE.json`; documentação `SCHEDULER-GUIDE.md`.

**CI na revisão `57276d29f4f2a75d9c9d85bc3801532f40fb103c`:** API run 38574851595 (success, 67 testes Python, 1 aviso, JavaScript syntax check); AIOX run 38574851619 (success, lint/typecheck/test/build). https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/38574851595 e https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/38574851619 .

**Limite:** comprovada a lógica determinística de fila e estado, não uma execução contínua de agentes fora da sessão. Os critérios marcados como aprovados no JSON são metadados cuja fonte deve ser conferida externamente.
