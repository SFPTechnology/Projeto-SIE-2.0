# Normalize Briefing

## SINKRA Task Anatomy (8 sections — migrated 2026-04-20 Wave 2)

```yaml
task: normalizeBriefing
atomic_layer: Atom
responsavel_type: Agent
session: null
phase: P00
Inputs:
  - { name: raw_briefing, type: text, source: user }
  - { name: reference_assets, type: array, source: user, optional: true }
Outputs:
  - { name: briefing.normalized.json, template: templates/briefing.normalized.json, lifecycle: [draft, validated] }
Pre_conditions:
  - raw_briefing.length > 0
Post_conditions:
  - briefing.normalized.json schema valid
  - all required fields populated OR marked placeholder_required
Acceptance_criteria:
  - Problem, objective, audience, constraints extracted
  - Source materials catalogued
  - Brand context reference resolved
Performance_and_Error_handling:
  duration_target: "< 3 min"
  error_strategy: request clarification from user
```

## Legacy Task Anatomy

```yaml
task_name: "Normalize Briefing"
status: active
responsible_executor: "slide-chief"
execution_type: Agent
elicit: true

input:
  - raw_briefing: "User input — topic, objectives, audience, context, constraints"
  - brand_context: "Workspace references (read-only from workspace/businesses/)"
  - source_materials: "Supporting docs, notes, URLs, screenshots, assets"
  - reference_assets: "Screenshots, PPTX, or visual references that trigger reference_first mode"
  - youtube_source: "(v2) YouTube URL for video-to-presentation pipeline (requires ENABLE_YOUTUBE_ENTRYPOINT)"
  - education_mode: "(v2) Boolean flag for andragogic validation (requires ENABLE_ANDRAGOGIC_VALIDATION)"

output:
  - briefing_normalized: "briefing.normalized.json"
  - intake_notes: "warnings, inferred values, blockers"

action_items:
  - "Phase 1: Extract fields from raw briefing"
  - "Phase 2: Resolve missing fields via elicitation (max 3 questions)"
  - "Phase 3: Detect format and apply planning rules"
  - "Phase 4: Resolve mode, aspect_ratio, induction_mode, max_slides"
  - "Phase 5: Check brand_config availability"
  - "Phase 6: Emit briefing.normalized.json or report blockers"

acceptance_criteria:
  - "topic and objective are explicit (not inferred without confirmation)"
  - "format is resolved from context or explicit user input"
  - "mode is derived from format_override or context triggers"
  - "aspect_ratio is derived from channel or defaults to 16:9"
  - "induction_mode set to reference_first when reference_assets present"
  - "max_slides calculated from format range or duration estimate"
  - "output_target includes ds presenter parity"
  - "warnings array captures all inferred values"
  - "blockers array captures all missing critical fields"

estimated_time: "1-3 exchanges with user"
```

## Workflow

### Phase 1: Field Extraction

Read the raw briefing and extract all available fields:

| Field | Source | Required? |
|-------|--------|-----------|
| `topic` | User input | YES — ASK if missing |
| `objective` | User input | YES — ASK if missing |
| `audience` | User input or inferred from context | INFER + FLAG |
| `context` | User input (where will this be presented?) | YES for mode detection |
| `duration` | User input or estimated from format | INFER + FLAG |
| `brand_config` | Workspace or user input | CHECK workspace first |
| `source_materials` | User-provided docs, URLs, notes | WARN if empty |
| `reference_assets` | User-provided screenshots, PPTX | Determines induction_mode |
| `output_targets` | User input or default | DEFAULT: ds |
| `youtube_source` | User-provided YouTube URL | Only when ENABLE_YOUTUBE_ENTRYPOINT=true |
| `education_mode` | User input or inferred from context | INFER + FLAG when educational signals detected |

### Phase 2: Elicitation (max 3 questions)

Present missing fields as a single consolidated prompt.

**Elicitation format:**
```
Briefing received. Resolving contract...

I need clarification on {N} points:
1. {question_1}
2. {question_2}
3. {question_3}

Preliminary resolution from what you provided:
- topic: "{extracted_topic}"
- context: {extracted_context} → mode: {inferred_mode}
- format: {inferred_format}
{warnings if any}
```

**Elicitation heuristics:**

