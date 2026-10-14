# SIE — Design System da Camada de Visualização (v1.0 · Julho 2026)
## Tokens, primitivas e critérios de validação de interface

**Fonte da direção visual:** SIE-REFERENCIA-COMPLETA.md, Seções 8 e 10 (padrões
observados no sistema em produção — tema escuro g100, Carbon, badges, rastreio inline).
**Arquivos canônicos:** `tokens_sie.css` (única fonte de cor/tipo/espaço) e
`primitivas_validacao.tsx` (badges, rastreio, faixas). Componentes da Camada B
não usam hex literal nem markup ad hoc de estado.

---

## 1. Princípios

1. **Estado normativo tem gramática visual fixa.** Severidade (INFO/ATENÇÃO/ERRO)
   e disciplina ([VERIFICAR]/Modificado/A-M) são sistemas distintos — cores e
   formas próprias, nunca intercambiáveis (Seção 8 da referência).
2. **Todo valor calculado exibe rastreio.** Nenhum número aparece sem a fórmula
   com substituição literal (`IB = S / V; S=340 VA; V=127 V`) via `RastreioInline`,
   recebida pronta do backend (RG-02: a UI não monta cálculo).
3. **Contraste é verificado, não presumido.** Cada par texto/fundo dos tokens tem
   razão WCAG calculada programaticamente (§3). Pares reprovados são proibidos e
   documentados (ex.: branco sobre `--sie-erro-fill`).
4. **Tema escuro é o padrão; impressão inverte.** `@media print` troca para traço
   escuro sobre branco (RNF-08) sem alterar componente.

## 2. Tokens (resumo — canônico em tokens_sie.css)

| Grupo | Tokens principais |
|---|---|
| Superfície | `--sie-fundo` #161616 · `--sie-camada` #262626 |
| Texto | `--sie-texto` #f4f4f4 · `--sie-texto-sec` #c6c6c6 · `--sie-link` #78a9ff |
| Interação | `--sie-interativo` #0f62fe · `--sie-foco` #ffffff · `--sie-selecao-fundo` #001d6c |
| Severidade | `--sie-info(-fill)` #4589ff · `--sie-atencao(-fill)` #f1c21b · `--sie-erro(-fill)` #fa4d56 |
| Disciplina | `--sie-verificar-fill` #393939 · `--sie-modificado-fill` #0043ce · origem A/M |
| Diagrama | `--sie-diagrama-traco` #f4f4f4 · tracejado de pendência `5 4` · espessura 1.5px |
| Tipo | IBM Plex Sans (UI) · IBM Plex Mono (rastreio/valores) · 12/14/20px |

Encadeamento: `var(--cds-*, fallback)` — onde o Carbon do projeto estiver
carregado, os tokens oficiais prevalecem; os fallbacks reproduzem o g100.

## 3. Evidência de contraste (WCAG 2.1 — calculada, RNF-01)

| Par | Razão | Alvo | Resultado |
|---|---|---|---|
| texto-primário / fundo | 16,45:1 | 4,5:1 | PASS |
| texto-secundário / fundo | 10,59:1 | 4,5:1 | PASS |
| texto-primário / camada | 13,76:1 | 4,5:1 | PASS |
| texto-secundário / camada | 8,86:1 | 4,5:1 | PASS |
| link #78a9ff / fundo | 7,68:1 | 4,5:1 | PASS |
| texto branco / botão #0f62fe | 5,00:1 | 4,5:1 | PASS |
| info como texto / fundo | 5,41:1 | 4,5:1 | PASS |
| badge INFO #001d6c / #4589ff | 4,51:1 | 4,5:1 | PASS |
| badge ATENÇÃO #161616 / #f1c21b | 10,75:1 | 4,5:1 | PASS |
| badge ERRO #161616 / #fa4d56 | 5,40:1 | 4,5:1 | PASS |
| **badge ERRO branco / #fa4d56** | **3,35:1** | 4,5:1 | **FAIL — PROIBIDO** |
| badge [VERIFICAR] #e0e0e0 / #393939 | 8,75:1 | 4,5:1 | PASS |
| badge Modificado #d0e2ff / #0043ce | 5,94:1 | 4,5:1 | PASS |
| traço do diagrama / fundo | 16,45:1 | 4,5:1 | PASS |
| atenção como texto / fundo | 10,75:1 | 4,5:1 | PASS |
| erro como texto / fundo | 5,40:1 | 4,5:1 | PASS |
| foco / fundo | 18,10:1 | 3:1 | PASS |
| borda interativa #6f6f6f / fundo | 3,60:1 | 3:1 (não-texto) | PASS |
| borda interativa / camada | 3,01:1 | 3:1 (não-texto) | PASS |
| borda sutil #393939 / fundo | 1,57:1 | — | decorativa (isenta 1.4.11); NÃO usar como limite de componente interativo |

