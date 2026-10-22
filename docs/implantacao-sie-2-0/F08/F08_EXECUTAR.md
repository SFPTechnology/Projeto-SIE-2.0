# F08 — Proteções e distribuição elétrica | ARTEFATO DE EXECUÇÃO AUTÔNOMA

> **SIE 2.0 • Modo sequencial QA3 • Passo 9 de 13**  
> **Status inicial do artefato:** `NAO_EXECUTADO`. Isto é uma instrução de trabalho, não uma declaração de conclusão.  
> **Próxima fase:** F09 • **Prioridade:** P1 crítico • **Épicos:** EP06, EP07 (distribuição final), EP17, EP20, EP28

## 0. MENSAGEM DE ATIVAÇÃO EMBUTIDA — F08

> **Como ativar:** em uma nova conversa do projeto SIE 2.0, anexe **somente** `F08_EXECUTAR.md` e envie a mensagem **«Execute a fase anexada.»**. **Não é preciso copiar este texto.** A anexação isolada não garante o início da execução: é necessário enviar a solicitação na conversa. O arquivo funciona como especificação operacional da fase, subordinada às instruções de segurança e às permissões reais da sessão.

### ATIVAR SIE 2.0 — EXECUÇÃO AUTÔNOMA CONTROLADA DA FASE F08

**Fase:** `F08 — Proteções e distribuição elétrica`  
**Artefato de execução:** `F08_EXECUTAR.md`  
**Repositório de trabalho:** `SFPTechnology/Projeto-SIE-2.0`  
**Título sugerido para a conversa:** `SIE 2.0 — F08 — Proteções e distribuição elétrica`  
**Modo operacional:** implementação incremental e autônoma para decisões técnicas rotineiras, sem intervenção humana desnecessária; execução limitada ao ambiente e à sessão disponíveis.

**Ordem de ativação — instruções obrigatórias à LLM:**

1. **Reconhecer o ambiente.** Inspecione o repositório GitHub realmente acessível, os artefatos deste arquivo, branch, commit, CI, dependências e os registros persistentes das fases anteriores. Não declare nenhum acesso, resultado ou autorização não observado.
2. **Validar a sequência.** Confirme a fase `F08`, seus pré-requisitos e o registro de passagem da fase anterior. Não suponha que o simples upload comprove os gates; reconcilie o estado declarado com código, logs, testes e evidências. Se faltar um pré-requisito indispensável, registre `BLOCKED`/`HUMAN_REQUIRED` e prossiga apenas com tarefas independentes e seguras.
3. **Executar a fase.** Siga as tasks e os critérios de aceite escritos **neste mesmo artefato**, em ordem de dependências, reaproveitando o trabalho validado no legado. Implemente efetivamente o código e a documentação quando houver ferramentas e autorização suficientes; não transforme a execução em mero planejamento.
4. **Executar e corrigir testes.** Utilize testes unitários, de integração, regressão, segurança, navegador e engenharia conforme a criticidade e aplicabilidade. Investigue causa-raiz, corrija defeitos e reexecute as verificações afetadas. Não modifique resultados esperados apenas para eliminar falhas.
5. **Submeter aos três revisores QA incorporados neste arquivo.** Execute as perspectivas críticas `QA-01` (arquitetura, código, testes), `QA-02` (engenharia elétrica e normas) e `QA-03` (integração, dados, segurança, UX/UI), com análises, achados, severidades e evidências **separadas**. Três papéis executados pela mesma LLM não são três auditorias humanas independentes.
6. **Corrigir inconformidades dos QA.** Para cada achado impeditivo, corrija a causa, realize novamente testes e revisão pertinente. Mantenha `PENDENTE`, `REPROVADO` ou `BLOQUEADO` quando faltem evidências, dados normativos ou autorização profissional.
7. **Registrar progresso real.** Havendo acesso de escrita, atualize no repositório os commits, a lista de arquivos modificados, testes, evidências, revisões QA, bloqueios e próxima ação. Respeite `docs/sie-orchestrator/` como fonte de estado quando existente e o relatório de execução `docs/implantacao-sie-2-0/F08/RELATORIO_EXECUCAO.md`. Sem acesso de escrita, forneça relatório para registro posterior, sem fingir persistência.
8. **Proteger o projeto.** Preserve a branch `main` e o sistema publicado; não faça merge, deploy, migração de produção, exclusão irreversível, uso de credenciais/custos externos ou liberação de conformidade ABNT NBR 5410, ABNT NBR 5419, NR-10 ou concessionária sem requisitos, autorização e evidências adequados.
9. **Julgar os gates antes de concluir.** Marque `F08` como `DONE` **somente** quando todas as tarefas essenciais e os três pareceres QA aplicáveis estiverem aprovados com provas verificáveis. Diferencie código implementado de cálculo homologado, além de observações de inferências e tarefas não executadas.
10. **Responder de forma consolidada.** Apresente o estado `F08`, implementações, commits, testes reais, os três pareceres QA, correções e riscos remanescentes. **Próximo marco:** `F09_EXECUTAR.md`. Informe passagem liberada somente quando satisfeitos os pré-requisitos; caso contrário, oriente a retomada desta mesma fase. Não peça ao usuário para copiar outro prompt ou preencher manualmente o controle CSV.

