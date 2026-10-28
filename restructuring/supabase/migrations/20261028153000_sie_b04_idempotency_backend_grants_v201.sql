-- SIE 2.0 B04/B05 / V2.0.1 - additive candidate, PostgreSQL 17.
-- NEVER apply remotely without explicit DDL authorization, backup and read-back.
-- Dependencies: GF02 (20261027195557), A03 (20261028102000), A04 (20261028102100).
-- Existing GF02 rows remain valid and have NULL idempotency fields.
-- This does NOT create a user, role, bucket, or production deployment.

ALTER TABLE public.sie_projects
  ADD COLUMN idempotency_key text,
  ADD COLUMN request_fingerprint_sha256 text;

ALTER TABLE public.sie_projects
  ADD CONSTRAINT sie_b04_project_idempotency_pair_chk CHECK (
    (idempotency_key IS NULL AND request_fingerprint_sha256 IS NULL) OR
    (idempotency_key IS NOT NULL
      AND length(idempotency_key) BETWEEN 8 AND 128
      AND idempotency_key = btrim(idempotency_key)
      AND request_fingerprint_sha256 ~ '^[0-9a-f]{64}$')
  );

CREATE UNIQUE INDEX sie_b04_project_owner_idempotency_idx
  ON public.sie_projects(owner_id, idempotency_key)
  WHERE idempotency_key IS NOT NULL;

-- No modification of actor/owner or request identity after creation.
-- Persist request fingerprint independently of subsequent project renames.
CREATE FUNCTION public.sie_b04_guard_project_identity()
RETURNS trigger LANGUAGE plpgsql SECURITY INVOKER SET search_path = ''
AS $function$
BEGIN
  IF TG_OP = 'UPDATE' THEN
    IF NEW.id IS DISTINCT FROM OLD.id OR
       NEW.owner_id IS DISTINCT FROM OLD.owner_id OR
       NEW.created_at IS DISTINCT FROM OLD.created_at OR
       NEW.idempotency_key IS DISTINCT FROM OLD.idempotency_key OR
       NEW.request_fingerprint_sha256 IS DISTINCT FROM OLD.request_fingerprint_sha256
    THEN
      RAISE EXCEPTION 'B04 immutable project identity or request key'
        USING ERRCODE = '23514';
    END IF;
  ELSIF NEW.idempotency_key IS NOT NULL THEN
    -- The writer must hash exactly the normalized original project name.
    IF NEW.request_fingerprint_sha256 IS DISTINCT FROM
       pg_catalog.encode(pg_catalog.sha256(
         pg_catalog.convert_to(pg_catalog.btrim(NEW.name), 'UTF8')), 'hex')
    THEN
      RAISE EXCEPTION 'B04 project idempotency fingerprint mismatch'
        USING ERRCODE = '23514';
    END IF;
  END IF;
  RETURN NEW;
END;
$function$;

CREATE TRIGGER sie_b04_guard_project_identity
  BEFORE INSERT OR UPDATE ON public.sie_projects
  FOR EACH ROW EXECUTE FUNCTION public.sie_b04_guard_project_identity();

REVOKE ALL ON FUNCTION public.sie_b04_guard_project_identity()
  FROM PUBLIC, anon, authenticated;

-- Browser privileges remain GF02 owner-only; browser cannot invoke A04 CAS,
-- DELETE electrical entities, or write server-generated calculations/audit.
-- The pre-existing service_role bypasses RLS; production backend MUST perform
-- ownership validation before use and MUST NEVER expose service_role key.
-- Narrow project UPDATE to name; FK + A04 triggers govern child DML.
REVOKE UPDATE ON TABLE public.sie_projects FROM service_role;
GRANT UPDATE(name) ON TABLE public.sie_projects TO service_role;

GRANT UPDATE(name,width_m,length_m,excluded_perimeter_m)
  ON TABLE public.sie_rooms TO service_role;
GRANT UPDATE(room_id,label,kind,apparent_power_va,quantity)
  ON TABLE public.sie_loads TO service_role;
GRANT UPDATE(code,nominal_voltage_v)
  ON TABLE public.sie_circuits TO service_role;
GRANT UPDATE(circuit_id,load_id)
  ON TABLE public.sie_circuit_loads TO service_role;

GRANT DELETE ON TABLE
  public.sie_rooms, public.sie_loads, public.sie_circuits, public.sie_circuit_loads
  TO service_role;
REVOKE DELETE ON TABLE
  public.sie_rooms, public.sie_loads, public.sie_circuits, public.sie_circuit_loads
  FROM PUBLIC, anon, authenticated;

-- Server-only system outputs and audit remain INSERT, SELECT only to
-- service_role. Do not add browser INSERT to machine output tables.
-- No SECURITY DEFINER, no permissive browser policy, no new tables exposed.
