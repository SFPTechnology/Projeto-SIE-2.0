# Quality Engineering 4-Way Benchmark

**Sinkra Hub vs OpenClaw vs BMAD-METHOD vs Paperclip**

**Date:** 2026-04-04
**Analyst:** bench-analyst@spy
**Data Source:** Local clone analysis (High Confidence)
**Methodology:** Exhaustive inventory of every quality engineering, governance, and DevOps practice in each repo

---

## 1. Project Identity

| | **Sinkra Hub** | **OpenClaw** | **BMAD-METHOD** | **Paperclip** |
|--|:-:|:-:|:-:|:-:|
| **Purpose** | AI Orchestration Framework | Personal AI Assistant | AI Dev Methodology | AI Agent Control Plane |
| **Primary Language** | TS + Python + Shell + YAML | TypeScript | JavaScript | TypeScript |
| **Code LOC** | 556K | 1.84M | 19K | 221K |
| **Knowledge LOC** | 8.6M (YAML+MD) | 205K | 52K MD | — |
| **Total Files** | 32,357 | 12,150 | ~474 | 978 |
| **Contributors** | 4 | 1,584 | ~20 | ~10 |
| **License** | Private | MIT | MIT | Private |
| **Skills** | 57 | 53 | 41 | 11 |
| **Agents** | 473 | ~5 | 3 | 7 adapters |
| **Test Files** | 13 | 3,534 | 5 | 190+ |
| **Squads** | 53 | 0 | 0 | 0 |

---

## 2. Quality Engineering — Complete Practice-by-Practice Comparison

### 2.1 Code Quality & Formatting

| Practice | Sinkra Hub | OpenClaw | BMAD | Paperclip |
|----------|:-:|:-:|:-:|:-:|
| **Linter** | ✅ Oxlint (doctor) | ✅ Oxlint | ✅ ESLint (5 plugins) | ❌ None |
| **Formatter** | ❌ | ✅ Oxfmt | ✅ Prettier + packagejson plugin | ❌ |
| **Markdown linter** | ❌ | ❌ | ✅ markdownlint-cli2 (6 rules) | ❌ |
| **TypeScript strict** | ⚠️ Partial | ✅ No `any` | ❌ Pure JS | ✅ Strict true |
| **max-warnings=0** | ❌ | ❌ | ✅ Zero tolerance | ❌ |
| **YAML linting** | ✅ js-yaml syntax | ❌ | ✅ eslint-plugin-yml | ❌ |
| **Forbidden tokens** | ❌ | ❌ | ✅ check-forbidden-tokens | ❌ |
| **Style guide** | ❌ | ❌ | ✅ _STYLE_GUIDE.md | ❌ |

### 2.2 Testing

| Practice | Sinkra Hub | OpenClaw | BMAD | Paperclip |
|----------|:-:|:-:|:-:|:-:|
| **Test framework** | Shell (custom) | Vitest | Node assertions (custom) | Vitest |
| **Test files** | 13 | **3,534** | 5 | 190+ |
| **E2E framework** | Shell (1 test) | Vitest E2E (**37**) | ❌ | Playwright (**2**) |
| **Coverage tool** | bash xtrace | V8 (Vitest) | c8 (not configured) | ❌ |
| **Coverage threshold** | 14.1% + CI floor | **70% enforced** | ❌ | ❌ |
| **Coverage regression gate** | ✅ baseline - 5pts | ✅ | ❌ | ❌ |
| **Test perf guardrails** | ✅ 5 rules | ✅ 5 rules | ❌ | ❌ |
| **Adversarial tests** | ❌ | ❌ | ✅ test-cases.yaml | ❌ |
| **Smoke tests** | ❌ | ❌ | ❌ | ✅ 4 scripts |

### 2.3 Schema & Validation

| Practice | Sinkra Hub | OpenClaw | BMAD | Paperclip |
|----------|:-:|:-:|:-:|:-:|
| **Schema framework** | Custom (9 fields) | zod | Custom (14 rules) | **zod (302+ schemas)** |
| **Schema LOC** | ~200 | ~2,000 | 736 | **2,487** |
| **Typed inference** | ❌ | ✅ zod infer | ❌ | ✅ zod infer |
| **Skill validation** | ✅ validate:skill | ❌ | ✅ **14 rules** (CRITICAL/HIGH/MEDIUM) | ❌ |
| **File ref validation** | ❌ | ❌ | ✅ **556-line validator** (strict mode) | ❌ |
| **Config schema** | ✅ 9-field squad schema | ✅ zod | ❌ | ✅ zod config schema |
| **AJV integration** | ❌ | ❌ | ❌ | ✅ ajv + ajv-formats |

