# Inventário do legado — F00

Baseline auditada: `SFPTechnology/Projeto-SIE-2.0`, commit `8d86db26f5e8675eaced4638af14bd84019e15e7`. Data da inspeção: 15/10/2026. Tarefas 00.02 e 00.06. A classificação refere-se a essa árvore, não a um sistema remoto publicado. As referências sem prefixo nas tabelas de API pertencem a `restructuring/apps/api/sie_api/`; manuais atuais pertencem a `restructuring/docs/`.

**Escopo e limite:** 12.127 arquivos rastreados no SHA foram enumerados por Git. O núcleo operacional identificado e seus contratos foram lidos; diretórios documentais, históricos e AIOX foram agrupados com manifesto reconstituível abaixo. Não se afirma revisão semântica individual de 12.127 arquivos, validação de todo PDF/JSON normativo, inspeção de conteúdo de cada ZIP aninhado, integração de pacotes históricos, execução de banco Supabase ou homologação elétrica.

Estados: **confirmado** = implementação/contrato identificados no fonte e testes nomeados; resultados de execução são os de `BASELINE_CI.md`, não inferidos pela presença de testes. **parcial** = fonte existente com integração/contrato incompleto. **não identificado** = implementação não localizada no escopo; não significa inexistência em outro repositório. **não verificado** = artefato identificado, sem comprovação do ambiente/execução ou conteúdo alegado. Para motores, “confirmado” nunca significa cálculo homologado.

## 1. Sistemas distintos presentes na árvore

| Fronteira | Arquivos da baseline | Papel observado | Cobertura da inspeção |
|---|---:|---|---|
| `restructuring/` | 41 | API Python, SQLite, CLI, UI estática, scheduler e testes atuais | Todos os arquivos enumerados; módulos e contratos operacionais lidos |
| `src/` | 3 | Otimizador, teste e schema TS isolados | Três arquivos inspecionados com leitura dirigida de contratos/testes; tipos e validadores importados ausentes |
| `supabase/` | 5 | DDL/seed de módulos históricos | Cinco migrations lidas; nenhum banco remoto acessado/aplicado |
| `tests/` | 1 | Teste TS da amostra normativa com Supabase | Lido; requer runtime/credenciais não fornecidos pelo package raiz |
| `Arquivos_Diversos/` | 133 | Normas, extrações, planos e 3 pacotes unifilar | Manifesto integral de nomes por grupos; leitura dirigida das referências/um pacote representativo |
| `.aiox-core/`, `.aiox/` | 2.271 + 6.076 | Framework e registros de automação do desenvolvimento | Constitution, personas e pontos de entrada/checks dirigidos; restantes catalogados |
| `docs/` | 3.164 | Especificações, stories, pesquisa e estado operacional | Estado canônico, plano e documentos usados nos contratos lidos; demais grupos catalogados |
| `outputs/` | 15 | Protótipo e design system | Presença/estrutura e fronteira de protótipo; não é a UI servida por restructuring |
| Demais arquivos | 418 | Configuração IDE/CI, scripts e documentos raiz | Catálogo reconstituível; pontos CI/quality lidos |

A referência `.gitmodules` aponta para o repositório de origem `SFPTechnology/sistema-de-instala-es-el-tricas-sie`. A execução principal observou resposta 404 à consulta de repositório e `not found` à consulta de branch; isso prova apenas indisponibilidade de acesso nessa sessão, sem concluir se o repositório é privado, removido ou inexistente. A falta do fonte de origem continua uma lacuna formal; caminhos citados em documentos não foram tratados como código disponível.

O plano histórico `Arquivos_Diversos/PLANO-REESTRUTURACAO-PYTHON-SIE.md:5-7,32-60` descreve outro sistema de origem, com árvore TypeScript mais ampla. Os caminhos `src/domain/calculo/geometria.ts`, `motor-demanda.ts`, `corrente-projeto.ts`, `src/domain/modelo/tipos.ts` e `src/domain/calculo/validadores.ts` não existem na baseline observada. Alegações de maturidade/conclusão nesse plano não são transferidas para o inventário atual. `docs/sie-orchestrator/PROJECT_STATE.md:18-22` já distingue os módulos ainda pendentes.

## 2. Contratos operacionais de engenharia

