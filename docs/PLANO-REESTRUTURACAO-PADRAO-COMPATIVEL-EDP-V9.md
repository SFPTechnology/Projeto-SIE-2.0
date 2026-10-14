# Plano de correção e reestruturação do campo “Padrão compatível” — EDP São Paulo V9

**Data da análise:** 26/07/2026  
**Responsável pela análise:** @analyst (Atlas)  
**Destinatários:** @dev, @architect, @po/@sm e @qa  
**Status:** plano técnico-funcional para refinamento e criação de stories; nenhuma implementação está autorizada por este documento  
**Fonte normativa principal:** `Arquivos_Diversos/Norma_EDP/PT.DT.PDN.00068_V9_chunks.json`  
**Norma analisada:** EDP São Paulo `PT.DT.PDN.00068`, versão 09, vigência indicada em 14/04/2026  
**Tela em escopo:** `projetos.$projetoId_.padrao-entrada`, seção “Fornecimento elétrico do projeto”, campo “Padrão compatível”

---

## 1. Resultado executivo

O defeito observado no campo “Padrão compatível” não é apenas uma ausência de opções no `Select`. Ele é consequência de três divergências estruturais:

1. a tela identificada como EDP São Paulo apresenta opções provenientes de um catálogo **genérico e parametrizável**, não do modelo de atendimento da EDP;
2. o sistema mantém simultaneamente um resultado genérico e um resultado EDP, e diferentes módulos posteriores consomem fontes diferentes;
3. o modelo de dados atual não representa dimensões obrigatórias da V9, especialmente topologia da rede, tensões 240/120 V, regras diferentes por topologia, solicitação de categoria superior, cargas especiais e todos os atributos físicos da subcategoria.

O comportamento da interface agrava o problema: quando o motor genérico retorna `sem-padrao`, `FornecimentoSelector` cria um conjunto vazio de IDs válidos e desabilita **todas** as opções. Portanto, o usuário entra justamente no estado em que precisa escolher uma solução e a interface não permite nenhuma escolha.

A correção definitiva deve:

- tornar o resultado EDP-SP a fonte canônica do padrão de entrada nessa rota;
- separar “categoria de atendimento” (U/D/T), “topologia/tensão da rede”, “subcategoria física” (U2, D2... T10) e “modalidade solicitada pelo cliente”;
- substituir o filtro binário atual por uma avaliação explícita de cada candidato, com status e motivo;
- propagar um único contrato de fornecimento para Circuitos, Correntes, Dimensionamento, Unifilar e Relatório;
- preservar rastreabilidade da norma, versão do catálogo, origem dos dados e decisões do usuário;
- impedir que um catálogo genérico 127/220/380 seja apresentado como se fosse catálogo EDP V9.

Alterar novamente apenas o piso de potência de `BI-127-220`, adicionar opções no JSON genérico ou habilitar todo o `Select` não resolve a causa e pode produzir dimensionamentos eletricamente incoerentes.

---

## 2. Escopo e limites desta análise

### 2.1 Incluído

- comparação do plano anterior com a V9 fornecida;
- análise do domínio genérico de padrão de entrada;
- análise do domínio EDP-SP;
- cálculo de carga instalada, demanda, categoria, corrente e subcategoria;
- interface “Padrão compatível” e componentes adjacentes;
- entrada de cargas em Dependências;
- API, persistência e migração;
- divisão de circuitos, correntes, balanceamento, dimensionamento de condutores;
- proteções e medição do padrão de entrada;
- unifilar, relatório e auditoria;
- plano de implementação, testes e critérios de aceite.

### 2.2 Não incluído

- validação jurídica da norma;
- substituição da análise de um responsável técnico;
- especificação de atendimento subterrâneo, que a própria V9 remete a outro padrão;
- definição arquitetural final, que deve ser ratificada por @architect;
- criação de story, autoridade de @po/@sm;
- decisão de qualidade final, autoridade de @qa;
- implementação de código.

### 2.3 Distinção normativa necessária

A classificação de categoria e padrão de atendimento da distribuidora vem da norma EDP V9. A NBR 5410 permanece aplicável à instalação de baixa tensão a jusante, mas não deve ser usada como fonte para inventar faixas U/D/T ou tensões disponibilizadas pela concessionária.

---

## 3. Fontes analisadas

### 3.1 Fonte normativa

Arquivo:

`Arquivos_Diversos/Norma_EDP/PT.DT.PDN.00068_V9_chunks.json`

O arquivo contém 76 blocos e cobre as páginas 1 a 91. Para este plano, os blocos de maior relevância foram:

| Bloco | Página(s) | Assunto |
|---|---:|---|
| 3 | 3 | objetivo, aplicação, limite de 75 kW e rede aérea |
| 17 | 14 | sistemas estrela 220/127 V e delta 240/120 V |
| 18 | 15 | limite de fornecimento, categorias e início das limitações |
| 19 | 16 | limites por topologia, cargas especiais, categoria superior e bomba de incêndio |
| 20–21 | 17 | materiais, responsabilidades e ramal de conexão |
| 22 | 18 | condutores do ramal de entrada e isolação |
| 23–25 | 19–20 | eletroduto, proteção, medição direta/indireta e proteções internas |
| 26–27 | 21–22 | aterramento e poste |
| 28–33 | 22–27 | carga instalada, demanda, corrente e queda de tensão |
| 34 | 28 | histórico da versão 09 e inclusão de MMGD |
| 36–39 | 30–33 | Tabelas 001 e 002, subcategorias U/D/T e especificações construtivas |

### 3.2 Artefatos do produto

- `docs/stories/story-FORNECIMENTO-SELECAO-01.md`;
- plano anterior apresentado em conversa;
- captura `Screenshot_200.jpg`;
- rota e componentes da tela de Padrão de entrada;
- motores genérico e EDP-SP;
- catálogos genérico, de categorias e de subcategorias;
- serviços consumidores;
- schemas de API e mapeamento Supabase;
- testes de domínio, API e interface.

---

## 4. Requisitos normativos rastreáveis

Os identificadores abaixo são de análise e servem apenas para rastreabilidade deste plano.

