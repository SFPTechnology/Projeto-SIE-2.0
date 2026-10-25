# Manual do usuário iniciante — SIE 2.0 (F12)

**Edição de testes locais.** Esta edição é instrumento consultivo de engenharia, não software de cálculo normativamente homologado ou plataforma disponibilizada a clientes.

## Acesso e segurança
1. Inicie a instalação local seguindo `restructuring/docs/MANUAL-OPERACIONAL.md`; mantenha API e navegador em loopback (`127.0.0.1`).
2. Confira o indicador de API conectada. Não exponha token local em print, suporte público, captura ou código.
3. Use dados de demonstração e confirme unidade, norma/edição/fonte e revisão de cada entrada. Não interprete o sistema como verificador automático de ART, NR-10 ou concessionária.
4. Salve projeto local e identifique `project_id`, `revision_id` e `calculation_run_id` quando o fluxo mostrar esses dados.
5. No fluxo F10, abra **Artefatos F10 e planta**, informe token, projeto e execução, selecione **Abrir geometria e histórico**. Confirme versão, revisão, documentos e histórico. Resultado deve estar íntegro e `CURRENT` antes de usar apenas como evidência de teste.
6. Se for exibido `STALE`, ocorreu alteração que tornou a publicação anterior obsoleta. Execute a revisão/recálculo no projeto e gere artefato novo; nunca distribua o antigo como vigente.
7. Consulte o relatório técnico e preserve versão e fontes. Confirme visualmente diagramas, grandezas, condutores e proteção com o engenheiro responsável.

## Erros usuais
- **API desconectada:** confirmar terminal/API e porta de loopback, nunca substituir por servidor público não aprovado.
- **401/403:** token de teste ausente ou inválido; não compartilhe token com suporte.
- **Documento não abre / integridade inválida:** interromper, preservar evidências sanitizadas e solicitar revisão ao administrador; não editar manifesto manualmente.
- **Regra sem fonte verificada / pendente:** cálculo consultivo não autorizado para instalação real. Não alterar o status por conta própria.

## Solicitação de suporte
Informe tela, ação, horário (incluindo fuso), versão/SHA, mensagem de erro, ID não sensível e passos para reproduzir com dados fictícios. Remova tokens, CPF, endereço real, dados do cliente, credenciais e relatórios sigilosos antes do envio.

## Limite técnico obrigatório
A F11 foi validada para **QA do software local**. Uso real de instalação exige projeto específico, normas vigentes, validação independente, inspeção/ensaios pertinentes e responsabilidade técnica. F12 ainda não autorizou produção.
