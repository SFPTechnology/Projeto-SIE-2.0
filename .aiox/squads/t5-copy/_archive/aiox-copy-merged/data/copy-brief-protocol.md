# Copy Brief Protocol — Mandatory Pre-Write Loading

> **Versão:** 1.0
> **Guardian:** Copy Chief
> **Regra:** NENHUMA copy é escrita sem carregar os dados abaixo.
> **Violação:** Copy produzida sem brief completo é DRAFT, não FINAL.

---

## Princípio

O Copy Chief não inventa dados. Ele extrai de fontes canônicas.

Antes de escrever qualquer peça de copy (landing page, email, ad, VSL, script),
o copy-chief DEVE carregar um brief estruturado a partir dos arquivos do workspace.

Quando existir `workspace/businesses/{business}/copy/{campaign_slug}/campaign-brief.yaml`,
esse arquivo passa a ser o artefato canônico de entrada da campanha.
O protocolo continua obrigatório, mas seu papel vira:

1. carregar brand truth
2. carregar product truth
3. carregar e validar o `Campaign Brief`
4. sinalizar gaps entre o brief e as fontes canônicas

Se `campaign-brief.yaml` não existir, o protocolo pode montar um brief implícito
apenas para trabalhos pequenos, exploratórios ou diagnósticos.
Para trabalho estratégico, multi-asset, high-ticket ou qualquer entrega `FINAL`,
o `Campaign Brief` persistido deve existir.

`campaign_slug` deixa de ser um detalhe opcional quando a campanha entra em modo real.
Regra operacional:

1. se o trabalho for estratégico, multi-asset, high-ticket ou `FINAL`, o `campaign_slug` deve ser identificado
2. se existir `workspace/businesses/{business}/copy/{campaign_slug}/campaign-brief.yaml`, ele governa a camada de campanha
3. se não existir `campaign_slug`, o chief pode montar apenas um brief implícito de runtime para diagnóstico, exploração ou `DRAFT`
4. sem `campaign_slug` persistido, não há promoção para `FINAL`

Se um arquivo obrigatório não existe ou está incompleto, o copy-chief DEVE:
1. Informar ao usuário quais dados faltam
2. Sugerir como preencher (qual agente, qual task)
3. NÃO prosseguir com copy final sem os dados — apenas DRAFT com disclaimers

---

## Camada 1: EMPRESA (carregar sempre, uma vez por sessão)

Estes arquivos definem QUEM somos. Carregam uma vez e valem para qualquer produto.

| # | Arquivo | O que extrair | Obrigatório? |
|---|---------|---------------|-------------|
| 1 | `{business}/company/icp.yaml` | ICP name, archetypes, pain stack, action/paralysis triggers, red/green flags | **SIM** |
| 2 | `{business}/brand/brandbook.yaml` | Archetype mix, trueline, voice DNA, forbidden words, signature phrases, promises, enemies, onlyness, message hierarchy, competitive positioning | **SIM** |
| 3 | `{business}/company/founder-dna.yaml` | Founder archetypes, origin story, teaching philosophy | Recomendado |
| 4 | `{business}/company/credentials.yaml` | Authority proof points, media, speaking | Recomendado |

**Path base:** `workspace/businesses/{business}/`

---

## Camada 2: PRODUTO (carregar por produto alvo da copy)

Estes arquivos definem O QUE estamos vendendo. Carregam por produto.

| # | Arquivo | O que extrair | Obrigatório? |
|---|---------|---------------|-------------|
| 7 | `{business}/products/{product}/proof.yaml` | Financial results, case studies, aggregate stats, proof hierarchy | **SIM** |
| 8 | `{business}/products/{product}/testimonials.yaml` | Depoimentos por tier, usage matrix, objection destroyers | **SIM** |
| 9 | `{business}/products/{product}/curriculum.yaml` | Estrutura, módulos, entregáveis, IEM, promessa verificável | **SIM** (se cohort/curso) |
| 10 | `{product_business}/products/{product}/offerbook.yaml` | Oferta completa, ancoragem, garantia, narrativa, pricing, value stack | **SIM** |
| 10b | `{brand_business}/company/offerbook.yaml` | Índice de produtos + voice rules compartilhadas | Referência |
| 11 | `{business}/operations/pricing-strategy.yaml` | Preços, tiers, payback, ROI | Recomendado |

**Path base:** `workspace/businesses/{business}/`

