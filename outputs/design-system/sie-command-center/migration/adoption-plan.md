# Plano de adoção lado a lado

O design atual deve permanecer operante. Esta proposta só entra no produto por uma futura story aprovada e por incrementos reversíveis.

## Estratégia

### Fase 0 — validação do conceito

- Revisar o protótipo com projetistas e responsáveis técnicos;
- Validar taxonomia dos módulos;
- Testar três tarefas críticas: localizar pendência, rastrear um valor e seguir para o próximo módulo;
- Registrar baseline de tempo, erros e compreensão;
- Não alterar a aplicação.

### Fase 1 — camada de tokens

- Criar namespace `--sie-*` mapeado para primitives Carbon/Radix;
- Adicionar testes de contraste e snapshots;
- Não trocar componentes nem rotas;
- Rollback: remover a importação da nova camada.

### Fase 2 — shell opt-in

- Implementar `EngineeringShell` sob feature flag;
- Manter `AppShell` atual como padrão;
- Reutilizar as rotas existentes dentro do novo shell;
- Comparar navegação, reflow e desempenho;
- Rollback: desativar feature flag.

### Fase 3 — um template piloto

- Selecionar uma rota com alta frequência e risco moderado;
- Aplicar `ListInspectorTemplate` ou `ParametersResultsTemplate`;
- Manter contratos de API e domínio intactos;
- Testar teclado, leitor de tela, zoom e regressão visual;
- Rollback: rota volta ao template original.

### Fase 4 — consolidação por módulo

- Migrar um agrupamento por vez: Entrada, Dimensionamento, Documentação;
- Remover hardcodes apenas após cobertura de tokens;
- Não misturar migração visual com mudança de regra normativa;
- Publicar changelog e guia de transição.

### Fase 5 — descontinuação do legado

- Somente após paridade funcional, métricas estáveis e aprovação;
- Remover estilos/componentes sem consumidores;
- Atualizar Storybook/pattern library;
- Manter histórico das decisões de consolidação.

## Gates por fase

- Story e acceptance criteria aprovados;
- Rastreabilidade para requisito/story existente;
- Zero regressão nos contratos CLI/API;
- `npm run lint`, `npm run typecheck`, `npm test`, `npm run build`;
- WCAG 2.2 AA para o fluxo migrado;
- Teste em 320 px, 768 px, 1280 px e zoom 200%;
- Feature flag e rollback testados;
- File List e checklist da story atualizados.

## Métricas sugeridas — precisam de baseline e aprovação

- Tempo para localizar um módulo;
- Tempo para identificar causa e próxima ação de uma pendência;
- Taxa de retorno ao módulo anterior por perda de contexto;
- Erros de interpretação de estado;
- Uso de busca/atalhos por especialistas;
- Abandono de fluxo;
- Volume de suporte por módulo.

Nenhuma meta numérica é definida sem pesquisa e aprovação de produto.

