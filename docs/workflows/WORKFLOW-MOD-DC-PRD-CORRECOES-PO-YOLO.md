# Workflow YOLO - Correcao do PRD MOD-DC apos validacao PO

**Produto:** SIE - Sistema de Instalacoes Eletricas  
**Modulo:** MOD-DC v3.0  
**Documento alvo:** `docs/prd/PRD-MOD-DC-modulo-dimensionamento-condutores.md`  
**Documento fonte:** `Arquivos_Diversos/PROMPT-DIMENSIONAMENTO-CONDUTORES-v3.md`  
**Modo:** YOLO documentado - execucao autonoma, sem perguntas ao usuario, respeitando autoridade dos agentes  
**Criado por:** Morgan (@pm)  
**Data:** 2026-07-12  
**Status:** Draft operacional para execucao

---

## 1. Objetivo

Corrigir o PRD MOD-DC para remover os bloqueios apontados por @po e deixa-lo pronto para nova validacao PO e posterior detalhamento por @sm.

O workflow nao cria stories e nao implementa codigo. O escopo e exclusivamente documental: alinhar o PRD ao prompt-base sem inventar requisitos.

---

## 2. Entradas Obrigatorias

| Entrada | Caminho | Uso |
|---|---|---|
| PRD atual | `docs/prd/PRD-MOD-DC-modulo-dimensionamento-condutores.md` | Documento a corrigir |
| Prompt-base | `Arquivos_Diversos/PROMPT-DIMENSIONAMENTO-CONDUTORES-v3.md` | Fonte de verdade funcional/normativa |
| Validacao PO | Mensagem/veredito @po `CONDITIONAL` | Lista de lacunas a resolver |
| Constitution | `.aiox-core/constitution.md` | Regras: No Invention, Agent Authority, Story-Driven |

---

## 3. Saidas Esperadas

| Saida | Caminho | Conteudo |
|---|---|---|
| PRD corrigido | `docs/prd/PRD-MOD-DC-modulo-dimensionamento-condutores.md` | PRD alinhado aos 5 pontos PO |
| Registro de alteracao | Secao final do PRD | Checklist de correcoes PO com status |
| Handoff arquitetural | Secao `AD-DC-01` no PRD | Decisao ainda pendente ou decisao recebida de @architect |
| Nova validacao solicitada | Mensagem final do executor | Pedido explicito para @po revalidar |

---

## 4. Regras de Execucao YOLO

1. Nao perguntar ao usuario durante a execucao.
2. Nao criar requisitos fora do prompt-base.
3. Nao resolver decisao arquitetural em nome de @architect.
4. Nao criar stories finais; isso fica para @sm apos validacao @po.
5. Toda alteracao deve apontar para uma das fontes:
   - `PROMPT-DIMENSIONAMENTO-CONDUTORES-v3.md`
   - validacao PO
   - realidade brownfield observada no repositorio
   - decisao formal de @architect, se existir
6. Se a decisao @architect nao existir, o PRD deve continuar `Draft`, mas com o bloqueio AD-DC-01 bem especificado.

---

## 5. Agentes e Autoridade

| Agente | Responsabilidade no workflow | Pode editar? | Observacao |
|---|---|---|---|
| @pm Morgan | Corrigir estrutura do PRD, transcrever requisitos, preparar handoffs | Sim | Dono deste workflow |
| @architect Aria | Decidir runtime/API AD-DC-01 | Sim, somente decisao arquitetural | PM nao pode decidir por Aria |
| @po Pax | Revalidar PRD corrigido | Nao durante execucao PM | Gate de aceite |
| @sm River | Criar stories depois do PASS PO | Nao neste workflow | Bloqueado ate novo PASS |

---

## 6. Correcoes Obrigatorias

### C1 - Stack real do app e AD-DC-01

**Problema PO:** o PRD justifica a divergencia entre prompt-base e stack real, mas ainda precisa de decisao @architect antes de DC-1/DC-7.

**Acao YOLO PM:**

1. Manter a observacao brownfield sobre TanStack Start + TypeScript + React/Carbon + Supabase.
2. Transformar `AD-DC-01` em gate formal com:
   - opcoes validas;
   - criterio de decisao;
   - impactos esperados;
   - status `PENDENTE-ARQUITETURA`;
   - regra: DC-1 e DC-7 nao podem iniciar sem decisao.
3. Adicionar handoff objetivo para @architect dentro do PRD.

**Nao fazer:** escolher TypeScript, Python ou hibrido como decisao final sem documento/retorno do @architect.

**Criterio de aceite:**

- `AD-DC-01` aparece como bloqueio rastreavel.
- PRD nao permite iniciar DC-1/DC-7 antes da decisao.

---

### C2 - FR16 inconsistente com Pydantic

**Problema PO:** FR16 ainda fala em Pydantic, mas o PRD deixou runtime/API em aberto.

