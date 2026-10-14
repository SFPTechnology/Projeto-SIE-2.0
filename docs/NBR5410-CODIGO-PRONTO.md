# 💻 Código Pronto para Copiar e Colar

Este arquivo contém snippets prontos para usar em diferentes contextos. **Copie, cole, customize.**

## 📋 Índice

- [HTML Simples](#html-simples)
- [HTML + Bootstrap](#html--bootstrap)
- [React Component](#react-component)
- [Vue Component](#vue-component)
- [JavaScript Vanilla](#javascript-vanilla)
- [Node.js/Express API](#nodejs-express-api)
- [CSS Estilos Prontos](#css-estilos-prontos)

---

## HTML Simples

### Solução Minimalista (Copie e Cole)

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Formulário Conformidade NBR 5410</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; padding: 20px; background: #f5f5f5; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; }
        .form-group { margin-bottom: 20px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; color: #1e40af; }
        input, select, textarea { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-family: Arial; }
        button { padding: 10px 20px; background: #1e40af; color: white; border: none; border-radius: 4px; cursor: pointer; margin-right: 10px; }
        button:hover { background: #1e3a8a; }
        .help-btn { background: #0284c7; padding: 5px 10px; font-size: 12px; }
        .alert { background: #fef3c7; border-left: 4px solid #f59e0b; padding: 15px; margin: 20px 0; border-radius: 4px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Conformidade NBR 5410</h1>

        <div class="alert">
            ℹ️ Clique em <strong>Ajuda</strong> próximo a cada campo para mais informações.
        </div>

        <form id="conformidade-form">
            <!-- CAMPO 1 -->
            <div class="form-group">
                <label>
                    Zona do Banheiro
                    <button type="button" class="help-btn" onclick="ajuda('zona')">?</button>
                </label>
                <select name="zona" required>
                    <option value="">-- Selecione --</option>
                    <option value="zona_0">Zona 0 (Interior da banheira)</option>
                    <option value="zona_1">Zona 1 (Até 0,6m da banheira)</option>
                    <option value="zona_2">Zona 2 (0,6m a 1,2m da banheira)</option>
                    <option value="zona_3">Zona 3 (Fora do banheiro)</option>
                </select>
            </div>

            <!-- CAMPO 2 -->
            <div class="form-group">
                <label>
                    DB Informado
                    <button type="button" class="help-btn" onclick="ajuda('db')">?</button>
                </label>
                <select name="db" required>
                    <option value="">-- Selecione --</option>
                    <option value="sim">Sim (Circuito protegido por DR)</option>
                    <option value="nao">Não (Sem proteção DR)</option>
                </select>
            </div>

            <!-- CAMPO 3 -->
            <div class="form-group">
                <label>
                    Grau de Proteção IP
                    <button type="button" class="help-btn" onclick="ajuda('ip')">?</button>
                </label>
                <input type="text" name="ip" placeholder="Ex: IP44, IPX7" required>
            </div>

            <!-- CAMPO 4 -->
            <div class="form-group">
                <label>
                    Influência Externa
                    <button type="button" class="help-btn" onclick="ajuda('influencia')">?</button>
                </label>
                <select name="influencia">
                    <option value="opcional">Opcional (padrão)</option>
                    <option value="obrigatorio">Obrigatório</option>
                    <option value="nao_aplicavel">Não aplicável</option>
                </select>
            </div>

            <!-- CAMPO 5 -->
            <div class="form-group">
                <label>
                    Classe
                    <button type="button" class="help-btn" onclick="ajuda('classe')">?</button>
                </label>
                <input type="text" name="classe" placeholder="Ex: AD2, AL2, MD1" required>
            </div>

            <!-- CAMPO 6 -->
            <div class="form-group">
                <label>
                    Observações
                    <button type="button" class="help-btn" onclick="ajuda('obs')">?</button>
                </label>
                <textarea name="observacoes" rows="4" placeholder="Notas técnicas adicionais..."></textarea>
            </div>

            <div>
                <button type="submit">✓ Enviar</button>
                <button type="reset">↺ Limpar</button>
                <button type="button" onclick="abrirGuiaCompleta()">📖 Guia Completo</button>
            </div>
        </form>
    </div>

    <script>
        function ajuda(campo) {
            const ajudas = {
                zona: 'Zona do Banheiro:\n\n• Zona 0: Interior da banheira (raro)\n• Zona 1: Até 0,6m (proteção máxima)\n• Zona 2: 0,6m-1,2m (proteção máxima)\n• Zona 3: Fora do banheiro\n\nPara mais detalhes, clique em "Guia Completo"',
                db: 'DB Informado:\n\n• SIM = Circuito com Disjuntor Residual (seguro)\n• NÃO = Sem proteção (NÃO-CONFORME)\n\n⚠️ CRÍTICO: Zona 1-2 SEM DB é proibido!',
                ip: 'Grau de Proteção IP:\n\nFormato: IPxy ou IPXy\n\n• Zona 0: IPX7/X8\n• Zona 1-2: IPX4 (padrão)\n• Zona 3: IPX1\n\nExemplos: IP44, IP54, IPX7',
                influencia: 'Influência Externa:\n\n• Obrigatório: Fatores especiais (sauna, umidade extrema)\n• Opcional: Banheiro comum (padrão)\n• Não aplicável: Áreas secas',
                classe: 'Classe:\n\n• AD2: Tomata em banheiro\n• AL2: Iluminação em banheiro\n• MD1: Ventilador/exaustor\n• AD4: Proteção máxima',
                obs: 'Observações:\n\nDocumente justificativas técnicas:\n\nEx: "Tomada Legrand, AD2, IP44, DR 30mA, Zona 2"'
            };
            alert(ajudas[campo] || 'Ajuda não disponível');
        }

        function abrirGuiaCompleta() {
            const opcao = prompt('Escolha:\n1 = Help Rápido\n2 = Guia Completa\n3 = Modal Interativo\n\nDigite 1, 2 ou 3:');
            const urls = {
                '1': 'NBR5410-Help-Rapido.md',
                '2': 'NBR5410-Conformidade-Guia-Completo.md',
                '3': 'NBR5410-Help-Modal.html'
            };
            if (urls[opcao]) window.open(urls[opcao], '_blank');
        }

        document.getElementById('conformidade-form').addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            const data = Object.fromEntries(formData);
            
            // Validações críticas
            if (data.zona.includes('zona_1') || data.zona.includes('zona_2')) {
                if (data.db === 'nao') {
                    alert('❌ ERRO CRÍTICO: Zona 1-2 SEM DB é NÃO-CONFORME!');
                    return;
                }
            }
            
            console.log('Dados do formulário:', data);
            alert('✓ Formulário validado com sucesso!');
        });
    </script>
</body>
</html>
```

---

## HTML + Bootstrap

### Com Bootstrap 5 (Copie e Cole)

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Conformidade NBR 5410</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .help-badge { display: inline-block; margin-left: 10px; background: #0284c7; color: white; padding: 3px 8px; border-radius: 3px; cursor: pointer; font-size: 11px; font-weight: bold; }
        .help-badge:hover { background: #0369a1; }
        .critical { border-left: 3px solid #ef4444; padding-left: 15px; }
    </style>
</head>
<body>
    <div class="container mt-5">
        <div class="row">
            <div class="col-md-8 offset-md-2">
                <h1 class="mb-4">📋 Conformidade NBR 5410</h1>

                <div class="alert alert-info">
                    <strong>ℹ️ Dica:</strong> Clique em <span class="badge bg-primary">?</span> para ajuda em cada campo.
                </div>

                <form id="form-conformidade">
                    <!-- ZONA -->
                    <div class="mb-3">
                        <label class="form-label">
                            Zona do Banheiro
                            <span class="help-badge" data-bs-toggle="tooltip" title="Clique para ajuda" onclick="mostrarAjudaZona()">?</span>
                        </label>
                        <select class="form-select" name="zona" required>
                            <option value="">-- Selecione --</option>
                            <option value="zona_1">Zona 1 (Até 0,6m) - IP mín: IPX4</option>
                            <option value="zona_2">Zona 2 (0,6-1,2m) - IP mín: IPX4</option>
                            <option value="zona_3">Zona 3 (Fora do banheiro) - IP mín: IPX1</option>
                        </select>
                    </div>

                    <!-- DB -->
                    <div class="mb-3 critical">
                        <label class="form-label">
                            DB Informado <span class="badge bg-danger">CRÍTICO</span>
                            <span class="help-badge" onclick="mostrarAjudaDB()">?</span>
                        </label>
                        <div class="form-check">
                            <input class="form-check-input" type="radio" name="db" value="sim" id="db_sim" required>
                            <label class="form-check-label" for="db_sim">
                                ✓ Sim (Circuito protegido por DR)
                            </label>
                        </div>
                        <div class="form-check">
                            <input class="form-check-input" type="radio" name="db" value="nao" id="db_nao">
                            <label class="form-check-label" for="db_nao">
                                ✗ Não (Sem proteção) ⚠️ NÃO-CONFORME
                            </label>
                        </div>
                    </div>

                    <!-- IP -->
                    <div class="mb-3">
                        <label class="form-label">
                            Grau de Proteção IP
                            <span class="help-badge" onclick="mostrarAjudaIP()">?</span>
                        </label>
                        <input type="text" class="form-control" name="ip" placeholder="Ex: IP44, IPX7" required>
                        <small class="form-text text-muted">Zona 1-2: mínimo IPX4 | Zona 3: mínimo IPX1</small>
                    </div>

                    <!-- CLASSE -->
                    <div class="mb-3">
                        <label class="form-label">
                            Classe
                            <span class="help-badge" onclick="mostrarAjudaClasse()">?</span>
                        </label>
                        <input type="text" class="form-control" name="classe" placeholder="Ex: AD2, AL2, MD1" required>
                    </div>

                    <!-- OBSERVAÇÕES -->
                    <div class="mb-3">
                        <label class="form-label">
                            Observações
                            <span class="help-badge" onclick="mostrarAjudaObs()">?</span>
                        </label>
                        <textarea class="form-control" name="observacoes" rows="3" placeholder="Notas técnicas..."></textarea>
                    </div>

                    <div class="d-grid gap-2 d-sm-flex justify-content-sm-end">
                        <button type="submit" class="btn btn-primary">✓ Enviar</button>
                        <button type="reset" class="btn btn-secondary">↺ Limpar</button>
                        <button type="button" class="btn btn-outline-primary" onclick="abrirGuia()">📖 Guia</button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <!-- MODALS DE AJUDA -->
    <div class="modal fade" id="ajudaModal" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title" id="ajudaTitulo">Ajuda</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                </div>
                <div class="modal-body" id="ajudaConteudo"></div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        const modal = new bootstrap.Modal(document.getElementById('ajudaModal'));

        function mostrarAjuda(titulo, conteudo) {
            document.getElementById('ajudaTitulo').textContent = titulo;
            document.getElementById('ajudaConteudo').innerHTML = conteudo;
            modal.show();
        }

        function mostrarAjudaZona() {
            mostrarAjuda('Zona do Banheiro', `
                <p><strong>Localização em relação à banheira:</strong></p>
                <ul>
                    <li><strong>Zona 1:</strong> Até 0,6m - Requer IPX4 mínimo, DB obrigatório</li>
                    <li><strong>Zona 2:</strong> 0,6m a 1,2m - Requer IPX4 mínimo, DB obrigatório</li>
                    <li><strong>Zona 3:</strong> Fora do banheiro - Requer IPX1 mínimo</li>
                </ul>
                <p><small>Para mais informações, consulte o <strong>Guia Completo</strong></small></p>
            `);
        }

        function mostrarAjudaDB() {
            mostrarAjuda('DB Informado', `
                <p><strong>Disjuntor Diferencial-Residual (DR/DDR)</strong></p>
                <ul>
                    <li><strong>SIM:</strong> Circuito protegido (seguro) ✓</li>
                    <li><strong>NÃO:</strong> Sem proteção (NÃO-CONFORME) ✗</li>
                </ul>
                <div class="alert alert-danger">
                    <strong>⚠️ CRÍTICO:</strong> Zona 1-2 SEM DB é proibido pela NBR 5410!
                </div>
            `);
        }

        function mostrarAjudaIP() {
            mostrarAjuda('Grau de Proteção IP', `
                <p><strong>Formato: IPxy ou IPXy</strong></p>
                <table class="table table-sm">
                    <tr><td>Zona 0</td><td>IPX7 ou IPX8</td></tr>
                    <tr><td><strong>Zona 1-2</strong></td><td><strong>IPX4 (padrão)</strong></td></tr>
                    <tr><td>Zona 3</td><td>IPX1</td></tr>
                </table>
                <p><small>Exemplos: IP44, IP54, IP65, IPX7</small></p>
            `);
        }

        function mostrarAjudaClasse() {
            mostrarAjuda('Classe do Equipamento', `
                <table class="table table-sm">
                    <tr><td><strong>AD2</strong></td><td>Tomada em banheiro</td></tr>
                    <tr><td><strong>AL2</strong></td><td>Iluminação em banheiro</td></tr>
                    <tr><td><strong>MD1</strong></td><td>Ventilador/exaustor</td></tr>
                    <tr><td><strong>AD4</strong></td><td>Proteção máxima</td></tr>
                </table>
            `);
        }

        function mostrarAjudaObs() {
            mostrarAjuda('Observações', `
                <p><strong>Documente justificativas técnicas:</strong></p>
                <p><code>Tomada Legrand, AD2, IP44, DR 30mA, Zona 2</code></p>
            `);
        }

        function abrirGuia() {
            const url = prompt('1 = Help Rápido\n2 = Guia Completa\n3 = Modal\n\nEscolha (1-3):');
            const urls = {'1': 'NBR5410-Help-Rapido.md', '2': 'NBR5410-Conformidade-Guia-Completo.md', '3': 'NBR5410-Help-Modal.html'};
            if (urls[url]) window.open(urls[url]);
        }

        document.getElementById('form-conformidade').addEventListener('submit', function(e) {
            e.preventDefault();
            const zona = document.querySelector('select[name="zona"]').value;
            const db = document.querySelector('input[name="db"]:checked').value;

            if ((zona.includes('zona_1') || zona.includes('zona_2')) && db === 'nao') {
                alert('❌ ERRO: Zona 1-2 SEM DB é NÃO-CONFORME!');
                return;
            }
            alert('✓ Formulário validado com sucesso!');
        });
    </script>
</body>
</html>
```

---

## React Component

### Hook Customizado + Component (Copie e Cole)

```jsx
// hooks/useHelpSchema.js
import { useState, useEffect } from 'react';

export const useHelpSchema = () => {
  const [schema, setSchema] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/docs/NBR5410-Help-Schema.json')
      .then(res => res.json())
      .then(data => {
        setSchema(data);
        setLoading(false);
      });
  }, []);

  return { schema: schema?.conformidade_nbr5410, loading };
};

// components/ConformidadeForm.jsx
import { useState } from 'react';
import { useHelpSchema } from '../hooks/useHelpSchema';

export default function ConformidadeForm() {
  const { schema, loading } = useHelpSchema();
  const [formData, setFormData] = useState({});
  const [helpField, setHelpField] = useState(null);

  if (loading) return <div>Carregando...</div>;

  const campos = schema.campos;

  return (
    <div style={{ maxWidth: '600px', margin: '0 auto', padding: '20px' }}>
      <h1>Conformidade NBR 5410</h1>

      <form onSubmit={(e) => {
        e.preventDefault();
        console.log('Dados:', formData);
        alert('✓ Formulário enviado!');
      }}>
        {/* ZONA */}
        <div style={{ marginBottom: '20px' }}>
          <label>
            {campos.zona_do_banheiro.label}
            <button
              type="button"
              onClick={() => setHelpField('zona_do_banheiro')}
              style={{ marginLeft: '10px', background: '#0284c7', color: 'white', border: 'none', padding: '2px 6px', borderRadius: '3px' }}
            >
              ?
            </button>
          </label>
          <select
            name="zona"
            onChange={(e) => setFormData({ ...formData, zona: e.target.value })}
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
          >
            <option value="">-- Selecione --</option>
            {campos.zona_do_banheiro.opcoes.map((opt) => (
              <option key={opt.valor} value={opt.valor}>
                {opt.label} - {opt.descricao}
              </option>
            ))}
          </select>
        </div>

        {/* DB */}
        <div style={{ marginBottom: '20px', borderLeft: '3px solid #ef4444', paddingLeft: '15px' }}>
          <label>
            {campos.db_informado.label} ⚠️ CRÍTICO
            <button
              type="button"
              onClick={() => setHelpField('db_informado')}
              style={{ marginLeft: '10px', background: '#0284c7', color: 'white', border: 'none', padding: '2px 6px', borderRadius: '3px' }}
            >
              ?
            </button>
          </label>
          {campos.db_informado.opcoes.map((opt) => (
            <div key={opt.valor} style={{ marginTop: '8px' }}>
              <label>
                <input
                  type="radio"
                  name="db"
                  value={opt.valor}
                  onChange={(e) => setFormData({ ...formData, db: e.target.value })}
                />
                {opt.label} - {opt.significado}
              </label>
            </div>
          ))}
        </div>

        {/* IP */}
        <div style={{ marginBottom: '20px' }}>
          <label>
            {campos.grau_de_protecao_ip.label}
            <button
              type="button"
              onClick={() => setHelpField('grau_de_protecao_ip')}
              style={{ marginLeft: '10px', background: '#0284c7', color: 'white', border: 'none', padding: '2px 6px', borderRadius: '3px' }}
            >
              ?
            </button>
          </label>
          <input
            type="text"
            placeholder={campos.grau_de_protecao_ip.exemplos_validos[0]}
            onChange={(e) => setFormData({ ...formData, ip: e.target.value })}
            style={{ width: '100%', padding: '8px', marginTop: '5px' }}
          />
        </div>

        <button type="submit" style={{ padding: '10px 20px', background: '#1e40af', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
          ✓ Enviar
        </button>
      </form>

      {/* HELP MODAL */}
      {helpField && (
        <div style={{ position: 'fixed', top: 0, left: 0, width: '100%', height: '100%', background: 'rgba(0,0,0,0.5)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 1000 }}>
          <div style={{ background: 'white', borderRadius: '8px', padding: '30px', maxWidth: '600px', maxHeight: '80vh', overflow: 'auto', position: 'relative' }}>
            <button
              onClick={() => setHelpField(null)}
              style={{ position: 'absolute', top: '10px', right: '10px', background: 'transparent', border: 'none', fontSize: '24px', cursor: 'pointer' }}
            >
              ✕
            </button>
            <h2>{campos[helpField].label}</h2>
            <p>{campos[helpField].descricao_longa}</p>
            {campos[helpField].opcoes && (
              <>
                <h3>Opções:</h3>
                <ul>
                  {campos[helpField].opcoes.map((opt) => (
                    <li key={opt.valor}>
                      <strong>{opt.label}</strong>: {opt.descricao || opt.significado}
                    </li>
                  ))}
                </ul>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
}
```

---

## JavaScript Vanilla

### Sem Frameworks (Copie e Cole)

```javascript
// help-system.js
class ConformidadeHelpSystem {
  constructor(schemaUrl) {
    this.schema = null;
    this.loadSchema(schemaUrl);
  }

  async loadSchema(url) {
    try {
      const response = await fetch(url);
      this.schema = await response.json();
      this.init();
    } catch (error) {
      console.error('Erro ao carregar schema:', error);
    }
  }

  init() {
    // Adicionar listeners a todos os botões de ajuda
    document.querySelectorAll('[data-help-field]').forEach(btn => {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const fieldName = btn.dataset.helpField;
        this.showHelp(fieldName);
      });
    });

    // Validação ao enviar formulário
    const form = document.getElementById('conformidade-form');
    if (form) {
      form.addEventListener('submit', (e) => {
        if (!this.validate(form)) {
          e.preventDefault();
        }
      });
    }
  }

  showHelp(fieldName) {
    const campo = this.schema.conformidade_nbr5410.campos[fieldName];
    if (!campo) return;

    const modal = this.createModal(campo);
    document.body.appendChild(modal);

    // Fechar ao clicar em X
    modal.querySelector('.modal-close').addEventListener('click', () => {
      modal.remove();
    });

    // Fechar ao clicar fora
    modal.addEventListener('click', (e) => {
      if (e.target === modal) modal.remove();
    });
  }

  createModal(campo) {
    const modal = document.createElement('div');
    modal.className = 'help-modal';
    modal.innerHTML = `
      <div class="help-modal-content">
        <button class="modal-close" type="button">✕</button>
        <h2>${campo.label}</h2>
        <p>${campo.descricao_longa}</p>
        ${campo.opcoes ? `
          <h3>Opções:</h3>
          <ul>
            ${campo.opcoes.map(opt => `
              <li>
                <strong>${opt.label}</strong>: ${opt.descricao || opt.significado}
              </li>
            `).join('')}
          </ul>
        ` : ''}
      </div>
    `;

    // Estilos inline
    Object.assign(modal.style, {
      position: 'fixed',
      top: 0,
      left: 0,
      width: '100%',
      height: '100%',
      background: 'rgba(0,0,0,0.5)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000
    });

    const content = modal.querySelector('.help-modal-content');
    Object.assign(content.style, {
      background: 'white',
      borderRadius: '8px',
      padding: '30px',
      maxWidth: '600px',
      maxHeight: '80vh',
      overflow: 'auto',
      position: 'relative'
    });

    return modal;
  }

  validate(form) {
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);

    const bloqueadores = this.schema.conformidade_nbr5410.bloqueadores_criticos;
    
    for (const bloqueador of bloqueadores) {
      if (bloqueador.condicao.includes('Zona 1 ou 2 SEM DB')) {
        if ((data.zona.includes('zona_1') || data.zona.includes('zona_2')) && data.db === 'nao') {
          alert(`❌ ${bloqueador.severidade}: ${bloqueador.acao}`);
          return false;
        }
      }
    }

    return true;
  }
}

// Usar
const helpSystem = new ConformidadeHelpSystem('docs/NBR5410-Help-Schema.json');
```

```html
<!-- Usar no HTML -->
<label>
  Zona do Banheiro
  <button type="button" data-help-field="zona_do_banheiro">?</button>
</label>
<select name="zona" required>...</select>

<label>
  DB Informado
  <button type="button" data-help-field="db_informado">?</button>
</label>
<select name="db" required>...</select>
```

---

## Node.js/Express API

### Servidor de Help (Copie e Cole)

```javascript
// server.js
const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const helpSchema = JSON.parse(fs.readFileSync(path.join(__dirname, 'docs/NBR5410-Help-Schema.json'), 'utf-8'));

// Rota: Obter ajuda de um campo específico
app.get('/api/help/:fieldName', (req, res) => {
  const { fieldName } = req.params;
  const campo = helpSchema.conformidade_nbr5410.campos[fieldName];

  if (!campo) {
    return res.status(404).json({ error: 'Campo não encontrado' });
  }

  res.json({
    label: campo.label,
    descricao_curta: campo.descricao_curta,
    descricao_longa: campo.descricao_longa,
    opcoes: campo.opcoes,
    exemplos: campo.exemplos
  });
});

// Rota: Obter todas as regras de ouro
app.get('/api/help/regras/ouro', (req, res) => {
  res.json(helpSchema.conformidade_nbr5410.regras_ouro);
});

// Rota: Obter checklist
app.get('/api/help/checklist', (req, res) => {
  res.json(helpSchema.conformidade_nbr5410.checklist);
});

// Rota: Validar campo
app.post('/api/validate', express.json(), (req, res) => {
  const { fieldName, value } = req.body;
  const bloqueadores = helpSchema.conformidade_nbr5410.bloqueadores_criticos;

  const violations = bloqueadores.filter(b => b.condicao.includes(fieldName));

  if (violations.length > 0) {
    return res.status(400).json({
      valid: false,
      violations: violations
    });
  }

  res.json({ valid: true });
});

app.listen(3000, () => console.log('Help API rodando em http://localhost:3000'));
```

---

## CSS Estilos Prontos

### Todos os Estilos em Um Arquivo

```css
/* styles.css */

/* CONTAINER */
.conformidade-container {
  max-width: 600px;
  margin: 0 auto;
  background: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

/* FORM GROUPS */
.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #1e40af;
  font-size: 14px;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-family: Arial, sans-serif;
  font-size: 14px;
}

.form-group input:focus,
.form-group select:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #1e40af;
  box-shadow: 0 0 0 2px rgba(30, 64, 175, 0.1);
}

/* HELP BUTTON */
.help-btn {
  background: #0284c7;
  color: white;
  border: none;
  padding: 4px 8px;
  border-radius: 3px;
  cursor: pointer;
  font-size: 12px;
  font-weight: bold;
  margin-left: 8px;
}

.help-btn:hover {
  background: #0369a1;
}

/* MODAL */
.help-modal {
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
  animation: fadeIn 0.3s;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.help-modal-content {
  background: white;
  border-radius: 8px;
  padding: 30px;
  max-width: 600px;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
  animation: slideIn 0.3s;
}

@keyframes slideIn {
  from { transform: translateY(-50px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

.help-modal-content h2 {
  color: #1e40af;
  margin-bottom: 15px;
}

.help-modal-content h3 {
  color: #1e40af;
  margin-top: 20px;
  margin-bottom: 10px;
  font-size: 16px;
}

.help-modal-content ul {
  margin-left: 20px;
  color: #666;
}

.help-modal-content li {
  margin-bottom: 8px;
  line-height: 1.5;
}

.modal-close {
  position: absolute;
  top: 10px;
  right: 10px;
  background: transparent;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
}

.modal-close:hover {
  color: #1e40af;
}

/* ALERTAS */
.alert {
  padding: 15px;
  margin: 20px 0;
  border-radius: 4px;
  border-left: 4px solid;
}

.alert-critical {
  background: #fee2e2;
  border-left-color: #ef4444;
  color: #991b1b;
}

.alert-info {
  background: #dbeafe;
  border-left-color: #0284c7;
  color: #0c4a6e;
}

.alert-warning {
  background: #fef3c7;
  border-left-color: #f59e0b;
  color: #92400e;
}

/* BUTTONS */
button[type="submit"],
button[type="reset"] {
  padding: 10px 20px;
  margin-right: 10px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: all 0.3s;
}

button[type="submit"] {
  background: #1e40af;
  color: white;
}

button[type="submit"]:hover {
  background: #1e3a8a;
}

button[type="reset"] {
  background: #e5e7eb;
  color: #374151;
}

button[type="reset"]:hover {
  background: #d1d5db;
}

/* RESPONSIVE */
@media (max-width: 768px) {
  .conformidade-container {
    padding: 20px;
  }

  .help-modal-content {
    margin: 20px;
    max-width: none;
  }

  .form-group input,
  .form-group select,
  .form-group textarea {
    font-size: 16px; /* Evita zoom em mobile */
  }
}
```

---

## 🎯 Quick Integration Checklist

- [ ] Escolheu seu framework/contexto
- [ ] Copiar o código acima para seu projeto
- [ ] Substitua os caminhos de arquivo conforme necessário
- [ ] Customize CSS para sua marca
- [ ] Teste em navegador
- [ ] Teste responsividade mobile
- [ ] Deploy!

---

**Código gerado por: Atlas (AIOX Analyst)**  
**Data: 2026-06-21**

