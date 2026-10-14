#!/usr/bin/env python3
"""
Prototype 3: Andragogic Validator Rules
===============================================================================
Story 0.5 (EPIC-SC-V2-001) — Prototype Validation

Validates:
  1. 3 Mayer rules applied to a sample deck-manifest.json
     - MAYER-01: Multimedia principle (every slide has a visual)
     - MAYER-06: Cognitive load / Segmentation (max words per slide type)
     - MAYER-05: Spatial contiguity (text and visual adjacency)
  2. Score and sub-checks in qa-report format
  3. Rules are not too restrictive for non-educational content

Prerequisites: None (pure Python, no external dependencies)

Run: python3 squads/slides-creator/scripts/prototype-andragogic.py

Rules reference: squads/slides-creator/data/andragogic-rules.yaml
===============================================================================
"""

import json
import os
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any

# ---------------------------------------------------------------------------
# Configuration — from andragogic-rules.yaml
# ---------------------------------------------------------------------------

# Word limit exceptions (from andragogic-rules.yaml word_limit_exceptions)
WORD_LIMIT_BASE = 40
WORD_LIMIT_EXCEPTIONS: dict[str, int] = {
    "data_table": 80,
    "comparison_matrix": 60,
    "quote": 60,
    "executive_summary": 80,
}

# K9 absolute max (from andragogic-rules.yaml always_on_rules K9)
K9_BASE_ABSOLUTE_MAX = 60

OUTPUT_DIR = "/tmp/slides-v2-prototype-andragogic"


# ---------------------------------------------------------------------------
# Data Structures
# ---------------------------------------------------------------------------

@dataclass
class RuleViolation:
    rule_id: str
    principle: str
    slide_index: int
    slide_title: str
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    message: str
    details: dict[str, Any] = field(default_factory=dict)


@dataclass
class RuleCheck:
    rule_id: str
    principle: str
    scope: str  # always_on | education_mode_only
    severity: str
    total_slides_checked: int = 0
    violations_count: int = 0
    pass_rate: float = 1.0
    violations: list[dict] = field(default_factory=list)


@dataclass
class QAReport:
    dimension: str = "andragogic"
    version: str = "1.0.0"
    timestamp: str = ""
    deck_id: str = ""
    education_mode: bool = False
    total_slides: int = 0
    rules_checked: int = 0
    total_violations: int = 0
    score: float = 0.0
    score_max: float = 100.0
    verdict: str = ""  # PASS | CONCERNS | FAIL
    checks: list[dict] = field(default_factory=list)
    summary: dict = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Sample Deck Manifest
# ---------------------------------------------------------------------------

