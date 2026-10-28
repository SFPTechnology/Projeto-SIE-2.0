-- A03: CANDIDATO DE REVISAO, NAO E UMA MIGRATION APLICADA.
-- SIE 2.0 V2.0.1 / somente codigo na branch de desenvolvimento.
-- Fonte: 13 FKs e 26 indexes no read-back; quatro FKs sem prefixo apropriado.
-- Nunca executar diretamente contra PROD sem autorizacao especifica e revisao de plano.
-- Sem DROP, sem CREATE TABLE e sem alteracao de RLS.

CREATE INDEX sie_projects_owner_idx
    ON public.sie_projects (owner_id);

CREATE INDEX sie_revisions_created_by_idx
    ON public.sie_project_revisions (created_by);

CREATE INDEX sie_audit_actor_idx
    ON public.sie_audit_events (actor_id);

CREATE INDEX sie_audit_revision_fk_idx
    ON public.sie_audit_events (revision_id, project_id);

-- Outros seis notices exigem EXPLAIN/planos com predicados reais:
-- sie_artifacts_run_scope_fk, sie_runs_revision_fk,
-- sie_links_circuit_scope_fk, sie_circuits_revision_fk,
-- sie_loads_room_scope_fk, sie_rooms_revision_fk.
-- Indexes existentes em outra ordem podem atender igualdades; nao criar sem prova.
-- Nao afirmar ganho de performance na base atual, que possui zero registros.
