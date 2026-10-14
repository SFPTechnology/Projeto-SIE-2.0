# CodeRabbit Environment Diagnostic — SDC-AUTO-1

Date: 2026-07-27
Owner: Gage (`@devops`)

## Scope

Resolver o bloqueio operacional reportado pelo QA para `SDC-AUTO-1`:

- gates npm globais da raiz;
- execução local do CodeRabbit CLI.

## Root npm gates

Status: RESOLVED

Foi criado um boundary explícito de qualidade na raiz do repositório:

- `package.json`
- `scripts/validate-sdc-auto-1.js`

Comandos validados:

```text
npm run lint      PASS
npm run typecheck PASS
npm test          PASS
npm run build     PASS
```

O boundary executa validações reais do escopo `SDC-AUTO-1`:

- `node -c` nos scripts JavaScript do runner/CLI/testes;
- `WorkflowValidator` nos workflows canônico e headless;
- suíte `sdc-headless-yolo.test.js` com 18 testes;
- contrato negativo do CLI sem `--dry-run`/`--adapter-module`;
- validação do gate QA YAML.

## CodeRabbit CLI

Status: BLOCKED BY ENVIRONMENT

Evidência:

```text
wsl bash -lc '~/.local/bin/coderabbit --version'
Illegal instruction (core dumped)

wsl bash -lc '~/.local/bin/coderabbit --help'
timeout / Illegal instruction
```

Diagnóstico:

- O binário instalado em WSL é Linux x86_64.
- A CPU exposta ao WSL tem `avx`, mas não expõe `avx2`.
- O binário falha antes de qualquer comando funcional (`--version`, `--help`, `doctor` ou review), portanto o problema ocorre antes de autenticação, repositório, argumentos ou escopo de review.
- A reinstalação pelo instalador oficial `https://cli.coderabbit.ai/install.sh` substituiu o binário, mas o novo binário manteve o mesmo erro de instrução ilegal.

Referência operacional:

- Documentação oficial CodeRabbit CLI: `https://docs.coderabbit.ai/cli`
- A documentação oficial lista instalação por script/Homebrew, autenticação via browser/API key e diagnóstico via `cr doctor`; neste ambiente, o binário falha antes de `doctor`.

## Required external action

Para obter CodeRabbit PASS real, uma destas rotas precisa ser executada fora deste ambiente WSL atual:

1. Rodar CodeRabbit em host/runner com CPU expondo AVX2 compatível.
2. Usar GitHub Actions/runner compatível com CodeRabbit autenticado.
3. Obter da CodeRabbit um build compatível com CPU sem AVX2.

Até uma dessas rotas existir, `CodeRabbit` deve permanecer como concern operacional, não como defeito de implementação `SDC-AUTO-1`.
