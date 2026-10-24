# W1 — Matriz QA independente de execução efetiva do motor

Task: W1-MOTOR-QA-PREP. Estado: READY para preparação; execução dependente do contrato final. Branch conhecida feat/f09-concessionarias-especializadas; HEAD 52b74702d4e55258b287fc8211240ff6e00dffaa, diff local preservado. Nenhum gate aprovado neste documento.

## Fontes inspecionadas

AGENTS.md, Constituição, story SIE-F10, parecer W1_QA_LOCAL; `persisted_source_f10._resolve_persisted_source` valida identidade/estado/output hash declarado e sinaliza NOT_SERVER_ATTESTED; `installation_service.analyze_legacy` e `CalculationRecord` são a base real indicada para execução, entradas e resultados. `storage_api.executar_ensaio_circuito` chama registro de ensaio; não equivale automaticamente a vínculo com CalculationRun.

## Casos para implementação e revisão

| ID | Cenário | Resultado exigido | Nível |
|---|---|---|---|
| M01 | Rodar analyze_legacy com snapshot persistido e parâmetros reais da fixture aprovada | Resultado persistido corresponde à execução real e W1 resolve seu vínculo | Integração SQLite/parser/motor real |
| M02 | Run VALID com output hash arbitrário, sem registro de execução | Rejeição, nunca ATTESTED | Negativo real |
| M03 | Resultado/registro de outro projeto, circuito ou revisão | Rejeição por incompatibilidade | Integração |
| M04 | Parâmetros/entrada mudam após captura | Snapshot publicado e executado permanecem coerentes ou geração falha | Concorrência |
| M05 | Resultado adulterado, hash não recomposto | Integridade falha | Adversarial |
| M06 | Resultado e hash adulterados conjuntamente no registro | Reexecução/referência autoritativa detecta divergência dentro do trust boundary | Adversarial |
| M07 | Versão de algoritmo, regra, contexto/fingerprint diverge | Falha fechada/estado obsoleto conforme contrato | Integração |
| M08 | Alteração de parâmetros mantendo mesmo circuito | input_sha256 muda e resultado antigo não é aceito | Unitário + integração |
| M09 | Interrupção antes/depois do motor e antes/depois do registro final | Ausência de falso sucesso, recovery/retry explícito | Processo/fault injection |
| M10 | Retry simultâneo ou repetido | Idempotência conforme contrato, sem sobrescrita | Concorrência real |
| M11 | CLI recebe resultado/hash declarado pelo cliente | Não usa cliente como autoridade de execução | CLI negativo |
| M12 | Geração/verify após reabertura do banco/processo | Vínculo e integridade recuperáveis; atualidade correta | Integração |
| M13 | Ausente/falho/parcial/stale ou legado sem evidência | Não promovido retroativamente a execução comprovada | Integração |
| M14 | Regressões W1 snapshot/registry/recovery/currentness | Comportamento preservado | Suíte focada e completa |

QA deve utilizar CalculationRecord e analyze_legacy reais; mocks apenas para unidades/fault injection declarados. Comparar result_json/result_sha256/input_sha256/versionamento e saída do motor conforme contrato aprovado. Não criar resultado técnico fictício nem equivalência entre ensaio e run.

## Evidência

Cada execução registrará comando, cwd, fixture, resultado, duração/exit code disponíveis, ambiente e SHA ou estado de diff efetivamente testado. Teste local não equivale a CI. Nenhuma execução desta matriz ocorreu durante o preparo. Parecer final exige contrato integrado, candidato congelado e revisão independente do diff final.

## Segurança

Negativos compartilhados pelo especialista: execução inexistente/cruzada, run fabricado, versões incompatíveis, adulteração coerente, inputs persistidos alterados e output divergente de reexecução. Locks cooperativos não comprovam proteção contra troca maliciosa externa de ancestrais symlink; manter trust boundary filesystem privado documentado.

## Reteste independente do incremento integrado

QA executou no diff local sobre HEAD informado, após integração de `executar_calculo_f10`, `consultar_calculo_f10` e adaptador/CLI:

- `python -m pytest -q tests/test_storage.py`: 10 passed, 1 warning, 0.64s, exit 0 (antes das duas ampliações de teste do owner).
- `python -m pytest -q tests/test_storage.py tests/test_persisted_source_f10.py tests/test_persisted_source_f10_sqlite.py tests/test_artifact_registry_f10.py tests/test_artifact_store_f10.py`: 71 passed, 1 warning, 2.46s, exit 0.
- `python -m pytest -q`: 1120 passed, 1 warning, 20.05s, exit 0.
- cwd de todos: `restructuring/apps/api`. Aviso: depreciação Starlette/httpx do ambiente, não falha de teste.

Inspeção confirmou ponte explícita `CalculationRecord.result_sha256` → `CalculationRun.output_sha256`, parâmetros exclusivamente da revisão persistida, execução `analyze_legacy` real, evidência append-only, versões atuais e snapshot vinculados na consulta. A fixture F05 real executa motor antes de construir run compatível, persiste parâmetros e testa CLI execute/publicação/verificação sem mocks parser/motor. Costuras unitárias com evidence mockada não são consideradas comprovação do motor.

Não foi reproduzido bloqueio funcional no conjunto executado. A lacuna anterior NOT_SERVER_ATTESTED foi corrigida para o recorte legado suportado; isso não significa homologação normativa. Banco/filesystem privados continuam a autoridade de confiança; hash/trigger não demonstram proteção contra ator que pode reescrever o banco/remover triggers.

Parecer: evidência local favorável à implementação de G01 no recorte atual. CI e SHA candidato final permanecem NOT_VERIFIED por este QA; W1 global não aprovada por esta evidência de diff. O parecer W1_QA_LOCAL anterior deve ser lido como checkpoint histórico superado quanto à ausência da execução server-side.

## Reteste final após sete negativos adicionais

Após congelamento do código comunicado pelo orquestrador, este QA repetiu `python -m pytest -q`, cwd `restructuring/apps/api`: **1127 passed, 1 warning in 17.92s**, exit 0. Esse resultado substitui a contagem 1120 para o diff final desta rodada e inclui os novos casos de mismatch dos campos críticos. O aviso é a mesma depreciação Starlette/httpx. Nenhuma alteração produtiva foi realizada pelo QA. DevOps recebeu o resultado diretamente para consolidação do candidato; CI permanece separado desta evidência local.
