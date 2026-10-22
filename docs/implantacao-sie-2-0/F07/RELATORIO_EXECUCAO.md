# F07 — Dimensionamento de condutores e queda de tensão

Data: 22/10/2026. **ESTADO: DONE — recorte computacional com fonte vinculada, seleção multicritério, QA3 e CI aprovados.**

Branch: `feat/f07-condutores-queda`. Código final: [`14c64bbcd615ba81d9d0eae60b91b3f24337402b`](https://github.com/SFPTechnology/Projeto-SIE-2.0/commit/14c64bbcd615ba81d9d0eae60b91b3f24337402b). Estado canônico: `docs/sie-orchestrator/ORCHESTRATOR_STATE.json`. Base documental anterior: `a9733551cd721fcecd9df39c8be42a44308c0579`.

## Resultado da continuação especializada

O bloqueio inicial foi resolvido no código: fonte oficial Prysmian Rev9 obtida e conferida visualmente; catálogo finito versionado no servidor; mínimos de fase, neutro e PE, Rca/XL e limites vinculados; seleção conjunta das seções em todos os trechos e caminhos, com agrupamentos identificados e invalidação por fonte/versão. O modo declaratório anterior continua compatível. O histórico do bloqueio e os pareceres anteriores foram preservados no Git.

O recorte cobre cobre/PVC/Superastic, seções de 2,5/4/6/10 mm², método B1 nas instalações 3/5/7, dois condutores carregados encostados, frequência de 60 Hz, condutor a 70 °C, ambiente a 30/40 °C, agrupamentos de 1–3 circuitos explicitamente identificados, conexões FN/FF e instalação fixa comum. Demais combinações são bloqueadas; não existe catálogo universal presumido. F01–F06 e seus aceites foram preservados.

## Tasks e evidências

| Task | Estado no recorte | Evidência observável |
|---|---|---|
| 07.01 | VERIFICADO | MATRIZ_LEGADO.md; motores Python/TS inventariados e preservados |
| 07.02 | VERIFICADO | Funções separadas de capacidade, fatores, fase, neutro, PE e queda, com testes |
| 07.03 | VERIFICADO | conductor_registry_f07.py, JSON versionado, concordância com F01; catálogo inválido/incompleto recusado sem HTTP 500 |
| 07.04 | VERIFICADO | Todos os trechos avaliados; política conjunta mantém os agrupamentos homogêneos sem média de fatores |
| 07.05 | VERIFICADO | Modelo AC com Rca/XL/FP por seção; limite total de 5% e local do terminal de 4%; combinações fora do modelo bloqueadas |
| 07.06 | VERIFICADO | Decimal com 200 dígitos, limites de entrada, unidades e fronteiras; arredondamento de apresentação separado |
| 07.07 | VERIFICADO | Propostas comerciais de fase, neutro e PE somente após verificar todos os critérios; falha, esgotamento e resultado inconclusivo explícitos |
| 07.08 | VERIFICADO | Histórico imutável; fonte, versão e entradas invalidam memórias, proteções e documentos; execuções canônicas VALID/PENDING → STALE |
| 07.09 | VERIFICADO | CLI/API/UI, consulta de fonte, memória JSON, fórmulas, intermediários, hashes, impressão e exportação |
| 07.10 | VERIFICADO | Comparação entre tabelas independentes, casos Fraction, transições/fronteiras, QA3 e regressão local/remota aprovados |

## Fontes e validação independente

Guia oficial Prysmian Rev9: 51 páginas, 3.172.193 bytes, SHA256 `1729461681fa12bbfe03ea92d26dfb2299c148670d3133046a52f8caf311e4d7`. URL, páginas, colunas, recorte, conferentes e limites estão em `VINCULACAO_FONTES.md`. O PDF completo não foi redistribuído. A página 33 fornece Rca/XL; a página 24 fornece coeficientes pré-calculados de comparação, independentes do algoritmo implementado. A concordância com as células aceitas da F01 foi verificada sem alterá-las.

O caso de 10 A, 100 m, 220 V e FP 0,8 selecionou 6 mm² pelo limite local de 4%: 4 mm² produz 4,0745...%, enquanto 6 mm² produz 2,73818...%. Valores racionais esperados foram calculados com Fraction e conferidos pelo agente pai. A tolerância de 0,02 V/(A·km) na comparação das tabelas deriva do arredondamento impresso e não aumenta os limites de 4%/5%.

## Testes locais observados

- `python -m pytest restructuring/apps/api/tests -q --tb=short`: **864 passed**, 1 aviso Starlette/httpx, 14,87 s. Inclui **77 novos casos** com fonte vinculada e 65 F07 anteriores, totalizando **142 testes F07**.
- `python -m pytest restructuring/e2e -q --tb=short`: **32 passed**, 75,01 s, sendo 30 anteriores e 2 novos fluxos de fonte/seleção.
- Após a última alteração visual/contratual: **2 E2E passed**, 30 deselected, 4,86 s.
- `python scripts/f00_golden.py --verify`: **34 casos**, fixture original intacta.
- `npm run lint`, `npm run typecheck`, `npm test` (**18 testes**) e `npm run build`: PASS.
- CLI `--select` gerou `SELECTED_SOURCE_LINKED` com propostas do catálogo; CLI `--catalog` e exemplo declaratório anterior operacionais.
- `node --check restructuring/apps/web/condutores.js` e `git diff --check`: PASS.

Dependências locais recuperadas sem alterar lockfiles ou pyproject. Playwright 1.55.0/Chromium 140 usados localmente, dentro do intervalo existente. Nenhuma expectativa foi relaxada: o caso de fronteira exata continua PENDENTE; o caso independente de catálogo esgotado continua NO_SOLUTION.

## QA3 da vinculação

| Revisor | Veredito | Evidência e correção |
|---|---|---|
| QA-01 | APROVADO | QA-01_VINCULACAO.md; catálogo estruturalmente inválido retorna BLOQUEADO/CATALOG_INVALID ou GET 422; 76 testes observados; terminação, vetor, grupos e hashes conferidos |
| QA-02 | APROVADO no recorte da fonte | QA-02_VINCULACAO.md; 11 páginas conferidas visualmente, 64 casos observados; parâmetros, coerência com F01 e referência independente aprovados |
| QA-03 | APROVADO | QA-03_VINCULACAO.md; 76 testes, autorização 401/403/503 e conflito 409; catálogo antigo após editar API corrigido; ensaio Node VM, 32 Chromium e 2 reexecuções conferidos |

Revisões de agentes de software, sem assinatura profissional humana ou homologação de instalação. Os pareceres antigos permanecem como histórico e são superados somente no escopo corrigido.

## Publicação e CI do código final

Commit local correspondente: `d4a985e8e640f57caa8fe1f0a742d6ad339bfd76`. Árvore local/remota idêntica: `f4ac4d73c369a1f7360484cd2d0b307edea8816b`. Os 20 arquivos da vinculação foram publicados com lease sobre o head esperado `a9733551`; PDFs, arquivos temporários e `run-artifacts/` ficaram excluídos.

| Workflow no SHA 14c64bbc | Run | Resultado observado nos logs |
|---|---|---|
| API/F00 | [39775756669](https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39775756669) | completed/success; job 119814142653: **864 passed**, 1 warning, 17,30 s; **34 golden**, fixture intacta |
| AIOX | [39775757139](https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39775757139) | completed/success; job 119814144577: **18 PASS**, lint/typecheck/test/build aprovados |
| Chromium | [39775756799](https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39775756799) | completed/success; job 119814142845: **32 passed**, 60,41 s; Chromium 156 instalado e ensaio real executado |

Head SHA, árvore, conclusão dos três runs, etapas e logs foram conferidos pelo conector GitHub. A instalação do navegador demorou cerca de 9 minutos; os testes começaram depois e passaram. Não houve cancelamento, repetição artificial ou ocultação de falha. O checkpoint de encerramento altera somente relatório, estado e story; o código permanece exatamente o aprovado no SHA `14c64bbc`. Eventuais runs do checkpoint documental são distintos e não substituem estes resultados.

## Gates, limites e passagem

Todos os gates computacionais da F07 estão atendidos no recorte implementado: fontes rastreáveis e casos independentes; estados explícitos de todos os critérios; seleção condicionada a todos os trechos e limites; invalidação em cascata; QA3 e regressão local/remota aprovados.

`normative_conformity_verified=false`, `authoritative_for_sizing=false`, `professional_approval=false` e `f08_protection_checks_pending=true` permanecem explícitos. O guia do fabricante não equivale à publicação oficial ABNT ou à homologação de uma instalação; os requisitos posteriores de proteção não são presumidos atendidos.

**F07 DONE no recorte computacional com fonte vinculada. Passagem para desenvolvimento da F08 liberada. Próximo arquivo: F08_EXECUTAR.md.** Sem merge em main, deploy, PR ou acesso a banco real.
