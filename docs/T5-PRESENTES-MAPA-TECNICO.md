# 🗺️ Mapa Técnico Detalhado - T5 PRESENTES Integration
**Guia de Estrutura de Diretórios e Ativação**

---

## 📁 ESTRUTURA COMPLETA DE INTEGRAÇÃO

### Localização Atual (Origem)
```
C:\Users\User\Documents\2026\Projects_Smart_Systems\
└── Projeto_Investigação_Arquivos\Arquivos_Diversos\T5 PRESENTES\
    ├── squads/                    (8 equipes multi-agente)
    ├── skills/                    (8 skills individuais)
    └── docs/bench/               (análises e documentação)
```

### Localização Destino (Projeto SIE)
```
C:\Users\User\Documents\2026\Projects_Smart_Systems\Projeto_SIE\
├── .claude/
│   ├── skills/                   ← SKILLS (8 arquivos)
│   ├── agents/                   ← COPYWRITERS (27 agentes)
│   ├── settings.json             ← REGISTRY
│   ├── SKILL-REGISTRY.md         ← ÍNDICE
│   └── .t5-COMMANDS.md          ← REFERENCE
│
├── .aiox/
│   ├── squads/                  ← SQUADS (8 equipes)
│   └── data/                    ← CONFIGURAÇÕES
│
└── docs/
    ├── T5-PRESENTES-PLANO-INSTALACAO-COMPLETO.md
    ├── T5-PRESENTES-MAPA-TECNICO.md
    └── t5-research/             ← DOCUMENTAÇÃO (30+ arquivos)
```

---

## 🎯 SQUADS - Mapeamento Completo

### Squad 1: RESEARCH (Pesquisa Profunda)

**Localização Origem:** `T5 PRESENTES/squads/research/`

**Localização Destino:** `.aiox/squads/t5-research/`

**Estrutura Interna:**
```
t5-research/
├── agents/
│   ├── spy.md                      # Orquestrador, análises rápidas
│   ├── research-head.md            # Pesquisa estratégica
│   └── bench-analyst.md            # Especialista em benchmarks
├── tasks/
│   ├── perform-market-research.md
│   ├── create-competitor-analysis.md
│   ├── benchmark-analysis.md
│   └── brainstorm-discovery.md
├── templates/
│   ├── market-research-tmpl.yaml
│   ├── competitor-analysis-tmpl.yaml
│   └── benchmark-report-tmpl.yaml
├── checklists/
│   ├── research-completeness.md
│   └── competitor-profile-checklist.md
├── workflows/
│   ├── market-research-workflow.yaml
│   └── benchmark-pipeline.yaml
└── config.yaml
```

**Ativação:**
- Skill CLI: `/t5-research-chief`
- Agente: `@t5-spy`, `@t5-research-head`, `@t5-bench-analyst`
- Squad: `@t5-squad-research`
- Alias rápido: `@research-chief`

**Comandos Principais:**
```bash
*perform-market-research {topic}
*create-competitor-analysis {competitors}
*brainstorm {topic}
*analyze-trends {market}
```

**Outputs Esperados:**
- `market-research.md` (Markdown)
- `competitor-matrix.json` (Matriz comparativa)
- `benchmark-scorecard.json` (Pontuação)
- `battle-card.md` (Resumo executivo)

---

### Squad 2: COPY (Copywriting Elite)

**Localização Origem:** `T5 PRESENTES/squads/copy/`

**Localização Destino:** `.aiox/squads/t5-copy/`

