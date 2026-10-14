# YouTube to Briefing

## SINKRA Task Anatomy (8 sections — migrated 2026-04-20 Wave 2)

```yaml
task: youtubeToBriefing
atomic_layer: Atom
responsavel_type: Worker
session: null
phase: P00
conditional: "input_type == youtube"
Inputs:
  - { name: youtube_url, type: string, source: user }
  - { name: transcription_model, type: enum, default: whisper-cpp }
Outputs:
  - { name: briefing-skeleton.json, type: JSON, passes_to: normalize-briefing }
  - { name: transcript.txt, type: text, retention_days: 7 }
  - { name: keyframes, type: directory, retention_days: 7 }
Pre_conditions:
  - yt-dlp available OR external transcription API configured
  - url accessible
Post_conditions:
  - briefing skeleton passes normalize-briefing pre-conditions
Acceptance_criteria:
  - Transcript captured with timestamp markers
  - Keyframes extracted at scene-change boundaries
  - Briefing skeleton has problem/objective/audience stubs
Performance_and_Error_handling:
  duration_target: "< 15 min for 1h video"
  error_strategy: retry with fallback transcription API
  fallback: manual briefing input if transcription fails 3x
```

## Legacy Task Anatomy

```yaml
task_name: "YouTube to Briefing"
status: active
responsible_executor: "slide-chief"
execution_type: Agent
elicit: true

input:
  - youtube_url: "YouTube video URL (required)"
  - brand_context: "Workspace brand references (optional, from workspace/businesses/)"
  - adaptation_preferences: "User preferences for content adaptation (collected in Stage 5)"

output:
  - youtube_extraction: "youtube-extraction.json (validated against schemas/contracts/youtube-extraction.schema.json)"
  - briefing_normalized: "briefing.normalized.json with source_type='youtube'"
  - cost_report: "extraction cost breakdown (embedded in extraction_status)"

action_items:
  - "Stage 1: Ingestao — yt-dlp metadata + availability check"
  - "Stage 2: Transcricao — youtube-transcript-api fast path + Whisper fallback"
  - "Stage 3: Extracao Visual — PySceneDetect + ffmpeg keyframes"
  - "Stage 4: Analise Multimodal — Gemini Flash triagem"
  - "Stage 5: Adaptacao Q&A — 3-5 elicitation questions"
  - "Stage 6: Briefing Generation — youtube-extraction.json to briefing.normalized.json"

acceptance_criteria:
  - "youtube-extraction.json validates against schemas/contracts/youtube-extraction.schema.json"
  - "briefing.normalized.json has source_type='youtube'"
  - "Budget cap SLIDES_VIDEO_COST_CAP ($5 default) is enforced"
  - "Total timeout is 5 minutes for a 30-minute video"
  - "Fallback chain is respected: subtitles -> Whisper local -> Whisper API -> HALT"
  - "Dual validation: output validated at producer AND consumer"
  - "extraction_status tracks transcript source, visual analysis engine, and cost"

estimated_time: "3-5 minutes per video (30 min video baseline)"

feature_flag: "ENABLE_YOUTUBE_ENTRYPOINT"
budget_cap_env: "SLIDES_VIDEO_COST_CAP"
budget_cap_default_usd: 5.00
timeout_seconds: 300

dependencies:
  schemas:
    - "schemas/contracts/youtube-extraction.schema.json"
  templates:
    - "squads/slides-creator/templates/briefing.normalized.json"
  data:
    - "squads/slides-creator/data/cost-tracking.yaml"
  prototype:
    - "squads/slides-creator/scripts/prototype-youtube.py"

tools_required:
  cli:
    - "yt-dlp (pip install yt-dlp)"
    - "ffmpeg (brew install ffmpeg)"
  python:
    - "youtube-transcript-api (pip install youtube-transcript-api)"
    - "scenedetect[opencv] (pip install scenedetect[opencv])"
    - "openai-whisper (pip install openai-whisper) — fallback only"
  apis:
    - "Gemini 2.5 Flash (GOOGLE_AI_API_KEY) — visual analysis"
    - "Whisper API (OPENAI_API_KEY) — transcription fallback only"
```