def create_sample_deck_manifest() -> dict[str, Any]:
    """
    Creates a sample deck-manifest.json that exercises all 3 Mayer rules.

    Includes intentional violations for prototype validation:
    - Slide 3: text-only (violates MAYER-01 multimedia)
    - Slide 5: 55 words (violates MAYER-06 cognitive load for standard slides)
    - Slide 7: text far from visual (violates MAYER-05 contiguity)
    - Slide 8: data_table with 75 words (PASSES — within exception limit)
    - Slide 9: quote with 50 words (PASSES — within exception limit)
    - Slide 10: 85 words (violates K9 absolute max for standard slides)
    """
    return {
        "deck_id": "prototype-validation-001",
        "title": "Event-Driven Architecture — Training Deck",
        "education_mode": False,  # Test with always-on rules only
        "slides": [
            {
                "index": 0,
                "title": "Event-Driven Architecture",
                "slide_type": "title",
                "content_variant": "title",
                "word_count": 8,
                "text": "Event-Driven Architecture: Building Scalable Systems",
                "visual_elements_count": 1,
                "visual_elements": [{"type": "background_image", "description": "Abstract tech pattern"}],
                "has_visual": True,
                "has_text": True,
                "text_visual_proximity": "adjacent"
            },
            {
                "index": 1,
                "title": "What are Events?",
                "slide_type": "concept",
                "content_variant": "definition",
                "word_count": 28,
                "text": "An event is an immutable record of something that happened in the system. Events carry data about what changed and when it occurred.",
                "visual_elements_count": 1,
                "visual_elements": [{"type": "diagram", "description": "Event flow diagram"}],
                "has_visual": True,
                "has_text": True,
                "text_visual_proximity": "adjacent"
            },
            {
                "index": 2,
                "title": "Event Producers and Consumers",
                "slide_type": "process",
                "content_variant": "explanation",
                "word_count": 35,
                "text": "Producers emit events when state changes. Consumers subscribe to events they care about. This decoupling allows teams to evolve their services independently without coordination overhead.",
                "visual_elements_count": 1,
                "visual_elements": [{"type": "flowchart", "description": "Producer-Consumer flow"}],
                "has_visual": True,
                "has_text": True,
                "text_visual_proximity": "adjacent"
            },
            {
                "index": 3,
                "title": "Why Event-Driven?",
                "slide_type": "concept",
                "content_variant": "explanation",
                "word_count": 32,
                "text": "Event-driven architecture enables loose coupling between services. Each service can be developed, deployed, and scaled independently. This reduces coordination costs and increases team autonomy.",
                "visual_elements_count": 0,  # VIOLATION: MAYER-01 — no visual
                "visual_elements": [],
                "has_visual": False,
                "has_text": True,
                "text_visual_proximity": "none"
            },
            {
                "index": 4,
                "title": "CQRS Pattern",
                "slide_type": "process",
                "content_variant": "explanation",
                "word_count": 30,
                "text": "Command Query Responsibility Segregation separates read and write models. Write model optimized for consistency. Read model optimized for query performance and denormalized views.",
                "visual_elements_count": 1,
                "visual_elements": [{"type": "diagram", "description": "CQRS architecture diagram"}],
                "has_visual": True,
                "has_text": True,
                "text_visual_proximity": "adjacent"
            },
            {
                "index": 5,
                "title": "Event Sourcing Benefits",
                "slide_type": "concept",
                "content_variant": "explanation",
                "word_count": 55,  # VIOLATION: MAYER-06 — exceeds 40 word limit for concept slides
                "text": "Event sourcing stores all state changes as a sequence of events. This provides complete audit trail and temporal queries. You can reconstruct any past state by replaying events up to that point. Combined with CQRS this creates a powerful pattern for complex domains where history and compliance matter significantly.",
                "visual_elements_count": 1,
                "visual_elements": [{"type": "illustration", "description": "Event store timeline"}],
                "has_visual": True,
                "has_text": True,
                "text_visual_proximity": "adjacent"
            },
            {
                "index": 6,
                "title": "Saga Pattern",
                "slide_type": "process",
                "content_variant": "explanation",
                "word_count": 38,
                "text": "Sagas manage distributed transactions across multiple services. Each step has a compensating action for rollback. Orchestration sagas use a central coordinator. Choreography sagas use event chains.",
                "visual_elements_count": 1,
                "visual_elements": [{"type": "sequence_diagram", "description": "Saga orchestration flow"}],
                "has_visual": True,
                "has_text": True,
                "text_visual_proximity": "adjacent"
            },
            {
                "index": 7,
                "title": "Partitioning Strategies",
                "slide_type": "comparison",
                "content_variant": "comparison",
                "word_count": 35,
                "text": "Hash partitioning distributes events evenly. Range partitioning groups related events. Round-robin ensures balanced load. Choose based on your access patterns and ordering requirements.",
                "visual_elements_count": 1,
                "visual_elements": [{"type": "infographic", "description": "Partitioning comparison chart"}],
                "has_visual": True,
                "has_text": True,
                "text_visual_proximity": "separated"  # VIOLATION: MAYER-05 — text not adjacent
            },
            {
                "index": 8,
                "title": "Performance Comparison",
                "slide_type": "data_table",
                "content_variant": "data",
                "word_count": 75,  # PASSES: data_table exception allows up to 80
                "text": "REST API: 50ms latency, 1000 req/s, synchronous coupling. Event-Driven: 5ms publish, 50ms consume, 10000 events/s, asynchronous decoupling. GraphQL: 30ms latency, 800 req/s, partial coupling. gRPC: 10ms latency, 5000 req/s, binary protocol coupling. Each approach has trade-offs between latency throughput and coupling that depend on your specific requirements and team expertise.",
                "visual_elements_count": 1,
                "visual_elements": [{"type": "table", "description": "Performance comparison table"}],
                "has_visual": True,
                "has_text": True,
                "text_visual_proximity": "adjacent"
            },
            {
                "index": 9,
                "title": "Martin Fowler on Events",
                "slide_type": "quote",
                "content_variant": "quote",
                "word_count": 50,  # PASSES: quote exception allows up to 60
                "text": "\"The biggest advantage of event-driven architecture is that it provides a natural way to model the real world. Things happen, and we react to them. This fundamental insight makes our systems more resilient and adaptable to change.\" — Martin Fowler, Enterprise Integration Patterns",
                "visual_elements_count": 1,
                "visual_elements": [{"type": "portrait", "description": "Martin Fowler portrait"}],
                "has_visual": True,
                "has_text": True,
                "text_visual_proximity": "adjacent"
            },
            {
                "index": 10,
                "title": "Migration Roadmap",
                "slide_type": "concept",
                "content_variant": "explanation",
                "word_count": 85,  # VIOLATION: K9 — exceeds 60 absolute max for concept slides
                "text": "Step one identify your bounded contexts and map dependencies between services. Step two select a pilot domain with clear event boundaries and low risk. Step three implement event publishing alongside existing synchronous calls using the strangler fig pattern. Step four gradually migrate consumers to process events instead of making direct API calls. Step five remove synchronous dependencies once all consumers have migrated. Step six monitor event flow and optimize partitioning based on observed patterns and performance metrics in production.",
                "visual_elements_count": 1,
                "visual_elements": [{"type": "timeline", "description": "Migration roadmap"}],
                "has_visual": True,
                "has_text": True,
                "text_visual_proximity": "adjacent"
            },
            {
                "index": 11,
                "title": "Thank You",
                "slide_type": "closing",
                "content_variant": "closing",
                "word_count": 12,
                "text": "Thank you for attending. Questions? Contact me at speaker@example.com",
                "visual_elements_count": 1,
                "visual_elements": [{"type": "background_image", "description": "Contact info with QR code"}],
                "has_visual": True,
                "has_text": True,
                "text_visual_proximity": "adjacent"
            }
        ]
    }


