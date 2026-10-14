const apiBase = localStorage.getItem('sie.apiBase') || 'http://127.0.0.1:8000';
const health = document.querySelector('#health');
const result = document.querySelector('#resultado');
let ultimaAnalise = null;

async function checkHealth() {
  try { const r = await fetch(`${apiBase}/api/v1/health`); const data = await r.json(); health.textContent = `API online · ${data.version}`; health.style.color = 'var(--accent)'; }
  catch { health.textContent = 'API local não conectada'; health.style.color = 'var(--warn)'; }
}
function value(form, name) { return form.elements[name].value; }
function number(form, name) { return Number(value(form, name)); }
function escapeHTML(value) { const node = document.createElement('span'); node.textContent = String(value ?? ''); return node.innerHTML; }
function card(label, main, note) { return `<div class="result-card"><span>${escapeHTML(label)}</span><strong>${escapeHTML(main)}</strong><small>${escapeHTML(note)}</small></div>`; }

document.querySelector('[data-focus]').addEventListener('click', () => document.querySelector('#corrente').focus());
document.querySelector('#analysis-form').addEventListener('submit', async (event) => {
  event.preventDefault(); const form = event.currentTarget; const submit = form.querySelector('[type=submit]'); submit.disabled = true; submit.textContent = 'Calculando…';
  const payload = { corrente_a:number(form,'corrente_a'), comprimento_m:number(form,'comprimento_m'), tensao_v:number(form,'tensao_v'), resistencia_ohm_km:number(form,'resistencia_ohm_km'), fator_correcao:number(form,'fator_correcao'), tabela_condutores:[{secao_mm2:2.5,capacidade_a:24},{secao_mm2:4,capacidade_a:32},{secao_mm2:6,capacidade_a:41},{secao_mm2:10,capacidade_a:57}], evidencia:{documento:value(form,'documento'),edicao:value(form,'edicao'),referencia:value(form,'referencia')} };
  try { const response = await fetch(`${apiBase}/api/v1/circuitos/analisar`, {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)}); const data = await response.json(); if(!response.ok) throw new Error(data.detail || 'Falha ao analisar'); ultimaAnalise = payload; const approved=data.liberado_para_uso_normativo; result.innerHTML=`<div class="section-heading"><div><p class="eyebrow">02 · RESULTADO</p><h2>Decisão técnica</h2></div><span class="tag ${approved?'':'muted'}">${escapeHTML(data.status_engenharia)}</span></div><div class="result-status ${approved?'approved':'pending'}">${approved?'Gate normativo aprovado.':'Gate normativo não aprovado.'} ${escapeHTML(data.aviso||'')}</div><div class="result-cards">${card('Condutor selecionado',`${data.condutor.secao_mm2} mm²`,`${data.condutor.capacidade_corrigida_a} A · ${data.condutor.criterio}`)}${card('Disjuntor comercial',`${data.disjuntor.corrente_a} A`,data.disjuntor.criterio)}${card('Queda de tensão',`${data.queda_tensao.queda_percentual}%`,`${data.queda_tensao.queda_v} V · ${data.queda_tensao.formula}`)}${card('Evidência',data.rastreabilidade.fonte,`${data.rastreabilidade.edicao} · ${data.rastreabilidade.referencia}`)}</div>`; }
  catch (error) { result.innerHTML=`<div class="section-heading"><div><p class="eyebrow">02 · RESULTADO</p><h2>Decisão técnica</h2></div></div><div class="result-status pending">Não foi possível concluir: ${escapeHTML(error.message)}</div>`; }
  finally { submit.disabled=false; submit.innerHTML='Executar análise <span>→</span>'; }
});
checkHealth();


// Local project data is opt-in and remains separate from the normative gate.
// Authentication token is read from a password input and never persisted.
const localProjectApi = 'http://127.0.0.1:8000/api/v1/local/projetos';
const projectStatus = document.querySelector('#project-status');
const projectId = document.querySelector('#project-id');
const projectRevision = document.querySelector('#project-revision');
const projectName = document.querySelector('#project-name');
const projectToken = document.querySelector('#project-token');

function authHeaders() {
  const token = projectToken.value.trim();
  if (token.length < 24) throw new Error('Informe o token local configurado na API.');
  return { Authorization: 'Bearer ' + token, 'Content-Type': 'application/json' };
}

async function projectResponse(response) {
  const data = await response.json();
  if (!response.ok) {
    const detail = typeof data.detail === 'string' ? data.detail : 'Verifique credenciais, campos e configuracao local.';
    throw new Error(response.status === 409 ? 'Conflito de revisao: ' + detail : detail);
  }
  return data;
}

document.querySelector('#project-save').addEventListener('click', async () => {
  if (!ultimaAnalise) {
    projectStatus.textContent = 'Execute uma analise antes de salvar.';
    return;
  }
  const button = document.querySelector('#project-save');
  button.disabled = true;
  try {
    const id = projectId.value.trim() || crypto.randomUUID();
    const payload = {
      id,
      nome: projectName.value.trim(),
      dados: { analise: ultimaAnalise },
      revisao_esperada: Number(projectRevision.value),
    };
    const response = await fetch(localProjectApi, {
      method: 'PUT', headers: authHeaders(), body: JSON.stringify(payload),
    });
    const saved = await projectResponse(response);
    projectId.value = saved.id;
    projectRevision.value = String(saved.revisao);
    projectStatus.textContent = 'Salvo localmente na revisao ' + saved.revisao + '. Copie o ID para reabrir.';
  } catch (error) {
    projectStatus.textContent = 'Nao foi possivel salvar: ' + error.message;
  } finally {
    button.disabled = false;
  }
});

document.querySelector('#project-load').addEventListener('click', async () => {
  const id = projectId.value.trim();
  if (!id) {
    projectStatus.textContent = 'Informe o ID do projeto que deseja reabrir.';
    return;
  }
  const button = document.querySelector('#project-load');
  button.disabled = true;
  try {
    const response = await fetch(localProjectApi + '/' + encodeURIComponent(id), {
      headers: authHeaders(),
    });
    const saved = await projectResponse(response);
    projectId.value = saved.id;
    projectName.value = saved.nome;
    projectRevision.value = String(saved.revisao);
    const entrada = saved.dados && saved.dados.analise;
    if (entrada && typeof entrada === 'object') {
      const form = document.querySelector('#analysis-form');
      for (const field of ['corrente_a', 'comprimento_m', 'tensao_v',
        'resistencia_ohm_km', 'fator_correcao']) {
        if (Object.prototype.hasOwnProperty.call(entrada, field)) {
          form.elements[field].value = entrada[field];
        }
      }
      for (const field of ['documento', 'edicao', 'referencia']) {
        if (entrada.evidencia && Object.prototype.hasOwnProperty.call(entrada.evidencia, field)) {
          form.elements[field].value = entrada.evidencia[field];
        }
      }
    }
    ultimaAnalise = null;
    result.textContent = 'Projeto reaberto. Execute uma nova analise para recalcular os resultados.';
    projectStatus.textContent = 'Projeto recuperado (revisao ' + saved.revisao + '). Confira os parametros e execute a analise.';
  } catch (error) {
    projectStatus.textContent = 'Nao foi possivel recuperar: ' + error.message;
  } finally {
    button.disabled = false;
  }
});