| ID | Exigência derivada da V9 | Fonte | Situação atual |
|---|---|---|---|
| EDP-PE-001 | Aplicação a unidade individual, instalação usual e rede aérea secundária EDP-SP | bloco 3, p. 3 | o projeto não registra área de concessão nem tipo de rede |
| EDP-PE-002 | Até 75 kW é baixa tensão; acima disso é primária ou exige estudo específico | blocos 3 e 18, p. 3 e 15 | existe corte acima de 75 kW, mas sem estado distinto para estudo excepcional |
| EDP-PE-003 | Rede estrela com neutro aterrado: 220/127 V | bloco 17, p. 14 | parcialmente representado no módulo EDP |
| EDP-PE-004 | Rede delta com neutro aterrado: 240/120 V | blocos 17–18, p. 14–15 | impossível no tipo `Tensao = 127 | 220 | 380` |
| EDP-PE-005 | Na rede delta, a fase de força deve atender somente cargas trifásicas | bloco 18, p. 15 | não modelado |
| EDP-PE-006 | U = FN, D = FFN, T = FFFN | bloco 18, p. 15 | representado parcialmente |
| EDP-PE-007 | Tipo depende de carga instalada, demanda, tipo de rede e local | bloco 18, p. 15 | o seletor EDP usa carga ativa e flag trifásica; rede/local não existem |
| EDP-PE-008 | Equipamentos devem ser compatíveis com a tensão disponibilizada | bloco 18, p. 15 | há validação parcial, limitada a 127/220/380 |
| EDP-PE-009 | U estrela ou delta para carga instalada até 12 kW | bloco 18, p. 15 | catálogo simplifica para U estrela 127 V |
| EDP-PE-010 | D estrela para carga acima de 12 e até 25 kW | bloco 18, p. 15 | faixa atual usa 12 como pertencente a D |
| EDP-PE-011 | D delta para carga acima de 12 e até 75 kW | bloco 18, p. 15 | inexistente |
| EDP-PE-012 | T estrela para carga acima de 25 e até 75 kW | blocos 18–19, p. 15–16 | faixa atual usa 25 como pertencente a T |
| EDP-PE-013 | T delta para carga acima de 12 e até 75 kW, somente com equipamento trifásico | bloco 19, p. 16 | inexistente; o código força T sem considerar a topologia |
| EDP-PE-014 | Cargas especiais e motores têm limites por categoria | blocos 18–19 e Tabelas 001/002 | catálogo estrutural guarda parte dos dados, mas o seletor não os usa |
| EDP-PE-015 | Valores acima dos limites de raio X, solda ou motor exigem estudo técnico | bloco 19, p. 16 | não existe estado canônico `REQUER_ESTUDO_TECNICO` |
| EDP-PE-016 | Cliente U pode solicitar D, e cliente D pode solicitar T, com possível taxa | bloco 19, p. 16, Nota 03 | o piso genérico de BI foi reduzido a zero, mas sem registrar solicitação, fundamento ou taxa |
| EDP-PE-017 | Bomba de incêndio deriva antes da chave geral, após medição, com proteção independente | bloco 19, p. 16 | não associado ao padrão de entrada |
| EDP-PE-018 | U, D2 e T2 têm responsabilidade diferenciada no ramal | blocos 20–22, p. 17–18 | o contrato reduzido não expõe essa consequência |
| EDP-PE-019 | Condutor de entrada varia com categoria e isolação PVC ou EPR/XLPE | bloco 22, p. 18 e Tabelas 001/002 | catálogo possui valores, mas o runtime reduz a apenas uma seção |
| EDP-PE-020 | Queda entre ponto de conexão e medição limitada a 1% | bloco 22, p. 18 | não está consolidada no resultado do padrão |
| EDP-PE-021 | Proteção principal e eletroduto seguem Tabelas 001/002 | blocos 23–24, p. 19 | dados existem no catálogo estrutural, mas não no contrato final |
| EDP-PE-022 | Medição direta até 150 A; indireta acima de 150 A | bloco 25, p. 20 e Tabelas 001/002 | catálogo contém a modalidade; contrato final não a expõe |
| EDP-PE-023 | Corrente acima de 150 A exige responsabilidade técnica | bloco 17, p. 14 e bloco 25, p. 20 | há aviso de corrente, mas não uma exigência documental consolidada |
| EDP-PE-024 | Aterramento e poste dependem da categoria/subcategoria | blocos 26–27, p. 21–22 | dados existem parcialmente e não são propagados |
| EDP-PE-025 | Dimensionamento do padrão parte de carga instalada, demanda e corrente | bloco 28, p. 22–23 | dois motores usam grandezas e fatores diferentes |
| EDP-PE-026 | Demanda total é a soma dos grupos a até i | bloco 29, p. 23 | estrutura EDP implementada |
| EDP-PE-027 | Grupo A usa carga instalada em kW para selecionar a Tabela 005 | blocos 29–30, p. 23–24 | o índice atual usa soma aparente em VA dividida por 1000 |
| EDP-PE-028 | MMGD dimensiona proteção pela maior corrente entre geração e carga instalada | blocos 34, 36 e 38 | catálogo tem alerta, mas o produto não possui entrada canônica de geração |
| EDP-PE-029 | A versão e a fonte normativa devem permanecer identificáveis | cabeçalho e histórico V9 | há fontes em JSON, porém o padrão persistido não possui versão/schema/proveniência completa |

---

## 5. Revisão crítica do plano anterior

### 5.1 Pontos que permanecem válidos

- separar catálogo genérico de catálogo da EDP;
- usar os dados EDP na rota identificada como “EDP São Paulo”;
- exibir motivo de incompatibilidade por opção;
- migrar configurações legadas;
- adicionar testes de fronteira e integração;
- não alterar silenciosamente as tensões cadastradas nas cargas.

### 5.2 Pontos que precisam ser corrigidos

#### A. U/D/T não são três faixas lineares universais

O plano anterior tratava:

- U: 0–12 kW;
- D: 12–25 kW;
- T: 25–75 kW.

Isso só aproxima parte do atendimento em estrela. A V9 possui regras diferentes em estrela e delta:

| Topologia | Categoria | Faixa textual V9 | Condição adicional |
|---|---|---:|---|
| estrela 220/127 | U | até 12 kW | FN |
| estrela 220/127 | D | acima de 12 até 25 kW | FFN |
| estrela 220/127 | T | acima de 25 até 75 kW | FFFN |
| delta 240/120 | U | até 12 kW | FN |
| delta 240/120 | D | acima de 12 até 75 kW | FFN |
| delta 240/120 | T | acima de 12 até 75 kW | FFFN e existência de equipamento trifásico |

Consequência: o catálogo atual, que exige continuidade sem sobreposição entre três faixas, não consegue representar a V9.

#### B. As fronteiras 12 kW e 25 kW estão invertidas no código

O texto da V9 usa:

- U: “até 12 kW”;
- D estrela: “acima de 12 kW até 25 kW”;
- T estrela: “acima de 25 kW até 75 kW”.

Logo, pela leitura textual:

- exatamente 12 kW pertence a U;
- exatamente 25 kW pertence a D no sistema estrela.

Os testes atuais exigem 12 → D e 25 → T. Essa divergência deve ser corrigida ou formalmente justificada por interpretação técnica documentada antes da implementação.

#### C. Reduzir o piso de BI para 0 kVA não é uma regra normativa

A alteração de `BI-127-220.potencia_min_kVA` para zero removeu o bloqueio do cenário visual, mas representa de forma incompleta a Nota 03.

Para carga que seria U e necessita atendimento D, a V9 admite uma **solicitação de categoria superior**, sujeita à decisão da concessionária e possível taxa. Isso não equivale a declarar que toda carga abaixo de 12 kW é automaticamente D.

O sistema deve distinguir:

- categoria mínima calculada;
- categoria superior elegível por solicitação;
- categoria efetivamente escolhida/solicitada;
- confirmação ou pendência de atendimento pela concessionária.

#### D. O catálogo genérico 220/380 V não é catálogo EDP-SP V9

O item genérico `TRI-220-380` não representa os sistemas 220/127 e 240/120 descritos pela V9. Mantê-lo visível na tela EDP cria uma opção tecnicamente enganosa.

#### E. Categoria não é sinônimo de padrão físico

U, D e T definem modalidade elétrica. U2, D2, D4, D6, D7, D9, D10, T2, T4, T6, T7, T9 e T10 definem degraus construtivos/protetivos. A escolha apresentada ao usuário deve deixar claro:

1. topologia/tensão da rede;
2. categoria calculada;
3. eventual categoria superior solicitada;
4. subcategoria determinada pela corrente;
5. especificação física resultante.

### 5.3 Pontos ausentes no plano anterior

- rede estrela versus delta;
- tensões 120 e 240 V;
- escopo rede aérea versus subterrânea;
- localização/área de concessão;
- regra da fase de força no delta;
- limitações de raio X, solda, motores e bomba de incêndio;
- medição direta/indireta;
- caixa, poste, eletroduto, aterramento e responsabilidade pelo ramal;
- requisito documental acima de 150 A;
- MMGD;
- inconsistência entre o motor genérico e o EDP;
- divergência entre os consumidores downstream;
- erro no índice em kW do grupo A;
- migração com versão e proveniência;
- estados `DADOS_INCOMPLETOS`, `REQUER_ESTUDO` e `FORA_DE_ESCOPO`.

### 5.4 Reavaliação da story anterior

`docs/stories/story-FORNECIMENTO-SELECAO-01.md` foi concluída com as premissas de que:

- as opções deveriam vir do catálogo do projeto;
- padrões incompatíveis não poderiam ser salvos;
- Correntes deveria consumir o contrato genérico selecionado;
- não seria criado um catálogo de distribuidora novo.

Essas premissas eram coerentes com o escopo declarado daquela story, mas não são suficientes para a rota EDP-SP após a comparação com a V9:

- o “catálogo do projeto” é o catálogo genérico, cuja própria fonte manda verificar os limites da distribuidora;
- a story tornou o contrato genérico canônico para Correntes, enquanto Divisão de circuitos permaneceu no contrato EDP;
- impedir o salvamento de incompatíveis não resolve a ausência de um candidato EDP corretamente modelado;
- a restrição “não criar catálogo de distribuidora” deve ser revista em nova story, pois o produto já possui um módulo e catálogos EDP, mas a tela não os usa como fonte da escolha;
- o critério “pendência desaparece quando o padrão cobre as cargas” precisa incluir categoria superior solicitada, topologia e confirmação da concessionária.

