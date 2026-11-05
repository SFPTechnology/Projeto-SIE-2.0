# C13 — Preparação para homologação profissional

**Estado:** `C13=NOT_SIGNED`  
**Escopo:** preparação documental do Bloco D; não constitui homologação elétrica, aceite profissional ou liberação operacional.

## 1. Base documental

| Documento | Uso nesta preparação | Estado |
|---|---|---|
| C11 — Procedimento de validação profissional | critérios e sequência de revisão | disponível |
| C12 — Dossiê de validação e evidências elétricas | organização das evidências E01–E11 | disponível |
| C13 — Termo de aceite técnico elétrico | instrumento de aceite | modelo sem assinatura |

## 2. Matriz de revisão E01–E11

| Engine | Evidência matemática/teste | Fonte normativa | Pendência de análise profissional |
|---|---|---|---|
| E01 | contratos e testes sintéticos C22 | fonte aplicável a iluminação/TUG ainda deve ser confirmada | validar parâmetros, hipóteses e casos reais |
| E02 | validação sintética de tensão, corrente e topologia | fonte normativa verificável necessária | conferir unidades e topologias |
| E03 | demanda e balanceamento rastreáveis em dados sintéticos | fatores versionados devem ser confirmados | aprovar fatores e aplicação |
| E04 | seleção fail-closed e rejeição de célula ausente | tabelas normativas versionadas necessárias | confirmar método de instalação, temperatura e agrupamento |
| E05 | queda de tensão com ausência de Rca/XL distinguida de zero | tabelas/células Rca e XL necessárias | validar limites e hipóteses |
| E06 | proteção e estados incompletos cobertos por testes | fonte normativa aplicável necessária | revisar Ib/In/Iz, I2, Icc e seletividade |
| E07 | DR/DPS com estados PASS/FAIL/PENDING_EVIDENCE | fonte normativa aplicável necessária | validar dimensionamento e aplicação |
| E08 | topologias TT/TN/IT e condutores tratados sinteticamente | fonte normativa aplicável necessária | revisar proteção contra choque e equipotencialização |
| E09 | catálogos versionados e origem rastreável | documentos de concessionária aplicáveis | confirmar vigência e células |
| E10 | preservação de campos históricos | decisão C19 | `DEFERRED_OPTIONAL_LEGACY_IMPORT_ONLY`; não revisar como requisito GREENFIELD |
| E11 | hashes, integridade e bloqueio de aprovação forçada | política de evidências do projeto | revisar cadeia de custódia e alterações |

## 3. Separação de evidências

- **Evidência matemática/teste:** resultados reproduzíveis dos testes sintéticos e descartáveis, sem equivaler a conformidade normativa.
- **Fonte normativa verificável:** documento, edição, seção/tabela e célula que deverão ser confirmados antes de qualquer aceite.
- **Análise profissional:** julgamento do engenheiro responsável sobre hipóteses, aplicabilidade, limites e resultados.
- **Aceite:** permanece pendente até assinatura/manifestação autêntica no instrumento C13.

## 4. Limitações e controles

Não foram inventados CREA, ART, assinatura, parecer, fonte normativa ou aprovação. Nenhuma operação remota, homologação elétrica, importação legada ou Auth real faz parte desta preparação. O estado de GC permanece `BLOCKED`.

## 5. Checklist para futura revisão

1. Conferir cada entrada, unidade, fórmula e resultado.
2. Vincular fonte normativa primária, edição e referência.
3. Registrar hipóteses e limitações por caso.
4. Reproduzir testes positivos, negativos e golden.
5. Emitir parecer profissional separado da evidência automatizada.
6. Preencher e assinar C13 somente após a revisão competente.
