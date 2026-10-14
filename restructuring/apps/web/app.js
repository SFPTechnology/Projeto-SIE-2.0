const apiBase = localStorage.getItem('sie.apiBase') || 'http://127.0.0.1:8000';
const health = document.querySelector('#health');
const result = document.querySelector('#resultado');

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
  try { const response = await fetch(`${apiBase}/api/v1/circuitos/analisar`, {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)}); const data = await response.json(); if(!response.ok) throw new Error(data.detail || 'Falha ao analisar'); const approved=data.liberado_para_uso_normativo; result.innerHTML=`<div class="section-heading"><div><p class="eyebrow">02 · RESULTADO</p><h2>Decisão técnica</h2></div><span class="tag ${approved?'':'muted'}">${escapeHTML(data.status_engenharia)}</span></div><div class="result-status ${approved?'approved':'pending'}">${approved?'Gate normativo aprovado.':'Gate normativo não aprovado.'} ${escapeHTML(data.aviso||'')}</div><div class="result-cards">${card('Condutor selecionado',`${data.condutor.secao_mm2} mm²`,`${data.condutor.capacidade_corrigida_a} A · ${data.condutor.criterio}`)}${card('Disjuntor comercial',`${data.disjuntor.corrente_a} A`,data.disjuntor.criterio)}${card('Queda de tensão',`${data.queda_tensao.queda_percentual}%`,`${data.queda_tensao.queda_v} V · ${data.queda_tensao.formula}`)}${card('Evidência',data.rastreabilidade.fonte,`${data.rastreabilidade.edicao} · ${data.rastreabilidade.referencia}`)}</div>`; }
  catch (error) { result.innerHTML=`<div class="section-heading"><div><p class="eyebrow">02 · RESULTADO</p><h2>Decisão técnica</h2></div></div><div class="result-status pending">Não foi possível concluir: ${escapeHTML(error.message)}</div>`; }
  finally { submit.disabled=false; submit.innerHTML='Executar análise <span>→</span>'; }
});
checkHealth();
