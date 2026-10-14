# PROMPT DE IMPLEMENTAÇÃO — MÓDULO: DIMENSIONAMENTO DE CONDUTORES

**Identificador:** MOD-DC-v2.0
**Data:** 2026-07-11
**Dependências upstream:** Módulo de Circuitos (contrato canônico ou adaptador 1:1), Módulo IB (corrente de projeto)
**Dependência downstream:** Módulo de Queda de Tensão (MOD-QT), Módulo de Proteção (futuro)

---

## 1. OBJETIVO

Implementar o módulo de dimensionamento de condutores para circuitos terminais de baixa tensão, determinando a seção mínima normalizada (IEC 60228) que satisfaça **simultaneamente** os três critérios da ABNT NBR 5410:2004:

1. **Capacidade de condução de corrente (Iz)** — seções 6.2.5 e 6.2.6
2. **Seção mínima por aplicação** — tabela 47 (iluminação, tomadas, sinalização, etc.)
3. **Proteção contra sobrecarga (coordenação IB ≤ In ≤ Iz)** — seção 5.3.4

A seção final é `max(seção_critério_1, seção_critério_2, seção_critério_3)`.

O terceiro critério — proteção contra curto-circuito (I²t) — será implementado em módulo futuro (MOD-CC). O sistema deve registrar explicitamente que esse critério não foi verificado, com status `PENDENTE-CC`.

---

## 2. REGRAS GERAIS (obrigatórias em toda implementação SIE)

### R-01: Rastreabilidade normativa
Todo valor calculado armazena `fonte` (ex.: "NBR 5410:2004, Tabela 36, método B1, coluna 3F+N Cu PVC") e `status_verificacao` ("VERIFICADO" | "PENDENTE" | "[VERIFICAR]").

### R-02: Série normalizada IEC 60228
As únicas seções admissíveis são: 0.5, 0.75, 1.0, 1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300, 400, 500 mm². Qualquer valor fora dessa série é rejeitado com erro `INC-07`. Validar com `secao in SERIE_IEC_60228`.

### R-03: Tensão nunca assume fallback silencioso
Circuito sem tensão declarada (`tensao_v is None`) não pode ser dimensionado. O módulo deve retornar status `ERRO-TENSAO-AUSENTE` e não prosseguir. (Disciplina INC-04.)

### R-04: VA direto, sem divisão por FP
Valores de potência aparente (VA) são usados diretamente. Nunca dividir VA por fator de potência para obter VA. (Disciplina INC-01.)

