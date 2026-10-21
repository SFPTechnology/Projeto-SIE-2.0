# Identidade de produção e autorização
|Papel planejado|Escopo|Operações|
|---|---|---|
|owner|organização própria|administrar membros e projetos|
|editor|organização própria|criar e revisar|
|reader|organização própria|consultar|
|auditor|organização própria|histórico e trilha, sem mutação|

Produção: contas verificadas, membership (user_id,organization_id,role), projeto organization_id e owner_id, revisões subordinadas ao projeto. Tenant deriva da sessão validada, nunca de cabeçalho confiado. Negar por padrão SELECT/INSERT/UPDATE/DELETE sem membership; WITH CHECK também em inserção/atualização. Proibir mudança de organização e autor pelo cliente. Excluir logicamente com conflito otimista e trilha. Backup fora de acesso HTTP.
Cenários exigidos na implantação: A não lê/lista/edita histórico, ensaios ou backups de B; reader não escreve; editor não administra membership; conta revogada e token expirado falham; UUID alheio não revela existência. Testar políticas com contas reais de ensaio e PostgreSQL isolado. Não executados: identidade/RLS de produção ainda não implementadas.
Local: único principal LOCAL_OWNER, credencial no ambiente, comparação constante, opt-in; acesso externo 403, produção 503, token ausente/incorreto 401. Sem credenciais não há abertura de banco. X-Forwarded-For não concede acesso. Não há multiusuário local anunciado.
