# Matriz preliminar de requisitos e aplicabilidade — F01

**Não homologada**. Instalações residenciais, comerciais e prediais são tipologias candidatas, não funcionalidades auditadas. Regras de SPDA, NR-10 e distribuidora são condicionais; outras tipologias pendentes de definição.

| ID | Categoria | MoSCoW | Requisito | Critério de aceite | Verificação |
|---|---|---|---|---|---|
| RF-001 | RF | Must | Identificar tipologia e limites | Tipologia incompatível não seleciona regra | `test_wrong_typology` |
| NOR-001 | NOR | Must | Proveniência e vigência da fonte | Ausência bloqueia seleção | `test_source_unverified_blocks` |
| ENG-001 | ENG | Must | Filtro por UF, distribuidora, tensão e material | Regra incompatível não aplica | `test_wrong_distributor` |
| SEG-001 | SEG | Must | Bloqueio conservador | Ausência de aprovação bloqueia | `test_unapproved_blocks` |
| RNF-001 | RNF | Must | Snapshot de regra por projeto | Revisão/hash ficam vinculados ao projeto | `test_revision_snapshot` |
| UX-001 | UX | Should | Pendência transparente | UI distingue bloqueio de elegibilidade | PENDENTE_UI |
| NOR-002 | NOR | Must | Conferência independente de células | Fonte, unidade, linha, coluna e dupla revisão | PENDENTE_FONTE |

Origem: F01_EXECUTAR.md tasks 01.01–01.10. Responsável: engenharia + produto + segurança, atribuição nominal pendente. Não há tabela normativa homologada.
