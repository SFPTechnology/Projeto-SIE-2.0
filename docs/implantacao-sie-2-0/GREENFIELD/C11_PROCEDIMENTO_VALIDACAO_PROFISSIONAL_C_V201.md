# C11 — Procedimento de validação e aceite técnico elétrico | SIE 2.0 — Bloco C

**Estado:** MODELO DE PROCEDIMENTO — NÃO HOMOLOGADO, NÃO ASSINADO.
**Emissão inicial:** 28/10/2026. **Repositório:** SFPTechnology/Projeto-SIE-2.0.
**Ramo:** `feat/v201-bloco-c-dominio-eletrico`. **PR:** https://github.com/SFPTechnology/Projeto-SIE-2.0/pull/11.
**Versão de código de referência:** `a82776203db9b1d60dd49cbbd6602a47093f9df1` (5 workflows de CI PASS verificados na data da emissão). Se houver novos commits, atualizar SHA e repetir ensaios.
**Natureza do aceite:** validação das funções do **software**, não aprovação automática de projetos elétricos, laudos de campo ou instalações físicas.

## 1. Responsável e habilitação — gate H0 (sem presunção)
1. O profissional que manifestou intenção de assumir a análise deve **confirmar nome, registro no CREA/UF, condição regular e atribuições efetivas**. Nunca completar esses campos por inferência ou memória.
2. Obter no CREA competente: (a) Certidão de Registro e Quitação e (b) Certidão de Registro e Anotações (com atribuições); validar a autenticidade e validade nos portais oficiais e preservar os documentos em repositório restrito, registrando somente protocolo/hash no repositório de código. Quando CREA-SP, iniciar em https://www.creasp.org.br/servico/.
3. Comparar as atribuições **específicas** com o escopo do parecer: análise de cálculos, regras de projeto de instalações elétricas BT, sistemas de proteção, concessionária, validação de software de engenharia. Em caso de dúvida, protocolar consulta de atribuições no Conselho e bloquear assinatura até manifestação oficial.
4. Examinar se há prestação de serviço técnico que exija ART, perante a Lei 6.496/1977, a Resolução Confea 1.137/2023 e demais regras aplicáveis. ART, quando exigível, deve ser registrada no momento legalmente adequado; **não inventar ART**. Decisão documentada: OBRIGATÓRIA / NÃO APLICÁVEL COM FUNDAMENTO / PENDENTE DE CONSULTA.
5. Autorresponsabilidade não elimina auditoria técnica: registrar ensaios com evidência reproduzível e, sempre que possível, contraprova independente por revisor de QA.

**Saída H0:** `VALIDATED` somente após certidões autenticadas, atribuições correspondentes, decisão fundamentada de ART e declaração explícita de inexistência de impedimento. Caso contrário `PENDING`.

## 2. Definir fronteiras e fontes — gate H1
- Identificar exatamente o commit SHA, artefatos e motores sob teste; registrar ambiente, dependências, dataset, versão de cálculo e hash dos resultados.
- Validar **documentos oficiais efetivamente utilizados**, edição, corrigendas, licença, regra local e vigência. Não considerar citações ou nomes dos registros JSON como prova de licença/conformidade.
- Matrizes de referência: ABNT NBR 5410 (condições de aplicação), requisitos da concessionária competente, NR-10 quando pertinente e NBR 5419 somente para funcionalidades de SPDA incluídas no escopo.
- P03 e P06, tabelas confiáveis de Rca/XL, DR/DPS, curto-circuito/I2, aterramento e limites normativos **não podem receber PASS sem parâmetros verificáveis**.
- Classificar funcionalidades como **IMPLEMENTADA E VALIDADA**, **IMPLEMENTADA COM RESTRIÇÕES (bloqueio operacional)** ou **NÃO IMPLEMENTADA / FORA DE ESCOPO APROVADO**. Uma restrição nunca pode ser escondida como `conforme`.

## 3. Plano de ensaios — gate H2
Cada grupo E01–E11 exige mínimo: (i) entrada explicitamente reproduzível; (ii) resultado esperado independente; (iii) resultado observado; (iv) erro/tolerância aceitos; (v) fonte de regra e edição; (vi) caso de borda e caso negativo; (vii) arquivos de logs, snapshot e SHA; (viii) decisão e assinatura do avaliador.

