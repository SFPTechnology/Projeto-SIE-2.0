# 📦 Plano Estratégico de Instalação Completo - T5 PRESENTES
**Síntese Executiva**

---

## 🎯 Visão Geral

O **T5 PRESENTES** é um pacote profissional AIOX que fornece 8 squads especializados + 8 skills individuais + documentação de pesquisa avançada. Implementa soluções end-to-end para:
- **Pesquisa & Análise Competitiva** (benchmarks, market intelligence)
- **Copywriting & Marketing** (27 copywriters virtualizados)
- **Design & Design Systems** (tokens, pattern libraries, DesignOps)
- **Apresentações & Narrativa** (slide decks profissionais)
- **SOPs & Operações** (procedimentos operacionais padrão)
- **Inteligência & Análise de Conteúdo** (Spy squad)

---

## 📊 ESTRUTURA DESCOBERTA

### Organização Principal (3 camadas)

```
T5 PRESENTES/
├── 📂 SQUADS/ (8 equipes especializadas)
│   ├── research/              # Pesquisa profunda + benchmarks (spy, research-head, bench-analyst)
│   ├── copy/                  # Copywriting elite (27 copywriters clássicos)
│   ├── design-system/         # Design systems (tokens, patterns, atomic design)
│   ├── design-ops/            # DesignOps (workflows, process, tooling)
│   ├── slides-creator/        # Criação de slides (narrativa + design)
│   ├── hormozi/               # Metodologia de ofertas (Alex Hormozi)
│   ├── aiox-sop/              # SOPs (procedimentos padrão - 6 agentes)
│   └── spy/                   # Análise de conteúdo & inteligência
│
├── 📂 SKILLS/ (8 habilidades individuais)
│   ├── research-bench/        # Benchmarking tool
│   ├── research-chief/        # Coordenador de pesquisa
│   ├── research-marketing-deepdive/
│   ├── design-chief/          # Coordenador de design
│   ├── design-md/             # Design em markdown
│   ├── slide-creator/         # Criador de slides
│   ├── sop-chief/             # Gerenciador de SOP
│   └── tech-research/         # Pesquisa técnica
│
└── 📂 DOCS/ (Pesquisa & análises)
    └── bench/
        ├── 2026-05-17-fazer-um-benchmark-top-10-das-melhores/
        │   ├── battle-card.md
        │   ├── comparison-matrix.md
        │   ├── executive-report.md
        │   ├── gap-analysis.md
        │   ├── scorecard.md
        │   └── (+ 15 arquivos de análise profunda)
        └── 3-way-final-omnichannel/
            ├── consolidated-scorecard.md
            ├── final-recommendation-matrix.md
            └── (+ análises de 4 players)
```

---

## 🚀 FASE 1: DIAGNÓSTICO TÉCNICO

### 1.1 Verificação de Pré-Requisitos

- [x] **Local de origem:** `C:\Users\User\Documents\2026\Projects_Smart_Systems\Projeto_Investigação_Arquivos\Arquivos_Diversos\T5 PRESENTES`
- [x] **Destino:** `C:\Users\User\Documents\2026\Projects_Smart_Systems\Projeto_SIE\.claude/` (sistema de skills/agents)
- [x] **Git repositório:** ✅ Ativo (branch: `feature/nbr5410-conformidade-closeout`)
- [x] **Estrutura AIOX:** ✅ Presente (`.aiox-core/`, `docs/stories/`, etc.)

### 1.2 Inventário de Componentes

| Categoria | Qtd | Tipo | Instalação |
|-----------|-----|------|-----------|
| **SQUADS** | 8 | Equipes multi-agente | Cópia + Ativação |
| **SKILLS** | 8 | Slash commands | Integração + Ativação |
| **DOCS** | 30+ | Markdown + JSON | Importação |
| **AGENTS** (em squads) | 27+ | Personas de copywriters | Automática via squad |
| **CHECKLISTS** | 6 | Validação de qualidade | Integração |
| **TEMPLATES** | 12+ | Modelos reutilizáveis | Importação |
| **WORKFLOWS** | 8 | Processos orquestrados | Ativação |
| **DATA FILES** | 20+ | Config, mappings, registries | Integração |

---

## 📋 FASE 2: PLANO DE INSTALAÇÃO (4 ETAPAS)

### ETAPA 1️⃣: Copiar Artefatos Núcleo

**Objetivo:** Trazer T5 PRESENTES para a estrutura AIOX do Projeto-SIE

