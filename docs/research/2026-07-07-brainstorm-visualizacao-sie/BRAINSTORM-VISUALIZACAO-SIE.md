# Brainstorming Session: SIE Visualmente Impactante

**Data:** 2026-07-07
**Facilitador:** Atlas (@analyst)
**Objetivo da sessão:** Ideação ampla (divergente)
**Escopo:** Visualização de dados, gráficos, diagramas e plantas elétricas para técnicos, arquitetos e engenheiros
**Perspectivas simuladas:** UX/Design, Frontend, Domínio Elétrico, Produto, QA

## Contexto

- Stack: TypeScript full-stack (TanStack Start + React 19 + Carbon Design System + Supabase).
- Cadeia atual: carga → demanda → circuitos derivados; dimensionamento/proteção/laudo em roadmap (P0-P2).
- Sessão anterior (`docs/research/2026-07-07-brainstorm-novos-modulos/`) priorizou memorial de cálculo embutido e "explicador normativo" — sinergia direta com visualização.

## Ideias Geradas

**Total:** 22

### 🎨 UX / Design

1. **Diagrama unifilar interativo gerado automaticamente** — a partir dos circuitos derivados, renderizar o unifilar em SVG (quadro → disjuntores → circuitos), com clique em cada elemento abrindo o memorial de cálculo. É *o* artefato visual que engenheiros esperam.
2. **Dashboard de balanço de cargas** — barras por fase (R/S/T) com alerta de desbalanceamento; medidor de demanda vs. categoria de fornecimento EDP.
3. **Mapa de calor de cargas por ambiente** — planta esquemática com ambientes coloridos por densidade de carga VA/m².
4. **Linguagem visual de conformidade (semáforo normativo)** — selo verde/âmbar/vermelho NBR5410 por circuito/ambiente, agregando num "score de conformidade" do projeto.
5. **Modo apresentação/cliente** — visão simplificada para o cliente leigo (custos, potências, o que cada disjuntor protege), distinta da visão técnica densa.

### 💻 Frontend / Implementação

6. **SVG próprio para o unifilar, não lib genérica de diagramas** — simbologia NBR (IEC 60617) é conjunto pequeno e fixo; componentes React de símbolos + layout determinístico (árvore quadro→circuitos) evitam dependência pesada tipo GoJS.
7. **Carbon Charts primeiro** — já integra com o design system existente; avaliar Recharts/visx só se faltar recurso.
8. **Export SVG → PDF/DXF** — unifilar exporta para PDF (laudo) e DXF (AutoCAD). DXF de unifilar é diferencial raro em SaaS nacional.
9. **Quadro de distribuição "fotorrealista"** — visão do QDC como será montado fisicamente (trilho DIN, posições), útil para o técnico executor.

### ⚡ Domínio Elétrico

10. **Diagrama multifilar/funcional por circuito** — detalhe fase/neutro/terra, seção, comprimento — quando o dimensionamento (P1) existir.
11. **Visualização da cadeia de cálculo** — Sankey/fluxo mostrando carga instalada → fatores de demanda → demanda final; explica visualmente por que a demanda deu aquele valor.
12. **Curvas de disjuntores sobrepostas** — gráfico de coordenação/seletividade (tempo×corrente) quando proteção (P1.5) existir.
13. **Planta elétrica simbólica por ambiente** — grid com pontos (tomadas, iluminação) posicionáveis por arrastar; gera a "planta de pontos" usada em obra sem ser CAD.

### 📊 Produto

14. **Unifilar como saída "hero" do produto** — marketing e onboarding centrados em "entre com os ambientes, saia com o unifilar pronto".
15. **Import de planta (imagem/PDF) como fundo** — usuário posiciona pontos elétricos sobre a planta baixa; menor esforço para "parecer CAD".
16. **Comparador visual de cenários** — dois unifilares/dashboards lado a lado (monofásico vs. trifásico, categoria U vs. T); conecta com a simulação da sessão anterior.

### 🧪 QA / Confiabilidade

17. **Snapshot testing visual do unifilar** — diagramas determinísticos; snapshots SVG protegem contra corrupção em refactors.
18. **Acessibilidade dos gráficos** — paleta segura para daltônicos + dados tabulares equivalentes (também exigência implícita de laudo).

