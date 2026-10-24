# F10 — Matriz verificável de execução (23/10/2026)

A verificação de **subfunções** não equivale a aprovação do requisito completo. Baseline de código: `afd73f02e2cd41ee1c2d8615c31616e90d65e4c0`; 1070 pytest pass + AIOX e Chromium success.

| Requisito | Estado | Dependência | Verificação atual | Próxima prova exigida |
|---|---|---|---|---|
| AC-10.01 Artefatos/revisão | INTEGRATED_LOCAL_ONLY | Modelo/execução persistidos | `test_artifact_store_f10.py`, hashes, CLI | Identidade extraída e confirmada de banco |
| AC-10.02 Planta/escala | IMPLEMENTED_PARTIAL | Base de planta autorizada | Testes de escala, unidade, vínculos | Importação real e geometria reconciliada |
| AC-10.03 Símbolos | IMPLEMENTED_PARTIAL | Catálogo/versionamento | SVG básico existente | Catálogo versionado/legenda/cobertura |
| AC-10.04 Diagramas | IMPLEMENTED_PARTIAL | Grafo autoritativo | Isolamento por quadro e links | Topologia integral e formatos aplicáveis |
| AC-10.05 Quadros | IMPLEMENTED_PARTIAL | Execução persistida | Quadro do snapshot | Resultados efetivos vinculados a run |
| AC-10.06 Quantitativos | IMPLEMENTED_PARTIAL | Percursos medidos válidos | Ledger de trechos com origem | Equipamentos e percursos da topologia |
| AC-10.07 Memorial | IMPLEMENTED_PARTIAL | Trilhas de cálculo | HTML de estudo | Fórmulas, intermediários e pendências reais |
| AC-10.08 Exportação | INTEGRATED_LOCAL_ONLY | PDF e interoperabilidade | JSON/CSV/SVG/HTML + hashes | PDF real e compatibilidade de importação |
| AC-10.09 UI/preview | NOT_STARTED | Renderer integrado | Chromium global (não F10) | Visual, responsividade, acessibilidade |
| AC-10.10 Reconciliação | IMPLEMENTED_PARTIAL | Fontes F06–F08 | Tabela ↔ snapshot | Modelo ↔ cálculos ↔ representações |

## Gates de conclusão

| Gate | Situação | Motivo |
|---|---|---|
| G01 — contratos/rastreabilidade | PENDING | Origem oficial de revisão/execução ainda não vinculada |
| G02 — snapshots/invalidação | PENDING | Verificação condicional existe; invalidação por evento do modelo falta |
| G03 — planta/geometria | PENDING | Importação autorizada/escala consistente não comprovada integralmente |
| G04 — símbolos | PENDING | Biblioteca e legenda completas pendentes |
| G05 — diagramas/quadros | PENDING | Integração com grafo/cálculo completos pendente |
| G06 — quantitativos | PENDING | Itens e percursos autoritativos ainda não reconciliados |
| G07 — memorial | PENDING | Trilhas reais detalhadas faltam |
| G08 — exportações/PDF | PENDING | PDF não implementado |
| G09 — reconciliação cruzada | PENDING | Fontes persistidas ainda não cobertas |
| G10 — UI/acessibilidade | PENDING | UI F10 ainda não existe |
| G11 — segurança/regressão | PENDING | CI passou, mas autorização por projeto/revisão F10 não integrada |
| G12 — QA-01 | PENDING | Nenhuma aprovação formal |
| G13 — QA-02 | PENDING | Nenhuma aprovação formal |
| G14 — QA-03 | PENDING | Nenhuma aprovação formal |

## Cenários com execução observada no CI

