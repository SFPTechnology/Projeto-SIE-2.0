# F01 — RELATÓRIO DE EXECUÇÃO E GOVERNANÇA NORMATIVA
Data: 2026-10-15
FASE: F01 — Engenharia de requisitos e governança normativa
ESTADO: **BLOCKED** (etapa estrutural parcialmente implementada e validada; blockers normativos obrigatórios)
BRANCH: `feat/f01-governanca-normativa`
PR (draft, sem merge): https://github.com/SFPTechnology/Projeto-SIE-2.0/pull/3
BASE PREDECESSORA: `audit/f00-baseline-2026-10-15` — PR #2, F00 **DONE**.
RECONCILIAÇÃO: merge commit `e611ce35a20959b0a3cc01d8c8d9d36d692d13d9` preserva ambas as linhas históricas, main inalterada.

## Predecessora e prova
F00 tem `docs/implantacao-sie-2-0/F00/RELATORIO_EXECUCAO.md`, `docs/sie-orchestrator/ORCHESTRATOR_STATE.json` revisão 9, 37 LEGACY-IDs, replay 34 golden, 134 pytest (35 golden incluídos), 3 E2E Chromium, 18 AIOX e QA3 **APROVADO no escopo da F00**. Não presumir homologação da engenharia pela F00.

## Execução efetiva das 10 tasks
| Task | Estado | Entrega ou prova |
|---|---|---|
| 01.01 — Recorte/tipologias | PARCIAL | Matriz residencial/comercial/predial; exclusão industrial do recorte do protótipo, sem dispensa técnica |
| 01.02 — Requisitos rastreáveis | PARCIAL | Matriz com 13 IDs RF/RNF/ENG/NOR/SEG/UX, MoSCoW, donos por função, teste/aceite e backlog; vinculação total a stories legadas ainda não completa |
| 01.03 — Catálogo de fontes | PARCIAL | `CATALOGO_FONTES_NORMATIVAS.json` v2, 8 fontes, SHA quando disponível, links oficiais, edição e licença NAO_CONFERIDA |
| 01.04 — Conferir regras/tabelas | BLOQUEADO | `REGISTRO_REGRAS_NORMATIVAS.md`; **0 células auditadas**; ausência de dupla conferência primária |
| 01.05 — Motor de aplicabilidade | IMPLEMENTED estrutural | `sie_api/domain/normative.py`, `normative_api.py`; contexto tipologia, UF, distribuidora, data; API HTTP com respostas conservadoras |
| 01.06 — Versionar regras | PARCIAL | Registro independente do código `sie_api/data/normative_registry.json`, IDs/revisões; **ainda sem snapshots históricos persistentes por projeto** |
| 01.07 — Conflitos/transições | PARCIAL | Marcador NR-10 2026/2027, ressalva de instalações existentes PENDENTE, não há precedência legal automática |
| 01.08 — Casos independentes | BLOQUEADO | `CASES_REFERENCIA_ENGENHARIA/casos_escopo.json` contém casos **só de triagem**; sem fixtures numéricas homologadas |
| 01.09 — Gate conservador | PARCIAL | Endpoint rejeita flags extras de aprovação; `release_allowed=false`, `normative_conformity_verified=false`; UI exibe pendências |
| 01.10 — Criticar/fechar recorte | PARCIAL | `PARECER_LACUNAS_NORMATIVAS.md`, QA3 e relatório; ainda sem gates essenciais |

## Correções e achados de implementação
1. Foi removido o protótipo desconectado `src/sie_normas/governance.py` que recebia flags `approved/source_verified` de chamadores. O módulo oficial integrado à API não permite aprovação normativa.
2. API `GET /api/v1/normas/catalogo`, `POST /api/v1/normas/aplicabilidade`; validações de escopo/revisão, sem dados de tabelas.
3. Teste CI inicialmente falhou ao examinar `app.routes`: FastAPI instalado usa `_IncludedRouter`; verificação corrigida para HTTP real em vez de afirmar que a rota estava ausente.
4. NR-10 anterior após 01/06/2027 tratada como `PENDENTE` para transição de instalações existentes; não inferir inaplicabilidade universal.
5. Registro de regras é JSON independente do código; mudanças editoriais não mudam código Python, mas **snapshots imutáveis no histórico de projetos não estão implantados**.
6. UX `#normas`: painel de metadados, sem opções de aprovação, texto escapado por `textContent` e falha fechada.

## Testes observados
- API executada em GitHub Actions CI para commit `fa6002d5e6846a9a4e9147e4b06c4828daf339d6`: https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/38722630175 — **149 passed, 1 warning**.
- Chromium real (incluindo teste F01 de catálogo visual): https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/38722630269 — **4 passed**.
- Gates AIOX na mesma revisão: https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/38722630211 — **success**.
- Evidências obtidas antes do commit de fechamento documental; CI posterior deve ser consultada separadamente, sem atribuir resultados antecipadamente.
- A baseline da F00 possuía 134 pytest e 3 Chromium; contagens entre diferentes revisões não devem ser somadas.
- `normative_conformity_verified=false` em todos os ensaios.

## QA3 — perspectivas críticas distintas
| Revisor | Veredito F01 | Evidência e impeditivo |
|---|---|---|
| QA-01 — arquitetura/código/testes | **PENDENTE** | `QA-01.md`; registro de metadados separado, API protegida, falta snapshot histórico permanente |
| QA-02 — elétrica/normas | **BLOQUEADO** | `QA-02.md`; 0 células conferidas, dados normativos/fixtures numéricos ausentes, NR-10 e EDP exigem revisão |
| QA-03 — integração/dados/segurança/UX | **PENDENTE** | `QA-03.md`; UI consultiva disponível, falta auditar logs de revisão, identidade/ACL/licenças |

