# 📚 Índice de Documentação — Conformidade NBR 5410

## 📄 Arquivos de Help Disponíveis

| Arquivo | Tipo | Uso | Descrição |
|---------|------|-----|-----------|
| **NBR5410-Conformidade-Guia-Completo.md** | Markdown | Referência Técnica Completa | 🔬 **Guia definitivo** — Explicações detalhadas de cada campo, exemplos práticos, FAQ técnicas, tabelas de referência. ~5.000 palavras. **Use quando:** Você precisa entender profundamente qualquer aspecto da conformidade. |
| **NBR5410-Help-Rapido.md** | Markdown | Cheat Sheet / Rápida | 🚀 **Resumo executivo** — Versão condensada de 1-2 páginas com o essencial. Tabelas rápidas, regras de ouro. **Use quando:** Você conhece a norma e precisa de referência rápida. |
| **NBR5410-Help-Modal.html** | HTML/CSS | Modal/Caixa de Ajuda | 💻 **Interface Web interativa** — Totalmente estilizado, responsivo, com FAQ clicável. **Use quando:** Integrar help diretamente no formulário ou sistema web. |
| **NBR5410-Help-Schema.json** | JSON | API / Sistema | ⚙️ **Estrutura de dados** — Schema JSON estruturado para cada campo. Ideal para APIs, sistemas backend, ou geração dinâmica de help. |
| **NBR5410-HELP-INDEX.md** | Markdown | Este Arquivo | 📍 **Índice e orientação** — Mapa de como usar todos os arquivos. |

---

## 🎯 Como Usar Cada Arquivo

### 1️⃣ **Guia Completo** → `NBR5410-Conformidade-Guia-Completo.md`

**Quando usar:**
- Primeira vez aprendendo sobre conformidade NBR 5410
- Precisando de explicação profunda de qualquer campo
- Preparando material de treinamento
- Auditoria técnica completa

**Conteúdo:**
- Visão geral da NBR 5410
- 6 campos descritos em detalhe (2-3 páginas cada)
- Tabelas de referência rápida
- Fluxo de preenchimento passo-a-passo
- 4 exemplos práticos detalhados (um completo, um crítico)
- Checklist técnica
- FAQ com 5 perguntas principais

**Exemplo de uso:**
```
Usuário: "Qual é a diferença entre Zona 1 e Zona 2?"
Sistema: Abrir "NBR5410-Conformidade-Guia-Completo.md" → seção "Zona do Banheiro"
```

---

### 2️⃣ **Help Rápido** → `NBR5410-Help-Rapido.md`

**Quando usar:**
- Você já conhece a norma, só precisa refrescar
- Preencher formulário rapidamente
- Material de referência impressa/física
- Consulta durante inspeção de campo

**Conteúdo:**
- O que é o formulário (1 parágrafo)
- 6 campos resumidos em uma tabela (função + opções)
- 3 regras de ouro
- Checklist rápida (5 itens)
- Link para documentação completa

**Exemplo de uso:**
```
Usuário: "Preciso de uma referência rápida dos valores IP por zona"
Sistema: Abrir "NBR5410-Help-Rapido.md" → tabela de 4 linhas com zonas e IPs
```

---

### 3️⃣ **Modal Web (Interativo)** → `NBR5410-Help-Modal.html`

**Quando usar:**
- Integrar help dentro do formulário online
- Abrir em popup/modal ao clicar "?"
- Exibir ao lado do formulário (sidebar)
- Compartilhar link HTML para consulta rápida no navegador

**Conteúdo:**
- Design responsivo (funciona em celular/tablet)
- Todos os 6 campos descritos com visuais
- Tabelas formatadas bonitas
- FAQ com abas clicáveis
- Cores e ícones visuais
- CSS estilos profissionais

**Como integrar:**
```html
<!-- Dentro do seu formulário HTML -->
<button onclick="window.open('docs/NBR5410-Help-Modal.html', 'help', 'width=1000,height=800')">
  ❓ Ajuda
</button>
```

**Exemplo de uso:**
```
Usuário: Clica no botão "?" próximo a um campo
Sistema: Abre modal HTML com explicação visual daquele campo
```

---

### 4️⃣ **Schema JSON (Para Sistemas)** → `NBR5410-Help-Schema.json`

**Quando usar:**
- API backend precisa servir descrições de campos
- Sistema de geração dinâmica de formulários
- Integração com CMS ou ferramentas de automação
- Sincronização de documentação com interface

