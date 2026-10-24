# F10 — Registro de execução

**Estado:** IMPLEMENTED / VALIDATING — implementação parcial; F10 não concluída.  
**Branch:** feat/f09-concessionarias-especializadas  
**Plano:** docs/implantacao-sie-2-0/F10/PLANO_IMPLEMENTACAO.md (commit 8810b839af6f3f077d02d6c480d124f8601e2def)  
**Commit de código/testes atual:** 77fb7ff7c04a721d9e26c7b4454828da7f9bf031  
**Estado canônico:** task F10 registrada RUNNING em docs/sie-orchestrator/ORCHESTRATOR_STATE.json; main preservada.

## Implementado

Em restructuring/apps/api/sie_api/representation_f10.py:

- Contrato por project_id, revision_id, calculation_run_id, rule_version e template_version.
- Validação de IDs e vínculos quadro/circuito; entradas incompletas, duplicadas, inconsistentes, negativas ou não finitas bloqueiam a exportação.
- SVG unifilar básico por quadro e circuito, com IDs, fases, disjuntor e condutor; rótulos escapados e metadados de rastreabilidade do artefato.
- Quadro de cargas estruturado a partir do mesmo snapshot e execução; estado marcado como study e conformidade normativa falsa.
- Validador cruzado de contrato, circuitos, quadro, carga, fase, disjuntor e condutor.
- Ledger de comprimentos apenas para trechos informados, contendo circuito, condutor, origem e estado MEASURED/DOCUMENTED/ESTIMATED. Não cria comprimentos ausentes.
- Overlay SVG de planta 2D a partir de posições explícitas em floor_plan, com referência de origem, revisão, unidades, escala declarada e mapeamento dos elementos por ID. Não importa base CAD/BIM, não edita geometria interativamente e não infere percursos.
- CLI local: python -m sie_api.representation_f10 --input <json> --output-dir <pasta-nova>, gerando JSON, SVG, CSV e HTML. Protege contra sobrescrever diretório existente.
- HTML imprimível de estudo com identificação de revisão, diagrama, quadro, trechos e aviso explícito de não conformidade.

Testes acrescentados em restructuring/apps/api/tests/test_representation_f10.py para snapshots, IDs duplicados, revisão divergente, vínculos inválidos, dados numéricos, escape, validador cruzado, proveniência do quantitativo, escala/mapeamento da planta, composição dos formatos e CLI/anti-sobrescrita.

## CI observado

No SHA 77fb7ff7c04a721d9e26c7b4454828da7f9bf031:
- SIE modular API: **1.052 passed**, 1 warning de depreciação Starlette/httpx.
- SIE Orchestrator AIOX Quality Gates: success.
- Browser E2E Chromium: em andamento na última consulta; aguarda conclusão.

Achados corrigidos durante os ensaios: caso inicial de escape que invalidava as referências do próprio grafo; duas falhas de teste introduzidas ao ampliar os cenários (quebras de linha literais no arquivo e mensagem de ID duplicado); validação de IDs duplicados foi efetivamente adicionada ao módulo. Expectativas do motor não foram relaxadas.

## Tasks F10

