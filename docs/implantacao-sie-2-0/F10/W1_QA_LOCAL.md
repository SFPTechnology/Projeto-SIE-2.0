# QA independente W1 — revisão local

Data: 2026-10-24. Branch de referência: feat/f09-concessionarias-especializadas. HEAD verificado: 52b74702d4e55258b287fc8211240ff6e00dffaa. Revisão realizada sobre alterações locais não commitadas; não há SHA candidato final nesta evidência.

## Execução

- Leitura de AGENTS.md e Constituição: realizada.
- Inspeção estática de adaptador persistido, registry e story: realizada.
- Comando `python -m pytest -q tests/test_artifact_store_f10.py tests/test_artifact_registry_f10.py tests/test_persisted_source_f10.py tests/test_persisted_source_f10_sqlite.py tests/test_storage.py`, cwd `restructuring/apps/api`: exit 1, runtime sem pytest.
- Mesmo comando com `/usr/bin/python3`: exit 1, runtime sem pytest.
- Após instalação das dependências declaradas pelo orquestrador, o mesmo comando com `python` foi reproduzido por este QA: exit 0, **65 passed in 1.99s**. Inclui SQLite/parser real, registro, publisher, recuperação e cenários de falha/concorrência previstos nesses arquivos. Os erros anteriores de ambiente foram resolvidos; não são bloqueio atual.

## Achados

1. G01: o adaptador verifica identidade/revisão/circuito e estado VALID do CalculationRun, porém não reexecuta o motor nem comprova seu output hash. O próprio source_kind registra NOT_SERVER_ATTESTED. Não há base para aprovar um requisito de execução efetiva server-side por esse estado declaratório.
2. Dependências F06–F08: a story restringe o bundle a topologia F02/F05 e identidade de run. Não devem ser anunciadas como verificadas ou incluídas no contrato sem lineage/revalidação. A mera presença desses estudos na revisão não demonstra consumo pelo renderer.
3. Documentação: story ainda contém afirmação de ausência de vínculo automático com histórico de revisões, incompatível com o adaptador persistido presente no workspace. Deve ser corrigida e alinhada ao alcance efetivo, mantendo a limitação de attestation acima.
4. Filesystem: registry rejeita symlinks por checagens antes de resolver/abrir caminhos. Isso não demonstra proteção contra substituição concorrente por ator local externo; restringir a garantia ao diretório local confiável ou mitigar com primitivas de abertura segura.

## Gates

Origem, snapshot, G02 e atualidade: implementação observada e 65 testes focados passando no workspace local; o conjunto não substitui rastreio no SHA candidato final. G01: PARTIAL. Segurança: PARTIAL até limites/revisão adversarial e reteste. CI: NOT_VERIFIED. QA global: não aprovado; faltam resolução do requisito G01 e exame do candidato final com evidências aplicáveis.

Este parecer é revisão independente estática e teste local parcial, não homologação normativa/profissional, nem aprovação da W1.