**Comando curto suficiente do usuário:** **Execute a fase anexada.**

**Início da execução:** inspecionar o repositório, reconstruir o estado real da fase `F08` e implementar a primeira task elegível, utilizando as instruções das seções seguintes. Não alegar processamento permanente fora desta sessão.

---

## INSTRUÇÃO IMEDIATA À LLM — INICIAR SEM COPIAR OUTRO PROMPT

O usuário anexou este arquivo como **comando de execução da fase F08**. Não apenas o resuma: **inspecione o repositório e execute as atividades elegíveis desta fase**, dentro das ferramentas e permissões realmente disponíveis. O usuário **não precisa colar nenhuma seção adicional**, preencher planilhas ou mandar comandos de terminal.

1. Reconheça o ambiente e o repositório `https://github.com/SFPTechnology/Projeto-SIE-2.0`. Confirme branch, commit SHA, PR, arquivos, normas autorizadas e testes reais. Não alegue acesso sem inspecionar; use os conectores disponíveis quando aplicáveis.
2. Confira o estado persistente existente e o handoff da fase anterior. **Consultar o handoff e o registro persistente de **F07** no repositório. Se os critérios predecessores essenciais estiverem bloqueados, não declarar esta fase liberada como um todo; executar apenas tarefas independentes e registrar as ressalvas.** Não replique módulos já implementados sem auditoria.
3. Implemente cada tarefa abaixo em ordem de dependências; quando cabível, prepare testes antes da mudança e corrija a causa-raiz. Continue automaticamente com tarefas seguras e tecnicamente determináveis, sem pedir autorização para decisões rotineiras já aprovadas.
4. **Antes da resposta final execute QA-01, QA-02 e QA-03 presentes neste mesmo arquivo** como revisões críticas distintas: contestar, encontrar defeitos, corrigir, reexecutar testes e produzir três pareceres. A mesma LLM usando três papéis não equivale a três auditores humanos independentes.
5. Persista progresso e evidências, se houver acesso à escrita, nos registros existentes do projeto (preferir `docs/sie-orchestrator/` quando já for a fonte canônica; use `docs/implantacao-sie-2-0/F08/` para o relatório desta fase sem duplicar fonte de verdade). O usuário **não precisa atualizar manualmente o controle CSV**.
6. Informe **somente após conferir os gates** o próximo arquivo da sequência. Se persistir impedimento essencial, mantenha `BLOCKED`, `PENDENTE` ou `HUMAN_REQUIRED`, produza instrução de retomada e **não avance automaticamente**.