```bash
# Locais de cópia:
SRC = C:\Users\User\Documents\2026\Projects_Smart_Systems\Projeto_Investigação_Arquivos\Arquivos_Diversos\T5 PRESENTES
DEST = C:\Users\User\Documents\2026\Projects_Smart_Systems\Projeto_SIE

# Estrutura de destino:
Projeto_SIE/
├── .claude/
│   ├── skills/
│   │   ├── t5-research-bench/           ← skills/research-bench
│   │   ├── t5-research-chief/           ← skills/research-chief
│   │   ├── t5-design-chief/             ← skills/design-chief
│   │   ├── t5-design-md/                ← skills/design-md
│   │   ├── t5-slide-creator/            ← skills/slide-creator
│   │   ├── t5-research-marketing/       ← skills/research-marketing-deepdive
│   │   ├── t5-sop-chief/                ← skills/sop-chief
│   │   └── t5-tech-research/            ← skills/tech-research
│   │
│   └── agents/ (opcional)
│       └── t5-copywriters/              ← squad/copy/agents
│
├── .aiox/
│   └── squads/                          ← squads/ (todos os 8)
│       ├── t5-research/
│       ├── t5-copy/
│       ├── t5-design-system/
│       ├── t5-design-ops/
│       ├── t5-slides-creator/
│       ├── t5-hormozi/
│       ├── t5-aiox-sop/
│       └── t5-spy/
│
└── docs/
    └── t5-research/                    ← docs/bench (todas as análises)
```

**Ações:**
- [ ] Copiar `skills/*` → `.claude/skills/t5-*/`
- [ ] Copiar `squads/*` → `.aiox/squads/t5-*/`
- [ ] Copiar `docs/bench/` → `docs/t5-research/`
- [ ] Preservar estrutura interna de cada componente

---

### ETAPA 2️⃣: Registrar Skills no Sistema AIOX

**Objetivo:** Fazer cada skill aparecer nos `/` commands do Claude Code

**Arquivos a criar/editar:**

#### A. **`.claude/SKILL-REGISTRY.md`** (índice mestre)

```markdown
# T5 PRESENTES - Skill Registry

## Research & Analysis
- `/t5-research-bench` — Benchmarking comparativo
- `/t5-research-chief` — Coordenador de pesquisa
- `/t5-research-marketing` — Deep dive em marketing
- `/t5-tech-research` — Pesquisa técnica

## Design
- `/t5-design-chief` — Coordenador de design
- `/t5-design-md` — Design em markdown

## Content & Presentations
- `/t5-slide-creator` — Criador de slides

## Operations
- `/t5-sop-chief` — Gerenciador de SOPs

## SQUADS (Multi-Agent Teams)
- `/t5-squad-research` — Equipe de pesquisa
- `/t5-squad-copy` — Equipe de copywriting (27 copywriters)
- `/t5-squad-design-system` — Equipe de design systems
- `/t5-squad-design-ops` — Equipe de DesignOps
- `/t5-squad-slides` — Equipe de apresentações
- `/t5-squad-hormozi` — Metodologia de ofertas
- `/t5-squad-sop` — Equipe de SOPs
- `/t5-squad-spy` — Equipe de análise de conteúdo
```

#### B. **`.claude/settings.json`** - Adicionar allowlist de skills

```json
{
  "skills": {
    "t5": {
      "research-bench": {
        "description": "Benchmarking and competitive analysis tool",
        "command": "/t5-research-bench"
      },
      "research-chief": {
        "description": "Research team coordinator",
        "command": "/t5-research-chief"
      },
      "design-chief": {
        "description": "Design system coordinator",
        "command": "/t5-design-chief"
      },
      "slide-creator": {
        "description": "Professional slide deck generator",
        "command": "/t5-slide-creator"
      },
      "sop-chief": {
        "description": "SOP management and automation",
        "command": "/t5-sop-chief"
      }
    }
  }
}
```

#### C. **Criar arquivo de ativação para cada skill**

Para cada skill, criar `{skillname}.ACTIVATION.md`:

```markdown
---
name: t5-research-bench
type: skill
slug: t5-research-bench
icon: 📊
description: Benchmarking and competitive analysis tool
activation_type: command
---

# t5-research-bench
[Conteúdo SKILL.md do skill copiado aqui]
```

**Ações:**
- [ ] Copiar `SKILL.md` de cada skill para `.claude/skills/t5-*/SKILL.md`
- [ ] Criar entrada em `SKILL-REGISTRY.md`
- [ ] Atualizar `settings.json` com referências
- [ ] Testar ativação: `/ t5-research-bench [TAB]`

