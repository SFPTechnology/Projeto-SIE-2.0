# C20 — Continuidade GREENFIELD e diagnóstico verificável

Data: 04/11/2026. Baseline inspecionado: `bdf302b0f5226a0d1af05eb8fd38bb4f5b9cf9b1`.
Branch: `feat/v201-bloco-c-dominio-eletrico`; PR #11 aberta, não draft, base Bloco B. Sem merge.

## Resultado da inspeção

C19 e scripts C16/C18 já excluíam a importação dos cinco projetos do GC. C08 ainda exibia blockers históricos como ativos; este incremento os arquiva e publica os quatro grupos atuais. C04/C05 e C12 explicitam E10 legado como diferido. Nada foi importado ou alterado no legado.

Supabase destino: consulta somente leitura confirmou ACTIVE_HEALTHY, PG17.11, somente migration GF02 `20261027195557`, nove tabelas public com RLS e dezesseis policies. A03 (0/4 índices), A04 (coluna lifecycle_state ausente), B04 (idempotency_key ausente) e C03 (0/10 tabelas) permanecem não aplicadas. Policies usam proprietário e UPDATE de projeto contém USING/WITH CHECK. Isso não comprova sessão A/B.

Advisor de segurança: proteção contra senhas vazadas desativada; nenhuma mudança/custo autorizado por este relatório. Performance: dez FKs sem índice e oito índices ainda não usados; avaliar plano representativo antes de acrescentar índices.

## Implementações desta rodada

1. Auth browser: geração assíncrona impede login pendente de reabrir sessão após logout; resposta de refresh antiga não derruba login novo; logout HTTP malsucedido deixa de indicar revogação confirmada.
2. Testes Node VM executam JS real com transporte sintético. Teste falha contra implementação anterior e passa com correção. Não substitui Supabase Auth real.
3. C18: recusa C17 é uma restrição respeitada. Bloqueio ativo passa a indicar alternativa de recuperação ainda não comprovada; flags artificiais não concedem GO.
4. PG17: quatro falhas injetadas após A03/A04/B04/C03, comparação de dados, catálogo, grants, RLS e funções, seguida de reaplicação integral. Workflow C03 executa prova em banco descartável exclusivo, nunca no destino.

**Limite da prova PG17:** rollback de transação que falha antes do commit. Não demonstra recuperação pós-commit no Supabase, nem autoriza DDL remoto.

## O que falta para concluir o Bloco C

| Frente | Pendência efetiva |
|---|---|
| Schema | Salvaguarda operacional alternativa comprovada, revisão de segurança/drift, aplicação A03/A04/B04/C03 e readback no destino |
| Auth | Login, renovação, expiração/revogação e isolamento real A/B; access tokens podem continuar válidos até expiração |
| E01 | Integração dos mínimos iluminação/TUG por tipologia, área/perímetro e golden independente |
| E02 | Validar FP, topologia, tensões e unidades com contraprovas |
| E03 | Fatores oficiais, divisão de circuitos e balanceamento |
| E04 | P06, métodos, materiais, temperatura/agrupamento e tabelas homologadas |
| E05 | Rca/XL com fonte autorizada e limites/condições reais |
| E06 | I2, Icc, capacidade de interrupção, curva e seletividade |
| E07 | Dimensionamento/coordenação DR/DPS com evidência normativa |
| E08 | TT/TN/IT, PE/N e proteção contra choque com evidência normativa |
| E09 | Regras completas concessionária, versão e proveniência por célula |
| E10 | Legado diferido; não bloqueia GREENFIELD |
| E11/C13 | Contraprovas, rastreabilidade final, integração e aceite profissional autêntico |
| QA final | Cinco workflows PASS no SHA final; integração e desempenho representativos no ambiente aplicável |

As lacunas acima derivam de `v201_c_calculation.py`, `v201_c_explicit_checks.py`, `v201_c_e01_e11_evidence.py` e da seção H do C12. Não foram inventados dados de normas ou aceites para preencher essas lacunas.

## Evidências de validação

Baseline: cinco workflows PASS no mesmo SHA: runs 41916449901 (C03), 41916449849 (API), 41916449854 (A03/A04), 41916449853 (AIOX), 41916449862 (Chromium).

Execução local desta rodada: pytest integral coletado durante auditoria — 1475 passed, 13 skipped; testes dirigidos após finalização dos novos arquivos — 17 passed, 4 skipped (PG17 ausente). Lint, typecheck, testes e build raiz PASS após instalar dependências do lockfile. Os quatro testes PG17 exigem confirmação pelo Actions do novo commit; resultados devem ser consultados no SHA publicado.

GC=BLOCKED. Sem escrita remota, C17, importação, merge, deploy, alteração em main/F12/produção ou homologação elétrica fictícia.


Workflow dispatch: commit publicado via GitHub Contents API para iniciar a validação do SHA final.
