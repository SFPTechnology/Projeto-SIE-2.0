-- MOD-DC - Store per-project overrides used by the conductor sizing engine (dimensionamento de condutores).
-- Mirrors the shape of public.parametros_edp_overrides (docs/supabase/0001_init.sql).
-- Source: repo-dimensionamento-condutores-overrides.supabase.ts expects table
-- public.dimensionamento_condutores_overrides (projeto_id, overrides, atualizado_em).

CREATE TABLE IF NOT EXISTS public.dimensionamento_condutores_overrides (
  projeto_id     TEXT PRIMARY KEY REFERENCES public.projetos(id) ON DELETE CASCADE,
  overrides      JSONB NOT NULL,
  atualizado_em  TIMESTAMP WITH TIME ZONE NOT NULL
);

GRANT ALL ON public.dimensionamento_condutores_overrides TO service_role;

ALTER TABLE public.dimensionamento_condutores_overrides ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "dimensionamento_condutores_overrides_all_anon"
  ON public.dimensionamento_condutores_overrides;
CREATE POLICY "dimensionamento_condutores_overrides_all_anon"
  ON public.dimensionamento_condutores_overrides
  FOR ALL TO anon USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "dimensionamento_condutores_overrides_all_authenticated"
  ON public.dimensionamento_condutores_overrides;
CREATE POLICY "dimensionamento_condutores_overrides_all_authenticated"
  ON public.dimensionamento_condutores_overrides
  FOR ALL TO authenticated USING (true) WITH CHECK (true);

COMMENT ON TABLE public.dimensionamento_condutores_overrides
  IS 'Overrides declarados manualmente por projeto para o motor de dimensionamento de condutores (MOD-DC).';
