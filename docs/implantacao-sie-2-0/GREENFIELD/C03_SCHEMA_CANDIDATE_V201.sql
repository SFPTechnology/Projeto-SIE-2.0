-- C03 CANDIDATE / REVIEW ONLY: NEVER execute on remote Supabase without
-- migration-new, disposable PostgreSQL verification, authorization and E02-E06.
-- Upstream: GF02+A03+A04+B04; target ONLY fozrymsidnaxmuvxxfhh.
-- All project-scoped relationships use (id,project_id,revision_id) where needed.
-- No normative approval is created by this schema.

ALTER TABLE public.sie_rooms
  ADD COLUMN IF NOT EXISTS room_type text,
  ADD COLUMN IF NOT EXISTS ceiling_height_m numeric(14,4)
    CHECK (ceiling_height_m IS NULL OR ceiling_height_m > 0);
ALTER TABLE public.sie_loads
  ADD COLUMN IF NOT EXISTS fixed_voltage_v numeric(10,3)
    CHECK (fixed_voltage_v IS NULL OR fixed_voltage_v > 0),
  ADD COLUMN IF NOT EXISTS appliance_type text,
  ADD COLUMN IF NOT EXISTS three_phase boolean;

CREATE TABLE public.sie_panels (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id uuid NOT NULL, revision_id uuid NOT NULL,
  code text NOT NULL CHECK (length(btrim(code)) BETWEEN 1 AND 64),
  nominal_voltage_v numeric(10,3) NOT NULL CHECK (nominal_voltage_v > 0),
  phase_mode text NOT NULL DEFAULT 'UNDECLARED'
    CHECK (phase_mode IN ('UNDECLARED','SINGLE','TWO','THREE')),
  grounding_scheme text CHECK (grounding_scheme IN ('TT','TN-S','TN-C','TN-C-S','IT')),
  created_at timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT sie_panels_revision_fk FOREIGN KEY(revision_id,project_id)
    REFERENCES public.sie_project_revisions(id,project_id) ON DELETE RESTRICT,
  CONSTRAINT sie_panels_scope_unique UNIQUE(id,project_id,revision_id),
  CONSTRAINT sie_panels_code_unique UNIQUE(project_id,revision_id,code)
);

CREATE TABLE public.sie_feeders (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id uuid NOT NULL,revision_id uuid NOT NULL,
  upstream_panel_id uuid, downstream_panel_id uuid NOT NULL,
  length_m numeric(14,4) CHECK (length_m IS NULL OR length_m >= 0),
  material text CHECK (material IN ('COPPER','ALUMINUM')),
  phase_section_mm2 numeric(12,4) CHECK (phase_section_mm2 IS NULL OR phase_section_mm2 > 0),
  neutral_section_mm2 numeric(12,4) CHECK (neutral_section_mm2 IS NULL OR neutral_section_mm2 > 0),
  pe_section_mm2 numeric(12,4) CHECK (pe_section_mm2 IS NULL OR pe_section_mm2 > 0),
  installation_method text,
  CONSTRAINT sie_feeder_revision_fk FOREIGN KEY(revision_id,project_id)
    REFERENCES public.sie_project_revisions(id,project_id) ON DELETE RESTRICT,
  CONSTRAINT sie_feeder_upstream_fk FOREIGN KEY(upstream_panel_id,project_id,revision_id)
    REFERENCES public.sie_panels(id,project_id,revision_id) ON DELETE RESTRICT,
  CONSTRAINT sie_feeder_downstream_fk FOREIGN KEY(downstream_panel_id,project_id,revision_id)
    REFERENCES public.sie_panels(id,project_id,revision_id) ON DELETE RESTRICT,
  CONSTRAINT sie_feeder_no_self CHECK (upstream_panel_id IS NULL OR upstream_panel_id <> downstream_panel_id)
);

