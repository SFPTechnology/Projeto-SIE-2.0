-- SIE 2.0 greenfield, GF02, exclusively for Supabase project fozrymsidnaxmuvxxfhh.
-- APP-SPECIFIC NAMES: do not import the SIE 1.0 migrations and do not run db push at the repository root.
-- Security model v1: owner-only; organizations and collaboration are NOT enabled.
-- The application tables are newly created under public, with RLS enabled for every table.
-- All machine-origin output is READ-ONLY to authenticated browser users.
-- No normative conformity, professional attestation, or release permission is granted.

CREATE TABLE public.sie_projects (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    owner_id uuid NOT NULL DEFAULT auth.uid() REFERENCES auth.users(id) ON DELETE RESTRICT,
    name text NOT NULL CHECK (length(btrim(name)) BETWEEN 1 AND 160),
    created_at timestamptz NOT NULL DEFAULT now()
);

CREATE TABLE public.sie_project_revisions (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id uuid NOT NULL REFERENCES public.sie_projects(id) ON DELETE RESTRICT,
    version integer NOT NULL CHECK (version > 0),
    created_by uuid NOT NULL DEFAULT auth.uid() REFERENCES auth.users(id) ON DELETE RESTRICT,
    source_sha256 text CHECK (source_sha256 IS NULL OR source_sha256 ~ '^[0-9a-f]{64}$'),
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT sie_revisions_project_version_unique UNIQUE (project_id, version),
    CONSTRAINT sie_revisions_id_project_unique UNIQUE (id, project_id)
);

CREATE TABLE public.sie_rooms (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id uuid NOT NULL,
    revision_id uuid NOT NULL,
    name text NOT NULL CHECK (length(btrim(name)) BETWEEN 1 AND 160),
    width_m numeric(14,4) NOT NULL CHECK (width_m > 0 AND width_m < 100000),
    length_m numeric(14,4) NOT NULL CHECK (length_m > 0 AND length_m < 100000),
    excluded_perimeter_m numeric(14,4) NOT NULL DEFAULT 0
        CHECK (excluded_perimeter_m >= 0 AND excluded_perimeter_m < 200000),
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT sie_rooms_revision_fk FOREIGN KEY (revision_id, project_id)
        REFERENCES public.sie_project_revisions(id, project_id) ON DELETE RESTRICT,
    CONSTRAINT sie_rooms_id_scope_unique UNIQUE (id, project_id, revision_id),
    CONSTRAINT sie_rooms_exclusion_valid CHECK (excluded_perimeter_m < 2 * (width_m + length_m))
);

CREATE TABLE public.sie_loads (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id uuid NOT NULL,
    revision_id uuid NOT NULL,
    room_id uuid NOT NULL,
    label text NOT NULL CHECK (length(btrim(label)) BETWEEN 1 AND 160),
    kind text NOT NULL CHECK (kind IN ('LIGHTING', 'TUG', 'TUE', 'OTHER')),
    apparent_power_va numeric(16,3) NOT NULL CHECK (apparent_power_va > 0 AND apparent_power_va < 1000000000),
    quantity integer NOT NULL DEFAULT 1 CHECK (quantity BETWEEN 1 AND 100000),
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT sie_loads_room_scope_fk FOREIGN KEY (room_id, project_id, revision_id)
        REFERENCES public.sie_rooms(id, project_id, revision_id) ON DELETE RESTRICT,
    CONSTRAINT sie_loads_id_scope_unique UNIQUE (id, project_id, revision_id)
);

CREATE TABLE public.sie_circuits (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id uuid NOT NULL,
    revision_id uuid NOT NULL,
    code text NOT NULL CHECK (length(btrim(code)) BETWEEN 1 AND 64),
    nominal_voltage_v numeric(10,3) NOT NULL
        CHECK (nominal_voltage_v > 0 AND nominal_voltage_v < 100000),
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT sie_circuits_revision_fk FOREIGN KEY (revision_id, project_id)
        REFERENCES public.sie_project_revisions(id, project_id) ON DELETE RESTRICT,
    CONSTRAINT sie_circuits_code_unique UNIQUE (project_id, revision_id, code),
    CONSTRAINT sie_circuits_id_scope_unique UNIQUE (id, project_id, revision_id)
);

