# F07 — Dimensionamento de condutores e queda de tensão

Data: 22/10/2026. **ESTADO: BLOCKED para encerramento integral; incremento de estudo implementado e verificado.**
Branch: `feat/f07-condutores-queda`. Base observada `d83fff44af4a543e66065c3c8423cc8a339ae060`, encerramento F06. Fonte canônica de estado: `docs/sie-orchestrator/ORCHESTRATOR_STATE.json`.

F01/F05/F06 preservadas. Handoff F06 DONE e logs/CI referenciados no relatório predecessor conferidos por leitura do repositório. A F07 usa Ib canônica, sem promover automaticamente o estudo F06 a dimensionamento definitivo.

## Tasks e evidências

|Task|Estado real|Evidência|
|---|---|---|
|07.01|IMPLEMENTED|MATRIZ_LEGADO.md: Python, otimizador TS, células F01 e limites|
|07.02|IMPLEMENTED no recorte|capacity, temperature_factor, grouping_factor, minimum, neutral, protective_earth, voltage_drop separados e testados|
|07.03|PARCIAL|Resolver F01 com versão, fonte/aceite e condições exatas, sem fallback; catálogo completo faltante|
|07.04|IMPLEMENTED no recorte|Critérios por todos os trechos, sem média de fatores; alternativas não somadas|
|07.05|PARCIAL|Modelo longitudinal AC mono/tri e totais por circuito/alimentador; regimes mistos/retorno desigual bloqueados; faltam referências normativas independentes|
|07.06|IMPLEMENTED|Decimal200, entrada limitada30 dígitos/expoente30, decisões sem arredondamento de apresentação, guard de fronteira explícito|
|07.07|PARCIAL/BLOQUEADO|Matriz de critérios; estado PENDENTE/REPROVADO e motivos. Seleção comercial NÃO implementada, null explícito, depende de catálogo completo|
|07.08|IMPLEMENTED|Fingerprint, histórico imutável, seção/trecho/Ib/método/tabela/levantamento/parâmetros invalidam memória; canônicos VALID/PENDING→STALE|
|07.09|IMPLEMENTED no recorte|CLI, API por trecho/circuito, memória com inputs/fórmula/intermediários/fontes/versão/hash, interface JSON e impressão|
|07.10|PARCIAL|Referências aritméticas independentes Fraction, fronteiras e regressão; fixture sintética versionada. Golden normativo auditado ausente|

Código: `restructuring/apps/api/sie_api/conductor_f07.py`, `conductor_api.py`, `conductor_cli.py`, registro de router em `main.py`; interface `condutores.html/js`, link no painel; exemplos F07 em examples e web; testes API e Chromium. Lista completa e checklist na story `docs/stories/SIE-F07.md`.

## Testes observados antes da publicação

- `python -m pytest restructuring/apps/api/tests -q --tb=short`: **787 passed**, 1 aviso Starlette/httpx, 14,59 s. Inclui **65 F07**.
- `python scripts/f00_golden.py --verify`: **34 casos** do SHA original, fixture intacta.
- `npm run lint`, `npm run typecheck`, `npm test` (**18 testes**), `npm run build`: PASS após instalação das dependências existentes de .aiox-core, sem alteração de lockfile.
- `node --check restructuring/apps/web/condutores.js` e `git diff --check`: PASS.
- CLI executada com fixture sintética; saída PENDENTE e capacidade corrigida22,272 A em cada trecho inicialmente, sem homologação.
- Primeira tentativa Chromium: **29 erros de setup**, pois o executável não pôde ser instalado (downloads Chromium156/Playwright1.64 retornaram arquivo truncado). Nenhum desses erros é descrito como teste funcional aprovado. Recuperação com Playwright1.55 dentro do intervalo já permitido pelo projeto concluída; resultado final registrado abaixo.

## QA3 e correções

|Revisor|Veredito do incremento|Gate integral|
|---|---|---|
|QA-01|APROVADO após correção de precisão;64 testes observados|BLOQUEADO por seleção/catálogo/referências|
|QA-02|APROVADO após corrigir neutro desigual, vínculo Rca/XL e limite de alimentador;64 testes observados|BLOQUEADO por fontes/casos completos|
|QA-03|APROVADO integração/segurança/invalidação;64 testes e ensaio JS de resposta atrasada|Visual comprovado no ensaio consolidado; fase integral BLOQUEADA|

Revisões de agentes de software, não auditorias humanas nem homologação profissional. Achados iniciais e revalidações preservados nos arquivos QA-01/02/03.md.

Defeitos corrigidos: precisão100 com entradas1000 dígitos podia esconder ultrapassagem; neutro desigual aceito em fórmula de retorno igual; impedância não vinculada à seção/material/isolação; limite do alimentador ignorado; snapshot canônico mantinha VALID apesar de flags novas; resposta atrasada podia reabilitar exportação após edição da API. Testes de reprodução implementados, sem relaxar critérios esperados.

