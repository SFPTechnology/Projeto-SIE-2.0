# Checkpoint P2 — contract_discovery

- Run ID: `sdc-yolo-dep-ux-01-2026-08-03T01-28-52-096-03-00`
- Manifest fingerprint: `c49c60abbdc9887c9b6c06764d21cf8b3520301ec8d301e452855e3ee20b7580`
- Responsável: `@ux-design-expert`
- Resultado: `BLOCKED`
- Estado terminal proposto: `worktree_blocked`

## Contrato inventariado

- Rota: `src/routes/projetos.$projetoId.tsx` consulta dependências e já fornece estados de loading, erro e vazio; renderiza `EstadoDependenciasResumo` e `TabelaDependencias`.
- Agregado: `src/domain/agregado/dependencia-agregado.ts` fornece ID, projeto, versão, estado, entrada, resultado opcional e timestamps.
- View model limpo: `src/components/app/dependencias-table-model.ts` mapeia nome, tipo/categoria/dimensões, iluminação, tomadas, cargas, atualização, estado, pendências, busca, filtros e paginação.
- `Calculada` deriva de `dep.estado === CALCULADA`; o rótulo é mantido no view model e em `StatusBadge.tsx`.
- `VERIFICAR` deriva dos status de área, perímetro, iluminação, tomadas e cargas adicionais, além de pendências/diagnósticos; o view model já consolida essa condição em `possuiPendenciasOuAlertas`.
- Busca e filtros atualmente suportados: estado, escopo (todas, pendências/alertas, com cargas, sem resultado) e paginação de seis itens.
- Ações protegidas confirmadas:
  - `Detalhe` → `setDetalhe(dep)` / `DependenciaDetalheModal`.
  - `Calcular` → `api.calcular(dep.id, autorAtual())`.
  - `Historico` → `setHist(dep.id)` / `HistoricoPanel`.
  - `Duplicar` → mutation que chama `api.criarDependencia(projetoId, entrada copiada, autorAtual())` e invalida cache.

## Sobreposição de worktree

- `src/components/app/TabelaDependencias.tsx` está modificado por outra frente (`+62/-8` no diff observado) e contém a mutation/botões de `Duplicar`, uma ação explicitamente protegida e obrigatória para o redesign.
- `src/styles.css` está modificado por outra frente (`+470/-15` no diff observado), contém os estilos `deps-*` necessários ao redesign e alterações amplas de design system/queda de tensão fora do escopo.
- `VisaoGeralDependenciasModal.tsx` também está sujo, embora seja superfície auxiliar e não o bloqueio primário.

## Decisão

Não existe separação segura para implementar P3/P4 sem tocar trabalho local preexistente e protegido. A execução não pode criar um baseline limpo, resetar, guardar, mover ou editar alterações de terceiros. É necessária reconciliação ou atribuição explícita de propriedade dos arquivos antes de uma nova execução.

- Próximo estado: `worktree_blocked`
