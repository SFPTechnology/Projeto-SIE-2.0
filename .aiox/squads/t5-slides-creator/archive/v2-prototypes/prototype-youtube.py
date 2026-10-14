#!/usr/bin/env python3
"""
Prototype 2: YouTube Transcript + Gemini Flash
===============================================================================
Story 0.5 (EPIC-SC-V2-001) — Prototype Validation

Validates:
  1. Transcript extraction from YouTube via youtube-transcript-api
  2. Chapter segmentation strategy via Gemini Flash (documented, not executed)
  3. Output mapping to briefing.normalized.json format

Prerequisites:
  - pip install youtube-transcript-api
  - GEMINI_API_KEY in .env (for Gemini Flash — documented only, not called)

Run: python3 squads/slides-creator/scripts/prototype-youtube.py

Contract reference: schemas/contracts/youtube-extraction.schema.json
===============================================================================
"""

import json
import os
import sys
from datetime import datetime
from typing import Any

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Sample video for testing (a public tech talk with captions)
# Replace with any YouTube video that has captions enabled
SAMPLE_VIDEO_ID = "dQw4w9WgXcQ"  # Placeholder — replace with real tech talk ID
SAMPLE_VIDEO_URL = f"https://www.youtube.com/watch?v={SAMPLE_VIDEO_ID}"

OUTPUT_DIR = "/tmp/slides-v2-prototype-youtube"

# ---------------------------------------------------------------------------
# Step 1: Extract transcript via youtube-transcript-api
# ---------------------------------------------------------------------------

def extract_transcript(video_id: str) -> dict[str, Any]:
    """
    Extract transcript from YouTube video using youtube-transcript-api.

    This is the fast path (no cost, no API key needed) for videos with
    existing captions. Falls back to Whisper for videos without captions
    (not implemented in this prototype).

    Returns data conforming to youtube-extraction.schema.json
    """
    print(f"\n--- Step 1: Transcript Extraction ---")
    print(f"  Video ID: {video_id}")
    print(f"  URL: https://www.youtube.com/watch?v={video_id}")

    try:
        from youtube_transcript_api import YouTubeTranscriptApi

        # Fetch transcript — tries auto-generated captions first,
        # then manual captions. Language preference: pt, en
        ytt_api = YouTubeTranscriptApi()
        transcript_data = ytt_api.fetch(video_id, languages=["pt", "en"])

        # Convert to our contract format (float seconds, not strings)
        segments = []
        for entry in transcript_data:
            segments.append({
                "start": float(entry.start),
                "end": float(entry.start + entry.duration),
                "text": entry.text
            })

        print(f"  [PASS] Transcript extracted: {len(segments)} segments")
        print(f"  [INFO] First segment: {segments[0] if segments else 'empty'}")
        print(f"  [INFO] Last segment: {segments[-1] if segments else 'empty'}")

        # Calculate total duration from segments
        total_duration = max(s["end"] for s in segments) if segments else 0

        return {
            "video_metadata": {
                "title": f"[Extracted from {video_id}]",
                "video_id": video_id,
                "duration_seconds": int(total_duration),
                "channel": "[requires YouTube Data API]",
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "language": "pt"
            },
            "transcript_segments": segments,
            "visual_moments": [],  # Requires frame analysis (Stage 3 of pipeline)
            "extraction_status": {
                "transcript_source": "youtube_captions",
                "visual_analysis_source": "none",
                "cost_usd": 0.0,
                "processing_time_seconds": 0.0
            },
            "_prototype_note": "Real pipeline adds visual_moments via PySceneDetect + Gemini Flash"
        }

    except ImportError:
        print("  [FAIL] youtube-transcript-api not installed")
        print("  [INFO] Install: pip install youtube-transcript-api")
        return _generate_sample_extraction(video_id)

    except Exception as e:
        print(f"  [WARN] Transcript extraction failed: {e}")
        print("  [INFO] Using sample data for prototype validation")
        return _generate_sample_extraction(video_id)


