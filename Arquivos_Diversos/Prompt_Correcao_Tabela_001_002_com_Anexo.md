# PROMPT — Correção da Tabela 001/002 com Importação do Anexo Oficial

> Prompt autocontido. Você (LLM executora) **não** tem histórico — todo o necessário está aqui.
> Há um **arquivo anexo** com as Tabelas 001 e 002 oficiais da EDP. Você vai importar dele, não criar números.

---

## 1. PAPEL E ESCOPO

Você é um engenheiro eletricista sênior implementando uma correção pontual no módulo "Padrão de Entrada" de um assistente de projetos elétricos.

**Corrigir apenas isto:** a sub-categoria, o disjuntor e o condutor de entrada exibidos pelo sistema (atualmente `T6 · Disjuntor 150 A · Condutor 50 mm²` para corrente de demanda de 107,4 A em Categoria T) **não têm origem rastreável**. A aba "Sub-categorias 001/002" do próprio sistema declara *"Tabelas 001/002 não populadas (default vazio com status VERIFICAR)"*, mas a Saída B continua emitindo valores — só possível se existir **fallback** (valor hardcoded, default ou lógica oculta) entregando resposta quando a tabela não tem.

**Fora de escopo:** roteamento de grupos de demanda, FPs, balanceamento de fases, divisão de circuitos, qualquer outro módulo.

---

## 2. PROBLEMA — DIAGNÓSTICO PRECISO

Duas faces a corrigir **juntas**:

**Face A — Tabela vazia.** Os IDs de sub-categoria reconhecidos pelo sistema são: **U2 · D2 · D4 · D6 · D7 · D9 · D10 · T2 · T4 · T6 · T7 · T9 · T10**. Nenhum deles existe na tabela ativa.

**Face B — Fallback silencioso.** Mesmo com a tabela vazia, a Saída B retorna `sub_categoria: "T6", disjuntor_A: 150, condutor_mm2: 50`. Esses valores vêm de algum lugar que não é a tabela 001/002. Quebra a rastreabilidade, que é a proposição fundamental do sistema.

> Popular a tabela sem remover o fallback resolve só os casos cobertos pelas linhas inseridas. Qualquer corrente fora das faixas — e qualquer falha de leitura — volta a invocar o fallback silenciosamente. **As duas correções são inseparáveis.**

---

## 3. INVARIANTES

1. **Rastreabilidade não-negociável.** Toda saída de sub-cat/disjuntor/condutor vem de uma linha cadastrada — com `fonte_linha` e `status_linha` publicados na Saída B.
2. **`IB ≤ In ≤ Iz` obrigatório.** O par (disjuntor, condutor) selecionado satisfaz a inequação. Linhas que a violem não são utilizáveis.
3. **Sub-categoria coerente com Categoria.** `U*` só sob U, `D*` só sob D, `T*` só sob T. Prefixos cruzados são bloqueados.
4. **Falhar de forma honesta.** Quando a tabela não cobrir a corrente, sistema declara ausência. **Sem "melhor palpite".**
5. **Importação fiel.** Os números vêm **exclusivamente** do anexo. Você **não** ajusta, arredonda, "corrige" nem completa valores com conhecimento próprio. Se um valor parecer suspeito, marca-se a linha — não se altera.

---

## 4. CORREÇÃO EM 4 FASES

### Fase 1 — Eliminação do fallback

**Pré-requisito:** nenhum.

**Ações:**
- Localizar o caminho que produz `sub_categoria`, `disjuntor_A` e `condutor_mm2` na Saída B quando a tabela está vazia.
- **Remover** todo valor hardcoded, default, valor de exemplo, lógica de aproximação ou herança de versão antiga que entregue resposta sem consultar a tabela.
- A função de seleção tem um único caminho de leitura: consultar a tabela. Se a leitura não retornar linha válida, retorna **nulo com motivo declarado** — não retorna palpite.

**Critério de aceite:** com a tabela vazia, Saída B retorna `sub_categoria: null, disjuntor_A: null, condutor_mm2: null`; tela exibe `ERRO — TABELA-001-002-VAZIA: cadastre a escada de sub-categorias para habilitar a seleção`. **Nenhum valor hardcoded sobrevive.** Esta fase deve ser concluída antes da Fase 2, senão a importação será testada contra um sistema ainda mascarado pelo fallback.

---

### Fase 2 — Importação fiel do anexo oficial

**Pré-requisito:** Fase 1 concluída.

**Fonte:** arquivo anexo com as Tabelas 001 e 002 da EDP São Paulo PT.DT.PDN.03.14.020 v06. Você **não** tem outra fonte — não complete, não infira, não arredonde, não preencha lacunas com conhecimento próprio.

