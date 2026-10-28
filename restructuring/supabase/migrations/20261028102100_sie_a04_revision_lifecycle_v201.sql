-- A04 / SIE 2.0 V2.0.1 / PostgreSQL 17
-- Additive to installed GF02, no recreation of existing tables, no legacy SQL.
-- Applied ONLY after explicit remote-DDL approval; initially branch-only.
-- DRAFT -> SEALED -> SUPERSEDED. Technical sealing is NOT professional approval.
-- Existing revision rows (if any) begin as DRAFT; never auto-approved.
ALTER TABLE public.sie_project_revisions
  ADD COLUMN lifecycle_state text NOT NULL DEFAULT 'DRAFT',
  ADD COLUMN base_revision_id uuid,
  ADD COLUMN lock_version bigint NOT NULL DEFAULT 0,
  ADD COLUMN idempotency_key text,
  ADD COLUMN sealed_snapshot jsonb,
  ADD COLUMN sealed_snapshot_sha256 text,
  ADD COLUMN sealed_at timestamptz,
  ADD COLUMN superseded_at timestamptz;

ALTER TABLE public.sie_project_revisions
  ADD CONSTRAINT sie_a04_revision_state_chk
    CHECK (lifecycle_state IN ('DRAFT', 'SEALED', 'SUPERSEDED')),
  ADD CONSTRAINT sie_a04_lock_version_chk CHECK (lock_version >= 0),
  ADD CONSTRAINT sie_a04_idempotency_key_chk
    CHECK (idempotency_key IS NULL OR
           (length(btrim(idempotency_key)) BETWEEN 1 AND 128)),
  ADD CONSTRAINT sie_a04_base_not_self_chk
    CHECK (base_revision_id IS NULL OR base_revision_id <> id),
  ADD CONSTRAINT sie_a04_state_consistency_chk
    CHECK (
      (lifecycle_state = 'DRAFT'
        AND sealed_snapshot IS NULL AND sealed_snapshot_sha256 IS NULL
        AND sealed_at IS NULL AND superseded_at IS NULL)
      OR
      (lifecycle_state = 'SEALED'
        AND sealed_snapshot IS NOT NULL AND
        sealed_snapshot_sha256 ~ '^[0-9a-f]{64}$'
        AND sealed_at IS NOT NULL AND superseded_at IS NULL)
      OR
      (lifecycle_state = 'SUPERSEDED'
        AND sealed_snapshot IS NOT NULL AND
        sealed_snapshot_sha256 ~ '^[0-9a-f]{64}$'
        AND sealed_at IS NOT NULL AND superseded_at IS NOT NULL)
    ),
  ADD CONSTRAINT sie_a04_base_same_project_fk
    FOREIGN KEY (base_revision_id, project_id)
      REFERENCES public.sie_project_revisions (id, project_id)
      ON DELETE RESTRICT;

-- Project uniquely identifies an owner in GF02: project+key scopes retries.
-- Nullable for preexisting GF02 drafts; B04 requires a non-null key on API writes.
CREATE UNIQUE INDEX sie_a04_idempotency_scope_idx
  ON public.sie_project_revisions (project_id, idempotency_key)
  WHERE idempotency_key IS NOT NULL;
CREATE INDEX sie_a04_base_revision_idx
  ON public.sie_project_revisions (base_revision_id, project_id)
  WHERE base_revision_id IS NOT NULL;

-- Every draft child DML (including direct Data API INSERT) serializes on the
-- revision identity, then re-checks state. A seal takes the SAME lock before
-- materializing a deterministic snapshot, preventing a concurrent child insert.
CREATE FUNCTION public.sie_a04_guard_child_write()
RETURNS trigger LANGUAGE plpgsql SECURITY INVOKER SET search_path = ''
AS $body$
DECLARE v_revision uuid; v_project uuid; v_state text;
BEGIN
  IF TG_OP = 'UPDATE' AND (
    NEW.project_id IS DISTINCT FROM OLD.project_id OR
    NEW.revision_id IS DISTINCT FROM OLD.revision_id
  ) THEN
    RAISE EXCEPTION 'A04 child cannot change project/revision scope'
      USING ERRCODE = '23514';
  END IF;
  IF TG_OP = 'DELETE' THEN
    v_revision := OLD.revision_id; v_project := OLD.project_id;
  ELSE
    v_revision := NEW.revision_id; v_project := NEW.project_id;
  END IF;

  PERFORM pg_catalog.pg_advisory_xact_lock(
    pg_catalog.hashtextextended(v_revision::text, 20261028)
  );
  SELECT r.lifecycle_state INTO v_state
    FROM public.sie_project_revisions r
    WHERE r.id = v_revision AND r.project_id = v_project;
  IF NOT FOUND OR v_state IS DISTINCT FROM 'DRAFT' THEN
    RAISE EXCEPTION 'A04 only DRAFT revision children may be changed'
      USING ERRCODE = '23514';
  END IF;

  IF TG_OP = 'DELETE' THEN RETURN OLD; END IF;
  RETURN NEW;
