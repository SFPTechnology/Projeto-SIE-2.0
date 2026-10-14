# Story SIE-AUTO-001 — CLI para projetos locais versionados

**Epic:** SIE 2.0 / continuação autônoma, persistência local e rastreabilidade.
**Estado de entrada:** READY. **Estado validado:** DONE (escopo da story), 2026-10-14. **Prioridade:** P1 — requisito CLI First.
**Fontes:** `.aiox-core/constitution.md` (princípios I, III, V); `restructuring/docs/ARQUITETURA-INTEGRADA.md`, `restructuring/docs/PERSISTENCIA-LOCAL.md`; protocolo do usuário SIE-AUTO-ORCHESTRATOR v2.0.

## Problema observável
A API opcional de projetos e o SQLite estão implementados e testados, e a UI permite salvar/reabrir projetos; porém não há um entrypoint de CLI de domínio para criar, consultar, revisar e auditar projetos independentemente da UI e do servidor HTTP.

## Objetivo
Fornecer comandos locais reproduzíveis, seguros e testáveis para o repositório de projetos existentes, sem alterar os contratos da API ou insinuar aprovação normativa.

## Critérios de aceite
- [x] AC-01: `python -m sie_api.cli --help` exibe comandos claros sem iniciar servidor.
- [x] AC-02: comando `salvar` cria e revisa projeto via JSON, UUID e revisão esperada, usando o mesmo `RepositorioProjetos`.
- [x] AC-03: `carregar` retorna projeto/versão; `historico` retorna eventos na ordem.
- [x] AC-04: entrada inválida, projeto inexistente e conflito de revisão falham sem sobrescrever dados.
- [x] AC-05: testes em `pytest` exercitam os três comandos e regressão (incluindo conflito), sem depender de serviço externo.
- [x] AC-06: nenhum comando concede aprovação normativa, imprime credenciais ou acessa banco remoto.
- [x] AC-07: `restructuring/README.md` e guia operacional orientam uso iniciante.
- [x] AC-08: GitHub Actions atual aprova testes Python e verificação de JavaScript na revisão exata da branch.

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
- [x] `restructuring/apps/api/sie_api/cli.py` — novo
- [x] `restructuring/apps/api/tests/test_cli.py` — novo
- [x] `restructuring/README.md` — atualizado
- [x] `restructuring/docs/PERSISTENCIA-LOCAL.md` — atualizado
- [x] `docs/sie-orchestrator/` — estados, evidências e histórico

## Evidências de validação
**Implementação:** `sie_api/cli.py` e `tests/test_cli.py`, com manejo de revisão/UUID, falha segura e UTF-8 com ou sem BOM no Windows. `restructuring/README.md` e `restructuring/docs/PERSISTENCIA-LOCAL.md` atualizados.

**Evidência CI:** workflow `SIE modular API` na revisão `63df096ce5befd940eaad5b11c916376496dcdc8`, run 38572009186 (success), 51 testes Python aprovados / 1 aviso, `node --check` aprovado. URL: https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/38572009186 .

**Qualificação:** os testes provam os critérios automatizados da story, não a conformidade normativa do SIE como um todo. A revisão AIOX e os gates da raiz permanecem trabalho distinto.
