# F06 — Contrato implementado e limites

Data: 21/10/2026. Motor `SIE_DEMAND_V1`. Todos os exemplos numéricos novos são sintéticos.

## Operação

A partir da raiz, com dependências da API instaladas:

```bash
PYTHONPATH=restructuring/apps/api python -m sie_api.demand_cli restructuring/examples/f06_demanda_demo.json
```

API: `POST /api/v1/demanda/calcular`; comparação: `POST /api/v1/demanda/comparar` com `before` e `after`. Interface técnica: `demanda.html`, acessível pelo painel. Não depende da interface para executar.

Potências e conectividade pertencem ao agregado F02/F05. Não há cópia editável alternativa de conectividade em armazenamento: salvar cenário exige fingerprint igual à topologia persistida. Levantamento F04 continua preservado; **a transferência F04→F02 exige mapa bijetivo de UUIDs explícito**. Use POST `/api/v1/demanda/projetar-levantamento` com survey/topology/links, ou CLI `--survey levantamento.json --links mapa.json`. Retorna rascunho F05 e auditoria; salve pela rotina F05 autenticada com nova revisão. Não escolhe associação por nome. Quantidade é aplicada uma única vez, sem inferir categoria/regra; tensão/fases conflitantes são recusadas. S derivado de P/fp é arredondado a 24 casas com registro de precisão. Para estudar mudança de equipamento, primeiro atualizar a carga canônica F05 e salvar sua revisão.

Cenários têm UUID imutável, regras e entradas próprias e resultado histórico. PUT/GET `/api/v1/local/projetos/{id}/demanda` exige o token local existente; PUT exige revisão esperada. Histórico recebe `stale=true` quando topologia ou levantamento muda; não servir Ib histórico como atual. Comparação retorna memórias completas, hashes e indicador de mudança. Não altera a corrente canônica dos circuitos nem integra cálculo de dimensionamento definitivo.

## Matemática

P em W, Q em var, S em VA. Sem conversão tácita kW/kVA. P/Q geram S pela raiz de P²+Q² quando ambos existem. P e fp explícito podem gerar S; S e fp podem gerar P. O sinal de Q não é inferido. Potências incompatíveis geram pendência. Soma de S significa soma escalar dos VA individuais, explicitada na memória, e não módulo da soma complexa. Campo desconhecido conserva contador `missing`; soma parcial nunca é chamada de total conhecido para liberação de Ib.

Classificação exige categoria e critério explícitos separados do rule_id. Cada regra contém versão, fonte, edição, finalidade, condição, faixas e fatores. Cada carga registra evidência de condição. Faixas são [inferior, superior); última pode ser aberta. WHOLE_GROUP aplica fator único à potência aparente total do grupo. PROGRESSIVE soma blocos contíguos desde zero e registra fator efetivo, preservando as faixas originais na memória. Não usar estes modelos para uma expressão de equipamento diferente sem implementação e referência própria.

Escopos: TERMINAL_CIRCUIT (contrato padrão explícito na saída), BOARD ou SUPPLY. BOARD/SUPPLY exigem target_id no caminho de cada carga. Mesmo grupo em alvos distintos não mistura instalações/fontes. Cada parcela de carga é propagada exatamente uma vez a cada ancestral. Não há segundo fator em cascata. Regras de quadro/fonte não autorizam Ib dos ramos abaixo de seu alvo. FINAL_CIRCUIT recusa regra de quadro/fonte. ENTRANCE não publica Ib dos circuitos.

Ib monofásica: S/U; trifásica: S/(√3·U_FF), somente com declaração explícita de equilíbrio. Base da tensão validada por F02. Cálculo Decimal com 80 dígitos, memória da fórmula e hipóteses. A saída é estudo e traz `authoritative_for_sizing=false`; fonte/entrada possui Ib de estudo somente com source_connections explícito, tensão compatível e hipótese trifásica declarada. Ib para dimensionamento definitivo não foi homologada.

## Fonte e confiança

Cadastro de regras novo não aceita autodeclaração de VERIFIED como prova. SYNTHETIC_STUDY continua como ensaio. Agora, IDs reservados EDP V09 são resolvidos no catálogo confiável do servidor, com fonte e fatores por carga; ver VINCULACAO_FONTES.md. Regras VERIFIED arbitrárias enviadas pelo cliente continuam pendentes. O cliente não pode substituir coeficientes de IDs reservados. Não foi criado fator universal nem extraído coeficiente de texto derivado como regra verificada.

Para ENTRANCE, contexto exige distribuidora, localidade, tipologia, edição e confirmação de área; igualdade exata com escopo da regra. Essa compatibilidade é um bloqueio estrutural e não valida vigência ou aprovação da concessionária. Não aciona automaticamente enquadramento EDP.

Fontes encontradas: `Arquivos_Diversos/Norma_EDP/PT.DT.PDN.00068_V9.pdf`; matriz e inventário F01 indicam demanda não homologada. O aceite anterior de F01 foi preservado; ele não fornece os coeficientes/condições ausentes neste catálogo. O bloqueio inicial foi superado no incremento de vinculação: catálogo com fonte oficial conferida e casos independentes derivados do documento; detalhes em VINCULACAO_FONTES.md. Nenhuma nova aprovação ABNT ou EDP foi declarada.

## Retomada concreta

1. A ponte explícita F04→F02 está implementada e ensaiada. Manter identidade/quantidade na operação; resultados históricos ficam stale quando as entradas mudam.
2. Catálogo EDP V09 conectado com referências, coeficientes, modelos e exceções. Ampliações para outras edições/territórios exigem conferência própria; não adaptar a fonte ao algoritmo.
3. Após validação de fonte/regra, integrar somente o resultado vigente aos motores de dimensionamento. A corrente da fonte já existe para estudo; preservar bloqueios para desequilíbrio ou dados insuficientes.
4. A vinculação foi reavaliada por QA3; evidências de testes e CI atuais constam do relatório.

CLI adicional: `--compare outro-cenario.json`; `--database local.sqlite --expected-revision N` salva cenário em projeto com topologia já cadastrada. Não realiza conexão de produção.
