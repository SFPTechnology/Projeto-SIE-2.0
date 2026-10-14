# Análise Completa - Erro nas Telas por Override Legado da Categoria U com 380 V

**Data:** 2026-06-22  
**Autor:** Atlas (`aios-analyst`)  
**Contexto:** análise do erro visualizado nas telas do sistema com a mensagem:

> `Falha ao carregar dados Override categoria U: 380 V não é ofertado para categoria U (monofásico) na rede EDP SP.`

---

## 1. Resumo executivo

O problema **não é de renderização de tela**. O defeito é um erro de **dado legado inválido** no módulo EDP-SP, que está sendo propagado para a UI por um **serviço compartilhado de backend/domínio**.

Existe um override persistido para a categoria `U` contendo `380 V`, combinação que passou a ser proibida pela nova validação. A aplicação já tem uma sanitização parcial para esse legado, mas ela foi aplicada apenas no endpoint específico de parâmetros EDP. As telas principais de **Padrão de Entrada** e **Correntes (IB)** continuam usando outro fluxo, que lê o override bruto e quebra antes da montagem da tela.

Em termos práticos:

- o erro **não nasce no componente visual**;
- o erro **não afeta todas as telas indiscriminadamente**;
- o erro afeta as telas que passam pelo fluxo central de cálculo EDP-SP e consomem o override legado sem saneamento.

---

## 2. Evidência observada

Na captura recebida, a tela exibida é:

- **Correntes de projeto (IB)**

Mensagem mostrada:

- `Falha ao carregar dados Override categoria U: 380 V não é ofertado para categoria U (monofásico) na rede EDP SP.`

Isso já indica duas coisas:

1. a tela está recebendo um `ErrorState` normal da aplicação;
2. o erro já chegou pronto do backend/domínio, com mensagem de regra de negócio.

---

## 3. Escopo real do impacto

O usuário reportou que “todas as telas estão assim”, mas a análise do código mostra um impacto mais preciso.

### 3.1 Telas afetadas diretamente

As telas afetadas são as que dependem do fluxo EDP-SP centralizado:

1. **Padrão de Entrada**
   - arquivo: `src/routes/projetos.$projetoId_.padrao-entrada.tsx`
2. **Correntes (IB)**
   - arquivo: `src/routes/projetos.$projetoId_.correntes.tsx`

### 3.2 Telas não necessariamente afetadas

A tela principal do projeto:

- `src/routes/projetos.$projetoId.tsx`

não consome esse mesmo merge de parâmetros EDP-SP no carregamento principal e, tecnicamente, **não deveria quebrar pelo mesmo motivo**.

### 3.3 Conclusão de escopo

Portanto, o problema:

- **não é global de UI**;
- **não é CSS/roteamento/renderização**;
- é um defeito concentrado nas telas que dependem do cálculo e snapshot EDP-SP.

---

## 4. Achados técnicos detalhados

## Achado 1 - O erro é de domínio, não de interface

O componente visual apenas mostra a mensagem recebida.

Arquivo relevante:

- `src/components/app/ErrorState.tsx`

Comportamento:

- recebe `titulo`, `detalhe` e `onRetry`;
- exibe uma `InlineNotification` com `Falha ao carregar dados`.

Conclusão:

- a UI **não gera** a mensagem;
- a UI apenas **renderiza** a mensagem já produzida pela camada superior.

---

## Achado 2 - Existe validação nova rejeitando `U + 380`

A regra de negócio que proíbe `380 V` para categoria `U` está implementada.

Arquivos relevantes:

- `src/api/schemas/parametros-edp.ts`
- `src/domain/distribuidora/edp-sp/parametros.ts`
- `src/domain/distribuidora/edp-sp/categorias-fornecimento.ts`

Regra implementada:

- `categoria U` não pode ofertar `380 V`;
- tentativas novas de persistência devem falhar;
- isso está correto do ponto de vista normativo e funcional.

Conclusão:

- a regra nova está correta;
- o problema não é a existência da validação;
- o problema é **como ela interage com dados antigos já persistidos**.

---

## Achado 3 - Há dado legado inválido persistido