CREATE TABLE public.sie_circuit_loads (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id uuid NOT NULL,
    revision_id uuid NOT NULL,
    circuit_id uuid NOT NULL,
    load_id uuid NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT sie_links_circuit_scope_fk FOREIGN KEY (circuit_id, project_id, revision_id)
        REFERENCES public.sie_circuits(id, project_id, revision_id) ON DELETE RESTRICT,
    CONSTRAINT sie_links_load_scope_fk FOREIGN KEY (load_id, project_id, revision_id)
        REFERENCES public.sie_loads(id, project_id, revision_id) ON DELETE RESTRICT,
    CONSTRAINT sie_links_one_circuit_per_load UNIQUE (load_id, project_id, revision_id),
    CONSTRAINT sie_links_unique_pair UNIQUE (circuit_id, load_id, project_id, revision_id)
);

CREATE TABLE public.sie_calculation_runs (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id uuid NOT NULL,
    revision_id uuid NOT NULL,
    input_sha256 text NOT NULL CHECK (input_sha256 ~ '^[0-9a-f]{64}$'),
    engine_version text NOT NULL CHECK (length(btrim(engine_version)) BETWEEN 1 AND 100),
    normative_status text NOT NULL DEFAULT 'NOT_EVALUATED'
        CHECK (normative_status IN ('NOT_EVALUATED', 'EVIDENCE_PENDING', 'REVIEW_REQUIRED')),
    output_snapshot jsonb,
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT sie_runs_revision_fk FOREIGN KEY (revision_id, project_id)
        REFERENCES public.sie_project_revisions(id, project_id) ON DELETE RESTRICT,
    CONSTRAINT sie_runs_id_scope_unique UNIQUE (id, project_id, revision_id)
);

CREATE TABLE public.sie_artifacts (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id uuid NOT NULL,
    revision_id uuid NOT NULL,
    calculation_run_id uuid NOT NULL,
    artifact_type text NOT NULL CHECK (artifact_type IN ('LOAD_SCHEDULE', 'SINGLE_LINE', 'MEMORIAL', 'DRAWING', 'OTHER')),
    content_sha256 text NOT NULL CHECK (content_sha256 ~ '^[0-9a-f]{64}$'),
    artifact_status text NOT NULL DEFAULT 'DRAFT'
        CHECK (artifact_status IN ('DRAFT', 'STALE', 'REVOKED')),
    storage_path text CHECK (storage_path IS NULL OR length(storage_path) BETWEEN 1 AND 512),
    created_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT sie_artifacts_run_scope_fk FOREIGN KEY (calculation_run_id, project_id, revision_id)
        REFERENCES public.sie_calculation_runs(id, project_id, revision_id) ON DELETE RESTRICT
);

CREATE TABLE public.sie_audit_events (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id uuid NOT NULL REFERENCES public.sie_projects(id) ON DELETE RESTRICT,
    revision_id uuid,
    actor_id uuid REFERENCES auth.users(id) ON DELETE SET NULL,
    event_type text NOT NULL CHECK (length(btrim(event_type)) BETWEEN 1 AND 100),
    payload jsonb NOT NULL DEFAULT '{}'::jsonb,
    occurred_at timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT sie_audit_revision_scope_fk FOREIGN KEY (revision_id, project_id)
        REFERENCES public.sie_project_revisions(id, project_id) ON DELETE RESTRICT
);

