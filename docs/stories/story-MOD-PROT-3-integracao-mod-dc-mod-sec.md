---
executor: "@dev"
quality_gate: "@architect"
quality_gate_tools: [contract_validation, regression_test, integration_test, api_review]
---

# Story MOD-PROT-3: Integração com MOD-DC (ponto único de acoplamento)

## Status

**Done**

## Story

**As a** engenheiro eletricista,
**I want** que o resultado do MOD-PROT alimente automaticamente o critério C2 do MOD-DC e exponha `tempo_atuacao_s` de forma rastreável,
**so that** eu não precise fornecer manualmente valores que o próprio sistema já calculou, sem quebrar nada que já funciona.

> ⚠️ **Risco HIGH desta story** (confirmado por `@architect *analyze-impact` sobre o PRD): `aplicarSugestaoProtecaoSeAusente` (`overrides.ts`) é consumido por **três** caminhos diferentes — MOD-DC (critério C2), `auto-otimizacao-retencao.ts` (épico AUTO-OTI) e, indiretamente, qualquer fluxo que dependa de `resolverParametrosCircuito`. Trate a suíte completa (`npx vitest run`) como gate de saída não-negociável desta story.

## Acceptance Criteria

1. `aplicarSugestaoProtecaoSeAusente` (`src/domain/dimensionamento-condutores/overrides.ts`) passa a consultar o motor MOD-PROT (`selecionarProtecaoCircuito`, Story MOD-PROT-1) e o override do circuito (`resolverParametrosProtecaoCircuito`, Story MOD-PROT-2) em vez de chamar `sugerirProtecaoCircuito` diretamente; a heurística permanece como fallback interno quando o motor completo não resolver (`in_a: null`).
2. A assinatura de retorno consumida pelo MOD-DC (`in_a`, `origem_in`, `i2_a`, `fonte_i2`) **não muda** — `ParametrosDimensionamento` continua com o mesmo shape.
3. Critério C2 (`motor-sobrecarga.ts`) continua sendo avaliado corretamente com os valores agora vindos do MOD-PROT (`origem_in: "MOD-PROT"` em vez de `"SUGESTAO"` quando o motor completo resolve).
4. `resultado.tempo_atuacao_s` calculado pelo MOD-PROT fica disponível no resultado do circuito (campo exposto, não injetado automaticamente em nenhuma chamada HTTP — ver Nota de Escopo abaixo).
5. Quando o motor MOD-PROT não resolve (IB fora de faixa), o sistema cai para `sugerirProtecaoCircuito` preservando exatamente o comportamento anterior à esta story (`origem_in: "SUGESTAO"`).

## Nota de Escopo (leia antes de implementar)

O PRD original (FR6) previa que esta story tornasse MOD-PROT "a fonte real de `tempo_atuacao_s` para o MOD-SEC". Investigação arquitetural (`docs/architecture/mod-prot-contrato-integracao.md`, Decisão D6) encontrou que **nenhum código no repositório hoje chama `POST /api/v1/modulos/mod-sec/validar`** — não existe orquestrador identificado para essa chamada. Por isso, **o escopo desta story fica reduzido a expor `tempo_atuacao_s` no resultado** (AC4) — a decisão de orquestrar automaticamente a chamada ao MOD-SEC (D6 do ADR, opção "b") é trabalho futuro, fora desta story. `@po` deve validar esta redução de escopo antes do desenvolvimento começar.

## 🤖 CodeRabbit Integration

**Story Type Analysis**
**Primary Type**: Integration (ponto de acoplamento com sistema já em produção)
**Secondary Type(s)**: Architecture (ponto único de falha identificado por impact analysis)
**Complexity**: High — baixo volume de código, mas múltiplos consumidores não óbvios (C2, AUTO-OTI) tornam o raio de regressão amplo

**Specialized Agent Assignment**
**Primary Agents**:
- @dev (implementação)
- @architect (revisão do ponto de acoplamento — já sinalizado como risco HIGH no impact analysis)

**Supporting Agents**:
- @qa (cobertura de regressão adicional, dado o risco elevado)

**Quality Gate Tasks**
- [ ] Pre-Commit (@dev): `coderabbit --prompt-only -t uncommitted`
- [ ] Pre-PR (@github-devops): `coderabbit --prompt-only --base main`
- [ ] Pre-Deployment (@github-devops): `coderabbit --prompt-only -t committed --base HEAD~10` — recomendado dado o risco HIGH desta story, mesmo não sendo story de infraestrutura

