\set ON_ERROR_STOP on
-- In a disposable PostgreSQL 17 container only. Never send these synthetic IDs
-- to the production Supabase database. This harness does not test real JWTs.
CREATE SCHEMA auth;
CREATE TABLE auth.users (id uuid PRIMARY KEY);
CREATE FUNCTION auth.uid() RETURNS uuid LANGUAGE sql STABLE
AS $$
 SELECT nullif(current_setting('request.jwt.claim.sub', true), '')::uuid
$$;
DO $roles$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='anon') THEN
    CREATE ROLE anon NOLOGIN;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='authenticated') THEN
    CREATE ROLE authenticated NOLOGIN;
  END IF;
  IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname='service_role') THEN
    CREATE ROLE service_role NOLOGIN BYPASSRLS;
  END IF;
END
$roles$;
GRANT USAGE ON SCHEMA auth TO authenticated, service_role;
GRANT EXECUTE ON FUNCTION auth.uid() TO authenticated, service_role;
GRANT USAGE ON SCHEMA public TO anon, authenticated, service_role;

\echo A03/A04 BASELINE INSTALL
\i restructuring/supabase/migrations/20261027195557_sie2_greenfield_foundation_owner_rls_v1.sql
\i restructuring/supabase/migrations/20261028102000_sie_a03_indexes_v201.sql
\i restructuring/supabase/migrations/20261028102100_sie_a04_revision_lifecycle_v201.sql

DO $test$
DECLARE n integer;
BEGIN
 SELECT count(*) INTO n FROM pg_indexes
 WHERE schemaname='public' AND indexname IN (
 'sie_projects_owner_idx', 'sie_revisions_created_by_idx',
 'sie_audit_actor_idx', 'sie_audit_revision_fk_idx');
 IF n <> 4 THEN RAISE EXCEPTION 'missing A03 indexes: %', n; END IF;
 SELECT count(*) INTO n FROM information_schema.columns
 WHERE table_schema='public' AND table_name='sie_project_revisions'
   AND column_name IN ('lifecycle_state', 'base_revision_id','lock_version',
      'idempotency_key','sealed_snapshot','sealed_snapshot_sha256','sealed_at','superseded_at');
 IF n <> 8 THEN RAISE EXCEPTION 'missing A04 columns: %', n; END IF;
END
$test$;

INSERT INTO auth.users(id) VALUES
 ('11111111-1111-4111-8111-111111111111'),
 ('22222222-2222-4222-8222-222222222222');
INSERT INTO public.sie_projects(id,owner_id,name) VALUES
 ('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa','11111111-1111-4111-8111-111111111111','A fixture'),
 ('bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb','22222222-2222-4222-8222-222222222222','B fixture');
INSERT INTO public.sie_project_revisions
 (id,project_id,version,created_by,idempotency_key)
VALUES ('cccccccc-cccc-4ccc-8ccc-cccccccccccc',
 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',1,
 '11111111-1111-4111-8111-111111111111','a-key-one');

SET ROLE authenticated;
SET request.jwt.claim.sub = '11111111-1111-4111-8111-111111111111';
DO $test$
DECLARE n int;
BEGIN
 SELECT count(*) INTO n FROM public.sie_projects;
 IF n<>1 THEN RAISE EXCEPTION 'owner A must see only one project'; END IF;
END
$test$;

INSERT INTO public.sie_rooms (project_id, revision_id, name, width_m, length_m)
VALUES (
  'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
  'cccccccc-cccc-4ccc-8ccc-cccccccccccc',
  'Sala segura',4,5);

INSERT INTO public.sie_circuits (project_id,revision_id,code,nominal_voltage_v)
VALUES (
  'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
  'cccccccc-cccc-4ccc-8ccc-cccccccccccc','C1',127);

SET request.jwt.claim.sub = '22222222-2222-4222-8222-222222222222';
DO $test$
DECLARE n int;
BEGIN
 SELECT count(*) INTO n FROM public.sie_projects
 WHERE id='aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa';
 IF n<>0 THEN RAISE EXCEPTION 'owner B can read project A'; END IF;
 BEGIN
  INSERT INTO public.sie_rooms(project_id,revision_id,name,width_m,length_m)
    VALUES ('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
     'cccccccc-cccc-4ccc-8ccc-cccccccccccc','Cross-owner',2,3);
  RAISE EXCEPTION 'B was wrongly allowed to insert into project A';
 EXCEPTION WHEN insufficient_privilege OR check_violation THEN NULL;
 END;
END
$test$;
RESET ROLE;
RESET request.jwt.claim.sub;

SET ROLE service_role;
SELECT (public.sie_a04_transition_revision(
 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
 'cccccccc-cccc-4ccc-8ccc-cccccccccccc',0,'SEALED')).lifecycle_state;
DO $test$
BEGIN
 BEGIN
  PERFORM public.sie_a04_transition_revision(
   'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
   'cccccccc-cccc-4ccc-8ccc-cccccccccccc',0,'SUPERSEDED');
  RAISE EXCEPTION 'stale CAS unexpectedly allowed';
 EXCEPTION WHEN serialization_failure THEN NULL;
 END;
