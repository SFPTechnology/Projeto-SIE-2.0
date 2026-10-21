# F04 — Reconstrução do cadastro preliminar
Data: 21/10/2026. Estado: VALIDATING. Branch feat/f04-cadastro-cargas, base F03 62d58a22b8f66a8334720b703bf1521f56e55e45.
A implementação local anterior 1ddc28f foi removida pela manutenção do ambiente antes de publicação. Esta é uma reconstrução verificável; não se atribuem ao novo código os resultados anteriores.

Tasks 04.01–04.09: hierarquia edificação/pavimento/ambiente, pontos ILUMINACAO/TUG/TUE, dados de placa separados de P/Q/S, origem declarado/estimado, grupos/tags, dados incompletos, totais decimais por projeto/ambiente/pavimento, arquivamento explícito, edição e desfazer. CLI load_survey_cli, API opt-in F03 e tela levantamento.html. Contrato em CONTRATO_DEMANDA.md, manual em restructuring/apps/web/levantamento-manual.html, fixture levantamento-demo.json. Nenhum merge, deploy, migração real ou alteração da main.

## Testes observados
- API antes da última correção FP: 573 passed (22 F04), 1 aviso Starlette existente.
- F04 após FP: 23 passed.
- F00: 34 casos, fixture intacta.
- AIOX lint/typecheck/test/build: PASS após instalar dependências do lock; 18 testes.
- JavaScript syntax e diff check: PASS.
- Chromium local: EM EXECUÇÃO. CI: NÃO EXECUTADO ainda.

## Revisões críticas
QA-01 APROVADO no escopo local: armazenamento aditivo, conflitos, referências, histórico e arquivamento exercitados.
QA-02 APROVADO no escopo preliminar após corrigir divergência entre FP declarado e P/S (tolerância absoluta 0,01). P/Q/S não se somam entre si; metadados de placa/atribuição não duplicam totais.
QA-03 PENDENTE navegador: correções implementadas para descarte de rascunho, gravações simultâneas, valores padrão ao editar e visibilidade de origem/unidades.
Os pareceres são revisões computacionais; não substituem validação profissional.

## Limites
Regras mínimas permanecem PENDENTE_FONTE_VALIDADA conforme fase; nenhuma fonte digitada concede validação normativa. Soma de S é aritmética, não vetorial. Dados ausentes são explicitados; não há motor de demanda nem conversão automática para circuitos F02. Identidade/RLS em produção permanecem fora do escopo local herdado da F03. CodeRabbit CLI indisponível. Passagem F05 ainda não declarada até finalizar navegador e CI.
