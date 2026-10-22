# F08 — Proteções e distribuição elétrica

Data: 22/10/2026. **ESTADO: VALIDATING — código, QA3 e regressão local aprovados; aguarda CI remoto.**

Branch: `feat/f08-protecoes-distribuicao`. Base F07 remota preservada: `5402ca7c09fb1333e6bbab59b75bc7ad50a36187`. Fonte de estado: `docs/sie-orchestrator/ORCHESTRATOR_STATE.json`. Não houve alteração da main, deploy ou banco real.

## Tasks implementadas e verificadas no recorte

| Task | Resultado e evidência |
|---|---|
| 08.01 | Contratos MCB/FUSE/RCD/SPD tipados; identidade, edição e proveniência separadas de fontes declaradas; catálogo finito do servidor. protection_contracts_f08.py, protection_registry_f08.py, FONTES.md |
| 08.02 | Thevenin radial complexo, máximo/mínimo, localização DEVICE/SEGMENT_END e base FN/FF vinculados; contribuições adicionais bloqueadas. Casos independentes racional3–4–5 e identidade trifásica quadrática |
| 08.03 | Ib≤In≤Iz e I2, com nota de duração>100h/ano ou>500h/vida; mesma regra nos candidatos. Testes por dispositivo/duração/fronteira |
| 08.04 | Interrupção com tensão/norma e falta máxima no dispositivo; energia≤k²S², domínio até5s e assimetria abaixo0,1s; fase, PE e neutro separados. Vínculos de dispositivo/cenário/faixa e material/temperatura |
| 08.05 | TN com laço fase-PE e domínio de curva; TT com DR/RA/IΔn/UL/tempo; TN-C/DR rejeitado; IT fora do modelo permanece PENDENTE. Não há aprovação genérica por Ib/Iz |
| 08.06 | DR: sensibilidade/tipo/condutores/PE/In/retaguarda/suportabilidade condicional. DPS: Uc/Up/tipo/In/Imax/Iimp/ligação/aterramento/retaguarda; Imax<In bloqueado; T3 fora do modelo permanece PENDENTE |
| 08.07 | Par montante/jusante provado no grafo, fonte de fabricante finita para iC60N C32→C16 1P230V, limite parcial260A. Igualdade, superação, tensão, conexão, identidade e temperatura testadas. Outros pares declarados permanecem pendentes |
| 08.08 | Quadros por fase com soma conservadora e proposta determinística para cargas FN, respeitando fonte/alimentadores e preservando FF/trifásicas. Proposta não aplicada; exige recálculo e decisão do projetista |
| 08.09 | Candidatos e variantes finitos reexecutam F07 e motor completo; identidade física impede reutilizar faltas antigas só renomeando cenários. Convergência computacional positiva real, ausência de solução, limite e cenário bloqueado testados. Estado global continua separado da homologação |
| 08.10 | CLI/API/interface, quadros e memória/exportação/impressão, vínculos com grafo e revisão; histórico imutável, último F07 atual obrigatório, hashes/revisão/concorrência e invalidação de documentos/cálculos |

Arquivos e checklist completos: `docs/stories/SIE-F08.md`. Exemplos são sintéticos, não produtos certificados ou instalações aprovadas.

## Fontes e domínio

`FONTES.md` registra URLs oficiais, versões, páginas, hashes e conferência visual independente. O catálogo A9F74116 abrange16A/curvaC/1P/230VAC/30°C/50–60Hz, Icn6000A segundo IEC60898-1 e I2=23,2A. Não mistura Icu de outra norma/tensão. Guia oficial de coordenação2026v4.0, PDF39/impressaA-31: limite parcial260A para o par registrado. A célula foi conferida pelo pesquisador e QA02; não é seletividade total nem certificação dos aparelhos instalados.

Os dados de fonte/curva/energia/k/DR/DPS fornecidos em estudos continuam declaratórios quando não autenticados no catálogo. Modelos fora do domínio falham de modo explícito. Não são criados fatores ou curvas ausentes.

## Testes finais observados

- `.venv/bin/python -m pytest restructuring/apps/api/tests -q --tb=short`: **1020 passed**, 1 aviso Starlette/httpx, **16,24s**; inclui **156 casos F08**, preservando864 anteriores.
- `.venv/bin/python -m pytest restructuring/e2e -q --tb=short`: **34 passed**, **77,89s**, Chromium140/Playwright1.55.
- `.venv/bin/python scripts/f00_golden.py --verify`: **34 casos**, fixture original intacta.
- `npm run lint`, `npm run typecheck`, `npm test` (**18 testes**), `npm run build`: PASS.
- `node --check restructuring/apps/web/protecoes.js`, CLI análise/catálogo e `git diff --check`: PASS. Exemplo retorna REPROVADO, sem ocultar falhas reais.
- QA03:9 testes API/CLI/persistência,2 E2E afetados e ensaio Chromium adicional de XSS/URLs/estados: PASS.

Instalação de dependências e recuperação de cache de navegador foram locais, sem modificar manifests ou lockfiles. CDN retornou ZIP inválido; mirror oficial Microsoft recuperou Chromium. Três falhas intermediárias de fixtures em edição foram corrigidas antes do congelamento; as expectativas de fronteira e limites não foram relaxadas. A suíte integral congelada acima substitui os ensaios intermediários.

## QA3 e correções

| Revisor | Parecer final | Evidência |
|---|---|---|
| QA-01 | APROVADO no recorte computacional | QA-01.md; entradas adversariais, convergência, pares260A e identidades contraditórias |
| QA-02 | APROVADO no recorte computacional | QA-02.md; cálculos independentes, fonte visual, DR/DPS/retornos, limites de seccionamento e campos incompatíveis |
| QA-03 | APROVADO no recorte de integração/segurança/UX | QA-03.md; autenticação, revisão409, stale, memória adulterada, XSS/links e separação dos estados |

Achados corrigidos: erro de contrato visual; falta sem vínculo de tensão; térmico sem dispositivo/cenário/faixa; fase indevidamente usada como prova de PE; omissão de falha F07; candidatos ignorando duração; renomeação de cenários burlando recálculo; catálogo atribuído a identidade contraditória; seletividade de fim de trecho; DPS Imax<In. Revisões foram reexecutadas após as correções.

Os revisores são agentes de software, sem assinatura ou aprovação profissional humana. `normative_conformity_verified=false`, `authoritative_for_sizing=false` e `professional_approval=false` permanecem obrigatórios, inclusive quando `computational_state=ATENDE_ESTUDO` ou uma variante converge.

## Gates e passagem

Gates locais de software satisfeitos no recorte documentado: estados coerentes/testados, recálculo/invalidação, relatório com limites explícitos e três QA aprovados. A publicação/CI remoto ainda será conferida antes de registrar DONE e liberar desenvolvimento da fase seguinte. IT completo, T3, outros pares/curvas/famílias e dados físicos fora do modelo permanecem pendentes por cenário; não são afirmados universais. Teste computacional não substitui inspeção/ensaio ou revisão profissional de instalação.