Portanto, a story anterior não deve ser editada retroativamente. Ela deve permanecer como registro histórico e ser sucedida pelas stories propostas neste plano.

---

## 6. Diagnóstico do sistema atual

### 6.1 Fluxo existente

```text
Dependências e cargas
        |
        +--> motor genérico --------------------> resultado genérico
        |       catálogo 127/220/380                  |
        |                                             +--> FornecimentoSelector
        |                                             +--> Correntes
        |                                             +--> Dimensionamento
        |                                             +--> Unifilar
        |
        +--> adaptador + motor EDP -------------> resultado EDP
                grupos a-i, U/D/T, subcategoria       |
                                                      +--> cards EDP
                                                      +--> Divisão de circuitos
                                                      +--> parte do Relatório
```

Há duas linhas de cálculo para o mesmo conceito e elas não convergem em um contrato canônico.

### 6.2 Causa imediata do combo totalmente desabilitado

Em `src/components/app/FornecimentoSelector.tsx:24-26`:

```ts
new Set(resultado.status === "ok"
  ? resultado.candidatosValidos.map((p) => p.id)
  : [])
```

Quando o resultado é `sem-padrao`, o conjunto é vazio. Como cada item do catálogo é habilitado somente se seu ID estiver nesse conjunto, todas as opções ficam desabilitadas.

Esse desenho é circular:

1. o motor não encontra padrão;
2. a interface conclui que não há IDs selecionáveis;
3. o usuário não consegue escolher uma alternativa;
4. o estado não pode ser resolvido pela própria interface.

### 6.3 Fonte de dados incorreta no componente

`FornecimentoSelector` recebe:

- `estado.resultado`, calculado pelo motor genérico;
- `estado.config.catalogo`, catálogo genérico persistido no projeto.

A mesma rota, logo abaixo, renderiza:

- `estado.edpSp.resultado`;
- `estado.edpSp.parametros`;
- `estado.edpSp.contratos`.

Assim, o campo principal da tela EDP não usa o resultado EDP exibido no restante da página.

### 6.4 Catálogo genérico incompatível com a finalidade da tela

`src/domain/nbr/catalogo-fornecimento.data.json` declara explicitamente:

> “Catálogo de padrões de entrada (genérico/parametrizável) — VERIFICAR limites contra norma da distribuidora local”.

Opções atuais:

- `MONO-127`;
- `MONO-220`;
- `BI-127-220`;
- `TRI-220-380`.

Esse catálogo:

- não representa estrela/delta;
- não representa 120/240 V;
- contém 380 V, ausente nos sistemas da V9;
- usa faixa em kVA demandada, enquanto a categoria EDP usa carga instalada em kW e a subcategoria usa corrente de demanda;
- não representa atendimento superior solicitado;
- não representa subcategorias físicas.

### 6.5 Modelo de tensão insuficiente

`src/domain/modelo/padrao-fornecimento.ts:7`:

```ts
export type Tensao = 127 | 220 | 380;
```

`src/api/schemas/padrao-entrada.ts:3` repete a mesma união.

O modelo não aceita 120 V nem 240 V. Consequentemente, não é possível implementar integralmente o sistema delta da V9 sem alterar domínio, schemas, persistência, modais de carga, circuitos, testes e consumidores.

### 6.6 Categorias EDP simplificadas indevidamente

`src/domain/distribuidora/edp-sp/categorias-fornecimento.data.json` contém apenas:

- U estrela 127 V, 0–12;
- D estrela 127/220 V, 12–25;
- T estrela 127/220 V, 25–75.

Além de omitir delta, `categorias-fornecimento.ts:98-107` obriga um catálogo linear, contínuo e sem sobreposição. A regra impede representar D delta e T delta, que ocupam faixas associadas a condições distintas.

### 6.7 Seletor de categoria incompleto

`seletor-categoria.ts`:

- seleciona por carga instalada ativa;
- força T quando existe carga trifásica;
- não recebe topologia da rede;
- não recebe localização;
- não distingue categoria mínima e solicitação superior;
- não avalia cargas especiais;
- não produz uma lista de candidatos com motivos.

O próprio comentário do arquivo reconhece que se trata de “primeira aproximação”.

### 6.8 Divergência no cálculo do grupo A

`motor-demanda.ts:93-103` informa que a Tabela 005 é indexada por `kw_instalado`, mas calcula:

```ts
const soma_armazenada_VA = ...
const indice_kW = soma_armazenada_VA / 1000;
```

O sistema possui a função `ativa(c) = VA × FP`, usada no total de carga instalada ativa, mas não a utiliza para o índice do grupo A.

Isso pode selecionar um fator de demanda diferente do fator correspondente à carga instalada em kW indicada pela V9.

### 6.9 Subcategoria estrutural reduzida no runtime

O arquivo `subcategorias-fornecimento.catalogo.data.json` já contém:

- sistema e número de fases;
- corrente/disjuntor;
- fusível e chave;
- medição direta/indireta;
- condutores PVC e EPR/XLPE;
- caixa;
- eletroduto;
- poste/PCI;
- aterramento;
- limites de motor;
- alertas.

Porém, `carregarSubcategorias()` reduz cada linha a:

- ID;
- categoria;
- corrente máxima;
- disjuntor;
- uma seção EPR/XLPE;
- status.

O contrato EDP final perde a maior parte da especificação que depende da escolha do padrão.

### 6.10 Semântica incorreta de `IB ≤ In ≤ Iz` na seleção da tabela EDP

`seletor-subcategoria.ts:85-87` trata `corrente_demanda_max_A` como `Iz`.

Nas Tabelas 001/002, o degrau é identificado pela proteção e pela especificação prescritiva do padrão. O limite de corrente da linha não deve ser renomeado implicitamente como capacidade de condução `Iz` do condutor sem rastreio do método/temperatura/agrupamento.

A coordenação NBR `IB ≤ In ≤ Iz` continua necessária no dimensionamento, mas deve usar a ampacidade efetivamente calculada, não um alias da corrente nominal da subcategoria.

### 6.11 Duas fontes de verdade downstream

#### Divisão de circuitos

`servico-divisao-circuitos.ts:25-37` usa:

```ts
telaPadrao.edpSp?.contratos.saidaA
```

#### Correntes

`servico-corrente.ts:270-296` usa:

```ts
tela.contratos
```

Esse é o contrato do motor genérico. A função `fonteDivisaoDeSaidaA()` ainda presume que:

- primeira tensão = fase-neutro;
- segunda tensão = fase-fase.

Para `TRI-220-380`, isso gera FN 220 V e FF 380 V, incompatível com o sistema estrela 220/127 V da EDP.

#### Dimensionamento e unifilar

- Dimensionamento consome Correntes;
- Unifilar consome Correntes e resultados de Dimensionamento;
- Relatório publica simultaneamente contratos genérico e EDP.

Logo, o padrão escolhido pode aparecer correto em um card EDP e produzir circuitos, correntes, fases e seções a partir de outro padrão.

### 6.12 Persistência fragmentada

Existem pelo menos duas persistências:

1. `projetos.padrao_entrada_config`, com catálogo genérico, override, isolação, balanceamento e divisão manual;
2. `parametros_edp_overrides`, com alterações do catálogo EDP.

Problemas:

- o catálogo genérico inteiro fica copiado em cada projeto;
- não há versão de schema da configuração;
- não há um ID canônico do sistema de rede EDP;
- não há categoria calculada versus solicitada;
- não há motivo/proveniência da seleção;
- não há status de confirmação da concessionária;
- alterações manuais recebem `status_verificacao: "VERIFICADO"`, mesmo sendo overrides de usuário;
- configurações de domínios diferentes estão agrupadas no mesmo objeto.

### 6.13 Testes que cristalizam divergências

