# Story SIE-F10 — Artefatos gráficos e documentação rastreável

**Estado:** READY_FOR_REVIEW / VALIDATED_LOCAL_PENDING_CI (não homologado)
**Branch de desenvolvimento:** `feat/f09-concessionarias-especializadas`
**Fonte:** `docs/implantacao-sie-2-0/F10/PLANO_IMPLEMENTACAO.md`, `RELATORIO_EXECUCAO.md` e critérios AC-10.01–AC-10.10 do orquestrador.
**Restrições:** preservar main, sem deploy, sem migração produtiva ou homologação normativa.

## Objetivo
Conectar representação e exportação F10 a snapshots verificáveis, à revisão e execução de cálculo; detectar obsolescência e bloquear inconsistências, sem criar dados técnicos fictícios.

## Critérios de aceite
- [x] AC-10.01: artefatos persistidos identificam projeto, revisão, cálculo, regras e template; snapshot e hashes verificáveis; integridade fail-closed
- [x] AC-10.02: planta com origem autorizada, escala/unidade controlada, geometria explícita e vínculos com elementos
- [x] AC-10.03: símbolos versionados, legenda e origem
- [x] AC-10.04: diagrama derivado de grafo; circuitos do quadro correto, sem ligações fictícias
- [x] AC-10.05: quadros de cargas consistentes com revisão e execução
- [x] AC-10.06: quantitativos com proveniência e sem comprimentos criados
- [x] AC-10.07: memorial técnico com cálculos/fórmulas somente se rastreáveis
- [x] AC-10.08: formatos obrigatórios e verificações de integridade; PDF conforme capacidade aprovada
- [x] AC-10.09: prévia, impressão, navegação, segurança visual e acessibilidade
- [x] AC-10.10: reconciliação entre modelo, artefatos e cálculos com bloqueio de divergência crítica
- [x] QA-01/02/03 formais e CI aplicável efetivamente aprovados

## Unidade executiva priorizada — W1
- [x] W1-01: carregar projeto/revisão histórica e verificar seu hash a partir de `RepositorioProjetos`, sem aceitar snapshot de origem declarado pelo cliente.
- [x] W1-02: identificar e validar `CalculationRun` persistido da revisão/circuito e documentar exatamente as dependências consumidas pelo bundle W1; não reinterpretar `ensaios_calculo` como run F02 nem incluir estudos F06–F08 sem lineage/fingerprint verificável.
- [x] W1-03: congelar snapshot e contrato antes de renderizar; falhar fechado em mutação/serialização inválida.
- [x] W1-04: persistir registro autoritativo de artefato e estado de publicação com recuperação/idempotência local; não afirmar atomicidade DB/filesystem.
- [x] W1-05: validar CLI/API existente, autenticação local e isolamento; documentar que token global não constitui ACL multiusuário.
- [x] W1-06: adicionar testes de integração SQLite para revisão/ensaio, dados cruzados/inexistentes, falha/retry e mutação concorrente; executar gates locais disponíveis.
- [x] Produzir pacote de exportação que guarda o snapshot canônico e um manifesto com sha256 por arquivo
- [x] Publicar pacote no sistema de arquivos local de maneira atômica e sem sobrescrita
- [x] Implementar verificação de conteúdo e estado de obsolescência quando a origem atual for conhecida, sem declarar atualidade na ausência de origem
- [x] Cobrir adulteração de snapshot/exportação, mudança de dependência, revisão incompatível e não sobrescrita
- [x] Corrigir isolamento de painéis no unifilar e cobrir com teste adversarial

## Lista de arquivos e verificações
A atualizar após cada incremento, com referências aos commits, workflow runs e limitações.

**Escopo autorizado de implementação W1 nesta continuação:** `restructuring/apps/api/sie_api/{artifact_store_f10.py,persisted_source_f10.py,storage.py,artifact_registry_f10.py}` e testes correspondentes, além deste registro. Alterações futuras em outros arquivos exigem atualização da story antes da edição.