END;
$body$;

-- These triggers cover the entire editable revision topology.
CREATE TRIGGER sie_a04_rooms_guard
  BEFORE INSERT OR UPDATE OR DELETE ON public.sie_rooms
  FOR EACH ROW EXECUTE FUNCTION public.sie_a04_guard_child_write();
CREATE TRIGGER sie_a04_loads_guard
  BEFORE INSERT OR UPDATE OR DELETE ON public.sie_loads
  FOR EACH ROW EXECUTE FUNCTION public.sie_a04_guard_child_write();
CREATE TRIGGER sie_a04_circuits_guard
  BEFORE INSERT OR UPDATE OR DELETE ON public.sie_circuits
  FOR EACH ROW EXECUTE FUNCTION public.sie_a04_guard_child_write();
CREATE TRIGGER sie_a04_links_guard
  BEFORE INSERT OR UPDATE OR DELETE ON public.sie_circuit_loads
  FOR EACH ROW EXECUTE FUNCTION public.sie_a04_guard_child_write();

CREATE FUNCTION public.sie_a04_guard_revision_write()
RETURNS trigger LANGUAGE plpgsql SECURITY INVOKER SET search_path = ''
AS $body$
DECLARE v_base record; v_rooms jsonb; v_loads jsonb;
        v_circuits jsonb; v_links jsonb; v_snapshot jsonb;
        v_old_meta jsonb; v_new_meta jsonb;
