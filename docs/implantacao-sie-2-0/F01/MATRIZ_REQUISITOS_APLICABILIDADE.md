# Matriz de requisitos × aplicabilidade — SIE F01

Origem: F01_EXECUTAR.md tasks 01.01–01.10, F00 (37 LEGACY-IDs; 16 lacunas formais) e fontes editoriais oficiais identificadas em 15/10/2026. **Escopo ainda em validação**, não homologação.

## Contexto de seleção

| Tipologia | Projeto BT | SPDA (NBR 5419) | Segurança NR-10 | EDP entrada SP | Fora do escopo/condição |
|---|---|---|---|---|---|
| Residencial | CANDIDATO | CONDICIONAL: análise técnica de risco | CONDICIONAL: atividades e instalações | CONDICIONAL: distribuidora, concessão e vigência | Média/alta tensão, indústria, GD sem recorte |
| Comercial | CANDIDATO | CONDICIONAL: análise técnica de risco | CONDICIONAL: atividades e instalações | CONDICIONAL: distribuidora, concessão e vigência | Sistema de potência, instalações especiais |
| Predial | CANDIDATO | CONDICIONAL: análise técnica de risco | CONDICIONAL: atividades e instalações | CONDICIONAL: distribuidora, concessão e vigência | SPDA sem estudo de risco, outras concessionárias |
| Industrial | FORA DO RECORTE DO PROTÓTIPO | PENDENTE RECORTE | PENDENTE RECORTE | PENDENTE | Não inferir inaplicabilidade da norma na engenharia real |

*As categorias acima definem o produto/protótipo, não dispensam obrigações legais.* A API consulta metadados com `NAO_APLICAVEL`, `PENDENTE` ou `BLOQUEADO`, jamais `APROVADO`.

## Requisitos com MoSCoW, origem, proprietário e aceite

| ID | Tipo | Pri. | Regra/escopo | Origem | Responsável (função) | Aceite/evidência |
|---|---|---|---|---|---|---|
| RF-001 | RF | Must | Capturar tipologia válida | F01.01/F00 | Produto | HTTP 422 para tipologia fora do recorte; test_wrong_typology_rejected_at_api_boundary |
| RF-002 | RF | Must | Consultar catálogo sem validar cálculo | F01.03 | Backend | GET /api/v1/normas/catalogo sem valores nem aprovação; test_catalog_remains_unverified |
| ENG-001 | ENG | Must | Contexto UF, distribuidora, data, tensão | F01.05 | Engenharia | Exclusão EDP por UF/distribuidora, transição NR10; tests de aplicabilidade |
| NOR-001 | NOR | Must | Metadados/proveniência de cada fonte | F01.03/F00 | Governança normativa | Catálogo v2 com origem, edição, hash ou lacuna e status |
| NOR-002 | NOR | Must | Célula: fonte primária, referência, linha/coluna, unidade, dois conferentes | F01.04 | Engenharia/QA | Zero células liberadas antes da dupla conferência; matriz em REGISTRO_REGRAS_NORMATIVAS |
| NOR-003 | NOR | Must | Transição editorial/vigência e jurisdição | F01.07/NR10 | Engenharia normativa | Casos 2026/2027; transição para instalações existentes pendente |
| SEG-001 | SEG | Must | Cliente não autoaprova conteúdo | F01.09 | Segurança/backend | Request extra='approved' 422; gate false; test_unknown_evidence_flags_are_rejected |
| SEG-002 | SEG | Must | Não permitir regras fora do recorte | F01.05 | Segurança/backend | Tipologias e EDP fora da UF/rede excluídas; testes |
| RNF-001 | RNF | Must | Preservar revisão por projeto imutável | F01.06 | Arquitetura/dados | PENDENTE: projeto/versionamento com evidência, sem migração em produção |
| RNF-002 | RNF | Must | Eventos/regras históricos auditáveis | F01.06/07 | Dados | PENDENTE: storage, hash, diff e trilha de transição |
| UX-001 | UX | Should | Status claro com motivos e revisão | F01.09 | UX/frontend | Endpoint retorna motivos, integração visual E2E PENDENTE |
| ENG-002 | ENG | Must | Casos de valores elétricos independentes | F01.08 | Engenharia/QA | BLOQUEADO: fonte primária e expected numérico conferido |
| NOR-004 | NOR | Must | Política de conflitos por edição | F01.07 | Engenharia normativa | PENDENTE: decisão manual versionada; sem precedência automática |

## Preservação do legado

O baseline F00 identifica ENG-001 (Iz arredondado antes da seleção de disjuntor) e ENG-002 (EDP U/D com carga trifásica), além de SQL/RLS e tabela personalizada. **Não corrigir o golden original por reescrita de expectativas.** Esses itens são riscos abertos para incremento específico, não validações normativas desta matriz.

Tasks F01.01–F01.03: trabalho estrutural verificável. F01.04, F01.06–F01.08, F01.10: parciais/bloqueadas até verificação documental e persistência.
