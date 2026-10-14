# Story SIE-AUTO-003 — Inventário de proveniência dos artefatos normativos

**Estado inicial:** BLOCKED (documentado na fila). **Recorte para recuperação:** inventariar hashes, origem e presença dos arquivos existentes, **sem** afirmar validação de células normativas. **Prioridade:** P1.

## Requisito existente
`docs/sie-orchestrator/EXECUTION_QUEUE.md` contém SIE-AUTO-003; `NOR-01` bloqueia motores normativos por faltar comprovação integral de fonte, edição, regra e valores.

## Critérios de aceite do SUBESCOPO de inventário
- [ ] AC-01: CLI lista referências de EDP e NBR já presentes no repositório sem copiar conteúdo protegido.
- [ ] AC-02: gera SHA256, tamanho e caminho relativo, com arquivos ausentes explicitamente registrados.
- [ ] AC-03: rejeita raiz inválida e caminhos que escapem do repositório; não faz downloads externos.
- [ ] AC-04: teste reproduzível compara hash e ausência/alteração de arquivos sem aprovar normas.
- [ ] AC-05: CI executa o inventário e publica manifesto como artefato auditável; testes Python e gates AIOX passam.
- [ ] AC-06: documenta distinção `arquivo identificado` versus `conteúdo normativo validado`.

## File List planejada
- `restructuring/apps/api/sie_api/normative_inventory.py`
- `restructuring/apps/api/tests/test_normative_inventory.py`
- `.github/workflows/sie-restructuring-api.yml`
- `docs/sie-orchestrator/NORMATIVE-SOURCES-RECOVERY.md`
- `docs/sie-orchestrator/ORCHESTRATOR_STATE.json`

## Bloqueio que permanecerá
**NOR-01** não será marcado como DONE somente porque houve hash de PDF/markdown. É indispensável validar edição, aplicabilidade e células de dados contra fontes autorizadas e casos de referência independentes. Arquivos podem existir e ainda serem de edição errada, extração inexata ou cópia não primária.
