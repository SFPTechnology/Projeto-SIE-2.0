-- A03 / SIE 2.0 V2.0.1. PostgreSQL 17. ADITIVE migration candidate.
-- Scope: GF02 alone; no legacy migration, no DROP, no production apply here.
-- Four uncovered FK prefixes identified by the 2026-10-28 catalog readback.
CREATE INDEX sie_projects_owner_idx ON public.sie_projects (owner_id);
CREATE INDEX sie_revisions_created_by_idx ON public.sie_project_revisions (created_by);
CREATE INDEX sie_audit_actor_idx ON public.sie_audit_events (actor_id);
CREATE INDEX sie_audit_revision_fk_idx ON public.sie_audit_events (revision_id, project_id);
-- Six further advisor notices overlap indexes in a different equality-column
-- order and require representative EXPLAIN before considering additions.
