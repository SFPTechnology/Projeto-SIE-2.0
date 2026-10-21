'use strict';
const $=id=>document.getElementById(id);
let doc=null, baseline=null, revision=0, busy=false;
const clone=x=>JSON.parse(JSON.stringify(x));
function status(s){$('status').textContent=s;}
function option(select,id,name){const o=document.createElement('option');o.value=id;o.textContent=name;select.append(o);}
function choices(id,rows,blank=false){$(id).replaceChildren();if(blank)option($(id),'','Sem destino');for(const row of rows)option($(id),row.id,row.name+' · '+row.id.slice(-4));}
function render(){if(!doc)return;const i=doc.installation;$('project').value=i.project.id;$('revision').textContent=`Revisão persistida: ${revision}. Rascunho exige validação.`;$('json').value=JSON.stringify(doc,null,2);choices('circuit',i.circuits);choices('board',i.boards);choices('downstream',i.boards,true);choices('device',i.devices);choices('segment',i.segments);circuit();segment();$('result').replaceChildren();}
function circuit(){if(!doc)return;const i=doc.installation,c=i.circuits.find(x=>x.id===$('circuit').value);if(!c)return;$('board').value=c.board_id;$('device').value=c.device_id;$('downstream').value=c.downstream_board_id||'';$('downstream').disabled=c.kind!=='FEEDER';$('loads').replaceChildren();for(const load of i.loads){const l=document.createElement('label'),input=document.createElement('input');input.type='checkbox';input.value=load.id;input.checked=c.load_ids.includes(load.id);input.disabled=c.kind!=='TERMINAL';l.append(input,document.createTextNode(load.name));$('loads').append(l);}}
function segment(){if(!doc)return;const s=doc.installation.segments.find(x=>x.id===$('segment').value);if(!s)return;$('length').value=s.length.value;$('method').value=s.conditions.installation_method;$('temperature').value=s.conditions.ambient_temperature.value;$('group').value=s.conditions.grouped_circuits;}
function load(raw,rev=0){doc=clone(raw);baseline=clone(raw);revision=rev;render();status('Documento aberto; valide os vínculos e a origem dos dados.');}
function url(path){const u=new URL($('api').value);if(!['http:','https:'].includes(u.protocol))throw Error('URL HTTP/HTTPS obrigatória');return u.origin+path;}
async function request(path,method='GET',body,auth=false){const headers={};if(body)headers['Content-Type']='application/json';if(auth)headers.Authorization='Bearer '+$('token').value;const r=await fetch(url(path),{method,headers,body:body?JSON.stringify(body):undefined});const data=await r.json();if(!r.ok)throw Error(`${r.status}: ${JSON.stringify(data.detail||data)}`);return data;}
function textNode(tag,text){const n=document.createElement(tag);n.textContent=text;return n;}
function focusSegment(id){if(doc.installation.segments.some(s=>s.id===id)){$('segment').value=id;segment();$('segment').focus();$('segment').scrollIntoView({block:'center',behavior:'smooth'});}}
function results(r){
 $('result').replaceChildren();
 $('result').append(textNode('h3',r.valid?'Conectividade válida':'Erros de integridade'));
 for(const error of r.errors||[]){const message=textNode('p',error.location.join(' → ')+': '+error.message);message.style.color='#ffb19f';$('result').append(message);const loc=error.location;if(loc[0]==='installation'&&loc[1]==='segments'&&typeof loc[2]==='number'){const b=textNode('button','Revisar trecho afetado');b.onclick=()=>focusSegment(doc.installation.segments[loc[2]].id);$('result').append(b);}}
 for(const warning of r.warnings||[]){const row=textNode('p',warning.message+' · '+warning.id);if(doc.installation.segments.some(s=>s.id===warning.id)){const b=textNode('button','Abrir trecho');b.onclick=()=>focusSegment(warning.id);row.append(b);}$('result').append(row);}
 const name=(rows,id)=>rows.find(x=>x.id===id)?.name||id;
 for(const path of r.paths||[]){const article=document.createElement('article');article.append(textNode('h3',name(doc.installation.loads,path.load_id)+' · '+(path.length_m===null?'Comprimento ambíguo':path.length_m+' m')));article.append(textNode('p',name(doc.installation.supplies,path.source_id)+' → '+path.board_ids.map(id=>name(doc.installation.boards,id)).join(' → ')+' → '+name(doc.installation.loads,path.load_id)));
  for(const leg of path.legs){article.append(textNode('h4',(leg.kind==='FEEDER'?'Alimentador: ':'Circuito final: ')+leg.name));for(const run of leg.runs){article.append(textNode('p','Percurso '+run.id+' · '+run.length_m+' m'));const list=document.createElement('ul');for(const seg of run.segments){const li=textNode('li',seg.name+' · '+seg.length.value+' m · '+seg.conditions.installation_method+' · '+seg.conditions.ambient_temperature.value+' °C · agrupamento '+seg.conditions.grouped_circuits);const b=textNode('button','Editar trecho');b.onclick=()=>focusSegment(seg.id);li.append(b);list.append(li);}article.append(list);}}$('result').append(article);
 }
 const detail=document.createElement('details');detail.append(textNode('summary','Relatório técnico completo e UUIDs'));detail.append(textNode('pre',JSON.stringify(r,null,2)));$('result').append(detail);
 status(r.valid?'Integridade válida; confira os avisos e os trechos.':'Vínculos inválidos: confira erros, UUID e trecho no relatório.');
}
async function validate(){if(!doc)throw Error('Abra um documento');const r=await request('/api/v1/topologia/validar','POST',doc);results(r);return r.valid;}
async function reopen(){const item=await request('/api/v1/local/projetos/'+encodeURIComponent($('project').value)+'/topologia','GET',null,true);load(item.document,item.revision);status('Reaberto. Resultados desatualizados: '+item.results_stale);}
function action(id,fn){$(id).onclick=async()=>{if(busy)return;busy=true;document.querySelectorAll('button').forEach(b=>b.disabled=true);try{await fn();}catch(e){status(e.message);}finally{busy=false;document.querySelectorAll('button').forEach(b=>b.disabled=false);}};}
action('demo',async()=>{const r=await fetch('topologia-demo.json');load(await r.json());await validate();});
action('open',reopen);
$('file').onchange=async e=>{if(busy){status('Aguarde a operação em andamento.');return;}try{load(JSON.parse(await e.target.files[0].text()));await validate();}catch(err){status(err.message);}};
action('apply',async()=>{doc=JSON.parse($('json').value);render();await validate();});
action('link',async()=>{if(!doc)throw Error('Abra um documento');const c=doc.installation.circuits.find(x=>x.id===$('circuit').value);c.board_id=$('board').value;c.device_id=$('device').value;c.downstream_board_id=c.kind==='FEEDER'?$('downstream').value:null;c.load_ids=c.kind==='TERMINAL'?[...$('loads input:checked')].map(x=>x.value):[];$('json').value=JSON.stringify(doc,null,2);await validate();});
action('edit',async()=>{if(!doc)throw Error('Abra um documento');const s=doc.installation.segments.find(x=>x.id===$('segment').value);s.length.value=$('length').value;s.conditions.installation_method=$('method').value;s.conditions.ambient_temperature.value=$('temperature').value;s.conditions.grouped_circuits=Number($('group').value);$('json').value=JSON.stringify(doc,null,2);await validate();});
action('undo',()=>{if(!baseline)throw Error('Abra um documento');doc=clone(baseline);render();status('Rascunho desfeito.');});
action('validate',validate);
action('save',async()=>{if(!await validate())return;const copy=clone(doc);copy.installation.project.revision=revision+1;await request('/api/v1/local/projetos/'+copy.installation.project.id+'/topologia','PUT',{document:copy,expected_revision:revision},true);await reopen();await validate();status('Nova revisão salva. Resultados dependentes devem ser recalculados.');});
action('export',()=>{if(!doc)throw Error('Abra um documento');const link=document.createElement('a');link.href=URL.createObjectURL(new Blob([JSON.stringify(doc,null,2)],{type:'application/json'}));link.download='topologia.json';link.click();URL.revokeObjectURL(link.href);});
$('circuit').onchange=circuit;$('segment').onchange=segment;
