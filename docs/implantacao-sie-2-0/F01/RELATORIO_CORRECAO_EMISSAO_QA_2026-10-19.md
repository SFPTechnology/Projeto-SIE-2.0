# F01 — Correção de emissão e diagnóstico Copilot

Run observado: https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39285814051, baseline `70ae61a495447e52a78db64a04e1bb49aa23d283`.

Os três processos CLI terminaram com exit 0, mas o gate recusou a ausência de `qa3-runs/QA-XX/PARECER_QA.md`. Nenhum artefato de parecer foi encontrado e as revisões cruzadas não executaram. Exit 0 não comprova entrega nem revisão. Os streams anteriores estavam em RUNNER_TEMP e não foram arquivados; a causa raiz exata não pode ser afirmada retrospectivamente.

Conflito concreto corrigido: perfis pediam implementação e saída sob docs/.../qa3-runs, enquanto execução concedia auditoria restrita com saída qa3-runs na raiz e fonte congelada. Contrato específico de Actions agora explicita auditoria, caminhos e ausência de execução de testes pelo modelo sem ferramenta autorizada. `--allow-tool=write` permanece: documentação oficial confirma a categoria de escrita (https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/allowing-tools).

Os dois estágios capturam stdout, stderr, versão e exit code; um coletor determinístico limita cada stream a 16 KiB após redigir credencial literal, tokens GitHub, cabeçalhos Authorization, pares de credenciais e chaves privadas. Somente cinco arquivos explicitamente permitidos são arquivados separadamente, com retenção de 7 dias. Não se coletam env, session, config ou árvores do Copilot. Diagnósticos não substituem parecer e nunca entram no bundle de QA.

Um smoke em processo separado deve criar arquivo de conteúdo exato antes de liberar as três sessões. Ferramentas somente view/create, shell negado, teto CLI válido de 30 créditos (é teto, não custo fixo). Smoke não usa perfis nem a árvore chmod: verifica apenas emissão de arquivo pela CLI, não prova funcionamento dos pareceres ou isolamento de cada revisão. Nenhum shell é oferecido ao modelo. As barreiras físicas dos runners QA e os gates de conteúdo/workspace/peer permanecem.

Validação local: 4 testes de sanitização/coleta passaram; auditor estático seguro; 6 mutações inseguras recusadas; YAML parseado; 19 blocos shell passaram bash -n. Nenhuma inferência local simulada ou alegação de execução profissional. Próximo run deve provar entrega real e revisões cruzadas.

F00 DONE; F01 BLOCKED; G06 não aprovado; F02 não liberada. Aprovação normativa, fontes/células e signoff profissional continuam pendentes.