Três papéis de LLM não equivalem a três revisores humanos independentes. Não houve assinatura de responsável habilitado.

## Gates finais
- F00 DONE observado: **ATENDIDO**
- Branch/commit/preservação de golden: **ATENDIDO** (histórico preservado, regressão em CI)
- Aplicabilidade e bloqueio conservador de fontes não homologadas: **ATENDIDO para protótipo**
- Regras com edição/vigência/condições e verificação independente para consumo normativo: **NÃO ATENDIDO**
- Valores de tabelas com dupla conferência e casos numéricos independentes: **NÃO ATENDIDO**
- Snapshots históricos de cada projeto e trilha de impacto: **NÃO ATENDIDO**
- Aprovação QA-01/02/03 integral: **NÃO ATENDIDO**

**DECISÃO: F01 BLOCKED. NÃO AVANÇAR À F02.** Retomar a F01 na mesma branch após conferência das fontes primárias e implementação rastreável dos históricos; produção/main/SQL não alterados.

## ADENDO DE RETOMADA — 15/10/2026 (prevalece sobre os estados históricos anteriores)

**Implementado agora:** `normative_snapshots.py`, `storage.py`, `storage_api.py` e `test_normative_snapshots_f01.py`. O SQLite **local** captura, na mesma transação da gravação de um projeto, um snapshot versionado do **catálogo de fontes** e um evento de revisão; SHA-256 e triggers impedem alteração inadvertida. GETs de histórico/impacto exigem token local. Bancos legados não recebem backfill inventado. A alteração de edição gera diff e exigência de análise sem recálculo automático.

**Limite decisivo:** snapshot do catálogo **não demonstra quais regras/células foram aplicadas a cada cálculo**; não representa histórico integral recuperável do projeto. Por isso a task 01.06 avança, mas continua PARCIAL, assim como 01.09. Nenhuma migração Postgres/Supabase foi executada.

**Fontes:** EDP PT.DT.PDN.00068 v09, edição publicada em 15/04/2026, identificada oficialmente; NBR 5410, NBR 5419 e NR-10 identificadas por catálogo/página oficiais, conforme `EVIDENCIA_FONTES_OFICIAIS.md`. O registro EDP recebeu revisão editorial 2; `verified_data=false`. Para projeto anterior à publicação da v09, a API retorna `PENDENTE`, sem presumir vigência.

**Testes:** CI após a implementação de snapshots: API **158 passed, 1 warning**, https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/38725502538 ; Chromium **4 passed**, https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/38725502550 ; AIOX success https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/38725502574 . O teste de cronologia EDP foi incluído depois; observar a CI do último commit de código para contagem final. Esses testes são computacionais, não avaliam conformidade de valores normativos.

**QA-01 PENDENTE** (vínculo regra aplicada e recuperação integral); **QA-02 BLOQUEADO** (zero células e zero casos normativos independentes com dupla conferência); **QA-03 PENDENTE** (controle multiusuário, produção, histórico). Pareceres atualizados em `QA-01.md`, `QA-02.md`, `QA-03.md`. As afirmações do relatório inicial de que "não existe snapshot" permanecem apenas como histórico de execução anterior, corrigido por este adendo.

**ESTADO FINAL DA RETOMADA: F01 BLOCKED; F02 NÃO LIBERADA; MAIN/PRODUÇÃO PRESERVADAS.** Não alterar essa decisão sem resolver os gates normativos e aprovações exigidos.

## Conferência final da CI após checkpoint de orquestração

Último commit conferido antes deste adendo: `61805b07db9e70963e3e868da098331cd19f4244`:
- API e persistência: **160 testes aprovados**, 1 aviso — https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/38726713101
- Navegador Chromium: **4 testes aprovados** — https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/38726712894
- Quality gates AIOX: **success** — https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/38726712882

Comparação com a baseline: os testes de regressão F00 permanecem representados na suíte integrada, sem alterar os resultados congelados do SHA original. A classificação normativa permanece **BLOCKED** apesar da CI verde; testes de software não substituem dupla conferência de células ou homologação de cálculos. Este adendo de documentação não modifica runtime, testes, fontes normativas ou banco.

## Adendo — Programa QA3 end-to-end configurado (15/10/2026)

Foram criados três perfis custom agents GitHub Copilot `.github/agents/f01-qa-*.agent.md`, seis skills em `.github/skills/f01-*/SKILL.md`, manifesto `QA3_MANIFEST.json`, plano `QA3_MULTIAGENTES_PLANO_EXECUCAO.md`, três branches de isolamento e issues #4, #5 e #6. Cada perfil tem responsabilidade **integral** por cinco etapas de correção e seis critérios de aceite, com perspectiva primária distinta e revisão cruzada apenas após parecer inicial isolado. O comando `scripts/f01_release_gate.py` verifica estruturas e recusa liberação de F02 sem as evidências exigidas; *não* certifica normas e não muda o estado sozinho.

**Importante:** esses três perfis estão **CONFIGURADOS**, porém NÃO foram efetivamente executados como três instâncias independentes. O projeto continua com **0 células de tabela homologadas, 0 casos quantitativos normativos independentes aprovados**, sem atestação profissional. Nenhum gate da F01 passa apenas por ter sido configurado. O programa não elimina os riscos QA-01, QA-02 e QA-03 anteriores.

