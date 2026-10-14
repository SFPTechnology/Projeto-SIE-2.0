# 🚀 Help Rápido — Conformidade NBR 5410

## O que é este formulário?
Validação de **segurança elétrica em banheiros** conforme norma NBR 5410 (Instalações Elétricas de Baixa Tensão).

---

## 6 Campos — Preencha nesta ordem:

### 1️⃣ **Zona do Banheiro**
Onde está o equipamento em relação à banheira?
- **Zona 0:** Dentro da banheira (raro)
- **Zona 1:** Até 0,6m de distância horizontal
- **Zona 2:** 0,6m a 1,2m de distância
- **Zona 3:** Longe da banheira (fora do banheiro)

**💡 Dica:** Meça a distância em linha reta da banheira ao equipamento.

---

### 2️⃣ **DB Informado** (Disjuntor Residual)
Há proteção contra choque elétrico?
- **Sim** ✅ → Circuito tem DR (seguro)
- **Não** ❌ → Circuito sem proteção (PERIGOSO)

**⚠️ CRÍTICO:** Zona 1-2 SEM DB = **NÃO CONFORME**

---

### 3️⃣ **Grau de Proteção IP**
Proteção do equipamento contra água/umidade.

| Zona | IP Mínimo |
|------|-----------|
| Zona 0 | IPX7 ou IPX8 |
| Zona 1 | **IPX4** ← mais comum |
| Zona 2 | **IPX4** ← mais comum |
| Zona 3 | IPX1 |

**Exemplos:** `IP44`, `IP54`, `IP65`, `IPX7`

**📌 Nota:** Procure na placa do equipamento o código IP (ex: "IP44").

---

### 4️⃣ **Influência Externa**
Há fatores ambientais especiais?
- **Obrigatório:** Temperatura extrema, sauna, umidade muito alta
- **Opcional:** Banheiro comum (padrão)
- **Não aplicável:** Circuitos em áreas secas

---

### 5️⃣ **Classe**
Tipo/padrão do equipamento.

| Equipamento | Classe |
|-------------|--------|
| Tomada em banheiro | **AD2** ← mais comum |
| Iluminação em banheiro | **AL2** |
| Ventilador/Exaustor | **MD1** |
| Proteção máxima | **AD4** |

---

### 6️⃣ **Observações**
Escreva uma breve justificativa técnica.

**Exemplo:**
```
"Tomada classe AD2, IP44, protegida por DR 30mA, 
Zona 2, conforme NBR 5410"
```

---

## ⚠️ 3 Regras de Ouro

1. **Zona 1-2 SEMPRE precisa de DB** (disjuntor residual)
2. **Zona 1-2 SEMPRE precisa de IP mínimo 4** (jatos de água)
3. **Documente tudo nas Observações** (futura auditoria)

---

## ✅ Checklist Rápida

- [ ] Zona selecionada (0-3)?
- [ ] IP adequado para zona? (veja tabela acima)
- [ ] DB informado para Zona 1-2?
- [ ] Classe selecionada?
- [ ] Observações preenchidas?

---

## 🔗 Documentação Completa
Para detalhes técnicos, consulte:  
**`docs/NBR5410-Conformidade-Guia-Completo.md`**

---

**Última atualização: 2026-06-21**

