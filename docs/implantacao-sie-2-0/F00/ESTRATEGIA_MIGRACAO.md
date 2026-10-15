# Estratégia de migração reversível — F00

Baseline `8d86db26f5e8675eaced4638af14bd84019e15e7`. Tarefa 00.07. **Escopo desta entrega:** classificação e roteiro técnico, sem migrar aplicação, tabelas ou dados. Proposta preparada pelo inventário e submetida ao @architect e QA; o parecer é registrado separadamente. As classificações não constituem ordem de executar fases posteriores.

## 1. Contratos a conservar

- Entradas/unidades e saídas dos 37 IDs em `MATRIZ_PRESERVACAO_FUNCIONAL.csv`; falhas observadas e cenários golden vinculados ao SHA original. Novo comportamento não recebe equivalência por existir arquivo com nome parecido.
- Gate `status_liberacao` permanece BLOQUEADO/PENDENTE e nenhuma flag de cliente concede aprovação. EDP mantém `liberado_para_padrao_entrada=false`; catálogo e regra interpretativa têm estados de fonte distintos.
- HTTP rotas, campos, códigos 401/404/409/422/503; CLI comandos, JSON stdout e códigos 0/2/3/4. Integrações existentes exigem contrato de compatibilidade antes de alterar nomes ou formatos.
- UUID, `revisao_esperada`, conflito sem sobrescrita, integridade JSON, limite de tamanho, gravação transacional e log de ações locais. O log não é backup de versões completas.
- Estado canônico em `docs/sie-orchestrator/ORCHESTRATOR_STATE.json`; JSON de scheduler é fila/estado, não executor. Estados AIOX permanecem separados.
- `NOR-01`, `NOR-02`, `EDP-01` e `SEC-01` não são encerrados pela F00. Limitações normativas, identidade de produção e aprovação de dados continuam gates próprios.

## 2. Classificação por comportamento

| Decisão | LEGACY-ID | Justificativa e condição de troca |
|---|---|---|
| **Manter** | 001–002,007,010–020,031 | Código identificado e contratos testáveis; baseline não demanda reescrita. Manter significa reter a implementação atual com limites, não homologar engenharia ou segurança de produção |
| **Encapsular** | 003–006,008–009 | Isolar primitivas determinísticas e catálogo preservando API; casos ENG-001/002 permanecem explicitamente caracterizados até correção versionada e aprovada. Sem troca de fórmula automática |
| **Encapsular após recuperar dependências** | 021–022 | Otimizador/schema TS incompletos. Recuperar tipos/validadores/consumidores e configurar runner local sem conexões externas; não equiparar C1-C6 ao seletor Python |
| **Encapsular como legado inativo** | 024–028 | SQL e pacotes gráficos ficam retidos; dependências e integração ausentes impedem afirmar preservação funcional. Qualquer adapter requer teste em ambiente descartável |
| **Substituir somente após projeto de migração** | 023 | SQL normativo necessita correção sintática, cadeia de schema, RLS e dados conferidos. Preservar o arquivo original e desenvolver evolução nova, sem editar silenciosamente a baseline |
| **Substituir/implementar após recuperar contrato** | 029–030,032–037 | Não há runtime integrado identificado. Primeiro buscar fonte original/casos aprovados; depois classificar port/refatoração/implementação nova com ausência explicitada |
| **Refatorar** | Nenhum neste momento | Sem benefício comprovado que justifique alterar runtime na fase de caracterização; reavaliar por story e golden após F00 |
| **Aposentar** | Nenhum neste momento | Sem evidência suficiente de não uso/equivalência. Não excluir ZIP, código, SQL, testes, normas ou documentos históricos |

Os itens 024–026 não estão aptos a publicação: políticas amplas e FKs faltantes devem ser tratadas no projeto futuro de persistência. Preservar o arquivo não significa manter uma política insegura num banco de produção.

## 3. Roteiro controlado por evidência

| Ordem | Trabalho | Prova de saída | Rollback/limite |
|---|---|---|---|
| 1 | Fixar SHA/árvore/versões, identificar contratos e lacunas | Baseline e matriz, hashes, testes e logs efetivos | Não alterar main/publicado; alterações F00 apenas docs/testes/manuais necessários |
| 2 | Recuperar código TS original e cadeia SQL sem assumir sua presença | Paths/imports completos e executáveis; dados de referência próprios; lacunas resolvidas por evidência | Reter módulos atuais; arquivo recuperado não substitui runtime automaticamente |
| 3 | Encapsular um contrato por story, via CLI/biblioteca antes de UI | Mesmas entradas/saídas/erros ou diferença formalmente versionada; golden antigo e novo em paralelo | Desativar adapter novo e voltar ao código anterior; manter os dados em formato compatível |
| 4 | Conferir fontes/casos de engenharia, incluindo limites e anomalias | QA-02 por regra/unidade; aprovação de dados separada de regressão | ENG-001/002 não podem ser corrigidos ajustando fixtures para ficar verde; manter caso antigo e registrar expectativa corrigida em teste distinto |
| 5 | Projetar persistência com identidade/ACL e esquema completos | Backup e teste de restauração; constraints/RLS por identidade; teste de autorização em instância descartável | Código rollback não desfaz esquema ou dados: usar cópia/reversão de migração testada e janela definida |
| 6 | Integrar UI e pacotes gráficos a contratos já estabilizados | E2E calcular/salvar/reabrir/recalcular; DXF/SVG/relatório verificados quando implementados | Ativação opt-in/adapter reversível; nunca inferir integração por arquivo ZIP ou exemplo |
| 7 | Executar QA/regressão e decidir mudança de uso | Pareceres separados; contrato, dados e escopo aprovados | Sem merge/deploy/migração real nesta fase; produção depende do marco/autorização próprio |