**Conteúdo:**
- Estrutura JSON completa de todos os campos
- Opções com valores e rótulos
- Tabelas estruturadas em arrays
- Regras, bloqueadores, FAQ em formato estruturado
- Pronto para consumir em linguagens de programação

**Exemplo de uso (Node.js):**
```javascript
const help = require('./docs/NBR5410-Help-Schema.json');

// Obter descrição de um campo
console.log(help.conformidade_nbr5410.campos.zona_do_banheiro.descricao_longa);

// Obter opções de um dropdown
const opcoes = help.conformidade_nbr5410.campos.db_informado.opcoes;
```

**Exemplo de uso (Python):**
```python
import json

with open('docs/NBR5410-Help-Schema.json', 'r', encoding='utf-8') as f:
    help_data = json.load(f)

# Obter regras de ouro
regras = help_data['conformidade_nbr5410']['regras_ouro']
for regra in regras:
    print(regra)
```

---

## 📱 Estratégia de Integração no Formulário

### Cenário 1: Formulário Web Simples
```
┌─────────────────────────────────┐
│  Zona do Banheiro    [?] Ajuda  │  ← Clique em [?] abre Modal HTML
│  [ ] Zona 0                      │
│  [ ] Zona 1                      │
│  [ ] Zona 2                      │
│  [ ] Zona 3                      │
└─────────────────────────────────┘

Ação: onclick → window.open('NBR5410-Help-Modal.html#zona-do-banheiro')
```

### Cenário 2: Sistema com Sidebar de Ajuda
```
┌──────────────────┬────────────────────────┐
│  Campo 1: Zona   │  📖 Help Rápido        │
│  Dropdown        │                        │
│  [Zona 1] ▼      │  **Zona do Banheiro**  │
│                  │  Define a localização  │
│                  │  do equipamento...     │
│                  │  [Ler Guia Completo]   │
└──────────────────┴────────────────────────┘

Ação: Carregar conteúdo dinamicamente de .JSON
```

### Cenário 3: Sistema com Tooltips
```
Zona do Banheiro [?]
    ↓ (ao passar mouse)
┌─────────────────────────────────────┐
│ Localização do equipamento em      │
│ relação à banheira. (Zona 0-3)     │
│ [Mais informações] → Modal         │
└─────────────────────────────────────┘

Ação: Usar campo 'descricao_curta' do JSON
```

---

## 🔍 Árvore de Busca no Índice

Se o usuário procura por **X**, use o **Y**:

| Usuário Procura Por | Arquivo Recomendado | Seção |
|-------------------|---------------------|--------|
| IP44 vs IPX4 | Guia Completo | FAQ #1 |
| Qual IP usar em Zona 1? | Help Rápido | Tabela Rápida |
| Exemplos práticos | Guia Completo | Exemplos Práticos |
| Classe AD2 significa o quê? | Guia Completo | Campo "Classe" |
| Preciso preencher rápido | Help Rápido | Toda a documentação |
| Integrar no meu sistema | Schema JSON | Todo o arquivo |
| Mostrar no navegador | Modal HTML | Todo o arquivo |
| Entender tudo | Guia Completo | Todo o arquivo |

---

## 📊 Comparação de Arquivos

| Aspecto | Guia Completo | Help Rápido | Modal HTML | Schema JSON |
|---------|---------------|------------|-----------|-----------|
| Tamanho | 📄📄📄 Grande | 📄 Pequeno | 🌐 Médio | ⚙️ Médio |
| Profundidade | 🔬 Muito Profundo | ⚡ Superficial | 🎯 Balanceado | 💻 Estruturado |
| Forma | 📝 Texto/Markdown | 📋 Resumo | 🖥️ Interativo | 🔗 Dados |
| Uso Offline | ✅ Sim | ✅ Sim | ✅ Sim | ✅ Sim |
| Integração API | ❌ Não | ❌ Não | ⚠️ Difícil | ✅ Fácil |
| Melhor Para | 👨‍🏫 Treinamento | 🚀 Campo | 💼 Sistema | 🤖 Backend |

---

## 🛠️ Instruções de Uso por Contexto

### Contexto 1: Primeiro Uso (Aprendizado)
1. **Leia:** `NBR5410-Help-Rapido.md` (5 minutos)
2. **Depois estude:** `NBR5410-Conformidade-Guia-Completo.md` (30 minutos)
3. **Pronto para preencher:** Use a checklist rápida