---

## Pre-Flight Check

Before executing this task, verify:

1. Feature flag `ENABLE_YOUTUBE_ENTRYPOINT` is enabled
2. `yt-dlp` is installed and accessible: `yt-dlp --version`
3. `ffmpeg` is installed: `ffmpeg -version`
4. `GOOGLE_AI_API_KEY` is set in `.env` (for Gemini Flash)
5. Budget cap is configured: `SLIDES_VIDEO_COST_CAP` (defaults to $5.00)

If any pre-flight check fails, HALT and report the missing prerequisite.

---

## Stage 1: Ingestao

**Objective:** Download video metadata and verify availability using yt-dlp.

**Cost:** $0.00 (free, local CLI)

### Steps

1. **Validate URL format**
   - Accept: `youtube.com/watch?v=`, `youtu.be/`, `youtube.com/shorts/`
   - Reject: non-YouTube URLs, playlist URLs (single video only)
   - Extract `video_id` from URL (11-character alphanumeric string)

2. **Extract metadata via yt-dlp (no download)**
   ```bash
   yt-dlp --dump-json --no-download "{youtube_url}"
   ```
   - Parse JSON output for: `id`, `title`, `duration`, `channel`, `upload_date`, `description`
   - If command fails: HALT with error "Video unavailable or URL invalid"

3. **Availability checks**
   - Duration check: reject videos > 120 minutes (budget guard)
   - Duration check: warn if video < 2 minutes (likely insufficient content)
   - Age restriction check: if `age_limit > 0`, warn user
   - Live stream check: if `is_live == true`, HALT with "Live streams not supported"

4. **Build video_metadata object**
   ```json
   {
     "title": "<from yt-dlp>",
     "video_id": "<11-char ID>",
     "duration_seconds": "<integer>",
     "channel": "<from yt-dlp>",
     "url": "<original URL>",
     "published_at": "<ISO 8601 from upload_date>",
     "language": "<from yt-dlp or 'unknown'>"
   }
   ```

### Exit Criteria
- `video_metadata` object populated with all required fields
- Video is available and within duration limits
- Cost accumulated: $0.00

### Error Handling
- Network error: retry once after 5s, then HALT
- Video private/deleted: HALT with clear message
- Region-locked: HALT with message suggesting VPN or alternate URL

---

## Stage 2: Transcricao

**Objective:** Extract transcript with timestamps in float seconds.

**Cost:** $0.00 (fast path) | $0.006/min (Whisper API fallback)

### Fallback Chain

```
[1] youtube-transcript-api (free, instant)
    ↓ fails
[2] Whisper local (free, 0.5-2x duration)
    ↓ fails or unavailable
[3] Whisper API (paid, fast)
    ↓ fails
[4] HALT with message
```

### Step 1: Fast Path — youtube-transcript-api

```python
from youtube_transcript_api import YouTubeTranscriptApi

ytt_api = YouTubeTranscriptApi()
transcript_data = ytt_api.fetch(video_id, languages=["pt", "en"])

segments = [{
    "start": float(entry.start),
    "end": float(entry.start + entry.duration),
    "text": entry.text
} for entry in transcript_data]
```

- Language priority: `["pt", "en"]` (configurable)
- On success: set `transcript_source = "youtube_captions"`
- On failure (no captions available): proceed to Step 2

### Step 2: Fallback — Whisper Local

```python
import whisper

# Extract audio first
# yt-dlp -x --audio-format mp3 -o "cache/slides-v2/videos/{video_id}/audio.mp3" "{url}"

model = whisper.load_model("medium")
result = model.transcribe("audio.mp3", language="pt")

segments = [{
    "start": float(seg["start"]),
    "end": float(seg["end"]),
    "text": seg["text"],
    "confidence": float(seg.get("avg_logprob", 0))
} for seg in result["segments"]]
```

- Model: `medium` (balance speed/accuracy)
- On success: set `transcript_source = "whisper_local"`
- On failure (no GPU, model too large): proceed to Step 3
- Cost: $0.00 (local compute)

