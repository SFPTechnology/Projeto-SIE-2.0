/**
 * Auto-Otimizador de Seção de Condutor
 * Encontra automaticamente a seção IDEAL que satisfaz TODOS os 6 critérios (C1-C6)
 */

import {
  ParametrosCircuito,
  ResultadoValidacao,
  ValidacaoCompleta,
  TamanhoComercial
} from '../modelo/tipos';

import {
  validarC1Capacidade,
  validarC2Sobrecarga,
  validarC3CurtoCircuito,
  validarC4Seletividade,
  validarC5QualidadeTecnica,
  validarC6Verificacoes
} from './validadores';

// Seções comerciais disponíveis (mm²)
const SECOES_COMERCIAIS: TamanhoComercial[] = [
  1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120
];

export interface ValidacaoSeção {
  c1: ResultadoValidacao;
  c2: ResultadoValidacao;
  c3: ResultadoValidacao;
  c4: ResultadoValidacao;
  c5: ResultadoValidacao;
  c6: ResultadoValidacao;
}

export interface ResultadoOtimizacao {
  status: 'APROVADO' | 'IMPOSSÍVEL_ATENDER';
  seçãoOtimizada: TamanhoComercial | null;
  validações: ValidacaoSeção | null;
  tentativas: number;
  tempoMs: number;
  mensagem: string;
}

/**
 * Auto-otimiza a seção de condutor testando todas as seções comerciais
 * Retorna a MENOR seção que passa em TODOS os 6 critérios
 */
export async function autoOtimizar(
  parametrosCircuito: ParametrosCircuito
): Promise<ResultadoOtimizacao> {
  const inicio = Date.now();
  let tentativas = 0;

  try {
    // Calcular seção mínima necessária para C1
    const seçãoMínimaC1 = calcularSeçãoMínimaC1(parametrosCircuito);

    // LOOP: Testar cada seção a partir da mínima
    for (const seção of SECOES_COMERCIAIS) {
      tentativas++;

      // Pular seções muito pequenas
      if (seção < seçãoMínimaC1) {
        continue;
      }

      console.log(`🔄 [AUTO-OTI] Testando seção ${seção}mm²...`);

      // VALIDAR TODOS OS 6 CRITÉRIOS
      const validação: ValidacaoSeção = {
        c1: await validarC1Capacidade(seção, parametrosCircuito),
        c2: await validarC2Sobrecarga(seção, parametrosCircuito),
        c3: await validarC3CurtoCircuito(seção, parametrosCircuito),
        c4: await validarC4Seletividade(seção, parametrosCircuito),
        c5: await validarC5QualidadeTecnica(seção, parametrosCircuito),
        c6: await validarC6Verificacoes(seção, parametrosCircuito)
      };

      // VERIFICAR SE TODOS OS CRITÉRIOS PASSARAM
      const todosAprovados = Object.values(validação).every(
        (v) => v.status === 'APROVADO'
      );

      if (todosAprovados) {
        console.log(`✅ [AUTO-OTI] SEÇÃO IDEAL ENCONTRADA: ${seção}mm²`);

        return {
          status: 'APROVADO',
          seçãoOtimizada: seção,
          validações: validação,
          tentativas,
          tempoMs: Date.now() - inicio,
          mensagem: `Seção otimizada: ${seção}mm² (testadas ${tentativas} seções)`
        };
      }

      // Log de falha para debug
      const falhas = Object.entries(validação)
        .filter(([_, v]) => v.status !== 'APROVADO')
        .map(([k]) => k)
        .join(', ');

      console.log(
        `❌ [AUTO-OTI] Seção ${seção}mm² falhou em: ${falhas}`
      );
    }

    // Nenhuma seção funcionou
    console.log(`❌ [AUTO-OTI] Impossível atender: nenhuma seção passou em todos os critérios`);

    return {
      status: 'IMPOSSÍVEL_ATENDER',
      seçãoOtimizada: null,
      validações: null,
      tentativas,
      tempoMs: Date.now() - inicio,
      mensagem: `Impossível atender: nenhuma das ${tentativas} seções testadas passou em TODOS os critérios`
    };
  } catch (erro) {
    console.error('[AUTO-OTI] Erro durante otimização:', erro);

    return {
      status: 'IMPOSSÍVEL_ATENDER',
      seçãoOtimizada: null,
      validações: null,
      tentativas,
      tempoMs: Date.now() - inicio,
      mensagem: `Erro: ${erro instanceof Error ? erro.message : 'Erro desconhecido'}`
    };
  }
}

