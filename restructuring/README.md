# SIE 2.0 — núcleo integrado de engenharia elétrica

O novo núcleo do SIE 2.0 reúne, em uma jornada local única, uma API FastAPI, motores determinísticos de cálculo e uma interface web premium. Ele foi criado de forma isolada do legado: nenhum arquivo pré-existente é substituído.

## O que já funciona

| Camada | Entrega |
|---|---|
| Domínio | entidades validadas e gate de evidência normativa |
| Motores | seleção de condutor, seleção de disjuntor e queda de tensão monofásica resistiva |
| API | validação estrutural e endpoint integrado de análise |
| Interface | painel responsivo, entradas, resultado explicável e status do gate |
| Qualidade | testes unitários e de API, com cenários seguros e rejeições |

## Executar localmente no Windows

1. Abra o PowerShell na pasta raiz do repositório.
2. Inicie a API:

```powershell
cd restructuring\apps\api
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[test]"
python -m pytest -q
python -m uvicorn sie_api.main:app --reload
```

3. Em outro PowerShell, sirva a interface:

```powershell
cd restructuring\apps\web
py -3.11 -m http.server 5173
```

4. Abra `http://127.0.0.1:5173`. A documentação da API fica em `http://127.0.0.1:8000/docs`.

## Jornada do usuário

1. Informe corrente, tensão, comprimento, resistência e fator de correção.
2. Informe a fonte, edição e referência que sustentam a tabela usada.
3. Clique em **Executar análise**.
4. Leia a seção selecionada, o disjuntor, a queda de tensão e as fórmulas/critério exibidos.
5. Verifique os avisos de pendência: nenhum botão ou dado preenchido pelo usuário libera o cálculo normativamente.

## Limites deliberados de segurança

- O cálculo é determinístico e rastreável, mas não declara conformidade automática com ABNT NBR 5410 ou qualquer concessionária.
- A liberação normativa está desabilitada nesta versão. Uma futura aprovação exigirá evidência conferida pelo servidor, controle de acesso e trilha de auditoria, não checkboxes do navegador.
- O modelo de queda de tensão atual é monofásico e resistivo; impedância, reatância, curto-circuito, seletividade, DR, EDP e topologias multifásicas continuam como extensões normativas condicionadas à matriz de evidências auditadas.

Consulte [MANUAL-OPERACIONAL.md](./docs/MANUAL-OPERACIONAL.md) para o guia completo e [ARQUITETURA-INTEGRADA.md](./docs/ARQUITETURA-INTEGRADA.md) para o desenho técnico.

## Documentação e segurança do Marco 002

- [Manual operacional HTML](docs/MANUAL-OPERACIONAL.html) — leitura pelo navegador.
- [Manual Markdown](docs/MANUAL-OPERACIONAL.md) — versão textual.
- [Relatório do Marco 002](docs/MARCO-002-RELATORIO.md) — código, testes, limitações e próximos gates.

A infraestrutura SQLite em `apps/api/sie_api/storage.py` possui API local opcional em `/api/v1/local/projetos`, desabilitada por padrão e protegida por token. Veja [guia de persistência](docs/PERSISTENCIA-LOCAL.md). O motor trifásico resistivo em `domain/engines.py` é uma função de cálculo ilustrativa, sem integração normativa, com `cos(phi)=1` e reatância desconsiderada.

## Projetos via CLI (sem navegador ou servidor)

Com o Python instalado e estando em `restructuring/apps/api`, consulte os comandos:

```powershell
python -m sie_api.cli --help
```

Crie um arquivo `dados.json` contendo um objeto JSON, por exemplo: `{ "circuitos": [] }`. Depois execute:

```powershell
python -m sie_api.cli --database sie-local.sqlite3 salvar --nome "Casa de teste" --arquivo dados.json
```

O retorno traz um UUID. Substitua `UUID` abaixo por esse identificador:

```powershell
python -m sie_api.cli --database sie-local.sqlite3 carregar --id UUID
python -m sie_api.cli --database sie-local.sqlite3 historico --id UUID
```

Para revisar o mesmo projeto, use novamente `salvar`, com `--id UUID` e `--revisao-esperada 1`. Nenhum desses comandos depende da API web nem aprova tecnicamente o projeto. Veja [tutorial CLI e API local](docs/PERSISTENCIA-LOCAL.md) e [story SIE-AUTO-001](../docs/stories/story-SIE-AUTO-001-CLI-LOCAL-PROJECTS.md).

## Orquestração segura das próximas etapas

O repositório também possui um **escalonador determinístico do SIE**, separado do executor AIOX existente. Ele valida as dez situações de uma atividade, detecta ciclos no grafo e ordena somente tarefas elegíveis. Não executa agentes nem faz deploy por conta própria.

```powershell
cd restructuring\apps\api
python -m sie_api.scheduler_cli --help
```

Consulte o [guia do escalonador](../../../docs/sie-orchestrator/SCHEDULER-GUIDE.md) (no repositório: `docs/sie-orchestrator/SCHEDULER-GUIDE.md`). A referência JSON canônica está em `docs/sie-orchestrator/ORCHESTRATOR_STATE.json` e deve ser reconciliada com os checks reais antes de modificar estados.
