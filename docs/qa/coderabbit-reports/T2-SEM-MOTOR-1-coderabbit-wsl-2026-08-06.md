# CodeRabbit WSL — T2-SEM-MOTOR-1

Data: 2026-08-06T02:29:35-03:00  
Responsável: Gage (`@devops`)  
Etapa: `repair_and_run_coderabbit_wsl`  
Status: **BLOCKED_ENVIRONMENT — block_and_log**

## Escopo e restrições

- Somente diagnóstico/reparo local no WSL e revisão read-only.
- Nenhum commit, push, PR, merge, release, deploy, migration ou alteração de remote.
- Nenhum token, credencial ou conteúdo de autenticação foi lido ou exibido.
- O worktree misto não foi stashed, revertido ou modificado.

## Diagnóstico do ambiente

| Item | Resultado |
|---|---|
| Distro | Ubuntu 22.04, WSL2 |
| Kernel | `6.18.33.2-microsoft-standard-WSL2` |
| Arquitetura | Linux `x86_64`, 64 bits |
| CPU | Intel Core i5-3210M, Ivy Bridge |
| ISA relevante | AVX presente; AVX2 ausente |
| libc | glibc 2.35 |
| Binário | ELF x86-64, bundle Bun, dinamicamente ligado |
| Caminho | `/root/.local/bin/coderabbit` |
| Tamanho | 103.364.928 bytes |
| SHA-256 | `a906c3734eb114c284c55cc88c2bd8ad871ddf249083017b11d9f962adb2972e` |

O binário aborta antes de processar comandos funcionais:

```text
coderabbit --version                 -> exit 132, Illegal instruction
coderabbit auth status --agent       -> exit 132, Illegal instruction
```

O backup anterior `/root/.local/bin/coderabbit.bak.20260727092930`
(SHA-256 `777cdbf4e7fd1ab584afcdff417e0f9379ed39c58ec63f43d8afb39746864cc9`)
também encerra `--version` com exit 132. Portanto, rollback para esse artefato
não corrige a incompatibilidade.

## Reparo suportado tentado

A documentação atual do fornecedor define WSL como o runtime suportado no
Windows e o instalador `https://cli.coderabbit.ai/install.sh` como mecanismo
oficial. O instalador consultado apresentou SHA-256
`b7e1267e4ab27dccfc757a81d26b8d2cbfa719716bbe975260df9c4b3425ddef`.
O canal stable anunciava a versão `0.7.2`, com artefatos oficiais apenas para
Linux x64/ARM64 e macOS x64/ARM64; não foi localizado build Linux x64 baseline
sem AVX2 nem CLI Windows nativa suportada.

Antes da tentativa foi criado o backup reversível:

```text
/root/.local/bin/coderabbit.before-0.7.2.20260806T051844Z
SHA-256: a906c3734eb114c284c55cc88c2bd8ad871ddf249083017b11d9f962adb2972e
```

O instalador foi iniciado com `CI=1`, sem login interativo e com o PATH já
configurado para não alterar o profile. O download do artefato permaneceu sem
progresso observável por mais de cinco minutos e foi encerrado somente na árvore
de processos iniciada por esta etapa. Os diretórios temporários do instalador
foram removidos pelo próprio fluxo de limpeza.

O executável original **não foi substituído**: caminho, tamanho, mtime e SHA-256
permaneceram iguais após a tentativa. Configuração e autenticação não foram
alteradas.

## Autenticação e revisão

- Auth status: **UNAVAILABLE** — o comando aborta com SIGILL antes de responder.
- Nova autenticação: **não solicitada**, conforme política YOLO.
- Comando de revisão previsto: `coderabbit --agent -t uncommitted`.
- Comando de revisão executado: **não**, pois o executável não inicia.
- Exit code da revisão: **N/A**.
- Findings CRITICAL: **UNAVAILABLE (não inventado)**.
- Findings HIGH: **UNAVAILABLE (não inventado)**.

Além do bloqueio do executável, a CLI documenta seleção por tipo de diff
(`uncommitted`, `committed` ou base) e por diretório de repositório, mas não uma
allowlist de arquivos. Neste worktree extremamente misto, `-t uncommitted`
revisaria mudanças alheias à T2. Sem commit/worktree isolado — operações fora da
autoridade desta etapa — não existe isolamento suportado e reproduzível do diff
atribuível à story.

## Veredito operacional

**FAIL / BLOCKED_ENVIRONMENT.** A etapa não pode declarar CodeRabbit PASS. São
necessárias, fora deste ambiente e desta autoridade, uma destas condições:

1. build oficial Linux x64 compatível com CPU sem AVX2;
2. host/runner WSL/Linux com AVX2 e autenticação já disponível; ou
3. diff T2 isolado em commit/worktree autorizado, para evitar revisão do
   worktree completo.

Até isso ocorrer, a revisão e as contagens de severidade permanecem
indisponíveis e o handoff não deve marcar o checkbox CodeRabbit como concluído.

## Referências

- `https://docs.coderabbit.ai/cli`
- `https://docs.coderabbit.ai/cli/reference`
- `https://docs.coderabbit.ai/cli/wsl-windows`
- `docs/qa/coderabbit-reports/SDC-AUTO-1-coderabbit-environment.md`
