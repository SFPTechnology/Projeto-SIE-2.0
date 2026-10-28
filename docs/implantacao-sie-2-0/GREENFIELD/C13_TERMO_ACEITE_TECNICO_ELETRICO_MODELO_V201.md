# C13 — Termo de avaliação e aceite técnico elétrico — MODELO NÃO ASSINADO

**Projeto:** SIE 2.0 · **Bloco:** C · **Finalidade:** avaliação técnica das funcionalidades de cálculo e regras elétricas implementadas no software.
**Número do termo:** [A DEFINIR] · **Data de decisão:** [A PREENCHER] · **Versão:** 1.0.
**Estado de emissão:** MODELO PARA REVISÃO, SEM APROVAÇÃO, SEM ASSINATURA.

## 1. Identificação do profissional
- Nome civil/profissional: **[A PREENCHER]**
- Título profissional conforme CREA: **[A PREENCHER]**
- Registro CREA/UF: **[A PREENCHER]**
- Número/protocolo da certidão de registro e quitação: **[A PREENCHER]**
- Número/protocolo da certidão de atribuições: **[A PREENCHER]**
- Resultado da validação de registro/atribuições: **[NÃO VERIFICADO / VERIFICADO / INAPTO]**
- ART: **[PENDENTE DE ENQUADRAMENTO / NÚMERO E REFERÊNCIA / NÃO EXIGÍVEL COM FUNDAMENTO DOCUMENTADO]**
- Revisor independente (caso designado): **[A PREENCHER]**

**Condição:** sem comprovação de habilitação e atribuições compatíveis, não emitir aceite profissional.

## 2. Objeto delimitado e exclusões
Objeto: verificar a implementação, precisão, segurança de bloqueios e rastreabilidade dos motores elétricos C03–C05 e do histórico eletrotécnico C07, conforme requisitos e normas **efetivamente comprovados** na data/versão do parecer.

**Este documento não atesta:**
- aprovação de projeto elétrico de obra específica ou de instalação física;
- execução, inspeção, comissionamento, medição e conformidade de instalação real;
- conformidade integral com toda norma apenas porque a norma foi citada;
- módulos não implementados, fora do escopo autorizado ou testes não executados;
- migração de dados, RLS, backup/restore ou implantação em produção.

## 3. Identificação inequívoca da versão avaliada
- Repositório: https://github.com/SFPTechnology/Projeto-SIE-2.0
- PR: https://github.com/SFPTechnology/Projeto-SIE-2.0/pull/11
- Branch e commit SHA final: **[A PREENCHER APÓS CONGELAMENTO]**
- Versão do catálogo normativo / hash: **[A PREENCHER]**
- Versão das regras da concessionária / evidência de aplicação: **[A PREENCHER]**
- Ambiente de teste e identificador do snapshot: **[A PREENCHER]**
- Documento C11 e dossiê C12: **[VERSÃO E SHA A PREENCHER]**
- Hash do manifesto de evidências: **[A PREENCHER]**

## 4. Resultado dos ensaios
| Grupo | Resultado a preencher |
|---|---|
| E01 Iluminação e TUG | [NÃO AVALIADO / APROVADO / REPROVADO / APROVADO COM RESTRIÇÕES] |
| E02 TUE, FP e topologia | [NÃO AVALIADO / APROVADO / REPROVADO / APROVADO COM RESTRIÇÕES] |
| E03 Demanda e circuitos | [NÃO AVALIADO / APROVADO / REPROVADO / APROVADO COM RESTRIÇÕES] |
| E04 Condutores e correções | [NÃO AVALIADO / APROVADO / REPROVADO / APROVADO COM RESTRIÇÕES] |
| E05 Queda de tensão e Rca/XL | [NÃO AVALIADO / APROVADO / REPROVADO / APROVADO COM RESTRIÇÕES] |
| E06 Proteção Ib/In/Iz/I2 e curto-circuito | [NÃO AVALIADO / APROVADO / REPROVADO / APROVADO COM RESTRIÇÕES] |
| E07 DR e DPS | [NÃO AVALIADO / APROVADO / REPROVADO / APROVADO COM RESTRIÇÕES] |
| E08 Aterramento, neutro e PE | [NÃO AVALIADO / APROVADO / REPROVADO / APROVADO COM RESTRIÇÕES] |
| E09 Normas da concessionária | [NÃO AVALIADO / APROVADO / REPROVADO / APROVADO COM RESTRIÇÕES] |
| E10 Sete campos elétricos legados | [NÃO AVALIADO / APROVADO / REPROVADO / APROVADO COM RESTRIÇÕES] |
| E11 Regressão, negativos, versionamento | [NÃO AVALIADO / APROVADO / REPROVADO / APROVADO COM RESTRIÇÕES] |

## 5. Parecer técnico fundamentado
**Metodologia aplicada:** [DESCREVER CALCULOS INDEPENDENTES, FONTES, AMOSTRAGEM E LIMITES].

**Principais resultados e evidências:** [DESCREVER, SEM INFERIR CONCLUSÕES DE TESTES NÃO FEITOS].

**Não conformidades detectadas e tratamento:** [LISTAR NC, CRITICIDADE, CORREÇÕES, REENSAIOS, RESTRIÇÕES].

**Limitações e módulos bloqueados:** [DESCREVER COMO A INTERFACE/API IMPEDE USO INSEGURO].

**Fontes normativas efetivamente consultadas, edição e aplicabilidade:** [DESCREVER E ANEXAR REFERÊNCIAS].

## 6. Decisão — assinalar APENAS APÓS avaliação
- [ ] **APROVADO NO ESCOPO EXATO DECLARADO**, com todos os requisitos obrigatórios avaliados e sem pendências impeditivas.
- [ ] **APROVADO COM RESTRIÇÕES EXPLICITADAS**, desde que os controles técnicos impeçam uso das funções não homologadas; listar restrições, evidências e critério de acompanhamento.
- [ ] **REPROVADO**, detalhando não conformidades impeditivas.
- [ ] **NÃO AVALIADO / EVIDÊNCIA INSUFICIENTE**.

**Decisão padrão deste MODELO: NÃO AVALIADO.** Nenhuma caixa foi assinalada.

**Efeito da decisão:** aceite profissional restrito ao objeto efetivamente testado. A decisão **não autoriza sozinha GC=PASS**, migração real, publicação, alteração de banco, deploy ou merge. Estes requerem gates de engenharia de software e homologação independentes.

## 7. Declaração de responsabilidade — assinar somente após revisão
“Declaro que examinei pessoalmente o escopo e as evidências identificados neste instrumento; que minha habilitação e atribuições profissionais são compatíveis com a atividade efetivamente assumida; e que o parecer acima expressa exclusivamente os ensaios, limitações e resultados efetivamente verificados. Os requisitos não avaliados permanecem sem aceite.”

- Local e data: **[A PREENCHER]**
- Nome e assinatura digital verificável: **[A PREENCHER]**
- Identificação do certificado, plataforma e referência de verificação: **[A PREENCHER]**
- Número da ART, quando exigível, ou fundamento para não aplicabilidade: **[A PREENCHER]**
- Hash SHA-256 do instrumento assinado: **[A PREENCHER]**

**Sem assinatura / sem dados preenchidos: este arquivo é apenas um MODELO e não representa manifestação pessoal do profissional.**
