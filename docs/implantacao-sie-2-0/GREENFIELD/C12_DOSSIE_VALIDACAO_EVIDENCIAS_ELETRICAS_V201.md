# C12 — Dossiê de evidências para validação elétrica | Bloco C — SIE 2.0

**Classificação:** PACOTE PARA PREENCHIMENTO PELO RESPONSÁVEL; NENHUM ACEITE EMITIDO.
**Identificador:** `SIE2-C12-20261028` · **Edição:** 1.0 · **Data:** 28/10/2026.
**Abrangência:** revisão do catálogo C04, motores C05, integração elétrica C03 e sete campos semânticos de legado. Exclusão: aprovação de projeto executivo ou instalações de terceiros, SPDA/fotovoltaico/recarga/ambientes especiais se não implementados e declarados no escopo.

## A. Identificação e autenticação do responsável
| Campo | Evidência requerida | Estado inicial |
|---|---|---|
| Nome profissional | Inserido pelo próprio avaliador no instrumento assinado | PENDENTE |
| CREA/UF e situação cadastral | Certidão de Registro e Quitação validada no CREA emissor | PENDENTE |
| Títulos e atribuições | Certidão de Registro e Anotações; verificar pertinência ao objeto | PENDENTE |
| Enquadramento ART | Exigível? fundamento; número e consulta se registrada | PENDENTE |
| Declaração de imparcialidade/limitação | Autorreflexão de conflito de interesse e revisão independente se aplicável | PENDENTE |
| Assinatura verificável | Plataforma/documento formal e metadados de assinatura | PENDENTE |

Certidões e dados pessoais devem ficar em armazenamento restrito. No GitHub armazenar somente referências, versões e hashes sem PII.

## B. Software e cadeia de evidência
- Repositório: https://github.com/SFPTechnology/Projeto-SIE-2.0
- PR de desenvolvimento: https://github.com/SFPTechnology/Projeto-SIE-2.0/pull/11
- Branch: `feat/v201-bloco-c-dominio-eletrico`.
- SHA de referência (não congelamento final): `a82776203db9b1d60dd49cbbd6602a47093f9df1`.
- CI observado no SHA de referência: API, PostgreSQL C03, PostgreSQL A03/A04, Chromium E2E, AIOX: **PASS**. **Isso é QA de software, não aceite elétrico.**
- Supabase de destino: `fozrymsidnaxmuvxxfhh`. Checagem agregada de 28/10/2026: **1 conta Auth confirmada e não excluída**; o vínculo dessa conta a uma sessão do titular e aos cinco projetos ainda requer prova.
- Origem legada `hlbksclcandbsyqrsbmx`: 5 projetos, 41 ambientes, 52 cargas adicionais, 1.934 registros em 15 tabelas. ETL real ainda não homologado.
- Migrations remotas: somente GF02; A03/A04/B04/C03 ainda não aplicadas.
- SHA final, versão de dependências, ID do ambiente isolado, snapshots e hash dos dados de ensaio: **A PREENCHER APÓS EXECUÇÃO**.

## C. Matriz de evidências por ensaio
Cada linha abaixo requer `case_id`, descrição detalhada, ambiente, entrada, versão da regra/fonte oficial autorizada, esperado independente, observado, diferença/tolerância, link ao log e evidência SHA256.

