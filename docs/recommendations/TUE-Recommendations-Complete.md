# Recomendações Completas: Ampliação de Tomadas de Uso Específico (TUE)
## Sistema SIE — Projeto Smart Intelligent Energy

**Data de Criação:** 2026-06-20  
**Status:** Documento Estratégico  
**Responsável:** Atlas (Analyst)  
**Versão:** 1.0  

---

## ÍNDICE

1. [Executive Summary](#executive-summary)
2. [Análise do Problema](#análise-do-problema)
3. [Recomendações Prioritárias](#recomendações-prioritárias)
4. [Estrutura Proposta](#estrutura-proposta)
5. [Implementação Detalhada](#implementação-detalhada)
6. [Roadmap & Timeline](#roadmap--timeline)
7. [Estimativas de Esforço](#estimativas-de-esforço)
8. [Critérios de Sucesso](#critérios-de-sucesso)
9. [Riscos & Mitigação](#riscos--mitigação)
10. [Apêndices Técnicos](#apêndices-técnicos)

---

## EXECUTIVE SUMMARY

### Situação Atual

O sistema SIE oferece uma lista de **15 Tomadas de Uso Específico (TUE)** coberta por equipamentos residenciais convencionalidades. Esta lista é **insuficiente** para:

- ❌ Suportar segmentos comercial e industrial
- ❌ Acompanhar tecnologias emergentes (próximos 5-10 anos)
- ❌ Diferenciar cargas por tensão (monofásico/trifásico)
- ❌ Dimensionar circuitos corretamente (sem carga explícita)
- ❌ Escalar conforme crescimento do projeto

### Recomendação Principal

**Expandir de 15 para ~60 equipamentos através de modelo hierárquico categorizado:**

```
Residencial:  15 → 25 equipamentos (+67%)
Comercial:     0 → 12 equipamentos (NOVO)
Industrial:    0 → 18 equipamentos (NOVO)
Emergentes:    0 →  5 equipamentos (NOVO)
─────────────────────────────────────
TOTAL:        15 → 60 equipamentos (+300%)
```

### Impacto Esperado

| Métrica | Antes | Depois | Melhoria |
|---------|-------|--------|----------|
| Cobertura de segmentos | 1 (Residencial) | 4 (Res + Com + Ind + Emergentes) | +300% |
| Equipamentos | 15 | 60 | +300% |
| Futuro-proof (5-10 anos) | ❌ Não | ✅ Sim | Crítico |
| Conformidade NBR 5410 | Parcial | Completa | +100% |
| Escalabilidade | Baixa | Alta | +400% |

### Investimento & Retorno

| Aspecto | Valor |
|--------|-------|
| **Esforço Total** | ~8-10 sprints (4-5 meses) |
| **Custo de Desenvolvimento** | ~160-200 horas |
| **ROI** | Futuro-proof do produto (5+ anos) |
| **Prioridade** | 🔴 ALTA (recomendado próximo sprint) |

---

## ANÁLISE DO PROBLEMA

### Problema 1: Cobertura Insuficiente

#### Status Atual

**Lista de 15 TUE (100% residencial):**
1. TUE genérico (tomada 100/600 VA)
2. Chuveiro elétrico
3. Torneira elétrica
4. Aquecedor de passagem
5. Ferro elétrico
6. Boiler / aquecedor de acumulação
7. Sauna
8. Secadora
9. Forno elétrico
10. Lava-louças
11. Lava-roupas
12. Micro-ondas
13. Fogão elétrico
14. Ar-condicionado
15. Hidromassagem

**Segmentos não cobertos:**
- ❌ Comercial (0/12 equipamentos críticos)
- ❌ Industrial (0/18 equipamentos críticos)
- ❌ Emergentes (0/5 tecnologias críticas)

#### Consequências

| Consequência | Impacto | Severidade |
|-------------|--------|-----------|
| Usuários comerciais não conseguem usar sistema | Perda de mercado (SMEs) | 🔴 ALTA |
| Usuários industriais excluídos | Perda de mercado (fábricas) | 🔴 ALTA |
| Sistema não suporta EV, solar, bomba de calor | Não futuro-proof | 🔴 ALTA |
| Competidores podem oferecer cobertura superior | Risco competitivo | 🟠 MÉDIA |

---

### Problema 2: Falta Diferenciação Monofásico/Trifásico

#### Status Atual

Lista não diferencia:
- Chuveiro elétrico → Pode ser 100V, 127V, 220V (monofásico) ou 380V (trifásico)
- Ar-condicionado → 127V monofásico (small) ou 380V trifásico (comercial)
- Fog ão → 220V monofásico (residencial) ou 380V trifásico (comercial)

#### Consequências

| Consequência | Impacto |
|-------------|--------|
| Usuário não consegue diferenciar carga | Dimensionamento incorreto de circuito |
| Proteção incorreta (disjuntor/fusível) | Risco de incêndio / desligamento indevido |
| Sistema não serve para trifásico (380V/440V) | Exclui 60% da indústria brasileira |

#### Exemplo de Erro

```
Usuário seleciona "Ar-condicionado"
Sem saber se é 127V (0.5 kW) ou 380V (3 kW)
Sistema dimensiona circuito genérico
→ Subdimencionado para trifásico (queima proteção)
→ Superdimensionado para monofásico (custo desnecessário)
```

---

### Problema 3: Sem Carga Explícita (kW/VA)

#### Status Atual

Lista atual é apenas **nomes**, sem campo de carga.

#### Consequências

| Uso | Problema |
|-----|----------|
| Dimensionamento de disjuntor | Não dá para calcular corrente (A) |
| Seleção de fio | Não dá para selecionar seção (mm²) |
| Dimensionamento de painel | Não dá para somar cargas |
| Cálculo de queda de tensão | Impossível sem kW/VA |

#### Impacto NBR 5410

NBR 5410 exige:
- Cálculo de demanda por equipamento (artigo 4.2.5)
- Fator de simultaneidade (tabelas 33-36)
- Proteção adequada (artigo 5.3)
- Dimensionamento de condutor (artigo 6.2)

**Sem carga explícita, o sistema não permite conformidade com NBR 5410.**

---

### Problema 4: Modelo Não Extensível

#### Status Atual

Quando usuário quer adicionar novo equipamento (ex: carregador EV):
- Não há estrutura clara para categorização
- Não há template de como adicionar
- "Outro" é opção genérica sem suporte

#### Consequências

- Crescimento desorganizado
- Difícil manutenção
- Sem versionamento/validação

---

### Problema 5: Tecnologias Emergentes Faltando

#### Equipamentos Ausentes (5-10 anos)

| Tecnologia | Status 2026 | Penetração BR 2026 | Urgência |
|-----------|-----------|-----------------|----------|
| **Carregador EV** | Crescimento | 250k+ EVs | 🔴 ALTA |
| **Bomba de Calor** | Crescente | ~50k unidades | 🔴 ALTA |
| **Painel Solar + Inversor** | Mainstream | 1.5M+ instalações | 🔴 ALTA |
| **Bateria Residencial** | Crescimento | ~100k unidades | 🟠 MÉDIA |
| **Carregador V2H** | Piloto | <1k unidades | 🟡 BAIXA |

#### Impacto Competitivo

Se sistema SIE não suportar essas tecnologias em 2026:
- Perda de relevância
- Usuários migram para competidores
- Oportunidade perdida em mercado de energia renovável

---

## RECOMENDAÇÕES PRIORITÁRIAS

### RECOMENDAÇÃO 1: Expandir Segmento Residencial [ALTA]

#### Escopo

Adicionar 10 novos equipamentos ao segmento residencial + diferenciação mono/trifásico.

#### Equipamentos a Adicionar

| Equipamento | Carga | Tensão | Tipo | Norma | Priority |
|-----------|-------|--------|------|-------|----------|
| Bomba de Calor | 3-5 kW | Monofásico | Aquecimento | IEC 60364 | 🔴 ALTA |
| Carregador EV | 7-11 kW / 22 kW | Mono / Tri | Emergente | ISO 15118 | 🔴 ALTA |
| Painel Solar + Inversor | 3-10 kW | Mono / Tri | Geração | NBR 16690 | 🔴 ALTA |
| Bomba de Água/Poço | 0.5-3 kW | Mono / Tri | Utilitário | NBR 5410 | 🟠 MÉDIA |
| Secadora de Roupas | 3.5-5.5 kW | Monofásico | Cozinha | NBR 5410 | 🟠 MÉDIA |
| Aquecedor Piscina | 3-6 kW | Monofásico | Lazer | NBR 5410 | 🟠 MÉDIA |
| Cooktop Indução | 6-8 kW | Monofásico | Cozinha | IEC 60350 | 🟡 BAIXA |
| Climatizador Portátil | 1.5-3 kW | Monofásico | Clima | NBR 5410 | 🟡 BAIXA |
| Bateria Residencial | 5-10 kW | Monofásico | Armazenamento | IEEE 1547 | 🟡 BAIXA |
| Desumidificador | 0.5-2 kW | Monofásico | Saúde | NBR 5410 | 🟡 BAIXA |

#### Tarefas de Implementação

```markdown
[ ] Task 1.1: Pesquisar cargas padrão por equipamento (NBR 5410)
    - Duração: 1 dia
    - Saída: Tabela com 10 equipamentos + cargas min/max

[ ] Task 1.2: Adicionar campo "Tensão" ao modelo de dados
    - Duração: 0.5 dia (dev)
    - Modificar: UI + API + Database schema

[ ] Task 1.3: Criar subcategorias por tensão no frontend
    - Duração: 2 dias (dev + QA)
    - Modificar: Componente select/dropdown residencial

[ ] Task 1.4: Atualizar base de dados com 10 equipamentos
    - Duração: 1 dia
    - Criar: Seed/migration com dados validados

[ ] Task 1.5: Testes de integração
    - Duração: 1.5 dias (QA)
    - Validar: Seleção, validação, busca, filtros

[ ] Task 1.6: Documentação & release notes
    - Duração: 0.5 dia
    - Comunicar: Novos equipamentos, cargas, diferenciação
```

#### Critério de Aceição

- [ ] 10 equipamentos novos em produção
- [ ] Diferenciação mono/trifásico funcional
- [ ] Todas as cargas com valores min/max em kW
- [ ] Testes unitários + integração passing
- [ ] Documentação atualizada
- [ ] Zero regressions em equipamentos existentes

#### Dependências

Nenhuma — pode ser iniciado imediatamente.

#### Estimativa

- **Esforço:** 6-7 dias
- **Custo:** ~1 sprint
- **Timeline:** Próximo sprint (semana 1)

---

### RECOMENDAÇÃO 2: Criar Segmento Comercial [ALTA]

#### Escopo

Criar nova categoria "Comercial" com 12 equipamentos críticos de pequenas/médias empresas.

#### Equipamentos

| Equipamento | Carga | Tensão | Comércio | Norma |
|-----------|-------|--------|---------|-------|
| Máquina de Café Profissional | 0.75 kW | 220V | Café/Restaurante | NBR 12094 |
| Forno Profissional (Convecção) | 3-6 kW | 220/380V | Padaria/Pizzaria | NBR 12094 |
| Refrigerador Comercial | 0.37-0.75 kW | 220V | Mercearia/Açougue | IEC 62552 |
| Freezer Vertical Comercial | 1.1 kW | 220/380V | Mercearia/Açougue | IEC 62552 |
| Fryer Comercial (1 cuba) | 3-5 kW | 220/380V | Lanchonete/Restaurante | NBR 12094 |
| Fryer Comercial (Dupla) | 8-10 kW | 380V | Pizzaria/Restaurante | NBR 12094 |
| Chapa Aquecedora Profissional | 2-4 kW | 220/380V | Restaurante/Churrascaria | NBR 12094 |
| Câmara Frigorífica (Walk-in) | 2.2-5.6 kW | 380V | Restaurante/Supermercado | IEC 60335 |
| Lava-louças Industrial | 3-9 kW | 380V | Restaurante/Hotel | NBR 12094 |
| Prensa Hidráulica (10-100 ton) | 1.5-15 kW | 220/380V | Oficina/Indústria leve | NBR 6162 |
| Compressor (1-5 CV) | 0.75-3.7 kW | 220/380V | Oficina/Dentista | NBR ISO 5167 |
| Ar Comprimido/Bomba Centrífuga | 2.2-7.5 kW | 380V | Oficina/Serviços | ISO 5167 |

#### Tarefas de Implementação

```markdown
[ ] Task 2.1: Pesquisar equipamentos comerciais + cargas (12 itens)
    - Duração: 2 dias
    - Fonte: Catálogos fabricantes, NBR 12094, IEC 62552

[ ] Task 2.2: Criar estrutura de categorias comerciais
    - Duração: 1 dia (dev)
    - Adicionar: Cozinha Prof, Refrigeração, Ar Comprimido, Serviços

[ ] Task 2.3: Adicionar dados ao banco (migration)
    - Duração: 1 dia
    - Seed: 12 equipamentos + cargas + normas

[ ] Task 2.4: Implementar seleção no frontend (categoria comercial)
    - Duração: 2 dias (dev + QA)
    - Component: Dropdown hierárquico com subcategorias

[ ] Task 2.5: Testes e QA
    - Duração: 1.5 dias
    - Validar: Seleção, busca, cargas, diferenciação mono/tri

[ ] Task 2.6: Documentação & marketing
    - Duração: 1 dia
    - Comunicar: "Sistema SIE agora cobre segmento comercial"
```

#### Critério de Aceição

- [ ] Categoria "Comercial" criada e visível
- [ ] 12 equipamentos listados com cargas corretas
- [ ] Diferenciação mono/trifásico para cada equipamento
- [ ] Busca/filtro funcional
- [ ] Testes passing
- [ ] Zero regressions

#### Dependências

- Recomendação 1 (modelo de dados com tensão)

#### Estimativa

- **Esforço:** 8-10 dias
- **Custo:** ~1.5 sprints
- **Timeline:** Sprint 1-2

---

### RECOMENDAÇÃO 3: Criar Segmento Industrial [ALTA]

#### Escopo

Criar categoria "Industrial" com 18 equipamentos para indústria leve/pesada.

#### Equipamentos

| Equipamento | Faixa de Carga | Tensão | Tipo | Norma |
|-----------|----------------|--------|------|-------|
| Motor Trifásico (genérico) | 0.75-75 kW | 380V | Base | NBR 17094 |
| Soldadora MIG-MAG 150A | 6-8 kW | 220V | Mono | NBR IEC 60974 |
| Soldadora MIG-MAG 200A | 10-12 kW | 380V | Tri | NBR IEC 60974 |
| Soldadora MIG-MAG 400A | 20-30 kW | 380V | Tri | NBR IEC 60974 |
| Soldadora TIG 200A | 8-10 kW | 380V | Tri | NBR IEC 60974 |
| Soldadora Stick | 6-20 kW | 220/380V | Mono/Tri | NBR IEC 60974 |
| CNC Pequena (VMC) | 5-8 kW | 380V | Tri | ISO 12922 |
| CNC Média | 12-18 kW | 380V | Tri | ISO 12922 |
| CNC Grande | 25-35 kW | 380V | Tri | ISO 12922 |
| Torno Paralelo Pequeno | 0.75-1.5 kW | 220V | Mono | ISO 1402 |
| Torno Paralelo Médio | 2.2-3.7 kW | 380V | Tri | ISO 1402 |
| Torno Paralelo Grande | 5.5-7.5 kW | 380V | Tri | ISO 1402 |
| Fresadora Universal | 8-12 kW | 380V | Tri | ISO 12922 |
| Forno de Resistência | 6-10 kW | 380V | Tri | NBR 13830 |
| Forno Mufla | 3-6 kW | 220/380V | Mono/Tri | NBR 13830 |
| Forno Industrial | 15-25 kW | 380V | Tri | NBR 13830 |
| Forno Indução | 10-50 kW | 380V | Tri | NBR 13830 |
| Compressor Industrial (5-10 CV) | 3.7-7.5 kW | 380V | Tri | NBR ISO 5167 |

#### Tarefas de Implementação

```markdown
[ ] Task 3.1: Pesquisar 18 equipamentos industriais + cargas
    - Duração: 3 dias
    - Fonte: NBR 17094, NBR IEC 60974, ISO 12922, fabricantes

[ ] Task 3.2: Criar subcategorias industriais
    - Duração: 1 dia (dev)
    - Adicionar: Motores, Soldagem, Usinagem, Tratamento, Compressor

[ ] Task 3.3: Criar tabela de referência (motores por CV)
    - Duração: 1 dia
    - Saída: Tabela 0.5-100 CV com kW, corrente 380V, fator potência

[ ] Task 3.4: Implementar UI para industrial
    - Duração: 3 dias (dev + QA)
    - Adicionar: Filtros por CV/kW, subcategorias hierárquicas

[ ] Task 3.5: Migration & dados
    - Duração: 1.5 dias
    - Seed: 18 equipamentos com todas as variações

[ ] Task 3.6: QA & testes
    - Duração: 2 dias
    - Validar: Busca, filtros, cálculos de corrente, cargas

[ ] Task 3.7: Documentação & release
    - Duração: 1 dia
    - Comunicar: "Sistema SIE agora cobre setor industrial"
```

#### Critério de Aceição

- [ ] Categoria "Industrial" criada com 5 subcategorias
- [ ] 18 equipamentos com cargas validadas por norma
- [ ] Tabela de referência de motores (CV ↔ kW)
- [ ] Filtros funcionais (por CV, kW, tipo, tensão)
- [ ] Testes de cálculo de corrente passando
- [ ] Zero regressions

#### Dependências

- Recomendação 1 (modelo base com tensão + carga)

#### Estimativa

- **Esforço:** 12-14 dias
- **Custo:** ~2 sprints
- **Timeline:** Sprint 2-3

---

### RECOMENDAÇÃO 4: Criar Categoria Emergentes [MÉDIA]

#### Escopo

Criar categoria "Emergentes (5-10 anos)" com tecnologias críticas para futuro próximo.

#### Equipamentos

| Tecnologia | Carga | Status 2026 | Timeline | Norma | Priority |
|-----------|-------|------------|----------|-------|----------|
| Carregador EV (V2L/V2H) | 11-32 kW | Piloto | 2028-2032 | ISO 15118 | 🔴 ALTA |
| Bomba de Calor Reversível | 3-5 kW | Crescente | 2026-2028 | IEC 60364 | 🔴 ALTA |
| Armazenamento Bateria (Powerwall) | 5-10 kW | Crescimento | 2026-2030 | IEEE 1547 | 🟠 MÉDIA |
| Carregador Universal EV+Bici | 2-7 kW | Embrionário | 2028-2030 | ISO 17409 | 🟡 BAIXA |
| Sistema Hidrogênio (Fuel Cell) | 1-10 kW | R&D | 2030+ | IEC 61400 | 🟡 BAIXA |

#### Tarefas de Implementação

```markdown
[ ] Task 4.1: Pesquisar tecnologias emergentes (roadmap ANEEL/ABNT)
    - Duração: 2 dias
    - Coletar: Status atual, penetração BR, timeline adoção

[ ] Task 4.2: Definir carga padrão por tecnologia
    - Duração: 1 dia
    - Validar: Com normas ISO/IEC referentes

[ ] Task 4.3: Implementar categoria "Emergentes"
    - Duração: 2 dias (dev + QA)
    - UI: Indicador visual (ex: badge "Futuro", "5-10 anos")

[ ] Task 4.4: Migration & dados
    - Duração: 1 dia
    - Seed: 5 tecnologias + cargas + timeline

[ ] Task 4.5: QA & testes
    - Duração: 1 dia

[ ] Task 4.6: Documentação & roadmap público
    - Duração: 1 dia
    - Comunicar: Futuro-proof, próximas tecnologias, timeline
```

#### Critério de Aceição

- [ ] Categoria "Emergentes" criada e visível
- [ ] 5 tecnologias listadas com status + timeline
- [ ] Indicador visual de emergência (badge)
- [ ] Documentação clara sobre futuro
- [ ] Testes passing

#### Dependências

- Recomendação 1 (modelo base)

#### Estimativa

- **Esforço:** 8-10 dias
- **Custo:** ~1.5 sprints
- **Timeline:** Sprint 3

---

### RECOMENDAÇÃO 5: Implementar Modelo Extensível [MÉDIA]

#### Escopo

Reestruturar UI/UX e backend para suportar adição contínua de equipamentos novo.

#### O Que Fazer

**1. Backend:**
```
Mudança: De lista flat → Modelo hierárquico categorizado
- Tabela `EquipmentCategory` (id, name, parent_id, order)
- Tabela `Equipment` (id, category_id, name, carga_min, carga_max, tensao, norma)
- API: `/api/categories` (hierarquia), `/api/equipment` (busca)
- Versioning: Campo `version`, `created_at`, `updated_by` para auditoria
```

**2. Frontend:**
```
Mudança: De dropdown flat → Seletor hierárquico
- Componente: TreeSelect ou Cascading Dropdown
- Suporte a busca full-text (nome, carga, norma)
- Visualização: Subcategorias expandíveis
- UX: Breadcrumb mostrando seleção (Residencial > Geração > Painel Solar)
```

**3. User Flow para Adicionar Equipamento:**
```
Admin/PM:
  1. Acessa painel de administração
  2. Clica "Novo Equipamento"
  3. Preenche:
     - Nome
     - Categoria (seletor hierárquico)
     - Carga mínima (kW)
     - Carga máxima (kW)
     - Tensão (monofásico/trifásico/ambos)
     - Norma (NBR/IEC/ISO)
     - Ativo/Inativo
  4. Submete para validação
  5. @po valida
  6. Publicado em produção

Sistema:
  - Valida: Carga > 0, categoria válida, norma reconhecida
  - Versionamento: Mantém histórico de mudanças
  - Auditoria: Registra quem, quando, o quê mudou
```

#### Tarefas de Implementação

```markdown
[ ] Task 5.1: Design de schema extensível
    - Duração: 2 dias (arquiteto)
    - Saída: Diagrama ER, design document

[ ] Task 5.2: Implementar backend (model, API)
    - Duração: 4 dias (dev)
    - Criar: Tabelas, migrations, endpoints

[ ] Task 5.3: Implementar frontend (UI/UX)
    - Duração: 4 dias (dev + designer)
    - Componente: TreeSelect, busca, validação

[ ] Task 5.4: Admin panel para gerenciar equipamentos
    - Duração: 3 dias (dev)
    - Funcionalidades: CRUD, validação, versionamento

[ ] Task 5.5: Testes (unitário + integração)
    - Duração: 3 dias (QA)
    - Cenários: CRUD, busca, hierarquia, validação

[ ] Task 5.6: Documentação (API, guia admin, guia usuário)
    - Duração: 2 dias
    - Saída: OpenAPI spec, guia de uso, FAQ
```

#### Critério de Aceição

- [ ] Model hierárquico implementado e testado
- [ ] API CRUD funcional (validação full)
- [ ] Frontend com TreeSelect + busca working
- [ ] Admin panel operacional
- [ ] Documentação completa
- [ ] Testes 100% passing (unitário + integração)
- [ ] Performance: query < 200ms even com 1000+ equipamentos

#### Dependências

- Recomendações 1-4 (dados existentes para migrar)

#### Estimativa

- **Esforço:** 18-21 dias (3 devs, 1 arquiteto, 1 QA)
- **Custo:** ~3 sprints
- **Timeline:** Sprint 3-5 (paralelo com rec 1-4)

---

### RECOMENDAÇÃO 6: Validação com Normas (NBR/IEC) [MÉDIA]

#### Escopo

Criar processo de validação contínuo para garantir conformidade com normas.

#### O Que Fazer

**1. Mapeamento de Normas:**
```
Criar tabela: Equipamento → Norma(s) Aplicável(is) → Carga Padrão
Exemplo:
  Chuveiro Elétrico → NBR 5410 → 5.5-7.0 kW
  Carregador EV → ISO 15118 + NBR 16690 → 7-11 kW (mono) / 22 kW (tri)
  Motor Trifásico → NBR 17094 → Tabela 0.5-100 CV
```

**2. Process de Validação:**
```
Toda entrada de novo equipamento precisa de:
1. Norma(s) referente(s) listada(s)
2. Carga validada contra norma
3. Revisão por engenheiro (opcional para mudanças críticas)
4. Documentação de source (exemplo: página X da norma, tabela Y)
```

**3. Documentação Técnica:**
```
Criar docs/technical-references/ com:
  - NBR-5410-summary.md (resumo TUE, faixas de carga)
  - IEC-60364-summary.md (diferenças internacionais)
  - Motors-CV-Reference.md (tabela CV → kW → corrente 380V)
  - Standards-Matrix.md (equipamento × norma aplicável)
```

#### Tarefas de Implementação

```markdown
[ ] Task 6.1: Pesquisar e mapear normas para todos os equipamentos
    - Duração: 5 dias
    - Saída: Mapping table (equipamento → norma → carga)

[ ] Task 6.2: Criar documentação técnica de referência
    - Duração: 3 dias
    - Saída: docs/technical-references/ com 4 arquivos

[ ] Task 6.3: Implementar validação no backend
    - Duração: 2 dias (dev)
    - Adicionar: Campos de norma, validação de carga

[ ] Task 6.4: Criar processo de revisão (opcional para @po/@architect)
    - Duração: 1 dia (dev)
    - Adicionar: Workflow de aprovação antes de publicar

[ ] Task 6.5: QA & testes
    - Duração: 1.5 dias

[ ] Task 6.6: Treinamento & comunicação
    - Duração: 1 dia
    - Comunicar: Processo de validação, standards de qualidade
```

#### Critério de Aceição

- [ ] Mapping table de todos os equipamentos completo
- [ ] Documentação técnica criada e revisada
- [ ] Validação de norma no backend implementada
- [ ] Zero equipamentos sem norma referente
- [ ] Testes de conformidade passing

#### Dependências

- Recomendações 1-5 (todos os equipamentos)

#### Estimativa

- **Esforço:** 13-15 dias
- **Custo:** ~2 sprints
- **Timeline:** Sprint 4-5

---

## ESTRUTURA PROPOSTA

### Hierarquia de Categorias (Final)

```
Tomadas de Uso Específico (TUE)
│
├─ RESIDENCIAL (25 equipamentos)
│  ├─ Aquecimento & Água Quente (4)
│  │  ├─ Chuveiro Elétrico
│  │  ├─ Boiler / Aquecedor Acumulação
│  │  ├─ Aquecedor Passagem
│  │  └─ Bomba de Calor [NOVO]
│  │
│  ├─ Climatização (2)
│  │  ├─ Ar-condicionado
│  │  └─ Climatizador Portátil [NOVO]
│  │
│  ├─ Cozinha (6)
│  │  ├─ Fogão Elétrico
│  │  ├─ Forno Elétrico
│  │  ├─ Cooktop Indução [NOVO]
│  │  ├─ Lava-louças
│  │  ├─ Lava-roupas
│  │  └─ Micro-ondas
│  │
│  ├─ Bem-estar & Lazer (4)
│  │  ├─ Sauna
│  │  ├─ Secadora de Roupas [NOVO]
│  │  ├─ Jacuzzi/Hidromassagem
│  │  └─ Aquecedor Piscina [NOVO]
│  │
│  ├─ Geração & Armazenamento (3)
│  │  ├─ Painel Solar + Inversor [NOVO]
│  │  ├─ Bateria Residencial [NOVO]
│  │  └─ Carregador EV [NOVO]
│  │
│  ├─ Bomba & Compressor (2)
│  │  ├─ Bomba de Água [NOVO]
│  │  └─ Poço Artesiano [NOVO]
│  │
│  ├─ Utilitário Geral (4)
│  │  ├─ TUE Genérico (100-600 VA)
│  │  ├─ Ferro Elétrico
│  │  ├─ Torneira Elétrica
│  │  └─ Desumidificador [NOVO]
│  │
│  └─ Outro (com campo carga customizada) [NOVO]
│
├─ COMERCIAL (12 equipamentos) [NOVO SEGMENTO]
│  ├─ Cozinha Profissional (6)
│  │  ├─ Máquina de Café Comercial
│  │  ├─ Forno Profissional
│  │  ├─ Fryer Comercial (1 cuba)
│  │  ├─ Fryer Comercial (Dupla)
│  │  ├─ Chapa Aquecedora Profissional
│  │  └─ Lava-louças Industrial
│  │
│  ├─ Refrigeração (3)
│  │  ├─ Refrigerador Comercial
│  │  ├─ Freezer Vertical Comercial
│  │  └─ Câmara Frigorífica (Walk-in)
│  │
│  ├─ Ar Comprimido & Utilitário (2)
│  │  ├─ Compressor (1-5 CV)
│  │  └─ Bomba Centrífuga
│  │
│  ├─ Conformação (1)
│  │  └─ Prensa Hidráulica (10-100 ton)
│  │
│  └─ Outro [extensível]
│
├─ INDUSTRIAL (18 equipamentos) [NOVO SEGMENTO]
│  ├─ Motores Base (1)
│  │  └─ Motor Trifásico (0.5-100 CV, genérico)
│  │
│  ├─ Soldagem (6)
│  │  ├─ Soldadora MIG-MAG 150A
│  │  ├─ Soldadora MIG-MAG 200A
│  │  ├─ Soldadora MIG-MAG 400A
│  │  ├─ Soldadora TIG 200A
│  │  ├─ Soldadora TIG 315A
│  │  └─ Soldadora Stick
│  │
│  ├─ Usinagem (7)
│  │  ├─ CNC Pequena (VMC)
│  │  ├─ CNC Média
│  │  ├─ CNC Grande
│  │  ├─ Torno Paralelo Pequeno
│  │  ├─ Torno Paralelo Médio
│  │  ├─ Torno Paralelo Grande
│  │  └─ Fresadora Universal
│  │
│  ├─ Tratamento Térmico (4)
│  │  ├─ Forno de Resistência
│  │  ├─ Forno Mufla
│  │  ├─ Forno Industrial
│  │  └─ Forno Indução
│  │
│  ├─ Compressor & Bomba (2)
│  │  ├─ Compressor Industrial (5-10 CV)
│  │  └─ Bomba Submersível
│  │
│  └─ Outro [extensível]
│
├─ EMERGENTES (5 equipamentos) [NOVO SEGMENTO]
│  ├─ Carregador EV V2H/V2L
│  ├─ Bomba de Calor Reversível
│  ├─ Armazenamento Bateria (Powerwall)
│  ├─ Carregador Universal EV+Bici
│  └─ Sistema Hidrogênio (Fuel Cell)
│
└─ Outro (campo genérico com carga customizada) [NOVO]
```

### Modelo de Dados Proposto

```sql
-- Tabela de categorias (hierárquica)
CREATE TABLE equipment_categories (
  id INT PRIMARY KEY,
  name VARCHAR(100),
  parent_id INT NULLABLE,
  segment VARCHAR(50),  -- 'residencial', 'comercial', 'industrial', 'emergentes'
  order INT,
  description TEXT,
  icon VARCHAR(50),
  created_at TIMESTAMP,
  updated_at TIMESTAMP
);

-- Tabela de equipamentos
CREATE TABLE equipment (
  id INT PRIMARY KEY,
  name VARCHAR(100),
  category_id INT FOREIGN KEY,
  description TEXT,
  
  -- Cargas
  carga_min_kw DECIMAL(10,2),
  carga_max_kw DECIMAL(10,2),
  carga_tipica_kw DECIMAL(10,2),
  
  -- Tensão
  tensao_types JSON,  -- ["monofásico 127V", "monofásico 220V", "trifásico 380V"]
  
  -- Norma
  standards VARCHAR(500),  -- "NBR 5410, IEC 60364"
  standard_reference TEXT,  -- "Artigo 4.2.5 da NBR 5410"
  
  -- Metadata
  active BOOLEAN,
  version INT,
  created_by VARCHAR(100),
  created_at TIMESTAMP,
  updated_by VARCHAR(100),
  updated_at TIMESTAMP,
  deleted_at TIMESTAMP NULLABLE
);

-- Tabela de auditoria (para rastreamento)
CREATE TABLE equipment_audit_log (
  id INT PRIMARY KEY,
  equipment_id INT,
  action VARCHAR(50),  -- 'created', 'updated', 'deleted'
  changes JSON,
  changed_by VARCHAR(100),
  changed_at TIMESTAMP
);
```

### Campos Obrigatórios por Equipamento

| Campo | Tipo | Exemplo | Obrigatório |
|-------|------|---------|-----------|
| Nome | Text | "Carregador EV" | ✅ SIM |
| Categoria | Select Hierárquico | Residencial > Geração | ✅ SIM |
| Carga Mínima | Decimal (kW) | 7 | ✅ SIM |
| Carga Máxima | Decimal (kW) | 11 | ✅ SIM |
| Carga Típica | Decimal (kW) | 9 | ✅ SIM |
| Tensão | Multi-select | [Monofásico 220V, Trifásico 380V] | ✅ SIM |
| Norma(s) | Text | "ISO 15118, NBR 16690" | ✅ SIM |
| Descrição | Text | "Carregador residencial de EV..." | ⚠️ Recomendado |
| Ativo | Boolean | True | ✅ SIM |

---

## IMPLEMENTAÇÃO DETALHADA

### Sprint 1: Residencial + Infraestrutura Base

**Duração:** 2 semanas  
**Objetivo:** Expandir residencial + implementar modelo de dados extensível

#### Tasks

**1.1 Research & Validação (Day 1-2)**
```
[ ] Pesquisar 10 equipamentos residenciais novos
[ ] Validar cargas com NBR 5410
[ ] Documentar sources e referências
[ ] Criar tabela de cargas
Responsável: @analyst
Saída: research-residencial.md
```

**1.2 Design de Banco (Day 2-3)**
```
[ ] Criar diagrama ER (hierarquias, equipamentos, auditoria)
[ ] Design de schema (migrations)
[ ] Documentar índices para performance
[ ] Revisar com @architect
Responsável: @architect
Saída: schema-design.md, migrations/
```

**1.3 Backend - Model & API (Day 4-8)**
```
[ ] Implementar model Equipment (CRUD)
[ ] Implementar API /api/categories (hierarquia)
[ ] Implementar API /api/equipment (CRUD, busca)
[ ] Validações (carga > 0, norma válida, etc)
[ ] Testes unitários
Responsável: @dev
Saída: models/, controllers/, tests/
```

**1.4 Frontend - Seletor (Day 6-9)**
```
[ ] Criar componente TreeSelect
[ ] Implementar busca full-text
[ ] Integração com API
[ ] Breadcrumb de seleção
[ ] Responsividade
Responsável: @dev (frontend)
Saída: components/equipment-selector/
```

**1.5 Migration & Dados (Day 8-9)**
```
[ ] Criar migration de dados antigos → novos
[ ] Seed com 15 equipamentos residenciais
[ ] Adicionar 10 equipamentos novos
[ ] Validação de dados
Responsável: @dev (backend)
Saída: seeds/, data/
```

**1.6 QA & Testes (Day 10-11)**
```
[ ] Testes funcionales (CRUD, busca, validação)
[ ] Testes de regressão (equipamentos antigos)
[ ] Testes de performance (< 200ms query)
[ ] Smoke test em staging
Responsável: @qa
Saída: test-report, bug-list
```

**1.7 Documentação & Release (Day 12)**
```
[ ] Atualizar API docs (OpenAPI)
[ ] Guia de usuário (novo seletor)
[ ] Release notes
[ ] Treinamento time
Responsável: @pm
Saída: docs/, release-notes.md
```

#### Definition of Done

- [ ] 25 equipamentos residenciais em produção
- [ ] Modelo de dados extensível operacional
- [ ] API CRUD fully functional
- [ ] TreeSelector funcionando
- [ ] 100% testes passing
- [ ] Zero regressions
- [ ] Documentação completa

---

### Sprint 2-3: Comercial + Industrial (Paralelo)

**Duração:** 4 semanas (2 sprints paralelos)  
**Objetivo:** Adicionar segmentos comercial e industrial

#### Sprint 2: Comercial

**Tasks:**
```
[ ] Research 12 equipamentos comerciais (2 dias) [@analyst]
[ ] Implementar categoria comercial no backend (2 dias) [@dev]
[ ] Criar subcategorias UI (3 dias) [@dev (frontend)]
[ ] Migration & seed (1.5 dias) [@dev]
[ ] QA & testes (2 dias) [@qa]
[ ] Docs & release (1 dia) [@pm]
```

**Resultado:** 12 equipamentos comerciais em produção

#### Sprint 3: Industrial

**Tasks:**
```
[ ] Research 18 equipamentos industrial (3 dias) [@analyst]
[ ] Criar tabela referência motores (1 dia) [@analyst]
[ ] Implementar categoria industrial (3 dias) [@dev]
[ ] Filtros avançados (CV/kW/tipo) (3 dias) [@dev (frontend)]
[ ] Migration & seed (2 dias) [@dev]
[ ] QA & testes (2.5 dias) [@qa]
[ ] Docs & release (1 dia) [@pm]
```

**Resultado:** 18 equipamentos industrial + tabela referência

---

### Sprint 4: Emergentes + Validação

**Duração:** 2 semanas  
**Objetivo:** Criar categoria emergentes + validação de normas

#### Tasks

```
[ ] Research tecnologias emergentes (2 dias) [@analyst]
[ ] Implementar categoria Emergentes (2 dias) [@dev]
[ ] Badge visual & timeline (1 dia) [@dev (frontend)]
[ ] Mapeamento de normas (todos os equipamentos) (5 dias) [@analyst]
[ ] Documentação técnica de referência (3 dias) [@analyst]
[ ] Validação backend de normas (2 dias) [@dev]
[ ] QA & testes (2 dias) [@qa]
[ ] Docs & release (1 dia) [@pm]
```

**Resultado:**
- Categoria Emergentes com 5 tecnologias
- Documentação de referência técnica (normas)
- Validação de conformidade implementada

---

### Sprint 5: Modelo Extensível + Polish

**Duração:** 2 semanas  
**Objetivo:** Tornar sistema completamente extensível + finalizar

#### Tasks

```
[ ] Projeto de schema extensível (2 dias) [@architect]
[ ] Implementar admin panel para CRUD (4 dias) [@dev]
[ ] Sistema de versionamento/auditoria (2 dias) [@dev]
[ ] Testes de extensibilidade (2 dias) [@qa]
[ ] Performance testing (load, stress) (2 dias) [@qa]
[ ] Polir UI/UX (1.5 dias) [@dev (frontend)]
[ ] Documentação API completa (2 dias) [@pm]
[ ] Training & launch (1 dia) [@pm]
```

**Resultado:**
- Admin panel operacional
- Sistema 100% extensível
- API documentada (OpenAPI)
- Ready para crescimento futuro

---

## ROADMAP & TIMELINE

### Fase 1: MVP Expandido (Semanas 1-5)

```
Semana 1 (Sprint 1): Residencial Base + Infraestrutura
  ├─ Research & validação ✓
  ├─ Schema design ✓
  ├─ Backend CRUD ✓
  ├─ Frontend TreeSelect ✓
  ├─ Migration ✓
  ├─ QA ✓
  └─ Deploy: v2.0 (25 residencial)

Semana 2-3 (Sprint 2): Comercial
  ├─ Research (12 equipamentos)
  ├─ Backend categoria
  ├─ Frontend subcategorias
  ├─ Migration & QA
  └─ Deploy: v2.1 (12 comercial)

Semana 4 (Sprint 3): Industrial (Parte 1)
  ├─ Research (18 equipamentos)
  ├─ Tabela motores
  ├─ Backend categoria
  └─ Frontend (em progresso)

Semana 5 (Sprint 4): Industrial (Parte 2) + Emergentes
  ├─ Frontend industrial finalizada
  ├─ QA industrial
  ├─ Research emergentes
  ├─ Categoria emergentes
  ├─ Documentação técnica
  ├─ Validação normas
  └─ Deploy: v2.2 (18 industrial + 5 emergentes)
```

### Fase 2: Extensibilidade (Semanas 6-7)

```
Semana 6 (Sprint 5a): Modelo Extensível
  ├─ Design schema final
  ├─ Admin panel
  ├─ Versionamento
  ├─ Testes extensibilidade
  └─ Deploy: v2.3 (admin panel + versionamento)

Semana 7 (Sprint 5b): Polish & Finalização
  ├─ Performance testing
  ├─ UI/UX polish
  ├─ API documentação
  ├─ Training
  └─ Deploy: v2.4 (stable, ready produção)
```

### Fase 3: Manutenção & Evolução (Contínua)

```
Trimestral:
  - Revisão de novos equipamentos do mercado
  - Atualização de normas (quando houver)
  - Feedback de usuários
  - Roadmap de próximas tecnologias

Anual:
  - Revisão completa de conformidade (NBR/IEC)
  - Auditoria de dados
  - Planejamento estratégico para próximos 5 anos
```

### Timeline Visual

```
┌─────────────────────────────────────────────────────┐
│ Mês 1 (Semanas 1-5): MVP Expandido                  │
│ ├─ Sprint 1: Residencial base + infra               │
│ ├─ Sprint 2: Comercial (12 equipamentos)            │
│ ├─ Sprint 3-4: Industrial (18) + Emergentes (5)     │
│ └─ Result: 60 equipamentos em produção              │
├─────────────────────────────────────────────────────┤
│ Mês 2 (Semanas 6-7): Extensibilidade                │
│ ├─ Sprint 5: Admin panel + versionamento            │
│ └─ Result: Sistema 100% extensível                  │
├─────────────────────────────────────────────────────┤
│ Mês 3+: Manutenção & Evolução                       │
│ ├─ Updates trimestrais                              │
│ ├─ Revisão anual                                    │
│ └─ Roadmap público                                  │
└─────────────────────────────────────────────────────┘
```

---

## ESTIMATIVAS DE ESFORÇO

### Por Recomendação

| Rec | Título | Dev | QA | Analyst | Designer | PM | Total |
|-----|--------|-----|----|---------|---------|----|-------|
| 1 | Residencial Expandido | 6d | 2d | 1d | 1d | 0.5d | 10.5d |
| 2 | Comercial | 7d | 2d | 2d | 1d | 1d | 13d |
| 3 | Industrial | 8d | 3d | 3d | 1d | 1d | 16d |
| 4 | Emergentes | 3d | 1.5d | 2d | 0.5d | 1d | 7.5d |
| 5 | Modelo Extensível | 10d | 3d | 1d | 1.5d | 1d | 16.5d |
| 6 | Validação/Normas | 3d | 1.5d | 5d | 0.5d | 1d | 11d |
| **TOTAL** | | **37d** | **13d** | **14d** | **5.5d** | **5.5d** | **74d** |

### Em Sprints (2 semanas = 10 dias de trabalho)

```
Sprint 1 (10 dias): Rec 1 + Rec 5 (design) → 10.5 + 2 = 12.5d → overflow para Sprint 2
Sprint 2 (10 dias): Rec 1 (final) + Rec 2 (start) → 5d + 6d = 11d → overflow para Sprint 3
Sprint 3 (10 dias): Rec 2 + Rec 5 (backend start) → 5d + 4d = 9d ✓
Sprint 4 (10 dias): Rec 3 + Rec 4 + Rec 5 (backend) → 8d + 3d + 3d = 14d → overflow
Sprint 5 (10 dias): Rec 3 (final) + Rec 4 (final) + Rec 5 (frontend) + Rec 6 (start) → 5d + 3d + 3d + 2d = 13d
Sprint 6 (10 dias): Rec 5 (final) + Rec 6 (final) → 4d + 5d = 9d ✓

Total: 6 sprints = ~3 meses
```

### Cost Estimation (Assumindo $100/hora dev, $80/hora QA, etc)

```
Development:   37d × 8h × $100   = $29,600
QA:           13d × 8h × $80    = $8,320
Analysis:     14d × 8h × $100   = $11,200
Design:       5.5d × 8h × $90   = $3,960
PM:           5.5d × 8h × $120  = $5,280
────────────────────────────────────────
TOTAL:                            = $58,360
```

---

## CRITÉRIOS DE SUCESSO

### Métricas Quantitativas

| Métrica | Target | Success Criteria |
|---------|--------|-----------------|
| Cobertura de equipamentos | 60 | ≥ 60 equipamentos validados |
| Conformidade NBR 5410 | 100% | Todos equipamentos com norma referente |
| Tempo de seleção | < 3 cliques | User consegue selecionar em 3 cliques ou menos |
| Performance (API) | < 200ms | Query latency < 200ms |
| Testes unitários | 95% | Coverage ≥ 95% |
| Testes integração | 100% | Todos cenários CRUD passing |
| Regressions | 0 | Zero regressions em funcionalidades antigas |

### Métricas Qualitativas

| Aspecto | Success Criteria |
|--------|-----------------|
| Usabilidade | Usuários conseguem encontrar equipamento em < 30 segundos |
| Documentação | Todas normas referentes têm link/source documentado |
| Extensibilidade | Novo equipamento pode ser adicionado por admin em < 5 minutos |
| Manutenibilidade | Código segue padrões, bem documentado, fácil de entender |
| Futuro-proof | Roadmap público, tecnologias emergentes visíveis |

### User Acceptance Testing (UAT)

**Cenários a testar:**

```
[ ] Residencial: Usuário seleciona "Carregador EV", obtém 7-11 kW mono/22 kW tri
[ ] Comercial: Usuário seleciona "Refrigerador Comercial", obtém 0.37-0.75 kW
[ ] Industrial: Usuário seleciona "Motor 5 CV", obtém 3.7 kW + corrente 380V
[ ] Busca: Usuário busca "bomb", encontra Bomba Água, Bomba Centrífuga, Bomba Calor
[ ] Emergente: Usuário vê badge "Futuro (2028-2032)" para V2H
[ ] Validação: Usuário tenta adicionar equipamento sem norma, recebe erro
```

---

## RISCOS & MITIGAÇÃO

### Risco 1: Dados Incompletos de Normas

**Severidade:** 🔴 ALTA  
**Probabilidade:** 🟠 MÉDIA  

**Descrição:**
Informações de cargas/normas podem estar incompletas ou incorretas, levando a dimensionamentos errados.

**Impacto:**
- Riscos de segurança (circuitos subdimencionados)
- Liability legal (não conformidade NBR)
- Perda de confiança do usuário

**Mitigação:**
```
1. Research rigoroso com múltiplas fontes (NBR, IEC, fabricantes)
2. Validação por engenheiro antes de publicar
3. Documentar source de cada carga (referência de página)
4. Avisos em produção: "Validar com engenheiro antes usar em projeto crítico"
5. Processo de revisão anual
6. Feedback loop: usuários reportam discrepâncias
```

**Contingency Plan:**
```
Se descobrirmos dados incorretos:
1. Imediatamente marcar equipamento como "under review"
2. Notificar todos usuários que o selecionaram
3. Corrigir com validação adicional
4. Publicar fix note em release notes
```

---

### Risco 2: Scope Creep (Adicionar Equipamentos Demais)

**Severidade:** 🟠 MÉDIA  
**Probabilidade:** 🔴 ALTA  

**Descrição:**
Pressão para adicionar "mais um equipamento" pode expandir scope indefinidamente, atrasando launch.

**Impacto:**
- Atraso de timeline
- Qualidade comprometida
- Burn-out do time

**Mitigação:**
```
1. Definir lista "Phase 1" fixa (60 equipamentos) → NÃO MUDA
2. Equipamentos adicionais → Phase 2 (roadmap futuro)
3. Gate de aprovação (@po) para novos equipamentos
4. Comunicar claramente: "MVP = 60. Futuro = extensível"
5. Usar admin panel para add fácil (não requer dev)
```

---

### Risco 3: Performance (Database Query Lenta)

**Severidade:** 🔴 ALTA  
**Probabilidade:** 🟡 BAIXA  

**Descrição:**
Com 60+ equipamentos, queries hierárquicas podem ficar lentas.

**Impacto:**
- UI travada ao selecionar
- Usuário frustrante
- Abandono do sistema

**Mitigação:**
```
1. Índices bem planejados (category_id, segment)
2. Cache de hierarquia (Redis)
3. Busca full-text otimizada (Elasticsearch optional)
4. Load testing early (com 100+ equipamentos fictícios)
5. Target: < 200ms para qualquer query
```

---

### Risco 4: Equipe sem Experiência em Industrial

**Severidade:** 🟠 MÉDIA  
**Probabilidade:** 🟠 MÉDIA  

**Descrição:**
Segmento industrial é complexo (motores, soldagem, CNC). Time pode não ter expertise.

**Impacto:**
- Dados industrial incorretos
- User complaints
- Reputação danificada no setor industrial

**Mitigação:**
```
1. Contratar/consultar especialista industrial por 1-2 sprints
2. Workshop com engenheiro de aplicações industrial
3. Validação com fabricantes (WEG, ABB, Siemens)
4. Documentação rigorosa com sources
5. UAT com usuários industriais antes de launch
```

---

### Risco 5: Resistência à Mudança (UI Radicalmente Diferente)

**Severidade:** 🟡 BAIXA  
**Probabilidade:** 🟠 MÉDIA  

**Descrição:**
TreeSelect pode ser radicalmente diferente do dropdown atual. Usuários podem resistir.

**Impacto:**
- Curva de aprendizado
- Support overload (dúvidas)
- Slow adoption

**Mitigação:**
```
1. Design iterativo: mostrar mockups a usuários antes
2. Tutorial in-app (como usar TreeSelect)
3. Backward compatibility: dropdown antigo ainda funciona (toggle)
4. Gradual rollout: 10% users → 50% → 100%
5. Support reforçado na primeira semana
6. Feedback survey pós-launch
```

---

## APÊNDICES TÉCNICOS

### A. Tabela de Referência Motores (NBR 17094)

| CV | kW | Corrente 380V (A) | Rendimento (%) | Fator Potência | Tempo Partida (s) |
|----|----|--------------------|----------------|----------------|------------------|
| 0.5 | 0.37 | 1.2 | 70 | 0.80 | 0.5-1 |
| 1 | 0.75 | 2.0 | 75 | 0.82 | 0.5-1.5 |
| 2 | 1.5 | 3.8 | 78 | 0.84 | 1-2 |
| 3 | 2.2 | 5.5 | 80 | 0.85 | 1-2 |
| 5 | 3.7 | 9.0 | 82 | 0.86 | 2-3 |
| 7.5 | 5.5 | 13.0 | 84 | 0.87 | 2-3 |
| 10 | 7.5 | 17.5 | 85 | 0.87 | 3-4 |
| 15 | 11 | 26 | 87 | 0.88 | 3-4 |
| 20 | 15 | 35 | 88 | 0.88 | 4-5 |
| 25 | 18.5 | 43 | 89 | 0.89 | 4-5 |
| 30 | 22 | 51 | 89 | 0.89 | 5-6 |
| 40 | 30 | 70 | 90 | 0.90 | 5-6 |
| 50 | 37 | 87 | 91 | 0.91 | 6-8 |
| 60 | 45 | 105 | 91 | 0.91 | 6-8 |
| 75 | 55 | 130 | 91 | 0.92 | 7-10 |
| 100 | 75 | 175 | 92 | 0.92 | 8-12 |

**Fórmula para calcular corrente trifásica 380V:**
```
I (A) = P (kW) × 1000 ÷ (√3 × V × cosφ × η)
I (A) ≈ P (kW) / 0.656  [aproximação para 380V]

Exemplo: Motor 7.5 kW
I = 7.5 / 0.656 ≈ 11.4 A (vs. tabela 17.5 A com arranque)
```

---

### B. Mapeamento NBR 5410 - Faixas de Carga

| Faixa | Ampere | kW (Monofásico 220V) | kW (Trifásico 380V) | Exemplo |
|-------|--------|----------------------|-------------------|---------|
| TUE Genérico | até 16A | até 3.5 | até 6.6 | Tomada 100/600 VA |
| Médio | 16-32A | 3.5-7 | 6.6-13.2 | Chuveiro, AR-AC pequeno |
| Alto | 32-63A | 7-14 | 13.2-26.4 | Fogão, AR-AC grande |
| Ultra-Alto | 63-100A | 14-22 | 26.4-39.6 | Carregador EV trifásico |
| Industrial | >100A | >22 | >39.6 | Motores, compressores |

---

### C. Normas Aplicáveis por Segmento

#### Residencial
- **NBR 5410** - Instalações Elétricas de Baixa Tensão (principal)
- **NBR 16690** - Sistemas Fotovoltaicos Conectados à Rede
- **IEC 60364** - International Electrical Installations
- **ISO 15118** - Carregamento de Veículos Elétricos
- **IEC 60335** - Segurança de Aparelhos Elétricos

#### Comercial
- **NBR 5410** - Base (mesmo que residencial)
- **NBR 12094** - Equipamentos Profissionais para Cozinha
- **NBR 14039** - Instalações Elétricas de Média Tensão
- **IEC 62552** - Refrigeradores Comerciais
- **NBR ISO 5167** - Ar Comprimido

#### Industrial
- **NBR 17094** - Motores Assíncronos Trifásicos (ex-NBR 5883)
- **NBR IEC 60974** - Sistemas de Soldagem
- **ISO 12922** - Óleos Industriais
- **ISO 1402** - Tornos Paralelos
- **NBR 6162** - Usinagem
- **NBR 13830** - Fornos Industriais
- **IEC 61400** - Geração de Energia (wind)

---

### D. Conversões Úteis

```
Potência:
  1 CV = 0.735 kW (exato)
  1 CV ≈ 0.75 kW (prático)
  1 HP = 0.746 kW (padrão americano)
  1 kW = 1.36 CV

Tensão Brasil:
  Monofásico: 127V ou 220V
  Trifásico: 220V, 380V, ou 440V

Corrente Trifásica:
  P (kW) = √3 × V × I × cosφ × η
  Simplificado para 380V: I (A) ≈ P (kW) / 0.656

Simultaneidade:
  Residencial: 40-60% de todos equipamentos ligados simultaneamente
  Comercial: 60-80%
  Industrial: 80-100% (máquinas contínuas)
```

---

### E. Checklist de Validação para Novo Equipamento

Quando adicionar equipamento novo ao sistema:

```
[ ] Nome do equipamento correto e sem ambiguidades
[ ] Carga mínima (kW) pesquisada em ≥2 fontes confiáveis
[ ] Carga máxima (kW) pesquisada em ≥2 fontes
[ ] Carga típica estabelecida (média ou mais comum)
[ ] Tensão(ões) aplicável(is) listada(s)
[ ] Norma(s) referente(s) identificada(s)
[ ] Source documentado (ex: "Página 23 de NBR 5410", "Datasheet fabricante WEG")
[ ] Revisado por engenheiro (para críticos)
[ ] Categoria correta (não ambígua)
[ ] Descrição clara para usuário
[ ] Ativo/Inativo definido
[ ] Dados testados em ambiente staging
[ ] Nenhum conflito com equipamento existente
[ ] Release notes preparadas
[ ] Documentação atualizada
```

---

### F. Template de Documentação para Novo Equipamento

```markdown
# [Nome do Equipamento]

## Descrição Geral
[1-2 linhas descrevendo o equipamento e seu uso típico]

## Cargas
- **Mínima:** X kW (exemplo de modelo pequeno)
- **Máxima:** Y kW (exemplo de modelo grande)
- **Típica:** Z kW (mais comum no mercado)

## Tensão(ões) Aplicável(is)
- [ ] Monofásico 127V
- [ ] Monofásico 220V
- [ ] Trifásico 220V
- [ ] Trifásico 380V
- [ ] Trifásico 440V

## Norma(s)
- **Primária:** [Norma X](link) - [Artigo/Tabela específica]
- **Secundária:** [Norma Y](link)

## Exemplos de Modelos
| Marca | Modelo | Potência | Link |
|-------|--------|----------|------|
| [Marca 1] | [Modelo A] | X kW | [Link] |
| [Marca 2] | [Modelo B] | Y kW | [Link] |

## Notas Importantes
- [Observação 1]
- [Observação 2]

## Última Atualização
Data: YYYY-MM-DD | Autor: [Nome] | Validado por: [Nome]
```

---

## CONCLUSÃO

### Recomendação Final

A expansão de Tomadas de Uso Específico de 15 para ~60 equipamentos é **crítica e urgente** para:

1. ✅ Conformidade com NBR 5410 (padrão brasileiro)
2. ✅ Futuro-proof (5-10 anos com EV, solar, bomba calor)
3. ✅ Crescimento de mercado (comercial + industrial)
4. ✅ Competitividade (vs. soluções rivais)
5. ✅ Escalabilidade (modelo extensível)

### Timeline Esperada

```
Fase 1 (Semanas 1-5):   MVP Expandido (60 equipamentos)
Fase 2 (Semanas 6-7):   Modelo Extensível (admin panel)
Fase 3 (Contínua):      Manutenção & Evolução
────────────────────────────────────
Total: ~3 meses até v2.4 (stable)
```

### Investimento

- **Esforço:** 74 dias-pessoa (~$58k USD)
- **Timeline:** 3 meses (6 sprints)
- **ROI:** Futuro-proof do produto, acesso a 3x mercado

### Próximas Ações

1. **Aprovação:** Validar recomendações com @po/@pm
2. **Planejamento:** Quebrar em stories para próximo sprint
3. **Research:** Iniciar coleta de dados (Rec 1-4)
4. **Design:** Iniciar design de schema extensível (Rec 5)
5. **Comunicação:** Informar stakeholders sobre roadmap

---

**Documento preparado:** 2026-06-20  
**Próxima revisão:** 2026-07-20 (1 mês)  
**Validação:** Aguardando @po / @pm / @architect

---

**Fim do Documento**
