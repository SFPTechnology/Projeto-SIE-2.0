# BLOCKER_REGISTRY — bloqueios e recuperação

| Código | Tipo | Sintoma / evidência | Causa / hipótese | Ação segura | Estado |
|---|---|---|---|---|---|
| NOR-01 | REQUIREMENT_GAP / DATA_INCONSISTENCY | Motor de condutor recebe tabela do cliente; não existe catálogo completo certificado integrado | Dados e condições normativas independentes não fechados | Continuar com cálculo preliminar, exigir auditoria documental | BLOCKED |
| NOR-02 | CALCULATION_FAILURE (risco de aceitação) | Só Ib≤In≤Iz e queda resistiva: insuficiente para conformidade integral | Ausência de verificações de curto-circuito, sobrecarga, harmônicos, impedância etc. | Não liberar motor; criar casos de referência após NOR-01 | BLOCKED |
| EDP-01 | REQUIREMENT_GAP | Seleção por corrente é candidato, não aprovação da distribuidora | Faltam verificações adicionais de elegibilidade | Manter `liberado_para_padrao_entrada=false` | BLOCKED para aprovação |
| SEC-01 | EXTERNAL_AUTHORIZATION | API com token local, sem perfis/identidade de produção | Auth de produção e requisitos de deploy não definidos | Manter localhost e recurso opt-in, avançar tarefas independentes | HUMAN_REQUIRED para deploy |
| UX-01 | TEST_FAILURE (ausência de evidência) | Testes unitários e estáticos não comprovam interação real no navegador | E2E não executado por browser | Planejar caso E2E, não certificar experiência | PENDING |
| CLI-01 | ARCHITECTURE_CONFLICT | Persistência exposta à UI e à API antes de CLI própria | Fere prioridade CLI-first documentada na Constitution | CLI e testes criados; run 38572009186 aprovado | DONE |

## Histórico de recuperação prévia
O histórico do PR registra falha de sintaxe Python ao configurar CORS, corrigida posteriormente, e dois workflows verdes na revisão base observada. Não reproduzir defeito já corrigido nem ocultar a regressão passada.

## Próxima hipótese
Implementar CLI a partir de `RepositorioProjetos` (sem duplicar lógica de domínio), provar transações e conflitos e somente então fechar CLI-01.

- CI-AIOX-01 (resolvido): os quatro gates da raiz não constavam do workflow novo; adicionado `.github/workflows/sie-orchestrator-quality.yml`, run 38572622950 success.
