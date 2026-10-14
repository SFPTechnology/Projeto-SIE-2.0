# Auditoria brownfield — interface atual do Projeto SIE

**Data:** 2026-07-31  
**Escopo:** `sistema-de-instala-es-el-tricas-sie-main/src`  
**Modo:** somente leitura; nenhum arquivo atual alterado

## Sumário executivo

A aplicação atual possui boa cobertura funcional e um conjunto amplo de componentes, mas o sistema visual está fragmentado entre Carbon, Radix/shadcn, Tailwind e estilos inline. A proposta nova não substitui essa base agora: cria uma referência semântica independente para orientar consolidação futura.

## Evidência quantitativa

| Indicador | Valor observado |
|---|---:|
| Arquivos TSX | 119 |
| Arquivos CSS | 4 |
| Rotas TSX | 12 |
| Componentes em `components/ui` | 46 |
| Componentes em `components/app` | 43 |
| Ocorrências de `style={{...}}` | 625 |
| Ocorrências de classes Carbon `cds--` | 68 |
| Ocorrências de cores hex em TSX/CSS | 123 |

Os números são contagens mecânicas com `rg`; representam sinais de dispersão, não um veredito individual sobre cada ocorrência.

## Pontos fortes existentes

- Stack moderna: React 19, TanStack Router/Query, Tailwind 4, Carbon, Radix e TypeScript.
- Biblioteca base já extensa em `src/components/ui/`.
- Fluxos técnicos reais para ambientes/dependências, padrão de entrada, circuitos, correntes, condutores, queda de tensão e unifilar.
- Componentes de estado, loading, erro, ajuda e rastreabilidade já presentes.
- Testes dedicados em áreas de maior risco, como dimensionamento e unifilar.
- Uso atual do tema Carbon `g100`, compatível com software técnico de alta densidade.

## Fricções observadas

### 1. Shell sem arquitetura de módulos

`src/components/app/AppShell.tsx` oferece marca, autor e conteúdo, porém não oferece navegação persistente, contexto do projeto, estado do fluxo ou busca global. As páginas resolvem navegação localmente por breadcrumbs e links diferentes.

**Impacto:** o usuário precisa reconstruir mentalmente onde está e qual módulo vem depois.

### 2. Layout e estilo distribuídos

Há grande volume de estilos inline e regras específicas em `src/styles.css`, além de tokens locais de unifilar/divisor.

**Impacto:** alterações globais de densidade, foco, espaçamento e contraste exigem múltiplas intervenções.

### 3. Duas bibliotecas visuais em paralelo

Carbon e primitives Radix/shadcn coexistem, mas não há camada documentada de tokens semânticos que determine quando e como cada primitive assume aparência SIE.

**Impacto:** risco de estados, raios, alturas, foco e comportamento divergentes.

### 4. Páginas técnicas como ilhas

Os módulos usam hero, ações e cards próprios. O percurso:

`Dependências → Padrão de entrada → Correntes → Condutores → Queda de tensão → Unifilar`

existe funcionalmente, mas não é apresentado como fluxo contínuo no shell.

**Impacto:** dependências downstream e próximos passos ficam menos previsíveis.

### 5. Densidade única

Tabelas largas e formulários extensos precisam atender especialistas e telas menores com o mesmo arranjo.

**Impacto:** muito scroll em desktop ou compressão excessiva em tablet.

## Decisões de consolidação

| Atual | Direção proposta |
|---|---|
| `AppShell` mínimo | `EngineeringShell` com projeto, módulos e comandos |
| Breadcrumb local variável | Cabeçalho contextual padronizado |
| Cards isolados | Painéis semânticos com slots e densidade |
| Cor por componente | Tokens por papel: ação, estado, superfície, dado |
| Links de próximo módulo | Jornada técnica persistente |
| Modal para todo detalhe | Inspetor lateral para leitura; modal apenas para decisão bloqueante |
| Métricas sem origem visível | Rastreabilidade no inspetor |
| Uma densidade | `comfortable` e `compact` via tokens |

## Rastreabilidade de módulos

| Novo agrupamento | Artefato funcional existente |
|---|---|
| Workspace / Projetos | `src/routes/index.tsx` |
| Ambientes e cargas | `src/routes/projetos.$projetoId.tsx` |
| Padrão de entrada | `src/routes/projetos.$projetoId_.padrao-entrada.tsx` |
| Circuitos | `src/routes/projetos.$projetoId_.circuitos.tsx` |
| Correntes | `src/routes/projetos.$projetoId_.correntes.tsx` |
| Condutores | `src/routes/projetos.$projetoId_.dimensionamento-condutores.tsx` |
| Queda de tensão | `src/routes/projetos.$projetoId_.queda-tensao.tsx` |
| Diagrama unifilar | rotas `unifilar` e `unifilar-diagrama` |
| Diagnóstico | `src/routes/diagnostico.tsx` |

Nenhum novo módulo funcional foi inventado. A proposta reorganiza capacidades já identificadas no código.

