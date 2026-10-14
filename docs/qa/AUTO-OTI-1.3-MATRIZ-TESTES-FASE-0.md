# Matriz QA Fase 0 — AUTO-OTI-1.3

**Data:** 2026-08-02  
**Escopo:** estratégia antecipada; o veredito final permanece sob `@qa` após implementação.

| Critério | Evidência obrigatória | Gate |
|---|---|---|
| AC1 | Teste API/CLI aplica circuito pertencente, recalcula, persiste linha vigente e retorna `DURAVEL`. | PASS |
| AC2 | Teste de integração UI confirma pelo caso de uso comum; MOD-QT lê após invalidação de query. | PASS |
| AC3 | Teste de lote filtra aprovados, confirma explicitamente, usa uma transação e retorna contagens. | PASS |
| AC4 | Teste de assinatura diferente marca linha anterior `OBSOLETA` e MOD-QT retorna `PEND`. | PASS |
| AC5 | Falha transitória sem commit preserva vigente e registra falha. | PASS |
| AC6 | Duas operações em circuitos distintos permanecem sem perda em teste concorrente Supabase/RPC. | PASS |
| AC7 | Versões divergentes no mesmo circuito retornam conflito sem efeito parcial. | PASS |
| AC8 | Precedência manual > automática vigente; remoção manual revela automática ou `PEND`. | PASS |
| AC9 | Tabela/RPC ausente distingue `FALHOU`; adaptador de teste explicita `VOLATIL`; nenhum badge aplicado. | PASS |
| AC10 | Circuito removido/renomeado/recriado por novo ID não reutiliza registro anterior. | PASS |
| AC11 | Sem fonte elegível, resposta mantém `null`, `—` e `PEND`. | PASS |
| AC12 | Inspeção por símbolo, typecheck, testes de regressão e build comprovam contratos/fórmulas intactos. | PASS |
| NFR-REL-01/02 | RPC tudo-ou-nada, retry idempotente por `(projetoId, operacaoId, hash)` e testes de deadlock/conflito. | BLOCK se ausente |
| NFR-DUR-01 | Apply → reload → nova aba → nova sessão conserva somente registros duráveis. | BLOCK se ausente |
| NFR-OBS-01 | Log correlaciona operação, projeto, circuitos, assinaturas, versões, contagens e persistência sem segredos. | PASS |
| NFR-SEC-01 | Testes de pertencimento/cross-project e RLS deny-by-default nos objetos novos. | BLOCK se ausente |
| NFR-COMP-01 | `RetornoMODQT`, schemas MOD-QT e endpoint protegido permanecem compatíveis. | BLOCK se regressão |
| NFR-CLI-01 | Execução do caso de uso sem React, navegador ou `localStorage`. | BLOCK se ausente |

Além dos testes automatizados, a revisão final deve comprovar `apply → validar → rollback → reapply` da migration em ambiente isolado, reconciliação da trilha de migrations e waiver formal para qualquer policy legada permissiva.
