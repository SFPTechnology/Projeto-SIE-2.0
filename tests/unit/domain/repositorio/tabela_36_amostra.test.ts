/**
 * Test: Regressão da Tabela 36 (amostra confirmada)
 * Story: DC-1, AC-DC-23
 *
 * Valida que a base normativa carregada coincide exatamente com a amostra
 * confirmada do documento-base (§12.2.1 do PRD-MOD-DC).
 */

import { describe, it, expect, beforeAll } from 'vitest';
import { createClient } from '@supabase/supabase-js';

const supabase = createClient(
  process.env.VITE_SUPABASE_URL!,
  process.env.VITE_SUPABASE_ANON_KEY!
);

describe('Tabela 36 — Amostra Confirmada (AC-DC-23)', () => {

  // Amostra de referência do documento-base (§12.2.1)
  const amostrasEsperadas = [
    // Cu, PVC, B1/2 carregados
    { tabela: 36, material: 'Cu', isolacao: 'PVC', metodo: 'B1', nCondutores: 2, secao: 1.5, iz: 17.5 },
    { tabela: 36, material: 'Cu', isolacao: 'PVC', metodo: 'B1', nCondutores: 2, secao: 2.5, iz: 24 },
    { tabela: 36, material: 'Cu', isolacao: 'PVC', metodo: 'B1', nCondutores: 2, secao: 4, iz: 32 },
    { tabela: 36, material: 'Cu', isolacao: 'PVC', metodo: 'B1', nCondutores: 2, secao: 6, iz: 41 },
    { tabela: 36, material: 'Cu', isolacao: 'PVC', metodo: 'B1', nCondutores: 2, secao: 10, iz: 57 },
    { tabela: 36, material: 'Cu', isolacao: 'PVC', metodo: 'B1', nCondutores: 2, secao: 16, iz: 76 },
    { tabela: 36, material: 'Cu', isolacao: 'PVC', metodo: 'B1', nCondutores: 2, secao: 25, iz: 101 },
    { tabela: 36, material: 'Cu', isolacao: 'PVC', metodo: 'B1', nCondutores: 2, secao: 35, iz: 125 },

    // Cu, PVC, B1/3 carregados
    { tabela: 36, material: 'Cu', isolacao: 'PVC', metodo: 'B1', nCondutores: 3, secao: 1.5, iz: 15.5 },
    { tabela: 36, material: 'Cu', isolacao: 'PVC', metodo: 'B1', nCondutores: 3, secao: 2.5, iz: 21 },
    { tabela: 36, material: 'Cu', isolacao: 'PVC', metodo: 'B1', nCondutores: 3, secao: 4, iz: 28 },
    { tabela: 36, material: 'Cu', isolacao: 'PVC', metodo: 'B1', nCondutores: 3, secao: 6, iz: 36 },
    { tabela: 36, material: 'Cu', isolacao: 'PVC', metodo: 'B1', nCondutores: 3, secao: 10, iz: 50 },
    { tabela: 36, material: 'Cu', isolacao: 'PVC', metodo: 'B1', nCondutores: 3, secao: 16, iz: 68 },
    { tabela: 36, material: 'Cu', isolacao: 'PVC', metodo: 'B1', nCondutores: 3, secao: 25, iz: 89 },
    { tabela: 36, material: 'Cu', isolacao: 'PVC', metodo: 'B1', nCondutores: 3, secao: 35, iz: 110 },

    // Cu, PVC, C (amostra)
    { tabela: 36, material: 'Cu', isolacao: 'PVC', metodo: 'C', nCondutores: 2, secao: 2.5, iz: 27 },
    { tabela: 36, material: 'Cu', isolacao: 'PVC', metodo: 'C', nCondutores: 3, secao: 2.5, iz: 24 },

    // Cu, PVC, D (amostra)
    { tabela: 36, material: 'Cu', isolacao: 'PVC', metodo: 'D', nCondutores: 2, secao: 2.5, iz: 29 },
    { tabela: 36, material: 'Cu', isolacao: 'PVC', metodo: 'D', nCondutores: 3, secao: 2.5, iz: 24 },
  ];

  it('deve carregar 100% das amostras confirmadas com valor correto', async () => {
    for (const amostra of amostrasEsperadas) {
      const { data, error } = await supabase
        .from('tabela_iz')
        .select('iz_amperes')
        .eq('tabela_nbr', amostra.tabela)
        .eq('material', amostra.material)
        .eq('isolacao', amostra.isolacao)
        .eq('metodo', amostra.metodo)
        .eq('numero_condutores_carregados', amostra.nCondutores)
        .eq('secao_mm2', amostra.secao)
        .single();

      if (error) {
        throw new Error(
          `Falta amostra: Tab ${amostra.tabela}, ${amostra.material} ${amostra.isolacao} ` +
          `${amostra.metodo}/${amostra.nCondutores}, S=${amostra.secao}mm² — ${error.message}`
        );
      }

      expect(parseFloat(data.iz_amperes)).toBe(amostra.iz,
        `Divergência em Tab36 ${amostra.metodo} ${amostra.nCondutores} S=${amostra.secao}: ` +
        `esperado ${amostra.iz}A, obteve ${data.iz_amperes}A`
      );
    }
  });

  it('deve ter status_verificacao=CONFIRMADO para amostra', async () => {
    const { data, error } = await supabase
      .from('tabela_iz')
      .select('status_verificacao')
      .eq('tabela_nbr', 36)
      .eq('material', 'Cu')
      .eq('isolacao', 'PVC')
      .eq('metodo', 'B1')
      .eq('numero_condutores_carregados', 2)
      .single();

    expect(data?.status_verificacao).toBe('CONFIRMADO');
  });

  it('deve ter rastreabilidade (fonte_chunk_id, versao_base_normativa_id)', async () => {
    const { data, error } = await supabase
      .from('tabela_iz')
      .select('fonte_chunk_id, versao_base_normativa_id')
      .eq('tabela_nbr', 36)
      .eq('material', 'Cu')
      .eq('isolacao', 'PVC')
      .eq('metodo', 'B1')
      .eq('numero_condutores_carregados', 2)
      .eq('secao_mm2', 1.5)
      .single();

    expect(data?.fonte_chunk_id).toBeTruthy();
    expect(data?.versao_base_normativa_id).toBe(1); // versão 1.0 criada na migration
  });

  it('regressão: nenhuma divergência é permitida (AC-DC-23)', async () => {
    const divergencias: any[] = [];

    for (const amostra of amostrasEsperadas) {
      const { data } = await supabase
        .from('tabela_iz')
        .select('iz_amperes')
        .eq('tabela_nbr', amostra.tabela)
        .eq('material', amostra.material)
        .eq('isolacao', amostra.isolacao)
        .eq('metodo', amostra.metodo)
        .eq('numero_condutores_carregados', amostra.nCondutores)
        .eq('secao_mm2', amostra.secao)
        .single();

      if (data && parseFloat(data.iz_amperes) !== amostra.iz) {
        divergencias.push({
          amostra,
          valorObtido: parseFloat(data.iz_amperes),
          esperado: amostra.iz,
        });
      }
    }

    expect(divergencias.length).toBe(0,
      `${divergencias.length} divergência(s) encontrada(s) na regressão: ` +
      JSON.stringify(divergencias, null, 2)
    );
  });
});
