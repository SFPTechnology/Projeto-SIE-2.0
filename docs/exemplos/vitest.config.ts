/**
 * Configuração Vitest para Testes de Quantidade TUG e Iluminação
 *
 * Vitest é uma alternativa moderna ao Jest com:
 * - Suporte nativo a TypeScript
 * - Muito mais rápido (~5-10x)
 * - Melhor integração com Vite
 * - Pool de workers customizável
 *
 * Para usar Vitest em vez de Jest:
 * 1. npm install -D vitest
 * 2. Remova jest.config.js
 * 3. Use este arquivo como vitest.config.ts
 * 4. Execute: npm test (se package.json usar vitest)
 */

import { defineConfig } from 'vitest/config';
import path from 'path';

export default defineConfig({
  test: {
    // Ambiente de teste
    environment: 'node',

    // Padrão de arquivos de teste
    include: [
      'src/**/*.test.ts',
      'src/**/*.spec.ts',
      '__tests__/**/*.test.ts'
    ],

    // Excluir arquivos
    exclude: [
      'node_modules',
      'dist',
      'build'
    ],

    // Globals (sem precisar importar describe, test, expect)
    globals: true,

    // Reportador de testes
    reporters: ['verbose'],

    // Cobertura de código
    coverage: {
      provider: 'v8', // ou 'c8'
      reporter: ['text', 'json', 'html', 'lcov'],
      exclude: [
        'node_modules/',
        'src/**/*.d.ts',
        'src/**/*.interface.ts'
      ],
      all: true,
      lines: 80,
      functions: 80,
      branches: 80,
      statements: 80
    },

    // Setup files
    setupFiles: [],

    // Timeout dos testes (ms)
    testTimeout: 10000,

    // Timeout de hook (ms)
    hookTimeout: 10000,

    // Bail - parar na primeira falha (false = executar todos)
    bail: 0,

    // Isolamento de testes
    isolate: true,

    // Threads/workers
    threads: true,
    maxThreads: 4,
    minThreads: 1,

    // Listar testes sem executá-los
    listTests: false,

    // Verbose output
    silent: false,

    // Output completo de erros
    printOutputFile: null,

    // Snapshotts
    snapshotFormat: {
      printBasicPrototype: false
    },

    // Mocking automático
    mockReset: true,
    restoreMocks: true,
    clearMocks: true
  },

  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      '@tests': path.resolve(__dirname, './__tests__')
    }
  }
});
