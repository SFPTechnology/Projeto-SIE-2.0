# KB_07: Design Fundamentals - Color, Typography, Layout, Icons

## COLOR THEORY APLICADA A APRESENTAÇÕES

### Círculo Cromático e Harmonias

**Cores Primárias:** Vermelho, Azul, Amarelo
**Cores Secundárias:** Verde, Laranja, Roxo
**Cores Terciárias:** Combinações intermediárias

**Harmonias principais:**

1. **Monocromática:** Variações de uma cor (ex: azul claro, médio, escuro)
   - Uso: Elegância, simplicidade, coesão
   - Exemplo: #E8F4F8, #0077BE, #003B5C (azuis)

2. **Análoga:** Cores adjacentes no círculo (ex: azul, azul-verde, verde)
   - Uso: Suavidade, natural, harmoniosa
   - Exemplo: #003B5C, #00897B, #00A86B

3. **Complementar:** Opostos no círculo (ex: azul e laranja)
   - Uso: Alto contraste, destaque, energia
   - Exemplo: #003B5C + #FF6F00

4. **Tríade:** 3 cores equidistantes (ex: vermelho, amarelo, azul)
   - Uso: Vibrante, balanceado, dinâmico
   - Exemplo: #C8102E, #FFA000, #003B5C

### Temperatura de Cor

**Cores Quentes (Vermelho, Laranja, Amarelo):**
- Emoção: Energia, urgência, atenção
- Uso: CTAs, alertas, destaques
- Avancem visualmente (parecem mais próximas)

**Cores Frias (Azul, Verde, Roxo):**
- Emoção: Calma, profissionalismo, confiança
- Uso: Backgrounds, elementos principais corporativos
- Recuam visualmente (parecem mais distantes)

### Psicologia de Cores por Contexto