**Incremento W1 em andamento (workspace local):** `persisted_source_f10.py` foi incorporado do protótipo experimental após comparação com `RepositorioProjetos`, `topology.load_document` e `CalculationRun`; não se usa `ensaios_calculo` como identidade de run F02. O gerador congela snapshot/contrato antes de renderizar para evitar divergência por mutação concorrente da entrada. Testes de integração inicializados; persistência autoritativa de estado/reconciliação entre SQLite e filesystem e QA independente ainda precisam de comprovação.

**Arquivos adicionados/alterados nesta execução:**
- `restructuring/apps/api/sie_api/persisted_source_f10.py` — resolução, geração e verificação contra revisão histórica e CalculationRun persistidos; suporte intencionalmente restrito a um circuito terminal e um cable run.
- `restructuring/apps/api/tests/test_persisted_source_f10.py` — testes do adaptador e comportamento fail-closed.
- `restructuring/apps/api/tests/test_persisted_source_f10_sqlite.py` — teste SQLite real da fronteira de leitura histórica (parser F05 isolado por patch).
- `restructuring/apps/api/sie_api/artifact_store_f10.py` — snapshot/contrato capturados antes da renderização.
- `restructuring/apps/api/tests/test_artifact_store_f10.py` — teste adversarial de mutação durante renderização.

**Validação local desta execução:** suíte API `python -m pytest -q` — 1087 passed, 1 warning; gates do repositório `npm run lint`, `npm run typecheck`, `npm test` (18 verificações) e `npm run build` concluídos com exit 0 após instalação das dependências declaradas em `.aiox-core/package-lock.json`. Esses resultados são locais ao workspace ainda não commitado e não substituem CI no SHA final nem QA independente. G02 segue parcial: registry durável e reconciliação/recuperação coordenada SQLite/filesystem, crash/restart e concorrência de publicação não foram implementados ou demonstrados nesta fatia.

**Continuação autorizada:** implementar registro SQLite local append-only de eventos e estados controlados de publicação, com reconciliação após interrupção; integrar ao adaptador/publisher e ampliar testes de recovery antes de rever o estado de W1-04/G02. Não alterar schema de produção nem interpretar ensaios locais como runs F02.

**Limite de dependências do bundle W1:** os renderizadores vigentes consomem snapshot topológico F02/F05 e a identidade de um `CalculationRun`; não incorporam estudos F06–F08. Portanto, a matriz deve provar essa lista de dependências do código. Se um artefato W1 passar a consumir dados F06–F08, deverá validar seus modelos, fingerprints e resultados antes de incluí-los. O estado `VALID` e os hashes declarados de `CalculationRun` são rastreados como dados persistidos, mas não são uma certificação independente de execução do motor.

## Limite de aceite
Testes automatizados não representam homologação normativa nem substituem revisões formais. Qualquer aceite remanescente conserva seu estado pendente até comprovação.
## Checkpoint verificável — 23/10/2026
**Onda W1 parcial**: adaptador integrado às revisões persistidas e à identidade declarada de CalculationRun. A execução server-side do motor ainda não é atestada. Os cinco subitens acima estão implementados e testados; isso NÃO significa AC-10.01 concluído, nem W1 VALIDATED.

**Arquivos incluídos/alterados**
- `restructuring/apps/api/sie_api/artifact_store_f10.py` — serialização canônica, manifesto, hashes por arquivo, publicação local com staging/lock e verificações de integridade/obsolescência condicionais à fonte fornecida.
- `restructuring/apps/api/sie_api/representation_f10.py` — CLI existente usa exportação verificada, separação de circuitos por quadro, validação de unidade da planta e execução CLI com planta.
- `restructuring/apps/api/tests/test_artifact_store_f10.py` — testes adversariais do pacote.
- `restructuring/apps/api/tests/test_representation_f10.py` — testes de unifilar multiquadro e CLI com manifesto.
- `docs/implantacao-sie-2-0/F10/MATRIZ_VERIFICACAO_V2.md` e `REGISTRO_OPERACIONAL.json` — evidências e retomada.