### 2.4 CI/CD & Automation

| Practice | Sinkra Hub | OpenClaw | BMAD | Paperclip |
|----------|:-:|:-:|:-:|:-:|
| **CI workflows** | 5 | **13** | 5 | 6 |
| **Quality gate CI job** | ✅ ci-gate | ✅ ci | ✅ quality.yaml (5 parallel jobs) | ✅ pr.yml |
| **Release automation** | ❌ manual | ✅ CalVer + channels | ✅ npm publish + Discord | ✅ YYYY.DDD.N + canary |
| **Canary releases** | ❌ | ✅ | ❌ | ✅ auto on master |
| **Rollback script** | ❌ | ❌ | ❌ | ✅ rollback-latest.sh |
| **Versioning scheme** | Manual | CalVer (vYYYY.M.D) | Semver | YYYY.DDD.N |
| **Dev channels** | ❌ | ✅ stable/beta/dev | ❌ | ✅ canary/stable |
| **Discord notifications** | ❌ | ❌ | ✅ webhook | ❌ |
| **Docs build validation** | ❌ | ✅ | ✅ Astro build + link check | ❌ |
| **Doc link validation** | ❌ | ✅ check-links | ✅ validate-doc-links | ❌ |

### 2.5 Git Hooks & Pre-commit

| Practice | Sinkra Hub | OpenClaw | BMAD | Paperclip |
|----------|:-:|:-:|:-:|:-:|
| **Hook framework** | Custom shell hooks | prek | **Husky** | ❌ CI-only |
| **Pre-commit** | ❌ (pre-push + PreToolUse) | ✅ prek | ✅ **Husky + lint-staged** | ❌ |
| **Pre-push** | ✅ **6 checks** | ❌ | ❌ | ❌ |
| **PreToolUse hooks** | ✅ **3 hooks** (Bash matcher) | ❌ | ❌ | ❌ |
| **lint-staged (fix staged only)** | ❌ | ❌ | ✅ eslint+prettier per filetype | ❌ |
| **Full test suite in hook** | ❌ | ❌ | ✅ npm test in pre-commit | ❌ |
| **Docs validation in hook** | ❌ | ❌ | ✅ if docs/ changed | ❌ |

### 2.6 Config & Drift Detection

| Practice | Sinkra Hub | OpenClaw | BMAD | Paperclip |
|----------|:-:|:-:|:-:|:-:|
| **Drift detection method** | SHA-256 hashes | SHA-256 hashes | Manifest versioning | State-based checks |
| **Tracked configs** | 7 governance files | Config schema + Plugin SDK | Installation manifest | 9 runtime checks |
| **Auto-regenerate** | ✅ config:drift:gen | ✅ gen commands | ✅ manifest update | ✅ --repair |
| **Manifest system** | ❌ | ❌ | ✅ YAML manifest + CSV tracker | ❌ |
| **Version tracking** | ❌ | ✅ CalVer | ✅ module versions + timestamps | ✅ YYYY.DDD.N |

### 2.7 Doctor & Health

| Practice | Sinkra Hub | OpenClaw | BMAD | Paperclip |
|----------|:-:|:-:|:-:|:-:|
| **Doctor command** | ✅ `npm run doctor` | ✅ `openclaw doctor` | ⚠️ `bmad status` | ✅ `paperclip doctor` |
| **Check count** | **10** | ~5 | 3 | **9** |
| **Auto-fix mode** | ✅ `--fix` | ✅ `--fix` | ❌ | ✅ **`--repair` + canRepair flag** |
| **Health endpoint** | ❌ (CLI-first) | ❌ | ❌ | ✅ `/api/health` |
| **Fix suggestions** | ✅ per-check hints | ✅ | ❌ | ✅ repair hints |
| **Infra health checks** | ❌ | ❌ | ❌ | ✅ DB, storage, LLM, port, secrets |

### 2.8 Code Review & PR Process

| Practice | Sinkra Hub | OpenClaw | BMAD | Paperclip |
|----------|:-:|:-:|:-:|:-:|
| **AI code review** | ✅ CodeRabbit | ❌ | ✅ CodeRabbit + config | ✅ Greptile (5/5 score) |
| **Review config file** | ❌ | ❌ | ✅ .coderabbit.yaml (path filters) | ❌ (Greptile auto) |
| **PR template** | ❌ | ❌ | ❌ | ✅ **Thinking Path + Risks + Model Used** |
| **Score gate** | ❌ | ❌ | ❌ | ✅ **5/5 Greptile required** |
| **Definition of Done** | ⚠️ ACs in stories | ❌ | ❌ | ✅ Checklist in AGENTS.md |