### Step 3: Fallback — Whisper API

```python
from openai import OpenAI

client = OpenAI()
with open("audio.mp3", "rb") as f:
    result = client.audio.transcriptions.create(
        model="whisper-1",
        file=f,
        response_format="verbose_json",
        timestamp_granularities=["segment"]
    )
```

- Cost: $0.006/minute of audio
- Budget check: estimate cost BEFORE calling (`duration_seconds / 60 * 0.006`)
- If estimated cost would exceed remaining video budget: HALT
- On success: set `transcript_source = "whisper_api"`
- On failure: proceed to Step 4

### Step 4: HALT

- All transcription methods failed
- HALT with message: "Transcription unavailable for this video. Tried: YouTube captions, Whisper local, Whisper API. Check video availability and API keys."
- Do NOT proceed to Stage 3 without transcript

### Output

```json
{
  "transcript_segments": [
    {
      "start": 0.0,
      "end": 5.4,
      "text": "Welcome to this talk...",
      "confidence": 0.95
    }
  ]
}
```

- Timestamps MUST be float seconds (NOT "MM:SS" strings)
- Confidence field is optional (available with Whisper, not with YouTube captions)

### Exit Criteria
- `transcript_segments[]` populated with start/end in float seconds
- `transcript_source` recorded in extraction_status
- Cost accumulated: $0.00 (fast path) or actual Whisper API cost

---

## Stage 3: Extracao Visual

**Objective:** Extract keyframes from video using scene detection.

**Cost:** $0.00 (local processing)

### Steps

1. **Download video for frame extraction**
   ```bash
   yt-dlp -f "bestvideo[height<=720]" --merge-output-format mp4 \
     -o "cache/slides-v2/videos/{video_id}/video.mp4" "{url}"
   ```
   - Resolution cap: 720p (sufficient for frame analysis, saves bandwidth)
   - Output: `cache/slides-v2/videos/{video_id}/video.mp4`

2. **Detect scene changes via PySceneDetect**
   ```python
   from scenedetect import detect, ContentDetector

   scene_list = detect(video_path, ContentDetector(threshold=27.0))
   ```
   - Threshold 27.0 is the recommended default for presentations/lectures
   - Expected output: 30-80 scenes for a 30-minute video
   - If > 100 scenes detected: increase threshold to 35.0 and re-run
   - If < 10 scenes detected: decrease threshold to 20.0 and re-run

3. **Extract keyframe per scene via ffmpeg**
   ```bash
   ffmpeg -ss {timestamp} -i video.mp4 -frames:v 1 -q:v 2 \
     "cache/slides-v2/videos/{video_id}/keyframes/scene_{index:04d}_{timestamp:.1f}s.jpg"
   ```
   - One frame per scene (at scene start)
   - Quality: `-q:v 2` (high quality JPEG)
   - Output dir: `cache/slides-v2/videos/{video_id}/keyframes/`

4. **Build frames manifest**
   ```json
   [
     {
       "index": 0,
       "timestamp_seconds": 0.0,
       "path": "cache/slides-v2/videos/{video_id}/keyframes/scene_0000_0.0s.jpg"
     }
   ]
   ```

### Guard Rails
- Max frames: 100 (if PySceneDetect returns more, increase threshold)
- Min frames: 5 (if less, decrease threshold or use fixed interval fallback: 1 frame every 30s)
- Timeout: 60 seconds for frame extraction phase

### Exit Criteria
- Keyframes saved to `cache/slides-v2/videos/{video_id}/keyframes/`
- Frames manifest with index, timestamp, path for each frame
- Cost accumulated: $0.00

---

## Stage 4: Analise Multimodal

**Objective:** Use Gemini Flash to analyze video content and classify visual moments.

**Cost:** ~$0.50-1.50 per 30-minute video

### Steps

1. **Budget pre-check**
   - Calculate remaining budget: `SLIDES_VIDEO_COST_CAP - accumulated_cost`
   - Estimated cost for Gemini Flash: ~$0.50-1.50 for 30min video
   - If remaining budget < $0.50: skip visual analysis, set `visual_analysis_source = "none"`