**Modelo de linha (destino):**
```
{
  sub_cat: <texto>,                    // ex.: "T2", "D4"
  categoria: "U" | "D" | "T",          // letra coerente com prefixo
  corrente_demanda_max_A: <número>,    // limite superior da faixa (Tab. 001)
  disjuntor_nominal_A: <número>,       // Tab. 001 ou 002
  secao_condutor_mm2: <número>,        // Tab. 002 (entrada)
  fonte: "EDP PT.DT.PDN.03.14.020 v06 — Tab. 001/002 (anexo)",
  status: "VERIFICADO" | "VERIFICAR"
}
```

**Procedimento de importação:**

1. **Parse do anexo.** Identifique colunas: sub-categoria, categoria (ou inferir do prefixo se o anexo não trouxer), corrente de demanda máxima da faixa, disjuntor nominal, seção do condutor. Se o anexo tiver as Tabelas 001 e 002 separadas, faça o **join** pela sub-categoria.
2. **Importação 1:1.** Cada linha do anexo gera exatamente uma linha no sistema. Preservar **todos** os valores numéricos como estão no anexo — incluindo casas decimais, se houver.
3. **Inferência da `categoria`** apenas quando o anexo não a explicitar: do prefixo do `sub_cat` (`U*` → U, `D*` → D, `T*` → T). Registrar que foi inferido.
4. **Atribuir `status`:**
   - `VERIFICADO` se a linha passa nas validações estruturais da Fase 4 (prefixo×categoria coerente, `In ≤ Iz`, monotonicidade na categoria).
   - `VERIFICAR` se a linha falha em alguma validação estrutural. **Importar mesmo assim**, marcada — não silenciar, não corrigir.
5. **Não criar linhas** que não estejam no anexo. Se o anexo cobrir só parte dos 13 IDs reconhecidos pelo sistema, as ausências ficam ausentes (a Fase 4 sinaliza).

**Conferência pós-importação (obrigatória, exibir ao usuário):**
- Contagem: nº de linhas no anexo == nº de linhas importadas.
- Hash/checksum: para cada linha, exibir `sub_cat → (corrente_max, disjuntor, secao)` lado a lado com o anexo, em formato auditável (CSV ou tabela), para conferência humana.
- Lista das linhas marcadas `VERIFICAR` com motivo (qual validação estrutural falhou).

**Critério de aceite:** o conjunto de linhas importadas é **idêntico** ao do anexo em quantidade e valores; toda divergência estrutural está marcada `VERIFICAR` e visível; nenhuma linha foi adicionada, removida, completada ou ajustada além do anexo.

---

### Fase 3 — Algoritmo de seleção com validação

**Pré-requisito:** Fase 2.

**Algoritmo:**
1. Receber `categoria` (da seleção por carga instalada) e `corrente_demanda_A` (calculada).
2. Filtrar a tabela por `linha.categoria == categoria`. Nenhuma sub-cat de outra letra entra como candidata.
3. Entre as filtradas, selecionar a linha com **menor `corrente_demanda_max_A` que seja ≥ `corrente_demanda_A`** — menor sub-categoria suficiente (não superdimensionar).
4. **Validar a linha antes de devolver:**
   - `corrente_demanda_A ≤ corrente_demanda_max_A` ✓
   - `disjuntor_nominal_A ≤ ampacidade(secao_condutor_mm2)` — `In ≤ Iz`
   - `corrente_demanda_A ≤ disjuntor_nominal_A` permitido — `IB ≤ In`
5. **Recusar linha `VERIFICAR` para seleção automática.** Se a melhor candidata estiver marcada, devolver com diagnóstico `ATENÇÃO — LINHA-PROVISORIA` e exigir confirmação humana antes de publicar (ou bloquear; ver Fase 4).
6. Se nenhuma linha atender, retornar nulo + diagnóstico.

**Saída B publica:** `sub_categoria`, `disjuntor_A`, `condutor_mm2`, **e** `fonte_linha` (cópia de `fonte`), **e** `status_linha`. A rastreabilidade vai ATÉ a linha.

**Critério de aceite:** para Categoria T e corrente 107,4 A, a função retorna a sub-categoria T cujo `corrente_demanda_max_A` é o **menor ≥ 107,4** entre as linhas T `VERIFICADO`; nunca cruza letras; resposta inclui `fonte_linha` e `status_linha`.

---

### Fase 4 — Validação estrutural, diagnósticos e UI

**Pré-requisito:** Fase 3.

**Validações estruturais (executadas ao salvar a tabela e ao recalcular):**

a. **Prefixo×Categoria.** `sub_cat` que começa com `U` exige `categoria = "U"`; idem D, T. Linhas que violem são marcadas `VERIFICAR`.

