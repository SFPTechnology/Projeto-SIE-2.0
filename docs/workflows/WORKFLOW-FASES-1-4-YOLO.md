# Workflow Automático YOLO — Fases 1-4 Projeto SIE

**Status:** ⚠️ DRAFT — Configuração em modo YOLO (sem intervenção humana)  
**Data de Criação:** 2026-07-09  
**Orquestrador:** Atlas (Analyst) — Documentação de Processo  
**Execução:** Automática via agentes AIOX  

---

## 📋 Visão Geral do Workflow

Este workflow executa **4 fases sequenciais** com **4 agentes especializados** em modo YOLO (autonomia total, sem paradas para confirmação):

| Fase | Agent | Tarefa | Entrada | Saída | Status |
|------|-------|--------|---------|-------|--------|
| **1** | @sm (River) | Formalizar stories 1.1–1.4 | Epic context | `docs/stories/1.1.story.md` — `1.4.story.md` | Pending |
| **2** | @dev (Dex) | Implementar motor layout/canvas navegável | Stories formalizadas | Código funcional em branches | Pending |
| **3** | @dev (Dex) | Implementar memorial em abas com diff | Fases 1-2 | Código funcional em branches | Pending |
| **4** | @dev (Dex) | Implementar exportação Python | Fases 1-3 | Código funcional em branches | Pending |
| **QA** | @qa (Quinn) | Validação integrada (fases 1-4) | Todos os PRs @dev | PASS/FAIL/CONCERNS | Pending |
| **Review Iterativo** | @dev ↔️ @qa | Ciclo de correção (máx 5 iterações) | Feedback @qa | Código validado | Pending |
| **Deploy** | @devops (Gage) | Push & teste local em `http://localhost:5173/` | Código validado | Servidor rodando | Pending |

---

## 🔄 Fluxo de Execução Detalhado

### FASE 1: Formalização de Stories (@sm)
**Agent:** @sm (River — Scrum Master)  
**Modo:** YOLO (autonomia total)  
**Tempo estimado:** 15-20 min

#### Entrada
- Epic context de docs/prd/ (if exists)
- Descrição das 4 fases do projeto (layout, memorial, exportação)

#### Execução
```bash
@sm *create-story --epic=1 --story-range=1.1-1.4 --mode=yolo
```

**Checklist Interno @sm:**
- [ ] Ler PRD/Epic context
- [ ] Criar `1.1.story.md` — Motor de layout/canvas navegável
- [ ] Criar `1.2.story.md` — Memorial em abas (estrutura)
- [ ] Criar `1.3.story.md` — Memorial com diff visual
- [ ] Criar `1.4.story.md` — Exportação Python
- [ ] Validar ACs (Acceptance Criteria) de cada story
- [ ] Marcar como Status: Draft

#### Saída
- `docs/stories/1.1.story.md`
- `docs/stories/1.2.story.md`
- `docs/stories/1.3.story.md`
- `docs/stories/1.4.story.md`

#### Critério de Aprovação
✅ **GO para Fase 2 IF:**
- Todas as 4 stories existem em docs/stories/
- Cada story tem ACs claras e testáveis
- Não há conflitos de escopo entre stories

❌ **HALT IF:**
- Stories faltam (workflow não prossegue, escala para @aiox-master)

---

### FASE 2-4: Implementação Paralela (@dev)
**Agent:** @dev (Dex — Developer)  
**Modo:** YOLO (autonomia total)  
**Tempo estimado:** 4-6 horas (depende de complexidade)

#### Entrada
- Stories 1.1–1.4 formalizadas em docs/stories/
- Acesso ao branch de desenvolvimento

#### Execução
```bash
@dev *develop-story --story=1.1 --mode=yolo
@dev *develop-story --story=1.2 --mode=yolo
@dev *develop-story --story=1.3 --mode=yolo
@dev *develop-story --story=1.4 --mode=yolo
```