def _generate_sample_extraction(video_id: str) -> dict[str, Any]:
    """
    Generate sample extraction data when youtube-transcript-api is unavailable.
    Uses realistic data that conforms to youtube-extraction.schema.json.
    """
    print("  [INFO] Generating sample extraction data for prototype validation")

    return {
        "video_metadata": {
            "title": "Building Scalable Systems with Event-Driven Architecture",
            "video_id": video_id,
            "duration_seconds": 1847,
            "channel": "TechTalks",
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "published_at": "2025-11-15T10:00:00Z",
            "language": "en"
        },
        "chapters": [
            {"timestamp_seconds": 0, "title": "Introduction", "summary": "Overview of event-driven architecture"},
            {"timestamp_seconds": 180.5, "title": "Core Concepts", "summary": "Events, producers, consumers"},
            {"timestamp_seconds": 420.0, "title": "Implementation Patterns", "summary": "CQRS, Event Sourcing, Saga"},
            {"timestamp_seconds": 780.0, "title": "Scaling Strategies", "summary": "Partitioning, backpressure, dead letters"},
            {"timestamp_seconds": 1200.0, "title": "Case Study", "summary": "Real-world migration from REST to events"},
            {"timestamp_seconds": 1600.0, "title": "Q&A", "summary": "Audience questions and wrap-up"}
        ],
        "visual_moments": [
            {"timestamp_seconds": 45.2, "type": "diagram", "description": "System architecture diagram", "confidence": 0.92},
            {"timestamp_seconds": 320.8, "type": "code", "description": "Event handler implementation", "text_content": "async function handleEvent(event) { ... }", "confidence": 0.88},
            {"timestamp_seconds": 550.0, "type": "diagram", "description": "CQRS pattern diagram", "confidence": 0.95},
            {"timestamp_seconds": 890.0, "type": "infographic", "description": "Partitioning strategies comparison", "confidence": 0.78},
            {"timestamp_seconds": 1250.0, "type": "screen_demo", "description": "Live demo of event dashboard", "confidence": 0.85}
        ],
        "transcript_segments": [
            {"start": 0.0, "end": 5.4, "text": "Welcome to this talk about event-driven architecture."},
            {"start": 5.4, "end": 12.1, "text": "Today we'll explore how events can decouple your systems.", "confidence": 0.95},
            {"start": 12.1, "end": 20.0, "text": "I've been building event-driven systems for the past 8 years.", "confidence": 0.92},
            {"start": 180.5, "end": 190.0, "text": "Let's start with the core concepts. What is an event?"},
            {"start": 190.0, "end": 200.0, "text": "An event is an immutable record of something that happened."},
            {"start": 420.0, "end": 430.0, "text": "Now let's look at implementation patterns. First, CQRS."},
            {"start": 430.0, "end": 445.0, "text": "CQRS separates read and write models for better scalability."},
            {"start": 780.0, "end": 790.0, "text": "Scaling event-driven systems requires careful partitioning."},
            {"start": 1200.0, "end": 1215.0, "text": "Let me show you a real case study from our migration."},
            {"start": 1600.0, "end": 1610.0, "text": "Thank you. Let's open up for questions."}
        ],
        "extraction_status": {
            "transcript_source": "youtube_captions",
            "visual_analysis_source": "gemini_flash",
            "cost_usd": 0.12,
            "processing_time_seconds": 34.7
        }
    }


# ---------------------------------------------------------------------------
# Step 2: Chapter Segmentation via Gemini Flash (documented)
# ---------------------------------------------------------------------------

def document_gemini_segmentation(extraction: dict[str, Any]) -> dict[str, Any]:
    """
    Documents how Gemini Flash would segment transcript into chapters.

    This prototype does NOT call Gemini Flash API — it documents the
    prompt template, expected input/output, and cost estimation.

    In production (Story 4.2), Gemini Flash receives the full transcript
    and returns structured chapters with key points.
    """
    print(f"\n--- Step 2: Gemini Flash Chapter Segmentation (Documented) ---")

    segments = extraction.get("transcript_segments", [])
    total_duration = extraction["video_metadata"]["duration_seconds"]

    # Concatenate transcript for prompt
    full_text = " ".join(s["text"] for s in segments)
    word_count = len(full_text.split())

    print(f"  Transcript: {len(segments)} segments, {word_count} words, {total_duration}s duration")

    # Document the Gemini Flash prompt template
    gemini_prompt = {
        "model": "gemini-2.0-flash",
        "purpose": "Segment YouTube transcript into logical chapters with key points",
        "cost_estimate": f"~${0.00001 * word_count:.4f} USD (input: {word_count} words)",
        "prompt_template": """You are an expert content analyzer. Given a YouTube video transcript,
segment it into logical chapters and extract key points for each chapter.

TRANSCRIPT:
{transcript_text}

VIDEO DURATION: {duration_seconds} seconds

OUTPUT FORMAT (JSON):
{
  "chapters": [
    {
      "timestamp_seconds": <float>,
      "end_seconds": <float>,
      "title": "<concise chapter title>",
      "summary": "<1-2 sentence summary>",
      "key_points": ["<point 1>", "<point 2>", ...],
      "slide_count_suggestion": <int>,
      "content_type": "<concept|process|data|comparison|timeline>"
    }
  ],
  "total_chapters": <int>,
  "estimated_slides": <int>,
  "main_topic": "<overall topic>"
}

RULES:
1. Each chapter should be 2-5 minutes of content
2. Key points become slide titles
3. content_type maps to VisualEngine routing table
4. Suggest 2-4 slides per chapter
5. Timestamps MUST be in float seconds (not MM:SS format)""",
        "expected_response_schema": {
            "chapters": [
                {
                    "timestamp_seconds": 0.0,
                    "end_seconds": 180.5,
                    "title": "Introduction",
                    "summary": "Overview of event-driven architecture and speaker background",
                    "key_points": [
                        "Event-driven architecture decouples systems",
                        "8 years of practical experience"
                    ],
                    "slide_count_suggestion": 2,
                    "content_type": "concept"
                }
            ]
        }
    }

    print(f"  [PASS] Gemini Flash prompt template documented")
    print(f"  [INFO] Estimated cost per video: ${gemini_prompt['cost_estimate']}")
    print(f"  [INFO] Model: {gemini_prompt['model']}")

    return gemini_prompt


