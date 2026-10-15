# F00 — Registro de riscos iniciais: integração, dados, segurança e UX

Data da inspeção: **15/10/2026**. Revisor: **QA-03**, perspectiva de IA distinta das revisões QA-01 e QA-02; não constitui auditoria humana independente.

Baseline examinada: `SFPTechnology/Projeto-SIE-2.0`, commit **`8d86db26f5e8675eaced4638af14bd84019e15e7`**. As referências de linha abaixo pertencem a esse commit, exceto a correção documental F00-OPS-01 explicitamente revalidada no worktree. Este documento registra a task **00.05** e insumos para 00.06/00.07; o parecer final de passagem da F00 deve confrontá-lo com os demais entregáveis e testes.

## 1. Escopo, classificação e limites

Foram inspecionados os arquivos rastreados da baseline, a API e a UI em `restructuring/`, cinco migrações SQL, os manifestos/lockfiles disponíveis, guias operacionais e os três ZIPs de visualização, incluindo seus ZIPs internos. A inspeção não alterou código da aplicação, esquema, dados reais, `main` ou serviço publicado. Não houve uso de credenciais nem conexão a projeto Supabase.

As classificações deste registro significam:

| Classe | Significado |
|---|---|
| **COMPROVADO — fonte** | A configuração ou lacuna está diretamente no arquivo citado; sua exploração em serviço publicado não foi demonstrada. |
| **COMPROVADO — execução local** | O comportamento foi reproduzido com dados sintéticos e arquivos temporários, sem atingir produção. |
| **HIPÓTESE** | Há uma condição plausível de risco; faltam ambiente, configuração ou reprodução para afirmar ocorrência. |
| **NÃO VERIFICADO** | Não foi feita a verificação correspondente. Não significa aprovado nem inexistência do risco. |

Severidade considera o impacto caso o componente seja utilizado nas condições indicadas. **ALTA não é alegação de incidente em produção.** Riscos de produção e de integração futura não bloqueiam, por si, a documentação da baseline; precisam permanecer abertos e impedir que o componente seja anunciado como pronto para essas utilizações.

## 2. Registro priorizado