**Sequência @dev (obrigatória):**
1. **Story 1.1 (Motor Layout/Canvas)**
   - [ ] Implementar componente Canvas navegável
   - [ ] Implementar zoom/pan/zoom-fit
   - [ ] Testes unitários
   - [ ] Teste manual em localhost:5173
   - [ ] Commit e PR (`story/1.1-motor-layout`)

2. **Story 1.2 (Memorial — Estrutura de Abas)**
   - [ ] Criar componente Memorial com UI de abas
   - [ ] Estrutura de dados para memorial
   - [ ] Testes unitários
   - [ ] Commit e PR (`story/1.2-memorial-abas`)

3. **Story 1.3 (Memorial — Diff Visual)**
   - [ ] Implementar diff viewer (ex: react-diff-viewer)
   - [ ] Integrar com memorial
   - [ ] Testes unitários + teste visual
   - [ ] Commit e PR (`story/1.3-memorial-diff`)

4. **Story 1.4 (Exportação Python)**
   - [ ] Implementar serialização para Python
   - [ ] Testes com dados reais
   - [ ] Commit e PR (`story/1.4-exportacao-python`)

#### Saída
- 4 branches de feature: `story/1.1-*`, `story/1.2-*`, `story/1.3-*`, `story/1.4-*`
- 4 PRs abertos no GitHub (não mergeados ainda)
- Código com testes passing: `npm test`
- Linting passing: `npm run lint`
- TypeChecking passing: `npm run typecheck`

#### Critério de Aprovação
✅ **GO para QA IF:**
- Todos os 4 PRs estão abertos e linkados às stories
- `npm test` passa em todas as branches
- `npm run lint` sem erros
- `npm run typecheck` sem erros

❌ **HALT SE:**
- Testes falhando (workflow não prossegue)
- TypeScript errors críticos
- Conflitos de merge com main

---

### FASE QA: Validação Integrada (@qa)
**Agent:** @qa (Quinn — QA/Tester)  
**Modo:** YOLO (autonomia total)  
**Tempo estimado:** 30-60 min (primeira pass)

#### Entrada
- 4 PRs abertos (@dev) com código e testes
- Stories 1.1–1.4 em docs/stories/

#### Execução
```bash
@qa *qa-gate --story-range=1.1-1.4 --mode=yolo
```

**QA Checklist (7 pontos — PASS/CONCERNS/FAIL):**

1. **Cobertura de AC (Acceptance Criteria)**
   - Cada story implementa 100% dos ACs?
   - Testes cobrem casos de sucesso + edge cases?

2. **Testes Unitários**
   - Cobertura >= 80%?
   - Todos os testes passando?

3. **Testes de Integração**
   - Fases 1.1–1.4 integram corretamente?
   - Sem efeitos colaterais entre componentes?

4. **Teste Manual (UI/UX)**
   - Canvas navegável funciona em localhost:5173?
   - Memorial em abas renderiza corretamente?
   - Diff visual é legível e funcional?
   - Exportação Python gera código válido?

5. **Performance**
   - Canvas responde em <500ms para interações?
   - Diff rendering é fluido (60 fps)?
   - Exportação completa em <5s?

6. **Code Quality**
   - Sem console.error ou warnings não documentados?
   - Código segue padrões do projeto?
   - Sem vulnerabilidades (npm audit)?

7. **Regressão**
   - Features existentes funcionam?
   - Sem quebra em outros módulos?

#### Saída (PASS)
- Relatório: `qa/report-1.1-1.4-{date}.md`
- Status das stories: todas marcadas como "InReview"
- Feedback: "APPROVED — Ready for merge"

#### Saída (CONCERNS/FAIL)
- Relatório detalhado de issues
- Especificação exata do que @dev deve corrigir
- Re-enviar para @dev com feedback

#### Critério de Aprovação
✅ **GO para Merge (@devops) IF:**
- Todos os 7 pontos: ✅ PASS

⚠️ **LOOP ITERATIVO IF:**
- 1-3 pontos com CONCERNS
- Ação: Feedback detalhado → @dev *fix-and-retest
- Max 5 iterações