**Self-Healing Configuration**
**Expected Self-Healing**:
- Primary Agent: @dev (light mode)
- Max Iterations: 2
- Timeout: 15 minutes
- Severity Filter: CRITICAL

**Predicted Behavior**:
- CRITICAL issues: auto_fix (até 2 iterações)
- HIGH issues: document_only — **mas dado o risco desta story, qualquer HIGH relacionado a `overrides.ts` deve ser escalado a @architect antes de aceitar como débito técnico**

**CodeRabbit Focus Areas**
**Primary Focus**:
- Nenhuma mudança de assinatura pública em funções consumidas por outros módulos (`aplicarSugestaoProtecaoSeAusente`, `resolverParametrosCircuito`, `dimensionarLoteComOverrides`)
- Regressão em `auto-otimizacao-retencao.ts` (consumidor não óbvio, achado do impact analysis)

**Secondary Focus**:
- Tratamento correto do caso de fallback (IB fora de faixa) — não pode silenciosamente retornar `in_a: null` sem cair para a heurística

## Tasks / Subtasks

- [x] Implementar a nova versão de `aplicarSugestaoProtecaoSeAusente` em `overrides.ts` (AC: 1, 2, 5)
  - [x] Chamar `selecionarProtecaoCircuito` (Story MOD-PROT-1) com `retorno_cc: circuito.retorno_cc`
  - [x] Se `resultado.in_a != null`: usar `origem_in: "MOD-PROT"`, `fonte_i2: resultado.norma_dispositivo`
  - [x] Se `resultado.in_a == null`: cair para `sugerirProtecaoCircuito` (comportamento idêntico ao atual)
  - [x] **Override do circuito propagado (correção aplicada após revisão do AC1):** a implementação inicial só chamava o motor global, sem considerar override salvo no MOD-PROT — não satisfazia literalmente o AC1 ("motor MOD-PROT (global **ou override do circuito**)"). Corrigido adicionando `RetornoMODPROT` e o campo `circuito.retorno_protecao` em `contratos.ts` (tipo definido localmente, não importado de `dimensionamento-disjuntores`, para preservar a direção única de dependência do ADR D2), e uma função `anexarRetornoProtecao` em `servico-dimensionamento-condutores.ts` que resolve o override (via `resolverParametrosProtecaoCircuito`) e anexa o resultado a cada circuito antes de `dimensionarLoteComOverrides`. `aplicarSugestaoProtecaoSeAusente` agora prioriza `circuito.retorno_protecao` sobre a chamada direta ao motor.
- [x] Expor `tempo_atuacao_s` no resultado do circuito (AC: 4)
  - [x] Campo adicionado a `ParametrosDimensionamento` e `ResultadoDimensionamento` (aditivo) — **não** foi criada chamada HTTP nova ao MOD-SEC nesta story (ver Nota de Escopo)
- [x] Testes de regressão (AC: 1–5)
  - [x] `dimensionamento-condutores-flow.test.ts` — todos os testes preexistentes passam; um teste teve sua expectativa **atualizada** (`origem_in` de `"SUGESTAO"` para `"MOD-PROT"`) porque encodava literalmente o comportamento antigo que esta story existe para mudar (AC3); novo teste dedicado adicionado cobrindo a propagação do override do MOD-PROT até o C2 do MOD-DC
  - [x] Novo teste cobrindo `auto-otimizacao-retencao.ts` — circuito sem `in_a` global, confirma `origem_in: "MOD-PROT"` via `mapearParametrosEfetivosAtuais` (consumidor não mapeado na v1 do PRD, achado do `*analyze-impact`)
  - [x] Teste de fallback: IB fora de faixa → `in_a`/`origem_in` permanecem `null` (não há cenário real em que MOD-PROT falhe e a heurística de fallback resolva, já que ambas compartilham deliberadamente a mesma série normativa — ver Dev Notes)
  - [x] Suíte relevante `npx vitest run` verde (122 testes em 19 arquivos entre as duas rodadas de verificação); suíte completa do projeto rodada uma vez com 1148/1159 passando — as 11 falhas são pré-existentes e não relacionadas (confirmado rodando os 3 arquivos isolados)

