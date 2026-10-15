# LEIA PRIMEIRO — Como utilizar os 3 agentes QA F01 (iniciante)
Data 15/10/2026. **Os agentes foram definidos; não foram executados.** Criar um perfil/issue no GitHub NÃO inicia sessão, não executa Copilot e não homologa norma.

## Artefatos incluídos
- Plano de cinco etapas e seis critérios: [QA3_MULTIAGENTES_PLANO_EXECUCAO.md](QA3_MULTIAGENTES_PLANO_EXECUCAO.md).
- Manifesto que permanece BLOCKED: [QA3_MANIFEST.json](QA3_MANIFEST.json).
- Perfis: `.github/agents/f01-qa-arquiteto.agent.md`, `f01-qa-engenheiro-eletrico.agent.md`, `f01-qa-dados-ux-llm.agent.md`.
- Seis skills em `.github/skills/f01-*/SKILL.md`.
- Verificador determinístico `scripts/f01_release_gate.py`: garante coerência, não credencia documentos.
- Script Windows opcional `scripts/INICIAR_F01_QA3.ps1`: prepara worktrees e pode chamar **três sessões separadas** no Copilot CLI quando as dependências estiverem disponíveis.

## Iniciar pelo Windows PowerShell (opcional)
Pré-requisitos: clone Git local, Git instalado, **GitHub Copilot CLI instalado e autenticado com direito de uso dos perfis** e três branches criadas (já existem remotamente). O ChatGPT não instalou nem autenticou essas ferramentas na sua máquina.

Antes do passo 1, abra a pasta do clone no terminal e confirme que não há mudanças locais pendentes. Execute `git fetch origin` e `git switch feat/f01-governanca-normativa` (ou `git switch -c feat/f01-governanca-normativa --track origin/feat/f01-governanca-normativa` se a branch ainda não existir localmente). Isso não faz merge na `main`.

1. Abra o terminal **PowerShell**, na pasta local do projeto que contém `.git`. O comando de pré-visualização:
   `powershell -File scripts/INICIAR_F01_QA3.ps1`
   Apenas lista o plano, sem iniciar agentes.
2. Para iniciar as três execuções separadas e sequenciais:
   `powershell -File scripts/INICIAR_F01_QA3.ps1 -Executar`
3. O script cria **fora da pasta principal** a pasta `SIE_F01_QA3_WORKTREES` com os três worktrees. Nenhum commit é enviado automaticamente para GitHub e não há merge. Os logs estarão em `SIE_F01_QA3_WORKTREES/logs`.
4. Cada agente precisa produzir o parecer **individual** e congelar a primeira versão no próprio ramo. Se Copilot exigir confirmação de permissões, ou se não houver licença/disponibilidade, a execução não estará concluída automaticamente.
5. Compare os três relatórios, execute revisão cruzada, corrija divergências e repita testes sobre a **integração final**. Não mescle implementação sem revisão e fonte técnica.
6. Para confirmar que a fase **permanece bloqueada** e que ninguém marcou artificialmente 6/6: na raiz do repositório use `python scripts/f01_release_gate.py --verify-invariants`. O comando retorna sucesso quando o **bloqueio está coerente**, e não quando a engenharia foi aprovada. `--check-release` deve retornar **código 1 enquanto faltarem provas**.

## Execução via Copilot em IDE
Abra em VS Code o worktree do respectivo agente e selecione o perfil `f01-qa-...` em Copilot Chat. Peça: “Execute integralmente E01–E05 da F01, documente G01–G06, corrija e teste tudo que for possível. Mantenha BLOCKED onde faltar evidência normativa”. Repita com contexto/sessão separados e **sem expor o primeiro parecer de um ao outro**. Perfis em feature branch podem não aparecer no seletor do Copilot cloud agent do GitHub.com até sua publicação na branch padrão; não mesclar na `main` apenas para ativá-los.

## Branches e tarefas
| Agente | Branch independente | Issue |
|---|---|---|
| QA-01 | `qa/f01-arquiteto` | https://github.com/SFPTechnology/Projeto-SIE-2.0/issues/4 |
| QA-02 | `qa/f01-engenheiro-eletrico` | https://github.com/SFPTechnology/Projeto-SIE-2.0/issues/5 |
| QA-03 | `qa/f01-dados-ux-llm` | https://github.com/SFPTechnology/Projeto-SIE-2.0/issues/6 |

Todos os três ramos foram iniciados a partir do SHA `8aec14ac0817ba75ea5e5cee90240368807f1bf7` (mesma baseline). O uso de três branches não prova, por si só, independência factual ou aprovação por profissional habilitado.

## Ao obter os resultados
- Se G01–G06 estiverem realmente comprovados e aprovados pelos revisores e houver revisão independente das normas, registrar evidências verificáveis, auditar e só então considerar F01 DONE.
- Se faltar original autorizado, dupla conferência, resultado esperado independente, vínculo real de regra aplicada ou QA3 aprovado, **F01 continua BLOCKED**, F02 não começa.
- Não carregar segredos API no chat, worktree, repositório nem relatório. Nenhuma alteração em produção/Supabase é executada por esses scripts.
