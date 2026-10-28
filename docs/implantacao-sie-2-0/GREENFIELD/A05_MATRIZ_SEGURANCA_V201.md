# A05 — Matriz owner-only / RLS / segredo / retenção

**Escopo:** GF02 instalada, desenvolvimento V2.0.1. Sem grants novos. `PROD=fozrymsidnaxmuvxxfhh`.

| Papel | SELECT | INSERT | UPDATE | DELETE |
|---|---|---|---|---|
| `anon` | nenhum dos 9 `sie_*` | nenhum | nenhum | nenhum |
| `authenticated` | 9 tabelas **sob RLS owner-only** | por colunas em projetos, revisões, ambientes, cargas, circuitos e links, **sob RLS** | somente `sie_projects.name`, sob RLS | nenhum |
| `service_role` | privilegiado | privilegiado conforme grants GF02 | `sie_projects` / `sie_artifacts` conforme grants | não presumir direitos efetivos; revogar/limitar se necessário |

**Controles:** toda operação privilegiada verifica titularidade no backend antes de ler/alterar projeto; jamais usar `raw_user_meta_data` ou `auth.jwt().user_metadata` para autorização; `service_role` apenas no servidor, sem log/HTML/bundle/ZIP; preferir menor privilégio; `auth.uid()` como fonte de identidade.

**Testes negativos de desenvolvimento:** A acessa projeto A; B recebe 404/403 para recursos A; usuário não autenticado não acessa projeto; B não pode associar carga/circuito entre projetos ou revisões; cliente não cria cálculos/artefatos/eventos do servidor; update de owner_id rejeitado. Testes simulados não equivalem a sessão A/B real.

**Risco residual:** nenhuma identidade em `auth.users` no checkpoint; testes reais A/B/Data API e verificação efetiva de `service_role` ficam pendentes de infraestrutura/integração e são gate de pré-produção (E02/E06).

**Dados e retenção:** classificar cadastro/artefato por projeto/titular; minimizar dados pessoais em logs; retenção, exclusão e backups sob política operacional a ratificar antes do GO. Excluir projeto operacional não apaga automaticamente backups/Storage; gerar solicitação controlada e trilha de auditoria.

**Ambientes:** DEV=branch Git e fixtures, TEST=opcional, STAGING=opcional no desenvolvimento, PROD=destino GF02. Não publicar dados reais como fixture.