---

## Camada 3: CONTEXTO (carregar se disponível)

Dados complementares que enriquecem a copy.

| # | Arquivo | O que extrair | Quando usar |
|---|---------|---------------|------------|
| 12 | `{business}/evidence/*.yaml` | Insights de sessões, dados de mercado | Se existir |
| 13 | `{business}/analytics/cohorts/*.yaml` | Health scores, RFM, executive summary | Se cohort |
| 14 | `{business}/movement/reading/persona/*.yaml` | Personas ideológicas, objeções, segmentação | Se movement intelligence |
| 15 | `docs/{business}/depoimentos/*.md` | Depoimentos brutos | Para volume de prova |
| 16 | `outputs/copy/{business}/drafts/*.md` | Drafts anteriores aprovados | Se existir trabalho prévio |

---

## Camada 4: CAMPANHA (carregar quando existir)

Estes arquivos definem O QUE esta campanha específica precisa dizer e entregar.

| # | Arquivo | O que extrair | Obrigatório? |
|---|---------|---------------|-------------|
| 17 | `workspace/businesses/{business}/copy/{campaign_slug}/campaign-brief.yaml` | Objective, audience, offer in scope, channels, constraints, success criteria | **SIM** para trabalho estratégico ou `FINAL` |
| 18 | `workspace/businesses/{business}/copy/{campaign_slug}/message-architecture.yaml` | Campaign message hierarchy, promise, mechanism, proof logic, language controls | Recomendado; **SIM** para multi-asset/high-ticket |
| 19 | `workspace/businesses/{business}/copy/{campaign_slug}/creative-brief.yaml` | Angle, emotional posture, must-have proof and CTA direction | Recomendado |
| 20 | `workspace/businesses/{business}/copy/{campaign_slug}/assets/*.yaml` | Asset-level specs e aprovação por deliverable | Se existir |

---

## Fonte Da Verdade Por Estágio

| Estágio | Artefato primário | Fonte da verdade | Fallback permitido? |
|---|---|---|---|
| Intake | `Campaign Brief` | `workspace/businesses/{business}/copy/{campaign_slug}/campaign-brief.yaml` | Sim, mas só para `DRAFT` pequeno/exploratório |
| Message Strategy | `Message Architecture` | `workspace/businesses/{business}/copy/{campaign_slug}/message-architecture.yaml` + brand/product truth | Só para campanhas leves; nunca para high-ticket sem explicitar a lógica |
| Creative Direction | `Creative Brief` | `workspace/businesses/{business}/copy/{campaign_slug}/creative-brief.yaml` | Pode ser comprimido em campanhas leves |
| Asset Planning | `Asset Brief` | `workspace/businesses/{business}/copy/{campaign_slug}/assets/*.yaml` | Pode ser implícito para peça única simples |
| Writing | `Copy Deck` / output final | `outputs/copy/{business}/...` | Não |
| Review | Checklists + approval state | `checklists/final-copy-readiness.md` + proof/brand/product sources | Não |
| Validation | test notes / iteration notes | runtime + evidence de mercado | Sim, depende do canal e do estágio da campanha |

### Verdades Duráveis Que Nunca Mudam De Dono

- `company/` e `brand/` definem identidade, voz e posicionamento
- `products/{product}/` define oferta, prova, currículo e narrativa reutilizável
- `copy/{campaign_slug}/` define o recorte estratégico da campanha
- `outputs/copy/{business}/` guarda a copy executável e entregue

---

## Checklist Pré-Escrita

Antes de produzir copy final, o copy-chief verifica:

```
BRIEF COMPLETO?
├── [ ] Campaign Brief carregado quando o trabalho for estratégico ou FINAL
├── [ ] ICP carregado (icp.yaml) — Sei PARA QUEM estou escrevendo
├── [ ] Brandbook carregado (brandbook.yaml) — Sei COMO falar, O QUE nos diferencia, REGRAS visuais/verbais
├── [ ] Proof stack carregado (proof.yaml) — Tenho PROVAS reais
├── [ ] Testimonials carregados (testimonials.yaml) — Tenho VOZES reais
├── [ ] Offerbook carregado (offerbook.yaml) — Sei a OFERTA completa
│   └── Se vazio: INFORMAR ao usuário. Só produzir DRAFT.
├── [ ] Curriculum carregado (curriculum.yaml) — Se for produto educacional
├── [ ] Pricing carregado (pricing-strategy.yaml) — Sei os NÚMEROS
└── [ ] Message Architecture carregada se a campanha exigir adaptação de mensagem

VALIDAÇÃO PÓS-ESCRITA:
├── [ ] Forbidden words checadas (brandbook.yaml > voice > forbidden_words)
├── [ ] Trueline presente ou coerente (conforme brandbook.yaml)
├── [ ] ICP archetypes endereçados (pelo menos 2 dos 5)
├── [ ] Depoimentos usados são de proof/testimonials.yaml (não inventados)
├── [ ] Números citados têm fonte (proof.yaml, credentials.yaml)
└── [ ] Pain stack refletido na copy (pelo menos 3 dores endereçadas)
```

