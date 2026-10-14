# NOR-01 — Recuperação controlada e inventário documental

**Estado:** BLOQUEIO NORMATIVO ATIVO. **Escopo:** SIE-AUTO-003 (inventário técnico parcial, não certificação). **Fonte do levantamento:** árvore da branch do repositório, leitura de `Arquivos_Diversos/QA_CONFERENCIA_CERTFID_TABELAS_EDP.md`, manifesto dos PDFs comentados e testes de integridade.

## Artefatos identificados no repositório

| Referência | Evidência presente | Classificação técnica | O que ainda falta |
|---|---|---|---|
| EDP PT.DT.PDN.00068 v09 | `Arquivos_Diversos/Norma_EDP/PT.DT.PDN.00068_V9.pdf` | Cópia PDF candidata a fonte primária | Confirmar origem oficial, edição, vigência e comparação de células para cada regra consumida pelo runtime |
| EDP v09 extraída | `Arquivos_Diversos/Norma_EDP/PT.DT.PDN.00068_V9_chunks.json` | Extração secundária | Conferir página, unidade, tabela e correspondência 1:1 com PDF |
| Registro de conferência EDP | `Arquivos_Diversos/QA_CONFERENCIA_CERTFID_TABELAS_EDP.md` | Registro histórico interno | Registro declara comparação em 01/07/2026; não substitui reexecução independente para o novo motor |
| NBR 5410 transcrita | `Arquivos_Diversos/NBR_5410_original/NBR-5410.md` | Transcrição Markdown, **não** documento oficial certificado | Identidade e edição da fonte ABNT, integridade e direitos de uso aplicáveis |
| NBR 5410 chunks | `Arquivos_Diversos/NBR_5410_original/NBR_5410_chunks.json` | Extração secundária | Integridade da extração, verificação das cláusulas e valores originais |
| NBR 5410 comentada | `Arquivos_Diversos/NBR_5410_comentada/chunks_json_16_pdfs_v2/manifesto_processamento.json` | Metadados de extração comentada | Não confundir comentários e dados editoriais com texto normativo primário |

### Bloqueios preservados

1. Fontes oficiais, edição aplicável e permissão de uso precisam ser verificadas para cada módulo antes de importar tabelas no cálculo.
2. O catálogo EDP pode conter linhas transcritas historicamente e ainda ser insuficiente para elegibilidade automática de padrão de entrada. É necessária uma matriz por caso, carga, modalidade e condições.
3. O documento interno `QA_CONFERENCIA_CERTFID_TABELAS_EDP.md` registra que `PT.DT.PDN.03.14.020 v06` não foi localizado naquele levantamento; não afirmar validação dessa fonte.
4. As Tabelas EDP 006/011 têm escopo diferente dos fatores de demanda já implementados; a ausência deve continuar registrada.
5. Os valores genéricos informados pelo cliente na API não são tratados como tabela normativa certificada.
6. A conferência de engenharia deve produzir casos independentes com entradas, unidades, arredondamentos, limites e resultados esperados justificáveis.

## Subtarefa técnica implementada

CLI `python -m sie_api.normative_inventory --root . --output source-manifest.json --require-all`:

- Calcula SHA-256 e tamanho dos seis artefatos existentes, sem transcrever seu conteúdo.
- Distingue `PRESENT_UNVERIFIED` de `MISSING`.
- Impede escape do diretório raiz por travessia de caminhos e links simbólicos.
- Define expressamente `normative_conformity_verified: false` e `repository_approval: false` em todas as saídas.
- GitHub Actions executa a CLI e arquiva manifesto da revisão, sem validar tabelas.

### Critério de conclusão do NOR-01

NOR-01 só poderá sair de BLOCKED quando a matriz de evidências normativas aplicáveis estiver completa, os dados da implementação forem comparados às fontes primárias disponíveis e os casos independentes forem validados. **Inventário de integridade de arquivo não é conferência de conteúdo nem declaração de conformidade.**

## Retomada objetiva

Conferir a saída do workflow da API com o manifesto do SHA e a execução dos testes. Prosseguir pela conferência controlada das tabelas realmente necessárias ao motor; manter os gates de liberação fechados na ausência de fonte primária validada.