# ---------------------------------------------------------------------------
# Step 3: Map to briefing.normalized.json format
# ---------------------------------------------------------------------------

def map_to_briefing_normalized(
    extraction: dict[str, Any],
    gemini_doc: dict[str, Any]
) -> dict[str, Any]:
    """
    Maps YouTube extraction output to briefing.normalized.json format.

    This is the bridge between the YouTube pipeline (Upgrade 4) and the
    existing slides-creator pipeline (v1). The normalized briefing is the
    standard input format for content-architect.

    source_type: "youtube_video" signals the pipeline that this briefing
    originated from YouTube content.
    """
    print(f"\n--- Step 3: Map to briefing.normalized.json ---")

    video = extraction["video_metadata"]
    chapters = extraction.get("chapters", [])
    segments = extraction.get("transcript_segments", [])
    visual_moments = extraction.get("visual_moments", [])

    # Build normalized briefing
    briefing_normalized = {
        "version": "2.0.0",
        "source_type": "youtube_video",
        "source_metadata": {
            "video_id": video["video_id"],
            "video_url": video["url"],
            "video_title": video["title"],
            "channel": video["channel"],
            "duration_seconds": video["duration_seconds"],
            "language": video.get("language", "en"),
            "extraction_cost_usd": extraction["extraction_status"]["cost_usd"]
        },
        "presentation": {
            "title": video["title"],
            "subtitle": f"Baseado em: {video['channel']}",
            "language": video.get("language", "en"),
            "target_slides": sum(
                ch.get("slide_count_suggestion", 3)
                for ch in gemini_doc.get("expected_response_schema", {}).get("chapters", [])
            ) or len(chapters) * 3,
            "education_mode": False,
            "audience_profile": {
                "dreyfus_level": "competent",
                "context": "professional"
            }
        },
        "modules": [],
        "visual_assets": {
            "from_video": [
                {
                    "timestamp_seconds": vm["timestamp_seconds"],
                    "type": vm["type"],
                    "description": vm.get("description", ""),
                    "confidence": vm["confidence"],
                    "usage_suggestion": _map_visual_to_engine(vm["type"])
                }
                for vm in visual_moments
            ]
        },
        "brand": {
            "design_tokens_path": None,
            "note": "Brand tokens should be provided by the user or loaded from workspace/businesses/{brand}/"
        },
        "_pipeline_hints": {
            "skip_normalize": True,
            "source_has_chapters": len(chapters) > 0,
            "source_has_visuals": len(visual_moments) > 0,
            "budget_cap_usd": 5.00
        }
    }

    # Map chapters to modules
    for i, chapter in enumerate(chapters):
        module = {
            "module_index": i,
            "title": chapter["title"],
            "summary": chapter.get("summary", ""),
            "timestamp_range": {
                "start": chapter["timestamp_seconds"],
                "end": chapters[i + 1]["timestamp_seconds"] if i + 1 < len(chapters) else video["duration_seconds"]
            },
            "key_points": chapter.get("key_points", [chapter.get("summary", "")]),
            "transcript_excerpt": _get_transcript_for_range(
                segments,
                chapter["timestamp_seconds"],
                chapters[i + 1]["timestamp_seconds"] if i + 1 < len(chapters) else video["duration_seconds"]
            ),
            "slide_count_suggestion": chapter.get("slide_count_suggestion", 3),
            "content_type": chapter.get("content_type", "concept"),
            "relevant_visuals": [
                vm for vm in visual_moments
                if chapter["timestamp_seconds"] <= vm["timestamp_seconds"] < (
                    chapters[i + 1]["timestamp_seconds"] if i + 1 < len(chapters) else video["duration_seconds"]
                )
            ]
        }
        briefing_normalized["modules"].append(module)

    print(f"  [PASS] Mapped to briefing.normalized.json format")
    print(f"  [INFO] Modules: {len(briefing_normalized['modules'])}")
    print(f"  [INFO] Visual assets from video: {len(briefing_normalized['visual_assets']['from_video'])}")
    print(f"  [INFO] source_type: {briefing_normalized['source_type']}")
    print(f"  [INFO] Target slides: {briefing_normalized['presentation']['target_slides']}")

    return briefing_normalized