**Estrutura Interna:**
```
t5-copy/
├── agents/                         # 27 COPYWRITERS CLÁSSICOS
│   ├── TIER_0_DIAGNOSTICO/
│   │   ├── claude-hopkins.md       # Publicidade científica
│   │   ├── eugene-schwartz.md      # 5 níveis de consciência
│   │   └── robert-collier.md       # Psicologia da conversação
│   │
│   ├── TIER_1_MASTERS/
│   │   ├── gary-halbert.md         # Cartas de vendas ($500M+)
│   │   ├── gary-bencivenga.md      # Bullets (80% success)
│   │   ├── david-ogilvy.md         # Branding premium
│   │   ├── clayton-makepeace.md    # Copy-response analysis
│   │   ├── control-data.md         # Testing & optimization
│   │   ├── joe-vitale.md           # Hypnotic writing
│   │   ├── john-caples.md          # Classic headlines
│   │   └── herschell-gordon-lewis.md # Direct response
│   │
│   ├── TIER_2_SISTEMATIZADORES/
│   │   ├── dan-kennedy.md          # Urgência & escassez
│   │   ├── jeff-walker.md          # Product Launch Formula (PLF)
│   │   ├── alex-hormozi.md         # Ofertas de $100M
│   │   ├── perry-marshall.md       # Direct response + Google Ads
│   │   ├── ryan-deiss.md           # Funnels de conversão
│   │   ├── russell-brunson.md      # Sales funnel automation
│   │   └── frank-kern.md           # Product creation
│   │
│   ├── TIER_3_ESPECIALISTAS_FORMATO/
│   │   ├── jon-benson.md           # VSL (Video Sales Letter)
│   │   ├── dan-koe.md              # Escrita digital
│   │   ├── andre-chaperon.md       # Soap opera sequences
│   │   ├── ann-gynn.md             # Email sequences
│   │   ├── michel-fortin.md        # Copywriting principles
│   │   ├── swoon-note.md           # Swoon bullets
│   │   └── joe-sugarman.md         # 30 Triggers de conversão
│   │
│   └── copy-chief.md               # Orquestrador principal
│
├── tasks/
│   ├── diagnose-copy-project.md
│   ├── recommend-copywriter.md
│   ├── create-sales-page.md
│   ├── write-email-sequence.md
│   ├── create-headlines.md
│   ├── write-vsl-script.md
│   └── validate-sugarman-triggers.md
│
├── templates/
│   ├── sales-page-tmpl.yaml
│   ├── email-sequence-tmpl.yaml
│   ├── vsl-script-tmpl.yaml
│   ├── headline-bank-tmpl.yaml
│   └── offer-framework-tmpl.yaml
│
├── checklists/
│   ├── sales-page-checklist.md
│   ├── email-copy-checklist.md
│   ├── vsl-script-checklist.md
│   ├── headline-criteria.md
│   └── 30-sugarman-triggers-checklist.md
│
├── workflows/
│   ├── copy-diagnosis-workflow.yaml
│   ├── sales-page-creation.yaml
│   ├── email-sequence-workflow.yaml
│   └── offer-creation.yaml
│
├── data/
│   ├── copywriter-expertise-map.json
│   ├── copy-frameworks.yaml
│   ├── sugarman-30-triggers.json
│   └── plf-template-structure.yaml
│
└── config.yaml
```

**Ativação:**
- Skill CLI: `/t5-squad-copy`
- Agente Principal: `@copy-chief`
- Agentes Tier 0: `@claude-hopkins`, `@eugene-schwartz`, `@robert-collier`
- Agentes Tier 1: `@gary-halbert`, `@gary-bencivenga`, `@david-ogilvy`, ... (5 mais)
- Agentes Tier 2: `@dan-kennedy`, `@jeff-walker`, `@alex-hormozi`, ... (4 mais)
- Agentes Tier 3: `@jon-benson`, `@dan-koe`, `@andre-chaperon`, ... (4 mais)
- Squad: `@t5-squad-copy`
- Alias: `@copy-chief` (direto)

**Workflow Padrão:**
```bash
@copy-chief
*diagnose {project-description}
# → Returns: Recommended tier + copywriter

@gary-halbert
*sales-page {offer}
# → Returns: Full sales page

@joe-sugarman
*validate-triggers
# → Returns: 30-trigger validation checklist
```

**Outputs Esperados:**
- `sales-page.md` (Full page)
- `email-sequence.md` (5-7 emails)
- `vsl-script.txt` (Video script)
- `headlines-bank.txt` (50+ opções)
- `sugarman-validation.json` (30 triggers)

---

### Squad 3: DESIGN-SYSTEM (Design Systems & Tokens)

**Localização Origem:** `T5 PRESENTES/squads/design-system/`

**Localização Destino:** `.aiox/squads/t5-design-system/`

