# SIE 2.0 — Testes reais de navegador (SIE-AUTO-005)

## Finalidade

Comprovar em Chromium que a interface local se comunica com a API FastAPI e o banco SQLite temporário, sem substituir testes técnicos e normativos de engenharia.

## O que é validado

| Caso | Comportamento |
|---|---|
| Fluxo básico | API online, cálculo do circuito e resultado com gate PENDENTE |
| Armazenamento | Salvar com token temporário e conferir revisão 1 |
| Atualização | Alterar dados, salvar revisão 2 e recuperar os parâmetros |
| Revalidação | Ao recuperar um projeto, os resultados são descartados até executar nova análise |
| Credencial inválida | Mensagem de acesso não autorizado, sem recuperar projeto |
| Conflito | Revisão obsoleta recebe erro e não sobrescreve silenciosamente |
| HTML não confiável | Texto de evidência é escapado e não vira elemento executável |

O teste navega de fato em Chromium e faz requisições HTTP reais para `127.0.0.1`. Não utiliza mock do navegador.

## Execução local — Windows / PowerShell

Na raiz do repositório GitHub:

```powershell
cd restructuring\apps\api
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[test,e2e]"
python -m playwright install chromium
cd ..\..
python -m pytest -q e2e
```

Se as dependências nativas do navegador não estiverem instaladas, o teste pode requerer configuração adicional na máquina. No GitHub Actions, o comando de instalação com dependências é `python -m playwright install --with-deps chromium`.

**Não é necessário executar os servidores manualmente** para esta suíte: os testes criam API e servidor estático local em processos temporários, usando portas 8000 e 5173. Termine qualquer outro serviço nessas portas antes de executar.

## Localização dos resultados

- `restructuring/e2e/test_browser_flow.py`: cenários.
- `.github/workflows/sie-e2e-browser.yml`: CI do Chromium.
- `.github/workflows/sie-restructuring-api.yml`: testes de API e sintaxe JavaScript.
- `.github/workflows/sie-orchestrator-quality.yml`: lint, typecheck, test e build AIOX.

## Como interpretar aprovação

CI verde demonstra os cenários testados. Não comprova acessibilidade completa, experiência em outros navegadores/dispositivos, carga elevada, autenticação multiusuário, integração com Supabase ou conformidade com ABNT NBR 5410/EDP. A suíte usa dados de demonstração. A `main` e a infraestrutura de produção não são modificadas.

## Evidências verificadas da revisão funcional

- GitHub Actions run **38612351246**: Chromium real — **3 passed**.
- GitHub Actions run **38612351333**: API/pytest — **90 passed, 1 warning**, incluindo sintaxe JS.
- GitHub Actions run **38612351441**: gates AIOX — lint, typecheck, test, build — concluídos com sucesso.
- SHA da revisão aferida: `f2642e3041b16ec0ddbf43e59b8e482f345d39d0`.

Antes de atualizar o registro de estado, confirme se o head mudou e revalide os checks pertinentes.
