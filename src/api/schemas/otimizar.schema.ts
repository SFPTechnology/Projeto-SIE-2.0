import { z } from 'zod';

/**
 * Schema de Requisição para Auto-Otimização
 */
export const OtimizarRequestSchema = z.object({
  corrente: z
    .number()
    .min(0.1, 'Corrente deve ser > 0.1A')
    .max(500, 'Corrente deve ser ≤ 500A'),

  comprimento: z
    .number()
    .min(0, 'Comprimento não pode ser negativo')
    .max(1000, 'Comprimento máximo 1000m'),

  temperatura: z
    .number()
    .min(10, 'Temperatura mínima 10°C')
    .max(70, 'Temperatura máxima 70°C')
    .default(30),

  circuitosAgrupados: z
    .number()
    .int()
    .min(1, 'Mínimo 1 circuito')
    .max(10, 'Máximo 10 circuitos no mesmo tubo')
    .default(1),

  esquemaAterramento: z
    .enum(['TN-S', 'TN-C', 'IT'], {
      errorMap: () => ({ message: 'Esquema deve ser TN-S, TN-C ou IT' })
    })
    .default('TN-S'),

  metodoReferencia: z
    .enum(['B1', 'C', 'E'], {
      errorMap: () => ({ message: 'Método deve ser B1, C ou E' })
    })
    .default('B1'),

  protecao: z
    .number()
    .min(10, 'Proteção mínima 10A')
    .max(100, 'Proteção máxima 100A'),

  material: z
    .enum(['cobre', 'aluminio'], {
      errorMap: () => ({ message: 'Material deve ser cobre ou aluminio' })
    })
    .default('cobre'),

  isolacao: z
    .enum(['PVC', 'XLPE', 'EPR'], {
      errorMap: () => ({ message: 'Isolação deve ser PVC, XLPE ou EPR' })
    })
    .default('PVC'),

  resistenciaAterramento: z
    .number()
    .min(1, 'Resistência mínima 1Ω')
    .max(100, 'Resistência máxima 100Ω')
    .optional()
    .default(5),

  projetoId: z
    .string()
    .uuid('ID de projeto inválido')
    .optional(),

  circuitoId: z
    .string()
    .uuid('ID de circuito inválido')
    .optional()
});

export type OtimizarRequest = z.infer<typeof OtimizarRequestSchema>;

/**
 * Schema de Resposta para Auto-Otimização
 */
export const ResultadoValidacaoSchema = z.object({
  status: z.enum(['APROVADO', 'REPROVADO', 'PENDENTE']),
  motivo: z.string(),
  valor: z.number().optional(),
  limite: z.number().optional()
});

export const ValidacaoSeçaoSchema = z.object({
  c1: ResultadoValidacaoSchema.describe('Capacidade de Condução'),
  c2: ResultadoValidacaoSchema.describe('Proteção contra Sobrecarga'),
  c3: ResultadoValidacaoSchema.describe('Proteção contra Curto-Circuito'),
  c4: ResultadoValidacaoSchema.describe('Coordenação de Proteção'),
  c5: ResultadoValidacaoSchema.describe('Qualidade Técnica'),
  c6: ResultadoValidacaoSchema.describe('Verificações Adicionais')
});

export type ValidacaoSeção = z.infer<typeof ValidacaoSeçaoSchema>;

export const OtimizarResponseSchema = z.object({
  status: z.enum(['APROVADO', 'IMPOSSÍVEL_ATENDER']),
  seçãoOtimizada: z.number().nullable(),
  validações: ValidacaoSeçaoSchema.nullable(),
  tentativas: z.number().int().min(0),
  tempoMs: z.number().int().min(0),
  mensagem: z.string(),
  rastreamento: z
    .object({
      projetoId: z.string().optional(),
      circuitoId: z.string().optional(),
      timestamp: z.string().datetime(),
      versaoAlgoritmo: z.string()
    })
    .optional()
});

export type OtimizarResponse = z.infer<typeof OtimizarResponseSchema>;

/**
 * Schema para resposta de erro
 */
export const ErroResponseSchema = z.object({
  erro: z.string(),
  detalhes: z.string().optional(),
  timestamp: z.string().datetime(),
  requestId: z.string().uuid().optional()
});

export type ErroResponse = z.infer<typeof ErroResponseSchema>;
