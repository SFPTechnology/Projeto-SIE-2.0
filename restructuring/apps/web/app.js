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
// F01 has no normative approval capability. Even contradictory API flags stay pending.
document.querySelector('#analysis-form').addEventListener('submit', async (event) => {
  event.preventDefault(); const form = event.currentTarget; const submit = form.querySelector('[type=submit]'); submit.disabled = true; submit.textContent = 'Calculando…';
  const payload = { corrente_a:number(form,'corrente_a'), comprimento_m:number(form,'comprimento_m'), tensao_v:number(form,'tensao_v'), resistencia_ohm_km:number(form,'resistencia_ohm_km'), fator_correcao:number(form,'fator_correcao'), tabela_condutores:[{secao_mm2:2.5,capacidade_a:24},{secao_mm2:4,capacidade_a:32},{secao_mm2:6,capacidade_a:41},{secao_mm2:10,capacidade_a:57}], evidencia:{documento:value(form,'documento'),edicao:value(form,'edicao'),referencia:value(form,'referencia')} };
  try { const response = await fetch(`${apiBase}/api/v1/circuitos/analisar`, {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)}); const data = await response.json(); if(!response.ok) throw new Error(data.detail || 'Falha ao analisar'); ultimaAnalise = payload; const safeNotice = data.liberado_para_uso_normativo === false && data.status_engenharia === 'PENDENTE' ? data.aviso : 'Resposta normativa inconsistente com esta versão. Liberação bloqueada.'; result.innerHTML=`<div class="section-heading"><div><p class="eyebrow">02 · RESULTADO</p><h2>Decisão técnica</h2></div><span class="tag muted">PENDENTE</span></div><div class="result-status pending">Gate normativo não aprovado. ${escapeHTML(safeNotice||'')}</div><div class="result-cards">${card('Condutor selecionado',`${data.condutor.secao_mm2} mm²`,`${data.condutor.capacidade_corrigida_a} A · ${data.condutor.criterio}`)}${card('Disjuntor comercial',`${data.disjuntor.corrente_a} A`,data.disjuntor.criterio)}${card('Queda de tensão',`${data.queda_tensao.queda_percentual}%`,`${data.queda_tensao.queda_v} V · ${data.queda_tensao.formula}`)}${card('Evidência',data.rastreabilidade.fonte,`${data.rastreabilidade.edicao} · ${data.rastreabilidade.referencia}`)}</div>`; }
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



function clearHistory() {
  const list = document.querySelector('#project-history-list');
  list.replaceChildren();
  document.querySelector('#project-history-summary').textContent = '';
}
document.querySelector('#project-history-refresh').addEventListener('click', async () => {
  clearHistory();
  const status = document.querySelector('#project-history-status');
  const id = projectId.value.trim();
  if (!id) { status.textContent = 'Informe o ID do projeto para consultar as revisões.'; return; }
  const btn = document.querySelector('#project-history-refresh');
  btn.disabled = true;
  try {
    const headers = authHeaders();
    const response = await fetch(localProjectApi + '/' + encodeURIComponent(id) + '/revisoes', {headers});
    const data = await projectResponse(response);
    if (!Array.isArray(data.revisoes) || data.normative_conformity_verified !== false) {
      throw new Error('Resposta histórica inválida ou não segura');
    }
    const list = document.querySelector('#project-history-list');
    data.revisoes.forEach((rev) => {
      const item = document.createElement('li');
      const select = document.createElement('button');
      select.type = 'button';
      select.textContent = 'Revisão ' + String(rev.revisao) + ' — ' + String(rev.nome) + ' — detalhes';
      select.addEventListener('click', async () => {
        try {
          const result = await projectResponse(await fetch(
            localProjectApi + '/' + encodeURIComponent(id) + '/revisoes/' + encodeURIComponent(rev.revisao),
            {headers: authHeaders()}));
          if (result.normative_conformity_verified !== false || result.historico_recuperavel !== true) {
            throw new Error('Revisão histórica sem verificação de integridade');
          }
          const circuitos = Array.isArray(result.dados?.circuitos) ? result.dados.circuitos.length : 'não informado';
          document.querySelector('#project-history-summary').textContent =
            'Revisão ' + result.revisao + ' recuperada integralmente; circuitos: ' + circuitos +
            '; SHA-256: ' + String(result.hash_sha256 || 'indisponível') +
            '. Fonte normativa não homologada. Nenhum recálculo automático foi realizado.';
        } catch (error) {
          document.querySelector('#project-history-summary').textContent =
            'Falha ao consultar revisão: ' + error.message;
        }
      });
      item.appendChild(select);
      list.appendChild(item);
    });
    status.textContent = data.revisoes.length +
      ' revisões locais efetivamente gravadas; versões legadas sem registro não são reconstruídas.';
  } catch (error) {
    clearHistory();
    status.textContent = 'Não foi possível consultar revisões: ' + error.message;
  } finally {
    btn.disabled = false;
  }
});

// F01: painel consultivo de fontes. Usar apenas texto (sem HTML de dados externos).
// Ausência do endpoint jamais altera o gate da análise de circuitos.
async function loadNormativeCatalog() {
  const status = document.querySelector('#normas-status');
  const list = document.querySelector('#normas-lista');
  if (!status || !list) return;
  try {
    const response = await fetch(`${apiBase}/api/v1/normas/catalogo`);
    if (!response.ok) throw new Error('HTTP ' + response.status);
    const data = await response.json();
    if (data.release_allowed !== false || data.normative_conformity_verified !== false ||
        !Array.isArray(data.sources)) throw new Error('Resposta de governança inesperada');
    list.replaceChildren();
    data.sources.forEach((source) => {
      const item = document.createElement('li');
      item.textContent = String(source.document || source.id || 'Fonte desconhecida') +
        ' — ' + String(source.edition || 'edição pendente') +
        ' — NÃO VERIFICADA';
      list.appendChild(item);
    });
    status.textContent = data.sources.length +
      ' fontes cadastradas. Validação de conteúdo pendente; nenhuma fonte liberada.';
  } catch {
    list.replaceChildren();
    status.textContent = 'Catálogo indisponível. Verificação e liberação normativa não realizadas.';
  }
}
loadNormativeCatalog();
