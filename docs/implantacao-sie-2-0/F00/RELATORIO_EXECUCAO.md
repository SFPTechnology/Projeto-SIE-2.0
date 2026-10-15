# F00 — Diagnóstico e preservação do legado

**FASE: F00. ESTADO: VALIDATING.** Data: 2026-10-15. Os pareceres e o registro canônico são conferidos antes da decisão final de passagem.

| Identificação | Registro observado |
|---|---|
| Repositório | https://github.com/SFPTechnology/Projeto-SIE-2.0 |
| Branch da entrega | `audit/f00-baseline-2026-10-15` |
| Branch de origem | `refactor/sie-2-foundation-2026-10-14` |
| COMMIT da baseline | `8d86db26f5e8675eaced4638af14bd84019e15e7` |
| Main observada | `2eee08d126d7bab0a0fe7b7d96b25004ac545447` |
| Fonte de estado | `docs/sie-orchestrator/ORCHESTRATOR_STATE.json` |
| Especificação executada | `F00_EXECUTAR.md` nesta pasta, cópia integral do anexo; SHA256 em `evidencias/baseline.json` |
| Story | `docs/stories/story-SIE-F00-BASELINE-PRESERVACAO.md` |

## Resultado e cobertura

A execução fixou a baseline remota e produziu inventário, contratos, mapa de motores/fontes, matriz de preservação, riscos, testes de caracterização e roteiro de migração reversível. A árvore original tem **12.127 entradas rastreadas**. O inventário lê os contratos do runtime operacional e classifica os demais artefatos históricos por grupos; não declara revisão semântica individual de toda a árvore.

A matriz possui **37 LEGACY-IDs, 19 campos**, com entradas, saídas, persistência, consumidores, destino, teste/lacuna e exceção. Estados observados: **20 confirmados, 5 parciais, 8 não identificados e 4 não verificados**. Preservação: **10 caracterizados sem migração, 11 retidos na baseline e 16 lacunas formais**. Retenção do mesmo arquivo não equivale à implementação futura validada. As lacunas são aceitas como resultado explícito do diagnóstico F00 e continuam impedindo alegações de equivalência ou completude nas fases que as exigem.

O pacote golden contém **34 entradas/saídas executadas do SHA original**, com hashes de 14 módulos, e um teste de metadados. O replay integral e a suíte atual concordam com a captura congelada. Casos que reproduzem defeitos são rotulados como anomalias; resultados herdados não se tornaram referências de engenharia aprovadas.

## Tasks e evidências

| Task | Estado técnico | Entrega/evidência |
|---|---|---|
| 00.01 — Congelar baseline | CONCLUÍDA | `BASELINE_CI.md`; árvore completa, SHA/tree, hash do anexo, versões, 55 hashes operacionais, PR/CI oficial em `evidencias/` |
| 00.02 — Inventariar contratos | CONCLUÍDA | `INVENTARIO_LEGADO.md`; 37 IDs, caminhos/linhas, telas/manuais, imports e fronteiras de integração |
| 00.03 — Mapear motores/fontes | CONCLUÍDA | `MATRIZ_MOTORES_FONTES.md`; grandezas, hipóteses, valores embutidos, casos independentes e fontes não verificadas |
| 00.04 — Produzir golden | CONCLUÍDA | `scripts/f00_golden.py`; fixture `f00_legacy_golden.json`; `test_legacy_golden.py`; replay 34, testes 35 |
| 00.05 — Auditar segurança/dependências | CONCLUÍDA no escopo explicitado | `REGISTRO_RISCOS_INICIAIS.md`; 14 riscos, segredos sem divulgação, licenças, CORS, RLS, SQLite e limites CVE/ambiente remoto |
| 00.06 — Matriz de preservação | CONCLUÍDA | `MATRIZ_PRESERVACAO_FUNCIONAL.csv`; 37 linhas, contratos/testes/destinos/exceções; vínculos golden conferidos |
| 00.07 — Estratégia de migração | CONCLUÍDA | `ESTRATEGIA_MIGRACAO.md`; `PARECER_ARQUITETURA.md` APROVADO para roteiro: 15 manter, 13 encapsular, 9 substituir, nenhum aposentar/refatorar nesta fase |
| 00.08 — Relatório e fechamento | EM VALIDAÇÃO | Este relatório, três QA e sincronização do estado; fechamento condicionado à conferência final |

## Alterações efetivas

- Criados inventário, matriz CSV, mapa de dependências, mapa de motores/fontes, estratégia, parecer de arquitetura, baseline/CI, registro de riscos, QA-01/02/03, relatório e evidências.
- Criados script de captura/replay, fixture congelada e 35 testes de caracterização. Nenhuma expectativa preexistente foi reescrita.
- CI da API passa a obter o histórico completo, verificar o replay do SHA original e reagir à alteração do script golden.
- Corrigidos os comandos do servidor estático no README e manual HTML para `--bind 127.0.0.1`.
- Corrigidas referências documentais que ainda tratavam como futura a caracterização já executada; risco EDP harmonizado como ENG-002.
- Estado/story reconciliados para VALIDATING; transição final aguarda o commit versionado. Código de produto Python/UI e migrations SQL permanecem idênticos à baseline; a comparação Git é parte do gate de regressão.

Todos os arquivos efetivos constam da File List da story e do diff da branch. A publicação versionada é feita em branch isolada e PR em rascunho para a branch de origem; isso não implica merge ou deploy. O commit exato de entrega é o head do PR F00 e o histórico Git associado, consultável sem alterar a baseline original.