| LEGACY-ID | Função/entrada → saída | Persistência/consumidores/tela/manual | Referência e estado |
|---|---|---|---|
| 001 | `CircuitoEletrico`: id, corrente A, percurso m, tensão V → dataclass validada | Sem armazenamento; usada por teste, não pelo schema HTTP | `domain/models.py:4-19`; confirmado, integração separada |
| 002 | Projeto/circuitos → contagem e validação estrutural; 422 para repetição/campos extras | HTTP `POST /api/v1/projetos/validar`; sem tela própria; README | `main.py:20-31,72-78`; confirmado |
| 003 | Ib A + fator + pares (mm²,A) → menor seção/capacidade corrigida | `application.py` → API → card Condutor; manual §§4–5 | `domain/engines.py:80-104`; confirmado com ENG-001 |
| 004 | Ib A + Iz A + catálogo → In mínimo admissível | Catálogo fixo `application.py:6`; card Disjuntor; manual §5 | `domain/engines.py:54-69`; confirmado com ENG-001 |
| 005 | I A, L m, R Ω/km, V → ΔV V/%, fórmula | Análise integrada; UI; manual §§4–5 | `domain/engines.py:34-43`; confirmado, resistivo monofásico |
| 006 | I A, L m, R Ω/km, V de linha → ΔV V/% | Só função/testes; sem API/UI; README:60 | `domain/engines.py:107-128`; parcial para integração |
| 007 | Evidência/flags → BLOQUEADO/PENDENTE; nunca APROVADO | Aplicação/API/UI; não salva decisão de conformidade | `domain/gates.py:16-32`; confirmado |
| 008 | Payload completo → condutor, disjuntor, queda, rastro e gate | `POST /api/v1/circuitos/analisar`; não salva sozinho; formulário manual | `application.py:9-26; main.py:48-56,81-86`; confirmado com ENG-001 |
| 009 | U/D/T + demanda A + carga kW + carga trifásica → categoria candidata/alertas | `POST /api/v1/edp/enquadrar`; sem tela; manual §8 | `domain/edp.py:29-65; main.py:89-99`; confirmado com ENG-002 |

**Fontes e valores:** o cliente fornece tabela/fator/R à API. A UI fixa quatro pares de seção/ampacidade em `apps/web/app.js:18`; a entrada de fonte do formulário não prova proveniência desses pares. O catálogo de disjuntores é fixo; o EDP possui metadado legado `VERIFICADO`, mas a regra de seleção por corrente é `DOCUMENTADO_SEM_FONTE_PRIMARIA`. Conferência de norma, limites e memória de cálculo são tratadas na matriz de motores/fontes e QA-02. Esta inspeção conserva `liberado_para_uso_normativo=false` e `liberado_para_padrao_entrada=false`.

**Anomalias que a caracterização deve conservar sem aprovar:** ENG-001: seleção do disjuntor recebe Iz arredondada do seletor de condutor (`application.py:15-17`), podendo admitir In=20 para Iz real=19,995 A no caso Ib=19,99 A, Izbase=20 A, fator=0,99975. ENG-002: modalidade U com carga trifásica declarada não recebe o bloqueio inverso de modalidade T (`domain/edp.py:55-65`). Manter o comportamento em teste não torna esses resultados adequados para uso normativo. Correção funcional futura exige aprovação técnica e uma expectativa nova explicitamente versionada.

## 3. Persistência, CLI e contratos de dados