### Contexto 2: Usando o Formulário (Preenchimento)
1. **Para cada campo:**
   - Leia resumo em `Help Rápido` (30 segundos)
   - Se dúvida → Abra `Modal HTML` ou `Guia Completo` (2-5 minutos)
2. **Após preencher:** Valide com checklist

### Contexto 3: Desenvolvedor (Integração)
1. **Estrutura de dados:** `Schema JSON` (referência para API)
2. **Frontend:** `Modal HTML` (copie e ajuste para seu design)
3. **Documentação:** Links internos para `Guia Completo`

### Contexto 4: Auditoria/Inspeção
1. **Material de campo:** Imprima `Help Rápido.md`
2. **Referência técnica:** Leve `Guia Completo.md` em PDF
3. **Validação:** Use checklist técnica do Guia

---

## 🔗 Links Internos de Navegação

### Do Help Rápido
```markdown
Para detalhes completos, consulte:
→ docs/NBR5410-Conformidade-Guia-Completo.md
```

### Do Modal HTML
```html
<p>Para documentação completa: <a href="docs/NBR5410-Conformidade-Guia-Completo.md">Guia Completo</a></p>
```

### Do Guia Completo
```markdown
Resumo rápido: Veja docs/NBR5410-Help-Rapido.md
Visualizar interativo: Abra docs/NBR5410-Help-Modal.html no navegador
Para integração em API: Consulte docs/NBR5410-Help-Schema.json
```

---

## 📞 Suporte e Atualizações

| Arquivo | Quando Atualizar | Como | Responsável |
|---------|------------------|------|------------|
| Guia Completo | Mudança na NBR 5410 | Edit .md | Analyst/Architect |
| Help Rápido | Mudança na Guia | Sincronizar resumo | Analyst |
| Modal HTML | Ajustes visuais | Edit HTML/CSS | UX/Designer |
| Schema JSON | Mudança de estrutura | Edit JSON | Developer |

---

## ✅ Checklist de Implementação

Se você vai integrar esses arquivos em um sistema:

- [ ] **Guia Completo:** Disponível para download/consulta
- [ ] **Help Rápido:** Impresso ou em PDF
- [ ] **Modal HTML:** Integrado ao formulário (botão "?" ou help sidebar)
- [ ] **Schema JSON:** Consumido pela API/backend
- [ ] **Links cruzados:** Todos os arquivos apontam uns para os outros
- [ ] **Versionamento:** Todos têm data de última atualização
- [ ] **Testes:** Usuários conseguem encontrar informação em < 2 minutos
- [ ] **Feedback:** Sistema coleta quais seções foram mais acessadas

---

## 🎓 Educação e Treinamento

### Para Novos Usuários
**Cronograma recomendado:**
1. **Dia 1:** Ler Help Rápido (5 min) + Visão Geral do Guia Completo (15 min)
2. **Dia 2:** Estudar 2 campos em profundidade do Guia (30 min)
3. **Dia 3:** Estudar 2 campos restantes (30 min)
4. **Dia 4:** Simular preenchimento do formulário (30 min)
5. **Dia 5:** Preencher caso real com supervisão (1 hora)

### Para Treinadores
- **Material:**  Use Guia Completo + Modal HTML em apresentação
- **Exercícios:** Exemplos práticos do Guia Completo
- **Avaliação:** Usar checklist técnica
- **Referência:** Entregar Help Rápido em PDF

---

## 📋 Versão e Metadados

| Metadado | Valor |
|----------|-------|
| **Versão** | 1.0 |
| **Data de Criação** | 2026-06-21 |
| **Última Atualização** | 2026-06-21 |
| **Criado Por** | Atlas (AIOX Analyst) |
| **Framework** | Synkra AIOX |
| **Norma Referenciada** | NBR 5410:2004 |
| **Idioma** | Português Brasileiro |
| **Licença** | Projeto Interno (Synkra) |

---

## 🚀 Próximos Passos

1. **Revisar:** Leia todos os 4 arquivos (30 minutos)
2. **Integrar:** Escolha qual/quais integrar ao seu sistema
3. **Testar:** Validar com usuários reais
4. **Coletar feedback:** Melhorar com base em uso real
5. **Manter:** Atualizações conforme a norma evolui

---

**Documento gerado por:** Atlas (AIOX Analyst)  
**Data:** 2026-06-21  
**Framework:** Synkra AIOX System  
**Status:** ✅ Completo e pronto para uso