O erro exibido só ocorre se ainda existir no repositório um override salvo com:

- `id = "U"`
- `tensoes_ofertadas` contendo `380`

Repositórios relevantes:

- `src/infra/repositorios/repositorio-parametros-edp.ts`
- `src/infra/supabase/repo-parametros-edp.supabase.ts`

Comportamento:

- o repositório retorna os `overrides` crus;
- não há saneamento no ponto de leitura da persistência;
- o dado inválido legado continua circulando.

Conclusão:

- a origem persistida do problema ainda existe;
- a aplicação está reagindo ao dado legado, não a um input novo do usuário.

---

## Achado 4 - A sanitização foi aplicada apenas em um caminho secundário

Existe saneamento no serviço de parâmetros EDP.

Arquivo relevante:

- `src/domain/servicos/servico-parametros-edp.ts`

Comportamento identificado:

- o `GET /api/v1/distribuidora/edp-sp/parametros` passa por uma sanitização de overrides legados;
- nesse fluxo, `380` é removido da categoria `U` antes do merge;
- esse endpoint já foi preparado para tolerar legado inválido.

Conclusão:

- esse endpoint específico está protegido;
- mas essa proteção **não foi centralizada** nem reutilizada nos demais fluxos.

---

## Achado 5 - O fluxo principal ainda faz merge com dado bruto

O defeito estrutural está no serviço central de Padrão de Entrada.

Arquivo-chave:

- `src/domain/servicos/servico-padrao-entrada.ts`

Trecho lógico relevante:

1. lê override persistido via `ctx.repoParamsEDP.obter(projeto.id)`
2. obtém `overrides` crus
3. chama `mesclarParametros(parametrosDefault(), overrides)`

O problema:

- esse merge acontece **sem sanitização prévia**;
- se vier `U + 380`, a validação do domínio lança erro;
- esse erro interrompe o carregamento do agregado usado pela tela.

Conclusão:

- o serviço central ainda está operando com a hipótese incorreta de que os dados persistidos já estão limpos;
- essa hipótese foi invalidada pela presença de legado.

---

## Achado 6 - A tela de Correntes depende desse mesmo fluxo central

Arquivo relevante:

- `src/domain/servicos/servico-corrente.ts`

Comportamento identificado:

- `servicoCorrente` chama `padraoSvc.obter(projetoId)`;
- `padraoSvc` é o serviço de Padrão de Entrada;
- logo, qualquer falha em `servicoPadraoEntrada` também quebra a tela de Correntes.

Conclusão:

- a tela de Correntes não tem um defeito próprio;
- ela herda o problema da tela de Padrão de Entrada porque depende do mesmo serviço.

---

## Achado 7 - O endpoint de parâmetros e as telas principais estão inconsistentes entre si

Hoje existem dois comportamentos diferentes para o mesmo conceito de dado:

### Caminho A - Tolerante ao legado

- `GET /api/v1/distribuidora/edp-sp/parametros`
- passa por `servicoParametrosEDP`
- sanitiza override legado

### Caminho B - Não tolerante ao legado

- `GET /api/v1/projetos/:id/padrao-entrada`
- `GET /api/v1/projetos/:id/correntes`
- passam por `servicoPadraoEntrada`
- não sanitizam override legado

Conclusão:

- há uma **inconsistência arquitetural**;
- a mesma entidade de negócio (`overrides EDP`) recebe tratamentos diferentes conforme o endpoint.

---

## 5. Causa raiz

A causa raiz é:

> **dado legado inválido (`categoria U` com `380 V`) persistido no repositório, combinado com uma sanitização aplicada apenas no endpoint secundário de parâmetros, mas ausente no fluxo central de montagem do estado EDP-SP usado pelas telas principais.**

Em formato de cadeia causal:

1. no passado, foi salvo um override inválido `U + 380`;
2. foi adicionada uma regra nova proibindo essa combinação;
3. o sistema passou a rejeitar corretamente gravações novas;
4. porém, o legado antigo continuou salvo;
5. uma correção parcial saneou apenas `servicoParametrosEDP`;
6. `servicoPadraoEntrada` continuou lendo o dado bruto;
7. as telas que dependem desse serviço passaram a falhar ao abrir.

