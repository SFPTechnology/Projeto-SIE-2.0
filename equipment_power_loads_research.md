# Pesquisa de Cargas — Equipamentos Comerciais e Industriais

**Data:** 2026-06-20  
**Objetivo:** Compilar dados de potência (kW, CV) para equipamentos comerciais e industriais conforme normas NBR/ISO

---

## Seção 1: Equipamentos Comerciais (Baixa/Média Tensão)

### 1.1 Cozinha Profissional

| Equipamento | Tipo Motor | Potência | Tensão | Modo | Notas |
|-------------|-----------|----------|--------|------|-------|
| Máquina de café comercial | Motor 1 CV | 0,75 kW | 127/220V | Monofásico | Bomba + motor resistência |
| Forno convecção prof. | Resistência/Motor | 3-6 kW | 220/380V | Mono/Trifásico | Depende de capacidade |
| Refrigerador comercial | Motor 0,5-1 CV | 0,37-0,75 kW | 220V | Monofásico | Compressor hermético |
| Freezer vertical prof. | Motor 1,5 CV | 1,1 kW | 220/380V | Mono/Trifásico | Compressor |
| Fryer comercial (1 cuba) | Resistência | 3-5 kW | 220/380V | Monofásico | Imersão óleo |
| Fryer dupla | Resistência | 8-10 kW | 380V | Trifásico | Alta demanda |
| Chapa aquecedora prof. | Resistência | 2-4 kW | 220/380V | Mono/Tri | Controle termostático |
| Liquidificador industrial | Motor 1-2 CV | 0,75-1,5 kW | 220V | Monofásico | Uso intermitente |

**Normas:** NBR 5410 (instalações), NBR 12094 (equipamentos)

---

### 1.2 Ar Comprimido & Bombas

| Equipamento | Potência Motor | CV | kW | Tensão | Tipo | Notas |
|-------------|----------------|----|----|--------|------|-------|
| Compressor 1 CV | 1 CV | 1 | 0,75 | 220V | Monofásico | Pequeno comércio |
| Compressor 2 CV | 2 CV | 2 | 1,5 | 220/380V | Mono/Trifásico | Oficinas |
| Compressor 5 CV | 5 CV | 5 | 3,7 | 380V | Trifásico | Uso industrial |
| Compressor 10 CV | 10 CV | 10 | 7,5 | 380V | Trifásico | Alta demanda |
| Bomba hidráulica 2 CV | 2 CV | 2 | 1,5 | 220/380V | Variável | Prensas |
| Bomba centrífuga 3 CV | 3 CV | 3 | 2,2 | 380V | Trifásico | Circulação |

**Norma de referência:** NBR ISO 5167 (potência), ISO 8573 (qualidade ar)

**Conversão padrão:** 1 CV = 0,735 kW (aproximado: 1 CV ≈ 0,75 kW)

---

### 1.3 Câmara Frigorífica (Walk-in/Comercial)

| Equipamento | Volume | Potência Compressor | Tensão | Tipo | Notas |
|-------------|--------|-------------------|--------|------|-------|
| Câmara pequena | 4-8 m³ | 1-2 CV (0,75-1,5 kW) | 220V | Mono | -18°C |
| Câmara média | 12-20 m³ | 3 CV (2,2 kW) | 380V | Trifásico | -18°C a -10°C |
| Câmara grande | 30-50 m³ | 5-7,5 CV (3,7-5,6 kW) | 380V | Trifásico | Armazenamento |
| Câmara ultrabaixa | 10-15 m³ | 5 CV (3,7 kW) | 380V | Trifásico | -25°C a -40°C |

**Fator de carga:** Ciclos compressor ~80% duty cycle

---

## Seção 2: Equipamentos Industriais (Média/Alta Tensão)

### 2.1 Motores Trifásicos — Classificação NBR/ISO

| CV | kW | Corrente 380V (A) | Rendimento % | Fator Potência | Norma |
|----|----|--------------------|--------------|----------------|-------|
| 0,5 | 0,37 | 1,2 | 70 | 0,80 | NBR 17094 |
| 1 | 0,75 | 2,0 | 75 | 0,82 | NBR 17094 |
| 2 | 1,5 | 3,8 | 78 | 0,84 | NBR 17094 |
| 3 | 2,2 | 5,5 | 80 | 0,85 | NBR 17094 |
| 5 | 3,7 | 9,0 | 82 | 0,86 | NBR 17094 |
| 7,5 | 5,5 | 13,0 | 84 | 0,87 | NBR 17094 |
| 10 | 7,5 | 17,5 | 85 | 0,87 | NBR 17094 |
| 15 | 11 | 26 | 87 | 0,88 | NBR 17094 |
| 20 | 15 | 35 | 88 | 0,88 | NBR 17094 |
| 25 | 18,5 | 43 | 89 | 0,89 | NBR 17094 |
| 30 | 22 | 51 | 89 | 0,89 | NBR 17094 |
| 40 | 30 | 70 | 90 | 0,90 | NBR 17094 |
| 50 | 37 | 87 | 91 | 0,91 | NBR 17094 |
| 60 | 45 | 105 | 91 | 0,91 | NBR 17094 |
| 75 | 55 | 130 | 91 | 0,92 | NBR 17094 |
| 100 | 75 | 175 | 92 | 0,92 | NBR 17094 |

