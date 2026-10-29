# C08 — Registro de execução C01/C02/C07 e seleção dos cinco projetos (28/10/2026)

**Declaração do responsável:** todos os cinco projetos do SIE original lhe pertencem e foram selecionados para migração ao SIE 2.0. Esta decisão substitui a indefinição de escopo, **não** a verificação de identidade no destino nem a autorização específica para DDL/ETL remoto.

## Evidências novas e rastreáveis
- `C01_C07_SELECTION_ALL_FIVE_V201.json`: 5 IDs de origem, contagens por projeto, decisão de migrar todos, Auth UUID de destino ainda nulo, escrita remota desabilitada.
- `C02_MATRIZ_COMPLETA_OPERACIONAL_V201.csv`: 15 tabelas e **99 colunas**, sendo 54 com mapeamento anterior e **45 sem regra semântica validada**; cada uma explicitamente em quarentena.
- `C01_SOURCE_FULL_PAYLOAD_FINGERPRINT_V201.json`: **1.934 linhas**, hashes SHA-256 dos payloads das 15 tabelas obtidos via consulta PostgreSQL estritamente de leitura; ainda não é snapshot de backup ou corte transacional.
- `C07_REAL_SOURCE_DATA_QUALITY_V201.md`: qualidade real agregada: largura/comprimento válidos; 41 alturas em zero; 4 cargas com tensão fixa nula; 2 trifásicas; 10 eventos de auditoria historicamente órfãos (4 de criação, 4 de exclusão e 2 de cálculo), todos preserváveis.
- `C09_RUNBOOK_MIGRACAO_ALL_FIVE_E_GC_V201.md`: dependências G0–G7 e exigências E02–E06.
- Validação offline de invariantes/deriva em `v201_c_migration_preflight.py`, `v201_c_source_cutoff.py` e testes negativos `test_c07_*`; nenhuma rota de escrita ou acesso ao Supabase nesses módulos.

**QA observado:** commit `42b36070eea2e2a4579386ae366fd2f8c1a48687` corrigiu a matriz CSV (54 linhas antigas tinham uma coluna extra). O CI `SIE modular API`, `SIE C03 PG17`, `SIE A03/A04 PG17` e `AIOX` foram observados `SUCCESS` nesse SHA; Chromium estava em execução no último read-back. Checks do SHA final após a documentação devem ser reconciliados antes de congelar a versão.

**GC formal permanece `BLOCKED`:** identidade Auth e propriedade vinculadas à conta real não verificadas; 45 regras de campos requerem disposição aprovada; backup/restore, corte e ETL real não realizados; parâmetros elétricos e catálogo normativo ainda sujeitos a revisão profissional; staging E02–E06 exige autorização específica antes de qualquer escrita.

---

# C08 — Consolidação do Bloco C, DEVELOPMENT — 28/10/2026

**Estado formal GC: BLOCKED.** O projeto avançou na implementação do domínio elétrico; este documento não é autorização de produção, de migração real, nem laudo de conformidade elétrica. PR #11 permanece DRAFT.

## Agentes especializados e entregas verificáveis

| Agente lógico | Responsabilidade | Estado |
|---|---|---|
| LEGACY — Engenharia de dados | Identificar origem, contagens, integridade e titularidade | Origem/contagens comprovadas; titularidade pendente |
| ETL — Dados e rastreabilidade | Mapear campos e registrar quarentena, replay, ownership | CLI sintética + preflight; dados reais não importados |
| ELEC — Engenharia elétrica | Calcular somente com parâmetros explícitos; testes matemáticos | Motor C05 ampliado; regras não homologadas |
| NORM — Governança de normas | Edição/edição vigente, células, licenças P03/P06, Rca/XL | Evidências oficiais de versão consultadas; aprovação humana pendente |
| BACK — FastAPI e persistência | Snapshots, imutabilidade, C05, round-trip e auditoria | DEV SQLite e PG17 descartável |
| SEG — Auth, owner A/B, RLS | Negativos de acesso, ausência de bypass e isolamento | Sintéticos PASS anteriores; Auth real a homologar |
| QA/DEVOPS — gate e CI | Independência de validação, regression por SHA, PR sem merge | CI em GitHub, verificar resultado integral do HEAD |

## Fonte real comprovada, NÃO vazia
Leitura autenticada no projeto legado `Electrical_Project`: 5 projetos; 41 ambientes; 52 cargas adicionais; 17 edições; 1805 eventos; 2 overrides EDP; 3 resultados de dimensionamento de condutores. Há tabelas adicionais que não constavam do esquema original de oito tabelas.

Dependências→projetos, cargas→dependências, edições→dependências, eventos→projetos e parâmetros EDP→projetos: zero referências órfãs na leitura. **Eventos→dependências: 10 órfãos históricos**, que requerem quarentena/reconciliação sem apagamento. O legado e o destino tinham **zero usuários Auth**, e a tabela legada `projetos` não possui owner_id; é IMPOSSÍVEL atribuir automaticamente proprietário legítimo. A fonte permanece somente leitura.

## Implementação técnica C03/C05/C06/C07
- C03: 10 tabelas elétricas novas; campos aditivos, relações compostas, RLS e imutabilidade. Migration `20261028203000` PENDING remotamente.
- C04: gateway normativo com hash e status fail-closed, nunca aprovado por JSON mutável.
- C05: VA por ambiente/circuito, corrente single/three explicitamente declarada, demanda condicionada a fator fornecido, capacidade corrigida, Ib/In/Iz básico e queda de tensão por R/X. Dados técnicos são escritos em DRAFT sob CAS, auditados, capturados no snapshot selado e preservados no clone. Resultado continuará `EVIDENCE_PENDING`; DR/DPS, curto-circuito/I2, seletividade, aterramento e limite normativo continuam pendentes.
- C05 PostgreSQL: ensaio em PostgreSQL 17 descartável com origem selada, writer server-only, replay e isolamento A/B sintético.
- C06/C07: ETL sintético transacional idempotente; preflight exige todos os projetos e mapeamento explícito, mas **NUNCA** se autoautoriza para importação real.

## Evidência de checks
O baseline `f1990afdccf5180e56c2818e580148bcfbd719e6` obteve os cinco workflows aprovados. O incremento mais recente antes desta documentação foi `ab621c4d5c12ac7e462d4662bdb826dff867069b`: PostgreSQL C03/C05, A03/A04 e AIOX PASS em read-back; API e Chromium aguardavam finalização na verificação. Exigir status concluído para o HEAD final, nunca reaproveitar aprovação de SHA anterior.

## Condições para GC integral
**C02/C07:** inventariar e mapear as colunas adicionais da fonte operacional; obter comprovação de titularidade dos cinco projetos, preservar os dez eventos órfãos com referência de origem; congelar fonte com backup e digest; executar ETL real reversível em staging autorizado com 100% dos registros aceitos reconciliados.

**C04/C05/E03:** aprovação de fontes/células normativas NBR/EDP, condições P03/P06 e lacunas Rca/XL; completar motor e testes golden integrados, inclusive planta/quadros e referências C03 no snapshot PostgreSQL canônico; aprovar profissionalmente o escopo usado.

**C08/E02–E06:** Auth/RLS real A/B em destino de homologação, migrations autorizadas, backup/restore, read-back, CI no mesmo SHA e aceite de release. Não antecipar deploy para Hostinger ou Supabase.

**Resultado:** GC=BLOCKED integral; desenvolvimento DEV incrementado com verificações concretas. `main`, F12, SIE 1.0, DHT, Supabase remoto e produção preservados.