| LEGACY-ID | Contrato | Dados/consumidores | Erros e referências |
|---|---|---|---|
| 010 | Salvar UUID/nome/objeto JSON/revisão esperada → nova revisão | SQLite `projetos(id,nome,dados_json,revisao,atualizado_em)` e `eventos_auditoria(id,projeto_id,acao,revisao,criado_em)`; CLI e API | 1 MiB; JSON finito; BEGIN IMMEDIATE; conflito sem sobrescrita. `storage.py:17-83`; confirmado |
| 011 | Carregar UUID → projeto completo ou None | Leitura do mesmo SQLite; CLI/API/UI | `storage.py:85-94`; API devolve 404; confirmado |
| 012 | Histórico UUID → ações/revisões/timestamps | Eventos apenas; **não há snapshots dos dados de cada revisão** | `storage.py:96-103`; confirmado com limite EX-F00-004 |
| 013 | `python -m sie_api.cli --database ... salvar/carregar/historico` | Lê JSON UTF-8/BOM, salva ou consulta SQLite diretamente; sem servidor/token | Exit 0/2/3/4; `cli.py:26-85`; confirmado; `PERSISTENCIA-LOCAL.md:7-46` |
| 014 | PUT `/api/v1/local/projetos`, GET `/{id}`, GET `/{id}/historico` | Mesmo repositório; opt-in por SIE_LOCAL_DB_PATH e SIE_LOCAL_API_TOKEN>=24; Bearer | 503/401/409/422/404; `storage_api.py:12-60`; confirmado; guia:50-108 |
| 015 | GET `/api/v1/health`; CORS de localhost/127.0.0.1:5173 | Health consumido pelo navegador; API sem identidade de produção | `main.py:10-17,67-69`; confirmado |

SQLite local e migrations Supabase são fronteiras independentes. Não há sincronização no runtime (`storage.py` usa `sqlite3`; `pyproject.toml:10-14` não declara cliente Supabase). A trilha de eventos permite rastrear ações e detectar conflitos, mas não recuperar automaticamente o conteúdo de uma revisão antiga. Banco real existente do usuário não foi lido; testes usam bases temporárias.

## 4. Telas e comportamento de interface

`restructuring/apps/web/index.html:15-83` define uma página com âncoras, não uma SPA React. `app.js:1-23` utiliza fetch para a API; CSS é local. LEGACY-016 cobre Visão geral, Nova análise, indicadores estáticos, formulário, resultado, rastreabilidade e guia. Manual atual: `restructuring/docs/MANUAL-OPERACIONAL.md:11-52` e versão HTML.

LEGACY-017 cobre o painel Projetos locais (`index.html:59-74; app.js:26-118`). O token permanece no input e não é gravado pelo script no localStorage/sessionStorage. A análise anterior é guardada em memória até o salvamento como `dados.analise`. Reabrir preenche parâmetros e evidência, zera `ultimaAnalise` e exige novo cálculo; não restaura a tabela salva como opção editável, pois o próximo submit recria a tabela fixa. A URL da persistência é fixa em `127.0.0.1:8000`, enquanto saúde/análise leem `sie.apiBase` do localStorage. Esses limites são EX-F00-008, sem modificação da UI nesta fase.

Testes identificados: `test_web_contract.py` verifica IDs, ausência de autoaprovação e não persistência do token. `restructuring/e2e/test_browser_flow.py:87-149` caracteriza calcular/salvar/reabrir/recalcular, token/revisão incorretos e escape de entrada. Sua presença não comprova execução atual; consultar `BASELINE_CI.md`. Não há tela EDP, histórico completo, editor geométrico, gerenciamento multiusuário, catálogo normativo editável, unifilar integrado ou exportação técnica nesta UI.

## 5. Automação, inventário normativo e tooling

| LEGACY-ID | Responsabilidade real | Entrada/saída e armazenamento | Referência |
|---|---|---|---|
| 018 | Escalonador SIE valida DAG, requisitos, dez estados e evidências não vazias; ordena READY | JSON schema1 → fila/transição/histórico; save atômico por replace e revisão otimista; sem lock interprocesso | `scheduler.py:14-29,49-126,129-220`; confirmado |
| 019 | CLI inspect/queue/promote/transition | `--state`/SIE_ORCHESTRATOR_STATE → JSON stdout; mesmo arquivo canônico; exit2 falha | `scheduler_cli.py:15-69`; confirmado |
| 020 | Inventariar seis fontes por SHA256 | SOURCE_SPECS + root → presença/hash/bytes; output JSON opcional; nunca aprova conteúdo | `normative_inventory.py:14-84`; confirmado |
| 031 | AIOX é ferramenta de desenvolvimento separada do produto | Node/workflows/manifests/agents → execução/checks do framework; estados próprios em `.aiox/` | `package.json:6-10; scripts/validate-sdc-auto-1.js:10-18,114-141`; confirmado no escopo de tooling |

