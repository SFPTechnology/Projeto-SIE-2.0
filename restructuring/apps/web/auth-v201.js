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
let refreshToken=null;
let authEmail=null;
let verifiedUserId=null;
let expiresAt=0;
let renewalTimer=null;
let renewalInFlight=null;
let sessionGeneration=0;
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
  sessionGeneration++;
  if(renewalTimer!==null)clearTimeout(renewalTimer);
  renewalTimer=null;
  accessToken=null;refreshToken=null;expiresAt=0;verifiedUserId=null;authEmail=null;
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
  if(typeof result.refresh_token!=="string" || !result.refresh_token ||
     !Number.isFinite(Number(result.expires_in)) || Number(result.expires_in)<=0)
    throw Error("Sessão incompleta; renovação indisponível");
  sessionGeneration++;
  accessToken=token;refreshToken=result.refresh_token;
  authEmail=email;verifiedUserId=verified.user_id;
  expiresAt=Date.now()+Number(result.expires_in)*1000;
  showSigned(verified.user_id);
  scheduleRenewal();
  message("Sessão validada. Acesso remoto de escrita continua desabilitado.");
}

// The refresh token is volatile; it is never persisted or transmitted to our
// API. Supabase Auth handles refresh-token rotation. The API verifies the new
// access token before the browser can consider it authenticated.
function scheduleRenewal(){
  if(renewalTimer!==null)clearTimeout(renewalTimer);
  renewalTimer=null;
  if(!refreshToken || !accessToken)return;
  const delay=Math.min(2147483647,Math.max(1000,expiresAt-Date.now()-60000));
  renewalTimer=setTimeout(()=>{
    renewSession().catch(()=>{
      showSignedOut();message("Sessão expirada ou revogada; entre novamente.");
    });
  },delay);
}
async function renewSession(){
  if(renewalInFlight)return renewalInFlight;
  if(!refreshToken || !accessToken)throw Error("Sessão ausente");
  const generation=sessionGeneration;
  const previousIdentity=verifiedUserId;
  renewalInFlight=(async()=>{
    try{
      const data=await request(authOrigin+"/auth/v1/token?grant_type=refresh_token",{
        method:"POST",headers:publicHeaders(),
        body:JSON.stringify({refresh_token:refreshToken})
      });
      if(!data || typeof data.access_token!=="string" ||
         typeof data.refresh_token!=="string" ||
         !Number.isFinite(Number(data.expires_in)) || Number(data.expires_in)<=0)
        throw Error("Refresh data rejected");
      const verified=await request(cfg.apiBase+"/api/v2/sie/auth/me",{
        headers:{"Authorization":"Bearer "+data.access_token}
      });
      if(verified.authorization_source!=="auth_server_verified" ||
         verified.user_id!==previousIdentity || generation!==sessionGeneration)
        throw Error("Identity/session changed during refresh");
      accessToken=data.access_token;
      refreshToken=data.refresh_token;
      expiresAt=Date.now()+Number(data.expires_in)*1000;
      scheduleRenewal();
      message("Sessão renovada e identidade confirmada.");
      return true;
    }catch(error){
      if(generation===sessionGeneration){
        showSignedOut();
        if(channel)channel.postMessage("logout");
      }
      throw error;
    }finally{renewalInFlight=null}
  })();
  return renewalInFlight;
}
document.getElementById("refresh").addEventListener("click",()=>{
  renewSession().catch(()=>message("Sessão não renovada; entre novamente."));
});
document.addEventListener("visibilitychange",()=>{
  if(!document.hidden && accessToken && expiresAt-Date.now()<60000){
    renewSession().catch(()=>message("Sessão expirada; entre novamente."));
  }
});

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
