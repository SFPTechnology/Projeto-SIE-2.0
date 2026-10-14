# Plano de Correção Obrigatória — Liberação para Uso Real
### Sistema de dimensionamento NBR 5410 / EDP São Paulo

**Origem:** seção 5 ("Condicionantes para liberação") do Relatório de Validação Técnica.
**Critério de ordenação:** **dependência de implementação** (não severidade). Cada item é posicionado onde seus *insumos* já existem.
**Regime de execução:** **phase-gated** — uma fase só inicia quando a anterior está concluída **e validada** pelos seus critérios de aceite. Pular fase é a principal fonte de retrabalho.

---

## 1. Por que a ordem difere da §5

A §5 ordenou por **risco** (o defeito inseguro primeiro). Este plano ordena por **fluxo de dados**, porque a cadeia do sistema é encadeada:

```
classificação de carga → demanda → categoria/entrada → divisão de circuitos
   → IB por circuito → condutores → queda de tensão → proteção/DR
   → balanceamento de fases → aterramento → memorial
```

Consequência prática: o item **mais crítico** da §5 (Tabela 001/002) **não** é o passo 1 deste plano, porque validar a sub-categoria exige a **corrente de demanda correta**, que depende da classificação de carga. O **dado** da tabela pode ser preparado já (fora da fila); sua **validação** gateia na Fase 1. Nenhuma prioridade se perde — ver mapa abaixo.

### Mapa de rastreabilidade §5 → Plano

| §5 (prioridade) | Passo neste plano | Observação |
|---|---|---|
| #2 tipo_aparelho obrigatório **[CRÍTICO]** | **0.1** | é o gate de entrada — vai para o início |
| #3 mapa tipo→grupo **[ALTO]** | **0.2** | junto da classificação |
| #8 FP + arredondamento **[MÉDIO]** | **0.3** (FP) / **1.3** (arred.) | correção de parâmetro |
| #1 Tabela 001/002 **[CRÍTICO]** | **1.2** | dado pode ser preparado já; validação gateia na 1.1 |
| #4 Divisão de Circuitos + DR **[ALTO]** | **Fase 2** | keystone da 2ª metade |
| #5 condutores + queda de tensão **[ALTO]** | **Fase 3** | depende dos circuitos |
| #6 balanceamento de fases **[ALTO]** | **4.1** | depende de IB+ligação por circuito |
| #7 aterramento/equipotencialização **[MÉDIO]** | **4.2** | PE por circuito + BEP |
| #9 memorial/unifilar/quadro **[MÉDIO]** | **Fase 5** | consome tudo |

---

## FASE 0 — Saneamento da entrada e da classificação *(fundação)*

> **Por que primeiro:** demanda, categoria e tudo a jusante consomem a classificação de carga. Erro aqui propaga para todo o sistema. Nenhum outro módulo deve ser tocado antes desta fase fechar.

### Passo 0.1 — `tipo_aparelho` obrigatório + bloqueio de cálculo  `[CRÍTICO]`
- **Pré-requisito:** nenhum.
- **Ações:** tornar `tipo_aparelho` (tipo EDP) campo obrigatório em toda carga adicional; impedir o cálculo de demanda enquanto existir carga sem tipo; converter o diagnóstico atual `ERR-CARGA-SEM-TIPO-APARELHO` em bloqueio efetivo (não apenas aviso).
- **Critério de aceite:** salvar uma carga sem tipo é impossível; o ar-condicionado de 3.516 VA passa a ter tipo e some o ERRO.

### Passo 0.2 — Correção do mapa tipo→grupo de demanda  `[ALTO]`
- **Pré-requisito:** 0.1.
- **Ações:** corrigir o roteamento: **motor / bomba → grupo g**; **forno elétrico → grupo d**; **ar-condicionado → grupo f**. Revisar a tabela completa tipo→grupo (a–i) item a item.
- **Critério de aceite:** motor e bomba de piscina aparecem no grupo g (maior 1,0 + restante 0,5), sem linha espúria no grupo i; forno + micro-ondas somam 2 aparelhos no grupo d (FD 0,70); ar-condicionado no grupo f.

### Passo 0.3 — Correção dos fatores de potência por tipo  `[MÉDIO]`
- **Pré-requisito:** nenhum (paralelo a 0.1/0.2).
- **Ações:** ajustar `forno_eletrico` para FP 1,0 e `iluminacao_descarga` para FP 0,55, conforme a fonte EDP declarada.
- **Critério de aceite:** os FPs por tipo batem com a norma EDP v06.

