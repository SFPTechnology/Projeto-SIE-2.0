/* B01: native-browser DEV sign-in. No tokens/cookies stored by this page.
 * The backend's /api/v2/sie/auth/me performs the actual Auth check.
 * This screen does not enable B04/B05 remote writes.
 */
const cfg=window.SIE_V201_PUBLIC_CONFIG || {};
const statusEl=document.getElementById("status");
const form=document.getElementById("login-form");
const signed=document.getElementById("signed-in");
const userEl=document.getElementById("session-user");
let accessToken=null;
let authEmail=null;
const channel=typeof BroadcastChannel!=="undefined" ? new BroadcastChannel("sie2-b01-logout") : null;
const authOrigin="https://fozrymsidnaxmuvxxfhh.supabase.co";
const originAllowed=new Set(["http://localhost:5173","http://127.0.0.1:5173"]);
const apiAllowed=new Set(["http://localhost:8000","http://127.0.0.1:8000"]);
const isDevelopment=originAllowed.has(location.origin);

function message(text){statusEl.textContent=text}
function configure(){
  if(!isDevelopment) throw Error("Tela disponível somente em localhost:5173");
  if(cfg.supabaseUrl!==authOrigin) throw Error("Projeto Supabase não autorizado");
  if(!apiAllowed.has(cfg.apiBase)) throw Error("Host API não é loopback autorizado");
  if(typeof cfg.publishableKey!=="string" || !cfg.publishableKey ||
     cfg.publishableKey.length>2048 || cfg.publishableKey.startsWith("sb_secret_"))
    throw Error("Informe somente uma chave pública de desenvolvimento");
}
function showSigned(userId){
  form.hidden=true;signed.hidden=false;
  userEl.textContent="Identidade verificada: "+userId;
}
function showSignedOut(){
  accessToken=null;authEmail=null;
  form.hidden=false;signed.hidden=true;userEl.textContent="";
  document.getElementById("password").value="";
}
function publicHeaders(){
  return {"apikey":cfg.publishableKey,"content-type":"application/json"};
}
async function request(url,options){
  const response=await fetch(url,{cache:"no-store",credentials:"omit",...options});
  if(!response.ok) throw Error("Operação rejeitada pelo serviço de autenticação");
  const data=await response.json();
  return data;
}
async function signIn(email,password){
  configure();
  const result=await request(authOrigin+"/auth/v1/token?grant_type=password",{
    method:"POST",headers:publicHeaders(),body:JSON.stringify({email,password})
  });
  const token=result?.access_token;
  if(typeof token!=="string" || token.length<20)
    throw Error("Sessão não emitida");
  const verified=await request(cfg.apiBase+"/api/v2/sie/auth/me",{
    method:"GET",headers:{"Authorization":"Bearer "+token},
  });
  if(typeof verified.user_id!=="string" || verified.authorization_source!=="auth_server_verified")
    throw Error("A API não confirmou a identidade");
  accessToken=token;authEmail=email;
  showSigned(verified.user_id);
  message("Sessão validada. Acesso remoto de escrita continua desabilitado.");
}
form.addEventListener("submit",async e=>{
  e.preventDefault();
  const btn=document.getElementById("login");
  btn.disabled=true;message("Validando credenciais...");
  try {
    const data=new FormData(form);
    await signIn(String(data.get("email")),String(data.get("password")));
  } catch(_error){
    showSignedOut();
    message("Não foi possível autenticar. Verifique a configuração, o usuário e a API.");
  } finally{btn.disabled=false}
});
document.getElementById("recover").addEventListener("click",async()=>{
  const email=document.getElementById("email").value.trim();
  if(!email || !document.getElementById("email").checkValidity()){
    message("Informe um e-mail válido para recuperação.");return;
  }
  try{
    configure();
    // Must also exist in the project's approved Auth redirect allowlist.
    const redirect=location.origin+"/auth/callback";
    const response=await fetch(authOrigin+"/auth/v1/recover?redirect_to="+encodeURIComponent(redirect),{
      method:"POST",headers:publicHeaders(),
      credentials:"omit",body:JSON.stringify({email}),cache:"no-store"
    });
    if(!response.ok) throw Error("recover failed");
    message("Se a conta existir e o provedor estiver configurado, o fluxo de recuperação será enviado.");
  }catch(_error){message("Recuperação indisponível. Verifique a configuração de redirects do Auth.")}
});
async function signOut(broadcast=true){
  const token=accessToken;showSignedOut();
  if(broadcast && channel)channel.postMessage("logout");
  if(!token){message("Sessão local encerrada.");return;}
  try{
    await fetch(authOrigin+"/auth/v1/logout?scope=local",{
      method:"POST",credentials:"omit",headers:{
        "apikey":cfg.publishableKey,"Authorization":"Bearer "+token}
    });
    message("Sessão local encerrada. Tokens anteriores podem valer até expirar.");
  }catch(_error){
    message("Sessão local limpa, mas não foi possível confirmar revogação remota.");
  }
}
document.getElementById("logout").addEventListener("click",()=>signOut());
if(channel)channel.onmessage=e=>{
  if(e.data==="logout"){showSignedOut();message("Sessão encerrada em outra guia.");}
};
try{configure();message("Configuração pública pronta; utilize apenas conta de teste autorizada.");}
catch(err){message(err.message)}