**CI verificado no commit de código** `afd73f02e2cd41ee1c2d8615c31616e90d65e4c0`: API 39953127011 (**1070 passed; 1 warning**), AIOX 39953126910 (**success**), Chromium 39953127014 (**success**). Browser genérico não equivale a teste visual específico F10. A aprovação formal de QA-01/02/03 segue PENDING.

**Próxima unidade:** integrar a origem canônica das revisões (SQLite `versoes_projeto`) e as execuções `ensaios_calculo` no gerador, com checagem da identidade e invalidação ao modificar a revisão/cálculo; não aceitar como confiável uma identidade de cálculo apenas informada pelo cliente.


## Retomada YOLO — 24/10/2026

Baseline reconfirmada: HEAD `52b74702d4e55258b287fc8211240ff6e00dffaa`; alterações locais preservadas. Registry SQLite, transições CAS, hash autoritativo externo ao pacote, lock e recovery já implementados no diff; a descrição anterior de G02 não implementado está superada, mas não equivale a aprovação.

Revisão de domínio confirmou: renderer W1 não consome resultados F06–F08. Permanece pendente comprovação de execução server-side do CalculationRun (NOT_SERVER_ATTESTED). QA independente em `docs/implantacao-sie-2-0/F10/W1_QA_LOCAL.md`. Sem CI do candidato e sem operações remotas.

Validação reproduzida nesta retomada: suíte API `python -m pytest -q`: 1114 passed, 1 warning, 17.72s, exit 0. QA independente executou 65 testes focados, exit 0. Gate G01 continua PARTIAL pela falta de atestação efetiva do motor; W1 não foi aprovada. Evidências referem-se ao diff local sobre HEAD, não a um commit candidato final.

## Contrato de execução efetiva W1 — continuação autorizada

Decisão arquitetural: reutilizar `installation_service.analyze_legacy`, `CalculationRecord` e `algorithm_identity` sobre snapshot F02 da revisão externa validada. Parâmetros `AnaliseCircuito` devem estar explicitamente persistidos na mesma revisão em `calculation_inputs_f10[run_uuid]`. Run e evidência devem coincidir em projeto, revisão, circuito, hashes de entrada/resultado, algoritmo e regra. Legado sem mapa ou incompatível falha fechado, sem inferir vínculo com ensaios locais.

Escopo de escrita autorizado antes da implementação: `storage.py`, `persisted_source_f10.py`, testes correspondentes e eventual serviço mínimo de coordenação F10; documentação canônica de contrato, segurança, QA e evidências. Evidência de execução persistida deve ser append-only e vinculada ao hash da revisão externa e snapshot F02. Não atribui homologação normativa.

## Implementação efetiva do motor — resultado local

Implementados `executar_calculo_f10` e `consultar_calculo_f10`: execução de `analyze_legacy` sobre revisão persistida e parâmetros explícitos; registro `execucoes_motor_f10` append-only; validação cruzada de projeto, revisão, snapshot, circuito, run, hashes, algoritmo e regra. Adaptador exige evidência íntegra; CLI `execute` não aceita parâmetros de cálculo do cliente. Origem passa a `SERVER_EXECUTED_LEGACY_MOTOR` somente após essa comprovação. Legado sem evidência falha fechado.

O teste SQLite real executa motor e parser oficiais antes de publicar/verificar o bundle. Resultados anteriores de G01 PARTIAL por ausência de execução ficam superados pela nova implementação, mas decisão de aprovação depende dos pareceres independentes e CI no candidato. Hashes não representam assinatura nem homologação normativa; banco e diretório privados são a fronteira de confiança.

Regressão local final independente: 1127 testes API passaram, 1 warning, 17.92s, exit 0, após os sete negativos finais. Lint/typecheck/npm test/build exit 0 na execução do orquestrador. QA independente favorável ao recorte suportado; CI ainda pendente no candidato. Novos documentos: `W1_CONTRATO_EXECUCAO_MOTOR.md`, `W1_MOTOR_QA_MATRIX.md` e pareceres finais nos caminhos canônicos F10. Sem alterações em main ou produção.