END
$test$;
RESET ROLE;
DO $test$
DECLARE r record; n int;
BEGIN
 SELECT lifecycle_state, lock_version, sealed_snapshot,
        sealed_snapshot_sha256, sealed_at INTO r
 FROM public.sie_project_revisions
 WHERE id='cccccccc-cccc-4ccc-8ccc-cccccccccccc';
 IF r.lifecycle_state<>'SEALED' OR r.lock_version<>1 OR
    r.sealed_at IS NULL OR r.sealed_snapshot IS NULL OR
    r.sealed_snapshot_sha256 <> encode(
      sha256(convert_to(r.sealed_snapshot::text,'UTF8')),'hex')
 THEN RAISE EXCEPTION 'sealed snapshot/hash/state mismatch'; END IF;
 SELECT jsonb_array_length(r.sealed_snapshot->'rooms') INTO n;
 IF n<>1 THEN RAISE EXCEPTION 'snapshot lost room fixture'; END IF;
 SELECT jsonb_array_length(r.sealed_snapshot->'circuits') INTO n;
 IF n<>1 THEN RAISE EXCEPTION 'snapshot lost circuit fixture'; END IF;
END
$test$;

SET ROLE authenticated;
SET request.jwt.claim.sub = '11111111-1111-4111-8111-111111111111';
DO $test$
BEGIN
 BEGIN
  PERFORM public.sie_a04_transition_revision(
   'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
   'cccccccc-cccc-4ccc-8ccc-cccccccccccc',1,'SUPERSEDED');
  RAISE EXCEPTION 'browser called privileged CAS';
 EXCEPTION WHEN insufficient_privilege THEN NULL;
 END;
 BEGIN
 INSERT INTO public.sie_rooms(project_id,revision_id,name,width_m,length_m)
   VALUES ('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
    'cccccccc-cccc-4ccc-8ccc-cccccccccccc','After seal',2,2);
 RAISE EXCEPTION 'sealed revision was writable';
 EXCEPTION WHEN check_violation THEN NULL;
 END;
 BEGIN
 UPDATE public.sie_project_revisions SET lifecycle_state='SUPERSEDED'
 WHERE id='cccccccc-cccc-4ccc-8ccc-cccccccccccc';
 RAISE EXCEPTION 'browser was allowed to supersede';
 EXCEPTION WHEN insufficient_privilege THEN NULL;
 END;
END
$test$;
RESET ROLE;
RESET request.jwt.claim.sub;

DO $test$
BEGIN
 BEGIN
 UPDATE public.sie_rooms SET name='Tampering'
 WHERE name='Sala segura';
 RAISE EXCEPTION 'sealed child was writable by owner';
 EXCEPTION WHEN check_violation THEN NULL;
 END;
 BEGIN
 DELETE FROM public.sie_circuits
 WHERE code='C1';
 RAISE EXCEPTION 'sealed circuit was deletable by owner';
 EXCEPTION WHEN check_violation THEN NULL;
 END;
 BEGIN
 UPDATE public.sie_project_revisions
 SET lifecycle_state='SUPERSEDED',lock_version=lock_version+2
 WHERE id='cccccccc-cccc-4ccc-8ccc-cccccccccccc';
 RAISE EXCEPTION 'stale lock was accepted';
 EXCEPTION WHEN check_violation THEN NULL;
 END;
 BEGIN
 UPDATE public.sie_project_revisions
 SET lifecycle_state='DRAFT',lock_version=lock_version+1
 WHERE id='cccccccc-cccc-4ccc-8ccc-cccccccccccc';
 RAISE EXCEPTION 'sealed -> draft was accepted';
 EXCEPTION WHEN check_violation THEN NULL;
 END;
END
$test$;

INSERT INTO public.sie_project_revisions
(id,project_id,version,created_by,idempotency_key,base_revision_id)
VALUES ('dddddddd-dddd-4ddd-8ddd-dddddddddddd',
 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',2,
 '11111111-1111-4111-8111-111111111111','a-key-two',
 'cccccccc-cccc-4ccc-8ccc-cccccccccccc');
DO $test$
DECLARE r record;
BEGIN
 SELECT lifecycle_state,base_revision_id,lock_version INTO r
 FROM public.sie_project_revisions
 WHERE id='dddddddd-dddd-4ddd-8ddd-dddddddddddd';
 IF r.lifecycle_state<>'DRAFT' OR r.lock_version<>0 OR
    r.base_revision_id<>'cccccccc-cccc-4ccc-8ccc-cccccccccccc'::uuid
 THEN RAISE EXCEPTION 'clone metadata invalid'; END IF;
 BEGIN
  INSERT INTO public.sie_project_revisions
    (project_id,version,created_by,idempotency_key,base_revision_id)
  VALUES('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',3,
    '11111111-1111-4111-8111-111111111111','a-key-two',
    'cccccccc-cccc-4ccc-8ccc-cccccccccccc');
  RAISE EXCEPTION 'duplicate idempotency key allowed';
 EXCEPTION WHEN unique_violation THEN NULL;
 END;
END
$test$;

SET ROLE service_role;
SELECT (public.sie_a04_transition_revision(
 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
 'cccccccc-cccc-4ccc-8ccc-cccccccccccc',1,'SUPERSEDED')).lifecycle_state;
RESET ROLE;
DO $test$
DECLARE r record;
BEGIN
 SELECT lifecycle_state,superseded_at,sealed_snapshot_sha256 INTO r
 FROM public.sie_project_revisions
 WHERE id='cccccccc-cccc-4ccc-8ccc-cccccccccccc';
 IF r.lifecycle_state<>'SUPERSEDED' OR r.superseded_at IS NULL OR
    r.sealed_snapshot_sha256 IS NULL
 THEN RAISE EXCEPTION 'superseded record invalid'; END IF;
 BEGIN
  DELETE FROM public.sie_project_revisions
  WHERE id='cccccccc-cccc-4ccc-8ccc-cccccccccccc';
  RAISE EXCEPTION 'superseded revision deleted';
 EXCEPTION WHEN check_violation THEN NULL;
 END;
END
$test$;

\echo A03/A04 PASS - migration, owner isolation (synthetic roles), seal hash, child immutability, stale lock, clone and idempotency
