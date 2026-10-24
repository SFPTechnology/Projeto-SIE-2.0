# Story SIE-F10 — Artefatos gráficos e documentação rastreável

**Estado:** IN_PROGRESS (não homologado)
**Branch de desenvolvimento:** `feat/f09-concessionarias-especializadas`
**Fonte:** `docs/implantacao-sie-2-0/F10/PLANO_IMPLEMENTACAO.md`, `RELATORIO_EXECUCAO.md` e critérios AC-10.01–AC-10.10 do orquestrador.
**Restrições:** preservar main, sem deploy, sem migração produtiva ou homologação normativa.

## Objetivo
Conectar representação e exportação F10 a snapshots verificáveis, à revisão e execução de cálculo; detectar obsolescência e bloquear inconsistências, sem criar dados técnicos fictícios.

## Critérios de aceite
- [ ] AC-10.01: artefatos persistidos identificam projeto, revisão, cálculo, regras e template; snapshot e hashes verificáveis; integridade fail-closed
- [ ] AC-10.02: planta com origem autorizada, escala/unidade controlada, geometria explícita e vínculos com elementos
- [ ] AC-10.03: símbolos versionados, legenda e origem
- [ ] AC-10.04: diagrama derivado de grafo; circuitos do quadro correto, sem ligações fictícias
- [ ] AC-10.05: quadros de cargas consistentes com revisão e execução
- [ ] AC-10.06: quantitativos com proveniência e sem comprimentos criados
- [ ] AC-10.07: memorial técnico com cálculos/fórmulas somente se rastreáveis
- [ ] AC-10.08: formatos obrigatórios e verificações de integridade; PDF conforme capacidade aprovada
- [ ] AC-10.09: prévia, impressão, navegação, segurança visual e acessibilidade
- [ ] AC-10.10: reconciliação entre modelo, artefatos e cálculos com bloqueio de divergência crítica
- [ ] QA-01/02/03 formais e CI aplicável efetivamente aprovados

## Unidade executiva priorizada — W1
- [ ] W1-01: carregar projeto/revisão histórica e verificar seu hash a partir de `RepositorioProjetos`, sem aceitar snapshot de origem declarado pelo cliente.
- [ ] W1-02: identificar e validar `CalculationRun` persistido da revisão/circuito e documentar exatamente as dependências consumidas pelo bundle W1; não reinterpretar `ensaios_calculo` como run F02 nem incluir estudos F06–F08 sem lineage/fingerprint verificável.
- [ ] W1-03: congelar snapshot e contrato antes de renderizar; falhar fechado em mutação/serialização inválida.
- [ ] W1-04: persistir registro autoritativo de artefato e estado de publicação com recuperação/idempotência local; não afirmar atomicidade DB/filesystem.
- [ ] W1-05: validar CLI/API existente, autenticação local e isolamento; documentar que token global não constitui ACL multiusuário.
- [ ] W1-06: adicionar testes de integração SQLite para revisão/ensaio, dados cruzados/inexistentes, falha/retry e mutação concorrente; executar gates locais disponíveis.
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
