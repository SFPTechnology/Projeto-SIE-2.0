# SIE 2.0 — Ativar os 3 agentes Copilot QA na F01 (iniciante)
**16/10/2026 · Status: infraestrutura GitHub Actions instalada; autenticação do titular da conta pendente.**

## O que foi criado

- Workflow: [F01 Copilot QA3 Isolated](https://github.com/SFPTechnology/Projeto-SIE-2.0/blob/feat/f01-governanca-normativa/.github/workflows/f01-copilot-qa-isolated.yml).
- Código verificador: `scripts/f01_copilot_reports_gate.py`.
- **Três jobs realmente separados**, em GitHub-hosted runners isolados, usando os agentes já existentes `f01-qa-arquiteto`, `f01-qa-engenheiro-eletrico`, `f01-qa-dados-ux-llm`. Todos recebem o **mesmo commit SHA exato** da `feat/f01-governanca-normativa`.
- **Três sessões posteriores** fazem revisão cruzada somente depois que todos os primeiros pareceres foram gerados, validados e arquivados.
- Artefatos: `f01-firstpass-QA-01-...`, `f01-firstpass-QA-02-...`, `f01-firstpass-QA-03-...` e `f01-crossreview-...`, com retenção de 14 dias.
- O repositório permanece em leitura apenas para o workflow. **Não existe push automático, merge, modificação de `main` nem desbloqueio F02**. Os relatórios **não** homologam células ABNT/EDP ou substituem o parecer profissional.

## Apenas UMA configuração humana de segurança é necessária

**Jamais cole a chave de acesso no chat, em issue, repositório, código-fonte ou workflow.** A conta GitHub é pessoal, por isso a opção indicada na documentação GitHub é um fine-grained PAT **de titular pessoa física**, com permissão *Copilot Requests* (não um classic PAT).

1. Acesse **[GitHub → Fine-grained personal access tokens](https://github.com/settings/personal-access-tokens/new)** com a conta que possui direito de uso do GitHub Copilot. Em *Resource owner*, selecione **sua conta pessoal**.
2. Em *Repository access*, selecione apenas `SFPTechnology/Projeto-SIE-2.0` se disponível. Em **Account permissions**, adicione **Copilot Requests** com a permissão indicada pelo GitHub. Use um token com validade curta, por exemplo 7 a 30 dias.
3. Gere o token e copie-o **somente** na tela de criação do segredo: [Projeto-SIE-2.0 → Settings → Secrets and variables → Actions](https://github.com/SFPTechnology/Projeto-SIE-2.0/settings/secrets/actions) → **New repository secret**.
4. Nome EXATO: `F01_COPILOT_PAT`. Cole a chave no campo secreto e clique **Add secret**. **Não é necessário informar a chave na plataforma SIE** ou ao ChatGPT.
5. Acesse [GitHub Actions — todas as execuções F01 Copilot QA3](https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/workflows/f01-copilot-qa-isolated.yml?query=branch%3Afeat%2Ff01-governanca-normativa). Se o workflow não constar na listagem porque só existe na feature branch, entre pelo [run inicial de instalação](https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/38993370293) ou por um run mais recente com título **SIE F01 - Copilot QA3 Isolated**.
6. No run que falhou **somente pela ausência de F01_COPILOT_PAT**, selecione **Re-run jobs → Re-run all jobs**. Esta operação reinicia exatamente o workflow da feature branch sem copiar arquivos para `main`. Prefira o **run mais recente** (após correções do workflow). A execução inicial falhar por falta de secret é comportamento **seguro e esperado**.
7. Depois, clique nos jobs **preflight**, **Independent first-pass QA-01/02/03**, **Cross-review**. Em **Artifacts**, estarão os relatórios e matrizes independentes, se tudo passar.

**Observação:** `workflow_dispatch` pode não aparecer na lista de execução manual porque GitHub exige a existência do workflow na branch padrão para esse evento. Sem tocar na `main`, use **Re-run all jobs** do run gerado pelo `push` à F01. Em rodadas futuras, o administrador pode alterar `COPILOT_RUN_REQUEST.md` e fazer commit na F01; isso inicia outro run pela regra `push`.

## Segurança, custo e comportamento

- **Não** utiliza `--yolo` nem permite shell arbitrário ao agente: usa **Autopilot** limitado, `--available-tools=view,grep,glob,edit`, somente escrita de relatórios, sem servidor GitHub MCP interno, `--deny-tool=shell` e GitHub Actions `permissions: contents: read`. Os jobs são **efêmeros**, em três máquinas virtuais distintas.
- Limites: até 5 continuações por sessão e timeout por job. `--max-ai-credits=6` é um **limite flexível de créditos por resposta**, não limite financeiro global rígido. Podem existir custos de uso Copilot/Actions conforme seu plano.
- O secret é injetado **apenas no passo do Copilot**, sem ser impresso no log; o checkout não preserva credenciais Git no diretório. Nunca reutilizar para banco ou produção.
- Primeiro parecer é congelado antes da segunda rodada; os revisores cruzados só recebem o parecer já produzido do colega.
- O validador rejeita seis gates incompletos, conclusões `accepted=true`, declaração de signoff, SHA/identidade inconsistente ou tokens aparentes em relatórios.
- Se ocorrer falha de autenticação, plano insuficiente, crédito esgotado ou qualquer inconsistência, o job falha e G06 **continua bloqueado**. A máquina não inventa aprovações.

## Como interpretar o resultado

Se os **seis** jobs Copilot forem aprovados, isso comprova sessões computacionais separadas com artefatos e revisões cruzadas. **Não aprova automaticamente G01–G06:** as células primárias ABNT/EDP, casos normativos independentes, autenticação de fontes e assinatura técnica externa seguem condicionadas às evidências exigidas pelo `QA3_MANIFEST.json`.

**F00=DONE. F01=BLOCKED até evidências reais. F02=NOT_RELEASED.** Nenhuma autorização rotineira adicional é pedida às LLMs, mas a criação do PAT pelo proprietário **é necessária e não pode ser terceirizada para o próprio agente**.

Documentação GitHub:
- [Autenticação da Copilot CLI em automações](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/authenticate-copilot-cli)
- [Copilot CLI + GitHub Actions](https://docs.github.com/en/copilot/how-tos/copilot-cli/automate-copilot-cli/automate-with-actions)
- [Referência de comandos Copilot CLI](https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference)
