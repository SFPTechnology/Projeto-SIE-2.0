# F11 — execução integral dos bloqueios de integração, recuperação e resiliência

**Base:** `feat/f11-qa-integrado`, SHA remoto `1f563570b88892f6ea8791929122e5ab03269941`; F10 preservada em `540f2c8e7e61a1efb6bf71abcedc8768d7086914`. **Destino:** mesma branch F11, sem merge em main, deploy ou alteração de produção. Story: `docs/stories/story-SIE-F11-QA-INTEGRADO.md`.

## Equipe e ordem

| Responsável | Entrega | Gate verificável |
|---|---|---|
| Integração de domínio F09/F10 | Contrato persistido de origem, projeto/revisão/run, hashes F06/F07/F08, bloqueio de mistura ou obsolescência, documento rastreável | Teste único da mudança de carga ao documento, recálculo e invalidação; nenhum cálculo normativo inferido |
| Persistência/recuperação | Backup offline de SQLite e todas as raízes referenciadas, restore isolado e CLI | Testes de múltiplas raízes, integridade, corrupção, symlink, caminho hostil, escrita concorrente e recusa de overwrite |
| Resiliência/desempenho | SLO local explícito, benchmark reproduzível e cenários de erro/concorrência | Medições com ambiente, amostra, limite e resultados, sem extrapolar para produção |
| QA-01 arquitetura | Revisão independente da ponte, invariantes, regressão e matriz de AC | Parecer com evidência por SHA e achados corrigidos |
| QA-02 engenharia | Revisão dimensional/normativa e bloqueios de aplicabilidade | Parecer separado, sem aprovação profissional fictícia |
| QA-03 segurança/UX | Revisão de restore, isolamento, navegador e limites do modelo local | Parecer separado, E2E real e testes negativos |
| DevOps | Gates AIOX/API/Chromium e publicação da branch | Três workflows concluídos com sucesso no mesmo SHA, árvores verificadas |

## Execução

1. Congelar baseline e requisitos; testes de falha para cada lacuna antes da implementação. Agentes trabalham em arquivos distintos e integram em uma única árvore.
2. Concluir contrato F09→F10 preservando os motores e seus limites. Gerar artefato somente com fonte e revisão coerentes; mudanças materiais tornam a saída obsoleta até novo run.
3. Criar pacote offline consistente de banco e arquivos, manifestos de hash e restore para destinos novos. Recusar estados em preparação, raízes ausentes, symlinks e alterações durante a cópia.
4. Medir concorrência, massa de dados, falhas e latências em ambiente local; definir SLOs para esse ambiente e registrar percentis/amostra. Não confundir SLO local com produção.
5. Rodar suíte API integral, casos históricos F00, npm lint/typecheck/test/build e E2E Chromium; corrigir causa de falhas e repetir o escopo afetado.
6. Realizar QA-01/02/03 em pareceres separados, atualizar matriz, story, estado canônico e relatório. Marcar F11 DONE somente se todos os critérios aplicáveis tiverem prova e nenhum impedimento técnico; liberação profissional/produção continua separada.
7. Publicar checkpoint na branch F11 e conferir CI no SHA exato. Qualquer edição posterior requer nova verificação do SHA resultante.

**Política de falha:** se faltar fonte profissional, instalação física ou autorização para produção, registrar pendência própria sem falsear evidências; avançar nos trabalhos independentes. Não usar dados reais de produção nem alterar expectativas de teste para mascarar defeitos.
