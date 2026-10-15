# NEXT_ACTION — F01 BLOCKED, prosseguir na F01; F02 não liberada
Data: 2026-10-15. Branch: `feat/f01-governanca-normativa`; PR #3 em rascunho sobre F00.

**F00 DONE; F01 BLOCKED; NOR-01 BLOCKED; F02 NÃO LIBERADA.** Fonte canônica `ORCHESTRATOR_STATE.json`.

## Implementado nesta retomada
- Fontes editoriais ABNT NBR 5410, NBR 5419 (1–4), NR-10 e EDP PT.DT.PDN.00068 V9 confirmadas nas páginas oficiais, com *tabelas não homologadas*. EDP v09 publicada em 15/04/2026, registro versão 2; triagem de referência anterior à publicação = PENDENTE.
- `normative_snapshots.py`, `storage.py`, `storage_api.py`: snapshot **do catálogo** por revisão de projeto no SQLite local, com hash, diff, histórico imutável via triggers e consultas sob token. Não há snapshot comprovado das **regras aplicadas ao cálculo**, recuperação do JSON histórico ou identidade multiusuário.
- Últimos testes comprovados no commit `a5b4cce`: **160 pytest, 1 warning** https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/38725806925 ; **4 Chromium** https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/38725806964 ; **AIOX success** https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/38725806937 . Novos commits documentais exigem verificar CI separadamente.

## Ordem de desbloqueio, mantendo FAIL_CLOSED
1. Fonte primária e direitos: validar edição/vigência/jurisdição da cópia e conferir tabela, linha, coluna, unidade, observações de cada célula Rca/XL/Iz/EDP, com dupla leitura independente. Não inventar valores.
2. Criar casos numéricos de referência independentes e assinados no escopo técnico, com fontes autorizadas, para cada regra real.
3. Associar por circuito e revisão as regras **usadas no cálculo** e memória/entradas/saídas, ensaiando integridade/histórico/restauração e segurança em banco descartável antes de uma migração de produção.
4. Resolver conflitos normativos, ressalvas da transição NR-10 e a aplicabilidade territorial/temporal e por tipologia/tensão.
5. Reexecutar regression/e2e/QA-01, QA-02, QA-03. Só marcar DONE com gates exigidos e evidências suficientes; F02 não pode começar antes.

Dossiê: `docs/implantacao-sie-2-0/F01/RELATORIO_EXECUCAO.md`, `EVIDENCIA_FONTES_OFICIAIS.md`, `EVIDENCIA_SNAPSHOTS_LOCAL.md`, `QA-01.md`, `QA-02.md`, `QA-03.md`.

Sem merge, deploy, edição de SQL remoto ou execução em background.

## Plano QA3 ampliado — 15/10/2026

Agentes F01 QA-01 (arquiteto), QA-02 (engenharia elétrica), QA-03 (dados/UX/LLM) foram definidos com seis skills em `.github/agents/f01-*.agent.md` e `.github/skills/f01-*/SKILL.md`, e têm três branches separadas e issues #4, #5, #6. **Ainda não foram executados como sessões independentes**. Leia `docs/implantacao-sie-2-0/F01/LEIA_PRIMEIRO_QA3.md` e `QA3_MULTIAGENTES_PLANO_EXECUCAO.md`. O objetivo é 6/6 gates mediante fontes/evidências, mas as verificações externas ainda são impeditivas. `QA3_MANIFEST.json` registra os seis gates NÃO APROVADOS; `python scripts/f01_release_gate.py --verify-invariants` deve confirmar o bloqueio correto, não forçar DONE.