| ID | Gravidade / classe | Achado e condição de risco | Evidência concreta | Tratamento e condição de encerramento |
|---|---|---|---|---|
| F00-SEG-01 | **ALTA / COMPROVADO — fonte** | Três tabelas têm RLS habilitada, mas políticas `FOR ALL` aceitam todas as linhas para `anon` e `authenticated`. Não existe isolamento por usuário/projeto nessas políticas. Havendo exposição e grants, leituras e mutações podem alcançar linhas de terceiros. | `supabase/migrations/20260716_001_create_dependencia_retornos_downstream.sql:22–34`; `20260717_001_create_dimensionamento_condutores_overrides.sql:14–26`; `20260730_001_create_queda_tensao_config.sql:17–29`. | Antes de integrar/publicar: definir identidade e pertencimento do projeto, conferir grants reais e criar políticas por operação com testes de permitir/negar e usuário A × B em banco descartável. **Exploração remota, grants ativos e estado do banco: NÃO VERIFICADOS.** |
| F00-SEG-02 | **ALTA / COMPROVADO — fonte** | A migração normativa concede `SELECT ON ALL TABLES IN SCHEMA public` a `anon` e `authenticated`, com comentário de RLS tratada separadamente; não há `ENABLE ROW LEVEL SECURITY` para suas dez tabelas nas cinco migrações presentes. O grant amplo alcança também tabelas já existentes no schema no momento da execução. | `supabase/migrations/20260712_001_create_normas_tables.sql:10–208`, especialmente `204–208`; busca de RLS nas cinco migrações. | Restringir grants às tabelas de catálogo realmente públicas; demonstrar RLS/autorizações de todas as outras tabelas e testar dados não públicos. O catálogo normativo pode ser público por decisão explícita; isso não autoriza publicar projetos. **Aplicação desse SQL no banco real: NÃO VERIFICADA.** |
| F00-DAT-01 | **ALTA / COMPROVADO — fonte; replay NÃO VERIFICADO** | A sequência SQL não forma uma instalação limpa demonstrada: o DDL usa `TEXT COMMENT '…'`, `NUMERIC … COMMENT` e expressão `COALESCE` em `UNIQUE` de tabela; outras migrações referenciam `public.dependencias`/`public.projetos`, sem sua criação nesta baseline. O seed pressupõe versão normativa `id=1`, sem inserir essa versão na sequência encontrada. | `20260712_001_create_normas_tables.sql:15,56–59,164`; `20260712_002_seed_tabela_36_amostra.sql:16,42,68,87,106,125`; `20260716_001_create_dependencia_retornos_downstream.sql:6`; `20260717_001_create_dimensionamento_condutores_overrides.sql:7`; `20260730_001_create_queda_tensao_config.sql:7`. | Recuperar o DDL de origem, corrigir o dialeto PostgreSQL em incremento próprio e executar instalação/seed/rollback em banco descartável. A gramática oficial não contém `COMMENT` inline como atributo de coluna; registrar comentário com a sintaxe PostgreSQL aplicável. Nenhum SQL foi executado nem corrigido nesta auditoria. |
| F00-DAT-02 | **ALTA / COMPROVADO — fonte** | O SQLite guarda apenas o JSON atual; o histórico registra ação/revisão/data, sem o JSON anterior. O controle de revisão evita sobrescrita concorrente, mas o histórico não permite restaurar uma revisão. Não existe comando de backup/restauração ou migração versionada no repositório local. | `restructuring/apps/api/sie_api/storage.py:21–35,70–81,96–103`; `restructuring/apps/api/sie_api/cli.py:46–55`; limitação reconhecida em `restructuring/docs/PERSISTENCIA-LOCAL.md:102–108`. | Manter somente dados de teste. Para migrar: backup consistente, checksum, restauração ensaiada, comparação semântica e rollback antes de trocar o armazenamento. Não anunciar trilha de eventos como histórico recuperável. |
| F00-DAT-03 | **MÉDIA / COMPROVADO — execução local** | A UI reabre parâmetros escalares e evidência, mas omite a `tabela_condutores` salva; a próxima análise envia sempre a tabela fixa do JavaScript. Projeto criado via CLI/API com tabela personalizada não mantém equivalência de entrada ao ser reanalisado pela UI. | `restructuring/apps/web/app.js:18,95–110`; API aceita `dados` arbitrários em `storage_api.py:15–20`. Ensaio Node VM sobre o `app.js` real, descrito na seção 5. | Preservar a tabela/versão do cenário ou rejeitar explicitamente esquemas incompatíveis ao abrir. Golden roundtrip de projeto CLI/API → UI deve comparar todos os campos usados pelo motor; até lá, equivalência desse caminho é **PARCIAL**. |
| F00-OPS-01 | **MÉDIA / COMPROVADO — fonte; CORRIGIDO no manual** | Na baseline o README inicia o servidor estático com `python -m http.server 5173`, sem bind de loopback. Isso pode servir a pasta em interfaces de rede. Um banco/exportação/segredo colocado na raiz web pode ser entregue sem a autenticação da API; nenhum dado real nessa situação foi encontrado/demonstrado. | Baseline: `restructuring/README.md:29–36`. Correção atual conferida em `README.md:33` e `restructuring/docs/MANUAL-OPERACIONAL.html:42`: comando agora contém `--bind 127.0.0.1`, conforme E2E `test_browser_flow.py:45–48`. | **Correção documental revalidada por diff**, sem mudança de runtime ou golden output. Risco residual: manter dados fora da raiz web mesmo em loopback. Ensaio sintético confirmou que um arquivo de extensão `.sqlite3` deliberadamente colocado na pasta servida é entregue. Não foi demonstrada exposição externa real. |
| F00-SEG-03 | **MÉDIA / COMPROVADO — fonte; uso multiusuário NÃO VERIFICADO** | Um único token compartilhado concede acesso a qualquer UUID do SQLite; não há identidade, proprietário ou organização. É o contrato declarado do teste local, não uma autenticação de produção. Endpoints de cálculo/validação são públicos dentro do processo; CORS não autentica esses endpoints. | `restructuring/apps/api/sie_api/storage_api.py:23–33,36–60`; `main.py:11–16,67–99`; `restructuring/docs/PERSISTENCIA-LOCAL.md:5,64,104–108`. | Preservar modo local desabilitado por padrão e loopback. Exigir autenticação/autorizações antes de implantar em rede compartilhada ou internet. Não classificar a ausência de conta de usuário no protótipo como bypass já explorado. |
| F00-SEG-04 | **MÉDIA / COMPROVADO — execução local; alcance HIPÓTESE** | A criação de SQLite herda permissões do sistema; no ensaio temporário desta sessão o arquivo nasceu `0644`. Acesso por outros usuários depende também das permissões dos diretórios e do sistema operacional. O código não cifra o conteúdo. | `restructuring/apps/api/sie_api/storage.py:18–20,40`; ensaio da seção 5; documentação local não fornece ACL específica de Windows. | Para dados profissionais, definir ACL do diretório/arquivo e política de proteção/backup. Não inferir ACL de Windows a partir do modo POSIX observado. O diretório temporário do ensaio permaneceu privado e foi removido. |
| F00-DEP-01 | **MÉDIA / COMPROVADO — fonte** | A API instala faixas de versões, sem lock Python de runtime/teste/E2E. CI instala a faixa disponível no momento e as actions são referenciadas por tags. O lock do AIOX é separado e não congela a API. | `restructuring/apps/api/pyproject.toml:1–17`; `.github/workflows/sie-restructuring-api.yml:17–25`; `sie-e2e-browser.yml:19–28`; `.aiox-core/package-lock.json`. | Registrar versões resolvidas do ambiente de teste e adotar lock/hash em incremento de dependências. Não atualizar dependências nesta F00 para obter testes verdes. Auditoria CVE atual é item **NÃO VERIFICADO**, separado do lock existente. |
| F00-DEP-02 | **MÉDIA / COMPROVADO — fonte** | Os três pacotes de visualização repetem código e ZIPs com cache Python, sem manifesto próprio ou licença de distribuição identificada. Importam `ezdxf`, FastAPI/Pydantic e componentes React/Carbon. Sua presença não comprova dependências instaláveis ou integração com a API atual. | ZIPs `Arquivos_Diversos/Unifilar/files (5).zip`, `(6).zip`, `(7).zip`; cópia `Arquivos_Diversos/Unifilar/Unifilar/files (7)/sie-camada-visualizacao-fase0-1b/backend/export_dxf.py:16–19`; `README.md:34–65`; router mantém `_carregar_pontos=None` em `backend/router_visualizacao.py:39–53`. | Tratar como **arquivado/candidato**, preservar hashes e escolher uma origem antes de reutilizar; recuperar licenças/notices, definir dependências e loader autorizado. Não instalar/reviver o histórico durante esta auditoria. |
| F00-LIC-01 | **MÉDIA / COMPROVADO — metadados; autorização jurídica NÃO VERIFICADA** | O manifesto do AIOX declara MIT e os lockfiles têm metadados de licença. Não foi localizada licença global do produto nem declaração de licença da API. A posse dos arquivos normativos e de snippets de terceiros não prova direito de redistribuição. | `.aiox-core/package.json` campo `license`; `package.json` sem `license`; `restructuring/apps/api/pyproject.toml` sem licença; inventário de arquivos de licença e seção 4. | Antes de distribuir: confirmar titularidade/licença do produto, notices e permissões dos anexos/normas. Sem parecer jurídico; nenhum problema de licença foi presumido apenas por ausência de campo. |
| F00-UX-01 | **MÉDIA / COMPROVADO — fonte; falha de rede HIPÓTESE** | Cálculos usam `sie.apiBase` do navegador, enquanto persistência aponta fixamente para `127.0.0.1:8000`. A UI não cancela nem estabelece timeout de `fetch`. Em configuração alternativa pode misturar servidores; um servidor que não termina a resposta pode manter botões aguardando. | `restructuring/apps/web/app.js:1,7,17–21,28,65–76,88–117`. | Documentar o contrato de endpoint local; futura configuração deve usar uma única origem validada, timeout/cancelamento e mensagem recuperável. Teste de servidor pendurado/customização de origem em navegador: **NÃO EXECUTADO**. |
| F00-AUD-01 | **MÉDIA / COMPROVADO — documentação histórica** | Há relatórios históricos de fases anteriores e exemplos de visualização com aceites marcados. Não são evidência do comportamento atual de todos os módulos. O manual atual é de protótipo parcial e reconhece várias ausências. | `restructuring/docs/AUDITORIA-INICIAL.md:29–30`; `restructuring/docs/QA-FINAL.md:15–24`; README de visualização arquivado `:81–100`; `restructuring/docs/MANUAL-OPERACIONAL.md:69–84`. | Vincular cada alegação a SHA, comando, resultado e escopo. Preservar históricos como históricos; a F00 deve usar o relatório/estado canônico atuais, sem converter texto antigo em aprovação. |
| F00-AUD-02 | **MÉDIA / NÃO VERIFICADO** | Varredura por assinaturas não demonstra ausência de todos os segredos nem cobre o histórico Git completo. Advisory CVE/licenças dos artefatos realmente resolvidos e configurações remotas também não foram auditados. | Escopo e resultados da seção 3; não houve consulta a banco/advisors nem execução de `npm audit`/`pip-audit`. | Conservar a limitação no parecer. Antes de produção, completar scanners e revisão manual em escopo autorizado; não declarar “zero vulnerabilidades”. |

