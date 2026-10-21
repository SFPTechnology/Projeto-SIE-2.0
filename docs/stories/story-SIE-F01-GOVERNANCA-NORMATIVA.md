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


## Correção QA01-F01 / QA03-F02 — vínculo estrito da revisão
- [x] Derivar entrada de ensaio da versão imutável com digest validado dentro da mesma transação.
- [x] Exigir/comparar sete campos do contrato tipado, com tabela e evidência aninhadas; rejeitar divergência antes do motor/gravação.
- [x] Preservar leitura de revisão/ensaio legado sem backfill; bloquear somente novos ensaios incompletos com orientação precisa.
- [x] Corrigir comentário EDP para candidato legado não homologado, sem alterar valores/status.
- [x] Testes adversariais de campos, tipos, hash, cópia mutável, histórico e API incluídos.
- [ ] Integrar somente após CI do novo commit e revisar os demais achados; G04/G06 permanecem pendentes.

File list: `restructuring/apps/api/sie_api/storage.py`, `analysis_contracts.py`, `domain/edp.py`; `restructuring/apps/api/tests/test_calculation_traces_f01.py`; `docs/sie-orchestrator/NEXT_ACTION.md`; relatório canônico de correção e esta story. Nenhuma alteração de UI necessária: não existe ainda consumidor de ensaios na tela; API HTTP recebe a orientação de revisão incompleta. Dados sintéticos e entrada cliente continuam sem aprovação normativa.

## Correções QA03-F01 / F04 / F06 — demonstração e navegação
- [x] Rotular os valores iniciais e tabela interna como demonstração sintética não homologada; remover NBR/edição normativa dos defaults fictícios.
- [x] Resultado desta versão permanece PENDENTE; booleano ou resposta contraditória não concede estilo/texto verde de aprovação.
- [x] Navegação principal preservada em telas móveis, com seis links e foco de teclado visível.
- [x] Incluir regressões Chromium para defaults, respostas contraditórias e teclado em 390/850px.

File list: `restructuring/apps/web/{app.js,index.html,styles.css}`; `restructuring/e2e/test_browser_flow.py`; relatório canônico, `RELATORIO_EXECUCAO.md` e esta story. Não altera números normativos, motores ou aprovação dos gates. PDF privado recebido não é publicado.

Validação desta UI: contratos HTML/JS 4 testes locais passaram e node --check passou. Instalação Chromium local bloqueada por ZIP remoto truncado (0 MiB); E2E e inspeção visual serão conferidos no CI, sem alegação de execução local. `.github/workflows/sie-e2e-browser.yml` arquiva screenshots móveis do teste com formulário sem token.

## Parecer lote 01 e correção R4 — 2026-10-20
- [x] Registrar ACEITE_CONDICIONADO das 8 células/6 casos; Anexo A vazio, identificação/registro/data/assinatura incompletos; não é homologação.
- [x] Manter P01–P08 abertas e registrar divergência R3 dos dois hashes de PDF sem substituição de fonte.
- [x] Corrigir coordenação seção/disjuntor na aplicação, preservando primitivos/F00 e rejeição quando nenhum par existe.
- [x] Registrar hash da orquestração em trilhas novas, mantendo leitura v1/v2 legada sem backfill.
- [x] Adicionar 11 casos de regressão e validar 91 testes focados locais.
- [ ] Resolver I2/contexto/fontes e demais pendências; R6 pacote original permanece pendente. G04/G06 e F02 não liberados.

File list: `restructuring/apps/api/sie_api/application.py`, `calculation_traces.py`, `restructuring/apps/api/tests/test_coordinated_selection_f01.py`; relatórios canônicos e esta story. Parecer integral e tabelas/valores protegidos não foram publicados.

- [x] Regressão CI inicial identificou mensagem distinta no caso congelado ANALISE-IZ-ARREDONDADO; correção preserva diagnóstico sempar versus insuficiênciaIb, sem modificar fixtureF00.92 testes locais passam, incluindo12novos; hashfunção coordenadora atual `0021874e4bb77675bca71c36c167f359d61b36cf1bb45ba31616f04946756c7d`.

## Incremento limitado P06/P03 — lote 01
- [x] Registrar aceite profissional declarado no JSON privado por hash, sem divulgar identidade/registro; 14 aceitos no escopo e 8 pendências mantidas.
- [x] Implementar vínculo server-side versionado de células, condições e valores, com rejeição de combinações incompatíveis e proveniência em trilha.
- [x] Implementar verificação parcial I2 e condições de duração, sem presumir I2 a partir de In ou homologar dados do dispositivo.
- [x] Expor contratos opcionais/API/CLI e exemplo limitado, mantendo entrada legada e leitura histórica sem backfill.
- [x] Testes locais e QA independente do incremento limitado concluídos; aguardar CI do SHA publicado.
- [ ] P06 integral: ampliar cobertura, fontes/condições e integração de regras fora do lote.
- [ ] P03 integral: fechar curto-circuito, seletividade/coordenação e fonte verificável do dispositivo.
- [ ] Reconciliar fontes, concluir gates F01 e revisão final; F01 BLOCKED e F02 não liberada.