**Limites:** não alterar a `main`, publicar produção, migrar dados reais, assumir custo, executar operação destrutiva, declarar aprovação normativa ou de concessionária sem autorização/evidência. Não invente documentos, resultados, testes, credenciais ou fonte de dados. Não prometa execução em background.

---

## 1. Missão desta fase

Completar os critérios de proteção e coordenação dos circuitos e alimentadores, conciliando proteção contra sobrecorrentes, choques elétricos, surtos e condições de falta com a topologia e os condutores.

**Resultado esperado:** evidências objetivas dos critérios de aceite e dos entregáveis descritos abaixo, sem substituir revisão profissional quando necessária.

## 2. O que verificar antes de começar

- F05: conectividade, condições de instalação e dados de fonte conhecidos.
- F07: seções e capacidades verificadas.
- F01: bases técnicas e normas/fabricantes verificadas para cada família de proteção.

**Entradas úteis, procurar no repositório antes de solicitar ao usuário:**

- Ib, Iz, seções, dados de fonte, impedâncias e topologia.
- Esquema de aterramento aplicável, condições da instalação e equipamentos.
- Curvas, capacidade de interrupção e demais características comprovadas de fabricantes.

Se faltar recurso indispensável, primeiro procure alternativas seguras já existentes (código, documentos, mock não normativo, testes). Peça **somente** acesso/decisão realmente indispensável; se uma parte estiver bloqueada, continue tarefas independentes desta mesma fase.

## 3. Tasks desta fase — executar na sequência de dependências

| ID | Atividade | Execução obrigatória | Critério de aceite |
|---|---|---|---|
| 08.01 | Modelar dispositivos de proteção | Disjuntores, fusíveis, DR e DPS com dados tipados e fabricante/edição quando aplicáveis. | Catálogo não mistura valores ilustrativos com produtos certificados. |
| 08.02 | Implementar correntes de curto-circuito | Definir modelos pertinentes de falta máxima/mínima, impedâncias e contribuições da fonte, com hipóteses e limites. | Casos independentes e falhas seguras. |
| 08.03 | Avaliar proteção contra sobrecarga | Aplicar verificações pertinentes além de Ib≤In≤Iz, incluindo condições de atuação compatíveis com o dispositivo. | Teste por dispositivo e curva aplicável. |
| 08.04 | Avaliar interrupção e suportabilidade | Confrontar correntes de falta, capacidade de interrupção, proteção dos condutores e tempos relevantes. | Cenários nominais e limites confirmados. |
| 08.05 | Avaliar seccionamento e choque | Ligar TN/TT/IT, caminhos de falta, parâmetros de circuito e dispositivos sob regras cabíveis. | Condições de proteção demonstradas ou pendentes. |
| 08.06 | Integrar DR e DPS | Seleção e coordenação por características e requisitos aplicáveis, respeitando interfaces com equipotencialização. | Verificações específicas, não aprovadas por default. |
| 08.07 | Verificar seletividade/coordenação | Analisar pares montante/jusante com dados confiáveis de curva/limite, documentando seletividade total/parcial quando comprovável. | Conclusões baseadas em dados de fabricante. |
| 08.08 | Revisar balanceamento de fases | Distribuir cargas entre fases considerando correntes, sistemas e condições de operação; preservar decisão do projetista. | Quadros sem inconsistência com circuitos cadastrados. |
| 08.09 | Iterar seleção de condutor/dispositivo | Aplicar recálculo quando o dispositivo não atende, a impedância muda ou a seção é alterada. | Sem loop infinito; critério de convergência e falha. |
| 08.10 | Consolidar quadro e parecer de proteções | Produzir quadro, proteção por circuito, memória, advertências e verificação dos vínculos. | Consistência quadro ↔ motor ↔ diagrama. |

> **Regra:** o fato de existir um arquivo ou uma implementação parcial não satisfaz sozinho o critério de aceite. Cada tarefa requer uma evidência observável.

## 4. Entregáveis obrigatórios