### 2.9 Documentation

| Practice | Sinkra Hub | OpenClaw | BMAD | Paperclip |
|----------|:-:|:-:|:-:|:-:|
| **Docs site** | ❌ | ✅ Mintlify | ✅ **Astro** | ❌ |
| **SPEC document** | ❌ | ✅ VISION.md | ❌ | ✅ **SPEC.md + SPEC-impl.md (1,405 LOC)** |
| **i18n docs** | ❌ | ✅ zh-CN + ja-JP | ✅ **FR + ZH + VI** | ❌ |
| **Boundary docs** | ✅ 1 CLAUDE.md | ✅ **11 AGENTS.md** | ✅ 1 AGENTS.md | ✅ 1 AGENTS.md |
| **Architecture docs** | ✅ 8-layer model | ✅ plugin boundaries | ❌ | ✅ subsystem docs (56 files) |

### 2.10 Observability & Tracing

| Practice | Sinkra Hub | OpenClaw | BMAD | Paperclip |
|----------|:-:|:-:|:-:|:-:|
| **Activity logging** | ❌ | ❌ | ❌ | ✅ **Mutation logging (actor, action, impact)** |
| **Run traceability** | ❌ | ❌ | ❌ | ✅ **X-Paperclip-Run-Id headers** |
| **Budget tracking** | ❌ | ❌ | ❌ | ✅ **Cost per agent/run** |
| **Metrics** | ✅ SYNAPSE engine-usage.jsonl | ❌ | ❌ | ✅ cost metrics |
| **Feedback collection** | ❌ | ❌ | ❌ | ✅ **Feedback system** |

---

## 3. Governance — Complete Comparison

| Practice | Sinkra Hub | OpenClaw | BMAD | Paperclip |
|----------|:-:|:-:|:-:|:-:|
| **Constitution** | ✅ **322 lines, 11 articles** | ❌ | ❌ | ❌ |
| **Constitutional hooks** | ✅ **3/6 articles automated** | ❌ | ❌ | ❌ |
| **Agent authority matrix** | ✅ **Exclusive ops per agent** | ❌ | ❌ | ❌ |
| **TTL governance** | ✅ **384 files, 5 layers** | ❌ | ❌ | ❌ |
| **Artifact classification** | ✅ **3-rule validator** | ❌ | ❌ | ❌ |
| **Cross-boundary enforcement** | ✅ Squad boundaries | ✅ Import boundaries | ❌ | ❌ |
| **CODEOWNERS** | ✅ **CI + local + shared engine** | ✅ Security CODEOWNERS | ❌ | ❌ |
| **Story-driven enforcement** | ✅ **Commit hook WARN** | ❌ | ❌ | ❌ |
| **Multi-business isolation** | ✅ **4 businesses L0-L4** | ❌ | ❌ | ✅ Company scoping |
| **Skill drift detection** | ✅ **MD5 hash** | ❌ | ✅ File ref validator | ❌ |
| **Agent-not-found handling** | ✅ **Levenshtein fuzzy** | ❌ | ❌ | ❌ |
| **SYNAPSE context engine** | ✅ **8 layers** | ❌ | ❌ | ❌ |
| **KPI baselines** | ✅ **3 processos medidos** | ❌ | ❌ | ❌ |
| **Document Registry** | ✅ **Lifecycle management** | ❌ | ✅ Manifest YAML | ❌ |
| **SINKRA compositional model** | ✅ **Token→Instance hierarchy** | ❌ | ❌ | ❌ |

---

## 4. Everything They Have That We Don't (34 Actionable Gaps)

### 4.1 From OpenClaw (8 actionable gaps)

| # | Practice | What It Does | Priority | Effort |
|---|----------|-------------|:--------:|:------:|
| OC-1 | **Formatter enforced (Oxfmt)** | Consistent code style, auto-fix on save/commit | P2 | 2h |
| OC-2 | **70% coverage enforced** | CI blocks if coverage drops below threshold | P1 | Volume growth |
| OC-3 | **37 E2E tests** | Comprehensive end-to-end validation | P2 | Weeks |
| OC-4 | **3,534 test files** | Massive unit test coverage | P2 | Months |
| OC-5 | **CalVer + dev channels** | Versioned releases with stable/beta/dev | P2 | 2-3d |
| OC-6 | **11 AGENTS.md boundary docs** | Progressive disclosure per subsystem | P3 | 1-2d |
| OC-7 | **i18n docs (zh-CN, ja-JP)** | Translated documentation | P3 | Weeks |
| OC-8 | **Plugin SDK (50+ exports)** | Typed contracts for third-party extensions | P3 | Months |

