---
name: f01-engenharia-fontes
description: "Verificação de fontes normativas oficiais BT ABNT, NR-10 e padrões EDP com proveniência celular"
---

# f01-engenharia-fontes

Verificação de fontes normativas oficiais BT ABNT, NR-10 e padrões EDP com proveniência celular.

## Procedimento obrigatório
1. Primeiro leia `docs/sie-orchestrator/NEXT_ACTION.md`, `docs/implantacao-sie-2-0/F01/QA3_MULTIAGENTES_PLANO_EXECUCAO.md` e o código real. Escreva hipóteses e ameaças.
2. Cite a origem de **cada** número/regra, com data, edição, método, unidade e célula. Diferencie documentação derivada de fonte primária. Bloqueie inferências.
3. Faça testes independentes e de regressão F00 antes/depois das alterações; use banco temporário, não DB remoto. Corrija inconsistências no mesmo ramo.
4. Registre artefato, hash/commit, teste/CI, resultado e achados; peça revisão cruzada **depois** de congelar sua primeira versão.
5. Nunca declare F01 DONE/F02 READY antes de a checagem automática e a validação técnica independente sustentarem TODOS os seis gates. Impossibilidade ou ausência de fonte = BLOCKED documentado.

## Método especializado
Defina para cada documento código, edição, errata, edição da cópia, vigência, jurisdição, tipo de instalação, abrangência, licença, hash, cláusula, página, linha, coluna, nota e unidade. Consulte fonte oficial autorizada e registre as evidências exatas sem redistribuir texto protegido. Classifique dados como NÃO VERIFICADOS, PARCIAIS ou verificados por duas leituras externas. Para EDP confirme área de concessão; para NR-10 distinga segurança ocupacional de dimensionamento; NBR 5419 somente no recorte SPDA. Rca, XL e Rdc20 não são intercambiáveis.

## Entrega da skill
Salvar um registro `SKILL-f01-engenharia-fontes.md` no pacote individual do agente, com source-ref, rastreabilidade, resultados de testes, avaliação de risco, blockers e links CI. Toda afirmação de conformidade requer evidência verificável além da execução da skill.