## Plano mestre YOLO da F01 — configurado, ainda NÃO executado
- Plano operacional: `docs/implantacao-sie-2-0/F01/PLANO_EXECUCAO_AUTONOMA_YOLO.md`.
- Executor não interativo com 3 QA, congelamento de commits, revisões cruzadas e até 3 ciclos de correção por agente: `scripts/f01_yolo_runner.py`. Plano sem efeitos: `python scripts/f01_yolo_runner.py`. Execução **somente em sandbox descartável com GitHub Copilot CLI autenticado e permissões restritas de GitHub**: `python scripts/f01_yolo_runner.py --execute --sandbox-confirmed`.
- O launcher executa `copilot -p --agent --yolo --no-ask-user`. Atualiza por push somente `qa/f01-*` e `feat/f01-governanca-normativa` após testes locais, não `main`, nem produção. O próprio prompt não garante controle do filesystem ou rede: isolamento VM/container é externo.
- Primeiro passe QA deve gerar dossiê; depois revisão cruzada, integração na F01 e mais testes. O executor não autodeclara G01..G06, não verifica CI remoto como prova, nem inicia F02; relatórios devem registrar `BLOCKED_EVIDENCE`/status correspondente quando não houver fontes independentes/licenças/signoff.
- **0 sessões QA executadas por esta atualização; F00 DONE; F01 BLOCKED; F02 não liberada.**

## EXECUÇÃO REAL NA F01 — continuação YOLO na sessão de 15/10/2026
**Esta seção posterior substitui as limitações técnicas desatualizadas descritas acima; adendos antigos permanecem para rastreabilidade.**

**Código implementado e testado no GitHub, sem reabrir F00:**
- `storage.py`: recuperação histórica de **novas** revisões completas de projetos locais, sem fabricar histórico de projetos preexistentes; armazenamento transacional, SHA-256, triggers e 2 rotas GET autenticadas.
- `analysis_contracts.py`, `calculation_traces.py`, `storage_api.py`: novo ensaio efetivamente calculado pelo servidor, vinculado a projeto/revisão/circuito, com entrada, resultado, ID de algoritmos e SHA-256 dos corpos das funções; 3 endpoints de ensaio sob token local. Referência normativa declarada pelo cliente explicitamente **NÃO VERIFICADA**; ID/célula normativa homologada permanece em listas vazias.
- Testes novos `test_project_revisions_f01.py`, `test_calculation_traces_f01.py`, `test_f01_independent_math_examples.py`; 5 casos aritméticos sintéticos independentes **não contam** como fixtures normativas G03.
- `scripts/f01_yolo_runner.py`: corrigido para `--autopilot --yolo --no-ask-user --max-autopilot-continues=10`; `--no-ask-user` sozinho não garante continuação multietapa conforme GitHub Docs.
- Relatório objetivo `EVIDENCIA_REPRODUTIBILIDADE_E_ENSAIOS_LOCAL.md`; perspectivas QA-01/02/03 reavaliadas e mantidas como PENDENTE/BLOQUEADO/PENDENTE.

**Limite do ambiente desta conversa:** Copilot CLI não instalado e shell sem acesso DNS a github.com; assim foi utilizada a integração GitHub conectada para commits e CI, **não** três processos agentes autônomos genuinamente independentes. As branches QA permanecem com SHA inicial e nenhuma primeira revisão congelada por agente; `QA3_MANIFEST.json` mantém 0/6 aceitos. Não declarar execução de QA3 ou 100%.

**Próxima prioridade sem reabrir F00:**
1. Confrontar fontes PDF primárias/licença e células Iz/Rca/XL/EDP com duas verificações reais, junto com jurisdição/vigência/NR-10 transitória.
2. Vincular rule/cell IDs homologados realmente consumidos ao ensaio do circuito, com memória e evidência técnica; **não falsificar regra usada**.
3. Executar 3 agentes Copilot em worktrees isoladas num runtime autenticado, registrar primeiros SHAs, testes e revisão cruzada.
4. Completar UX histórico, RBAC/tenant/migração segura e CI integradas; reavaliar 10 AC e 6 gates.
**F01 BLOCKED, NOR-01 BLOCKED, F02 NÃO LIBERADA.**
