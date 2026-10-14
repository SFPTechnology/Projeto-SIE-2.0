# Índice Completo — Testes Unitários NBR 5410

Guia de navegação para todos os arquivos criados para testes de quantidade TUG e iluminação.

---

## 📋 Documentação Principal

### 1. **TUTORIAL-NBR5410-Quantidade-TUG-Iluminacao.md**
📁 Localização: `docs/TUTORIAL-NBR5410-Quantidade-TUG-Iluminacao.md`

**Seções:**
- Introdução: O que é Quantidade de TUG
- As 4 Categorias (CAT-A, CAT-B, CAT-C)
- Passo a Passo: Calcular TUG (6 passos)
- Entendendo as Fórmulas Normativas (F-03 a F-06)
- Pontos de Iluminação: Nova Sistemática (F-07-QTD, F-08)
- Origem Automática vs. Manual
- Exemplo Prático Completo (3 cômodos)
- Implementação Técnica (TypeScript)
- **NOVO: Testes Unitários (Seção 10)** ← 48 testes com exemplos
- FAQ — Dúvidas Comuns
- Checklist de Implementação

**Tamanho:** ~2.500 linhas

**Tempo de leitura:** 45-60 minutos

**Melhor para:** Entender a lógica de cálculo e começar do zero

---

## 🧪 Arquivos de Testes

### 2. **calculoQuantidade.test.ts**
📁 Localização: `docs/exemplos/calculoQuantidade.test.ts`

**O que é:** Arquivo completo de testes unitários pronto para usar

**Contém:**
- 48+ testes unitários
- Cobertura de todas as fórmulas (F-03, F-04a, F-04b, F-06, F-07-QTD, F-08)
- Testes de origem AUTOMATICO/MANUAL
- Testes de validações
- Testes de casos extremos
- Testes de mapeamento tipo → categoria

**Tamanho:** ~700 linhas

**Como usar:**
```bash
# Copiar para o projeto
cp docs/exemplos/calculoQuantidade.test.ts src/__tests__/

# Instalar Jest
npm install --save-dev jest @types/jest ts-jest

# Executar
npm test
```

**Exemplo de teste:**
```typescript
test("Sala 5m × 4m → 4 tomadas com carga 400 VA", () => {
  const result = calcularQuantidadeTUG({
    tipo: "sala",
    largura_m: 5,
    comprimento_m: 4,
    perimetro_excluido_m: 0
  });

  expect(result.quantidade).toBe(4);
  expect(result.carga_total_va).toBe(400);
});
```

---

## ⚙️ Configurações

### 3. **jest.config.js**
📁 Localização: `docs/exemplos/jest.config.js`

**O que é:** Configuração pronta do Jest (framework de testes padrão)

**Inclui:**
- Suporte a TypeScript via ts-jest
- Configuração de cobertura
- Aliases de módulo
- Transformadores

**Quando usar:** Se projeto usa Jest (React, Node.js tradicional)

**Instalação:**
```bash
npm install --save-dev jest @types/jest ts-jest
cp docs/exemplos/jest.config.js ./
```

---

### 4. **vitest.config.ts**
📁 Localização: `docs/exemplos/vitest.config.ts`

**O que é:** Configuração moderna do Vitest (alternativa ao Jest)

**Vantagens:**
- ✅ 5-10x mais rápido que Jest
- ✅ Suporte nativo a TypeScript
- ✅ Melhor integração com Vite
- ✅ Menos dependências

**Quando usar:** Se projeto é novo ou usa Vite

**Instalação:**
```bash
npm install --save-dev vitest
cp docs/exemplos/vitest.config.ts ./
```

---

## 📚 Guias e Referências

### 5. **README-TESTES.md**
📁 Localização: `docs/exemplos/README-TESTES.md`

**Seções:**
- 📦 Instalação passo a passo
- 🚀 Executando testes (comando por comando)
- 📊 Estrutura dos testes
- ✅ Casos de teste cobertos (com tabelas)
- 🔍 Interpretando resultados
- 🛠️ Troubleshooting (5 problemas + soluções)
- 📈 Melhorando cobertura
- 🔄 Integração com CI/CD (GitHub Actions, GitLab)
- ✨ Dicas profissionais

**Tamanho:** ~400 linhas

**Melhor para:** Implementação prática dos testes