Os achados acima permanecem **ABERTOS** nesta baseline, exceto **F00-OPS-01 corrigido nos comandos dos dois manuais** e controles positivos verificados abaixo. A alteração de manuais foi feita pelo executor principal e revalidada pelo QA-03; este revisor não modificou código da aplicação. A F00 não autoriza aplicar as migrações permissivas em produção.

## 3. Segredos e cobertura da inspeção

Foi feita varredura local dos **12.127 arquivos rastreados**, lendo **11.995 arquivos textuais** e excluindo **132 arquivos binários/não textuais** dessa primeira etapa. As assinaturas procuradas foram cabeçalho de chave privada, formatos de tokens GitHub/OpenAI/Supabase, access-key ID AWS, JWT e candidatos genéricos de atribuição de credencial. A saída da inspeção continha apenas **arquivo, linha e categoria**, sem valores.

Não houve ocorrência das assinaturas específicas de chave/token na etapa textual. A expressão genérica encontrou **41 candidatos** em ferramentas, documentação, templates e testes. Contextos de fixture/template/referência foram identificados sem revelar valores; os candidatos genéricos restantes **não foram validados como credenciais ativas**. Exemplos de localizações para triagem: `.aiox-core/data/tech-presets/angular-nestjs.md:694`, `.aiox-core/development/tasks/qa-security-checklist.md:492`, `.aiox-core/development/agent-teams/design-system/scripts/design-system/validate-capture-input.cjs:250`. Não se afirma que esses candidatos sejam segredos.