## Fechamento W1 — escopo de CI autorizado

File list adicional antes da edição: `.github/workflows/sie-restructuring-api.yml`, `.github/workflows/sie-orchestrator-quality.yml`, `.github/workflows/sie-e2e-browser.yml`, `MATRIZ_VERIFICACAO_V2.md`, `REGISTRO_OPERACIONAL.json` e `RELATORIO_EXECUCAO.md` na pasta F10. Incluir os paths da story/F10 nos três workflows garante CI no SHA final de documentação/configuração. Não altera motores nem amplia funcionalidades.


## Decisão W1 — candidato de fechamento em 24/10/2026

Código avaliado: `283c4fa66592f3f07daf7e52e24cf2d75895798b`, tree `4ade0d26e90e4c24480e3b5bb3285d8e2b694e12`. Revalidação nesse SHA: `python -m pytest -q` (cwd `restructuring/apps/api`), **1127 passed, 1 warning, 21.53s, exit 0**; lint/typecheck/npm test/build exit 0. QA independente reproduziu 1127 testes no diff e 78 focados no candidato; pareceres `W1_MOTOR_QA_MATRIX.md` e `W1_MOTOR_SECURITY.md`.

G01 e G02 são tecnicamente satisfeitos no recorte local documentado: um circuito/run/cable_run, motor `analyze_legacy`, parâmetros explicitamente persistidos na revisão, banco e filesystem privados e escritores cooperativos. A execução efetiva é registrada e conferida contra revisão/snapshot/inputs/resultado/versões. Fonte indisponível nunca é CURRENT. Não há ACL multiusuário nem garantia contra ator com poder de reescrever banco ou trocar ancestrais filesystem. F06–F08 não são consumidos pelo renderer W1. Não representa homologação normativa.

**Decisão de fechamento:** W1_DONE no recorte suportado somente após sucesso dos três workflows no SHA deste candidato de fechamento. Antes de conferir esses resultados, estado global é VALIDATED_LOCAL_PENDING_CI. Os resultados de SHA anterior abaixo são referências históricas, não aprovação automática do SHA deste documento. F10 permanece RUNNING; F09 permanece DONE; ondas B–E continuam fora do escopo.

Workflows exigidos no candidato: `SIE modular API`, `SIE Orchestrator AIOX Quality Gates`, `SIE Browser E2E (Chromium)`. O CI passa a disparar também por mudança na story e documentação F10. Qualquer falha reabre o gate afetado e impede W1_DONE.

## Continuação integral F10 — escopo e contratos liberados antes da implementação

W1 foi concluída no SHA `7d8edda79019fed91396d53e99bd897191d69ba3`, com os três workflows aprovados. Esta continuação inclui as ondas B–E e AC-10.02–AC-10.10, sem alterar main, produção ou declarar homologação normativa.

File list autorizada: novos módulos `sie_api/floorplan_f10.py`, `symbols_f10.py`, `documents_f10.py`, testes `test_floorplan_f10.py`, `test_symbols_f10.py`, `test_documents_f10.py`; integração em `representation_f10.py`, `artifact_store_f10.py`, `persisted_source_f10.py` e testes correspondentes; `pyproject.toml` para PDF real após validar dependência; `sie_api/artifacts_api_f10.py` e registro em `main.py`; UI `restructuring/apps/web/artefatos.html`, `artefatos.js`, navegação existente e testes E2E F10; documentação canônica e workflows somente para gates necessários.

Contratos: base de planta JSON explícita e autorizada por referência declarada, com hash, unidades m/cm/mm, dimensões, escala/calibração e vínculos ID; nunca importar SVG ativo arbitrário nem inventar comprimentos. Catálogo SIE esquemático interno versionado, com origem/legenda e sem atribuição ABNT não verificada. Documentos consomem somente snapshot congelado e resultado efetivo vinculado em `verified_calculation_f10`; não inventam fórmulas ou materiais. PDF real deve ser incluído no manifesto e verificado. CLI permanece caminho primário; UI observa, navega e exporta o resultado do serviço oficial. Toda divergência crítica modelo/cálculo/representação bloqueia publicação. QA-01/02/03 serão realizados por agentes separados e não equivalem a homologação profissional.