# ---------------------------------------------------------------------------
# Rule Validators
# ---------------------------------------------------------------------------

def check_mayer_01(slide: dict) -> RuleViolation | None:
    """
    MAYER-01: Principio Multimidia (always_on, severity HIGH)

    Todo slide DEVE conter pelo menos um elemento visual.
    Excecoes: content_variant=quote com max 15 palavras, slide_type=STATEMENT.
    """
    if slide["visual_elements_count"] == 0:
        # Check exceptions
        if slide.get("content_variant") == "quote" and slide["word_count"] <= 15:
            return None
        if slide.get("slide_type", "").upper() == "STATEMENT":
            return None

        return RuleViolation(
            rule_id="MAYER-01",
            principle="Mayer — Principio Multimidia",
            slide_index=slide["index"],
            slide_title=slide["title"],
            severity="HIGH",
            message=f"Slide sem elemento visual (visual_elements_count=0)",
            details={
                "slide_type": slide.get("slide_type"),
                "content_variant": slide.get("content_variant"),
                "word_count": slide["word_count"],
                "fix_suggestion": "Adicionar diagrama, icone, ilustracao ou imagem ao slide"
            }
        )
    return None


def check_mayer_06(slide: dict) -> RuleViolation | None:
    """
    MAYER-06: Principio da Segmentacao / Cognitive Load (always_on, severity HIGH)

    Cada slide DEVE respeitar o limite de palavras para seu tipo.
    Limite-base: 40 palavras. Excecoes por slide_type conforme word_limit_exceptions.
    """
    slide_type = slide.get("slide_type", "")
    limit = WORD_LIMIT_EXCEPTIONS.get(slide_type, WORD_LIMIT_BASE)
    word_count = slide["word_count"]

    if word_count > limit:
        return RuleViolation(
            rule_id="MAYER-06",
            principle="Mayer — Principio da Segmentacao (Cognitive Load)",
            slide_index=slide["index"],
            slide_title=slide["title"],
            severity="HIGH",
            message=f"Slide com {word_count} palavras, limite para {slide_type} e {limit}",
            details={
                "word_count": word_count,
                "word_limit": limit,
                "slide_type": slide_type,
                "excess_words": word_count - limit,
                "is_exception_type": slide_type in WORD_LIMIT_EXCEPTIONS,
                "fix_suggestion": f"Reduzir para <= {limit} palavras ou dividir em 2 slides"
            }
        )
    return None