A fonte canônica já existente é `docs/sie-orchestrator/ORCHESTRATOR_STATE.json`. Markdown de estado/histórico serve de evidência derivada; nenhum documento cria agentes em background. O scheduler verifica estrutura e referências de evidência, não sua veracidade externa. O `typecheck` raiz é sintaxe/exports JavaScript do AIOX, sem execução `tsc` do `src/` legado. Os scripts `sync:ide`, `validate:structure` e `validate:agents` citados em `AGENTS.md` não existem no `package.json` raiz desta baseline; não foram presumidos disponíveis. Framework AIOX não é motor de carga/engenharia.

## 6. TypeScript isolado, Supabase e pacote gráfico histórico

| IDs | Arquivos/contrato observado | Estado e limite |
|---|---|---|
| 021 | `src/domain/calculo/otimizador.ts:6-20,49-104,138-223`: autoOtimizar/diagnosticarFalhas e tabelas/fatores simplificados | Parcial: imports de tipos/validadores ausentes; teste TS existe; equivalência com Python não comprovada |
| 022 | `src/api/schemas/otimizar.schema.ts:1-129`: schemas Zod request/response/erro | Parcial: nenhuma rota ou consumidor integrado; Zod/runner não declarados no package raiz |
| 023 | `20260712_001_create_normas_tables.sql` + `002_seed_tabela_36_amostra.sql` | Não verificado: DDL/seed existente; banco aplicado não observado; COMMENT inline e constraint expressão devem ser testados; rótulos CONFIRMADO não homologam dados |
| 024 | `20260716_001_create_dependencia_retornos_downstream.sql:4-43` | Não verificado: FK public.dependencias ausente do conjunto; FOR ALL amplo anon/authenticated; sem consumidor Python |
| 025 | `20260717_001_create_dimensionamento_condutores_overrides.sql:6-29` | Não verificado: FK public.projetos e repositório citado ausentes; políticas amplas; sem integração SQLite |
| 026 | `20260730_001_create_queda_tensao_config.sql:6-32` | Não verificado: config JSONB por projeto; mesma lacuna de FK/políticas/consumidor |
| 027 | `Arquivos_Diversos/Unifilar/Unifilar/files (7)/sie-camada-visualizacao-fase0-1b/` | Parcial: contratos/adaptador/router e React SVG presentes; injeção de loader exigida; não incluído em main.py |
| 028 | Mesmo pacote: `backend/export_dxf.py:16-19,99` e README:67-94 | Parcial: DXF com ezdxf não declarado no pyproject atual; não há rota/exportador atual integrado; CAD real não verificado |

O prefixo completo das migrations é `supabase/migrations/`. O teste TS `tests/unit/domain/repositorio/tabela_36_amostra.test.ts:9-15,51-99` cria cliente Supabase com variáveis externas; não é um teste offline do Python e não foi executado implicitamente por npm test. As três distribuições unifilar files (5)/(6)/(7) são preservadas como versões distintas. Foi lido o pacote files (7) como amostra dirigida de contrato, não certificadas igualdade ou integração dos três.

## 7. Comportamentos históricos sem implementação integrada identificada

| LEGACY-ID | Comportamento | Documento que o descreve | Lacuna formal |
|---|---|---|---|
| 029 | Carga instalada/demanda por grupo | Plano Python:149-150 | LACUNA-FUNC-001: motor-demanda/fatores ausentes; EDP recebe demanda pronta |
| 030 | Projeto gráfico completo, memoriais/PDF/quantitativos | Manual atual:82-84; plano:177-186 | LACUNA-FUNC-002: pacote unifilar não equivale a pipeline de entrega |
| 032 | Geometria e iluminação mínima | Plano:145-146 | LACUNA-FUNC-003: sem módulo/saída executável identificada |
| 033 | TUG/TUE por dependência | Plano:147 | LACUNA-FUNC-004: sem módulo/saída executável identificada |
| 034 | IB e resolução de ligação | Plano:148 | LACUNA-FUNC-005: corrente fornecida à API não prova esse cálculo |
| 035 | Divisão de circuitos | Plano:118,124 | LACUNA-FUNC-006: contrato/adaptador 1:1 avulso não demonstra divisão normativa |
| 036 | Balanceamento de fases | Plano:151 | LACUNA-FUNC-007: sem motor operacional identificado |
| 037 | Curto, seletividade, DR, neutro/PE e seccionamento completos | Plano:152-154; PROJECT_STATE:18-22 | LACUNA-FUNC-008: Ib≤In≤Iz simples não cobre proteções completas |