---

### ETAPA 3️⃣: Configurar Squads & Agentes

**Objetivo:** Registrar squads multi-agentes (especialmente copy squad com 27 copywriters)

#### A. **Criar pasta `.aiox/squads/t5-*/`**

Para cada squad:
```
.aiox/squads/t5-{squad-name}/
├── agents/                    # 2-6 agentes por squad
│   ├── {agent-1}.md
│   ├── {agent-2}.md
│   └── ...
├── tasks/                     # Tasks executáveis
├── templates/                 # Modelos de saída
├── checklists/                # Validação de qualidade
├── workflows/                 # Orquestração
├── config.yaml               # Configuração
└── SQUAD.md                  # Documentação
```

#### B. **Casos Especiais:**

**Squad Copy (27 copywriters):**
- [x] `@copy-chief` — Orquestrador principal
- [x] Tier 0: Claude Hopkins, Eugene Schwartz, Robert Collier (diagnóstico)
- [x] Tier 1: Gary Halbert, Gary Bencivenga, David Ogilvy + 5 masters
- [x] Tier 2: Dan Kennedy, Jeff Walker, Alex Hormozi + sistematos
- [x] Tier 3: Jon Benson, Dan Koe, Andre Chaperon (especialistas de formato)

**Squad AIOX SOP (6 agentes):**
- [x] `sop-chief` — Orquestrador
- [x] `sop-creator` — Cria SOPs
- [x] `sop-extractor` — Extrai de processos
- [x] `sop-analyst` — Analisa qualidade
- [x] `sop-auditor` — Validação
- [x] `sop-ml-architect` — Integração de ML

**Ações:**
- [ ] Copiar estrutura de cada squad para `.aiox/squads/t5-*/`
- [ ] Registrar agentes em `.aiox/squads/t5-*/SQUAD.md`
- [ ] Para Copy squad: Mapear 27 copywriters em `.aiox/squads/t5-copy/agents/`
- [ ] Testar ativação: `@t5-copy-chief`, `@copy-chief` etc.

---

### ETAPA 4️⃣: Ativar Slash Commands (`/`)

**Objetivo:** Registrar todos os `/` commands no Claude Code

#### A. **Estrutura de Ativação de Skills**

```bash
# Para cada skill criado em .claude/skills/:
/t5-research-bench        → Abre research-bench skill
/t5-research-chief        → Abre research-chief skill
/t5-design-chief          → Abre design-chief skill
/t5-slide-creator         → Abre slide-creator skill
/t5-sop-chief             → Abre sop-chief skill
/t5-design-md             → Design em markdown
/t5-tech-research         → Pesquisa técnica
/t5-research-marketing    → Marketing deep dive

# Para cada squad criado em .aiox/squads/:
@t5-squad-copy            → Ativa copy squad (27 copywriters)
@t5-squad-research        → Ativa research squad
@t5-squad-design-system   → Design systems squad
@t5-squad-design-ops      → DesignOps squad
@t5-squad-sop             → SOP squad (6 agentes)
@t5-squad-spy             → Spy/análise squad
@t5-squad-slides          → Slides creator squad
@t5-squad-hormozi         → Ofertas squad

# Aliases diretos para copiers populares:
@copy-chief               → Equivalente a @t5-squad-copy
@research-chief           → Equivalente a @t5-research-chief
@design-chief             → Equivalente a @t5-design-chief
```

#### B. **Arquivo de Registro Global**

Criar `.claude/.t5-COMMANDS.md`:

```markdown
# T5 PRESENTES - Slash Commands Reference

## Quick Access

### Research & Analysis (3 cliques)
1. Type: `/t5-research-bench`
2. Or: `/t5-research-chief`
3. Or: `/t5-research-marketing`

### Design
1. Type: `/t5-design-chief`
2. Or: `/t5-design-md`

### Copywriting (Elite Team)
1. Type: `/t5-squad-copy` (ativa 27 copywriters)
2. Then: `@copy-chief` para orquestradora
3. Then: `@gary-halbert`, `@dan-kennedy`, etc.

### SOPs & Operações
1. Type: `/t5-sop-chief`
2. Or: `@t5-squad-sop`

### Squads Completos
- `@t5-squad-research` — Pesquisa profunda
- `@t5-squad-copy` — Copywriting elite
- `@t5-squad-design-system` — Design systems
- `@t5-squad-design-ops` — DesignOps
- `@t5-squad-sop` — Operações padrão
- `@t5-squad-spy` — Análise de conteúdo
- `@t5-squad-slides` — Apresentações
- `@t5-squad-hormozi` — Metodologia de ofertas

## Command Activation Steps

1. **Ativar skill:**
   ```
   /t5-research-bench
   *brainstorm
   ```

2. **Ativar agente:**
   ```
   @copy-chief
   *recommend
   @gary-halbert
   *sales-page
   ```

3. **Ativar squad inteiro:**
   ```
   @t5-squad-copy
   *diagnose
   ```

## Troubleshooting

- Skill não aparece em `/`? → Verifique `.claude/skills/t5-*/SKILL.md`
- Agente não responde? → Verifique `.aiox/squads/t5-*/agents/`
- Squad não carrega? → Rode `aiox doctor` para diagnóstico
```