| Código | Verificação | Critério mínimo obrigatório |
|---|---|---|
| E01 | Iluminação e TUG | Áreas, perímetros, tipologias, ambientes especiais e limites de regra; sem valores presumidos |
| E02 | TUE, FP e topologia | VA/W/BTU/h devidamente identificados; tensões ausentes bloqueiam dimensionamento; monofásico/trifásico explícitos |
| E03 | Demanda, divisão e equilíbrio | Fatores justificados e versões, carga por fase e separação de circuitos testadas |
| E04 | Condutores e correções | Método de instalação, material, temperatura, agrupamento, catálogos e fator de correção rastreáveis |
| E05 | Queda de tensão | Comprimento, FP, Rca/XL, topologia e percentual com limites normativos aplicáveis; sem R/X confiáveis, pendente |
| E06 | Sobrecarga, curto e I2 | Ib ≤ In ≤ Iz, atuação I2, Icc, poder de interrupção e seletividade dentro do escopo |
| E07 | DR e DPS | Sensibilidade, coordenação, localização, hipóteses e exceções rastreáveis |
| E08 | Aterramento e PE | TT/TN/IT, condutor de proteção, neutralização, proteção contra choque e continuidade conforme escopo |
| E09 | Padrão de entrada/concessionária | Edição oficial e aplicabilidade territorial, demanda e enquadramento, cada valor rastreável |
| E10 | Legado / 7 campos de engenharia | `fator_potencia`, `fator_potencia_iluminacao`, `fator_potencia_tug`, `dimensionamento_condutores_overrides.overrides`, `dimensionamento_condutores_resultado.secoes`, `dimensionamento_disjuntores_overrides.overrides`, `queda_tensao_config.config`: decidir uso, arquivo ou bloqueio, sem promoção automática dos resultados antigos |
| E11 | Falhas, regressões e fontes | Negativos de nulos/valores inválidos, desatualização de regra, imutabilidade e deriva de hashes |

**Atenção aos dados reais do legado:** 41 alturas iguais a zero, 4 cargas com tensão não declarada, 2 trifásicas sem topologia comprovada e 10 eventos históricos com referência órfã. Nenhum dado será preenchido por inferência. Todos os resultados legados mantêm `NOT_EVALUATED` até avaliação.

## 4. Procedimento operacional
1. Executar testes unitários, de integração, de contrato, PostgreSQL 17 e Chromium no **mesmo commit** e arquivar links de execução.
2. Realizar contraprovas por planilha/cálculo independente para todos os casos golden selecionados. Não usar somente o próprio algoritmo como oráculo.
3. Identificar falhas por criticidade: **CRÍTICA** (pode produzir indicação indevida de conformidade/segurança), **ALTA** (erro de dimensionamento), **MÉDIA** (inconsistência/traço), **BAIXA** (cosmética).
4. Corrigir e refazer ensaios afetados; acompanhar pela chave `case_id + rule_revision + commit_sha`.
5. Preencher o dossiê C12 com evidências reais, não completar resultados por expectativa.
6. Firmar termo C13 com uma das decisões: **APROVADO NO ESCOPO DESCRITO**, **APROVADO COM RESTRIÇÕES EXPRESSAS**, **REPROVADO** ou **NÃO AVALIADO**. Não usar `APROVADO` como default.
7. Vincular parecer assinado ao SHA final e ao manifesto de evidências. Alterações posteriores de regra/motor invalidam o aceite dos trechos afetados.

## 5. Gate para encerramento do Bloco C
- `H0`: registro e atribuições verificados.
- `H1`: escopo, fontes e limites verificados.
- `H2`: E01–E11 executados e decididos, com resultados críticos resolvidos ou funcionalidades críticas tecnicamente bloqueadas e excluídas de modo explícito do escopo de uso.
- `H3`: termo assinado pelo profissional, autenticável e vinculado ao SHA/versões.
- `GC-DEV`: CI e implementação de escopo aprovados, distinguindo-se de `GC-INT`.
- `GC-INT`: somente após migração/homologação isolada com autorização específica, RLS real, reconciliação e restauração testadas.
- `GC=PASS`: permitido exclusivamente após cumprimento dos requisitos contratuais aplicáveis e validação independente; NÃO resulta de editar arquivos Markdown/JSON.

**Limites:** Nenhuma assinatura humana, ART, validação CREA ou conformidade técnica está atestada neste procedimento. Nenhum merge, DDL/DML remoto ou liberação para produção decorre de sua publicação.

**Fontes oficiais de procedimento:** https://www.creasp.org.br/servico/ ; https://normativos.confea.org.br/Ementas/Visualizar?id=76099 ; https://supabase.com/docs/reference/javascript/auth-getuser .
