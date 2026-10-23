# F09 — concessionárias e aplicações especializadas

**Data:** 23/10/2026
**Estado:** `DONE` — integração essencial F06–F08 implementada, validada localmente e aprovada pelos três workflows remotos do SHA de código `59ba39c3ba1f9875c7092300cc6b8045bb3bc7e6`.
**Branch:** `feat/f09-concessionarias-especializadas`
**Commit de código publicado:** `59ba39c3ba1f9875c7092300cc6b8045bb3bc7e6` (derivado de `67b1ab497d590dd48a31deeb8381b8b11f0b0db5`)
**F08:** `DONE` para os gates de software no SHA `fc5f208bf5ee15911dd9bf78505339a97fd6d69b`, CI run `39872564016` success.

## Escopo e decisão do responsável

O responsável validou os itens 1 e 2 anteriormente apontados e determinou que as extensões do item 3 não sejam implementadas. Essas decisões foram respeitadas: nenhum item aceito foi reaberto e SPDA, fotovoltaicos/outras fontes, recarga de veículos e ambientes especiais não foram desenvolvidos. As extensões são opcionais e não bloqueiam o núcleo F09 nesta execução. Essa aceitação é uma decisão de escopo do responsável; não é apresentada como auditoria profissional independente nem como autorização da concessionária.

## Implementação desta retomada

A rota local autenticada `PUT /api/v1/local/projetos/{project_id}/distribuidoras/enquadrar` integra o enquadramento às revisões locais persistidas:

- F06: exige cenário atual de entrada e deriva corrente de demanda e potência ativa instalada por fonte; não aceita esses valores como entrada livre nesse fluxo.
- F07: exige o estudo mais recente não obsoleto, confirma o hash de entrada e compara o resultado persistido com recálculo do servidor.
- F08: exige o estudo mais recente não obsoleto; a rotina histórica verifica vínculo com F07, hash do resultado e recálculo.
- Proveniência: registra projeto/revisão, fonte, identificadores, hashes de entrada/topologia/resultado de F06–F08, hash do catálogo F09 e estados computacionais F07/F08. Mudança de F06–F08 ou do catálogo F09 torna o resultado obsoleto.
- Persistência: grava o diagnóstico na revisão local com controle otimista; uma avaliação nova substitui a anterior como avaliação vigente. Alterações posteriores nas evidências de origem tornam o registro anterior obsoleto.
- Segurança e limites: autenticação local existente, resposta consultiva, sem fallback para outra concessionária; `normative_conformity_verified=false`, `utility_approval=false` e `connection_release=false`.
- Bloqueio seguro: ausência, divergência, adulteração ou obsolescência de evidência retorna erro explícito e não gera enquadramento.

Rotas de histórico: `GET /api/v1/local/projetos/{project_id}/distribuidoras/enquadramentos`.

## Tasks e gates

| Task | Estado nesta execução | Evidência |
|---|---|---|
| 09.01 Catálogo/escopo de distribuidora | ACEITO PELO RESPONSÁVEL no item 1 | Catálogo candidato EDP SP V09 e escopo registrados; nenhum padrão EDP é reutilizado para outra distribuidora. |
| 09.02 Motor candidato/contexto | ACEITO PELO RESPONSÁVEL no item 1 | Motor preserva contexto, versão e bloqueios consultivos; edição futura ou contexto incompatível não libera candidato. |
| 09.03 Integração de fornecimento | IMPLEMENTADO E TESTADO | `distributor_persistence_f09.py`; vínculo a cenário de entrada F06 e estudos atuais F07/F08. |
| 09.04 Diagnóstico | APROVADO no recorte | Categoria candidata, pendências e proveniência; nenhuma promessa de aprovação. |
| 09.05 Isolamento entre distribuidoras | APROVADO no recorte | Distribuidora sem catálogo retorna `PADRAO_NAO_CADASTRADO`; sem fallback EDP. |
| 09.06–09.09 Extensões especializadas | FORA DO ESCOPO POR DECISÃO DO RESPONSÁVEL | SPDA, FV/outras fontes, VE e ambientes especiais não foram implementados e não bloqueiam F09 nesta execução. |
| 09.10 Limites, versão e obsolescência | APROVADO no recorte | Testes de distribuidora/contexto incompatível, fonte ausente, revisão concorrente, resultado F06 alterado após persistência e edição do catálogo alterada. |

## Testes observados nesta retomada

- Testes focados da nova integração: **6 passed**.
- Suíte completa da API: **1.033 passed**, um aviso de depreciação Starlette/httpx.
- `npm run lint`: PASS.
- `npm run typecheck`: PASS.
- `npm test`: **18 passed**.
- `npm run build`: PASS.
- `git diff --check`: PASS.
- E2E navegador não coletado: Playwright não está instalado no ambiente local; nenhuma interface visual foi alterada.
- CI remoto no SHA `59ba39c3ba1f9875c7092300cc6b8045bb3bc7e6`: API run `39880107120` PASS; Chromium run `39880107058` PASS; AIOX run `39880107092` PASS.

## Revisões QA

| Perspectiva | Estado | Conclusão |
|---|---|---|
| QA-01 — arquitetura/código/testes | APROVADO | Consulta somente histórico atual, recálculo confere os dados persistidos, entrada incompatível bloqueia e registros anteriores ficam obsoletos. Testes e CI remoto passaram. |
| QA-02 — engenharia/normas | ITENS 1 E 2 ACEITOS PELO RESPONSÁVEL | Decisão de escopo registrada conforme instrução do responsável. Não equivale a parecer assinado por profissional independente. O serviço continua sem liberar conformidade normativa ou conexão. |
| QA-03 — integração/dados/segurança | APROVADO no recorte da API local | Revisão esperada, autenticação, persistência, proveniência, obsolescência e CI cobertos; UI não integra o escopo. |

As três perspectivas de revisão foram feitas pelo mesmo agente e constituem autocrítica estruturada, não auditoria humana independente.

## Estado da passagem

A integração essencial pendente foi implementada e aprovada nos testes locais e nos três workflows de CI do SHA publicado. Os critérios opcionais 09.06–09.09 foram excluídos da passagem por decisão expressa do responsável. F09 está `DONE` no escopo essencial e o desenvolvimento de F10 está liberado segundo os gates do projeto. Nenhum merge em `main`, deploy ou alteração de banco real foi realizado.

A liberação de desenvolvimento não representa aprovação de projeto, conformidade normativa de uma instalação ou autorização de conexão pela distribuidora.
