# Story SIE-AUTO-001 — CLI para projetos locais versionados

**Epic:** SIE 2.0 / continuação autônoma, persistência local e rastreabilidade.
**Estado de entrada:** READY. **Prioridade:** P1 — requisito CLI First.
**Fontes:** `.aiox-core/constitution.md` (princípios I, III, V); `restructuring/docs/ARQUITETURA-INTEGRADA.md`, `restructuring/docs/PERSISTENCIA-LOCAL.md`; protocolo do usuário SIE-AUTO-ORCHESTRATOR v2.0.

## Problema observável
A API opcional de projetos e o SQLite estão implementados e testados, e a UI permite salvar/reabrir projetos; porém não há um entrypoint de CLI de domínio para criar, consultar, revisar e auditar projetos independentemente da UI e do servidor HTTP.

## Objetivo
Fornecer comandos locais reproduzíveis, seguros e testáveis para o repositório de projetos existentes, sem alterar os contratos da API ou insinuar aprovação normativa.

## Critérios de aceite
- [ ] AC-01: `python -m sie_api.cli --help` exibe comandos claros sem iniciar servidor.
- [ ] AC-02: comando `salvar` cria e revisa projeto via JSON, UUID e revisão esperada, usando o mesmo `RepositorioProjetos`.
- [ ] AC-03: `carregar` retorna projeto/versão; `historico` retorna eventos na ordem.
- [ ] AC-04: entrada inválida, projeto inexistente e conflito de revisão falham sem sobrescrever dados.
- [ ] AC-05: testes em `pytest` exercitam os três comandos e regressão (incluindo conflito), sem depender de serviço externo.
- [ ] AC-06: nenhum comando concede aprovação normativa, imprime credenciais ou acessa banco remoto.
- [ ] AC-07: `restructuring/README.md` e guia operacional orientam uso iniciante.
- [ ] AC-08: GitHub Actions atual aprova testes Python e verificação de JavaScript na revisão exata da branch.

## Dependências
- `DAT-01` SQLite versionado com testes: satisfazido em `restructuring/apps/api/sie_api/storage.py`.
- GitHub Actions `SIE modular API`: verificação atual registrada no estado do orquestrador.
- Não depende de liberação normativa; o CLI só gerencia dados preliminares.

## Escopo negativo
Sem autenticação multiusuário, alterações em produção, Supabase remoto, migrações normativas, assinatura profissional ou merge na `main`.

## Plano de execução
1. Implementar `sie_api/cli.py` com argparse e JSON estrito.
2. Implementar `tests/test_cli.py` com criação, edição, conflito e leitura.
3. Atualizar guias existentes.
4. Confirmar GitHub Actions; só então marcar DONE.

## Checklist de arquivos
- [ ] `restructuring/apps/api/sie_api/cli.py` — novo
- [ ] `restructuring/apps/api/tests/test_cli.py` — novo
- [ ] `restructuring/README.md` — atualizado
- [ ] `restructuring/docs/PERSISTENCIA-LOCAL.md` — atualizado
- [ ] `docs/sie-orchestrator/` — estados, evidências e histórico

## Evidências de validação
A preencher exclusivamente com commits, execuções e resultados efetivos. Não marcar DONE apenas por criar arquivos.
