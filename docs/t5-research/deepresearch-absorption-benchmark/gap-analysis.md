# Gap Analysis

| Gap | Severidade | Achado | Resolução |
| --- | --- | --- | --- |
| canonical_trace | critical | Nenhum player entrega integralmente trace.jsonl, tool-calls.jsonl, sources.yaml, claims.yaml, report.md, cost-latency.yaml e replay-manifest.yaml. | Criar contrato SINKRA DeepResearchRunner antes de absorver runtime. |
| claim_provenance | critical | Vários projetos produzem relatório antes de claims verificáveis. | Obrigar claims.yaml com source_ids e checagem claim-source. |
| private_data_boundary | high | Projetos private-KB têm padrões úteis, mas não resolvem isolamento L0-L4/SINKRA por padrão. | Adapters com classificação de fonte, redaction e fixtures sintéticas. |
| judge_drift | high | Benchmarks com LLM judge não pinam suficientemente prompt/model/raw outputs. | Judge manifest versionado e raw judge outputs anexados. |
| license_uncertainty | high | Alguns players têm licença ausente, metadados divergentes ou dependências proprietárias. | Clean-room patterns e revisão jurídica antes de vendorizar. |
| cost_visibility | medium | Custo e latência raramente aparecem como artefatos obrigatórios. | cost-latency.yaml obrigatório por run. |
