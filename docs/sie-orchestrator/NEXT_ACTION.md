# NEXT_ACTION — retomada segura

**Story concluída:** SIE-AUTO-011 (escalonador determinístico). Evidências: 67 pytest + JS, run 38574851595; root AIOX gates, run 38574851619.

**Próxima atividade pronta:** **SIE-AUTO-004 — reforçar contratos do núcleo de cálculo e limites de aplicação**, SEM inventar norma ou alterar dados de EDP.

## Como retomar
1. Verificar branch `refactor/sie-2-foundation-2026-10-14`, PR #1, novo head e checks.
2. Abrir `docs/sie-orchestrator/ORCHESTRATOR_STATE.json`; conferir que SIE-AUTO-004 e SIE-AUTO-005 estão READY e NOR-01 permanece BLOCKED.
3. Criar story `docs/stories/story-SIE-AUTO-004-ENGINE-CONTRACTS.md` com critérios de aceite baseados nos limites reais de `domain/engines.py` e `main.py`.
4. Especificar testes de entradas inválidas, precisão, comprimento zero, catálogos inconsistentes, métodos e unidades, sem extrapolar equivalência com ABNT NBR 5410.
5. Executar pytest, JavaScript check, 4 gates AIOX; documentar diferenças e SHA. Não alterar testes esperados apenas para acomodar bug.
6. Se bloqueios normativos impedirem cálculo completo, registrar e continuar tarefa independente como SIE-AUTO-005.

**Responsabilidades:** AIOX é o executor de stories; `scheduler.py` apenas planeja a fila e valida metadados. A LLM não executa fora desta sessão por mera presença de arquivos. Não fazer merge/deploy ou conceder conformidade normativa.