| Task | Estado | Situação verificável |
|---|---|---|
| 10.01 contrato documento ↔ projeto | PARCIAL | Contrato e metadados embutidos nos formatos suportados; snapshot/hash imutável e persistência documental por revisão ainda não integrados. |
| 10.02 editor/importador de planta | PARCIAL | Overlay JSON/SVG com escala e pontos explicitamente fornecidos; falta importar base autorizada real, editor interativo e impactos da geometria sobre percursos persistidos. |
| 10.03 símbolos/convenções | PARCIAL | Representação básica de quadro/circuitos; biblioteca completa de símbolos/legendas e convenções gráficas pendentes. |
| 10.04 diagrama gerado do grafo | PARCIAL | Unifilar SVG básico; multifilar/prumada e topologia completa ainda não integrados. |
| 10.05 quadros de cargas | PARCIAL | Tabela fiel às entradas do snapshot/run; sem novos cálculos elétricos ou análise de equilíbrio de fases. |
| 10.06 quantitativos | PARCIAL | CSV por trecho com origem/estado, quando fornecidos; integração automática com topologia autoritativa e cálculo de materiais pendente. |
| 10.07 memoriais/relatórios | PARCIAL | HTML imprimível de estudo; memorial de cálculo completo com fórmulas intermediárias e referências ainda pendente. |
| 10.08 exportação/interoperabilidade | PARCIAL | JSON/CSV/SVG/HTML via CLI; PDF e CAD/BIM/round-trip não implementados. |
| 10.09 prévia e revisão visual | PENDENTE | Não há UI F10, zoom/navegação nem teste visual/acessibilidade do produto em desktop/tela pequena. |
| 10.10 validador cruzado | PARCIAL | Consistência entre snapshot/quadro e contrato verificada; proteção/resultados de cálculo normativo entre relatórios ainda não conciliados. |

## QA incorporado

- QA-01 — arquitetura/código/testes: PENDENTE de revisão final integrada; API e AIOX verdes no SHA acima.
- QA-02 — engenharia/normas: PENDENTE. A implementação não recalcula nem certifica instalações; não equivale a assinatura profissional.
- QA-03 — integração/dados/segurança/UX: PENDENTE do E2E final e revisão visual. Escape e bloqueio de exportação inconsistente cobertos por testes; UI visual não existe ainda.

## Decisão de passagem

F10 **não está DONE** e F11 não está liberada. Ainda faltam integração/persistência por revisão, importação/editoração real de planta, conexão do ledger à topologia canônica, diagrama completo, memorial técnico completo, PDF e revisão visual. O CI do Chromium no SHA do código ainda deve ser confirmado. Nenhuma conformidade normativa ou aprovação profissional/concessionária é declarada.

Nenhuma mudança em main, merge, deploy, alteração de banco de produção, homologação profissional ou aprovação normativa/concessionária foi executada.

## Retomada técnica 23/10/2026 — incremento verificado W1 (não encerra F10)

**Referência do código:** `afd73f02e2cd41ee1c2d8615c31616e90d65e4c0`, branch `feat/f09-concessionarias-especializadas`.
- Novo `artifact_store_f10.py`: gera `snapshot.json` com serialização canônica, `manifest.json` com `artifact_id`, revisão, cálculo, versões, `generated_at`, `snapshot_sha256` e hashes individuais das exportações. O pacote é preparado em diretório temporário e publicado por renomeação; lock entre escritores cooperativos impede regravação.
- O comando existente `python -m sie_api.representation_f10 --input fonte.json --output-dir nova_pasta` agora gera também snapshot e manifesto, sem regravar a pasta anterior.
- Verificador independente: `python -m sie_api.artifact_store_f10 verify --directory nova_pasta [--current-input fonte_atual.json]`; rejeita inventário adulterado, hashes incorretos e saídas inconsistentes. Sem origem atual independente, retorna `CURRENTNESS_UNVERIFIED`; com mudança verificada da origem, `STALE` (código de saída 2). A opção de entrada atual ainda **não** realiza consulta automática ao banco.
- O SVG agora agrupa circuitos por painel; ligação a elemento não painel é rejeitada. Plano não aceita unidade fora de `m`, `cm`, `mm`. Chamada CLI com planta deixa de chamar função antes de sua definição.
- Testes adicionados: corrupção de snapshot/arquivos, ausência de arquivo, duplicação, hashes, estabilidade de fingerprint, revisões/cálculos divergentes, topologia/carga modificadas, CLI e isolamento multiquadro.

**CI do código:** [API run 39953127011](https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39953127011) — 1.070 passed e 1 warning; [AIOX 39953126910](https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39953126910) — success; [Chromium 39953127014](https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39953127014) — success. Todos no mesmo SHA de código. A suíte de navegador é regressão global, não cobertura visual própria dos novos recursos F10.