Para esses IDs, o destino funcional permanece **não definido** até recuperar o código original ou aprovar um contrato novo. A matriz nunca marca “preservado” por existir plano, arquivo SQL ou teste não executável. A exceção formal retém o artefato e explicita a falta, não dispensa a futura validação.

## 8. Matriz de preservação e evidências

`MATRIZ_PRESERVACAO_FUNCIONAL.csv` tem 37 IDs estáveis, entradas/unidades, saídas, persistência, consumidores, tela/manual, destino, teste/lacuna e exceção por comportamento. “Mesma implementação mantida na baseline” significa que o código operacional não foi migrado por F00; não afirma comparação entre versões. Para `parcial`, `não identificado` e `não verificado`, a equivalência é **NÃO COMPROVADA** e a retenção documental tem status `LACUNA_FORMAL`. Falhas conhecidas ENG-001/002 continuam identificadas.

Testes existentes são nomeados na matriz. O vínculo golden foi conferido em `restructuring/apps/api/tests/fixtures/f00_legacy_golden.json`: `baseline_sha` coincide com o SHA acima, `source_sha256` fixa o fonte e os 34 casos contêm entradas/saídas capturadas. `scripts/f00_golden.py --verify` reproduziu os 34 sem alterar a fixture (`evidencias/clean-golden-replay.log:4`); `test_legacy_golden.py` executou 35 testes (`evidencias/golden-tests.log:5`). A regressão completa registrou 134 passed e 1 warning (`evidencias/clean-api-regression.log:12`); o browser registrou 3 passed (`evidencias/browser-e2e.log:8`). São logs produzidos pela execução principal e lidos nesta revisão documental; não nova execução por este inventário.

| LEGACY-ID | Golden IDs conferidos |
|---|---|
| 003 | CONDUTOR, CONDUTOR-LIMIAR, CONDUTOR-DUPLICADO, ANALISE-IZ-ARREDONDADO |
| 004 | DISJUNTOR, DISJUNTOR-SEM-CANDIDATO, ANALISE-IZ-ARREDONDADO |
| 005 | QT-MONO, QT-MONO-ZERO, QT-MONO-ROUND, QT-MONO-INVALID |
| 006 | QT-TRI, QT-TRI-ZERO |
| 007 | GATE-SEM-FONTE, GATE-CLIENTE, GATE-VAZIO |
| 008 | ANALISE, ANALISE-IZ-ARREDONDADO |
| 009 | EDP-U-70; EDP-D-63/100/150/200/300/350; EDP-T-63/100/150/200/300/350; EDP-T-SEM-TRIFASICA; EDP-75KW; EDP-SEM-CATEGORIA; EDP-U-CARGA-TRIFASICA |
| 010–012 | STORAGE-REVISOES |

O teste `test_current_behavior_matches_frozen_legacy` usa parametrização por ID da fixture (`test_legacy_golden.py:29-31`); os casos ENG-001/002 têm `known_anomaly` preenchido com a descrição da anomalia, conferidos em `test_fixture_records_original_revision_and_scope:19-26`. A coluna `golden_cases` da matriz contém cada ID literal. O corpus caracteriza comportamento; correção das fórmulas é verificação distinta em test_engines/QA-02. Resultado de teste e deltas de implementação são registrados em `BASELINE_CI.md`; QA é registrado em pareceres separados. Nenhuma linha desta matriz concede aprovação normativa.

## 9. Manifesto de cobertura reconstituível

O manifesto físico autoritativo é a árvore Git do SHA fixado; sua enumeração integral foi persistida em `evidencias/arvore-baseline.txt`, com metadados em `evidencias/baseline.json`. Reprodução sem alterar o repositório:

```bash
git ls-tree -r --name-only 8d86db26f5e8675eaced4638af14bd84019e15e7
git ls-tree -r -z 8d86db26f5e8675eaced4638af14bd84019e15e7 Arquivos_Diversos docs .aiox-core .aiox
```

