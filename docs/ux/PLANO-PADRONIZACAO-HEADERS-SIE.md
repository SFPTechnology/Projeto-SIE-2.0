# Plano de padronização dos headers — SIE

**Status:** pronto para implementação UX/UI  
**Responsável de design:** `aiox-ux-design-expert`  
**Escopo:** padronização visual e estrutural dos headers de página; sem alteração de regras de domínio ou fluxos de cálculo.

## Objetivo

Consolidar todos os headers de seção do SIE em um padrão único, tomando como referência visual `C:\Users\User\Downloads\Screenshot_234.jpg`.

O resultado deve restabelecer uma entrada de página consistente, legível e reconhecível, sem descaracterizar workspaces técnicos ou alterar as ações já existentes.

## Evidências analisadas

| Referência | Leitura |
|---|---|
| `Screenshot_234.jpg` | Padrão canônico: breadcrumb discreto, hero azul escuro em card de raio amplo, eyebrow, título com peso leve, descrição e ação principal no trilho direito. |
| `Screenshot_231.jpg` | Planejador de circuitos: hero próprio de workspace, título em `h2`, tags no topo e ausência de header de página. |
| `Screenshot_232.jpg` | Queda de tensão: navegação em botões separados e título dentro de card funcional; a entrada da página fica fragmentada. |

## Diagnóstico

A identidade de marca está disponível no código, mas não é aplicada de forma uniforme.

- [`src/styles/sie-theme.css`](../../sistema-de-instala-es-el-tricas-sie-main/src/styles/sie-theme.css) já define IBM Plex Sans/Mono, a rampa de azuis SIE e tokens Carbon semânticos.
- [`src/styles.css`](../../sistema-de-instala-es-el-tricas-sie-main/src/styles.css) possui dois precedentes próximos ao desejado: `.deps-hero` e `.sie-page-hero`.
- Há concorrência entre estilos compartilhados, estilos inline e componentes com CSS próprio (`divisor-hero`, `qt-card-header`, `sie-pagehead`).
- Breadcrumbs são duplicados: o `SieShell` já recebe trilha contextual, enquanto várias rotas adicionam outra navegação no conteúdo.

## Padrão canônico: `SiePageHero`

Criar um organismo de design system reutilizável, chamado provisoriamente `SiePageHero`. O nome definitivo deve seguir a convenção do repositório.

### Estrutura semântica

```text
SieShell
└── Conteúdo da página
    ├── Breadcrumb contextual discreto
    └── SiePageHero
        ├── Conteúdo principal
        │   ├── Eyebrow opcional
        │   ├── h1 único da página
        │   └── Descrição opcional
        └── Trilho de ações e metadados
            ├── Ação primária opcional
            ├── Ações secundárias opcionais
            └── Tags/metadados opcionais
```

### Regras de conteúdo

- Cada rota deve ter apenas um `h1` como título da página.
- O eyebrow é contextual, opcional e nunca substitui o título.
- Ações devem permanecer fora do fluxo do texto, no trilho direito; em telas menores, devem quebrar abaixo do conteúdo.
- Tags representam metadados ou estado; não devem competir visualmente com a ação primária.
- Navegação entre páginas deve ser breadcrumb/link discreto, não botões de aparência primária.
- Cabeçalhos internos de cards e workspaces permanecem `h2` ou inferiores e não substituem o header de página.

### Especificação visual derivada da referência

| Elemento | Especificação alvo |
|---|---|
| Família tipográfica | `var(--sie-font-sans)`; `var(--sie-font-mono)` somente para IDs, números e dados técnicos. |
| Eyebrow | 12px, peso 600, `letter-spacing: 0.08em`, caixa alta, `--cds-text-secondary`. |
| Título | `clamp(2rem, 4vw, 2.75rem)`, peso 400, line-height 1.05, `--cds-text-primary`. |
| Descrição | 16px, line-height 1.5, largura máxima aproximada de 760px, `--cds-text-secondary`. |
| Contêiner hero | padding de 28px; borda azul translúcida; raio de 16px; sem sombra concorrente. |
| Fundo | Gradiente SIE unificado: azul profundo vertical com foco radial azul sutil no canto superior direito. Usar tokens/variáveis centralizados, sem repetir hexadecimais nas rotas. |
| Ação primária | Botão Carbon `primary`, alinhado ao topo/trilho direito, mantendo o comportamento atual. |
| Responsividade | Abaixo de 960px, conteúdo e ações em coluna; ação ocupa largura natural/total conforme o componente Carbon. |

## Matriz de migração

