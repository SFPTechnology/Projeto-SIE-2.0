# SIE Command Center

Nova proposta de Design System e arquitetura de experiência para o Projeto SIE.

## Resultado

Esta entrega cria uma variante **independente, navegável e documentada**. Nenhum componente, rota, token ou estilo do produto atual foi modificado.

- **Direção:** premium empresarial, técnica, precisa e orientada a dados.
- **Cores prioritárias:** `#0B3367` (primária) e `#061E3D` (secundária).
- **Padrão de workspace:** navegação por ciclo do projeto + superfície central + inspetor contextual.
- **Piso de acessibilidade:** WCAG 2.2 AA.
- **Estado:** conceito validável; não é implementação de produção nem executa cálculos.

## Como visualizar

Abra [`prototype/index.html`](./prototype/index.html) no navegador. O protótipo não utiliza dependências externas.

Interações disponíveis:

- Navegação pelos módulos;
- `Ctrl/Cmd + K` para abrir a paleta de comandos;
- `?` para abrir ajuda/atalhos;
- Alternância entre densidade confortável e compacta;
- Seleção de circuitos e atualização do inspetor;
- Inspetor responsivo e navegação mobile.

## Artefatos

| Área | Arquivo | Conteúdo |
|---|---|---|
| Protótipo | [`prototype/index.html`](./prototype/index.html) | Workspace interativo e responsivo |
| Preview desktop | [`prototype/sie-command-center-desktop.png`](./prototype/sie-command-center-desktop.png) | Captura em 1600 × 1000 |
| Preview mobile | [`prototype/sie-command-center-mobile.png`](./prototype/sie-command-center-mobile.png) | Captura de inspeção responsiva |
| Tokens | [`tokens/sie-premium.tokens.json`](./tokens/sie-premium.tokens.json) | Fonte DTCG de tokens |
| Tokens CSS | [`tokens/sie-premium.css`](./tokens/sie-premium.css) | Variáveis consumidas pelo protótipo |
| Arquitetura | [`docs/experience-architecture.md`](./docs/experience-architecture.md) | IA, módulos, layouts e componentes |
| Componentes | [`docs/component-catalog.md`](./docs/component-catalog.md) | Catálogo Atomic Design e contratos |
| Auditoria | [`audit/current-state.md`](./audit/current-state.md) | Evidências brownfield e oportunidades |
| Pesquisa | [`research/benchmark.md`](./research/benchmark.md) | Referências oficiais e decisões derivadas |
| Adoção | [`migration/adoption-plan.md`](./migration/adoption-plan.md) | Estratégia lado a lado e rollback |
| Qualidade | [`validation/quality-report.md`](./validation/quality-report.md) | Checklist de UX, UI, a11y e validações |

## Princípios

1. **Fluxo antes de telas:** os módulos acompanham a sequência real do cálculo.
2. **Contexto sempre visível:** projeto, módulo, estado e seleção não desaparecem.
3. **Dados explicáveis:** estado técnico inclui motivo, origem e próxima ação.
4. **Densidade progressiva:** resumo primeiro; detalhe no inspetor, expansão ou drill-down.
5. **Atalhos sem exclusão:** teclado acelera especialistas, mas toda ação continua acessível por ponteiro.
6. **Zero hardcode na camada visual:** o protótipo consome somente tokens semânticos.
7. **CLI continua soberano:** esta proposta observa e organiza resultados; não substitui a fonte de verdade operacional.

## Limites conhecidos

- Persona primária e dispositivo principal ainda não estão validados com pesquisa de campo.
- Métricas e números do protótipo são explicitamente demonstrativos.
- A adoção em produção exige story aprovada, testes com projetistas e implementação incremental por `@dev`.
- Decisões de arquitetura de frontend em produção requerem ratificação de `@architect`.
- A promoção formal pelo squad está bloqueada porque os paths canônicos `squads/` e `workspace/` não existem neste checkout.