File list: `restructuring/apps/api/sie_api/{analysis_contracts.py,application.py,cell_bindings.py,protection_checks.py,calculation_traces.py,storage.py,cli.py}`; `restructuring/apps/api/tests/test_cell_binding_protection_f01.py`; `restructuring/examples/f01_lote01_ensaio_parcial.json`; `docs/implantacao-sie-2-0/F01/{IMPLEMENTACAO_P06_P03_LOTE01.md,ACEITE_PROFISSIONAL_LOTE01_RECEBIDO_2026-10-20.json,RELATORIO_EXECUCAO.md}`; `docs/sie-orchestrator/{NEXT_ACTION.md,ORCHESTRATOR_STATE.json}` e esta story.

- [x] Separar registro versionado do lote em `restructuring/apps/api/sie_api/data/f01_lote01_cells_v1.json`, incluído na file list; resolvedor Python conserva revisão, valores e hash semântico das células. Testes relacionados e de leitura JSON aprovados pelo implementador; CI final permanece obrigatória. P03/P06 integrais seguem pendentes.


## Recuperação e integração após checkpoint 4b1cb54 — 2026-10-20
- [x] Recuperar candidatos locais sem reset/descarte; incorporar checkpoint remoto por fast-forward.
- [x] Integrar verificações condicionais P03/P04 e trilhas v4, mantendo bloqueio normativo e leitura histórica.
- [x] Integrar triagem EDP contextual versionada, sem homologar conciliação candidata.
- [x] Acrescentar testes P07 de restauração e isolamento por projeto; separar métricas do lote limitado e QA histórico.
- [x] Corrigir achados QA de CLI não finita e resposta obsoleta na UI; incluir regressões.
- [x] Validar 440 testes API, 6 testes raiz, replay F00 34 e gates AIOX locais.
- [x] Confirmar CI em `2ee1260244ae0f0ef1bf225d6390adf4642cbce5`: API 440, replay F00 34, AIOX e Chromium 17 PASS; download local truncado não é apresentado como execução local.
- [ ] Resolver fontes/conflitos e demais condições P01–P08; F01 BLOCKED e F02 não liberada.

File list desta retomada: `sie_api/{analysis_contracts,application,calculation_traces,cli,main,complementary_checks,protection_extended,voltage_checks,edp_context}.py`, `sie_api/domain/edp.py`, `sie_api/data/edp_context_v1.json` (sob restructuring/apps/api); `restructuring/apps/api/tests/test_complementary_integration_f01.py`, `test_edp_context_f01.py`, `test_f01_progress_scope_metrics.py`, `test_p07_restore_isolation_f01.py`, `test_protection_extended_f01.py`, `test_voltage_impedance_f01.py` (os seis sob o mesmo diretório de testes); `restructuring/apps/web/{app.js,index.html,styles.css}`; `restructuring/e2e/test_browser_flow.py`; `scripts/f01_{inventory_audit,gate_dashboard}.py`; `docs/implantacao-sie-2-0/F01/{EDP_CONCILIACAO_LOTE02.json,P04_MODELO_QUEDA_IMPEDANCIA.md,RELATORIO_EXECUCAO.md}` e esta story.

CI final do incremento: API https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39505791712 ; AIOX https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39505791748 ; Chromium https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39505791783 . CodeRabbit não executado por CLI indisponível; story global e gates normativos seguem BLOCKED.


## Encerramento por aceite do titular — 2026-10-20

Instrução expressa do usuário: considerar todas as exigências validadas e finalizar o sistema. Critério de aceite desta alteração: registrar o aceite real, encerrar F01 no fluxo de projeto e permitir desenvolvimento F02 sem fabricar verificação normativa ou modificar os aceites anteriores/F00. Status desta alteração: Done por aceite do titular; publicação e CI conferidas no SHA65a2203.

- [x] Registrar decisão literal e hash, com distinção entre aceite de projeto e comprovação técnica.
- [x] Encerrar requisitos de projeto F01 por aceite do titular, mantendo valores técnicos anteriores auditáveis.
- [x] Validar guardião/dashboard/orquestrador:449 testes API,34 F00 e AIOX aprovados localmente.
- [x] Publicar decisão em `65a220311b6ba182475c2dbf7c8720e4826e03df` e confirmar API449/F0034/AIOX/Chromium17 no mesmo SHA.

File list: `ACEITE_TITULAR_ENCERRAMENTO_F01.json`, `QA3_MANIFEST.json`, `RELATORIO_EXECUCAO.md` na F01; `docs/sie-orchestrator/{ORCHESTRATOR_STATE.json,NEXT_ACTION.md,PROJECT_STATE.md,EXECUTION_QUEUE.md}`; `scripts/f01_{release_gate,gate_dashboard,yolo_runner}.py`; testes de governança F01 afetados em `restructuring/apps/api/tests/`; esta story.

Evidências do encerramento: API https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39515589279 ; AIOX https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39515589144 ; Chromium https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39515589239 . Encerramento de projeto F01 DONE; desenvolvimento F02 liberado, sem atestação normativa ou produção inventadas.