### 4.2 From BMAD (14 actionable gaps)

| # | Practice | What It Does | Priority | Effort |
|---|----------|-------------|:--------:|:------:|
| BM-1 | **Husky pre-commit hooks** | Run checks before EVERY commit (not just push) | P1 | 1h |
| BM-2 | **lint-staged (fix staged only)** | Auto-fix only changed files, fast | P1 | 1h |
| BM-3 | **ESLint full config (5 plugins)** | JS + Node + unicorn + YAML + prettier conflict resolution | P2 | 2h |
| BM-4 | **Prettier + packagejson plugin** | Consistent formatting + sorted package.json | P2 | 1h |
| BM-5 | **markdownlint-cli2 (6 rules)** | Markdown quality enforcement | P2 | 1h |
| BM-6 | **max-warnings=0** | Zero tolerance for warnings in CI | P1 | 30min |
| BM-7 | **CodeRabbit .coderabbit.yaml** | Dedicated review config with path filters | P2 | 30min |
| BM-8 | **Adversarial review tests** | Test cases for edge-case content review | P3 | 2-3d |
| BM-9 | **736-line skill validator** | 14 rules with severity levels | P2 | Existing partial |
| BM-10 | **556-line file ref validator** | Cross-file reference validation with strict mode | P1 | 1-2d |
| BM-11 | **Style guide document** | Formal writing/formatting guidelines | P3 | 1d |
| BM-12 | **Forbidden tokens check** | Scan for PII/secrets before publish | P1 | 2h |
| BM-13 | **Astro docs site** | Generated docs with build validation in CI | P3 | 1w |
| BM-14 | **Discord webhook notifications** | Auto-notify on releases | P3 | 1h |

### 4.3 From Paperclip (12 actionable gaps)

| # | Practice | What It Does | Priority | Effort |
|---|----------|-------------|:--------:|:------:|
| PC-1 | **302+ zod schemas** | Type-safe validation for all domain entities | P2 | Weeks |
| PC-2 | **canRepair flag on doctor checks** | Each check declares if auto-fixable | P1 | 2h |
| PC-3 | **Greptile code review (5/5 score)** | AI review with minimum score gate | P2 | 1d |
| PC-4 | **PR template (Thinking Path)** | Structured PR description with reasoning trace | P1 | 1h |
| PC-5 | **Activity logging (mutations)** | Every mutation logged with actor/action/impact | P2 | 2-3d |
| PC-6 | **Run traceability (Run-Id)** | Every execution traceable by unique ID | P2 | 1-2d |
| PC-7 | **Budget system** | Cost control per agent/run | P3 | 1w |
| PC-8 | **Rollback script** | Revert releases safely | P1 | 2h |
| PC-9 | **Smoke tests (4 scripts)** | Post-release validation | P1 | 1d |
| PC-10 | **SPEC.md + SPEC-implementation.md** | Formal spec (1,405 LOC) from goal to contract | P2 | 2-3d |
| PC-11 | **Definition of Done checklist** | Formal DoD in AGENTS.md | P2 | 1h |
| PC-12 | **Release automation (canary + stable)** | Auto canary on master, manual stable dispatch | P2 | 2-3d |

---

## 5. Exclusive Practices (What Each Has That Nobody Else Does)

### Sinkra Hub: 16 Exclusive Practices