### R-05: Design System — IBM Carbon
Toda UI segue IBM Carbon Design System. Proibido: texto branco (#fff) sobre fundo vermelho de erro (#fa4d56) — contraste 3.35:1, abaixo de WCAG AA 4.5:1. Usar texto escuro sobre fundo vermelho, ou texto branco sobre fundo escuro.

### R-06: Isolação é escolha explícita do projetista
O tipo de isolação do condutor (PVC ou EPR/XLPE) nunca é assumido pelo sistema. O projetista seleciona explicitamente em cada projeto (ou como padrão global do projeto com override por circuito). Sem seleção → status `ERRO-ISOLACAO-AUSENTE`. (Resolução INC-12.)

---

## 3. CONTEXTO ARQUITETURAL

### 3.1 Posição na cadeia

```
Cargas → Demanda → Categoria → Circuitos → IB → ★ DIMENSIONAMENTO CONDUTORES ★ → Queda de Tensão → Proteção
```

### 3.2 Contrato de entrada (do módulo de Circuitos)

Cada circuito chega com, no mínimo:

```python
class CircuitoParaDimensionamento(BaseModel):
    id: str                          # ex.: "ILUM-Dormitorio-1"
    descricao: str
    tipo: Literal["ILU", "TUG", "TUE"]
    potencia_va: float               # VA total do circuito
    tensao_v: Optional[float]        # 127 | 220 | None
    corrente_projeto_a: float        # IB calculado upstream
    num_fases: Literal[1, 2, 3]      # monofásico, bifásico, trifásico
    fases: list[str]                 # ex.: ["R"], ["R","S"], ["R","S","T"]
    tem_neutro: bool
    fp_carga: Optional[float]        # fator de potência da carga (para info, NÃO para recalcular VA)
    fonte_ib: str                    # rastreabilidade do cálculo IB
```

### 3.3 Contrato de saída (para módulos downstream)

```python
class ResultadoDimensionamento(BaseModel):
    circuito_id: str
    
    # Entradas capturadas
    material: Literal["Cu", "Al"]
    isolacao: Literal["PVC", "EPR", "XLPE"]
    metodo_instalacao: str           # referência de método (ex.: "B1", "B2", "C", "D", "E", "F", "G")
    temperatura_ambiente_c: int      # 30 (padrão NBR) ou outro
    num_circuitos_agrupados: int     # para fator de agrupamento
    
    # Fatores de correção
    fator_temperatura: float         # FCT — tabela 40 NBR 5410
    fator_agrupamento: float         # FCA — tabela 42 NBR 5410
    
    # Resultados dos 3 critérios
    secao_por_capacidade_mm2: float  # critério 1
    secao_minima_aplicacao_mm2: float  # critério 2 (tabela 47)
    secao_por_coordenacao_mm2: float   # critério 3 (IB ≤ In ≤ Iz)
    
    # Resultado final
    secao_final_mm2: float           # max dos 3 critérios — SEMPRE na série IEC 60228
    iz_condutor_a: float             # capacidade real do condutor na seção final, com fatores aplicados
    in_disjuntor_a: Optional[float]  # corrente nominal do disjuntor selecionado (pode ser None se proteção não implementada)
    
    # Verificações
    ib_menor_in: Optional[bool]      # IB ≤ In
    in_menor_iz: Optional[bool]      # In ≤ Iz
    i2_menor_145iz: Optional[bool]   # I2 ≤ 1.45·Iz (I2 = 1.45·In para disjuntores)
    
    # Status e rastreabilidade
    status: Literal["DIMENSIONADO", "ERRO-TENSAO-AUSENTE", "ERRO-ISOLACAO-AUSENTE", "ERRO-METODO-AUSENTE", "PENDENTE-CC"]
    alertas: list[str]               # avisos não-bloqueantes
    rastreio: dict                   # log completo: tabela usada, linha, coluna, fatores
    
    # Flag de curto-circuito pendente
    curto_circuito_verificado: bool  # sempre False nesta versão
```

---

## 4. MODELO DE DADOS (persistência)

### 4.1 Tabela de capacidade de condução (Iz base)

```sql
CREATE TABLE tabela_iz (
    id SERIAL PRIMARY KEY,
    material VARCHAR(2) NOT NULL CHECK (material IN ('Cu', 'Al')),
    isolacao VARCHAR(4) NOT NULL CHECK (isolacao IN ('PVC', 'EPR', 'XLPE')),
    metodo_instalacao VARCHAR(3) NOT NULL,
    secao_mm2 DECIMAL(6,2) NOT NULL,
    num_condutores_carregados INT NOT NULL,  -- 2 ou 3
    iz_a DECIMAL(6,2) NOT NULL,
    fonte VARCHAR(200) NOT NULL,             -- ex.: "NBR 5410:2004, Tabela 36"
    status_verificacao VARCHAR(20) NOT NULL DEFAULT '[VERIFICAR]',
    
    UNIQUE (material, isolacao, metodo_instalacao, secao_mm2, num_condutores_carregados)
);
```

**Nota sobre `[VERIFICAR]`:** As tabelas 36 a 39 da NBR 5410 contêm centenas de valores de Iz. O implementador deve popular ao menos os métodos B1 e C para Cu/PVC e Cu/EPR com seções de 1.5 a 35 mm² (faixa residencial/comercial). Valores não populados devem manter `status_verificacao = '[VERIFICAR]'` e impedir dimensionamento com `ERRO-TABELA-INCOMPLETA`.

### 4.2 Tabela de fatores de correção por temperatura

```sql
CREATE TABLE fator_correcao_temperatura (
    id SERIAL PRIMARY KEY,
    isolacao VARCHAR(4) NOT NULL,
    temperatura_ambiente_c INT NOT NULL,
    fator DECIMAL(4,3) NOT NULL,
    fonte VARCHAR(200) NOT NULL,
    status_verificacao VARCHAR(20) NOT NULL DEFAULT '[VERIFICAR]',
    
    UNIQUE (isolacao, temperatura_ambiente_c)
);

-- Valores de referência (tabela 40 NBR 5410) — [VERIFICAR] contra original
-- PVC (referência 30°C): 25°C→1.04, 30°C→1.00, 35°C→0.96, 40°C→0.91, 45°C→0.87, 50°C→0.82, 55°C→0.76, 60°C→0.71
-- EPR/XLPE (referência 30°C): 25°C→1.02, 30°C→1.00, 35°C→0.98, 40°C→0.96, 45°C→0.93, 50°C→0.90, 55°C→0.87, 60°C→0.83
```

### 4.3 Tabela de fatores de agrupamento

```sql
CREATE TABLE fator_correcao_agrupamento (
    id SERIAL PRIMARY KEY,
    disposicao VARCHAR(50) NOT NULL,    -- ex.: "feixes", "camada_unica_parede", "camada_unica_piso", etc.
    num_circuitos INT NOT NULL,
    fator DECIMAL(4,3) NOT NULL,
    fonte VARCHAR(200) NOT NULL,
    status_verificacao VARCHAR(20) NOT NULL DEFAULT '[VERIFICAR]',
    
    UNIQUE (disposicao, num_circuitos)
);

-- Valores de referência (tabela 42 NBR 5410) — [VERIFICAR] contra original
-- Feixes ou eletroduto: 1→1.00, 2→0.80, 3→0.70, 4→0.65, 5→0.60, 6→0.57, 7→0.54, 8→0.52, 9→0.50, 10-12→0.45, 13-16→0.41, 17-20→0.38
```

### 4.4 Tabela de seções mínimas por aplicação

```sql
CREATE TABLE secao_minima_aplicacao (
    id SERIAL PRIMARY KEY,
    tipo_circuito VARCHAR(30) NOT NULL,     -- "iluminacao", "tomadas", "sinalizacao", "forca"
    material VARCHAR(2) NOT NULL,
    secao_minima_mm2 DECIMAL(5,2) NOT NULL,
    fonte VARCHAR(200) NOT NULL,
    status_verificacao VARCHAR(20) NOT NULL DEFAULT '[VERIFICAR]',
    
    UNIQUE (tipo_circuito, material)
);

-- Valores (tabela 47 NBR 5410) — [VERIFICAR] contra original
-- Iluminação: Cu→1.5, Al→2.5 (Al não admitido abaixo de 16 mm² conforme nota)
-- Tomadas (TUG): Cu→2.5, Al→2.5 (Al não admitido abaixo de 16 mm²)
-- Nota: Al não é admitido em seções inferiores a 16 mm² para instalações fixas (NBR 5410 6.2.6.1.2)
```

### 4.5 Resultado do dimensionamento por circuito

```sql
ALTER TABLE circuito ADD COLUMN IF NOT EXISTS (
    -- Entradas de dimensionamento
    material_condutor VARCHAR(2),
    isolacao_condutor VARCHAR(4),
    metodo_instalacao VARCHAR(3),
    temperatura_ambiente_c INT DEFAULT 30,
    num_circuitos_agrupados INT DEFAULT 1,
    
    -- Fatores calculados
    fator_correcao_temperatura DECIMAL(4,3),
    fator_correcao_agrupamento DECIMAL(4,3),
    
    -- Seções por critério
    secao_capacidade_mm2 DECIMAL(6,2),
    secao_minima_mm2 DECIMAL(6,2),
    secao_coordenacao_mm2 DECIMAL(6,2),
    
    -- Resultado final
    secao_final_mm2 DECIMAL(6,2),
    iz_final_a DECIMAL(6,2),
    
    -- Rastreabilidade
    rastreio_dimensionamento JSONB,
    status_dimensionamento VARCHAR(30) DEFAULT 'PENDENTE',
    curto_circuito_verificado BOOLEAN DEFAULT FALSE
);
```

---

## 5. ALGORITMO — PSEUDOCÓDIGO

```python
SERIE_IEC_60228 = [0.5, 0.75, 1.0, 1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300, 400, 500]

def dimensionar_condutor(circuito: CircuitoParaDimensionamento,
                          material: str,
                          isolacao: str,
                          metodo: str,
                          temp_ambiente: int = 30,
                          num_agrupados: int = 1,
                          disposicao_agrupamento: str = "feixes") -> ResultadoDimensionamento:
    """
    Determina a seção mínima normalizada do condutor.
    """
    
    # ──────────────────────────────────────────
    # GUARDA: validações de entrada
    # ──────────────────────────────────────────
    if circuito.tensao_v is None:
        return ResultadoDimensionamento(status="ERRO-TENSAO-AUSENTE", ...)
    
    if isolacao is None or isolacao not in ("PVC", "EPR", "XLPE"):
        return ResultadoDimensionamento(status="ERRO-ISOLACAO-AUSENTE", ...)
    
    if material == "Al":
        # NBR 5410, 6.2.6.1.2: Al não admitido em seções < 16 mm² para instalações fixas
        secao_minima_al = 16.0  # mm²
    
    IB = circuito.corrente_projeto_a
    
    # ──────────────────────────────────────────
    # CRITÉRIO 1: Capacidade de condução (Iz)
    # ──────────────────────────────────────────
    
    # 1a. Determinar número de condutores carregados
    if circuito.num_fases == 3:
        n_condutores_carregados = 3  # neutro não conta em sistema equilibrado
    else:
        n_condutores_carregados = 2  # fase + neutro
    
    # 1b. Buscar fatores de correção
    FCT = buscar_fator_temperatura(isolacao, temp_ambiente)
    FCA = buscar_fator_agrupamento(disposicao_agrupamento, num_agrupados)
    
    if FCT is None or FCA is None:
        return ResultadoDimensionamento(status="ERRO-FATOR-NAO-ENCONTRADO", ...)
    
    # 1c. Corrente corrigida que o condutor precisa suportar
    #     Iz_necessario = IB / (FCT × FCA)
    #     Buscar na tabela de Iz a menor seção cujo Iz_base ≥ Iz_necessario
    Iz_necessario = IB / (FCT * FCA)
    
    secao_c1, iz_base_c1 = buscar_secao_por_iz(
        material=material,
        isolacao=isolacao,
        metodo=metodo,
        n_condutores=n_condutores_carregados,
        iz_minimo=Iz_necessario
    )
    
    if secao_c1 is None:
        return ResultadoDimensionamento(status="ERRO-IZ-INSUFICIENTE", ...)
    
    # Iz real do condutor na seção encontrada (com fatores aplicados)
    Iz_real_c1 = iz_base_c1 * FCT * FCA
    
    # ──────────────────────────────────────────
    # CRITÉRIO 2: Seção mínima por aplicação (tabela 47)
    # ──────────────────────────────────────────
    
    tipo_aplicacao = mapear_tipo_para_aplicacao(circuito.tipo)
    # ILU → "iluminacao", TUG → "tomadas", TUE → "forca"
    
    secao_c2 = buscar_secao_minima_aplicacao(tipo_aplicacao, material)
    
    # ──────────────────────────────────────────
    # CRITÉRIO 3: Coordenação com proteção (IB ≤ In ≤ Iz)
    # ──────────────────────────────────────────
    
    # Selecionar In comercial imediatamente acima de IB
    SERIE_IN = [6, 10, 13, 16, 20, 25, 32, 40, 50, 63, 70, 80, 100, 125]
    In = next((i for i in SERIE_IN if i >= IB), None)
    
    if In is None:
        return ResultadoDimensionamento(status="ERRO-IN-EXCEDIDO", ...)
    
    # O condutor deve suportar a corrente do disjuntor:
    # Iz_condutor ≥ In (mais conservador: Iz ≥ I2/1.45 onde I2=1.45·In → Iz ≥ In)
    # Buscar seção cujo Iz_real (com fatores) ≥ In
    
    secao_c3 = None
    for secao_candidata in SERIE_IEC_60228:
        iz_base = buscar_iz(material, isolacao, metodo, secao_candidata, n_condutores_carregados)
        if iz_base is None:
            continue
        iz_real = iz_base * FCT * FCA
        if iz_real >= In:
            secao_c3 = secao_candidata
            break
    
    if secao_c3 is None:
        return ResultadoDimensionamento(status="ERRO-COORDENACAO-IMPOSSIVEL", ...)
    
    # ──────────────────────────────────────────
    # RESULTADO FINAL
    # ──────────────────────────────────────────
    
    secao_final = max(secao_c1, secao_c2, secao_c3)
    
    # Aplicar restrição Al ≥ 16 mm²
    if material == "Al" and secao_final < 16.0:
        secao_final = 16.0
        alertas.append("Al: seção elevada para 16 mm² (mínimo NBR 5410, 6.2.6.1.2)")
    
    # Garantir que está na série IEC 60228
    assert secao_final in SERIE_IEC_60228, f"INC-07: {secao_final} não está na série normalizada"
    
    # Iz real na seção final
    iz_base_final = buscar_iz(material, isolacao, metodo, secao_final, n_condutores_carregados)
    Iz_final = iz_base_final * FCT * FCA
    
    # Verificações de coordenação
    ib_ok = IB <= In
    in_ok = In <= Iz_final
    i2_ok = (1.45 * In) <= (1.45 * Iz_final)  # equivalente a In ≤ Iz
    
    return ResultadoDimensionamento(
        secao_final_mm2=secao_final,
        iz_condutor_a=Iz_final,
        in_disjuntor_a=In,
        ib_menor_in=ib_ok,
        in_menor_iz=in_ok,
        i2_menor_145iz=i2_ok,
        status="DIMENSIONADO",
        curto_circuito_verificado=False,  # PENDENTE-CC
        rastreio={
            "criterio_1": {"secao": secao_c1, "iz_base": iz_base_c1, "iz_necessario": Iz_necessario,
                           "FCT": FCT, "FCA": FCA, "tabela": "NBR 5410, Tabela 3X"},
            "criterio_2": {"secao": secao_c2, "fonte": "NBR 5410, Tabela 47"},
            "criterio_3": {"secao": secao_c3, "In": In, "Iz_real": iz_real},
            "decisivo": "criterio_X",  # qual critério determinou secao_final
            "versao_modulo": "MOD-DC-v2.0"
        }
    )
```

### 5.1 Funções auxiliares

```python
def buscar_secao_por_iz(material, isolacao, metodo, n_condutores, iz_minimo) -> tuple[float, float]:
    """
    Percorre a tabela de Iz em ordem crescente de seção.
    Retorna (secao_mm2, iz_base) da primeira seção cujo Iz_base ≥ iz_minimo.
    Retorna (None, None) se nenhuma seção atende.
    """
    resultados = db.query(TabelaIz).filter(
        TabelaIz.material == material,
        TabelaIz.isolacao == isolacao,
        TabelaIz.metodo_instalacao == metodo,
        TabelaIz.num_condutores_carregados == n_condutores,
        TabelaIz.iz_a >= iz_minimo,
        TabelaIz.status_verificacao != '[VERIFICAR]'  # não usar valores não verificados
    ).order_by(TabelaIz.secao_mm2.asc()).first()
    
    if resultados is None:
        return (None, None)
    return (resultados.secao_mm2, resultados.iz_a)


def mapear_tipo_para_aplicacao(tipo: str) -> str:
    MAPA = {
        "ILU": "iluminacao",
        "TUG": "tomadas",
        "TUE": "forca",
    }
    return MAPA.get(tipo, "forca")
```

---

## 6. API — FastAPI

```python
# ─── Schemas ───

class EntradaDimensionamento(BaseModel):
    circuito_id: str
    material: Literal["Cu", "Al"]
    isolacao: Literal["PVC", "EPR", "XLPE"]
    metodo_instalacao: str                    # "B1", "B2", "C", etc.
    temperatura_ambiente_c: int = 30
    num_circuitos_agrupados: int = 1
    disposicao_agrupamento: str = "feixes"

class EntradaDimensionamentoLote(BaseModel):
    projeto_id: str
    material_padrao: Literal["Cu", "Al"]
    isolacao_padrao: Literal["PVC", "EPR", "XLPE"]
    metodo_padrao: str = "B1"
    temperatura_padrao: int = 30
    overrides: Optional[dict[str, EntradaDimensionamento]] = None  # por circuito_id

# ─── Endpoints ───

@router.post("/api/v1/projetos/{projeto_id}/circuitos/{circuito_id}/dimensionar")
async def dimensionar_circuito(projeto_id: str, circuito_id: str, entrada: EntradaDimensionamento):
    """Dimensiona um único circuito."""
    ...

@router.post("/api/v1/projetos/{projeto_id}/dimensionar-lote")
async def dimensionar_lote(projeto_id: str, entrada: EntradaDimensionamentoLote):
    """Dimensiona todos os circuitos do projeto com parâmetros padrão + overrides."""
    ...

@router.get("/api/v1/projetos/{projeto_id}/dimensionamento")
async def obter_dimensionamento(projeto_id: str):
    """Retorna o resultado do dimensionamento de todos os circuitos."""
    ...

@router.get("/api/v1/tabelas/iz")
async def listar_tabela_iz(material: Optional[str] = None, isolacao: Optional[str] = None, metodo: Optional[str] = None):
    """Consulta a tabela de Iz com filtros opcionais."""
    ...

@router.get("/api/v1/tabelas/fatores-temperatura")
async def listar_fatores_temperatura(isolacao: Optional[str] = None):
    ...

@router.get("/api/v1/tabelas/fatores-agrupamento")
async def listar_fatores_agrupamento(disposicao: Optional[str] = None):
    ...
```

---

## 7. UI — IBM Carbon Design System

### 7.1 Configuração de projeto (painel superior)

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Dimensionamento de Condutores — Projeto: proj-1                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  Material padrão:  (●) Cobre (Cu)   ( ) Alumínio (Al)                  │
│                                                                         │
│  Isolação padrão:  [ PVC ▾ ]   ← Dropdown: PVC | EPR | XLPE           │
│                                                                         │
│  Método de instalação padrão:  [ B1 — Eletroduto embutido ▾ ]         │
│                                                                         │
│  Temperatura ambiente:  [ 30 °C ▾ ]                                    │
│                                                                         │
│  [ Dimensionar todos os circuitos ]                                     │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Comportamento:**
- Material, isolação e método são obrigatórios antes de habilitar o botão "Dimensionar"
- O botão dispara o endpoint de lote
- Cada circuito pode ter override individual (ver 7.3)

### 7.2 Tabela de resultados

```
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ # │ Circuito              │ Tipo │ IB (A) │ S₁ (mm²) │ S₂ (mm²) │ S₃ (mm²) │ S final │ Iz (A) │ In (A) │ Status            │
├───┼───────────────────────┼──────┼────────┼──────────┼──────────┼──────────┼─────────┼────────┼────────┼───────────────────┤
│ 1 │ ILUM-Dormitorio-1     │ ILU  │  2.36  │   1.5    │   1.5    │   1.5    │   1.5   │  17.5  │   6    │ ✓ DIMENSIONADO    │
│ 2 │ TUG-Cozinha-1         │ TUG  │ 12.60  │   2.5    │   2.5    │   2.5    │   2.5   │  24.0  │  16    │ ✓ DIMENSIONADO    │
│ 3 │ ADD-Banheiro-Chuveiro │ TUE  │ 34.65  │   6.0    │   2.5    │   6.0    │   6.0   │  41.0  │  40    │ ✓ DIMENSIONADO    │
│ 4 │ TUE-Forno-1           │ TUE  │   —    │    —     │    —     │    —     │    —    │   —    │   —    │ ✗ ERRO-TENSAO     │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

**Colunas:**
- **S₁**: seção por capacidade de condução (critério 1)
- **S₂**: seção mínima por aplicação (critério 2)
- **S₃**: seção por coordenação com proteção (critério 3)
- **S final**: `max(S₁, S₂, S₃)` — célula destacada em negrito
- O critério decisivo (que determinou S final) deve ter a célula com borda ou fundo diferenciado (Carbon: `$interactive-01` sutil)

### 7.3 Painel de detalhe por circuito (expansível na linha ou modal)

```
┌─────────────────────────────────────────────────────────────────────┐
│  Circuito: ADD-Banheiro-2-Chuveiro-2                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Parâmetros (override):                                            │
│  Material: [Cu ▾]  Isolação: [PVC ▾]  Método: [B1 ▾]              │
│  Temp: [30°C ▾]  Agrupados: [3 ▾]  Disposição: [feixes ▾]         │
│                                                                     │
│  Cálculo:                                                          │
│  IB = 34.65 A                                                      │
│  FCT = 1.00 (PVC, 30°C — NBR 5410 Tab. 40)                       │
│  FCA = 0.70 (feixes, 3 circuitos — NBR 5410 Tab. 42)             │
│  Iz necessário = 34.65 / (1.00 × 0.70) = 49.50 A                 │
│                                                                     │
│  Critério 1 (capacidade): 10 mm² (Iz base = 57 A, Tab. 36 B1)    │
│  Critério 2 (mínimo TUE): 2.5 mm² (Tab. 47)                      │
│  Critério 3 (In=40A → Iz≥40): 6 mm² (Iz=41A)                     │
│                                                                     │
│  ► Seção final: 10 mm² (decisivo: critério 1 — capacidade)        │
│  ► Iz real: 57 × 1.00 × 0.70 = 39.9 A                            │
│  ► In selecionado: 40 A                                            │
│                                                                     │
│  Verificações:                                                     │
│  ✓ IB (34.65) ≤ In (40)                                           │
│  ✗ In (40) ≤ Iz (39.9) — ATENÇÃO: Iz < In em 0.1 A              │
│  ⚠ Curto-circuito: NÃO VERIFICADO (módulo pendente)              │
│                                                                     │
│  Fonte: NBR 5410:2004, Tab. 36, B1, Cu PVC 3 cond. carregados     │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

**Nota:** O exemplo acima mostra um caso real onde In > Iz (40 > 39.9) — o sistema deve sinalizar isso como ATENÇÃO e sugerir subir a seção para 16 mm².

### 7.4 Resumo de dimensionamento (rodapé ou card)

```
┌───────────────────────────────────────────────────────────────────┐
│  Resumo do Dimensionamento                                        │
│                                                                   │
│  Total de circuitos: 44                                          │
│  Dimensionados: 40 ✓   Erros: 3 ✗   Pendentes: 1 ⚠             │
│                                                                   │
│  Critério decisivo mais frequente:                               │
│    Capacidade: 28 circuitos                                      │
│    Mínimo:      8 circuitos                                      │
│    Coordenação: 4 circuitos                                      │
│                                                                   │
│  Seções utilizadas: 1.5 (12×), 2.5 (18×), 4 (6×), 6 (3×),     │
│                     10 (1×)                                      │
│                                                                   │
│  ⚠ Nenhum circuito teve verificação de curto-circuito           │
│                                                                   │
└───────────────────────────────────────────────────────────────────┘
```

---

## 8. PARÂMETROS CONFIGURÁVEIS

| Parâmetro | Padrão | Fonte | [VERIFICAR] |
|-----------|--------|-------|-------------|
| Temperatura de referência PVC | 70°C (condutor) | NBR 5410 Tab. 36 nota | Sim |
| Temperatura de referência EPR/XLPE | 90°C (condutor) | NBR 5410 Tab. 37 nota | Sim |
| Temperatura ambiente padrão | 30°C | NBR 5410 Tab. 40 | Sim |
| Seção mínima Al instalações fixas | 16 mm² | NBR 5410 6.2.6.1.2 | Sim |
| Seção mínima Cu iluminação | 1.5 mm² | NBR 5410 Tab. 47 | Sim |
| Seção mínima Cu tomadas | 2.5 mm² | NBR 5410 Tab. 47 | Sim |
| Série In disjuntores | 6...125 A | IEC 60898 / fabricantes | Não |

---

## 9. CRITÉRIOS DE ACEITE

| ID | Critério | Verificação |
|----|----------|-------------|
| **CA-DC-01** | Circuito ILU Cu PVC B1 30°C 1 agrupado com IB=2.36A → seção final = 1.5 mm² (critério 2 decisivo) | Teste automatizado |
| **CA-DC-02** | Circuito TUE Cu PVC B1 30°C 3 agrupados com IB=34.65A → seção final ≥ 6 mm² (critério 1 decisivo) | Teste automatizado |
| **CA-DC-03** | Material Al com seção calculada < 16 mm² → sistema eleva para 16 mm² com alerta | Teste automatizado |
| **CA-DC-04** | Circuito com tensao_v=None → status "ERRO-TENSAO-AUSENTE", nenhum cálculo executado | Teste automatizado |
| **CA-DC-05** | Circuito sem isolação selecionada → status "ERRO-ISOLACAO-AUSENTE" | Teste automatizado |
| **CA-DC-06** | Seção final está na série IEC 60228 em 100% dos casos | Teste automatizado |
| **CA-DC-07** | Valor de Iz com `status_verificacao='[VERIFICAR]'` na tabela → dimensionamento recusado com "ERRO-TABELA-INCOMPLETA" | Teste automatizado |
| **CA-DC-08** | Campo `rastreio` contém tabela, linha, coluna, fatores FCT e FCA, e versão do módulo | Inspeção |
| **CA-DC-09** | Campo `curto_circuito_verificado` é `False` em todos os resultados desta versão | Teste automatizado |
| **CA-DC-10** | UI exibe os 3 critérios em colunas separadas e destaca o decisivo | Inspeção visual |
| **CA-DC-11** | Endpoint de lote com 44 circuitos do proj-1 retorna em < 2 segundos | Teste de performance |
| **CA-DC-12** | Quando In > Iz (falha de coordenação), sistema emite ATENÇÃO e sugere seção superior | Teste automatizado |
| **CA-DC-13** | Al em circuito ILU (seção mínima 1.5 Cu, mas Al mínimo 16) → seção final = 16 mm² Al | Teste automatizado |
| **CA-DC-14** | Dropdown de isolação é obrigatório (não tem opção vazia) — projetista sempre escolhe | Inspeção visual |
| **CA-DC-15** | Texto branco sobre fundo #fa4d56 não aparece em nenhum estado de erro | Teste automatizado |

---

## 10. ITENS [VERIFICAR]

| ID | Item | Fonte necessária | Impacto |
|----|------|-------------------|---------|
| **VER-DC-01** | Valores de Iz nas tabelas 36–39 para métodos B1 e C, Cu e Al, PVC e EPR/XLPE, seções 1.5–35 mm² | NBR 5410:2004 original | Bloqueante: sem esses valores, critério 1 não funciona |
| **VER-DC-02** | Fatores de correção por temperatura (tabela 40) — valores exatos por isolação | NBR 5410:2004 original | Bloqueante: FCT incorreto invalida todo o dimensionamento |
| **VER-DC-03** | Fatores de agrupamento (tabela 42) — valores para disposições "feixes", "camada única parede", "camada única piso" | NBR 5410:2004 original | Bloqueante: FCA incorreto invalida o dimensionamento |
| **VER-DC-04** | Seções mínimas por aplicação (tabela 47) — confirmar todos os tipos e materiais | NBR 5410:2004 original | Bloqueante |
| **VER-DC-05** | Restrição Al ≥ 16 mm² em instalações fixas — confirmar se aplica a circuitos terminais ou também alimentadores | NBR 5410:2004 seção 6.2.6.1.2 | Potencialmente bloqueante para Al |

---

## 11. SUITE DE NÃO-REGRESSÃO (pytest)

```python
import pytest
from motor_dimensionamento import dimensionar_condutor, SERIE_IEC_60228

# ─── Fixtures ───

@pytest.fixture
def circuito_ilu_basico():
    return CircuitoParaDimensionamento(
        id="ILUM-Dormitorio-1", descricao="Iluminação Dormitório 1",
        tipo="ILU", potencia_va=300, tensao_v=127,
        corrente_projeto_a=2.36, num_fases=1, fases=["R"],
        tem_neutro=True, fp_carga=1.0, fonte_ib="IB-calc-v1"
    )

@pytest.fixture
def circuito_tue_chuveiro():
    return CircuitoParaDimensionamento(
        id="ADD-Banheiro-2-Chuveiro-2", descricao="Chuveiro Banheiro 2",
        tipo="TUE", potencia_va=7700, tensao_v=220,
        corrente_projeto_a=34.65, num_fases=1, fases=["R","S"],  # bifásico 220V
        tem_neutro=False, fp_carga=1.0, fonte_ib="IB-calc-v1"
    )

@pytest.fixture
def circuito_sem_tensao():
    return CircuitoParaDimensionamento(
        id="TUE-Forno-1", descricao="Forno sem tensão",
        tipo="TUE", potencia_va=5000, tensao_v=None,
        corrente_projeto_a=0, num_fases=1, fases=["R"],
        tem_neutro=True, fp_carga=0.9, fonte_ib="IB-calc-v1"
    )

# ─── Testes CA-DC ───

def test_ca_dc_01_ilu_secao_minima(circuito_ilu_basico):
    """CA-DC-01: ILU com IB baixo → seção mínima 1.5 mm² por tabela 47."""
    r = dimensionar_condutor(circuito_ilu_basico, material="Cu", isolacao="PVC", metodo="B1")
    assert r.status == "DIMENSIONADO"
    assert r.secao_final_mm2 == 1.5
    assert r.secao_minima_aplicacao_mm2 == 1.5

def test_ca_dc_02_tue_chuveiro_capacidade(circuito_tue_chuveiro):
    """CA-DC-02: TUE alta corrente → critério 1 (capacidade) decisivo."""
    r = dimensionar_condutor(circuito_tue_chuveiro, material="Cu", isolacao="PVC",
                              metodo="B1", num_circuitos_agrupados=3)
    assert r.status == "DIMENSIONADO"
    assert r.secao_final_mm2 >= 6.0
    assert r.secao_por_capacidade_mm2 >= r.secao_minima_aplicacao_mm2

def test_ca_dc_03_al_minimo_16(circuito_ilu_basico):
    """CA-DC-03: Al sempre ≥ 16 mm²."""
    r = dimensionar_condutor(circuito_ilu_basico, material="Al", isolacao="PVC", metodo="B1")
    assert r.secao_final_mm2 >= 16.0
    assert any("16 mm²" in a for a in r.alertas)

def test_ca_dc_04_tensao_ausente(circuito_sem_tensao):
    """CA-DC-04: Tensão None → ERRO, sem cálculo."""
    r = dimensionar_condutor(circuito_sem_tensao, material="Cu", isolacao="PVC", metodo="B1")
    assert r.status == "ERRO-TENSAO-AUSENTE"
    assert r.secao_final_mm2 is None

def test_ca_dc_05_isolacao_ausente(circuito_ilu_basico):
    """CA-DC-05: Isolação não informada → ERRO."""
    r = dimensionar_condutor(circuito_ilu_basico, material="Cu", isolacao=None, metodo="B1")
    assert r.status == "ERRO-ISOLACAO-AUSENTE"

def test_ca_dc_06_serie_iec(circuito_tue_chuveiro):
    """CA-DC-06: Seção final sempre na série IEC 60228."""
    r = dimensionar_condutor(circuito_tue_chuveiro, material="Cu", isolacao="PVC", metodo="B1")
    if r.secao_final_mm2 is not None:
        assert r.secao_final_mm2 in SERIE_IEC_60228

def test_ca_dc_09_curto_circuito_pendente(circuito_ilu_basico):
    """CA-DC-09: curto_circuito_verificado é sempre False."""
    r = dimensionar_condutor(circuito_ilu_basico, material="Cu", isolacao="PVC", metodo="B1")
    assert r.curto_circuito_verificado is False

def test_ca_dc_12_coordenacao_alerta():
    """CA-DC-12: Se In > Iz, emitir ATENÇÃO."""
    # Construir cenário onde FCA reduz Iz abaixo de In
    circuito = CircuitoParaDimensionamento(
        id="TESTE-COORD", descricao="Teste coordenação",
        tipo="TUE", potencia_va=4400, tensao_v=220,
        corrente_projeto_a=20.0, num_fases=1, fases=["R","S"],
        tem_neutro=False, fp_carga=1.0, fonte_ib="teste"
    )
    r = dimensionar_condutor(circuito, material="Cu", isolacao="PVC", metodo="B1",
                              num_circuitos_agrupados=9)  # FCA muito baixo
    if r.in_menor_iz == False:
        assert any("ATENÇÃO" in a or "coordenação" in a.lower() for a in r.alertas)

def test_ca_dc_13_al_ilu_16mm2(circuito_ilu_basico):
    """CA-DC-13: Al em ILU → 16 mm² (não 1.5 ou 2.5)."""
    r = dimensionar_condutor(circuito_ilu_basico, material="Al", isolacao="PVC", metodo="B1")
    assert r.secao_final_mm2 == 16.0
```

---

## 12. NÃO TOCAR

- Módulo de Cargas (levantamento de cargas)
- Módulo de Demanda (cálculo de demanda, fatores de demanda)
- Módulo IB (cálculo de corrente de projeto)
- Adaptador 1:1 de circuitos (provisório)
- Módulo de Categoria de Entrada (Saída A / Saída B)
- Tabelas 001/002 (subcategoria EDP)
- Fórmula de demanda EDP (D = a+b+...+i)
- Mapeamento de fases (R/S/T e helper ABC→RST)

---

## 13. FORA DE ESCOPO (não implementar neste módulo)

- Cálculo de queda de tensão (módulo MOD-QT separado)
- Cálculo de curto-circuito / integral I²t (módulo MOD-CC futuro)
- Seleção automática de DR (módulo MOD-DR futuro)
- Dimensionamento de eletrodutos (módulo MOD-ELET futuro)
- Diagrama unifilar (módulo MOD-UNIF com PRD próprio)
- Relatório técnico / memorial descritivo
- Planejador de circuitos real (substituição do adaptador 1:1)
