# Plano de Implementação — Correção de Pontos de Iluminação

**Data:** 2026-07-06  
**Status:** Pronto para Implementação  
**Complexidade:** Baixa (mudança localizada com impacto em 2 arquivos)

---

## 1. Resumo Executivo

A tela "Dependência" exibe corretamente a quantidade de pontos de iluminação nos cards. Contudo, existe **código duplicado e inconsistente** em dois arquivos que pode causar problemas em:
- Testes automatizados
- Futuras implementações que reutilizem `dependencias-table-model.ts`
- Badges informativos (tooltip) com números errados

**Solução:** Consolidar as implementações e corrigir o uso de `pontosMin` por `quantidade`.

---

## 2. Problema Detalhado

### 2.1 Duplicação de Função

| Arquivo | Linha | Campo Usado | Status |
|---------|-------|------------|--------|
| `src/components/app/dependencias-table-model.ts` | 209-211 | `pontosMin` | ❌ INCORRETO |
| `src/components/app/TabelaDependencias.tsx` | 303-305 | `quantidade` | ✅ CORRETO |

### 2.2 Diferença Semântica

```
Exemplo: Dormitório 6m × 4m = 24 m²

✅ CORRETO (quantidade):
   - Formula: 1 + floor((24 - 6) / 4) = 1 + 4 = 5 pontos
   - Exibe: "5 pontos"

❌ INCORRETO (pontosMin):
   - Valor da tabela: 1 (mínimo normativo)
   - Exibe: "1 ponto" (errado!)
```

### 2.3 Impacto em Badges

**Linhas 981 e 1152 em `TabelaDependencias.tsx`:**
```typescript
{badgeOrigemIluminacao(item.dep, r.iluminacao.valor.pontosMin)}
```

O badge recebe `pontosMin` quando deveria receber `quantidade` para exibir o número real no tooltip.

---

## 3. Arquivos Afetados

```
src/
├── components/app/
│   ├── dependencias-table-model.ts       [CORRIGIR]
│   ├── TabelaDependencias.tsx            [CORRIGIR]
│   └── __tests__/
│       └── dependencias-table-view-model.test.ts  [VERIFICAR]
```

---

## 4. Plano de Implementação

### Fase 1: Correção de `dependencias-table-model.ts`

**Arquivo:** `src/components/app/dependencias-table-model.ts`  
**Linhas:** 209-211

**Antes:**
```typescript
const iluminacaoPrincipal = r
  ? `${r.iluminacao.valor.pontosMin} ponto${r.iluminacao.valor.pontosMin > 1 ? "s" : ""}`
  : "Nao calculado";
```

**Depois:**
```typescript
const iluminacaoPrincipal = r
  ? `${r.iluminacao.valor.quantidade} ponto${r.iluminacao.valor.quantidade > 1 ? "s" : ""}`
  : "Nao calculado";
```

**Justificativa:** Alinha com a implementação correta de `TabelaDependencias.tsx` e reflete o cálculo real baseado em NBR 5410.

---

### Fase 2: Correção de Badges em `TabelaDependencias.tsx`

**Arquivo:** `src/components/app/TabelaDependencias.tsx`  
**Linhas:** 981, 1152

**Antes:**
```typescript
// Linha 981
{badgeOrigemIluminacao(item.dep, r.iluminacao.valor.pontosMin)}

// Linha 1152
{badgeOrigemIluminacao(item.dep, r.iluminacao.valor.pontosMin)}
```

**Depois:**
```typescript
// Linha 981
{badgeOrigemIluminacao(item.dep, r.iluminacao.valor.quantidade)}

// Linha 1152
{badgeOrigemIluminacao(item.dep, r.iluminacao.valor.quantidade)}
```

**Justificativa:** O tooltip (título) do badge precisa exibir o número real, não o mínimo normativo.

---

### Fase 3: Consolidação (Opcional, Recomendado)

**Considerar no futuro:**
- Remover `mapDependenciaToRowViewModel` de `dependencias-table-model.ts` se não for utilizado em produção
- Manter apenas em `TabelaDependencias.tsx` como fonte única de verdade
- Atualizar testes para importar da localização correta

**Status:** Não é bloqueador para esta correção. Pode ser feito em refatoração posterior.

---

## 5. Testes

