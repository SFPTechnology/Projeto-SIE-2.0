# Gap Absorption Roadmap

**34 practices to absorb from OpenClaw, BMAD, and Paperclip**

**Date:** 2026-04-04
**Source:** Quality Engineering 4-Way Benchmark

---

## Priority Matrix

### Wave 1 — Immediate (P1, <1 day each, 8 items)

| # | Source | Practice | Effort | ROI |
|---|--------|----------|:------:|:---:|
| 1 | BMAD | **Husky pre-commit hooks** | 1h | Catch issues before commit, not push |
| 2 | BMAD | **lint-staged (fix staged only)** | 1h | Auto-fix without touching unstaged files |
| 3 | BMAD | **max-warnings=0 in CI** | 30min | Zero tolerance for warnings |
| 4 | Paperclip | **PR template (Thinking Path)** | 1h | Structured reasoning in every PR |
| 5 | BMAD | **Forbidden tokens check** | 2h | Prevent PII/secrets leaking |
| 6 | Paperclip | **canRepair flag on doctor checks** | 2h | Smarter auto-fix decisions |
| 7 | Paperclip | **Rollback script** | 2h | Safe release reversal |
| 8 | Paperclip | **Definition of Done checklist** | 1h | Clear completion criteria |

**Total effort:** ~10 hours
**Impact:** Pre-commit pipeline + PR process + release safety

---

### Wave 2 — Short-term (P2, 1-3 days each, 11 items)

| # | Source | Practice | Effort | ROI |
|---|--------|----------|:------:|:---:|
| 9 | BMAD | **Prettier + packagejson plugin** | 1h | Consistent formatting |
| 10 | BMAD | **markdownlint-cli2 (6 rules)** | 1h | Markdown quality enforcement |
| 11 | BMAD | **ESLint full config (5 plugins)** | 2h | Deep JS linting |
| 12 | BMAD | **CodeRabbit .coderabbit.yaml** | 30min | Review config with path filters |
| 13 | BMAD | **556-line file ref validator** | 1-2d | Cross-file reference integrity |
| 14 | Paperclip | **Smoke tests post-release** | 1d | Post-release validation |
| 15 | Paperclip | **Activity logging** | 2-3d | Mutation traceability |
| 16 | Paperclip | **Run traceability (Run-Id)** | 1-2d | Per-execution tracing |
| 17 | Paperclip | **Release automation canary+stable** | 2-3d | Automated releases |
| 18 | Paperclip | **SPEC document** | 2-3d | Formal specification |
| 19 | Paperclip | **Greptile code review gate** | 1d | AI review with score requirement |

**Total effort:** ~15-20 days
**Impact:** Formatting + linting + release pipeline + observability

---

### Wave 3 — Medium-term (P2-P3, weeks, 9 items)

| # | Source | Practice | Effort | ROI |
|---|--------|----------|:------:|:---:|
| 20 | Paperclip | **zod schemas for critical configs** | 1-2w | Type-safe validation |
| 21 | OpenClaw | **More E2E tests (target: 10+)** | 1-2w | Integration coverage |
| 22 | OpenClaw | **CalVer + dev channels** | 2-3d | Versioned releases |
| 23 | BMAD | **Adversarial review tests** | 2-3d | Edge-case test cases |
| 24 | Paperclip | **Budget system** | 1w | Cost control |
| 25 | BMAD | **Discord webhook notifications** | 1h | Release notifications |
| 26 | BMAD | **Docs site with build validation** | 1w | Generated docs |
| 27 | BMAD | **Style guide** | 1d | Writing guidelines |
| 28 | OpenClaw | **Boundary docs per subsystem** | 1-2d | Progressive disclosure |

**Total effort:** ~6-8 weeks
**Impact:** Schema depth + testing + documentation + cost control

---

### Wave 4 — Long-term (P3, months, 6 items)

| # | Source | Practice | Effort | Impact |
|---|--------|----------|:------:|:------:|
| 29 | OpenClaw | **70% coverage target** | Volume growth | Quality baseline |
| 30 | OpenClaw | **37+ E2E tests** | Volume growth | Integration confidence |
| 31 | OpenClaw | **Plugin SDK** | Months | Third-party extensibility |
| 32 | BMAD/OC | **i18n documentation** | Months | International reach |
| 33 | Paperclip | **302+ zod schemas full coverage** | Months | Complete type-safe validation |
| 34 | OpenClaw | **3,534+ test files** | Months | Massive test coverage |

**Total effort:** Ongoing
**Impact:** Scale and maturity

---

## Suggested Epic

These 34 gaps could form **Epic 112 — Quality Engineering Absorption** with 4 waves matching the priority matrix above.

**Wave 1:** 8 stories, ~10h — Sprint 1
**Wave 2:** 11 stories, ~15-20d — Sprints 2-3
**Wave 3:** 9 stories, ~6-8w — Sprints 4-7
**Wave 4:** 6 stories, ongoing — Continuous improvement

**Estimated total SP:** ~80-100 SP across 34 stories.

---

## Quick Win ROI: Wave 1 Only

If you implement only Wave 1 (10 hours of work):

| Metric | Before | After Wave 1 |
|--------|:------:|:------------:|
| Pre-commit hooks | 0 | Husky + lint-staged |
| CI warning tolerance | warnings allowed | max-warnings=0 |
| PR process | no template | Thinking Path + DoD |
| Release safety | no rollback | rollback script |
| Secret scanning | none | forbidden tokens check |
| Doctor intelligence | --fix (all or nothing) | canRepair per check |
| **Practices absorbed** | 0/34 | **8/34 (24%)** |

---

*Generated from 4-Way Quality Engineering Benchmark | 2026-04-04*