Evidência computacional da configuração antes do fechamento documental: CI GitHub Actions API **168 testes aprovados** https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/38740090384 ; navegador e AIOX no mesmo SHA conforme GitHub Actions. O número de testes mede software, não homologação de engenharia.

**F01 = BLOCKED; F02 = NÃO LIBERADA; PR #3 segue draft.**

## Adendo — Plano de execução autônoma YOLO entregue
Adicionado plano `PLANO_EXECUCAO_AUTONOMA_YOLO.md`, orquestrador `scripts/f01_yolo_runner.py`, testes determinísticos em `restructuring/apps/api/tests/test_f01_yolo_runner.py` e check de prévia no GitHub Actions. Execução: tripla primeira passagem em sessões Copilot distintas com worktrees independentes, retries limitados, primeira revisão congelada em SHA, três revisões cruzadas, integração controlada em F01 e novo replay F00 **somente como regressão**. O script requer autenticação GitHub Copilot CLI e VM/container previamente isolado, não autentica normas/linhas/células ou pareceres humanos. Publica somente branches QA/F01, sem force e sem merge na main; CI final e validação normativa seguem exigidos.
Esta entrega registra um **plano + executor configurado** e seus testes; NÃO executou as três sessões QA, NÃO homologou nenhuma célula normativa, NÃO aprovou nenhum dos seis gates e NÃO encerrou a F01.

## Retomada com execução efetiva no GitHub — 15/10/2026
A partir do checkpoint do programa YOLO, foram **implementadas alterações concretas** na branch `feat/f01-governanca-normativa`: preservação transacional de histórico completo das versões **novas** em SQLite (`versoes_projeto`), rastreabilidade de ensaios de cálculo realmente processados pelo servidor (`ensaios_calculo`), contratos compartilhados estritos, hashes do código-fonte das funções, cinco novas rotas HTTP protegidas, novos testes de API, regressão e matemática independente sintética (sem uso normativo). Veja `EVIDENCIA_REPRODUTIBILIDADE_E_ENSAIOS_LOCAL.md` para métodos, limites e resultados. Foi também corrigida a configuração do executável autônomo Copilot para usar `--autopilot` e continuação limitada.

**Separação rigorosa de homologação:** não foram importadas ou conferidas células primárias ABNT/EDP (Iz/Rca/XL/demanda), não existem casos normativos numéricos assinados, e `normative_rule_ids_used_verified=[]` nos ensaios. Nenhuma conta/credencial de produção, Supabase, `main` ou arquivos golden F00 foram alterados.

Os arquivos `QA-01.md`, `QA-02.md` e `QA-03.md` receberam novas revisões de perspectiva técnica **pelo mesmo assistente**; isto não se apresenta como execução independente dos três agentes Copilot, inexistente neste runtime sem CLI. Os três perfis e as três branches estão prontos, mas seus commits individuais/cross-reviews **ainda não existem**.

A CI computacional é exigida no SHA final; a execução do código elevou a suíte para pelo menos **200 testes** aprovados antes dos commits finais documentais, além de 4 Chromium e AIOX nos commits verificados. Não afirmar conformidade ABNT/EDP com base em CI.

**Status deliberado e preservado:** F00 DONE; F01 BLOCKED; G01..G06 0 aceitos no manifesto; F02 não liberada. Prioridade subsequente: provas documentais e dupla conferência, vínculo a regras homologadas, UX/segurança multiusuário, agentes QA3 de fato independentes e parecer final em CI mesmo commit.

## Verificação integrada encerrada — commit `516ade10731664148bdd60e2cf468dbcfe3494d6`
- **API + testes históricos/cálculo/regressão:** 200 testes aprovados, 1 warning — https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/38802503246
- **Navegador Chromium:** 4 testes aprovados — https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/38802503369
- **AIOX quality gates:** success — https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/38802503251
- Replay F00 e inventário executados pela workflow API; não altera golden nem normativa.
- **Essas três CI são do MESMO commit**, comprovam qualidade de software no recorte ensaiado, não aprovação de fonte ABNT/EDP.
- Não ocorreu execução de três Copilot agents realmente independentes; o CLI não está presente na infraestrutura disponível desta conversa. QA-01 PENDENTE, QA-02 BLOQUEADO e QA-03 PENDENTE, sem signoff profissional.
- `QA3_MANIFEST.json`: G01–G06 **0/6 aprovados**; F01 BLOCKED; F02 não liberada; PR #3 permanece draft e `main` intocada.

## EXECUÇÃO DIRETA DOS PACOTES PF-01 A PF-05 — 16/10/2026

**Autoridade e fonte:** `PLANO_UNICO_FECHAMENTO_F01.md`, material de execução `F01_EXECUTAR.md`, `ORCHESTRATOR_STATE.json`, `QA3_MANIFEST.json`. Implementação direta via plugin GitHub no escopo F01. **F00 original intocada, main intocada, sem deploy ou Supabase.**

### PF-01 — Inventário e triagem REALIZADOS, homologação ainda bloqueada
- Repositório inspecionado: PDF `Arquivos_Diversos/Norma_EDP/PT.DT.PDN.00068_V9.pdf`, extração Markdown V09, texto derivado `NBR_5410_original/NBR-5410.md`, F00 `fontes-sha256.json`, `edp.py`, `engines.py`, `application.py`.
- Inventariado `INVENTARIO_CELULAS_E_REGRAS_USADAS.csv`: **24 entradas** (13 categorias EDP codificadas + 11 necessidades de dados/regras; **não** 24 células primárias homologadas).
- `PF01_AUDITORIA_FONTES_2026-10-16.md` documenta extrações NBR 5410 (capacidade em tabelas 36–39, temperatura em 40–41, agrupamento 42–45), candidatos EDP de tabela 001/002 e transição NR-10; original ABNT autorizado e dupla conferência faltantes.
- Fonte editorial oficial EDP declara versão 09 publicada 15/04/2026; o frontmatter da extração local apresenta 14/04/2026. Não converter essa diferença em data de vigência automática.

