const viewContent = {
  overview: {
    label: "Visão geral",
    title: "Visão geral do projeto",
    description: "Acompanhe o fluxo técnico, riscos e próximos cálculos em uma única superfície.",
    panel: "Circuitos críticos",
  },
  ambientes: {
    label: "Ambientes e cargas",
    title: "Ambientes e cargas",
    description: "Organize dependências, quantidades e cargas antes de derivar os circuitos.",
    panel: "Dependências que influenciam o dimensionamento",
  },
  padrao: {
    label: "Padrão de entrada",
    title: "Padrão de entrada",
    description: "Compare demanda, fornecimento e estados da distribuidora com motivos rastreáveis.",
    panel: "Alternativas e impactos no projeto",
  },
  circuitos: {
    label: "Circuitos",
    title: "Circuitos do projeto",
    description: "Revise a derivação das cargas e mantenha o contexto técnico de cada circuito.",
    panel: "Circuitos e dependências",
  },
  correntes: {
    label: "Correntes",
    title: "Correntes de projeto",
    description: "Analise IB, balanceamento e os valores que alimentam as verificações seguintes.",
    panel: "Correntes que requerem inspeção",
  },
  condutores: {
    label: "Condutores",
    title: "Dimensionamento de condutores",
    description: "Compare critérios normativos, seção adotada e personalizações por circuito.",
    panel: "Condutores com menor margem",
  },
  queda: {
    label: "Queda de tensão",
    title: "Queda de tensão",
    description: "Inspecione resultados, cenários e alertas sem perder a origem de cada valor.",
    panel: "Circuitos próximos ao limite",
  },
  unifilar: {
    label: "Diagrama unifilar",
    title: "Diagrama unifilar",
    description: "Navegue pela estrutura elétrica, selecione elementos e configure a exportação.",
    panel: "Estrutura do diagrama",
  },
  diagnostico: {
    label: "Diagnóstico",
    title: "Diagnóstico e conformidade",
    description: "Consolide pendências técnicas, severidade, causa e próxima ação recomendada.",
    panel: "Pendências por prioridade",
  },
};

const circuitContent = {
  C14: {
    application: "Forno elétrico",
    phase: "2F · 220 V",
    current: "28,7 A",
    conductor: "Cu · 4 mm²",
    length: "34,0 m",
    severity: "Requer revisão",
  },
  C08: {
    application: "Ar-condicionado suíte",
    phase: "2F · 220 V",
    current: "12,4 A",
    conductor: "Cu · 2,5 mm²",
    length: "18,5 m",
    severity: "Conforme",
  },
  C03: {
    application: "TUG cozinha",
    phase: "1F + N · 127 V",
    current: "16,9 A",
    conductor: "Cu · 2,5 mm²",
    length: "21,0 m",
    severity: "Conforme",
  },
};

const body = document.body;
const palette = document.querySelector("#command-palette");
const commandSearch = document.querySelector("#command-search");
const commandResults = document.querySelector("#command-results");
const toast = document.querySelector("#prototype-toast");
const toastMessage = document.querySelector("#toast-message");
const inspector = document.querySelector("#inspector-panel");
let toastTimer;

function showToast(message) {
  window.clearTimeout(toastTimer);
  toastMessage.textContent = message;
  toast.hidden = false;
  toastTimer = window.setTimeout(() => {
    toast.hidden = true;
  }, 3600);
}

function activateView(view) {
  const content = viewContent[view];
  if (!content) return;

  document.querySelectorAll("[data-view]").forEach((item) => {
    const isActive = item.dataset.view === view;
    item.classList.toggle("is-active", isActive);
    if (isActive) {
      item.setAttribute("aria-current", "page");
    } else {
      item.removeAttribute("aria-current");
    }
  });

  document.querySelector("#view-title").textContent = content.title;
  document.querySelector("#view-description").textContent = content.description;
  document.querySelector("#breadcrumb-current").textContent = content.label;
  document.querySelector("#engineering-title").textContent = content.panel;

  body.classList.remove("is-menu-open");
  document.querySelector("#mobile-menu-trigger").setAttribute("aria-expanded", "false");
  showToast(`${content.title} selecionado no protótipo.`);
}

function openPalette() {
  if (!palette.open) {
    palette.showModal();
  }
  commandSearch.value = "";
  filterCommands("");
  window.setTimeout(() => commandSearch.focus(), 0);
}