| # | Practice | Detail |
|---|----------|--------|
| 1 | Constitution (322 lines, 11 articles) | No other project has a formal constitution |
| 2 | Constitutional hooks (3/6 automated) | Enforcement of constitutional articles via git hooks |
| 3 | Agent authority matrix | Exclusive operations per agent (@devops→push, @pm→epics) |
| 4 | TTL governance (5 layers, 384 files) | Document staleness enforcement by workspace layer |
| 5 | Artifact classification (3-rule validator) | Decision tree: workspace/ vs outputs/ vs .aiox-core/ |
| 6 | Story-driven commit enforcement | Hook detects commits without story reference |
| 7 | SYNAPSE 8-layer context engine | Multi-layer context injection pipeline |
| 8 | 473 agents across 53 squads | Largest agent ecosystem of any project analyzed |
| 9 | Cross-squad boundary enforcement | Validates squad isolation (150 violations detected) |
| 10 | Agent-not-found Levenshtein fuzzy | Suggests closest matches with --fallback |
| 11 | Config drift SHA-256 (7 governance files) | Tracks constitutional configs specifically |
| 12 | Squad config schema (9 mandatory fields) | + auto-fixer for 48 squads |
| 13 | Skill drift detection (MD5 OUTDATED vs NEW) | Distinguishes real drift from unprojected skills |
| 14 | KPI baselines (3 processes measured) | Quantified governance metrics |
| 15 | Doctor with 10 checks + --fix | Most comprehensive unified health check |
| 16 | Multi-business L0-L4 isolation | 4 businesses with TTL-governed workspaces |

### OpenClaw: 4 Exclusive Practices

| # | Practice | Detail |
|---|----------|--------|
| 1 | 70% coverage enforced in CI | Highest coverage standard of any project |
| 2 | 37 E2E tests | Most E2E coverage |
| 3 | CalVer + stable/beta/dev channels | Most sophisticated release management |
| 4 | 11 AGENTS.md boundary files | Progressive architectural disclosure |

### BMAD: 6 Exclusive Practices

| # | Practice | Detail |
|---|----------|--------|
| 1 | max-warnings=0 CI enforcement | Zero tolerance — only BMAD does this |
| 2 | Husky + lint-staged + full npm test | Most rigorous pre-commit pipeline |
| 3 | Forbidden tokens check | Only BMAD scans for PII/secrets pre-publish |
| 4 | Adversarial review tests | Only BMAD has adversarial test cases |
| 5 | 14-rule skill validator (CRITICAL/HIGH/MEDIUM) | Most rigorous skill validation |
| 6 | Multi-language docs (FR + ZH-CN + VI) | 3 translations |

### Paperclip: 5 Exclusive Practices

| # | Practice | Detail |
|---|----------|--------|
| 1 | 302+ zod schemas (2,487 LOC) | Most comprehensive schema validation |
| 2 | Activity logging (actor/action/impact) | Only Paperclip traces all mutations |
| 3 | Run traceability (X-Paperclip-Run-Id) | Only Paperclip has per-run tracing |
| 4 | PR template with Thinking Path | Only Paperclip requires reasoning trace in PRs |
| 5 | Greptile 5/5 score required | Only Paperclip requires AI review score gate |

---

## 6. Quantitative Scorecard

| Metric | Sinkra | OpenClaw | BMAD | Paperclip |
|--------|:------:|:--------:|:----:|:---------:|
| **Quality practices** | 20 | 12 | 14 | 11 |
| **Governance practices** | 16 | 2 | 2 | 1 |
| **Total practices** | **36** | 14 | 16 | 12 |
| **Exclusive practices** | **16** | 4 | 6 | 5 |
| **Pre-commit/push checks** | 6+3 | 2 | **3+full npm test** | 0 |
| **Schema validators** | 9 fields | zod | **14 rules** | **302+ schemas** |
| **Doctor checks** | **10** | ~5 | 3 | **9** |
| **Test files** | 13 | **3,534** | 5 | 190+ |
| **E2E tests** | 1 | **37** | 0 | 2 |
| **Coverage** | 14.1% | **70%** | 0% | 0% |
| **CI workflows** | 5 | **13** | 5 | 6 |
| **Linter plugins** | 1 (oxlint) | 1 (oxlint) | **5 (ESLint)** | 0 |
| **Release automation** | ❌ | ✅ | ✅ | ✅ |
| **Code review AI** | ✅ CodeRabbit | ❌ | ✅ CodeRabbit | ✅ Greptile |

---

## 7. Verdict by Category

| Category | Leader | Why |
|----------|--------|-----|
| **Governance** | **Sinkra Hub** | 16 exclusive practices, constitution, 473 governed agents |
| **Testing volume** | **OpenClaw** | 3,534 tests, 37 E2E, 70% coverage |
| **Schema validation** | **Paperclip** | 302+ zod schemas (2,487 LOC) — nobody comes close |
| **Skill validation** | **BMAD** | 14 rules with severity levels + file ref validator |
| **Pre-commit rigor** | **BMAD** | Husky + lint-staged + full npm test + docs validation |
| **Formatting** | **BMAD** | Prettier + ESLint + markdownlint + max-warnings=0 |
| **Doctor/health** | **Sinkra ≈ Paperclip** | Sinkra 10 checks, Paperclip 9 checks + canRepair |
| **Release automation** | **Paperclip** | YYYY.DDD.N + canary auto + rollback + smoke tests |
| **Observability** | **Paperclip** | Activity logging + run traceability + budget + feedback |
| **PR process** | **Paperclip** | Thinking Path template + Greptile 5/5 gate |
| **Documentation** | **BMAD** | Astro site + 3 translations + style guide + link validation |
| **Total practices** | **Sinkra Hub (36)** | 2.25x more than second place (BMAD 16) |

