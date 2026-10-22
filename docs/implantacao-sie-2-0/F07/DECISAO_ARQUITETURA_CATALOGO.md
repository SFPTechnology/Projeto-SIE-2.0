# F07 — Decisão de arquitetura para catálogo e seleção fonte-vinculados

Data: 22/10/2026. Papel delegado: arquitetura. Base inspecionada: `conductor_f07.py`, `conductor_api.py`, `conductor_cli.py`, CONTRATO.md e artefato F07. Esta decisão não valida células numéricas nem concede homologação normativa.

## Decisão

Preservar o contrato `Study` e a análise declaratória existentes. Acrescentar um serviço de seleção com catálogo finito, imutável e versionado no servidor. Ele usa o agregado F02/F05 como conectividade canônica e reutiliza a fórmula Decimal e a avaliação de todos os trechos do motor atual. Os aceites e as células F01 permanecem intactos; novos dados e a relação documental com o lote aceito pertencem a uma versão F07 separada.

O catálogo deve carregar somente dados efetivamente conferidos na fonte oficial/fabricante: identificador, edição, URL, hash do PDF, página, tabela/célula, grandeza/unidade e condições de aplicação. Rca/XL devem estar relacionados a produto, material, isolação, seção, temperatura, frequência e arranjo. As restrições físicas do recorte não podem ser inferidas de texto livre ou de um nome genérico como PVC. O PDF completo e suas figuras não precisam ser redistribuídos no repositório público.

O recorte proposto pelo especialista — cobre/PVC, família de cabo identificada, B1, dois condutores carregados, 60Hz/70°C, neutro sem redução e PE da mesma seção — é uma hipótese de aplicação a confirmar na leitura das fontes. Nenhum valor ou faixa de seção deste documento é uma tabela aprovada. Condutores separados, PEN, harmônicas, solo, influências adicionais e arranjos diferentes só entram se houver regra correspondente; caso contrário recebem bloqueio específico. Condições de PE/proteção mecânica merecem contrato próprio, mesmo quando se escolhe PE igual à fase.

## Interfaces mínimas

|Camada|Contrato recomendado|
|---|---|
|Domínio|Catálogo/resolver separados da seleção; funções puras para capacidade/fatores/mínimos/N/PE/queda; política de seleção explícita|
|CLI|Ação de seleção sobre JSON canônico e consulta de catálogo; memória JSON completa; estado calculado separado de conformidade profissional|
|API|Endpoint de seleção e catálogo, preservando `/condutores/analisar`; persistência local herda token, isolamento e revisão otimista existentes|
|UI|Consultar catálogo/seleção pelo mesmo serviço; mostrar seção por circuito/percurso, cada critério e os motivos de rejeição; nenhuma decisão elétrica exclusiva em JavaScript|
|Histórico|Entrada solicitada, catálogo e parâmetros resolvidos, candidato escolhido, resultados por trecho/circuito, política e hashes; snapshot da seleção não altera silenciosamente o cadastro canônico|

A seleção não deve aceitar tabelas, Rca/XL, fatores ou flags de verificação arbitrárias do cliente sob um identificador reservado do servidor. Se o contrato antigo trouxer parâmetros em conflito, rejeitar ou registrar claramente a divergência; não esconder substituição. A resolução do servidor deve ficar visível na memória para permitir reprodução.

## Avaliação conjunta da instalação

Escolher cada circuito isoladamente e depois somar resultados não garante a queda acumulada: os limites dos alimentadores e dos terminais dependem da cadeia até a fonte. Cada candidato final deve, portanto, ser um vetor de seções dos percursos, avaliado contra todos os trechos e todos os limites de circuito/alimentador na topologia inteira. Percursos alternativos/paralelos, fases/bases/cosφ incompatíveis e queda anterior à origem sem evidência continuam bloqueados no modelo atual.

Não se exige otimizador econômico global para cumprir a F07. Uma implementação determinística e conservadora pode:

1. Resolver o mínimo local de cada percurso por capacidade e mínimos aplicáveis, verificando todos os seus trechos.
2. Calcular as quedas e limites de todas as cadeias com o vetor completo.
3. Quando uma cadeia falhar por queda, aumentar monotonicamente as seções ajustáveis do caminho com um critério de desempate estável e documentado, recalculando a instalação inteira.
4. Parar somente quando todos os critérios F07 aplicáveis atenderem, ou quando se esgotarem as seções do catálogo para a falha observada.

Uma política simples pode aumentar todos os percursos ajustáveis dos caminhos reprovados a cada iteração. É conservadora e termina após número finito de incrementos, mas pode superdimensionar. Não deve alegar resultado econômico ótimo ou mínimo global. Para atribuir esgotamento à impossibilidade no recorte, a monotonicidade da tabela de capacidade/queda precisa ser validada; dados não monotônicos exigem busca completa ou estado inconclusivo explícito.

Se for adotada enumeração de combinações, deve haver poda local e orçamento de trabalho. Orçamento excedido produz `PENDENTE`/`SEARCH_BUDGET_EXCEEDED`, nunca uma conclusão falsa de ausência de solução. Uma rejeição de capacidade não é motivo para omitir critérios de seção, N, PE e queda: cada um deve conservar estado explícito.

## Fingerprint e invalidação

Incluir na chave: entradas físicas canônicas, atribuições por circuito/trecho, versão do algoritmo/política, versão e hash integral do catálogo, identificação da fonte e regras de mínimos/limites. Uma fonte, catálogo, política, Ib, seção, método ou trecho alterados tornam resultados e documentos anteriores stale. A persistência deve invalidar execuções canônicas de proteção e documentos como o fluxo atual já faz. Não é necessário criar migração de produção nem alterar o esquema histórico F02 para incluir metadados adicionais de F07.

Um cálculo fonte-vinculado deve registrar um estado distinto da análise declaratória. Pode indicar que todos os critérios F07 do recorte foram satisfeitos, mantendo `normative_conformity_verified=false` e `authoritative_for_sizing=false`; não afirma proteção integral, curto-circuito/adiabático ou homologação profissional. Esses critérios futuros devem ser classificados como F08, sem esconder qualquer requisito obrigatório de F07.

## Riscos que os testes e QA precisam contestar

- Índice de coluna errado na extração do PDF: comparar dados extraídos com página renderizada e caso independente.
- Seção mínima ou PE de um arranjo aplicado a outro: rejeição explícita, inclusive proteção mecânica/condutor separado.
- Recálculo local que ignora alimentadores ou o efeito a jusante: casos com dois trechos e dois níveis de quadro.
- Parâmetros de candidato calculados para seção anterior: resolver novamente toda impedância após cada mudança de seção.
- Igualdade exata ou muito próxima de limite: preservar a política de precisão e fronteira já documentada, sem arredondamento decisório.
- Histórico válido com nova versão do catálogo/política: testes de mudança de hash/revisão sem alteração das entradas físicas.
- Escopo de fonte recebido do cliente como aprovação: metadado descritivo não deve liberar combinações fora do resolver.

**Parecer de arquitetura:** extensão proposta é compatível com a fundação existente e suficiente para implementar as tasks 07.03/07.05/07.07/07.10 no recorte documental que o especialista comprovar. Aprovação de dados, implementação, testes e gates finais pertence às revisões QA, não é presumida por esta decisão.