**Exemplo de comando:**
```bash
# Executar todos os testes
npm test

# Modo watch (reexecuta ao salvar)
npm run test:watch

# Com cobertura
npm run test:coverage

# Apenas testes de F-03
npm test -- --testNamePattern="F-03"
```

---

### 6. **RESUMO-ARQUIVOS-TESTES.md**
📁 Localização: `docs/exemplos/RESUMO-ARQUIVOS-TESTES.md`

**Seções:**
- 📁 Todos os arquivos criados (com descrição)
- 🚀 Início rápido (3 minutos)
- 📊 Comparação Jest vs. Vitest
- 📈 Estrutura de testes por fórmula
- ✅ Checklist de implementação completo
- 📝 Template para novo teste
- 📚 Referências rápidas (assertivas, hooks)
- 🐛 Debugging
- 📊 Métricas esperadas

**Tamanho:** ~350 linhas

**Melhor para:** Visão geral e comparações

---

## 📊 Tabela Comparativa

| Arquivo | Tipo | Tamanho | Tempo Leitura | Melhor Para |
|---------|------|---------|---|---|
| **TUTORIAL** | 📚 Guia completo | 2.500 linhas | 45-60 min | Entender a lógica |
| **calculoQuantidade.test.ts** | 🧪 Testes | 700 linhas | 30 min | Implementar tests |
| **jest.config.js** | ⚙️ Config | 40 linhas | 5 min | Setup Jest |
| **vitest.config.ts** | ⚙️ Config | 50 linhas | 5 min | Setup Vitest |
| **README-TESTES.md** | 📖 Guia prático | 400 linhas | 20 min | Executar testes |
| **RESUMO-ARQUIVOS-TESTES.md** | 📋 Índice | 350 linhas | 15 min | Visão geral |
| **INDEX.md** | 🗂️ Este arquivo | 200 linhas | 10 min | Navegar tudo |

**Total:** ~4.200+ linhas de documentação e código pronto para usar

---

## 🎯 Fluxo de Uso Recomendado

### Para Iniciante

```
1. Leia o TUTORIAL (seção 1-4) → 20 min
   ↓
2. Leia RESUMO-ARQUIVOS-TESTES (visão geral) → 10 min
   ↓
3. Copie calculoQuantidade.test.ts
   ↓
4. Copie jest.config.js (ou vitest.config.ts)
   ↓
5. Instale dependências → npm install --save-dev jest
   ↓
6. Execute testes → npm test
   ↓
7. Leia README-TESTES.md (se tiver dúvidas)
```

### Para Experiente

```
1. Copie calculoQuantidade.test.ts
   ↓
2. Copie jest.config.js
   ↓
3. npm install --save-dev jest
   ↓
4. npm test
   ↓
5. Modifique conforme necessário
```

---

## 📈 Cobertura de Testes

### Fórmulas Testadas

| Fórmula | Descrição | Testes | Status |
|---------|-----------|--------|--------|
| **F-03** | CAT-A: ceil(P/5) | 4 | ✅ |
| **F-04a** | CAT-B Normal: ceil(P/3.5) | 5 | ✅ |
| **F-04b** | CAT-B Banheiro: 1 | 4 | ✅ |
| **F-06** | CAT-C: condicional | 4 | ✅ |
| **F-07-QTD** | Iluminação: 1+floor((A-6)/4) | 5 | ✅ |
| **F-08** | Iluminação carga: 100+60×floor((A-6)/4) | 5 | ✅ |
| **Origem** | AUTOMATICO/MANUAL | 5 | ✅ |
| **Validações** | Entrada inválida | 5 | ✅ |
| **Casos Extremos** | Limites mín/máx | 5 | ✅ |
| **Mapeamento** | Tipo → Categoria | 6 | ✅ |

**Total:** 48+ testes

---

## 🚀 Instalação Rápida (Copiar-Colar)

### Opção 1: Jest (Padrão)

```bash
# 1. Instalar
npm install --save-dev jest @types/jest ts-jest

# 2. Copiar arquivos
cp docs/exemplos/calculoQuantidade.test.ts src/__tests__/
cp docs/exemplos/jest.config.js ./

# 3. Adicionar scripts (no package.json)
# "test": "jest"
# "test:watch": "jest --watch"
# "test:coverage": "jest --coverage"

# 4. Executar
npm test
```