**Notas:**
- NBR 17094 = Motores assíncronos trifásicos (ex-NBR 5883)
- Rendimento aumenta com potência
- Fator de potência (cosφ) típico 0,80-0,92
- Corrente calculada: P(kW) ÷ (√3 × V × η × cosφ)

---

### 2.2 Máquinas de Solda

| Tipo | Modelo Típico | Potência | Tensão Entrada | Modo | Notas |
|------|--------------|----------|----------------|------|-------|
| Soldadora MIG-MAG | Small 150A | 6-8 kW | 220V | Monofásico | Hobby/pequeno comércio |
| Soldadora MIG-MAG | Medium 200A | 10-12 kW | 380V | Trifásico | Oficina padrão |
| Soldadora MIG-MAG | Industrial 400A | 20-30 kW | 380V | Trifásico | Fabricação |
| Soldadora TIG | 200A AC/DC | 8-10 kW | 380V | Trifásico | Alumínio |
| Soldadora TIG | 315A AC/DC | 15-20 kW | 380V | Trifásico | Aço inox |
| Soldadora stick | 200A | 6-8 kW | 220/380V | Mono/Tri | Básica |
| Soldadora stick | 400A | 15-20 kW | 380V | Trifásico | Industrial |

**Norma:** NBR IEC 60974 (sistemas de soldagem)

**Duty cycle:** 50%, 60%, 100% (contínuo) — afeta carga real

---

### 2.3 Equipamentos de Fabricação

#### 2.3.1 Prensa Hidráulica

| Capacidade | Motor Bomba | Pressão | Potência Instalada | Tensão | Notas |
|-----------|-----------|---------|-------------------|--------|-------|
| 10 ton | 1-2 CV | 140 bar | 1,5-2 kW | 220V | Pequena |
| 20 ton | 2 CV | 140 bar | 1,5 kW | 220V | Lab/pequena oficina |
| 50 ton | 3-5 CV | 140 bar | 2,2-3,7 kW | 380V | Oficina |
| 100 ton | 5-7,5 CV | 140 bar | 3,7-5,5 kW | 380V | Industrial |
| 200 ton | 10 CV | 140 bar | 7,5 kW | 380V | Produção |
| 500 ton | 15-20 CV | 210 bar | 11-15 kW | 380V | Grande indústria |

**Fator de uso:** 60-70% do tempo máquina está ciclo pressão

---

#### 2.3.2 CNC/Fresadora

| Equipamento | Potência Spindle | Motor Eixo Z | Total | Tensão | Notas |
|-----------|-----------------|-------------|-------|--------|-------|
| CNC Pequena (VMC) | 3-5 kW | 1,5 kW | 5-8 kW | 380V | Usinagem leve |
| CNC Média | 8-15 kW | 2-3 kW | 12-18 kW | 380V | Produção padrão |
| CNC Grande | 20-30 kW | 5-7,5 kW | 25-35 kW | 380V | Alto volume |
| Fresadora manual | 3-5 kW | 1,5-2 kW | 5-7 kW | 220V | Oficina |
| Fresadora universal | 5-10 kW | 2-3 kW | 8-12 kW | 380V | Multipropósito |

**Norma:** ISO 12922 (óleos), NBR 6162 (usinagem)

---

#### 2.3.3 Tornos

| Tipo | Potência Motor | Voltagem | Categoria | Notas |
|------|--------------|----------|-----------|-------|
| Torno de bancada | 0,5-1 CV (0,37-0,75 kW) | 220V | Hobby |  |
| Torno paralelo pequeno | 1-2 CV (0,75-1,5 kW) | 220V | Oficina |  |
| Torno paralelo médio | 3-5 CV (2,2-3,7 kW) | 380V | Produção | Mais comum |
| Torno paralelo grande | 7,5-10 CV (5,5-7,5 kW) | 380V | Pesado | Peças grandes |
| Torno CNC | 5-15 CV (3,7-11 kW) | 380V | Automação | Spindle + servos |

---

### 2.4 Fornos Industriais

| Tipo Forno | Capacidade | Potência | Tensão | Tempo Aquecimento | Notas |
|-----------|-----------|----------|--------|------------------|-------|
| Forno de resistência | 1 m³ | 6-10 kW | 380V | 30-60 min | Tratamento térmico |
| Forno mufla | 0,5 m³ | 3-6 kW | 220/380V | 20-40 min | Laboratório |
| Forno industrial | 2-5 m³ | 15-25 kW | 380V | 1-2 h | Ceramista/vidro |
| Forno de câmara | 5-10 m³ | 30-50 kW | 380V | 2-4 h | Produção contínua |
| Forno indução | Variável | 10-50 kW | 380V | Contínuo | Fusão metal |
| Estufa industrial | 1 m³ | 3-5 kW | 220/380V | 20-40 min | Secagem |
| Autoclave | Variável | 5-15 kW | 380V | Ciclo | Esterilização |

