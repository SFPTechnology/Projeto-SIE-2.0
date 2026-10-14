# Caveats — AIOX Research × Deep Research Bench Submission

Honest disclosures about the AIOX submission. These caveats are public-facing and accompany the score.

## Provider & Model

- **LLM:** `claude-sonnet-4-6` (Anthropic, direct API)
- **Why not Opus:** Production-typical AIOX deployments use Sonnet. Submitting with Opus would inflate the score and misrepresent real-world AIOX performance.

## Pipeline

- **Skill invoked:** `/tech-research --yolo` (autonomous, no clarifying questions)
- **Multi-LLM cross-reference:** DISABLED for this submission. AIOX *can* invoke multiple LLMs via `--deep` flag, but that would inflate single-provider comparison.
- **Coverage Gate:** ACTIVE at 50/70 threshold. Tasks failing coverage are reported as-is (not retried indefinitely).
- **Citation Gate:** ACTIVE at 0.85 verified_ratio. Tasks with unverified citations are flagged but answers reported.

## Budget & Cost

- **Total cost:** $X.XX USD (to fill after run)
- **Cost per task (avg):** $Y.YY USD
- **Wall time total:** Z minutes
- **Tasks executed:** N / N_total (skipped reasons listed in score-report.json)

## Limitations

1. **Search providers:** WebSearch + Context7 + (optional) Exa. No proprietary search index.
2. **No private KB:** AIOX has private-KB capability (Local Deep Research absorption planned) but disabled for this public submission.
3. **No browser automation:** AIOX does not run Playwright/Puppeteer in this submission (limits dynamic web evidence).
4. **No deep-read of PDFs:** WebFetch only — no specialized PDF extraction.

## What This Score Means

✅ A user invoking AIOX `/tech-research` in production today on similar query patterns would expect this performance.

❌ This is NOT the maximum theoretical AIOX score. Adding:
- `--deep` flag (multi-LLM cross-reference) would likely add ~5-10%
- Private-KB integration would likely add ~5-15% for domain-specific tasks
- Browser automation would help on dynamic-content questions
- Opus model would likely add ~10-20%

We report what production looks like, not what's possible with maximum spend.

## Reproducibility

See `reproducibility.md` for full env, model pinning, and re-execution instructions.

## Contact

Questions about the submission: alan@alanicolas.com
