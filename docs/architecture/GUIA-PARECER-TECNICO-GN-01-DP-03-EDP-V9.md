# Guia para obtenção do Parecer Técnico GN-01 e DP-03 — EDP V9

> **Tipo do documento:** guia operacional  
> **Data:** 2026-07-26  
> **Norma de referência:** PT.DT.PDN.00068, versão V9, de 14/04/2026  
> **Resultado esperado:** parecer técnico real, preenchido, com decisões e fundamentação normativa rastreáveis  
> **Arquivo final esperado:** `docs/architecture/PARECER-TECNICO-GN-01-DP-03-EDP-V9.md`

## 1. Finalidade deste guia

Este guia explica como obter, construir, validar, assinar e registrar o parecer
técnico necessário para encerrar os gates:

- **GN-01:** ratificação do tratamento das fronteiras exatas de 12 kW e
  25 kW;
- **DP-03:** definição do tratamento de cargas trifásicas não enquadradas
  diretamente nas faixas textuais da PT.DT.PDN.00068 V9.

O parecer não pode ser produzido por inferência do desenvolvedor, do agente de
IA, do Product Owner ou do arquiteto de software. O conteúdo técnico e os
status de aprovação devem decorrer de validação técnica competente. O parecer
não exige identificação pessoal, registro profissional, organização, data,
bloco bibliográfico no cabeçalho ou assinatura.

Este arquivo é somente um guia. Ele não substitui o parecer e não deve ser
usado como evidência de aprovação dos gates.

## 2. Por que o workflow está bloqueado

O PRD atribui ao responsável técnico a autoridade para ratificar GN-01 e
participar da decisão de DP-03:

- `GN-01`: ratificação das fronteiras exatas de 12 e 25 kW;
- `DP-03`: tratamento de cargas trifásicas abaixo ou fora das faixas T
  textuais.

A interpretação documental existente no projeto ainda é provisória. Ela
indica, para o sistema estrela:

- categoria U para carga instalada de até 12 kW;
- categoria D para carga instalada acima de 12 kW e até 25 kW;
- categoria T para carga instalada acima de 25 kW e até 75 kW.

Isso sugere que exatamente 12 kW pertence a U e exatamente 25 kW pertence a D
no sistema estrela. Entretanto, essa interpretação não pode ser convertida em
regra definitiva de software até que GN-01 seja ratificado.

Também existe uma lacuna para instalações com equipamentos trifásicos que
ficam abaixo dos pisos textuais da categoria T. O sistema não pode escolher
silenciosamente uma categoria, alterar a tensão da carga ou declarar
compatibilidade sem a decisão técnica de DP-03.

## 3. Documentos que devem ser reunidos

Antes de contatar o responsável técnico, preparar o seguinte pacote:

1. Norma original:
   `Arquivos_Diversos/Norma_EDP/PT.DT.PDN.00068_V9.pdf`.
2. Transcrição pesquisável da norma:
   `Arquivos_Diversos/Norma_EDP/PT.DT.PDN.00068_V9_markdown_limpo.md`.
3. PRD:
   `docs/prd/PRD-PADRAO-COMPATIVEL-EDP-V9.md`.
4. Relatório de revalidação:
   `docs/prd/RV-01-PRD-PADRAO-COMPATIVEL-EDP-V9.md`.
5. Plano de reestruturação:
   `docs/PLANO-REESTRUTURACAO-PADRAO-COMPATIVEL-EDP-V9.md`.
6. Este guia.

O PDF original deve ser a fonte normativa principal. A versão Markdown serve
para localização e pesquisa, mas não deve substituir a inspeção das páginas,
tabelas e notas do PDF.

## 4. Conteúdo mínimo do parecer

O parecer deve resultar de análise técnica compatível com o tema elétrico
avaliado, mas o arquivo não precisa expor dados pessoais ou profissionais.

Nome, registro profissional, organização, data, identificação bibliográfica no
cabeçalho e assinatura não fazem parte do conteúdo mínimo. Se fornecidos
voluntariamente, esses metadados poderão ser registrados em anexo separado. Sua
ausência não invalida o parecer e não impede a avaliação de GN-01 ou DP-03.

Permanecem obrigatórios somente o tratamento técnico de GN-01 e DP-03, a
fundamentação normativa de cada conclusão, as condições e exceções aplicáveis e
um status final para cada gate.