- `seletor-categoria.test.ts` exige 12 → D e 25 → T;
- `seletor-subcategoria.test.ts` usa 380 V no caso trifásico EDP;
- testes de API validam simultaneamente contratos genérico e EDP, sem exigir igualdade semântica;
- não há teste ponta a ponta garantindo que Padrão de entrada, Correntes, Dimensionamento, Unifilar e Relatório usem o mesmo sistema;
- não há teste de rede delta;
- não há teste de solicitação de categoria superior;
- não há teste das restrições de cargas especiais;
- não há teste de migração que impeça reinterpretar `TRI-220-380` como EDP.

### 6.14 Findings priorizados

| Finding | Severidade | Evidência | Efeito |
|---|---|---|---|
| F-01 — duas fontes canônicas | crítica | `servico-divisao-circuitos` usa EDP; `servico-corrente` usa genérico | tensões e fases divergentes no mesmo projeto |
| F-02 — catálogo errado no campo EDP | crítica | `FornecimentoSelector` usa `estado.config.catalogo` | opção apresentada não corresponde à V9 |
| F-03 — dead-end da interface | alta | conjunto válido vazio quando `status !== ok` | usuário não consegue resolver a pendência |
| F-04 — delta não representável | crítica | `Tensao` aceita apenas 127/220/380 | cobertura normativa incompleta |
| F-05 — categoria linear | alta | catálogo exige faixas contínuas U/D/T | D/T delta não podem coexistir |
| F-06 — fronteiras divergentes | alta | testes 12 → D e 25 → T | categoria incorreta nos limites |
| F-07 — índice do grupo A em kVA | alta | soma VA/1000 usada como kW | fator de demanda potencialmente incorreto |
| F-08 — solicitação superior mascarada | alta | BI com piso zero | decisão do cliente vira enquadramento automático |
| F-09 — contrato estrutural incompleto | alta | campos da tabela descartados no runtime | padrão físico e relatório incompletos |
| F-10 — override vira verificado | alta | merge define `VERIFICADO` | perda de proveniência normativa |
| F-11 — migração sem versão | alta | JSON de projeto sem schema normativo | atualização pode reinterpretar dados |
| F-12 — lacunas especiais/MMGD | alta quando aplicável | alertas não entram no avaliador | falsa conclusão de compatibilidade |

---

## 7. Modelo funcional proposto

### 7.1 Separar os conceitos

| Conceito | Exemplo | Origem |
|---|---|---|
| distribuidora/norma | EDP-SP / PT.DT.PDN.00068 V9 | contexto do projeto |
| tipo de rede | aérea ou subterrânea | dados do atendimento |
| topologia | estrela com neutro / delta com neutro | rede disponível no local |
| tensões nominais | 220/127 ou 240/120 V | topologia |
| categoria mínima | U, D ou T | carga, demanda, rede, local e cargas especiais |
| categoria solicitada | D em vez de U; T em vez de D | decisão explícita do cliente, Nota 03 |
| subcategoria | D4, T6 etc. | corrente e Tabelas 001/002 |
| padrão físico | proteção, medição, cabos, caixa, eletroduto, poste, terra | subcategoria + isolação |
| estado regulatório | compatível, estudo, fora de escopo, pendente | avaliação completa |

### 7.2 Estados mínimos de um candidato

Cada opção avaliada deve retornar um estado tipado e motivos estruturados:

| Estado | Uso |
|---|---|
| `DETERMINADO` | opção mínima resultante das regras disponíveis |
| `ELEGIVEL_POR_SOLICITACAO` | categoria superior admitida pela Nota 03 |
| `INCOMPATIVEL` | falha objetiva de tensão, faixa, fases ou carga especial |
| `REQUER_ESTUDO_TECNICO` | excede limite especial ou há situação prevista para análise da EDP |
| `DADOS_REDE_PENDENTES` | não se conhece estrela/delta, rede aérea/subterrânea ou localização |
| `FORA_ESCOPO_REDE_SUBTERRANEA` | requer outro padrão técnico |
| `FORA_ESCOPO_MEDIA_TENSAO` | carga acima de 75 kW sem enquadramento excepcional |
| `CATALOGO_DESATUALIZADO` | norma/configuração persistida incompatível com a versão atual |

O nome final dos enums é decisão de implementação; os significados são requisitos funcionais.

### 7.3 Informações que devem anteceder a seleção

O motor não deve declarar compatibilidade definitiva sem:

- distribuidora/área de concessão;
- tipo de rede de conexão;
- topologia/tensões disponíveis no local;
- carga instalada ativa;
- demanda calculada;
- presença e tensão das cargas mono/bi/trifásicas;
- cargas especiais relevantes;
- presença de MMGD, caso o produto passe a suportá-la.

Se essas informações não existirem, a interface deve apresentar pendência explícita, não uma lista vazia de padrões “incompatíveis”.

### 7.4 Matriz de opções EDP que o catálogo precisa conseguir representar

| Opção lógica | Rede | Tensões | Categoria | Regra base |
|---|---|---|---|---|
| U-ESTRELA | estrela | FN 127 V | U | carga ≤ 12 kW |
| D-ESTRELA | estrela | FN 127 / FF 220 V | D | 12 < carga ≤ 25 kW |
| T-ESTRELA | estrela | FN 127 / FF 220 V | T | 25 < carga ≤ 75 kW |
| U-DELTA | delta | FN 120 V | U | carga ≤ 12 kW |
| D-DELTA | delta | FN 120 / FF 240 V | D | 12 < carga ≤ 75 kW |
| T-DELTA | delta | 120/240 V | T | 12 < carga ≤ 75 kW e carga trifásica |

Além dessas regras base, o avaliador deve gerar as alternativas superiores permitidas pela Nota 03.

Casos de equipamento trifásico com carga igual ou inferior a 12 kW, ou trifásico em estrela com carga igual ou inferior a 25 kW, não devem ser resolvidos por inferência silenciosa. A tabela textual não os enquadra diretamente nas faixas T correspondentes; o comportamento deve ser confirmado com responsável técnico/EDP e, até lá, classificado como pendência ou estudo.

### 7.5 Seleção em duas etapas

Para reduzir ambiguidade:

1. **Fornecimento disponível no local:** rede, topologia e tensões;
2. **Padrão de atendimento do projeto:** categoria mínima/solicitada e subcategoria calculada.

Se o produto optar por um único campo visual, cada opção deve carregar todas essas dimensões e exibi-las no rótulo.

Exemplo de rótulo informativo:

`D4 — Categoria D, estrela 220/127 V, medição direta, disjuntor 100 A`

Não usar somente `BI-127-220 — compatível`.

### 7.6 Fonte canônica

Para projetos EDP-SP, deve existir um único resultado canônico de padrão de entrada, consumido por todos os módulos. Conceitualmente, ele deve conter:

- fonte e versão normativa;
- versão do schema do resultado;
- escopo do atendimento;
- topologia e tensões;
- carga instalada kW/kVA e demanda VA;
- categoria mínima;
- categoria solicitada/selecionada;
- fundamento da seleção;
- corrente de demanda e fórmula;
- subcategoria;
- especificação estrutural completa;
- diagnósticos e pendências;
- assinatura/hash das entradas relevantes, se o projeto já adotar esse mecanismo;
- timestamp/autoria da escolha manual.

A forma final do contrato deve ser ratificada por @architect antes de o @dev migrar consumidores.

---

## 8. Reestruturação do campo “Padrão compatível”

### 8.1 Regras de apresentação

- não montar opções a partir de `estado.config.catalogo` na rota EDP;
- não condicionar a existência de candidatos a `resultado.status === "ok"`;
- renderizar todas as alternativas avaliadas pelo motor EDP;
- para cada alternativa, exibir estado e motivo;
- ordenar:
  1. determinado;
  2. elegível por solicitação;
  3. requer estudo;
  4. incompatível;
- mostrar a norma e versão usadas;
- exibir separadamente categoria mínima e opção solicitada;
- não permitir salvar candidato incompatível;
- permitir avançar para fluxo de estudo somente como pendência, nunca como “compatível”;
- se faltar topologia/rede, solicitar o dado antes da seleção definitiva;
- se não houver opção automática, apresentar ação e diagnóstico, não um combo morto.

### 8.2 Razões de incompatibilidade