**Acao YOLO PM:**

Substituir FR16 por texto neutro de contrato:

```markdown
**FR16:** Publicar contratos formais de entrada (`CircuitoParaDimensionamento`) e saida (`ResultadoDimensionamento`) conforme §14 do documento-base, preservando os campos, secoes por criterio, verificacoes tri-estado e objeto `rastreio`. A representacao tecnica concreta (Pydantic, Zod/TypeScript ou equivalente) deve seguir a decisao AD-DC-01, sem alterar o contrato funcional.
```

**Criterio de aceite:**

- FR16 nao assume Pydantic como tecnologia obrigatoria.
- Os nomes `CircuitoParaDimensionamento` e `ResultadoDimensionamento` permanecem.
- A decisao tecnica fica vinculada a AD-DC-01.

---

### C3 - CA-DC-01...CA-DC-25 completos no PRD

**Problema PO:** criterios de aceite foram apenas referenciados, fragilizando story drafting.

**Acao YOLO PM:**

1. Criar uma tabela integral `CA-DC-01` a `CA-DC-25` na secao de criterios de aceite do PRD.
2. Transcrever do prompt-base sem alterar valor numerico, status ou verificacao.
3. Manter os gates destacados:
   - CA-DC-09
   - CA-DC-23
   - CA-DC-25
4. Cada story DC-1...DC-10 deve continuar referenciando seu subconjunto.

**Criterio de aceite:**

- `rg "CA-DC-" PRD` mostra todos os ids de `CA-DC-01` a `CA-DC-25`.
- Nenhum criterio depende apenas de "ver documento-base".

---

### C4 - Catalogo minimo de erros completo

**Problema PO:** faltam itens explicitos do catalogo central, como `ERRO-METODO-AUSENTE`, `ERRO-AGRUPAMENTO-NAO-TABELADO` e `INC-07`.

**Acao YOLO PM:**

1. Criar ou expandir uma secao `Catalogo minimo de erros` no PRD.
2. Transcrever do prompt-base:
   - `ERRO-TENSAO-AUSENTE`
   - `ERRO-ISOLACAO-AUSENTE`
   - `ERRO-METODO-AUSENTE`
   - `ERRO-MATERIAL-NAO-ADMITIDO`
   - `ERRO-LINHA-INCOMPATIVEL`
   - `ERRO-CONSULTA-INCOMPLETA`
   - `ERRO-TABELA-INCOMPLETA`
   - `ERRO-FATOR-NAO-ENCONTRADO`
   - `ERRO-AGRUPAMENTO-NAO-TABELADO`
   - `ERRO-COR-FUNCAO`
   - `INC-07`
   - `REQUER-ESTUDO-PARALELO`
   - `PENDENTE-I2`
   - `VERIFICAR-NEUTRO-HARMONICAS`
3. Registrar regra: nenhum erro vira alerta, nenhum alerta suprime pendencia.

**Criterio de aceite:**

- Todos os codigos acima aparecem no PRD.
- `ERRO-METODO-AUSENTE`, `ERRO-AGRUPAMENTO-NAO-TABELADO` e `INC-07` aparecem explicitamente no catalogo central.

---

### C5 - Fontes, hierarquia, premissas e glossario completos

**Problema PO:** o PRD resumiu demais as fontes, hierarquia, premissas e glossario do prompt-base.

**Acao YOLO PM:**

Adicionar uma secao antes de `Requisitos`, ou expandir a introducao, com quatro blocos:

1. **Fontes e limites de conhecimento**
   - NBR 5410 chunks;
   - PT.DT.PDN.00068 v09 chunks;
   - Guia EM/04_condutores como material explicativo com numeracao 1997 proibida;
   - MOD-DC-v2 como artefato historico, nao fonte normativa;
   - proibicao de internet, catalogos e normas nao anexadas;
   - lacunas viram `[VERIFICAR]`.

2. **Hierarquia e aplicabilidade**
   - NBR 5410 como referencia geral;
   - EDP apenas para area/concessao/ramal de entrada nas condicoes do prompt;
   - requisitos cumulativos quando aplicaveis;
   - exemplos explicativos nao viram regra;
   - conflitos viram `CONFLITANTE` ou `[VERIFICAR]`.

3. **Premissas operacionais**
   - sistema-alvo trifasico estrela 220/127 V, aceitando mono/bi/tri;
   - 60 Hz;
   - regime permanente e fator de carga 100%;
   - cabos ate 0,6/1 kV, nao armados;
   - circuitos chegam com IB calculado;
   - VA usado diretamente;
   - tensao jamais assumida.

4. **Glossario**
   - IB, Iz, In, I2;
   - metodo de referencia;
   - condutores carregados;
   - FCT/FCS/FRS/FCA;
   - PE/PEN;
   - TH3.