Esse roteiro não escolhe novas bibliotecas além das observadas; as bibliotecas propostas em plano histórico não se tornam dependências por constarem em documento.

## 4. Equivalência e desvios conhecidos

Comparar entrada normalizada, unidade, precisão, arredondamento, saída e erros no SHA antigo e no adapter candidato. Excluir de igualdade apenas campos inerentemente variáveis (timestamps, UUID gerado e tempo de execução) quando houver normalização documentada. Nunca normalizar resultado elétrico, revisão ou status de liberação para esconder divergência.

**ENG-001:** o pipeline passa capacidade corrigida arredondada do condutor ao seletor de disjuntor. Preservar o cenário e sinalizar que Ib=19,99 A, Izbase=20 A e fator=0,99975 produzem Iz real=19,995 A, enquanto a decisão pode comparar com 20,00 A. Futuro fix exige memória de cálculo independente, sem autoaprovar o resultado legado.

**ENG-002:** a regra EDP atual não bloqueia modalidade U quando a entrada declara carga trifásica. Manter esse caso como limite conhecido e testar uma regra corrigida em mudança futura, após confirmar aplicabilidade. O campo de liberação permanece false.

As lacunas TS, SQL, unifilar, demanda e demais comportamentos não encontrados são exceções formais da matriz, com status `LACUNA_FORMAL`. Uma exceção documenta ausência e retenção; não aprova equivalência de algo não executável.

## 5. Plano de rollback e proteção de dados

**Fonte e código:** manter branch isolada e SHA de referência; reaplicar/remover apenas os commits da story autorizada. Reverter código de adapter restaura o contrato antigo somente quando o formato de dados continuou compatível; não tocar main nem executar reset destrutivo no trabalho compartilhado.

**SQLite:** antes de qualquer futura migração, parar escritores ou usar backup consistente do SQLite em arquivo separado; preservar base e log juntos. Testar restauração em caminho temporário com CLI/GET carregar, revisão esperada, conflito 409 e histórico. Comparar dados antes/depois. `historico()` não restaura conteúdo anterior. Não copiar só um arquivo enquanto há gravação sem método de consistência validado.

**Postgres/Supabase:** não aplicar as cinco migrations na F00. Antes de mudança futura, obter cadeia completa e baseline do schema, backup/restauração em instância descartável e ensaio das políticas por identidade; definir downgrade/restauração específica para mudanças de dados. Reverter commit de SQL não reverte DDL nem restaura registros de produção.

**Estado operacional:** scheduler.save_state usa revisão otimista e replace atômico, sem lock interprocesso. Um escritor por workspace; cópia do estado/histórico antes da transição e validação do snapshot restaurado. Restaurar estado não significa reexecutar nem desfazer tarefa externa.

**Dados de fonte:** normas/extratos/ZIPs são ativos de referência; preservar hashes, edição, proveniência e exemplares originais. Rótulo VERIFICADO/CONFIRMADO legado e hash não são autorização normativa; dados novos só substituem versão mediante trilha de revisão.

## 6. Critérios para aprovação técnica da estratégia

1. Todos os IDs possuem manter/encapsular/substituir ou lacuna formal, sem aposentadoria automática.
2. Contratos HTTP/CLI/SQLite e gate normativo foram explicitamente preservados.
3. Reversão de código é separada de restauração de dados/schema; ensaio de restauração é requisito antes da migração futura.
4. AIOX e scheduler não são confundidos com motores elétricos nem executor contínuo.
5. ENG-001/002, dependências ausentes e bloqueios normativos/produção não são encerrados por teste golden.
6. Aprovação desta estratégia vale apenas para a classificação/roteiro F00. Não libera execução da migração, engenharia profissional, main, produção, custo externo ou nova fase sem seus gates.

Parecer de arquitetura e evidências QA devem ser vinculados no relatório F00. **Status de revisão: APROVADO exclusivamente no escopo técnico da tarefa 00.07**, conforme `PARECER_ARQUITETURA.md`. A atualização desta nota não altera as decisões, os contratos nem os procedimentos do documento revisado.
