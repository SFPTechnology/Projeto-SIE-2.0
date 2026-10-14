-- Seed data: Amostra de Tabela 36 confirmada (§12.2.1 do documento-base)
-- Story DC-1: AC-DC-07 — Regressão da base normativa
-- Data: 2026-07-12

-- Amostra confirmada: Tabela 36 (Cu, PVC), métodos B1/C/D
-- Valores extraídos de PRD-MOD-DC, §12.2.1

-- ========================================
-- Tabela 36 — Cu, PVC, B1 (2 condutores carregados)
-- ========================================

INSERT INTO tabela_iz (
  tabela_nbr, material, isolacao, metodo, numero_condutores_carregados,
  secao_mm2, iz_amperes, fonte_chunk_id, status_verificacao, versao_base_normativa_id
)
SELECT 36, 'Cu', 'PVC', 'B1', 2, secao, iz, 'chunks_118_p108', 'CONFIRMADO', 1
FROM (
  VALUES
    (1.5::NUMERIC, 17.5::NUMERIC),
    (2.5::NUMERIC, 24::NUMERIC),
    (4::NUMERIC, 32::NUMERIC),
    (6::NUMERIC, 41::NUMERIC),
    (10::NUMERIC, 57::NUMERIC),
    (16::NUMERIC, 76::NUMERIC),
    (25::NUMERIC, 101::NUMERIC),
    (35::NUMERIC, 125::NUMERIC)
) AS t(secao, iz)
WHERE NOT EXISTS (
  SELECT 1 FROM tabela_iz
  WHERE tabela_nbr = 36 AND material = 'Cu' AND isolacao = 'PVC'
    AND metodo = 'B1' AND numero_condutores_carregados = 2
);

-- ========================================
-- Tabela 36 — Cu, PVC, B1 (3 condutores carregados)
-- ========================================

INSERT INTO tabela_iz (
  tabela_nbr, material, isolacao, metodo, numero_condutores_carregados,
  secao_mm2, iz_amperes, fonte_chunk_id, status_verificacao, versao_base_normativa_id
)
SELECT 36, 'Cu', 'PVC', 'B1', 3, secao, iz, 'chunks_118_p108', 'CONFIRMADO', 1
FROM (
  VALUES
    (1.5::NUMERIC, 15.5::NUMERIC),
    (2.5::NUMERIC, 21::NUMERIC),
    (4::NUMERIC, 28::NUMERIC),
    (6::NUMERIC, 36::NUMERIC),
    (10::NUMERIC, 50::NUMERIC),
    (16::NUMERIC, 68::NUMERIC),
    (25::NUMERIC, 89::NUMERIC),
    (35::NUMERIC, 110::NUMERIC)
) AS t(secao, iz)
WHERE NOT EXISTS (
  SELECT 1 FROM tabela_iz
  WHERE tabela_nbr = 36 AND material = 'Cu' AND isolacao = 'PVC'
    AND metodo = 'B1' AND numero_condutores_carregados = 3
);

-- ========================================
-- Tabela 36 — Cu, PVC, C (2 condutores carregados)
-- ========================================

INSERT INTO tabela_iz (
  tabela_nbr, material, isolacao, metodo, numero_condutores_carregados,
  secao_mm2, iz_amperes, fonte_chunk_id, status_verificacao, versao_base_normativa_id
)
SELECT 36, 'Cu', 'PVC', 'C', 2, secao, iz, 'chunks_118_p109', 'CONFIRMADO', 1
FROM (
  VALUES
    (2.5::NUMERIC, 27::NUMERIC)
) AS t(secao, iz)
WHERE NOT EXISTS (
  SELECT 1 FROM tabela_iz
  WHERE tabela_nbr = 36 AND material = 'Cu' AND isolacao = 'PVC'
    AND metodo = 'C' AND numero_condutores_carregados = 2
);

-- ========================================
-- Tabela 36 — Cu, PVC, C (3 condutores carregados)
-- ========================================

INSERT INTO tabela_iz (
  tabela_nbr, material, isolacao, metodo, numero_condutores_carregados,
  secao_mm2, iz_amperes, fonte_chunk_id, status_verificacao, versao_base_normativa_id
)
SELECT 36, 'Cu', 'PVC', 'C', 3, secao, iz, 'chunks_118_p109', 'CONFIRMADO', 1
FROM (
  VALUES
    (2.5::NUMERIC, 24::NUMERIC)
) AS t(secao, iz)
WHERE NOT EXISTS (
  SELECT 1 FROM tabela_iz
  WHERE tabela_nbr = 36 AND material = 'Cu' AND isolacao = 'PVC'
    AND metodo = 'C' AND numero_condutores_carregados = 3
);

-- ========================================
-- Tabela 36 — Cu, PVC, D (2 condutores carregados)
-- ========================================

INSERT INTO tabela_iz (
  tabela_nbr, material, isolacao, metodo, numero_condutores_carregados,
  secao_mm2, iz_amperes, fonte_chunk_id, status_verificacao, versao_base_normativa_id
)
SELECT 36, 'Cu', 'PVC', 'D', 2, secao, iz, 'chunks_118_p109', 'CONFIRMADO', 1
FROM (
  VALUES
    (2.5::NUMERIC, 29::NUMERIC)
) AS t(secao, iz)
WHERE NOT EXISTS (
  SELECT 1 FROM tabela_iz
  WHERE tabela_nbr = 36 AND material = 'Cu' AND isolacao = 'PVC'
    AND metodo = 'D' AND numero_condutores_carregados = 2
);

-- ========================================
-- Tabela 36 — Cu, PVC, D (3 condutores carregados)
-- ========================================

INSERT INTO tabela_iz (
  tabela_nbr, material, isolacao, metodo, numero_condutores_carregados,
  secao_mm2, iz_amperes, fonte_chunk_id, status_verificacao, versao_base_normativa_id
)
SELECT 36, 'Cu', 'PVC', 'D', 3, secao, iz, 'chunks_118_p109', 'CONFIRMADO', 1
FROM (
  VALUES
    (2.5::NUMERIC, 24::NUMERIC)
) AS t(secao, iz)
WHERE NOT EXISTS (
  SELECT 1 FROM tabela_iz
  WHERE tabela_nbr = 36 AND material = 'Cu' AND isolacao = 'PVC'
    AND metodo = 'D' AND numero_condutores_carregados = 3
);