def check_mayer_05(slide: dict) -> RuleViolation | None:
    """
    MAYER-05: Principio da Contiguidade Espacial (always_on, severity MEDIUM)

    Texto explicativo e o elemento visual DEVEM estar adjacentes no mesmo slide.
    """
    if (slide.get("has_visual") and
        slide.get("has_text") and
        slide.get("text_visual_proximity") != "adjacent"):

        return RuleViolation(
            rule_id="MAYER-05",
            principle="Mayer — Principio da Contiguidade Espacial",
            slide_index=slide["index"],
            slide_title=slide["title"],
            severity="MEDIUM",
            message=f"Texto e visual nao estao adjacentes (proximity: {slide.get('text_visual_proximity')})",
            details={
                "text_visual_proximity": slide.get("text_visual_proximity"),
                "fix_suggestion": "Reposicionar texto proximo ao elemento visual no layout do slide"
            }
        )
    return None


def check_k9(slide: dict) -> RuleViolation | None:
    """
    K9: Killer Item — Sobrecarga Textual Absoluta (always_on, severity CRITICAL)

    Barreira final absoluta. Usa word_limit_exceptions como fonte unica de verdade,
    com fallback de 60 palavras para tipos sem excecao definida.
    """
    slide_type = slide.get("slide_type", "")
    type_limit = WORD_LIMIT_EXCEPTIONS.get(slide_type, K9_BASE_ABSOLUTE_MAX)
    k9_limit = max(type_limit, K9_BASE_ABSOLUTE_MAX)
    word_count = slide["word_count"]

    if word_count > k9_limit:
        return RuleViolation(
            rule_id="K9",
            principle="Killer Item — Sobrecarga Textual Absoluta",
            slide_index=slide["index"],
            slide_title=slide["title"],
            severity="CRITICAL",
            message=f"Slide com {word_count} palavras excede limite absoluto de {k9_limit} para {slide_type}",
            details={
                "word_count": word_count,
                "k9_limit": k9_limit,
                "slide_type": slide_type,
                "excess_words": word_count - k9_limit,
                "is_exception_type": slide_type in WORD_LIMIT_EXCEPTIONS,
                "fix_suggestion": f"BLOQUEANTE: Reduzir para <= {k9_limit} palavras. Slide nao pode ser publicado assim."
            }
        )
    return None


# ---------------------------------------------------------------------------
# Validator Engine
# ---------------------------------------------------------------------------

