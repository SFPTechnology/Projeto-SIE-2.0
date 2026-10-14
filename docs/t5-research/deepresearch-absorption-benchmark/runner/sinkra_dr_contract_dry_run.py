#!/usr/bin/env python3
"""Generate SINKRA-DR-40 contract dry-run outputs.

This runner validates the bench output contract without executing third-party
deep research projects. Each adapter run emits the nine required artifacts so
the dashboard, evaluators and future real adapters have a stable target shape.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


REQUIRED_OUTPUTS = [
    "trace.jsonl",
    "tool-calls.jsonl",
    "claims.yaml",
    "sources.yaml",
    "report.md",
    "rubric-results.yaml",
    "cost-latency.yaml",
    "failure-analysis.md",
    "replay-manifest.yaml",
]


ADAPTERS = [
    {
        "id": "dzhng-deep-research",
        "role": "minimal_baseline",
        "mode": "contract_stub",
        "capabilities": ["breadth_depth", "structured_outputs", "progress"],
    },
    {
        "id": "gpt-researcher",
        "role": "research_facade",
        "mode": "contract_stub",
        "capabilities": ["source_strategy", "mcp_retriever", "report_facade"],
    },
    {
        "id": "langchain-open-deep-research",
        "role": "graph_runtime",
        "mode": "contract_stub",
        "capabilities": ["supervisor_graph", "parallel_research", "compression"],
    },
    {
        "id": "local-deep-research",
        "role": "local_private_runtime",
        "mode": "contract_stub",
        "capabilities": ["local_first", "mcp_api", "private_kb"],
    },
    {
        "id": "deep-searcher",
        "role": "private_kb_rag",
        "mode": "contract_stub",
        "capabilities": ["provider_registry", "collection_routing", "chain_of_rag"],
    },
    {
        "id": "drbench",
        "role": "enterprise_oracle",
        "mode": "contract_stub",
        "capabilities": ["task_eval_env", "report_insights", "sandbox_fixture"],
    },
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(f"{json.dumps(row, ensure_ascii=False)}\n" for row in rows))


def write_yaml(path: Path, value: dict[str, Any]) -> None:
    path.write_text(yaml.safe_dump(value, allow_unicode=True, sort_keys=False))


def load_yaml(path: Path) -> dict[str, Any]:
    return yaml.safe_load(path.read_text()) or {}


def load_gold_claims(base: Path, task: dict[str, Any]) -> list[dict[str, Any]]:
    rel = task.get("gold_claims_file")
    if not rel:
        return []
    path = base / rel
    if not path.exists():
        return []
    return list((load_yaml(path).get("claims") or []))


def materialize_run(base: Path, out_root: Path, adapter: dict[str, Any], task_path: Path) -> dict[str, Any]:
    task = load_yaml(task_path)
    task_id = str(task["id"])
    adapter_id = str(adapter["id"])
    run_id = f"{adapter_id}__{task_id}"
    run_dir = out_root / adapter_id / task_id
    run_dir.mkdir(parents=True, exist_ok=True)
    timestamp = now_iso()
    gold_claims = load_gold_claims(base, task)
    selected_claims = gold_claims[:5]

    events = [
        {"timestamp": timestamp, "run_id": run_id, "system_id": adapter_id, "task_id": task_id, "event_type": "plan_created", "payload": {"mode": "contract_dry_run", "group": task.get("group")}},
        {"timestamp": timestamp, "run_id": run_id, "system_id": adapter_id, "task_id": task_id, "event_type": "search_query", "payload": {"query": task.get("prompt"), "synthetic": True}},
        {"timestamp": timestamp, "run_id": run_id, "system_id": adapter_id, "task_id": task_id, "event_type": "source_extracted", "payload": {"source_id": f"{task_id}-S1", "fixture": "public_or_private_synthetic"}},
        {"timestamp": timestamp, "run_id": run_id, "system_id": adapter_id, "task_id": task_id, "event_type": "claim_created", "payload": {"claims": len(selected_claims)}},
        {"timestamp": timestamp, "run_id": run_id, "system_id": adapter_id, "task_id": task_id, "event_type": "final_answer", "payload": {"report": "report.md", "dry_run": True}},
    ]
    write_jsonl(run_dir / "trace.jsonl", events)

    write_jsonl(run_dir / "tool-calls.jsonl", [
        {"timestamp": timestamp, "run_id": run_id, "tool": "fixture_loader", "status": "ok", "input": task_path.name, "output": "fixtures loaded"},
        {"timestamp": timestamp, "run_id": run_id, "tool": "contract_normalizer", "status": "ok", "input": adapter_id, "output": REQUIRED_OUTPUTS},
    ])

    claims = {
        "schema": "sinkra-claims-v1",
        "run_id": run_id,
        "task_id": task_id,
        "system_id": adapter_id,
        "mode": "contract_dry_run",
        "claims": [
            {
                "id": claim.get("id", f"{task_id}-C{index + 1}"),
                "text": claim.get("text", f"Dry-run claim {index + 1}"),
                "source_ids": claim.get("source_refs", [f"{task_id}-S{index + 1}"]),
                "support": "synthetic_gold_fixture",
                "required": bool(claim.get("required", False)),
            }
            for index, claim in enumerate(selected_claims)
        ],
    }
    write_yaml(run_dir / "claims.yaml", claims)

    sources = {
        "schema": "sinkra-sources-v1",
        "run_id": run_id,
        "task_id": task_id,
        "system_id": adapter_id,
        "sources": [
            {
                "id": f"{task_id}-S{index + 1}",
                "type": "synthetic_fixture",
                "title": f"Fonte sintética {index + 1} para {task_id}",
                "path": f"fixtures/gold-claims/{task_id}.yaml",
                "credibility": "HIGH",
            }
            for index, _ in enumerate(selected_claims)
        ],
    }
    write_yaml(run_dir / "sources.yaml", sources)

    report = [
        f"# Dry-Run Report — {adapter_id} / {task_id}",
        "",
        "Status: contrato materializado; sistema real não executado.",
        "",
        f"Prompt: {task.get('prompt')}",
        "",
        "## Claims Sintéticos",
        "",
    ]
    report.extend(f"- {claim['id']}: {claim['text']}" for claim in claims["claims"])
    report.extend([
        "",
        "## Próximo Passo",
        "",
        "Substituir este stub pelo adapter real mantendo exatamente os mesmos outputs.",
        "",
    ])
    (run_dir / "report.md").write_text("\n".join(report))

    write_yaml(run_dir / "rubric-results.yaml", {
        "schema": "sinkra-rubric-results-v1",
        "run_id": run_id,
        "mode": "contract_dry_run",
        "scores": {
            "required_outputs": 100,
            "claim_schema": 100,
            "source_schema": 100,
            "real_execution": 0,
        },
        "verdict": "PASS_CONTRACT_ONLY",
    })

    write_yaml(run_dir / "cost-latency.yaml", {
        "schema": "sinkra-cost-latency-v1",
        "run_id": run_id,
        "mode": "contract_dry_run",
        "wall_clock_seconds": 0,
        "llm_tokens": 0,
        "search_api_cost_usd": 0,
        "notes": "Dry-run sem execução de modelo ou ferramenta externa.",
    })

    (run_dir / "failure-analysis.md").write_text(
        "# Failure Analysis\n\n"
        "- Nenhuma falha de contrato detectada no dry-run.\n"
        "- Risco remanescente: adapter real ainda precisa provar tool-use, custo, latência e qualidade factual.\n"
    )

    write_yaml(run_dir / "replay-manifest.yaml", {
        "schema": "sinkra-replay-manifest-v1",
        "run_id": run_id,
        "task_file": str(task_path.relative_to(base)),
        "adapter": adapter,
        "outputs": REQUIRED_OUTPUTS,
        "mode": "contract_dry_run",
    })

    missing = [name for name in REQUIRED_OUTPUTS if not (run_dir / name).exists()]
    return {
        "run_id": run_id,
        "adapter": adapter_id,
        "task_id": task_id,
        "status": "PASS" if not missing else "FAIL",
        "missing_outputs": missing,
        "output_dir": str(run_dir.relative_to(base)),
        "claims": len(claims["claims"]),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bench-dir", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--out", default="execution-results/2026-05-18-contract-dry-run")
    parser.add_argument("--limit", type=int, default=0)
    args = parser.parse_args()

    base = Path(args.bench_dir).resolve()
    out_root = base / args.out
    out_root.mkdir(parents=True, exist_ok=True)
    task_paths = sorted((base / "tasks").glob("SINKRA-DR-*.yaml"))
    if args.limit:
        task_paths = task_paths[: args.limit]

    records: list[dict[str, Any]] = []
    for adapter in ADAPTERS:
        for task_path in task_paths:
            records.append(materialize_run(base, out_root, adapter, task_path))

    passed = sum(1 for record in records if record["status"] == "PASS")
    manifest = {
        "schema": "sinkra-dr-contract-dry-run-manifest-v1",
        "generated_at": now_iso(),
        "mode": "contract_dry_run",
        "adapters": ADAPTERS,
        "tasks": len(task_paths),
        "runs": len(records),
        "pass": passed,
        "fail": len(records) - passed,
        "required_outputs": REQUIRED_OUTPUTS,
        "records": records,
    }
    (out_root / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")

    rows = [
        "| Métrica | Valor |",
        "| --- | --- |",
        f"| Adapters | {len(ADAPTERS)} |",
        f"| Tasks | {len(task_paths)} |",
        f"| Runs | {len(records)} |",
        f"| PASS | {passed} |",
        f"| FAIL | {len(records) - passed} |",
        f"| Outputs por run | {len(REQUIRED_OUTPUTS)} |",
    ]
    (out_root / "README.md").write_text(
        "# SINKRA-DR-40 Contract Dry-Run\n\n"
        "Este resultado valida o formato dos outputs obrigatórios. Não representa execução real dos repositórios.\n\n"
        + "\n".join(rows)
        + "\n"
    )
    print(json.dumps({k: manifest[k] for k in ["mode", "tasks", "runs", "pass", "fail"]}, ensure_ascii=False))
    return 0 if passed == len(records) else 1


if __name__ == "__main__":
    raise SystemExit(main())