### PF-02 — Parcial no software, **BLOCKED_EVIDENCE** normativo
- Ensaios de matemática independentes anteriores permanecem `DEMO_SYNTHETIC`; **nenhuma fixture com valor primário homologado** foi inserida artificialmente.
- **0** células primárias duas vezes conferidas; **0** casos numéricos normativos homologados; segunda leitura realmente independente/profissional faltante.
- É inseguro importar Rca, XL, Iz, demanda EDP ou limite territorial apenas do texto derivado/chunks. Não reclassificar G02/G03.

### PF-03 — Correções reais integradas
- `engines.py` preserva **Iz não arredondada** na seleção de proteção; `application.py` disponibiliza `capacidade_decisao_a` para auditoria, arredondando somente a visualização. Corrige o comportamento inseguro ENG-001, mantendo condicional normativo fechado.
- `edp.py` remove alegação indevida `status: VERIFICADO`; agora `DOCUMENTADO_SEM_FONTE_PRIMARIA`. Adiciona alerta `EDP-003` que bloqueia seleção automática U/D com carga trifásica. Corrige uma via insegura do ENG-002 sem assumir critérios normativos completos de modalidade.
- `test_legacy_golden.py` preserva replay integral do **F00 original** e documenta explicitamente divergências F01 de segurança, em vez de exigir que defeitos caracterizados permaneçam no software novo. **Fixture F00 não foi modificada.**
- `calculation_traces.py` grava a **linha de entrada realmente consumida**, fator, resistência e Iz de decisão como `CLIENT_SUPPLIED_UNVERIFIED_NOT_NORMATIVE_CELL`; nenhuma falsa célula ABNT é atribuída.
- A interface `restructuring/apps/web/index.html` / `app.js` exibe revisões locais imutáveis sob token, SHA-256, mensagens de ausência de homologação e sem recálculo implícito; `test_browser_flow.py` acrescenta ensaio Chromium histórico e token incorreto.

### PF-04 — NÃO EXECUTADO como QA independente
Três perfis e branches já existiam, mas esta infraestrutura não dispõe de GitHub Copilot CLI autenticado. Revisões próprias de QA técnica podem detectar falhas e orientar correções, porém **não contam** para as três sessões independentes e três revisões cruzadas exigidas pelo G06. Os pareceres existentes permanecem PENDENTE/BLOQUEADO/PENDENTE.

### PF-05 — Verificação de software, fechamento normativo BLOQUEADO
Suíte CI de referência do commit `e1faaa61` (antes da inclusão de rastreabilidade detalhada):
- API: **215 pytest aprovados**, 1 warning — https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/38941702211 .
- Chromium: **5 testes aprovados** — https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/38941702181 .
- AIOX: **success** — https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/38941702206 .
Verificar também os workflows do último SHA final; a reprodução F00 permanece separada.

### Pendências críticas precisas
1. **G01/G02:** original ABNT autorizado com direito de uso, conciliação EDP com publicação vigente e **todas** as células necessárias por motor sob leituras independentes A/B; resolver jurisdição, edição e vigência.
2. **G03:** fixtures com resultado normativo independente do motor, fonte original e revisores.
3. **G04:** vínculo completo ao ID da **célula homologada realmente carregada no servidor**, não apenas input do cliente; controle profissional/tenant e portabilidade ainda pendentes.
4. **G05:** controles RBAC/UX e CI integrada de último commit; não homologar em produção.
5. **G06:** três QA efetivamente independentes, três pareceres iniciais congelados, revisões cruzadas e aprovações externas exigidas.
6. **AC-01.01–04 e AC-01.06–10:** ainda não aprovados formalmente no orquestrador. AC-01.05 permanece único formalmente aprovado.

**Resultado honesto:** PF-01 inventário executado, PF-02 impedido por evidência, PF-03 correções reais, PF-04 aguardando ambiente independente, PF-05 CI parcialmente comprovada, **F01 BLOCKED, 0/6 gates, 1/10 AC; F00 DONE, F02 não liberada**.

## Auditoria adicional — execução solicitada de Copilot e fontes oficiais em 16/10/2026

**Escopo factual:** tentativa de ativar Copilot, verificação dos documentos oficiais externos, correção de aplicabilidade NR-10, testes e checagem de bloqueios remanescentes. F00 permanece `DONE`, F02 não iniciada.

### Copilot: bloqueio operacional efetivamente investigado
- No ambiente desta conversa `command -v copilot` não encontrou binário, `gh` também não está instalado e não há variáveis de autenticação `GH_TOKEN/GITHUB_TOKEN/COPILOT_*`. O shell local não resolve `github.com` para Git.
- O conector ChatGPT GitHub disponível **edita código e CI**, mas **não expõe** o parâmetro obrigatório `agent_assignment.base_branch` para atribuição correta a um Copilot Cloud Agent via REST; assim, usar `assignees=[copilot-swe-agent[bot]]` sem campo de branch poderia abrir trabalho contra `main`, contrariando a decisão do projeto. Nenhum issue foi atribuída ao Copilot com base insegura.
- Os três agentes **NÃO foram iniciados**; `QA3_MANIFEST.json` preserva `agent_executions_verified=0` e G06 `BLOCKED`. As 3 branches QA existem, mas seus commits não são pareceres independentes. Nenhum agente foi simulado.

