# F07 — Dimensionamento de condutores e queda de tensão

Data:22/10/2026. **ESTADO: VALIDATING — recorte computacional implementado, fontes vinculadas e QA3/local aprovados; publicação/CI deste incremento em conferência.**
Branch:`feat/f07-condutores-queda`. Base documental remota:a9733551cd721fcecd9df39c8be42a44308c0579; código anterior69b533a9 aprovado com787API/30Chromium. Estado canônico:`docs/sie-orchestrator/ORCHESTRATOR_STATE.json`.

## Resultado concreto da continuação especializada

O bloqueio inicial foi resolvido no código: fonte oficialPrysmianRev9 obtida e conferida visualmente; catálogo finito versionado no servidor; mínimos fase/N/PE,Rca/XL e limites vinculados; seleção conjunta de todas as seções/trechos e caminhos, com agrupamentos identificados e invalidação por fonte/versão. O modoStudy declaratório anterior continua compatível. Histórico do bloqueio, implementação anterior e CI permanecem no Git e nos pareceres iniciais.

O recorte cobre Cu/PVC/Superastic2,5/4/6/10mm²,B1métodos3/5/7,doiscarregadosencostados,60Hz/70°C,ambiente30/40°C,feixes1–3 explicitamente identificados,conexõesFN/FF e instalaçãofixacomum. Demais combinações são bloqueadas; não existe catálogo universal presumido. F01–F06 e seus aceites foram preservados.

## Tasks e evidências

|Task|Estado no recorte|Evidência observável|
|---|---|---|
|07.01|IMPLEMENTED|MATRIZ_LEGADO.md; motores Python/TS inventariados e preservados|
|07.02|IMPLEMENTED|Funções separadas de capacidade/fatores/fase/N/PE/queda e respectivos testes|
|07.03|IMPLEMENTED|conductor_registry_f07.py, JSONversionado, resolverF01 concordante, rejeição de catálogo inválido/incompleto semHTTP500|
|07.04|IMPLEMENTED|Todos os trechos avaliados; política conjunta e feixes mantidos homogêneos sem média de fatores|
|07.05|IMPLEMENTED|AC com Rca/XL/FP por seção; total de cada circuito/alimentador5% e terminal local4%; misturas fora do modelo bloqueadas|
|07.06|IMPLEMENTED|Decimal200, limites de entrada, unidades e fronteira; apresentação não decide aprovação|
|07.07|IMPLEMENTED|Propostas comerciaisfase/N/PE por circuito somente após todos os critérios; falha/esgotamento/inconclusivo explícitos|
|07.08|IMPLEMENTED|Histórico imutável; fonte/versão/entradas invalidam memórias e proteções/documentos; canônicosVALID→STALE|
|07.09|IMPLEMENTED|CLI/API/UI, fonte consultável, memóriaJSON/fórmulas/intermediários/hash, impressão e exportação|
|07.10|IMPLEMENTED local|Confronto tabela24×Rca/XL33, casosFraction independentes, transições/fronteiras/ataques; QA3 e regressão local aprovados|

## Fontes e validação independente

Guia oficialPrysmianRev9,51p,3.172.193bytes,SHA2561729461681fa12bbfe03ea92d26dfb2299c148670d3133046a52f8caf311e4d7. URL,páginas/colunas,recorte,conferentes e limites em VINCULACAO_FONTES.md. PDF não redistribuído. Página33 fornece Rca/XL; página24 fornece coeficientes pré-calculados de comparação, independentes do algoritmo implementado. Concordância com células aceitasF01 foi verificada sem alterá-las.

Caso10A/100m/220V/FP0,8 reproduziu a primeira seção6mm² pelo limite local4%;4mm² retorna4,0745...% e6mm²2,73818...%. Valores racionais esperados foram calculados comFraction e conferidos pelo agente pai. Tolerância0,02V/(A.km) no confronto de tabelas é derivada do arredondamento impresso, sem aumentar limites4%/5%.

## Testes locais realmente observados

- `python -m pytest restructuring/apps/api/tests -q --tb=short`: **864passed**,1avisoStarlette/httpx,14,87s. Inclui **77novoscasos fonte-vinculada** +65F07anteriores (**142F07**).
- `python -m pytest restructuring/e2e -q --tb=short`: **32passed**,75,01s (30anteriores+2novos fonte-vinculada).
- Reexecução após última limpeza visual/contrato explícito: **2E2E fonte-vinculada passed**,30deselected,4,86s.
- `python scripts/f00_golden.py --verify`: **34casos**,fixtureoriginalintacta.
- `npm run lint`, `npm run typecheck`, `npm test` (**18testes**), `npm run build`: PASS.
- CLI`--select` gerou SELECTED_SOURCE_LINKED com propostas reais do catálogo; CLI`--catalog` e exemploStudy anterior operacionais.
- `node --check restructuring/apps/web/condutores.js` e `git diff --check`: PASS.

Instalação local de dependências foi recuperada após mudança de turno, sem alterar lockfiles/pyproject; Playwright1.55.0/Chromium140 usados localmente, dentro do intervalo já existente. Nenhuma expectativa foi relaxada para aprovar: o cenário de fronteira exata foi separado do cenário de catálogo esgotado, mantendo PENDENTE na fronteira e NO_SOLUTION no cenário independente.

## QA3 — Revisões da continuação

|Revisor|Veredito|Evidência e correção|
|---|---|---|
|QA-01|APROVADO recorte computacional|QA-01_VINCULACAO.md; catálogo estruturalmente inválido agoraBLOQUEADO/CATALOG_INVALID eGET422;76testes observados, terminação/vetor/grupos/hashes conferidos|
|QA-02|APROVADO fonte/matemática/engenharia do recorte|QA-02_VINCULACAO.md;11páginas visualmente conferidas,64casos observados, parâmetros/coerênciaF01/referência independente aprovados|
|QA-03|APROVADO integração/segurança/UX/invalidação|QA-03_VINCULACAO.md;76testes+auth401/403/503/conflito409; catálogo antigo após mudarAPI corrigido,NodeVM+32Chromium e2reexecuções conferidos|

Revisões de agentes de software; não são assinaturas profissionais humanas ou homologação de instalação. Os pareceres antigos permanecem para histórico, superados somente no escopo corrigido.

## Gates e próxima decisão

Atendidos localmente no recorte: fontes rastreáveis e casos independentes; estados de todos os critérios obrigatóriosF07; seleção comercial condicionada a todos os trechos/limites; alterações invalidam cálculos/proteções/documentos; trêsQA aprovados; regressão sem falhas.

**Pendente somente publicar e conferir CI deste incremento para encerrar F07.** Sem merge/main/deploy/banco real. `normative_conformity_verified=false`, `authoritative_for_sizing=false`, `professional_approval=false`, `f08_protection_checks_pending=true` são limites de uso/proteção, não um bloqueio genérico para concluir a fase computacionalF07. Passagem seguinte depende do fechamento verificável do CI e estado canônico.
