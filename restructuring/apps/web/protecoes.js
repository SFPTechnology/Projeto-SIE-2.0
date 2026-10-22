'use strict';
const $=id=>document.getElementById(id);
let sequence=0,memory=null;
const states={PENDENTE:'Pendente',BLOQUEADO:'Bloqueado',REPROVADO:'Reprovado',NAO_ATENDE:'Não atende',NAO_APLICAVEL:'Não aplicável',ATENDE_ESTUDO:'Atende ao estudo',ATENDE_CALCULO_PARCIAL:'Atende ao cálculo parcial',CALCULADO_ESTUDO:'Calculado para estudo',PENDENTE_OU_FALHO:'Pendente ou falho',CONVERGED_STUDY:'Convergência no estudo computacional',EVALUATED_FINITE_SET:'Conjunto finito avaliado',ITERATION_LIMIT:'Limite de iterações atingido',NOT_REQUESTED:'Iteração não solicitada',PROPOSTA_ESTUDO:'Proposta de estudo',PENDENTE_OU_SEM_MELHORIA:'Pendente ou sem melhoria'};
function invalidate(){sequence++;memory=null;$('export').disabled=$('print').disabled=true;$('criteria').replaceChildren();$('balance-proposals').replaceChildren();$('pending').replaceChildren();for(const id of ['summary','memory','faults','balance','selection-summary','selection'])$(id).textContent='';$('status').textContent='Dados alterados. Analise novamente para gerar memória atual.';}
function apiBase(){const url=new URL($('api').value);if(!['http:','https:'].includes(url.protocol)||!['localhost','127.0.0.1','[::1]'].includes(url.hostname)||url.username||url.password)throw Error('Informe API local sem credenciais');return url;}
$('document').addEventListener('input',invalidate);$('api').addEventListener('input',()=>{invalidate();$('catalog-memory').textContent='';$('sources').replaceChildren();$('catalog-pairs').replaceChildren();});
$('demo').onclick=async()=>{invalidate();const captured=sequence;try{const response=await fetch('protecoes-demo.json');if(!response.ok)throw Error('Exemplo indisponível');const data=await response.json();if(captured===sequence)$('document').value=JSON.stringify(data,null,2);}catch(e){if(captured===sequence)$('status').textContent=e.message;}};
$('file').onchange=async()=>{invalidate();const captured=sequence;try{const file=$('file').files[0];if(file){const data=JSON.parse(await file.text());if(captured===sequence)$('document').value=JSON.stringify(data,null,2);}}catch(e){if(captured===sequence)$('status').textContent='Arquivo JSON inválido';}};
$('calculate').onclick=async()=>{invalidate();const captured=sequence,input=$('document').value;$('calculate').disabled=true;try{const payload=JSON.parse(input);const response=await fetch(new URL('/api/v1/protecoes/analisar',apiBase()),{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(payload)});const result=await response.json();if(!response.ok)throw Error('Dados incompatíveis: '+JSON.stringify(result.detail));if(captured!==sequence||input!==$('document').value)return;memory=result;for(const [cid,row]of Object.entries(result.circuits??{})){const name=payload.conductor_study.topology.installation.circuits.find(c=>c.id===cid)?.name??cid;for(const [criterion,check]of Object.entries(row.checks??row.criteria??{})){const tr=document.createElement('tr');for(const value of[name,criterion,states[check.status]??check.status,check.reason??check.motivo??'']){const td=document.createElement('td');td.textContent=value;tr.append(td);}$('criteria').append(tr);}}$('summary').textContent=(states[result.status]??result.status)+' • '+Object.keys(result.circuits??{}).length+' circuitos • confira os critérios e suas limitações';$('faults').textContent=JSON.stringify(result.faults??result.fault_scenarios??{},null,2);$('balance').textContent=JSON.stringify(result.boards??result.phase_balance??result.balance??{},null,2);renderProposals(result,payload);$('memory').textContent=JSON.stringify(result,null,2);$('status').textContent='Memória calculada. '+(states[result.status]??result.status)+' — sem homologação normativa.';$('export').disabled=$('print').disabled=false;}catch(e){if(captured===sequence)$('status').textContent=e.message;}finally{$('calculate').disabled=false;}};
$('export').onclick=()=>{if(!memory)return;const url=URL.createObjectURL(new Blob([JSON.stringify(memory,null,2)],{type:'application/json'}));const a=document.createElement('a');a.href=url;a.download='SIE_F08_memoria.json';a.click();URL.revokeObjectURL(url);};
$('print').onclick=()=>{if(memory)window.print();};