O usuário deve receber motivos concretos, por exemplo:

- “A rede selecionada é delta 240/120 V; esta opção é de rede estrela 220/127 V”;
- “A carga instalada de 31,2 kW excede o limite de D em estrela (25 kW)”;
- “Existe carga fixa de 220 V, indisponível no atendimento U”;
- “Categoria U não admite a carga especial cadastrada”;
- “A corrente de demanda excede D10”;
- “Atendimento acima do limite exige estudo técnico da EDP”;
- “A rede subterrânea não é coberta pela PT.DT.PDN.00068 V9”;
- “Topologia da rede ainda não informada”.

### 8.3 Comportamento de salvamento

Ao salvar:

- persistir somente a decisão do usuário e sua proveniência, não uma cópia mutável do catálogo oficial;
- registrar se é categoria mínima ou solicitação superior;
- guardar norma/versão usadas na decisão;
- recalcular o resultado canônico;
- invalidar Padrão de entrada, Divisão, Correntes, Dimensionamento, Unifilar e Relatório;
- registrar auditoria;
- rejeitar no servidor uma opção cujo status atual não permita seleção;
- detectar alteração das cargas entre exibição e salvamento e exigir novo cálculo.

---

## 9. Seções e módulos associados

### 9.1 Dependências e cargas adicionais

Arquivos principais:

- `NovaDependenciaModal.tsx`;
- `EditarDependenciaModal.tsx`;
- `TabelaDependencias.tsx`;
- `adaptador-projeto.ts`;
- modelo e schema de `CargaAdicional`.

Impactos:

- opções de tensão devem vir do fornecimento disponível, não ficar limitadas/hardcoded em 127 e 220;
- carga trifásica não pode forçar sempre 220 V;
- rede delta exige 120/240 V e regra da fase de força;
- fallback “sem tensão” deve ser topologia-aware;
- mudanças de potência, FP, quantidade, tensão, tipo e trifasicidade devem invalidar a seleção;
- cargas especiais precisam de classificação suficiente para as limitações EDP;
- a escolha de padrão não pode alterar silenciosamente a tensão fixa da carga.

### 9.2 Demanda por grupos EDP

Arquivos:

- `motor-demanda.ts`;
- `fatores-demanda.ts`;
- `adaptador-projeto.ts`;
- `DemandaPorGrupoEDPCard.tsx`.

Correções:

- usar kW ativo no índice da Tabela 005;
- manter separação entre VA aparente, W/kW ativo e FP;
- validar unidades e nomes dos campos (`p_nominal_W` hoje armazena VA);
- preservar rastreio do grupo a-i, fator, índice e fonte;
- impedir que carga genericamente classificada como TUE mas pertencente a outro grupo passe sem pendência;
- criar testes de reconciliação: soma de grupos = DT.

### 9.3 Categoria e subcategoria

Arquivos:

- `categorias-fornecimento.data.json`;
- `categorias-fornecimento.ts`;
- `seletor-categoria.ts`;
- `motor-edp-sp.ts`;
- `seletor-subcategoria.ts`;
- `CategoriaSubcategoriaCard.tsx`.

Correções:

- substituir o catálogo linear por regras condicionais por topologia;
- corrigir fronteiras;
- separar seleção mínima de solicitação superior;
- avaliar cargas especiais;
- selecionar subcategoria pela corrente e pelo conjunto de linhas aplicável;
- não chamar corrente de linha de `Iz`;
- expor a especificação estrutural completa.

### 9.4 Parâmetros EDP por projeto

Arquivos:

- `parametros.ts`;
- `ParametrosEDPEditor.tsx`;
- schema/serviço/repositório de parâmetros EDP.

Correções:

- usuário não deve transformar override em dado “VERIFICADO”;
- fonte oficial e override devem ter proveniências diferentes;
- não permitir editar livremente tensões/faixas normativas sem perfil e justificativa definidos pelo produto;
- validar topologia e condições, não continuidade linear;
- versionar overrides e detectar incompatibilidade após atualização normativa;
- separar parametrização técnica legítima de seleção do usuário final.

### 9.5 Condutor e isolação do ramal de entrada

Arquivos:

- `CondutorIsolacaoCard.tsx`;
- catálogo estrutural;
- contratos EDP.

Correções:

- selecionar a seção correspondente à isolação escolhida;
- expor PVC e EPR/XLPE sem reduzir um deles;
- informar responsabilidade do fornecimento para U, D2 e T2;
- associar caixa, eletroduto, poste e aterramento;
- manter essa especificação separada do dimensionamento de circuitos terminais.

### 9.6 Proteção e medição

Correções:

- propagar disjuntor, fusível/chave e modalidade de medição;
- exigir pendência documental acima de 150 A;
- associar proteção à subcategoria;
- manter proteções internas NBR 5410 em módulo próprio;
- incluir tratamento especial da bomba de incêndio;
- não confundir proteção do padrão de entrada com proteção de cada circuito.

### 9.7 Divisão de circuitos

Arquivo:

- `servico-divisao-circuitos.ts`.

Correções:

- continuar recebendo o contrato canônico EDP, mas pelo mesmo ponto de acesso usado por Correntes;
- resolver tensão FN/FF conforme topologia;
- respeitar a restrição da fase de força no delta;
- invalidar divisões manuais que se tornarem impossíveis após troca do padrão;
- preservar divisões manuais ainda válidas.

### 9.8 Correntes e balanceamento

Arquivos:

- `servico-corrente.ts`;
- `corrente-circuitos.ts`;
- `balanceamento-fases.ts`;
- rota de Correntes.

Correções:

- remover dependência do contrato genérico na rota EDP;
- não adaptar arrays por posição para inferir FN/FF;
- usar propriedades nomeadas do contrato canônico;
- calcular tipo de ligação e IB com a tensão efetiva;
- representar neutro corretamente por circuito;
- recalcular balanceamento quando categoria/topologia mudar;
- bloquear Correntes quando o padrão estiver pendente, sem usar fallback genérico oculto.

### 9.9 Dimensionamento de condutores e critérios C1–C6

Arquivos:

- `servico-dimensionamento-condutores.ts`;
- adaptadores e contratos de MOD-DC;
- tela de Dimensionamento.

Impactos:

- tensão altera IB e queda de tensão;
- número de fases altera fórmula e distribuição;
- presença de neutro altera condutores;
- padrão escolhido deve invalidar resultados e overrides incompatíveis;
- seções do ramal de entrada EDP não podem ser misturadas com seções de circuitos terminais;
- o critério C1 anteriormente pendente pode permanecer incorreto se receber corrente derivada do padrão genérico.

### 9.10 Queda de tensão

Devem permanecer distintos:

- limite EDP entre ponto de conexão e medição;
- limite NBR 5410 dos circuitos internos.

O padrão deve fornecer topologia, tensão e especificação do ramal para o cálculo EDP. MOD-QT deve continuar responsável pelos circuitos internos.

### 9.11 Aterramento

O catálogo estrutural deve propagar:

- seção para PVC;
- seção para EPR/XLPE;
- eletroduto de aterramento;
- referência à categoria.

O esquema TT/TN/IT da instalação interna não deve ser inferido apenas da topologia de fornecimento da concessionária.

### 9.12 Unifilar e exportações

Arquivos:

- rotas `unifilar` e `unifilar-diagrama`;
- `montar-unifilar-graph.ts`;
- serialização e renderizadores/exportadores.

Correções:

- incluir origem do barramento, topologia, tensões FN/FF, categoria e subcategoria;
- usar circuitos calculados pelo contrato canônico;
- invalidar/regenerar após mudança de padrão;
- marcar o diagrama como pendente quando a seleção não estiver confirmada;
- não exibir 380 V em um projeto EDP-SP V9, salvo contexto de outro fornecimento explicitamente separado.

### 9.13 Relatório técnico

`servico-relatorio-projeto.ts` publica hoje:

- contrato genérico;
- contrato EDP;
- correntes derivadas do genérico.

Correções:

- publicar um único padrão canônico;
- incluir fonte/versão, topologia, categoria mínima/solicitada, subcategoria e especificação;
- declarar pendências e estudos;
- garantir que correntes e circuitos reportados usem o mesmo padrão;
- manter diagnóstico de migração/configuração legada;
- incluir requisitos documentais e responsabilidade por materiais quando aplicável.

