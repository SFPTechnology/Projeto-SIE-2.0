# Testes Unitários — Sistemática de Quantidade TUG e Iluminação

Guia completo para instalar e executar os testes das fórmulas NBR 5410.

## 📦 Instalação

### Passo 1: Instalar dependências

```bash
# Com npm
npm install --save-dev jest @types/jest ts-jest typescript

# Ou com yarn
yarn add --dev jest @types/jest ts-jest typescript

# Ou com pnpm
pnpm add -D jest @types/jest ts-jest typescript
```

### Passo 2: Copiar arquivos de teste

1. Copie `calculoQuantidade.test.ts` para `src/__tests__/` ou `tests/`
2. Copie `jest.config.js` para a raiz do projeto
3. (Opcional) Atualize `tsconfig.json` para compilação correta

### Passo 3: Atualizar package.json

Adicione estes scripts à seção `"scripts"`:

```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "test:debug": "node --inspect-brk node_modules/.bin/jest --runInBand",
    "test:quantity": "jest calculoQuantidade.test.ts"
  }
}
```

---

## 🚀 Executando os Testes

### Executar todos os testes

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
  F-04a: Quantidade de TUG em CAT-B Normal
    ✓ Cozinha 4m × 3m → 4 tomadas com carga mista 1.900 VA (8ms)
    ...
  ✓ 45 passed (250ms)
```

---

### Modo watch (reexecuta automaticamente ao salvar)

```bash
npm run test:watch
```

Útil durante desenvolvimento — o Jest reexecuta os testes conforme você edita o código.

---

### Cobertura de código

```bash
npm run test:coverage
```

**Output esperado:**
```
----------|---------|---------|---------|---------|------|
File      | % Stmts | % Branch| % Funcs | % Lines | Unc |
----------|---------|---------|---------|---------|------|
All files |   100   |   100   |   100   |   100   | — |
calculoQuantidade.ts | 100 | 100 | 100 | 100 | — |
----------|---------|---------|---------|---------|------|

COVERAGE: 100% of statements, 100% of branches, 100% of functions
```

---

### Testes específicos

```bash
# Apenas testes de F-03 (CAT-A)
npm test -- --testNamePattern="F-03"

# Apenas testes de validação
npm test -- --testNamePattern="Validações"

# Apenas testes de iluminação
npm test -- --testNamePattern="Iluminação"

# Apenas testes de origem AUTOMATICO/MANUAL
npm test -- --testNamePattern="Origem"
```

---

### Debug de testes

```bash
npm run test:debug
```

Abre o Chrome DevTools para debug interativo. Útil quando algo falha.

---

## 📊 Estrutura dos Testes

### Organizados por Fórmula

```
calculoQuantidade.test.ts
├── F-03: CAT-A (4 testes)
├── F-04a: CAT-B Normal (5 testes)
├── F-04b: CAT-B Banheiro (4 testes)
├── F-06: CAT-C (4 testes)
├── F-07-QTD: Iluminação Quantidade (5 testes)
├── F-08: Iluminação Carga (5 testes)
├── Origem AUTOMATICO/MANUAL (5 testes)
├── Validações (5 testes)
├── Casos Extremos (5 testes)
└── Mapeamento Tipo → Categoria (6 testes)
```

**Total: 48 testes**

---

## ✅ Casos de Teste Cobertos

### F-03: CAT-A (Salas, Dormitórios)

| Teste | Entrada | Saída Esperada |
|-------|---------|---|
| 1 | Sala 5m × 4m | 4 tomadas, 400 VA |
| 2 | Sala 2m × 2m | ≥ 1 tomada |
| 3 | Com perímetro excluído | Quantidade reduzida |
| 4 | Sala 10m × 8m | 8 tomadas, 800 VA |

---

### F-04a: CAT-B Normal (Cozinha, Copa, Área de Serviço)

| Teste | Entrada | Saída Esperada |
|-------|---------|---|
| 1 | Cozinha 4m × 3m | 4 tomadas, 1.900 VA |
| 2 | Copa 2m × 2m | 3 tomadas, 1.800 VA |
| 3 | Cozinha 6m × 5m | 7 tomadas, 2.200 VA |
| 4 | Carga mista | 3×600 + demais×100 |
| 5 | Área de serviço | Aplica F-04a |

---

### F-04b: CAT-B Banheiro

| Teste | Entrada | Saída Esperada |
|-------|---------|---|
| 1 | Banheiro 2m × 1.5m | Sempre 1 tomada, 600 VA |
| 2 | Banheiro 4m × 3m | Sempre 1 tomada (perímetro não importa) |
| 3 | Com perímetro excluído | Sempre 1 tomada |
| 4 | Banheiro extra-grande | Sempre 1 tomada |

---

### F-06: CAT-C (Varanda, Área Externa)

| Teste | Entrada | Saída Esperada |
|-------|---------|---|
| 1 | Varanda 3m × 2m (6 m²) | 1 tomada (A ≤ 6) |
| 2 | Varanda 4m × 2m (8 m²) | 3 tomadas (aplica F-03) |
| 3 | Limite 6 m² | Inclusivo em A ≤ 6 |
| 4 | Área 8m × 5m (40 m²) | 6 tomadas |

---

### F-07-QTD: Iluminação Quantidade

| Teste | Entrada | Saída Esperada |
|-------|---------|---|
| 1 | Sala 6 m² | 1 ponto |
| 2 | Sala 10 m² | 2 pontos |
| 3 | Sala 20 m² | 4 pontos |
| 4 | Sala 50 m² | 12 pontos |
| 5 | Banheiro 3 m² | 1 ponto |

---

### F-08: Iluminação Carga

| Teste | Entrada | Saída Esperada |
|-------|---------|---|
| 1 | Área ≤ 6 m² | 100 VA |
| 2 | Área 10 m² | 160 VA |
| 3 | Área 20 m² | 280 VA |
| 4 | Área 50 m² | 760 VA |
| 5 | Distribuição uniforme | carga_por_ponto = total/qtd |

---

### Origem AUTOMATICO vs. MANUAL

| Teste | Ação | Resultado |
|-------|------|-----------|
| 1 | Cálculo inicial | origem = AUTOMATICO |
| 2 | Editar quantidade | origem muda para MANUAL |
| 3 | Editar novamente | origem permanece MANUAL |
| 4 | Guardar original | quantidade_automatica preservada |
| 5 | Badge visual | [A] ou [M] |

---

### Validações

| Teste | Entrada Inválida | Exceção Esperada |
|-------|---|---|
| 1 | Quantidade < 1 | "Quantidade deve ser >= 1" |
| 2 | Largura ≤ 0 | "Largura deve ser > 0" |
| 3 | Comprimento ≤ 0 | "Comprimento deve ser > 0" |
| 4 | Perímetro excluído < 0 | "...não pode ser negativo" |
| 5 | Perímetro excluído > total | "...maior que perímetro total" |

---

## 🔍 Interpretando Resultados

### Teste Passou ✓

```
✓ Sala 5m × 4m → 4 tomadas com carga 400 VA (12ms)
```

Significa que:
- A função retornou a quantidade esperada (4)
- A carga foi calculada corretamente (400 VA)
- O teste executou em 12ms (performance boa)

---

### Teste Falhou ✗

```
✗ Sala 5m × 4m → 4 tomadas com carga 400 VA
  Expected: 4
  Received: 3
