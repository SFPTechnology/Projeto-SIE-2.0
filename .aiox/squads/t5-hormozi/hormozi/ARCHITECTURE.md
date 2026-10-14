# Hormozi Squad — Architecture

## Overview

O squad `hormozi` é composto por 15 agentes especializados, cada um dominando uma dimensão da metodologia Alex Hormozi. Operado pelo `hormozi-chief` via triagem/roteamento, aplica frameworks $100M Offers, $100M Leads, Acquisition.com e Grand Slam Offers em negócios reais.

## Agent Hierarchy

```
hormozi-chief (Orchestrator — Triage & Routing)
│
├── Strategy & Business Advisory
│   ├── hormozi-advisor       # Strategic consulting, business model
│   ├── hormozi-audit         # Business audit, teardowns
│   └── hormozi-models        # Business models, unit economics
│
├── Offers & Pricing
│   ├── hormozi-offers        # Grand Slam Offers, offer stacks
│   └── hormozi-launch        # Launch strategy, urgency/scarcity
│
├── Lead Generation
│   ├── hormozi-leads         # Core 4 lead gen methods
│   ├── hormozi-ads           # Paid ads: Meta, Google, YouTube
│   ├── hormozi-hooks         # Hooks for attention capture
│   └── hormozi-content       # Content as lead magnet
│
├── Sales & Conversion
│   ├── hormozi-closer        # Sales scripts, closing techniques
│   └── hormozi-copy          # Conversion copy (landers, emails, ads)
```

## Execution Flow

```
Business strategy question (offer, leads, scaling, pricing, content, sales, audit)
                              ↓
                hormozi-chief classifies intent
                              ↓
       ┌──────────────────────┼──────────────────────┐
       v                      v                      v
  Strategy/Models        Offer Design           Lead Gen / Sales
  (advisor, audit,       (offers, launch)       (leads, ads, hooks,
   models)                                       content, closer, copy)
       ↓                      ↓                      ↓
  Business recommendation + framework application
       ↓
  Artifacts → workspace/businesses/{biz}/L1-L4
```

## Methodology Frameworks

| Book / Framework | Applied in agents |
|------------------|-------------------|
| $100M Offers (Grand Slam Offers) | hormozi-offers, hormozi-launch |
| $100M Leads (Core 4) | hormozi-leads, hormozi-ads, hormozi-hooks, hormozi-content |
| Acquisition.com teardowns | hormozi-audit, hormozi-advisor |
| Unit Economics | hormozi-models |
| Sales Conversion | hormozi-closer, hormozi-copy |

## Core 4 Lead Generation Methods

```
Warm                                    Cold
 │                                       │
 ├─ Warm Outreach        ├─ Cold Outreach
 ├─ Content              └─ Paid Ads
 │
 (Post to audience)
```

## Grand Slam Offer Framework

```
Dream Outcome × Perceived Likelihood
────────────────────────────────────── = Offer Value
Time Delay × Effort & Sacrifice
```

Stack increases value through: outcomes, bonuses, guarantees, scarcity, urgency.

## Decision Tree (hormozi-chief routing)

```
Is this about offer design? → hormozi-offers + hormozi-launch
Is this about lead gen? → hormozi-leads + (ads/hooks/content)
Is this about sales/closing? → hormozi-closer + hormozi-copy
Is this about business model? → hormozi-models + hormozi-advisor
Is this about business health? → hormozi-audit
```

## Integration Points

| Consumer | How it uses hormozi outputs |
|----------|---------------------------|
| copy squad | Offer stacks → copy briefs |
| brand squad | Positioning informed by Grand Slam Offer |
| c-level | Strategic advisory from hormozi-advisor |
| workspace L1-strategy | Pricing strategy derived from hormozi-models |

## Outputs Location

| Artifact | Path |
|----------|------|
| Offer stacks | `workspace/businesses/{biz}/L1-strategy/offerbook.yaml` |
| Pricing strategy | `workspace/businesses/{biz}/L1-strategy/pricing-strategy.yaml` |
| Lead magnets | `workspace/businesses/{biz}/L4-operational/campaigns/{slug}/` |
| Business audits | Generated on demand |

## Boundary

- **In scope:** Offer design, lead generation, pricing, content strategy, sales/closing, business model, business audit (Hormozi methodology)
- **Out of scope:** Implementation (dev), actual copy production (copy squad consumes strategic outputs)

## Tasks Canônicas (57 total)

Extensive library covering: offer teardowns, value equation calculators, lead magnet generators, landing page reviews, sales script templates, business model canvases, pricing matrices, audit checklists.