**Estrutura Interna:**
```
t5-design-system/
├── agents/
│   ├── design-chief.md             # Orquestrador
│   ├── token-architect.md          # Design tokens
│   ├── pattern-librarian.md        # Component patterns
│   └── accessibility-guardian.md   # A11y validation
├── tasks/
│   ├── audit-design-system.md
│   ├── extract-tokens.md
│   ├── build-pattern-library.md
│   ├── create-documentation.md
│   └── accessibility-audit.md
├── templates/
│   ├── token-manifest-tmpl.yaml
│   ├── pattern-spec-tmpl.yaml
│   ├── component-library-tmpl.yaml
│   └── design-doc-tmpl.md
├── checklists/
│   ├── design-system-completeness.md
│   ├── token-coverage.md
│   ├── pattern-library-checklist.md
│   └── accessibility-wcag-2.1-aa.md
└── workflows/
    ├── design-system-audit.yaml
    ├── token-extraction.yaml
    └── component-documentation.yaml
```

**Ativação:**
- Skill CLI: `/t5-design-chief`
- Squad: `@t5-squad-design-system`
- Alias: `@design-chief`

**Comandos:**
```bash
@design-chief
*audit-codebase
# → Returns: Design system audit

*extract-tokens {codebase}
# → Returns: token-manifest.yaml

*build-library
# → Returns: Pattern library documentation
```

---

### Squad 4: DESIGN-OPS (DesignOps & Workflows)

**Localização Origem:** `T5 PRESENTES/squads/design-ops/`

**Localização Destino:** `.aiox/squads/t5-design-ops/`

**Estrutura:**
```
t5-design-ops/
├── agents/
│   ├── designops-chief.md
│   ├── process-optimizer.md
│   ├── tooling-architect.md
│   └── team-enabler.md
├── tasks/
│   ├── audit-design-processes.md
│   ├── optimize-workflow.md
│   ├── design-toolchain.md
│   └── enable-team.md
├── templates/ & checklists/
└── workflows/
```

---

### Squad 5: SLIDES-CREATOR (Apresentações Profissionais)

**Localização Origem:** `T5 PRESENTES/squads/slides-creator/`

**Localização Destino:** `.aiox/squads/t5-slides-creator/`

**Estrutura:**
```
t5-slides-creator/
├── agents/
│   ├── slides-chief.md
│   ├── narrative-architect.md
│   ├── visual-designer.md
│   └── output-renderer.md
├── tasks/
│   ├── analyze-audience.md
│   ├── create-narrative.md
│   ├── design-visuals.md
│   └── render-deck.md
├── templates/
│   ├── pitch-deck-tmpl.yaml
│   ├── training-deck-tmpl.yaml
│   └── executive-deck-tmpl.yaml
├── examples/
│   ├── design-100-fixture/
│   └── pitch-deck-fixture/
└── references/
    ├── narrative-patterns.md
    ├── design-system.md
    └── output-contracts.md
```

---

### Squad 6: HORMOZI (Metodologia de Ofertas - Alex Hormozi)

**Localização Origem:** `T5 PRESENTES/squads/hormozi/`

**Localização Destino:** `.aiox/squads/t5-hormozi/`

**Estrutura:**
```
t5-hormozi/
├── agents/
│   ├── hormozi-chief.md
│   ├── offer-architect.md
│   ├── pricing-strategist.md
│   └── value-designer.md
├── tasks/
│   ├── discover-problems.md
│   ├── design-offer.md
│   ├── calculate-unit-economics.md
│   └── build-delivery-mechanism.md
├── templates/
│   ├── offer-framework-tmpl.yaml
│   ├── unit-economics-tmpl.json
│   └── delivery-spec-tmpl.yaml
└── workflows/
    └── hormozi-4-part-workflow.yaml
```

---

### Squad 7: AIOX-SOP (Standard Operating Procedures)

**Localização Origem:** `T5 PRESENTES/squads/aiox-sop/`

**Localização Destino:** `.aiox/squads/t5-sop/`