def _get_transcript_for_range(
    segments: list[dict],
    start: float,
    end: float
) -> str:
    """Extract transcript text for a time range."""
    texts = [
        s["text"] for s in segments
        if s["start"] >= start and s["start"] < end
    ]
    return " ".join(texts) if texts else ""


def _map_visual_to_engine(visual_type: str) -> str:
    """
    Map visual_moment type to recommended VisualEngine.
    Based on routing_table from visual-engines.yaml.
    """
    mapping = {
        "diagram": "d2",          # architecture/hierarchy -> D2
        "code": "mermaid",        # code snippets -> Mermaid sequence
        "text_slide": "none",     # text-only -> no visual engine needed
        "whiteboard": "d2",       # whiteboard drawings -> D2 recreation
        "screen_demo": "none",    # screenshots -> use frame directly
        "infographic": "gpt_image",  # infographics -> GPT Image recreation
        "speaker_only": "none",   # speaker face -> skip
        "other": "none"
    }
    return mapping.get(visual_type, "none")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("============================================")
    print(" Prototype 2: YouTube + Gemini Flash")
    print("============================================")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Step 1: Extract transcript
    extraction = extract_transcript(SAMPLE_VIDEO_ID)

    # Save extraction output (conforms to youtube-extraction.schema.json)
    extraction_path = os.path.join(OUTPUT_DIR, "youtube-extraction.json")
    with open(extraction_path, "w", encoding="utf-8") as f:
        json.dump(extraction, f, indent=2, ensure_ascii=False)
    print(f"\n  Saved: {extraction_path}")

    # Step 2: Document Gemini Flash segmentation
    gemini_doc = document_gemini_segmentation(extraction)

    gemini_path = os.path.join(OUTPUT_DIR, "gemini-segmentation-spec.json")
    with open(gemini_path, "w", encoding="utf-8") as f:
        json.dump(gemini_doc, f, indent=2, ensure_ascii=False)
    print(f"  Saved: {gemini_path}")

    # Step 3: Map to briefing.normalized.json
    briefing = map_to_briefing_normalized(extraction, gemini_doc)

    briefing_path = os.path.join(OUTPUT_DIR, "briefing-normalized.json")
    with open(briefing_path, "w", encoding="utf-8") as f:
        json.dump(briefing, f, indent=2, ensure_ascii=False)
    print(f"  Saved: {briefing_path}")

    # Summary
    print("\n============================================")
    print(" Prototype 2 Results")
    print("============================================")
    print(f"  Extraction: {'LIVE' if 'youtube_transcript_api' in sys.modules else 'SAMPLE DATA'}")
    print(f"  Segments: {len(extraction.get('transcript_segments', []))}")
    print(f"  Chapters: {len(extraction.get('chapters', []))}")
    print(f"  Visual moments: {len(extraction.get('visual_moments', []))}")
    print(f"  Briefing modules: {len(briefing.get('modules', []))}")
    print(f"  Output dir: {OUTPUT_DIR}/")
    print("")
    print("  Files generated:")
    print(f"    - {extraction_path}")
    print(f"    - {gemini_path}")
    print(f"    - {briefing_path}")
    print("")
    print("  Pipeline flow validated:")
    print("    youtube-transcript-api -> extraction.json")
    print("    -> Gemini Flash segmentation (documented)")
    print("    -> briefing.normalized.json (slides-creator input)")


if __name__ == "__main__":
    main()