---

## 6. Impacto funcional

### 6.1 Impacto no usuário

O usuário vê:

- mensagem genérica de falha de carregamento;
- tela principal do fluxo indisponível;
- sensação de que “o sistema inteiro quebrou”.

### 6.2 Impacto técnico

- o agregado EDP-SP não é montado;
- a navegação funcional fica interrompida;
- o dado legado inválido continua sendo uma bomba de efeito recorrente.

### 6.3 Impacto de manutenção

- comportamentos divergentes entre endpoints aumentam risco de regressão;
- qualquer nova tela que reutilize `servicoPadraoEntrada` herdará o mesmo defeito.

---

## 7. O que não é a causa

É importante registrar o que **não** explica o erro:

1. **não é problema de CSS ou tema**
2. **não é problema de roteamento do frontend**
3. **não é problema do componente `ErrorState`**
4. **não é problema da query React Query em si**
5. **não é falha do catálogo default atual de categorias**

O catálogo atual já está coerente para `U`:

- `tensoes_ofertadas: [127]`

Logo, o erro vem do **override persistido**, não do catálogo base.

---

## 8. Recomendação objetiva

## Recomendação principal

Aplicar a **mesma sanitização de overrides legados** no fluxo central usado por:

- `servicoPadraoEntrada`
- `servicoCorrente`

Ponto ideal:

- antes do `mesclarParametros(parametrosDefault(), overrides)` em `calcularEdpSp()`

ou, de forma ainda melhor:

- extrair a sanitização para uma função compartilhada de domínio e reutilizá-la em:
  - `servicoParametrosEDP`
  - `servicoPadraoEntrada`

## Recomendação complementar

Persistir a cura do legado, para que o dado inválido deixe de existir no repositório.

Isso pode ser feito por:

1. migração corretiva no banco
2. rotina de saneamento de leitura com regravação
3. script administrativo pontual

## Recomendação de arquitetura

Centralizar a regra em um único ponto:

- **validar e sanitizar overrides EDP antes de qualquer merge**

Assim, qualquer endpoint ou tela que use esses parâmetros se comportará de forma consistente.

---

## 9. Critério objetivo para considerar a correção concluída

A correção estará fechada quando os três cenários abaixo passarem juntos:

1. **Tela de Padrão de Entrada abre normalmente** mesmo com legado antigo no banco.
2. **Tela de Correntes abre normalmente** para o mesmo projeto.
3. **PUT de parâmetros EDP continua rejeitando** qualquer nova tentativa de salvar `categoria U + 380`.

Ou seja:

- tolerância para legado no carregamento;
- rejeição para dado novo inválido no salvamento.

---

## 10. Conclusão final

O sistema não está quebrando “em todas as telas” por um erro genérico de frontend. O que existe é um **ponto único de falha no fluxo central do módulo EDP-SP**, provocado por override legado inválido e por uma sanitização incompleta.

O defeito é classicamente de **compatibilidade retroativa**:

- a regra nova está certa;
- o dado legado está errado;
- a aplicação ficou parcialmente adaptada;
- as telas principais continuam consumindo o caminho não adaptado.

Portanto, a ação correta não é mexer nos componentes visuais, e sim **corrigir o fluxo central de leitura/merge dos parâmetros EDP-SP e eliminar o legado persistido**.

---

## 11. Arquivos citados na análise

- `src/components/app/ErrorState.tsx`
- `src/domain/servicos/servico-parametros-edp.ts`
- `src/domain/servicos/servico-padrao-entrada.ts`
- `src/domain/servicos/servico-corrente.ts`
- `src/infra/repositorios/repositorio-parametros-edp.ts`
- `src/infra/supabase/repo-parametros-edp.supabase.ts`
- `src/routes/projetos.$projetoId_.padrao-entrada.tsx`
- `src/routes/projetos.$projetoId_.correntes.tsx`
- `src/routes/projetos.$projetoId.tsx`
- `src/domain/distribuidora/edp-sp/parametros.ts`