**Ações:**
- [ ] Criar `.claude/SKILL-REGISTRY.md` com todas as skills
- [ ] Criar `.claude/.t5-COMMANDS.md` com referência de commands
- [ ] Adicionar entradas em `.claude/settings.json`
- [ ] Testar cada `/` command manualmente
- [ ] Documentar aliases de acesso rápido

---

## ✅ FASE 3: CHECKLIST DE QUALIDADE

### 3.1 Validação de Cópia

- [ ] Todos os 8 squads copiados → `.aiox/squads/t5-*/`
- [ ] Todos os 8 skills copiados → `.claude/skills/t5-*/`
- [ ] Todos os docs copiados → `docs/t5-research/`
- [ ] Estrutura interna preservada (agents/, tasks/, templates/, etc.)
- [ ] Nenhum arquivo quebrado ou truncado

### 3.2 Validação de Ativação

- [ ] Cada `/t5-*` command aparece no tab completion
- [ ] Cada `@t5-*-squad` reconhecido como agente
- [ ] `@copy-chief` dispara 27 copywriters
- [ ] `@research-chief` dispara equipe de pesquisa
- [ ] `@design-chief` dispara equipe de design
- [ ] `@sop-chief` dispara equipe AIOX-SOP

### 3.3 Validação de Funcionalidade

**Research Squad:**
- [ ] `/t5-research-bench` executa benchmarks
- [ ] `*brainstorm` gera ideação estruturada
- [ ] Outputs em Markdown + JSON validados

**Copy Squad:**
- [ ] `@copy-chief` carrega 27 copywriters
- [ ] `*diagnose` retorna recomendação
- [ ] Cada copywriter selecionável (Halbert, Bencivenga, etc.)
- [ ] `*sales-page` gera página profissional

**Design Squad:**
- [ ] `/t5-design-chief` carrega
- [ ] `/t5-design-md` gera design em markdown
- [ ] Tokens e patterns acessíveis

**SOP Squad:**
- [ ] `@t5-squad-sop` carrega 6 agentes
- [ ] `*extract` extrai procedimentos
- [ ] Checklists de qualidade funcionais

### 3.4 Validação de Integração

- [ ] Documentos benchmark acessíveis em `docs/t5-research/`
- [ ] Templates carregáveis via squad
- [ ] Checklists integradas no workflow
- [ ] Dados de config aplicados corretamente

---

## 🎬 FASE 4: ATIVAÇÃO SEQUENCIAL

### Ordem Recomendada de Ativação

**Dia 1: Fundação**
1. Copiar squads + skills → `.aiox/` e `.claude/`
2. Registrar em `SKILL-REGISTRY.md` e `settings.json`
3. Testar `/t5-research-bench` (skill simples)
4. Validar 3 comandos: `/`, `@`, `*help`

**Dia 2: Pesquisa**
5. Ativar `@t5-squad-research` (3 agentes)
6. Executar `*brainstorm {topic}`
7. Testar `*perform-market-research`
8. Validar outputs (Markdown + JSON)

**Dia 3: Design & Copy**
9. Ativar `@t5-squad-copy` (27 copywriters)
10. Ativar `@copy-chief` (orquestrador)
11. Executar `*diagnose` para teste
12. Selecionar `@gary-halbert` ou outro
13. Ativar `@t5-squad-design-system`

**Dia 4: Operações**
14. Ativar `@t5-squad-sop` (6 agentes)
15. Testar `*extract` em processo real
16. Executar `*create-sop`
17. Validar checklists de qualidade

**Dia 5: Integração Final**
18. Linkar squads ao workflow AIOX existente
19. Criar stories no `docs/stories/` para usar T5
20. Documentar SOPs de uso em `.claude/README-T5.md`
21. Deploy em produção

