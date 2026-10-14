# Persona-Weight Methodology

## Conceito

Cada persona (academic researcher, founder, agency operator, enterprise CI analyst) tem **peso de dimensão diferente**. Um academic não liga pra Distribuição mas vive de Citações. Um founder vive de Planejamento+Saída. Por isso o scorecard suporta **weights_override** por scenario (ver `scenario-scorecards.json`).

## 4 Personas Canônicas (AIOX market panel)

### 1. Academic Researcher (Sackett/Creswell)
- Citações: 30%
- Sandbox: 15% (run experiments)
- Saída: 15% (paper-grade)
- Modelo: 12%
- Multi-Agente: 10%
- Outros: 18%

### 2. Founder/PM (Cagan/Perri lineage)
- Planejamento: 25% (product discovery)
- Saída: 18% (BMC/PRD/Lean Canvas)
- Governance: 12%
- Citações: 12%
- Outros: 33%

### 3. Agency Operator (PT-BR vertical)
- Saída: 22% (battle cards, decks)
- Distribuição: 18% (white-label)
- Multi-Agente: 12%
- Planejamento: 12%
- Outros: 36%

### 4. Enterprise CI Analyst (Gilad lineage)
- Citações: 22%
- Memória: 18% (cross-quarter intel)
- Sandbox: 12%
- Multi-Agente: 12%
- Outros: 36%

## Como aplicar

Use `scenario-scorecards.json#weights_override` para cada scenario testado. Esse arquivo lista os pesos ajustados e ranking dos 10 players naquela perspectiva.

## Anti-pattern

**NUNCA inflar AIOX scores ajustando pesos.** Pesos devem refletir a persona real, não preferência interna.
