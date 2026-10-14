# Story SIE-AUTO-003 — Evidências normativas e proveniência

**Estado:** BLOCKED para validação normativa; subescopo de inventário técnico concluído. **Prioridade:** P1.
**Fontes:** `EXECUTION_QUEUE.md`, NOR-01, `NORMATIVE-SOURCES-RECOVERY.md`.

## Objetivo
Normalizar evidências de tabelas e fontes do SIE sem confundir hash de arquivo, cópia digital, transcrição e conformidade ABNT/EDP.

## Critérios de aceite

- [x] AC-01: CLI inventaria referências existentes da EDP e da NBR sem copiar conteúdo.
- [x] AC-02: SHA-256, tamanho, caminho e ausência identificados.
- [x] AC-03: caminhos fora da raiz e links simbólicos externos rejeitados, sem downloads.
- [x] AC-04: testes de integridade e da condição `normative_conformity_verified=false`.
- [x] AC-05: CI gera manifesto e upload; run **38613344311** success, **99 pytest passed**, 6/6 presentes, artifact **11917953248**. Gates AIOX run **38613344624** e Chromium run **38613344320** com sucesso na revisão `e9fecb6aabd89a95912332573b5998fcb9f858d6`.
- [x] AC-06: distinção entre integridade de arquivo e validação normativa descrita em `NORMATIVE-SOURCES-RECOVERY.md`.
- [ ] AC-07: confirmar versão e aplicabilidade de cada fonte primária; comparar células e regras consumidas pelos motores; validar resultados de referência independentes.

## File List

- [x] `restructuring/apps/api/sie_api/normative_inventory.py`
- [x] `restructuring/apps/api/tests/test_normative_inventory.py`
- [x] `.github/workflows/sie-restructuring-api.yml`
- [x] `docs/sie-orchestrator/NORMATIVE-SOURCES-RECOVERY.md`
- [x] `docs/sie-orchestrator/ORCHESTRATOR_STATE.json`
- [x] Esta story.

## Decisão

A story permanece BLOCKED: o material ABNT presente em Markdown/chunks pode ser uma extração secundária e o registro de conferência EDP não substitui validação independente do novo software. O inventário é uma evidência técnica real, não o encerramento de NOR-01.