**Estrutura Completa:**
```
t5-sop/
├── agents/                         # 6 AGENTES
│   ├── sop-chief.md                # Orquestrador
│   ├── sop-creator.md              # Cria SOPs
│   ├── sop-extractor.md            # Extrai de processos
│   ├── sop-analyst.md              # Analisa qualidade
│   ├── sop-auditor.md              # Validação
│   └── sop-ml-architect.md         # Integração de ML
│
├── tasks/
│   ├── extract-sop-from-process.md
│   ├── create-sop.md
│   ├── analyze-sop-quality.md
│   ├── audit-sop-compliance.md
│   └── build-ml-sop.md
│
├── checklists/
│   ├── sop-completeness-checklist.md
│   ├── extraction-completeness-checklist.md
│   ├── sop-quality-checklist.md
│   ├── sop-ml-validation-checklist.md
│   ├── 14-point-crosby-checklist.md
│   └── stranger-test-checklist.md
│
├── templates/
│   ├── sop-standard-template.md
│   ├── process-extraction-tmpl.yaml
│   └── ml-integration-tmpl.yaml
│
├── data/
│   ├── category-map.yaml
│   ├── confidence-levels.yaml
│   ├── infrastructure-connections.yaml
│   ├── risk-register.yaml
│   └── market-categories.yaml
│
├── workflows/
│   ├── sop-extraction-workflow.yaml
│   ├── sop-creation-workflow.yaml
│   └── sop-validation-workflow.yaml
│
└── config.yaml
```

**Ativação:**
- Skill CLI: `/t5-sop-chief`
- Squad: `@t5-squad-sop`
- Agentes: `@sop-creator`, `@sop-extractor`, `@sop-analyst`, `@sop-auditor`, `@sop-ml-architect`
- Alias: `@sop-chief`

**Comandos:**
```bash
@sop-chief
*extract "processo de vendas"
# → Returns: SOP draft

*validate {sop-file}
# → Returns: Validation report (14-point Crosby)

*publish
# → Returns: Publication-ready SOP
```

---

### Squad 8: SPY (Análise de Conteúdo & Inteligência)

**Localização Origem:** `T5 PRESENTES/squads/spy/`

**Localização Destino:** `.aiox/squads/t5-spy/`

**Estrutura:**
```
t5-spy/
├── agents/
│   ├── spy-chief.md
│   ├── content-analyst.md
│   ├── intel-gatherer.md
│   └── trend-spotter.md
├── tasks/
│   ├── analyze-content.md
│   ├── gather-competitive-intel.md
│   ├── spot-trends.md
│   └── summarize-findings.md
├── templates/ & checklists/
└── workflows/
```

---

## 🎯 SKILLS - Mapeamento Completo

### Skill 1: RESEARCH-BENCH

**Origem:** `T5 PRESENTES/skills/research-bench/SKILL.md`

**Destino:** `.claude/skills/t5-research-bench/SKILL.md`

**Ativação:** `/t5-research-bench`

**Funcionalidade:** Benchmarking comparativo de produtos/competidores

**Entrada/Saída:**
```
Input:  "Compare Product A vs B vs C"
Output: 
  - comparison-matrix.md
  - scorecard.json
  - battle-card.md
  - gap-analysis.json
```

---

### Skill 2: RESEARCH-CHIEF

**Origem:** `T5 PRESENTES/skills/research-chief/SKILL.md`

**Destino:** `.claude/skills/t5-research-chief/SKILL.md`

**Ativação:** `/t5-research-chief`

**Funcionalidade:** Coordenador de pesquisa (meta-skill para squad)

---

### Skill 3: DESIGN-CHIEF

**Origem:** `T5 PRESENTES/skills/design-chief/SKILL.md`

**Destino:** `.claude/skills/t5-design-chief/SKILL.md`

**Ativação:** `/t5-design-chief`

**Funcionalidade:** Coordenador de design

---

### Skill 4: DESIGN-MD

**Origem:** `T5 PRESENTES/skills/design-md/SKILL.md`

**Destino:** `.claude/skills/t5-design-md/SKILL.md`

**Ativação:** `/t5-design-md`

**Funcionalidade:** Design em markdown format

---

### Skill 5: SLIDE-CREATOR

**Origem:** `T5 PRESENTES/skills/slide-creator/SKILL.md`

**Destino:** `.claude/skills/t5-slide-creator/SKILL.md`