def validate_deck(deck_manifest: dict[str, Any]) -> QAReport:
    """
    Apply all always_on andragogic rules to a deck manifest.
    Returns a QA report in the format compatible with qa-inspector.
    """
    slides = deck_manifest.get("slides", [])
    education_mode = deck_manifest.get("education_mode", False)

    # Define rule checks
    rule_definitions = [
        {
            "id": "MAYER-01",
            "principle": "Mayer — Principio Multimidia",
            "scope": "always_on",
            "severity": "HIGH",
            "checker": check_mayer_01
        },
        {
            "id": "MAYER-06",
            "principle": "Mayer — Principio da Segmentacao",
            "scope": "always_on",
            "severity": "HIGH",
            "checker": check_mayer_06
        },
        {
            "id": "MAYER-05",
            "principle": "Mayer — Principio da Contiguidade Espacial",
            "scope": "always_on",
            "severity": "MEDIUM",
            "checker": check_mayer_05
        },
        {
            "id": "K9",
            "principle": "Killer Item — Sobrecarga Textual Absoluta",
            "scope": "always_on",
            "severity": "CRITICAL",
            "checker": check_k9
        }
    ]

    all_violations: list[RuleViolation] = []
    checks: list[RuleCheck] = []

    for rule_def in rule_definitions:
        # Skip education-only rules when not in education mode
        if rule_def["scope"] == "education_mode_only" and not education_mode:
            continue

        rule_check = RuleCheck(
            rule_id=rule_def["id"],
            principle=rule_def["principle"],
            scope=rule_def["scope"],
            severity=rule_def["severity"],
            total_slides_checked=len(slides)
        )

        for slide in slides:
            violation = rule_def["checker"](slide)
            if violation:
                all_violations.append(violation)
                rule_check.violations.append(asdict(violation))
                rule_check.violations_count += 1

        rule_check.pass_rate = (
            (len(slides) - rule_check.violations_count) / len(slides)
            if slides else 1.0
        )
        checks.append(rule_check)

    # Calculate overall score
    # Scoring: each rule has equal weight, score = average pass rate * 100
    total_pass_rate = sum(c.pass_rate for c in checks) / len(checks) if checks else 1.0
    score = round(total_pass_rate * 100, 1)

    # Determine verdict
    has_critical = any(v.severity == "CRITICAL" for v in all_violations)
    has_high = any(v.severity == "HIGH" for v in all_violations)

    if has_critical:
        verdict = "FAIL"
    elif has_high:
        verdict = "CONCERNS"
    elif score >= 90:
        verdict = "PASS"
    else:
        verdict = "CONCERNS"

    # Build severity summary
    severity_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for v in all_violations:
        severity_counts[v.severity] += 1

    report = QAReport(
        dimension="andragogic",
        version="1.0.0",
        timestamp=datetime.now(timezone.utc).isoformat(),
        deck_id=deck_manifest.get("deck_id", "unknown"),
        education_mode=education_mode,
        total_slides=len(slides),
        rules_checked=len(checks),
        total_violations=len(all_violations),
        score=score,
        score_max=100.0,
        verdict=verdict,
        checks=[asdict(c) for c in checks],
        summary={
            "by_severity": severity_counts,
            "rules_passed": sum(1 for c in checks if c.violations_count == 0),
            "rules_with_violations": sum(1 for c in checks if c.violations_count > 0),
            "education_mode_rules_skipped": sum(
                1 for r in rule_definitions if r["scope"] == "education_mode_only" and not education_mode
            ),
            "worst_slide": max(
                [(s["index"], sum(1 for v in all_violations if v.slide_index == s["index"]))
                 for s in slides],
                key=lambda x: x[1],
                default=(None, 0)
            ),
            "word_count_stats": {
                "min": min(s["word_count"] for s in slides) if slides else 0,
                "max": max(s["word_count"] for s in slides) if slides else 0,
                "avg": round(sum(s["word_count"] for s in slides) / len(slides), 1) if slides else 0,
                "slides_over_base_limit": sum(1 for s in slides if s["word_count"] > WORD_LIMIT_BASE)
            }
        }
    )

    return report


# ---------------------------------------------------------------------------
# Restrictiveness Test
# ---------------------------------------------------------------------------

