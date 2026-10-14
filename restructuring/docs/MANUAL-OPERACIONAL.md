# Manual iniciante — SIE 2.0

## 1. Para que serve

O SIE 2.0 é o ambiente de apoio ao projeto elétrico. Nesta primeira entrega integrada, ele permite analisar um circuito com três motores: capacidade corrigida do condutor, escolha de disjuntor comercial e queda de tensão monofásica resistiva. A finalidade é tornar cada resultado visível, reproduzível e revisável.

## 2. Primeiro acesso

Siga o procedimento de execução descrito no README. Ao abrir a página, o indicador no canto superior direito deve mostrar **API online**. Caso mostre **API local não conectada**, confirme que o terminal da API ainda está em execução na porta 8000.

## 3. Entenda a tela

| Área | O que mostra | Como usar |
|---|---|---|
| Barra lateral | navegação da jornada | use para ir a visão geral, análise, governança e guia |
| Centro de comando | resumo do produto | clique em **Nova análise** para ir ao primeiro campo |
| Indicadores | escopo da versão atual | servem como leitura rápida, não como certificado técnico |
| Analisar circuito | entradas que alimentam o motor | preencha valores reais e verificáveis |
| Decisão técnica | resultado do motor e situação do gate | confira o critério e não ignore avisos |
| Rastreabilidade | sequência de dados até a saída | use para revisão e auditoria |

## 4. Preenchimento passo a passo

1. **Corrente de projeto (A):** informe `Ib`, obtida pelo cálculo da carga do circuito.
2. **Comprimento (m):** informe o comprimento elétrico de ida; o motor aplica o fator `2` na fórmula monofásica para representar ida e volta.
3. **Tensão nominal (V):** informe a tensão do circuito, como 127 V ou 220 V.
4. **Resistência (Ω/km):** informe a resistência apropriada para o condutor e condição estudada, extraída de fonte técnica aplicável.
5. **Fator de correção:** informe um fator entre 0 e 1. Ele reduz a capacidade-base da tabela quando a condição de instalação exige correção.
6. **Fonte, edição e referência:** registre o documento e a localização precisa do dado usado.
7. **Controles de validação:** marque somente após a conferência efetiva da fonte e dos testes independentes.
8. Clique em **Executar análise**.

## 5. Leitura do resultado

- **Condutor selecionado:** menor seção da tabela informada cuja capacidade corrigida atende a corrente de projeto.
- **Disjuntor comercial:** menor valor de catálogo que satisfaz `Ib ≤ In ≤ Iz`.
- **Queda de tensão:** queda em volts e percentual, acompanhada da fórmula usada.
- **Evidência:** metadados que permitem reproduzir a análise.
- **Gate normativo:** aparece como `BLOQUEADO`, `PENDENTE` ou `APROVADO`. O sistema não deve ser usado para afirmar conformidade quando esse status não estiver aprovado.

## 6. Avisos comuns

| Mensagem | Significado | Ação |
|---|---|---|
| `Ib excede Iz` | condutor corrigido insuficiente | reveja seção, método de instalação ou carga |
| `Nenhum disjuntor comercial atende` | catálogo não produz uma combinação segura | revise condutor/corrente/catálogo |
| `Tabela não possui seção suficiente` | nenhuma linha da tabela atende a demanda | inclua seção tecnicamente válida ou revise o circuito |
| Gate pendente | evidência ou testes ainda não foram confirmados | faça a revisão documental e técnica |

## 7. Limites e responsabilidade

O aplicativo não substitui projeto, norma aplicável, concessionária, ART ou responsável técnico. A liberação exibida é somente o resultado do gate de evidências fornecidas para este módulo; não equivale a aprovação integral da instalação.

## 8. Padrão de entrada EDP

O endpoint `POST /api/v1/edp/enquadrar` incorpora o catálogo conferido das Tabelas 001/002 do padrão **EDP São Paulo PT.DT.PDN.00068 v09**, com vigência indicada no repositório em 14/04/2026. Ele retorna categoria, disjuntor, medição e condutores de entrada, preservando a fonte e seu status **VERIFICADO**. A sugestão por corrente permanece identificada como regra de automação e não substitui a análise final da concessionária.

## 9. Testes locais

Com o ambiente virtual ativo, execute:

```powershell
cd restructuring\apps\api
python -m pytest -q
```

Os testes cobrem validação de entradas, cálculos, regras de proteção e endpoint HTTP. Em caso de erro, não use os resultados até restabelecer a execução verde.