**Criterio de aceite:**

- Os quatro blocos existem no PRD.
- O PRD deixa de depender apenas das referencias finais para preservar regras de fonte.

---

## 7. Sequencia de Execucao

### Fase 0 - Preparacao

```bash
rg -n "FR16|AD-DC-01|CA-DC-|Catalogo|FONTES|HIERARQUIA|PREMISSAS|GLOSS" docs/prd/PRD-MOD-DC-modulo-dimensionamento-condutores.md
rg -n "## 8|## 9|## 10|## 11|## 14|## 23|## 25|CA-DC-01|CA-DC-25" Arquivos_Diversos/PROMPT-DIMENSIONAMENTO-CONDUTORES-v3.md
```

Resultado esperado: localizar os trechos fonte e os pontos de insercao no PRD.

### Fase 1 - Corrigir AD-DC-01 e FR16

1. Atualizar `AD-DC-01`.
2. Atualizar FR16 para contrato neutro.
3. Verificar que `Pydantic` aparece apenas como opcao condicionada pela decisao arquitetural ou citacao do prompt-base.

### Fase 2 - Inserir contexto normativo completo

1. Adicionar fontes e limites.
2. Adicionar hierarquia e aplicabilidade.
3. Adicionar premissas.
4. Adicionar glossario.

### Fase 3 - Inserir catalogo de erros

1. Criar secao propria apos requisitos ou antes dos criterios de aceite.
2. Transcrever codigos minimos.
3. Ligar catalogo aos FRs e stories DC-2/DC-6/DC-10.

### Fase 4 - Transcrever CA-DC-01...25

1. Substituir referencia resumida por tabela integral.
2. Manter destaques de gate.
3. Preservar numeracao, valores e verificacao do prompt-base.

### Fase 5 - Atualizar checklist PM/PO no PRD

1. Marcar cada item de correcao PO como `RESOLVIDO` ou `BLOQUEADO POR AD-DC-01`.
2. Manter status do PRD como `Draft` ate decisao @architect e nova validacao @po.

---

## 8. Validacoes Automatizadas

Executar apos edicao:

```bash
rg -n "FR16|AD-DC-01|PENDENTE-ARQUITETURA|ERRO-METODO-AUSENTE|ERRO-AGRUPAMENTO-NAO-TABELADO|INC-07" docs/prd/PRD-MOD-DC-modulo-dimensionamento-condutores.md
rg -n "CA-DC-0[1-9]|CA-DC-1[0-9]|CA-DC-2[0-5]" docs/prd/PRD-MOD-DC-modulo-dimensionamento-condutores.md
rg -n "Fontes e limites|Hierarquia e aplicabilidade|Premissas operacionais|Glossario" docs/prd/PRD-MOD-DC-modulo-dimensionamento-condutores.md
```

Checklist manual:

- [ ] FR16 nao fixa Pydantic como obrigatorio.
- [ ] AD-DC-01 bloqueia DC-1/DC-7.
- [ ] CA-DC-01...25 estao integrais.
- [ ] Catalogo de erros contem todos os codigos minimos.
- [ ] Fontes/hierarquia/premissas/glossario preservam o prompt-base.
- [ ] Nao ha novos requisitos fora do prompt-base.

---

## 9. Gate de Conclusao

### PASS

O workflow e considerado concluido quando:

- os cinco pontos PO foram corrigidos no PRD;
- unica pendencia restante e `AD-DC-01`, caso @architect ainda nao tenha decidido;
- o PRD esta pronto para nova validacao @po.

### BLOCK

Bloquear e escalar se:

- a correcao exigir escolher runtime/API sem @architect;
- houver conflito entre prompt-base e realidade brownfield que altere requisito funcional;
- faltar trecho fonte para transcrever criterios CA-DC ou catalogo de erros;
- a alteracao exigir criar story ou implementar codigo.

---

## 10. Comando de Execucao Recomendado

```bash
@aiox-pm *yolo
@aiox-pm corrigir docs/prd/PRD-MOD-DC-modulo-dimensionamento-condutores.md \
  --source=Arquivos_Diversos/PROMPT-DIMENSIONAMENTO-CONDUTORES-v3.md \
  --workflow=docs/workflows/WORKFLOW-MOD-DC-PRD-CORRECOES-PO-YOLO.md
```

Depois da correcao:

```bash
@aiox-po verificar docs/prd/PRD-MOD-DC-modulo-dimensionamento-condutores.md \
  contra Arquivos_Diversos/PROMPT-DIMENSIONAMENTO-CONDUTORES-v3.md
```

---

## 11. Proximo Passo

Executar este workflow para corrigir o PRD. Em seguida, solicitar nova validacao @po. Se @po mantiver `CONDITIONAL` apenas por AD-DC-01, acionar @architect para decisao formal antes de qualquer story DC-1/DC-7.