2. **Prepare Gemini Flash request**

   Option A -- Upload video file (preferred for short videos < 15min):
   ```python
   from google import genai

   client = genai.Client(api_key=os.getenv("GOOGLE_AI_API_KEY"))
   video_file = client.files.upload(file=video_path)
   ```

   Option B -- Send keyframes as images (for longer videos):
   - Select top 30 keyframes (evenly distributed across video duration)
   - Send as batch image analysis

3. **Gemini Flash prompt**

   ```
   Analyze this video/these frames from a presentation/lecture and return JSON:

   {
     "chapters": [
       {
         "timestamp_seconds": <float>,
         "title": "<chapter title>",
         "summary": "<1-2 sentence summary>"
       }
     ],
     "visual_moments": [
       {
         "timestamp_seconds": <float>,
         "type": "diagram|code|text_slide|whiteboard|screen_demo|infographic|speaker_only",
         "description": "<what is being shown>",
         "text_content": "<OCR of visible text, if any>",
         "confidence": <0.0-1.0>
       }
     ],
     "key_concepts": ["concept1", "concept2"],
     "presentation_structure": {
       "main_thesis": "<main argument or topic>",
       "supporting_arguments": ["arg1", "arg2"],
       "examples_shown": ["example1", "example2"]
     }
   }

   RULES:
   1. Timestamps MUST be in float seconds (e.g., 45.2), NOT "MM:SS"
   2. Classify visual moments by what appears ON SCREEN, not what is said
   3. speaker_only = only the presenter's face/body, no visual aids
   4. confidence: how certain you are about the classification (0.0-1.0)
   5. Focus on moments with educational/informational visual content
   ```

   - Model: `gemini-2.5-flash`
   - Response format: `application/json`
   - Timeout: 120 seconds

4. **Parse and validate response**
   - Validate JSON structure
   - Filter visual_moments: remove entries with `type = "speaker_only"` (no slide value)
   - Filter visual_moments: remove entries with `confidence < 0.3` (noise)
   - Associate keyframe paths with visual_moments by nearest timestamp

5. **Record cost**
   - Actual cost from API response metadata
   - Update accumulated cost: `accumulated_cost += actual_cost`
   - Set `visual_analysis_source = "gemini_flash"`

### Error Handling
- Gemini API error: retry once, then set `visual_analysis_source = "none"` and continue
- Timeout: set `visual_analysis_source = "none"` and continue (visual analysis is enhancement, not blocking)
- Budget exceeded: set `visual_analysis_source = "none"` and continue

### Exit Criteria
- `chapters[]` populated (or empty if Gemini unavailable)
- `visual_moments[]` populated with type classification and confidence
- `visual_analysis_source` recorded
- Cost tracked in extraction_status

---

## Stage 5: Adaptacao Q&A

**Objective:** Elicit 3-5 adaptation questions from the user to tailor the presentation.

**Cost:** $0.00 (uses conversation context, no API call)

**IMPORTANT:** This stage has `elicit: true`. User interaction is REQUIRED.

### Questions Template

Based on the structured content from Stages 1-4, present the user with 3-5 targeted questions:

#### Question 1: TARGET PRODUCT/SERVICE
```
O video original fala sobre: "{main_thesis}"
Qual e o seu produto/servico que quer apresentar?
(Ou deseja manter o conteudo original?)
```

#### Question 2: TARGET AUDIENCE
```
O publico sugerido pelo video e: "{inferred_audience}"
Seu publico e diferente? Se sim, qual?
```

#### Question 3: TONE/STYLE
```
O tom do video e: "{detected_tone}"
Quer manter esse tom ou prefere algo diferente?
Opcoes: profissional | casual | tecnico | inspiracional | educacional
```

#### Question 4: STRUCTURE (keep vs adapt)
```
O video tem {N} secoes-chave:
{numbered list of chapters}

Quais quer manter, quais adaptar, quais remover?
(Default: manter todas)
```

