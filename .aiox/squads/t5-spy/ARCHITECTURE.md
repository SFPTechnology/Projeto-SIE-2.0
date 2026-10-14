# Spy Squad — Architecture

## Overview

O squad `spy` combina **competitive intelligence** + **evidence-based research**: universal benchmarking, content analysis, PICO/OSINT pipeline, systematic reviews, decision science, e bias detection. Absorveu o squad legado `deep-research` em 2026-04-13.

## Agent Hierarchy

```
spy (Orchestrator — Content Intelligence)
│
├── Research Pipeline (absorbed deep-research)
│   ├── dr-orchestrator       # Deep Research Pipeline Coordinator
│   ├── research-head         # Market Intelligence & Lead
│   └── reference-competitor-clone  # Competitor baseline cloning
│
├── Evidence-Based Research Specialists
│   ├── sackett               # Evidence hierarchy (5 levels)
│   ├── cochrane              # Systematic review methodology
│   ├── higgins               # Risk of bias assessment
│   ├── ioannidis             # False positives, replicability
│   └── creswell              # Mixed methods research
│
├── Benchmarking & Analysis
│   ├── bench-analyst         # Universal benchmarking methodology
│   ├── benchmark-runtime     # Runtime benchmark execution
│   └── forsgren              # DORA metrics (DevOps performance)
│
├── Decision Science & Bias
│   ├── kahneman              # System 1/System 2, biases
│   └── klein                 # Recognition-primed decision, pre-mortem
│
└── OSINT & Collection
    ├── gilad                 # Competitive Intelligence (CI) framework
    └── booth                 # Information retrieval, systematic search
```

## Research Pipelines

### Pipeline 1: Deep Research (Use Case Routing)

```
Research question
       ↓
dr-orchestrator classifies intent
       ↓
    ┌──┴──┐
    ▼     ▼
Market intel       Tech research       Content DNA extraction
   ↓                    ↓                      ↓
research-head     bench-analyst       reference-competitor-clone
   ↓                    ↓                      ↓
Player analysis   Benchmark matrix    Viral pattern swipe file
   ↓                    ↓                      ↓
      ┌─────────────────┴─────────────────┐
      ▼                                   ▼
Systematic review      Decision recommendation
(sackett/cochrane)     (kahneman/klein)
```

### Pipeline 2: Competitive Intelligence

```
Competitor target
       ↓
gilad (CI framework) + booth (OSINT retrieval)
       ↓
Data collection (public + ethical)
       ↓
Evidence-based analysis
├── sackett: evidence hierarchy
├── higgins: bias detection
└── ioannidis: false positive check
       ↓
Insight synthesis
├── kahneman: bias audit of conclusions
└── klein: pre-mortem of recommendations
       ↓
Actionable intelligence report
```

### Pipeline 3: Universal Benchmarking

```
Subjects to compare (codebases, LLMs, products, companies)
       ↓
bench-analyst designs benchmark methodology
       ↓
benchmark-runtime executes quantitative tests
       ↓
forsgren applies DORA metrics (when DevOps-relevant)
       ↓
Matrix + gap analysis + battle card
```

## Evidence Hierarchy (Sackett)

```
Level 1: Systematic reviews + meta-analyses
Level 2: RCTs (randomized controlled trials)
Level 3: Cohort studies
Level 4: Case-control studies
Level 5: Expert opinion (lowest)
```

Spy always prioritizes Level 1-2 sources; Level 5 tagged as such.

## Bias Mitigation (Kahneman + Higgins + Ioannidis)

| Bias | Mitigation |
|------|-----------|
| Confirmation bias | Pre-register hypothesis before collecting data |
| Availability heuristic | Systematic search (booth) vs. ad-hoc |
| Anchoring | Multiple independent estimates |
| Publication bias | Check Level 1 meta-analyses, not just studies |
| False positives | Ioannidis p-value correction, replication check |

## Outputs Location

| Type | Path |
|------|------|
| Research reports | `outputs/spy/{case-slug}/` |
| Swipe files (content DNA) | `outputs/spy/swipes/{competitor-slug}/` |
| Battle cards (benchmarks) | `outputs/spy/benchmarks/{comparison-id}/` |
| Systematic reviews | `outputs/spy/reviews/{topic}/` |

## Integration Points

| Consumer | Uses spy outputs for |
|----------|---------------------|
| brand-chief | Competitive positioning |
| hormozi-chief | Market analysis before offer design |
| c-level (vision-chief) | Strategic decision support |
| copy-chief | Swipe files → copy frameworks |

## Boundary

- **In scope:** Research (deep, market, tech), competitive intelligence, benchmarking, evidence-based analysis, bias detection, decision support
- **Out of scope:** Creative execution (@copy, @brand), strategic decision making (@c-level consumes spy outputs), product strategy (@hormozi consumes spy outputs)

## Tasks Canônicas (59 total)

Extensive library covering: deep research templates, PICO question formulation, systematic review protocols, benchmark methodologies, competitor clone procedures, swipe file generators, evidence hierarchy checklists, bias assessment frameworks, DORA metric collection, OSINT techniques.