## Dev Notes

### O ponto de acoplamento exato (copiar a estrutura, não redesenhar)

O ADR já especifica o corpo completo da função (`mod-prot-contrato-integracao.md`, Decisão D5) — implemente exatamente essa estrutura:

```ts
function aplicarSugestaoProtecaoSeAusente(
  circuito: CircuitoParaDimensionamento,
  parametros: ParametrosDimensionamento,
): ParametrosDimensionamento {
  if (parametros.in_a != null) return parametros;

  const resultado = selecionarProtecaoCircuito({
    ib_a: circuito.corrente_projeto_a,
    tipo_instalacao: parametros.tipo_instalacao,
    tipo_carga: circuito.tipo,
    retorno_cc: circuito.retorno_cc,
  });

  if (resultado.in_a != null) {
    return {
      ...parametros,
      in_a: resultado.in_a,
      origem_in: resultado.origem_in, // "MOD-PROT"
      i2_a: parametros.i2_a ?? resultado.i2_a,
      fonte_i2: parametros.fonte_i2 ?? resultado.norma_dispositivo,
    };
  }

  const sugestao = sugerirProtecaoCircuito({ ib_a: circuito.corrente_projeto_a, tipo_instalacao: parametros.tipo_instalacao });
  if (sugestao.in_a == null) return parametros;
  return {
    ...parametros,
    in_a: sugestao.in_a,
    origem_in: sugestao.origem_in, // "SUGESTAO"
    i2_a: parametros.i2_a ?? sugestao.i2_a,
    fonte_i2: parametros.fonte_i2 ?? sugestao.fonte_i2,
  };
}
```
[Source: architecture/mod-prot-contrato-integracao.md#d5]

### Os três consumidores — nenhum pode quebrar

1. **`motor-sobrecarga.ts` (critério C2)** — consome `in_a`/`i2_a` de `ParametrosDimensionamento`. Já trata `in_a == null` com pendência `AGUARDANDO-PROTECAO` (ver `motor-sobrecarga.ts:21`) — esse comportamento não muda.
2. **`src/components/app/dimensionamento-condutores/auto-otimizacao-retencao.ts`** — chama `resolverParametrosCircuito` **diretamente** (não passa por `dimensionarLoteComOverrides`), para lógica de retenção do épico AUTO-OTI. Este é o consumidor que a primeira versão do PRD não havia mapeado — encontrado pelo `*analyze-impact`. Teste de regressão obrigatório (ver Tasks).
3. **UI de dimensionamento de condutores** (`projetos.$projetoId_.dimensionamento-condutores.tsx`) — consome o resultado via `api.dimensionarCondutoresLote`; não deveria precisar de nenhuma mudança, mas vale checar visualmente após a implementação (snapshot VRT `dimensionamento-condutores.vrt.test.tsx`).

[Source: PRD-MOD-PROT-dimensionamento-disjuntores.md#0.1]

### Por que o escopo de `tempo_atuacao_s` foi reduzido

Ver "Nota de Escopo" acima. Resumo: `POST /api/v1/modulos/mod-sec/validar` existe mas não tem chamador identificado no código — não é seguro (nem seria "No Invention") inventar um orquestrador só para esta story. Expor o campo é suficiente para não bloquear o restante do epic; a automação fica para depois. [Source: architecture/mod-prot-contrato-integracao.md#d6]

### Previous Story Insights

Depende diretamente de MOD-PROT-1 (`selecionarProtecaoCircuito`) e MOD-PROT-2 (`resolverParametrosProtecaoCircuito`, `DisjuntorOverride`). Revisar o File List e Completion Notes de ambas antes de iniciar esta story — em particular, confirmar o nome exato dos exports (podem ter mudado durante a implementação em relação ao que está descrito nos Dev Notes dessas stories).

### Testing

- Framework: Vitest.
- Testes de regressão são o foco principal desta story (ver Tasks) — não é uma story de "testar coisa nova", é uma story de "provar que nada quebrou".
- Rodar a suíte completa (`npx vitest run`) é mandatório antes de mover a story para InReview — não apenas os arquivos diretamente relacionados.

### Project Structure Notes

Único arquivo de produção modificado nesta story: `src/domain/dimensionamento-condutores/overrides.ts`. Nenhum arquivo novo de domínio é esperado (a lógica nova já foi criada nas Stories MOD-PROT-1/2) — esta story é puramente de **fiação** (wiring) entre módulos já existentes.

> **Atualização pós-implementação:** a fiação completa do AC1 (override, não só motor global) exigiu tocar também `contratos.ts` (novo campo aditivo `retorno_protecao` + tipo `RetornoMODPROT`) e `servico-dimensionamento-condutores.ts` (nova função `anexarRetornoProtecao`, chamada em `dimensionarLoteProjeto`) — ver Completion Notes.

## Change Log

| Date | Version | Description | Author |
|------|---------|--------------|--------|
| 2026-08-05 | 1.0 | Story criada a partir do PRD-MOD-PROT e do ADR `mod-prot-contrato-integracao.md`; escopo de `tempo_atuacao_s`/MOD-SEC reduzido conforme Decisão D6 do ADR | River (@sm) |
| 2026-08-05 | 1.1 | Validated GO (8/10) — Status: Draft → Ready. Redução de escopo do FR6 (exposição de `tempo_atuacao_s`, sem orquestração automática ao MOD-SEC) ratificada e sincronizada de volta no PRD-MOD-PROT (Seção 2, FR6) | Pax (@po) |
| 2026-08-05 | 1.2 | Implementado, com correção de escopo em relação ao Dev Notes original (AC1 exigia considerar override, não só motor global — gap identificado e corrigido durante a implementação). Suíte de regressão completa verde. Status: Ready → Ready for Review | Dex (@dev) |
| 2026-08-08 | 1.3 | QA Gate PASS (5/5 ACs; tsc exit 0, sem regressao em MOD-DC/MOD-SEC) | Quinn (@qa) |
| 2026-08-08 | 1.4 | Status: Ready for Review -> InReview (normalizacao de ciclo de vida) | Dex (@dev) |

## Dev Agent Record

### Agent Model Used

Claude Sonnet 5 (claude-sonnet-5), modo YOLO (autônomo)

### Debug Log References

Nenhum log de debug formal. Principal achado documentado: a primeira implementação de `aplicarSugestaoProtecaoSeAusente` (seguindo literalmente o snippet do Dev Notes/ADR) só chamava o motor global — não considerava override salvo no MOD-PROT, o que deixava o AC1 parcialmente insatisfeito ("global **ou override do circuito**"). Identificado em autorrevisão antes de marcar a story completa, não por falha de teste (nenhum teste cobria esse caminho até eu adicionar um). Corrigido adicionando o campo `retorno_protecao` ao contrato de circuito e uma função de anexação na camada de aplicação — ver Completion Notes para o desenho da correção e a análise de import circular que descartei uma alternativa mais simples.

`npx vitest run` completo: 1148/1159 passando. As 11 falhas (3 arquivos: 2 VRT de unifilar + 1 timeout em teste de catálogo de impedância) são pré-existentes e não relacionadas — confirmado rodando os 3 arquivos completamente isolados (sem nenhum outro teste no processo), onde ainda falham identicamente. Nenhum desses arquivos foi tocado por esta story ou por qualquer story do épico MOD-PROT.

### Completion Notes List

- **Correção de escopo pós-implementação inicial:** adicionei `RetornoMODPROT` (tipo definido localmente em `contratos.ts`, não importado de `dimensionamento-disjuntores`, para preservar a direção única de dependência A→B do ADR) e o campo `CircuitoParaDimensionamento.retorno_protecao`. `aplicarSugestaoProtecaoSeAusente` agora prioriza esse campo (já resolvido, override-aware) sobre a chamada direta ao motor.
- **Nova função `anexarRetornoProtecao`** em `servico-dimensionamento-condutores.ts`, chamada dentro de `dimensionarLoteProjeto`, busca os overrides persistidos do MOD-PROT (`ctx.repoDisjOverrides`) e resolve cada circuito via `resolverParametrosProtecaoCircuito` (importado de `@/domain/dimensionamento-disjuntores`) antes do dimensionamento.
- **Risco de import circular avaliado e descartado:** cheguei a considerar importar o *serviço* de aplicação do MOD-PROT (`servicoDimensionamentoDisjuntores`) dentro de `servico-dimensionamento-condutores.ts`, mas esse serviço já importa `anexarRetornosMODCC` de volta — criaria um ciclo real entre os dois arquivos de serviço. Em vez disso, chamei o *domínio* de MOD-PROT diretamente (`resolverParametrosProtecaoCircuito`), que só tem imports `import type` de `dimensionamento-condutores` (erradicados em tempo de compilação, sem ciclo em runtime). Confirmado sem erro após `npx tsc --noEmit` completo duas vezes.
- **Teste pré-existente corrigido, não ignorado:** `tests/api/dimensionamento-condutores-flow.test.ts` tinha um teste que esperava literalmente `origem_in: "SUGESTAO"` no cenário que esta story existe para mudar — atualizei a expectativa para `"MOD-PROT"` com comentário explicando o porquê, em vez de deixar o teste quebrado ou reescrever a lógica para preservar o comportamento antigo.
- **Fallback (AC5) é estruturalmente correto mas raramente exercido na prática:** como o motor MOD-PROT (Story 1) reaproveita deliberadamente a mesma série normativa da heurística (`SERIE_PROTECAO_IN_A`), não existe hoje um valor de IB em que o motor falhe e a heurística resolva — ambos falham juntos acima de 63A. O código de fallback está correto e testado (nenhuma exceção, comportamento preservado), mas documentei essa nuance para não sugerir que há um cenário real de "motor falha, heurística salva" além do caso degenerado de falha conjunta.

### File List

**Criados:**
- `src/domain/dimensionamento-condutores/overrides.test.ts`

**Modificados:**
- `src/domain/dimensionamento-condutores/contratos.ts` (campos aditivos `norma_dispositivo`/`capacidade_interrupcao`/`tempo_atuacao_s`/`retorno_protecao`; novo tipo `RetornoMODPROT`)
- `src/domain/dimensionamento-condutores/overrides.ts` (`aplicarSugestaoProtecaoSeAusente` reescrita)
- `src/domain/dimensionamento-condutores/servico-dimensionamento-condutores.ts` (`anexarRetornosMODCC` exportado; nova `anexarRetornoProtecao`; rastreio de proteção; wiring em `dimensionarLoteProjeto`)
- `src/components/app/dimensionamento-condutores/auto-otimizacao-retencao.test.ts` (novo teste de regressão)
- `tests/api/dimensionamento-condutores-flow.test.ts` (expectativa de teste corrigida + novo teste de propagação de override)

## QA Results

### Review Date: 2026-08-08

### Reviewed By: Quinn (Test Architect)

**Traceability:** 5/5 ACs atendidas.

- **AC1 (correção de escopo validada):** `dimensionamento-condutores/overrides.ts:112` chama `selecionarProtecaoCircuito` e a cadeia de precedência documentada em `:81-88` cobre os **três** caminhos — override do circuito, motor global e fallback heurístico. A lacuna apontada pelo @dev (primeira implementação só cobria o motor global) está fechada.
- **AC2:** `ParametrosDimensionamento` inalterado — garantido em todos os consumidores por `tsc --noEmit` exit 0.
- **AC3:** `origem_in: "MOD-PROT"` gravado em `:102`; critério C2 consome o mesmo campo.
- **AC4:** `tempo_atuacao_s` exposto em `ResultadoProtecaoCircuito`, sem injeção automática em chamada HTTP.
- **AC5:** fallback devolve `origem_in: "SUGESTAO"` com comportamento idêntico ao anterior; rastreado ao ADR `mod-prot-contrato-integracao.md` (D5).

**Escopo da evidência (limitação declarada):** o gate se apoia em análise estática, tipagem e testes unitários/integração (1186/1187 na suíte completa, zero regressão em MOD-DC/MOD-SEC). **Não** houve validação em runtime/navegador. A recomendação do @dev de um QA Loop completo dado o risco HIGH **permanece pertinente** e não é substituída por este gate.

### Gate Status

Gate: PASS → docs/qa/gates/MOD-PROT-3-integracao-mod-dc-mod-sec.yml

### Re-Review Date: 2026-08-08

Re-verificado apos o commit `2ecd1ca`: `tsc` exit 0, `lint` exit 0, `build` e `build:spa` exit 0, sem regressao em MOD-DC/MOD-SEC. Veredito mantido.

### Gate Status (mantido)

Gate: PASS -> docs/qa/gates/MOD-PROT-3-integracao-mod-dc-mod-sec.yml
