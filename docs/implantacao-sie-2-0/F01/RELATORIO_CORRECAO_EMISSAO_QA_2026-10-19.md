# F01 — Correção de emissão e diagnóstico Copilot

Run observado: https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39285814051, baseline `70ae61a495447e52a78db64a04e1bb49aa23d283`.

Os três processos CLI terminaram com exit 0, mas o gate recusou a ausência de `qa3-runs/QA-XX/PARECER_QA.md`. Nenhum artefato de parecer foi encontrado e as revisões cruzadas não executaram. Exit 0 não comprova entrega nem revisão. Os streams anteriores estavam em RUNNER_TEMP e não foram arquivados; a causa raiz exata não pode ser afirmada retrospectivamente.

Conflito concreto corrigido: perfis pediam implementação e saída sob docs/.../qa3-runs, enquanto execução concedia auditoria restrita com saída qa3-runs na raiz e fonte congelada. Contrato específico de Actions agora explicita auditoria, caminhos e ausência de execução de testes pelo modelo sem ferramenta autorizada. `--allow-tool=write` permanece: documentação oficial confirma a categoria de escrita (https://docs.github.com/en/copilot/how-tos/copilot-cli/use-copilot-cli/allowing-tools).

Os dois estágios capturam stdout, stderr, versão e exit code; um coletor determinístico limita cada stream a 16 KiB após redigir credencial literal, tokens GitHub, cabeçalhos Authorization, pares de credenciais e chaves privadas. Somente cinco arquivos explicitamente permitidos são arquivados separadamente, com retenção de 7 dias. Não se coletam env, session, config ou árvores do Copilot. Diagnósticos não substituem parecer e nunca entram no bundle de QA.

Um smoke em processo separado deve criar arquivo de conteúdo exato antes de liberar as três sessões. Ferramentas somente view/create, shell negado, teto CLI válido de 30 créditos (é teto, não custo fixo). Smoke não usa perfis nem a árvore chmod: verifica apenas emissão de arquivo pela CLI, não prova funcionamento dos pareceres ou isolamento de cada revisão. Nenhum shell é oferecido ao modelo. As barreiras físicas dos runners QA e os gates de conteúdo/workspace/peer permanecem.

Validação local: 4 testes de sanitização/coleta passaram; auditor estático seguro; 6 mutações inseguras recusadas; YAML parseado; 19 blocos shell passaram bash -n. Nenhuma inferência local simulada ou alegação de execução profissional. Próximo run deve provar entrega real e revisões cruzadas.

F00 DONE; F01 BLOCKED; G06 não aprovado; F02 não liberada. Aprovação normativa, fontes/células e signoff profissional continuam pendentes.

## Evidência posterior — run 39288590946
Smoke recusado pelo gate de arquivo real, antes da matriz. Diagnóstico sanitizado arquivado confirmou CLI 1.0.98, exit code 0, stderr vazio e stdout: “I can’t create SMOKE.txt because no file-creation tool is available in this session.” Logo, exit 0 novamente não comprovava emissão. A allowlist do smoke só incluía view/create, excluindo apply_patch usado por alguns modelos segundo a referência oficial: https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-command-reference .

Correção incremental: smoke permite view/create/edit/apply_patch e prompt não impõe ferramenta específica. Perfis usam os mesmos nomes literais da allowlist QA, sem execute/shell. Auditor verifica ferramenta alternativa do smoke e superfícies dos três perfis. Mutantes sem apply_patch devem ser rejeitados. Esta evidência identifica deficiência concreta da allowlist do smoke; não comprova ainda causa completa da ausência de pareceres no run anterior. Gates e isolamento físico inalterados.

## Resultado operacional verificado — run 39289599183

**Bloqueio operacional de emissão/validação QA3 resolvido neste run.** Workflow completou SUCCESS: https://github.com/SFPTechnology/Projeto-SIE-2.0/actions/runs/39289599183 . Baseline imutável dos seis pareceres: `29c506cbd4f0045c4d54e4f50098d989d7260194`. Edições documentais posteriores não mudam esse baseline nem representam nova execução de QA.

| Etapa | Job ID | Resultado |
|---|---:|---|
| Smoke emissão real | 118186602547 | SUCCESS |
| Primeira passagem QA-01 | 118186790399 | SUCCESS |
| Primeira passagem QA-02 | 118186790829 | SUCCESS |
| Primeira passagem QA-03 | 118186790417 | SUCCESS |
| Cruzada QA-01 sobre QA-03 | 118188934519 | SUCCESS |
| Cruzada QA-02 sobre QA-01 | 118188934628 | SUCCESS |
| Cruzada QA-03 sobre QA-02 | 118188934458 | SUCCESS |
| Bundle | 118190197343 | SUCCESS |

Artefatos reais: primeiras passagens QA-01 `12203619071`, QA-02 `12203454687`, QA-03 `12203834361`; cruzadas QA-01/QA-03 `12205311913`, QA-02/QA-01 `12205696039`, QA-03/QA-02 `12205890518`; bundle `12204368415`. Todos pertencem ao mesmo run e baseline. SHA-256 do ZIP bundle informado pelo GitHub: `25aa79df297e235306f57f1f85ce28b384695811d366ea850f199be06908715e`.

Os nove arquivos foram baixados e revalidados localmente pelos scripts originais `f01_copilot_reports_gate.py`/`f01_qa3_evidence_bundle.py` do baseline. A comparação integral do JSON recalculado com o bundle remoto foi idêntica: três primeiras passagens, três revisões cruzadas, nove hashes. O registro exato foi preservado em `QA3_EXECUTION_EVIDENCE_39289599183.json`. Diagnósticos continuam separados e não foram contados como parecer.

Os pareceres existem e são substantivos; identificam limites como vínculo entre parâmetros do cálculo e revisão de circuito, fronteira single-user do token, proveniência EDP, fontes/células ausentes e baseline histórico desatualizado do manifesto. Achados são recomendações a conferir e implementar separadamente, não correções já efetuadas por estes jobs. Testes não executados pelo modelo foram corretamente descritos como não executados.

**Limite do resultado:** independência de processos GitHub Actions foi verificada; não equivale a independência profissional nem homologação normativa. O bundle registra `independent_professional_signoff=false`, `accepted_normative_gates=0`, `normative_cells_verified_by_bundle=0`, `f01_released=false`, `f02_release_allowed=false`. Portanto F00 DONE; F01 BLOCKED; aprovação G06 e passagem F02 não concedidas. Nenhuma nova tentativa cega ou afrouxamento de gate foi necessário após o smoke corrigido.


## Implementação dos achados QA01-F01 e QA03-F02

Antes: somente corrente/tensão/comprimento eram comparados quando presentes; fator, tabela/Iz, resistência e evidência podiam divergir, e circuito somente nome aceitava ensaio. Reprodução local com testes de mutação demonstrou execução indevida do motor nos casos fator/resistência antes da correção.

Depois: a transação lê `versoes_projeto`, valida o digest histórico e deriva a entrada completa de `AnaliseCircuito` dessa versão. A cópia mutável de `projetos.dados_json` não alimenta o motor. Os sete campos e aninhamentos são comparados com validação estrita de tipos/números finitos; bool/string não substituem números. Só após igualdade o motor executa a entrada salva. Incompletude histórica produz HTTP422 com orientação de salvar nova revisão; nenhuma revisão ou trilha preexistente é reconstruída ou alterada.

Cobertura adicionada: mutações individuais dos sete campos, seção/Iz e proveniência/flags; ausência de cada campo salvo; tipos inválidos/não finitos; adulteração da cópia atual; hash histórico corrompido antes motor; fluxo HTTP legado→revisão completa; consulta de ensaio v1 legado mantida. Fixtures válidas de ensaio agora salvam entradas completas. Comentário EDP corrigido sem alterar dados normativos. CI final do commit deve ser conferida separadamente; nenhuma aprovação G04/G06 ou liberação F01/F02 decorre desta correção.

## Correções da interface — QA03-F01/F04/F06

Dados iniciais e tabela interna agora são identificados em aviso visível como fictícios e de demonstração sintética não homologada. Defaults de fonte/edição não atribuem esses valores à NBR 5410. A versão atual não implementa liberação normativa: resultado e estilo permanecem PENDENTE; flags isoladas ou respostas contraditórias produzem aviso de inconsistência, sem aprovação verde. Em até 850px, a navegação principal continua visível com seis links e foco de teclado destacado, sem novo menu ou dependência de clique.

Regressões Chromium cobrem defaults, resposta adulterada com liberação=true e status PENDENTE/APROVADO, navegação via Tab/Enter em 390 e 850px. Não houve redesenho amplo ou nova integração. Homologação F01/G04/G06 e liberação F02 continuam pendentes.

Validação local da UI: 4 testes de contrato passaram; JavaScript passou node --check. Chromium não instalou neste runtime (download ZIP truncado/0 MiB); teste E2E e revisão das capturas390px dependem do CI. Capturas são geradas por página limpa, sem preencher token, e arquivadas por7dias em artefato separado.

## Parecer recebido em 2026-10-20 — aceite condicionado do lote 01

O documento recebido declara aceite no escopo de 8 células e 6 casos, condicionado integralmente ao Anexo A. Os checkboxes desse anexo continuam vazios e há campos de identificação profissional/registro/data/assinatura por preencher. Registrar **ACEITE_CONDICIONADO**, não homologação nem signoff concluído. P01–P08 permanecem pendentes; nenhuma flag de liberação é alterada. O parecer integral e seus dados pessoais não são publicados.

R3: o parecer informa exemplar de PDF com SHA-256 `e1c02de1e1b5ed070ad7b642e60e0491a0c899e83fe8f2ad5699a743842bbda6`, diferente do exemplar privado anteriormente recebido `45f246e3e33db1bf18dd60743ac93b6ac1ec0796742e169a8014682bfb19aa3d`. São fontes distintas para fins de proveniência. Não substituir hashes, presumir equivalência ou atribuir dupla leitura ao mesmo arquivo sem resolver a divergência.

R1/P03 continua risco alto: I2 exige identificação/fonte do dispositivo e contexto; não presumir universalmente I2=1,45In. A NOTA da proteção é condicional ao regime/tempo de sobrecarga, não requisito universal. Proteção completa, curto-circuito, coordenação e aplicação real continuam pendentes. R6 permanece pendente no pacote de entrega original preservado; este incremento não modifica esse pacote.

### R4 — coordenação funcional corrigida

Antes, uma seção que suportava Ib podia ser escolhida mesmo sem disjuntor comercial admissível, causando rejeição quando seção maior permitiria par. A aplicação agora encontra o menor In comercial ≥ Ib, seleciona a menor seção com Iz ≥ esse In e revalida Ib ≤ In ≤ Iz. Para catálogo fixo independente da seção, isso equivale a percorrer seções até existir par. O primitivo selecionar_condutor e sua semântica/F00 não foram alterados. Cenário sintético de regressão Ib=20,5 e fator=0,87 passa a selecionar seção 4 e In=25; ausência de catálogo/par continua rejeitada. Critério e aviso declaram I2 não verificado.

Trilhas novas registram `orchestration_source` com ID e SHA-256 da função coordenadora; versões v1/v2 anteriores continuam legíveis sem backfill. Hash do arquivo application.py: `78ff6a6032f2657a9f7b86fca22e5c165b20670bb82042ff97e9dbbca2089e73`; hash da função: `1b553bff8823f066da876cc79d335cbfd0cac95d5a9d4bcfcef0a3f53d7bd090`.

Validação focada local: 91 testes passaram, incluindo 11 casos novos de coordenação/proveniência, fronteiras exatas sem arredondamento para decisão, catálogo ausente/insuficiente, nenhum par, HTTP e gate false. Revisão independente do coordenador confirmou os casos novos e regressões API/traces. CI do SHA publicado deve ser conferida; não equivale a nova homologação por três revisores. F01 BLOCKED; G04/G06 não aprovados; F02 não liberada.