**Ativação:** `/t5-slide-creator`

**Funcionalidade:** Criação de apresentações profissionais

---

### Skill 6: RESEARCH-MARKETING-DEEPDIVE

**Origem:** `T5 PRESENTES/skills/research-marketing-deepdive/SKILL.md`

**Destino:** `.claude/skills/t5-research-marketing/SKILL.md`

**Ativação:** `/t5-research-marketing`

**Funcionalidade:** Deep dive em pesquisa de marketing

---

### Skill 7: SOP-CHIEF

**Origem:** `T5 PRESENTES/skills/sop-chief/SKILL.md`

**Destino:** `.claude/skills/t5-sop-chief/SKILL.md`

**Ativação:** `/t5-sop-chief`

**Funcionalidade:** Gerenciador de SOPs

---

### Skill 8: TECH-RESEARCH

**Origem:** `T5 PRESENTES/skills/tech-research/SKILL.md`

**Destino:** `.claude/skills/t5-tech-research/SKILL.md`

**Ativação:** `/t5-tech-research`

**Funcionalidade:** Pesquisa técnica e arquitetura

---

## 📚 DOCUMENTATION - Mapeamento

### Origem
```
T5 PRESENTES/docs/bench/
├── 2026-05-17-fazer-um-benchmark-top-10-das-melhores/
│   ├── battle-card.md
│   ├── comparison-matrix.md
│   ├── comparison-matrix.json
│   ├── executive-report.md
│   ├── gap-analysis.md
│   ├── inventory-players.md
│   ├── scorecard.md
│   ├── deep/
│   │   ├── feature-comparison.md
│   │   ├── pricing-analysis.md
│   │   ├── reviews-sentiment.md
│   │   └── ux-analysis.md
│   └── (+ 7 arquivos JSON)
│
└── 3-way-final-omnichannel/
    ├── ai-capability-ranking.md
    ├── battle-card-3way.md
    ├── consolidated-scorecard.md
    ├── cross-bench-matrix.md
    ├── executive-report-3way.md
    ├── final-recommendation-matrix.md
    └── (+ 9 arquivos JSON)
```

### Destino
```
Projeto_SIE/docs/t5-research/
├── README.md (Índice)
├── benchmarks/
│   ├── 2026-05-17-top-10/
│   │   └── (todos os 15 arquivos)
│   └── 3-way-omnichannel/
│       └── (todos os 11 arquivos)
└── analysis-templates/
    └── (templates reutilizáveis)
```

---

## ⚙️ CONFIGURAÇÃO & REGISTRY

### `.claude/SKILL-REGISTRY.md`

```markdown
# T5 PRESENTES - Skill Registry

## Skills Disponíveis (8)

### Research & Analysis
- [ ] `/t5-research-bench` — Benchmarking comparativo
- [ ] `/t5-research-chief` — Coordenador de pesquisa
- [ ] `/t5-research-marketing` — Marketing deep dive
- [ ] `/t5-tech-research` — Pesquisa técnica

### Design
- [ ] `/t5-design-chief` — Coordenador de design
- [ ] `/t5-design-md` — Design em markdown

### Content
- [ ] `/t5-slide-creator` — Criador de slides

### Operations
- [ ] `/t5-sop-chief` — Gerenciador de SOPs

## Squads Disponíveis (8)

### Multi-Agent Teams
- [ ] `@t5-squad-research` — 3 agentes
- [ ] `@t5-squad-copy` — 27 copywriters
- [ ] `@t5-squad-design-system` — Design systems
- [ ] `@t5-squad-design-ops` — DesignOps
- [ ] `@t5-squad-slides` — Apresentações
- [ ] `@t5-squad-hormozi` — Ofertas
- [ ] `@t5-squad-sop` — SOPs (6 agentes)
- [ ] `@t5-squad-spy` — Análise de conteúdo

## Direct Aliases

- `@copy-chief` → `@t5-squad-copy`
- `@research-chief` → `@t5-research-chief`
- `@design-chief` → `@t5-design-chief`
- `@sop-chief` → `@t5-sop-chief`
```

### `.claude/settings.json` - Adições

