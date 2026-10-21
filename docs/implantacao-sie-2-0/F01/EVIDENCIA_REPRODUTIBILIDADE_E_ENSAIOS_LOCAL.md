# F01 — Evidências de execução real: revisões locais e ensaios de cálculo
Data: 2026-10-15. **Escopo de desenvolvimento local, sem homologação normativa.**

## Alterações efetivamente implementadas no GitHub durante a execução
1. `sie_api/storage.py`: nova tabela `versoes_projeto` guarda *nome, todos os dados JSON, revisão, hash SHA-256 e data* em transação única com projeto, eventos de auditoria e catálogo normativo. Os gatilhos impedem UPDATE/DELETE SQL usuais. Versões legadas não são inventadas.
2. `storage_api.py`: `GET /api/v1/local/projetos/{id}/revisoes` e `GET /api/v1/local/projetos/{id}/revisoes/{n}` autenticados; falham fechados quando revisão inexiste ou hash é inválido.
3. `sie_api/analysis_contracts.py`: contrato Pydantic compartilhado por análise HTTP e registro de ensaio; bloqueia campos arbitrários como `release_allowed`.
4. `sie_api/calculation_traces.py` + `storage.py`: ensaio de algoritmo *executado no servidor*, por circuito, revisão e UUID do ensaio. Persiste entradas, saídas, IDs dos **algoritmos realmente executados** (`selecionar_condutor`, `selecionar_disjuntor`, `calcular_queda_tensao_monofasica`), digest e cópia imutável; auditoria de acesso por token local.
5. `POST /api/v1/local/projetos/{id}/revisoes/{n}/circuitos/{nome}/ensaios`, `GET .../revisoes/{n}/ensaios`, `GET /api/v1/local/projetos/{id}/ensaios/{uuid}`; recusam revisão antiga, circuito não cadastrado/duplicado, dados incompatíveis, token ausente ou alegação arbitrária de aprovação.
6. `test_project_revisions_f01.py`, `test_calculation_traces_f01.py`, `test_f01_independent_math_examples.py`: testes de API, integridade, concorrência otimista, recuperação, corrupção, casos-limite e matemática independente.

## Níveis de proveniência que NÃO podem ser confundidos
| Camada | Informação vinculada ao circuito | Estado |
|---|---|---|
| Versão do projeto | Input completo tal como **salvo pelo usuário** | Preservado, imutável no fluxo normal e reconstituível **a partir das novas versões** |
| Snapshot do catálogo | Metadados ABNT/EDP/NR-10 conhecidos no momento do salvamento | Preservado, mas NÃO prova uso no cálculo |
| Execução registrada | Inputs + outputs efetivamente processados e IDs de algoritmos Python | **Comprovado como execução de algoritmo local**, com digest |
| Referência textual no input | `evidencia.documento/edicao/referencia` declarada pelo cliente | **DECLARADA, NÃO VERIFICADA** |
| Linha/célula ABNT/EDP realmente consumida | Sem ID/célula controlada pelo servidor; catálogo Iz/Rca/XL/demanda não homologado | **NÃO COMPROVADO** |
| Conformidade normativa e liberação profissional | Fonte não auditada, licença/edição/aplicabilidade incompletas, sem QA externo | **BLOQUEADA** |

A assinatura SHA-256 detecta alteração unilateral de JSON, mas não protege contra administrador que altera dados **e digest**. Controle de acesso atual usa um token de desenvolvimento e não substitui identidade/roles/tenant em produção. Nenhum Supabase, banco remoto ou produção foi modificado.

## Cálculos independentes demonstrativos — NÃO NORMATIVOS
Os casos em `test_f01_independent_math_examples.py` usam apenas aritmética e entradas sintéticas, não transcrições de norma:

| Caso | Expectativa aritmética independente | Interpretação |
|---|---|---|
| Queda monofásica resistiva | `2 × 0,030 km × 20 A × 7,41 Ω/km = 8,892 V`, arredondado a **8,89 V**; para 220 V, **4,04%** | Modelo resistivo específico de ensaio, não verificação geral de instalação |
| Queda trifásica resistiva equilibrada | `√3 × 0,100 km × 15 A × 1,25 Ω/km ≈ 3,2476 V` ⇒ **3,25 V**, em 400 V **0,81%** | Não considera XL/cosφ diferente de 1 |
| Seleção hipotética de condutor | `24 × 0,8=19,2 A` insuficiente para 20 A; `32 × 0,8=25,6 A` suficiente; hipotético In=20 A satisfaz `20≤20≤25,6` | Capacidades e disjuntores sintéticos; NÃO inserir em catálogo ABNT |
| Proteção | `Ib=20 A > Iz=19,2 A` deve rejeitar | Ensaio de desigualdade, não certificação de dispositivo |
| Comprimento zero | `ΔV=0,00 V`, `0,00%` | Caso de contorno |

**As 5 fixtures de álgebra independente NÃO preenchem G03**, que exige valores técnicos normativos comprovados e aplicação independente. O resultado não implica normas ABNT NBR 5410 ou padrões EDP homologados.

## Origem e vigência: consulta pública nesta execução
- A [EDP](https://www.edp.com.br/normas-e-padroes-tecnicos/) lista **PT.DT.PDN.00068**, versão **09**, data de publicação **15/04/2026**, área EDP São Paulo. Não há autenticação da cópia PDF do repo contra o download oficial nem conferência de células.
- O [MTE](https://www.gov.br/trabalho-e-emprego/pt-br/acesso-a-informacao/participacao-social/conselhos-e-orgaos-colegiados/comissao-tripartite-partitaria-permanente/normas-regulamentadora/normas-regulamentadoras-vigentes/norma-regulamentadora-no-10-nr-10) confirma Portaria 737/2026 e vigência geral da nova NR-10 em **01/06/2027**, com ressalva transitória para instalações existentes ainda não resolvida no projeto.
- Licenças ABNT e células Iz/Rca/XL/demanda: **não auditadas** nesta execução.

## Prova computacional e risco residual
CI GitHub Actions API/Chromium/AIOX deve ser registrada por SHA de commit efetivamente concluído. Regressão da F00 roda em `scripts/f00_golden.py --verify` dentro da CI sem mudança de golden.

**AC-01.06/G04: melhorado, mas PARCIAL**. Há histórico local real de entradas e ensaios, mas nenhum vínculo homologado com a linha/nota/célula normativa realmente consumida, tampouco ACL profissional multiusuário ou migração reversível no PostgreSQL. **F01 segue BLOCKED e F02 não liberada.**

## Observação sobre independência dos revisores
O trabalho nesta conversa executou código e testes reais via GitHub. **Não** conseguiu iniciar três processos Copilot CLI realmente isolados porque esse executável não está disponível neste ambiente; três perspectivas de uma mesma LLM não substituem QA3 independente nem aprovação profissional. O programa QA3 e seus perfis continuam prontos para execução em ambiente autenticado.
