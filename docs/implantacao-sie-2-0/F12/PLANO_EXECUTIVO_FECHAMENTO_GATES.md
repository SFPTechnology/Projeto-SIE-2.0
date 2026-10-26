# PLANO_EXECUTIVO_F12_FECHAMENTO_GATES — SIE 2.0

**Fase:** F12 | **Modo:** YOLO técnico controlado, progressivo e fail-closed | **Emissão:** 25/10/2026
**Baseline:** `feat/f12-liberacao-controlada` no SHA `d12d7ee14a4b3a7ef658beea63740d834b241487`.
**Pré-requisito:** F11 `DONE` somente para QA de software local; não equivale a aprovação profissional.
**Escopo:** fechar evidências de G01–G10 da F12; quando não houver ambiente ou autoridade demonstrados, produzir evidências e registrar bloqueios sem alegar aprovação.

## 1. Estrutura multiagente especializada

| Papel | Agente / competências | Escopo implementável sem mudança real | Evidência exigida para gate real |
|---|---|---|---|
| Orquestrador | A01 Arquiteto principal, contratos de domínio e transição | inventariar, priorizar DAG e evitar alteração de motores F06–F10 | registro canônico e QA3 |
| Segurança | A02 DevSecOps/IAM/TLS | auditoria de superfícies, testes negativos, HTTPS de loopback descartável | IAM real, MFA/segregação, revisão de segredos, HTTPS público e logs |
| Dados | A03 DBA, SQLite, backup, reversão | upgrade/downgrade, cópia consistente offline, restore integral em fixture | RPO/RTO acordados, volume e topologia representativos, ensaio completo |
| Release | A04 DevOps, cadeia de suprimentos | build determinístico do checkout e SHA-256 + SBOM simples | assinatura/atestado e promoção de pacote em ambiente aprovado |
| Qualidade | A05 Testes/API/browser | CI, smoke TLS, autenticação negativa, regressão F11 | homologação E2E por perfis, compatibilidade cliente e aceite |
| Operação | A06 SRE/observabilidade | alertas propostos, playbook e sonda local | monitoramento real, alarme testado e janela assistida |
| Elétrica | A07 Engenheiro eletricista sênior | matriz de aplicabilidade, inventário de lacunas e casos exigíveis | responsável habilitado, fontes/casos normativos, laudos e parecer assinados |
| Governança | A08 Gestor de mudanças | registro e decisão GO/NO-GO automática sobre evidências | identificador de mudança, titular, impacto, janela, custo, aceite institucional |

Os agentes são papéis de trabalho com responsabilidades separadas, não identidades humanas nem pareceres profissionais. Podem ser executados como rotinas/ciclos de revisão especializados pelo assistente. Apenas profissional habilitado aprova projetos e instalações reais.

## 2. Sequência determinística por dependências

| Onda | Tasks/Gates | Execução | Aceite de software ou condição de passagem |
|---|---|---|---|
| W0 — reconhecer | 12.01, G01 | congelar SHA F11, HEAD F12, inventário de dependências, superfícies API e limites; criar story/checkpoint | nenhum diff indevido, dados do candidato rastreáveis |
| W1 — proteção | 12.02, G03 | auditar identidade, exposição externa, TLS e secrets; ensaio TLS em loopback; negar persistência local em SIE_ENV=production | negações passam; identidade/HTTPS reais ficam pendentes até evidência externa |
| W2 — recuperação | 12.03, G04/G05 | restaurar pacote F11 multi-raiz com banco isolado; comparar SHA/contagens; testar upgrade e downgrade e rollback após erro | ensaio em fixture reprodutível, sem sobrescrever fonte nem alterar produção |
| W3 — cadeia de release | 12.05, G07 | criar tar determinístico de fontes permitidas + manifesto SHA256 + verificação de integridade; repetir e comparar byte-a-byte | dois builds equivalentes e checksum, sem secrets/arquivos locais |
| W4 — homologação limitada | 12.04/12.06, G06/G07 | CI com API, AIOX e Chromium herdados; smoke HTTPS/API em ambiente sintético; relatório de risco | passes no SHA exato; não declarar homologação representativa apenas pelo runner |
| W5 — autorização | 12.07, G02/G08 | montar checklist, registrar parecer QA3 e matriz elétrica; preparar pacote de decisão | `GO` apenas se evidência aplicável, responsável, janela e custos forem aprovados |
| W6 — rollout | 12.08, G09 | depois de W5 GO: backup consistente, versão canário, migração, smoke, alerta e rollback | logs de execução real, ID de mudança e rollback exercitado |
| W7 — operação | 12.09/12.10, G10 | janela assistida, métricas/alertas/tickets, manutenção normativa e revisão as-built | pós-deploy saudável; plano operativo e responsabilidade profissional |

## 3. Modo YOLO e precedência
1. A01 reconstrói estado sem pedir confirmações de decisões técnicas já aceitas.
2. A02–A06 executam tarefas seguras e de baixo impacto em branch F12, CI, fixtures e loopback, corrigindo testes falhos sem reduzir expectativas.
3. A07 audita limitações documentais, não inventa ART, habilitação elétrica, ensaio de campo ou parecer assinado.
4. A08 compara evidências com G01–G10; bloqueios `HUMAN_REQUIRED`/ `PENDENTE` não viram `DONE` por mera delegação do trabalho.
5. Para PROD, pré-requisito obrigatório é decisão formal com alvo específico, ambiente, custo/janela, rollback, responsável e QA. Sem isso, NÃO executar merge/deploy/migração/alteração de DNS, segredos ou dados externos.
6. Nenhuma ação de produção deve ser inferida a partir de nomes de projetos Supabase: os projetos visíveis ao conector estão associados a outras soluções, não ao SIE 2.0.

## 4. Arquitetura de evidências
- Origem de verdade: `docs/sie-orchestrator/ORCHESTRATOR_STATE.json`; preservar status F11 e gates anteriores.
- Relatório: `docs/implantacao-sie-2-0/F12/RELATORIO_EXECUCAO.md`.
- Provas W1–W4: `scripts/f12_release_gate.py`, `scripts/f12_bundle.py`, `scripts/f12_staging_smoke.py`, workflow F12 e seus logs; evidência de artefatos GitHub CI.
- G02/G08–G10: registros assinados, cópias verificáveis, laudo e pós-deploy somente se ocorrerem.
- QA: QA-01 arquitetura/release, QA-02 engenharia, QA-03 segurança/dados/UX. Três perspectivas da mesma LLM não são três auditorias humanas independentes.

## 5. Política de saída
- **PREPARAÇÃO VALIDADA:** testes W1–W4 passados; não significa GO.
- **F12 HUMAN_REQUIRED:** sem identidade/ambiente profissional de produção, autorização ou parecer; conservar bloqueio.
- **GO:** decisão documentada G01–G08 com responsáveis e evidências reais.
- **F12 DONE:** somente após G09/G10, pós-deploy comprovado e três pareceres QA aplicáveis aprovados no escopo real.
- Sem GO formal, terminar execução técnica com pendências explícitas; nunca declarar encerramento F00–F12 como versão liberada.

## 6. Recuperação e rollback
Se regressão de CI: identificar causa, corrigir branch, repetir gate no novo SHA. Se falha no ensaio de DB: descartar clone e restaurar cópia íntegra nova; não alterar dados originais. Se uma produção autorizada vier a falhar: congelar escritas, desabilitar versão nova, acionar responsáveis e restaurar conjuntamente DB + todas as raízes registradas; não executar automaticamente sem runbook e autorização aplicáveis.