- Motor de curto-circuito por cenário e trecho.
- Verificações de proteção, DR, DPS, aterramento e coordenação por regra.
- Catálogos de fabricantes com proveniência.
- Quadros de cargas e proteções consolidados.
- Suíte independente de testes técnicos.

Colocar o código nas camadas apropriadas do sistema; documentos e relatórios em caminhos compatíveis com a convenção do repositório. Não substituir silenciosamente arquivos legados.

## 5. Condições técnicas que não podem ser ignoradas

- Não garantir seletividade apenas comparando correntes nominais.
- Não confirmar atuação/segurança sem dados de falta e curvas.
- Proteção contra choque segue o esquema e contexto apropriados.
- Os testes computacionais não substituem inspeção/ensaios físicos de instalações.

## 6. Gates de passagem (conferir evidências)

- Curto-circuito, proteção de condutor e dispositivos têm estados coerentes e testados.
- Mudança em quadro/dispositivo desencadeia recálculos necessários.
- Relatório apresenta limitações de fabricante/dados e não libera cenário incompleto.

**Obrigatório:** as tasks essenciais devem estar verificadas, sem regressão impeditiva; QA-01, QA-02 e QA-03 devem aprovar os critérios **aplicáveis a esta fase**. Pendências de fases futuras podem permanecer explicitamente classificadas, mas nenhuma dependência obrigatória deve ser presumida resolvida. Teste computacional não concede aprovação normativa.

## 7. Bloqueios previstos e recuperação

- Impedância da fonte ou curva ausentes: manter avaliação dependente como PENDENTE.
- Dados normativos ambíguos: bloquear afirmação de conformidade e registrar análise.

Investigar logs e causa-raiz → executar correção segura → repetir teste específico → rodar regressão → registrar evidências. Após três tentativas sem progresso, alterar hipótese/estratégia; não repetir ações idênticas. Dados normativos ausentes nunca devem ser substituídos por valores inventados.

## 8. Exemplo de referência

Troca de disjuntor em QD1 exige verificar carga, Iz do trecho alimentado, capacidade de interrupção, desligamento e coordenação com proteção a montante.

Este exemplo não prova execução real.

## 9. QA3 — Três revisores críticos EMBUTIDOS (obrigatórios)

Iniciar **após as implementações elegíveis**, com análise cética e evidência real. Atribuir a cada revisor o estado `NAO_EXECUTADO`, `PENDENTE`, `APROVADO`, `REPROVADO` ou `BLOQUEADO` e listar os problemas por gravidade `CRITICA`, `ALTA`, `MEDIA`, `BAIXA`.

### QA-01 — Revisor de Arquitetura, Código e Testes

- Revisar contratos entre curto-circuito, proteções, condutores e grafo da instalação.
- Exigir testes de condições-limite, cenários de falha e regressão dos módulos dependentes.
- Verificar modelos de equipamentos e suas curvas como dados tipados/versionados.
- Não admitir estados aprovados com verificações obrigatórias ausentes.

**Saída:** achados, criticidade, evidências verificáveis (arquivo/linha, teste/log/commit), correção efetiva e veredito `APROVADO`, `REPROVADO`, `BLOQUEADO` ou `PENDENTE`.

### QA-02 — Revisor de Engenharia Elétrica e Normas

- Validar correntes de curto-circuito e impedâncias de fontes e trechos nos cenários aplicáveis.
- Verificar sobrecarga, atuação, capacidade de interrupção e suportabilidade térmica.
- Revisar esquema TN/TT/IT quando pertinente, DR, DPS, aterramento e equipotencialização.
- Exigir dados e curvas de fabricante para coordenação/seletividade; não inferir por In.

**Saída:** achados, criticidade, evidências verificáveis (arquivo/linha, teste/log/commit), correção efetiva e veredito `APROVADO`, `REPROVADO`, `BLOQUEADO` ou `PENDENTE`.

### QA-03 — Revisor de Integração, Dados, Segurança e UX