Nos ZIPs foram inspecionados **3 arquivos externos + 3 ZIPs internos**, com **59 entradas textuais** examinadas por assinaturas específicas e **21 entradas binárias/cache** excluídas. Não houve ocorrência dessas assinaturas nos textos. Não se extraiu nem se executou código dos pacotes durante a varredura.

**Não verificado:** segredos em imagens/PDFs/binários, formatos não cobertos, credenciais obfuscadas, histórico completo de commits, validade/revogação de qualquer credencial, variáveis de produção e configuração ativa de Supabase/hosting. Não houve vazamento confirmado por esta inspeção; isso não equivale a ausência comprovada de segredos.

Os arquivos de exclusão já contêm medidas úteis: `.gitignore:3–8` ignora extensões/chaves usuais; `restructuring/.gitignore:9–17` ignora bancos e arquivos `.env`. Um ignore não remove histórico nem impede leitura de arquivos por um servidor estático.

## 4. Mapa de dependências e licenças da baseline

| Limite | Dependências / consumidor | Fixação observada | Evidência e alcance |
|---|---|---|---|
| Gates raiz Node | `scripts/validate-sdc-auto-1.js`; shell executa rotinas AIOX e validações do projeto | Raiz sem dependências npm declaradas; versões de Node são externas | `package.json:1–12`. Não há motivo para inventar um lock de dependências vazias na raiz. |
| AIOX de ferramentas | 15 dependências diretas: `ajv`, `chalk`, `commander`, `diff`, `execa`, `fast-glob`, `fs-extra`, `glob`, `highlight.js`, `inquirer`, `js-yaml`, `proper-lockfile`, `semver`, `tar`, `validator` | `.aiox-core/package-lock.json`, lockfile v3, **127 entradas** de dependência; versão declarada do pacote `5.2.9` | `.aiox-core/package.json`. Metadados do lock: 94 MIT, 17 ISC, 7 BlueOak-1.0.0, 4 BSD-3-Clause, 2 Apache-2.0 e uma entrada de Python-2.0, 0BSD e `(MIT OR CC0-1.0)`. Não é auditoria dos textos legais dos pacotes. |
| Dashboard de diagnóstico AIOX | Ferramenta auxiliar, separada da interface SIE | Lock v3, **351 entradas** | `.aiox-core/scripts/diagnostics/health-dashboard/package-lock.json`. Todas têm campo de licença; inclui uma entrada CC-BY-4.0. Não instalado nem presumido componente do produto. |
| API Python | Runtime: `fastapi>=0.110,<1`, `pydantic>=2,<3`, `uvicorn>=0.27,<1`; build: `setuptools>=68`, `wheel` | **Sem lock Python encontrado** | `restructuring/apps/api/pyproject.toml:1–11`; runtime mínimo declarado Python 3.11; CI declara Python 3.12. Faixas não são versões efetivamente testadas. |
| Testes API/E2E | `pytest>=8,<10`, `httpx>=0.27,<1`; `playwright>=1.55,<2` e navegador Chromium | Sem lock/navegador hash nesse manifesto | `pyproject.toml:13–15`; workflows de API e E2E. Execuções globais e versões efetivas devem ser lidas em `BASELINE_CI.md`. |
| UI atual | HTML/CSS/JavaScript nativos → API local; dados persistidos → API tokenizada → SQLite | Sem CDN ou pacote JS de runtime nessa UI | `restructuring/apps/web/index.html:8,83`; `app.js:1,28`. Não confundir com os componentes React arquivados. |
| SQLite e CLI | Bibliotecas padrão Python `sqlite3`, `json`, `pathlib`, `argparse`, `uuid` | Versão acompanha o runtime Python/sistema | `storage.py:5–10`; `cli.py:10–17`. A CLI de armazenamento não depende de token HTTP nem precisa conectar à rede. |
| SQL/Supabase | Cinco migrações; dependem de PostgreSQL e do DDL de tabelas legado ausente | Versão/estado de servidor e histórico de migração **NÃO VERIFICADOS** | `supabase/migrations/`; riscos F00-SEG-01/02 e F00-DAT-01. Não foi localizado client Supabase no núcleo Python atual. |
| Visualização arquivada | Python/Pydantic/FastAPI/`ezdxf`; React/Carbon no exemplo; requer loader do projeto | Sem manifesto/lock próprios nos ZIPs examinados | Cópias em `Arquivos_Diversos/Unifilar/`; loader ainda não registrado no módulo. Nenhum pacote desse histórico foi instalado. |
| Git externo | `.gitmodules` cita `sistema-de-instala-es-el-tricas-sie-main` | Arquivo de configuração não comprova conteúdo disponível ou checkout reprodutível | `.gitmodules:1–4`. O inventário principal deve registrar o resultado de `git ls-tree`/submódulo; não inferir implementação desse repositório externo. |

