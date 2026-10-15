# Parecer de lacunas e plano de desbloqueio — F01

Data: 2026-10-15. Baseline confirmada: F00 **DONE** no PR #2; 37 comportamentos, 34 cenários golden, 134 testes de API (35 golden inclusos), 3 Chromium e QA3 F00 aprovados. F00 não depende de homologação completa de normas.

## Pendências impeditivas

| ID | Severidade | Tarefa | Achado | Resolução verificável |
|---|---|---|---|---|
| F01-NOR-01 | CRÍTICA | 01.03/04 | Apenas 6 artefatos de NBR/EDP possuem hashes; edições, origem, licenças e linhas não confrontadas; NBR 5419 2026 sem texto autorizado | Obter fonte primária/licença/escopo e dupla conferência, assinando matriz célula a célula |
| F01-NOR-02 | ALTA | 01.07 | NR-10: Portaria MTE 737/2026 nova redação geral em 01/06/2027, exceção para instalações existentes exige estudo | Documentar requisitos de transição por situação e data, com parecer técnico |
| F01-ENG-01 | ALTA | 01.08 | Nenhum caso normativo **numérico** com valor esperado independente e fonte primária homologada | Fixtures numéricas independentes, precisão/limites e conferentes |
| F01-DAT-01 | ALTA | 01.06 | Metadados versionados, mas snapshots imutáveis dos projetos e trilha de mudanças ainda não persistidos | Arquitetar storage, migrar apenas banco descartável após autorização, testar histórico e rollback |
| F01-SEG-01 | MÉDIA | 01.09 | A API F01 rejeita flags e retorna bloqueios; não cria identidade de produção nem privilégio de aprovador | Testar autorizações e tenant boundary na fase própria, manter liberação fechada |
| F01-UX-01 | MÉDIA | 01.09 | UI atual não consulta/mostra lista detalhada de F01; somente endpoint explicável | Adicionar estado legível e E2E de interface posteriormente |
| F01-F00-RISK | ALTA | legado | Iz arredondado, aplicação EDP incompleta, SQL/RLS e tabela personalizada ainda abertos na F00 | Corrigir nos incrementos específicos e conservar golden de caracterização |

## Trabalho estrutural permitido

Disponibilizar catálogo **de metadados**, API de consulta contextual, teste de exclusão e bloqueio, metadados de edição e rastreabilidade sem importar valores normativos. O sistema deve continuar sinalizando `liberado_para_uso_normativo = false`; o código novo não altera cálculos legados, banco, main ou produção.

## Condição de conclusão

F01 somente DONE quando as tasks essenciais, conferências necessárias à seleção de regras, snapshots históricos, testes integrados e QA-01/02/03 aplicáveis estejam aprovados. Caso contrário, manter `BLOCKED` com evidências de implementação parcial. **F02 não liberada.**
