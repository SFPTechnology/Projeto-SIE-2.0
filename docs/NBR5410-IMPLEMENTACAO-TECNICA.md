# 🔧 Guia de Implementação Técnica — Help System Completo

## 📋 Índice
1. [Quick Start (5 minutos)](#quick-start)
2. [Implementação por Framework](#implementação-por-framework)
3. [Padrões de Integração](#padrões-de-integração)
4. [Checklist de Implementação](#checklist-de-implementação)
5. [Troubleshooting](#troubleshooting)

---

## ⚡ Quick Start (5 minutos)

### Passo 1: Copiar Arquivos
```bash
# Copie estes 5 arquivos para seu projeto
docs/
├── NBR5410-Help-Hub.html
├── NBR5410-Help-Modal.html
├── NBR5410-Help-Rapido.md
├── NBR5410-Conformidade-Guia-Completo.md
├── NBR5410-Help-Schema.json
└── NBR5410-HELP-INDEX.md
```

### Passo 2: Adicionar Botão de Ajuda (HTML Simples)
```html
<!-- Seu formulário existente -->
<form id="conformidade-form">
  <div class="form-group">
    <label for="zona_banheiro">
      Zona do Banheiro
      <button type="button" onclick="abrirAjuda()">❓</button>
    </label>
    <select id="zona_banheiro" name="zona">
      <option>Zona 0</option>
      <option>Zona 1</option>
      <option>Zona 2</option>
      <option>Zona 3</option>
    </select>
  </div>

  <!-- Mais campos... -->
</form>

<script>
function abrirAjuda() {
  window.open('docs/NBR5410-Help-Modal.html', 'help',
              'width=1000,height=800,scrollbars=yes');
}
</script>
```

### Passo 3: Pronto!
Abra seu formulário e clique em ❓ para ver o help modal.

---

## 🛠️ Implementação por Framework

### React.js

#### 1. Instalar e Importar
```jsx
// src/components/ConformidadeForm.jsx
import { useState } from 'react';
import helpSchema from '../docs/NBR5410-Help-Schema.json';

export default function ConformidadeForm() {
  const [showHelp, setShowHelp] = useState(false);
  const [helpContent, setHelpContent] = useState(null);

  const handleHelpClick = (fieldName) => {
    const campo = helpSchema.conformidade_nbr5410.campos[fieldName];
    setHelpContent(campo);
    setShowHelp(true);
  };

  return (
    <div>
      {/* Formulário */}
      <form>
        <div className="form-group">
          <label>
            Zona do Banheiro
            <button 
              type="button" 
              onClick={() => handleHelpClick('zona_do_banheiro')}
            >
              ❓
            </button>
          </label>
          <select name="zona_banheiro">
            <option>Zona 0</option>
            <option>Zona 1</option>
            <option>Zona 2</option>
            <option>Zona 3</option>
          </select>
        </div>
      </form>

      {/* Help Modal */}
      {showHelp && (
        <div className="modal">
          <div className="modal-content">
            <button onClick={() => setShowHelp(false)}>✕</button>
            <h2>{helpContent?.label}</h2>
            <p>{helpContent?.descricao_longa}</p>
            <h3>Opções:</h3>
            <ul>
              {helpContent?.opcoes?.map(opt => (
                <li key={opt.valor}>
                  <strong>{opt.label}</strong>: {opt.descricao}
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
```

#### 2. CSS para Modal
```css
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  padding: 30px;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
}

.modal-content button {
  position: absolute;
  top: 10px;
  right: 10px;
  border: none;
  background: transparent;
  font-size: 24px;
  cursor: pointer;
}
```

---

### Vue.js

```vue
<!-- ConformidadeForm.vue -->
<template>
  <form>
    <div class="form-group">
      <label>
        Zona do Banheiro
        <button type="button" @click="abrirAjuda('zona_do_banheiro')">
          ❓
        </button>
      </label>
      <select v-model="formData.zona_banheiro">
        <option>Zona 0</option>
        <option>Zona 1</option>
        <option>Zona 2</option>
        <option>Zona 3</option>
      </select>
    </div>
  </form>

  <!-- Help Modal -->
  <div v-if="showHelp" class="modal">
    <div class="modal-content">
      <button @click="showHelp = false">✕</button>
      <h2>{{ helpContent?.label }}</h2>
      <p>{{ helpContent?.descricao_longa }}</p>
      <h3>Opções:</h3>
      <ul>
        <li v-for="opt in helpContent?.opcoes" :key="opt.valor">
          <strong>{{ opt.label }}</strong>: {{ opt.descricao }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import helpSchema from '@/docs/NBR5410-Help-Schema.json';

export default {
  name: 'ConformidadeForm',
  data() {
    return {
      formData: {},
      showHelp: false,
      helpContent: null,
      helpSchema
    };
  },
  methods: {
    abrirAjuda(fieldName) {
      this.helpContent = this.helpSchema.conformidade_nbr5410.campos[fieldName];
      this.showHelp = true;
    }
  }
};
</script>

<style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 8px;
  padding: 30px;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
}

.modal-content button {
  position: absolute;
  top: 10px;
  right: 10px;
  border: none;
  background: transparent;
  font-size: 24px;
  cursor: pointer;
}
</style>
```

---

### Next.js / TypeScript

```typescript
// pages/api/help/[campo].ts
import type { NextApiRequest, NextApiResponse } from 'next';
import helpSchema from '@/docs/NBR5410-Help-Schema.json';

type ResponseData = {
  label?: string;
  descricao_longa?: string;
  opcoes?: any[];
  error?: string;
};

export default function handler(
  req: NextApiRequest,
  res: NextApiResponse<ResponseData>
) {
  const { campo } = req.query;

  if (!campo || typeof campo !== 'string') {
    res.status(400).json({ error: 'Campo não especificado' });
    return;
  }

  const campoData = (helpSchema as any).conformidade_nbr5410.campos[campo];

  if (!campoData) {
    res.status(404).json({ error: 'Campo não encontrado' });
    return;
  }

  res.status(200).json({
    label: campoData.label,
    descricao_longa: campoData.descricao_longa,
    opcoes: campoData.opcoes
  });
}
```

```jsx
// components/HelpButton.jsx
'use client';

import { useState } from 'react';

export default function HelpButton({ fieldName }) {
  const [help, setHelp] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleClick = async () => {
    setLoading(true);
    const res = await fetch(`/api/help/${fieldName}`);
    const data = await res.json();
    setHelp(data);
    setLoading(false);
  };

  return (
    <>
      <button onClick={handleClick} type="button">❓</button>
      {help && (
        <div className="help-popup">
          <h3>{help.label}</h3>
          <p>{help.descricao_longa}</p>
        </div>
      )}
    </>
  );
}
```

---

### Angular

```typescript
// src/app/services/help.service.ts
import { Injectable } from '@angular/core';
import helpSchema from '../../docs/NBR5410-Help-Schema.json';

@Injectable({
  providedIn: 'root'
})
export class HelpService {
  getCampoHelp(fieldName: string) {
    return (helpSchema as any).conformidade_nbr5410.campos[fieldName];
  }

  getRegrasOuro() {
    return (helpSchema as any).conformidade_nbr5410.regras_ouro;
  }

  getChecklist() {
    return (helpSchema as any).conformidade_nbr5410.checklist;
  }
}
```

```typescript
// src/app/components/help-modal/help-modal.component.ts
import { Component, Input, Output, EventEmitter } from '@angular/core';

@Component({
  selector: 'app-help-modal',
  template: `
    <div class="modal" *ngIf="visible">
      <div class="modal-content">
        <button (click)="fechar()">✕</button>
        <h2>{{ content?.label }}</h2>
        <p>{{ content?.descricao_longa }}</p>
        <h3>Opções:</h3>
        <ul>
          <li *ngFor="let opt of content?.opcoes">
            <strong>{{ opt.label }}</strong>: {{ opt.descricao }}
          </li>
        </ul>
      </div>
    </div>
  `,
  styles: [`
    .modal {
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.5);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 1000;
    }
  `]
})
export class HelpModalComponent {
  @Input() visible = false;
  @Input() content: any;
  @Output() fecharEvent = new EventEmitter();

  fechar() {
    this.fecharEvent.emit();
  }
}
```

---

## 📐 Padrões de Integração

### Padrão 1: Pop-up Modal (Recomendado para Desktop)

```javascript
function abrirAjuda() {
  const modal = window.open(
    'docs/NBR5410-Help-Modal.html',
    'help',
    'width=1000,height=800,scrollbars=yes,toolbar=no'
  );
  modal.focus();
}
```

**Vantagens:** Simples, não interfere com formulário  
**Desvantagens:** Pop-ups podem ser bloqueados

---

### Padrão 2: Sidebar (Recomendado para Aplicações)

```html
<div style="display: grid; grid-template-columns: 1fr 300px; gap: 20px;">
  <!-- Formulário à esquerda -->
  <form id="formulario"></form>

  <!-- Help sidebar à direita -->
  <aside id="help-sidebar" style="border-left: 1px solid #ccc; padding: 20px;">
    <h3>Ajuda: <span id="help-title"></span></h3>
    <div id="help-content"></div>
  </aside>
</div>

<script>
function atualizarAjuda(fieldName) {
  fetch('docs/NBR5410-Help-Schema.json')
    .then(r => r.json())
    .then(data => {
      const campo = data.conformidade_nbr5410.campos[fieldName];
      document.getElementById('help-title').textContent = campo.label;
      document.getElementById('help-content').innerHTML = `
        <p>${campo.descricao_curta}</p>
        <h4>Opções:</h4>
        <ul>
          ${campo.opcoes.map(o => `<li><strong>${o.label}</strong>: ${o.descricao}</li>`).join('')}
        </ul>
      `;
    });
}

// Atualizar ao focar em cada campo
document.querySelectorAll('input, select, textarea').forEach(el => {
  el.addEventListener('focus', () => atualizarAjuda(el.name));
});
</script>
```

---

### Padrão 3: Tooltip em Hover (Recomendado para Mobile)

```html
<style>
.help-icon {
  cursor: help;
  border-bottom: 1px dotted #1e40af;
  font-weight: bold;
}

.tooltip {
  position: relative;
  display: inline-block;
}

.tooltip .tooltiptext {
  visibility: hidden;
  width: 250px;
  background-color: #1e40af;
  color: #fff;
  text-align: left;
  border-radius: 6px;
  padding: 10px;
  position: absolute;
  z-index: 1;
  bottom: 125%;
  left: 50%;
  margin-left: -120px;
  opacity: 0;
  transition: opacity 0.3s;
  font-size: 13px;
  font-weight: normal;
}

.tooltip:hover .tooltiptext {
  visibility: visible;
  opacity: 1;
}
</style>

<label>
  Zona do Banheiro
  <span class="tooltip help-icon">
    ?
    <span class="tooltiptext">
      Localização do equipamento em relação à banheira.
      Zona 0-3 conforme distância.
    </span>
  </span>
</label>
```

---

## ✅ Checklist de Implementação

### Fase 1: Preparação (15 minutos)
- [ ] Copiar 5 arquivos para diretório `docs/`
- [ ] Revisar Help Hub (`NBR5410-Help-Hub.html`)
- [ ] Ler Guia Completo para entender contexto
- [ ] Definir qual padrão usar (modal, sidebar, tooltip)

### Fase 2: Desenvolvimento (2-4 horas)
- [ ] Adicionar botões de ajuda ao formulário
- [ ] Integrar com framework escolhido (React/Vue/Angular/etc)
- [ ] Testar links e funcionalidades
- [ ] Ajustar CSS para corresponder design
- [ ] Validar responsividade em mobile

### Fase 3: Testes (1-2 horas)
- [ ] Testar abertura do Help Modal
- [ ] Testar em diferentes browsers
- [ ] Testar em mobile/tablet
- [ ] Validar links internos (Markdown files)
- [ ] Testar JSON schema carregando corretamente

### Fase 4: Deployment (30 minutos)
- [ ] Deploy em staging
- [ ] Validar em staging
- [ ] Deploy em produção
- [ ] Monitor de acessos
- [ ] Collect user feedback

---

## 🐛 Troubleshooting

### Problema: Pop-up é bloqueado
**Solução:** Use iframe ou sidebar em vez de `window.open()`
```javascript
// Usar iframe
<iframe src="docs/NBR5410-Help-Modal.html" 
        style="width:100%; height:600px; border:1px solid #ccc;">
</iframe>
```

### Problema: JSON não carrega em JavaScript
**Solução:** Usar fetch com try-catch
```javascript
async function loadHelp() {
  try {
    const response = await fetch('docs/NBR5410-Help-Schema.json');
    if (!response.ok) throw new Error('Failed to load');
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Erro ao carregar help:', error);
    // Fallback para help genérico
  }
}
```

### Problema: Markdown files não renderizam
**Solução:** Usar biblioteca markdown
```javascript
// Instalar: npm install marked
import { marked } from 'marked';

async function loadMarkdownGuide() {
  const response = await fetch('docs/NBR5410-Conformidade-Guia-Completo.md');
  const markdown = await response.text();
  const html = marked(markdown);
  document.getElementById('guide').innerHTML = html;
}
```

### Problema: CSS do Modal não funciona em iframe
**Solução:** Adicionar `sandbox` attribute e permitir styles
```html
<iframe src="docs/NBR5410-Help-Modal.html"
        sandbox="allow-same-origin allow-scripts"
        style="width:100%; height:600px;">
</iframe>
```

---

## 📊 Monitoramento & Analytics

### Coletar dados de uso
```javascript
// Rastrear quais campos recebem mais help requests
function trackHelpAccess(fieldName) {
  // Google Analytics
  if (window.gtag) {
    gtag('event', 'help_accessed', {
      field_name: fieldName,
      timestamp: new Date()
    });
  }

  // Seu analytics backend
  fetch('/api/analytics/help', {
    method: 'POST',
    body: JSON.stringify({ field: fieldName })
  });
}
```

### Dashboard de uso (exemplo)
```
Campos com mais acessos de help:
1. Zona do Banheiro - 245 acessos
2. DB Informado - 189 acessos
3. Grau de Proteção IP - 156 acessos
4. Classe - 98 acessos
5. Observações - 45 acessos
```

---

## 🔄 Versionamento e Atualizações

### Como manter documentação sincronizada

```bash
# Arquivo de versão
docs/NBR5410-VERSION.txt
1.0 - 2026-06-21 - Versão inicial
1.1 - 2026-07-15 - Atualizações baseado em feedback
```

### Sistema de versionamento
```json
{
  "version": "1.0",
  "lastUpdated": "2026-06-21",
  "schema": {
    "version": "1.0",
    "compatibility": ">=1.0"
  }
}
```

---

## 📞 Suporte e Manutenção

| Tópico | Responsável | Frequência |
|--------|------------|-----------|
| Atualizações de conteúdo | Analyst | Semestral |
| Ajustes de design | UX/Designer | Conforme necessário |
| Monitoramento de bugs | Developer | Contínuo |
| Análise de uso | PM | Mensal |

---

## 🎓 Treinamento da Equipe

### Para Desenvolvedores (2 horas)
1. Revisar Help Hub (30 min)
2. Estudar Schema JSON (30 min)
3. Implementar em projeto teste (60 min)

### Para Designers (1 hora)
1. Revisar Modal HTML (30 min)
2. Customizar CSS para marca (30 min)

### Para PMs/Analistas (1 hora)
1. Entender Help Index (30 min)
2. Definir estratégia de uso (30 min)

---

**Documento versão 1.0 | Data: 2026-06-21**  
**Gerado por: Atlas (AIOX Analyst)**

