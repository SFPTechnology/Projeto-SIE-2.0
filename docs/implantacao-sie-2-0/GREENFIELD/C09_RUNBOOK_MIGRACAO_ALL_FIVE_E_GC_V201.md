# RUNBOOK DE ENCERRAMENTO C / MIGRAÇÃO DOS CINCO PROJETOS — V2.0.1

**Estado:** EXECUTÁVEL POR ETAPAS, **SEM GO PARA ESCRITA REMOTA**. A declaração do responsável nesta conversa, 28/10/2026, selecionou todos os cinco projetos para migração; não constitui login Auth, autorização geral de DDL, laudo elétrico ou aprovação GC.

## 0. Limites invioláveis
- Origem `hlbksclcandbsyqrsbmx` / `Electrical_Project`: **SELECT ONLY**; sem alterações nem exclusões; repositório SIE original somente leitura.
- Destino `fozrymsidnaxmuvxxfhh` / `SIE_2.0`: **SEM ESCRITAS** nesta execução; migrations A03/A04/B04/C03 pendentes, somente GF02 anteriormente aplicada.
- Não modificar `main`, F12, Hostinger, produção ou DHT. PR #11 DRAFT na branch `feat/v201-bloco-c-dominio-eletrico`.
- Nenhuma credencial/secreto, token JWT, dump integral ou dados pessoais de auditoria no GitHub. Separar artefatos de evidências agregadas de dumps cifrados e restritos.

## 1. Insumos gerados
1. `C01_C07_SELECTION_ALL_FIVE_V201.json`: IDs de cinco projetos, intenção de migrar 5/5, contagens e target Auth **nulo**.
2. `C02_MATRIZ_COMPLETA_OPERACIONAL_V201.csv`: 99 colunas de 15 tabelas, 45 ainda `QUARANTINE_UNMAPPED`. Enumerar explicitamente cada atributo antes de uma transformação sem perdas.
3. `C01_SOURCE_FULL_PAYLOAD_FINGERPRINT_V201.json`: 1.934 linhas, SHA-256 agregado por tabela em SELECT único; prova somente estado observado, não é backup nem snapshot transacional.
4. `C07_REAL_SOURCE_DATA_QUALITY_V201.md`: quatro cargas sem tensão fixa; dois registros trifásicos; 41 pés-direitos zerados; dez referências históricas de auditoria sem dependência atual.
5. `v201_c_migration_preflight.py` e `v201_c_source_cutoff.py`: validadores determinísticos offline sem conexão, escrita ou aprovação automática.

## 2. Fluxo de execução: dependências e critérios objetivos
| Ordem | Responsável lógico | Ação obrigatória | Evidência / GO |
|---|---|---|---|
| G0 | Titularidade e SecOps | Vincular os 5 IDs de origem ao usuário real autenticado de destino após verificação independente; não derivar de autor textual | Auth UID genuíno e comprovante de vínculo; sem usuário falso |
| G1 | DBA e Dados | Completar as 45 disposições pendentes, revisar enums TUE/OUTRA/ILUMINACAO, conversões de unidade e preservação de histórico | Matriz aprovada 99/99; itens sem transformação ficam na camada bruta governada |
| G2 | DBA / infraestrutura | Registrar autorização específica para criar staging isolado, capacidade de backup/restore e aplicação A03/A04/B04/C03 | GO de DDL no staging, rollback testado, fingerprint de schema e contas A/B segregadas |
| G3 | Dados | Definir corte consistente com export cifrado de 15 tabelas; computar hash por arquivo e comparar impressão digital com readback anterior; detectar alterações após corte | Export íntegro, manifesto assinado e proteção de dados pessoais |
| G4 | ETL | Executar dry-run em staging com UUIDs determinísticos, reexecução idempotente, atomicidade e quarentena explícita | 5 projetos; 41 ambientes; 52 cargas; 1.805 eventos; 1.934 linhas contabilizadas sem perdas silenciosas |
| G5 | Engenheiro Elétrico | Validar P03/P06, Rca/XL, tabelas EDP, motores DR/DPS, aterramento, proteção, queda de tensão, demanda e exemplos golden | Evidências de norma/licença/célula e assinatura profissional por aplicabilidade |
| G6 | Segurança e QA | Testar usuários reais A/B, 403/404 cross-tenant, imutabilidade de snapshot, RLS, restore e replay sob falha | QA independente com logs e hashes |
| G7 | Orquestrador | Congelar SHA, executar os cinco workflows no mesmo SHA e emitir C08 com aceites segregados | Contrato GC=PASS somente se todos os gates anteriores cumpridos |