$('catalog').onclick=async()=>{const captured=sequence;try{const response=await fetch(new URL('/api/v1/protecoes/catalogo',apiBase()));if(!response.ok)throw Error('Catálogo indisponível');const data=await response.json();if(captured!==sequence)return;$('catalog-memory').textContent=JSON.stringify(data,null,2);renderPairs(data);$('sources').replaceChildren();for(const source of [...(data.sources??[]),...(data.coordination_catalog?.source?[data.coordination_catalog.source]:[])]){const url=new URL(source.url);if(url.protocol!=='https:'||!['www.se.com','ckm-content.se.com','download.schneider-electric.com'].includes(url.hostname)||url.username||url.password)continue;const p=document.createElement('p'),a=document.createElement('a');a.href=url.href;a.target='_blank';a.rel='noopener noreferrer';a.textContent=source.reference??source.document??source.id;p.append(a);$('sources').append(p);}}catch(e){if(captured===sequence)$('status').textContent=e.message;}};

function circuitName(payload,id){return payload.conductor_study.topology.installation.circuits.find(c=>c.id===id)?.name??id;}
function paragraph(container,text){const p=document.createElement('p');p.textContent=text;container.append(p);}
function renderProposals(result,payload){
 for(const board of result.boards??[]){
  const section=document.createElement('div');
  const name=payload.conductor_study.topology.installation.boards.find(b=>b.id===board.board_id)?.name??board.board_id;
  const proposal=board.proposal;
  paragraph(section,name+' • '+(states[board.balance_status]??board.balance_status));
  if(proposal){
   paragraph(section,(states[proposal.status]??proposal.status)+' • Proposta não aplicada • Recálculo completo necessário');
   if(proposal.phase_currents_a)paragraph(section,'Correntes propostas: '+Object.entries(proposal.phase_currents_a).map(([phase,value])=>phase+': '+value+' A').join(' · ')+' • Diferença: '+proposal.spread_a+' A');
   for(const item of proposal.assignments??[])paragraph(section,circuitName(payload,item.circuit_id)+': '+item.current_phase_set+' → '+item.proposed_phase_set);
  }else paragraph(section,'Proposta de redistribuição não disponível neste estudo.');
  $('balance-proposals').append(section);
 }
 const variants=result.selection?.variants;
 $('selection-summary').textContent='Cálculo: '+(states[result.computational_state]??result.computational_state??'Pendente')+' • '+(states[variants?.status]??variants?.status??'Iteração não solicitada')+' • Resultado global: '+(states[result.status]??result.status)+' • Alterações não aplicadas. Sem homologação normativa.';
 $('selection').textContent=JSON.stringify(result.selection??{},null,2);
 for(const text of result.mandatory_pending??[]){const li=document.createElement('li');li.textContent=text;$('pending').append(li);}
}
function renderPairs(data){
 $('catalog-pairs').replaceChildren();
 const pairs=data.coordination_catalog?.pairs??data.coordination_pairs??data.selectivity_pairs??[];
 if(!pairs.length){paragraph($('catalog-pairs'),'Nenhum par de seletividade vinculado neste catálogo. A relação entre correntes nominais não comprova coordenação.');return;}
 for(const pair of pairs){const up=pair.upstream??{},down=pair.downstream??{};paragraph($('catalog-pairs'),(up.manufacturer??'')+' '+(up.model??'')+' '+(up.curve??'')+(up.nominal_current_a??'')+' A montante → '+(down.model??'')+' '+(down.curve??'')+(down.nominal_current_a??'')+' A jusante • '+pair.voltage_v+' V • Limite de seletividade parcial: '+pair.selectivity_limit_a+' A. Não equivale à homologação da instalação.');}
}
