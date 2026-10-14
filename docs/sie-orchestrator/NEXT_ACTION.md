# NEXT_ACTION — retomada segura

**Atividade:** SIE-AUTO-001 (CLI First para projetos locais).
**Estado registrado:** RUNNING após criação da story, ainda sem evidência de testes CLI.
**Branch:** `refactor/sie-2-foundation-2026-10-14`.
**Story:** `docs/stories/story-SIE-AUTO-001-CLI-LOCAL-PROJECTS.md`.

## Próximo passo executável
1. Inspecionar story e versão atual de `sie_api/storage.py`.
2. Criar `sie_api/cli.py` com argparse, comandos `salvar`, `carregar`, `historico` e saída JSON.
3. Criar testes isolados em `tests/test_cli.py`.
4. Atualizar manual e README; checar instruções AIOX antes de mexer em arquivos adicionais.
5. Consultar CI para o SHA **exato** e corrigir regressões antes de mudar story para DONE.
6. Reconciliar esta documentação com evidências recentes e passar à próxima atividade READY.

## Condições
- Se `main`, PR, branch ou arquivos forem alterados externamente, não assumir equivalência: reavaliar antes de escrever.
- Se ferramenta de escrita ou CI estiver bloqueada, registrar e prosseguir por tarefa independente.
- Não fazer merge, deploy ou liberação normativa sem gates.