A enumeração usou `-z` para nomes UTF-8 com espaços; contagem textual com nomes escapados não deve ser confundida com revisão de conteúdo. Cada grupo abaixo é retido integralmente; o hash identifica a árvore inteira e seus blobs, sem sugerir leitura semântica de cada arquivo.

| Grupo histórico/documental | Quantidade | Git tree da baseline | Inspeção realizada |
|---|---:|---|---|
| Arquivos_Diversos/Correção_1 | 3 | `4482fe516625747c44472b2d424d7a962ebb5bfb` | Catálogo de planos, sem reexecução |
| Arquivos_Diversos/Correção_2 | 3 | `5288fa9e1c9b3964bf2b2fc3118506c86feebda7` | Catálogo de planos, sem reexecução |
| Arquivos_Diversos/NBR_5410_comentada | 50 | `c3a7f00958c28f6c88bd773f5fcf9fa8df091517` | PDFs/extratos/manifestos catalogados; sem validação integral da norma/OCR |
| Arquivos_Diversos/NBR_5410_original | 2 | `9461911a140254913e211b94cebdd6bc955580e1` | Transcrição/extrato identificados; sem homologação |
| Arquivos_Diversos/Norma_EDP | 5 | `adf40c612bff9197dfac969410748ba8fb4debab` | PDF, tabelas e extratos identificados; conteúdo sob QA-02 |
| Arquivos_Diversos/Unifilar | 52 | `f9e79eb446810e93e83585422c77e95abebc1ca2` | ZIPs e três expansões catalogados; leitura dirigida de files (7) |
| Arquivos_Diversos (diretos) | 18 | árvore-pai `c61c929540ac01487c375607896ab0c2cb1980a5` | Plano Python/referências usados; restantes retidos por manifesto |
| docs/t5-research | 2.904 | `cb1d859f94edda5c1b888e39d7ba854b578531e2` | Catálogo de arquivos; sem auditoria individual de bibliotecas/projetos de terceiros |
| docs demais | 260 | árvore-pai `ef41286c8cd8aa5e747dd58af77bb2d061a92f99` | Leitura dirigida de estado, stories, planos/contratos; restantes catalogados |
| outputs | 15 | `c10e7f44c96278e8efc4a119fed53ca3732d3315` | Prototipagem/design; não conta como integração funcional |
| .aiox-core | 2.271 | `9a2c45edcec36bb428572a5a1cca7135df7f175d` | Tooling separado; pontos de entrada lidos |
| .aiox | 6.076 | `674f1d8ba4bd21ca2af62902e23b5202c65b31c2` | Registros, squads e handoffs; catálogo de paths, não auditoria completa |

Os três ZIPs de `Arquivos_Diversos/Unifilar/` tiveram nomes de membros externos enumerados via `zipfile` e hashes calculados; ZIPs internos **não** foram extraídos/atestados:

| ZIP | Membros externos (arquivos) | SHA256 |
|---|---:|---|
| files (5).zip | 3 | `69a9df4e1e917e12f44e390b14ce92445fb5f86e041e9d9405e6aa8608c80872` |
| files (6).zip | 3 | `71d639b592213fea7d1bc064e99e5d7dfdf4660776fecf5acf6c643a4ab257d2` |
| files (7).zip | 2 | `c3a738b58ef42189c82cf295af5877df30fdba5e4e65f6b1db8eeee2553aafb1` |

Expansões retidas: files (5) tree `7f46d4ab0d96e702a26f45ec4d24cb375120890a`; files (6) `920b14e253e172755450a395699da0ee4d9ecacb`; files (7) `3ca8eb96dc82d3ea1cbef498b22cc4d29715c423`. Igualdade com ZIP aninhado ou entre expansões não foi demonstrada.

### Arquivos operacionais, testes e manuais da fronteira atual

Lista integral de `restructuring/` no SHA de referência, incluindo inicializadores vazios e workflow aninhado (um arquivo YAML dentro de restructuring não é workflow GitHub ativo da raiz):