### 🔀 Combinações e Wild Cards

19. **(1+11+explicador normativo) "Unifilar explicável"** — hover em qualquer elemento mostra a regra NBR e o cálculo que o gerou.
20. **(8+memorial) Laudo com diagramas embutidos** — o PDF do laudo (P2) nasce com unifilar + gráficos de demanda, da mesma fonte SVG.
21. **🃏 Vista 3D do quadro/instalação (Three.js)** — impacto de marketing máximo, baixo valor de engenharia; wild card consciente.
22. **🃏 "Raio-X da residência"** — visão isométrica esquemática da casa com circuitos coloridos percorrendo os ambientes; identidade visual única.

## Categorização

| Categoria | Ideias | Tema |
|---|---|---|
| **Unifilar (hero)** | 1, 6, 8, 14, 19 | O artefato central |
| **Dashboards de cálculo** | 2, 4, 11 | Transparência do motor |
| **Planta / espacial** | 3, 13, 15, 22 | Dimensão espacial sem virar CAD |
| **Futuro (depende P1/P1.5)** | 10, 12 | Pós-dimensionamento |
| **Comunicação/venda** | 5, 16, 21 | Cliente leigo e marketing |
| **Base técnica** | 7, 9, 17, 18 | Stack e qualidade |

## Top 5 Recomendações Priorizadas

| # | Ideia | Valor | Esforço | ROI | Racional |
|---|---|---|---|---|---|
| 1 | **Unifilar SVG automático (1+6)** | 10 | 6 | 1,67 | Artefato que técnicos/engenheiros mais valorizam; dados já existem (circuitos derivados); vira o "hero" do produto |
| 2 | **Dashboard balanço/demanda (2+11)** | 8 | 3 | 2,67 | Carbon Charts pronto; explica a caixa-preta do cálculo com dados já processados |
| 3 | **Semáforo de conformidade (4)** | 8 | 3 | 2,67 | Aproveita as validações NBR existentes; impacto visual imediato em todo o app |
| 4 | **Unifilar explicável (19)** | 9 | 4 | 2,25 | Sinergia direta com memorial/explicador da sessão anterior; diferencial competitivo único |
| 5 | **Export PDF/DXF (8)** | 8 | 5 | 1,60 | Conecta o visual ao entregável pago (laudo P2) e ao fluxo real do engenheiro (CAD) |

### Próximos passos por recomendação

1. **Unifilar SVG:** @ux-design-expert desenha wireframe + inventário de símbolos IEC 60617 necessários; @architect define contrato circuitos→diagrama.
2. **Dashboards:** spike com Carbon Charts sobre os dados de demanda existentes (baixo risco, alta visibilidade).
3. **Semáforo:** mapear validações NBR existentes → estados visuais; definir agregação do score.
4. **Unifilar explicável:** depende do contrato `{ resultado, memorial }` da sessão anterior — reforça a prioridade daquela decisão.
5. **Export:** avaliar libs de geração DXF em JS (ex.: dxf-writer) e pipeline SVG→PDF.

## Key Insights

- **O unifilar é o ponto de alavancagem:** simultaneamente o visual mais impactante, o mais esperado pelo público técnico e o que mais reaproveita dados já existentes.
- Dashboards e semáforo são **vitórias rápidas** com Carbon Charts; planta espacial e 3D são camadas posteriores.
- Forte sinergia com a sessão de novos módulos: **memorial + explicador + unifilar** formam um único conceito de produto — "cálculo visível e defensável".
- A ordem visual saudável segue o roadmap: unifilar/dashboards agora (dados existem), multifilar e curvas de disjuntor depois de P1/P1.5.

## Metadados da Sessão

- **Ideias geradas:** 22
- **Categorias identificadas:** 6
- **Perspectivas:** 5 (UX, Frontend, Domínio Elétrico, Produto, QA)
- **Duração:** ~30 min
- **Sessão relacionada:** `docs/research/2026-07-07-brainstorm-novos-modulos/BRAINSTORM-NOVOS-MODULOS-DIMENSIONAMENTO.md`

---

**Handoffs sugeridos:**
- @ux-design-expert → wireframes do unifilar e dashboards
- @pm → consolidar as duas sessões (novos módulos + visualização) num epic