**Decisão:** W1 PARCIAL, AC-10.01 PARCIAL, F10 RUNNING / implementação parcial. Exportação local não substitui persistência integrada por revisão nem autenticação da fonte, e não garante inviolabilidade contra ator com escrita no sistema de arquivos. Planta autorizada/CAD, símbolos completos, memorial de cálculo integral, PDF, reconciliação com registros F06–F08 e UI F10 permanecem pendentes. QA-01, QA-02 e QA-03 formais seguem `PENDING`; nenhuma homologação normativa foi concedida. As 14 gates de conclusão seguem pendentes, sem falsificar aprovação por suíte verde.


## Decisão W1 — candidato de fechamento em 24/10/2026

Código avaliado: `283c4fa66592f3f07daf7e52e24cf2d75895798b`, tree `4ade0d26e90e4c24480e3b5bb3285d8e2b694e12`. Revalidação nesse SHA: `python -m pytest -q` (cwd `restructuring/apps/api`), **1127 passed, 1 warning, 21.53s, exit 0**; lint/typecheck/npm test/build exit 0. QA independente reproduziu 1127 testes no diff e 78 focados no candidato; pareceres `W1_MOTOR_QA_MATRIX.md` e `W1_MOTOR_SECURITY.md`.

G01 e G02 são tecnicamente satisfeitos no recorte local documentado: um circuito/run/cable_run, motor `analyze_legacy`, parâmetros explicitamente persistidos na revisão, banco e filesystem privados e escritores cooperativos. A execução efetiva é registrada e conferida contra revisão/snapshot/inputs/resultado/versões. Fonte indisponível nunca é CURRENT. Não há ACL multiusuário nem garantia contra ator com poder de reescrever banco ou trocar ancestrais filesystem. F06–F08 não são consumidos pelo renderer W1. Não representa homologação normativa.

**Decisão de fechamento:** W1_DONE no recorte suportado somente após sucesso dos três workflows no SHA deste candidato de fechamento. Antes de conferir esses resultados, estado global é VALIDATED_LOCAL_PENDING_CI. Os resultados de SHA anterior abaixo são referências históricas, não aprovação automática do SHA deste documento. F10 permanece RUNNING; F09 permanece DONE; ondas B–E continuam fora do escopo.

Workflows exigidos no candidato: `SIE modular API`, `SIE Orchestrator AIOX Quality Gates`, `SIE Browser E2E (Chromium)`. O CI passa a disparar também por mudança na story e documentação F10. Qualquer falha reabre o gate afetado e impede W1_DONE.


## Candidato integral F10 — decisão atual de software (24/10/2026)

Esta seção supera os estados históricos anteriores somente para o incremento integral atual. Baseline W1 aprovada: `7d8edda79019fed91396d53e99bd897191d69ba3`. Código e documentos ainda serão congelados no candidato; não há SHA final inventado.

**Estado: VALIDATED_LOCAL_PENDING_CI.** QA-01: PASS_LOCAL (1181 testes API, 1 aviso, 22,63s); QA-02: PASS_LOCAL (72 testes focados, PDF multi de sete páginas inspecionado). QA-03: PASS_LOCAL após E2E/print6p/STALE/mobile e fechamento SEC-F10-01; ver QA-03.md. Lint/typecheck/npm test/build passaram no diff; não equivalem a CI.

### Matriz requisito → implementação → evidência

