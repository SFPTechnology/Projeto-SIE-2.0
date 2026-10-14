-- MOD-CC/SEC/QT Integration - Store downstream module returns (C3/C4/C5 validation results).
-- Source: sistema-de-instala-es-el-tricas-sie-main/docs/supabase/0009_dependencia_retornos_downstream.sql

CREATE TABLE IF NOT EXISTS public.dependencia_retornos_downstream (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  dependencia_id UUID NOT NULL REFERENCES public.dependencias(id) ON DELETE CASCADE,
  modulo TEXT NOT NULL CHECK (modulo IN ('MOD-CC', 'MOD-SEC', 'MOD-QT')),
  payload JSONB NOT NULL,
  recebido_em TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  versao_modulo TEXT NULL,
  origem TEXT NULL,
  created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_dependencia_retornos_downstream_dep_modulo
  ON public.dependencia_retornos_downstream(dependencia_id, modulo);

CREATE INDEX IF NOT EXISTS idx_dependencia_retornos_downstream_recebido
  ON public.dependencia_retornos_downstream(recebido_em DESC);

ALTER TABLE public.dependencia_retornos_downstream ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "dependencia_retornos_downstream_all_anon"
  ON public.dependencia_retornos_downstream;
CREATE POLICY "dependencia_retornos_downstream_all_anon"
  ON public.dependencia_retornos_downstream
  FOR ALL TO anon USING (true) WITH CHECK (true);

DROP POLICY IF EXISTS "dependencia_retornos_downstream_all_authenticated"
  ON public.dependencia_retornos_downstream;
CREATE POLICY "dependencia_retornos_downstream_all_authenticated"
  ON public.dependencia_retornos_downstream
  FOR ALL TO authenticated USING (true) WITH CHECK (true);

COMMENT ON TABLE public.dependencia_retornos_downstream
  IS 'Armazena retornos de modulos downstream (MOD-CC, MOD-SEC, MOD-QT) para rastreabilidade e auditoria.';

COMMENT ON COLUMN public.dependencia_retornos_downstream.modulo
  IS 'Modulo de validacao: MOD-CC (curto-circuito/C3), MOD-SEC (seccionamento/C4), MOD-QT (queda de tensao/C5)';

COMMENT ON COLUMN public.dependencia_retornos_downstream.payload
  IS 'Retorno completo do modulo (RetornoMODCC/RetornoMODSEC/RetornoMODQT) como JSONB.';