### Opção 2: Vitest (Moderno)

```bash
# 1. Instalar
npm install --save-dev vitest

# 2. Copiar arquivos
cp docs/exemplos/calculoQuantidade.test.ts src/__tests__/
cp docs/exemplos/vitest.config.ts ./

# 3. Adicionar scripts (no package.json)
# "test": "vitest"
# "test:watch": "vitest --watch"
# "test:coverage": "vitest --coverage"

# 4. Executar
npm test
```

---

## ✅ Checklist Final

- [ ] Leu o TUTORIAL (entende a lógica)
- [ ] Leu RESUMO-ARQUIVOS-TESTES (sabe o que tem onde)
- [ ] Copiou calculoQuantidade.test.ts
- [ ] Copiou jest.config.js ou vitest.config.ts
- [ ] Instalou dependências
- [ ] Executou `npm test` com sucesso
- [ ] Todos os 48 testes passaram ✓
- [ ] Cobertura é 100%
- [ ] Leu README-TESTES.md (para debugging)

---

## 🔗 Navegação Rápida

### Por Interesse

**💡 "Quero entender como calcular TUG"**
→ TUTORIAL seção 3-4

**🧪 "Quero ver testes prontos"**
→ calculoQuantidade.test.ts

**⚙️ "Quero configurar o Jest"**
→ jest.config.js + README-TESTES seção 1

**🚀 "Quero começar AGORA"**
→ RESUMO-ARQUIVOS-TESTES seção "Início Rápido"

**🐛 "Tenho um problema"**
→ README-TESTES seção "Troubleshooting"

**📊 "Quero comparar Jest vs. Vitest"**
→ RESUMO-ARQUIVOS-TESTES seção "Comparação"

**📈 "Quero adicionar mais testes"**
→ RESUMO-ARQUIVOS-TESTES seção "Template para Novo Teste"

---

## 📞 Referências

### Documentos do Projeto

- 📄 `docs/TUTORIAL-NBR5410-Quantidade-TUG-Iluminacao.md` — Tutorial principal
- 📄 `docs/NBR5410-Quantidade-TUG-Iluminacao-Sistematica.md` — Documento técnico original
- 📄 `docs/REFERENCIA-INTEGRAL-SISTEMA.md` — Fórmulas NBR

### Frameworks de Teste

- 🔗 [Jest Documentation](https://jestjs.io/) — Framework padrão
- 🔗 [Vitest Documentation](https://vitest.dev/) — Alternativa moderna
- 🔗 [Testing Library](https://testing-library.com/) — Para testes de UI

### Normas

- 📋 NBR 5410:2004 — Instalações Elétricas de Baixa Tensão

---

## 📝 Versão e Histórico

**Versão Atual:** 1.0  
**Data:** 2026-07-05  
**Autor:** Atlas - Business Analyst  
**Status:** ✅ Completo e pronto para uso

---

## 🎁 Bonus: Exemplos de Uso

### Exemplo 1: Sala de 20 m²

```typescript
test("Sala 20 m² → 4 TUG + 4 pontos iluminação", () => {
  // TUG
  const tug = calcularQuantidadeTUG({
    tipo: "sala",
    largura_m: 5,
    comprimento_m: 4
  });
  expect(tug.quantidade).toBe(4); // 4 tomadas
  expect(tug.carga_total_va).toBe(400); // 400 VA

  // Iluminação
  const ilum = calcularQuantidadeIluminacao({
    tipo: "sala",
    largura_m: 5,
    comprimento_m: 4
  });
  expect(ilum.quantidade).toBe(4); // 4 pontos
  expect(ilum.carga_total_va).toBe(280); // 280 VA
});
```

### Exemplo 2: Editar com Origem Manual

```typescript
test("Usuário edita quantidade para 5 por layout especial", async () => {
  const dep = { id: "dep-001", tipo: "sala" };
  
  await editarQuantidade(dep, "TUG", 5, "Layout exige 5");
  
  expect(dep.resultado.tomadas.origem).toBe("MANUAL");
  expect(dep.resultado.tomadas.quantidade).toBe(5);
  expect(dep.resultado.tomadas.justificativa).toBe("Layout exige 5");
});
```

---

**Aproveite! 🚀**

Todos os arquivos estão prontos para usar. Dúvidas? Consulte README-TESTES.md ou o TUTORIAL.