Os números de licença refletem campos do lockfile, não uma aprovação jurídica. A licença global do produto, autorização para redistribuir normas e notices de todos os snippets continuam não verificadas. Nenhum advisory de vulnerabilidade atual foi consultado: versões no lock podem estar fixadas e ainda assim ter CVEs.

## 5. Reproduções seguras executadas pelo QA-03

### 5.1 Armazenamento SQLite com biblioteca padrão

Com `PYTHONPATH=restructuring/apps/api`, foi importado o `RepositorioProjetos` real e criado um SQLite em `TemporaryDirectory`. O nome sintético continha texto semelhante a SQL, armazenado como texto; a tabela permaneceu existente. Não se utilizou arquivo do usuário.

| Verificação | Resultado observado |
|---|---|
| Nome sintético com aspas e fragmento SQL | Roundtrip literal; tabela `projetos` preservada |
| Gravação com revisão 0 após criar revisão 1 | `ConflitoRevisao` levantado; versão atual não sobrescrita |
| JSON serializado acima de 1 MiB | `ValueError`, rejeitado |
| JSON com `NaN` | `ValueError`, rejeitado |
| Campos do histórico | Somente `acao`, `criado_em`, `revisao` |
| Permissão do SQLite temporário nesta sessão POSIX | `0644`, dependente do umask; diretório temporário privado |

