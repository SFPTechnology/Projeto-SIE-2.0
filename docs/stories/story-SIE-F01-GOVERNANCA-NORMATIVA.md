# Story SIE-F01 — Engenharia de requisitos e governança normativa
Estado: **BLOCKED**. Épicos EP02, EP13, EP18; interfaces EP19/EP20. Prioridade P0.
Origens: `F01_EXECUTAR.md`; F00 DONE e baseline no PR #2.
Branch: `feat/f01-governanca-normativa`, PR draft #3.

## Critérios de aceite com rastreabilidade
- [x] F00 DONE realmente auditado e reconciliado no histórico da branch F01.
- [x] Matriz preliminar de tipologia, RF/RNF/ENG/NOR/SEG/UX, MoSCoW e aceites.
- [x] Registro normativo separado do código Python com IDs estáveis, revisões e bloqueio.
- [x] API de triagem por metadados rejeita flags cliente; testes HTTP e UX de pendência.
- [ ] Cada regra tem fonte primária verificada, cláusula/tabela/unidade e dupla conferência.
- [ ] Normas por localidade/vigência e resolução de conflito completamente confirmadas.
- [ ] Casos quantitativos independentes com valores esperados e fórmula auditada.
- [x] Snapshot de **metadados do catálogo** por revisão de projeto no SQLite local, com hash/diff/auditoria e sem backfill fictício.
- [ ] Snapshot das **regras/células efetivamente usadas no cálculo**, histórico de resultados e identidade/revalidação profissionais.
- [ ] Gate QA-01, QA-02, QA-03 aplicáveis aprovados com evidências.
- [ ] Encerramento F01 = DONE e passagem F02 permitida.

## File list de alterações/novidades F01
- `restructuring/apps/api/sie_api/domain/normative.py`, `normative_api.py`, `data/normative_registry.json`, `main.py`.
- `restructuring/apps/api/sie_api/normative_snapshots.py`, `storage.py`, `storage_api.py`, `tests/test_normative_snapshots_f01.py`.
- `restructuring/apps/api/tests/test_normative_f01.py`, `test_web_contract.py`, `restructuring/e2e/test_browser_flow.py`.
- `restructuring/apps/web/index.html`, `app.js`, `styles.css`.
- `restructuring/apps/api/pyproject.toml` (package data) e `.github/workflows/sie-restructuring-api.yml`.
- `docs/implantacao-sie-2-0/F01/*`; `docs/sie-orchestrator/*` (estado).
- Protótipo duplicado inicial `src/sie_normas/governance.py` e `tests/test_f01_normative_governance.py` removidos na branch após substituição pela integração real.
- Histórico F00 integrado por merge explícito, sem editar golden original.

## Limites e recuperação
Sem aprovação normativa, merge, deploy, Supabase real, uso de credenciais/custos ou referência numérica inventada. Retomar F01 após prova primária e solução segura de snapshots/QA.


## Correção de execução Copilot — 2026-10-19
- [x] Registrar run 39285814051: CLI exit 0, três relatórios ausentes, nenhuma revisão cruzada, G06 não aprovado.
- [x] Corrigir contrato audit-only dos perfis para output na raiz qa3-runs e preservar bloqueios normativos.
- [x] Capturar stdout/stderr, versão e exit code com sanitização limitada e artefato separado sempre.
- [x] Exigir emissão real de arquivo pequeno antes da matriz, sem shell LLM, sem ampliação de permissões.
- [x] Confirmar novo run com relatórios válidos e revisões cruzadas; nenhuma aprovação normativa antecipada (run 39289599183).

File list desta correção: `.github/workflows/f01-copilot-qa-isolated.yml`; `.github/agents/f01-qa-{arquiteto,engenheiro-eletrico,dados-ux-llm}.agent.md`; `scripts/f01_copilot_diagnostics.py`; `scripts/f01_qa_workflow_audit.py`; `tests/test_f01_copilot_diagnostics.py`; `docs/implantacao-sie-2-0/F01/RELATORIO_CORRECAO_EMISSAO_QA_2026-10-19.md`; esta story.

- [x] Diagnóstico real do smoke 39288590946 arquivado: CLI exit 0 sem ferramenta de criação disponível; matriz não executada.
- [x] Smoke admite create/edit/apply_patch; perfis audit-only usam nomes literais sem execute; auditor recusa remoção de apply_patch.
- [x] Validar novo smoke e depois entregas QA (run 39289599183); F01 BLOCKED e G06 pendente.

## Evidência final do desbloqueio operacional QA3
- [x] Run `39289599183` SUCCESS no baseline `29c506cbd4f0045c4d54e4f50098d989d7260194`: smoke + 3 primeiras passagens + 3 cruzadas + bundle.
- [x] Nove arquivos baixados e validados localmente; JSON recalculado idêntico ao bundle remoto (9 hashes).
- [x] Registro persistido em `docs/implantacao-sie-2-0/F01/QA3_EXECUTION_EVIDENCE_39289599183.json`; relatório canônico atualizado com jobs/artefatos.
- [ ] Rever e corrigir achados técnicos dos pareceres; validar fontes/células e obter signoff independente exigido para G06.

O bloqueio operacional de arquivos QA3 foi resolvido; F01 segue BLOCKED, sem homologação e sem liberação F02. Checkboxes pendentes anteriores de novo run estão atendidas somente quanto à execução operacional neste baseline, não aos gates normativos.
