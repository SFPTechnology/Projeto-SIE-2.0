const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../../web/auth-v201.js'), 'utf8');
const elements = new Map();
let calls = 0;
const document = {hidden:false, addEventListener(){}, getElementById(id){
  if(!elements.has(id)) elements.set(id, {hidden:id==='signed-in', value:'', textContent:'', addEventListener(){}});
  return elements.get(id);
}};
const ctx = vm.createContext({
  document, location:{origin:'http://127.0.0.1:5173'},
  window:{SIE_V201_PUBLIC_CONFIG:{supabaseUrl:'https://fozrymsidnaxmuvxxfhh.supabase.co', publishableKey:'sb_publishable_fixture', apiBase:'http://127.0.0.1:8000'}},
  setTimeout(){return 1}, clearTimeout(){}, fetch:async()=>{calls++; throw Error('network must remain unused')}
});
vm.runInContext(source,ctx);
(async()=>{
  await assert.rejects(ctx.signIn('fixture@example.invalid','synthetic'),/SYNTHETIC_ONLY/);
  assert.equal(calls,0);
  assert.match(elements.get('status').textContent,/SYNTHETIC_ONLY/);
  console.log('PASS: default Auth configuration blocks every remote call');
})().catch(error=>{console.error(error);process.exitCode=1});
