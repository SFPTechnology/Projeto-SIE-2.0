# F02 — Arquitetura e modelagem do domínio elétrico
Data:20/10/2026. Estado: **VALIDATING — implementação e QA locais aprovados; CI de publicação pendente**.
Branch: `feat/f02-dominio-eletrico`. F01 encerrada por aceite do titular, sem reabertura. F00 e lote01 preservados.

A especificação utilizada foi recuperada do kit original e depois confrontada com o anexo F02_EXECUTAR.md: ambos SHA-256 `eb4f127c6ff53d3b2a9f0c9064b08e020b1c5fcdf684aac924ab06e25ad0f1ae`.

## Tasks e provas

| Task | Resultado implementado | Evidência |
|---|---|---|
|02.01 Contextos|Domínio puro separado de aplicação,DTO,HTTP,persistência,UI e regras;10contextos documentados|DIAGRAMA_DOMINIO_ELETRICO.md; imports e testes|
|02.02 Entidades|Project,Building,Floor,Room,Supply,Board,LoadPoint,Load,Circuit,CableRun,Segment,Device,CalculationRun,Revision comUUID/referências|domain/installation.py; test_installation_f02.py|
|02.03 Grandezas|Decimaltexto e unidades; FN/FF,P/Q/S,fases estritas; precisão preservada e sem conversão implícita|Schemas e regressões de unidades/precisão|
|02.04 Topologia|Fonte→quadros→dispositivos→alimentadores/circuitos→cargas; órfãos,ciclos,duplicações e disponibilidade de fases recusados|GRAFO_TOPOLOGIA.json; exemplo com2terminais no mesmo quadro e alimentador|
|02.05 Condições|Cada segmento mantém método,meio,temperatura,agrupamento e exposição; admite condições distintas|Exemplo/testes; adaptador global recusa heterogeneidade|
|02.06 Contratos|DTOs versionados,5rotas stateless,1rota local autenticada,CLI com5operações; erros explícitos|CONTRATOS_MOTORES.md; OPENAPI_F02.json; integraçãoHTTP/CLI|
|02.07 Dependências|Hashes de modelo,entrada,código e catálogo efetivo; versão de regra; estadosVALID/PENDING/INVALID/STALE|installation_service.py e regressões de invalidação|
|02.08 Snapshots|JSONcanônico imutável por valor,identidade/revisão/hash; referências exatas e persistênciaSQLite aditiva com conflito otimista|test_installation_integration_f02.py; revisão antiga intacta|
|02.09 Migração|Adaptador opcional compara dados canônicos e resposta do motor original,recusando incompatibilidades; preserva campos legados|MAPA_DEPENDENCIAS_CALCULO.md; replay34F00; teste de adoção sem perda|

## Correções efetivas após QA

- Soma de comprimentos deixou de depender do contextoDecimal padrão,evitando arredondamento silencioso antes da comparação.
- ResultadoJSON não-objeto/incompleto/grandezas inválidas gera422,sem erro500.
- Parâmetros canônicos de impedância não são ignorados: o adaptador resistivo recusa o cenário até mapeamento explícito.
- Booleanos/floats/textos não são aceitos como número de fases; fonte e alimentadores limitam a disponibilidade descendente.
- Impedância declarada deve ter a frequência da fonte ancestral.
- Identidade do algoritmo inclui os módulos e valores reais do catálogo de disjuntores; alteração do catálogo torna o registroSTALE.
- Dispositivo com corrente nominal declarada incompatível com a seleção do legado é recusado.

## Testes observados

- `python -m pytest restructuring/apps/api/tests -q`: **539 passed**,1aviso de depreciação Starlette/TestClient;90testesF02 estão incluídos nessa contagem.
- `python scripts/f00_golden.py --verify`: **34casosPASS**,fixture original intacta.
- `npm run lint`, `npm run typecheck`, `npm test` (**18casos**), `npm run build`: aprovados.
- Testes auxiliares da raiz:6PASS; execução conjunta API+raiz545PASS, sem somar às539API.
- Suíte integrada cobreHTTP,CLI,SQLite,concorrência,unidades,identidade,conectividade,referências,precisão,invalidação e compatibilidade.
- NenhumE2EChromium local é afirmado nestaF02; não houve mudança da interface. O workflow de navegador será conferido no SHA publicado.

## QA3 desta F02

|Revisor|Veredito no escopo|Registro|
|---|---|---|
|QA-01 arquitetura/código/testes|APROVADO após correções|QA-01.md|
|QA-02 modelagem elétrica|APROVADO após correções|QA-02.md|
|QA-03 integração/dados/segurança|APROVADO após correções|QA-03.md|

Foram revisores computacionais separados nesta sessão,com achados e testes próprios; não são três assinaturas profissionais humanas e não reutilizam o QA3F01. Os testes focados dos pareceres se sobrepõem à suíte; não somar contagens.

## Limites e decisão de passagem

O modelo representa cenários mais amplos que o motor monofásico legado. O adaptador não calcula redes trifásicas,percursos ramificados,condições heterogêneas ou impedância canônica; recusa esses casos explicitamente. Verificações complementares e vínculoF01 continuam nas rotas originais,sem correspondência implícita ao novo modelo. Tabelas/material/isolação não recebem homologação pela adaptação numérica.

VALID indica apenas integridade e correspondência computacional; o registro recebido pela rota stateless não tem origem autenticada por assinatura. Persistência é local e opt-in,semRBACmultiusuário ou migração de produção. Não há geração de desenhos ou novos motores nesta fase de arquitetura.

Os três gates funcionais do artefato estão demonstrados localmente. A passagem será consolidada após CI no mesmo SHA. Próximo marco após confirmação: **F03_EXECUTAR.md**. Nenhum merge ou deploy realizado.