### Verificação de fonte primária efetivamente realizada
- Documento oficial MTE `Portaria MTE nº 737/2026` inspecionado no PDF https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/inspecao-do-trabalho/seguranca-e-saude-no-trabalho/sst-portarias/2026-1/portaria-mte-no-737-nova-nr-10.pdf, incluindo **art. 3º** (prazo específico somente 10.6.4(e) para instalações existentes) e **art. 5º** (vigência geral em 01/06/2027). Fonte primária oficial; não prova 6/6 gates.
- Código `sie_api/domain/normative.py` e API `normative_api.py`: triagem agora diferencia instalações existentes em 01/06/2027, início geral de 01/06/2027 e exceção específica em 01/06/2028; `test_normative_f01.py` testa os limites e conserva `normative_approved=false`.
- Fonte EDP V09 oficial encontrada em https://www.edp.com.br/Ginp/Download/PT.DT.PDN.00068_V9.pdf (domínio oficial). O resultado indexado declara início de vigência **14/04/2026** e 91 páginas; o catálogo público lista publicação em **15/04/2026**. O PDF é servido de forma incompatível com o leitor PDF web (`application/octet-stream`); não se obteve inspeção visual direta das Tabelas 001/002, nem comparação de bytes com cópia do GitHub. `edp.py` recebeu a URL oficial, mas campo `confirmacao_binaria_pdf=false` e status `DOCUMENTADO_SEM_FONTE_PRIMARIA` se mantêm.
- O catálogo ABNT oficial lista `NBR 5410:2004 Versão Corrigida:2008` e partes 1–4 da `NBR 5419:2026 Versão Corrigida:2026`. Identificação editorial comprovada; conteúdo de células ABNT, licença e direito de uso não foram demonstrados. **Nenhum valor foi importado do web para o motor.**
- Documento rastreável: `AUDITORIA_FONTES_OFICIAIS_2026-10-16.md`.

### Comprovação de CI
Commit `a4c41553aecff0c479867e27f56cb0cb8c9cf612` aprovado com **219 pytest**, **5 Chromium** e **AIOX**:
- https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/38956570954
- https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/38956570839
- https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/38956570882

Houve commits posteriores com documentação da auditoria e testes de metadados EDP; consultar o último SHA/CI antes de qualquer aceite. **0/6 gates aceitos, 1/10 AC formalmente aprovado; F01 BLOCKED**, sem reabrir F00.

### Correções verificadas, achados restantes
- **Corrigido:** ambiguidade de vigência NR-10, antes tratada como transição global da norma; novo motivo específico `10_6_4_E_PRAZO_ESPECIFICO_INSTALACAO_EXISTENTE_ATE_2028_05_31`, sem concessão de conformidade.
- **Corrigido:** fonte EDP com URL oficial legível e campo explícito `confirmacao_binaria_pdf=false`; teste impede classificação como homologada.
- **Bloqueios ainda externos:** original ABNT autorizado e conferência física das tabelas Iz/fatores/Rca/XL, PDF EDP oficial verificado visualmente/byte a byte e todas as células usadas por motor com segunda leitura independente, expected normativos externos, profissional homologador independente, 3 sessões Copilot QA, revisões cruzadas e critérios de G04/G05 ainda incompletos.
- **Próxima ação sem duplicação:** executar o `scripts/f01_yolo_runner.py` em ambiente já isolado com Copilot CLI autenticado, conferir PDF EDP/ABNT por dois revisores separados e associar evidence hashes por célula. Não repetir F00 nem iniciar F02 enquanto as provas faltarem.

## Implementações adicionais de qualidade e rastreabilidade — 19/10/2026

Esta rodada **executou código e testes**, não reabriu F00 e não iniciou F02; o plano de referência continua `PLANO_UNICO_FECHAMENTO_F01.md`.

**1. Copilot QA3, sem uso de credencial:**
- Corrigido `.github/workflows/f01-copilot-qa-isolated.yml`: antes o Copilot tinha `edit` mas **não tinha `create`**, inviabilizando a emissão dos dois relatórios. Agora usa lista restrita `view,grep,glob,edit,create,apply_patch,skill` e proíbe shell/MCP.
- Bloqueio físico de escrita de arquivos e diretórios do checkout via `chmod a-w`; somente a pasta `qa3-runs/QA-XX` fica gravável no job correspondente. Continua sem permissão de push da Actions; peer é congelado com SHA-256 antes da revisão cruzada.
- Novo `scripts/f01_qa_workflow_audit.py` verifica configuração, branches, isolamento, criação dos relatórios, SHA compartilhado, permissões de checkout e guardrails. Testes adversariais com permissões inseguras detectam alterações sem consumir Copilot.
- **Nenhuma sessão Copilot foi efetivamente executada**; `F01_COPILOT_PAT` precisa ser cadastrado pelo titular na área GitHub Actions Secrets. Não contar jobs mockados como QA3 independente.