### Passo 0.4 — Captura da tensão de placa por carga  `[deriva de F-05]`
- **Pré-requisito:** nenhum.
- **Ações:** capturar a tensão nominal de cada carga (não assumir 220 V para todo TUE). Default por tipo, mas editável por carga.
- **Critério de aceite:** um micro-ondas declarado 127 V não é mais tratado como 220 V bifásico.
- **Nota:** insumo necessário para o IB correto (Fase 2.3) e para o condutor (Fase 3).

**🚪 Gate da Fase 0:** todas as cargas classificadas e com tensão; nenhuma pendência de tipo.

---

## FASE 1 — Demanda e entrada *(consome Fase 0)*

### Passo 1.1 — Revalidação da demanda por grupo
- **Pré-requisito:** Fase 0.
- **Ações:** reexecutar a demanda com a classificação corrigida; confirmar que grupos f e g passam a existir e que o AC entra na conta.
- **Critério de aceite:** DT recalculado e completo (com AC ≈ 25,7 kVA na configuração atual); D1/D3 coerentes; demanda reproduzível a partir das tabelas.

### Passo 1.2 — Correção da Tabela 001/002 + entrada  `[CRÍTICO]`
- **Pré-requisito:** dado pode ser preparado já; **validação** gateia em 1.1.
- **Ações:** substituir a linha única inconsistente pela **escada completa** da norma EDP (sub-categorias da Categoria T: T2…T10), com **pares disjuntor ↔ seção válidos** e rótulos coerentes com a categoria. Recalcular sub-categoria/disjuntor/condutor da entrada.
- **Critério de aceite:** para a corrente de demanda correta, a entrada resolve em sub-categoria coerente (ex.: T2 para ~58–67 A) com `In ≤ Iz` satisfeito; **nunca** disjuntor 150 A com 25 mm². Validação obrigatória da condição `IB ≤ In ≤ Iz` na saída.
- **Pendência de dado:** valores oficiais T2…T10 — ver §"Informações necessárias".

### Passo 1.3 — Arredondamento de exibição da corrente  `[MÉDIO]`
- **Ações:** exibir a corrente de demanda com casas decimais adequadas (ex.: 58,3 A).
- **Critério de aceite:** sem dízimas na interface.

**🚪 Gate da Fase 1:** entrada dimensionada de forma **segura e completa**; remove o Bloqueio A da validação.

---

## FASE 2 — Divisão de Circuitos *(keystone — consome Fase 1)*  `[ALTO]`

> **Por que aqui:** é o módulo ausente que destrava toda a 2ª metade. Sem circuitos terminais reais, não há o que dimensionar, proteger ou aterrar.

### Passo 2.1 — Entidade `Circuito` e roteamento de cargas
- **Pré-requisito:** Fase 1.
- **Ações:** criar a entidade `Circuito`; alocar cargas em circuitos conforme NBR 5410 9.5.3: **iluminação separada de TUG**; **circuito exclusivo** para cada TUE e para todo equipamento > 10 A; agrupar respeitando limites de carga/pontos; tipar cada circuito (iluminação / TUG seca / TUG molhada / TUE dedicado / carga fixa).
- **Critério de aceite:** nenhum circuito mistura iluminação e TUG; chuveiro/motor/AC em circuitos próprios; cada carga em exatamente um circuito.

### Passo 2.2 — Marcação de DR por circuito  *(parte de §5 #4)*
- **Pré-requisito:** 2.1.
- **Ações:** marcar `requer_DR` (≤ 30 mA) em todo circuito que sirva área molhada (banheiro, cozinha, área de serviço, lavanderia) ou externa, conforme NBR 5410 5.1.3.2.
- **Critério de aceite:** circuitos de banheiros (chuveiro/hidromassagem), cozinha e área externa do projeto saem com DR obrigatório marcado.

### Passo 2.3 — Tensão por circuito e IB definitivo
- **Pré-requisito:** 2.1 + Fase 0.4.
- **Ações:** selecionar a tensão de cada circuito (a partir da tensão de placa das cargas) e recalcular IB por circuito com a ligação correta (mono/bi/tri).
- **Critério de aceite:** IB por circuito reflete a tensão real das cargas; saída pronta para o dimensionamento de condutores.

**🚪 Gate da Fase 2:** circuitos terminais reais, tipados, com DR e IB corretos.

---

## FASE 3 — Dimensionamento elétrico por circuito *(consome Fase 2)*  `[ALTO]`

### Passo 3.1 — Captura de dados de instalação por circuito
- **Pré-requisito:** Fase 2.
- **Ações:** capturar por circuito: **método de instalação** (referências B1, B2, etc.), **temperatura ambiente**, **agrupamento de circuitos** e **comprimento**.
- **Critério de aceite:** todo circuito tem os quatro dados; sem eles, o dimensionamento não roda.