## 3. Política de preservação de anomalias
- **10 eventos órfãos de dependência:** manter payload bruto com integridade e referência antiga; carimbo `ORPHAN_HISTORICAL_REFERENCE`, não criar dependência artificial nem descartar. Criado (4), excluído (4), calculado (2).
- **41 pés-direitos <= 0:** preservar `0` como valor legado e classificar altura não fornecida/insuficiente; não preencher automaticamente e não reprovar largura/comprimento que são positivos.
- **4 cargas com tensão fixa nula:** preservar nulo; cálculo condicionado a tensão/ligação informada, sem inferência 127/220/380 V.
- **2 cargas trifásicas:** preservar sinalizador, porém exigir topologia/linha-linha e condições de balanceamento antes de dimensionar.
- **45 colunas sem regra aprovada:** arquivar seu valor integral com rastreabilidade e proibir perda silenciosa na projeção canônica. Não transformar `autor` em identidade Auth.
- **Dados normativos antigos:** armazenar resultado de legado sob `NOT_EVALUATED`; nunca homologar automaticamente ou sobrescrever memória profissional.

## 4. Instruções específicas para E02–E06 (execução futura sujeita a GO específico)
1. Criar ambiente de **homologação isolado**, sem utilizar o Supabase de produção; definir escopo e dados mínimos.
2. Preparar backup da origem e do destino de homologação, confirmar restauração em infraestrutura descartável.
3. Revisar e aplicar, por ferramenta de migration versionada, **A03 → A04 → B04 → C03** apenas ao staging autorizado; conferir manifesto e RLS.
4. Criar/validar contas Auth reais e distintas para A e B; associar explicitamente o usuário proprietário aos cinco projetos; sem valores de UUID artificiais.
5. Exportar a origem com corte consistente e retenção cifrada, revalidar hashes; executar transformação de todos os registros com transação e ledger de reexecução.
6. Testar isolamento A/B inclusive consultas diretas, chamadas API, logs e acesso a artefatos; verificar que `service_role` nunca é exposto ao frontend.
7. Conferir totais e fingerprints do staging, testar rollback e reprocessamento. Produzir relatório de aceites com assinaturas da engenharia elétrica, segurança e responsável.
8. Só então alterar contrato C08 de `BLOCKED` para `PASS`, referenciando evidências autênticas. **GO de produção é distinto e posterior.**

## 5. Execução local segura (somente verificação)
A partir da raiz do repositório, no Python 3.12 com API instalada:
```bash
python -m sie_api.v201_c_migration_preflight
python -m pytest restructuring/apps/api/tests/test_c07_migration_preflight_v201.py restructuring/apps/api/tests/test_c07_source_cutoff_v201.py -q
```
Executar os comandos do pacote Python no ambiente configurado com `restructuring/apps/api` em PYTHONPATH ou instalação `pip install -e restructuring/apps/api`. Os scripts não contêm DSN e não acessam produção.

**Resultado desta rodada:** seleção do usuário registrada e inventário auditado; `GC=BLOCKED` até os G0–G7 comprovados. Nenhuma tarefa automatizada está autorizada a trocar esses statuses por texto autoatribuído.