## 5. Passo a passo

### Passo 1 — Confirmar o escopo da validação

Antes da análise:

1. confirmar que GN-01 e DP-03 serão respondidos separadamente;
2. confirmar que estrela e delta serão analisadas sem equivalência implícita;
3. exigir fundamentação com seção, tabela, nota ou página aplicável;
4. informar que as conclusões serão versionadas no repositório do projeto.

Não prosseguir usando conclusões fictícias ou exemplos como decisão definitiva.

### Passo 2 — Enviar a solicitação formal

Pode-se enviar a seguinte mensagem:

```text
Assunto: Solicitação de parecer técnico — GN-01 e DP-03 — EDP V9

Prezado(a),

solicitamos a emissão de parecer técnico referente à interpretação da
PT.DT.PDN.00068, versão V9, para utilização no projeto SIE.

O parecer deve tratar expressamente:

1. GN-01:
   - enquadramento de carga instalada exatamente igual a 12 kW;
   - enquadramento de carga instalada exatamente igual a 25 kW;
   - distinção entre as topologias estrela 220/127 V e delta 240/120 V;
   - efeito, se houver, da presença de equipamento trifásico;
   - justificativa com seção, tabela, nota e página da norma;
   - status final APROVADO ou REPROVADO.

2. DP-03:
   - tratamento de equipamentos/cargas trifásicas que não se enquadram
     diretamente nas faixas T textuais;
   - limites aplicáveis em estrela e delta;
   - tratamento das fronteiras exatas;
   - situações que exigem solicitação de categoria superior, confirmação
     da concessionária ou estudo técnico;
   - justificativa com seção, tabela, nota e página da norma;
   - status final APROVADO ou REPROVADO.

O arquivo final será registrado como:
docs/architecture/PARECER-TECNICO-GN-01-DP-03-EDP-V9.md
```

### Passo 3 — Criar um rascunho sem valor de aprovação

Enquanto o profissional estiver analisando, usar um nome que deixe claro o
estado do documento:

```text
docs/architecture/PARECER-TECNICO-GN-01-DP-03-EDP-V9-RASCUNHO.md
```

Não usar o nome definitivo enquanto existirem:

- campos vazios;
- instruções entre sinais de menor e maior;
- alternativas como `APROVADO|REPROVADO`;
- conclusões ainda não confirmadas;
- ausência de fundamentação técnica.

### Passo 4 — Registrar a fundamentação normativa

Cada justificativa deve apontar a base técnica utilizada. Não é obrigatório
repetir documento e versão em um bloco de identificação no cabeçalho. Para esta
análise, devem ser conferidos no PDF original, quando aplicáveis:

- seção 5.3.2 — Limite de fornecimento;
- seção 5.3.3 — Categorias de atendimento;
- seção 5.3.4 — Limitações no atendimento;
- Tabela 001 — categorias U e D;
- Tabela 002 — categoria T;
- Nota 01;
- Nota 02;
- Nota 03.

### Passo 5 — Analisar GN-01

GN-01 deve responder, sem deixar implícitos os limites:

1. Qual categoria mínima se aplica a exatamente 12 kW em estrela?
2. Qual categoria mínima se aplica a exatamente 12 kW em delta?
3. Qual categoria mínima se aplica a exatamente 25 kW em estrela?
4. Qual tratamento se aplica a exatamente 25 kW em delta?
5. A presença de equipamento trifásico muda alguma dessas respostas?
6. Os termos “até” e “acima de” produzem quais intervalos inclusivos e
   exclusivos?
7. A Nota 03 altera a categoria mínima ou apenas permite solicitar uma
   categoria superior?
8. Há necessidade de confirmação da concessionária em algum dos casos?

O parecer deve apresentar a regra em linguagem direta. Exemplos de formato,
sem antecipar a conclusão do profissional:

```text
Para a topologia [...], uma instalação com carga exatamente igual a 12 kW
deve receber o tratamento [...], porque a seção [...], página [...], define
[...].
```

Não basta escrever “de acordo com a norma”. A justificativa deve permitir que
outra pessoa reconstrua a interpretação.

### Passo 6 — Analisar DP-03

DP-03 deve tratar, pelo menos, os seguintes cenários:

1. equipamento trifásico em sistema estrela com carga instalada inferior a
   25 kW;
2. equipamento trifásico em sistema estrela com carga exatamente igual a
   25 kW;
