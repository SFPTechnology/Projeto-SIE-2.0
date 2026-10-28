# Story SIE-C-V201 — Migração do domínio elétrico (DEVELOPMENT)

**Entrada:** GB=PASS exclusivamente DEVELOPMENT, SHA `63805c03c7146103cdd67eca4da3e369a751d379`, branch B `feat/v201-bloco-b-auth-api`.
**Branch C:** `feat/v201-bloco-c-dominio-eletrico`. Escopo C01–C08 do plano executivo V2.0.

## Critérios de aceite
- [ ] C01 — inventário read-only e classificação de fonte legada (ausência somente se comprovada).
- [ ] C02 — matriz explícita de conversão e rejeições, sem proprietários presumidos.
- [ ] C03 — migrations aditivas, modelo elétrico relacional, constraints por projeto/revisão e RLS.
- [ ] C04 — catálogo e gateway normativo versionados; sem conformidade por default/flag.
- [ ] C05 — snapshot imutável, pipeline determinístico com hash, runs server-only, pendências técnicas explícitas.
- [ ] C06 — ETL de staging privado, idempotente, reversível, sem carga remota.
- [ ] C07 — relatório de reconciliação sintética/sem origem; não confundir com migração real.
- [ ] C08 — testes e contratos para D, SHA e CI verificados, GC verdadeiro.

## Restrições
SIE original somente leitura. Sem alterações na `main`, F12, Supabase remoto, Hostinger, DHT ou produção. A03/A04/B04/C03 pendentes remotamente; sem declaração de homologação elétrica. O perfil GB DEVELOPMENT não autoriza E02–E06.

## File list
- `docs/stories/story-SIE-C-V201-DOMINIO-ELETRICO.md`
- Atualizar a lista de arquivos e os critérios conforme evidência executada.

**Status:** IN_PROGRESS — implementação e QA pendentes.
