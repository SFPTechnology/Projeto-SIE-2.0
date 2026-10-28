\set ON_ERROR_STOP on
\echo C03 PostgreSQL 17 disposable integration
DO $test$
DECLARE n integer;
BEGIN
 SELECT count(*) INTO n FROM pg_tables
 WHERE schemaname='public' AND tablename IN
 ('sie_panels','sie_feeders','sie_circuit_technical','sie_room_benches',
  'sie_floorplans','sie_floorplan_vertices','sie_graphical_bindings',
  'sie_legacy_results','sie_distributor_overrides','sie_normative_rule_versions');
 IF n<>10 THEN RAISE EXCEPTION 'C03 expected 10 additional tables, got %',n; END IF;
 SELECT count(*) INTO n FROM pg_class c
 JOIN pg_namespace ns ON c.relnamespace=ns.oid
 WHERE ns.nspname='public' AND c.relname IN
 ('sie_panels','sie_feeders','sie_circuit_technical','sie_room_benches',
  'sie_floorplans','sie_floorplan_vertices','sie_graphical_bindings',
  'sie_legacy_results','sie_distributor_overrides','sie_normative_rule_versions')
 AND c.relrowsecurity;
 IF n<>10 THEN RAISE EXCEPTION 'C03 RLS required on all tables'; END IF;
END $test$;

-- DRAFT revision produced by A03/A04 disposable integration fixture
INSERT INTO public.sie_panels
 (id,project_id,revision_id,code,nominal_voltage_v,phase_mode) VALUES
 ('a0a0a0a0-aaaa-4aaa-8aaa-aaaaaaaaa001',
 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
 'dddddddd-dddd-4ddd-8ddd-dddddddddddd','QDG',220,'TWO'),
 ('a0a0a0a0-aaaa-4aaa-8aaa-aaaaaaaaa002',
 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
 'dddddddd-dddd-4ddd-8ddd-dddddddddddd','QDC',127,'SINGLE');
INSERT INTO public.sie_feeders
 (project_id,revision_id,upstream_panel_id,downstream_panel_id,phase_section_mm2)
 VALUES ('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
 'dddddddd-dddd-4ddd-8ddd-dddddddddddd',
 'a0a0a0a0-aaaa-4aaa-8aaa-aaaaaaaaa001',
 'a0a0a0a0-aaaa-4aaa-8aaa-aaaaaaaaa002',10);

INSERT INTO public.sie_circuits
 (id,project_id,revision_id,code,nominal_voltage_v)
 VALUES ('0b0b0b0b-bbbb-4bbb-8bbb-bbbbbbbbb001',
 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
 'dddddddd-dddd-4ddd-8ddd-dddddddddddd','C03-QDC',127);
INSERT INTO public.sie_circuit_technical
 (circuit_id,project_id,revision_id,panel_id,phase_mode,phase_section_mm2)
 VALUES ('0b0b0b0b-bbbb-4bbb-8bbb-bbbbbbbbb001',
 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
 'dddddddd-dddd-4ddd-8ddd-dddddddddddd',
 'a0a0a0a0-aaaa-4aaa-8aaa-aaaaaaaaa002','SINGLE',2.5);
INSERT INTO public.sie_floorplans
 (id,project_id,revision_id,source_sha256,coordinate_unit,real_units_per_drawing_unit,origin)
 VALUES ('f0f0f0f0-ffff-4fff-8fff-fffffffff001',
 'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
 'dddddddd-dddd-4ddd-8ddd-dddddddddddd',
 repeat('b',64),'mm',0.001,'DEV_SYNTHETIC');

DO $test$
BEGIN
 -- A03/A04 fixture has a SEALED/SUPERSEDED A revision; new children must be denied.
 BEGIN
   INSERT INTO public.sie_panels(project_id,revision_id,code,nominal_voltage_v)
   VALUES('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
     'cccccccc-cccc-4ccc-8ccc-cccccccccccc','IMMUTABLE',127);
   RAISE EXCEPTION 'new child inserted on SEALED revision';
 EXCEPTION WHEN check_violation THEN NULL;
 END;
 BEGIN
   UPDATE public.sie_panels SET code='NEW-CODE'
   WHERE id='a0a0a0a0-aaaa-4aaa-8aaa-aaaaaaaaa001'
   AND revision_id='dddddddd-dddd-4ddd-8ddd-dddddddddddd';
   -- DRAFT update is allowed; restore for fixture consistency.
   UPDATE public.sie_panels SET code='QDG'
   WHERE id='a0a0a0a0-aaaa-4aaa-8aaa-aaaaaaaaa001';
 EXCEPTION WHEN OTHERS THEN
   RAISE EXCEPTION 'C03 DRAFT edits unexpectedly blocked';
 END;
 BEGIN
   INSERT INTO public.sie_panels (project_id,revision_id,code,nominal_voltage_v)
   VALUES ('bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb',
   'dddddddd-dddd-4ddd-8ddd-dddddddddddd','CROSS',127);
   RAISE EXCEPTION 'cross-project reference accepted';
 EXCEPTION WHEN foreign_key_violation THEN NULL;
 END;
 BEGIN
   INSERT INTO public.sie_feeders
   (project_id,revision_id,upstream_panel_id,downstream_panel_id)
   VALUES ('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
   'dddddddd-dddd-4ddd-8ddd-dddddddddddd',
   'a0a0a0a0-aaaa-4aaa-8aaa-aaaaaaaaa001',
   'a0a0a0a0-aaaa-4aaa-8aaa-aaaaaaaaa001');
   RAISE EXCEPTION 'self feeder accepted';
 EXCEPTION WHEN check_violation THEN NULL;
 END;
 BEGIN
   INSERT INTO public.sie_normative_rule_versions
   (rule_id,rule_version,source_edition,source_sha256,status)
   VALUES ('TEST-UNTRUSTED',1,'synthetic',repeat('a',64),'APPROVED');
   RAISE EXCEPTION 'unattested approval accepted';
 EXCEPTION WHEN check_violation THEN NULL;
 END;
END $test$;

SET ROLE authenticated;
SET request.jwt.claim.sub = '11111111-1111-4111-8111-111111111111';
DO $test$ DECLARE n int; BEGIN
 SELECT count(*) INTO n FROM public.sie_panels;
 IF n<>2 THEN RAISE EXCEPTION 'Owner A must see 2 C03 panels, got %',n; END IF;
 BEGIN
  INSERT INTO public.sie_panels(project_id,revision_id,code,nominal_voltage_v)
  VALUES('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
  'dddddddd-dddd-4ddd-8ddd-dddddddddddd','FORBIDDEN',127);
  RAISE EXCEPTION 'browser INSERT allowed';
 EXCEPTION WHEN insufficient_privilege THEN NULL;
 END;
END $test$;
SET request.jwt.claim.sub = '22222222-2222-4222-8222-222222222222';
DO $test$ DECLARE n int; BEGIN
 SELECT count(*) INTO n FROM public.sie_panels;
 IF n<>0 THEN RAISE EXCEPTION 'Owner B read A panels'; END IF;
END $test$;
RESET ROLE;
\echo C03 PG17 PASS: FKs, RLS, no write grants, normative approval constraints
