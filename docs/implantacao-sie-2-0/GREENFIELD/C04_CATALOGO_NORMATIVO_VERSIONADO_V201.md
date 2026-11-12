# C04 — Catálogo normativo versionado, status conservador

**Fonte em uso:** `restructuring/apps/api/sie_api/data/normative_registry.json` — registros com `id`, `revision`, `edition`, localidade quando aplicável, `official_url`, `license_status` e `verified_data`. O histórico traz NBR 5410/5419, NR-10, EDP-SP; valores/versionamento declarados no repositório **não são homologação**.

**Gateway:** `v201_c_normative.catalog_snapshot()` valida unicidade ID+revision, calcula SHA256 de JSON canônico; `resolve_rule(rule_id,revision,uf,distributor)` rejeita regra não encontrada, versão ambígua e localidade sem comprovação. Todo registro sem validação retorna `EVIDENCE_PENDING`; registro local `APPROVED` sem verificação confiável externa retorna `REVIEW_REQUIRED` (anti-falsificação); revogado => `REVOKED`. O catálogo não confere conformidade em nome de normas técnicas.

**Pendências de engenharia:** P03 proteção; P06 condições de aplicação; Rca/XL para impedâncias; fonte/licença/tabela EDP versionada e vigência por célula. Ausência de parâmetros mantém C05 em pendência. Não atribuir `conforme` a cálculo que apenas soma cargas em VA.

**Invalidar resultados:** todo output C05 registra hash do catálogo; alterações exigem novo cálculo e novo hash, com preservação do histórico anterior. Revisões de projeto devem ser clonadas em DRAFT antes de edição. Verificação de invalidade em persistência remota fica no gate E02/E03.