**2. Proveniência técnica dos cálculos:**
- `sie_api/calculation_traces.py` gera `trace_schema_version=2`, hash SHA-256 da **linha de condutor efetivamente selecionada**, registra origem declarada dos três parâmetros (Iz base, fator, resistência) e valida novamente a capacidade corrigida usada no disjuntor com `Decimal`.
- `validar_registro` detecta a linha ou origem adulteradas **mesmo quando o digest geral for recalculado**; traços históricos sem `trace_schema_version` continuam legíveis como v1. Isso prova consistência de inputs, **não a autenticidade de célula ABNT/EDP**.
- Testes de falsificação e compatibilidade em `test_calculation_traces_f01.py`.

**3. Verificação automática de 6 gates e 10 AC:**
- `scripts/f01_gate_dashboard.py` cruza `QA3_MANIFEST.json` com `ORCHESTRATOR_STATE.json`, exige unicidade de G01–G06, AC-01.01–10 e QA-01–03, acusa falsos `accepted=true`, signoff ausente ou `F01=DONE` prematuro. Modo comum imprime status com exit 0 quando coerente; `--strict` retorna exit 1 enquanto faltam evidências.
- A CI grava `run-artifacts/f01-evidence-status.json` e publica o artefato `f01-evidence-status`. **Não atualiza/aprova automaticamente** nenhum status do orquestrador.

**4. Preparação de inventário normativo sem dados fictícios:**
- `scripts/f01_inventory_audit.py` compara todas as 13 categorias codificadas EDP ao inventário de 24 dependências de código, detecta omissão e proíbe status numérico de homologação.
- `--write-pending run-artifacts/f01-cells-to-review.json` produz fila estruturada de **24 grupos candidatos**, com `cell_instances=[]`, sem valores normativos preenchidos nem segunda conferência inventada. O artefato `f01-cells-to-review` é disponibilizado pelo GitHub Actions.
- Esses 24 itens **não** representam 24 células originais verificadas ou o universo exaustivo de células aplicadas: ainda é preciso desdobrar cada condição do motor e inspecionar a fonte primária.

**5. Comprovação de CI:**
- Commit `3d581d69f885e5d1202be4249e0fdae09e81694c`: **247 testes Python aprovados**, 1 warning, auditorias de workflow/inventário/gates e replay original F00; workflow https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39207007457 .
- Workflow AIOX aprovado no mesmo commit: https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39207007434 .
- Chromium: https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39207007462 (verificar sua conclusão antes de citar como PASS).
- Mudanças no relatório/estado exigem **nova verificação do SHA final da branch**, não extrapolar testes de commit intermediário.

**Bloqueios após esta implementação:** `F00=DONE`, `F01=BLOCKED`, `F02=NOT_RELEASED`; **0/6 gates aceitos**, **1/10 AC formalmente aprovado**, **0/3 agentes QA independentes**, **0 células primárias homologadas**. Evidência externa ABNT/EDP + dois leitores reais e secret Copilot continuam indispensáveis.

## Rodada adicional — 19/10/2026: G06 comprovabilidade e pré-teste Copilot CLI sem credenciais

**Implementações efetivas (não nova fase/novo plano):**
1. `scripts/f01_qa3_evidence_bundle.py`: agrega **três primeiros pareceres e três revisões cruzadas reais** (nove arquivos: três JSON, seis MD), confere SHA de baseline e run ID, revalida bloqueios/não aprovação e calcula SHA-256 de cada artefato. O arquivo `QA3_EVIDENCE.json` documenta execução de jobs, **não confere fontes normativas nem cria parecer profissional**.
2. `f01-copilot-qa-isolated.yml`: novo job `evidence-bundle` condicionado a todos os seis jobs anteriores, baixa os seis artefatos do mesmo workflow, verifica e arquiva `f01-qa3-evidence-<run_id>`. O relatório de resumo distingue trabalho dos agentes, agregação e signoff externo.
3. `f01-copilot-qa-isolated.yml`: novo job `cli-smoke` que instala **@github/copilot em Node 22** e confere `copilot --help` para opções usadas no workflow sem fornecer token à CLI e sem invocar nenhum modelo. Os três agentes **dependem** do sucesso desse preflight.
4. `scripts/f01_qa_workflow_audit.py`: verificações estruturais agora cobrem `cli-smoke`, agregação das seis execuções, artefatos baixados, hashes e permissões de checkout.
5. `test_f01_qa3_evidence_bundle.py` e `test_f01_integrated_preflight.py`: casos adversariais de arquivo ausente, SHA trocado, tentativa de passar gate sem prova, credenciais em parecer e supressão das salvaguardas. Os arquivos sintéticos **NÃO** são contados como QA executado.

**Execução real de infraestrutura:** GitHub Actions [run 39243775881](https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39243775881) confirmou o job `Validate real Copilot CLI flags without token or AI inference` = **SUCCESS**. O `preflight` falhou **exatamente** em `F01_COPILOT_PAT` ausente. Os agentes e `evidence-bundle` foram corretamente SKIPPED; 0 sessões independentes executadas. Isto prova instalação e suporte de opções CLI **na versão instalada nesse run**, não prova modelo autenticado ou execução de agentes.

**Próximo desbloqueio estritamente externo:** titular da conta cadastra `F01_COPILOT_PAT` nas Actions Secrets e reexecuta o último run da F01 com workflow; então QA-01/02/03 e cruzadas devem gerar o bundle `QA3_EVIDENCE.json`. Ainda são necessárias fontes normativas ABNT/EDP, reconciliação real de cada célula e atestação profissional, sem alteração arbitrária dos gates.

**Invariantes:** F00 DONE intocada, F01 BLOCKED, F02 não liberada, 0/6 gates aceitos, 1/10 AC formalmente aprovado, 0 células normativas homologadas, 0/3 agentes executados até evidência real.

