# QA — Resultado da Verificação: Correção P-UTF8

## Encoding UTF-8 em Mensagens de Diagnóstico

**Agente:** Quinn (QA Guardian)
**Data:** 2026-07-01
**Branch:** `feature/nbr5410-conformidade-closeout`
**Arquivos auditados:** `src/domain/distribuidora/edp-sp/validacao.ts`, `src/domain/distribuidora/edp-sp/__tests__/validacao.test.ts`
**Prompt de origem:** `C:\Users\User\Downloads\P-UTF8_Corrigir_Encoding_Mensagens_Diagnostico.md`

---

## Decisão do Gate

| Resultado | Veredicto |
|-----------|-----------|
| **GATE DECISION** | ✅ **PASS** |
| Critérios de aceite (seção 3) | 3 / 3 PASS |
| Itens da suíte de testes (seção 4) | 2 / 3 PASS, 1 / 3 N/A (justificado) |
| Regressões introduzidas | 0 |

> Nenhum "?" ou "??" corrompido remanescente em `src/` ou `tests/`. A hipótese de causa raiz do prompt original (headers HTTP/charset em backend FastAPI) **não corresponde à stack real do projeto** — não existe backend FastAPI/Python neste repositório. A causa raiz real era mojibake gravado diretamente nos literais de string do arquivo `.ts`. O critério de aceite (mensagens legíveis, sem corrupção) foi cumprido pela correção do problema real.

---

## Análise por Critério de Aceitação (seção 3 do prompt)

### CA-01 — Nenhum "??" em mensagens

**Status: ✅ PASS**

**Evidência:** Varredura com regex (`[a-záàâãéêíóôõúç]\?+[a-záàâãéêíóôõúç]`, case-insensitive) em toda a árvore `src/` e `tests/` do projeto antes e depois da correção.

**Antes** — 6 ocorrências de mojibake encontradas, todas em `edp-sp/validacao.ts` e seu teste:

| Arquivo | Linha | Trecho corrompido |
|---------|-------|--------------------|
| `validacao.ts` | 69 | `"fog?o"` |
| `validacao.ts` | 164 | `` `Descri??o "${carga.nome...` `` |
| `validacao.ts` | 165 | `` `mas o tipo selecionado ? ${...}. Confirme a classifica??o...` `` |
| `__tests__/validacao.test.ts` | 204 | `"regras configur?veis"` |
| `__tests__/validacao.test.ts` | 211 | `"Forno el?trico"` |
| `__tests__/validacao.test.ts` | 227 | `"dispara aten??o"` |
| `__tests__/validacao.test.ts` | 252 | `"dispara aten??o"` |

**Depois:** 0 ocorrências. Os únicos matches remanescentes da varredura são falsos-positivos legítimos (`?url` em imports do Vite, `?projetoId=` em query strings de teste de API) — não são mojibake.

---

### CA-02 — Acentos preservados ("Descrição", "classificação", "piscina")

**Status: ✅ PASS**

**Evidência de código (após correção, `validacao.ts:160-166`):**
```typescript
return {
  codigo: "ATN-TIPO-DIVERGENTE",
  severidade: "ATENCAO",
  mensagem:
    `Descrição "${carga.nome ?? carga.id}" sugere ${tiposEsperados.join(" / ")} ` +
    `mas o tipo selecionado é ${carga.tipoAparelho}. Confirme a classificação do projetista.` +
    (revisado ? " Revisado manualmente pelo projetista." : ""),
```

"Descrição", "classificação" e "é" restaurados com os diacríticos corretos. "Piscina" (citado no prompt) já não estava corrompido no código-fonte — as regras de bomba/piscina (`REGRAS_TIPO_DESCRICAO_PADRAO`, termo `"bomba"`) usam texto sem acento, então não havia corrupção ali.

---

### CA-03 — Caracteres especiais (ç, ã, ó) legíveis

**Status: ✅ PASS**

**Evidência:** `fog?o` → `fogão` em `validacao.ts:69` (array `REGRAS_TIPO_DESCRICAO_PADRAO`, campo `termos`). `configur?veis` → `configuráveis` e `aten??o` → `atenção` nos testes. Todos os caracteres ç/ã/ã/é/á/ção presentes nas strings corrigidas renderizam corretamente (confirmado via leitura do arquivo pós-edição e `file` reportando `UTF-8 text` sem BOM, consistente com o restante do repositório).

---

## Análise por Item da Suíte de Testes (seção 4 do prompt)

### T1 — JSON com acentos → serialização mantém UTF-8

**Status: ⚠️ N/A — hipótese de arquitetura não se aplica a este projeto**

