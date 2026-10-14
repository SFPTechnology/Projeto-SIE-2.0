# Resumo — Arquivos de Testes Unitários

Todos os arquivos necessários para implementar testes de quantidade TUG e iluminação conforme NBR 5410.

---

## 📁 Arquivos Criados

### 1. **calculoQuantidade.test.ts** (Arquivo Principal de Testes)

**Localização recomendada:** `src/__tests__/calculoQuantidade.test.ts`

**O que contém:**
- 48+ testes unitários completos
- Cobertura de todas as fórmulas (F-03 a F-08, F-07-QTD)
- Testes de validação e casos extremos
- Testes de origem AUTOMATICO/MANUAL

**Tamanho:** ~700 linhas de código

**Tempo de execução:** < 1 segundo

---

### 2. **jest.config.js** (Configuração Jest)

**Localização recomendada:** Raiz do projeto

**O que contém:**
- Configuração completa para Jest
- Suporte a TypeScript (ts-jest)
- Cobertura de código configurada
- Aliases e transformadores

**Usar se:** Projeto usa Jest (padrão React/Node)

---

### 3. **vitest.config.ts** (Configuração Vitest - Alternativa)

**Localização recomendada:** Raiz do projeto

**O que contém:**
- Configuração moderna do Vitest
- Pool de workers otimizado
- Cobertura com v8
- Suporte nativo a TypeScript

**Usar se:** Projeto usa Vite ou quer alternativa mais rápida

**Vantagens do Vitest:**
- ✅ 5-10x mais rápido que Jest
- ✅ Suporte nativo a ES modules
- ✅ Melhor integração com Vite
- ✅ Menos dependências

---

### 4. **README-TESTES.md** (Guia Completo)

**Localização recomendada:** `docs/exemplos/` ou `tests/`

**O que contém:**
- Instalação passo a passo
- Comandos para executar testes
- Interpretação de resultados
- Troubleshooting
- Integração CI/CD (GitHub Actions, GitLab CI)
- Dicas profissionais

**Tamanho:** ~400 linhas

---

## 🚀 Início Rápido (3 minutos)

### Passo 1: Copiar arquivos

```bash
# Criar pasta de testes
mkdir -p src/__tests__

# Copiar arquivo de testes
cp docs/exemplos/calculoQuantidade.test.ts src/__tests__/

# Copiar configuração (escolha uma)
cp docs/exemplos/jest.config.js ./          # OU
cp docs/exemplos/vitest.config.ts ./
```

---

### Passo 2: Instalar dependências

**Para Jest:**
```bash
npm install --save-dev jest @types/jest ts-jest typescript
```

**Para Vitest:**
```bash
npm install --save-dev vitest
```

---

### Passo 3: Adicionar scripts ao package.json

```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage"
  }
}
```

Ou para Vitest:
```json
{
  "scripts": {
    "test": "vitest",
    "test:watch": "vitest --watch",
    "test:coverage": "vitest --coverage"
  }
}
```

---

### Passo 4: Executar testes

```bash
npm test
```

**Output esperado:**
```
PASS  src/__tests__/calculoQuantidade.test.ts
  F-03: Quantidade de TUG em CAT-A
    ✓ Sala 5m × 4m → 4 tomadas com carga 400 VA (12ms)
    ✓ Sala pequena 2m × 2m → mínimo 1 tomada (5ms)
  ...
  ✓ 48 passed (250ms)
```

---

## 📊 Comparação: Jest vs. Vitest

| Aspecto | Jest | Vitest |
|---------|------|--------|
| **Instalação** | npm i jest @types/jest ts-jest | npm i vitest |
| **Velocidade** | 👍 Padrão | 👍👍👍 5-10x mais rápido |
| **TypeScript** | ✓ Com ts-jest | ✓ Nativo |
| **Curva Aprendizado** | ✓ Bem documentado | ✓ Familiar se conhecer Jest |
| **Comunidade** | ✓✓✓ Muito maior | ✓✓ Crescendo |
| **Vite Integration** | ✗ Separado | ✓✓ Nativo |
| **CommonJS** | ✓✓ Ótimo | ✓ Suporta |
| **Workspace Support** | ✓ Sim | ✓ Sim |

