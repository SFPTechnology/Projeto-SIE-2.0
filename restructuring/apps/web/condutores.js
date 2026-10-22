'use strict';
const $ = id => document.getElementById(id);
const criteriaNames={capacity:'Capacidade de corrente',minimum_phase:'Seção mínima da fase',neutral:'Neutro',pe:'Condutor de proteção (PE)',voltage:'Queda de tensão'};
const stateNames={ATENDE_LOTE_LIMITADO:'Atende ao lote limitado',ATENDE_ESTUDO:'Atende ao estudo',CALCULADO_ESTUDO:'Calculado para estudo',REPROVADO:'Reprovado',PENDENTE:'Pendente',BLOQUEADO:'Bloqueado',NAO_APLICAVEL:'Não aplicável'};
const displayPercent=value=>value==null?'—':Number(value).toLocaleString('pt-BR',{maximumFractionDigits:4});
let memory = null;
let sequence = 0;
function invalidate() {sequence++; memory = null; $('export').disabled = $('print').disabled = true; $('criteria').replaceChildren(); $('paths').replaceChildren(); $('memory').textContent = ''; $('summary').textContent = ''; $('status').textContent = 'Dados alterados. Analise novamente para gerar memória atual.';}
$('document').addEventListener('input', invalidate);
$('api').addEventListener('input', invalidate);
$('demo').onclick = async () => {try {const r = await fetch('condutores-demo.json'); if (!r.ok) throw Error('Exemplo indisponível'); $('document').value = JSON.stringify(await r.json(), null, 2); invalidate();} catch(e) {$('status').textContent=e.message;}};
$('file').onchange = async () => {invalidate(); try {const f=$('file').files[0]; if(f) $('document').value=JSON.stringify(JSON.parse(await f.text()),null,2);} catch(e) {$('status').textContent='Arquivo JSON inválido';}};
$('calculate').onclick = async () => {
 invalidate(); $('calculate').disabled=true;
 const input=$('document').value; const requestSequence=sequence;
 try {
  const base=new URL($('api').value);
  if(!['http:','https:'].includes(base.protocol) || !['localhost','127.0.0.1','[::1]'].includes(base.hostname) || base.username || base.password) throw Error('Informe API local sem credenciais');
  const response=await fetch(new URL('/api/v1/condutores/analisar',base),{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(JSON.parse(input))});
  const result=await response.json(); if(!response.ok) throw Error('Dados incompatíveis: '+JSON.stringify(result.detail));
  if(input!==$('document').value || requestSequence!==sequence) return;
  memory=result;
  for(const row of result.segments) for(const [name,check] of Object.entries(row.criteria)) {
   const tr=document.createElement('tr');
   for(const value of [(result.input_snapshot.topology.installation.segments.find(s=>s.id===row.segment_id)?.name??row.segment_id)+' / '+row.section_mm2+' mm²',criteriaNames[name]??name,stateNames[check.status]??check.status,check.reason]) {const td=document.createElement('td');td.textContent=value;tr.append(td);}
   $('criteria').append(tr);
  }
  for(const [id,row] of Object.entries(result.circuits)) {const p=document.createElement('p');p.textContent=(result.input_snapshot.topology.installation.circuits.find(c=>c.id===id)?.name??id)+': '+(stateNames[row.voltage_total.status]??row.voltage_total.status)+' · '+displayPercent(row.voltage_total.total_percent)+' % (apresentação) · '+row.voltage_total.reason;$('paths').append(p);}
  $('summary').textContent=result.segments.length+' trechos • '+result.status+' • Seleção comercial não liberada';
  $('memory').textContent=JSON.stringify(result,null,2); $('status').textContent='Memória calculada. '+result.status+' — confira fontes e pendências. Sem homologação normativa.';
  $('export').disabled=$('print').disabled=false;
 } catch(e) {if(requestSequence===sequence) $('status').textContent=e.message;} finally {$('calculate').disabled=false;}
};
$('export').onclick=()=>{if(!memory)return;const url=URL.createObjectURL(new Blob([JSON.stringify(memory,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='SIE_F07_memoria.json';a.click();URL.revokeObjectURL(url);};
$('print').onclick=()=>{if(memory) window.print();};