### 9.14 Auditoria e histórico

Registrar:

- cálculo automático;
- seleção ou solicitação manual;
- justificativa;
- usuário/data;
- norma e catálogo;
- conjunto de entradas;
- valor anterior e novo;
- motivo de invalidação;
- eventual confirmação da concessionária, se esse fluxo existir no produto.

### 9.15 MMGD

O catálogo já contém alerta de MMGD, mas não foi localizada entrada de geração no domínio do projeto.

Até o produto suportar essa informação:

- não declarar a proteção do padrão como completamente verificada quando houver MMGD conhecida;
- criar pendência explícita quando a existência de geração for informada por algum fluxo;
- não implementar fórmula com dado inexistente;
- submeter a expansão do escopo a @po/@architect.

### 9.16 Validação, recálculo e conformidade

Arquivos:

- `src/domain/servicos/servico-validacao.ts`;
- `src/domain/servicos/servico-recalculo.ts`;
- validações de conformidade NBR 5410;
- diagnósticos de tensão pendente.

Correções:

- incorporar pendências do padrão canônico na prontidão do projeto;
- distinguir “tensão da carga não confirmada” de “tensão indisponível na rede”;
- bloquear recálculo downstream quando a decisão efetiva estiver obsoleta;
- recalcular automaticamente a avaliação de candidatos após alteração de carga;
- não declarar conformidade global quando padrão, medição ou estudo técnico estiverem pendentes;
- manter a conformidade NBR interna separada da conformidade do atendimento EDP.

### 9.17 APIs, cache e navegação

Arquivos:

- rotas API de padrão de entrada e parâmetros EDP;
- `src/lib/api-client.ts`;
- `src/hooks/queries.ts`;
- navegação do projeto e estados de prontidão.

Correções:

- retornar candidatos avaliados e razões pela API;
- validar a seleção no servidor contra a versão atual das entradas;
- incluir versão/ETag ou mecanismo equivalente para impedir salvamento sobre cálculo obsoleto;
- invalidar explicitamente as queries de:
  - padrão de entrada;
  - divisão de circuitos;
  - correntes;
  - dimensionamento e otimização;
  - unifilar;
  - relatório;
- mostrar no menu/status do projeto quando o padrão estiver pendente ou obsoleto;
- manter tratamento de erro consistente entre CLI, API e UI.

---

## 10. Plano de execução para @dev

Pela Constitution, cada pacote abaixo precisa ser convertido em story por @po/@sm antes de implementação. Mudanças de contrato entre módulos exigem validação de @architect.

### Fase 0 — Decisões e baseline

1. Criar stories com critérios deste documento.
2. Ratificar com @architect a fonte canônica e a separação entre catálogo genérico e EDP.
3. Confirmar com responsável técnico:
   - fronteiras exatas de 12 e 25 kW;
   - tratamento de carga trifásica abaixo das faixas T;
   - disponibilidade da topologia da rede no fluxo do produto;
   - interpretação dos degraus de corrente das Tabelas 001/002.
4. Registrar o cenário da captura como fixture de regressão.
5. Capturar resultados atuais dos módulos para comparação.

**Saída:** decisões documentadas, stories criadas e baseline reproduzível.

### Fase 1 — Modelo normativo e catálogo

1. Criar modelo explícito de:
   - distribuidora/norma;
   - tipo de rede;
   - topologia;
   - tensões FN/FF;
   - categoria mínima e solicitada;
   - subcategoria;
   - estados de avaliação.
2. Ampliar o tipo de tensão sem contaminar catálogos de outras distribuidoras.
3. Reestruturar categorias EDP para regras condicionais.
4. Manter Tabelas 001/002 como catálogo oficial versionado e imutável em runtime.
5. Preservar todos os campos estruturais.
6. Separar proveniência oficial de override.
7. Adicionar validação de consistência do catálogo.

**Saída:** domínio capaz de representar toda a matriz da V9.

### Fase 2 — Motor de avaliação de candidatos

1. Corrigir índice do grupo A.
2. Calcular categoria mínima por topologia e faixa correta.
3. Gerar alternativas superiores da Nota 03.
4. Avaliar tensão e fases de todas as cargas.
5. Avaliar limitações de cargas especiais e motores.
6. Calcular corrente conforme o sistema.
7. Selecionar subcategoria e especificação estrutural.
8. Produzir lista de candidatos com status e razões.
9. Produzir estados para rede/dados pendentes, estudo e fora de escopo.
10. Não selecionar automaticamente uma opção que dependa de solicitação do cliente.

**Saída:** função pura e testável, independente da UI.

### Fase 3 — Contrato canônico e convergência dos consumidores

1. Definir o contrato canônico validado por @architect.
2. Fazer `servicoPadraoEntrada` expor uma única decisão efetiva para projetos EDP.
3. Migrar Divisão de circuitos.
4. Migrar Correntes.
5. Migrar Balanceamento.
6. Migrar Dimensionamento.
7. Migrar Unifilar.
8. Migrar Relatório.
9. Remover adaptações posicionais de arrays de tensão.
10. Manter o resultado genérico somente em contexto genérico explicitamente separado.

**Saída:** todos os módulos usam o mesmo sistema, tensões e padrão.

### Fase 4 — API e persistência

1. Versionar o schema da configuração.
2. Persistir referência ao catálogo, não cópia oficial mutável.
3. Persistir topologia/rede e decisão do usuário.
4. Persistir categoria mínima versus solicitada.
5. Persistir proveniência e auditoria.
6. Validar no servidor o candidato selecionado.
7. Implementar controle de configuração obsoleta.
8. Separar configurações não relacionadas, conforme decisão arquitetural.

**Saída:** configuração rastreável e segura contra atualização normativa.

### Fase 5 — Migração de projetos existentes

1. Ler configurações legadas sem destruí-las.
2. Classificar cada seleção:
   - mapeável com segurança;
   - exige topologia;
   - incompatível com V9;
   - catálogo customizado;
   - seleção ausente.
3. Não mapear automaticamente `TRI-220-380` para EDP.
4. Não transformar `BI-127-220` de piso zero em categoria mínima; reconhecer possível solicitação superior.
5. Marcar projeto para revisão quando não houver equivalência inequívoca.
6. Registrar migração e versão anterior.
7. Disponibilizar relatório de migração via CLI antes da UI, conforme Constitution.

**Saída:** projetos preservados e sem reinterpretação silenciosa.

### Fase 6 — Interface

1. Substituir `FornecimentoSelector` por componente orientado à avaliação EDP.
2. Incluir coleta/pendência de rede e topologia.
3. Exibir categoria mínima, alternativas e motivos.
4. Exibir subcategoria e consequências construtivas.
5. Implementar confirmação para solicitação superior.
6. Exibir estudo/fora de escopo sem habilitar como compatível.
7. Incluir estados de carregamento, erro e configuração obsoleta.
8. Invalidar todas as queries dependentes.
9. Atualizar Dependências para tensões do fornecimento.

**Saída:** campo acionável, explicável e sem dead-end.

### Fase 7 — Relatório, unifilar e rastreabilidade

1. Atualizar payloads.
2. Mostrar uma única fonte canônica.
3. Exibir norma, topologia, categoria, subcategoria e especificação.
4. Atualizar unifilar e exportações.
5. Exibir pendências e estudos.
6. Garantir consistência por assinatura das entradas ou mecanismo equivalente já adotado.

**Saída:** documentos coerentes com o cálculo.

### Fase 8 — Remoção controlada do legado

1. Medir projetos ainda dependentes do catálogo genérico.
2. Remover o seletor genérico da rota EDP.
3. Remover contratos duplicados dos relatórios EDP.
4. Manter catálogo genérico somente se existir requisito explícito para outra distribuidora/modo.
5. Remover normalizadores temporários após concluir a migração.

**Saída:** ausência de dupla fonte de verdade.

---

## 11. Critérios de aceite

### Campo e candidatos