CREATE INDEX sie_revisions_project_idx ON public.sie_project_revisions(project_id, created_at);
CREATE INDEX sie_rooms_scope_idx ON public.sie_rooms(project_id, revision_id);
CREATE INDEX sie_loads_scope_idx ON public.sie_loads(project_id, revision_id, room_id);
CREATE INDEX sie_circuits_scope_idx ON public.sie_circuits(project_id, revision_id);
CREATE INDEX sie_links_circuit_idx ON public.sie_circuit_loads(project_id, revision_id, circuit_id);
CREATE INDEX sie_runs_scope_idx ON public.sie_calculation_runs(project_id, revision_id, created_at);
CREATE INDEX sie_artifacts_scope_idx ON public.sie_artifacts(project_id, revision_id, calculation_run_id);
CREATE INDEX sie_audit_scope_idx ON public.sie_audit_events(project_id, occurred_at);

-- Explicit privilege posture: anon has ZERO table access.

ALTER TABLE public.sie_projects ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON TABLE public.sie_projects FROM PUBLIC, anon, authenticated;
GRANT SELECT ON TABLE public.sie_projects TO authenticated;
ALTER TABLE public.sie_project_revisions ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON TABLE public.sie_project_revisions FROM PUBLIC, anon, authenticated;
GRANT SELECT ON TABLE public.sie_project_revisions TO authenticated;
ALTER TABLE public.sie_rooms ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON TABLE public.sie_rooms FROM PUBLIC, anon, authenticated;
GRANT SELECT ON TABLE public.sie_rooms TO authenticated;
ALTER TABLE public.sie_loads ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON TABLE public.sie_loads FROM PUBLIC, anon, authenticated;
GRANT SELECT ON TABLE public.sie_loads TO authenticated;
ALTER TABLE public.sie_circuits ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON TABLE public.sie_circuits FROM PUBLIC, anon, authenticated;
GRANT SELECT ON TABLE public.sie_circuits TO authenticated;
ALTER TABLE public.sie_circuit_loads ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON TABLE public.sie_circuit_loads FROM PUBLIC, anon, authenticated;
GRANT SELECT ON TABLE public.sie_circuit_loads TO authenticated;
ALTER TABLE public.sie_calculation_runs ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON TABLE public.sie_calculation_runs FROM PUBLIC, anon, authenticated;
GRANT SELECT ON TABLE public.sie_calculation_runs TO authenticated;
ALTER TABLE public.sie_artifacts ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON TABLE public.sie_artifacts FROM PUBLIC, anon, authenticated;
GRANT SELECT ON TABLE public.sie_artifacts TO authenticated;
ALTER TABLE public.sie_audit_events ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON TABLE public.sie_audit_events FROM PUBLIC, anon, authenticated;
GRANT SELECT ON TABLE public.sie_audit_events TO authenticated;

-- Column-restricted INSERT/UPDATE. No browser DELETE, no arbitrary owner transfer.
GRANT INSERT (name, owner_id) ON TABLE public.sie_projects TO authenticated;
GRANT INSERT (project_id, version, source_sha256) ON TABLE public.sie_project_revisions TO authenticated;
GRANT INSERT (project_id, revision_id, name, width_m, length_m, excluded_perimeter_m) ON TABLE public.sie_rooms TO authenticated;
GRANT INSERT (project_id, revision_id, room_id, label, kind, apparent_power_va, quantity) ON TABLE public.sie_loads TO authenticated;
GRANT INSERT (project_id, revision_id, code, nominal_voltage_v) ON TABLE public.sie_circuits TO authenticated;
GRANT INSERT (project_id, revision_id, circuit_id, load_id) ON TABLE public.sie_circuit_loads TO authenticated;
GRANT UPDATE (name) ON TABLE public.sie_projects TO authenticated;

-- Authenticated users can only see/insert their own projects; revision authorship
-- is derived from auth.uid(), not user_metadata or a caller-supplied role.
CREATE POLICY sie_projects_owner_select ON public.sie_projects
    FOR SELECT TO authenticated USING (owner_id = (SELECT auth.uid()));
CREATE POLICY sie_projects_owner_insert ON public.sie_projects
    FOR INSERT TO authenticated WITH CHECK (owner_id = (SELECT auth.uid()));
