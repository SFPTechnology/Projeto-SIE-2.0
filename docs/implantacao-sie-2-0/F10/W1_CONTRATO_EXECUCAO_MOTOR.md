# W1 — contrato de execução efetiva do motor

Decisão W1-MOTOR-01, responsável arquitetura/domínio, 24/10/2026. Inspeção estática sobre branch feat/f09-concessionarias-especializadas, HEAD 52b74702d4e55258b287fc8211240ff6e00dffaa e diff local preservado. Não constitui aprovação de gate.

## Evidência existente

- `installation_service.analyze_legacy` executa `application.analisar_circuito` e valida compatibilidade dos parâmetros explícitos com InstallationSnapshot: circuito, corrente/tensão, percurso/cabo/disjuntor; limitações monofásicas resistivas são preservadas.
- `installation_service.CalculationRecord` inclui projeto/revisão/snapshot, circuito, versões, hash de entrada, resultado canônico e digest. `algorithm_identity` deriva identidade de fontes reais e catálogo.
- `storage.executar_ensaio` opera sobre outro formato legado (`dados.circuitos`) e persiste ensaios_calculo. Esse registro não é CalculationRun nem possui vínculo persistido demonstrado com seu UUID. Não utilizar equivalência por nome.
- `domain.installation.CalculationRun` exige output digest quando VALID, mas não comprova que motor foi executado.

## Contrato mínimo aprovado para implementação

1. Repositório carrega revisão externa histórica com digest validado, lê `installation_snapshot` e identifica um run UUID único no agregado.
2. Parâmetros completos AnaliseCircuito devem estar persistidos explicitamente nessa mesma revisão em `dados.calculation_inputs_f10[run_uuid]`. Esta chave é contrato novo de armazenamento W1; ausência implica erro fechado. Não converter arbitrariamente grandezas nem aceitar substituição por parâmetros do cliente.
3. Operação `executar_calculo_f10(project_id, revision, run_id)` executa `analyze_legacy` sobre o snapshot autoritativo e os parâmetros salvos, usando regra do run. Não duplica motor nem concede homologação normativa.
4. Exigir run VALID, circuito/revisão compatíveis e correspondência exata entre input_sha256, output_sha256/result_sha256, algorithm_version e rule_version reais. Divergência é rejeitada; não mutar revisão histórica/run para criar correspondência artificial.
5. Persistir evidência append-only externa ao pacote, vinculando projeto, revisão externa/digest, snapshot/hash, UUID do run, parâmetros e CalculationRecord/result/hash. Chave única projeto/revisão/run e retry idêntico sem duplicação; conflito não sobrescreve evidência.
6. `consultar_calculo_f10(project_id, revision, run_id)` valida integridade e vínculos. Adaptador W1 exige evidência válida e revalida compatibilidade antes de afirmar execução efetiva. Ausência ou adulteração bloqueia geração comprovada.
7. CLI oferece execução explícita antes de generate. Registros legados declarados não recebem atestação retroativa; devem ser preparados em revisão válida com entradas e hashes compatíveis, e executados pelo caminho oficial.

## Critérios de teste

Positivo real: SQLite + snapshot real + analyze_legacy + resultado persistido + adapter/publisher, sem mock do motor. Negativos: ausência de parâmetros/evidência, parâmetros incompatíveis, input/output/algorithm/rule divergentes, circuito/projeto/revisão cruzados, adulteração de record e digest, falha do motor sem sucesso persistido, retry e concorrência. Evidências não dispensam QA independente, CI aplicável e SHA final.

## Áreas de escrita

Persistência: storage.py e test_storage.py. Integração: persisted_source_f10.py e testes correspondentes. Story deve registrar file list e critérios antes das alterações. Registry/publisher existentes são reutilizados. Ondas B–E não são alteradas.