## Execução real QA3 — 19/10/2026: bloqueio de política GitHub Copilot

**Solicitação do usuário:** secret `F01_COPILOT_PAT` cadastrado; iniciar 3 agentes independentemente na branch F01 sem reabrir F00.

**Tentativa A — https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39258820804**
- Commit `fcc9b37a709701e3ae10cb90951e5832756ddf0b` com gatilho de execução.
- `cli-smoke=SUCCESS`; `preflight=SUCCESS` (isso comprova a presença de texto no secret, **não** autorização real do serviço Copilot).
- Os 3 jobs `first-pass=FAILURE` pela CLI GitHub Copilot 1.0.98: `Invalid value for --max-ai-credits: "6". Use at least 30 AI credits.`
- `cross-review=SKIPPED` e `evidence-bundle=SKIPPED`. **Nenhum parecer gerado.**

**Correção aplicada — commit `98ef1706de4776b27309c379f2dcfa5b44e6c0a1`:** elevar `--max-ai-credits` de 6 para **30** em primeira leitura e revisão cruzada, menor valor aceito pela CLI 1.0.98. Limite flexível por sessão, sem representar autorização de cobrança irrestrita.

**Tentativa B — https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39259071550**
- Mesmo commit `98ef1706de4776b27309c379f2dcfa5b44e6c0a1`. `cli-smoke=SUCCESS`; `preflight=SUCCESS`.
- Os três jobs QA-01/QA-02/QA-03 `FAILURE` na execução real de `copilot -p` com mensagem idêntica `Error: Access denied by policy settings`.
- A CLI recebeu a variável de ambiente `COPILOT_GITHUB_TOKEN` mascarada (`***`), mas a presença do token não garante licença/política ou direito à inferência.
- Não houve resultados QA suficientes para `PARECER_QA.md`, `MATRIZ_6_GATES.json` ou revisões cruzadas; seis jobs independentes não concluídos. **Não declarar G06 concluído.**

**Causa raiz de bloqueio verificável:** o serviço remoto GitHub Copilot recusou inferência por *policy settings*; conforme https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/troubleshoot-copilot-cli-auth, verificar licença Copilot da conta pessoal e políticas Copilot CLI da organização, quando aplicável. Verificar também que o fine-grained PAT tem **Account → Copilot requests: write**; `Copilot agent settings: read` não substitui essa permissão. A documentação oficial https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens lista `copilot_requests` somente com nível `write`.

**Próxima execução:** **NÃO acionar retries automáticos enquanto o usuário não confirmar licença Copilot CLI habilitada e permissão correta**. Depois, novo run na branch F01 por `COPILOT_RUN_REQUEST.md`, com checagem real do primeiro agente antes de disparar consumo múltiplo. Caso a política continue negando, registrar exceção externa com request ID para suporte GitHub, sem tentar contornar política ou atribuir revisão profissional fictícia.

**Estado:** F00 DONE; F01 BLOCKED; F02 NOT_RELEASED; 0/3 sessões independentes finalizadas, 0/3 revisões cruzadas, 0/6 gates aceitos. `main` preservada.


## Adendo documental prevalecente — PDF privado recebido em 2026-10-19

Recebido para inspeção privada um PDF de 217 páginas cuja capa identifica NBR 5410:2004, versão corrigida em 17/03/2008. SHA-256 do arquivo recebido: `45f246e3e33db1bf18dd60743ac93b6ac1ec0796742e169a8014682bfb19aa3d`. Esta identificação não comprova autenticidade, origem oficial, licença, direitos de reprodução ou aplicabilidade. PDF, imagens e valores das células não são publicados no repositório.

Mapa documental informado pela leitura visual do coordenador, um único leitor, páginas PDF 109–118 inspecionadas:

| Referência | Página PDF | Página impressa |
|---|---|---|
| Tabela 36 | 109 | 101 |
| Tabela 37 | 110 | 102 |
| Tabela 38 | 111–112 | 103–104 |
| Tabela 39 | 112–113 | 104–105 |
| Tabela 40 | 114 | 106 |
| Tabela 41 — resistividade térmica do solo; não resistência elétrica | 115 | 107 |
| Tabela 42 | 116 | 108 |
| Tabelas 43 e 44 | 117 | 109 |
| Tabela 45 | 118 | 110 |
| Notas de agrupamento, leitura ainda pendente | 119–120 | 111–112 |

Estado da fonte: RECEBIDA / INSPEÇÃO DOCUMENTAL PARCIAL. Este mapa não é extração numérica de células, não é dupla leitura A/B e não concede homologação: zero células aprovadas por este adendo. Continuam pendentes contexto/método/notas, leituras independentes, direitos/origem e casos quantitativos. Valores sintéticos da UI não foram substituídos pelo PDF. F01 BLOCKED; F02 não liberada.

## Parecer recebido em 2026-10-20 — aceite condicionado do lote 01

O documento recebido declara aceite no escopo de 8 células e 6 casos, condicionado integralmente ao Anexo A. Os checkboxes desse anexo continuam vazios e há campos de identificação profissional/registro/data/assinatura por preencher. Registrar **ACEITE_CONDICIONADO**, não homologação nem signoff concluído. P01–P08 permanecem pendentes; nenhuma flag de liberação é alterada. O parecer integral e seus dados pessoais não são publicados.