| Grupo | Evidência crítica exigida | Resultado observado | Parecer |
|---|---|---|---|
| E01 Iluminação/TUG | 3 tipologias, fronteiras de área/perímetro, cozinha/banheiro e casos negativos | NÃO EXECUTADO NESTE DOSSIÊ | PENDENTE |
| E02 TUE/FP/topologia | NULL de tensão, fase, BTU/h e W identificados e conversão justificada | NÃO EXECUTADO NESTE DOSSIÊ | PENDENTE |
| E03 Demanda/divisão | Fatores oficiais e contraprovas de balanceamento | NÃO EXECUTADO NESTE DOSSIÊ | PENDENTE |
| E04 Condutores | Material, método, agrupamento, temperatura, tabela e limites | NÃO EXECUTADO NESTE DOSSIÊ | PENDENTE |
| E05 Queda de tensão | Rca/XL oficial, trechos, fator de potência, limites e tolerâncias | NÃO EXECUTADO NESTE DOSSIÊ | PENDENTE |
| E06 Proteções | Ib/In/Iz/I2, Icc, curva, poder de interrupção, seletividade | NÃO EXECUTADO NESTE DOSSIÊ | PENDENTE |
| E07 DR/DPS | Localização, coordenação, sensibilidade e restrições normativas | NÃO EXECUTADO NESTE DOSSIÊ | PENDENTE |
| E08 Aterramento | TT/TN/IT, PE/N e proteção contra choque | NÃO EXECUTADO NESTE DOSSIÊ | PENDENTE |
| E09 EDP/concessionária | Concessão, categoria, versão e cálculos oficiais vigentes | NÃO EXECUTADO NESTE DOSSIÊ | PENDENTE |
| E10 Legado | Sete campos elétricos: decisão individual, retenção e não promoção de `NOT_EVALUATED` | NÃO EXECUTADO NESTE DOSSIÊ | PENDENTE |
| E11 Segurança/negativos | Alteração de catálogo, entrada ausente, resultado obsoleto, regressão | NÃO EXECUTADO NESTE DOSSIÊ | PENDENTE |

**Atenção:** os cinco workflows PASS não demonstram nenhuma dessas onze conclusões normativas por si sós. Se um ensaio já existe em outra execução, importar apenas sua evidência verificável e compatível com o SHA/versões.

## D. Casos de dados incompletos — tratamento obrigatório
| Ocorrência | Quantidade de origem | Decisão admissível |
|---|---:|---|
| Altura/pe-direito zero | 41 | Histórico fiel; cálculo que depende da altura deve exigir dado válido |
| Tensão fixa ausente | 4 cargas | Não inferir tensão de fornecimento |
| Marcador trifásico | 2 cargas | Exigir topologia e tensão de linha comprovadas |
| Eventos de auditoria com dependência removida | 10 | Preservar em arquivo governado como referência histórica |
| Campos adicionais anteriormente não mapeados | 45 | 15 fonte/histórico, 22 tabelas vazias, 7 revisão elétrica, 1 revisão UX |

## E. Registro de não conformidades
Utilizar linhas: `NC-ID | E01-E11 | Severidade | Descrição objetiva | Exigência normativa/fontes | Reprodução | Evidência | Responsável pela correção | Prazo | Resultado do reteste | Situação`.

**Preencher durante execução.** Não há NC considerada resolvida por omissão. Pendências conhecidas a examinar: P03, P06, Rca/XL, proteção I2/curto, DR/DPS, aterramento, versão e aplicabilidade concessionária, sete campos elétricos do legado.

## F. Manifesto mínimo de evidências
| ID | Tipo | Arquivo ou referência | SHA-256 | Data/verificação |
|---|---|---|---|---|
| EV-01 | Certidões CREA, guarda restrita | A PREENCHER | A PREENCHER | A PREENCHER |
| EV-02 | Fontes normativas licenciadas, guarda restrita | A PREENCHER | A PREENCHER | A PREENCHER |
| EV-03 | Casos golden e cálculo independente | A PREENCHER | A PREENCHER | A PREENCHER |
| EV-04 | Resultados E01–E11 e logs | A PREENCHER | A PREENCHER | A PREENCHER |
| EV-05 | Relatório NC/reteste | A PREENCHER | A PREENCHER | A PREENCHER |
| EV-06 | Manifesto do código e hashes | A PREENCHER | A PREENCHER | A PREENCHER |
| EV-07 | Termo de decisão técnica assinado | A PREENCHER | A PREENCHER | A PREENCHER |

## G. Decisão provisória
**ESTADO: NÃO AVALIADO / PENDENTE DE EVIDÊNCIAS PROFISSIONAIS.**
**Assinatura: NÃO COLETADA.** **ART: NÃO VERIFICADA.** **LIBERAÇÃO PARA USO NORMATIVO: NÃO AUTORIZADA.**
Finalizar somente mediante verificação externa das evidências, decisão explícita do responsável e termo C13 autenticado.