- `restructuring/.github/workflows/api-quality.yml`
- `restructuring/.gitignore`
- `restructuring/README.md`
- `restructuring/apps/api/pyproject.toml`
- `restructuring/apps/api/sie_api/__init__.py`
- `restructuring/apps/api/sie_api/application.py`
- `restructuring/apps/api/sie_api/cli.py`
- `restructuring/apps/api/sie_api/domain/__init__.py`
- `restructuring/apps/api/sie_api/domain/edp.py`
- `restructuring/apps/api/sie_api/domain/engines.py`
- `restructuring/apps/api/sie_api/domain/gates.py`
- `restructuring/apps/api/sie_api/domain/models.py`
- `restructuring/apps/api/sie_api/main.py`
- `restructuring/apps/api/sie_api/normative_inventory.py`
- `restructuring/apps/api/sie_api/scheduler.py`
- `restructuring/apps/api/sie_api/scheduler_cli.py`
- `restructuring/apps/api/sie_api/storage.py`
- `restructuring/apps/api/sie_api/storage_api.py`
- `restructuring/apps/api/tests/test_api.py`
- `restructuring/apps/api/tests/test_cli.py`
- `restructuring/apps/api/tests/test_domain.py`
- `restructuring/apps/api/tests/test_edp.py`
- `restructuring/apps/api/tests/test_engines.py`
- `restructuring/apps/api/tests/test_normative_inventory.py`
- `restructuring/apps/api/tests/test_scheduler.py`
- `restructuring/apps/api/tests/test_storage.py`
- `restructuring/apps/api/tests/test_storage_api.py`
- `restructuring/apps/api/tests/test_web_contract.py`
- `restructuring/apps/web/app.js`
- `restructuring/apps/web/index.html`
- `restructuring/apps/web/styles.css`
- `restructuring/docs/ARQUITETURA-INTEGRADA.md`
- `restructuring/docs/AUDITORIA-INICIAL.md`
- `restructuring/docs/CONTRATOS-ENGENHARIA.md`
- `restructuring/docs/MANUAL-OPERACIONAL.html`
- `restructuring/docs/MANUAL-OPERACIONAL.md`
- `restructuring/docs/MARCO-002-RELATORIO.md`
- `restructuring/docs/PERSISTENCIA-LOCAL.md`
- `restructuring/docs/QA-FINAL.md`
- `restructuring/docs/TESTE-E2E-NAVEGADOR.md`
- `restructuring/e2e/test_browser_flow.py`

A lista inclui os dez módulos de teste Python, E2E separado e documentação Markdown/HTML. A matriz associa os contratos aos testes específicos, em vez de inferir cobertura pela contagem de arquivos. Workflows ativos: `.github/workflows/sie-restructuring-api.yml`, `sie-e2e-browser.yml`, `sie-orchestrator-quality.yml`. O workflow `restructuring/.github/workflows/api-quality.yml` é histórico/não descoberto como workflow ativo pelo GitHub nessa posição.

### Demais fronteiras do manifesto

| Fronteira | Arquivos | Tratamento |
|---|---:|---|
| `.ai` | 2 | Configuração/documentação/tooling retidos; leitura dirigida só dos pontos de execução usados; restante catalogado |
| `.antigravity` | 12 | Configuração/documentação/tooling retidos; leitura dirigida só dos pontos de execução usados; restante catalogado |
| `.claude` | 295 | Configuração/documentação/tooling retidos; leitura dirigida só dos pontos de execução usados; restante catalogado |
| `.codex` | 24 | Configuração/documentação/tooling retidos; leitura dirigida só dos pontos de execução usados; restante catalogado |
| `.cursor` | 12 | Configuração/documentação/tooling retidos; leitura dirigida só dos pontos de execução usados; restante catalogado |
| `.gemini` | 25 | Configuração/documentação/tooling retidos; leitura dirigida só dos pontos de execução usados; restante catalogado |
| `.github` | 15 | Configuração/documentação/tooling retidos; leitura dirigida só dos pontos de execução usados; restante catalogado |
| `.kimi` | 12 | Configuração/documentação/tooling retidos; leitura dirigida só dos pontos de execução usados; restante catalogado |
| `[arquivos-raiz]` | 18 | Configuração/documentação/tooling retidos; leitura dirigida só dos pontos de execução usados; restante catalogado |
| `scripts` | 3 | Configuração/documentação/tooling retidos; leitura dirigida só dos pontos de execução usados; restante catalogado |

Total do manifesto: **12.127**. Nenhum arquivo da baseline foi classificado para exclusão nesta F00.