---

## 📈 FASE 5: DOCUMENTAÇÃO & CONHECIMENTO

### 5.1 Documentação de Uso

Criar `docs/T5-PRESENTES-README.md`:

```markdown
# T5 PRESENTES - Quick Start Guide

## 🎯 Cenários de Uso

### Cenário 1: Comparar Produtos
```bash
/t5-research-bench
*compare "Product A" "Product B"
```

### Cenário 2: Escrever Página de Vendas
```bash
@copy-chief
*diagnose
@gary-halbert
*sales-page
```

### Cenário 3: Criar Design System
```bash
@t5-squad-design-system
*analyze-codebase
*extract-tokens
*create-library
```

### Cenário 4: Documentar Procedimento
```bash
@t5-squad-sop
*extract "processo X"
*validate
*publish
```
```

### 5.2 Integração com Stories

Criar stories para usar T5:
- `docs/stories/T5.1-Pesquisa-Competitiva.md` — Use research squad
- `docs/stories/T5.2-Copywriting-Vendas.md` — Use copy squad
- `docs/stories/T5.3-Design-System.md` — Use design squad
- `docs/stories/T5.4-SOP-Operacional.md` — Use SOP squad

### 5.3 Memory & Knowledge Base

Salvar em `.claude/projects/{slug}/MEMORY.md`:
```markdown
# T5 PRESENTES Integration Memory

## Squads Ativos
- Copy: 27 copywriters virtualizados
- Research: 3 agentes (spy, research-head, bench-analyst)
- Design: 2 squads (system + ops)
- SOP: 6 agentes (chief, creator, extractor, analyst, auditor, ml-arch)

## Workflows Críticos
- Research → Benchmark → Battle Card → Exec Report
- Copy: Diagnose → Recommend → Execute → Validate (Sugarman 30-trigger check)
- Design: Audit → Extract → Library → Document

## Quick Commands
- `/t5-research-bench` — Benchmarking
- `@copy-chief` — Elite copywriting
- `@t5-squad-design-system` — Design systems
- `@t5-squad-sop` — Operações
```

---

## 🔐 FASE 6: SEGURANÇA & CONFORMIDADE

### 6.1 Validação de Segurança

- [ ] Nenhuma chave privada exposta em arquivos
- [ ] Credenciais de API em `.env` (não em código)
- [ ] Permissões de arquivo corretas (600 para secrets)
- [ ] Audit trail de quem rodou qual comando

### 6.2 Conformidade AIOX

- [ ] Squads respeitam `Constitution.md` (Article IV - No Invention)
- [ ] Templates seguem padrões AIOX
- [ ] Workflows documentados em `.aiox-core/workflows/`
- [ ] Agentes registrados em `.aiox/agents/`

---

## 📊 RESUMO EXECUTIVO - TIMELINE

| Fase | Etapa | Duração | Entrega |
|------|-------|---------|---------|
| 1 | Diagnóstico | 1h | Mapa de componentes |
| 2 | Cópia de artefatos | 2h | 8 squads + 8 skills |
| 2 | Registro de skills | 1h | SKILL-REGISTRY.md |
| 3 | Validação | 2h | Checklist completo |
| 4 | Ativação sequencial | 5 dias | Todos os 16 componentes |
| 5 | Documentação | 1h | README + stories |
| 6 | Segurança | 30min | Audit completo |
| **TOTAL** | — | **~12h** | **Sistema operacional** |

---

## 🚀 PRÓXIMOS PASSOS IMEDIATOS

1. **HOJE:** 
   - [ ] Copiar T5 PRESENTES → Projeto_SIE
   - [ ] Criar `.claude/SKILL-REGISTRY.md`
   
2. **AMANHÃ:**
   - [ ] Registrar skills em `settings.json`
   - [ ] Testar 3 `/` commands
   
3. **SEMANA:**
   - [ ] Ativar squads (copy, research, design, sop)
   - [ ] Criar 4 stories de teste
   - [ ] Deploy em produção

---

## 📞 CONTATO & SUPORTE

- **T5 Docs:** `docs/t5-research/`
- **Skill Registry:** `.claude/SKILL-REGISTRY.md`
- **Squad Config:** `.aiox/squads/t5-*/config.yaml`
- **Commands:** `.claude/.t5-COMMANDS.md`

---

**Versão:** 1.0  
**Data:** 21 Junho 2026  
**Autor:** Atlas (Analyst) - Investigação Completa  
**Status:** 🟢 Pronto para Implementação

