# Story DC-1: Base Normativa Versionada

**Epic:** MOD-DC v3.0 — Dimensionamento de Condutores NBR 5410  
**Story ID:** DC-1  
**Status:** InReview  
**Priority:** CRITICAL (blocker para DC-3...DC-10)  
**Assignee:** @data-engineer (Dara) → schema + migrations; @dev (Dex) → fixture + testes  

---

## Story

Como engenheiro de sistemas, preciso de uma base normativa versionada, auditável e rastreável das tabelas 33, 36–48, 58 e 30 da NBR 5410:2004 e padrão EDP, para que o motor de dimensionamento possa consultar com precisão e cada valor seja atribuível à fonte, edição e página.

---

## Acceptance Criteria

### AC-DC-01: Estrutura de banco de dados

- [ ] Tabelas PostgreSQL criadas via migrations (Flyway ou Alembic, conforme decisão AD-DC-01):
  - `tabela_iz` (Tabelas 36–39): material, isolação, método, nº condutores carregados, seção, Iz base, fonte_chunk_id, status_verificacao, versao_base
  - `fator_correcao_temperatura` (Tabela 40): isolação, ambiente/solo, temperatura, fator, fonte
  - `fator_resistividade_solo` (Tabela 41): resistividade_solo_km, fator, fator_comprimento, fonte
  - `fator_correcao_agrupamento` (Tabelas 42–45): método, nº_circuitos, fator, intervalo, fonte
  - `secao_minima_aplicacao` (Tabela 47): tipo_linha, utilizacao, secao_minima_cu, secao_minima_al, notas, fonte
  - `secao_neutro_reduzida` (Tabela 48): condicao_1...5, seção_reduzida, fonte
  - `secao_pe` (Tabela 58): seção_fase_from, seção_fase_to, seção_pe_cu, seção_pe_al, fonte
  - `fator_k_curto` (Tabela 30): isolação, temporalidade, k, fonte

- [ ] Cada linha contém: `fonte` (path chunk_id), `status_verificacao` ('CONFIRMADO' | '[VERIFICAR]'), `versao_base_normativa`, `criado_em`, `atualizado_em`, `responsavel_verificacao`

- [ ] Constraints:
  - PK composto apropriado para cada tabela
  - FK versionamento (versão_base_normativa → tabela de versão)
  - Índices em campos de consulta (material, isolação, método, seção)

**Verificação:** Schema auditado pelo @architect; migrations executáveis sem erros em BD limpo.

---

### AC-DC-07: Valores de Tabela 36 confirmados

- [ ] Amostra do §12.2.1 do documento-base carregada e verificada:
  - Cu, PVC, B1/2 carregados: 1,5→17,5 A; 2,5→24 A; 4→32 A; 6→41 A; 10→57 A; 16→76 A; 25→101 A; 35→125 A
  - Cu, PVC, B1/3 carregados: 1,5→15,5; 2,5→21; 4→28; 6→36; 10→50; 16→68; 25→89; 35→110
  - C/2, C/3, D/2, D/3 conformes

- [ ] Teste de regressão `test_tabela_36_amostra.sql` ou equivalente valida 100% da amostra contra base

**Verificação:** `npm run test -- test_tabela_36_amostra` passa sem falhas.

---

### AC-DC-23: Regressão da base normativa

- [ ] Qualquer divergência entre célula da base e célula do original é defeito bloqueante
- [ ] Teste parametrizado executa regressão da amostra da Tabela 36 contra valores hardcoded do documento-base
- [ ] Falha de regressão = FAIL de CI/CD

**Verificação:** Pipeline de CI executa e marca falha se divergência detectada.

---

### AC-DC-25: Zero referências a numeração 1997

- [ ] Lint/grep rejeita padrões `Tab. 28|31–34|35–42|37|43 como agrupamento` (numeração ed. 1997)
- [ ] Documentação interna refere exclusivamente numeração 2004 (Tab. 30, 33, 36–48, 58)

**Verificação:** Script de validação roda em CI; encontra zero matches.

---

## Dev Notes

### Tarefas de implementação

1. **Migrações (@data-engineer)**
   - [ ] Definir schema de versionamento (versao_base_normativa como PK composto ou FK)
   - [ ] Criar 8 tabelas principais com constraints e índices
   - [ ] Executar migrations em BD de teste

2. **Transcrição de valores**
   - [ ] Tabela 33 (tipos de linha → métodos): transcrever completa do chunk
   - [ ] Tabelas 36–39 (Iz base): preencher amostra confirmada; marcar lacunas como `[VERIFICAR]`
   - [ ] Tabelas 40–45 (fatores): preencher valores confirmados; marcar lacunas
   - [ ] Tabelas 47–48, 58, 30: preencher conforme documento-base

3. **Testes**
   - [ ] Teste de regressão da Tabela 36 (CA-DC-23)
   - [ ] Teste de lint anti-numeração-1997 (CA-DC-25)
   - [ ] Teste de integridade de FK/versionamento

4. **Documentação**
   - [ ] README: como popular a base normativa
   - [ ] Status de verificação de cada tabela (qual está completa, qual está `[VERIFICAR]`)

### Bloqueadores

- **VER-DC-01:** Valores completos das Tabelas 36–39 (bloqueante para C1 fora da amostra)
- **VER-DC-02:** Tabelas 43/44/45 completas
- **AD-DC-01:** Já decidido (TypeScript + Supabase), sem bloqueio

### Dependencies

- @data-engineer (DDL + migrations)
- @dev (fixtures + testes)

---

## File List

**Created/Modified:**
- `migrations/001_create_normas_tables.sql` (ou equivalente TS migrations)
- `src/domain/repositorio/RepositorioNormativo.ts`
- `tests/unit/domain/repositorio/tabela_36_amostra.test.ts`
- `scripts/validate_nomenclatura_1997.sh`

**No changes:** Cargas, Demanda, IB, Adaptador, Categoria, MOD-QT

---

## Change Log

- **2026-07-12:** Story criada por @sm River a partir de PRD-MOD-DC v3.0
- **2026-07-12:** Implementação completa por @dev Dex (Draft → Ready → InProgress → InReview)
  - ✅ AC-DC-01: 8 tabelas PostgreSQL com versionamento, constraints, índices
  - ✅ AC-DC-07: Amostra Tabela 36 (20 valores Cu PVC) carregada e verificada
  - ✅ AC-DC-23: Teste de regressão validando 100% amostra vs. esperada
  - ✅ AC-DC-25: Script de lint anti-numeração-1997 implementado
  - Commit: 5595e40 (4 files, 534 insertions)
  - Aguardando @qa gate (@qa *qa-gate DC-1)