b. **`In ≤ Iz` na própria linha.** `disjuntor_nominal_A ≤ ampacidade(secao_condutor_mm2)`. Onde o sistema não tiver tabela de ampacidade própria, usar tabela de referência declarada (`fonte: "NBR 5410 Tab. 36/37"` ou equivalente, sob `status: VERIFICAR`). Linha que viole é **marcada e não selecionável automaticamente** — não é apagada (o dado do anexo é preservado), mas o algoritmo da Fase 3 a recusa.

c. **Monotonicidade dentro da categoria.** Para a mesma categoria, ordenar por `corrente_demanda_max_A` ascendente: `disjuntor_nominal_A` e `secao_condutor_mm2` devem ser **não-decrescentes**. Inversão sinaliza `VERIFICAR` nas linhas envolvidas.

d. **Cobertura de IDs reconhecidos.** O sistema reconhece 13 IDs (U2; D2/D4/D6/D7/D9/D10; T2/T4/T6/T7/T9/T10). Para cada ID **ausente** do anexo, emitir `ATENÇÃO — SUB-CAT-AUSENTE: <ID>`. Não fabricar a linha.

e. **Conferência de importação.** Disponibilizar comando "Exportar tabela importada" que produza um CSV idêntico ao anexo, para conferência reversa.

**Diagnósticos por severidade:**

- `ERRO — TABELA-001-002-VAZIA` — tabela sem linhas.
- `ERRO — CATEGORIA-SEM-LINHAS` — categoria selecionada sem linhas `VERIFICADO`.
- `ERRO — CORRENTE-ACIMA-DO-MAIOR-PADRAO` — corrente excede o maior `corrente_demanda_max_A` da categoria (provável caso de MT, fora do escopo BT).
- `ERRO — LINHA-INCONSISTENTE` — a linha que seria selecionada viola `In ≤ Iz` ou prefixo×categoria. Saída nula com motivo.
- `ATENÇÃO — LINHA-PROVISORIA` — linha selecionada está `VERIFICAR`; exige confirmação humana.
- `ATENÇÃO — SUB-CAT-AUSENTE` — um ID reconhecido não veio do anexo.
- `ATENÇÃO — CORRENTE-NA-FRONTEIRA` — dentro de X% (config) do limite superior da sub-cat selecionada.
- `INFO — SUB-CATEGORIA-DETERMINADA` — seleção normal sobre linha `VERIFICADO`.

**UI:**
- Aba "Sub-categorias 001/002" lista todas as linhas com `status`, `fonte` e, para `VERIFICAR`, o motivo.
- Seção "Categoria e sub-categoria" exibe a sub-cat selecionada **com link/rastro para a linha de origem na tabela**.
- Botão "Importar Tabelas 001/002" recebe o arquivo, mostra o **diff** entre estado atual e anexo, e exige confirmação antes de salvar.
- Quando a saída for nula, tela exibe `**sub-categoria não determinada — motivo: <diagnóstico>**`. Nunca um valor sem origem.

**Critério de aceite:**
- Esvaziando a tabela: tela exibe ERRO e Saída B nula (Fase 1 sustentada).
- Importando o anexo: linhas idênticas, validações estruturais executadas, linhas problemáticas marcadas.
- Tentativa de salvar manualmente uma linha `U2 · categoria T` ou `disjuntor 150 A · seção 25 mm²` é bloqueada (recupera o defeito histórico).
- Saída B sempre carrega `fonte_linha` e `status_linha`.

---

## 5. CRITÉRIO DE ACEITE GLOBAL

A correção está completa quando, **simultaneamente:**

1. **Origem rastreável:** toda saída vem de linha cadastrada (com `fonte_linha`/`status_linha`).
2. **Sem fallback:** esvaziar a tabela produz saída nula + ERRO.
3. **Importação fiel:** o conjunto de linhas no sistema é idêntico ao do anexo (sem adição, remoção, ajuste ou completamento).
4. **Segurança verificada:** linhas que violem `In ≤ Iz` ou prefixo×categoria estão marcadas e não são selecionáveis automaticamente.
5. **Reprodutibilidade:** auditor parte da Saída B, abre a aba 001/002, encontra a linha que originou a resposta e vê a fonte normativa.
6. **Auditoria reversa:** o sistema consegue exportar a tabela importada para conferência byte-a-byte contra o anexo.

---

## 6. PRINCÍPIO INVIOLÁVEL

> Você **não** tem autorização para inventar, completar, arredondar, corrigir ou inferir valores numéricos das Tabelas 001/002 a partir de conhecimento próprio. A fonte é exclusivamente o anexo. Valores que pareçam suspeitos no anexo são **marcados** (`VERIFICAR`), nunca alterados. Linhas faltantes no anexo ficam ausentes no sistema — não são preenchidas por dedução.
>
> Esta restrição existe porque o defeito que a correção remove é justamente a presença de números sem origem auditável. Reintroduzir números a partir de memória — sob qualquer pretexto — reinstaura o defeito.