#### Question 5: VISUAL REFERENCES (conditional -- only if visual_moments > 0)
```
Identifiquei {M} conceitos visuais no video:
{list of visual_moments with type and description}

Quais fazem sentido para seu contexto?
Quer recriar algum diagrama para seu produto?
```

### Adaptive Behavior

- If user says "manter tudo" / "keep as is": skip remaining questions, use original content
- If user provides product/audience: adapt all questions to reference their context
- If visual_moments is empty: skip Question 5
- Maximum 5 questions. Do NOT exceed this.

### Output

```json
{
  "adaptation": {
    "target_product": "<user response or original>",
    "target_audience": "<user response or inferred>",
    "tone": "<selected tone>",
    "structure_decisions": {
      "keep": [<chapter indices>],
      "adapt": [<chapter indices>],
      "remove": [<chapter indices>]
    },
    "visual_selections": [<selected visual_moment indices>],
    "reorganize": false
  }
}
```

### Exit Criteria
- User has answered at least Questions 1-3
- Adaptation preferences recorded
- Ready to generate briefing

---

## Stage 6: Briefing Generation

**Objective:** Convert youtube-extraction.json to briefing.normalized.json with source_type="youtube".

**Cost:** $0.00 (data transformation only)

### Steps

1. **Assemble youtube-extraction.json**

   Combine outputs from Stages 1-4:
   ```json
   {
     "video_metadata": { ... },       // Stage 1
     "chapters": [ ... ],              // Stage 4
     "visual_moments": [ ... ],        // Stage 4
     "transcript_segments": [ ... ],   // Stage 2
     "extraction_status": {
       "transcript_source": "<youtube_captions|whisper_local|whisper_api>",
       "visual_analysis_source": "<gemini_flash|none>",
       "cost_usd": <accumulated_cost>,
       "processing_time_seconds": <total_elapsed>
     }
   }
   ```

2. **Validate youtube-extraction.json at PRODUCER**
   - Validate against `schemas/contracts/youtube-extraction.schema.json`
   - Required fields: video_metadata, transcript_segments, visual_moments, extraction_status
   - Timestamps must be float seconds (type: number, not string)
   - If validation fails: HALT with schema violation details

3. **Transform to briefing.normalized.json**

   Mapping from youtube-extraction to briefing.normalized:

   | YouTube Extraction | Briefing Normalized |
   |-------------------|---------------------|
   | `video_metadata.title` + adaptation.target_product | `topic` |
   | adaptation.target_product context | `objective` |
   | adaptation.target_audience | `audience` |
   | "Adapted from YouTube video" | `context` |
   | `duration_seconds / 60` | `duration_minutes` |
   | "general" (default) | `format` |
   | "async" (default for video-sourced) | `mode` |
   | "16:9" | `aspect_ratio` |
   | "reference_first" if visual_moments > 0 | `induction_mode` |
   | `len(chapters) * 3` (clamped 8-30) | `max_slides` |
   | check workspace | `brand_config_resolved` |
   | count of source transcript sections | `source_materials_count` |
   | count of keyframe paths | `reference_assets_count` |
   | `["ds"]` | `output_targets` |
   | collected during normalization | `warnings` |
   | empty (or validation errors) | `blockers` |

   Additional YouTube-specific fields (optional, for content-architect consumption):
   ```json
   {
     "source_type": "youtube",
     "youtube_source": {
       "url": "<original URL>",
       "video_id": "<11-char ID>",
       "extraction_profile": "<transcript_source>",
       "chapters": [ ... ],
       "visual_moments": [ ... ],
       "adaptation": { ... }
     }
   }
   ```

4. **Validate briefing.normalized.json at CONSUMER**
   - Validate against `squads/slides-creator/templates/briefing.normalized.json`
   - All required fields from the schema must be present
   - `blockers` array must be empty to proceed
   - If validation fails: add violations to `blockers[]`

5. **Apply adaptation decisions**
   - Remove chapters marked for removal in adaptation.structure_decisions
   - Tag chapters marked for adaptation with `adapted: true`
   - Filter visual_moments to only those selected by user
   - Apply tone override to content context

