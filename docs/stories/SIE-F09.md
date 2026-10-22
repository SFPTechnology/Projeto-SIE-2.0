# Story SIE-F09 — Concessionárias e aplicações especializadas

**Estado:** IMPLEMENTED_PARTIAL / VALIDATING  
**Branch:** `feat/f09-concessionarias-especializadas`  
**Escopo:** diagnóstico consultivo por padrão de distribuidora e contratos opcionais para extensões; não libera projeto ou conexão.

## Entrega desta iteração

- API de catálogo e enquadramento consultivo em `/api/v1/distribuidoras` e `/api/v1/distribuidoras/enquadrar`.
- A única entrada cadastrada é EDP São Paulo, documento `PT.DT.PDN.00068`, edição 09, recorte de rede aérea secundária. A referência à edição foi conferida no portal oficial em 22/10/2026. Vigência final continua condicionada.
- O motor EDP anterior é reutilizado apenas como gerador de categoria candidata. O retorno inclui escopo da fonte, gates pendentes, alertas, data da última consulta e `connection_release=false`.
- Distribuidora desconhecida não herda valores EDP. Data do projeto posterior à consulta oficial impede sugestão até atualizar o catálogo.
- Extensões opcionais SPDA, fotovoltaica, recarga de veículos e ambientes especiais têm contratos próprios e não estão vinculadas como pré-requisito do núcleo. Sem motor e conjunto de critérios completos, retornam pendência e `release=false`.
- SPDA identifica a série ABNT NBR 5419 (Partes 1–4, versões corrigidas 2026 listadas no Catálogo ABNT); VE identifica ABNT NBR 17019:2022 como metadado de catálogo. Nenhuma delas foi convertida em regra de cálculo.

## Critérios e limites

| Task | Estado | Evidência / limite |
|---|---|---|
| 09.01 Catálogo por distribuidora | PARCIAL | `distributor_engine_f09.py`; apenas EDP SP identificada. Outros cadastros dependem de fonte, área, edição e vigência próprias. Critérios V09 continuam pendentes de revisão profissional e de catálogo completo. |
| 09.02 Motor candidato EDP | PARCIAL | Reusa `enquadrar_com_contexto`; gates de território, edição, fornecimento, demanda/medição, ramal, proteção e processo da distribuidora ficam PENDING. Sem liberação de conexão. |
| 09.03 Fornecimento | PENDENTE | API não integra automaticamente as evidências estruturadas F06/F07/F08; exige conferência cruzada no caso real. |
| 09.04 Diagnóstico consultivo | IMPLEMENTADO | API distingue sugestão, bloqueio e padrão não cadastrado; sem promessa de aceitação. |
| 09.05 Interface multi-distribuidora | IMPLEMENTADO PARCIAL | Contrato comum e registro isolado; somente adaptador candidato EDP disponível. |
| 09.06 SPDA | INTERFACE / MOTOR PENDENTE | Extensão opcional separada. Catálogo ABNT lista NBR 5419-1 a -4 corrigidas em 2026; critérios integrais, análise de risco e casos não foram validados. |
| 09.07 FV e outras fontes | INTERFACE / MOTOR PENDENTE | Não calculado. Inversores, proteções, conexão, UPS e geradores exigem catálogo técnico e caso independente. |
| 09.08 Recarga de veículos | INTERFACE / MOTOR PENDENTE | Extensão opcional; ABNT NBR 17019:2022 registrada apenas como metadado do catálogo. |
| 09.09 Ambientes especiais | INTERFACE / MOTOR PENDENTE | Isolado do núcleo; sem classificador nem regra habilitada. |
| 09.10 Limites/versões | PARCIAL | Testes cobrem distribuidora desconhecida, território incompatível, carga especial, data posterior à última consulta e preservação do estado bloqueado. Integração real de mudança de concessionária/edição aguarda persistência de projeto. |

## Verificação local

- F09 + regressão EDP contextual: **38 passed**.
- Suíte completa da API: **1027 passed** (inclui testes de replay dourado; 1 aviso Starlette/httpx).
- `npm run lint`, `npm run typecheck`, `npm test` (18 testes), `npm run build`, `compileall` e `git diff --check`: PASS.
- Dependências instaladas somente no ambiente local de validação. Nenhum manifesto ou lockfile alterado.

Os resultados acima verificam software e estados de bloqueio. Não verificam conformidade normativa, instalação física, versão em qualquer data futura ou aprovação da distribuidora.