### Especificação gráfica integral — correção do contrato antes da implementação dependente

A especificação `ESPECIFICACAO_ENGENHARIA_CAMADA_GRAFICA_F10.md`, consultada pelo orquestrador na fonte original, exige importação de arquivo real PNG/JPEG ou SVG seguro; geometria JSON isolada não satisfaz AC-10.02. Escopo adicional autorizado: preservar original e MIME/tamanho/hash/autorização declarada; calibração confirmada com ator/data; geometria versionada com controle otimista; UI pan/zoom/camadas/seleção de elemento existente/undo-redo/save explícito e aviso de alterações não salvas. `floorplan_f10.py` poderá importar SVG seguro com subset estrito e rejeitar DTD, entidades, scripts, handlers, URLs/href externos e conteúdo ativo. Símbolos exigem origem/licença/versionamento. Diagramas multifilar/prumada só devem ser emitidos se os dados os sustentarem; caso contrário, declarar indisponibilidade com motivo. CAD/BIM permanecem opcionais. UI/API novas podem implementar import/calibrate/geometry/generate/query/history/download nos módulos F10 já autorizados e persistir novas revisões com compare-and-swap; sem tocar produção.

### Correção de cobertura integral após QA-02 — multicircuito/multiquadro

Full não pode herdar a restrição W1 de circuito único. Autoriza-se antes da correção um resolvedor full dedicado, mantendo W1 sem `--full` inalterada: `dados.calculation_runs_f10` mapeia explicitamente cada UUID de circuito ao UUID de run, com cobertura exata sem duplicações/IDs extras; cada cálculo exige execução server-side real validada. O run passado à CLI/API é apenas âncora de identidade do pacote, nunca prova de todos os circuitos. Snapshot inclui `calculation_scope_f10=PER_CIRCUIT_RUN_MAP_V1`, `calculation_dependencies_f10` e `verified_calculations_f10`; quadro e memorial identificam o run e versões de cada circuito. Verificação de atualidade reconsulta todos os cálculos. Contagem de fases (`phases_count`) não é atribuição de fase; sem identificação explícita preservada, `phase=UNSPECIFIED`. Não inferir L1/L2/L3 de `phases=1` ou `3`.

Escopo DevOps de evidência visual: `.github/workflows/sie-e2e-browser.yml` poderá arquivar capturas F10 geradas pelos testes de navegador em `run-artifacts/f10-*`, sem versionar os arquivos temporários nem alterar critérios dos testes.


## Candidato integral F10 — preparação final

Escopo de coerência canônica autorizado antes da edição: somente o nó F10 de `docs/sie-orchestrator/ORCHESTRATOR_STATE.json`; preservar F09, W1, main e produção. Estado local VALIDATED_LOCAL_PENDING_CI; aprovação final depende de QA-03 e três workflows no SHA final, sem liberar F11 antecipadamente.


## Parecer local integral concluído — candidato final

AC-10.01–AC-10.10 e QA-01/02/03 foram implementados/examinados no contrato suportado; checkboxes representam aceite local de software, condicionado ao CI final. QA-01 reproduziu 1181 testes; QA-02 reproduziu 72 focados e inspecionou PDF multi7p; QA-03 concluiu segurança e E2E/print6p/STALE/mobile, com SEC-F10-01 fechado. File list inclui nominalmente `restructuring/apps/api/sie_api/pdf_f10.py`, `test_full_f10_integration.py`, `test_artifacts_api_f10.py`, `restructuring/e2e/test_f10_browser.py` e demais módulos/arquivos F10 listados anteriormente. As três revisões são separadas e não homologam instalações.

Regra final: F10_DONE somente após sucesso dos três workflows obrigatórios no SHA final deste candidato, com fonte/snapshot/runs/asset/versões verificados. Até a consulta desses resultados permanece VALIDATED_LOCAL_PENDING_CI. Não executar F11 neste incremento; main/produção preservadas.
