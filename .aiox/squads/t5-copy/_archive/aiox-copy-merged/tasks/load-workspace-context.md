# Load Workspace Context Task

Task para carregar contexto operacional do `workspace` antes de executar qualquer task de copy.

## Metadata

```yaml
task:
  name: Load Workspace Context
  id: load-workspace-context
  version: "1.0.0"
  category: research
  estimated_time: "10-20 min"
  dependencies:
    - workspace/domains/content/copy-governance.yaml
    - workspace/domains/content/copy-information-architecture.yaml
    - workspace/_templates/product-offerbook/
    - workspace/_templates/content/
    - workspace/_templates/sales-process/
  outputs:
    - outputs/workspace-context/campaign-context-brief.yaml
```

---

## Objective

Garantir que o squad de copy use dados reais e regras vigentes do workspace.

---

## Phase 1: Governance Snapshot

1. Ler `workspace/domains/content/copy-governance.yaml`.
2. Ler `workspace/domains/content/copy-information-architecture.yaml`.
3. Extrair:
   - princípios obrigatórios
   - rules por superfície (`S1`, `S2`, `S3`)
   - stage source of truth
   - campaign slug policy
   - quality gates aplicáveis ao deliverable solicitado
4. Registrar em `governance_constraints`.

---

## Phase 2: Durable Truth Snapshot

1. Carregar a camada `brand`:
   - `workspace/businesses/{business}/L0-identity/`
   - `workspace/businesses/{business}/brand/`
2. Carregar a camada `product`:
   - `workspace/businesses/{business}/L3-product/{product}/`
   - `workspace/businesses/{business}/L3-product/{product}/narrative/`
3. Registrar:
   - brand truth disponível
   - product truth disponível
   - gaps críticos que impedem `FINAL`

---

## Phase 3: Campaign Snapshot

1. Identificar `campaign_slug` quando o trabalho for estratégico, multi-asset, high-ticket ou `FINAL`.
2. Carregar a camada `campaign` em `workspace/businesses/{business}/copy/{campaign_slug}/` quando existir.
3. Registrar:
   - `campaign_brief`
   - `message_architecture`
   - `creative_brief`
   - `asset_briefs`
4. Se `campaign_slug` não existir:
   - marcar `campaign_context.status: implicit_draft_only`
   - impedir promoção para `FINAL`

---

## Phase 4: Template Snapshot

1. Carregar templates relevantes em `workspace/_templates/product-offerbook/`.
2. Carregar templates relevantes em `workspace/_templates/content/`.
3. Carregar templates relevantes em `workspace/_templates/sales-process/`.
4. Para cada template usado, mapear:
   - campos obrigatórios
   - campos opcionais
   - lacunas de input do usuário

---

## Output Contract

Salvar arquivo `outputs/workspace-context/campaign-context-brief.yaml` com:

```yaml
campaign_context_brief:
  generated_at: "YYYY-MM-DDTHH:mm:ssZ"
  request_type: "<sales-page|email-sequence|ad-copy|...>"
  business_slug: ""
  product_slug: ""
  campaign_slug: ""
  governance_constraints:
    surface: "S1|S2|S3"
    required_rules: []
    quality_gates: {}
    promotion_rule: ""
  source_of_truth:
    brand_layer: []
    product_layer: []
    campaign_layer: []
    delivery_layer:
      - "outputs/copy/{business}/..."
  brand_truth:
    available_files: []
    missing_files: []
  product_truth:
    available_files: []
    missing_files: []
  campaign_context:
    status: "ready|missing|implicit_draft_only"
    available_files: []
    missing_files: []
    final_allowed: false
  workflow_alignment:
    selected_workflow: ""
    execution_track: ""
    canonical_artifacts_expected: []
  templates_loaded:
    - path: ""
      required_fields: []
      missing_inputs: []
  assumptions: []
  blockers: []
```

---

## Quality Checklist

- [ ] Leu `copy-governance.yaml` e `copy-information-architecture.yaml`.
- [ ] Selecionou superfície correta (`S1`, `S2` ou `S3`).
- [ ] Mapeou brand truth, product truth e campaign truth separadamente.
- [ ] Carregou pelo menos 1 template de `content/`, `product-offerbook/` ou `sales-process/`.
- [ ] Registrou `assumptions` e `blockers` no output final.

---

## Fallback

Se algum arquivo obrigatório do workspace não existir:

1. Reportar exatamente o caminho faltante.
2. Não inventar schema/campos.
3. Se faltar `campaign_slug` ou `campaign-brief.yaml` em trabalho estratégico, marcar `implicit_draft_only`.
4. Pedir insumo mínimo faltante antes de continuar execução de copy.
