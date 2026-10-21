# Story SIE-F02 — Modelo de domínio elétrico e contratos de cálculo

Estado: **Ready for Review / VALIDATING**. Início: 20/10/2026. Branch de trabalho: `feat/f02-dominio-eletrico`, sem merge na principal.

Origem: tasks 02.01–02.09 do kit sequencial F02. Predecessora: F01 encerrada como projeto por aceite expresso do titular, registrado em `docs/implantacao-sie-2-0/F01/ACEITE_TITULAR_ENCERRAMENTO_F01.json`. Esse encerramento permite desenvolvimento; não acrescenta homologação normativa. F00 e os oito valores/seis casos aceitos do lote 01 permanecem preservados.

## Resultado esperado e limites

Representar a instalação como agregado versionado com identidade, unidades, relações e trechos explícitos. Os motores recebem contratos tipados e retornam intermediários, pendências e proveniência; representação gráfica e documentos consomem a mesma revisão. O adaptador legado deve manter a mecânica existente e permitir regressão/retorno à versão anterior. Este incremento não cria aprovação normativa, produção, migração de banco ativo ou histórico persistente novo por mera emissão de um snapshot em memória.

## Critérios de aceite rastreáveis

- [x] **AC-02.01 / task 02.01:** delimitar projeto, cadastro, topologia, cargas, regras, cálculo, representação, documento, usuário e auditoria; regras e decisões de engenharia ficam no servidor.
- [x] **AC-02.02 / task 02.02:** modelar Project, Building, Floor, Room, Supply, Board, LoadPoint, Load, Circuit, CableRun, Segment, Device, CalculationRun e Revision, com identidade/referências/revisão verificadas.
- [x] **AC-02.03 / task 02.03:** contratos rejeitam unidades incompatíveis e não finitos; distinguem FN/FF, P/Q/S, corrente, impedância, comprimento, seção e temperatura sem conversão implícita.
- [x] **AC-02.04 / task 02.04:** validar caminho fonte → quadro → dispositivo → alimentador/circuito → carga; detectar ciclos, órfãos e referências cruzadas incompatíveis; caso de aceite contém dois circuitos por quadro e alimentador entre quadros.
- [x] **AC-02.05 / task 02.05:** condições de instalação pertencem a cada Segment; validar caso com condições distintas sem aplicar um único fator global como regra de todos os trechos.
- [x] **AC-02.06 / task 02.06:** publicar DTOs versionados para entradas/saídas/erros/intermediários/proveniência; frontend não reproduz seleção ou cálculo elétrico.
- [x] **AC-02.07 / task 02.07:** invalidar resultados por alterações de carga/topologia/algoritmo/regra, distinguindo VALID, PENDING, INVALID e STALE com motivos.
- [x] **AC-02.08 / task 02.08:** produzir snapshot imutável por valor e hash verificável da revisão compartilhada por cálculo/representação/documento; declarar ausência de persistência quando for somente memória/resposta HTTP.
- [x] **AC-02.09 / task 02.09:** adaptador de circuito legado resolve referência canônica, exige entrada explícita compatível, preserva diagnósticos e replay congelado F00; leitura antiga não recebe backfill inventado.
- [x] **G-F02-01:** testes de unidade, identidade, revisão, conectividade, múltiplos circuitos/alimentador e condições por segmento concluídos com resultados reais registrados.
- [x] **G-F02-02:** regressões API/CLI, replay F00 e AIOX concluídos no candidato; Chromium quando houver alteração ou fluxo web aplicável.
- [x] **G-F02-03:** revisões QA-01/02/03 aplicáveis concluídas sobre implementação identificada, com achados resolvidos ou limitações explícitas; não reutilizar QA3 F01 como parecer F02.

## Contratos e evidências de trabalho

- `docs/implantacao-sie-2-0/F02/CONTRATOS_MOTORES.md`: responsabilidades e contratos implementados.
- `docs/implantacao-sie-2-0/F02/MAPA_DEPENDENCIAS_CALCULO.md`: dependências e invalidação implementadas.
- Resultados observados:539 testes API,34 replay F00 e AIOX aprovados;90 testes F02 integrados nessa contagem. QA-01/02/03 aprovados no escopo. CI do SHA publicado será conferida antes de encerrar a passagem.

## File list inicial

Criados nesta preparação:

- `docs/stories/story-SIE-F02-DOMINIO-ELETRICO.md`
- `docs/implantacao-sie-2-0/F02/CONTRATOS_MOTORES.md`
- `docs/implantacao-sie-2-0/F02/MAPA_DEPENDENCIAS_CALCULO.md`

Arquivos de runtime, testes e integração serão acrescentados pelo implementador conforme efetivamente alterados. Implementação validada localmente; aguarda CI do SHA publicado.


## File list final e validação

- `restructuring/apps/api/sie_api/domain/installation.py`: modelo puro.
- `restructuring/apps/api/sie_api/installation_{service,contracts,api,storage_api}.py`: aplicação,DTOs,HTTP,persistência aditiva.
- `restructuring/apps/api/sie_api/{cli,main}.py`: composição aditiva.
- `restructuring/apps/api/tests/test_installation{,_integration,_adversarial,_precision,_electrical}_f02.py`: invariantes,API,CLI,precisão,segurança e compatibilidade.
- `restructuring/examples/f02_instalacao_demo.json`: cenário sintético executável.
- `docs/implantacao-sie-2-0/F02/*`: especificação original,diagrama,schema,topologia,OpenAPI,contratos,dependências,relatório e três pareceres.
- `docs/sie-orchestrator/{ORCHESTRATOR_STATE.json,PROJECT_STATE.md,NEXT_ACTION.md,EXECUTION_QUEUE.md}` e esta story.

O domínio representa cenários que o adaptador legado não calcula; a recusa explícita é comportamento validado, preservando o motor F01. Não houve migração/descarte de dados ou alteração de interface legada. A persistência F02 é explícita, local e testada; não confundir a emissão stateless de snapshot com uma gravação automática.