/**
 * Calcula a seção MÍNIMA necessária baseada apenas em C1
 * Otimização: evita testar seções que já sabemos que falham em C1
 */
function calcularSeçãoMínimaC1(params: ParametrosCircuito): TamanhoComercial {
  const { corrente, temperatura = 30, circuitosAgrupados = 1 } = params;

  // Tabela simplificada de capacidades (cobre, PVC, @ 30°C)
  // Em produção, usar as tabelas completas do domínio
  const capacidadesBase: Record<TamanhoComercial, number> = {
    1.5: 15.5,
    2.5: 21,
    4: 27,
    6: 36,
    10: 50,
    16: 68,
    25: 89,
    35: 120,
    50: 155,
    70: 195,
    95: 245,
    120: 295
  };

  // Aplicar fator de redução de temperatura
  const fatorTemp = calcularFatorTemperatura(temperatura);

  // Aplicar fator de agrupamento de circuitos
  const fatorAgrupamento = calcularFatorAgrupamento(circuitosAgrupados);

  // Capacidade mínima necessária
  const capacidadeNecessária = corrente / (fatorTemp * fatorAgrupamento);

  // Encontrar a seção mínima
  for (const seção of SECOES_COMERCIAIS) {
    if (capacidadesBase[seção] >= capacidadeNecessária) {
      return seção;
    }
  }

  // Se nenhuma seção suficiente, retornar a maior
  return SECOES_COMERCIAIS[SECOES_COMERCIAIS.length - 1];
}

/**
 * Fator de redução de capacidade por temperatura
 * NBR 5410: cada 10°C acima de 30°C reduz capacidade ~13%
 */
function calcularFatorTemperatura(temperatura: number): number {
  if (temperatura <= 30) return 1.0;

  const deltaTemp = temperatura - 30;
  const fatoresDeRducao = Math.ceil(deltaTemp / 10);
  return Math.max(0.7, 1.0 - fatoresDeRducao * 0.13);
}

/**
 * Fator de redução de capacidade por circuitos agrupados
 * NBR 5410: agrupamento de 3-4 circuitos reduz ~20%, 5-6 reduz ~30%
 */
function calcularFatorAgrupamento(circuitosAgrupados: number): number {
  if (circuitosAgrupados <= 1) return 1.0;
  if (circuitosAgrupados <= 2) return 1.0;
  if (circuitosAgrupados <= 4) return 0.8;
  if (circuitosAgrupados <= 6) return 0.7;
  return 0.6; // Muito agrupado
}

/**
 * Diagnóstico detalhado: por que falhou?
 */
export function diagnosticarFalhas(
  validação: ValidacaoSeção
): string[] {
  const falhas: string[] = [];

  if (validação.c1.status !== 'APROVADO') {
    falhas.push(`C1 - ${validação.c1.motivo}`);
  }
  if (validação.c2.status !== 'APROVADO') {
    falhas.push(`C2 - ${validação.c2.motivo}`);
  }
  if (validação.c3.status !== 'APROVADO') {
    falhas.push(`C3(CC) - ${validação.c3.motivo}`);
  }
  if (validação.c4.status !== 'APROVADO') {
    falhas.push(`C4(SEC) - ${validação.c4.motivo}`);
  }
  if (validação.c5.status !== 'APROVADO') {
    falhas.push(`C5(QT) - ${validação.c5.motivo}`);
  }
  if (validação.c6.status !== 'APROVADO') {
    falhas.push(`C6 - ${validação.c6.motivo}`);
  }

  return falhas;
}