| Prioridade | Seção | Estado atual | Ação de padronização |
|---|---|---|---|
| P1 | Queda de tensão | `qt-nav-actions` externo + `qt-card-header` funcional | Criar o hero de página antes do card. Converter “Voltar ao projeto” em breadcrumb; manter Tutorial como ação secundária; rebaixar o título interno do alimentador a `h2` contextual. |
| P1 | Planejador de circuitos | `divisor-hero` interno, título em `h2`, tags no topo | Adicionar `SiePageHero` na rota. Mover Camada C, título e tags para ele; preservar o workspace e toolbar abaixo; manter títulos internos como `h2`. |
| P2 | Correntes | `sie-page-hero` com estilos inline | Migrar para `SiePageHero`; remover gradiente, raio, tipografia e espaçamentos inline. |
| P2 | Dimensionamento de condutores | `sie-page-hero` e constantes de estilo locais | Migrar para `SiePageHero`; manter ação “Dimensionar condutores” no primeiro card até decisão explícita de produto para promovê-la ao hero. |
| P2 | Unifilar interativo | Hero próximo ao padrão, mas com estilos inline e múltiplos links de topo | Migrar ao organismo; reduzir navegação ao breadcrumb contextual. |
| P2 | Diagrama unifilar | Mesmo padrão do Unifilar, com links paralelos | Migrar ao organismo e eliminar variações próprias de gradiente. |
| P3 | Padrão de entrada | `deps-hero` próximo ao alvo; Tutorial dentro da cópia | Adotar o organismo e deslocar Tutorial para ações secundárias. |
| P3 | Dependências | Referência funcional do padrão atual | Usar como rota piloto para o organismo; preservar CTA “Nova dependência”. |
| P3 | Projetos | Variante compacta `sie-pagehead` após métricas | Criar variante `index` do organismo: sem hero obrigatório quando as métricas forem o primeiro bloco, mas com a mesma tipografia, alinhamento e área de ação. |
| Especial | Command Center | Header técnico de workspace e feature flag | Manter `EngineeringShell` e headers contextuais internos. Aplicar apenas o hero de página na entrada da rota quando habilitada; não criar segundo `h1`. |

## Componentes e estilos afetados

- `src/styles/sie-theme.css`: consolidar tokens semânticos exclusivos do hero, se necessários.
- `src/styles.css`: substituir `.deps-hero` e `.sie-page-hero` por estilos do organismo ou mantê-los apenas como compatibilidade temporária.
- `src/routes/projetos.$projetoId.tsx`
- `src/routes/projetos.$projetoId_.padrao-entrada.tsx`
- `src/routes/projetos.$projetoId_.correntes.tsx`
- `src/routes/projetos.$projetoId_.dimensionamento-condutores.tsx`
- `src/routes/projetos.$projetoId_.unifilar.tsx`
- `src/routes/projetos.$projetoId_.unifilar-diagrama.tsx`
- `src/routes/projetos.$projetoId_.queda-tensao.tsx`
- `src/routes/projetos.$projetoId_.circuitos.tsx`
- `src/components/divisor/DivisorCircuitosWorkspace.tsx`
- `src/components/divisor/divisor-workspace.css`
- `src/components/app/queda-tensao/PainelAlimentador.tsx`
- `src/routes/index.tsx`

## Ordem de implementação

1. Criar/validar a story de desenvolvimento com critérios de aceite e file list.
2. Definir tokens de hero e construir `SiePageHero` isoladamente, com variantes e testes de renderização.
3. Migrar Dependências como referência de baixo risco.
4. Migrar Queda de tensão e Planejador de circuitos, que apresentam maior divergência estrutural.
5. Migrar Correntes, Dimensionamento e os dois módulos Unifilar.
6. Migrar Padrão de entrada e a variante de índice Projetos.
7. Revisar Command Center em modo habilitado, preservando sua semântica de workspace.
8. Remover estilos inline e classes legadas somente após todas as rotas consumidoras terem sido migradas.

## Critérios de aceite

- [ ] Todas as seções listadas possuem header de página consistente com a referência `Screenshot_234.jpg`.
- [ ] Cada página possui exatamente um `h1`; títulos de cards/workspaces usam `h2` ou inferior.
- [ ] IBM Plex Sans é a fonte padrão dos headers; IBM Plex Mono é restrita a dados técnicos.
- [ ] Cores, bordas, gradientes e tipografia do hero são consumidos por tokens, sem valores de cor duplicados nas rotas.
- [ ] Breadcrumb e ações não aparecem duplicados.
- [ ] Ações existentes continuam disponíveis e com a mesma semântica funcional.
- [ ] Layout responde adequadamente em desktop e telas menores que 960px.
- [ ] Contraste de texto, botões e bordas atende WCAG AA.
- [ ] Testes visuais/snapshots são atualizados apenas após validação deliberada do novo padrão.
- [ ] `npm run lint`, `npm run typecheck`, `npm test` e build definidos pela story passam antes da conclusão.

## Fora de escopo

- Alterar cálculos, APIs, regras de domínio, permissões ou feature flags.
- Mudar a arquitetura funcional de módulos técnicos.
- Redesenhar componentes internos que não sejam cabeçalhos de página.
- Remover informações técnicas necessárias dos workspaces.

## Riscos e cuidados

- Não duplicar o breadcrumb já fornecido pelo `SieShell`; decidir uma única fonte visual da trilha antes da migração.
- A migração do Planejador deve preservar os tags de estado e a toolbar de ações operacionais.
- A migração da Queda de tensão deve manter o tutorial acessível e preservar os nomes/IDs usados por testes.
- O Command Center exige cuidado com a hierarquia de headings já protegida por testes.

## Próximo passo recomendado

O `aiox-ux-design-expert` deve executar um audit/tokenize/migrate focado neste documento e, antes de qualquer alteração de código, encaminhar uma story para criação por `aiox-sm` ou `aiox-po`, conforme a Constitution do projeto.