- **AC-01:** em estado sem candidato automaticamente compatível, o campo não fica com todas as opções mudas; mostra alternativas avaliadas e motivos.
- **AC-02:** nenhuma opção da tela EDP é carregada do catálogo genérico 127/220/380.
- **AC-03:** toda opção exibe topologia, tensões, categoria e subcategoria quando disponível.
- **AC-04:** opção incompatível não pode ser salva no cliente nem na API.
- **AC-05:** opção que requer estudo não é rotulada como compatível.
- **AC-06:** categoria superior exige ação explícita e registra que decorre da Nota 03.
- **AC-07:** ausência de dados de rede gera pendência acionável.

### Norma e cálculo

- **AC-08:** estrela 220/127 e delta 240/120 são representáveis.
- **AC-09:** exatamente 12 e 25 kW seguem a interpretação normativa aprovada.
- **AC-10:** D delta e T delta seguem condições distintas.
- **AC-11:** carga acima de 75 kW não recebe padrão BT automático.
- **AC-12:** cargas especiais produzem bloqueio ou estudo conforme limites.
- **AC-13:** Tabela 005 é indexada por kW ativo.
- **AC-14:** DT reconcilia com a soma dos grupos a-i.
- **AC-15:** corrente e subcategoria registram fórmula e entradas.

### Consistência sistêmica

- **AC-16:** Padrão de entrada, Divisão, Correntes, Dimensionamento, Unifilar e Relatório usam o mesmo contrato.
- **AC-17:** uma troca de padrão invalida todos os resultados dependentes.
- **AC-18:** não aparece 380 V em projeto EDP V9.
- **AC-19:** tensão fixa de carga nunca é alterada pela seleção.
- **AC-20:** circuitos incompatíveis ficam bloqueados com razão, sem fallback.
- **AC-21:** relatório não publica dois padrões concorrentes.

### Persistência e auditoria

- **AC-22:** seleção persiste norma, versão, decisão e proveniência.
- **AC-23:** catálogo oficial não é duplicado como configuração editável em cada projeto.
- **AC-24:** configuração legada não é reinterpretada silenciosamente.
- **AC-25:** atualização normativa marca decisões obsoletas.
- **AC-26:** histórico registra autor, data, valor anterior, novo e justificativa.

### Especificação física

- **AC-27:** subcategoria expõe medição, proteção, condutores, caixa, eletroduto, poste e aterramento.
- **AC-28:** PVC e EPR/XLPE usam as colunas corretas.
- **AC-29:** acima de 150 A gera medição indireta e pendência documental.
- **AC-30:** U/D2/T2 exibem a responsabilidade diferenciada do ramal.

---

## 12. Matriz mínima de testes

### 12.1 Fronteiras de categoria

| Caso | Topologia | Carga | Resultado esperado |
|---|---|---:|---|
| B01 | estrela | 0 kW | U |
| B02 | estrela | 11,999 kW | U |
| B03 | estrela | 12,000 kW | U, salvo decisão técnica diferente documentada |
| B04 | estrela | 12,001 kW | D |
| B05 | estrela | 25,000 kW | D, salvo decisão técnica diferente documentada |
| B06 | estrela | 25,001 kW | T |
| B07 | estrela | 75,000 kW | T |
| B08 | qualquer | 75,001 kW | fora de escopo/estudo |
| B09 | delta | 12,001 kW sem tri | D |
| B10 | delta | 25–75 kW sem tri | D |
| B11 | delta | 12,001–75 kW com tri | T |

### 12.2 Tensões e topologia

- U estrela oferta somente tensão adequada FN 127;
- D/T estrela ofertam FN 127 e FF 220;
- U delta oferta FN 120;
- D/T delta ofertam tensões aplicáveis 120/240;
- 127/220 não é tratado como igual a 120/240;
- 380 V não é candidato EDP;
- fase de força delta não alimenta carga não trifásica;
- topologia ausente produz pendência.

### 12.3 Solicitação superior

- projeto U sem necessidade FF → U determinado, D elegível;
- projeto U com carga 220 em rede estrela → U incompatível, D elegível por solicitação;
- projeto D → T elegível por solicitação;
- alternativa superior não é selecionada automaticamente;
- seleção grava aceite/justificativa;
- recálculo mantém categoria mínima separada da solicitada.

### 12.4 Cargas especiais

- raio X e solda em U;
- solda >10 kVA em D;
- raio X 220 V >1500 W em D;
- solda 220 V >10 kVA e trifásica >30 kVA em T;
- raio X 220 V >1500 W e trifásico >20 kVA em T;
- motor no limite e acima do limite por subcategoria;
- bomba de incêndio gera circuito/proteção especial;
- caso superior gera estudo, não candidato compatível.

### 12.5 Demanda

- Tabela 005 muda de faixa pelo kW ativo, não kVA;
- FP diferente de 1 altera kW sem corromper kVA;
- quantidade e fatores dos grupos b-f/i;
- maior/restantes nos grupos g/h;
- `D1 + D3 = DT`;
- cargas mono e tri distribuídas corretamente;
- unidade VA/W claramente validada.

### 12.6 Subcategorias

Testar cada degrau:

- U2;
- D2, D4, D6, D7, D9, D10;
- T2, T4, T6, T7, T9, T10.

Para cada linha validar:

- limite de corrente;
- proteção;
- medição;
- condutor PVC;
- condutor EPR/XLPE;
- caixa;
- eletroduto;
- poste/PCI;
- aterramento;
- motor;
- alertas.

Testar 150 A, imediatamente acima de 150 A, 350 A e acima de 350 A.

### 12.7 Integração ponta a ponta

Para a mesma fixture:

1. cadastrar dependências e cargas;
2. calcular demanda;
3. avaliar padrão;
4. selecionar/solicitar;
5. dividir circuitos;
6. calcular correntes;
7. dimensionar;
8. montar unifilar;
9. gerar relatório.

Asserções:

- mesmo sistema;
- mesmas tensões;
- mesma categoria/subcategoria;
- nenhum módulo usa catálogo genérico;
- nenhuma tensão é reinterpretada;
- todos os resultados são invalidados após mudança.

### 12.8 Regressão da captura

Fixture equivalente à captura:

- cargas requerem 127 e 220 V;
- demanda baixa o suficiente para enquadramento mínimo U;
- rede estrela EDP.

Esperado:

- U é incompatível com a necessidade FF 220;
- D aparece como elegível por solicitação superior;
- o usuário pode selecionar D mediante confirmação;
- subcategoria D é calculada pela corrente;
- Correntes/Dimensionamento/Unifilar passam a usar 127/220;
- nenhuma opção fica silenciosamente desabilitada.

### 12.9 Migração

- configuração sem versão;
- catálogo persistido com BI mínimo 8;
- catálogo persistido com BI mínimo 0;
- seleção `MONO-127`;
- seleção `MONO-220`;
- seleção `BI-127-220`;
- seleção `TRI-220-380`;
- catálogo customizado;
- override EDP antigo;
- projeto sem topologia;
- leitura reversível e idempotente.

---

## 13. Mapa de arquivos provável

### Domínio EDP

- `src/domain/distribuidora/edp-sp/categorias-fornecimento.data.json`
- `src/domain/distribuidora/edp-sp/categorias-fornecimento.ts`
- `src/domain/distribuidora/edp-sp/seletor-categoria.ts`
- `src/domain/distribuidora/edp-sp/motor-edp-sp.ts`
- `src/domain/distribuidora/edp-sp/motor-demanda.ts`
- `src/domain/distribuidora/edp-sp/seletor-subcategoria.ts`
- `src/domain/distribuidora/edp-sp/subcategorias-fornecimento.ts`
- `src/domain/distribuidora/edp-sp/subcategorias-fornecimento.catalogo.data.json`
- `src/domain/distribuidora/edp-sp/validacao.ts`
- `src/domain/distribuidora/edp-sp/contratos.ts`
- `src/domain/distribuidora/edp-sp/parametros.ts`
- `src/domain/distribuidora/edp-sp/adaptador-projeto.ts`

### Modelo/API/persistência