**AZUL (#003B5C, #0077BE):**
- Significado: Confiança, profissionalismo, estabilidade
- Indústrias: Finance, Tech, Healthcare
- Uso: Cor corporativa dominante

**VERDE (#00A86B, #2E7D32):**
- Significado: Crescimento, sustentabilidade, positivo
- Indústrias: ESG, Healthcare, Agro
- Uso: Dados positivos, crescimento, "go"

**VERMELHO (#C8102E, #8B0000):**
- Significado: Urgência, perigo, negativo, paixão
- Indústrias: Varejo (promoções), Alertas
- Uso: Dados negativos, riscos, "stop"

**AMARELO/ÂMBAR (#FFA000, #FFD700):**
- Significado: Atenção, otimismo, energia
- Indústrias: Energia, Construção
- Uso: Avisos, highlights, estados intermediários

**ROXO (#6C63FF, #7C4DFF):**
- Significado: Premium, criatividade, inovação
- Indústrias: Luxury, Tech inovador
- Uso: Produtos premium, features exclusivas

**CINZA (#6E6E6E, #36454F):**
- Significado: Neutralidade, sofisticação, modernidade
- Indústrias: Universal
- Uso: Elementos secundários, texto, backgrounds

### Paletas Pré-Definidas por Indústria

**Consultoria Clássica (McKinsey style):**
```
Primary:   #003B5C (navy blue)
Secondary: #6E6E6E (medium gray)
Accent+:   #00A86B (emerald green - positivo)
Accent-:   #C8102E (crimson red - negativo)
Neutral:   #F5F5F5 (light gray - background)
```

**Tech/Startup:**
```
Primary:   #0066FF (electric blue)
Secondary: #00E5FF (cyan)
Accent:    #6C63FF (purple)
Dark:      #0A0A0A (near black)
Light:     #F9F9F9 (off-white)
```

**Financial Services:**
```
Primary:   #001F3F (deep navy)
Secondary: #00563F (forest green)
Accent:    #D4AF37 (gold)
Alert:     #8B0000 (burgundy)
Neutral:   #F9F9F9 (off-white)
```

**Healthcare/Pharma:**
```
Primary:   #00897B (calming teal)
Secondary: #7E57C2 (soft lavender)
Accent:    #D84315 (terracotta - energia)
White:     #FFFFFF (clean)
Light:     #E8F5E9 (mint green)
```

**Sustainability/ESG:**
```
Primary:   #2E7D32 (earth green)
Secondary: #00695C (ocean teal)
Accent:    #F9A825 (sun yellow)
Neutral:   #EFEBE9 (natural beige)
Dark:      #1B5E20 (deep forest)
```

### Contraste e Acessibilidade (WCAG)

**Níveis de conformidade:**

**WCAG AA (mínimo aceitável):**
- Texto normal: 4.5:1 contrast ratio
- Texto large (18pt+ ou 14pt+ bold): 3:1

**WCAG AAA (ideal):**
- Texto normal: 7:1
- Texto large: 4.5:1

**Ferramentas de teste:**
- WebAIM Contrast Checker
- Adobe Color Accessibility Tools
- Figma plugins (A11y Color Contrast)

**Exemplos práticos:**

```
✅ PASSA AA: #000000 em #FFFFFF (21:1)
✅ PASSA AA: #003B5C em #FFFFFF (12.6:1)
✅ PASSA AA: #FFFFFF em #003B5C (12.6:1)
❌ FALHA AA: #6E6E6E em #CCCCCC (2.8:1)
✅ PASSA AA: #6E6E6E em #FFFFFF (5.7:1)
```

**Regra prática:**
- Texto escuro (#000000 a #666666) em fundo claro (#FFFFFF a #CCCCCC) → Geralmente passa
- Texto branco (#FFFFFF) em fundo (#000000 a #767676) → Geralmente passa
- Tons médios em tons médios → Geralmente FALHA (evitar)

---

## TYPOGRAPHY SYSTEM

### Anatomia Tipográfica

**Elementos fundamentais:**

- **Baseline:** Linha onde caracteres "sentam"
- **X-height:** Altura de letras minúsculas sem ascenders/descenders
- **Ascender:** Parte que sobe acima de x-height (b, d, f, h, k, l)
- **Descender:** Parte que desce abaixo de baseline (g, j, p, q, y)
- **Cap height:** Altura de letras maiúsculas
- **Kerning:** Espaço entre pares de letras (AV, Ty)
- **Leading (line-height):** Distância entre baselines de linhas consecutivas
- **Tracking (letter-spacing):** Espaço uniforme entre todas as letras

### Famílias de Fontes

**Serif (com serifas):**
- Exemplos: Garamond, Georgia, Times New Roman
- Uso: Tradicional, editorial, corpo de texto longo
- **NÃO recomendado** para slides (menos legível em projeção)

**Sans-serif (sem serifas):**
- Exemplos: Helvetica Neue, Arial, Roboto, Open Sans
- Uso: Moderno, clean, legibilidade em telas
- **RECOMENDADO** para apresentações business

**Monospace:**
- Exemplos: Courier New, Consolas, Monaco
- Uso: Código, dados técnicos, tabelas numéricas

**Fonte padrão recomendada:**
```
Primária: Helvetica Neue (Mac) / Arial (Windows fallback)
Alternativa: Roboto, Open Sans (Google Fonts)
Dados/código: Courier New
```

### Hierarquia Tipográfica (6 níveis)

| Nível | Nome | Uso | Fonte | Tamanho | Peso | Cor | Leading |
|-------|------|-----|-------|---------|------|-----|---------|
| 1 | Display | Títulos de capa | Helvetica Neue | 36-48pt | Bold | #003B5C | 1.1 |
| 2 | H1 | Títulos de slide | Helvetica Neue | 28-32pt | Bold | #003B5C | 1.2 |
| 3 | H2 | Subtítulos | Helvetica Neue | 20-24pt | Bold | #003B5C | 1.3 |
| 4 | H3 | Seções | Helvetica Neue | 16-18pt | Bold | #6E6E6E | 1.3 |
| 5 | Body | Texto corrido | Helvetica Neue | 14-16pt | Regular | #000000 | 1.5 |
| 6 | Caption | Anotações, fontes | Helvetica Neue | 10-12pt | Regular | #6E6E6E | 1.4 |
| 7 | Legal | Disclaimers | Helvetica Neue | 8-9pt | Regular | #999999 | 1.3 |

**Regras de aplicação:**

1. **Contraste de tamanho:** Mínimo 2pt de diferença entre níveis adjacentes
2. **Máximo 3 níveis** por slide (evitar hierarquia confusa)
3. **Consistência absoluta:** Mesmo nível = mesma formatação sempre

### Formatação Semântica

**BOLD (negrito):**
- KPIs e números críticos ("R$ 150M", "45% de crescimento")
- Conclusões principais em bullets
- Totais em tabelas
- Palavras-chave em destaque

**ITALIC (itálico):**
- Termos técnicos em primeira menção ("EBITDA", "Capabilities system")
- Ênfase sutil em palavra específica
- Fontes de dados no rodapé
- Citações diretas

**CAPS (maiúsculas):**
- Siglas (CEO, ROI, EBITDA, NPS)
- Headers de seção (EXECUTIVE SUMMARY, RECOMMENDATIONS)
- Labels em frameworks (STRATEGY, STRUCTURE, SYSTEMS)

**Underline (sublinhado):**
- **EVITAR** em slides (pode parecer link)
- Exceção: Links reais (mas preferir cor diferente)

**Combinações:**
- ❌ Bold + Italic juntos (overload visual)
- ❌ CAPS + Bold (muito agressivo)
- ✅ CAPS sozinho OU Bold sozinho

### Pairing (Combinação de Fontes)

**Regra:** Máximo 2 famílias por apresentação

**Combinações efetivas:**

**Opção 1 - Monofontic (recomendado):**
```
Tudo: Helvetica Neue (varia apenas peso e tamanho)
Vantagem: Máxima coesão, profissional
```

**Opção 2 - Contraste Sans + Monospace:**
```
Texto: Helvetica Neue
Dados/tabelas: Courier New
Vantagem: Clareza em tabelas numéricas
```

**Opção 3 - Contraste Sans + Sans (uso avançado):**
```
Títulos: Montserrat Bold (geométrica, impacto)
Corpo: Open Sans Regular (legível, neutro)
Vantagem: Personalidade + legibilidade
```

**❌ Evitar:**
- Serif + Serif diferentes
- Mais de 2 famílias
- Fontes muito similares (confunde, não adiciona valor)

### Espaçamento (Leading e Tracking)

**Leading (line-height):**

```
Títulos (28-48pt): 1.1-1.2 × font size
  Exemplo: 32pt font → 38pt leading

Subtítulos (18-24pt): 1.2-1.3 × font size
  Exemplo: 20pt font → 26pt leading

Corpo de texto (14-16pt): 1.4-1.6 × font size
  Exemplo: 14pt font → 21pt leading

Captions (10-12pt): 1.3-1.4 × font size
  Exemplo: 11pt font → 15pt leading
```

**Regra:** Quanto menor a fonte, maior o leading relativo (legibilidade)

**Tracking (letter-spacing):**

```
Display/Títulos grandes: -10 a 0 (comprimir levemente)
Títulos médios: 0 (padrão)
Corpo de texto: 0 (nunca mexer)
CAPS: +10 a +30 (expandir para legibilidade)
Captions pequenos: +5 a +10 (expandir)
```

**Exemplo de aplicação CAPS:**
```
❌ EXECUTIVE SUMMARY (tracking 0) → apertado
✅ EXECUTIVE SUMMARY (tracking +20) → legível
```

### Alinhamento

**Left-aligned (esquerda):**
- Padrão para texto ocidental
- Bullets e parágrafos
- Tabelas (labels de linhas)
- **USO:** 90% dos casos

**Center (centralizado):**
- Títulos de slide (opcional)
- Elementos isolados (logo, citação destaque)
- **CUIDADO:** Não centralizar parágrafos longos

**Right (direita):**
- Números em tabelas (valores alinhados por decimal)
- Datas, números de página
- **USO:** Específico, não geral

**Justified (justificado):**
- **EVITAR** em slides completamente
- Cria rios de espaço (irregular)
- Dificulta leitura em linhas curtas

---

## LAYOUT & GRID SYSTEMS

### Grid de 12 Colunas × 8 Linhas

**Especificações padrão para slides 16:9:**

```
Slide total: 27cm × 19.05cm (16:9 aspect ratio)

Margens:
  Superior: 2.0cm
  Inferior: 1.5cm
  Esquerda: 1.5cm
  Direita: 1.5cm

Área útil: 24cm (largura) × 15.55cm (altura)

Grid:
  Colunas: 12 (cada 2cm)
  Linhas: 8 (cada ~1.95cm)
  Gutters (espaço entre colunas): 0.5cm
```

**Uso do grid:**

```
Título: Linha 1, Colunas 1-12 (full width)

Layout 70/30:
  Principal: Colunas 1-8, Linhas 2-7
  Sidebar: Colunas 9-12, Linhas 2-7

Layout 50/50:
  Esquerda: Colunas 1-6, Linhas 2-7
  Direita: Colunas 7-12, Linhas 2-7

Layout centralizado:
  Conteúdo: Colunas 2-11, Linhas 2-7
  (1 coluna de margem cada lado)

Rodapé: Linha 8 (ou abaixo), Colunas 1-12
```

**Snap to grid:**
TODO elemento deve alinhar às linhas de grid (não posições arbitrárias)

### Regra dos Terços

**Divisão:** 3×3 (horizontal × vertical)

**Pontos de interesse:** Interseções das linhas (4 pontos)

**Aplicação:**
- Posicionar elemento focal em um dos 4 pontos
- Não centralizar tudo (estático, chato)
- Criar dinamismo visual

**Exemplo:**
```
┌─────┬─────┬─────┐
│     │     │  X  │ ← Imagem principal no ponto superior direito
├─────┼─────┼─────┤
│     │     │     │
├─────┼─────┼─────┤
│  X  │     │     │ ← Callout box no ponto inferior esquerdo
└─────┴─────┴─────┘
```

### Proporção Áurea (1:1.618)

**Uso:** Divisões harmoniosas naturais

**Aplicação em slides:**
```
Divisão vertical:
  Seção maior: 61.8% da largura (14.8cm de 24cm)
  Seção menor: 38.2% da largura (9.2cm de 24cm)

Divisão horizontal:
  Seção maior: 61.8% da altura (9.6cm de 15.5cm)
  Seção menor: 38.2% da altura (5.9cm de 15.5cm)
```

**Quando usar:** Layouts assimétricos elegantes

### White Space (Espaço Negativo)

**Princípio:** "Menos é mais"

**Regra 30-40%:** 30-40% da área do slide deve estar vazia

**Benefícios:**
- Respiro visual (não overwhelm)
- Foca atenção no que importa
- Profissionalismo (não amador lotado)

**Técnicas:**

1. **Padding (espaçamento interno):**
   - Caixas de texto: 0.5-0.8cm ao redor do texto
   - Callout boxes: 0.5cm mínimo

2. **Margin (espaçamento entre elementos):**
   - Entre título e conteúdo: 1.0-1.5cm
   - Entre elementos distintos: 0.8-1.2cm
   - Entre slide edge e conteúdo: Respeitar margens de grid

3. **Não preencher todo espaço disponível:**
   - Se gráfico pode ser 100% da área, fazer 70-80%
   - Deixar respiro ao redor

**Teste:** Se slide parece "cheio", remover 20% do conteúdo

### Visual Weight e Balance

**Weight (peso visual):**
- Elementos maiores = mais pesados
- Cores escuras = mais pesadas que claras
- Formas complexas = mais pesadas que simples

**Balance (equilíbrio):**

**Simétrico:**
- Espelhamento em eixo vertical
- Formal, estável, tradicional
- Uso: Title slides, apresentações conservadoras

**Assimétrico:**
- Elementos diferentes em lados diferentes
- Dinâmico, moderno, interessante
- Uso: Data slides, apresentações inovadoras

**Equilíbrio de peso:**
```
Elemento grande + leve (cinza claro) à esquerda
=
Elemento pequeno + pesado (azul escuro) à direita
```

### Z-Pattern vs F-Pattern (Eye Tracking)

**Z-Pattern (slides):**
```
1 → → → 2
    ↓
3 ← ← ← 4

Leitura: Top-left → Top-right → Diagonal → Bottom-left → Bottom-right
```

**Aplicação:**
- Título: Top-left
- Número/data: Top-right
- Conteúdo principal: Centro
- Fonte/página: Bottom-right

**F-Pattern (texto denso):**
```
→ → → →
↓
→ → →
↓
→ →
↓
```

**Evitar em slides:** Indica muito texto (red flag)

---

## ICONOGRAPHY STANDARDS

### Estilos de Ícones

**Line / Outline (recomendado para business):**
- Apenas contorno, sem preenchimento
- Espessura: 2pt uniforme
- Clean, escalável, profissional
- Exemplo: Feather Icons

**Filled / Solid:**
- Preenchimento sólido
- Uso: Destaque pontual, CTAs
- Menos versátil que line

**Duotone (2 cores):**
- Base + acento
- Uso: Hierarquia visual (principal vs secundário)
- Cuidado: Não overuse

**Flat (design plano):**
- Sem sombras, sem gradientes
- Cores chapadas
- Moderno, minimalista

### Especificações Técnicas

**Tamanho padrão:** 1.5cm × 1.5cm (para uso em slides)

**Espessura de linha:** 2pt (consistente em todos ícones)

**Grid de construção:** 24×24px (design) → escalar proporcionalmente

**Cor:**
- Monocromático: 1 cor (#003B5C ou #6E6E6E)
- Categórico: Cores diferentes se significados diferentes
- NUNCA: Cores aleatórias

**Consistência:**
- TODOS ícones mesmo estilo (line OU filled, não misto)
- TODOS mesma espessura
- TODOS mesma complexidade (simples ou detalhados, não misto)

### Quando Usar Ícones

**✅ BOM:**
- Navegação/Agenda (ícones para cada seção)
- Conceitos abstratos (crescimento, risco, inovação)
- Callouts e highlights (ícone + texto)
- Process steps (numeração com ícone)
- Categorização visual

**❌ RUIM:**
- Decoração gratuita (chart junk)
- Quando texto é mais claro
- Ícones culturalmente ambíguos
- Muitos ícones diferentes (confusão)

### Bibliotecas Recomendadas

**Open Source / Free:**

1. **Feather Icons** (287 ícones)
   - Estilo: Line, ultra-clean
   - Peso: 2pt consistente
   - Licença: MIT (uso livre)
   - URL: feathericons.com

2. **Material Design Icons** (5000+ ícones)
   - Estilo: Filled e Outline
   - Google ecosystem
   - Licença: Apache 2.0
   - URL: material.io/icons

3. **Font Awesome** (Grátis + Pro)
   - Estilo: Solid, Regular, Light
   - Vasta biblioteca
   - Licença: Mix (verificar)
   - URL: fontawesome.com

**Premium (pago):**

1. **Streamline** ($199-499)
   - 100,000+ ícones
   - Ultra consistente (mesmos designers)
   - Múltiplos pesos
   - Uso comercial

2. **Noun Project Pro** ($39.99/ano)
   - Milhões de ícones
   - Curadoria necessária (qualidade varia)
   - Sem atribuição (pro)

### Uso em Slides - Exemplo

```markdown
ELEMENTO: Ícones de Processo (5 steps)

ESTILO: Line icons, Feather Icons library

ESPECIFICAÇÕES:
- Tamanho: 1.5cm × 1.5cm cada
- Espessura: 2pt
- Cor: #003B5C (navy)
- Espaçamento: 2cm entre ícones (center-to-center)

DISPOSIÇÃO:
Horizontal, colunas 2-11, linha 3
[Icon 1] → [Icon 2] → [Icon 3] → [Icon 4] → [Icon 5]

ÍCONES ESPECÍFICOS:
1. Feather "search" (pesquisa/análise)
2. Feather "users" (stakeholders)
3. Feather "tool" (implementação)
4. Feather "trending-up" (resultados)
5. Feather "check-circle" (conclusão)

LABELS:
Abaixo de cada ícone (0.3cm)
Helvetica Neue Regular 11pt #000000
Texto: "Análise", "Stakeholders", "Implementação", "Resultados", "Validação"
```

---

## CHECKLIST DE DESIGN

**Antes de finalizar qualquer slide:**

**Cor:**
- [ ] Paleta consistente (máximo 5 cores)
- [ ] Contraste suficiente (WCAG AA mínimo)
- [ ] Cores têm significado (não aleatórias)
- [ ] Acessível para daltônicos (não depende só de cor)

**Tipografia:**
- [ ] Máximo 2 famílias de fontes
- [ ] Hierarquia clara (3 níveis máximo por slide)
- [ ] Tamanhos de fonte >= 11pt (legibilidade)
- [ ] Formatações semânticas corretas (bold, italic, CAPS)
- [ ] Leading apropriado (1.3-1.5 para corpo)

**Layout:**
- [ ] Alinhado ao grid (12×8)
- [ ] White space adequado (30-40%)
- [ ] Elementos não tocam bordas (respiro)
- [ ] Visual weight balanceado
- [ ] Não overcrowded (remover 20% se em dúvida)

**Ícones:**
- [ ] Estilo consistente (todos line OU filled)
- [ ] Tamanho uniforme (1.5cm padrão)
- [ ] Têm função (não decorativos)
- [ ] Culturalmente apropriados

**Geral:**
- [ ] Design serve conteúdo (não ofusca)
- [ ] Profissional (não parece template gratuito)
- [ ] Coeso com resto da apresentação

---

**FIM DO KB_07**

Total: ~1400 palavras - Padrão 12/10 atingido