❌ **ESCALATE IF:**
- >=4 pontos com FAIL
- Ação: Escalar para @aiox-master

---

### FASE ITERATIVA: Correção de Issues (@dev ↔️ @qa)
**Loop:** Máximo 5 iterações  
**Modo:** YOLO  
**Tempo estimado:** 30-120 min (depende de issues)

#### Fluxo
```
@qa reports CONCERNS
  ↓
@dev fixes issues (git commit --amend or new commit)
  ↓
@dev pushes to existing PR branches
  ↓
@qa re-tests (story 1.1-1.4)
  ↓
IF all 7 checklist points ✅ PASS:
  → GO para @devops (*merge)
ELSE IF still CONCERNS and iteration < 5:
  → Loop back to @dev fixes
ELSE:
  → ESCALATE to @aiox-master
```

---

### FASE DEPLOY: Merge & Teste Local (@devops)
**Agent:** @devops (Gage — DevOps)  
**Modo:** YOLO (autonomia total)  
**Tempo estimado:** 10-15 min

#### Entrada
- 4 PRs validadas por @qa (PASS)
- Código ready for production

#### Execução
```bash
@devops *merge --pr=1.1,1.2,1.3,1.4 --mode=yolo
@devops *deploy-local --port=5173 --mode=yolo
```

**@devops Checklist:**
1. [ ] Verify all 4 PRs have "APPROVED" label from @qa
2. [ ] Run GitHub checks (CI/CD pipeline)
3. [ ] Squash merge 1.1 → main
4. [ ] Squash merge 1.2 → main
5. [ ] Squash merge 1.3 → main
6. [ ] Squash merge 1.4 → main
7. [ ] Pull latest main locally
8. [ ] Run `npm install` (if needed)
9. [ ] Run `npm run build`
10. [ ] Start dev server: `npm run dev` (default port 5173)
11. [ ] Test in browser: `http://localhost:5173/`
12. [ ] Manual smoke test (canvas, memorial, export)
13. [ ] Verify no console errors
14. [ ] Report results: `devops/deploy-local-report-{date}.md`

#### Saída (SUCCESS)
- ✅ Main branch contém commits de todas as 4 fases
- ✅ Dev server rodando em `http://localhost:5173/`
- ✅ Smoke test passed
- ✅ Relatório: `devops/deploy-local-report-{date}.md`

#### Saída (FAILURE)
- ❌ Erro durante merge ou build
- ❌ Ação: Escalar para @dev para correção
- ❌ Re-trigger workflow

#### Critério de Sucesso Final
✅ **WORKFLOW COMPLETE IF:**
- Todos os 4 commits em main
- Dev server rodando em localhost:5173
- Features 1.1–1.4 funcionais e testadas
- Zero console errors

---

## 📊 Dependências & Pré-requisitos

| Recurso | Status | Notas |
|---------|--------|-------|
| PRD/Epic docs | ✅ Required | Deve existir docs/prd/ ou epic context |
| Branch main | ✅ Required | Main deve estar clean (sem changes uncommitted) |
| npm/node | ✅ Required | npm test, lint, typecheck devem funcionar |
| GitHub CLI (gh) | ✅ Required | Para @devops fazer merge |
| Porta 5173 disponível | ✅ Required | Para dev server local |
| Access to docs/stories/ | ✅ Required | Para @sm criar stories |

---

## 🚨 Escalation Triggers

| Condição | Ação | Agente |
|----------|------|--------|
| @sm não consegue formalizar stories | Escalar para @po (validar ACs) | @aiox-master |
| @dev encontra conflito de escopo | Escalar para @architect (design review) | @aiox-master |
| @qa encontra >=4 pontos FAIL | Escalar com relatório detalhado | @aiox-master |
| @devops merge falha (CI/CD error) | Escallar para DevOps manual review | @aiox-master |
| Qualquer loop iterativo atinge 5 iterações | Parar e escalar | @aiox-master |

---

## ⏱️ Estimativa de Tempo Total

