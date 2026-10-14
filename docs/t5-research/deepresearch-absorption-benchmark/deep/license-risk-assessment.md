# License Risk Assessment

## Licenças no Universo do Bench

| License | Players | Risk para AIOX absorption |
|---|---|---|
| **MIT** | DeerFlow, LangChain ODR, Local DR, AutoResearchClaw | 🟢 **NONE** — REUSE full |
| **Apache-2.0** | GPT-Researcher, OpenResearcher, DeepResearcher, Tongyi | 🟢 **LOW** — REUSE com atribuição (NOTICE.txt) |
| **Jina proprietary** | Jina node-DR | 🔴 **HIGH** — não REUSE, apenas inspirar arquitetura |
| **Elastic License v2** | AIOX apps/research | 🟡 **MEDIUM** — afasta community OSS |

## Análise por Absorption Target

### GAP-01 (Sandbox) — AutoResearchClaw (MIT)
✅ **CLEAR.** MIT permite REUSE com mínima atribuição (preservar copyright notice). Podemos copiar/adaptar diretamente o pattern de Docker hardened.

### GAP-02 (Distribution) — GPT-Researcher (Apache-2.0)
✅ **CLEAR.** Apache-2.0 permite REUSE com NOTICE.txt + manter changelog de modificações. Pattern de PyPI packaging + Docker Hub publishing pode ser adotado.

### GAP-03 (MCP) — LangChain ODR (MIT) + GPT-Researcher (Apache-2.0)
✅ **CLEAR.** Ambas permitem REUSE. Adotar pattern de MCP server exposure.

### GAP-04 (Model backend) — OpenResearcher/DeepResearcher/Tongyi (Apache-2.0)
✅ **CLEAR.** Apache-2.0 dos modelos + datasets permite uso comercial. Apenas adicionar **NOTICE.txt** em `packages/@sinkra/research-cli` listing terceiros.

### GAP-05 (Memory) — DeerFlow TIAMAT (MIT)
✅ **CLEAR.** MIT. Atenção: TIAMAT pode ter dependências (Redis? PostgreSQL?) com licenses próprias — verificar cada uma.

### GAP-06 (Scholarly DB) — Local DR (MIT)
✅ **CLEAR.** MIT. Adapter pattern (arxiv/pubmed/semantic-scholar) pode ser copiado/adaptado.

### Anti-pattern — NÃO absorver de Jina (proprietary)
❌ **FORBIDDEN.** node-DeepResearch tem "All rights reserved" no LICENSE. **Apenas inspirar arquitetura** (single-loop pattern, budget monitoring concept) — nunca copiar código ou prompts.

## Recomendação para apps/research License

**Status atual:** Elastic License v2 (não OSI).

**Pros:**
- ✅ Protege contra SaaS competitor (AWS/Azure copiando)
- ✅ Permite uso comercial interno
- ✅ Mantém marca AIOX

**Cons:**
- ❌ **8/9 competidores OSS = community contribution friction**
- ❌ Não enterprise procurement friendly em alguns setores
- ❌ Não pode ser submetido a OSI ou Awesome Lists genéricas

**Recomendação:**

### Dual-License (Elastic v2 + AGPLv3)

```
apps/research-pro/       → Elastic License v2 (enterprise features)
apps/research-community/ → AGPLv3 (CE — community edition)
```

**AGPLv3** mantém proteção SaaS competitor (qualquer fork hospedado precisa publicar source) MAS é OSI-approved. Community pode contribuir sem fricção.

Modelo precedente: **MongoDB (SSPL), Sentry (BSL → BSL-1.1), Codecov (BSL).** Sentry CE em AGPLv3 funciona.

**Esforço:** 2 pts. Mas **impacto adoção:** alto.

## License Compatibility Matrix

| AIOX absorbs from | License upstream | AIOX redistribute as | OK? |
|---|---|---|---|
| AutoResearchClaw (sandbox) | MIT | Sinkra MIT or Apache-2.0 | ✅ |
| GPT-Researcher (PyPI) | Apache-2.0 | Sinkra Apache-2.0 | ✅ |
| LangChain ODR (MCP) | MIT | Sinkra MIT | ✅ |
| OpenResearcher (model wrap) | Apache-2.0 + NOTICE | Sinkra Apache-2.0 | ✅ |
| DeerFlow (memory) | MIT | Sinkra MIT | ✅ |
| Local DR (scholarly) | MIT | Sinkra MIT | ✅ |
| Jina node-DR (anything) | Jina proprietary | ❌ FORBIDDEN | ❌ |

## Action Items

1. **Adicionar NOTICE.txt** em `packages/@sinkra/research-cli` com licenses de terceiros
2. **Dual-license apps/research** (Elastic v2 + AGPLv3 CE) — efforto 2pts
3. **NUNCA** copiar/adaptar código Jina — apenas inspirar arquitetura conceitualmente
4. **CI guard:** adicionar `validate:license-headers` em packages/@sinkra/research-*

## Sources

- Cada `LICENSE` inspecionado nos clones em `../bench/`
- AIOX `apps/research/LICENSE`
- OSI license list https://opensource.org/licenses
- Apache-2.0 NOTICE requirement https://www.apache.org/licenses/LICENSE-2.0#redistribution
