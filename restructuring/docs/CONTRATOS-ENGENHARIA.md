# SIE 2.0 — Contratos determinísticos dos motores demonstrativos

**Story:** SIE-AUTO-004. **Escopo:** funções em `apps/api/sie_api/domain/engines.py` e contrato de análise `apps/api/sie_api/main.py`.

## Matriz de entrada, hipótese, saída e falha segura

| Motor | Entrada | Unidade | Hipótese explícita | Saída | Falhas seguras |
| --- | --- | --- | --- | --- | --- |
| Seleção de condutor | Ib, fator global, pares (seção, capacidade) | A, adimensional, mm²/A | Capacidade já corresponde à instalação e à tabela fornecida; `Iz = Iz_base × fator` | Menor seção informada com `Iz >= Ib` | Corrente/fator inválidos, fator >1, tabela vazia, seção duplicada, valor não finito e insuficiência |
| Escolha de disjuntor | Ib, Iz corrigida, catálogo de In | A | Verifica **somente** `Ib <= In <= Iz`, não certifica proteção contra sobrecarga e curto-circuito | Menor In compatível | Catálogo vazio, qualquer In não positivo/não finito, inexistência de solução |
| Queda monofásica resistiva | I, L de ida, R, tensão | A, m, Ω/km, V | `ΔV = 2 × L(km) × I × R`; modelo resistivo, sem reatância | ΔV [V] e percentual [%] | I, R, U não positivos/finitos; L negativo/não finito |
| Queda trifásica resistiva | I, L, R, tensão de linha | A, m, Ω/km, V | Sistema trifásico equilibrado; `cos(phi)=1`, `X=0`, `ΔV = √3 × L(km) × I × R` | ΔV [V] e percentual [%] | Mesmo contrato de entrada do motor monofásico |

## Valores-limite

- Comprimento `0 m`: ΔV deve ser precisamente `0.00 V` e `0.00%`. É um caso matemático válido para testar o núcleo, não a representação de um circuito físico pronto para execução.
- Entradas negativas, NaN, infinito e objetos ausentes: a camada de domínio deve rejeitar sem selecionar catálogo.
- O contrato HTTP usa Pydantic para rejeitar valores incompatíveis; o motor também revalida parâmetros críticos.
- A API de análise aceita comprimento não negativo. A UI permite zero para manter contrato coerente.
- A lista de condutores é informada pelo usuário e não possui certificação de fonte independente nesta etapa.
- Saídas são arredondadas para duas casas decimais com `Decimal` e `ROUND_HALF_UP`, exclusivamente para apresentação; não confundir com arredondamento normativo estabelecido por norma.
- O cálculo resistivo não contempla fator de potência variável, reatância, harmônicas, temperatura, deslocamento de fase, queda anterior nem desbalanceamento.
- A seleção de disjuntor não verifica `I2 ≤ 1,45 Iz`, capacidade de interrupção, curva, coordenação, seletividade ou condições de instalação.
- Nenhum cálculo daqui gera `APROVADO` normativo, porque o gate de liberação de evidências é conservador e separado.

## Critério técnico de aceite desta story

Todos os testes de borda e regressão devem passar em CI; o JavaScript e os gates AIOX do repositório precisam permanecer aprovados. A existência desses testes não equivale à validação de tabelas de NBR 5410 ou às decisões da concessionária.

**Fontes de comprovação:** `tests/test_engines.py`, `tests/test_api.py`, execução de GitHub Actions e relatório da story. Casos físicos e normativos independentes continuam pendentes de confirmação de fontes primárias.