### Passo 3.2 — Dimensionamento de condutores
- **Pré-requisito:** 3.1.
- **Ações:** aplicar seção mínima (NBR 5410 Tab. 47 — 1,5 mm² iluminação, 2,5 mm² força) e ampacidade (Tab. 36–39) com fatores de correção de temperatura e agrupamento; garantir `IB ≤ Iz`.
- **Critério de aceite:** seção de cada circuito satisfaz ampacidade corrigida e piso mínimo.
- **Pendência de dado:** tabelas de ampacidade e fatores — ver §"Informações necessárias".

### Passo 3.3 — Queda de tensão
- **Pré-requisito:** 3.2 (usa comprimento da 3.1).
- **Ações:** calcular a queda acumulada por circuito; reiterar a seção quando a queda — não a ampacidade — governar.
- **Critério de aceite:** queda dentro do limite NBR 5410 6.2.7; seção ajustada onde necessário.
- **Pendência de dado:** percentuais e ponto de referência exatos — ver §"Informações necessárias".

### Passo 3.4 — Proteção contra sobrecorrente por circuito
- **Pré-requisito:** 3.2/3.3.
- **Ações:** dimensionar o dispositivo de proteção de cada circuito com `IB ≤ In ≤ Iz` **e** `I₂ ≤ 1,45·Iz`; verificar coordenação e capacidade de interrupção (Icu) vs. curto presumido.
- **Critério de aceite:** as duas inequações satisfeitas em todos os circuitos; Icu compatível.

**🚪 Gate da Fase 3:** condutores e proteções de circuito dimensionados e verificados.

---

## FASE 4 — Sistema *(consome Fase 3)*

### Passo 4.1 — Balanceamento de fases  `[ALTO]`
- **Pré-requisito:** circuitos com IB e ligação (Fase 2/3).
- **Ações:** distribuir os circuitos entre as fases A/B/C minimizando o desequilíbrio (substituir o "tudo na Fase A" provisório).
- **Critério de aceite:** corrente por fase aproximadamente equilibrada (premissa do cálculo de corrente de demanda passa a ser real).

### Passo 4.2 — Aterramento e equipotencialização  `[MÉDIO]`
- **Pré-requisito:** Fase 3.
- **Ações:** definir o esquema de aterramento (na entrada EDP, tipicamente **TN-C-S** `[VERIFICAR]`); dimensionar condutor de proteção (PE) por circuito; especificar o barramento de equipotencialização principal (BEP) e a equipotencialização suplementar em áreas molhadas (NBR 5410 6.4).
- **Critério de aceite:** todo circuito com PE; BEP definido; áreas molhadas com equipotencialização suplementar.

**🚪 Gate da Fase 4:** instalação eletricamente completa e equilibrada, com proteção contra choque íntegra (DR + PE + equipotencialização).

---

## FASE 5 — Saída auditável *(consome tudo)*  `[MÉDIO]`

### Passo 5.1 — Memorial, quadro de cargas e unifilar
- **Pré-requisito:** Fases 0–4.
- **Ações:** gerar memorial de cálculo rastreável (entradas, fórmulas, normas, etapas), quadro de cargas por circuito e diagrama unifilar.
- **Critério de aceite:** documento auditável suficiente para conferência e base de ART.

---

## 2. Marcos de reavaliação (re-rodar a validação)

| Após | Reverifica | Remove |
|---|---|---|
| Fase 1 | itens 3, 4, 5, 6, 7 da validação | **Bloqueio A** (entrada insegura) |
| Fase 4 | itens 8 a 14 | **Bloqueio B** (2ª metade ausente) |
| Fase 5 | item 15 + validação integral | habilita parecer de liberação |

> Liberação para uso real **somente** após a Fase 5 e nova validação técnica integral, com ART do engenheiro responsável.

---

## 3. Premissas assumidas (a confirmar com o desenvolvedor)

Estas premissas vêm da observação das gravações e podem alterar o **esforço** (não a ordem) de alguns passos:

1. Normas estão armazenadas como **configuração editável** (não hardcoded) — confirmado pelas tabelas EDP editáveis na tela.
2. **Não existe** entidade `Circuito` persistida; o IB é calculado sobre o andaime provisório (um pseudo-circuito por carga). → Fase 2 é greenfield.
3. **Não há** captura de comprimento, método de instalação, temperatura ou agrupamento em nenhuma tela. → Fase 3.1 é greenfield.
4. **Não há** tratamento de DR, PE ou aterramento. → Fases 2.2 e 4.2 são greenfield.
5. A tensão por carga **não** é capturada hoje (TUE assume 220 V). → Fase 0.4 é novo campo.

Se alguma premissa estiver errada, o passo correspondente muda de "greenfield" para "refatoração", o que reduz/altera o escopo.