| Critério | Implementação examinada | Teste/parecer |
|---|---|---|
| AC-10.01 | Fonte persistida, runs por circuito, snapshot/hash/registry/recovery | `test_persisted_source_f10_sqlite.py; test_full_f10_integration.py` |
| AC-10.02 | SVG original seguro, autorização, calibração confirmada, IDs e geometria CAS | `test_floorplan_f10.py; test_artifacts_api_f10.py; test_f10_browser.py` |
| AC-10.03 | Catálogo versionado interno, origem/licença e legenda usada | `test_floorplan_f10.py` |
| AC-10.04 | Unifilar derivado do grafo, isolamento multi-quadro, indisponibilidade explícita dos formatos sem dados | `test_representation_f10.py; test_full_f10_integration.py` |
| AC-10.05 | Quadros da mesma revisão/run, entradas e resultados reais com unidades/proveniência | `test_documents_f10.py; test_full_f10_integration.py` |
| AC-10.06 | Equipamentos e ledger de trechos existentes; sem reserva ou medidas implícitas | `test_documents_f10.py; test_full_f10_integration.py` |
| AC-10.07 | Memorial com resultados/fórmulas/intermediários retornados, limitações e referências | `test_documents_f10.py; QA-02.md` |
| AC-10.08 | JSON/CSV/SVG/HTML/PDF reais, hashes e verificação, round-trip suportado | `test_full_f10_integration.py; test_documents_f10.py` |
| AC-10.09 | Editor/preview desktop/mobile, teclado, busca, camadas, undo/redo, CAS e impressão | `test_f10_browser.py; QA-03.md` |
| AC-10.10 | cross_validation.json no manifesto e bloqueio de divergência modelo/projeção/resultados | `test_full_f10_integration.py` |

### Gates locais e regra final

| Gate | Critério | Evidência vinculada | Estado local |
|---|---|---|---|
| G01 — contratos/rastreabilidade | AC-10.01 | testes e pareceres acima | PASS_LOCAL |
| G02 — snapshots/invalidação/recovery | AC-10.01 | testes e pareceres acima | PASS_LOCAL |
| G03 — planta/geometria | AC-10.02 | testes e pareceres acima | PASS_LOCAL |
| G04 — símbolos | AC-10.03 | testes e pareceres acima | PASS_LOCAL |
| G05 — diagramas/quadros | AC-10.04/05 | testes e pareceres acima | PASS_LOCAL |
| G06 — quantitativos | AC-10.06 | testes e pareceres acima | PASS_LOCAL |
| G07 — memorial | AC-10.07 | testes e pareceres acima | PASS_LOCAL |
| G08 — exportações/PDF | AC-10.08 | testes e pareceres acima | PASS_LOCAL |
| G09 — reconciliação | AC-10.10 | testes e pareceres acima | PASS_LOCAL |
| G10 — UI/acessibilidade | AC-10.09 | testes e pareceres acima | PASS_LOCAL |
| G11 — segurança/regressão | QA-03 + suíte/CI | testes e pareceres acima | PASS_LOCAL |
| G12 — QA-01 | QA-01.md | testes e pareceres acima | PASS_LOCAL |
| G13 — QA-02 | QA-02.md | testes e pareceres acima | PASS_LOCAL |
| G14 — QA-03 | QA-03.md | testes e pareceres acima | PASS_LOCAL |

### Limites do produto e condição de DONE

O modo integral cobre múltiplos quadros/circuitos com evidência independente de cada run; cada execução ainda respeita os limites do motor `analyze_legacy` e rejeita topologias/grandezas não suportadas. Fase atribuída ausente é UNSPECIFIED, sem inferir L1 de uma contagem. Multifilar/prumada sem conectividade/elevações suficientes ficam indisponíveis com motivo; CAD/BIM são opcionais. Importação de planta implementa subset SVG seguro, não CAD nem todo SVG arbitrário. Quantitativo geométrico não é medição de obra.

Autorização continua single-owner local por token; não é ACL multiusuário. Banco e filesystem privados são autoridade; hashes não são assinatura contra ator com escrita arbitrária. Homologação normativa/profissional permanece falsa. Nenhuma aprovação humana foi fabricada.

F10 só recebe DONE quando QA-01/02/03 estiverem favoráveis e os três workflows **SIE modular API**, **SIE Orchestrator AIOX Quality Gates** e **SIE Browser E2E (Chromium)** concluírem success no SHA exato que contém este fechamento. Qualquer alteração de código invalida as verificações afetadas. Resultados históricos não aprovam o candidato atual. Essa regra permite a decisão de software após conferir CI sem reescrever o commit validado. Main, produção e F09 permanecem preservados; F11 não é executada neste incremento.