```json
{
  "skills": {
    "t5-presentes": {
      "enabled": true,
      "components": {
        "research-bench": "/t5-research-bench",
        "research-chief": "/t5-research-chief",
        "design-chief": "/t5-design-chief",
        "design-md": "/t5-design-md",
        "slide-creator": "/t5-slide-creator",
        "research-marketing": "/t5-research-marketing",
        "sop-chief": "/t5-sop-chief",
        "tech-research": "/t5-tech-research"
      },
      "squads": {
        "research": "@t5-squad-research",
        "copy": "@t5-squad-copy",
        "design-system": "@t5-squad-design-system",
        "design-ops": "@t5-squad-design-ops",
        "slides": "@t5-squad-slides",
        "hormozi": "@t5-squad-hormozi",
        "sop": "@t5-squad-sop",
        "spy": "@t5-squad-spy"
      },
      "aliases": {
        "copy-chief": "@t5-squad-copy",
        "research-chief": "@t5-research-chief",
        "design-chief": "@t5-design-chief",
        "sop-chief": "@t5-sop-chief"
      }
    }
  }
}
```

---

## 🔄 FLUXO DE ATIVAÇÃO TÉCNICO

### 1. CLI Registration
```bash
# Arquivo: .claude/SKILL-REGISTRY.md
# Resultado: `/t5-*` aparece em tab completion
```

### 2. Settings Injection
```bash
# Arquivo: .claude/settings.json
# Resultado: Aliases funcionam (@copy-chief → @t5-squad-copy)
```

### 3. Agent Loading
```bash
# Arquivo: .aiox/squads/t5-{squad}/agents/{agent}.md
# Resultado: Agentes carregam com persona completa
```

### 4. Task Execution
```bash
# Arquivo: .aiox/squads/t5-{squad}/tasks/{task}.md
# Resultado: `*comando` executa workflow
```

### 5. Template Rendering
```bash
# Arquivo: .aiox/squads/t5-{squad}/templates/{template}.yaml
# Resultado: Outputs renderizados conforme especificação
```

---

## 🧪 TESTE TÉCNICO (5-STEP)

### Step 1: Skill Registry
```bash
cat .claude/SKILL-REGISTRY.md
# Esperado: 8 skills + 8 squads listados
```

### Step 2: CLI Activation
```bash
# Type: /t5-
# Expected: autocomplete shows 8 skills
```

### Step 3: Skill Loading
```bash
/t5-research-bench
# Expected: Skill carrega com persona Atlas
```

### Step 4: Agent Loading
```bash
@copy-chief
# Expected: 27 copywriters carregam, *help mostra todos
```

### Step 5: Task Execution
```bash
@copy-chief
*diagnose "sales page for SaaS product"
# Expected: Recomendação de copywriter + tier classification
```

---

## 🔐 Permissões & Segurança

### Arquivo Permissions
```bash
# Scripts executáveis
.aiox/squads/t5-*/scripts/*.js    → 755

# Configuração sensível
.aiox/squads/t5-*/data/secrets.* → 600

# Documentação
.aiox/squads/t5-*/agents/*.md    → 644
```

### API Keys & Credentials
```bash
# NUNCA em arquivo de configuração
# SEMPRE em .env ou secrets manager

# .env (exemplo):
T5_RESEARCH_API_KEY=xxx
T5_COPY_OPENAI_KEY=xxx
T5_DESIGN_FIGMA_TOKEN=xxx
```

---

## 🚀 Quick Reference - Commands

```bash
# Research
/t5-research-bench                # Skill individual
@t5-squad-research               # Squad completo

# Copy (27 copywriters)
@copy-chief                       # Orquestrador
@gary-halbert                     # Copywriter específico
@joe-sugarman                     # Outro copywriter

# Design
/t5-design-chief                  # Skill
@t5-squad-design-system          # Squad

# Operations
/t5-sop-chief                     # Skill
@t5-squad-sop                    # Squad (6 agentes)

# Content
/t5-slide-creator                 # Skill
@t5-squad-slides                 # Squad
```

---

**Versão:** 1.0  
**Data:** 21 Junho 2026  
**Autor:** Atlas (Investigação Técnica)  
**Status:** 🟢 Pronto para Implementação Técnica