### 5.1 Teste Unitário (Verificar)

**Arquivo:** `src/components/app/__tests__/dependencias-table-view-model.test.ts`

```bash
npx vitest run src/components/app/__tests__/dependencias-table-view-model.test.ts
```

**O que verificar:**
- Teste atualmente usa `dependencias-table-model.ts` (a versão com erro)
- Após correção, o teste deve passar e refletir valores corretos
- Se o teste falhar, significa que o teste estava validando o comportamento **incorreto**

### 5.2 Teste Manual (Visual)

1. Abrir a aplicação: `npx vite dev`
2. Navegar para tela de Dependências
3. Visualizar cards em grid (mobile) e tabela
4. **Verificar:**
   - ✅ Número de pontos exibido corretamente (não apenas "1 ponto")
   - ✅ Badge de origem (Manual/Automático) mostra número correto ao passar o mouse
   - ✅ Secundária mostra VA total correto

### 5.3 Teste de Regressão

```bash
npx vitest run          # Todos os testes
npx eslint .            # Lint
npx tsc --noEmit        # Type checking
```

---

## 6. Checklist de Implementação

- [ ] **Fase 1:** Editar `src/components/app/dependencias-table-model.ts` (linha 210)
  - Trocar `r.iluminacao.valor.pontosMin` por `r.iluminacao.valor.quantidade`
  
- [ ] **Fase 2:** Editar `src/components/app/TabelaDependencias.tsx` (linhas 981 e 1152)
  - Trocar `r.iluminacao.valor.pontosMin` por `r.iluminacao.valor.quantidade` (2 ocorrências)
  
- [ ] **Testes:** Executar suite de testes
  ```bash
  npx vitest run src/components/app/__tests__/dependencias-table-view-model.test.ts
  ```
  
- [ ] **Verificação Manual:** Testar cards em navegador
  - Criar nova dependência com área > 6 m²
  - Verificar que mostra número correto (ex: 3, 4, 5 pontos)
  - Passar mouse no badge para verificar tooltip
  
- [ ] **Git:** Commitar mudanças
  ```bash
  git add src/components/app/dependencias-table-model.ts
  git add src/components/app/TabelaDependencias.tsx
  git commit -m "fix: corrigir quantidade de pontos de iluminação nos cards
  
  - Substituir pontosMin por quantidade em dependencias-table-model.ts
  - Corrigir badges para exibir quantidade real em TabelaDependencias.tsx
  - Alinha com cálculo NBR 5410 correto
  
  Fixes #<issue-id>"
  ```
  
- [ ] **Code Review:** Aguardar aprovação

---

## 7. Impacto Estimado

| Aspecto | Impacto |
|---------|---------|
| **Linhas Modificadas** | ~4 linhas |
| **Arquivos Afetados** | 2 |
| **Testes a Rodar** | ~2-3 testes |
| **Risco de Regressão** | ⬇️ Muito Baixo |
| **Tempo Estimado** | ~10 min (código) + ~5 min (testes) |

---

## 8. Referência de Código

### Estrutura de `resultado.iluminacao.valor`

```typescript
// src/domain/nbr/types.ts linha 151
readonly iluminacao: ItemRastreado<{
  quantidade: number;      // ← USAR ESTE
  pontosMin: number;       // ← NÃO USAR PARA EXIBIÇÃO
  vaTotal: number;
}>;
```

### Cálculo Correto

```typescript
// src/domain/calculo/iluminacao.ts linhas 38-43
const quantidade =
  d.pontosIluminacaoOverride !== undefined && d.pontosIluminacaoOverride > 0
    ? d.pontosIluminacaoOverride
    : quantidadeIluminacaoAutomatica(d);

const pontosMin = t.pontosMin;  // Sempre mínimo da tabela (ex: 1)
```

---

## 9. Rollback

Se necessário reverter:

```bash
git revert <commit-hash>
```

Não há dados persistidos afetados — é apenas correção de UI.

---

## 10. Aprovadores Recomendados

- [ ] @dev (implementação)
- [ ] @qa (testes)
- [ ] @architect (verificação de impacto)

---

**Documento Preparado por:** Atlas (Analyst)  
**Última Atualização:** 2026-07-06  
**Status:** ✅ Pronto para Implementação
