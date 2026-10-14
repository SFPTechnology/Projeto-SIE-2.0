# DEPENDENCY_GRAPH — dependências verificáveis

```mermaid
flowchart TD
    ST[SQLite local + testes existentes] --> CLI[SIE-AUTO-001 CLI local]
    AIOX[AGENTS.md + Constitution] --> CLI
    AIOX --> GATES[SIE-AUTO-002 quality gates]
    API[FastAPI + UI atuais] --> E2E[SIE-AUTO-005 E2E]
    ST --> E2E
    CLI --> E2E
    DOCS[Documentos ABNT / EDP] --> NOR[SIE-AUTO-003 evidência normativa]
    NOR --> ENG[SIE-AUTO-007 motores completos]
    CALC[Primitivas do domínio] --> ENG
    ENG --> REL[SIE-AUTO-008 memoriais e diagramas]
    AUTH[SIE-AUTO-006 identidade e dados] --> REL
    REL --> FINAL[SIE-AUTO-009 documentação / UX final]
    E2E --> FINAL
    GATES --> RELEASE[SIE-AUTO-010 revisão de liberação]
    FINAL --> RELEASE
```

## Dependências inspecionadas
- SQLite (`sie_api/storage.py`) opera sem API e sem rede: predecessor real de CLI.
- API opcional (`storage_api.py`) opera com token local e não é identidade de produção.
- `domain/engines.py` implementa exemplos resistivos; evidências normativas completas não são demonstradas por essas funções.
- Fonte EDP registrada em `Arquivos_Diversos/QA_CONFERENCIA_CERTFID_TABELAS_EDP.md`, com lacunas de abrangência declaradas pelo documento; catálogo técnico não é elegibilidade aprovada.
- O gate normativo não pode migrar para APROVADO por simples entrada da UI.

## Política de transição
Somente promover PREDECESSOR a satisfeito quando houver arquivo verificável + testes adequados. Mocks, exemplos e tabelas provisórias **não** satisfazem gates normativos.
