# Inventory — PPTAgent

## Identidade

- **Repo:** `icip-cas/PPTAgent`
- **Clone local:** `../bench/PPTAgent`
- **Licença:** MIT
- **Prioridade:** P0
- **Papel na stack:** planejamento agentic, reflexão, design critique e avaliação.

## Evidência Lida

- `../bench/PPTAgent/README.md`
- `../bench/PPTAgent/pptagent/pptgen.py`
- `../bench/PPTAgent/deeppresenter`

## Capacidades Fortes

| Capacidade | Observação |
|---|---|
| Planner | Separa planejamento antes da geração final. |
| Research/design agents | Papéis especializados para conteúdo e design. |
| Reflection | Loop de revisão para melhorar slides. |
| PPTEval | Avaliação por conteúdo, design e coerência. |
| MCP/CLI | Indícios de uso via comando e integração agentic. |

## Limitações

- Mais framework acadêmico/agentic do que produto UX.
- Pode ser pesado para MVP se absorvido integralmente.
- O padrão de avaliação precisa ser adaptado à governança SINKRA.

## O Que Absorver

1. **Planning layer:** plano explícito antes de render.
2. **Reflection history:** cada alteração registra motivo, evidência e alvo.
3. **Design critique:** avaliação visual separada da narrativa.
4. **Rubricas PPTEval:** complementar QA SINKRA.
5. **Before/after QA:** comparar deck antes e depois da reflexão.

## Integração SINKRA Recomendada

```yaml
deck_spec:
  narrative_plan: ...
  design_plan: ...
  reflection_history:
    - slide_id: s03
      issue: "headline not action-oriented"
      fix: "rewrite action title"
      evaluator: "qa-inspector"
```

## Critério de Aceite

- Todo deck tem plano narrativo e plano visual antes da renderização.
- QA falha reencaminha para agente correto.
- Reflection não reescreve briefing sem permissão.
- QA final mostra delta de melhoria por dimensão.