**Recomendação:** Use **Vitest** se projeto é novo ou usa Vite. Use **Jest** se projeto é estabelecido.

---

## 📈 Estrutura de Testes por Fórmula

```
calculoQuantidade.test.ts
│
├── F-03: CAT-A (Salas, Dormitórios)
│   ├── Sala padrão 5m × 4m → 4 tomadas ✓
│   ├── Sala pequena → mínimo 1 ✓
│   ├── Com perímetro excluído ✓
│   └── Sala grande 10m × 8m ✓
│
├── F-04a: CAT-B Normal (Cozinha, Copa)
│   ├── Cozinha padrão 4m × 3m → 4 tomadas ✓
│   ├── Carga mista (3×600 + demais×100) ✓
│   ├── Cozinha grande ✓
│   └── Área de serviço ✓
│
├── F-04b: CAT-B Banheiro (Especial)
│   ├── SEMPRE 1 tomada ✓
│   ├── Perímetro não importa ✓
│   └── Carga sempre 600 VA ✓
│
├── F-06: CAT-C (Varanda, Área Externa)
│   ├── Pequena (A ≤ 6 m²) → 1 tomada ✓
│   ├── Grande (A > 6 m²) → aplica F-03 ✓
│   └── Limite crítico: 6 m² ✓
│
├── F-07-QTD: Iluminação Quantidade
│   ├── Até 6 m² → 1 ponto ✓
│   ├── 10 m² → 2 pontos ✓
│   ├── 20 m² → 4 pontos ✓
│   └── 50 m² → 12 pontos ✓
│
├── F-08: Iluminação Carga
│   ├── Até 6 m² → 100 VA ✓
│   ├── 10 m² → 160 VA ✓
│   ├── 20 m² → 280 VA ✓
│   └── Distribuição uniforme ✓
│
├── Origem AUTOMATICO vs. MANUAL
│   ├── Inicial: AUTOMATICO ✓
│   ├── Após editar: MANUAL ✓
│   ├── Permanece MANUAL ✓
│   └── Guarda quantidade original ✓
│
├── Validações
│   ├── Quantidade >= 1 ✓
│   ├── Dimensões > 0 ✓
│   └── Perímetro excluído válido ✓
│
├── Casos Extremos
│   ├── 1m × 1m (muito pequeno) ✓
│   ├── 50m × 40m (muito grande) ✓
│   └── Decimais arredondados ✓
│
└── Mapeamento Tipo → Categoria
    ├── Sala → CAT-A ✓
    ├── Cozinha → CAT-B ✓
    ├── Banheiro → CAT-B ✓
    ├── Varanda → CAT-C ✓
    └── Tipo inválido → CAT-A (default) ✓
```

---

## ✅ Checklist de Implementação

### Instalação e Setup

- [ ] Copiar `calculoQuantidade.test.ts` para `src/__tests__/`
- [ ] Copiar `jest.config.js` ou `vitest.config.ts` para raiz
- [ ] Instalar dependências: `npm install --save-dev jest @types/jest ts-jest`
- [ ] Adicionar scripts ao `package.json`
- [ ] Verificar `tsconfig.json` está configurado corretamente

### Execução Básica

- [ ] Executar `npm test` com sucesso
- [ ] Todos os 48 testes devem passar ✓
- [ ] Tempo de execução < 1 segundo
- [ ] Sem warnings de tipo TypeScript

### Cobertura

- [ ] Executar `npm run test:coverage`
- [ ] Cobertura deve ser 100% para `calcularQuantidadeTUG()`
- [ ] Cobertura deve ser 100% para `calcularQuantidadeIluminacao()`
- [ ] Cobertura deve ser 100% para `editarQuantidade()`

### Validações

- [ ] Testes de validação executam com sucesso
- [ ] Exceções são lançadas corretamente
- [ ] Mensagens de erro são claras

### Modo Watch

- [ ] Executar `npm run test:watch`
- [ ] Editar um arquivo de implementação
- [ ] Testes reexecutam automaticamente

### CI/CD

- [ ] Adicionar workflow GitHub Actions (opcional)
- [ ] Testes passam em CI/CD
- [ ] Coverage report é gerado

---

## 📝 Template para Novo Teste

