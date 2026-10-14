# P-CERTFID — Registro de Conferência das Tabelas EDP contra a Norma

**Referência:** `P-CERTFID_Certificar_Valores_Tabelas_EDP.md`
**Conferido em:** 2026-07-01
**Conferido por:** Dex (agente `@dev`, Synkra AIOX) — conferência automatizada, valor a valor
**Escopo:** `tabela_005`–`tabela_010`/`012`–`015` (fatores de demanda, grupos A–I) e catálogo `subcategorias-fornecimento.catalogo.data.json` (Tabelas 001/002 EDP)
**Não alterado:** lógica de aplicação das tabelas, cálculos de demanda, `fonte`/`versao_norma` nos arquivos `.data.json` (campo validado por comparação exata de string em `fatores-demanda.ts`; alterá-lo quebraria o boot).

---

## 1. Método de conferência

1. Baixado o PDF oficial já referenciado no repositório (`url_fonte` do catálogo): `https://www.edp.com.br/Ginp/Download/PT.DT.PDN.00068_V9.pdf` (91 páginas, EDP São Paulo, **Versão 09**, vigência 14/04/2026).
2. Texto extraído localmente com `pdftotext -layout` (Git for Windows / poppler), sem depender de terceiros. `WebFetch` sozinho não conseguiu decodificar os streams comprimidos do PDF — por isso a extração foi feita via binário local.
3. Cada valor do sistema (`tabela_0XX.data.json` e `subcategorias-fornecimento.catalogo.data.json`) foi comparado célula a célula contra o texto bruto extraído do PDF oficial (não contra o markdown de consolidação `Arquivos_Diversos/tabelas_001_002_padrao_edp.md`, para evitar verificação circular — embora essa consolidação também tenha se confirmado fiel ao PDF).

## 2. Checklist — Tabela_005 a Tabela_015 (fatores de demanda)

| Tabela | Grupo | Descrição oficial | Pág. PDF | Nº de faixas conferidas | Resultado |
|---|---|---|---|---|---|
| tabela_005 | A | Fatores de demanda — Tomadas e iluminação (residencial) | 33 | 11/11 | ✓ 100% idêntico |
| tabela_007 | B | Fatores de demanda — Chuveiros, torneiras, aquecedores de passagem, ferros | 34–35 | 17/17 | ✓ 100% idêntico |
| tabela_008 | C | Fatores de demanda — Aquecedor central/boiler/sauna | 35 | 3/3 | ✓ 100% idêntico |
| tabela_009 | D | Fatores de demanda — Secadora, forno elétrico, lava-louça/roupa, micro-ondas | 35–36 | 4/4 | ✓ 100% idêntico |
| tabela_010 | E | Fatores de demanda — Fogões elétricos | 36 | 12/12 | ✓ 100% idêntico |
| tabela_012 | F | Fatores de demanda — Condicionadores de ar (uso comercial) | 37 | 6/6 | ✓ 100% idêntico |
| tabela_013 | G | Fatores de demanda — Motores (maior/restantes) | 37 | 2/2 | ✓ 100% idêntico |
| tabela_014 | H | Fatores de demanda — Equipamentos especiais (maior/restantes) | 37 | 2/2 | ✓ 100% idêntico |
| tabela_015 | I | Fatores de demanda — Hidromassagem | 37 | 4/4 | ✓ 100% idêntico |

Nenhuma divergência numérica encontrada. Exemplo de conferência (tabela_005, faixas completas):

```
Sistema (JSON)          PDF oficial (Tabela 005, pág. 33)
≤1 kW      → 0,86        C≤1        → 0,86  ✓
1–2 kW     → 0,75        1<C≤2      → 0,75  ✓
2–3 kW     → 0,66        2<C≤3      → 0,66  ✓
3–4 kW     → 0,59        3<C≤4      → 0,59  ✓
4–5 kW     → 0,52        4<C≤5      → 0,52  ✓
5–6 kW     → 0,45        5<C≤6      → 0,45  ✓
6–7 kW     → 0,40        6<C≤7      → 0,40  ✓
7–8 kW     → 0,35        7<C≤8      → 0,35  ✓
8–9 kW     → 0,31        8<C≤9      → 0,31  ✓
9–10 kW    → 0,27        9<C≤10     → 0,27  ✓
>10 kW     → 0,24        C>10       → 0,24  ✓
```

As demais tabelas seguiram o mesmo procedimento (todas as faixas conferidas individualmente); os textos brutos extraídos ficam disponíveis para reconferência em `pdftotext` a partir do PDF oficial citado acima.

