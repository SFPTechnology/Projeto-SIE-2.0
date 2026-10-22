# QA-03 — Vinculação e seleção F07 — Integração, dados, segurança e UX

Data: 22/10/2026. Revisão independente de agente de software; não é auditoria humana ou homologação profissional.

## Escopo e provas observadas

Foram inspecionados `conductor_api.py`, `conductor_cli.py`, `conductor_selection_f07.py`, `conductor_registry_f07.py`, `condutores.html/js`, novos testes API e os dois E2E de seleção fonte-vinculada. O estudo livre anterior permanece compatível; seleção usa contrato separado e rota própria, resolvendo tabelas no servidor.

`python -m pytest restructuring/apps/api/tests/test_conductor_binding_f07.py -q --tb=short` executado por este revisor: **76 passed, 1 warning, 1,70 s**. O aviso é de depreciação Starlette/httpx.

Ensaio adicional TestClient com banco SQLite temporário e variáveis de ambiente restauradas ao final:

|Cenário|Resultado observado|
|---|---|
|PUT seleção sem credencial|401|
|PUT seleção com token incorreto|401|
|PUT com cliente remoto203.0.113.10|403|
|PUT em ambienteprod|503|
|PUT seleção para outro UUID de projeto|422|
|PUT válido com topologia cadastrada/revisão esperada|200|
|Reutilizar UUID histórico|422|
|Nova seleção com revisão concorrente antiga|409|

A consulta autenticada retornou seleção histórica e coleção `studies` vazia compatível; `professional_approval=false` foi preservado. Não houve acesso a dados reais ou produção.

## Integração e dados

- Contrato rejeita campos extras de aprovação/tabela do cliente. Catálogo GET fornece versão/hash/fonte; POST de seleção não é gravação de estado nem autorização de conformidade.
- PUT/GET históricos herdam a fronteira local existente (token, ambiente e loopback). A escrita é otimista e transacional, preserva memória anterior e não sobrescreve silenciosamente a topologia pela seção proposta.
- O fingerprint inclui entrada física, parâmetros, versão/política do motor e catálogo/fontes/células F01. Testes cobrem alteração de seção, Ib, percurso, método, parâmetro, revisão de catálogo e hash de fonte com invalidação das memórias antigas.
- Execuções canônicas VALID/PENDING são marcadas STALE na gravação de seleção e são reconstruídas pelo serializer canônico. Documentos/proteção dependentes permanecem explicitamente obsoletos; a escolha F07 não conclui a proteção F08.
- UI usa `textContent`/`createElement`, restringe API a HTTP(S) de loopback sem credenciais na URL e confere geração/JSON antes de renderizar resposta. Importação/exemplos também descartam resposta anterior após nova edição. JSON exportado conserva os estados, fontes e limites da análise.

## Achado QA03-V1 — MÉDIA — catálogo anterior permanece visível depois de alterar API

Reprodução por inspeção do fluxo: consultar catálogo pelo botão `catalog` preenche `#catalog-memory`; editar `#api` dispara `invalidate()`, mas essa função não limpa `#catalog-memory`. Com isso, a seção “Catálogo e fontes disponíveis” ainda exibe hash/metadados obtidos do servidor anterior. O resultado calculado/exportação é invalidado corretamente, porém a evidência visual de catálogo pode ser interpretada como sendo da API recém-informada.

Correção indicada ao implementador: limpar o catálogo ao alterar a API (ou na invalidação conservadora) e comprovar que a resposta antiga não restaura a consulta depois da edição. Não é defeito da matemática nem da autorização local.

## Navegador e impressão

Os dois novos E2E foram lidos: seleção de exemplo, consulta do catálogo, exportação com hash/flags,20linhas de critérios, impressão PDF em memória, nova corrente sem solução e histórico autenticado com alteração de comprimento/revisão concorrente. A execução consolidada será anexada após logs observados; este revisor não abriu servidores nas portas de teste para evitar interferência na suíte do executor.

## Veredito inicial

**PENDENTE** para fechamento de integração visual até corrigir QA03-V1 e observar execução Chromium. Integração API/CLI, autorização local, contrato de dados e invalidação foram aprovados nos ensaios examinados. O parecer não atribui conformidade profissional nem aprova verificações futuras F08. Nenhum código foi alterado por este revisor.

## Revalidação e veredito final — APROVADO no recorte fonte-vinculado

**QA03-V1 RESOLVIDO.** O listener de alteração de `#api` agora invalida resultado e limpa `#catalog-memory`. Executei ensaio Node `vm` com DOM simulado e `fetch` adiado: catálogo já exibido, nova consulta pendente, edição da API, liberação da resposta antiga. O catálogo permanece vazio, a resposta anterior é descartada e os botões de exportação/impressão continuam desabilitados (**PASS**). Não se alterou a expectativa para ocultar a falha.

Logs do executor examinados:

- `/tmp/f07-fontes/e2e-all.log`: **32 passed,75,01s**. Inclui os30fluxos anteriores e2novosfluxos de fonte/seleção/histórico.
- `/tmp/f07-fontes/api-final.log`: **864 passed,1warning,14,87s**;77novos testes da vinculação adicionados aos787anteriores. A validação explícita `application=ORDINARY_FIXED_INSTALLATION_NO_SPECIAL_REQUIREMENTS` e a rejeição422 de aplicação especial foram conferidas no código/teste; não representam aprovação de locais especiais.
- `/tmp/f07-fontes/e2e-source-final.log`: **2 passed,30deselected,4,86s**, depois da correção do catálogo visual e do contrato de aplicação. O E2E contém a asserção de limpeza de catálogo ao editar API.

Inspecionei a captura Chromium final de seleção: contraste e textos legíveis, estado “Proposta selecionada com fonte vinculada”, matriz com nomes/seções de trecho e critérios visíveis, sem sobreposição na área capturada. A exportação mantém versão/hash de fonte e flags profissionais falsas; a edição limpa proposta/exportação antes de recalcular. O ensaio de impressão comprova emissão PDF em memória, não revisão visual de todas as páginas ou relatório técnico homologado.

**QA-03: APROVADO para os critérios aplicáveis de integração CLI/API/UI, segurança, histórico, rastreabilidade e invalidação F07 no recorte implementado.** Não foram encontrados achados impeditivos remanescentes nesta revisão. A aprovação não abrange conformidade profissional, proteção definitiva F08, outros catálogos/condições ou locais especiais. CI remoto e publicação devem ser registrados pelo executor/DevOps com seus SHAs e runs reais; não são presumidos por este parecer local.