6. **Save outputs**
   - `youtube-extraction.json` → working directory
   - `briefing.normalized.json` → working directory
   - Both files logged in cost-log if applicable

### Exit Criteria
- `youtube-extraction.json` validates against shared schema (producer validation)
- `briefing.normalized.json` validates against briefing contract (consumer validation)
- `source_type = "youtube"` is set
- `blockers` array is empty
- Total cost <= `SLIDES_VIDEO_COST_CAP`
- Total time <= 5 minutes

---

## Budget Enforcement

Budget tracking follows `squads/slides-creator/data/cost-tracking.yaml`.

### Per-Stage Cost Breakdown (30-min video baseline)

| Stage | Component | Cost |
|-------|-----------|------|
| 1 | yt-dlp metadata (local) | $0.00 |
| 2a | youtube-transcript-api (fast path) | $0.00 |
| 2b | Whisper local (fallback) | $0.00 |
| 2c | Whisper API (fallback) | ~$0.18 (30min) |
| 3 | PySceneDetect + ffmpeg (local) | $0.00 |
| 4 | Gemini 2.5 Flash (visual analysis) | ~$0.50-1.50 |
| 5 | Q&A (conversation, no API) | $0.00 |
| 6 | Data transformation (local) | $0.00 |
| **Total (fast path)** | | **~$0.50-1.50** |
| **Total (Whisper API fallback)** | | **~$0.68-1.68** |

### Budget Cap Algorithm

```
remaining = SLIDES_VIDEO_COST_CAP - accumulated_cost

BEFORE each paid API call:
  1. estimate = estimated_cost_for_call
  2. IF estimate > remaining:
     - Skip this call
     - Use degraded alternative (none, or free fallback)
     - Log: "Budget guard: skipped {engine}, cost ${estimate} > remaining ${remaining}"
  3. IF estimate <= remaining:
     - Proceed with call
     - After call: accumulated_cost += actual_cost
     - Log entry to cost tracking
```

---

## Timeout Enforcement

Total pipeline timeout: 300 seconds (5 minutes) for a 30-minute video.

### Per-Stage Timeout Budget

| Stage | Timeout | Action on Timeout |
|-------|---------|-------------------|
| 1 - Ingestao | 30s | HALT (video inaccessible) |
| 2 - Transcricao | 90s | Move to next fallback in chain |
| 3 - Extracao Visual | 60s | Use fixed-interval fallback (1 frame/30s) |
| 4 - Analise Multimodal | 120s | Skip analysis, set source="none" |
| 5 - Adaptacao Q&A | No timeout | User-interactive, wait for response |
| 6 - Briefing Generation | 10s | Should never timeout (data transform) |

---

## Error Recovery

| Error | Stage | Action |
|-------|-------|--------|
| Video unavailable | 1 | HALT with clear message |
| No captions + no Whisper | 2 | HALT: "Transcription unavailable" |
| PySceneDetect fails | 3 | Fallback: ffmpeg fixed interval (1 frame/30s) |
| Gemini API error | 4 | Continue without visual analysis |
| User abandons Q&A | 5 | Use defaults (keep all, original tone) |
| Schema validation fails | 6 | HALT: report validation errors |
| Budget exceeded | Any | Skip paid operations, continue with free |
| Timeout exceeded | Any | Per-stage timeout actions above |

---

## Integration Points

### Upstream (produces input for this task)
- User provides YouTube URL via `*create-from-youtube` command on slide-chief

### Downstream (consumes output of this task)
- `briefing.normalized.json` feeds directly into Phase 1 of `generate-presentation.yaml`
- Content-architect consumes `youtube_source.visual_moments` for `visual_strategy`
- Visual-scout uses keyframe paths as `reference_assets`

### Cross-Squad Contract
- Output `youtube-extraction.json` conforms to `schemas/contracts/youtube-extraction.schema.json`
- Contract is shared between etl-ops (producer) and slides-creator (consumer)
- Schema drift detected by contract tests (Story 4.4)