3. equipamento trifásico em sistema delta com carga instalada inferior a
   12 kW;
4. equipamento trifásico em sistema delta com carga exatamente igual a
   12 kW;
5. carga acima de 75 kW;
6. equipamento sujeito às limitações específicas de motor, solda ou raio X;
7. ausência de dados suficientes sobre topologia, tensão ou características
   do equipamento.

Para cada cenário, o responsável deve declarar:

- se há enquadramento direto;
- se é possível solicitar categoria superior;
- se a solicitação depende de confirmação da EDP;
- se é obrigatório estudo técnico;
- se o caso deve permanecer pendente até obtenção de informação adicional;
- quais limites de potência, carga, tensão, topologia e número de fases foram
  utilizados.

O profissional não precisa criar nomes de enums ou desenhar o software. Ele
deve descrever o tratamento técnico em linguagem inequívoca. A transformação
posterior desse tratamento em contrato de software pertence à arquitetura e à
implementação.

### Passo 7 — Registrar a justificativa normativa

Cada decisão deve conter:

1. código e versão do documento;
2. seção;
3. tabela, quando aplicável;
4. nota, quando aplicável;
5. página do PDF;
6. regra textual interpretada;
7. raciocínio que liga a regra à conclusão;
8. exceções e condições adicionais.

Modelo:

```yaml
justificativa_normativa: |
  Documento: PT.DT.PDN.00068, V9.
  Seção: 5.3.4 — Limitações no atendimento.
  Tabela/nota: <informar>.
  Página(s): <informar conforme o PDF>.
  Interpretação: <explicar os limites inclusivos/exclusivos>.
  Condições adicionais: <informar ou declarar que não se aplicam>.
```

### Passo 8 — Definir o status de cada gate

Cada gate recebe seu próprio status:

```yaml
GN-01:
  status: APROVADO

DP-03:
  status: APROVADO
```

ou:

```yaml
GN-01:
  status: REPROVADO

DP-03:
  status: REPROVADO
```

Significado:

- `APROVADO`: o responsável técnico ratifica o tratamento escrito no parecer;
- `REPROVADO`: o tratamento proposto não pode ser usado como regra definitiva
  e o gate continua bloqueado.

`APROVADO` não significa que todo cenário analisado seja automaticamente
compatível. Por exemplo, o responsável pode aprovar como tratamento definitivo
que determinado cenário sempre produza “requer estudo técnico”.

Não usar `PENDENTE` no arquivo final solicitado, pois a necessidade recebida
exige uma decisão entre `APROVADO` e `REPROVADO`. Se o profissional ainda não
puder decidir, manter o documento como rascunho e não promover para o nome
definitivo.

### Passo 9 — Revisar o conteúdo do parecer

Antes de concluir, confirmar:

1. se estrela e delta foram tratadas separadamente;
2. se exatamente 12 kW foi respondido;
3. se exatamente 25 kW foi respondido;
4. se cargas trifásicas abaixo dos pisos textuais foram tratadas;
5. se o limite acima de 75 kW foi mencionado;
6. se a Nota 03 foi interpretada;
7. se categoria mínima e categoria superior solicitada não foram confundidas;
8. se a necessidade de confirmação da EDP foi registrada;
9. se todas as referências apontam para o PDF correto;
10. se cada gate possui somente um status final.

Caso alguma resposta esteja ambígua, devolver o rascunho para revisão técnica.
O arquiteto ou o desenvolvedor não deve completar a lacuna por conta própria.

### Passo 10 — Registrar o aceite do conteúdo

O aceite pode ser registrado no próprio fluxo de revisão do projeto, sem
assinatura, nome, registro profissional, organização ou data no parecer. O
registro precisa identificar o artefato aceito e preservar seu conteúdo
versionado.

### Passo 11 — Salvar o arquivo definitivo

Somente após preenchimento e revisão do conteúdo, salvar ou renomear o arquivo
para:

```text
docs/architecture/PARECER-TECNICO-GN-01-DP-03-EDP-V9.md
```

O nome deve ser preservado exatamente, incluindo maiúsculas, hífens e extensão.

### Passo 12 — Validar o arquivo final

Executar a conferência abaixo:

```text
[ ] O arquivo está no diretório docs/architecture.
[ ] O nome do arquivo está correto.
[ ] O PDF original foi efetivamente analisado.
[ ] GN-01 responde exatamente 12 kW.
[ ] GN-01 responde exatamente 25 kW.
[ ] GN-01 distingue estrela e delta.
[ ] DP-03 trata cargas/equipamentos trifásicos fora das faixas.
[ ] DP-03 informa os limites aplicáveis.
[ ] As justificativas contêm seção, tabela/nota e página.
[ ] GN-01 tem status APROVADO ou REPROVADO.
[ ] DP-03 tem status APROVADO ou REPROVADO.
[ ] Não existem placeholders.
[ ] Não existem conclusões atribuídas a agente de IA.
```

## 6. Modelo completo do parecer final

Copiar este modelo para o arquivo de rascunho e substituir todos os campos.

```markdown
# Parecer Técnico — GN-01 e DP-03 — EDP V9

## 1. Escopo

O presente parecer trata das fronteiras exatas de 12 kW e 25 kW e do
tratamento de cargas/equipamentos trifásicos não enquadrados diretamente nas
faixas textuais da PT.DT.PDN.00068 V9.

## 2. Parecer GN-01

GN-01:
  tratamento_exato_para_12_kw: |
    <conclusão técnica completa, distinguindo estrela e delta>

  tratamento_exato_para_25_kw: |
    <conclusão técnica completa, distinguindo estrela e delta>

  justificativa_normativa: |
    <documento, seção, tabela/nota, página, interpretação e condições>

  status: <APROVADO ou REPROVADO>

## 3. Parecer DP-03

DP-03:
  tratamento_de_cargas_trifasicas_fora_das_faixas: |
    <tratamento técnico completo para os cenários analisados>

  limites_aplicaveis: |
    <limites de carga, potência, topologia, tensão, fases e equipamentos>

  justificativa_normativa: |
    <documento, seção, tabela/nota, página, interpretação e condições>

  status: <APROVADO ou REPROVADO>

## 4. Condições e limitações

Os status atribuídos a GN-01 e DP-03 referem-se aos tratamentos descritos neste
documento e não dispensam confirmação ou estudo da concessionária nos casos
indicados na fundamentação.
```

## 7. O que não deve ser feito

Não:

- copiar a leitura provisória do PRD e apresentá-la como conclusão técnica;
- usar aprovação de agente de IA como aprovação normativa;
- usar aprovação do arquiteto de software como substituta da responsabilidade
  técnica;
- tratar exatamente 12 kW como “acima de 12 kW”;
- tratar exatamente 25 kW como “acima de 25 kW”;
- forçar automaticamente categoria T para qualquer equipamento trifásico;
- tratar a Nota 03 como concessão automática de categoria superior;
- omitir a topologia da rede;
- misturar 220/127 V com 240/120 V;
- considerar o arquivo concluído apenas porque ele existe;
- alterar manualmente os status do PRD antes da revalidação formal.

## 8. Retomada do workflow

Depois que o parecer definitivo estiver no repositório:

1. verificar a completude, a fundamentação e os status técnicos;
2. encaminhar o parecer ao `@architect`;
3. solicitar que o arquiteto traduza DP-03 para regras e estados do contrato
   canônico, sem modificar a conclusão normativa;
4. encaminhar a evidência a `@pm` e `@po`;
5. reexecutar RV-01 sobre o novo snapshot;
6. atualizar formalmente os estados de GN-01 e DP-03;
7. verificar os demais gates listados no PRD e no relatório RV-01;
8. somente marcar `implementation_authorized: true` se todas as condições de
   autorização estiverem satisfeitas;
9. após autorização, solicitar a `@sm` ou `@po` a criação/refinamento das
   stories;
10. somente então encaminhar as stories Ready para implementação.

A existência do parecer encerra a ausência de evidência de GN-01 e DP-03, mas
não substitui a reexecução de RV-01. Também não resolve automaticamente outros
gates que permaneçam pendentes no snapshot vigente.

## 9. Critério de conclusão

Esta atividade estará concluída quando:

1. o arquivo definitivo existir no caminho exigido;
2. GN-01 e DP-03 estiverem respondidos sem ambiguidades;
3. as conclusões forem rastreáveis à base normativa aplicável;
4. cada gate possuir status final;
5. o parecer tiver sido recebido por `@architect`, `@pm` e `@po`;
6. RV-01 tiver sido formalmente reexecutado.