CREATE TABLE public.sie_circuit_technical (
  circuit_id uuid PRIMARY KEY,
  project_id uuid NOT NULL,revision_id uuid NOT NULL,
  panel_id uuid,
  phase_mode text NOT NULL DEFAULT 'UNDECLARED'
    CHECK (phase_mode IN ('UNDECLARED','SINGLE','TWO','THREE')),
  power_factor numeric(5,4) CHECK (power_factor IS NULL OR power_factor > 0 AND power_factor <= 1),
  cable_length_m numeric(14,4) CHECK (cable_length_m IS NULL OR cable_length_m >= 0),
  material text CHECK (material IN ('COPPER','ALUMINUM')),
  installation_method text,
  phase_section_mm2 numeric(12,4) CHECK (phase_section_mm2 IS NULL OR phase_section_mm2 > 0),
  neutral_section_mm2 numeric(12,4) CHECK (neutral_section_mm2 IS NULL OR neutral_section_mm2 > 0),
  pe_section_mm2 numeric(12,4) CHECK (pe_section_mm2 IS NULL OR pe_section_mm2 > 0),
  breaker_nominal_a numeric(12,4) CHECK (breaker_nominal_a IS NULL OR breaker_nominal_a > 0),
  dr_nominal_ma numeric(12,4) CHECK (dr_nominal_ma IS NULL OR dr_nominal_ma > 0),
  dps_type text,
  conductor_catalog_version text,
  normative_rule_version text,
  CONSTRAINT sie_technical_circuit_fk FOREIGN KEY(circuit_id,project_id,revision_id)
    REFERENCES public.sie_circuits(id,project_id,revision_id) ON DELETE RESTRICT,
  CONSTRAINT sie_technical_panel_fk FOREIGN KEY(panel_id,project_id,revision_id)
    REFERENCES public.sie_panels(id,project_id,revision_id) ON DELETE RESTRICT
);

CREATE TABLE public.sie_room_benches (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id uuid NOT NULL,revision_id uuid NOT NULL,room_id uuid NOT NULL,
  ordinal integer NOT NULL CHECK (ordinal > 0),
  width_m numeric(14,4) NOT NULL CHECK(width_m > 0),
  is_kitchen_or_pantries boolean NOT NULL,
  CONSTRAINT sie_bench_room_fk FOREIGN KEY(room_id,project_id,revision_id)
    REFERENCES public.sie_rooms(id,project_id,revision_id) ON DELETE RESTRICT,
  CONSTRAINT sie_bench_order_unique UNIQUE(room_id,project_id,revision_id,ordinal)
);

CREATE TABLE public.sie_floorplans (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id uuid NOT NULL,revision_id uuid NOT NULL,
  source_sha256 text NOT NULL CHECK(source_sha256 ~ '^[0-9a-f]{64}$'),
  coordinate_unit text NOT NULL CHECK(coordinate_unit IN ('m','cm','mm')),
  real_units_per_drawing_unit numeric(18,8) NOT NULL CHECK(real_units_per_drawing_unit>0),
  origin text NOT NULL CHECK(origin IN ('AUTHORIZED_UPLOAD','DEV_SYNTHETIC')),
  CONSTRAINT sie_floorplan_revision_fk FOREIGN KEY(revision_id,project_id)
    REFERENCES public.sie_project_revisions(id,project_id) ON DELETE RESTRICT,
  CONSTRAINT sie_floorplan_scope_unique UNIQUE(id,project_id,revision_id)
);

CREATE TABLE public.sie_floorplan_vertices (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id uuid NOT NULL,revision_id uuid NOT NULL,
  floorplan_id uuid NOT NULL,room_id uuid NOT NULL,
  ordinal integer NOT NULL CHECK(ordinal>0),
  x numeric(16,6) NOT NULL,y numeric(16,6) NOT NULL,
  CONSTRAINT sie_vertices_floorplan_fk FOREIGN KEY(floorplan_id,project_id,revision_id)
    REFERENCES public.sie_floorplans(id,project_id,revision_id) ON DELETE RESTRICT,
  CONSTRAINT sie_vertices_room_fk FOREIGN KEY(room_id,project_id,revision_id)
    REFERENCES public.sie_rooms(id,project_id,revision_id) ON DELETE RESTRICT,
  CONSTRAINT sie_vertices_order_unique UNIQUE(floorplan_id,room_id,ordinal)
);

