# C19 — Decisão de escopo: SIE 2.0 Greenfield sem importação legada

**Data:** 04/11/2026  
**Decisão expressa do responsável:** concluir o SIE 2.0 como **sistema novo**, **sem importar inicialmente os cinco projetos** já existentes no SIE original.

## Objetivo e efeitos vinculantes

- **SIE 2.0:** construir e homologar integralmente módulos, fluxos, autenticação, persistência, cálculos, documentos, UX e segurança no banco de destino `fozrymsidnaxmuvxxfhh` com projetos **novos** e dados de ensaio isolados.
- **SIE original:** manter repositório `SFPTechnology/Projeto-SIE` e origem Supabase `hlbksclcandbsyqrsbmx` em **somente leitura**, sem excluir, substituir, alterar ou transferir os projetos automaticamente.
- **Migração dos cinco projetos:** registrar na fila de evolução **opcional e futura**, fora do escopo obrigatório do Gate GC e de liberação do sistema novo. Evidências históricas C01/C02/C07 permanecem conservadas para eventual retomada; antigas flags `MIGRATE` em inventário histórico não representam ordem de execução atual.
- **Migrations de SCHEMA A03/A04/B04/C03:** permanecem necessárias ao banco do SIE 2.0, com testes, readback e aprovação de segurança. Não são sinônimo de importação de projetos antigos.
- **Auth novo:** funcionamento de sessão e isolamento A/B é obrigatório para o produto novo, mas vincular os cinco IDs de projeto legado a um titular não é exigência da liberação greenfield.
- **Engenharia elétrica:** avaliações normativas E01–E11 e aceite profissional humano C13 não são dispensados.
- **Segurança de dados:** a decisão do titular de não realizar backup remoto C17 continua em vigor; logo não se pode promover o GO de DDL enquanto não houver salvaguarda alternativa aprovada, recuperável e comprovada. A exclusão da migração antiga não equivale à autorização para operar sem recuperação.
- **Ambientes:** sem custos extras, sem testes no PC do usuário, sem alteração de `main`, F12, SIE original ou produção.

## Matriz de critérios de entrega

| Bloco | Requerido para SIE 2.0 greenfield? | Evidência para liberação |
|---|---|---|
| A03/A04/B04/C03 (schema do SIE novo) | SIM | migrations aplicadas na homologação, readback, teste em mesma versão/ambiente |
| Autenticação e RLS multiusuário | SIM | testes reais de autorização A/B, sessão, revogação e proteção de dados |
| Módulos C03–C05, E01–E11 e regras normativas | SIM | valores independentes, fontes autorizadas e parecer técnico |
| CI de API, E2E, AIOX e PG17 | SIM | cinco workflows PASS no SHA final |
| Aceite elétrico humano C13 | SIM | parecer assinado e versão/escopo rastreáveis |
| Recuperação/rollback antes de DDL remoto | SIM | evidência operacional de meio recuperável/alternativa segura aprovada |
| Importação dos cinco projetos legados | **NÃO** | trabalho futuro independente se solicitado |
| Backup, snapshot e corte do **banco antigo para ETL** | **NÃO, nesta entrega** | só se a migração do legado voltar ao escopo |
| 5/5 vinculações Auth dos projetos antigos | **NÃO, nesta entrega** | só se a migração do legado voltar ao escopo |
| Preservação do SIE original | SIM | nenhuma escrita no legado nem alteração do repositório original |

## Encaminhamento

1. Ajustar contratos e testes do Gate GC para retirar exclusivamente os itens relacionados à importação legada.
2. Continuar QA e implementação na branch C usando projetos sintéticos/novos e provas independentes.
3. Reavaliar bloqueios restantes de DDL, Auth e homologação sem confundi-los com a migração dos cinco projetos.
4. Somente declarar `GC=PASS` quando os critérios efetivos de entrega greenfield forem atendidos e aceitos — nunca por mudança de flags.

**Situação nesta decisão:** escopo greenfield **ratificado**; implementação completa e GC ainda **não liberados**; nenhum banco remoto alterado por esta formalização.
