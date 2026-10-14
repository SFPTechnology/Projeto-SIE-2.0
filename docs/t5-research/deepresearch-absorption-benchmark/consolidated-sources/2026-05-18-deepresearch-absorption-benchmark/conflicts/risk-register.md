# Risk Register — Deepresearch Absorption

> Top 10 risks identificados, com mitigation + owner.

## Risk Matrix

| ID | Risk | Prob | Impact | Score | Owner |
|---|---|---|---|---:|---|
| RISK-01 | Docker sandbox security CVE | MEDIUM | HIGH | 12 | @aiox-devops + @aiox-architect |
| RISK-10 | Inadvertent copy of Jina proprietary | LOW | VERY HIGH | 12 | @aiox-architect + @aiox-devops |
| RISK-03 | Apache-2.0 NOTICE oversight | LOW | HIGH | 9 | @aiox-devops + @aiox-pm |
| RISK-04 | Competidores absorvem AIOX gaps primeiro | MEDIUM | MEDIUM | 9 | @vision-strategist + @aiox-pm |
| RISK-05 | AGPLv3 community adoption fails | MEDIUM | MEDIUM | 9 | @aiox-pm + @vision-strategist |
| RISK-07 | Memory schema regression | MEDIUM | MEDIUM | 9 | @aiox-dev + @aiox-qa |
| RISK-09 | Capacity insuficiente (1 FT) | MEDIUM | MEDIUM | 9 | @vision-strategist + @aiox-pm |
| RISK-08 | Bench re-score below target | LOW | HIGH | 6 | @aiox-qa + @aiox-architect |
| RISK-02 | MCP spec evolution | LOW | MEDIUM | 4 | @aiox-architect |
| RISK-06 | HF model availability | LOW | LOW | 2 | @aiox-architect |

## Detailed Risks

### 🔴 RISK-01 — Docker Sandbox Security CVE

**Probability:** MEDIUM (Docker stack histórico tem vulnerabilities ocasionais)
**Impact:** HIGH (security incident = customer trust loss)

**Mitigation:**
- Quarterly security audit
- Minimal base image (ubuntu:22.04 stripped)
- Network policy egress deny + allowlist domains
- Read-only base filesystem
- Resource limits (CPU/memory/timeout)
- Auto-update CVE scanner em CI (e.g. Trivy)

**Trigger:** New CVE in Docker stack → immediate patch + customer notification

### 🔴 RISK-10 — Inadvertent Copy of Jina Proprietary Code

**Probability:** LOW (if devs trained)
**Impact:** VERY HIGH (license violation + legal exposure)

**Mitigation:**
- Explicit NO-GO list em `deep/license-risk-assessment.md`
- Code review check: "Did this PR touch Jina patterns?"
- Dev training: clean-room implementation for any Jina inspiration
- Git hooks: pre-commit checks if `../bench/node-DeepResearch/` referenced

**Trigger:** Jina legal team notice → immediate remove + redo from scratch

### 🟠 RISK-03 — Apache-2.0 NOTICE Compliance

**Probability:** LOW (com CI guard)
**Impact:** HIGH (license violation)

**Mitigation:**
- NOTICE.txt template em packages/@sinkra/*
- CI guard `validate:license-headers`
- Legal review pre-major-release
- Document attribution clearly em README

### 🟠 RISK-04 — Competidores Absorvem AIOX Gaps Primeiro

**Probability:** MEDIUM (DeerFlow já tem memory; Tongyi pode adicionar governance)
**Impact:** MEDIUM (perda de differentiator)

**Mitigation:**
- Wave 1 rápido (8 weeks)
- Governance + PT-BR vertical são moats **arquiteturais** difíceis de copiar
- Continue innovating (Wave 2-3 mantém ritmo)

**Trigger:** DeerFlow 3.0 lança com governance gates → re-strategize

### 🟠 RISK-05 — AGPLv3 Community Adoption Fails

**Probability:** MEDIUM (community não é automático)
**Impact:** MEDIUM (sem community contribution dilui posicionamento OSS)

**Mitigation:**
- Marketing investment: Discord + Twitter + blog posts
- Identify 5-10 early advocates antes do launch
- Feature parity demo entre Elastic v2 e AGPLv3 CE
- Document contribution guide

**Trigger:** 6 weeks pós-launch sem PR community → reassess + double marketing

### 🟠 RISK-07 — Memory Schema Regression

**Probability:** MEDIUM
**Impact:** MEDIUM (memory loss = quality regression)

**Mitigation:**
- Versioned schema YAML
- Migration scripts
- Tests em CI (forward + backward migration)
- Rollback procedure documentado
- Backup pre-migration automated

### 🟠 RISK-09 — Capacity Insuficiente

**Probability:** MEDIUM (1 dev FT é apertado)
**Impact:** MEDIUM (timeline slip)

**Mitigation:**
- Allocate 2 dev FT OR
- Extend timeline (20 → 26 weeks) OR
- De-scope Wave 3 (manter v5.5.0 → v6.0.0 next quarter)

**Decision needed:** Antes de Sprint 1, @vision-strategist confirma capacity.

### 🟡 RISK-08 — Bench Re-score Below Target

**Probability:** LOW (80% confidence em target)
**Impact:** HIGH (compromete narrativa marketing)

**Mitigation:**
- Bench checkpoint per-wave (re-score após Wave 1, 2, 3)
- Redo gaps if missed
- Adjustable scope (de-scope or re-prioritize)

**Trigger:** Wave 1 checkpoint Week 8 score < 70 → re-strategize

### 🟢 RISK-02 — MCP Spec Evolution

**Probability:** LOW (spec é stable em 2026)
**Impact:** MEDIUM

**Mitigation:**
- Pin to MCP spec v1
- Auto-test against latest quarterly
- Version negotiation em capabilities exchange

### 🟢 RISK-06 — HF Model Availability

**Probability:** LOW (Apache-2.0 garante persistence)
**Impact:** LOW (BYOK fallback always functional)

**Mitigation:**
- Apache-2.0 license garante community can re-host
- Fallback BYOK always works
- Monitor HF status

## Overall Risk Assessment

**MEDIUM.** Mitigations disponíveis para todos os top risks.

- 0 risks com prob HIGH × impact HIGH (sem critical unmitigated)
- 2 risks com score 12 (RISK-01 + RISK-10) com mitigations sólidas
- 7 risks score 4-9 com mitigations
- 1 risk score 2 (baixo)

## Risk Review Cadence

- **Per-sprint:** Owner reviews owned risks
- **Per-wave checkpoint:** All risks reviewed + status updated
- **Per-major-release:** External review (e.g. roundtable) reviews top 3

## Risk Aceitos

Riscos não mitigados (aceitos como parte do trade-off):

1. **Bench score 88 é estimativa.** Reality pode ser 80-90. Aceito como uncertainty.
2. **20 weeks timeline.** Risk de slippage 20-30%. Aceito como project nature.
3. **Apache-2.0 NOTICE burden ongoing.** Aceito como cost-of-doing-business.
