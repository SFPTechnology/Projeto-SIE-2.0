'use strict';
const $ = id => document.getElementById(id);
const criteriaNames={capacity:'Capacidade de corrente',minimum_phase:'Seção mínima da fase',neutral:'Neutro',pe:'Condutor de proteção (PE)',voltage:'Queda de tensão'};
const stateNames={ATENDE_LOTE_LIMITADO:'Atende ao lote limitado',ATENDE_ESTUDO:'Atende ao estudo',CALCULADO_ESTUDO:'Calculado para estudo',REPROVADO:'Reprovado',PENDENTE:'Pendente',BLOQUEADO:'Bloqueado',NAO_APLICAVEL:'Não aplicável',ATENDE_FONTE_VINCULADA:'Atende à fonte vinculada',SELECTED_SOURCE_LINKED:'Proposta selecionada com fonte vinculada',NO_SOLUTION_IN_CATALOG:'Nenhuma solução no catálogo',CALCULATED_SOURCE_LINKED:'Calculado com fonte vinculada'};
const displayPercent=value=>value==null?'—':Number(value).toLocaleString('pt-BR',{maximumFractionDigits:4});
let memory = null;
let sequence = 0;
function invalidate() {sequence++; memory = null; $('export').disabled = $('print').disabled = true; $('criteria').replaceChildren(); $('paths').replaceChildren(); $('memory').textContent = ''; $('summary').textContent = ''; $('selected').replaceChildren(); $('status').textContent = 'Dados alterados. Analise novamente para gerar memória atual.';}
$('document').addEventListener('input', invalidate);
$('api').addEventListener('input',()=>{invalidate();$('catalog-memory').textContent='';});
async function loadDemo(file) {invalidate();const captured=sequence;try {const r=await fetch(file);if(!r.ok)throw Error('Exemplo indisponível');const data=await r.json();if(captured===sequence)$('document').value=JSON.stringify(data,null,2);}catch(e){if(captured===sequence)$('status').textContent=e.message;}}
$('demo').onclick=()=>loadDemo('condutores-demo.json');
$('source-demo').onclick=()=>loadDemo('condutores-selecao-demo.json');
function apiBase(){const base=new URL($('api').value);if(!['http:','https:'].includes(base.protocol)||!['localhost','127.0.0.1','[::1]'].includes(base.hostname)||base.username||base.password)throw Error('Informe API local sem credenciais');return base;}
$('catalog').onclick=async()=>{const captured=sequence;try{const r=await fetch(new URL('/api/v1/condutores/catalogo',apiBase()));if(!r.ok)throw Error('Catálogo indisponível');const data=await r.json();if(captured===sequence)$('catalog-memory').textContent=JSON.stringify(data,null,2);}catch(e){if(captured===sequence)$('status').textContent=e.message;}};
$('file').onchange=async()=>{invalidate();const captured=sequence;try{const f=$('file').files[0];if(f){const data=JSON.parse(await f.text());if(captured===sequence)$('document').value=JSON.stringify(data,null,2);}}catch(e){if(captured===sequence)$('status').textContent='Arquivo JSON inválido';}};
$('calculate').onclick = async () => {
 invalidate(); $('calculate').disabled=true;
 const input=$('document').value; const requestSequence=sequence;
 try {
  const base=apiBase();const payload=JSON.parse(input);const isSelection=payload.schema_version==='SIE_F07_SELECTION_V1';
  const response=await fetch(new URL(isSelection?'/api/v1/condutores/selecionar':'/api/v1/condutores/analisar',base),{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});
  const result=await response.json(); if(!response.ok) throw Error('Dados incompatíveis: '+JSON.stringify(result.detail));
  if(input!==$('document').value || requestSequence!==sequence) return;
  memory=result;const analysis=isSelection?result.memory:result;
  for(const row of analysis?.segments??[]) for(const [name,check] of Object.entries(row.criteria)) {
   const tr=document.createElement('tr');
   for(const value of [(analysis.input_snapshot.topology.installation.segments.find(s=>s.id===row.segment_id)?.name??row.segment_id)+' / '+row.section_mm2+' mm²',criteriaNames[name]??name,stateNames[check.status]??check.status,check.reason]) {const td=document.createElement('td');td.textContent=value;tr.append(td);}
   $('criteria').append(tr);
  }
  for(const [id,row] of Object.entries(analysis?.circuits??{})) {const p=document.createElement('p');p.textContent=(analysis.input_snapshot.topology.installation.circuits.find(c=>c.id===id)?.name??id)+': '+(stateNames[row.voltage_total.status]??row.voltage_total.status)+' · '+displayPercent(row.voltage_total.total_percent)+' % (apresentação) · '+row.voltage_total.reason;$('paths').append(p);}
  const chosen=result.selected_sections_by_circuit;
  for(const [id,sections] of Object.entries(chosen??{})){const p=document.createElement('p');const name=payload.topology.installation.circuits.find(c=>c.id===id)?.name??id;p.textContent=name+': fase '+sections.phase_mm2+' mm² · neutro '+(sections.neutral_mm2??'não aplicável')+(sections.neutral_mm2?' mm²':'')+' · PE '+sections.pe_mm2+' mm²';$('selected').append(p);}
  if(isSelection&&!chosen){const p=document.createElement('p');p.textContent=(result.problems??[]).map(x=>x.message??x.reason??x.criterion).join(' · ');$('selected').append(p);}
  $('summary').textContent=(analysis?.segments?.length??0)+' trechos • '+(isSelection?(stateNames[result.status]??result.status):result.status)+(isSelection?' • Catálogo finito e condições conferidas por critério':' • Seleção comercial não liberada no estudo livre');
  $('memory').textContent=JSON.stringify(result,null,2); $('status').textContent='Memória calculada. '+(isSelection?(stateNames[result.status]??result.status):result.status)+' — confira fontes e pendências. Sem homologação normativa.';
  $('export').disabled=$('print').disabled=false;
 } catch(e) {if(requestSequence===sequence) $('status').textContent=e.message;} finally {$('calculate').disabled=false;}
};
$('export').onclick=()=>{if(!memory)return;const url=URL.createObjectURL(new Blob([JSON.stringify(memory,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='SIE_F07_memoria.json';a.click();URL.revokeObjectURL(url);};
$('print').onclick=()=>{if(memory) window.print();};