**Consumo específico:** ~5-10 kWh por m³ por ciclo (típico)

---

## Seção 3: Tabela Consolidada — Referência Rápida

| Equipamento | CV | kW | Tensão | Modo | Norma | Categoria |
|-----------|----|----|--------|------|-------|-----------|
| **COMERCIAL** | | | | | | |
| Máquina café prof. | 1 | 0,75 | 220V | Mono | NBR 12094 | Cozinha |
| Forno convecção | 2-4 | 1,5-3 | 380V | Tri | NBR 12094 | Cozinha |
| Refrigerador prof. | 0,5-1 | 0,37-0,75 | 220V | Mono | IEC 62552 | Climatização |
| Compressor 5 CV | 5 | 3,7 | 380V | Tri | NBR ISO 5167 | Ar comprimido |
| Câmara frigorif. | 3-5 | 2,2-3,7 | 380V | Tri | IEC 60335 | Refrigeração |
| **INDUSTRIAL** | | | | | | |
| Motor padrão | 1-100 | 0,75-75 | 380V | Tri | NBR 17094 | Geral |
| Soldadora MIG 200A | — | 10-12 | 380V | Tri | NBR IEC 60974 | Solda |
| Prensa 100 ton | 5-7,5 | 3,7-5,5 | 380V | Tri | NBR 6162 | Conformação |
| CNC médio | — | 12-18 | 380V | Tri | ISO 12922 | Usinagem |
| Forno resistência | — | 15-25 | 380V | Tri | NBR 13830 | Tratamento |
| Torno paralelo | 3-5 | 2,2-3,7 | 380V | Tri | ISO 1402 | Usinagem |

---

## Conversões e Fatores

### Conversão CV ↔ kW
- **1 CV = 0,735 kW** (exato)
- **1 CV ≈ 0,75 kW** (aproximação comum indústria)
- **1 HP = 0,746 kW** (padrão americano)

### Fator de Simultaneidade
Para painéis de distribuição com múltiplos equipamentos:
- Máquinas intermitentes: 60-70%
- Motores contínuos: 80-100%
- Equipamentos aquecimento: 90-100%
- Refrigeração: 60-80%

### Fator de Potência (cosφ)
- Motores 0,75-1 kW: 0,75-0,80
- Motores 1-5 kW: 0,80-0,85
- Motores 5-50 kW: 0,85-0,90
- Motores >50 kW: 0,90-0,92
- Resistências: 1,0 (puramente ativa)

### Corrente Trifásica 380V
```
I (A) = P (kW) × 1000 ÷ (√3 × 380 × cosφ × η)
I (A) = P (kW) / 0,656
```
*Exemplo: Motor 7,5 kW, cosφ=0,87, η=0,85 → I ≈ 17,5 A*

---

## Normas de Referência

| Norma | Descrição | Escopo |
|-------|-----------|--------|
| **NBR 5410** | Instalações elétricas BT | Circuitos, dimensionamento |
| **NBR 17094** | Motores assíncronos trifásicos | Classificação, potências |
| **NBR 12094** | Equipamentos comerciais | Cozinha profissional |
| **NBR ISO 5167** | Ar comprimido e vácuo | Qualidade, potência |
| **NBR IEC 60974** | Sistemas de soldagem | MIG/TIG/Stick |
| **NBR 6162** | Usinagem | Tolerâncias, segurança |
| **NBR 13830** | Fornos industriais | Classificação, desempenho |
| **ISO 1402** | Tornos paralelos | Dimensões, especificações |
| **ISO 12922** | Óleos de corte | Qualidade |
| **IEC 62552** | Refrigeradores comerciais | Consumo, eficiência |
| **IEC 60335** | Segurança equipamentos | Uso doméstico/comercial |

---

## Notas Importantes

### Cargas de Arranque
- Motores assíncronos: Corrente inicial **4-7× corrente nominal**
- Duração: **0,1-5 segundos** (depende de carga inercial)
- Queda de tensão durante arranque: 5-15% (dimensionar fiação!)

### Fator Potência e Harmônicos
- Conversores de frequência (VFD): geram harmônicos 5º, 7º, 11º
- Fator potência desbalanceado em trifásico: Verificar com analisador
- Capacitor correção: Instalar com filtro LC apropriado

### Seleção de Disjuntor/Fusível
- Proteção térmica: I_nominal ≤ Izt (tempo de fusão)
- Proteção magnética: I_trip ≈ 10-15 × I_nominal
- Referência: NBR 5410, tabela com seção e corrente máxima

---

**Compilação:** 2026-06-20 | Fontes: NBR, ISO, IEC, fabricantes | Próxima revisão: 2026-12-20
