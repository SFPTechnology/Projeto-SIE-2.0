# Slides Creator Templates

JSON schemas and examples for the canonical artifacts produced by the slides-creator pipeline.

## Available Templates

| File | Producer | Description |
|------|----------|-------------|
| `briefing.normalized.json` | slide-chief | Schema for the normalized briefing contract. Output of *normalize-briefing. |
| `deck-manifest.json` | content-architect | Schema for the renderer-agnostic deck manifest. Output of *assemble-manifest. |
| `qa-report.json` | qa-inspector | Schema for the QA evaluation report. Output of *score-deck. |

## Usage

These schemas define the contract between agents. Each file contains:

- JSON Schema properties and required fields
- An `_example` key with a realistic sample payload
- Description fields that trace back to the agent frameworks that produce/consume the artifact

Agents consuming these artifacts should validate against the schema before processing.
