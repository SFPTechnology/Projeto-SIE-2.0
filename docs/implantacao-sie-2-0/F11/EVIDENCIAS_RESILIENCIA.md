# F11 — resiliência e desempenho local

**Escopo:** sondagem reproduzível em SQLite temporário, dados sintéticos, um processo Python 3.12 no executor local. Story AC-11.07. Não é capacidade de produção, benchmark de navegador, HTTP sob carga ou ensaio de instalação.

## Contrato local provisório de aceitação

Para o cenário sintético de até 900 KiB (abaixo do limite de 1 MiB do repositório), 64 leituras e 8–16 escritores simultâneos da **mesma revisão**, o alvo de engenharia para esta máquina é: p95 de leitura histórica até **250 ms**, criação até **500 ms**, grupo concorrente até **2 s**, exatamente um vencedor e os demais conflitos de revisão, sem perder histórico. Lock de SQLite com timeout configurado em 50 ms deve falhar sem escrever; conexão indisponível em loopback com timeout de 200 ms deve falhar sem alterar o banco; corrupção de versão histórica deve ser recusada. Estes são **limites locais provisórios**, não SLO de produção aceito pelo responsável.

## Procedimento e resultados observados

Comando a partir de `restructuring/apps/api`:

```sh
python -m pytest -q tests/test_f11_resilience.py
python -m sie_api.resilience_probe_f11 --payload-kib 512 --readers 64 --writers 8
python -m sie_api.resilience_probe_f11 --payload-kib 900 --readers 64 --writers 16
```

O teste de invariantes teve **5 passed em 0,24 s**. Cinco repetições independentes do primeiro cenário e uma do segundo:

| Cenário | Criação | Leitura p95 | Grupo concorrente | Lock | Transporte indisponível | Resultado |
|---|---:|---:|---:|---:|---:|---|
| 512 KiB, 64 leituras, 8 escritores; cinco execuções | 8,849–26,274 ms | 2,806–3,723 ms | 36,923–69,136 ms | 50,551–50,651 ms | 1,171–1,250 ms | 1 vencedor, 7 conflitos; revisão 2 preservada; corrupção recusada em todas |
| 900 KiB, 64 leituras, 16 escritores; uma execução | 13,337 ms | 5,046 ms | 92,015 ms | 50,658 ms | 1,222 ms | 1 vencedor, 15 conflitos; revisão 2 preservada; corrupção recusada |

O script `sie_api.resilience_probe_f11` imprime JSON com métricas e não persiste nada fora de um diretório temporário. O teste funcional evita limites temporais rígidos para não falhar por lentidão transitória de CI; o parecer compara medições reais com os alvos provisórios.

## Limites e riscos

- Concorrência testada: escritores de uma revisão em um único host/processo, via conexões SQLite separadas. Não cobre múltiplos processos em hosts distintos nem sistema de arquivos de rede.
- Tamanho: 900 KiB de texto sintético, não um projeto real com milhares de objetos. Dados acima de 1 MiB são rejeitados pelo contrato atual e têm teste legado.
- Lock: timeout forçado em conexão direta para verificar falha atômica; não representa o timeout de 5 s configurado no repositório durante uma carga real.
- Falha de rede: porta vinculada sem escuta em loopback, sem API/UX de retry. Não se inferem mensagens ou recuperação do navegador.
- Corrupção: adulteração da revisão histórica após remover seu gatilho em banco **descartável**; o hash rejeitou a leitura. Não mede backup/restore, coberto em ensaio distinto.
- P95 em 64 leituras e cinco repetições é uma sondagem, não distribuição estatística ou capacidade sustentada. Repetir no ambiente alvo e definir SLO de produção antes de qualquer publicação externa.
