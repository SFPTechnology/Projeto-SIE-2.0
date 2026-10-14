# Reproducibility — AIOX Research × Deep Research Bench

## Environment

| Component | Value (to fill after run) |
|---|---|
| AIOX version | (commit SHA do `sinkra-hub` no momento do run) |
| Bench repo | `Ayanami0730/deep_research_bench` |
| Bench commit SHA | (PIN exato no momento do clone) |
| Date executed | (preencher após run) |
| OS | macOS Darwin 24.6.0 (or specify Linux distro) |

## LLM Configuration

| Setting | Value | Rationale |
|---|---|---|
| Model | `claude-sonnet-4-6` | Production-typical (NOT opus to inflate score) |
| Temperature | 0.7 | tech-research default |
| Max tokens | 8000 per call | tech-research default |
| Max iterations per task | 3 | COVERAGE_GATE bound |
| Budget cap (per task) | $0.50 USD | Honest reporting + cost discipline |
| Provider | Anthropic API direct | (not OpenRouter for determinism) |

## Pipeline Configuration

| Setting | Value |
|---|---|
| Skill | `/tech-research` |
| Mode | `--yolo` (autonomous, no clarifying questions) |
| Coverage Gate threshold | 50/70 |
| Citation Gate threshold | 0.85 verified_ratio |
| Multi-LLM cross-reference | disabled (single-LLM submission) |
| Search providers | WebSearch + Context7 + Exa (when available) |

## How to Reproduce

```bash
# 1. Clone Sinkra Hub at the exact commit
git clone https://github.com/oalanicolas/sinkra-hub
cd sinkra-hub
git checkout <commit-sha-from-this-doc>

# 2. Clone the bench at the pinned SHA
git clone https://github.com/Ayanami0730/deep_research_bench ../bench/deep-research-bench
cd ../bench/deep-research-bench
git checkout <bench-commit-sha-from-this-doc>
cd -

# 3. Set API keys
export ANTHROPIC_API_KEY=sk-...
export EXA_API_KEY=...  # optional

# 4. Run pilot first (5 tasks, ~$1-3)
bash docs/bench/aiox-deep-research-bench-submission/scripts/run-deep-research-bench.sh --pilot 5

# 5. Validate pilot score ≥0.40 before proceeding
python3 docs/bench/aiox-deep-research-bench-submission/scripts/aggregate-scores.py --pilot

# 6. Full run (40+ tasks, ~$5-15, ~1-2h)
bash docs/bench/aiox-deep-research-bench-submission/scripts/run-deep-research-bench.sh --full

# 7. Compute final score
python3 docs/bench/aiox-deep-research-bench-submission/scripts/aggregate-scores.py
```

## Determinism Limitations

LLM inference is non-deterministic at temperature > 0. To minimize variance:

1. Run each task 3x and report median score (not mean)
2. Use temperature 0.7 (lower variance than 1.0)
3. Pin model version exactly (e.g., `claude-sonnet-4-6-20251001` not `claude-sonnet-4-6-latest`)

Expected variance: ±3-5% on individual task scores, ±1-2% on aggregate score.

## Anti-Inflation Disclosures

What we did NOT do (intentional honest reporting):

- ❌ Use `claude-opus-4-7` (more expensive, higher quality, NOT production-typical)
- ❌ Use multi-LLM cross-reference (would inflate score with single-submission claim)
- ❌ Run only easy tasks and skip hard ones
- ❌ Use a custom evaluation prompt that differs from the bench's judge
- ❌ Disable Coverage/Citation gates to allow weaker answers through

What we DID do:

- ✅ Use standard `/tech-research --yolo` invocation (no special bench-only branches)
- ✅ Run ALL tasks in the bench (no cherry-picking)
- ✅ Use the bench's official judge protocol
- ✅ Report total cost and wall time
- ✅ Pin bench commit SHA for future verification
