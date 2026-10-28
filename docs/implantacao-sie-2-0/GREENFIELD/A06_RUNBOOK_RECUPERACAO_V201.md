# A06 — Preparação de recuperação / sem restore físico no Bloco A

**Estado:** PROCEDIMENTO DOCUMENTADO; ENSAIO NÃO EXECUTADO. O restore real é gate de E04, antes de E06 GO.

## Para qualquer DDL futura no Supabase existente
1. Confirmar `project_ref=fozrymsidnaxmuvxxfhh`, organização `takynlbrhcdenqsrxhps`, saúde e versão PG.
2. Comparar schema/migration history com baseline assinado A01; diferenciar arquivos `restructuring/supabase/migrations` de raiz legada.
3. Exigir autorização de DDL **específica**; listar tabelas impactadas, locks/intervalos e rollback/forward-fix. Não realizar `db push` indiscriminado.
4. Verificar backup disponível real (snapshot, dump ou PITR) com administrador; não afirmar que backups existem sem consultá-los. Descrever retenção real e separar cópia SQL de objetos do Storage.
5. Executar migration aditiva versionada apenas quando autorizada; conferir schema, grants, RLS, índices e migration history em leitura imediatamente depois.
6. Se surgir falha, parar novas escritas, registrar log e hash, avaliar transação aplicada vs. parcial, preparar forward-fix/compensação revisada. Não executar DROP destrutivo para reverter sem decisão específica.
7. Para pré-produção E04, restaurar em recurso seguro apropriado; conferir contagem, FKs, RLS/grants, índices, manifestos, checksums e conteúdo de Storage conforme aplicável; medir RPO/RTO reais.

## Situação em 28/10/2026
- GF02 existente: nove tabelas sem dados operacionais no checkpoint.
- Backup disponível: **NÃO VERIFICADO**.
- Restore ensaiado: **NÃO**.
- RPO, RTO: **NÃO MEDIDOS**.
- Storage integrado: **NÃO**.

**Conclusão:** documentação pode apoiar GA de desenvolvimento sob revisão 2.0.1; não autoriza mudança de produção nem E06 GO.