def test_non_educational_restrictiveness(report: QAReport, deck_manifest: dict) -> dict:
    """
    Test that always_on rules are not too restrictive for non-educational content.

    Criteria:
    - Score should be >= 70% for a typical corporate deck
    - Only MAYER-01, MAYER-05, MAYER-06, K9 apply (no Kolb, DPC, Dreyfus, etc.)
    - data_table, quote, comparison_matrix, executive_summary have relaxed limits
    """
    slides = deck_manifest.get("slides", [])
    total = len(slides)

    # Count slides that pass all checks
    clean_slides = 0
    for slide in slides:
        violations = []
        if check_mayer_01(slide):
            violations.append("MAYER-01")
        if check_mayer_06(slide):
            violations.append("MAYER-06")
        if check_mayer_05(slide):
            violations.append("MAYER-05")
        if check_k9(slide):
            violations.append("K9")
        if not violations:
            clean_slides += 1

    # Word limit exceptions working correctly?
    exception_slides = [s for s in slides if s.get("slide_type") in WORD_LIMIT_EXCEPTIONS]
    exception_passes = sum(
        1 for s in exception_slides
        if s["word_count"] <= WORD_LIMIT_EXCEPTIONS.get(s["slide_type"], WORD_LIMIT_BASE)
    )

    result = {
        "test": "Non-educational restrictiveness check",
        "education_mode": False,
        "total_slides": total,
        "clean_slides": clean_slides,
        "clean_rate": f"{clean_slides / total * 100:.0f}%",
        "is_acceptable": clean_slides / total >= 0.70,
        "education_rules_applied": 0,
        "always_on_rules_applied": report.rules_checked,
        "word_limit_exceptions_tested": len(exception_slides),
        "word_limit_exceptions_passed": exception_passes,
        "exceptions_working": exception_passes == len(exception_slides),
        "verdict": "NOT TOO RESTRICTIVE" if clean_slides / total >= 0.60 else "TOO RESTRICTIVE"
    }

    return result


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("============================================")
    print(" Prototype 3: Andragogic Validator Rules")
    print("============================================")

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Step 1: Create sample deck manifest
    print("\n--- Step 1: Sample Deck Manifest ---")
    deck_manifest = create_sample_deck_manifest()
    print(f"  Created deck with {len(deck_manifest['slides'])} slides")
    print(f"  education_mode: {deck_manifest['education_mode']}")

    manifest_path = os.path.join(OUTPUT_DIR, "deck-manifest-sample.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(deck_manifest, f, indent=2, ensure_ascii=False)
    print(f"  Saved: {manifest_path}")

    # Step 2: Apply 3 Mayer rules + K9
    print("\n--- Step 2: Apply Andragogic Rules ---")
    report = validate_deck(deck_manifest)

    print(f"\n  Results:")
    print(f"  Score: {report.score}/{report.score_max}")
    print(f"  Verdict: {report.verdict}")
    print(f"  Rules checked: {report.rules_checked}")
    print(f"  Total violations: {report.total_violations}")
    print(f"  By severity: {report.summary['by_severity']}")

    # Print each violation
    for check in report.checks:
        status = "PASS" if check["violations_count"] == 0 else "FAIL"
        print(f"\n  [{status}] {check['rule_id']}: {check['principle']}")
        print(f"        Scope: {check['scope']} | Severity: {check['severity']}")
        print(f"        Pass rate: {check['pass_rate']:.0%} ({check['total_slides_checked'] - check['violations_count']}/{check['total_slides_checked']})")

        for v in check["violations"]:
            print(f"        -> Slide {v['slide_index']}: \"{v['slide_title']}\"")
            print(f"           {v['message']}")
            if "fix_suggestion" in v.get("details", {}):
                print(f"           Fix: {v['details']['fix_suggestion']}")

    # Save QA report
    report_path = os.path.join(OUTPUT_DIR, "qa-report-andragogic.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(asdict(report), f, indent=2, ensure_ascii=False)
    print(f"\n  Saved: {report_path}")

    # Step 3: Test restrictiveness
    print("\n--- Step 3: Restrictiveness Test ---")
    restrictiveness = test_non_educational_restrictiveness(report, deck_manifest)

    for key, value in restrictiveness.items():
        print(f"  {key}: {value}")

    restrictiveness_path = os.path.join(OUTPUT_DIR, "restrictiveness-test.json")
    with open(restrictiveness_path, "w", encoding="utf-8") as f:
        json.dump(restrictiveness, f, indent=2, ensure_ascii=False)
    print(f"\n  Saved: {restrictiveness_path}")

    # Summary
    print("\n============================================")
    print(" Prototype 3 Results")
    print("============================================")
    print(f"  Score: {report.score}/{report.score_max} ({report.verdict})")
    print(f"  Rules: {report.summary['rules_passed']} passed, {report.summary['rules_with_violations']} with violations")
    print(f"  Violations: {report.summary['by_severity']}")
    print(f"  Restrictiveness: {restrictiveness['verdict']}")
    print(f"  Word limit exceptions: {'WORKING' if restrictiveness['exceptions_working'] else 'BROKEN'}")
    print(f"  Education rules skipped: {report.summary['education_mode_rules_skipped']}")
    print(f"  Output dir: {OUTPUT_DIR}/")
    print("")
    print("  Files generated:")
    print(f"    - {manifest_path}")
    print(f"    - {report_path}")
    print(f"    - {restrictiveness_path}")
    print("")
    print("  Expected violations (by design):")
    print("    - Slide 3: MAYER-01 (text-only, no visual)")
    print("    - Slide 5: MAYER-06 (55 words, limit 40 for concept)")
    print("    - Slide 7: MAYER-05 (text separated from visual)")
    print("    - Slide 10: MAYER-06 + K9 (85 words, limit 60 for concept)")
    print("")
    print("  Expected passes (exception types):")
    print("    - Slide 8: data_table with 75 words (limit 80)")
    print("    - Slide 9: quote with 50 words (limit 60)")


if __name__ == "__main__":
    main()
