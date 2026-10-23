# Story SIE-F10 — Artefatos gráficos e documentação rastreável

**Estado:** IN_PROGRESS (não homologado)
**Branch de desenvolvimento:** `feat/f09-concessionarias-especializadas`
**Fonte:** `docs/implantacao-sie-2-0/F10/PLANO_IMPLEMENTACAO.md`, `RELATORIO_EXECUCAO.md` e critérios AC-10.01–AC-10.10 do orquestrador.
**Restrições:** preservar main, sem deploy, sem migração produtiva ou homologação normativa.

## Objetivo
Conectar representação e exportação F10 a snapshots verificáveis, à revisão e execução de cálculo; detectar obsolescência e bloquear inconsistências, sem criar dados técnicos fictícios.

## Critérios de aceite
- [ ] AC-10.01: artefatos persistidos identificam projeto, revisão, cálculo, regras e template; snapshot e hashes verificáveis; integridade fail-closed
- [ ] AC-10.02: planta com origem autorizada, escala/unidade controlada, geometria explícita e vínculos com elementos
- [ ] AC-10.03: símbolos versionados, legenda e origem
- [ ] AC-10.04: diagrama derivado de grafo; circuitos do quadro correto, sem ligações fictícias
- [ ] AC-10.05: quadros de cargas consistentes com revisão e execução
- [ ] AC-10.06: quantitativos com proveniência e sem comprimentos criados
- [ ] AC-10.07: memorial técnico com cálculos/fórmulas somente se rastreáveis
- [ ] AC-10.08: formatos obrigatórios e verificações de integridade; PDF conforme capacidade aprovada
- [ ] AC-10.09: prévia, impressão, navegação, segurança visual e acessibilidade
- [ ] AC-10.10: reconciliação entre modelo, artefatos e cálculos com bloqueio de divergência crítica
- [ ] QA-01/02/03 formais e CI aplicável efetivamente aprovados

## Unidade executiva priorizada — W1
- [ ] Produzir pacote de exportação que guarda o snapshot canônico e um manifesto com sha256 por arquivo
- [ ] Publicar pacote no sistema de arquivos local de maneira atômica e sem sobrescrita
- [ ] Implementar verificação de conteúdo e estado de obsolescência quando a origem atual for conhecida, sem declarar atualidade na ausência de origem
- [ ] Cobrir adulteração de snapshot/exportação, mudança de dependência, revisão incompatível e não sobrescrita
- [ ] Corrigir isolamento de painéis no unifilar e cobrir com teste adversarial

## Lista de arquivos e verificações
A atualizar após cada incremento, com referências aos commits, workflow runs e limitações.

## Limite de aceite
Testes automatizados não representam homologação normativa nem substituem revisões formais. Qualquer aceite remanescente conserva seu estado pendente até comprovação.