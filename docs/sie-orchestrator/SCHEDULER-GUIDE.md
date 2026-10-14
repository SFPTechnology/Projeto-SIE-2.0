# Guia operacional — Escalonador SIE-AUTO-ORCHESTRATOR

## Finalidade
O escalonador do SIE é uma camada **determinística de planejamento** vinculada à story SIE-AUTO-011. Ele não substitui os componentes AIOX existentes (`MasterOrchestrator`, `RecoveryHandler` e `SessionState`). Ele valida o grafo de atividades, seleciona a fila elegível, registra transições e grava um estado local retomável.

**Importante:** esta ferramenta **não implementa código sozinha**, não invoca LLMs, não executa comandos de sistema, não acessa rede, não faz push, merge ou deploy, e não fornece aprovação normativa. A execução real continua dependente de ferramentas autorizadas e testes.

## Onde estão os arquivos

| Item | Caminho |
|---|---|
| Motor de dependências | `restructuring/apps/api/sie_api/scheduler.py` |
| Comandos do terminal | `restructuring/apps/api/sie_api/scheduler_cli.py` |
| Estado JSON verificável | `docs/sie-orchestrator/ORCHESTRATOR_STATE.json` |
| Quadro de status | `docs/sie-orchestrator/PROJECT_STATE.md` |
| Fila explicada | `docs/sie-orchestrator/EXECUTION_QUEUE.md` |
| Critérios e testes | `docs/sie-orchestrator/VALIDATION_MATRIX.md` |

## Preparação no Windows — primeira execução

1. Clone ou atualize a **branch de reestruturação**, sem alterar a `main`.
2. Abra PowerShell na pasta raiz do repositório.
3. Ative o Python e instale as dependências já descritas em `restructuring/README.md`.
4. Acesse a pasta da API:

```powershell
cd restructuring\apps\api
python -m sie_api.scheduler_cli --help
```

5. Trabalhe sobre **uma cópia local** do estado para não modificar por engano a versão rastreada pelo Git:

```powershell
Copy-Item "..\..\..\docs\sie-orchestrator\ORCHESTRATOR_STATE.json" ".\sie-state-local.json"
```

6. Consulte o quadro e a fila:

```powershell
python -m sie_api.scheduler_cli --state .\sie-state-local.json inspect
python -m sie_api.scheduler_cli --state .\sie-state-local.json queue
```

7. Para promover atividades `PENDING` que têm requisitos validados e predecessoras `DONE`, execute:

```powershell
python -m sie_api.scheduler_cli --state .\sie-state-local.json promote
```

8. Registre uma transição autorizada de atividade elegível (substitua o ID):

```powershell
python -m sie_api.scheduler_cli --state .\sie-state-local.json transition --id SIE-AUTO-004 --to RUNNING --reason "Story e dependencias revisadas"
```

O comando atualiza `revision` e acrescenta um evento com estado anterior, novo estado, motivo e data. Se as dependências não forem satisfeitas, ele retornará erro seguro.

## Entendendo os estados

| Estado | Interpretação |
|---|---|
| PENDING | Descoberta, sem execução iniciada |
| READY | Requisitos e dependências conferidos |
| RUNNING | Implementação sendo executada por um executor autorizado |
| IMPLEMENTED | Código criado, mas não completamente validado |
| VALIDATING | Testes e evidências em verificação |
| DONE | Todos os critérios de aceite registrados com `passed=true` e evidências; a veracidade das referências ainda requer conferência externa |
| FAILED | Execução ou teste falhou |
| BLOCKED | Impedimento técnico registrado |
| RECOVERING | Nova estratégia de recuperação em andamento |
| HUMAN_REQUIRED | Ação externa necessária para esta tarefa; independentes continuam elegíveis |

## Regras de segurança

- Uma atividade não entra em READY enquanto houver dependência obrigatória não DONE ou requisito não verificado.
- O motor recusa IDs repetidos, dependências inexistentes, ciclos, estados inválidos e transições proibidas.
- DONE exige critérios de aceite com campo `passed` verdadeiro e evidência não vazia. **Esse controle verifica estrutura e presença, não autentica a evidência**: conferir os links e os logs permanece obrigatório.
- Não alterar manualmente uma tarefa para DONE para contornar a máquina de estados.
- Alterações do JSON são gravadas com substituição de arquivo e revisão otimista. **Não há trava entre processos**: use um escritor por workspace e não compartilhe o arquivo entre máquinas durante gravação.
- O JSON é memória operacional; **nunca é** credencial de acesso nem documento de projeto normativo.

## Retomada após interrupção

Leia nesta ordem: `PROJECT_STATE.md`, `NEXT_ACTION.md`, `ORCHESTRATOR_STATE.json`, último SHA do PR e testes CI. Compare o estado do JSON com os commits e logs de fato. Se divergirem, registre o bloqueio e não classifique tarefas como DONE sem evidências.

## Limites do escopo e próxima integração

O AIOX possui executor de stories/epics e recuperação; a conexão automática entre a fila específica do SIE e os agentes AIOX **não está implementada nesta story**. Essa integração futura exigirá contrato de handoff, autoridade de agente, resultados assinados/reconciliados e regras de retomada para que a fila produza execução real com segurança.