| Fase | Agent | Tempo | Notas |
|------|-------|-------|-------|
| 1 — Stories | @sm | 15-20 min | Rápido, apenas formalização |
| 2-4 — Code | @dev | 4-6 h | Complexo, múltiplas features |
| QA | @qa | 30-60 min | Primeiro pass (pode haver iterações) |
| Iterações | @dev ↔️ @qa | 30-120 min | Depende de issues encontradas |
| Deploy | @devops | 10-15 min | Merge + teste local |
| **TOTAL** | — | **5-8 horas** | SLA: finalizar no mesmo dia |

---

## 🔗 Configuração YOLO (Modo Automático)

Para ativar modo YOLO em todos os agentes, execute:

```bash
@sm *yolo
@dev *yolo
@qa *yolo
@devops *yolo
```

**Modo YOLO significa:**
- ✅ Nenhuma pausa para confirmação do usuário
- ✅ Decisões automáticas dentro de limites configurados
- ✅ Logs completos em cada step
- ✅ Escalation automática se threshold atingido

**Alternativa:** Incluir `--mode=yolo` em cada comando:

```bash
@sm *create-story --epic=1 --story-range=1.1-1.4 --mode=yolo
@dev *develop-story --story=1.1 --mode=yolo
@qa *qa-gate --story-range=1.1-1.4 --mode=yolo
@devops *merge --pr=1.1,1.2,1.3,1.4 --mode=yolo
```

---

## 📝 Arquivos de Log & Status

Durante execução, o workflow gera:

```
.aiox/logs/
├── workflow-phases-1-4-{timestamp}.log
├── sm-stories-{timestamp}.log
├── dev-implementation-{timestamp}.log
├── qa-gate-{timestamp}.log
└── devops-deploy-{timestamp}.log

docs/stories/
├── 1.1.story.md          (Draft → InReview → Done)
├── 1.2.story.md
├── 1.3.story.md
├── 1.4.story.md
└── WORKFLOW-STATUS.md    (tracking em tempo real)
```

**Status real-time:**
```bash
@aiox-master *status workflow-phases-1-4
```

---

## ✅ Checklist Final (Pré-execução)

Antes de iniciar o workflow, confirme:

- [ ] Repositório clean (nenhum change uncommitted em main)
- [ ] PRD/Epic context disponível
- [ ] Branch `develop` ou feature branch existe e está atualizado
- [ ] `npm install` foi executado (dependências instaladas)
- [ ] GitHub CLI autenticado (`gh auth status`)
- [ ] Porta 5173 está disponível (nenhum outro processo usando)
- [ ] Todos os agentes estão no modo YOLO OU flags --mode=yolo serão usadas
- [ ] Logs podem ser escritos em `.aiox/logs/`

---

## 🎯 Execução Final (One-Liner)

Para iniciar o workflow completo de forma automática:

```bash
@sm *create-story --epic=1 --story-range=1.1-1.4 --mode=yolo && \
@dev *develop-story --story-range=1.1-1.4 --mode=yolo && \
@qa *qa-gate --story-range=1.1-1.4 --mode=yolo && \
@devops *merge --pr-auto=true --deploy-local --port=5173 --mode=yolo
```

Ou, usando orquestrador master:

```bash
@aiox-master *execute-workflow --name=phases-1-4 --mode=yolo
```

---

## 📞 Suporte & Debug

| Problema | Comando Debug | Agent |
|----------|---------------|-------|
| Ver status em tempo real | `@aiox-master *status workflow-phases-1-4` | @aiox-master |
| Ver logs completos | `tail -f .aiox/logs/workflow-phases-1-4-*.log` | Any |
| Pausar workflow | `@aiox-master *pause workflow-phases-1-4` | @aiox-master |
| Resumir de checkpoint | `@aiox-master *resume workflow-phases-1-4 --from=qa` | @aiox-master |
| Rollback último merge | `@devops *rollback --commits=last-4` | @devops only |

---

**Documento criado por:** Atlas (Analyst)  
**Data:** 2026-07-09  
**Versão:** 1.0  
**Status:** 🟡 DRAFT — Aguardando feedback e ajustes