CREATE TABLE public.sie_graphical_bindings (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id uuid NOT NULL,revision_id uuid NOT NULL,floorplan_id uuid NOT NULL,
  room_id uuid,circuit_id uuid,
  symbol_code text NOT NULL CHECK(length(btrim(symbol_code)) BETWEEN 1 AND 100),
  x numeric(16,6) NOT NULL,y numeric(16,6) NOT NULL,
  CONSTRAINT sie_binding_type CHECK ((room_id IS NOT NULL) <> (circuit_id IS NOT NULL)),
  CONSTRAINT sie_binding_plan_fk FOREIGN KEY(floorplan_id,project_id,revision_id)
    REFERENCES public.sie_floorplans(id,project_id,revision_id) ON DELETE RESTRICT,
  CONSTRAINT sie_binding_room_fk FOREIGN KEY(room_id,project_id,revision_id)
    REFERENCES public.sie_rooms(id,project_id,revision_id) ON DELETE RESTRICT,
  CONSTRAINT sie_binding_circuit_fk FOREIGN KEY(circuit_id,project_id,revision_id)
    REFERENCES public.sie_circuits(id,project_id,revision_id) ON DELETE RESTRICT
);

CREATE TABLE public.sie_legacy_results (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id uuid NOT NULL,revision_id uuid NOT NULL,
  source_system text NOT NULL,
  source_record_id text NOT NULL,
  source_sha256 text NOT NULL CHECK(source_sha256 ~ '^[0-9a-f]{64}$'),
  legacy_engine_version text,
  result_snapshot jsonb NOT NULL,
  normative_status text NOT NULL DEFAULT 'NOT_EVALUATED'
    CHECK(normative_status='NOT_EVALUATED'),
  CONSTRAINT sie_legacy_results_revision_fk FOREIGN KEY(revision_id,project_id)
    REFERENCES public.sie_project_revisions(id,project_id) ON DELETE RESTRICT,
  CONSTRAINT sie_legacy_results_source_unique UNIQUE(project_id,revision_id,source_system,source_record_id)
);

CREATE TABLE public.sie_distributor_overrides (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  project_id uuid NOT NULL,revision_id uuid NOT NULL,
  field_name text NOT NULL, value_json jsonb NOT NULL,
  reason text NOT NULL CHECK(length(btrim(reason))>0),
  source_sha256 text NOT NULL CHECK(source_sha256 ~ '^[0-9a-f]{64}$'),
  valid_by uuid REFERENCES auth.users(id) ON DELETE RESTRICT,
  CONSTRAINT sie_override_revision_fk FOREIGN KEY(revision_id,project_id)
    REFERENCES public.sie_project_revisions(id,project_id) ON DELETE RESTRICT,
  CONSTRAINT sie_override_field_unique UNIQUE(project_id,revision_id,field_name)
);

CREATE TABLE public.sie_normative_rule_versions (
  rule_id text NOT NULL,rule_version integer NOT NULL CHECK(rule_version>0),
  source_edition text NOT NULL, source_sha256 text NOT NULL CHECK(source_sha256 ~ '^[0-9a-f]{64}$'),
  effective_from date, effective_until date,
  locality_uf char(2), distributor text,
  method text, status text NOT NULL
    CHECK (status IN ('CANDIDATE','EVIDENCE_PENDING','REVIEW_REQUIRED','APPROVED','REVOKED')),
  evidence_sha256 text CHECK(evidence_sha256 IS NULL OR evidence_sha256 ~ '^[0-9a-f]{64}$'),
  approval_reference text,approved_by uuid REFERENCES auth.users(id) ON DELETE RESTRICT,
  CONSTRAINT sie_rule_version_pk PRIMARY KEY(rule_id,rule_version),
  CONSTRAINT sie_rule_window CHECK(effective_until IS NULL OR effective_from IS NULL OR effective_until>=effective_from),
  CONSTRAINT sie_rule_approval CHECK(status<>'APPROVED' OR
    (evidence_sha256 IS NOT NULL AND approval_reference IS NOT NULL AND approved_by IS NOT NULL))
);


-- All new project/revision child entities are DRAFT-only; sealed and historical
-- revisions cannot be modified even by a trusted backend service_role.
CREATE FUNCTION public.sie_c03_guard_revision_edit()
RETURNS trigger LANGUAGE plpgsql SET search_path = '' AS $fn$
DECLARE p uuid; r uuid; state text;
BEGIN
  IF TG_OP='DELETE' THEN
    p := OLD.project_id; r := OLD.revision_id;
  ELSE
    p := NEW.project_id; r := NEW.revision_id;
    IF TG_OP='UPDATE' AND
       (OLD.project_id <> NEW.project_id OR OLD.revision_id <> NEW.revision_id) THEN
      RAISE EXCEPTION 'C03 immutable scope' USING ERRCODE='23514';
    END IF;
  END IF;
  SELECT lifecycle_state INTO state FROM public.sie_project_revisions
  WHERE id=r AND project_id=p;
  IF NOT FOUND OR state <> 'DRAFT' THEN
    RAISE EXCEPTION 'C03 revision is not DRAFT' USING ERRCODE='23514';
  END IF;
  IF TG_OP='DELETE' THEN RETURN OLD; ELSE RETURN NEW; END IF;