| Testes / comando | Resultado | Referência |
|---|---|---|
| `python -m pytest -q` (workdir: restructuring/apps/api) | **1070 passed, 1 warning** | API #39953127011 |
| Snapshot, manifesto, fingerprint, corrupção e não sobrescrita | PASS dentro da suíte API | `tests/test_artifact_store_f10.py` |
| Revisão/cálculo/carga divergentes e fonte atual inválida | PASS dentro da suíte API | `tests/test_artifact_store_f10.py` |
| Circuito atribuído a painel diferente e não painel | PASS dentro da suíte API | `tests/test_representation_f10.py` |
| `npm run lint`, `typecheck`, `test`, `build` | PASS no workflow AIOX | #39953126910 |
| Chromium regressão geral | PASS | #39953127014 |
| UI F10, PDF, importação real, banco integrado, QA formal | NÃO EXECUTADO / PENDING | Sem evidência correspondente |

**Nota de segurança:** hashes sem assinatura verificável demonstram consistência de bytes e reconstrução de artefatos, não identidade/autenticidade frente a atacante com escrita tanto no pacote quanto no manifesto.


## Decisão W1 — candidato de fechamento em 24/10/2026

Código avaliado: `283c4fa66592f3f07daf7e52e24cf2d75895798b`, tree `4ade0d26e90e4c24480e3b5bb3285d8e2b694e12`. Revalidação nesse SHA: `python -m pytest -q` (cwd `restructuring/apps/api`), **1127 passed, 1 warning, 21.53s, exit 0**; lint/typecheck/npm test/build exit 0. QA independente reproduziu 1127 testes no diff e 78 focados no candidato; pareceres `W1_MOTOR_QA_MATRIX.md` e `W1_MOTOR_SECURITY.md`.

G01 e G02 são tecnicamente satisfeitos no recorte local documentado: um circuito/run/cable_run, motor `analyze_legacy`, parâmetros explicitamente persistidos na revisão, banco e filesystem privados e escritores cooperativos. A execução efetiva é registrada e conferida contra revisão/snapshot/inputs/resultado/versões. Fonte indisponível nunca é CURRENT. Não há ACL multiusuário nem garantia contra ator com poder de reescrever banco ou trocar ancestrais filesystem. F06–F08 não são consumidos pelo renderer W1. Não representa homologação normativa.

**Decisão de fechamento:** W1_DONE no recorte suportado somente após sucesso dos três workflows no SHA deste candidato de fechamento. Antes de conferir esses resultados, estado global é VALIDATED_LOCAL_PENDING_CI. Os resultados de SHA anterior abaixo são referências históricas, não aprovação automática do SHA deste documento. F10 permanece RUNNING; F09 permanece DONE; ondas B–E continuam fora do escopo.

Workflows exigidos no candidato: `SIE modular API`, `SIE Orchestrator AIOX Quality Gates`, `SIE Browser E2E (Chromium)`. O CI passa a disparar também por mudança na story e documentação F10. Qualquer falha reabre o gate afetado e impede W1_DONE.

### Matriz W1 específica (não equivale aos gates completos de toda F10)

| Gate W1 | Parecer local | Evidência |
|---|---|---|
| Identidade/origem | PASS | revisão histórica/digest, SQLite/parser reais |
| G01 execução/dependências | PASS no recorte | analyze_legacy real, registro append-only, positivos e 7 negativos de vínculo/hashes/versões |
| Snapshot/consistência | PASS | congelamento e locks cooperativos, teste mutação |
| G02 recuperação | PASS no recorte | crash real antes/depois rename, reopen, retry, histórico e reconciliação |
| Integridade/atualidade | PASS no recorte | hash autoritativo externo ao bundle, cinco estados fail-closed |
| Segurança/CLI | PASS no recorte local | parecer segurança; não expor como ACL multiusuário |
| QA independente | PASS local | W1_MOTOR_QA_MATRIX.md e W1_MOTOR_SECURITY.md |
| CI SHA final | PENDING na emissão | conferir três runs no SHA final; sem inferência do SHA anterior |
| W1 global | VALIDATED_LOCAL_PENDING_CI | torna-se W1_DONE somente com três sucessos no SHA final |


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