Uma reprodução mínima, sem dependências de FastAPI e sem rede:

```bash
PYTHONPATH=restructuring/apps/api python - <<'PY'
from pathlib import Path
from tempfile import TemporaryDirectory
from uuid import uuid4
from sie_api.storage import RepositorioProjetos, ConflitoRevisao
with TemporaryDirectory(prefix="sie-f00-audit-") as folder:
    repo = RepositorioProjetos(Path(folder) / "synthetic.sqlite3")
    pid = str(uuid4())
    assert repo.salvar(pid, "Teste local", {"circuitos": []}, 0) == 1
    try:
        repo.salvar(pid, "Nao sobrescrever", {}, 0)
    except ConflitoRevisao:
        pass
    else:
        raise AssertionError("Conflito nao rejeitado")
    assert repo.carregar(pid)["nome"] == "Teste local"
    assert set(repo.historico(pid)[0]) == {"acao", "revisao", "criado_em"}
print("SQLite sintetico: revisao e trilha confirmadas")
PY
```

### 5.2 Reabertura de tabela personalizada

O `app.js` real foi executado em Node `vm`, com DOM e `fetch` sintéticos. A resposta de abertura trazia `tabela_condutores=[{secao_mm2:16,capacidade_a:500}]`, **dado artificial sem autoridade normativa**. Após acionar o callback real de reabertura e o de análise, o corpo enviado continha a tabela fixa `2.5/24, 4/32, 6/41, 10/57`, portanto `exact_roundtrip=false`.

Esse ensaio caracteriza o contrato JavaScript e não equivale a execução em navegador. Nenhum banco, endpoint remoto ou valor real de projeto foi utilizado. Para a futura correção, o teste de aceitação deve salvar tabela distinta, abrir, executar análise e conferir o payload inteiro — além dos campos visíveis.

### 5.3 Arquivo entregue por servidor estático

Foi iniciado `ThreadingHTTPServer` **somente em `127.0.0.1`**, com porta efêmera e diretório temporário contendo `dummy.sqlite3` com marcador sintético. Um GET local retornou o marcador com HTTP 200. Servidor e diretório foram encerrados/removidos. Isso comprova o comportamento do servidor estático para um arquivo deliberadamente exposto; não demonstra banco real exposto nem teste pela rede externa.

### 5.4 O que não foi reproduzido nesta revisão