END $fn$;

DO $
DECLARE tbl text;
BEGIN
  FOREACH tbl IN ARRAY ARRAY[
    'sie_panels','sie_feeders','sie_circuit_technical','sie_room_benches',
    'sie_floorplans','sie_floorplan_vertices','sie_graphical_bindings',
    'sie_legacy_results','sie_distributor_overrides'
  ] LOOP
    EXECUTE format(
      'CREATE TRIGGER %I BEFORE INSERT OR UPDATE OR DELETE ON public.%I
       FOR EACH ROW EXECUTE FUNCTION public.sie_c03_guard_revision_edit()',
      tbl || '_draft_only',tbl);
  END LOOP;
END $;
REVOKE ALL ON FUNCTION public.sie_c03_guard_revision_edit() FROM PUBLIC, anon, authenticated;
-- Versioned rules are append-only; a replacement requires a new version.
CREATE FUNCTION public.sie_c03_rule_no_mutation()
RETURNS trigger LANGUAGE plpgsql SET search_path = '' AS $fn$
BEGIN
  RAISE EXCEPTION 'C03 normative rule version is immutable' USING ERRCODE='23514';
END $fn$;
CREATE TRIGGER sie_c03_rule_no_mutation BEFORE UPDATE OR DELETE
ON public.sie_normative_rule_versions
FOR EACH ROW EXECUTE FUNCTION public.sie_c03_rule_no_mutation();
REVOKE ALL ON FUNCTION public.sie_c03_rule_no_mutation() FROM PUBLIC, anon, authenticated;

-- Newly exposed tables: default deny anon, owner-only SELECT for authenticated.
-- Writes are backend-only, with owner verification in trusted application code.
DO $$
DECLARE tbl text;
BEGIN
  FOREACH tbl IN ARRAY ARRAY[
    'sie_panels','sie_feeders','sie_circuit_technical','sie_room_benches',
    'sie_floorplans','sie_floorplan_vertices','sie_graphical_bindings',
    'sie_legacy_results','sie_distributor_overrides'
  ] LOOP
    EXECUTE format('ALTER TABLE public.%I ENABLE ROW LEVEL SECURITY',tbl);
    EXECUTE format('REVOKE ALL ON TABLE public.%I FROM PUBLIC, anon, authenticated',tbl);
    EXECUTE format('GRANT SELECT ON TABLE public.%I TO authenticated',tbl);
    EXECUTE format('GRANT SELECT, INSERT ON TABLE public.%I TO service_role',tbl);
    EXECUTE format(
      'CREATE POLICY %I ON public.%I FOR SELECT TO authenticated USING (
       EXISTS (SELECT 1 FROM public.sie_projects p
               WHERE p.id = project_id AND p.owner_id = (SELECT auth.uid())))',
      tbl || '_owner_select',tbl);
  END LOOP;
END $$;
ALTER TABLE public.sie_normative_rule_versions ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON TABLE public.sie_normative_rule_versions FROM PUBLIC,anon,authenticated;
GRANT SELECT, INSERT ON TABLE public.sie_normative_rule_versions TO service_role;

CREATE INDEX sie_panels_scope_idx ON public.sie_panels(project_id,revision_id);
CREATE INDEX sie_feeders_scope_idx ON public.sie_feeders(project_id,revision_id);
CREATE INDEX sie_technical_scope_idx ON public.sie_circuit_technical(project_id,revision_id);
CREATE INDEX sie_benches_room_scope_idx ON public.sie_room_benches(project_id,revision_id,room_id);
CREATE INDEX sie_plans_scope_idx ON public.sie_floorplans(project_id,revision_id);
CREATE INDEX sie_vertices_scope_idx ON public.sie_floorplan_vertices(project_id,revision_id,floorplan_id);
CREATE INDEX sie_bindings_scope_idx ON public.sie_graphical_bindings(project_id,revision_id,floorplan_id);
CREATE INDEX sie_legacy_result_scope_idx ON public.sie_legacy_results(project_id,revision_id);
CREATE INDEX sie_override_scope_idx ON public.sie_distributor_overrides(project_id,revision_id);
