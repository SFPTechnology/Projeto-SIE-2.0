# Inventário e matriz de persistência
Base: branch F02, SQLite local; não foi acessado banco real nem aplicado SQL Supabase legado.

|Atual|Destino F03|Verificação|
|---|---|---|
|projetos: UUID, JSON, revisão, atualizado_em|criado_em, excluido_em, índice ativos|upgrade/downgrade, tombstone|
|versoes_projeto: chave projeto/revisão, digest, timestamp|preservado imutável|replay e restore|
|snapshots_normativos e eventos_snapshot_normativo|preservados, NAO_HOMOLOGADO|regressão F01/F02|
|ensaios_calculo: FK versão, digest, índice circuito|preservado imutável|regressão|
|eventos_auditoria|autor LOCAL_OWNER para novas operações; LEGACY_UNKNOWN para antigas|sem identidade arbitrária de cliente|
|schema_migrations|versão 1|transação BEGIN IMMEDIATE|

DDL anterior continua sendo bootstrap legado idempotente; migração F03 é aditiva e versionada. Inicializar o repositório não prova banco histórico migrado: a tabela schema_migrations registra aplicação real. created_at de dados antigos é a primeira data disponível (atualizado_em), não data original comprovada. Revisão administrativa de arquivamento não cria snapshot de conteúdo artificial. Histórico anterior continua consultável com token local. Sem rota HTTP de exclusão. Nenhuma alteração em dados normativos ou topologia do F02.