```

Significa que:
- A função retornou 3, mas esperávamos 4
- Há um bug na fórmula ou lógica
- Verifique a implementação de `calcularQuantidadeTUG()`

---

### Assertivas Comuns

```typescript
// Testa igualdade
expect(result.quantidade).toBe(4);

// Testa intervalo
expect(result.quantidade).toBeGreaterThanOrEqual(1);

// Testa tipo
expect(result.origem).toBe("AUTOMATICO");

// Testa nulidade
expect(result.justificativa).toBeNull();

// Testa valor em array
expect(["CAT-A", "CAT-B", "CAT-C"]).toContain(result.categoria);

// Testa exception
expect(() => funcao()).toThrow("mensagem de erro");
```

---

## 🛠️ Troubleshooting

### Problema: "Cannot find module 'jest'"

**Solução:**
```bash
npm install jest @types/jest ts-jest --save-dev
```

---

### Problema: "TypeScript compiler version mismatch"

**Solução:**
```bash
npm install typescript --save-dev
npx tsc --version  # Verifique a versão
```

---

### Problema: Testes passam localmente mas falham em CI/CD

**Solução:** Atualize `jest.config.js` com:
```javascript
{
  testEnvironment: 'node',
  detectOpenHandles: true,
  forceExit: true
}
```

---

### Problema: Coverage está baixa

**Solução:** Verifique se todos os arquivos estão incluídos:
```bash
npm test -- --coverage --collectCoverageFrom="src/**/*.ts"
```

---

## 📈 Melhorando Cobertura

Adicionar mais testes:

```typescript
describe("Novo caso de teste", () => {
  test("Descrição clara do que está testando", () => {
    const resultado = calcularQuantidadeTUG({
      // ... entrada ...
    });

    expect(resultado).toMatchObject({
      quantidade: 5,
      origem: "AUTOMATICO"
    });
  });
});
```

---

## 🔄 Integração com CI/CD

### GitHub Actions

```yaml
# .github/workflows/tests.yml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '18'
      - run: npm ci
      - run: npm test -- --coverage
      - run: npm run test:coverage
```

### GitLab CI

```yaml
# .gitlab-ci.yml
test:
  image: node:18
  script:
    - npm ci
    - npm test -- --coverage
  coverage: '/Coverage: \d+\.\d+%/'
```

---

## 📚 Referências

- **Jest Docs:** https://jestjs.io/
- **TypeScript + Jest:** https://jestjs.io/docs/getting-started#using-typescript
- **Testing Best Practices:** https://jestjs.io/docs/tutorial-react#snapshot-testing

---

## ✨ Dicas Profissionais

1. **Use `test.each()`** para testes paramétricos:
   ```typescript
   test.each([
     [5, 4, 4],
     [2, 2, 1],
     [10, 8, 8]
   ])("Sala %dm × %dm → %d tomadas", (l, c, qtd) => {
     const result = calcularQuantidadeTUG({ 
       tipo: "sala", 
       largura_m: l, 
       comprimento_m: c 
     });
     expect(result.quantidade).toBe(qtd);
   });
   ```

2. **Use `describe.only()`** para executar apenas um bloco:
   ```typescript
   describe.only("F-03", () => {
     // ... testes ...
   });
   ```

3. **Use `test.skip()`** para pular um teste:
   ```typescript
   test.skip("Teste em progresso", () => {
     // Não executado
   });
   ```

4. **Use snapshots** para resultados complexos:
   ```typescript
   expect(resultado).toMatchSnapshot();
   ```

---

**Última atualização:** 2026-07-05  
**Autor:** Atlas - Business Analyst  
**Versão:** 1.0
