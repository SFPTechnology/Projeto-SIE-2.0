# EXEMPLO COMPLETO: Especificação de Slide Nível Elite

Este exemplo demonstra o nível de detalhe esperado em CADA slide de uma apresentação McKinsey-level.

---

# SLIDE 7 - CRESCIMENTO DO MERCADO BRASILEIRO DE IA

## METADADOS
- **Seção:** Análise de Mercado (Seção 2)
- **Posição:** Slide 7 de 45
- **Tipo:** Data Slide (Quantitative - Mixed: Line Chart + Table)
- **Tempo de apresentação:** 3 minutos
- **Audiência primária:** C-level executives (CEO, CFO, CTO)
- **Objetivo:** Demonstrar oportunidade de mercado e urgência de ação

---

## TÍTULO (ACTION TITLE)

**Texto:**
"Mercado brasileiro de IA crescerá 45% ao ano até 2027, superando média global em 1.7×"

**Formatação:**
- **Fonte:** Helvetica Neue Bold
- **Tamanho:** 28pt
- **Cor:** #003B5C (navy blue)
- **Alinhamento:** Esquerda
- **Posição:** Grid linha 1, colunas 1-12, margem 1.5cm da borda esquerda
- **Leading:** 1.2
- **Max width:** 24cm (wrap em 2 linhas se necessário)

---

## LAYOUT & GRID

### Grid Configuration
- Colunas: 12 (24cm total)
- Linhas: 8 (16cm total)
- Gutters: 0.5cm
- Margens: 2cm superior, 1.5cm lateral, 1.5cm inferior

### Zonas Visuais
```
┌────────────────────────────────────────────────┐
│ TÍTULO (action title)                     (1)  │
├──────────────────────────────┬─────────────────┤
│                              │  ┌───────────┐  │
│   GRÁFICO DE LINHAS          │  │ INSIGHTS  │  │
│   (crescimento temporal)     │  │   BOX     │  │
│                              │  └───────────┘  │
├──────────────────────────────┴─────────────────┤
│   TABELA DECOMPOSIÇÃO POR SETOR                │
├────────────────────────────────────────────────┤
│ Fontes: (1) IDC... (2) McKinsey...        [7]  │
└────────────────────────────────────────────────┘
```

---

## ELEMENTO 1: GRÁFICO DE LINHAS COMPARATIVO

**Tipo:** Line Chart (2 séries)
**Enumeração:** Gráfico 7
**Posição:** Colunas 1-8, Linhas 2-6
**Dimensões:** 16cm × 10cm

### Eixos

**Eixo X:**
- Anos: 2020, 2021, 2022, 2023, 2024, 2025E, 2026E, 2027E
- Fonte: Helvetica Neue Regular 11pt #6E6E6E
- "E" em itálico para estimados

**Eixo Y:**
- Escala: R$ 0bi, 5bi, 10bi, 15bi, 20bi, 25bi
- Título: "Receita (R$ bilhões)" vertical
- Gridlines: #E5E5E5 20% opacidade

### Séries de Dados

**Série 1 - Brasil:**
- Cor: #00A86B (verde)
- Linha: 3pt sólida
- Marcadores: círculos 8pt
- Dados: 2.3, 3.1, 4.8, 6.9, 9.2, 13.4, 17.8, 23.1 (R$ bi)

**Série 2 - Média Global:**
- Cor: #6E6E6E (cinza)
- Linha: 2pt tracejada
- Marcadores: quadrados 6pt
- Dados: 2.3, 2.9, 3.8, 4.9, 6.1, 7.8, 9.7, 11.9 (R$ bi)

**Área Sombreada:**
- Entre séries 2024-2027
- Cor: #00A86B 15% opacidade

**Legenda:**
- Posição: Dentro do gráfico, canto superior esquerdo
- Fundo: branco 85% opacidade
- Itens: "Brasil (CAGR: 45%)" | "Média Global (CAGR: 27%)"

---

## ELEMENTO 2: CAIXA DE INSIGHTS

**Posição:** Colunas 9-12, Linhas 2-4
**Dimensões:** 4.5cm × 6cm
**Background:** #E8F4F8 (azul claríssimo)
**Borda esquerda:** 4pt sólida #003B5C

**Título:** "DRIVERS PRINCIPAIS" (12pt Bold CAPS)

**Bullets:**
1. ► "Investimento corporativo (+120% desde 2022)" - verde #00A86B
2. ► "Regulação favorável (Marco Legal IA, 2024)" - verde #00A86B
3. ⚠ "Escassez de mão de obra qualificada (desafio)" - vermelho #C8102E

---

## ELEMENTO 3: TABELA SETORIAL

**Enumeração:** Tabela 7.1
**Posição:** Colunas 1-8, Linhas 7-8
**Título:** "Tabela 7.1 - Crescimento por setor (2024-2027E)"

| Setor | 2024 | 2027E | CAGR | Share |
|-------|------|-------|------|-------|
| Serviços Financeiros | 3.2 | 8.1 | 36% | 35% |
| Varejo & E-commerce | 2.1 | 5.9 | **42%** | 26% |
| Saúde | 1.4 | 3.7 | 38% | 16% |
| Manufatura | 1.2 | 2.9 | 34% | 13% |
| Outros | 1.3 | 2.5 | 24% | 10% |
| **TOTAL** | **9.2** | **23.1** | **45%** | **100%** |

**Formatação:**
- Header: Fundo #003B5C, texto branco Bold 11pt
- Body: Zebra striping (branco/#F5F5F5)
- Destaque: 42% com fundo verde claro #E8F8F0

---

## RODAPÉ

**Fontes:**
```
(1) IDC Brasil. "Mercado de IA 2024-2027". Mar 2024. https://idc.com/br/ai-2024
(2) McKinsey. "AI Adoption LATAM". Out 2024. https://mckinsey.com/ai-survey
(3) Análise da equipe com base em (1) e (2)
```

**Página:** 7 (alinhado à direita)

---

## CHECKLIST DE QUALIDADE

- [x] Título é action title
- [x] Dados exatos do material fonte
- [x] Gráfico enumerado (Gráfico 7)
- [x] Tabela enumerada (Tabela 7.1)
- [x] Fontes completas com URLs
- [x] Cores seguem paleta (#003B5C, #00A86B, #6E6E6E)
- [x] Tipografia consistente
- [x] Grid respeitado
- [x] "So What?" respondido

---

**STATUS:** COMPLETO - PRONTO PARA IMPLEMENTAÇÃO

---

Este nível de detalhe (2000+ palavras por slide) é o padrão McKinsey Elite.
Para deck de 50 slides = 100.000 palavras de especificação total.
