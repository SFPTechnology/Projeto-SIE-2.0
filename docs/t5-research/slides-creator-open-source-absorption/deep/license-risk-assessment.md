# Deep Dive — License Risk Assessment

## Objetivo

Separar o que podemos copiar, adaptar, apenas estudar ou evitar na absorção dos projetos open-source.

## Matriz de Risco

| Projeto | Licença | Risco | Uso recomendado |
|---|---|---:|---|
| `ppt-master` | MIT | Baixo | Pode inspirar arquitetura e, se necessário, reaproveitar código com atribuição. Preferir reimplementação adaptada ao DeckSpec. |
| Presenton | Apache-2.0 | Baixo | Pode orientar API/MCP/self-hosted. Cuidar de NOTICE se reaproveitar código. |
| PPTAgent | MIT | Baixo | Pode inspirar planner/reflection/avaliação. |
| presentation-ai | MIT | Baixo | Pode orientar editor, temas e outline-first. |
| powerpoint-skill | MIT | Baixo | Pode absorver regras e scripts com atribuição quando fizer sentido. |
| slide-deck-ai | MIT | Baixo | Pode orientar CLI/provider baseline. |
| banana-slides | AGPL-3.0 | Alto | Usar como benchmark de UX. Não copiar código sem decisão jurídica. |
| PresentAgent-2 | Não verificada | Alto | Usar como referência conceitual até confirmar licença. |

## Classes de Absorção

| Classe | Definição | Permitido agora |
|---|---|---|
| Ideia/padrão | Conceito de produto ou arquitetura sem copiar código | Sim |
| Interface compatível | Recriar endpoint/contrato inspirado em comportamento | Sim, com cuidado |
| Código adaptado | Copiar/alterar trechos | Só MIT/Apache com atribuição e revisão |
| Dependência direta | Importar pacote ou rodar componente | Só após ADR/licença |
| Fork | Usar projeto como base | Não recomendado para nenhum |

## Riscos Específicos

### banana-slides

AGPL pode contaminar distribuição se código for integrado a serviço/produto sem conformidade. Usar apenas para:

- análise de UX;
- screenshots;
- wireflows próprios;
- descrição de padrões;
- comparação de capabilities.

### PresentAgent-2

Licença não verificada no inventário. Até confirmar:

- não copiar código;
- não importar dependências;
- não expor como componente.

## Política Recomendada

1. Criar ADR de absorção OSS antes de qualquer reuso de código.
2. Reimplementar os módulos críticos em estilo SINKRA.
3. Manter `THIRD_PARTY_NOTICES.md` se código MIT/Apache for incorporado.
4. Registrar origem por artifact no bench.
5. Para AGPL, tratar como competitor research, não como fonte de implementação.
