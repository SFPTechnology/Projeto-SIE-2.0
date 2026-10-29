# C03 — ADR do domínio elétrico relacional / candidato V2.0.1

**Estado:** PROPOSTO / não aplicado ao Supabase. Baseline GF02 + A03/A04/B04 pendentes remotamente. Arquivo candidato: `C03_SCHEMA_CANDIDATE_V201.sql`.

## Decisão arquitetural
Preservar os seis vínculos básicos GF02 e adicionar entidades referenciais ao invés de guardar todo o domínio em `jsonb` opaco:
- `sie_panels` (quadros, modo de fase, aterramento), `sie_feeders` (origem/destino, comprimento, PE/neutro, material), `sie_circuit_technical` (potência/fator, método, bitolas, dispositivos);
- `sie_room_benches` (bancadas por cômodo), extensão controlada de `sie_rooms` e `sie_loads`;
- `sie_floorplans`, `sie_floorplan_vertices`, `sie_graphical_bindings` (escala explícita, relação gráfico↔ID, geometria poligonal); 
- `sie_legacy_results` (somente histórico não homologado), `sie_distributor_overrides` (justificativa e fonte), `sie_normative_rule_versions` (edição, localidade, status e evidências).

## Integridade e fronteiras
FKs compostas `(id,project_id,revision_id)` onde cabível; RLS em todas as tabelas novas; `anon` sem acesso; `authenticated` limitado à leitura owner-only; inserções confiáveis destinadas exclusivamente a backend protegido, sem exposição de serviço privilegiado no navegador. Aprovação de catálogo exige evidência e autoridade verificáveis; simples JSON nunca a gera (C04).

## Riscos e pendências verificáveis
- `C03_SCHEMA_CANDIDATE_V201.sql` é **candidato**, não migration canônica com ID nem DDL aplicada ao banco remoto. O perfil de uso em produção depende de autorização específica, PG17 isolado, freeze, read-back, backup e E02–E06.
- Modelo de dimensionamento completo ainda não opera sem topologia, resistência/reatância e método/catálogo aprovados; não preencher parâmetros por suposição.
- Descrever e validar imutabilidade dos novos filhos de revisões `SEALED` por trigger PostgreSQL e cobertura de clone/copy antes de permitir C03 PASS amplo. A estrutura atual de C03 somente propõe tabelas/relações.
- `APPROVED` no cadastro não equivale a assinatura profissional; exigir E03.