---

## 8. What Each Project Should Learn From The Others

### Sinkra Hub Should Absorb (34 gaps):

**Immediate (P1, <1 day each):**
1. Husky pre-commit hooks (from BMAD)
2. lint-staged for staged files only (from BMAD)
3. max-warnings=0 in CI (from BMAD)
4. PR template with Thinking Path (from Paperclip)
5. Forbidden tokens check (from BMAD)
6. canRepair flag on doctor checks (from Paperclip)
7. Rollback script (from Paperclip)
8. Definition of Done checklist (from Paperclip)

**Short-term (P2, 1-3 days each):**
9. Prettier + packagejson plugin (from BMAD)
10. markdownlint-cli2 (from BMAD)
11. ESLint full config (from BMAD)
12. CodeRabbit .coderabbit.yaml (from BMAD)
13. File ref validator (from BMAD)
14. Smoke tests post-release (from Paperclip)
15. Activity logging (from Paperclip)
16. Run traceability (from Paperclip)
17. Release automation canary+stable (from Paperclip)
18. SPEC document (from Paperclip)
19. Greptile code review gate (from Paperclip)

**Medium-term (P2-P3, weeks):**
20. zod schemas for critical domain entities (from Paperclip)
21. More E2E tests (from OpenClaw)
22. CalVer + dev channels (from OpenClaw)
23. Adversarial review tests (from BMAD)
24. Budget system (from Paperclip)
25. Discord webhook notifications (from BMAD)
26. Docs site with build validation (from BMAD)
27. Style guide (from BMAD)
28. Boundary docs per subsystem (from OpenClaw)

**Long-term (P3, months):**
29. 70% coverage target (from OpenClaw — volume growth)
30. 37+ E2E tests (from OpenClaw — volume growth)
31. Plugin SDK (from OpenClaw)
32. i18n documentation (from BMAD/OpenClaw)
33. 302+ zod schemas full coverage (from Paperclip)
34. 3,534+ test files (from OpenClaw — volume growth)

### OpenClaw Should Learn:
- Constitutional governance framework (from Sinkra)
- TTL document staleness (from Sinkra)
- Agent authority enforcement (from Sinkra)
- Pre-commit hooks with lint-staged (from BMAD)
- zod schema validation depth (from Paperclip)
- PR template with reasoning trace (from Paperclip)

### BMAD Should Learn:
- TypeScript strict mode (from Paperclip/OpenClaw)
- zod schema validation (from Paperclip)
- E2E testing framework (from OpenClaw/Paperclip)
- Doctor command with --fix (from Sinkra/Paperclip)
- Coverage measurement and thresholds (from OpenClaw)
- Governance framework (from Sinkra)

### Paperclip Should Learn:
- Linting (ESLint/Oxlint from BMAD/Sinkra)
- Pre-commit hooks (from BMAD)
- Coverage measurement (from OpenClaw)
- Constitutional governance (from Sinkra)
- Agent authority matrix (from Sinkra)
- Skill validation rules (from BMAD)

---

## 9. The Composite Ideal

If you could combine the best of each project:

```
IDEAL = Sinkra Governance (16 practices)
      + OpenClaw Testing Volume (3,534 tests, 70% coverage)
      + BMAD Formatting Rigor (5 plugins, max-warnings=0, lint-staged)
      + Paperclip Schema Depth (302+ zod schemas)
      + Paperclip Observability (activity logging, run tracing, budget)
      + Paperclip PR Process (Thinking Path, Greptile 5/5)
      + BMAD Skill Validation (14 rules, adversarial tests)
      + BMAD Docs (Astro site, 3 translations, style guide)

Total: ~78 unique practices
```

No single project has more than 36 (Sinkra). The composite ideal has 78. There is massive opportunity for cross-pollination across the ecosystem.

---

*Generated by bench-analyst@spy | 4-Way Quality Engineering Benchmark | 2026-04-04*
*Data sources: 4 local clones, exhaustive file-level inventory*