Script de verificação: qualquer alteração de token exige recalcular (o script de
1 tela em Python está registrado no histórico da sessão; incorporar como
`tests/test_ds_contraste.py` é o critério DS-10).

## 4. Primitivas (primitivas_validacao.tsx)

| Primitiva | Uso obrigatório |
|---|---|
| `BadgeSeveridade` | Todo diagnóstico INFO/ATENÇÃO/ERRO em card, linha do unifilar, memorial |
| `BadgeVerificar` | Todo campo pendente de confirmação humana — nunca texto solto "[VERIFICAR]" estilizado ad hoc |
| `BadgeModificado` | Linhas de tabela EDP editadas pelo projetista |
| `BadgeOrigem` | Ao lado de todo valor com origem automática/manual |
| `RastreioInline` | Sob todo valor calculado (fórmula + substituição do backend) |
| `FaixaProvisoria` | Topo de TODO artefato quando `payload.provisorio === true` (R-04) |
| `ListaPendencias` | Bloco de pendências no memorial do circuito |

## 5. Critérios de validação da interface (DS-01 a DS-10)

Para uso no E2/E5/E6 do ROTEIRO-CAMADA-B (somam-se aos UF/PE/MF):

- **DS-01** Nenhum hex literal em componente da Camada B — só `var(--sie-*)`
  (guarda: `grep -rnE "#[0-9a-fA-F]{3,6}" --include="*.tsx" <dirs>` deve retornar
  apenas `tokens_sie.css` e fallbacks dentro de `var(`).
- **DS-02** Severidade renderizada exclusivamente via `BadgeSeveridade`; cores
  conferem com Seção 8 (INFO azul, ATENÇÃO amarelo, ERRO vermelho).
- **DS-03** `[VERIFICAR]` renderizado exclusivamente via `BadgeVerificar` —
  cinza neutro, nunca amarelo/vermelho (não é severidade).
- **DS-04** Badge ERRO jamais com texto branco (evidência §3 — 3,35:1 reprova).
- **DS-05** Todo valor calculado visível acompanha `RastreioInline` com a fórmula
  do backend.
- **DS-06** `FaixaProvisoria` presente em todo artefato com `provisorio=true`.
- **DS-07** Foco visível em todo elemento interativo (anel `--sie-foco`, offset 1px);
  navegação Tab+Enter íntegra (reforça UF-06).
- **DS-08** Impressão: unifilar e quadros legíveis em A4/A3 com o tema print
  (traço escuro/fundo branco) — validar preview de impressão (RNF-08).
- **DS-09** Tipografia: valores/fórmulas em Plex Mono; UI em Plex Sans; nenhum
  outro font-family.
- **DS-10** Teste automatizado de contraste dos tokens (`test_ds_contraste.py`)
  presente e verde — recalcula as razões do §3 a partir do CSS.

## 6. Integração

```tsx
import "./tokens_sie.css";  // uma vez, na raiz do app (ou da página Unifilar)
import { BadgeSeveridade, BadgeVerificar, RastreioInline, FaixaProvisoria }
  from "./primitivas_validacao";
```

O contêiner da página recebe `data-theme="sie-g100"`. `UnifilarHero.tsx` e
`simbolos_iec.tsx` já consomem os tokens `--sie-*` (com fallback `--cds-*`).

`[VERIFICAR]`: os hex do g100 aqui usados seguem a paleta Carbon padrão; se o
tema do SIE em produção tiver customizações (ex.: azul de seleção diferente),
ajustar o fallback no token — nunca no componente.