| ID | WHEN | THEN |
|----|------|------|
| BN_001 | objective is vague | Ask: "What should the audience DO, FEEL, or KNOW after?" |
| BN_002 | audience is missing | Infer from topic + context. Flag for confirmation. |
| BN_003 | source_materials empty + complex topic | Warn: content will rely on general knowledge |
| BN_004 | brand_config missing + workspace has brand data | Auto-resolve from workspace. Report what was loaded. |
| BN_005 | reference_assets include screenshots/PPTX | Set induction_mode = reference_first |
| BN_006 | duration not specified | Estimate from format defaults. Flag estimate. |
| BN_007 | youtube_source provided + ENABLE_YOUTUBE_ENTRYPOINT=true | Set input_type = youtube_url. Extract video_id. Flag for transcription. |
| BN_008 | youtube_source provided + ENABLE_YOUTUBE_ENTRYPOINT=false | WARN: YouTube entrypoint disabled. Ignore youtube_source. |
| BN_009 | education signals detected (curso, aula, treinamento, workshop, tutorial, formacao) | Infer education_mode=true. Flag for confirmation. |
| BN_010 | education_mode=true + ENABLE_ANDRAGOGIC_VALIDATION=false | WARN: Andragogic validation disabled. education_mode will be stored but not enforced. |

### Phase 3: Format Detection

Apply the Format Selection tree from SOP-SLIDES-003 section 3.0:

| Signal | Format |
|--------|--------|
| "conference", "keynote", "TED" | ted_keynote |
| "investors", "fundraising", "Series A", "pitch" | pitch_deck |
| "sales", "prospect", "demo", "champion" | sales_deck |
| "technical", "engineering", "architecture", "code" | technical |
| "zoom", "virtual", "remote meeting" | zoom_virtual |
| "carousel", "stories", "reels", "instagram" | carousel_stories |
| None of the above | general |

### Phase 4: Planning Resolution

After format detection, derive execution constraints:

1. **mode** — from format_override (if format forces it) or mode_selection tree
2. **aspect_ratio** — from channel detection or default 16:9
3. **induction_mode** — registry_first (default) or reference_first (if reference_assets)
4. **max_slides** — from format slide_range, duration estimate, or default 15

### Phase 5: Brand Config Check

```
IF brand_config provided in briefing → use it
ELSE IF workspace/businesses/ has brand data → auto-resolve, report source
ELSE → WARN: "No brand config available. Deck will use generic defaults."
```

### Phase 6: Emit Output

Produce `briefing.normalized.json` with all fields resolved.

**Output schema:**
```json
{
  "topic": "string",
  "objective": "string",
  "audience": "string",
  "context": "string",
  "duration_minutes": "number",
  "format": "ted_keynote | pitch_deck | sales_deck | technical | zoom_virtual | carousel_stories | general",
  "mode": "palco | live | async",
  "aspect_ratio": "16:9 | 16:10 | 9:16 | 1:1",
  "induction_mode": "registry_first | reference_first",
  "max_slides": "number",
  "brand_config_resolved": "boolean",
  "brand_config_source": "string",
  "source_materials_count": "number",
  "reference_assets_count": "number",
  "output_targets": ["ds"],
  "youtube_source": "string | null",
  "input_type": "briefing | youtube_url",
  "education_mode": "boolean",
  "warnings": ["string"],
  "blockers": ["string"]
}
```

## Veto Conditions

| Condition | Action |
|-----------|--------|
| topic missing after 1 clarification | HALT intake. Report: "Cannot proceed without topic." |
| objective missing after 1 clarification | HALT intake. Report: "Cannot proceed without objective." |
| blockers array non-empty | HALT pipeline. List all blockers. |
| format forces mode but user requests different mode | WARN: format overrides mode. Ask confirmation. |

## Output Example

**Input:**
> "Preciso de uma apresentacao sobre o AIOX para uma conferencia de tech. Temos screenshots do produto e um doc com os principais features."

**Output:**
```
Briefing received. Resolving contract...

Clarification needed:
1. What should the audience DO, FEEL, or KNOW after this deck?

Preliminary resolution:
- topic: "AIOX"
- context: conferencia de tech → mode: palco
- format: general (could be ted_keynote or technical — depends on objective)
- ratio: 16:9 (projector default)
- induction_mode: reference_first (screenshots detected)
- source_materials: 1 doc (features)
- reference_assets: screenshots (count TBD)

Warnings:
- No brand_config specified. Will check workspace.
- Duration not specified. Estimating 30min based on conference format.

Awaiting objective clarification.
```

## Handoff

| Next Agent | When |
|------------|------|
| content-architect | Briefing normalized, no blockers, planning constraints ready |
| template-curator | induction_mode = reference_first (before content-architect) |

## Quality Gate

- [ ] All required fields resolved or explicitly blocked
- [ ] Format derived from evidence, not guessed
- [ ] Mode consistent with format override (if applicable)
- [ ] Warnings list all inferred values
- [ ] Blockers list all missing critical fields
- [ ] output_targets includes "ds"