---

## Mapa de Produtos por Business

Brand + Product vivem no mesmo business. Produtos são descobertos dinamicamente.

**Path base:** `workspace/businesses/{business}/`

```
{business}/
├── company/     → brand layer (icp, brand, credentials, offerbook INDEX)
├── brand/       → brand layer (brandbook, positioning, logo)
└── products/    → product layer (offerbook, proof, testimonials, curriculum)
    ├── {product_1}/
    ├── {product_2}/
    └── {product_n}/
```

Cada produto DEVE ter: `offerbook.yaml`, `proof.yaml`, `testimonials.yaml`.
Produtos educacionais também precisam de `curriculum.yaml`.

---

## Exemplo de Uso

**Usuário:** "Preciso reescrever a landing page do {product}"

**Copy Chief carrega:**
1. `workspace/businesses/{business}/company/offerbook.yaml` → Índice → aponta para offerbook do produto
2. `workspace/businesses/{business}/company/icp.yaml` → ICP name, archetypes
3. `workspace/businesses/{business}/brand/brandbook.yaml` → Voice DNA, forbidden words, archetype mix, onlyness, positioning
4. `workspace/businesses/{business}/products/{product}/offerbook.yaml` → Oferta completa do produto
5. `workspace/businesses/{business}/products/{product}/proof.yaml` → Financial results
6. `workspace/businesses/{business}/products/{product}/testimonials.yaml` → Depoimentos estruturados
7. `workspace/businesses/{business}/products/{product}/curriculum.yaml` → Estrutura, IEM (se educacional)
8. `workspace/businesses/{business}/copy/{campaign_slug}/campaign-brief.yaml` → Objetivo, assets e constraints da campanha, se existir
9. `workspace/businesses/{business}/copy/{campaign_slug}/message-architecture.yaml` → Mensagem e prova por campanha, se a campanha for estratégica

**Copy Chief informa:**
> "Brand + product truth carregados. Campaign Brief validado. Status: FINAL."

---

## Offerbook Prerequisites Gate

Antes de USAR um offerbook, verificar se ele foi criado com os 7 arquivos obrigatórios.

```
REQUIRED para offerbook existir:
1. ICP (>=85% completo)
2. Brand voice (com forbidden_words)
3. Positioning (com onlyness)
4. Proof stack (>=3 resultados verificáveis)
5. Testimonials (>=5 depoimentos estruturados)
6. Produto structure (currículo/agenda/deliverables)
7. Pricing (definido em qualquer arquivo canônico)

7/7 → offerbook FINAL
6/7 → offerbook DRAFT (gap marcado)
<=5/7 → offerbook NÃO PODE ser criado
```

## Governing Separation

- Brand layer define identidade e posicionamento durável
- Product layer define oferta, prova e narrativa reutilizável
- Campaign layer define o recorte estratégico da campanha
- Delivery layer guarda a copy pronta

Referência canônica: `workspace/domains/content/copy-information-architecture.yaml`

---

## Anti-Padrões (o que NÃO fazer)

1. **Escrever de memória** — Sempre ler os arquivos, mesmo que "lembre" de sessões anteriores
2. **Inventar depoimentos** — Todo depoimento deve existir em proof.yaml ou testimonials.yaml
3. **Ignorar forbidden words** — "Mágico", "Revolucionário", "Fácil" são PROIBIDOS
4. **Pular o ICP** — Sem saber para quem, a copy vira genérica
5. **Copiar pain stack de outro produto** — Cada produto tem seu proof stack
6. **Produzir FINAL sem brief** — Sem dados = DRAFT com disclaimer, nunca FINAL
