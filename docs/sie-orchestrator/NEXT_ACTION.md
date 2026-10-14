# NEXT_ACTION — retomada segura

**Atividade corrente:** SIE-AUTO-004 — contratos do núcleo elétrico, estado VALIDATING.

## Alterações publicadas
- Story: `docs/stories/story-SIE-AUTO-004-ENGINE-CONTRACTS.md`.
- Código: `restructuring/apps/api/sie_api/domain/engines.py` — validação integral de catálogos e comprimentos não negativos.
- Testes: `restructuring/apps/api/tests/test_engines.py` — regressões de valores não finitos, duplicidades e comprimento zero.
- Último commit funcional dos testes: `14bd4d3953b28906a7a409586296095a9af99310`.

## Próxima ação verificável
1. Consultar os checks da branch após a última alteração.
2. Inspecionar falhas, corrigir e executar novamente até concluir os gates.
3. Atualizar story, file list e evidências; marcar DONE somente após conferir todos os critérios.
4. Retomar SIE-AUTO-005, caso esteja READY, sem modificar a main.
5. Preservar NOR-01 BLOCKED até conferência da fonte primária; não liberar cálculo normativo.

**Limites:** nenhuma execução fora da sessão é presumida. PR #1 continua como rascunho; sem merge ou deploy.