O prompt presume um backend Python/FastAPI serializando diagnósticos via `json.dumps(..., ensure_ascii=False)`. **Este projeto não possui backend FastAPI** — é uma aplicação TanStack Start (SSR) / SPA estática em TypeScript, com `DiagnosticoEDP.mensagem` sendo uma `string` TS nativa, consumida diretamente pelos componentes React (`projetos.$projetoId_.correntes.tsx`) sem uma etapa de serialização JSON intermediária no fluxo de exibição. Não há mecanismo de "escape ASCII" equivalente ao `ensure_ascii` do Python nesta stack — o risco descrito no prompt não existe aqui. O teste foi substituído, em espírito, pela suíte `validacao.test.ts` (22/22 passando), que garante que a string `mensagem` chega correta ao consumidor.

### T2 — HTML com charset → navegador exibe acentos corretamente

**Status: ✅ PASS**

**Evidência de código (`index.html:4`):**
```html
<meta charset="UTF-8" />
```
Presente desde antes desta correção — não precisou de alteração. Confirma que o documento HTML raiz declara UTF-8 corretamente para o navegador.

### T3 — Diagnósticos → "Descrição" exibido, não "Descri??o"

**Status: ✅ PASS**

Coberto pelo teste automatizado `validacao.test.ts` (casos `ATN-TIPO-DIVERGENTE`) e por inspeção direta do literal de string corrigido (ver CA-02). Sem servidor rodando neste ambiente para captura de screenshot do runtime; validação feita por análise estática de código + suíte de testes.

---

## Resumo Executivo

```
CA-01  Nenhum "??" em mensagens                        ✅ PASS
CA-02  Acentos preservados                             ✅ PASS
CA-03  Caracteres especiais (ç, ã, ó) legíveis         ✅ PASS
T1     JSON com acentos mantém UTF-8                   ⚠️ N/A (sem backend FastAPI nesta stack)
T2     HTML com charset correto                        ✅ PASS
T3     "Descrição" exibido corretamente                ✅ PASS
```

---

## Validação Técnica

| Verificação | Resultado |
|-------------|-----------|
| `vitest run src/domain/distribuidora/edp-sp/__tests__/validacao.test.ts` | **22/22 PASS** |
| `tsc --noEmit` | 2 erros pré-existentes, **não relacionados** a esta correção (`EditarDependenciaModal.tsx:1098`, `NovaDependenciaModal.tsx:964` — `mut.mutate()` sem argumento) |
| Varredura regex de mojibake em `src/` + `tests/` | **0 ocorrências residuais** |
| Encoding de arquivo (`file` no arquivo `.ts`) | `UTF-8 text` (sem BOM), consistente com o restante do repositório |

---

## Achados Secundários

### Desvio de diagnóstico técnico no prompt de origem (fora do escopo da correção)

O documento `P-UTF8_Corrigir_Encoding_Mensagens_Diagnostico.md` presume incorretamente uma arquitetura backend FastAPI/Python para o projeto `proj-1`. A stack real (TanStack Start + Vite + Supabase, ver `CLAUDE.md` do submódulo) não possui esse componente. Isso não invalida o critério de aceite (que é sobre o resultado observável — mensagens legíveis), mas o exemplo de implementação da seção 2.1 do prompt (`fastapi.responses.JSONResponse` com `media_type`) **não é aplicável e não deve ser usado como referência futura** para este repositório.

### Causa raiz real

O mojibake estava gravado como texto literal no arquivo-fonte `.ts` (não era um problema de runtime/serialização). Isso sugere que, em algum momento, o arquivo foi editado ou salvo através de uma ferramenta/pipeline que não preservou UTF-8 corretamente (ex.: cópia via terminal com codepage incorreta no Windows, ou edição por uma ferramenta que decodificou o arquivo como Latin-1/CP1252 e regravou os bytes não mapeáveis como `?`). Recomenda-se, para prevenção, garantir que qualquer pipeline de edição automatizada (scripts, IDEs, CI) trate arquivos do repositório explicitamente como UTF-8.

---

## Ação Recomendada

Nenhuma ação corretiva adicional necessária. Todos os critérios de aceite do prompt foram cumpridos pela correção já aplicada em `validacao.ts` e `validacao.test.ts`. Recomenda-se apenas invalidar a premissa de arquitetura FastAPI do prompt original caso ele seja reaproveitado como referência em correções futuras.

---

*Relatório gerado por Quinn — guardião da qualidade 🛡️*
*Metodologia: inspeção estática de código + execução de testes automatizados (vitest, tsc) + varredura regex de encoding*
