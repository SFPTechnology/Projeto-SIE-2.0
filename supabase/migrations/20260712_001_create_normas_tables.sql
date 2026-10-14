-- Migration: Create normative tables for MOD-DC v3.0
-- Date: 2026-07-12
-- Story: DC-1 — Base Normativa Versionada
-- Scope: NBR 5410:2004 (Ed. 2004) + EDP PT.DT.PDN.00068 v09

-- ========================================
-- Versionamento
-- ========================================

CREATE TABLE IF NOT EXISTS versao_base_normativa (
  id SERIAL PRIMARY KEY,
  versao TEXT NOT NULL UNIQUE,
  descricao TEXT,
  data_vigencia DATE NOT NULL,
  fonte_referencia TEXT COMMENT 'Caminho aos chunks/arquivo da norma',
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO versao_base_normativa (versao, descricao, data_vigencia, fonte_referencia)
VALUES ('1.0', 'NBR 5410:2004 + EDP PT.DT.PDN.00068_V9 (amostra confirmada)', '2026-07-12', 'Arquivos_Diversos/NBR_5410_original/NBR_5410_chunks.json, PT_DT_PDN_00068_V9_chunks.json')
ON CONFLICT (versao) DO NOTHING;

-- ========================================
-- Tabela IZ (Tabelas 36–39)
-- ========================================

CREATE TABLE IF NOT EXISTS tabela_iz (
  id SERIAL PRIMARY KEY,
  tabela_nbr INTEGER NOT NULL COMMENT '36, 37, 38 ou 39',
  material TEXT NOT NULL COMMENT 'Cu, Al',
  isolacao TEXT NOT NULL COMMENT 'PVC, EPR, XLPE',
  metodo TEXT NOT NULL COMMENT 'A1, A2, B1, B2, C, D, E, F, G',
  numero_condutores_carregados INTEGER NOT NULL COMMENT '2, 3, 4, etc.',
  secao_mm2 NUMERIC NOT NULL COMMENT 'Seção em mm²',
  iz_amperes NUMERIC NOT NULL COMMENT 'Iz base (30°C ar ou 20°C solo)',
  fonte_chunk_id TEXT COMMENT 'Referência ao chunk da norma',
  status_verificacao TEXT CHECK (status_verificacao IN ('CONFIRMADO', '[VERIFICAR]')) DEFAULT 'CONFIRMADO',
  versao_base_normativa_id INTEGER NOT NULL,
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  responsavel_verificacao TEXT,

  FOREIGN KEY (versao_base_normativa_id) REFERENCES versao_base_normativa(id),
  UNIQUE(tabela_nbr, material, isolacao, metodo, numero_condutores_carregados, secao_mm2)
);

CREATE INDEX idx_tabela_iz_consulta ON tabela_iz(material, isolacao, metodo, numero_condutores_carregados);

-- ========================================
-- Fator Correção Temperatura (Tabela 40)
-- ========================================

CREATE TABLE IF NOT EXISTS fator_correcao_temperatura (
  id SERIAL PRIMARY KEY,
  isolacao TEXT NOT NULL COMMENT 'PVC, EPR, XLPE',
  meio TEXT NOT NULL CHECK (meio IN ('ambiente', 'solo')) COMMENT 'Ambiente (ref 30°C) ou Solo (ref 20°C)',
  temperatura_graus INTEGER NOT NULL COMMENT 'Temperatura em °C',
  fator NUMERIC NOT NULL COMMENT 'Fator de correção',
  fonte_chunk_id TEXT,
  status_verificacao TEXT CHECK (status_verificacao IN ('CONFIRMADO', '[VERIFICAR]')) DEFAULT 'CONFIRMADO',
  versao_base_normativa_id INTEGER NOT NULL,
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  atualizado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (versao_base_normativa_id) REFERENCES versao_base_normativa(id),
  UNIQUE(isolacao, meio, temperatura_graus)
);

-- ========================================
-- Resistividade Térmica do Solo (Tabela 41)
-- ========================================

CREATE TABLE IF NOT EXISTS fator_resistividade_solo (
  id SERIAL PRIMARY KEY,
  resistividade_solo_km NUMERIC NOT NULL COMMENT 'K·m em K·m',
  fator NUMERIC NOT NULL COMMENT 'Fator de redução',
  fator_comprimento NUMERIC COMMENT 'Se aplicável',
  fonte_chunk_id TEXT,
  status_verificacao TEXT CHECK (status_verificacao IN ('CONFIRMADO', '[VERIFICAR]')) DEFAULT 'CONFIRMADO',
  versao_base_normativa_id INTEGER NOT NULL,
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (versao_base_normativa_id) REFERENCES versao_base_normativa(id),
  UNIQUE(resistividade_solo_km)
);

-- ========================================
-- Fator Correção Agrupamento (Tabelas 42–45)
-- ========================================

CREATE TABLE IF NOT EXISTS fator_correcao_agrupamento (
  id SERIAL PRIMARY KEY,
  metodo TEXT NOT NULL COMMENT 'B, C, D, E, F, G',
  numero_circuitos INTEGER NOT NULL COMMENT 'Número de circuitos agrupados',
  fator NUMERIC NOT NULL,
  intervalo_min INTEGER COMMENT 'Intervalo mínimo (ex: 9 para faixa 9-11)',
  intervalo_max INTEGER COMMENT 'Intervalo máximo (ex: 11 para faixa 9-11)',
  fonte_chunk_id TEXT,
  status_verificacao TEXT CHECK (status_verificacao IN ('CONFIRMADO', '[VERIFICAR]')) DEFAULT 'CONFIRMADO',
  versao_base_normativa_id INTEGER NOT NULL,
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (versao_base_normativa_id) REFERENCES versao_base_normativa(id),
  UNIQUE(metodo, numero_circuitos)
);

-- ========================================
-- Seções Mínimas por Aplicação (Tabela 47)
-- ========================================

CREATE TABLE IF NOT EXISTS secao_minima_aplicacao (
  id SERIAL PRIMARY KEY,
  tipo_linha TEXT NOT NULL COMMENT 'Instalação fixa, flexível, etc.',
  utilizacao TEXT NOT NULL COMMENT 'Iluminação, Força, Sinalização',
  secao_minima_cu_mm2 NUMERIC COMMENT 'Mínimo Cu em mm²',
  secao_minima_al_mm2 NUMERIC COMMENT 'Mínimo Al em mm²',
  notas TEXT COMMENT 'Notas da tabela (ex: circuitos de tomadas são força)',
  fonte_chunk_id TEXT,
  status_verificacao TEXT CHECK (status_verificacao IN ('CONFIRMADO', '[VERIFICAR]')) DEFAULT 'CONFIRMADO',
  versao_base_normativa_id INTEGER NOT NULL,
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (versao_base_normativa_id) REFERENCES versao_base_normativa(id),
  UNIQUE(tipo_linha, utilizacao)
);

-- ========================================
-- Seções Reduzidas de Neutro (Tabela 48)
-- ========================================

CREATE TABLE IF NOT EXISTS secao_neutro_reduzida (
  id SERIAL PRIMARY KEY,
  condicao_1 BOOLEAN COMMENT 'Trifásico equilibrado',
  condicao_2 BOOLEAN COMMENT 'Corrente harmônica TH3 ≤ 15%',
  condicao_3 BOOLEAN COMMENT 'Neutro protegido individualmente',
  condicao_4 BOOLEAN COMMENT 'Seção fase ≥ 10 mm² Cu / 16 Al',
  condicao_5 BOOLEAN COMMENT 'Sem diversidade relevante',
  secao_neutro_reduzida_mm2 NUMERIC COMMENT 'Seção reduzida permitida',
  fonte_chunk_id TEXT,
  status_verificacao TEXT CHECK (status_verificacao IN ('CONFIRMADO', '[VERIFICAR]')) DEFAULT 'CONFIRMADO',
  versao_base_normativa_id INTEGER NOT NULL,
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (versao_base_normativa_id) REFERENCES versao_base_normativa(id)
);

-- ========================================
-- Seção do Condutor de Proteção (Tabela 58)
-- ========================================

CREATE TABLE IF NOT EXISTS secao_pe (
  id SERIAL PRIMARY KEY,
  secao_fase_from_mm2 NUMERIC NOT NULL COMMENT 'Seção fase inicial (inclusive)',
  secao_fase_to_mm2 NUMERIC COMMENT 'Seção fase final (inclusive, NULL = até infinito)',
  secao_pe_cu_mm2 NUMERIC COMMENT 'Seção PE Cu recomendada',
  secao_pe_al_mm2 NUMERIC COMMENT 'Seção PE Al recomendada',
  fonte_chunk_id TEXT,
  status_verificacao TEXT CHECK (status_verificacao IN ('CONFIRMADO', '[VERIFICAR]')) DEFAULT 'CONFIRMADO',
  versao_base_normativa_id INTEGER NOT NULL,
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (versao_base_normativa_id) REFERENCES versao_base_normativa(id),
  UNIQUE(secao_fase_from_mm2, COALESCE(secao_fase_to_mm2, -1))
);

-- ========================================
-- Fator K para Curto-Circuito (Tabela 30)
-- ========================================

CREATE TABLE IF NOT EXISTS fator_k_curto (
  id SERIAL PRIMARY KEY,
  isolacao TEXT NOT NULL COMMENT 'PVC, EPR, XLPE',
  temporalidade TEXT NOT NULL CHECK (temporalidade IN ('até 5s', 'até 10s', 'acima 10s')) COMMENT 'Categoria de tempo de atuação',
  k NUMERIC NOT NULL COMMENT 'Fator k para cálculo de ∫i²dt',
  fonte_chunk_id TEXT,
  status_verificacao TEXT CHECK (status_verificacao IN ('CONFIRMADO', '[VERIFICAR]')) DEFAULT 'CONFIRMADO',
  versao_base_normativa_id INTEGER NOT NULL,
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (versao_base_normativa_id) REFERENCES versao_base_normativa(id),
  UNIQUE(isolacao, temporalidade)
);

-- ========================================
-- Tipos de Linha (Tabela 33) — Referência
-- ========================================

CREATE TABLE IF NOT EXISTS tipo_linha_tabela33 (
  id SERIAL PRIMARY KEY,
  numero_tipo TEXT NOT NULL COMMENT '1, 2, 3, ..., 11, 11A, 11B, 12-18, 21-27, etc.',
  descricao TEXT NOT NULL COMMENT 'Descrição do tipo de linha',
  metodo TEXT NOT NULL COMMENT 'Método de referência derivado (A1, B1, C, D, E, F, G)',
  fonte_chunk_id TEXT,
  status_verificacao TEXT CHECK (status_verificacao IN ('CONFIRMADO', '[VERIFICAR]')) DEFAULT '[VERIFICAR]',
  versao_base_normativa_id INTEGER NOT NULL,
  criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  FOREIGN KEY (versao_base_normativa_id) REFERENCES versao_base_normativa(id),
  UNIQUE(numero_tipo)
);

-- ========================================
-- Grant public access (Supabase RLS handled separately)
-- ========================================

GRANT SELECT ON ALL TABLES IN SCHEMA public TO authenticated;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO anon;
