# F12 — dossiê para decisão profissional, de mudança e go-live

**Estado institucional atual:** `NO-GO / HUMAN_REQUIRED`; registrado também em [issue de governança #7](https://github.com/SFPTechnology/Projeto-SIE-2.0/issues/7).

## 1. Itens comprovados para desenvolvimento
- Handoff F11 SHA `11643cf3ad7da2e6182183c6071148f924bfe741`: CI de software local validada na fase anterior.
- SHA de código F12 testado: `d7b55a7f3a8ec3eb15ff06a9478b8936134f61ad`, sem alteração de motores normativos, bases de produção ou `main`.
- GitHub Actions: API **1210 passed / 1 warning** `40248897962`; Chromium **36 passed** `40248897906`; AIOX lint/typecheck/test/build `40248897831`; F12 safety **8 + 19 passed** `40248897899`.
- Pacote QA local `sie-f12-local-qa.tar.gz`: 127 arquivos; SHA-256 de exemplo do SHA de código: `6e29e1f980d50b4a0d394d863915f6660bfba029a1b797eff0f85deebc7bdcfa`. Duas builds byte a byte idênticas; recusa de checksum adulterado testada. Cada novo SHA (inclusive documentação) exige nova geração/checksum.
- HTTPS local com certificado efêmero e ambiente `SIE_ENV=production`: health e validação estrutural verificadas, persistência local 503; **não significa autenticação real, TLS público ou segurança de produção**.
- SQLite F03 e arquivos F05/F10: 19 testes de upgrade/downgrade, restore e falhas usando fixtures; **não representam volume, infraestrutura ou dados reais**.

## 2. Aprovação que não pode ser fabricada por automação
| Gate | Prova mínima e autoridade | Estado |
|---|---|---|
| G02 — Engenharia | fontes, casos de cálculos independentes, condições de uso e engenheiro habilitado/ART pertinente, conforme finalidade | BLOQUEADO para alegar conformidade |
| G03 — Ambiente/IAM | plataforma SIE definida, OIDC/MFA/ACL/RBAC/RLS conforme banco, autenticação por projeto e ensaios de IDOR | HUMAN_REQUIRED |
| G04/G05 — Dados | RPO/RTO acordados, snapshot antes, migração em cópia representativa, restore + hash e rollback verificados | PARCIAL apenas sintético |
| G06 — Operação | DNS/TLS e renovação, métricas, alertas, escopo de logs, equipe e suporte real | PENDENTE |
| G07 — Release | dependências fixadas, imagem/binário reproduzível, assinatura/SBOM, smoke de homologação e E2E por papéis | PARCIAL local |
| G08 — Mudança | ticket, aprovador designado, custos, janela, impacto, comunicação e GO explícito sobre alvo identificado | HUMAN_REQUIRED |
| G09/G10 — Rollout | backup/rollout progressivo, monitoramento, rollback e decisão pós-deploy em produção | NÃO EXECUTADOS |

## 3. Registro esperado do aprovador (não preenchido artificialmente)
- Ambiente e owner do projeto SIE / URL e conta de infraestrutura:
- Escopo legal/profissional pretendido: consultivo local ou uso real com validação elétrica:
- Planilha de riscos assinada, engenheiro habilitado e ART/parecer quando aplicável:
- Gestor de mudança e autorizador, ID da solicitação, impacto, custo e janela:
- Resultado G01–G08 no SHA/tag exato, prova restore/migração, ambiente de homologação e ferramentas de monitoramento:
- Ato formal GO/NO-GO e assinatura/fonte de evidência:
- Pós-deploy, tempos/indicadores, reversões e aceite de saúde:

**Política:** ao faltar qualquer campo essencial, continuar com testes e documentação independentes, mas não executar deploy ou migração em ambiente real; o consentimento geral para automação não cria identidade de ambiente, laudo habilitado nem aprovação institucional.
