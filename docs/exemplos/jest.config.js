/**
 * Configuração Jest para Testes de Quantidade TUG e Iluminação
 *
 * Coloque este arquivo na raiz do projeto ou em uma pasta específica
 * Local sugerido: jest.config.js (raiz) ou config/jest.config.js
 */

module.exports = {
  // Ambiente de teste
  testEnvironment: 'node',

  // Preset TypeScript (se usar ts-jest)
  preset: 'ts-jest',

  // Padrão de arquivos de teste
  testMatch: [
    '**/__tests__/**/*.test.ts',
    '**/?(*.)+(spec|test).ts'
  ],

  // Módulos de setup
  setupFilesAfterEnv: [],

  // Cobertura de código
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.d.ts',
    '!src/**/*.interface.ts',
    '!src/**/index.ts'
  ],

  // Limite de cobertura (opcional - aumentar conforme necessário)
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    }
  },

  // Mapear aliases (se usar)
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1'
  },

  // Transformadores
  transform: {
    '^.+\\.tsx?$': ['ts-jest', {
      tsconfig: {
        jsx: 'react',
        esModuleInterop: true,
        allowSyntheticDefaultImports: true
      }
    }]
  },

  // Extensões de módulo
  moduleFileExtensions: ['ts', 'tsx', 'js', 'jsx', 'json', 'node'],

  // Timeout de testes (ms)
  testTimeout: 5000,

  // Verbose output
  verbose: true
};