- Testar rastreio de proteção montante/jusante e causas de reprovação.
- Verificar acesso seguro a fichas de dispositivos e vínculo à revisão do projeto.
- Confirmar UX que diferencia cálculo pendente, cenário falho e caso não aplicável.
- Exigir registros de inspeção/ensaios quando aplicável; não os simular.

**Saída:** achados, criticidade, evidências verificáveis (arquivo/linha, teste/log/commit), correção efetiva e veredito `APROVADO`, `REPROVADO`, `BLOQUEADO` ou `PENDENTE`.

### QA consolidado — executar antes da resposta final

1. **Inspecionar:** congelar branch/SHA, entradas, cenários, regras e testes; comparar estado planejado, implementado e validado.
2. **Criticar:** três pareceres separados. Para cada achado, informar requisito, gravidade, prova, reprodução e risco.
3. **Corrigir:** implementar correções permitidas; jamais editar os testes esperados para mascarar cálculos errados ou relaxar segurança para obter verde.
4. **Revalidar:** rodar teste reprovado, integrações afetadas e regressões; repetir revisão quando as alterações impactarem pareceres.
5. **Decidir:** marcar a fase `DONE` somente se todos os gates obrigatórios da fase e os três QA estiverem `APROVADO`, sem evidências simuladas. Para F12, isso não substitui autorização formal para deploy.
6. **Registrar:** referências concretas de commits, testes, fontes, QA e blockers; informar o que não pôde ser verificado.

| Revisor | Estado inicial | Evidência que deverá ser demonstrada |
|---|---|---|
| QA-01 — Arquitetura/código/testes | NAO_EXECUTADO | Contratos, código, testes, regressões, SHA |
| QA-02 — Engenharia/normas | NAO_EXECUTADO | Grandezas, premissas, aplicabilidade, cálculos e fontes, quando cabíveis |
| QA-03 — Integração/dados/segurança/UX | NAO_EXECUTADO | API, banco, segurança, UX e testes reais, quando aplicáveis |

**Distinção:** três perspectivas da mesma LLM são autocrítica estruturada, não validação técnica humana independente. Quando a etapa exigir decisão profissional, registrá-la como pendência explícita.

## 10. Estado, evidências e retomada automáticos

Salvar no repositório, se disponível, um relatório legível em `docs/implantacao-sie-2-0/F08/RELATORIO_EXECUCAO.md` e sincronizar a fila/estado persistentes **já existentes**. Conteúdo mínimo:

```text
FASE: F08
ESTADO: PENDING | READY | RUNNING | IMPLEMENTED | VALIDATING | DONE | BLOCKED | HUMAN_REQUIRED
BRANCH / COMMIT: ...
TASKS: ID → estado → evidência verificável
ALTERAÇÕES: arquivos e commits reais
TESTES: comando/CI → resultado observado
QA-01: estado → achados/correções/testes
QA-02: estado → achados/correções/testes
QA-03: estado → achados/correções/testes
GATES: atendidos, não atendidos e não verificados
BLOCKERS: causa e condição de desbloqueio
PRÓXIMO ARQUIVO: F09 (somente se a passagem for permitida)
```

Se não houver escrita no repositório, entregar esse relatório na conversa como arquivo ou texto, sem afirmar que foi persistido no GitHub. Não prometer que a próxima sessão conservará automaticamente estado não salvo.

## 11. Formato ÚNICO da resposta final para o usuário

Apresentar, de forma sucinta: **fase/estado**, tasks implementadas, links de código/commits, testes realmente executados, tabela dos três pareceres QA, falhas corrigidas, riscos/bloqueios ainda existentes e instrução simples sobre o próximo passo.

**Próximo arquivo:** `F09_EXECUTAR.md`. Informe este nome apenas quando os gates de passagem estiverem demonstrados.

**Não solicitar ao usuário para copiar prompts, preencher tabelas ou selecionar comandos.** Quando houver dependência externa indispensável, fazer uma pergunta direta e específica.
