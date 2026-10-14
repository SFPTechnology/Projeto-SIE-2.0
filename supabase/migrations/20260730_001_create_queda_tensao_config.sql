-- MOD-QT: store per-project voltage-drop configuration.
-- Mirrors the shape used by dimensionamento_condutores_resultado/overrides.
-- Source: repo-queda-tensao-config.supabase.ts expects table
-- public.queda_tensao_config (projeto_id, config, atualizado_em).

CREATE TABLE IF NOT EXISTS public.queda_tensao_config (
  projeto_id     TEXT PRIMARY KEY REFERENCES public.projetos(id) ON DELETE CASCADE,
  config         JSONB NOT NULL DEFAULT '{}'::jsonb,
  atualizado_em  TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_queda_tensao_config_projeto
  ON public.queda_tensao_config (projeto_id);

GRANT ALL ON public.queda_tensao_config TO service_role;

ALTER TABLE public.queda_tensao_config ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "queda_tensao_config_all_anon"
  ON public.queda_tensao_config;
CREATE POLICY "queda_tensao_config_all_anon"
  ON public.queda_tensao_config
  FOR ALL TO anon USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "queda_tensao_config_all_authenticated"
  ON public.queda_tensao_config;
CREATE POLICY "queda_tensao_config_all_authenticated"
  ON public.queda_tensao_config
  FOR ALL TO authenticated USING (true) WITH CHECK (true);

COMMENT ON TABLE public.queda_tensao_config
  IS 'Per-project MOD-QT voltage-drop configuration: feeder, lengths, applied sections, and cable profile.';
