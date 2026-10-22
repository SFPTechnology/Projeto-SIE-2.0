# QA-01 — Vinculação de catálogo e seleção F07

Revisão de arquitetura, código e testes realizada por agente de software; não é homologação normativa ou auditoria humana. Data:22/10/2026. Base do incremento anterior preservada; pareceres anteriores não foram sobrescritos.

## Escopo inspecionado

`conductor_registry_f07.py`, `conductor_selection_f07.py`, integrações `conductor_api.py`/`conductor_cli.py` e `test_conductor_binding_f07.py`. Interface visual estava em integração e pertence ao QA-03. Missão derivada dos itens07.03/05/07/08/10 do artefato F07.

## Testes observados

`python -m pytest restructuring/apps/api/tests/test_conductor_binding_f07.py -q --tb=short` → **64 passed**,1 aviso Starlette/httpx,1,36s.

Confirmados no código/testes: valores de catálogo derivados exclusivamente do servidor, concordância com células F01 aceitas, precisão Decimal200 e limites de entrada herdados, comparação sem arredondamento de apresentação, verificação de todos os trechos e limites por alimentador/terminal, política conservadora finita sem promessa de ótimo econômico, grupos explícitos com mesma corrente e seções normalizadas conjuntamente, fingerprints incluindo fonte/catálogo/política, histórico imutável e invalidação canônica/proteção/documentos. Modelo declaratório anterior permanece separado.

## Achado QA01-V1 — MÉDIA, impeditivo do contrato de catálogo — tabela incompleta/metadado inválido pode lançar exceção em vez de bloquear com motivo

Requisito:07.03 e QA-01 exigem rejeição de tabelas inválidas/incompletas; erro de fonte deve produzir diagnóstico explícito, sem aprovar e sem derrubar o endpoint.

Reprodução em processo isolado, com cópia de `registry.CATALOG`:

1. Remover `sections[0].iz_base_a`; chamar `select(Selection.model_validate_json(exemplo))`.
2. Resultado observado: `KeyError: 'iz_base_a'`, não `BLOQUEADO/CATALOG_INVALID`.
3. Restaurar e alterar `source.sha256` para `invalid`; chamar novamente.
4. Resultado observado: `ValidationError` ao construir `Study`, em vez de bloqueio estruturado. A consulta de catálogo tampouco valida esse campo antes da resolução.

Causa: `catalog()` acessa campos obrigatórios por subscrição sem validar integralmente a estrutura/metadados. `_select` só transforma `ValueError` da chamada inicial em `CATALOG_INVALID`; metadados incorretos podem alcançar `inspect_scope`/`resolve` e falhar posteriormente. Exemplo adicional relevante: data `source.verified_on` inválida.

Risco: não houve aprovação matemática incorreta, mas falha de contrato/diagnóstico e indisponibilidade do cálculo quando a tabela do servidor está incompleta/corrompida. Não é necessário relaxar validação; o correto é validar o catálogo inteiro antes de usá-lo e normalizar erros como `ValueError` com motivo seguro. Fonte/células F01 anteriores não devem ser alteradas para acomodar erro.

Correção solicitada: validação estrutural e numérica de campos obrigatórios, fatores, mínimos, fonte/hash/data/escopo, seguida de testes que comprovem POST de seleção bloqueado e GET de catálogo com erro controlado para entrada de catálogo inválida/incompleta. Nenhum código foi modificado por este revisor.

## Veredito inicial

**REPROVADO até corrigir QA01-V1.** A política de seleção conjunta e a arquitetura do incremento atendem ao recorte computacional examinado, mas o contrato de rejeição de tabela incompleta precisa ser fechado. Não concedo DONE nem aprovação normativa. A conclusão da fase depende ainda das evidências consolidadas de QA-02/QA-03, regressão e CI do código final.

## Revalidação QA01-V1 — RESOLVIDO

O catálogo passou a ter validação estrutural, metadados de fonte e hash/data, textos e referências com os limites dos contratos utilizados na resolução, grandezas decimais finitas dentro da precisão, fatores de referência, escopo compatível com a política implementada, mínimos comerciais representáveis e limites de queda dentro da faixa. A resolução inicial rejeita dados incompletos/incompatíveis antes de construir o estudo. `KeyError`, erro de tipo e decimal inválido são normalizados em `ValueError`; a API de seleção responde `BLOQUEADO/CATALOG_INVALID` e a consulta de catálogo responde422.

Reexecutei as reproduções originais e variantes de edição longa, limite de queda101 e pisoPE1000: todas retornaram `BLOQUEADO/CATALOG_INVALID`; GET catálogo422, sem exceção não controlada. O teste parametrizado `test_invalid_catalog_is_rejected_without_http500` cobre12variantes, sem modificar valores esperados para ocultar erros.

Comando observado na revalidação: `python -m pytest restructuring/apps/api/tests/test_conductor_binding_f07.py -q --tb=short` → **76 passed**,1 aviso Starlette/httpx,1,54s.

## Conferência da seleção conjunta

Cada circuito inicia na menor seção que satisfaz capacidade corrigida e mínimos mecânicos de todos os seus trechos. A avaliação posterior cobre o vetor completo de seções e os limites de todos os alimentadores/circuitos e dos terminais. O crescimento conservador nos caminhos reprovados e a normalização dos grupos só elevam índices do catálogo. O catálogo exige capacidade não decrescente eRca/XL não crescentes, enquanto correntes e fator de potência permanecem fixos e positivos no recorte. Assim, crescer uma seção não piora os critérios examinados.

ComN circuitos e4seções, cada índice admite no máximo3incrementos; o limite `1+N·3` inclui a avaliação final. Esgotamento de um caminho reprovado é relatado como ausência de solução **nesse catálogo**; eventual busca não concluída permanecePENDENTE. A política pode superdimensionar em relação a outra combinação viável, o que está declarado sem promessa de ótimo econômico.

Grupos agrupados exigem membros identificados, circuitos distintos e mesma corrente. A normalização mantém todos os circuitos de cada componente de agrupamento com a mesma seção em cada solução/iteração publicada. Não se reaproveita uma declaração genérica de homogeneidade enquanto se altera só a seção de um membro. Casos fora do recorte, harmônicas, material/isolação/método/frequência/condição não cobertos recebem bloqueio explícito.

## Veredito atual

**APROVADO para arquitetura, contratos, código e testes da seleção F07 no recorte fonte-vinculado implementado.** QA01-V1 corrigido e revalidado; não restam achados impeditivos desta perspectiva. As flags de conformidade profissional e de dimensionamento definitivo permanecem falsas, e proteção integral daF08 não é presumida.

Este parecer não concede aprovação normativa e não presume CI remoto ou QA visual que não executei. O encerramento computacional daF07 deve consolidar QA-02/QA-03, regressão eCI do código final, mantendo explícitas as fronteiras do catálogo e os requisitos posteriores de proteção. A reprovação inicial acima fica preservada somente como histórico do ciclo de correção.