Use este template para adicionar novos testes:

```typescript
describe("Nova Funcionalidade", () => {
  test("descrição clara do que está testando", () => {
    // Arrange (preparar dados)
    const entrada = {
      tipo: "sala",
      largura_m: 5,
      comprimento_m: 4,
      perimetro_excluido_m: 0
    };

    // Act (executar)
    const resultado = calcularQuantidadeTUG(entrada);

    // Assert (validar)
    expect(resultado.quantidade).toBe(4);
    expect(resultado.carga_total_va).toBe(400);
  });

  test("cenário de exceção", () => {
    expect(() => {
      calcularQuantidadeTUG({
        tipo: "sala",
        largura_m: -5, // Inválido
        comprimento_m: 4,
        perimetro_excluido_m: 0
      });
    }).toThrow("Largura deve ser > 0");
  });
});
```

---

## 🔍 Argumentos de CLI Úteis

```bash
# Executar apenas um arquivo de teste
npm test calculoQuantidade.test.ts

# Executar testes que correspondem a um padrão
npm test -- --testNamePattern="F-03"

# Executar apenas testes que falharam na última vez
npm test -- --onlyChanged

# Gerar coverage HTML
npm test -- --coverage --coverageReporters=html

# Executar em modo debug
npm test -- --inspect-brk --runInBand

# Watch com re-execução em qualquer arquivo
npm test -- --watch --watchAll

# Limpar cache
npm test -- --clearCache
```

---

## 📚 Referências Rápidas

### Assertivas Mais Usadas

```typescript
// Igualdade
expect(value).toBe(expectedValue);
expect(value).toEqual({ a: 1 });

// Comparações
expect(value).toBeGreaterThan(5);
expect(value).toBeLessThanOrEqual(10);

// Null/Undefined
expect(value).toBeNull();
expect(value).toBeUndefined();
expect(value).toBeDefined();

// Booleanos
expect(value).toBeTruthy();
expect(value).toBeFalsy();

// Arrays/Strings
expect(array).toContain("item");
expect(string).toMatch(/pattern/);
expect(array).toHaveLength(3);

// Exceções
expect(() => func()).toThrow();
expect(() => func()).toThrow("message");
```

### Hooks de Teste

```typescript
describe("Suite", () => {
  beforeAll(() => {
    // Executado uma vez ANTES de todos os testes
  });

  beforeEach(() => {
    // Executado ANTES de cada teste
  });

  afterEach(() => {
    // Executado DEPOIS de cada teste
  });

  afterAll(() => {
    // Executado uma vez DEPOIS de todos os testes
  });

  test("teste", () => {});
});
```

---

## 🐛 Debugging

### Ver output completo de um teste

```typescript
test("debug", () => {
  const result = calcularQuantidadeTUG({...});
  
  // Imprime no console
  console.log("Resultado:", JSON.stringify(result, null, 2));
  
  // Ou use debugger
  debugger;
});
```

Executar com:
```bash
node --inspect-brk node_modules/.bin/jest --runInBand
```

---

## 📊 Métricas Esperadas

| Métrica | Valor Esperado |
|---------|---|
| Testes Totais | 48+ |
| Taxa de Passou | 100% ✓ |
| Tempo Execução | < 1 segundo |
| Cobertura Linhas | 100% |
| Cobertura Branches | 100% |
| Cobertura Funções | 100% |

---

## 🎯 Próximas Etapas

1. **Implementar funções:** Criar `src/services/calculoQuantidade.ts`
2. **Adicionar testes de integração:** Testar com banco de dados
3. **Setup CI/CD:** GitHub Actions ou GitLab CI
4. **Coverage reports:** Publicar em Codecov ou similar
5. **Performance:** Monitorar tempo de execução

---

## 📞 Suporte

Se encontrar problemas:

1. Leia **README-TESTES.md** (troubleshooting)
2. Verifique **jest.config.js** ou **vitest.config.ts**
3. Limpe cache: `npm test -- --clearCache`
4. Reinstale: `rm -rf node_modules && npm install`

---

**Versão:** 1.0  
**Data:** 2026-07-05  
**Autor:** Atlas - Business Analyst  
**Status:** Pronto para usar ✅