R3: o parecer informa exemplar de PDF com SHA-256 `e1c02de1e1b5ed070ad7b642e60e0491a0c899e83fe8f2ad5699a743842bbda6`, diferente do exemplar privado anteriormente recebido `45f246e3e33db1bf18dd60743ac93b6ac1ec0796742e169a8014682bfb19aa3d`. São fontes distintas para fins de proveniência. Não substituir hashes, presumir equivalência ou atribuir dupla leitura ao mesmo arquivo sem resolver a divergência.

R1/P03 continua risco alto: I2 exige identificação/fonte do dispositivo e contexto; não presumir universalmente I2=1,45In. A NOTA da proteção é condicional ao regime/tempo de sobrecarga, não requisito universal. Proteção completa, curto-circuito, coordenação e aplicação real continuam pendentes. R6 permanece pendente no pacote de entrega original preservado; este incremento não modifica esse pacote.

### R4 — coordenação funcional corrigida

Antes, uma seção que suportava Ib podia ser escolhida mesmo sem disjuntor comercial admissível, causando rejeição quando seção maior permitiria par. A aplicação agora encontra o menor In comercial ≥ Ib, seleciona a menor seção com Iz ≥ esse In e revalida Ib ≤ In ≤ Iz. Para catálogo fixo independente da seção, isso equivale a percorrer seções até existir par. O primitivo selecionar_condutor e sua semântica/F00 não foram alterados. Cenário sintético de regressão Ib=20,5 e fator=0,87 passa a selecionar seção 4 e In=25; ausência de catálogo/par continua rejeitada. Critério e aviso declaram I2 não verificado.

Trilhas novas registram `orchestration_source` com ID e SHA-256 da função coordenadora; versões v1/v2 anteriores continuam legíveis sem backfill. Hash do arquivo application.py: `78ff6a6032f2657a9f7b86fca22e5c165b20670bb82042ff97e9dbbca2089e73`; hash da função: `1b553bff8823f066da876cc79d335cbfd0cac95d5a9d4bcfcef0a3f53d7bd090`.

Validação focada local: 91 testes passaram, incluindo 11 casos novos de coordenação/proveniência, fronteiras exatas sem arredondamento para decisão, catálogo ausente/insuficiente, nenhum par, HTTP e gate false. Revisão independente do coordenador confirmou os casos novos e regressões API/traces. CI do SHA publicado deve ser conferida; não equivale a nova homologação por três revisores. F01 BLOCKED; G04/G06 não aprovados; F02 não liberada.

### Ajuste de compatibilidade do diagnóstico F00
A primeira CI da correçãoR4 detectou mudança apenas na mensagem do caso congelado ANALISE-IZ-ARREDONDADO: havia capacidade paraIb, mas não par comercial. A seleção agora validaIb primeiro e distingue explicitamente ausência de capacidadeIb de ausência de parIn/Iz, preservando a mensagem de segurança anterior sem alterar fixture/primitivosF00.92 testes focados locais passaram,12casos novos no total. Hash atualizado da função coordenadora (a trilha grava esse hash automaticamente): `0021874e4bb77675bca71c36c167f359d61b36cf1bb45ba31616f04946756c7d`. O hash anterior acima descreve o primeiro incremento, não a função atual. CI final deve confirmar replay congelado; não se concede homologação.

## Atualização P06/P03 — lote 01, 2026-10-20

Recebido aceite profissional declarado e confirmado no JSON privado, SHA-256 `2ffbed5b4cb89a10eed13a42acac1fad4daa3873b90c30b5a9439af8846fdd6c`: 8 células e 6 casos aceitos apenas no escopo do lote, P01–P08 pendentes. Nome, registro profissional e documento integral não são publicados; o registro sanitizado é `ACEITE_PROFISSIONAL_LOTE01_RECEBIDO_2026-10-20.json`. A referência declarada pelo responsável é o PDF `e1c02de1e1b5ed070ad7b642e60e0491a0c899e83fe8f2ad5699a743842bbda6`, distinto do exemplar anteriormente recebido `45f246e3e33db1bf18dd60743ac93b6ac1ec0796742e169a8014682bfb19aa3d`. Não se presume equivalência nem autenticação independente da credencial/assinatura.

Incremento limitado implementado: registro server-side versionado e vínculo de IDs/condições/capacidades/fatores antes do cálculo; isolamento PVC/EPR, método e condições de agrupamento/temperatura/radiação. Verificação parcial de sobrecarga usa I2 declarado com proveniência do dispositivo, sem deduzir I2 de In; trata o limite ordinário e a NOTA conforme duração informada. Proveniência e condições integram a trilha, com rejeição de remoção/adulteração e compatibilidade histórica sem backfill. Exemplo CLI/API e limites constam em `IMPLEMENTACAO_P06_P03_LOTE01.md`.

Validação informada pelo implementador: 200 testes locais passaram após ajuste de radiação infravermelha; revisão independente QA aprovou o incremento restrito com testes e combinações adversariais. CI do SHA publicado deve confirmar regressões completas/F00, AIOX e Chromium. Não se executa nova rodada QA3 cara neste marco parcial. QA3 operacional anterior foi 3+3 SUCCESS no run `39289599183` e baseline `29c506cbd4f0045c4d54e4f50098d989d7260194`, não revisão do código posterior.

**P03 e P06 não concluídas integralmente. F01 BLOCKED; F02 não liberada.** Próximos bloqueios: proteção contra curto-circuito, seletividade/coordenação completa, proveniência verificada de dispositivos, cobertura de células e condições fora do lote, EDP, reconciliação dos exemplares/fontes e revisão final do SHA. O aceite limitado 14/8 não libera o motor, a instalação nem produção.