BEGIN
  IF TG_OP = 'DELETE' THEN
    IF OLD.lifecycle_state <> 'DRAFT' THEN
      RAISE EXCEPTION 'A04 sealed/superseded revision cannot be deleted'
        USING ERRCODE = '23514';
    END IF;
    RETURN OLD;
  END IF;

  IF TG_OP = 'INSERT' THEN
    IF NEW.lifecycle_state <> 'DRAFT' OR NEW.lock_version <> 0 OR
       NEW.sealed_snapshot IS NOT NULL OR
       NEW.sealed_snapshot_sha256 IS NOT NULL OR
       NEW.sealed_at IS NOT NULL OR NEW.superseded_at IS NOT NULL THEN
      RAISE EXCEPTION 'A04 new revision must be an unsealed DRAFT'
        USING ERRCODE = '23514';
    END IF;
    IF NEW.base_revision_id IS NOT NULL THEN
      SELECT b.version, b.lifecycle_state INTO v_base
        FROM public.sie_project_revisions b
        WHERE b.id = NEW.base_revision_id AND b.project_id = NEW.project_id;
      IF NOT FOUND OR v_base.lifecycle_state NOT IN ('SEALED', 'SUPERSEDED')
         OR v_base.version >= NEW.version THEN
        RAISE EXCEPTION 'A04 base revision must be sealed and older in same project'
          USING ERRCODE = '23514';
      END IF;
    END IF;
    RETURN NEW;
  END IF;

  -- Identity, author, project, version, base and retry key are immutable.
  v_old_meta := pg_catalog.to_jsonb(OLD)
    - 'lifecycle_state' - 'lock_version'
    - 'sealed_snapshot' - 'sealed_snapshot_sha256'
    - 'sealed_at' - 'superseded_at' - 'source_sha256';
  v_new_meta := pg_catalog.to_jsonb(NEW)
    - 'lifecycle_state' - 'lock_version'
    - 'sealed_snapshot' - 'sealed_snapshot_sha256'
    - 'sealed_at' - 'superseded_at' - 'source_sha256';
  IF v_new_meta IS DISTINCT FROM v_old_meta OR
     NEW.lock_version <> OLD.lock_version + 1 THEN
    RAISE EXCEPTION 'A04 stale lock or attempt to change immutable revision fields'
      USING ERRCODE = '23514';
  END IF;

  IF OLD.lifecycle_state = 'DRAFT' AND NEW.lifecycle_state = 'DRAFT' THEN
    IF NEW.sealed_snapshot IS NOT NULL OR NEW.sealed_snapshot_sha256 IS NOT NULL
       OR NEW.sealed_at IS NOT NULL OR NEW.superseded_at IS NOT NULL THEN
      RAISE EXCEPTION 'A04 draft cannot provide sealed metadata'
        USING ERRCODE = '23514';
    END IF;
    RETURN NEW;
  END IF;

  IF OLD.lifecycle_state = 'DRAFT' AND NEW.lifecycle_state = 'SEALED' THEN
    -- Serialize against all child writes on this revision.
    PERFORM pg_catalog.pg_advisory_xact_lock(
      pg_catalog.hashtextextended(OLD.id::text, 20261028)
    );
    SELECT COALESCE(pg_catalog.jsonb_agg(pg_catalog.to_jsonb(t) ORDER BY t.id), '[]'::jsonb)
      INTO v_rooms FROM public.sie_rooms t
      WHERE t.project_id = OLD.project_id AND t.revision_id = OLD.id;
    SELECT COALESCE(pg_catalog.jsonb_agg(pg_catalog.to_jsonb(t) ORDER BY t.id), '[]'::jsonb)
      INTO v_loads FROM public.sie_loads t
      WHERE t.project_id = OLD.project_id AND t.revision_id = OLD.id;
    SELECT COALESCE(pg_catalog.jsonb_agg(pg_catalog.to_jsonb(t) ORDER BY t.id), '[]'::jsonb)
      INTO v_circuits FROM public.sie_circuits t
      WHERE t.project_id = OLD.project_id AND t.revision_id = OLD.id;
    SELECT COALESCE(pg_catalog.jsonb_agg(pg_catalog.to_jsonb(t) ORDER BY t.id), '[]'::jsonb)
      INTO v_links FROM public.sie_circuit_loads t
      WHERE t.project_id = OLD.project_id AND t.revision_id = OLD.id;

    v_snapshot := pg_catalog.jsonb_build_object(
      'schema_version', 1, 'project_id', OLD.project_id,
      'revision_id', OLD.id, 'version', OLD.version,
      'source_sha256', NEW.source_sha256,
      'rooms', v_rooms, 'loads', v_loads,
      'circuits', v_circuits, 'circuit_loads', v_links
    );
    NEW.sealed_snapshot := v_snapshot;
    NEW.sealed_snapshot_sha256 := pg_catalog.encode(
      pg_catalog.sha256(pg_catalog.convert_to(v_snapshot::text, 'UTF8')), 'hex'
    );
    NEW.sealed_at := pg_catalog.clock_timestamp();
    NEW.superseded_at := NULL;
    RETURN NEW;
  END IF;

  IF OLD.lifecycle_state = 'SEALED' AND NEW.lifecycle_state = 'SUPERSEDED' THEN
    IF NEW.source_sha256 IS DISTINCT FROM OLD.source_sha256 OR
       NEW.sealed_snapshot IS DISTINCT FROM OLD.sealed_snapshot OR
       NEW.sealed_snapshot_sha256 IS DISTINCT FROM OLD.sealed_snapshot_sha256 OR
       NEW.sealed_at IS DISTINCT FROM OLD.sealed_at THEN
      RAISE EXCEPTION 'A04 cannot edit sealed content or hash'
        USING ERRCODE = '23514';
    END IF;
    NEW.superseded_at := pg_catalog.clock_timestamp();
    RETURN NEW;
  END IF;
  RAISE EXCEPTION 'A04 invalid lifecycle transition % -> %',
    OLD.lifecycle_state, NEW.lifecycle_state USING ERRCODE = '23514';
END;
$body$;

CREATE TRIGGER sie_a04_revision_guard
  BEFORE INSERT OR UPDATE OR DELETE ON public.sie_project_revisions
  FOR EACH ROW EXECUTE FUNCTION public.sie_a04_guard_revision_write();

-- Optional companion guard: TRUNCATE skips row triggers. Deny for all
-- application tables under normal application and service roles.
REVOKE TRUNCATE ON TABLE
  public.sie_project_revisions, public.sie_rooms, public.sie_loads,
  public.sie_circuits, public.sie_circuit_loads
  FROM PUBLIC, anon, authenticated, service_role;

-- Application users cannot seal/supersede. Only a trusted backend may
-- perform these UPDATEs after verifying project ownership and lock_version.
REVOKE UPDATE ON TABLE public.sie_project_revisions FROM authenticated;
GRANT UPDATE (lifecycle_state, lock_version, source_sha256)
  ON TABLE public.sie_project_revisions TO service_role;

-- Neither trigger function is a client callable RPC.
REVOKE ALL ON FUNCTION public.sie_a04_guard_child_write() FROM PUBLIC, anon, authenticated;
REVOKE ALL ON FUNCTION public.sie_a04_guard_revision_write() FROM PUBLIC, anon, authenticated;