## Testes realmente executados

| Grupo | Resultado observado |
|---|---|
| Suíte legada sem novo arquivo | **99 passed**, 1 warning |
| Captura/replay da baseline original | **34 cenários iguais**; fixture inalterada; captura recusa sobrescrita |
| Pacote golden atual | **35 passed**: 34 cenários + metadados |
| Suíte completa da API/domínio/CLI/SQLite/scheduler | **134 passed**, 1 warning; inclui os 35 golden |
| Reprodução em venv nova com versões fixadas | **134 passed**, replay 34, `pip check` exit 0 |
| Navegador Chromium real local | **3 passed**, 8,24 s; API/UI/SQLite temporários, portas verificadas livres |
| Tooling AIOX | **18 testes**; `npm run lint`, `npm run typecheck`, `npm test`, `npm run build` exit 0 |
| JS e workflow | `node --check` exit 0; YAML com histórico completo, step replay e dois gatilhos conferidos |
| Fontes | **6 presentes / 0 ausentes**, hashes; `normative_conformity_verified=false` |

Comandos, stdout/stderr e códigos estão em `evidencias/test-results.json` e seus logs. Os grupos se sobrepõem: 35 golden fazem parte dos 134; replay de 34 cenários não é uma nova contagem de 134 testes. O warning Starlette/httpx não foi ocultado. A CI original do SHA foi consultada diretamente: API 99, Chromium 3 e gates AIOX success, com IDs/URLs em `BASELINE_CI.md`; esses resultados são distintos das execuções locais e de eventual CI da entrega.

## QA3 e correções

| Revisor | Estado do parecer | Achados e tratamento |
|---|---|---|
| QA-01 — Arquitetura/código/testes | APROVADO | 14+55 hashes originais, replay e regressão conferidos; vínculos golden da matriz/inventário corrigidos e revalidados; TS ausente mantido como lacuna |
| QA-02 — Engenharia/fontes | APROVADO | Aritmética independente executada; unidades/fontes/hipóteses conferidas; ENG-001/002 documentados e caracterizados; conteúdo EDP local confrontado sem presumir vigência |
| QA-03 — Integração/dados/segurança/UX | APROVADO | RLS e roundtrip de tabela personalizada registrados; comando estático corrigido; rollback e evidências locais conferidos, com exceções mantidas |

Os pareceres completos têm achados, severidade, arquivo/linha, reprodução, tratamento e limites em `QA-01.md`, `QA-02.md` e `QA-03.md`. São revisões por agentes de IA, sem equivalência a três auditorias humanas independentes ou assinatura de engenheiro. CodeRabbit está indisponível; a configuração permite degradação, registrada como não executado, sem aprovação simulada.

## Riscos e bloqueios que continuam abertos

| Risco/dependência | Evidência | Efeito remanescente |
|---|---|---|
| ENG-001 — arredondamento de Iz antes da decisão | Iz real 19,995 A vira 20,00 A; pipeline pode selecionar In=20 A | Correção elétrica futura deve usar precisão adequada e memória independente; liberação normativa permanece fechada |
| ENG-002 — compatibilidade da modalidade EDP | U/D com carga trifásica podem retornar candidato | Completar regra/aplicabilidade antes de alegar elegibilidade; `liberado_para_padrao_entrada=false` |
| Tabela personalizada no roundtrip CLI/API → UI | F00-DAT-03; a UI recria a tabela fixa ao recalcular | Contrato parcial; teste e correção necessários antes de afirmar equivalência desse fluxo |
| SQL/RLS e cadeia de migrações | F00-SEG-01/02, DAT-01; políticas amplas, dialeto/FKs/seed sem instalação limpa demonstrada | Não executar no banco real; futuro projeto de schema/identidade e ensaio descartável |
| Código legado externo/imports/motores ausentes | Resposta 404 de acesso ao upstream; TS incompleto; 16 lacunas formais | Recuperar código e casos ou formalizar ausência na fase que exigir o módulo; não presumir preservação funcional |
| Fontes normativas, proteção completa e produção | NOR-01/SIE-AUTO-003 BLOCKED; SIE-AUTO-006 HUMAN_REQUIRED | Estados anteriores preservados; hash e testes não resolvem normas, identidade ou autorização de produção |
| Dependências/segredos/licenças | Escopo e exceções no registro de riscos; não há auditoria CVE/histórico integral ou parecer jurídico | Limites explícitos, sem declaração de ausência universal de vulnerabilidades |

Os bloqueios acima não são omitidos nem encerrados pela caracterização. O gate de F00 avalia inventário, evidência e retenção; gates de engenharia, migração real, conformidade e produção dependem das correções/evidências específicas.

## Gates, persistência e retomada

| Gate F00 | Estado nesta revisão |
|---|---|
| Inventário completo do escopo selecionado e limites explícitos | ATENDIDO |
| Matriz de contratos/entrada/saída/destino/testes ou exceção formal | ATENDIDO |
| Golden originado no SHA, regressão e riscos/falhas classificados | ATENDIDO |
| Estratégia reversível aprovada no escopo técnico | ATENDIDO |
| Três QA aplicáveis aprovados | ATENDIDO |
| Documentação/estado versionados e main/produção preservadas | EM VALIDAÇÃO DE FECHAMENTO |

**Próxima ação atual:** registrar o commit versionado, finalizar o JSON canônico/checklist e publicar a branch/PR F00. A passagem só será declarada na revisão final se todos os gates essenciais estiverem atendidos. Nenhuma fase posterior foi executada nesta sessão.
