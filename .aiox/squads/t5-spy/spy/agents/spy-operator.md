# Spy Operator

```yaml
id: spy-operator
name: "Spy Operator"
role: "Human approval and strategic input"
tier: human
specialty: "Approval, scoping, executive decision"
sinkra_type: Human
human_in_the_loop: true
```

## Purpose

The Spy Operator is the **Human executor** in the SINKRA Four-Executor model for the spy squad. Responsible for strategic decisions, scope approval, and quality sign-off during benchmark and research pipelines.

## Responsibilities

- Approve or reject benchmark scope before pipeline starts
- Validate executive reports before publication
- Provide strategic input on competitive positioning
- Sign off on deviation requests (DEV-SPY-*)

## Activation

This agent activates when:
- `bench-detect` requires human confirmation of comparison type (elicit: true)
- Executive report requires approval before publish
- Cross-domain handoff requires sign-off

## Executor Profile

| Field | Value |
|-------|-------|
| SINKRA Type | Human |
| Human-in-the-Loop | true |
| Output Schema | competitive-brief |
| Can Execute | false |
| Can Review | competitive-intelligence, market-analysis |

## SINKRA Mandamentos Compliance

- M1 (One Executor per Task): Human is assigned as executor for tasks requiring human judgment
- M5 (Quality Gates): Human provides final approval gate for published benchmarks

_spy-operator v1.0.0 | spy squad_