## 3. Checklist — Tabelas 001/002 (categoria → disjuntor → condutor → seção)

13 categorias conferidas (U2, D2, D4, D6, D7, D9, D10, T2, T4, T6, T7, T9, T10) contra Anexo A do PDF (págs. 30–32), campo a campo: disjuntor de entrada, fusível NH/chave, tipo de medição, condutor PVC/EPR-XLPE, caixa, eletroduto de entrada, poste, PCI, aterramento (condutor e eletroduto), limites de motor FN/FF/FFF.

| Categoria | Disjuntor | Condutor PVC/EPR | Aterramento PVC/EPR | Maior motor FN/FF/FFF | Resultado |
|---|---:|---|---|---|---|
| U2 | 70 A | resp. distribuidora | 16/16 mm² | 1 / — / — | ✓ |
| D2 | 63 A | resp. distribuidora | 16/16 mm² | 1 / 3 / — | ✓ |
| D4 | 100 A | 35/25 mm² | 16/16 mm² | 1 / 3 / — | ✓ |
| D6 | 150 A | 70/50 mm² | 35/25 mm² | 1 / 3 / — | ✓ |
| D7 | 200 A | 95/70 mm² | 50/35 mm² | 1 / 5 / — | ✓ |
| D9 | 300 A | 185/120 mm² | 95/70 mm² | 1 / 5 / — | ✓ |
| D10 | 350 A | 240/185 mm² | 120/95 mm² | 1 / 5 / — | ✓ |
| T2 | 63 A | resp. distribuidora | 16/16 mm² | 1 / 3 / 8 | ✓ |
| T4 | 100 A | 35/25 mm² | 16/16 mm² | 1 / 3 / 15 | ✓ |
| T6 | 150 A | 70/50 mm² | 35/25 mm² | 1 / 5 / 25 | ✓ |
| T7 | 200 A | 95/70 mm² | 50/35 mm² | 1 / 5 / 30 | ✓ |
| T9 | 300 A | 185/120 mm² | 95/70 mm² | 1 / 5 / 60 | ✓ |
| T10 | 350 A | 240/185 mm² | 120/95 mm² | 1 / 5 / 60 | ✓ |

Fusível NH/chave, tipo de medição, caixa, eletroduto, poste e PCI também conferidos linha a linha — sem divergência.

## 4. Status final

- ✅ 100% dos valores de FD (tabela_005 a tabela_015) batidos contra `PT.DT.PDN.00068 v09`.
- ✅ 100% dos pares categoria/disjuntor/condutor/seção (13 categorias, Tabelas 001/002) confirmados.
- ✅ `status_verificacao: "VERIFICADO"` já presente em todos os arquivos — agora **confirmado por conferência independente contra o PDF oficial**, não apenas herdado de trabalho anterior.
- ✅ Fonte e data de conferência registradas neste documento (fora do JSON de runtime, para não violar a validação estrita de `fonte` em `fatores-demanda.ts`).

## 5. Pendências que permanecem em aberto (não resolvidas por esta conferência)

1. **`PT.DT.PDN.03.14.020 v06`** — segunda norma citada no P-CERTFID e no `README.md` do módulo — **não foi localizada nem anexada**. Não há URL ou arquivo dela no repositório. O código (`FONTES_ACEITAS` em `fatores-demanda.ts`) aceita essa string como fonte válida, mas nenhum dado atual a utiliza (todos usam v09). Não fabriquei conferência contra um documento que não tenho — se essa norma ainda for exigível, é preciso anexá-la para conferência real.
2. **`corrente_demanda_max_A`** no catálogo 001/002 é um campo **derivado** (igual ao valor do disjuntor de entrada), não uma coluna literal da Tabela 001/002 do PDF. Já mapeado como gap conhecido em `Arquivos_Diversos/PLANO_CORRECAO_TABELAS_001_002_COM_ANEXO.md` (seção 4.2) — fora do escopo desta conferência de valores.
3. `tabela_006` (carga mínima — instalações especiais) e `tabela_011` (potência/corrente de condicionadores de ar) existem na norma oficial mas não estão implementadas como tabelas de FD no sistema — estrutura diferente das demais (não é uma tabela simples de fator por faixa), por isso a numeração `tabela_0XX` pula esses dois números no repositório. Não é um defeito desta auditoria; é um gap de escopo pré-existente, registrado aqui para rastreabilidade.
