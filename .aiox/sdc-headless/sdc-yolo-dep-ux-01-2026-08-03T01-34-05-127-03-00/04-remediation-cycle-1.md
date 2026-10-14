# Checkpoint P4 — remediação (cycle 1)

- Run ID: `sdc-yolo-dep-ux-01-2026-08-03T01-34-05-127-03-00`
- Responsável: `@ux-design-expert`
- Resultado: `PASS — aguardando P5`
- Escopo da correção: somente `src/components/app/__tests__/status-badge.test.tsx`.
- Correção aplicada:
  - removida a expectativa da superfície legada `Tabela de dependências`;
  - adicionadas expectativas para a superfície atual `Dependências do projeto`, resumo `Dependências`, estado `Calculada` e os rótulos `Detalhe`, `Calcular`, `Historico`, `Duplicar`.
- Proteções verificadas:
  - nenhuma implementação, handler, contrato ou estilo foi alterado;
  - a correção não toca alterações preexistentes fora do arquivo de teste.
- Próximo estado: `local_quality` (cycle 1).