## Gates e condição de retomada

Atendidos no recorte: critérios obrigatórios com estados explícitos; análise por trecho; invalidade em cascata testada; memória fiel e fonte limitada F01 reaproveitada.

**Não atendidos:** catálogo completo com mínimos de fase/neutro/PE, Rca/XL por condições e limites aplicáveis; comparação com casos normativos independentes auditados; rotina de seleção comercial multicritério sobre candidatos completos. Ver CONTRATO.md e MATRIZ_LEGADO.md. Os PDFs comentados do acervo e os testes herdados não substituem automaticamente estas provas primárias por parâmetro.

**Próxima ação: retomar esta mesma F07 com vinculação das fontes/casos faltantes e seleção comercial. Passagem à próxima fase não liberada.** Não há reabertura da F01, merge em main, deploy ou acesso a banco real. `normative_conformity_verified=false` e `authoritative_for_sizing=false` permanecem explícitos.

## Recuperação e validação Chromium

Download alternativo da mesma versão156 também falhou. Foi utilizada Playwright1.55.0, já permitida pelo pyproject existente, com Chromium140 headless shell obtido do mirror oficial. Nenhum teste foi pulado e não se alteraram as expectativas. `python -m pytest restructuring/e2e -q --tb=short`: **30 passed**,70,27 s (27 anteriores+3 F07). Os novos testes conferem20 linhas de critérios, memória/exportação JSON, impressão PDF em memória, edição de seção e recálculo, histórico com alteração de comprimento, e descarte de resposta assíncrona após mudar API.

A última alteração do fingerprint inclui também revisão, fonte e aceite do catálogo servidor; novo teste cobre mudança de revisão com valores iguais. Regressão final **787 API /65 F07**,14,59 s. O teste visual não transforma a impressão do estudo em relatório homologado.

## Conferência final de interface

Captura Chromium inspecionada pelo executor: interface escura, botões acessíveis, estado PENDENTE e matriz visíveis, sem erro de JavaScript. Os critérios/estados apresentados foram traduzidos e os nomes de trechos/circuitos substituem UUIDs na leitura principal. Percentuais da interface usam até4 casas somente para apresentação; memória/decisão Decimal mantidas. Impressão testada como emissão PDF em memória, sem alegação de revisão visual de todas as páginas ou de relatório técnico homologado. Após este ajuste exclusivamente visual, os três E2E F07 foram reexecutados; resultado abaixo.

Reexecução final dos E2E F07 após ajuste visual: **3 passed,27 deselected**, sem exclusão da regressão anterior de30casos. Reexecução específica API F07: **65 passed**. Publicação/CI ainda não foram presumidos como concluídos neste checkpoint; serão registrados com SHA e runs observados.


## Publicação e CI conferidos — 22/10/2026

Código publicado em [`69b533a9ea315022eecb247539a551950d81e5ed`](https://github.com/SFPTechnology/Projeto-SIE-2.0/commit/69b533a9ea315022eecb247539a551950d81e5ed), branch `feat/f07-condutores-queda`. Commit local correspondente `c6e8e682dea9b39febf15dde48864e3bb91c5bd9`. Árvore local/remota exatamente igual: `f0a64095e1a7fad807fc97869d6eb1888e786c07`. Foram publicados os 20 arquivos da story; artefatos temporários ficaram excluídos. Nenhum PR, merge ou deploy.

|Workflow no SHA 69b533a9|Run|Conclusão e prova observada|
|---|---|---|
|API/F00|[39720730426](https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39720730426)|completed/success; job 119633320362, logs: 787 passed, 1 warning, 10.21 s;34 golden e fixture unchanged|
|AIOX|[39720730305](https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39720730305)|completed/success; job 119633319779,18 PASS; lint/typecheck/test/build success|
|Chromium|[39720730315](https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39720730315)|completed/success; job 119633319837,logs: 30 passed, 56.05 s; instalação e ensaio real concluídos|

Head SHA, árvore, conclusão dos três runs, etapas e logs conferidos pelo conector GitHub. A última reexecução local dos 3 testes F07 de navegador aprovou em 6,53 s após os rótulos em português; 65 F07 passaram em 1,51 s. O checkpoint de encerramento modifica somente relatório/estado/story; o código permanece exatamente o aprovado pelo CI no SHA 69b533a9. Eventuais workflows disparados pelo checkpoint documental são distintos desses runs e não são usados para atribuir aprovação a outro SHA.

**F07 continua BLOCKED para encerramento integral.** O incremento computacional está publicado e aprovado pelos três QA e pelo CI. Catálogo completo, seleção comercial multicritério e casos normativos independentes continuam necessários. Passagem à fase seguinte não liberada; retomar esta mesma F07. `normative_conformity_verified=false` e `authoritative_for_sizing=false` preservados.
