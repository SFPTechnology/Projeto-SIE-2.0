# C07 — Diagnóstico de qualidade do legado real (somente leitura)

**Data de observação:** 28/10/2026. **Origem:** Supabase `Electrical_Project`, `hlbksclcandbsyqrsbmx`. **Destino pretendido:** `fozrymsidnaxmuvxxfhh`.

A titularidade declarada pelo responsável contempla todos os cinco projetos. Isso **não cria** uma conta Supabase Auth nem autoriza qualquer escrita remota. Esta auditoria utilizou exclusivamente SELECTs agregados; nenhuma linha de negócio foi copiada ao repositório.

## Seleção e integridade
- Projetos selecionados: **5/5**.
- Ambientes: **41**; cargas adicionais: **52**; auditoria histórica: **1.805**.
- Número de tabelas de domínio: **15**; total de registros de domínio: **1.934**.
- Matriz de colunas: **99**; 54 mapeamentos anteriores preservados e **45 campos novos explicitamente `QUARANTINE_UNMAPPED`** até aprovação semântica.
- Rastreabilidade de conteúdo: arquivo `C01_SOURCE_FULL_PAYLOAD_FINGERPRINT_V201.json`, SHA-256 de cada tabela calculado dentro do PostgreSQL em uma única consulta. **Impressão digital não é backup, não estabelece corte transacional e não comprova identidade.**

## Qualidade dimensional e elétrica — observação real
| Teste agregador | Ocorrências | Tratamento obrigatório |
|---|---:|---|
| Ambientes com largura não positiva | 0 | Dados preserváveis |
| Ambientes com comprimento não positivo | 0 | Dados preserváveis |
| Ambientes com pé-direito menor ou igual a zero | **41** | Preservar campo legado; não inventar altura; pedir dado explícito apenas em cálculo que o exija |
| Ambientes sem área real informada | **12** | Preservar nulo; área geométrica derivada só com critério aprovado |
| Ambientes sem perímetro real informado | **12** | Preservar nulo; perímetro derivado somente de modo identificado |
| Cargas com VA/quantidade fora dos limites básicos analisados | 0 | Conservar sem atribuir conformidade |
| Cargas com tensão fixa ausente | **4** | Não inferir 127/220/380 V nem dimensionar sem tensão |
| Cargas marcadas como trifásicas | **2** | Exigir topologia e tensão linha-linha explícitas |
| Cargas com fator de potência explícito inválido | 0 | FP ausente não deve ser assumido como aprovado |

A agregação inicial de dimensões reportou 41 entradas com ao menos um atributo inválido; consulta de detalhamento mostrou que **todas as 41 têm dimensões de piso positivas**, enquanto o campo `pe_direito_m` está em zero. O gate de entrada deve distinguir altura ausente de dimensões do piso inválidas.

## Eventos históricos órfãos
Foram observados **10** eventos cujo `dep_id` não existe mais em `dependencias`:
- `DEPENDENCIA_CRIADA`: 4
- `DEPENDENCIA_EXCLUIDA`: 4
- `CALCULADA`: 2

Podem representar uma sequência legítima de criação/exclusão/cálculo. **Não** tratar como corrupção comprovada nem descartar. Conservar id original, tipo, referência legada, carimbo temporal e hash do payload em archive governado; marcar como `ORPHAN_HISTORICAL_REFERENCE` até reconciliação de proveniência, sem identificar um usuário atual a partir do texto `autor`.

## Política de transformação
1. **Camada de preservação:** arquivos brutos de origem cifrados e restauráveis em local homologado, com hash por tabela/arquivo e manifest de proveniência; proteger informações pessoais dos eventos.
2. **Camada canônica:** inserir apenas campos com mapeamento aprovado; para elementos incompletos manter estado `MIGRATED_LEGACY_PENDING_TECHNICAL_REVIEW`, não `APPROVED`.
3. **Cálculos:** quatro cargas sem tensão fixa, duas trifásicas sem topologia e 41 alturas zeradas não podem ser reparadas com defaults silenciosos.
4. **Reconciliação:** 100% dos 1.934 registros precisam estar representados no controle de transferência como aceitos, preservados historicamente ou em quarentena justificada. Isso **não** significa que todos devem virar linhas de cálculo canônico.
5. **Corte:** exigir autorização individual para criar staging, aplicar migrations e migrar reais, backup/restore verificável, identidade Auth e evidência profissional. A decisão de migrar todos os cinco projetos não suspende esses gates.

**Veredicto:** `PASS_READ_ONLY_SOURCE_DQ`; `BLOCKED_OWNER_AUTH_CUTOFF_SEMANTICS_NORMATIVE_E02_E06`; `GC=BLOCKED`.