CREATE POLICY sie_projects_owner_update_name ON public.sie_projects
    FOR UPDATE TO authenticated
    USING (owner_id = (SELECT auth.uid()))
    WITH CHECK (owner_id = (SELECT auth.uid()));

CREATE POLICY sie_project_revisions_owner_select ON public.sie_project_revisions
    FOR SELECT TO authenticated USING (EXISTS (SELECT 1 FROM public.sie_projects p WHERE p.id = project_id AND p.owner_id = (SELECT auth.uid())));
CREATE POLICY sie_project_revisions_owner_insert ON public.sie_project_revisions
    FOR INSERT TO authenticated WITH CHECK (EXISTS (SELECT 1 FROM public.sie_projects p WHERE p.id = project_id AND p.owner_id = (SELECT auth.uid())) AND created_by = (SELECT auth.uid()));

CREATE POLICY sie_rooms_owner_select ON public.sie_rooms
    FOR SELECT TO authenticated USING (EXISTS (SELECT 1 FROM public.sie_projects p WHERE p.id = project_id AND p.owner_id = (SELECT auth.uid())));
CREATE POLICY sie_rooms_owner_insert ON public.sie_rooms
    FOR INSERT TO authenticated WITH CHECK (EXISTS (SELECT 1 FROM public.sie_projects p WHERE p.id = project_id AND p.owner_id = (SELECT auth.uid())));

CREATE POLICY sie_loads_owner_select ON public.sie_loads
    FOR SELECT TO authenticated USING (EXISTS (SELECT 1 FROM public.sie_projects p WHERE p.id = project_id AND p.owner_id = (SELECT auth.uid())));
CREATE POLICY sie_loads_owner_insert ON public.sie_loads
    FOR INSERT TO authenticated WITH CHECK (EXISTS (SELECT 1 FROM public.sie_projects p WHERE p.id = project_id AND p.owner_id = (SELECT auth.uid())));

CREATE POLICY sie_circuits_owner_select ON public.sie_circuits
    FOR SELECT TO authenticated USING (EXISTS (SELECT 1 FROM public.sie_projects p WHERE p.id = project_id AND p.owner_id = (SELECT auth.uid())));
CREATE POLICY sie_circuits_owner_insert ON public.sie_circuits
    FOR INSERT TO authenticated WITH CHECK (EXISTS (SELECT 1 FROM public.sie_projects p WHERE p.id = project_id AND p.owner_id = (SELECT auth.uid())));

CREATE POLICY sie_circuit_loads_owner_select ON public.sie_circuit_loads
    FOR SELECT TO authenticated USING (EXISTS (SELECT 1 FROM public.sie_projects p WHERE p.id = project_id AND p.owner_id = (SELECT auth.uid())));
CREATE POLICY sie_circuit_loads_owner_insert ON public.sie_circuit_loads
    FOR INSERT TO authenticated WITH CHECK (EXISTS (SELECT 1 FROM public.sie_projects p WHERE p.id = project_id AND p.owner_id = (SELECT auth.uid())));

CREATE POLICY sie_calculation_runs_owner_select ON public.sie_calculation_runs
    FOR SELECT TO authenticated USING (EXISTS (SELECT 1 FROM public.sie_projects p WHERE p.id = project_id AND p.owner_id = (SELECT auth.uid())));

CREATE POLICY sie_artifacts_owner_select ON public.sie_artifacts
    FOR SELECT TO authenticated USING (EXISTS (SELECT 1 FROM public.sie_projects p WHERE p.id = project_id AND p.owner_id = (SELECT auth.uid())));

CREATE POLICY sie_audit_events_owner_select ON public.sie_audit_events
    FOR SELECT TO authenticated USING (EXISTS (SELECT 1 FROM public.sie_projects p WHERE p.id = project_id AND p.owner_id = (SELECT auth.uid())));

-- IMPORTANT: calculation runs, artifacts, and audit events are server-write-only.
-- Do not deploy a service_role credential to browsers. This migration creates no user.
