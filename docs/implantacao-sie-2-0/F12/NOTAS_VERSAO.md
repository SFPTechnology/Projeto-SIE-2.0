# Notas da F12 — candidato de preparação, sem release público

## O que foi acrescentado ao desenvolvimento
- Rastreabilidade explícita do candidato F11 ao SHA Git e manifesto JSON com flags `false` para produção, homologação profissional, deploy e aprovação de mudança.
- Validador `scripts/f12_release_gate.py` sem acesso a secrets, dados reais, nuvem ou operação destrutiva; exige ancestor Git, F11 DONE e documentos; pedido `--require-production` é recusado.
- Testes adversariais e workflow CI com permissões `contents: read` e sem ação de deploy.
- Guias para responsável, operador e usuário; checklist GO/NO-GO, rollback, incidentes e revisão normativa.

## O que permanece do SIE 2.0 F11
Projeto local de único proprietário, análise consultiva F09/F10, documentos e snapshots persistidos, avaliação de obsolescência, exportações e backup/restore offline multi-raiz. Limites da F11 continuam válidos. A nova documentação não altera motores, tabelas, cálculos nem banco.

## Não incluído
Liberação de domínio público, migração de clientes reais, autenticação/ACL multiusuário de produção, chaves/secrets, infraestrutura observável real, inspeção de instalação elétrica e atestado de normas/concessionária. Não recomendar publicação externa baseada apenas neste candidato.

## Condição de atualização
Qualquer mudança de código, dependência, banco, regra, template ou infraestrutura exige novo SHA, testes, manifesto atualizado e QA proporcional. Releases históricos devem manter edição e snapshot das regras que efetivamente usaram.
