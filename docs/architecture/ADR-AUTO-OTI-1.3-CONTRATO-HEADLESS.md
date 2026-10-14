# ADR-AUTO-OTI-1.3 — Contrato headless para seções otimizadas

- **Data:** 2026-08-02
- **Autoridade:** Aria (Architect) / equipe de arquitetura
- **Status:** Aceito

## Caso de uso

O caso de uso `aplicarSecoesOtimizadasProjeto` aplica, de forma reproduzível, as seções otimizadas de todos os circuitos de um projeto.

## Decisão

1. Expor o endpoint `POST /api/v1/projetos/:projetoId/dimensionamento-condutores/aplicar-secoes-otimizadas` como contrato HTTP canônico.
2. Disponibilizar o CLI `bin/aplicar-secoes-otimizadas.mjs`, que consome exclusivamente essa API (sem acesso direto ao banco ou ao domínio).
3. O domínio produz uma assinatura JSON estável (canonicalização determinística) e seu hash SHA-256; a assinatura acompanha cada aplicação e permite idempotência/auditoria.
4. Persistir uma linha por projeto e circuito, com versão/assinatura, usando RPC transacional e recibo da operação para garantir atomicidade e rastreabilidade.
5. As linhas possuem os estados `VIGENTE` e `OBSOLETA`; uma nova aplicação obsoleta a versão anterior do mesmo projeto/circuito na mesma transação.
6. O módulo MOD-QT consulta somente linhas `VIGENTE`; registros `OBSOLETA` permanecem para histórico e não participam de cálculos.
7. Contratos protegidos existentes permanecem inalterados (compatibilidade retroativa).

## Consequências

- A API e o CLI ficam desacoplados da persistência e podem ser operados headlessly em automações.
- Assinatura estável + SHA-256 viabilizam deduplicação, auditoria e verificação de integridade.
- RPC transacional evita estados parciais, ao custo de manter recibos e histórico de versões.
- Consumidores devem filtrar explicitamente `VIGENTE`; dados obsoletos não devem ser usados por MOD-QT.

## Gates de aceitação

- [ ] POST implementa o caso de uso e retorna recibo com assinatura/hash.
- [ ] CLI chama apenas o endpoint versionado e propaga erros/recibo.
- [ ] Canonicalização JSON e SHA-256 são determinísticos para a mesma entrada.
- [ ] RPC grava projeto/circuitos atomicamente e alterna `VIGENTE`/`OBSOLETA`.
- [ ] MOD-QT lê exclusivamente `VIGENTE`.
- [ ] Testes de contrato confirmam que os contratos protegidos não foram alterados.
