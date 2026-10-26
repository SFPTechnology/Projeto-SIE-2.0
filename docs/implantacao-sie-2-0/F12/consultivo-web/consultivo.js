"use strict";
// Stateless and same-origin by design; no token, localStorage, cookie or persistent project.
const $ = (id) => document.getElementById(id);
const form = $("form");
const result = $("results");
const state = $("state");
const submit = $("execute");
const fmt = (value) => String(value ?? "Pendente");

async function json(path, options = {}) {
  const response = await fetch(path, {cache: "no-store", credentials: "omit", ...options});
  const body = await response.json();
  if (!response.ok) throw new Error("Requisição recusada (" + response.status + ")");
  return body;
}
function add(label, value) {
  const group = document.createElement("div");
  const key = document.createElement("dt");
  const display = document.createElement("dd");
  key.textContent = label;
  display.textContent = fmt(value);
  group.append(key, display);
  result.append(group);
}
async function health() {
  try {
    const info = await json("/api/v1/health");
    $("api").textContent = info.status === "ok"
      ? "Motor consultivo acessível · versão " + info.version
      : "Saúde do serviço não confirmada";
  } catch {
    $("api").textContent = "Serviço não disponível; nenhuma análise pode ser efetuada.";
  }
}
form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const fields = new FormData(form);
  const payload = {
    corrente_a: Number(fields.get("corrente_a")),
    comprimento_m: Number(fields.get("comprimento_m")),
    tensao_v: Number(fields.get("tensao_v")),
    resistencia_ohm_km: Number(fields.get("resistencia_ohm_km")),
    fator_correcao: Number(fields.get("fator_correcao")),
    tabela_condutores: [
      {secao_mm2:2.5,capacidade_a:24}, {secao_mm2:4,capacidade_a:32},
      {secao_mm2:6,capacidade_a:41}, {secao_mm2:10,capacidade_a:57}
    ],
    evidencia: {documento:"Caso sintético F12",edicao:"DEMO",referencia:"Tabela fictícia não homologada"}
  };
  result.replaceChildren();
  submit.disabled = true;
  state.textContent = "Analisando caso sintético…";
  try {
    const data = await json("/api/v1/circuitos/analisar", {
      method:"POST", headers:{"Content-Type":"application/json"},
      body:JSON.stringify(payload)
    });
    if (data.liberado_para_uso_normativo !== false) throw new Error("Gate de segurança normativa inconsistente");
    add("Seção demonstrativa", fmt(data.condutor?.secao_mm2) + " mm²");
    add("Capacidade corrigida", fmt(data.condutor?.capacidade_corrigida_a) + " A");
    add("Proteção hipotética", fmt(data.disjuntor?.corrente_a) + " A");
    add("Queda resistiva legada", fmt(data.queda_tensao?.queda_percentual) + "%");
    add("Gate de liberação", "NÃO HOMOLOGADO");
    state.textContent = "Análise demonstrativa concluída; sem aprovação normativa.";
  } catch {
    state.textContent = "Não foi possível validar a demonstração. Nenhum resultado está aprovado.";
  } finally {
    submit.disabled = false;
  }
});
health();