- `src/domain/modelo/padrao-fornecimento.ts`
- `src/domain/modelo/padrao-entrada.ts`
- `src/domain/modelo/projeto.ts`
- `src/api/schemas/padrao-entrada.ts`
- `src/api/schemas/parametros-edp.ts`
- `src/domain/servicos/servico-padrao-entrada.ts`
- `src/domain/servicos/servico-parametros-edp.ts`
- `src/infra/supabase/mapeadores.ts`
- `src/infra/supabase/repo-parametros-edp.supabase.ts`
- migrations Supabase correspondentes, se aprovadas na story

### Interface

- `src/routes/projetos.$projetoId_.padrao-entrada.tsx`
- `src/components/app/FornecimentoSelector.tsx`
- componentes em `src/components/app/edp-sp/`
- `src/components/app/NovaDependenciaModal.tsx`
- `src/components/app/EditarDependenciaModal.tsx`
- utilitários de tensão recomendada

### Consumidores

- `src/domain/servicos/servico-divisao-circuitos.ts`
- `src/domain/calculo/derivar-circuitos.ts`
- `src/domain/servicos/servico-corrente.ts`
- `src/domain/calculo/corrente-circuitos.ts`
- `src/domain/servicos/servico-dimensionamento-condutores.ts`
- `src/domain/unifilar/`
- rotas de Correntes, Dimensionamento e Unifilar
- `src/domain/servicos/servico-relatorio-projeto.ts`
- renderizadores/exportadores de relatório

### Testes

- testes EDP em `src/domain/distribuidora/edp-sp/__tests__/`
- `tests/domain/calculo/`
- `tests/domain/servicos/`
- `tests/api/padrao-entrada.test.ts`
- testes de API de parâmetros EDP
- testes de unifilar/relatório
- teste UI/VRT do seletor e cards EDP

---

## 14. Estratégia de migração e compatibilidade

### 14.1 Princípios

- migração não destrutiva;
- nenhuma equivalência por nome apenas;
- nenhuma conversão 380 → 220;
- nenhuma categoria superior presumida;
- seleção antiga preservada para auditoria;
- recálculo obrigatório quando entradas normativas mudarem;
- processo idempotente.

### 14.2 Matriz de migração indicativa

| Legado | Possível destino | Regra |
|---|---|---|
| `MONO-127` | U estrela | somente se distribuidora/rede estrela estiverem confirmadas e cargas forem compatíveis |
| `MONO-220` | sem mapeamento EDP direto | exigir revisão |
| `BI-127-220` | D estrela | exigir rede estrela e distinguir categoria mínima de solicitação superior |
| `TRI-220-380` | sem mapeamento EDP V9 | exigir revisão; nunca converter automaticamente |
| catálogo customizado | sem mapeamento automático | preservar e solicitar revisão |

### 14.3 Transição

Enquanto houver projetos legados:

- cálculo EDP novo pode rodar em modo de comparação;
- divergências devem ser expostas por diagnóstico;
- o contrato legado não deve continuar alimentando silenciosamente novos resultados;
- o CLI deve oferecer inventário/migração antes de qualquer fluxo exclusivamente visual.

---

## 15. Riscos e controles

| Risco | Severidade | Controle |
|---|---|---|
| corrente calculada com tensão errada | crítica | contrato único e teste ponta a ponta |
| categoria incorreta nas fronteiras | alta | teste 12/25/75 e validação técnica |
| confundir solicitação superior com enquadramento automático | alta | campos e estados separados |
| mapear 380 V para EDP | crítica | bloqueio de migração |
| perder configuração de projeto | alta | migração não destrutiva e rollback |
| override manual tratado como norma verificada | alta | proveniência explícita |
| subcategoria sem especificação completa | alta | contrato estrutural completo |
| mudança de padrão não invalidar dimensionamento | alta | matriz de invalidação e integração |
| MMGD não considerada | alta quando aplicável | pendência explícita |
| rede subterrânea avaliada pela norma aérea | alta | gate de escopo |
| regressão em outros fornecedores | média | separar módulo genérico do EDP |

---

## 16. Decisões pendentes

Estas decisões não devem ser assumidas pelo @dev:

1. **Fonte da topologia da rede:** cadastro manual, dado da concessionária ou configuração do projeto.
2. **Escopo delta 240/120:** suporte imediato integral ou bloqueio explícito até uma story dedicada.
3. **Carga trifásica abaixo das faixas T textuais:** enquadramento ou estudo.
4. **Fluxo de categoria superior:** apenas registro de intenção ou confirmação da concessionária.
5. **Área de concessão/localização:** como o projeto comprova que a V9 é aplicável.
6. **Rede subterrânea:** redirecionamento para outro módulo ou apenas fora de escopo.
7. **Governança de parâmetros EDP:** quem pode alterar e com qual efeito de verificação.
8. **MMGD:** entrada imediata ou pendência explícita.
9. **Destino do catálogo genérico:** outra distribuidora/modo ou descontinuação.
10. **Contrato canônico:** forma final e estratégia de compatibilidade, sob autoridade de @architect.

---

## 17. Anti-soluções

Não considerar a correção concluída se consistir apenas em:

- habilitar todos os itens do `Select`;
- alterar novamente `potencia_min_kVA`;
- adicionar U/D/T ao catálogo genérico;
- remover o `disabled` sem validação da API;
- usar 380 V como tensão EDP;
- selecionar D automaticamente para toda carga pequena com 220 V;
- selecionar T automaticamente para toda carga trifásica sem topologia;
- manter Correntes no contrato genérico e cards no contrato EDP;
- marcar overrides como `VERIFICADO`;
- copiar o catálogo oficial para cada projeto;
- mapear IDs legados por semelhança textual;
- esconder estados de estudo/fora de escopo como “incompatível”.

---

## 18. Definition of Done proposta

O conjunto só está concluído quando:

- todas as decisões pendentes necessárias estiverem documentadas;
- stories e critérios estiverem aprovados;
- catálogo cobrir a matriz V9 definida;
- motor de candidatos for puro, rastreável e testado;
- houver um único contrato efetivo por projeto EDP;
- todos os consumidores estiverem migrados;
- persistência e migração forem idempotentes;
- cenário da captura estiver coberto;
- testes de estrela/delta, fronteiras, especiais e subcategorias passarem;
- relatório e unifilar refletirem o mesmo padrão;
- `npm run lint`, `npm run typecheck`, `npm test` e `npm run build` passarem;
- checklist e File List das stories forem atualizados;
- @qa emitir o parecer de qualidade;
- documentação técnica e operacional estiver atualizada.

---

## 19. Ordem recomendada de stories

Esta é uma decomposição sugerida; a criação e priorização pertencem a @po/@sm.

1. **PE-EDP-V9-01 — Modelo de rede, tensão e catálogo normativo**
2. **PE-EDP-V9-02 — Correção de demanda e avaliador de candidatos**
3. **PE-EDP-V9-03 — Contrato canônico e migração de Correntes/Divisão**
4. **PE-EDP-V9-04 — Propagação para Dimensionamento e Unifilar**
5. **PE-EDP-V9-05 — Persistência, versão e migração legada**
6. **PE-EDP-V9-06 — Reestruturação do campo Padrão compatível**
7. **PE-EDP-V9-07 — Especificação física, relatório e auditoria**
8. **PE-EDP-V9-08 — Testes de integração e remoção do legado**

O @dev não deve iniciar pela story visual. A sequência deve respeitar:

`CLI/domínio → contratos/observabilidade → API/persistência → UI`.

---

## 20. Conclusão

O campo “Padrão compatível” está sem opções utilizáveis porque a interface transforma `sem-padrao` em conjunto vazio de candidatos. Entretanto, a causa funcional é mais ampla: a rota EDP usa catálogo genérico, o catálogo EDP é incompleto diante da V9 e os módulos posteriores não compartilham a mesma fonte.

A V9 não autoriza tratar o atendimento como quatro opções genéricas por tensão e kVA. A compatibilidade depende, no mínimo, de rede, topologia, tensões, carga instalada ativa, demanda, fases, categoria, solicitação superior, cargas especiais e subcategoria construtiva.

A correção deve começar no domínio e terminar na interface. Só então o campo poderá oferecer opções realmente compatíveis, explicar por que cada alternativa é válida ou inválida e garantir que a escolha produza o mesmo resultado em Correntes, Dimensionamento, Unifilar e Relatório.
