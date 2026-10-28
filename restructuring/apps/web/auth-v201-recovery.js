/* Recovery callback DEV only. No JWT saved; URL fragment removed on arrival. */
const cfg=window.SIE_V201_PUBLIC_CONFIG||{};
const status=document.getElementById("status");
const form=document.getElementById("reset");
const url="https://fozrymsidnaxmuvxxfhh.supabase.co";
const allowed=new Set(["http://localhost:5173","http://127.0.0.1:5173"]);
const incoming=new URLSearchParams(location.hash.replace(/^#/,""));
const token=incoming.get("access_token");
const kind=incoming.get("type");
history.replaceState(null,"",location.pathname);
let active=null;
function notify(value){status.textContent=value}
function guard(){
  if(!allowed.has(location.origin) || cfg.supabaseUrl!==url ||
     !cfg.publishableKey || typeof cfg.publishableKey!=="string" ||
     cfg.publishableKey.startsWith("sb_secret_")){
    throw Error("Configuração de recuperação não autorizada");
  }
  if(typeof token!=="string" || token.length<20 || kind!=="recovery"){
    throw Error("Link inválido ou não suportado; solicite um novo convite");
  }
}
async function verify(){
  guard();
  const r=await fetch(url+"/auth/v1/user",{cache:"no-store",credentials:"omit",
    headers:{"apikey":cfg.publishableKey,"authorization":"Bearer "+token}});
  if(!r.ok)throw Error("Sessão de recuperação inválida");
  const data=await r.json();
  if(!data?.id || data.is_anonymous===true)throw Error("Identidade não permitida");
  active=token;
  notify("Convite confirmado. Defina uma nova senha.");
}
form.addEventListener("submit",async event=>{
  event.preventDefault();
  if(!active){notify("Recuperação não autorizada.");return;}
  const password=document.getElementById("new-password").value;
  if(typeof password!=="string" || password.length<12){
    notify("Use uma senha com pelo menos 12 caracteres.");return;
  }
  const button=document.getElementById("save");button.disabled=true;
  try{
    const r=await fetch(url+"/auth/v1/user",{
      method:"PUT",cache:"no-store",credentials:"omit",
      headers:{"apikey":cfg.publishableKey,"authorization":"Bearer "+active,
        "content-type":"application/json"},
      body:JSON.stringify({password})});
    if(!r.ok)throw Error("Update rejected");
    // Force fresh login; revoked access tokens may still live until expiry.
    active=null;document.getElementById("new-password").value="";
    form.hidden=true;notify("Senha atualizada. Faça login novamente na página DEV.");
  }catch(_e){notify("Não foi possível alterar a senha. Solicite outro link ou confira o provedor.");}
  finally{button.disabled=false;}
});
verify().catch(error=>{active=null;form.hidden=true;notify(error.message);});
