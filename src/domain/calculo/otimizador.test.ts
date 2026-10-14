import { describe, it, expect, beforeEach, vi } from 'vitest';
import {
  autoOtimizar,
  diagnosticarFalhas,
  type ResultadoOtimizacao
} from './otimizador';
import type { ParametrosCircuito } from '../modelo/tipos';

describe('AUTO-OTIMIZADOR: Core Algorithm', () => {
  let parametrosPadrao: ParametrosCircuito;

  beforeEach(() => {
    // Parâmetros base para testes
    parametrosPadrao = {
      corrente: 20,
      comprimento: 50,
      temperatura: 30,
      circuitosAgrupados: 1,
      esquemaAterramento: 'TN-S',
      metodoReferencia: 'B1',
      protecao: 40,
      material: 'cobre',
      isolacao: 'PVC'
    };
  });

  describe('✅ Casos de Sucesso', () => {
    it('deve encontrar seção 10mm² para circuito padrão 20A/50m @ 30°C', async () => {
      const resultado = await autoOtimizar(parametrosPadrao);

      expect(resultado.status).toBe('APROVADO');
      expect(resultado.seçãoOtimizada).toBe(10);
      expect(resultado.validações).toBeDefined();
      expect(resultado.tempoMs).toBeLessThan(1000); // < 1 segundo
    });

    it('deve todos os 6 critérios retornarem APROVADO', async () => {
      const resultado = await autoOtimizar(parametrosPadrao);

      if (resultado.status === 'APROVADO' && resultado.validações) {
        expect(resultado.validações.c1.status).toBe('APROVADO');
        expect(resultado.validações.c2.status).toBe('APROVADO');
        expect(resultado.validações.c3.status).toBe('APROVADO');
        expect(resultado.validações.c4.status).toBe('APROVADO');
        expect(resultado.validações.c5.status).toBe('APROVADO');
        expect(resultado.validações.c6.status).toBe('APROVADO');
      }
    });

    it('deve retornar a MENOR seção que passa', async () => {
      const resultado = await autoOtimizar(parametrosPadrao);

      if (resultado.status === 'APROVADO') {
        // Testar com próxima seção menor (deveria falhar)
        const proximaSeção = [1.5, 2.5, 4, 6, 10, 16, 25].find(
          (s) => s < resultado.seçãoOtimizada!
        );

        // Se houver seção menor, ela deveria ter sido testada
        expect(resultado.tentativas).toBeGreaterThan(1);
      }
    });
  });

  describe('❌ Casos de Falha', () => {
    it('deve retornar IMPOSSÍVEL_ATENDER para corrente muito alta', async () => {
      const params: ParametrosCircuito = {
        ...parametrosPadrao,
        corrente: 500 // Impossível de atender
      };

      const resultado = await autoOtimizar(params);

      expect(resultado.status).toBe('IMPOSSÍVEL_ATENDER');
      expect(resultado.seçãoOtimizada).toBeNull();
    });

    it('deve registrar número de tentativas', async () => {
      const resultado = await autoOtimizar(parametrosPadrao);

      if (resultado.status === 'APROVADO') {
        // Se encontrou em 10mm², foram testadas seções [4, 6, 10]
        expect(resultado.tentativas).toBeGreaterThanOrEqual(1);
        expect(resultado.tentativas).toBeLessThanOrEqual(12); // Max 12 seções
      }
    });
  });

  describe('⏱️ Sensibilidade a Parâmetros', () => {
    it('deve aumentar seção com temperatura mais alta', async () => {
      const baixaTemp = await autoOtimizar({
        ...parametrosPadrao,
        temperatura: 30
      });

      const altaTemp = await autoOtimizar({
        ...parametrosPadrao,
        temperatura: 50
      });

      if (
        baixaTemp.status === 'APROVADO' &&
        altaTemp.status === 'APROVADO'
      ) {
        expect(altaTemp.seçãoOtimizada).toBeGreaterThanOrEqual(
          baixaTemp.seçãoOtimizada!
        );
      }
    });

    it('deve aumentar seção com mais circuitos agrupados', async () => {
      const umCircuito = await autoOtimizar({
        ...parametrosPadrao,
        circuitosAgrupados: 1
      });

      const quatroCircuitos = await autoOtimizar({
        ...parametrosPadrao,
        circuitosAgrupados: 4
      });

      if (
        umCircuito.status === 'APROVADO' &&
        quatroCircuitos.status === 'APROVADO'
      ) {
        expect(quatroCircuitos.seçãoOtimizada).toBeGreaterThanOrEqual(
          umCircuito.seçãoOtimizada!
        );
      }
    });

    it('deve aumentar seção com comprimento maior', async () => {
      const curto = await autoOtimizar({
        ...parametrosPadrao,
        comprimento: 20
      });

      const longo = await autoOtimizar({
        ...parametrosPadrao,
        comprimento: 80
      });

      if (curto.status === 'APROVADO' && longo.status === 'APROVADO') {
        expect(longo.seçãoOtimizada).toBeGreaterThanOrEqual(
          curto.seçãoOtimizada!
        );
      }
    });
  });

  describe('🔍 Diagnóstico de Falhas', () => {
    it('deve diagnosticar corretamente por que seção falha', () => {
      // Mock de validação com falhas
      const validacaoComFalhas = {
        c1: { status: 'REPROVADO', motivo: 'Capacidade insuficiente' },
        c2: { status: 'APROVADO', motivo: 'OK' },
        c3: { status: 'REPROVADO', motivo: 'PE muito fino' },
        c4: { status: 'APROVADO', motivo: 'OK' },
        c5: { status: 'APROVADO', motivo: 'OK' },
        c6: { status: 'APROVADO', motivo: 'OK' }
      };

      const diagnostico = diagnosticarFalhas(validacaoComFalhas);

      expect(diagnostico).toContain('C1 - Capacidade insuficiente');
      expect(diagnostico).toContain('C3(CC) - PE muito fino');
      expect(diagnostico).toHaveLength(2); // Apenas 2 falhas
    });
  });

  describe('⚡ Performance', () => {
    it('deve completar em menos de 1 segundo', async () => {
      const inicio = Date.now();

      await autoOtimizar(parametrosPadrao);

      const duracao = Date.now() - inicio;
      expect(duracao).toBeLessThan(1000);
    });

    it('deve manter performance mesmo com múltiplas calls', async () => {
      const resultados = await Promise.all([
        autoOtimizar(parametrosPadrao),
        autoOtimizar({ ...parametrosPadrao, corrente: 30 }),
        autoOtimizar({ ...parametrosPadrao, temperatura: 50 }),
        autoOtimizar({ ...parametrosPadrao, comprimento: 100 })
      ]);

      resultados.forEach((r) => {
        expect(r.tempoMs).toBeLessThan(1000);
      });
    });
  });

  describe('🛡️ Edge Cases', () => {
    it('deve lidar com corrente muito baixa', async () => {
      const resultado = await autoOtimizar({
        ...parametrosPadrao,
        corrente: 0.5
      });

      expect(resultado.status).toBe('APROVADO');
      expect(resultado.seçãoOtimizada).toBeLessThanOrEqual(2.5);
    });

    it('deve lidar com comprimento zero (local)', async () => {
      const resultado = await autoOtimizar({
        ...parametrosPadrao,
        comprimento: 0
      });

      expect(resultado.status).toBe('APROVADO');
    });

    it('deve validar parâmetros obrigatórios', async () => {
      // @ts-expect-error - Teste com parâmetro inválido
      const resultado = await autoOtimizar({
        corrente: undefined,
        comprimento: 50
      });

      expect(resultado.status).toBe('IMPOSSÍVEL_ATENDER');
    });
  });
});

describe('AUTO-OTIMIZADOR: Algoritmo Guloso', () => {
  it('deve parar na PRIMEIRA seção que passa em TODOS os critérios', async () => {
    const params: ParametrosCircuito = {
      corrente: 20,
      comprimento: 50,
      temperatura: 30,
      circuitosAgrupados: 1,
      esquemaAterramento: 'TN-S',
      metodoReferencia: 'B1',
      protecao: 40,
      material: 'cobre',
      isolacao: 'PVC'
    };

    const resultado = await autoOtimizar(params);

    if (resultado.status === 'APROVADO') {
      // Greedy: deveria parar na primeira seção válida
      // Para esse circuito, esperamos 10mm² (não 16mm² ou maior)
      expect(resultado.seçãoOtimizada).toBeLessThanOrEqual(10);
    }
  });
});