Autenticação/CORS HTTP completos e E2E Chromium não foram executados pelo QA-03 nesta etapa; existem testes de produto para esses caminhos em `tests/test_storage_api.py`, `tests/test_api.py` e `restructuring/e2e/test_browser_flow.py`, mas sua mera existência não é resultado. O Python padrão inspecionado inicialmente não tinha FastAPI, pytest, httpx, uvicorn ou Playwright instalados. Eventuais execuções globais posteriores e ambiente isolado do executor principal devem ser confrontados com `BASELINE_CI.md` antes do parecer final.

## 6. Controles positivos observados

| Controle | Evidência | Estado desta revisão |
|---|---|---|
| Armazenamento HTTP desabilitado sem token >=24 caracteres e caminho de banco; Bearer comparado com `secrets.compare_digest` | `storage_api.py:23–33` | Confirmado no fonte; teste HTTP depende do relatório global |
| UUID validado, nome limitado, SQL parametrizado e limite de JSON | `storage.py:49–60,64–81,85–102` | Parcialmente exercitado pelo ensaio local; controles adicionais visíveis no fonte |
| Revisão otimista e auditoria na mesma transação | `storage.py:62–82` | Conflito reproduzido; não representa backup/restauração |
| CORS com duas origens locais específicas, sem wildcard | `main.py:11–16` | Confirmado no fonte; não equivale a autenticação |
| Token lido de campo password, sem escrita em local/session storage | `index.html:65`; `app.js:26–38`; `tests/test_web_contract.py:37–41` | Confirmado no fonte; nenhum token de produção utilizado |
| Escape de dados textuais antes de compor HTML e uso de `textContent` nas mensagens locais | `app.js:12–20,71–73,111–114` | Confirmado no fonte; ensaio E2E XSS existente, execução a conferir no relatório global |
| Reabertura invalida resultado e exige novo cálculo | `app.js:110–112`; manual `:73–80` | Confirmado; não resolve omissão da tabela personalizada |
| Interface e manual anunciam protótipo/local e ausência de aprovação normativa | `index.html:30,51–52,62`; `MANUAL-OPERACIONAL.md:50–52,80–84` | Confirmado no conteúdo, sem homologação de engenharia |

## 7. Fontes públicas e verificações externas

Para interpretar políticas e dialeto SQL, foram consultadas fontes primárias em 15/10/2026:

- [Supabase — Row Level Security](https://supabase.com/docs/guides/database/postgres/row-level-security): grants autorizam operações na tabela; policies restringem linhas. Uma policy verdadeira não cria isolamento por proprietário.
- [PostgreSQL — CREATE TABLE](https://www.postgresql.org/docs/current/sql-createtable.html): gramática de criação de colunas e constraints, usada na inspeção da primeira migração. Não se executou parser/servidor PostgreSQL.

A tentativa de abrir `https://supabase.com/changelog.md` pelo serviço de navegação falhou por content-type `text/markdown` não suportado. Não foi alegado cumprimento de revisão completa de breaking changes. Nenhuma alteração Supabase foi implementada e não foi necessário autenticar, chamar advisors ou consultar dados reais.

## 8. Condições para a revisão final QA-03

Para aprovar **o diagnóstico F00**, conferir que inventário/matriz/plano tratam os módulos arquivados como candidatos, registram os caminhos sem equivalência e mantêm os riscos de produção abertos; que o rollback não se apoia no histórico de metadados; e que testes globais reais estão associados ao SHA original. Não basta este registro existir.

Para aprovar **uso de produção**, continuam pendentes, entre outros, RLS/grants/identidades verificados, replay de migração, restauração de backup, lock de runtime, auditoria de dependências/segredos e validação profissional da engenharia. A aprovação do inventário da F00 não satisfaz esses gates de fases posteriores.

**Estado deste registro:** diagnóstico produzido; F00-OPS-01 corrigido/revalidado nos manuais, demais riscos abertos e nenhuma exploração remota comprovada. **Parecer QA-03 final: APROVADO exclusivamente para o diagnóstico F00**, conforme `QA-03.md`; os riscos de uso/produção permanecem abertos.