function closePalette() {
  if (palette.open) palette.close();
}

function filterCommands(value) {
  const query = value.trim().toLocaleLowerCase("pt-BR");
  commandResults.querySelectorAll("button").forEach((item) => {
    item.hidden = query.length > 0 && !item.textContent.toLocaleLowerCase("pt-BR").includes(query);
  });
}

function selectCircuit(circuitId) {
  const content = circuitContent[circuitId];
  if (!content) return;

  document.querySelectorAll("[data-circuit]").forEach((row) => {
    row.classList.toggle("is-selected", row.dataset.circuit === circuitId);
  });

  document.querySelector("#inspector-title").textContent = `Circuito ${circuitId}`;
  const values = inspector.querySelectorAll(".property-list dd");
  [content.application, content.phase, content.current, content.conductor, content.length].forEach(
    (value, index) => {
      values[index].textContent = value;
    },
  );

  const badge = inspector.querySelector(".inspector-status .status-badge");
  badge.textContent = content.severity;
  badge.className =
    content.severity === "Conforme"
      ? "status-badge status-badge-success"
      : "status-badge status-badge-warning";

  if (window.matchMedia("(max-width: 1400px)").matches) {
    body.classList.add("is-inspector-open");
  }
}

document.querySelectorAll("[data-view]").forEach((item) => {
  item.addEventListener("click", () => activateView(item.dataset.view));
});

document.querySelectorAll("[data-view-target]").forEach((item) => {
  item.addEventListener("click", () => activateView(item.dataset.viewTarget));
});

document.querySelector("#command-trigger").addEventListener("click", openPalette);
document.querySelector("#help-trigger").addEventListener("click", openPalette);

document.querySelector("#mobile-menu-trigger").addEventListener("click", (event) => {
  const isOpen = body.classList.toggle("is-menu-open");
  event.currentTarget.setAttribute("aria-expanded", String(isOpen));
});

document.querySelector("#density-trigger").addEventListener("click", () => {
  const nextDensity = body.dataset.density === "compact" ? "comfortable" : "compact";
  body.dataset.density = nextDensity;
  showToast(`Densidade ${nextDensity === "compact" ? "compacta" : "confortável"} ativada.`);
});

document.querySelector("#inspector-trigger").addEventListener("click", () => {
  if (window.matchMedia("(max-width: 1400px)").matches) {
    body.classList.toggle("is-inspector-open");
  } else {
    body.classList.toggle("is-inspector-hidden");
  }
});

document.querySelector(".inspector-close").addEventListener("click", () => {
  body.classList.remove("is-inspector-open");
});

document.querySelector("#validate-trigger").addEventListener("click", () => {
  showToast("Validação simulada. O protótipo não executa regras de engenharia.");
});

document.querySelectorAll("[data-circuit]").forEach((row) => {
  row.addEventListener("click", () => selectCircuit(row.dataset.circuit));
  row.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      selectCircuit(row.dataset.circuit);
    }
  });
});

document.querySelectorAll(".segmented-control button").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelectorAll(".segmented-control button").forEach((item) => {
      const isSelected = item === button;
      item.classList.toggle("is-selected", isSelected);
      item.setAttribute("aria-pressed", String(isSelected));
    });
    showToast(`Visualização ${button.textContent.trim()} selecionada.`);
  });
});

commandSearch.addEventListener("input", (event) => filterCommands(event.target.value));

commandResults.addEventListener("click", (event) => {
  const command = event.target.closest("button");
  if (!command) return;

  if (command.dataset.commandView) {
    activateView(command.dataset.commandView);
  } else if (command.dataset.commandAction === "validate") {
    showToast("Validação simulada. O protótipo não executa regras de engenharia.");
  }
  closePalette();
});

palette.addEventListener("click", (event) => {
  const bounds = palette.getBoundingClientRect();
  const isBackdrop =
    event.clientX < bounds.left ||
    event.clientX > bounds.right ||
    event.clientY < bounds.top ||
    event.clientY > bounds.bottom;
  if (isBackdrop) closePalette();
});

document.addEventListener("keydown", (event) => {
  if ((event.ctrlKey || event.metaKey) && event.key.toLocaleLowerCase("pt-BR") === "k") {
    event.preventDefault();
    openPalette();
  }

  if (event.key === "?" && !event.ctrlKey && !event.metaKey && document.activeElement.tagName !== "INPUT") {
    event.preventDefault();
    openPalette();
  }
});
