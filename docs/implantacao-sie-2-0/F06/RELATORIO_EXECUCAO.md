# F06 — Demanda e alimentação elétrica

Data: 21/10/2026. **ESTADO: VALIDATING — vinculação implementada, testes locais aprovados; CI do incremento em preparação.**
Branch: `feat/f06-demanda-alimentacao`. Incremento autorizado pelo usuário: **“Realize a vinculação.”** Base remota: `98b03d0ec7c28c7563fc79b19cc99a9f308d8dff`. Fonte canônica: `docs/sie-orchestrator/ORCHESTRATOR_STATE.json`.

## Resultado da vinculação

O bloqueio anterior por ausência de catálogo confiável foi resolvido no código. **22 regras EDP V09** com edição, hashes, página/tabela, critérios, faixas, coeficientes e exceções são resolvidas pelo servidor. Detalhes, provas da fonte e instruções em [VINCULACAO_FONTES.md](VINCULACAO_FONTES.md).

Fonte oficial consultada/download realizado em 21/10/2026. PDF oficial e PDF do repositório têm hashes binários diferentes; texto integral extraído idêntico. Foram conferidas visualmente as tabelas das páginas 34–37. Não houve atribuição de assinatura humana ou aprovação da distribuidora.

|Task|Implementação e evidência atual|
|---|---|
|06.01|Classificação explícita e independente do rule_id; tipo de equipamento/quantidade/condições declarados.|
|06.02|P/Q/S por ambiente, circuito, quadro, fonte e empreendimento; ponte F04/F02 por UUID e quantidade única.|
|06.03|Catálogo do servidor, fonte oficial, limites superiores inclusivos, base ativa em W para T005/006, quantidades para T007–010/012/015, máximos e partidas para T013/014; testes independentes das pp42–44.|
|06.04|Regra EDP de entrada não calcula circuito final/alimentador; território, tipologia, atividade, edição e data conferidos; condições desconhecidas permanecem pendentes por instalação.|
|06.05|Ib mono/trifásico e fonte com conexão/tensão/equilíbrio explícitos, fórmulas/precisão e hash. Disponível na API; não sobrescreve Ib canônica nem homologa dimensionamento definitivo.|
|06.06|Grafo F05 único, propagação sem dupla contagem; máximo um por empate; partidas simultâneas declaradas; rótulo de grupo não fraciona artificialmente mesma regra/fonte.|
|06.07|Histórico imutável, comparação de cenários/equipamentos, fingerprint de topologia/levantamento/catálogo; catálogo alterado invalida memória anterior.|
|06.08|Memória de fatores por carga, seleção e fonte; CLI, API, consulta de catálogo e exemplo documental na interface.|
|06.09|Escopo EDP SP/edição V09, data até a última conferência, tipologia/atividade, tensão/frequência e área confirmada; conformidade profissional e aprovação da concessionária separadas.|

## Testes locais observados

- API completa: **722 passed**, um aviso Starlette/httpx; resultado mais recente registrado no commit/CI.
- Vinculação: **85 testes novos**, incluindo referência documental, cada limiar/faixa, exceções, máximos/empates/partidas, escopo incompatível, adulteração recusada e invalidação por catálogo.
- F06 total: **118 testes** (33 anteriores + 85 novos).
- Chromium: **27 passed**, 47,59 s; novo fluxo consulta catálogo de 22 regras e calcula referência `CALCULATED_SOURCE_LINKED`.
- F00: **34 golden**, fixture intacta.
- AIOX: `npm run lint`, `npm run typecheck`, `npm test` (**18 testes**) e `npm run build`: PASS.
- CLI calculou exemplo documental e consultou catálogo real. Sintaxe JS e `git diff --check`: PASS.

## QA3 da vinculação

|Revisor|Veredito|Evidência/correções|
|---|---|---|
|QA-01|APROVADO para código/vínculo|Resolver do servidor, reserva de IDs, memória sem coeficiente fictício, fingerprint e invalidação; QA-01.md|
|QA-02|APROVADO para fonte/matemática do recorte|Fonte oficial+PDF local, texto idêntico, revisão visual, bases kW/quantidade, exceções e referência independente; QA-02.md|
|QA-03|APROVADO para integração/UX|API/CLI, consulta de catálogo, exemplo documental, fatores por carga e E2E; QA-03.md|

Três perspectivas do mesmo assistente; não equivalem a três auditorias humanas independentes. Os pareceres atuais superam o bloqueio inicial da vinculação sem conceder homologação profissional.

Correções críticas: seleção de T005 pela potência ativa, e não VA; limites superiores inclusivos; um único máximo em empate; partidas simultâneas agrupadas; exceções sem extrapolação; grupos não fracionáveis pelo rótulo; coeficientes reservados não substituíveis; edição futura não presumida; mudança de catálogo invalida resultado histórico. O exemplo da fonte arredonda a parcela a para 2221 VA; teste usa conta racional exata e registra diferença inferior a 0,5 VA, sem forçar igualdade artificial.

## Limites operacionais

`CALCULATED_SOURCE_LINKED` significa cálculo vinculado à fonte conferida. `normative_conformity_verified=false`, `utility_approval=false` e `authoritative_for_sizing=false` continuam explícitos. Dados de placa, mínimos aplicáveis, tipos, quantidade, partidas e condições precisam ser declarados/conferidos na instalação. Não há conversão automática de CV/HP ou levantamento de área/vitrine; não se aplicam estas regras a outra edição/concessionária. Casos fora do recorte recebem diagnóstico por instalação, sem fator inventado.

Código/estado anteriores preservados no histórico Git. Sem merge em main, deploy ou banco real. Incremento publicado em [`20e067bc1b1cfa01234810ec5fee67de47e58ae0`](https://github.com/SFPTechnology/Projeto-SIE-2.0/commit/20e067bc1b1cfa01234810ec5fee67de47e58ae0). Árvore remota `834e6de8056a1cd087eaa15d67b4ef12f77bb29f` idêntica à local `e6502459c74adef9a13d64b7443300a9c1e24997`. Atualização com lease sobre o head esperado; sem PR, merge ou deploy. CI será registrado após observação dos três workflows.
