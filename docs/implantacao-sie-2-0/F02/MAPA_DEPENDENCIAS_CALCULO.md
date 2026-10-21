# F02 — Dependências, snapshots e recuperação
Data:20/10/2026.

## Dependências implementadas

- Agregado inteiro: hierarquia espacial, cargas, topologia, dispositivos, cabos, segmentos/condições e revisão produzem SHA-256 canônico.
- Algoritmo: versão do adaptador + código efetivamente utilizado + catálogo de disjuntores em memória produzem identidade com SHA-256.
- Entrada: DTO legado completo, incluindo fatores/tabela/resistência declarados, possui hash próprio.
- Regra: versão declarada é comparada separadamente; não recebe homologação por ser informada.

A granularidade da invalidação é conservadora: qualquer alteração no agregado pode tornar o resultado STALE, inclusive uma alteração editorial. Não há cache invisível ou recálculo automático.

| Estado | Condição |
|---|---|
| INVALID | Projeto/circuito não pertence ao snapshot atual |
| STALE | Snapshot, revisão, algoritmo, regra ou entrada diverge |
| PENDING | Dependências correspondem, mas não há resultado |
| VALID | Dependências e integridade correspondem; sem homologação |

## Revisões imutáveis e documentos

Snapshot contém o texto JSON canônico por valor, identidade, revisão e hash; não retém referência mutável ao agregado. A revalidação confere hash, schema e identidade/revisão. Documento e CalculationRecord usam a mesma RevisionReference (projeto, revisão, hash), com recusa de divergência.

A gravação local usa o repositório SQLite já existente: esperado N, modelo N+1. Ela preserva os outros campos legados de dados, grava snapshot na nova revisão e mantém as revisões anteriores imutáveis. Alterações concorrentes geram409; referências de outro projeto ou revisão inadequada são recusadas. O token local não representa RBAC multiusuário.

## Adoção progressiva e rollback

1. Continuar operando contratos F01 sem alteração; rotas novas têm prefixo /modelo.
2. Validar agregado canônico e capturar snapshot. Para projeto existente, adotar explicitamente sua próxima revisão local, preservando os dados antigos.
3. Usar adaptador apenas no recorte compatível. Nenhum fator normativo ou conversão de unidades é inferido.
4. Se necessário retornar ao fluxo legado, deixar de chamar as novas rotas e consumir os dados/revisões legados preservados. Para recuperar arquivo SQLite, utilizar backup consistente e restauração já testados em P07; nunca sobrescrever o arquivo ativo silenciosamente.
5. O rollback de código é retorno à baseline da F01 em checkout isolado. Não é necessário desfazer DDL: nenhuma migração de produção ou alteração do esquema de persistência foi introduzida na F02.

Testes verificam resultado equivalente ao motor anterior, rejeição de incompatibilidades, preservação de dados/revisões, conflito otimista, autenticação local, troca de algoritmo/catálogo, referência de documento e ausência de mutação do histórico. O replay dos34casos F00 continua critério de regressão.
